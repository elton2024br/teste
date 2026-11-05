"""Fresh-game starter regressions. Does not certify the full stone mission."""
import argparse
import json
from pathlib import Path
import re
import subprocess


def press_a(count, wait=180):
    return (f"run 1 30\nrun 0 {wait}\n") * count


def bootstrap():
    # Recorded introductory inputs for this source revision; assertions detect drift.
    return (
        "run 0 1502\nrun 8 20\nrun 0 280\n"
        + "run 1 12\nrun 0 45\n" * 12
        + "run 1 12\nrun 0 60\n" * 18
        + "run 1 12\nrun 0 90\n" * 25
        + "run 128 12\nrun 0 15\nrun 1 12\nrun 0 90\n"
        + "run 1 12\nrun 0 100\n" * 12
        + "run 1 12\nrun 0 45\n" * 7
        + "run 16 64\nrun 64 64\nrun 0 90\nrun 32 16\nrun 0 90\nrun 128 64\nrun 0 30\n"
        + press_a(30, 90)
        + "run 128 32\nrun 0 30\nrun 32 16\nrun 0 30\nrun 128 64\nrun 0 180\n"
        + "run 16 32\nrun 0 30\n" + press_a(3)
    )


def progress(line):
    values = dict(re.findall(r"(\w+)=([^ ]+)", line))
    return {key: int(values[key], 16 if key == "flags" else 10)
            for key in ("partner", "flags", "keyitem", "party", "starter")}


def check(args):
    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    for name, down, expected in [("capivagua", 0, 1), ("ararafogo", 1, 2), ("tatupedra", 2, 0)]:
        commands = bootstrap()
        commands += "progress\n"  # Still at the choice menu, no grant.
        commands += "run 2 30\nrun 0 90\nprogress\n"  # Cancel via B.
        commands += press_a(3)  # Reopen introduction and choice.
        commands += "run 128 12\nrun 0 30\n" * down
        commands += press_a(4) + "progress\n"
        commands += press_a(8) + "progress\n"  # Supplies and repeated interaction.
        commands += f"shot {args.output / (name + '.ppm')}\nquit\n"
        proc = subprocess.run([str(args.runner), str(args.rom), "--symbols", str(args.symbols)],
                              input=commands, capture_output=True, text=True, timeout=120)
        (args.output / (name + '.log')).write_text(proc.stdout + proc.stderr)
        states = [progress(line) for line in proc.stdout.splitlines() if line.startswith("PROGRESS base=")]
        assert proc.returncode == 0, (name, proc.returncode, proc.stderr)
        assert not proc.stderr, (name, proc.stderr)
        assert len(states) == 4, (name, states)
        assert states[0]['partner'] == states[0]['party'] == 0, (name, 'premature grant', states)
        assert states[1]['partner'] == states[1]['party'] == 0, (name, 'cancel grants creature', states)
        assert states[2]['partner'] == 1 and states[2]['party'] == 1 and states[2]['starter'] == expected, (name, states)
        assert states[3]['party'] == 1 and states[3]['starter'] == expected and states[3]['flags'] & 1, (name, 'duplicate/supplies', states)
        results.append({'starter': name, 'result': 'PASS', 'states': states})
        print(name + ': PASS', flush=True)
    (args.output / 'results.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', type=Path, required=True)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--symbols', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    check(parser.parse_args())
