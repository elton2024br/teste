"""Continue a five-stone save through Terras Raras and the sanctuary ending."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import snapshot
from check_second_habitat import key_items, party_health
from party_recovery import party_identities


def campaign_flag_bytes(emu, symbols):
    block1 = emu.read(symbols["gSaveBlock1Ptr"], 32)
    return tuple(emu.read(block1 + offset) for offset in (0xF75, 0xF76, 0xF77, 0xF78))


def fight_tio_sam(emu, symbols, battle_shot=None):
    captured = False
    for cycle in range(260):
        handler = emu.read(symbols["gBattlerControllerFuncs"], 32) & ~1
        if handler == symbols["HandleInputChooseMove"]:
            assert emu.read(symbols["gMoveSelectionCursor"]) == 0
            if battle_shot is not None and not captured:
                emu.send(f"shot {battle_shot}")
                captured = True
        emu.send(press_a(1, 90))
        state = snapshot(emu, symbols)
        assert state["map"] == "3/3", ("left Terras Raras", state)
        if campaign_flag_bytes(emu, symbols)[3] & 0x02:
            assert emu.read(symbols["gBattleOutcome"]) == 1, "expected B_OUTCOME_WON"
            return cycle + 1
    raise AssertionError("Tio Sam battle did not finish")


def inspect_marker(emu, symbols, direction, output):
    before = snapshot(emu, symbols)
    emu.send(f"run {direction} 4\nrun 0 30\nrun 1 12\nrun 0 300")
    assert snapshot(emu, symbols)["position"] == before["position"]
    assert emu.read(symbols["sLockFieldControls"]) != 0
    emu.send(f"shot {output}")
    for _ in range(8):
        if emu.read(symbols["sLockFieldControls"]) == 0:
            break
        emu.send("run 2 12\nrun 0 180")
    else:
        raise AssertionError("rare-stone marker did not release controls")


def inspect_sanctuary(emu, symbols, output):
    before = snapshot(emu, symbols)
    assert before["position"] == [5, 9], before
    emu.send("run 128 12\nrun 0 20\nrun 64 12\nrun 0 20\n"
             "run 1 12\nrun 0 300")
    assert snapshot(emu, symbols)["position"] == before["position"]
    assert emu.read(symbols["sLockFieldControls"]) != 0
    emu.send(f"shot {output}")
    for _ in range(12):
        if emu.read(symbols["sLockFieldControls"]) == 0:
            break
        emu.send("run 2 12\nrun 0 180")
    else:
        raise AssertionError("rare sanctuary did not release controls")


def return_to_village_via_sanctuary(emu, symbols, output):
    before = snapshot(emu, symbols)
    assert before["map"] == "3/3" and before["position"] == [5, 9], before
    emu.send("run 128 12\nrun 0 20\nrun 64 12\nrun 0 20\n"
             "run 1 12\nrun 0 300")
    assert emu.read(symbols["sLockFieldControls"]) != 0
    emu.send(f"shot {output}")
    emu.send(press_a(2, 300))
    assert emu.read(symbols["sLockFieldControls"]) != 0
    choice_output = output.with_name(output.stem + "-choice" + output.suffix)
    emu.send(f"shot {choice_output}")
    emu.send(press_a(1, 600))
    returned = snapshot(emu, symbols)
    assert returned["map"] == "3/0" and returned["position"] == [8, 9], returned
    assert emu.read(symbols["sLockFieldControls"]) == 0
    return returned


def revisit_rare_lands_from_village(emu, symbols):
    emu.send("run 16 48\nrun 0 30\nrun 64 700\nrun 0 30\n"
             "run 128 32\nrun 0 30\nrun 16 16\nrun 0 30\n"
             "run 64 500\nrun 0 60\nrun 32 16\nrun 0 30\n"
             "run 64 340\nrun 0 120")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/20" and state["position"] == [11, 71], state
    emu.send("run 32 20\nrun 0 60\nrun 64 600\nrun 0 600")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/2" and state["position"] == [23, 9], state
    for expected in ("3/21", "3/22", "3/3"):
        emu.send("run 16 20\nrun 0 600")
        state = snapshot(emu, symbols)
        assert state["map"] == expected and state["position"] == [5, 9], state
    return state


def inspect_post_campaign_guide(emu, symbols, output):
    before = snapshot(emu, symbols)
    assert before["map"] == "3/0" and before["position"] == [8, 9], before
    emu.send("run 64 12\nrun 0 20\nrun 1 12\nrun 0 300")
    assert emu.read(symbols["sLockFieldControls"]) != 0
    emu.send(f"shot {output}")
    for _ in range(8):
        if emu.read(symbols["sLockFieldControls"]) == 0:
            break
        emu.send("run 2 12\nrun 0 180")
    else:
        raise AssertionError("post-campaign guide did not release controls")
    after = snapshot(emu, symbols)
    assert after == before, (before, after)


def return_to_sanctuary_via_guide(emu, symbols, output):
    before = snapshot(emu, symbols)
    assert before["map"] == "3/0" and before["position"] == [8, 9], before
    emu.send("run 64 12\nrun 0 20\nrun 1 12\nrun 0 300")
    assert emu.read(symbols["sLockFieldControls"]) != 0
    emu.send(press_a(2, 300))
    assert emu.read(symbols["sLockFieldControls"]) != 0
    emu.send(f"shot {output}")
    emu.send(press_a(1, 600))
    returned = snapshot(emu, symbols)
    assert returned["map"] == "3/3" and returned["position"] == [5, 9], returned
    assert emu.read(symbols["sLockFieldControls"]) == 0
    return returned


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    fifth = json.loads((args.fifth_habitat_results / "results.json").read_text())
    assert fifth["rom_sha1"] == digest
    assert fifth["partner"] == args.partner
    source = args.fifth_habitat_results / "fifth-habitat.sav"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / "campaign-ending.sav"
    shutil.copyfile(source, save)
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}

    emu = Emulator(args, "campaign-ending", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        initial = snapshot(emu, symbols)
        assert initial == fifth["continued"], (initial, fifth["continued"])
        identities = party_identities(emu, symbols)
        assert identities == fifth.get("party_identities", identities)
        assert campaign_flag_bytes(emu, symbols) == (0xFF, 0x00, 0xE0, 0x01)
        items = key_items(emu, symbols)
        assert all(items.get(item) == 1 for item in (361, 362, 363, 364, 365))
        initial_health = party_health(emu, symbols)
        assert initial_health and all(hp == max_hp and hp > 0
                                      for hp, max_hp in initial_health), initial_health

        emu.send("run 16 20\nrun 0 600\nrun 64 12\nrun 0 60")
        entered = snapshot(emu, symbols)
        assert entered["map"] == "3/3" and entered["position"] == [5, 9], entered
        emu.send(f"shot {args.output / 'rare-lands-entry.ppm'}")

        inspect_marker(emu, symbols, 32, args.output / "drought-marker.ppm")
        inspect_marker(emu, symbols, 16, args.output / "forest-marker.ppm")
        emu.send("run 64 4\nrun 0 30")
        emu.send(press_a(2, 180))
        cycles = fight_tio_sam(
            emu, symbols, args.output / "tio-sam-battle.ppm"
        )
        for _ in range(14):
            if campaign_flag_bytes(emu, symbols)[3] & 0x04:
                break
            emu.send(press_a(1, 180))
        emu.send("run 0 300")
        emu.send(f"shot {args.output / 'ending-message.ppm'}")
        emu.send(press_a(2, 300))
        assert emu.read(symbols["sLockFieldControls"]) != 0
        emu.send(f"shot {args.output / 'sanctuary-reveal-message.ppm'}")
        emu.send(press_a(4, 300))
        assert emu.read(symbols["sLockFieldControls"]) != 0
        emu.send(f"shot {args.output / 'campaign-epilogue.ppm'}")
        for _ in range(12):
            if emu.read(symbols["sLockFieldControls"]) == 0:
                break
            emu.send("run 2 12\nrun 0 180")
        ended = snapshot(emu, symbols)
        assert party_identities(emu, symbols) == identities
        ended_flags = campaign_flag_bytes(emu, symbols)
        assert ended_flags == (0xFF, 0x00, 0xE0, 0x07), ended_flags
        items = key_items(emu, symbols)
        assert all(items.get(item) == 1 for item in (361, 362, 363, 364, 365)), items
        assert emu.read(symbols["sLockFieldControls"]) == 0

        inspect_sanctuary(emu, symbols, args.output / "restored-sanctuary.ppm")

        emu.send("run 64 24\nrun 0 60")
        assert snapshot(emu, symbols)["position"] == [5, 7]
        inspect_marker(emu, symbols, 32, args.output / "water-marker.ppm")
        inspect_marker(emu, symbols, 16, args.output / "roots-marker.ppm")
        inspect_marker(emu, symbols, 64, args.output / "flood-marker.ppm")
        ended = snapshot(emu, symbols)
        emu.send(f"shot {args.output / 'campaign-complete.ppm'}")

        emu.send("run 8 12\nrun 0 60\n" + "run 128 12\nrun 0 20\n" * 3
                 + "run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\n"
                 + "run 1 12\nrun 0 600")
    finally:
        emu.close()

    emu = Emulator(args, "campaign-ending-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == ended, (ended, continued)
        continued_flags = campaign_flag_bytes(emu, symbols)
        assert continued_flags == ended_flags
        continued_identities = party_identities(emu, symbols)
        assert continued_identities == identities
        items_after = key_items(emu, symbols)
        assert all(items_after.get(item) == 1 for item in (361, 362, 363, 364, 365))
        emu.send("run 128 36\nrun 0 60\nrun 64 4\nrun 0 30")
        sanctuary_position = snapshot(emu, symbols)
        assert sanctuary_position["position"] == [5, 9], sanctuary_position
        inspect_sanctuary(emu, symbols,
                          args.output / "restored-sanctuary-continue.ppm")
        village_return = return_to_village_via_sanctuary(
            emu, symbols, args.output / "sanctuary-return-prompt.ppm"
        )
        assert campaign_flag_bytes(emu, symbols) == ended_flags
        assert key_items(emu, symbols) == items_after
        assert party_identities(emu, symbols) == identities
        emu.send(f"shot {args.output / 'returned-to-village.ppm'}")
        inspect_post_campaign_guide(
            emu, symbols, args.output / "post-campaign-guide.ppm"
        )
        guide_return = return_to_sanctuary_via_guide(
            emu, symbols, args.output / "guide-return-choice.ppm"
        )
        assert campaign_flag_bytes(emu, symbols) == ended_flags
        assert key_items(emu, symbols) == items_after
        assert party_identities(emu, symbols) == identities
        second_village_return = return_to_village_via_sanctuary(
            emu, symbols, args.output / "second-sanctuary-return-prompt.ppm"
        )
        sanctuary_revisit = revisit_rare_lands_from_village(emu, symbols)
        inspect_sanctuary(
            emu, symbols, args.output / "sanctuary-after-village-return.ppm"
        )
        emu.send(f"shot {args.output / 'continued.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = dict(
        rom_sha1=digest,
        result="PASS",
        source_save_sha256=source_hash,
        partner=args.partner,
        source_fifth_habitat="fresh five-stone save with ordinary save/Continue",
        test_writes=False,
        initial=initial,
        initial_party_health=initial_health,
        entered=entered,
        battle_input_cycles=cycles,
        ended=ended,
        ended_flag_bytes=list(ended_flags),
        continued=continued,
        party_identities=continued_identities,
        continued_flag_bytes=list(continued_flags),
        rare_stone_markers_checked=["water", "roots", "drought", "forest", "flood"],
        restored_sanctuary_visits=4,
        staged_sanctuary_reveal=True,
        campaign_epilogue=True,
        optional_return_to_village=True,
        village_return=village_return,
        post_campaign_guide_reception=True,
        optional_guide_return_to_sanctuary=True,
        guide_return_to_sanctuary=guide_return,
        second_village_return=second_village_return,
        sanctuary_revisit_after_village=sanctuary_revisit,
        stones={"water": items_after[361], "roots": items_after[362],
                "drought": items_after[363], "forest": items_after[364],
                "flood": items_after[365]},
        scope=("Native five-stone save; Pantanal east transition; Tio Sam battle, "
               "expanded ending, restored sanctuary before and after ordinary save/Continue, "
               "optional return to the village, post-campaign guide reception, optional "
               "guide return to the sanctuary and a full-path sanctuary revisit. "
               "Uses provisional inherited map art and does not claim final balance, "
               "credits or a polished ending."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Terras Raras/Tio Sam/sanctuary ending/save/Continue: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "fifth-habitat-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    check(parser.parse_args())
