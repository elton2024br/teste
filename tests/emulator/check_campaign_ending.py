"""Continue a five-stone save through Terras Raras and the minimal ending."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import snapshot
from check_second_habitat import key_items


def campaign_flag_bytes(emu, symbols):
    block1 = emu.read(symbols["gSaveBlock1Ptr"], 32)
    return tuple(emu.read(block1 + offset) for offset in (0xF75, 0xF76, 0xF77, 0xF78))


def fight_tio_sam(emu, symbols):
    for cycle in range(260):
        handler = emu.read(symbols["gBattlerControllerFuncs"], 32) & ~1
        if handler == symbols["HandleInputChooseMove"]:
            assert emu.read(symbols["gMoveSelectionCursor"]) == 0
        emu.send(press_a(1, 90))
        state = snapshot(emu, symbols)
        assert state["map"] == "3/3", ("left Terras Raras", state)
        if campaign_flag_bytes(emu, symbols)[3] & 0x02:
            assert emu.read(symbols["gBattleOutcome"]) == 1, "expected B_OUTCOME_WON"
            return cycle + 1
    raise AssertionError("Tio Sam battle did not finish")


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
        assert campaign_flag_bytes(emu, symbols) == (0xFF, 0x00, 0xE0, 0x01)
        items = key_items(emu, symbols)
        assert all(items.get(item) == 1 for item in (361, 362, 363, 364, 365))

        emu.send("run 16 20\nrun 0 600\nrun 64 12\nrun 0 60")
        entered = snapshot(emu, symbols)
        assert entered["map"] == "3/3" and entered["position"] == [5, 9], entered
        emu.send(f"shot {args.output / 'rare-lands-entry.ppm'}")

        emu.send(press_a(2, 180))
        cycles = fight_tio_sam(emu, symbols)
        for _ in range(14):
            if campaign_flag_bytes(emu, symbols)[3] & 0x04:
                break
            emu.send(press_a(1, 180))
        emu.send("run 0 300")
        emu.send(f"shot {args.output / 'ending-message.ppm'}")
        for _ in range(12):
            if emu.read(symbols["sLockFieldControls"]) == 0:
                break
            emu.send("run 2 12\nrun 0 180")
        ended = snapshot(emu, symbols)
        ended_flags = campaign_flag_bytes(emu, symbols)
        assert ended_flags == (0xFF, 0x00, 0xE0, 0x07), ended_flags
        items = key_items(emu, symbols)
        assert all(items.get(item) == 1 for item in (361, 362, 363, 364, 365)), items
        assert emu.read(symbols["sLockFieldControls"]) == 0
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
        items_after = key_items(emu, symbols)
        assert all(items_after.get(item) == 1 for item in (361, 362, 363, 364, 365))
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
        entered=entered,
        battle_input_cycles=cycles,
        ended=ended,
        ended_flag_bytes=list(ended_flags),
        continued=continued,
        continued_flag_bytes=list(continued_flags),
        stones={"water": items_after[361], "roots": items_after[362],
                "drought": items_after[363], "forest": items_after[364],
                "flood": items_after[365]},
        scope=("Native five-stone save; Pantanal east transition; Tio Sam battle, "
               "minimal ending, normal save and Continue. Uses provisional inherited "
               "map art and does not claim final balance, credits or a polished ending."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Terras Raras/Tio Sam/minimal ending/save/Continue: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "fifth-habitat-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    check(parser.parse_args())
