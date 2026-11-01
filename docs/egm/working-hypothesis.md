# Bichos do Brasil — visual identity planning

Status: working hypothesis, before clarification and independent review. This is not an approved specification or a completed EGM concept brief.

## Goal established by the user

Give the game a Brazilian visual identity that is clearly distinct from FireRed. Use EGM to plan the work before further implementation. The current target is a FireRed revision 1 ROM hack.

## Current evidence

Release 0.2 replaces the two village house facades, introduces stone paths, opens the garden and includes earlier Portuguese text changes. Trees, player and NPC sprites, laboratory, interiors, battle presentation and menus still use FireRed artwork. The existing field layout and story progression also retain much of FireRed's structure.

## Working hypothesis

A consistent regional art direction should guide new terrain, vegetation, buildings, characters, interface and creature designs. Start with one complete playable area, including its interiors and one battle, so the result can be judged as a game rather than as an illustration. The user selected the Amazon as the regional setting. Confirm the player’s role and main adventure before choosing detailed assets.

## Decisions still open

- Confirmed: the Amazon is the setting.
- Open: the player’s role, central objective and tone of the adventure.
- The first playable area's boundaries and which visual elements must change for it to feel original.
- How much the story, navigation and battle presentation should depart from FireRed.

## Risks to investigate

Changing isolated facades leaves the overall game recognizably FireRed. A single generic tropical palette may erase regional distinctions. GBA tile and palette limits require testing the final assets at native resolution. Old emulator states are unreliable across builds with relocated data. A successful build alone does not verify collisions, transitions, battle graphics or normal save files.

## Proposed planning sequence

Clarify the setting and scope in conversation; anchor the hypothesis; obtain the user's explicit readiness confirmation required by egm-brainstorm; run fresh-context Goldfish reviews; save a reviewed concepts_brief.md; proceed to a detailed design through egm-draft. No reviewers have been launched, and no design is approved yet.

## Amazon setting — user-confirmed direction

The user selected the Amazon. Working proposals below are not yet approved requirements.

Build a small fictional riverside community rather than treating the entire Amazon as one uniform place. Draw a consistent visual vocabulary from waterways, forest canopy, stilt houses, wooden walkways, docks, regional boats, fruit trees and shaded gathering places. The house art from 0.2 is provisional and should be reassessed against this setting.

Make the river influence navigation, rather than adding water as decoration. A first playable area could connect the player’s home, a community dock, a short forest trail and a local care/research building. Keep the first version small enough to test all transitions and collisions.

Proposed creature references include river dolphins, arapaima, caimans, macaws, sloths and monkeys. Names, silhouettes and battle sprites need original designs. Do not treat Amazonian wildlife as interchangeable or add every species to the same habitat without checking it.

Cultural references require specificity. Do not invent a generic Indigenous community, combine distinct traditions, or present fictional folklore as a documented local belief. Any named real community or tradition needs research before inclusion.

The main gameplay objective is still open. It determines whether the early map needs a research station, a rival, a rescue event, a competition or another story structure. Do not turn the proposed riverside setting into an assumed story without the user’s answer.

## Scope update — five Brazilian habitats

The user requested “5 habit. Brasileiros,” interpreted as five Brazilian habitats. This expands the earlier Amazon setting into a journey across five regions, with the Amazon as the proposed starting area. The exact five-region selection below is a planning proposal, not a confirmed user selection.

1. Amazon: a riverside community, navigable river edges, flooded forest and forest trails.
2. Cerrado: open savanna, twisted trees, veredas and seasonal streams.
3. Caatinga: dry woodland, rocky ground, seasonal water and drought-adapted plants.
4. Atlantic Forest: dense hillside forest, waterfalls and coastal connections.
5. Pantanal: floodplain, wetlands, open grassland and waterways.

Each region needs its own terrain tiles, vegetation, architecture, creature habitats and navigation pattern. Avoid making the same map with different colors. Wet and dry seasons are visual and narrative references at this stage; a dynamic season system is not an agreed feature.

Proposed first milestone: a complete small Amazon starting area. Establish the asset and testing process there before expanding to the other four habitats. Main story, player role, exact region list and full campaign size remain open. No Goldfish review has run.

## Central objective — confirmed by the user

The player travels through five Brazilian habitats to obtain one rare stone in each. This is the central progression goal. The Amazon starting area remains the working proposal, and the five-region list remains proposed until reviewed with the user.

