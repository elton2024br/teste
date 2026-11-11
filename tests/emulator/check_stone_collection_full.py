"""Synthetic pre-collection/full-key-pocket fixture; not natural gameplay."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from check_intro import Emulator
from check_starters import press_a
from check_defeat_recovery import dismiss, snapshot
from check_stone_repair import pocket, set_pocket_fixture
from check_stone_revisit import walk_to


def stone_present(emu, symbols):
    # Pinned ObjectEvent layout: active bit, localId/mapNum/mapGroup at +8.
    for i in range(16):
        obj = symbols['gObjectEvents'] + i * 36
        if emu.read(obj, 32) & 1 and emu.read(obj + 8, 32) & 0xFFFFFF == 0x01000D:
            return True  # LOCALID_AMAZON_STONE=13, forest group 1 / map 0.
    return False


def interact(emu, symbols):
    emu.send(press_a(4))
    dismiss(emu)
    assert emu.read(symbols['sLockFieldControls']) == 0, 'controls remain locked'
    state = snapshot(emu, symbols)
    assert state['map'] == '1/0' and state['position'] == [11, 6], state
    assert state['party'] == 1 and state['starter'] == 2, state
    return state


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
    save = args.output / 'collection.sav'
    shutil.copyfile(source, save)
    symbols = {p[2]: int(p[0], 16) for line in args.symbols.read_text().splitlines()
               if len(p := line.split()) == 3}
    items = json.loads((args.rom.parent / 'src/data/items.json').read_text())['items']
    assert len(items) == 375 and items[361]['itemId'] == 'ITEM_TOWN_MAP'
    filler = [i for i, item in enumerate(items) if item['pocket'] == 'POCKET_KEY_ITEMS' and i != 361][:30]
    assert len(set(filler)) == 30
    emu = Emulator(args, 'collection-fixture', save, test_writes=True)
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                 'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
        assert snapshot(emu, symbols) == case['continued']
        set_pocket_fixture(emu, symbols, filler)
        block = emu.read(symbols['gSaveBlock1Ptr'], 32)
        # Explicit synthetic setup: clear only WATER_STONE in the flag word.
        # Partner, supplies, agent victory and control remain unchanged.
        address = block + 0xF74
        word = emu.read(address, 32)
        emu.send(f'write32 {address:08x} {word & ~0x800:08x}')
        assert snapshot(emu, symbols)['flags'] == 7
        prepared = pocket(emu, symbols)
        emu.send('run 16 48\nrun 0 30')
        walk_to(emu, symbols, 64, '1/0', [11, 6])
        assert stone_present(emu, symbols), 'stone object did not spawn'
        refused = []
        for _ in range(3):
            state = interact(emu, symbols)
            assert state['flags'] == 7, ('premature stone completion', state)
            assert stone_present(emu, symbols), 'full-bag attempt removed object'
            assert pocket(emu, symbols) == prepared, 'full-bag attempt changed items'
            refused.append(state['flags'])
        emu.send(f'shot {args.output / "full-refused.ppm"}')
        # Free exactly one slot artificially; collection itself uses normal A.
        set_pocket_fixture(emu, symbols, filler[:-1] + [0])
        collected = interact(emu, symbols)
        assert collected['flags'] == 15 and not stone_present(emu, symbols), collected
        expected = [(item, 1) for item in filler[:-1]] + [(361, 1)]
        assert pocket(emu, symbols) == expected, 'collection lost/duplicated an item'
        interact(emu, symbols)
        assert pocket(emu, symbols) == expected and not stone_present(emu, symbols)
        emu.send(f'shot {args.output / "collected.ppm"}')
        # Save directly in the forest; copied native saves need overwrite confirmation.
        emu.send('run 8 12\nrun 0 60\n' + 'run 128 12\nrun 0 20\n' * 3
                 + 'run 1 12\nrun 0 240\nrun 1 12\nrun 0 240\nrun 1 12\nrun 0 600\n')
    finally:
        emu.close()
    emu = Emulator(args, 'continue-forest', save)
    try:
        emu.send('run 0 300\nrun 8 20\nrun 0 100\n'
                 'run 1 30\nrun 0 1200\nrun 2 30\nrun 0 1200')
        continued = snapshot(emu, symbols)
        assert continued == collected, (collected, continued)
        assert pocket(emu, symbols) == expected and not stone_present(emu, symbols)
        # Cross the restored bridge on the saved forest map, without writes.
        south = walk_to(emu, symbols, 128, '1/0', [11, 12])
        assert south['flags'] == 15 and pocket(emu, symbols) == expected
        emu.send(f'shot {args.output / "continued-bridge.ppm"}')
    finally:
        emu.close()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash, 'source save changed'
    report = dict(rom_sha1=digest, result='PASS', synthetic_fixture=True,
                  fixture_writes=['key-item pocket', 'clear water-stone flag before map entry'],
                  source_save_sha256=source_hash, filler_ids=filler,
                  full_refusal_flags=refused, object_preserved_on_refusal=True,
                  collection_flags=collected['flags'], object_removed_on_success=True,
                  stone_quantity=1, other_items_preserved=29, repeated_collection_unchanged=True,
                  forest_save_continue=True, continued=continued, crossed_bridge_after_continue=True,
                  scope='Artificial pre-collection/full-key-pocket state with Ararafogo; '
                        'normal collection script, refusal/retry, no duplication, native forest '
                        'save/Continue and bridge crossing. Not naturally reachable fullness, '
                        'other partners/pockets or every save path.')
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print('synthetic full-pocket collection/forest save/Continue: PASS', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['runner', 'rom', 'symbols', 'mission-results', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    check(parser.parse_args())
