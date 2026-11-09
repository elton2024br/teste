"""Normal menu saves after each starter; not a full stone-mission test."""
import argparse
import hashlib
import json
from pathlib import Path

from check_intro import Emulator
from check_starters import bootstrap, press_a, progress


def state(emulator):
    line = emulator.send('progress')[0]
    assert line.endswith('map=3/0'), ('expected village', line)
    return progress(line)


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    partners = [('capivagua', 0, 1), ('ararafogo', 1, 2), ('tatupedra', 2, 0)]
    for name, _, _ in partners:
        assert not (args.output / (name + '.sav')).exists(), 'Use a fresh output directory.'
    results = []
    for name, down, expected in partners:
        save = args.output / (name + '.sav')
        emu = Emulator(args, name + '-save', save)
        try:
            emu.send(bootstrap() + 'run 128 12\nrun 0 30\n' * down + press_a(12))
            before = state(emu)
            assert before == dict(partner=1, flags=1, keyitem=0, party=1, starter=expected), before
            # Repeated guide interactions can finish on either page of its text.
            # B dismisses both pages without starting another conversation.
            emu.send('run 2 12\nrun 0 180\n' * 3)
            # With a partner and no Pokedex, SALVAR is the fourth menu entry.
            emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                     + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 600\n')
            emu.send(f'shot {args.output / (name + "-saved.ppm")}')
        finally:
            emu.close()
        # mGBA can append its 16-byte RTC buffer to the 128 KiB flash save.
        assert save.stat().st_size in (131072, 131088), (name, 'invalid native save size')
        # A separate core/process must load the ordinary save, not a savestate.
        emu = Emulator(args, name + '-continue', save)
        try:
            emu.send('run 0 300\nrun 8 20\nrun 0 100\n')
            emu.send(f'shot {args.output / (name + "-continue-menu.ppm")}')
            emu.send('run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200\n')
            restored = state(emu)
            assert restored == before, (name, before, restored)
            # Interact with the guide again: no duplicate partner or reset.
            emu.send(press_a(8))
            repeated = state(emu)
            assert repeated == before, (name, 'repeat interaction after Continue', repeated)
            emu.send(f'shot {args.output / (name + "-continued.ppm")}')
        finally:
            emu.close()
        results.append(dict(partner=name, result='PASS', before=before,
                            restored=restored, repeated=repeated, save_bytes=save.stat().st_size))
        print(name + ': save/Continue PASS', flush=True)
    report = dict(rom_sha1=hashlib.sha1(args.rom.read_bytes()).hexdigest(), cases=results,
                  scope='Village saves after partner/supplies and repeated guide interaction; '
                        'not full mission, capture, defeat, inventory-full or post-stone saves.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
