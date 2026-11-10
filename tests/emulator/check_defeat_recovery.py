"""Lose normally, save after recovery, restart and verify the river stays locked."""
import argparse
import hashlib
import json
from pathlib import Path

from check_intro import Emulator
from check_starters import bootstrap, press_a, progress


def position(emu, symbols):
    # Offsets match ObjectEvent/PlayerAvatar in the pinned FireRed source.
    index = emu.read(symbols['gPlayerAvatar'] + 5)
    assert index < 16, index
    coords = emu.read(symbols['gObjectEvents'] + index * 36 + 0x10, 32)
    return [(coords & 65535) - 7, (coords >> 16) - 7]


def snapshot(emu, symbols):
    line = emu.send('progress')[0]
    return dict(progress(line), map=line.split('map=')[1], position=position(emu, symbols))


def dismiss(emu):
    emu.send('run 2 12\nrun 0 180\n' * 3)


def reach_control(emu, symbols):
    # From (8,9) in the village, the central path avoids wild grass.
    emu.send('run 16 48\nrun 0 30\nrun 64 700\nrun 0 30\n')
    assert position(emu, symbols) == [11, 11], position(emu, symbols)
    emu.send('run 128 48\nrun 0 30\nrun 16 16\nrun 0 30\nrun 64 4\nrun 0 30\n')
    state = snapshot(emu, symbols)
    assert state['map'] == '1/0' and state['position'] == [12, 14], state
    return state


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    # A reused output directory can conceal logs from an earlier run.
    assert not any(args.output.iterdir()), 'Use a fresh output directory.'
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    save = args.output / 'recovered.sav'
    emu = Emulator(args, 'defeat-recovery', save)
    try:
        # Fresh Ararafogo; use the first attack throughout this loss scenario.
        emu.send(bootstrap() + 'run 128 12\nrun 0 30\n' + press_a(12))
        dismiss(emu)
        initial = reach_control(emu, symbols)
        assert initial['partner'] == initial['party'] == initial['flags'] == 1, initial
        assert initial['starter'] == 2 and initial['keyitem'] == 0, initial
        emu.send(press_a(4))
        locked_before = snapshot(emu, symbols)
        assert locked_before == initial, (initial, locked_before)
        emu.send(f'shot {args.output / "control-locked-before.ppm"}')
        dismiss(emu)
        emu.send('run 32 16\nrun 0 30\nrun 32 4\nrun 0 30\n')
        emu.send(press_a(4, 300))
        for turns in range(80):
            emu.send(press_a(1, 300))
            current = snapshot(emu, symbols)
            assert not current['flags'] & 2, ('unexpected victory in loss scenario', current)
            if current['map'] == '4/0':
                break
        else:
            raise AssertionError(('did not recover within 80 input cycles', current))
        # Map transition precedes the automatic recovery dialogue and heal.
        emu.send('run 0 300')
        # The rush-home screen is a task, followed by Mom's script. Both must
        # finish before movement is possible. Stop before A talks to Mom again.
        for _ in range(40):
            if (emu.read(symbols['sGlobalScriptContextStatus']) == 2
                    and emu.read(symbols['sLockFieldControls']) == 0
                    and emu.read(symbols['gMain'] + 4, 32) & ~1 == symbols['CB2_Overworld']):
                break
            emu.send(press_a(1, 300))
        else:
            raise AssertionError('recovery dialogue did not finish')
        recovered = snapshot(emu, symbols)
        assert recovered == dict(partner=1, party=1, flags=1, starter=2, keyitem=0,
                                 map='4/0', position=[8, 5]), recovered
        assert emu.read(symbols['gBattleOutcome']) == 2, 'expected B_OUTCOME_LOST'
        # Current HP/max HP are unencrypted fields in struct Pokemon.
        party = symbols['gPlayerParty']
        hp = emu.read(party + 0x56) | (emu.read(party + 0x57) << 8)
        max_hp = emu.read(party + 0x58) | (emu.read(party + 0x59) << 8)
        assert hp == max_hp and hp > 0, (hp, max_hp)
        emu.send(f'shot {args.output / "recovered-house.ppm"}')
        # No Pokedex; the partner adds POKEMON before BAG, PLAYER and SALVAR.
        emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                 + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 600\n')
        emu.send(f'shot {args.output / "saved-after-defeat.ppm"}')
    finally:
        emu.close()
    assert save.stat().st_size in (131072, 131088), 'invalid native save size'
    # Start a new emulator process. No savestate or memory writes are used.
    emu = Emulator(args, 'continue-after-defeat', save)
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n')
        emu.send(f'shot {args.output / "continue-menu.ppm"}')
        emu.send('run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200\n')
        continued = snapshot(emu, symbols)
        assert continued == recovered, ('save did not preserve recovery', recovered, continued)
        continued_hp = emu.read(party + 0x56) | (emu.read(party + 0x57) << 8)
        continued_max_hp = emu.read(party + 0x58) | (emu.read(party + 0x59) << 8)
        assert continued_hp == hp and continued_max_hp == max_hp, (continued_hp, continued_max_hp)
        emu.send(f'shot {args.output / "continued-house.ppm"}')
        # Walk out normally and retry the same control after the defeat.
        # Respawn is (8,5), unlike the new-game start. The south-arrow exit
        # metatile is at (4,8); the adjacent tile at (5,8) is ordinary floor.
        emu.send('run 128 32\nrun 0 30')
        assert position(emu, symbols) == [8, 7], position(emu, symbols)
        emu.send('run 32 64\nrun 0 30')
        assert position(emu, symbols) == [4, 7], position(emu, symbols)
        emu.send('run 128 48\nrun 0 180\nrun 128 16\nrun 0 20\n'
                 'run 16 32\nrun 0 20\nrun 64 4\nrun 0 30\n')
        outside = snapshot(emu, symbols)
        assert outside['map'] == '3/0' and outside['position'] == [8, 9], outside
        reach_control(emu, symbols)
        emu.send(press_a(4))
        locked_after = snapshot(emu, symbols)
        assert locked_after == locked_before, (locked_before, locked_after)
        emu.send(f'shot {args.output / "control-locked-after.ppm"}')
        dismiss(emu)
        emu.send('run 32 16\nrun 0 30')
        assert position(emu, symbols) == [11, 14], 'movement still locked after retry'
    finally:
        emu.close()
    report = dict(rom_sha1=hashlib.sha1(args.rom.read_bytes()).hexdigest(), result='PASS',
                  partner='ararafogo', battle_outcome=2, input_cycles=turns + 1,
                  locked_before=locked_before, recovered=recovered, hp=hp, max_hp=max_hp,
                  continued=continued, continued_hp=continued_hp, continued_max_hp=continued_max_hp,
                  save_bytes=save.stat().st_size, locked_after=locked_after,
                  scope='Fresh game, agent loss, house respawn/healing, flags unchanged and '
                        'normal save/Continue in a new process; control still locked after walking back. '
                        'No full victory mission, post-stone save or other partners.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print('ararafogo defeat/recovery/save/Continue: PASS', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
