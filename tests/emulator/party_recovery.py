"""Party identity and opt-in full HP/status/PP fixture helpers."""


SUBSTRUCT_ORDERS = (
    (0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3), (0, 3, 1, 2),
    (0, 2, 3, 1), (0, 3, 2, 1), (1, 0, 2, 3), (1, 0, 3, 2),
    (2, 0, 1, 3), (3, 0, 1, 2), (2, 0, 3, 1), (3, 0, 2, 1),
    (1, 2, 0, 3), (1, 3, 0, 2), (2, 1, 0, 3), (3, 1, 0, 2),
    (2, 3, 0, 1), (3, 2, 0, 1), (1, 2, 3, 0), (1, 3, 2, 0),
    (2, 1, 3, 0), (3, 1, 2, 0), (2, 3, 1, 0), (3, 2, 1, 0),
)


def read_bytes(emu, address, size):
    assert address % 4 == size % 4 == 0
    return b"".join(emu.read(address + i, 32).to_bytes(4, "little")
                    for i in range(0, size, 4))


def _write_bytes(emu, address, raw):
    assert address % 4 == len(raw) % 4 == 0
    for offset in range(0, len(raw), 4):
        value = int.from_bytes(raw[offset:offset + 4], "little")
        emu.send(f"write32 {address + offset:08x} {value:08x}")


def _decrypt_secure(raw):
    personality = int.from_bytes(raw[0:4], "little")
    key = personality ^ int.from_bytes(raw[4:8], "little")
    secure = bytearray()
    for offset in range(32, 80, 4):
        word = int.from_bytes(raw[offset:offset + 4], "little") ^ key
        secure.extend(word.to_bytes(4, "little"))
    checksum = sum(int.from_bytes(secure[i:i + 2], "little")
                   for i in range(0, 48, 2)) & 0xFFFF
    assert checksum == int.from_bytes(raw[28:30], "little")
    return secure


def _encrypt_secure(raw, secure):
    personality = int.from_bytes(raw[0:4], "little")
    key = personality ^ int.from_bytes(raw[4:8], "little")
    checksum = sum(int.from_bytes(secure[i:i + 2], "little")
                   for i in range(0, 48, 2)) & 0xFFFF
    raw[28:30] = checksum.to_bytes(2, "little")
    for offset in range(0, 48, 4):
        word = int.from_bytes(secure[offset:offset + 4], "little") ^ key
        raw[32 + offset:36 + offset] = word.to_bytes(4, "little")


def _moves_offset(raw):
    personality = int.from_bytes(raw[0:4], "little")
    # Each tuple maps logical substruct type -> physical encrypted slot.
    return SUBSTRUCT_ORDERS[personality % 24][1] * 12


def party_identities(emu, symbols):
    count = emu.read(symbols["gPlayerPartyCount"])
    base = symbols["gPlayerParty"]
    result = []
    for slot in range(count):
        raw = bytearray(read_bytes(emu, base + slot * 100, 100))
        personality = int.from_bytes(raw[0:4], "little")
        secure = _decrypt_secure(raw)
        growth_offset = SUBSTRUCT_ORDERS[personality % 24][0] * 12
        glyphs = list(raw[8:18])
        assert 0xFF in glyphs, glyphs
        glyphs = glyphs[:glyphs.index(0xFF)]
        assert all(0xBB <= glyph <= 0xD4 or glyph == 0x02 for glyph in glyphs), glyphs
        nickname = "".join("Á" if glyph == 0x02
                           else chr(glyph - 0xBB + ord("A")) for glyph in glyphs)
        result.append({
            "slot": slot,
            "personality": personality,
            "ot_id": int.from_bytes(raw[4:8], "little"),
            "species": int.from_bytes(
                secure[growth_offset:growth_offset + 2], "little"
            ),
            "nickname": nickname,
        })
    return result


def _max_pp(emu, symbols, move, bonus):
    # agbcc pads this nine-byte C struct to a twelve-byte array stride.
    base = emu.read(symbols["gBattleMoves"] + move * 12 + 4)
    return base + (base * 20 * bonus // 100)


def party_recovery_state(emu, symbols):
    count = emu.read(symbols["gPlayerPartyCount"])
    base = symbols["gPlayerParty"]
    result = []
    for slot in range(count):
        raw = bytearray(read_bytes(emu, base + slot * 100, 100))
        secure = _decrypt_secure(raw)
        moves_offset = _moves_offset(raw)
        growth_offset = SUBSTRUCT_ORDERS[int.from_bytes(raw[0:4], "little") % 24][0] * 12
        pp_bonuses = secure[growth_offset + 8]
        moves = [int.from_bytes(secure[moves_offset + i * 2:moves_offset + i * 2 + 2],
                                "little") for i in range(4)]
        pp = list(secure[moves_offset + 8:moves_offset + 12])
        maximum_pp = [_max_pp(emu, symbols, move, (pp_bonuses >> (i * 2)) & 3)
                      if move else 0 for i, move in enumerate(moves)]
        result.append({
            "slot": slot,
            "hp": int.from_bytes(raw[86:88], "little"),
            "max_hp": int.from_bytes(raw[88:90], "little"),
            "status": int.from_bytes(raw[80:84], "little"),
            "moves": moves,
            "pp": pp,
            "max_pp": maximum_pp,
        })
    return result


def apply_two_member_recovery_fixture(emu, symbols, add_second_member):
    """Prepare only party size/condition; gameplay still decides every battle."""
    base = symbols["gPlayerParty"]
    count_address = symbols["gPlayerPartyCount"]
    count = emu.read(count_address)
    if add_second_member:
        assert count == 1
        lead = read_bytes(emu, base, 100)
        _write_bytes(emu, base + 100, lead)
        aligned = count_address & ~3
        shift = (count_address & 3) * 8
        value = (emu.read(aligned, 32) & ~(0xFF << shift)) | (2 << shift)
        emu.send(f"write32 {aligned:08x} {value:08x}")
    else:
        assert count == 2

    for slot in range(2):
        address = base + slot * 100
        raw = bytearray(read_bytes(emu, address, 100))
        max_hp = int.from_bytes(raw[88:90], "little")
        assert max_hp > 1
        raw[86:88] = (max_hp - 1).to_bytes(2, "little")
        raw[80:84] = (8 if slot == 1 else 0).to_bytes(4, "little")  # poison
        secure = _decrypt_secure(raw)
        moves_offset = _moves_offset(raw)
        for move_slot in range(4):
            move = int.from_bytes(
                secure[moves_offset + move_slot * 2:moves_offset + move_slot * 2 + 2],
                "little",
            )
            if move and (slot == 1 or move_slot > 0):
                secure[moves_offset + 8 + move_slot] = 1
        _encrypt_secure(raw, secure)
        _write_bytes(emu, address, raw)

    state = party_recovery_state(emu, symbols)
    assert len(state) == 2
    assert all(mon["hp"] == mon["max_hp"] - 1 for mon in state)
    assert state[0]["status"] == 0 and state[1]["status"] == 8
    assert any(pp == 1 and maximum > 1
               for mon in state for pp, maximum in zip(mon["pp"], mon["max_pp"]))
    return state


def assert_party_fully_recovered(emu, symbols):
    state = party_recovery_state(emu, symbols)
    assert len(state) == 2, state
    for mon in state:
        assert mon["hp"] == mon["max_hp"] and mon["hp"] > 0, mon
        assert mon["status"] == 0, mon
        assert mon["pp"] == mon["max_pp"], mon
    return state
