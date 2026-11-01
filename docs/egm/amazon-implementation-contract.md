# Amazon expedition — concrete implementation contract

This addendum supplies the specifications requested by the formal readiness review. It is design, not implemented behavior. It is authoritative over older open-ended statements in amazon-expedition.md. The campaign and first mission remain those approved by the user.

## Map graph and coordinates

Coordinates are zero-based metatile coordinates. All four layouts use elevation 3 on walkable land and closed collision boundaries except listed crossings. Existing unrelated warps, connections, objects, trainers and coordinate events are removed from these four playable slots. No new map IDs are allocated.

| Slot | Dimensions | Role | Connections |
| --- | --- | --- | --- |
| PalletTown | 24×20 | Riverside village/dock | North to Route1, offset 0; no south connection |
| Route1 | 24×24 | Forest trail | South to PalletTown, offset 0; north to ViridianForest, offset 0 |
| ViridianForest | 24×20 | Blockade and stone clearing | South to Route1, offset 0; no other external exits |
| PalletTown_PlayersHouse_1F | 13×10 | Start and recovery | Warp only; no map-edge connections |

Open each connected north/south edge only at x=11,12. Village movement from the house reaches these crossings; trail crossings at y=0 and y=23 connect through its interior. Forest's south crossing is at y=19. Every connection is reciprocal. Block the village's northern crossing through coordinate events at (11,1) and (12,1) until the partner flag is set; move the player one tile south with a short guide message. Do not dynamically alter an edge connection.

House footprint: village x=4..8, y=3..7, with door warp (6,7) into house (5,8). House exit warp (5,9) arrives in village (6,8). New-game spawn is house (5,6), facing south. Retain the recovery destination (8,5) and LOCALID_MOM at (8,4), with the redesigned caregiver graphic. Place no furniture on the spawn/recovery/exit routes. A dock caregiver at (11,16) offers the same free voluntary party heal. Guide at (8,8) presents starters and mission.

Forest: a river/closed barrier occupies y=10 across the interior x=1..22; the only eventual crossing is x=11,12. Accessible southern paths lead to an agent at (10,14) and control at (12,13). Agent interaction is explicit, not a long-range surprise trigger. Its only interaction tiles are (9,14),(11,14),(10,13),(10,15); all have tall-grass behavior so the grass battle backdrop is selected. Remove other original forest trainers. Their flags do not unlock this objective.

The agent's defeat enables the control. Control activation replaces (11,10) and (12,10) with walkable bridge metatiles and persists a shutdown flag. On map load derive bridge state from that flag. Stone at (11,5), approached from (11,6). Collision boundaries prevent entering the north bank through river edges. Return uses the same bridge; no one-way ledges or required field moves. Stone sprite visibility follows acquisition state, while its event remains repeat-safe if invoked again.

## Semantic metatile allocation

Use secondary metatiles 0x280..0x287 consistently for grass, walkable path, solid tree, solid water, solid house wall, door behavior, solid control and walkable bridge. Define these symbolic assignments in a new include/constants/amazon_metatiles.h and use named values in scripts. Base land regions use grass/path; boundary tree/water and house footprints use solid collision. Add a tall-grass encounter metatile 0x288 for route patches and the agent interaction positions. Its behavior must be genuine encounter grass, not just grass artwork. Stone placement uses an object over walkable path, not a second invisible wall.

The asset manifest assigns the eight component tile indices and layer attributes for each of these nine metatiles; generate them from the authored indexed tile sheet rather than hand-editing conflicting old definitions. Validate every referenced tile index against that area's loaded sheet. Other decorative metatiles may be added only inside the documented budget and may not change the gameplay masks above.

## Saved identifiers

Use nine named aliases for currently unused saved flags 0x4A7..0x4AF, in this order: partner chosen, capture supplies received, agent defeated, blockade disabled, water stone acquired, stone two acquired, stone three acquired, stone four acquired, stone five acquired. Existing source declares these FLAG_UNUSED identifiers and a read-only named-reference search found no gameplay references. Before implementation also scan numeric and generated references; fail allocation validation if any conflicting use is found. Do not allocate 0x4B0 onward: those are existing boss flags.

