"""Continue a native first-mission save through the Cerrado and second stone."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import dismiss, snapshot


def key_items(emu, symbols):
    block1 = emu.read(symbols["gSaveBlock1Ptr"], 32)
    block2 = emu.read(symbols["gSaveBlock2Ptr"], 32)
    key = emu.read(block2 + 0xF20, 32) & 0xFFFF
    result = {}
    for index in range(30):
        slot = emu.read(block1 + 0x3B8 + index * 4, 32)
        item = slot & 0xFFFF
        if item:
            result[item] = (slot >> 16) ^ key
    return result


def party_health(emu, symbols):
    count = emu.read(symbols["gPlayerPartyCount"])
    party = symbols["gPlayerParty"]
    result = []
    for index in range(count):
        pokemon = party + index * 100
        hp = emu.read(pokemon + 0x56) | (emu.read(pokemon + 0x57) << 8)
        max_hp = emu.read(pokemon + 0x58) | (emu.read(pokemon + 0x59) << 8)
        result.append([hp, max_hp])
    return result


def fight_cerrado_agent(emu, symbols):
    for cycle in range(260):
        handler = emu.read(symbols["gBattlerControllerFuncs"], 32) & ~1
        if handler == symbols["HandleInputChooseMove"]:
            assert emu.read(symbols["gMoveSelectionCursor"]) == 0
        emu.send(press_a(1, 90))
        state = snapshot(emu, symbols)
        assert state["map"] == "3/20", ("left second habitat", state)
        if state["flags"] & 0x10:
            assert emu.read(symbols["gBattleOutcome"]) == 1, "expected B_OUTCOME_WON"
            return cycle + 1
    raise AssertionError("Cerrado agent battle did not finish")


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    first = json.loads((args.first_mission_results / "results.json").read_text())
    assert first["rom_sha1"] == digest
    matching = [case for case in first["cases"] if case["partner"] == args.partner]
    assert len(matching) == 1, (args.partner, first["cases"])
    first_case = matching[0]
    partner = args.partner
    source = args.first_mission_results / (partner + ".sav")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / "second-habitat.sav"
    shutil.copyfile(source, save)
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}

    emu = Emulator(args, "second-habitat", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        initial = snapshot(emu, symbols)
        assert initial == first_case["continued"], initial
        assert key_items(emu, symbols).get(361) == 1
        assert 362 not in key_items(emu, symbols)

        # Village -> first habitat -> new north exit -> Campo Cerrado.
        emu.send("run 16 48\nrun 0 30\nrun 64 700\nrun 0 30\n"
                 "run 128 32\nrun 0 30\nrun 16 16\nrun 0 30\n"
                 "run 64 500\nrun 0 60\nrun 32 16\nrun 0 30\n"
                 "run 64 40\nrun 0 120")
        entered = snapshot(emu, symbols)
        assert entered["map"] == "3/20" and entered["position"] == [11, 78], entered
        emu.send("run 64 300\nrun 0 60")
        assert snapshot(emu, symbols)["position"] == [11, 71]
        emu.send(f"shot {args.output / 'cerrado-entry.ppm'}")

        emu.send(press_a(2, 180))
        cycles = fight_cerrado_agent(emu, symbols)
        for _ in range(8):
            if snapshot(emu, symbols)["flags"] & 0x20:
                break
            emu.send(press_a(1, 180))
        emu.send("run 0 300")
        emu.send(f"shot {args.output / 'root-stone-message.ppm'}")
        for _ in range(8):
            if emu.read(symbols["sLockFieldControls"]) == 0:
                break
            emu.send("run 2 12\nrun 0 180")
        rewarded = snapshot(emu, symbols)
        assert rewarded["flags"] == 0x3F, rewarded
        items = key_items(emu, symbols)
        assert items.get(361) == items.get(362) == 1, items
        healed = party_health(emu, symbols)
        assert healed and all(hp == max_hp and hp > 0 for hp, max_hp in healed), healed
        assert emu.read(symbols["sLockFieldControls"]) == 0
        emu.send(f"shot {args.output / 'root-stone.ppm'}")

        # Ordinary in-game save, then Continue in a new emulator process.
        emu.send("run 8 12\nrun 0 60\n" + "run 128 12\nrun 0 20\n" * 3
                 + "run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\n"
                 + "run 1 12\nrun 0 600")
    finally:
        emu.close()

    emu = Emulator(args, "second-habitat-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == rewarded, (rewarded, continued)
        items_after = key_items(emu, symbols)
        assert items_after.get(361) == items_after.get(362) == 1
        emu.send(f"shot {args.output / 'continued.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = dict(
        rom_sha1=digest,
        result="PASS",
        source_save_sha256=source_hash,
        partner=partner,
        source_first_mission="fresh first mission with ordinary save/Continue",
        test_writes=False,
        initial=initial,
        entered=entered,
        battle_input_cycles=cycles,
        rewarded=rewarded,
        continued=continued,
        healed_party=healed,
        stones={"water": items_after[361], "roots": items_after[362]},
        scope=("Native first-mission save; walk through the new forest connection; "
               "Cerrado battle, two unique key items, normal save and Continue. "
               "Does not validate the other two partners, full key-item pocket, "
               "the northern Route 2 campaign, or final art."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print("second habitat/battle/root stone/save/Continue: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "first-mission-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    check(parser.parse_args())
