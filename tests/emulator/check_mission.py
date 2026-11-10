"""Fresh stone missions with normal inputs and post-mission save/Continue."""
import argparse
import hashlib
import json
from pathlib import Path

from check_intro import Emulator
from check_starters import bootstrap, press_a
from check_defeat_recovery import dismiss, reach_control, snapshot


def fight(emu, symbols):
    # Both partners start with their elemental attack in slot 1. Resolve the
    # unique move-input handler, avoiding duplicate static action-handler names.
    for cycle in range(300):
        handler = emu.read(symbols['gBattlerControllerFuncs'], 32) & ~1
        if handler == symbols['HandleInputChooseMove']:
            cursor = emu.read(symbols['gMoveSelectionCursor'])
            assert cursor in (0, 1), cursor
            if cursor == 0:
                emu.send('run 16 12\nrun 0 20')
        emu.send(press_a(1, 90))
        current = snapshot(emu, symbols)
        assert current['map'] == '1/0', ('lost/left mission', current)
        if current['flags'] & 2:
            assert emu.read(symbols['gBattleOutcome']) == 1, 'expected B_OUTCOME_WON'
            dismiss(emu)
            return cycle + 1
    raise AssertionError('agent battle did not finish within 300 input cycles')


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    cases = []
    for name, down, starter in [('ararafogo', 1, 2), ('tatupedra', 2, 0)]:
        save = args.output / (name + '.sav')
        emu = Emulator(args, name + '-mission', save)
        try:
            emu.send(bootstrap() + 'run 128 12\nrun 0 30\n' * down + press_a(12))
            dismiss(emu)
            initial = reach_control(emu, symbols)
            assert initial == dict(partner=1, flags=1, keyitem=0, party=1, starter=starter,
                                   map='1/0', position=[12, 14]), initial
            emu.send(press_a(4))
            assert snapshot(emu, symbols) == initial, 'control unlocked before victory'
            dismiss(emu)
            emu.send('run 32 16\nrun 0 30\nrun 32 4\nrun 0 30\n' + press_a(4, 300))
            cycles = fight(emu, symbols)
            victory = snapshot(emu, symbols)
            assert victory['flags'] == 3 and victory['keyitem'] == 0, victory
            emu.send('run 16 16\nrun 0 30\nrun 64 4\nrun 0 30\n' + press_a(4))
            dismiss(emu)
            opened = snapshot(emu, symbols)
            assert opened['flags'] == 7 and opened['keyitem'] == 0, opened
            emu.send('run 32 16\nrun 0 30\nrun 64 128\nrun 0 30')
            assert snapshot(emu, symbols)['position'] == [11, 6], 'bridge was not passable'
            emu.send(press_a(4))
            dismiss(emu)
            stone = snapshot(emu, symbols)
            assert stone['flags'] == 15 and stone['keyitem'] == 361, stone
            emu.send(f'shot {args.output / (name + "-stone.ppm")}')
            emu.send('run 128 700\nrun 0 90')
            returned = snapshot(emu, symbols)
            assert returned['map'] == '3/0' and returned['position'] == [11, 5], returned
            emu.send('run 128 64\nrun 0 30\nrun 32 48\nrun 0 30\nrun 64 4\nrun 0 30'
                     + '\n' + press_a(4))
            emu.send(f'shot {args.output / (name + "-guide.ppm")}')
            dismiss(emu)
            before = snapshot(emu, symbols)
            assert before == dict(partner=1, flags=15, keyitem=361, party=1, starter=starter,
                                  map='3/0', position=[8, 9]), before
            emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                     + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 600\n')
        finally:
            emu.close()
        assert save.stat().st_size in (131072, 131088), 'invalid native save size'
        emu = Emulator(args, name + '-continue', save)
        try:
            emu.send('run 0 300\nrun 8 20\nrun 0 100')
            emu.send(f'shot {args.output / (name + "-continue-menu.ppm")}')
            emu.send('run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
            continued = snapshot(emu, symbols)
            assert continued == before, (before, continued)
            emu.send(f'shot {args.output / (name + "-continued.ppm")}')
        finally:
            emu.close()
        cases.append(dict(partner=name, result='PASS', battle_input_cycles=cycles,
                          initial=initial, victory=victory, opened=opened, stone=stone,
                          before_save=before, continued=continued, save_bytes=save.stat().st_size))
        print(name + ': mission/save/Continue PASS', flush=True)
    report = dict(rom_sha1=hashlib.sha1(args.rom.read_bytes()).hexdigest(), cases=cases,
                  scope='Fresh games, locked control, agent victory, bridge crossing, stone, '
                        'village guide and ordinary save/Continue in new processes. '
                        'No capture, full inventory or stone quantity/duplication checks.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