VAR_STARTER_MON remains an index: 0 armadillo/Bulbasaur, 1 capybara/Squirtle, 2 macaw/Charmander. A separate chosen flag distinguishes default zero from confirmation. No species ID is written into VAR_STARTER_MON. Set FLAG_SYS_POKEMON_GET only following successful partner grant. Keep the Pokédex locked for this milestone. Set respawn HEAL_LOCATION_PALLET_TOWN on the first interior transition before any battle. No new save structure is introduced.

## Stone item definition

Reuse item slot 361, formerly ITEM_TOWN_MAP, for ITEM_PEDRA_DAS_AGUAS; use a semantic alias for the unchanged numeric ID and replace the positional JSON record at that slot. The town-map item is unavailable in the sealed demo. Audit references to its old constant so no retained reachable event grants the stone as a map reward.

Complete record: english = P. das Águas; itemId = ITEM_PEDRA_DAS_AGUAS; price = 0; holdEffect = HOLD_EFFECT_NONE; holdEffectParam = 0; importance = 1; registrability = 0; pocket = POCKET_KEY_ITEMS; type = ITEM_TYPE_BAG_MENU; fieldUseFunc = FieldUseFunc_AmazonStone; battleUsage = 0; battleUseFunc = NULL; secondaryId = 0. Description: Uma pedra rara ligada aos rios. Use charmap encoding and line-wrap within the actual item-description window.

Add the handler declaration in include/item_use.h and definition in src/item_use.c. It displays a short Portuguese message saying the stone has no use at this location, closes through the existing bag-message return callback, and does not consume the item or change flags. Bind gItemIcon_PedraDasAguas / gItemIconPalette_PedraDasAguas to the new icon/palette paths already listed. Validate encoded name length including EOS <=14.

Grant quantity is one. With prerequisites met, if item already exists but its acquisition flag is unset, reconcile by setting the flag without adding a copy. If the flag is set but the item is missing, permit a guarded repair grant; preserve the flag if repair cannot fit and explain the failure. Otherwise precheck space, execute additem, inspect actual success and only then set completion. Repeated interactions never increase quantity. A fixture with no available key-item slot tests failure; it must leave the reward eligible and be recoverable after restoring room. No full player save fixture is distributed as a new-game requirement.

## Learnsets, permissions and encounters

All three species use their two listed starting moves at level 1, the previously specified additional move at level 8, then the learnset terminator. No further moves or evolutions are enabled in the milestone. Set their TM/HM and tutor permission masks to zero; no field-move progression is required. Keep existing move mechanics and the prior stat/ability table. The level-4 agent uses these default learnsets, so both opponents have their two intended moves.

For Route1 and ViridianForest land encounters use encounter_rate 10 and the existing engine's 12 weights: 20,20,10,10,10,10,5,5,4,4,1,1. Species by slot: capybara, armadillo, macaw, capybara, armadillo, macaw, capybara, armadillo, macaw, capybara, armadillo, macaw. Every slot has min level 2 and max level 4. Village and house have no encounters. Do not enable surfing or fishing tables. Wild battles can only start on the authored encounter-grass masks.

Balance acceptance is a repeatable route with each starter and no mandatory capture: free recovery, retry and completion must remain possible. Record turns, defeats and resource consumption. Balance values are reviewable proposals; do not silently rebalance species during test automation.

## Asset conversion contract

Source files are authored during implementation, not claimed to exist in this design. A manifest row contains source path, output path, expected dimensions, frame layout, color count, transparent index, palette group, source hash and converter version. Its planned output set is exactly the asset files enumerated in the design. Editable artwork and indexed outputs are separate.

Preserve the existing frame layouts of replacement sheets. Creature front/back 64×64; icons 32×64; footprints 16×16 monochrome. Player walk/item sheets 144×32. Guide sheet 160×32; caregiver/agent sheets follow their inspected original frame geometry. Player battle back 64×320; agent front 64×64. Grass backdrop terrain 64×104; entry animation 64×80. Retain their existing tilemap geometry. New key-item icon uses the existing neighboring item's actual dimensions, checked before authoring; reject a mismatch instead of resizing unpredictably.

