"""Confirm release through native UI in an isolated copy of a synthetic-party save."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import snapshot
from check_stone_revisit import walk_to
from check_capture import capsules, read_bytes
from check_village_pc import party, boxes, menu, task_active, leave_storage, approach


def confirmation(emu, symbols):
    emu.send(press_a(1, 90) + 'run 128 12\nrun 0 60\n' * 3 + press_a(1, 180))
    assert task_active(emu, symbols, 'Task_ReleaseMon'), 'release confirmation did not open'


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    fixture = json.loads((args.capture_results / 'results.json').read_text())
    assert fixture['rom_sha1'] == digest and fixture['result'] == 'PASS'
    assert fixture['synthetic_full_party'] is True
    source = args.capture_results / 'captured.sav'
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / 'isolated-release.sav'
    shutil.copyfile(source, save)
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    emu = Emulator(args, 'isolated-release', save)  # No write opt-in or savestates.
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                 'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
        assert snapshot(emu, symbols) == fixture['continued']
        original_party, original_boxes = party(emu, symbols), boxes(emu, symbols)
        assert len(original_party) == 6 and [p['species'] for p in original_party] == [7] * 6
        assert list(original_boxes) == [0] and original_boxes[0]['species'] == 1
        emu.send('run 32 64\nrun 0 30')
        walk_to(emu, symbols, 128, '3/0', [11, 15])
        approach(emu, symbols)
        emu.send(press_a(3, 180))
        assert menu(emu, symbols) == 2
        # Deposit one Capivagua to open WITHDRAW mode with a spare party slot.
        emu.send('run 128 12\nrun 0 60\n' + press_a(1, 600))
        emu.send(press_a(1, 90) + press_a(1, 180) + press_a(1, 600))
        leave_storage(emu, symbols)
        prepared_party, prepared_boxes = party(emu, symbols), boxes(emu, symbols)
        assert prepared_party == original_party[1:] and len(prepared_party) == 5
        assert prepared_boxes == {0: original_boxes[0], 1: original_party[0]}
        emu.send('run 64 12\nrun 0 60\n' + press_a(1, 600))
        confirmation(emu, symbols)
        emu.send(f'shot {args.output / "confirmation-no.ppm"}')
        emu.send('run 2 12\nrun 0 180')
        assert task_active(emu, symbols, 'Task_PokeStorageMain')
        assert party(emu, symbols) == prepared_party and boxes(emu, symbols) == prepared_boxes
        # Reopen, explicitly select YES, and confirm only on this copied save.
        confirmation(emu, symbols)
        emu.send('run 64 12\nrun 0 60')
        emu.send(f'shot {args.output / "confirmation-yes.ppm"}')
        emu.send(press_a(1, 600))
        expected_boxes = {1: prepared_boxes[1]}
        assert party(emu, symbols) == prepared_party and boxes(emu, symbols) == expected_boxes
        storage = emu.read(symbols['gPokemonStoragePtr'], 32)
        assert read_bytes(emu, storage + 4, 80) == bytes(80), 'selected box slot was not cleared'
        emu.send(f'shot {args.output / "released-message.ppm"}')
        emu.send(press_a(1, 180))
        emu.send(f'shot {args.output / "farewell.ppm"}')
        emu.send(press_a(1, 600))
        assert task_active(emu, symbols, 'Task_PokeStorageMain')
        emu.send(f'shot {args.output / "released-slot.ppm"}')
        leave_storage(emu, symbols)
        emu.send('run 2 12\nrun 0 180')
        assert menu(emu, symbols) is None and emu.read(symbols['sLockFieldControls']) == 0
        before = snapshot(emu, symbols)
        assert before == dict(partner=1, flags=1, keyitem=0, party=5, starter=1,
                              map='3/0', position=[13, 15]), before
        assert len(party(emu, symbols)) + len(boxes(emu, symbols)) == 6
        assert party(emu, symbols) == prepared_party and boxes(emu, symbols) == expected_boxes
        assert capsules(emu, symbols) == 4
        emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                 + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\nrun 1 12\nrun 0 600')
    finally:
        emu.close()
    emu = Emulator(args, 'continue-release', save)
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                 'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
        assert snapshot(emu, symbols) == before
        assert party(emu, symbols) == prepared_party and boxes(emu, symbols) == expected_boxes
        storage = emu.read(symbols['gPokemonStoragePtr'], 32)
        assert read_bytes(emu, storage + 4, 80) == bytes(80)
        assert capsules(emu, symbols) == 4
        emu.send(f'shot {args.output / "continued.ppm"}')
    finally:
        emu.close()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash, 'source save modified'
    report = dict(rom_sha1=digest, result='PASS', source_save_sha256=source_hash,
                  source_full_party_is_synthetic=True, interface_test_writes=False,
                  isolated_copy=True, source_preserved=True, cancel_preserves_creature=True,
                  confirmed_release_species=1, selected_box_slot_cleared=True,
                  only_selected_creature_removed=True, counts_before=dict(party=5, pc=2),
                  counts_after=dict(party=5, pc=1), other_creatures_identity_checksum_preserved=True,
                  normal_save_continue=True, progress=before,
                  scope='Cancel then confirm release of boxed Tatupedra in an isolated native-save '
                        'copy sourced from synthetic full-party capture; other creatures, progress, '
                        'capsules and persistence verified. No party-member release, egg/HM refusal, '
                        'all names or every release path.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print('isolated cancel/confirmed release/save/Continue: PASS', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'capture-results', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
