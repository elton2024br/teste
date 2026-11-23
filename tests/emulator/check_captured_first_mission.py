"""Continue a natural two-member capture through the first stone mission."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_capture import capsules
from check_defeat_recovery import dismiss, reach_control, snapshot
from check_intro import Emulator
from check_starters import press_a
from check_stone_revisit import walk_to
from party_recovery import assert_party_fully_recovered, party_identities


PARTNERS = {
    "capivagua": (1, 7, "CAPIVÁGUA"),
    "ararafogo": (2, 4, "ARARAFOGO"),
    "tatupedra": (0, 1, "TATUPEDRA"),
}


def fight_with_captured_partner(emu, symbols, switch_handlers):
    switches = 0
    for cycle in range(360):
        handler = emu.read(symbols["gBattlerControllerFuncs"], 32) & ~1
        if handler in switch_handlers:
            if switches == 0:
                # The cursor starts on the fainted leader; choose slot 2, then SHIFT.
                emu.send("run 128 12\nrun 0 30\n" + press_a(2, 180))
                switches = 1
            else:
                emu.send(press_a(1, 180))
            continue
        if handler == symbols["HandleInputChooseMove"]:
            cursor = emu.read(symbols["gMoveSelectionCursor"])
            assert cursor in (0, 1), cursor
            if cursor == 0:
                emu.send("run 16 12\nrun 0 20")
        emu.send(press_a(1, 90))
        current = snapshot(emu, symbols)
        assert current["map"] == "1/0", ("left first mission", current)
        if current["flags"] & 2:
            assert emu.read(symbols["gBattleOutcome"]) == 1, "expected B_OUTCOME_WON"
            dismiss(emu)
            return cycle + 1, switches
    raise AssertionError("two-member agent battle did not finish")


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    capture = json.loads((args.capture_results / "results.json").read_text())
    assert capture["rom_sha1"] == digest and capture["result"] == "PASS"
    assert not capture["synthetic_full_party"]
    assert capture["before_save"]["party"] == 2
    partner = capture["starter"]
    starter, starter_species, starter_name = PARTNERS[partner]
    expected_identities = capture["party_identities"]
    assert [mon["species"] for mon in expected_identities] == [starter_species, 1]
    assert [mon["nickname"] for mon in expected_identities] == [starter_name, "TATUPEDRA"]

    source = args.capture_results / "captured.sav"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / (partner + ".sav")
    shutil.copyfile(source, save)
    lines = [p for line in args.symbols.read_text().splitlines()
             if len(p := line.split()) == 3]
    symbols = {p[2]: int(p[0], 16) for p in lines}
    switch_handlers = {int(p[0], 16) for p in lines if p[2] == "WaitForMonSelection"}
    assert switch_handlers

    emu = Emulator(args, "captured-first-mission", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        loaded = snapshot(emu, symbols)
        assert loaded == capture["continued"], (loaded, capture["continued"])
        assert party_identities(emu, symbols) == expected_identities
        capsules_after_capture = capsules(emu, symbols)
        assert capsules_after_capture == capture["capsules_after"]

        # Route 1 grass -> south connection -> village central path -> forest control.
        emu.send("run 32 64\nrun 0 30")
        walk_to(emu, symbols, 128, "3/0", [11, 0])
        emu.send("run 128 240\nrun 0 30")
        assert snapshot(emu, symbols)["position"] == [11, 15]
        emu.send(press_a(6))
        dismiss(emu)
        caregiver_recovery = assert_party_fully_recovered(emu, symbols)
        assert party_identities(emu, symbols) == expected_identities
        emu.send("run 64 96\nrun 0 30\nrun 32 48\nrun 0 30")
        village = snapshot(emu, symbols)
        assert village["position"] == [8, 9], village
        initial = reach_control(emu, symbols)
        assert initial == dict(partner=1, flags=1, keyitem=0, party=2, starter=starter,
                               map="1/0", position=[12, 14]), initial
        assert party_identities(emu, symbols) == expected_identities

        emu.send(press_a(4))
        assert snapshot(emu, symbols) == initial, "control unlocked before victory"
        dismiss(emu)
        emu.send("run 32 16\nrun 0 30\nrun 32 4\nrun 0 30\n" + press_a(4, 300))
        cycles, switches = fight_with_captured_partner(emu, symbols, switch_handlers)
        victory = snapshot(emu, symbols)
        assert victory["flags"] == 3 and victory["party"] == 2, victory
        assert party_identities(emu, symbols) == expected_identities

        emu.send("run 16 16\nrun 0 30\nrun 64 4\nrun 0 30\n" + press_a(4))
        dismiss(emu)
        opened = snapshot(emu, symbols)
        assert opened["flags"] == 7 and opened["party"] == 2, opened
        emu.send("run 32 16\nrun 0 30\nrun 64 128\nrun 0 30")
        assert snapshot(emu, symbols)["position"] == [11, 6]
        emu.send(press_a(4))
        dismiss(emu)
        stone = snapshot(emu, symbols)
        assert stone["flags"] == 15 and stone["keyitem"] == 361, stone
        assert party_identities(emu, symbols) == expected_identities

        emu.send("run 128 700\nrun 0 90")
        returned = snapshot(emu, symbols)
        assert returned["map"] == "3/0" and returned["position"] == [11, 5], returned
        emu.send("run 128 64\nrun 0 30\nrun 32 48\nrun 0 30\nrun 64 4\nrun 0 30"
                 + "\n" + press_a(4))
        dismiss(emu)
        before = snapshot(emu, symbols)
        assert before == dict(partner=1, flags=15, keyitem=361, party=2, starter=starter,
                              map="3/0", position=[8, 9]), before
        before_identities = party_identities(emu, symbols)
        assert before_identities == expected_identities
        assert capsules(emu, symbols) == capsules_after_capture
        emu.send(f"shot {args.output / 'two-member-first-stone.ppm'}")
        emu.send("run 8 12\nrun 0 60\n" + "run 128 12\nrun 0 20\n" * 3
                 + "run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\n"
                 + "run 1 12\nrun 0 600")
    finally:
        emu.close()

    emu = Emulator(args, "captured-first-mission-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == before, (before, continued)
        continued_identities = party_identities(emu, symbols)
        assert continued_identities == expected_identities
        assert capsules(emu, symbols) == capsules_after_capture
        emu.send(f"shot {args.output / 'two-member-first-stone-continued.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    case = dict(
        partner=partner,
        result="PASS",
        battle_input_cycles=cycles,
        battle_switches=switches,
        initial=initial,
        victory=victory,
        opened=opened,
        stone=stone,
        before_save=before,
        continued=continued,
        party_identities=continued_identities,
        capsules=capsules_after_capture,
        caregiver_recovery=caregiver_recovery,
        save_bytes=save.stat().st_size,
    )
    report = dict(
        rom_sha1=digest,
        result="PASS",
        source_capture_sha256=source_hash,
        natural_capture=True,
        cases=[case],
        scope=("Native save after a natural Tatupedra capture; return through Route 1, "
               "first agent victory, control, water stone, village guide, normal save "
               "and Continue. Stable personality, OT, species and nickname checked for "
               "both party members; no memory writes or savestates."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(partner + " natural two-member first mission/save/Continue: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "capture-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    check(parser.parse_args())
