# Bounded readiness recheck

Two fresh-context reviewers completed one follow-up pass: implementation readiness and codebase details. Both confirmed persona, standard, full target/contract and previous report reads, with source inspection. No builds, gameplay or ordinary-save tests were executed.

## Resolved source-grounded issues

The reviewers confirmed that the corrected starter encoding, party-menu flag, startup checkpoint, recovery coordinates, item 361 schema, abbreviated item label, encounter structure, battle-terrain selection, mGBA API availability and pinned ROM source are compatible with inspected code. This is design/source evidence, not a passing game test.

## Findings and subsequent design dispositions

- Readiness reviewer: indexed warp records and post-transition positions were ambiguous. Explicit paired warp index 0 records and arrival semantics were added.
- Both reviewers: house secondary tileset was not included. The contract now explicitly retains GenericBuilding1, adds its graphics/palette/metatile outputs, and binds every map's primary/secondary pair.
- Readiness reviewer: deterministic route/indoor/encounter masks were missing. The contract now supplies boundaries, walkable routes, obstacles, encounter patches and bridge geometry.
- Readiness reviewer: starter UI primitives and capture-item identifier were missing. The contract now specifies multichoice, picture, confirmation, index mapping and five ITEM_POKE_BALL.
- Code reviewer: hidden acquired-stone object made repair unreachable. A guarded repair interaction is now bound to the always-reachable dock caregiver.
- Code reviewer: reused Town Map ID exposes an unrelated help topic. src/help_system.c was added to the manifest and the topic must be replaced/disabled.

The follow-up reviewers read the contract before all these final clarifications were appended. These dispositions are documented author corrections, not an independent claim that the reviewers subsequently passed the revised version. The one-re-audit limit is reached. Do not label remaining runtime checks passed.

## Remaining implementation evidence

Author and inspect the original artwork, implement the specified map/event/item/save changes, validate allocations, build from pinned inputs, test each starter route and normal saving, independently apply the patch, and record final hashes. No remaining architectural choice was identified after the explicit clarifications; execution may still reveal defects requiring ordinary diagnosis and fixes.

Proceed through implementation-phases.md with per-phase exit checks. The design is a specified implementation proposal, not a certified release.
