"""Continue a native second-mission save through Caatinga and the third stone."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import snapshot
from check_second_habitat import key_items, party_health
from party_recovery import (apply_two_member_recovery_fixture,
                            assert_party_fully_recovered, party_identities)


def fight_caatinga_agent(emu, symbols, battle_shot=None, switch_handlers=None,
                         battle_stats=None):
    captured = False
    switches = 0
    for cycle in range(260):
        handler = emu.read(symbols["gBattlerControllerFuncs"], 32) & ~1
        if switch_handlers is not None and handler in switch_handlers:
            assert switches == 0, switches
            emu.send("run 128 12\nrun 0 30\n" + press_a(2, 180))
            switches += 1
            continue
        if handler == symbols["HandleInputChooseMove"]:
            assert emu.read(symbols["gMoveSelectionCursor"]) == 0
            if battle_shot is not None and not captured:
                emu.send(f"shot {battle_shot}")
                captured = True
        emu.send(press_a(1, 90))
        state = snapshot(emu, symbols)
        assert state["map"] == "3/2", ("left third habitat", state)
        if state["flags"] & 0x40:
            assert emu.read(symbols["gBattleOutcome"]) == 1, "expected B_OUTCOME_WON"
            if battle_stats is not None:
                battle_stats["mandatory_switches"] = switches
            return cycle + 1
    raise AssertionError("Caatinga agent battle did not finish")


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    second = json.loads((args.second_habitat_results / "results.json").read_text())
    assert second["rom_sha1"] == digest
    assert second["partner"] == args.partner
    source = args.second_habitat_results / "second-habitat.sav"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / "third-habitat.sav"
    shutil.copyfile(source, save)
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}

    emu = Emulator(args, "third-habitat", save, test_writes=args.recovery_fixture)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        initial = snapshot(emu, symbols)
        assert initial == second["continued"], (initial, second["continued"])
        identities = party_identities(emu, symbols)
        assert identities == second.get("party_identities", identities)
        assert key_items(emu, symbols).get(361) == key_items(emu, symbols).get(362) == 1
        assert 363 not in key_items(emu, symbols)
        fixture_before = None
        if args.recovery_fixture:
            fixture_before = apply_two_member_recovery_fixture(
                emu, symbols, add_second_member=False
            )

        # Step around the defeated Cerrado agent and take the provisional trail.
        emu.send("run 32 20\nrun 0 60\nrun 64 600\nrun 0 600")
        entered = snapshot(emu, symbols)
        assert entered["map"] == "3/2" and entered["position"] == [23, 9], entered
        emu.send(f"shot {args.output / 'caatinga-entry.ppm'}")

        emu.send(press_a(2, 180))
        cycles = fight_caatinga_agent(
            emu, symbols, args.output / "caatinga-battle.ppm"
        )
        for _ in range(10):
            if snapshot(emu, symbols)["flags"] & 0x80:
                break
            emu.send(press_a(1, 180))
        emu.send("run 0 300")
        emu.send(f"shot {args.output / 'drought-stone-message.ppm'}")
        for _ in range(8):
            if emu.read(symbols["sLockFieldControls"]) == 0:
                break
            emu.send("run 2 12\nrun 0 180")
        rewarded = snapshot(emu, symbols)
        assert rewarded["flags"] == 0xFF, rewarded
        items = key_items(emu, symbols)
        assert items.get(361) == items.get(362) == items.get(363) == 1, items
        healed = party_health(emu, symbols)
        assert healed and all(hp == max_hp and hp > 0 for hp, max_hp in healed), healed
        full_recovery = (assert_party_fully_recovered(emu, symbols)
                         if args.recovery_fixture else None)
        assert emu.read(symbols["sLockFieldControls"]) == 0
        assert party_identities(emu, symbols) == identities
        emu.send(f"shot {args.output / 'drought-stone.ppm'}")

        emu.send("run 8 12\nrun 0 60\n" + "run 128 12\nrun 0 20\n" * 3
                 + "run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\n"
                 + "run 1 12\nrun 0 600")
    finally:
        emu.close()

    emu = Emulator(args, "third-habitat-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == rewarded, (rewarded, continued)
        items_after = key_items(emu, symbols)
        assert items_after.get(361) == items_after.get(362) == items_after.get(363) == 1
        continued_recovery = (assert_party_fully_recovered(emu, symbols)
                              if args.recovery_fixture else None)
        continued_identities = party_identities(emu, symbols)
        assert continued_identities == identities
        emu.send(f"shot {args.output / 'continued.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = dict(
        rom_sha1=digest,
        result="PASS",
        source_save_sha256=source_hash,
        partner=args.partner,
        source_second_habitat="fresh second mission with ordinary save/Continue",
        test_writes=args.recovery_fixture,
        recovery_fixture_before=fixture_before,
        full_recovery=full_recovery,
        continued_recovery=continued_recovery,
        party_identities=continued_identities,
        initial=initial,
        entered=entered,
        battle_input_cycles=cycles,
        rewarded=rewarded,
        continued=continued,
        healed_party=healed,
        stones={"water": items_after[361], "roots": items_after[362],
                "drought": items_after[363]},
        scope=("Native second-mission save; Campo Cerrado trail transition; "
               "Caatinga battle, three unique key items, normal save and Continue. "
               "Uses provisional inherited map art and does not validate habitat four."
               + (" The opt-in recovery fixture changes only the two-member party's "
                  "condition to verify full-team HP/status/PP recovery."
                  if args.recovery_fixture else "")),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print("third habitat/battle/drought stone/save/Continue: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "second-habitat-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    parser.add_argument("--recovery-fixture", action="store_true")
    check(parser.parse_args())
