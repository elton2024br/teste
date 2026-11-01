# Bichos do Brasil — five habitats and five rare stones

Status: concept reviewed by six fresh-context Goldfish agents. Recommendations below await user alignment; this is not an approved implementation specification.

## Overview

Create a Brazilian creature adventure with an identity distinct from FireRed. The player explores five Brazilian habitats and obtains one rare stone in each. Creatures draw on recognizable Brazilian animals with moderate fantasy: clear animal silhouettes, a small number of visible power motifs and coherent evolution families.

The existing technical base is a FireRed revision 1 ROM hack. Release 0.2 demonstrates initial house, path, garden and text changes. It does not establish a complete original adventure or a working creature-and-stone progression loop.

## Confirmed user goals

- Five Brazilian habitats.
- One rare stone to obtain in each habitat.
- Brazilian-animal-inspired collectible creatures, in a style halfway between natural and fantastical.
- A visual identity that looks different from FireRed.
- An Amazon setting as part of the world.
- EGM planning and independent review before expanding implementation.

## Proposed world structure

Use the Amazon as the starting habitat, followed by Cerrado, Caatinga, Atlantic Forest and Pantanal in an order still to be designed. This exact selection and ordering are proposals. Pampa is not included in this proposed five-region selection.

Give each habitat a distinctive route structure, environmental obstacle and creature community. Reuse the same movement, battle, capture, healing and inventory systems; five habitats do not require five new engines. River navigation should shape the Amazon route, initially through map design and a simple scripted crossing if needed.

Stones are fictional story objects. Their names, individual powers, acquisition challenges and guardians have not been confirmed. Their combined purpose is confirmed: opening the route to the Terras Raras. Do not present them as factual mineral deposits or invent traditions for real communities.

## Analysis from the six reviews

### Content scope is the main planning blocker

Five regions multiply maps, architecture, vegetation, dialogue and creature assets. Replacing only facades leaves much of FireRed recognizable. Conversely, replacing every menu, animation and species before producing a playable area makes the work difficult to finish. Bound the first expedition and prove its complete visible loop before expanding.

### The player needs a reason to seek the stones

The collection target and final payoff are now clear: the five stones open the route to the Terras Raras, where prehistoric animals and fantastical beings or discoveries can help save the world. The protagonist's role and the specific world-threatening problem remain open. Each stone needs an understandable local objective and visible progress feedback. Five identical item-fetching errands with different colors would not meet the identity goal.

### Creature designs need complete asset families

A drawing alone is not a usable creature. Each initial species needs an agreed silhouette, front and back battle sprites, party icon, palette, encounter or partner assignment, basic stats and usable moves. Evolution chains, a starter trio, guardians and exploration abilities are still proposals, not mandatory first-milestone work.

### Existing progression needs an audit

The opening area is coupled to Oak scripts, scene variables, coordinate triggers and laboratory movement. Replacing the scenery does not remove these dependencies. Each stone needs one authoritative, save-backed acquisition state. Reward granting, dialogue and access must agree, including when item delivery cannot complete.

### Build, patch and save checks prove different things

A successful build does not prove correct tile loading or movement. Patch reconstruction does not prove gameplay. Emulator states do not prove normal in-game saving. Release evidence must name the final ROM hash and distinguish these checks.

## Recommended first milestone: one complete Amazon expedition

Proposed production cap:

- Three outdoor maps: riverside community with dock; forest trail; stone destination.
- One accessible home interior; an outdoor care NPC provides healing.
- One partner species and one catchable species, with complete front/back/icon assets. Species selection remains open. No evolution chains or starter-selection trio required for this milestone.
- One stone and an accessible return route.
- One short local objective, explained by a character and reflected in dialogue after completion.
- A coherent original visual set for the visible terrain, vegetation, buildings, player, essential NPCs, both creatures and the battle backdrop. Retained UI elements must be listed explicitly rather than described as fully replaced.

Proposed player sequence:

