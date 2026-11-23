"""Final-boss defeat fixture, recovery, native Continue and successful retry."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import snapshot
from check_second_habitat import key_items, party_health
from check_campaign_ending import campaign_flag_bytes, fight_tio_sam
from party_recovery import (assert_party_fully_recovered, party_identities,
                            party_recovery_state)


def current_hp(emu, symbols, slot=0):
    mon = symbols["gPlayerParty"] + slot * 100
    return (emu.read(mon + 0x54, 32) >> 16,
            emu.read(mon + 0x58, 32) & 0xFFFF)


def set_hp_fixture(emu, symbols, all_party=False):
    count = emu.read(symbols["gPlayerPartyCount"])
    assert count == (2 if all_party else 1), count
    maximum_hp = []
    for slot in range(count):
        address = symbols["gPlayerParty"] + slot * 100 + 0x54
        hp, max_hp = current_hp(emu, symbols, slot)
        assert hp == max_hp and max_hp > 1, (slot, hp, max_hp)
        word = emu.read(address, 32)
        emu.send(f"write32 {address:08x} {(word & 0xFFFF) | (1 << 16):08x}")
        assert current_hp(emu, symbols, slot) == (1, max_hp)
        maximum_hp.append(max_hp)
    return maximum_hp


def lose_from_hp_fixture(emu, symbols, switch_handlers):
    switches = 0
    for cycle in range(300):
        handler = emu.read(symbols["gBattlerControllerFuncs"], 32) & ~1
        if handler in switch_handlers:
            assert switches == 0, switches
            # The cursor starts on the fainted leader; choose slot 2, then SHIFT.
            emu.send("run 128 12\nrun 0 30\n" + press_a(2, 180))
            switches += 1
            continue
        if handler == symbols["HandleInputChooseMove"]:
            assert emu.read(symbols["gMoveSelectionCursor"]) == 0
        emu.send(press_a(1, 150))
        state = snapshot(emu, symbols)
        flags = campaign_flag_bytes(emu, symbols)
        assert not flags[3] & 0x06, ("ending granted before victory", flags)
        if state["map"] == "4/0":
            assert emu.read(symbols["gBattleOutcome"]) == 2, "expected B_OUTCOME_LOST"
            return cycle + 1, switches
        assert state["map"] == "3/3", ("unexpected map during battle", state)
    raise AssertionError("HP fixture did not reach a normal defeat")


def finish_recovery(emu, symbols, output):
    emu.send("run 0 300")
    for page in range(40):
        emu.send(f"shot {output / ('recovery-' + str(page) + '.ppm')}")
        if (emu.read(symbols["sGlobalScriptContextStatus"]) == 2
                and emu.read(symbols["sLockFieldControls"]) == 0
                and emu.read(symbols["gMain"] + 4, 32) & ~1 == symbols["CB2_Overworld"]):
            return
        emu.send(press_a(1, 300))
    raise AssertionError("recovery dialogue did not finish")


def save_from_house(emu):
    emu.send("run 8 12\nrun 0 60\n" + "run 128 12\nrun 0 20\n" * 3
             + "run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\n"
             + "run 1 12\nrun 0 600")


def return_to_rare_lands(emu, symbols):
    # House -> village.
    emu.send("run 128 32\nrun 0 30\nrun 32 64\nrun 0 30\n"
             "run 128 48\nrun 0 180\nrun 128 16\nrun 0 20\n"
             "run 16 32\nrun 0 20\nrun 64 4\nrun 0 30")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/0" and state["position"] == [8, 9], state

    # Village -> Floresta Amazônica -> Campo Cerrado checkpoint.
    emu.send("run 16 48\nrun 0 30\nrun 64 700\nrun 0 30\n"
             "run 128 32\nrun 0 30\nrun 16 16\nrun 0 30\n"
             "run 64 500\nrun 0 60\nrun 32 16\nrun 0 30\n"
             "run 64 340\nrun 0 120")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/20" and state["position"] == [11, 71], state

    # Campo Cerrado -> Caatinga -> Mata Atlântica -> Pantanal -> Terras Raras.
    emu.send("run 32 20\nrun 0 60\nrun 64 600\nrun 0 600")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/2" and state["position"] == [23, 9], state
    for expected in ("3/21", "3/22", "3/3"):
        emu.send("run 16 20\nrun 0 600")
        state = snapshot(emu, symbols)
        assert state["map"] == expected and state["position"] == [5, 9], state


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    fifth = json.loads((args.fifth_habitat_results / "results.json").read_text())
    assert fifth["rom_sha1"] == digest and fifth["partner"] == args.partner
    source = args.fifth_habitat_results / "fifth-habitat.sav"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / "final-defeat.sav"
    shutil.copyfile(source, save)
    lines = [p for line in args.symbols.read_text().splitlines()
             if len(p := line.split()) == 3]
    symbols = {p[2]: int(p[0], 16) for p in lines}
    switch_handlers = {int(p[0], 16) for p in lines if p[2] == "WaitForMonSelection"}
    assert switch_handlers

    emu = Emulator(args, "campaign-final-defeat-fixture", save, test_writes=True)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200\n"
                 "run 16 20\nrun 0 600\nrun 64 12\nrun 0 60")
        entered = snapshot(emu, symbols)
        assert entered["map"] == "3/3" and entered["position"] == [5, 9], entered
        initial_flags = campaign_flag_bytes(emu, symbols)
        initial_items = key_items(emu, symbols)
        assert initial_flags == (0xFF, 0x00, 0xE0, 0x01), initial_flags
        assert all(initial_items.get(item) == 1 for item in range(361, 366))
        identities = party_identities(emu, symbols)
        assert identities == fifth.get("party_identities", identities)
        assert len(identities) == (2 if args.all_party_hp_fixture else 1), identities
        initial_recovery = party_recovery_state(emu, symbols)
        original_max_hp = set_hp_fixture(emu, symbols, args.all_party_hp_fixture)
        assert party_identities(emu, symbols) == identities
        emu.send(f"shot {args.output / 'hp-fixture-before-battle.ppm'}")

        emu.send(press_a(2, 180))
        loss_cycles, loss_switches = lose_from_hp_fixture(
            emu, symbols, switch_handlers
        )
        finish_recovery(emu, symbols, args.output)
        recovered = snapshot(emu, symbols)
        recovered_flags = campaign_flag_bytes(emu, symbols)
        recovered_items = key_items(emu, symbols)
        recovered_health = party_health(emu, symbols)
        assert recovered["map"] == "4/0" and recovered["position"] == [8, 5], recovered
        assert recovered_flags == initial_flags, (initial_flags, recovered_flags)
        assert recovered_items == initial_items
        assert recovered_health == [[hp, hp] for hp in original_max_hp], recovered_health
        if args.all_party_hp_fixture:
            recovered_recovery = assert_party_fully_recovered(emu, symbols)
        else:
            recovered_recovery = party_recovery_state(emu, symbols)
        assert party_identities(emu, symbols) == identities
        emu.send(f"shot {args.output / 'recovered-after-tio-sam.ppm'}")
        save_from_house(emu)
    finally:
        emu.close()

    # Reopen with writes disabled. The rest of the scenario is normal gameplay.
    emu = Emulator(args, "campaign-final-defeat-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == recovered, (recovered, continued)
        assert campaign_flag_bytes(emu, symbols) == recovered_flags
        assert key_items(emu, symbols) == recovered_items
        assert party_identities(emu, symbols) == identities
        if args.all_party_hp_fixture:
            assert_party_fully_recovered(emu, symbols)
        emu.send(f"shot {args.output / 'continued-after-defeat.ppm'}")

        return_to_rare_lands(emu, symbols)
        emu.send("run 64 12\nrun 0 60")
        emu.send(press_a(2, 180))
        win_cycles = fight_tio_sam(emu, symbols)
        for _ in range(14):
            if campaign_flag_bytes(emu, symbols)[3] & 0x04:
                break
            emu.send(press_a(1, 180))
        emu.send("run 0 300")
        final_flags = campaign_flag_bytes(emu, symbols)
        final_items = key_items(emu, symbols)
        assert final_flags == (0xFF, 0x00, 0xE0, 0x07), final_flags
        assert all(final_items.get(item) == 1 for item in range(361, 366))
        assert party_identities(emu, symbols) == identities
        emu.send(f"shot {args.output / 'completed-after-retry.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = dict(
        rom_sha1=digest,
        result="PASS",
        partner=args.partner,
        fixture_writes=True,
        fixture=("all party members current HP set to 1"
                 if args.all_party_hp_fixture
                 else "party slot 0 current HP set to 1"),
        fixture_scope="no flags, items, identities or outcomes written",
        battle_outcome_loss=2,
        loss_input_cycles=loss_cycles,
        mandatory_switches=loss_switches,
        party_identities=identities,
        initial_party_recovery=initial_recovery,
        recovered=recovered,
        recovered_flag_bytes=list(recovered_flags),
        recovered_party_health=recovered_health,
        recovered_party_condition=recovered_recovery,
        five_stones_preserved_after_loss=True,
        normal_save_continue=True,
        continued=continued,
        returned_through_all_habitats=True,
        win_input_cycles=win_cycles,
        final_flag_bytes=list(final_flags),
        campaign_completed_after_retry=True,
        source_save_preserved=True,
        scope=("Artificial HP=1 fixture applied to "
               + ("both members" if args.all_party_hp_fixture else "the lead member")
               + "; normal final-boss defeat, home recovery, "
               "five stones and pre-ending flags preserved, ordinary save/Continue with "
               "writes disabled, stable party identities, return through the cleared "
               "campaign and normal victory. "
               "Not evidence of naturally accumulated battle damage."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(args.partner + " final defeat fixture/recovery/Continue/retry: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "fifth-habitat-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    parser.add_argument("--all-party-hp-fixture", action="store_true",
                        help="require two members and set current HP=1 on both")
    check(parser.parse_args())
