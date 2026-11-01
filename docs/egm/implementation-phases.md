# Amazon implementation phases

Authoritative specifications: amazon-expedition.md and amazon-implementation-contract.md. These tasks do not claim implementation or test success.

## Phase 1 — safe starting area

- Pin source/tool inputs and preserve the current 0.2 changes as a source patch.
- Implement the four-map graph, spawn, reciprocal connections and sealed boundaries.
- Initialize respawn before any battle; preserve the house caregiver recovery coordinates.
- Remove inherited opening triggers from the accessible route.
- Exit checks: fresh boot, every required connection/door, no access to unfinished maps, induced defeat returns safely.

## Phase 2 — complete event loop

- Starter preview/cancel/confirm and indexed choice persistence.
- Party-menu flag and one-time capture supplies.
- Trainer defeat enables control; control enables bridge; stone grant follows successful delivery.
- Repeated events and failed grants preserve consistent progression.
- Exit checks: complete the route with temporary assets, lose/retry and return safely.

## Phase 3 — creature/item data

- Replace three starter slots and audit all accessible encounters/trainer parties.
- Integrate complete starter moves, stats, names and disabled unfinished evolutions.
- Integrate the stone's key-item record, icon and non-consuming use handler.
- Exit checks: all three choices, capture, summary/icons, no original creature appearances on the route, inventory consistency.

## Phase 4 — original visual set

- Author complete creature, character, environment, interior and battle assets.
- Validate indexed conversion, frame layout and per-area palette/tile allocations.
- Exit checks: native-resolution screenshots of all visible families and transitions; compare with the intended Amazon direction.

## Phase 5 — release evidence

- Rebuild from pinned inputs and record final hashes.
- Independently apply the cumulative patch with Floating IPS and compare hashes.
- Test normal menu save, close the emulator, reopen with only the ordinary save file, and verify all progression assertions.
- Publish no readiness claim while required checks are failed or unrun. Package patch, source changes, instructions and evidence; omit the base ROM.