1. Receive a clear local expedition objective and a partner.
2. Explore the community and learn where the stone destination is.
3. Traverse a river-shaped route, encounter a wild creature and have a reachable capture opportunity.
4. Complete the destination challenge, whose exact design remains open.
5. Obtain the stone once, receive visible confirmation and return to the community.
6. Save through the game menu, close the emulator and resume with the stone and progress intact.

The production caps are recommendations, not a reduction of the confirmed five-habitat campaign goal.

## Goals and non-goals for the milestone

In scope: a complete expedition, original visible asset families, battle/capture/healing, one-time stone acquisition, safe return, defeat recovery, normal saving and reproducible delivery.

Deferred: the other four regions, full evolution roster, a starter trio, multiplayer, seasonal simulation, a new battle engine, full interface replacement and an entirely new quest engine. Their omission from this milestone does not decide the final campaign design.

## Alternatives weighed

- Build all five habitats at once: postpone because content and regression costs are not bounded yet.
- Keep changing houses alone: insufficient because trees, characters, interiors and battles still dominate the perceived identity.
- Continue the independent browser prototype as the main game: possible, but the current ROM-based work already has working GBA systems; changing platform would require another explicit decision.
- Add a new quest framework: existing inventory, flags and scripts appear sufficient for five stones; audit and reuse them first.
- Produce a starter trio and evolution chains immediately: postpone until two complete creature designs work at native resolution.
- Treat emulator-state restoration as persistence validation: insufficient; test normal save files across process restart.

## Technical requirements for the later specification

- Pin source revisions and tool versions. Produce a complete ordered build from clean inputs, including art conversions and map object regeneration.
- Replace hard-coded one-off asset mutation with checked inputs and explicit asset allocations. Fail before partial integration when preconditions do not hold.
- Current field-map configuration provides 640 primary and 384 secondary tiles, 640 primary and 384 secondary metatiles, and seven primary plus six secondary palettes. Report usage for each actual area; do not assume one region's success proves every tileset fits.
- Verify final artwork at the GBA's 240×160 display resolution, including transitions and battle rendering.
- Audit inherited opening events before replacing the expedition's story.
- Define stone grant and completion behavior for first interaction, repeated interaction, failed grant and reloaded progress.
- Proposed save policy for the initial expedition release: require a new game; make no promise of compatibility with earlier prototype saves or emulator states. User alignment is still needed on this policy.
- Package cumulative patches against the clean revision 1 base, SHA-1 dd5945db9b930750cb39d00c84da8571feebf417. Independently apply the distributed patch and compare it to the final build hash.
- The present IPS tool requires equal source/target sizes up to 16 MiB. Revisit packaging if the ROM grows.

## Acceptance evidence

Run a fresh-game route on the final distributed artifact. Record pass/fail separately for boot, movement and collisions, every required door, encounters, battle, capture, healing, defeat recovery, one-time stone acquisition, repeat interaction, safe return and normal save/restart/load. Check state consistency before acquisition, after acquisition and after reload. Record map, relevant flags, inventory, build hash and reproduction steps for failures.

Include native-resolution screenshots of exploration, an interior, a battle and stone feedback. No future check is claimed passed by this brief.

## Key decisions for the next planning turn

The user confirmed that collecting the five stones opens the route to the Terras Raras, containing prehistoric animals and fantastical discoveries that can help save the world. The user has since identified the antagonist as Tio Sam, a fictional American capitalist seeking world domination. His specific method is proposed in the antagonist section below. Then resolve the protagonist's role, exact habitat list, first destination challenge, two initial creature designs, acceptable inherited interface and save-compatibility policy. Convert the aligned brief into a detailed design with egm-draft before implementation.

## Review provenance

Six fresh-context agents completed BRAINSTORM review, each confirming its persona and target were read. Lenses: design, codebase details, zoom-out, comprehension, implementation readiness and structural maintenance. See goldfish_review_report.md for the status and synthesis. Findings are design recommendations; no new implementation or gameplay tests were performed during review.

## User-confirmed story update — the Terras Raras

