"""Revisit the stone and caregiver using copies of native mission-test saves."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import dismiss, snapshot


def stone_quantity(emu, symbols):
    # Pinned FireRed SaveBlock1/2 and ItemSlot layouts; item IDs are plain,
    # quantities are XORed with the low half of the per-save encryption key.
    block1 = emu.read(symbols['gSaveBlock1Ptr'], 32)
    block2 = emu.read(symbols['gSaveBlock2Ptr'], 32)
    assert 0x02000000 <= block1 < 0x02040000, block1
    assert 0x02000000 <= block2 < 0x02040000, block2
    key = emu.read(block2 + 0xF20, 32) & 65535
    slots = [emu.read(block1 + 0x3B8 + index * 4, 32) for index in range(30)]
    quantities = [(slot >> 16) ^ key for slot in slots if slot & 65535 == 361]
    assert quantities == [1], ('stone missing, duplicated or wrong quantity', quantities)
    return sum(quantities)


def walk_to(emu, symbols, direction, map_id, xy):
    for _ in range(90):
        current = snapshot(emu, symbols)
        if current['map'] == map_id and current['position'] == xy:
            return current
        emu.send(f'run {direction} 16\nrun 0 60')
    raise AssertionError(('destination not reached', map_id, xy, current))


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    fixture = json.loads((args.mission_results / 'results.json').read_text())
    assert fixture['rom_sha1'] == digest, 'Mission fixtures must match this ROM build.'
    assert [c['partner'] for c in fixture['cases']] == ['ararafogo', 'tatupedra']
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    cases = []
    for case in fixture['cases']:
        assert case['result'] == 'PASS', case
        name = case['partner']
        source = args.mission_results / (name + '.sav')
        original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        save = args.output / (name + '.sav')
        shutil.copyfile(source, save)
        emu = Emulator(args, name + '-revisit', save)
        try:
            emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                     'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
            initial = snapshot(emu, symbols)
            assert initial == case['continued'], (initial, case['continued'])
            counts = [stone_quantity(emu, symbols)]
            emu.send('run 16 48\nrun 0 30')
            north = walk_to(emu, symbols, 64, '1/0', [11, 6])
            assert north['flags'] == 15, north
            # Returning from another process/map must recreate the open bridge.
            # The stone object is gone; retry A at its old location three times.
            for _ in range(3):
                emu.send(press_a(4))
                dismiss(emu)
                counts.append(stone_quantity(emu, symbols))
            emu.send(f'shot {args.output / (name + "-stone-revisited.ppm")}')
            south = walk_to(emu, symbols, 128, '3/0', [11, 15])
            assert south['flags'] == 15, south
            # Face the caregiver at (11,16), heal repeatedly with the stone held.
            for _ in range(3):
                emu.send(press_a(6))
                dismiss(emu)
                counts.append(stone_quantity(emu, symbols))
                assert emu.read(symbols['sLockFieldControls']) == 0, 'caregiver still locks controls'
            final = snapshot(emu, symbols)
            assert final['flags'] == 15 and final['keyitem'] == 361, final
            assert final['party'] == initial['party'] == 1, final
            emu.send(f'shot {args.output / (name + "-caregiver-revisited.ppm")}')
        finally:
            emu.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == original_hash, 'source save modified'
        cases.append(dict(partner=name, result='PASS', source_save_sha256=original_hash,
                          initial=initial, north=north, final=final, stone_quantities=counts,
                          stone_retries=3, caregiver_interactions=3))
        print(name + ': bridge/stone quantity/revisits PASS', flush=True)
    report = dict(rom_sha1=digest, cases=cases,
                  scope='Copies of ordinary saves from check_mission.py; bridge reconstructed '
                        'after Continue/map entry, stone remains a single slot/quantity 1 after '
                        'three old-location retries and three caregiver interactions. '
                        'No full inventory, missing-stone repair, capture or new save cycle.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'mission-results', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
