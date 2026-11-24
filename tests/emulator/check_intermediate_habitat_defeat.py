"""Lose to a middle-habitat agent, recover, Continue and win the retry."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import attempt_trainer_balls, snapshot
from check_second_habitat import fight_cerrado_agent, key_items, party_health
from check_third_habitat import fight_caatinga_agent
from check_fourth_habitat import campaign_flag_bytes, fight_atlantic_agent
from check_campaign_final_defeat import finish_recovery, save_from_house, set_hp_fixture
from check_fifth_habitat_defeat import lose_two_member_with_trainer_balls
from party_recovery import assert_party_fully_recovered, party_identities


HOUSE_TO_VILLAGE = (
    "run 128 32\nrun 0 30\nrun 32 64\nrun 0 30\n"
    "run 128 48\nrun 0 180\nrun 128 16\nrun 0 20\n"
    "run 16 32\nrun 0 20\nrun 64 4\nrun 0 30"
)
VILLAGE_TO_CERRADO = (
    "run 16 48\nrun 0 30\nrun 64 700\nrun 0 30\n"
    "run 128 32\nrun 0 30\nrun 16 16\nrun 0 30\n"
    "run 64 500\nrun 0 60\nrun 32 16\nrun 0 30\n"
    "run 64 340\nrun 0 120"
)
CERRADO_TO_CAATINGA = "run 32 20\nrun 0 60\nrun 64 600\nrun 0 600"
CAATINGA_TO_ATLANTIC = "run 16 20\nrun 0 600\nrun 64 12\nrun 0 60"


STAGES = {
    "second": {
        "source_save": lambda root, partner: root / (partner + ".sav"),
        "source_kind": "first mission",
        "enter": VILLAGE_TO_CERRADO,
        "return": VILLAGE_TO_CERRADO,
        "map": "3/20",
        "position": [11, 71],
        "flags_before": (0x0F, 0x00, 0x00),
        "flags_after": (0x3F, 0x00, 0x00),
        "stone": 362,
        "fight": fight_cerrado_agent,
        "label": "Cerrado",
    },
    "third": {
        "source_save": lambda root, partner: root / "second-habitat.sav",
        "source_kind": "second habitat",
        "enter": CERRADO_TO_CAATINGA,
        "return": VILLAGE_TO_CERRADO + "\n" + CERRADO_TO_CAATINGA,
        "map": "3/2",
        "position": [23, 9],
        "flags_before": (0x3F, 0x00, 0x00),
        "flags_after": (0xFF, 0x00, 0x00),
        "stone": 363,
        "fight": fight_caatinga_agent,
        "label": "Caatinga",
    },
    "fourth": {
        "source_save": lambda root, partner: root / "third-habitat.sav",
        "source_kind": "third habitat",
        "enter": CAATINGA_TO_ATLANTIC,
        "return": (VILLAGE_TO_CERRADO + "\n" + CERRADO_TO_CAATINGA + "\n"
                   + CAATINGA_TO_ATLANTIC),
        "map": "3/21",
        "position": [5, 9],
        "flags_before": (0xFF, 0x00, 0x00),
        "flags_after": (0xFF, 0x00, 0x60),
        "stone": 364,
        "fight": fight_atlantic_agent,
        "label": "Mata Atlantica",
    },
}


def assert_checkpoint(emu, symbols, stage):
    state = snapshot(emu, symbols)
    assert state["map"] == stage["map"] and state["position"] == stage["position"], state
    return state


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), "Use a fresh output directory."
    stage = STAGES[args.stage]
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    source_report = json.loads((args.source_results / "results.json").read_text())
    assert source_report["rom_sha1"] == digest
    if args.stage == "second":
        partner_cases = [case for case in source_report["cases"]
                         if case["partner"] == args.partner]
        partners = [case["partner"] for case in source_report["cases"]]
        assert partners.count(args.partner) == 1, (args.partner, partners)
        expected_identities = partner_cases[0].get("party_identities")
    else:
        assert source_report["partner"] == args.partner
        expected_identities = source_report.get("party_identities")
    source = stage["source_save"](args.source_results, args.partner)
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / (args.stage + "-habitat-defeat.sav")
    shutil.copyfile(source, save)
    lines = [p for line in args.symbols.read_text().splitlines()
             if len(p := line.split()) == 3]
    symbols = {p[2]: int(p[0], 16) for p in lines}
    actions = {int(p[0], 16) for p in lines if p[2] == "HandleInputChooseAction"}
    switch_handlers = {int(p[0], 16) for p in lines if p[2] == "WaitForMonSelection"}
    assert actions and switch_handlers

    emu = Emulator(args, args.stage + "-habitat-defeat-fixture", save, test_writes=True)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200\n"
                 + stage["enter"])
        entered = assert_checkpoint(emu, symbols, stage)
        initial_flags = campaign_flag_bytes(emu, symbols)
        initial_items = key_items(emu, symbols)
        assert initial_flags == stage["flags_before"], initial_flags
        assert all(initial_items.get(item) == 1 for item in range(361, stage["stone"]))
        assert stage["stone"] not in initial_items
        identities = party_identities(emu, symbols)
        if expected_identities is not None:
            assert identities == expected_identities
        assert len(identities) == (2 if args.all_party_hp_fixture else 1), identities
        original_max_hp = set_hp_fixture(emu, symbols, args.all_party_hp_fixture)
        assert party_identities(emu, symbols) == identities
        emu.send(f"shot {args.output / 'hp-fixture-before-battle.ppm'}")

        emu.send(press_a(2, 180))
        if args.all_party_hp_fixture:
            throws, loss_switches, loss_cycles = lose_two_member_with_trainer_balls(
                emu, symbols, actions, switch_handlers, stage["map"]
            )
        else:
            throws = attempt_trainer_balls(emu, symbols, actions)
            loss_switches = 0
            for cycle in range(80):
                state = snapshot(emu, symbols)
                if state["map"] == "4/0":
                    loss_cycles = cycle + 1
                    break
                emu.send(press_a(1, 240))
            else:
                raise AssertionError("HP fixture did not reach a normal defeat")
        assert emu.read(symbols["gBattleOutcome"]) == 2, "expected B_OUTCOME_LOST"
        assert campaign_flag_bytes(emu, symbols) == initial_flags
        assert key_items(emu, symbols) == initial_items
        finish_recovery(emu, symbols, args.output)
        recovered = snapshot(emu, symbols)
        recovered_health = party_health(emu, symbols)
        assert recovered["map"] == "4/0" and recovered["position"] == [8, 5], recovered
        assert campaign_flag_bytes(emu, symbols) == initial_flags
        assert key_items(emu, symbols) == initial_items
        assert recovered_health == [[hp, hp] for hp in original_max_hp], recovered_health
        if args.all_party_hp_fixture:
            recovered_condition = assert_party_fully_recovered(emu, symbols)
        else:
            recovered_condition = None
        assert party_identities(emu, symbols) == identities
        emu.send(f"shot {args.output / 'recovered-with-stone-pending.ppm'}")
        save_from_house(emu)
    finally:
        emu.close()

    emu = Emulator(args, args.stage + "-habitat-defeat-continue", save)
    try:
        emu.send("run 0 300\nrun 8 20\nrun 0 100\n"
                 "run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200")
        continued = snapshot(emu, symbols)
        assert continued == recovered, (recovered, continued)
        assert campaign_flag_bytes(emu, symbols) == initial_flags
        assert key_items(emu, symbols) == initial_items
        assert party_identities(emu, symbols) == identities
        if args.all_party_hp_fixture:
            assert_party_fully_recovered(emu, symbols)
        emu.send(HOUSE_TO_VILLAGE + "\n" + stage["return"])
        returned = assert_checkpoint(emu, symbols, stage)
        emu.send(press_a(2, 180))
        retry_stats = {}
        win_cycles = stage["fight"](
            emu, symbols, switch_handlers=switch_handlers,
            battle_stats=retry_stats
        )
        for _ in range(12):
            if campaign_flag_bytes(emu, symbols) == stage["flags_after"]:
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
        assert final_flags == stage["flags_after"], final_flags
        assert all(final_items.get(item) == 1 for item in range(361, stage["stone"] + 1))
        assert final_health and all(hp == max_hp and hp > 0 for hp, max_hp in final_health)
        assert party_identities(emu, symbols) == identities
        if args.all_party_hp_fixture:
            assert_party_fully_recovered(emu, symbols)
        assert emu.read(symbols["sLockFieldControls"]) == 0
        emu.send(f"shot {args.output / 'stone-after-retry.ppm'}")
    finally:
        emu.close()

    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = dict(
        rom_sha1=digest,
        result="PASS",
        stage=args.stage,
        habitat=stage["label"],
        partner=args.partner,
        fixture_writes=True,
        fixture=("all party members current HP set to 1"
                 if args.all_party_hp_fixture
                 else "party slot 0 current HP set to 1"),
        fixture_scope="no flags, items, identities or outcomes written",
        source=stage["source_kind"] + " save with ordinary Continue",
        trainer_ball_attempts=throws,
        battle_outcome_loss=2,
        loss_input_cycles=loss_cycles,
        mandatory_switches=loss_switches,
        retry_mandatory_switches=retry_stats["mandatory_switches"],
        party_identities=identities,
        entered=entered,
        recovered=recovered,
        recovered_flag_bytes=list(initial_flags),
        recovered_party_health=recovered_health,
        recovered_party_condition=recovered_condition,
        pending_stone_preserved_after_loss=True,
        normal_save_continue=True,
        continued=continued,
        returned=returned,
        win_input_cycles=win_cycles,
        rewarded=rewarded,
        final_flag_bytes=list(final_flags),
        pending_stone_received_after_retry=True,
        source_save_preserved=True,
        scope=("Artificial HP=1 fixture applied to "
               + ("both members" if args.all_party_hp_fixture else "the lead member")
               + "; normal intermediate-agent defeat, home "
               "recovery, prior stones and pending reward preserved, ordinary save/Continue "
               "with writes disabled, stable party identities, return through prior "
               "habitats and normal victory. "
               "Not evidence of naturally accumulated damage."),
    )
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{args.partner} {stage['label']} defeat/recovery/retry: PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ["runner", "rom", "symbols", "source-results", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--stage", required=True, choices=STAGES)
    parser.add_argument("--partner", required=True,
                        choices=["capivagua", "ararafogo", "tatupedra"])
    parser.add_argument("--all-party-hp-fixture", action="store_true",
                        help="require two members and set current HP=1 on both")
    check(parser.parse_args())