Tilesets are 128 pixels wide, 8-pixel aligned. Primary sheets may occupy at most 640 tiles; each secondary at most 384. Map palettes 0..6 are primary, 7..12 secondary; never use 13..15 as loaded map palettes. Characters and battle pictures use their own existing 16-color palette groups. For creature/character art index zero is transparent and there are at most 15 opaque colors per palette. Source sheets may be quantized once during conversion, but final indexed outputs and native-resolution screenshots must be inspected.

The converter validates all inputs and allocation references before replacing outputs. Stage outputs in a temporary directory outside the checkout; on validation or conversion failure leave all tracked outputs untouched. Produce an allocation report and file hash list. A final-art appearance cannot be inferred from schema validation; inspect it in-game.

## Ordinary-save runner interface

Extend runner arguments to ROM --save PATH. If the save exists open it read/write and pass the VFile through mCore loadSave before reset; do not load an emulator state. Preserve the save handle for its required lifetime. After the user triggers menu saving, run enough frames for the engine's completion feedback; expose savedataClone through a flushsave command to persist the engine save bytes atomically to PATH. Test the file with a completely new runner process, not savedataRestore in the same process.

Add read8/read16/read32 and wait-for-value commands with frame timeouts. Resolve symbol addresses from the final ELF/map, including save-block pointers and party pointers; never hard-code addresses from an earlier build. The route driver checks the actual starter index, acquired flags and inventory after reading current pointers. Record a command transcript, frame count and assertion result. Failure screenshots and the final build hash belong in the evidence record. Emulator save/load commands remain debugging tools and are not accepted in the normal-save test route.

## Reproducible build and phases

Pin pokefirered commit ce6406d8c2eaf46d543c8a2606de0c3cb1951982 and agbcc da598c1d918402c42c0c0d7128ba14567f3175e9. Record the local Debian binutils package version, gcc, libpng and converter versions in validation.json. Use the tested /workspace/toolchain/activate.sh initialization; retain TLS/signature checks when refreshing packages.

After validated art conversion, from /workspace/pokefirered run make generated; force rebuilding build/firered_rev1/data/maps.o and build/firered_rev1/data/map_events.o with GAME_VERSION=FIRERED GAME_REVISION=1; then make -j4 firered_rev1. The release helper must stop on the actual failing command, not a log-capture success. For a reproducibility check rebuild into a clean output tree from the pinned base plus recorded source changes and require the same ROM hash. Constrain this first release to 16 MiB, equal to the base, so the current IPS packaging limit is explicit.

The final patch must be applied with an independent IPS tool, not only its creator's internal parser. Use Floating IPS from https://github.com/Alcaro/Flips at commit ff216a75df0987047a67d7923567dc4482ce07ac, with its CLI invocation `flips --apply vila-ipe.ips clean-base.gba independently-patched.gba`. Record tool build and invocation output; compare the independently patched SHA-1/SHA-256 with the final ROM. If acquiring/building that tool is blocked, report independent verification as unrun rather than substituting the same parser. The remote commit was verified read-only; the tool has not been installed or executed yet.

Phase exits: (1) fresh startup and valid recovery; (2) map graph, event progression and no softlocks; (3) three starter branches, wild capture and stone inventory; (4) original art and native-resolution inspection; (5) clean build, independent patch verification and normal save/process-restart. Complete all required checks before claiming the expedition ready. No phase has been implemented by this document.

## Final clarifications from the bounded readiness recheck

### Indexed house warps

Use ordinary warp events, not coordinate-script warps. Village warp index 0: (6,7), destination MAP_PALLET_TOWN_PLAYERS_HOUSE_1F, destination warp index 0. House warp index 0: (5,9), destination MAP_PALLET_TOWN, destination warp index 0. Both use the appropriate existing door/exit metatile behavior and land elevation. The engine first places the player at the destination warp's coordinate. Retain its standard door/exit arrival behavior to step off the warp: expected playable arrival house (5,8), village (6,8). These are post-transition expectations, not destination warp definitions. Verify both actual arrival and immediate re-entry to avoid a warp loop.

### Tileset bindings

