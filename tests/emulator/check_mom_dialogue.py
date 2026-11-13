"""Guide dialogue in both appearances; healing checked with an explicit HP fixture."""
import argparse
import hashlib
import json
from pathlib import Path

from check_intro import Emulator
from intro_flow import new_game
from check_starters import press_a
from check_defeat_recovery import dismiss, snapshot
from check_capture import capsules


def hp(emu, symbols):
    mon = symbols['gPlayerParty']
    return (emu.read(mon + 0x54, 32) >> 16, emu.read(mon + 0x58, 32) & 65535)


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    cases = []
    for gender in [0, 1]:
        emu = Emulator(args, 'appearance-' + str(gender), test_writes=True)
        try:
            emu.send(new_game(gender=gender))
            initial = snapshot(emu, symbols)
            assert initial['map'] == '4/0' and initial['position'] == [5, 6], initial
            assert initial['partner'] == initial['party'] == initial['flags'] == 0, initial
            # Approach Mom around the table, then inspect each guide page.
            emu.send('run 128 16\nrun 0 30\nrun 16 48\nrun 0 30\nrun 64 32\nrun 0 30')
            assert snapshot(emu, symbols)['position'] == [8, 5]
            for page in range(3):
                emu.send(press_a(1, 300))
                emu.send(f'shot {args.output / (str(gender) + "-guide-" + str(page) + ".ppm")}')
            dismiss(emu)
            guided = snapshot(emu, symbols)
            assert guided == dict(partner=0, flags=0, keyitem=0, party=0, starter=0,
                                  map='4/0', position=[8, 5]), guided
            assert emu.read(symbols['sLockFieldControls']) == 0
            # Exit the house and receive Capivagua from the actual village guide.
            emu.send('run 128 32\nrun 0 30\nrun 32 64\nrun 0 30\n'
                     'run 128 48\nrun 0 180\nrun 128 16\nrun 0 20\n'
                     'run 16 32\nrun 0 20\nrun 64 4\nrun 0 30')
            assert snapshot(emu, symbols)['position'] == [8, 9]
            emu.send(press_a(15))
            dismiss(emu)
            chosen = snapshot(emu, symbols)
            assert chosen == dict(partner=1, flags=1, keyitem=0, party=1, starter=1,
                                  map='3/0', position=[8, 9]), chosen
            assert capsules(emu, symbols) == 5
            # Return through the normal doorway; no progression flags are injected.
            emu.send('run 32 32\nrun 0 30\nrun 64 48\nrun 0 180')
            entered = snapshot(emu, symbols)
            assert entered['map'] == '4/0', entered
            emu.send('run 16 48\nrun 0 30\nrun 64 48\nrun 0 30')
            assert snapshot(emu, symbols)['position'] == [8, 5], snapshot(emu, symbols)
            # Synthetic condition ONLY: reduce party slot 0 HP to 1, preserving
            # the level/mail bytes in this aligned, unencrypted Pokemon word.
            address = symbols['gPlayerParty'] + 0x54
            before_hp, max_hp = hp(emu, symbols)
            assert before_hp == max_hp and max_hp > 1
            word = emu.read(address, 32)
            emu.send(f'write32 {address:08x} {(word & 65535) | (1 << 16):08x}')
            assert hp(emu, symbols) == (1, max_hp)
            emu.send(press_a(1, 300))
            emu.send(f'shot {args.output / (str(gender) + "-rest.ppm")}')
            emu.send(press_a(1, 600))
            emu.send(f'shot {args.output / (str(gender) + "-healed.ppm")}')
            # Stop as soon as the script releases control; extra A presses
            # would start another conversation and another healing cycle.
            for _ in range(12):
                if (emu.read(symbols['sLockFieldControls']) == 0
                        and emu.read(symbols['sGlobalScriptContextStatus']) == 2):
                    break
                emu.send('run 2 12\nrun 0 180')
            else:
                raise AssertionError('healing dialogue did not release control')
            healed = snapshot(emu, symbols)
            assert healed == dict(partner=1, flags=1, keyitem=0, party=1, starter=1,
                                  map='4/0', position=[8, 5]), healed
            assert hp(emu, symbols) == (max_hp, max_hp), hp(emu, symbols)
            assert capsules(emu, symbols) == 5, 'healing charged supplies'
            assert emu.read(symbols['sLockFieldControls']) == 0
            emu.send('run 128 16\nrun 0 30')
            assert snapshot(emu, symbols)['position'] == [8, 6], 'movement still locked'
            cases.append(dict(appearance=gender, result='PASS', before_partner=guided,
                              chosen=chosen, healed=healed, hp_fixture=1, hp_restored=max_hp,
                              capsules_after=5, fixture_writes=['party slot 0 HP only']))
        finally:
            emu.close()
        print('appearance ' + str(gender) + ': guide/partner/HP-fixture healing PASS', flush=True)
    report = dict(rom_sha1=hashlib.sha1(args.rom.read_bytes()).hexdigest(), cases=cases,
                  scope='Both appearances, natural new game/guide partner acquisition and '
                        'normal home interaction; HP=1 prepared artificially only after partner '
                        'selection. No injected partner/progression. Not natural battle damage, '
                        'status/PP recovery, every party size or a new save cycle.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