## Anchored working hypothesis for the readiness checkpoint

Create a GBA adventure with its own Brazilian visual identity, built from the FireRed revision 1 code base. The player starts in a fictional Amazon riverside community and travels through five Brazilian habitats to obtain one rare stone in each. Each habitat has distinct navigation, architecture, plants and creature designs; its stone is the reward for completing its main expedition.

## Proposed implementation boundaries for review

Build one complete Amazon expedition first: riverside starting community, home interior, dock, a short connected forest route and a stone destination. Give the expedition an explicit beginning, a reachable objective and a return route. Test movement, collisions, doors, dialogue, encounters, battle, capture, stone acquisition and normal saving/reloading.

Treat stones as fictional story items rather than claims about the real geology of each habitat. Their names, appearance, abilities, guardians, puzzles and connection to the ending remain design proposals. Do not silently add multiplayer, a dynamic seasonal system, a new battle engine or a full national map to the first milestone.

Rare-stone acquisition must have a testable state: absent before the objective, granted once, retained after saving and reloading, and reflected in the player’s progress. Acquiring a stone should not leave the player trapped in its destination.

## Review questions

- Does the five-stone loop make each habitat meaningfully different, or repeat the same errand?
- What is the smallest complete Amazon expedition that proves the game’s visual identity and progression?
- Which existing FireRed systems should be reused, and which recognizable visual assets need replacement first?
- Can the new maps and sprites fit GBA limits without sacrificing readability?
- How will build reproducibility, independent patch verification and normal save testing work?

Readiness status: awaiting the user's explicit confirmation before fresh-context Goldfish reviewers are launched, as required by egm-brainstorm. No review findings or approved specification exist yet.

## Creature art direction — confirmed by the user

The user chose a middle ground between realistic Brazilian animals and strongly fantastical creatures. Preserve recognizable anatomy and silhouettes; introduce a small number of visible fantastical traits tied to the creature’s abilities. Do not merely recolor existing Pokémon sprites.

Working art rules:
- The underlying animal must remain recognizable at native GBA battle and icon sizes.
- Each early creature gets one main visual motif, rather than many competing ornaments.
- Evolution should change silhouette and ability while retaining the recognizable animal family.
- Use regional species references and check their habitats before assigning encounters.
- Front sprites, back sprites, party icons and palette variants must belong to the same design.

Provisional examples, not approved final species:
- A capybara-inspired water partner with river-shaped markings and a small aquatic plant motif.
- A macaw-inspired fire partner with ember-colored feather tips; its silhouette remains avian.
- An armadillo-inspired ground/plant partner with stone-like armor and small shoots between plates.
- A jaguar-inspired creature with luminous rosettes that indicate its power.
- A river-dolphin-inspired creature with current-shaped markings and subtle water effects.

Earlier creature names, starting-partner assignments, types and the exact roster were suggestions, not user-confirmed decisions. Starting creatures need not all be native to the starting village if a credible in-world origin is provided. Do not imply that all suggested species occur together in every habitat.

## Updated scope for concept review

Confirmed user goals: five Brazilian habitats, one rare stone to obtain in each, collectible Brazilian-animal-inspired creatures, and a visual balance between recognizable animals and fantasy. The user also wants the result to look distinct from FireRed. Current GBA/FireRed revision 1 implementation is the working technical base.

Proposed first milestone: a complete small Amazon expedition with a limited creature roster, one obtainable stone and verified normal saving. A six-creature party, specific starter trio, guardians, creature powers used outside battle and exact habitat list remain proposals for review. Goldfish readiness confirmation is still pending.

## Review outcome

The user confirmed readiness with “Ok”. Six fresh-context Goldfish agents completed review. The current consolidated planning source is concepts_brief.md; review status and synthesis are in goldfish_review_report.md. Earlier pending-readiness notes above are historical. The concept brief awaits user alignment and is not an implementation approval.

## Confirmed story payoff

The five stones open the route to the Terras Raras, where prehistoric animals and fantastical discoveries can help save the world. The world-threatening problem remains open. See the updated concepts_brief.md. This new endgame destination was not part of the completed review.

## Confirmed antagonist

Tio Sam is a fictional American capitalist seeking world domination. The updated concept brief distinguishes this confirmed character from a proposed extraction-and-creature-control plot. Story additions await alignment before formal design; reviewers have not reviewed them yet.
