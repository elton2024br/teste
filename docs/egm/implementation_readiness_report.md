# Formal EGM implementation-readiness review

Target: amazon-expedition.md, original reviewed snapshot lines 175–401; preceding feature context supplied. Mode: implementation-only, not the full five-stage review. Three fresh-context agents completed the review. No reviewer performed a build or gameplay test.

| Reviewer | Status | Required material read |
| --- | --- | --- |
| formal_readiness | completed | Readiness persona, implementation-readiness standard, full target/context, relevant existing sources |
| formal_code | completed | Codebase-details persona, readiness standard, full target/context and source bindings |
| formal_style | completed | Style persona and full target/context |

## Consolidated findings and disposition

- R1 — Blocker: new 1F startup bypasses 2F respawn initialization. Source-grounded correction added: initialize checkpoint before battle and preserve explicit house recovery contract. Requires later implementation/test, not claimed fixed in ROM.
- R2 — Blocker: narrative stone name exceeds the fixed inventory label field. Abbreviated inventory name and encoded-length validation specified; full narrative name retained.
- R3 — Blocker: map topology and event geometry are not specified. Still open; current Route1/forest connections do not implement the proposed route automatically.
- R4 — Major: VAR_STARTER_MON encoding and party-menu flag are missing. Corrected design keeps indices and explicitly requires FLAG_SYS_POKEMON_GET and repeat-safe supply delivery.
- R5 — Major: complete stone slot/JSON/icon/use behavior is missing. Still open beyond the corrected display-name requirement.
- R6 — Major: learnset levels, permissions and encounter slot weights are incomplete. Still open.
- R7 — Major: final art inputs, palette allocations, metatile compositions and transactional conversion contract are deferred. Still open.
- R8 — Major: ordinary-save lifecycle, source/tool pinning, build targets and independent patch invocation are unspecified. Still open; current runner supports emulator states, not normal-save validation.
- R9 — Major: grass battle art may not be selected on plain-ground agent triggers. Still open; bind the trigger terrain or specify a scoped override.
- R10 — Major: no buildable phases. Explicit phase sequence and behavioral exit checks added.
- R11 — Major/Nit: stale decisions and obsolete inspection gates. Key contradictions corrected, but full document consolidation remains necessary.

## Evidence and limitations

Code review confirmed src/data/items.json generates items.h; individual trainer IDs live in include/constants/opponents.h; Rick is ID 102. New planned assets/tooling are future creations, not missing existing dependencies. Reviewers did not exhaustively inspect every large graphics/data table or binary image, and did not verify all identifier references. A report with no runtime tests cannot certify asset or save safety.

## Outcome

Review complete; readiness FAILED. The corrected design is not a completed implementation and has not been re-audited. Finish the remaining specifications, then perform a bounded readiness recheck before claiming the first expedition is ready to implement.
