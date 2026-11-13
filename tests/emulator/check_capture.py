"""Wild capture into party or a synthetic full-party PC case, with save/Continue."""
import argparse
import hashlib
import json
from pathlib import Path

from check_intro import Emulator
from check_starters import bootstrap, press_a
from check_defeat_recovery import dismiss, snapshot
from check_stone_revisit import walk_to


def read_bytes(emu, address, size):
    assert address % 4 == size % 4 == 0
    return b''.join(emu.read(address + i, 32).to_bytes(4, 'little') for i in range(0, size, 4))


def full_party_fixture(emu, symbols):
    """Clone the valid starter into the five spare slots, then set count=6."""
    base = symbols['gPlayerParty']
    original = read_bytes(emu, base, 100)
    for slot in range(1, 6):
        for offset in range(0, 100, 4):
            word = int.from_bytes(original[offset:offset + 4], 'little')
            emu.send(f'write32 {base + slot * 100 + offset:08x} {word:08x}')
    address = symbols['gPlayerPartyCount']
    shift = (address & 3) * 8
    aligned = address & ~3
    word = (emu.read(aligned, 32) & ~(255 << shift)) | (6 << shift)
    emu.send(f'write32 {aligned:08x} {word:08x}')
    assert emu.read(address) == 6
    return original


def assert_party_preserved(emu, symbols, original):
    base = symbols['gPlayerParty']
    assert emu.read(symbols['gPlayerPartyCount']) == 6
    lead = read_bytes(emu, base, 100)
    assert lead[:28] == original[:28], 'lead identity changed'
    secure, growth = box_secure_data(lead[:80])
    assert int.from_bytes(secure[growth:growth + 2], 'little') == 7, 'lead species changed'
    for slot in range(1, 6):
        assert read_bytes(emu, base + slot * 100, 100) == original, ('party slot changed', slot)


def box_secure_data(raw):
    assert len(raw) == 80
    assert not raw[19] & 5, 'bad egg/egg flags'
    personality = int.from_bytes(raw[:4], 'little')
    key = personality ^ int.from_bytes(raw[4:8], 'little')
    secure = b''.join((int.from_bytes(raw[i:i + 4], 'little') ^ key).to_bytes(4, 'little')
                      for i in range(32, 80, 4))
    checksum = sum(int.from_bytes(secure[i:i + 2], 'little') for i in range(0, 48, 2)) & 65535
    assert checksum == int.from_bytes(raw[28:30], 'little'), 'PC checksum invalid'
    # Growth-substructure positions from GetSubstruct in the pinned pokemon.c.
    growth = [0,0,0,0,0,0,1,1,2,3,2,3,1,1,2,3,2,3,1,1,2,3,2,3][personality % 24] * 12
    return secure, growth


def pc_capture(emu, symbols, empty=False):
    # Pinned PokemonStorage alignment: box array starts at +4, 14 x 30 x 80 bytes.
    base = emu.read(symbols['gPokemonStoragePtr'], 32)
    assert 0x02000000 <= base <= 0x02040000 - 0x83D0, base
    occupied = [i for i in range(420) if emu.read(base + 4 + i * 80 + 19) & 2]
    if empty:
        assert occupied == [], occupied
        return None
    assert occupied == [0], ('expected exactly the first PC slot', occupied)
    raw = read_bytes(emu, base + 4, 80)
    secure, growth = box_secure_data(raw)
    name = list(raw[8:18]); name = name[:name.index(255)]
    assert all(0xBB <= c <= 0xD4 for c in name), name
    return dict(box=0, slot=0, species=int.from_bytes(secure[growth:growth + 2], 'little'),
                nickname=''.join(chr(c - 0xBB + ord('A')) for c in name),
                experience=int.from_bytes(secure[growth + 4:growth + 8], 'little'), checksum_valid=True)


def capsules(emu, symbols):
    block1 = emu.read(symbols['gSaveBlock1Ptr'], 32)
    block2 = emu.read(symbols['gSaveBlock2Ptr'], 32)
    key = emu.read(block2 + 0xF20, 32) & 65535
    # SaveBlock1 Poke Ball pocket: 13 ItemSlots, ITEM_POKE_BALL = 4.
    slots = [emu.read(block1 + 0x430 + i * 4, 32) for i in range(13)]
    return sum((slot >> 16) ^ key for slot in slots if (slot & 65535) == 4)