Collecting all five stones opens the route to the Terras Raras. This hidden destination contains prehistoric animals and fantastical beings or discoveries that can help save the world. This adds a campaign destination beyond the five Brazilian habitats; it does not silently replace one of those habitats or add it to the first playable milestone.

The threat, the way these creatures help, the route-opening mechanism and the resolution are not yet defined. Prehistoric species and fantastic designs remain to be chosen. Use “Terras Raras” as a fictional place name; do not assume the user meant rare-earth minerals, a mining plot or a geological claim.

Planning consequence: the five-stone journey needs to introduce the threat and explain why this hidden place offers hope. The first Amazon expedition should foreshadow that purpose while keeping its immediate local objective understandable. A map of the campaign can reserve a locked destination without implementing its contents in the first milestone.

The existing Goldfish review predates this story update. Its production, progression and testing recommendations remain relevant, but no reviewer has yet assessed the added endgame destination.

## User-confirmed antagonist — Tio Sam

The antagonist is Tio Sam, a fictional American capitalist who wants to dominate the world. His nationality, capitalist motivation and ambition are user-defined character traits. His actions belong to this individual and his fictional organization; they do not describe real Americans collectively.

### Dramatic mechanism — user-approved direction

Tio Sam leads a fictional corporation seeking control over the five habitats' resources. His extraction machines damage local environments and displace creatures. He wants the five stones to enter the Terras Raras and turn their prehistoric animals and fantastical powers into instruments of control.

The player travels with animal companions, helps communities confront specific local consequences and earns access to each stone. Gathering the stones first opens a route to potential allies in the Terras Raras. These allies should participate in a defined resolution rather than serving as an unexplained instant cure.

An Amazon opening could show one concrete, readable threat: a river passage blocked by the corporation's operation, preventing a community from reaching a needed destination. This is a proposed fictional event, not an account of a real company or community. Map scripts and existing battle systems can support it without new simulation systems.

Use encounters, dialogue and environmental consequences to communicate the antagonist's values. His means, organization name, personal history and final confrontation remain proposals to design. The story must explain why the player opens the route despite the villain's interest, and how collecting the stones avoids simply delivering access to him.

### Current campaign spine

Five Brazilian habitats → five rare stones → route to the Terras Raras → prehistoric and fantastical allies → confrontation with Tio Sam's plan. This is a narrative outline; specific quests and mechanics have not been implemented or formally approved.

### Review status

The six-agent review predates the Terras Raras payoff and named antagonist. Revisit story coherence, route gating and content scope when drafting/reviewing the design. Preserve the first-milestone limit; the added endgame does not make the entire campaign part of the first release.

## Story alignment checkpoint

The user answered “Ok” to the proposed extraction-and-creature-control plot. This confirms that narrative direction. The river-blockage opening, exact quest structure, roster, map counts and technical policies still require design decisions. The next artifact is design_draft.md, beginning with overview and goals.

## Technical-plan decision

The user selected stones as named, described key items in the bag (Option A). The technical draft retains acquisition flags as the authoritative story state, with successful delivery before completion. A flags-only display was considered but not selected.

## Save-policy decision

The user selected a new game for the redesigned adventure. Earlier prototype saves are not supported; normal saving and restart within the new release remain mandatory. Migration of old saves is out of scope for the initial expedition.

## User-directed scope update: three starting partners

The player chooses among the capybara/water, macaw/fire and armadillo/earth candidates presented in conversation. This supersedes the review recommendation to ship a single starter. All three require complete artwork, data and starting-route tests. Evolution chains and a rival counter-choice were not requested. Ordinary capture remains required, but the wild roster is still open. See design_draft.md for selection and persistence requirements.

## Creature integration decision

The user selected replacement of original Pokémon by original Brazilian creatures (response “11”, interpreted as option 1). Use audited existing species slots and complete asset/data replacement; do not extend the roster by keeping original Pokémon alongside the new animals. Releases may be incremental, but accessible encounters must not be represented as fully original until audited. The initial trio remains capybara/water, macaw/fire and armadillo/ground, chosen by the player.