Village and Route1: gTileset_General plus gTileset_PalletTown. Forest clearing: gTileset_General plus gTileset_ViridianForest. House: gTileset_Building plus gTileset_GenericBuilding1. Add the house secondary family to the file manifest: data/tilesets/secondary/generic_building_1/tiles.png, metatiles.bin, metatile_attributes.bin and palettes/07.pal through palettes/12.pal. Author its indoor floor, wall, furniture, doorway and recovery-space tiles; do not copy outdoor artwork blindly into it.

The semantic secondary metatile ID meanings apply by behavior across these three secondary families; appearance is region/interior-specific. ID 0x280 is walkable floor/grass, 0x281 path/floor, 0x282 solid tree/wall, 0x283 solid water/furniture, 0x284 house-wall/furniture, 0x285 doorway, 0x286 solid control/furniture, 0x287 walkable bridge/floor and 0x288 encounter grass (not used indoors). Palettes 7..12 remain the complete loaded secondary range. Output assets for GenericBuilding1 must be listed in the art manifest and validated alongside the other families.

### Deterministic gameplay masks

House: boundary walls at x=0,12 and y=0,9 except exit (5,9); open interior x=1..11,y=1..8. A decorative bed occupies x=1..2,y=2..3, a table x=9..10,y=2..3. All other interior tiles remain walkable; caregiver occupies (8,4). Spawn (5,6), recovery (8,5), exit and the entire walking connection between them remain unobstructed.

Village: open interior except house footprint x=4..8,y=3..7, solid banks along x=1..2, and the dock's water south of y=17. Keep a walkable route from (6,8) to the north crossing and dock caregiver. Border x=0,23 and y=0,19 is solid except the declared northern crossing. No village encounter grass.

Trail: solid outer boundary except north/south crossings. Main path x=10..13 throughout the interior is walkable. Encounter grass rectangles x=5..8,y=5..8 and x=15..18,y=13..16 connect to the central path by walkable strips at y=6 and y=14 respectively. No unavoidable encounter before partner confirmation. Other interior land is walkable grass; decorative solid trees cannot intersect the path or patch-access strips.

Forest: open interior southern land x=1..22,y=11..18; northern land x=1..22,y=1..9. River/barrier row y=10 is solid except the two bridge tiles after shutdown. Border solid except south x=11,12. Stone (11,5) and its approach are walkable. Encounter grass is confined to x=4..7,y=14..16 plus the four specified agent interaction tiles. Keep agent, control, bridge approach and return routes connected. Decorative solids cannot introduce another crossing or seal these paths.

Return acknowledgment derives from the water-stone acquisition flag, so no tenth durable acknowledgment flag is required.

### Starter presentation and supplies

The guide uses an existing scripted multichoice with four entries: Capivágua, Ararafogo, Tatupedra, Voltar. Bind the menu entry in include/constants/multichoice.h and src/script_menu.c after checking how the current menu tables are declared. On one of the three creature choices, use showmonpic for that species, show a short Portuguese type/style description with MSGBOX_YESNO, hide the picture and return to selection on No. Yes attempts the guarded grant. Cancel/Voltar closes without durable changes. No new custom menu renderer is required.

Grant five ITEM_POKE_BALL through the separate supplies transaction. If space is unavailable, the guide offers them again later without another partner. Store the supplies flag only after a successful additem result. Keep the original index mapping specified above; displayed menu order need not equal the saved index.

### Reachable inventory repair

The dock caregiver is always reachable after returning from the clearing and offers the inventory-consistency check before voluntary healing. If the water-stone flag is set and ITEM_PEDRA_DAS_AGUAS is absent, offer the guarded repair grant through that caregiver. This remains reachable after the acquired stone object is hidden. If repair cannot fit, explain and preserve the state for a retry; do not clear the acquisition flag or reset the mission. If the flag is unset, the caregiver does not grant a stone merely because the player asks. With flag set and item present, no item is added. Add this exact mismatch fixture to the route tests.

### Reused item help topic

Add src/help_system.c to the item-slot reference audit. Replace or disable the Town Map possession-based help topic for reused ID 361; acquiring the stone must not advertise Town Map use. The new stone's description and harmless use behavior are its only bag affordances in this milestone.