def caught_identity(emu, symbols):
    # Pokemon size 100; nickname and level are unencrypted fields.
    mon = symbols['gPlayerParty'] + 100
    glyphs = [emu.read(mon + 8 + i) for i in range(11)]
    assert 0xFF in glyphs, glyphs
    name = glyphs[:glyphs.index(0xFF)]
    assert all(0xBB <= c <= 0xD4 for c in name), name
    return dict(nickname=''.join(chr(c - 0xBB + ord('A')) for c in name),
                level=emu.read(mon + 0x54))


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    lines = [p for line in args.symbols.read_text().splitlines() if len(p := line.split()) == 3]
    symbols = {p[2]: int(p[0], 16) for p in lines}
    # Static action-handler names repeat in the ELF; examine player battler 0.
    actions = {int(p[0], 16) for p in lines if p[2] == 'HandleInputChooseAction'}
    assert actions
    save = args.output / 'captured.sav'
    emu = Emulator(args, 'capture', save, test_writes=args.full_party_fixture)
    try:
        emu.send(bootstrap() + press_a(12))  # Capivagua, including five capsules.
        dismiss(emu)
        initial = snapshot(emu, symbols)
        assert initial == dict(partner=1, flags=1, keyitem=0, party=1, starter=1,
                               map='3/0', position=[8, 9]), initial
        before_capsules = capsules(emu, symbols)
        assert before_capsules == 5, before_capsules
        expected_party = 6 if args.full_party_fixture else 2
        if args.full_party_fixture:
            pc_capture(emu, symbols, empty=True)
            original = full_party_fixture(emu, symbols)
            assert_party_preserved(emu, symbols, original)
        emu.send('run 16 48\nrun 0 30')
        walk_to(emu, symbols, 64, '3/19', [11, 16])
        emu.send('run 16 64\nrun 0 60')  # Grass at x=15, y=13..16.
        for step in range(80):
            emu.send(f'run {64 if step % 2 == 0 else 128} 32\nrun 0 180')
            if emu.read(symbols['gMain'] + 4, 32) & ~1 == symbols['BattleMainCB2']:
                break
        else:
            raise AssertionError('no natural encounter within 80 walking cycles')
        emu.send('run 0 300')
        assert not emu.read(symbols['gBattleTypeFlags'], 32) & 8, 'trainer battle'
        enemy = symbols['gBattleMons'] + 88
        # The recorded encounter is Tatupedra. Read enemy party before battle
        # initialization finishes copying stats into BattlePokemon.
        wild_level = emu.read(symbols['gEnemyParty'] + 0x54)  # level (unencrypted)
        assert wild_level == 3, ('expected level-3 encounter', wild_level)
        for cycle in range(160):
            hp = emu.read(enemy + 0x28, 32) & 65535
            handler = emu.read(symbols['gBattlerControllerFuncs'], 32) & ~1
            if handler in actions:
                assert hp > 0, 'wild creature fainted'
                if hp <= 6:
                    break
            emu.send(press_a(1, 90))  # Fight/Tackle and ordinary dialogue.
        else:
            raise AssertionError('could not weaken wild creature')
        species = emu.read(enemy, 32) & 65535
        assert species == 1 and hp == 4, (species, hp)
        emu.send(f'shot {args.output / "weakened.ppm"}')
        emu.send('run 16 12\nrun 0 30\n' + press_a(1, 180))  # BAG.
        emu.send('run 16 12\nrun 0 90\nrun 16 12\nrun 0 90')  # Ball pocket.
        for attempt in range(5):
            if attempt:
                emu.send(press_a(1, 180))  # BAG stays selected; ball pocket remembered.
            emu.send('run 0 60')
            emu.send(press_a(2, 180))  # Select ball, USE.
            for _ in range(80):
                emu.send('run 2 12\nrun 0 120')  # Advance and decline nickname.
                current = snapshot(emu, symbols)
                handler = emu.read(symbols['gBattlerControllerFuncs'], 32) & ~1
                field = emu.read(symbols['gMain'] + 4, 32) & ~1 == symbols['CB2_Overworld']
                outcome = emu.read(symbols['gBattleOutcome'])
                if current['party'] == expected_party and outcome == 7 and field:
                    break
                if outcome != 7 and handler in actions:
                    break  # Escaped ball; retry without inventing a success.
            else:
                raise AssertionError('throw did not return to a controllable state')
            if current['party'] == expected_party and outcome == 7 and field:
                break
        else:
            raise AssertionError('no capture with the five granted capsules')
        assert emu.read(symbols['gBattleOutcome']) == 7, 'expected B_OUTCOME_CAUGHT'
        after_capsules = capsules(emu, symbols)
        assert after_capsules == before_capsules - (attempt + 1), after_capsules
        if args.full_party_fixture:
            caught = pc_capture(emu, symbols)
            assert caught == dict(box=0, slot=0, species=1, nickname='TATUPEDRA', experience=27,
                                  checksum_valid=True), caught
            assert_party_preserved(emu, symbols, original)
        else:
            caught = caught_identity(emu, symbols)
            assert caught == dict(nickname='TATUPEDRA', level=3), caught
        before = snapshot(emu, symbols)
        assert before == dict(partner=1, flags=1, keyitem=0, party=expected_party, starter=1,
                              map='3/19', position=[15, 14]), before
        emu.send(f'shot {args.output / "caught.ppm"}')
        emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                 + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 600\n')
    finally:
        emu.close()
    assert save.stat().st_size in (131072, 131088), 'invalid native save size'
    emu = Emulator(args, 'continue-capture', save)
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                 'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
        continued = snapshot(emu, symbols)
        assert continued == before, (before, continued)
        if args.full_party_fixture:
            assert pc_capture(emu, symbols) == caught
            assert_party_preserved(emu, symbols, original)
        else:
            assert caught_identity(emu, symbols) == caught
        assert capsules(emu, symbols) == after_capsules
        emu.send(f'shot {args.output / "continued.ppm"}')
    finally:
        emu.close()
    report = dict(rom_sha1=hashlib.sha1(args.rom.read_bytes()).hexdigest(), result='PASS',
                  starter='capivagua', encounter_cycles=step + 1, wild_species=species,
                  wild_hp_before_throw=hp, caught=caught, outcome=7, throws=attempt + 1,
                  capsules_before=before_capsules, capsules_after=after_capsules,
                  before_save=before, continued=continued, save_bytes=save.stat().st_size,
                  synthetic_full_party=args.full_party_fixture,
                  scope=('Artificial full party cloned from the valid starter before a natural encounter; '
                         'normal capture into PC, checksum/identity, six party slots preserved and '
                         'ordinary save/Continue. No natural acquisition of six creatures, PC UI '
                         'retrieval, full PC or catch-rate statistics.' if args.full_party_fixture else
                        'One recorded natural Tatupedra capture with normal inputs, capsule '
                        'consumption and ordinary save/Continue. No catch-rate statistics, '
                        'full party/PC, other wild species or inventory-full cases.'))
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print('capture/capsule consumption/save/Continue: PASS', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--full-party-fixture', action='store_true')
    check(parser.parse_args())
