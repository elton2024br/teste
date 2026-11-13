"""Native village-PC UI; source save comes from the explicit full-party fixture."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import bootstrap, press_a
from check_defeat_recovery import dismiss, snapshot
from check_stone_revisit import walk_to
from check_capture import read_bytes, box_secure_data, capsules


def identity(raw):
    secure, growth = box_secure_data(raw[:80])
    return dict(species=int.from_bytes(secure[growth:growth + 2], 'little'),
                experience=int.from_bytes(secure[growth + 4:growth + 8], 'little'),
                header=raw[:28].hex())


def party(emu, symbols):
    return [identity(raw) for i in range(6)
            if (raw := read_bytes(emu, symbols['gPlayerParty'] + i * 100, 100))[19] & 2]


def boxes(emu, symbols):
    base = emu.read(symbols['gPokemonStoragePtr'], 32)
    assert 0x02000000 <= base <= 0x02040000 - 0x83D0
    return {i: identity(read_bytes(emu, base + 4 + i * 80, 80)) for i in range(420)
            if emu.read(base + 4 + i * 80 + 19) & 2}


def menu(emu, symbols):
    found = []
    for i in range(16):
        task = symbols['gTasks'] + i * 40
        if (emu.read(task + 4) and emu.read(task, 32) & ~1 == symbols['Task_PCMainMenu']):
            found.append(emu.read(task + 8, 32) & 65535)
    assert len(found) <= 1, 'duplicate PC menu tasks'
    return found[0] if found else None


def leave_storage(emu, symbols):
    # B opens "Continue BOX operations?" with NO selected. A returns to menu.
    emu.send('run 2 12\nrun 0 180\nrun 1 12\nrun 0 600')
    assert menu(emu, symbols) == 2, 'did not return to storage menu'


def approach(emu, symbols):
    emu.send('run 16 32\nrun 0 30\nrun 128 4\nrun 0 30')
    state = snapshot(emu, symbols)
    assert state['map'] == '3/0' and state['position'] == [13, 15], state


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    fixture = json.loads((args.capture_results / 'results.json').read_text())
    assert fixture['rom_sha1'] == digest and fixture['result'] == 'PASS'
    assert fixture['synthetic_full_party'] is True
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    # Natural new game: the new service must remain closed before a partner.
    emu = Emulator(args, 'no-partner')
    try:
        emu.send(bootstrap())
        dismiss(emu)  # Cancel the guide's choice without granting anything.
        assert snapshot(emu, symbols)['party'] == 0
        emu.send('run 16 80\nrun 0 30\nrun 128 96\nrun 0 30\nrun 128 4\nrun 0 30')
        # Enough A inputs to open the normal service; the pre-partner gate
        # must still prevent its PC-menu task from being created.
        emu.send(press_a(3, 180))
        assert menu(emu, symbols) is None, 'PC opened before partner selection'
        emu.send(f'shot {args.output / "no-partner.ppm"}')
        dismiss(emu)
        blocked = snapshot(emu, symbols)
        assert blocked['partner'] == blocked['party'] == blocked['flags'] == 0, blocked
        assert emu.read(symbols['sLockFieldControls']) == 0
    finally:
        emu.close()
    source = args.capture_results / 'captured.sav'
    original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    save = args.output / 'village-pc.sav'
    shutil.copyfile(source, save)
    emu = Emulator(args, 'pc-interface', save)  # No test-write opt-in.
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                 'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
        assert snapshot(emu, symbols) == fixture['continued']
        initial_party, initial_boxes = party(emu, symbols), boxes(emu, symbols)
        assert len(initial_party) == 6 and [p['species'] for p in initial_party] == [7] * 6
        assert list(initial_boxes) == [0] and initial_boxes[0]['species'] == 1
        emu.send('run 32 64\nrun 0 30')
        walk_to(emu, symbols, 128, '3/0', [11, 15])
        approach(emu, symbols)
        emu.send(f'shot {args.output / "station.ppm"}')
        emu.send(press_a(3, 180))
        assert menu(emu, symbols) == 2
        emu.send(f'shot {args.output / "menu.ppm"}')
        emu.send(press_a(1, 180))  # WITHDRAW with six members: reject.
        assert menu(emu, symbols) == 3
        assert party(emu, symbols) == initial_party and boxes(emu, symbols) == initial_boxes
        emu.send(f'shot {args.output / "party-full.ppm"}')
        emu.send('run 2 12\nrun 0 60\nrun 128 12\nrun 0 60\n' + press_a(1, 600))
        assert menu(emu, symbols) is None
        emu.send(press_a(1, 90))  # First party member; STORE context.
        emu.send(press_a(1, 180))  # Choose destination box.
        emu.send(press_a(1, 600))  # Confirm BOX1.
        emu.send(f'shot {args.output / "deposited.ppm"}')
        leave_storage(emu, symbols)
        deposited_party, deposited_boxes = party(emu, symbols), boxes(emu, symbols)
        assert snapshot(emu, symbols)['party'] == len(deposited_party) == 5
        assert list(deposited_boxes) == [0, 1]
        assert deposited_boxes[0] == initial_boxes[0]
        assert deposited_boxes[1] == initial_party[0]
        assert deposited_party == initial_party[1:]
        # Select WITHDRAW and retrieve Tatupedra from the first box slot.
        emu.send('run 64 12\nrun 0 60\n' + press_a(1, 600))
        emu.send(press_a(1, 90))
        emu.send(f'shot {args.output / "withdraw-context.ppm"}')
        emu.send(press_a(1, 600))
        emu.send(f'shot {args.output / "withdrawn.ppm"}')
        leave_storage(emu, symbols)
        final_party, final_boxes = party(emu, symbols), boxes(emu, symbols)
        assert snapshot(emu, symbols)['party'] == len(final_party) == 6
        assert final_party[:5] == deposited_party and final_party[5] == initial_boxes[0]
        assert final_boxes == {1: deposited_boxes[1]}
        assert emu.read(symbols['gPlayerParty'] + 500 + 0x54) == 3
        assert len(final_party) + len(final_boxes) == 7, 'lost/duplicated creature'
        emu.send('run 2 12\nrun 0 180')  # Close the outer PC menu.
        assert menu(emu, symbols) is None
        assert emu.read(symbols['sLockFieldControls']) == 0
        assert emu.read(symbols['sGlobalScriptContextStatus']) == 2
        before = snapshot(emu, symbols)
        assert before == dict(partner=1, flags=1, keyitem=0, party=6, starter=1,
                              map='3/0', position=[13, 15]), before
        assert capsules(emu, symbols) == 4
        emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                 + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\nrun 1 12\nrun 0 600')
    finally:
        emu.close()
    emu = Emulator(args, 'continue-pc', save)
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                 'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
        assert snapshot(emu, symbols) == before
        assert party(emu, symbols) == final_party and boxes(emu, symbols) == final_boxes
        assert capsules(emu, symbols) == 4
        emu.send(f'shot {args.output / "continued.ppm"}')
    finally:
        emu.close()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == original_hash, 'source save modified'
    report = dict(rom_sha1=digest, result='PASS', source_save_sha256=original_hash,
                  source_full_party_is_synthetic=True, interface_test_writes=False,
                  pre_partner_gate='PASS', full_party_withdrawal_rejected=True,
                  counts_initial=dict(party=6, pc=1), counts_after_deposit=dict(party=5, pc=2),
                  counts_after_withdraw=dict(party=6, pc=1), withdrawn_species=1, withdrawn_level=3,
                  deposited_species=7, species_exp_identity_checksum_preserved=True,
                  normal_save_continue=True, scope='Native village-PC menu, STORE and WITHDRAW, '
                  'using a save sourced from synthetic full-party capture. No writes/savestates '
                  'in the UI test. Does not validate natural acquisition of six members, '
                  'full PC, every option/box or full interface translation.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print('village PC gate/deposit/withdraw/save/Continue: PASS', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'capture-results', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
