"""Lose before stone five, recover, Continue, return and complete the mission."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import attempt_trainer_balls, snapshot
from check_second_habitat import key_items, party_health
from check_fifth_habitat import campaign_flag_bytes, fight_pantanal_agent
from check_campaign_final_defeat import (
    finish_recovery,
    save_from_house,
    set_hp_fixture,
)


def return_to_pantanal(emu, symbols):
    emu.send("run 128 32\nrun 0 30\nrun 32 64\nrun 0 30\n"
             "run 128 48\nrun 0 180\nrun 128 16\nrun 0 20\n"
             "run 16 32\nrun 0 20\nrun 64 4\nrun 0 30")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/0" and state["position"] == [8, 9], state
    emu.send("run 16 48\nrun 0 30\nrun 64 700\nrun 0 30\n"
             "run 128 32\nrun 0 30\nrun 16 16\nrun 0 30\n"
             "run 64 500\nrun 0 60\nrun 32 16\nrun 0 30\n"
             "run 64 340\nrun 0 120")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/20" and state["position"] == [11, 71], state
    emu.send("run 32 20\nrun 0 60\nrun 64 600\nrun 0 600")
    state = snapshot(emu, symbols)
    assert state["map"] == "3/2" and state["position"] == [23, 9], state
    for expected in ("3/21", "3/22"):
        emu.send("run 16 20\nrun 0 600")
        state = snapshot(emu, symbols)
        assert state["map"] == expected and state["position"] == [5, 9], state


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    fourth = json.loads((args.fourth_habitat_results / "results.json").read_text())
    assert fourth["rom_sha1"] == digest and fourth["partner"] == args.partner
    source = args.fourth_habitat_results / "fourth-habitat.sav"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / "fifth-defeat.sav"
    shutil.copyfile(source, save)
    lines = [p for line in args.symbols.read_text().splitlines()
             if len(p := line.split()) == 3]
    symbols = {p[2]: int(p[0], 16) for p in lines}
    actions = {int(p[0], 16) for p in lines if p[2] == "HandleInputChooseAction"}

    emu = Emulator(args, "fifth-habitat-defeat-fixture", save, test_writes=True)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200\n"
                 "run 16 20\nrun 0 600\nrun 64 12\nrun 0 60")
        entered = snapshot(emu, symbols)
        initial_flags = campaign_flag_bytes(emu, symbols)
        initial_items = key_items(emu, symbols)
        assert entered["map"] == "3/22" and entered["position"] == [5, 9], entered
        assert initial_flags == (0xFF, 0x00, 0x60, 0x00), initial_flags
        assert all(initial_items.get(item) == 1 for item in range(361, 365))
        assert 365 not in initial_items
        original_max_hp = set_hp_fixture(emu, symbols)

        emu.send(press_a(2, 180))
        throws = attempt_trainer_balls(emu, symbols, actions)
        for cycle in range(80):
            state = snapshot(emu, symbols)
            if state["map"] == "4/0":
                break
            emu.send(press_a(1, 240))
        else:
            raise AssertionError("HP fixture did not reach a normal Pantanal defeat")
        assert emu.read(symbols["gBattleOutcome"]) == 2, "expected B_OUTCOME_LOST"
        loss_flags = campaign_flag_bytes(emu, symbols)
        assert loss_flags == initial_flags, (initial_flags, loss_flags)
        finish_recovery(emu, symbols, args.output)
        recovered = snapshot(emu, symbols)
        recovered_flags = campaign_flag_bytes(emu, symbols)
        recovered_items = key_items(emu, symbols)
        recovered_health = party_health(emu, symbols)
        assert recovered["map"] == "4/0" and recovered["position"] == [8, 5], recovered
        assert recovered_flags == initial_flags
        assert recovered_items == initial_items
        assert recovered_health == [[original_max_hp, original_max_hp]], recovered_health
        emu.send(f"shot {args.output / 'recovered-before-fifth-stone.ppm'}")
        save_from_house(emu)
    finally:
        emu.close()

    emu = Emulator(args, "fifth-habitat-defeat-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == recovered, (recovered, continued)
        assert campaign_flag_bytes(emu, symbols) == recovered_flags
        assert key_items(emu, symbols) == recovered_items
        return_to_pantanal(emu, symbols)
        emu.send("run 64 12\nrun 0 60")
        emu.send(press_a(2, 180))
        win_cycles = fight_pantanal_agent(emu, symbols)
        for _ in range(10):
            if campaign_flag_bytes(emu, symbols)[3] & 0x01:
                break
            emu.send(press_a(1, 180))
        emu.send("run 0 300")
        for _ in range(8):
            if emu.read(symbols["sLockFieldControls"]) == 0:
                break
            emu.send("run 2 12\nrun 0 180")
        rewarded = snapshot(emu, symbols)
        final_flags = campaign_flag_bytes(emu, symbols)
        final_items = key_items(emu, symbols)
        final_health = party_health(emu, symbols)
        assert final_flags == (0xFF, 0x00, 0xE0, 0x01), final_flags
        assert all(final_items.get(item) == 1 for item in range(361, 366)), final_items
        assert final_health and all(hp == max_hp and hp > 0 for hp, max_hp in final_health)
        assert emu.read(symbols["sLockFieldControls"]) == 0
        emu.send(f"shot {args.output / 'fifth-stone-after-retry.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = dict(
        rom_sha1=digest,
        result="PASS",
        partner=args.partner,
        fixture_writes=True,
        fixture="party slot 0 current HP set to 1; no flags, items or outcomes written",
        trainer_ball_attempts=throws,
        battle_outcome_loss=2,
        recovered=recovered,
        recovered_flag_bytes=list(recovered_flags),
        recovered_party_health=recovered_health,
        four_stones_preserved_after_loss=True,
        fifth_agent_and_stone_pending_after_loss=True,
        normal_save_continue=True,
        continued=continued,
        returned_through_prior_habitats=True,
        win_input_cycles=win_cycles,
        rewarded=rewarded,
        final_flag_bytes=list(final_flags),
        fifth_stone_received_after_retry=True,
        source_save_preserved=True,
        scope=("Artificial HP=1 fixture only; normal Pantanal-agent defeat, home "
               "recovery, four stones and pending reward preserved, ordinary save/Continue "
               "with writes disabled, return through prior habitats and normal victory. "
               "Not evidence of naturally accumulated damage or other intermediate agents."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(args.partner + " Pantanal defeat fixture/recovery/retry: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "fourth-habitat-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    check(parser.parse_args())
