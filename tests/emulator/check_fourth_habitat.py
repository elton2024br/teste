"""Continue a native third-mission save through Mata Atlântica and stone four."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import snapshot
from check_second_habitat import key_items, party_health


def campaign_flag_bytes(emu, symbols):
    block1 = emu.read(symbols["gSaveBlock1Ptr"], 32)
    return tuple(emu.read(block1 + offset) for offset in (0xF75, 0xF76, 0xF77))


def fight_atlantic_agent(emu, symbols, battle_shot=None):
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
        assert state["map"] == "3/21", ("left fourth habitat", state)
        if campaign_flag_bytes(emu, symbols)[2] & 0x20:
            assert emu.read(symbols["gBattleOutcome"]) == 1, "expected B_OUTCOME_WON"
            return cycle + 1
    raise AssertionError("Mata Atlântica agent battle did not finish")


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    third = json.loads((args.third_habitat_results / "results.json").read_text())
    assert third["rom_sha1"] == digest
    assert third["partner"] == args.partner
    source = args.third_habitat_results / "third-habitat.sav"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / "fourth-habitat.sav"
    shutil.copyfile(source, save)
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}

    emu = Emulator(args, "fourth-habitat", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        initial = snapshot(emu, symbols)
        assert initial == third["continued"], (initial, third["continued"])
        assert campaign_flag_bytes(emu, symbols) == (0xFF, 0x00, 0x00)
        items = key_items(emu, symbols)
        assert items.get(361) == items.get(362) == items.get(363) == 1
        assert 364 not in items

        # The tile east of the Caatinga checkpoint is the provisional exit.
        emu.send("run 16 20\nrun 0 600\nrun 64 12\nrun 0 60")
        entered = snapshot(emu, symbols)
        assert entered["map"] == "3/21" and entered["position"] == [5, 9], entered
        emu.send(f"shot {args.output / 'atlantic-entry.ppm'}")

        emu.send(press_a(2, 180))
        cycles = fight_atlantic_agent(
            emu, symbols, args.output / "atlantic-battle.ppm"
        )
        for _ in range(10):
            if campaign_flag_bytes(emu, symbols)[2] & 0x40:
                break
            emu.send(press_a(1, 180))
        emu.send("run 0 300")
        emu.send(f"shot {args.output / 'forest-stone-message.ppm'}")
        for _ in range(8):
            if emu.read(symbols["sLockFieldControls"]) == 0:
                break
            emu.send("run 2 12\nrun 0 180")
        rewarded = snapshot(emu, symbols)
        rewarded_flags = campaign_flag_bytes(emu, symbols)
        assert rewarded_flags == (0xFF, 0x00, 0x60), rewarded_flags
        items = key_items(emu, symbols)
        assert all(items.get(item) == 1 for item in (361, 362, 363, 364)), items
        healed = party_health(emu, symbols)
        assert healed and all(hp == max_hp and hp > 0 for hp, max_hp in healed), healed
        assert emu.read(symbols["sLockFieldControls"]) == 0
        emu.send(f"shot {args.output / 'forest-stone.ppm'}")

        emu.send("run 8 12\nrun 0 60\n" + "run 128 12\nrun 0 20\n" * 3
                 + "run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\n"
                 + "run 1 12\nrun 0 600")
    finally:
        emu.close()

    emu = Emulator(args, "fourth-habitat-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == rewarded, (rewarded, continued)
        continued_flags = campaign_flag_bytes(emu, symbols)
        assert continued_flags == rewarded_flags
        items_after = key_items(emu, symbols)
        assert all(items_after.get(item) == 1 for item in (361, 362, 363, 364))
        emu.send(f"shot {args.output / 'continued.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = dict(
        rom_sha1=digest,
        result="PASS",
        source_save_sha256=source_hash,
        partner=args.partner,
        source_third_habitat="fresh third mission with ordinary save/Continue",
        test_writes=False,
        initial=initial,
        entered=entered,
        battle_input_cycles=cycles,
        rewarded=rewarded,
        rewarded_flag_bytes=list(rewarded_flags),
        continued=continued,
        continued_flag_bytes=list(continued_flags),
        healed_party=healed,
        stones={"water": items_after[361], "roots": items_after[362],
                "drought": items_after[363], "forest": items_after[364]},
        scope=("Native third-mission save; Caatinga east transition; Mata Atlântica "
               "battle, four unique key items, normal save and Continue. Uses "
               "provisional inherited map art and does not validate habitat five."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print("fourth habitat/battle/forest stone/save/Continue: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "third-habitat-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    check(parser.parse_args())
