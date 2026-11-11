"""Exercise the Amazon intro, identity choices and a real save/restart cycle."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from intro_flow import new_game


class Emulator:
    def __init__(self, args, label, save=None, test_writes=False):
        command = [str(args.runner), str(args.rom), '--symbols', str(args.symbols)]
        if save:
            command += ['--save', str(save)]
        if test_writes:
            command += ['--test-writes', 'enabled']
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True, bufsize=1)
        self.log = ['TEST FIXTURE WRITES ENABLED'] if test_writes else []
        self.logfile = args.output / (label + '.log')

    def send(self, commands):
        answers = []
        for command in commands.splitlines():
            self.proc.stdin.write(command + '\n')
            self.proc.stdin.flush()
            answer = self.proc.stdout.readline().strip()
            assert answer, ('emulator stopped', command)
            self.log += [command, answer]
            answers.append(answer)
        return answers

    def read(self, address, bits=8):
        return int(self.send(f'read{bits} {address:08x}')[0].split()[-1], 16)

    def close(self):
        self.proc.stdin.write('quit\n')
        self.proc.stdin.flush()
        _, errors = self.proc.communicate(timeout=20)
        self.logfile.write_text('\n'.join(self.log) + '\n' + errors)
        assert self.proc.returncode == 0 and not errors, (self.proc.returncode, errors)


def text(emulator, address):
    # The test uses uppercase ASCII names; the engine's A-Z glyphs are BB-D4.
    encoded = [emulator.read(address + index) for index in range(8)]
    return ''.join(chr(value - 0xBB + ord('A')) for value in encoded[:encoded.index(0xFF)])


def identity(emulator, symbols):
    block1 = emulator.read(symbols['gSaveBlock1Ptr'], 32)
    block2 = emulator.read(symbols['gSaveBlock2Ptr'], 32)
    return {'name': text(emulator, block2), 'gender': emulator.read(block2 + 8),
            'sam': text(emulator, block1 + 0x3A4C),
            'progress': emulator.send('progress')[0]}


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    symbols = {parts[2]: int(parts[0], 16) for line in args.symbols.read_text().splitlines()
               if len(parts := line.split()) == 3}
    results = []
    save = args.output / 'fresh-normal.sav'
    assert not save.exists(), 'Choose a new output directory to ensure a fresh game/save.'
    for label, gender, reject, empty, expected in [
        ('male-custom', 0, False, False, 'A'),
        ('female-custom', 1, False, False, 'A'),
        ('rename-after-no', 0, True, False, 'B'),
        ('male-empty-default', 0, False, True, 'CAIO'),
        ('female-empty-default', 1, False, True, 'BIA'),
    ]:
        emu = Emulator(args, label, save if label == 'male-custom' else None)
        try:
            emu.send(new_game(gender=gender, reject_name=reject, empty_name=empty))
            state = identity(emu, symbols)
            emu.send(f'shot {args.output / (label + ".ppm")}')
            assert state['name'] == expected and state['gender'] == gender, state
            assert state['sam'] == 'SAM' and state['progress'].endswith('map=4/0'), state
            assert 'partner=0 flags=00 keyitem=0 party=0' in state['progress'], state
            if label == 'male-custom':
                # Select SALVAR in the game menu, accept the prompt and wait.
                emu.send('run 8 12\nrun 0 60\nrun 128 12\nrun 0 20\n'
                         'run 128 12\nrun 0 20\nrun 1 12\nrun 0 240\n'
                         'run 1 12\nrun 0 600\n')
            results.append({'case': label, 'result': 'PASS', **state})
        finally:
            emu.close()
        print(label + ': PASS', flush=True)
    emu = Emulator(args, 'continue-new-process', save)
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n')
        emu.send(f'shot {args.output / "continue-menu.ppm"}')
        emu.send('run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200\n')
        restored = identity(emu, symbols)
        assert restored['name'] == 'A' and restored['gender'] == 0, restored
        assert restored['sam'] == 'SAM' and restored['progress'].endswith('map=4/0'), restored
        emu.send(f'shot {args.output / "continued.ppm"}')
        results.append({'case': 'ordinary-save-new-process', 'result': 'PASS', **restored})
    finally:
        emu.close()
    print('ordinary-save-new-process: PASS', flush=True)
    report = {'rom_sha1': hashlib.sha1(args.rom.read_bytes()).hexdigest(),
              'cases': results, 'scope': 'Intro and a house save/restart; not the full stone mission.'}
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
