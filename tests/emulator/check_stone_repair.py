"""Synthetic missing-stone/full-key-pocket fixtures; not natural gameplay."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import dismiss, snapshot


def pocket(emu, symbols):
    block = emu.read(symbols['gSaveBlock1Ptr'], 32)
    block2 = emu.read(symbols['gSaveBlock2Ptr'], 32)
    assert 0x02000000 <= block <= 0x0203E000, block
    assert 0x02000000 <= block2 <= 0x0203F000, block2
    key = emu.read(block2 + 0xF20, 32) & 65535
    words = [emu.read(block + 0x3B8 + i * 4, 32) for i in range(30)]
    return [(w & 65535, (w >> 16) ^ key) for w in words]


def set_pocket_fixture(emu, symbols, ids):
    assert len(ids) == 30
    block = emu.read(symbols['gSaveBlock1Ptr'], 32)
    block2 = emu.read(symbols['gSaveBlock2Ptr'], 32)
    key = emu.read(block2 + 0xF20, 32) & 65535
    for i, item in enumerate(ids):
        word = item | (((1 if item else 0) ^ key) << 16)
        emu.send(f'write32 {block + 0x3B8 + i * 4:08x} {word:08x}')
    assert pocket(emu, symbols) == [(item, 1 if item else 0) for item in ids]


def interact(emu, symbols):
    emu.send(press_a(6))
    dismiss(emu)
    assert emu.read(symbols['sLockFieldControls']) == 0, 'controls still locked'
    current = snapshot(emu, symbols)
    assert current['flags'] == 15 and current['party'] == 1, current
    assert current['position'] == [11, 15] and current['map'] == '3/0', current


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    digest = hashlib.sha1(args.rom.read_bytes()).hexdigest()
    fixtures = json.loads((args.mission_results / 'results.json').read_text())
    assert fixtures['rom_sha1'] == digest
    case = next(c for c in fixtures['cases'] if c['partner'] == 'ararafogo')
    assert case['result'] == 'PASS'
    source = args.mission_results / 'ararafogo.sav'
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    items = json.loads((args.rom.parent / 'src/data/items.json').read_text())['items']
    assert len(items) == 375 and items[361]['itemId'] == 'ITEM_TOWN_MAP'
    filler = [i for i, item in enumerate(items) if item['pocket'] == 'POCKET_KEY_ITEMS' and i != 361][:30]
    assert len(set(filler)) == 30
    # The same command must be rejected without opt-in, outside EWRAM or unaligned.
    for extra, address in [([], '02000000'), (['--test-writes', 'enabled'], '08000000'),
                           (['--test-writes', 'enabled'], '02000001')]:
        proc = subprocess.run([str(args.runner), str(args.rom)] + extra,
                              input=f'write32 {address} 0\n', capture_output=True, text=True, timeout=20)
        assert proc.returncode == 16 and 'write32 requires' in proc.stderr, proc
    results = []
    for name, ids in [('missing', [0] * 30), ('full', filler)]:
        save = args.output / (name + '.sav')
        shutil.copyfile(source, save)
        emu = Emulator(args, name + '-fixture', save, test_writes=True)
        try:
            emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                     'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
            assert snapshot(emu, symbols) == case['continued']
            assert [q for item, q in pocket(emu, symbols) if item == 361] == [1]
            emu.send('run 16 48\nrun 0 30\nrun 128 96\nrun 0 30')
            assert snapshot(emu, symbols)['position'] == [11, 15]
            set_pocket_fixture(emu, symbols, ids)
            prepared = pocket(emu, symbols)
            if name == 'full':
                interact(emu, symbols)
                assert pocket(emu, symbols) == prepared, 'full bag was modified or stone granted'
                emu.send(f'shot {args.output / "full-refused.ppm"}')
                # Free exactly one slot via fixture setup; the next ordinary
                # interaction must recover the stone without losing other items.
                set_pocket_fixture(emu, symbols, filler[:-1] + [0])
            interact(emu, symbols)
            repaired = pocket(emu, symbols)
            assert [q for item, q in repaired if item == 361] == [1], repaired
            expected = [(i, 1) for i in filler[:-1]] + [(361, 1)] if name == 'full' else [(361, 1)] + [(0, 0)] * 29
            assert repaired == expected, ('other items lost/modified', repaired)
            interact(emu, symbols)
            assert pocket(emu, symbols) == repaired, 'repeat caregiver duplicated stone'
            before = snapshot(emu, symbols)
            emu.send(f'shot {args.output / (name + "-repaired.ppm")}')
            emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                     + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\n'
                     + 'run 1 12\nrun 0 600\n')
        finally:
            emu.close()
        # Reopen without fixture writes enabled, using ordinary persistence.
        emu = Emulator(args, name + '-continue', save)
        try:
            emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                     'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
            assert snapshot(emu, symbols) == before, (before, snapshot(emu, symbols))
            assert pocket(emu, symbols) == repaired, 'repair did not persist'
        finally:
            emu.close()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash, 'source save modified'
        results.append(dict(case=name, result='PASS', synthetic_fixture=True,
                            prepared_occupied=sum(item != 0 for item, _ in prepared),
                            repaired_occupied=sum(item != 0 for item, _ in repaired),
                            stone_quantity=1, other_items_preserved=True,
                            full_refusal_checked=name == 'full', normal_save_continue=True))
        print(name + ': synthetic fixture/repair/save/Continue PASS', flush=True)
    report = dict(rom_sha1=digest, source_save_sha256=source_hash, fixture_writes=True,
                  write_guards='PASS', filler_ids=filler, cases=results,
                  scope='Artificial key-pocket fixtures after a completed Ararafogo mission; '
                        'caregiver missing-stone repair, full-pocket refusal, retry after '
                        'freeing one slot, no duplication and ordinary save/Continue. '
                        'Not natural acquisition/fullness, stone-object collection or other pockets.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'mission-results', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
