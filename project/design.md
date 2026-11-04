# Selene: Tidelocked: Act II design (updated 2026-11-04, names as of build "the Hearth Tree")

## World and lore (2026-11-04)
- The Root-Kin of Earth: a highly advanced techno-magical civilisation that grows its technology from specialised, magically hardened trees. Tools, cities, vehicles and ships are organic. No nation states, local cultures preserved; one World Government for thousands of years, a democracy with slight meritocratic elements.
- **Selene** (she/her, never "the Selene"), named for the Greek Moon goddess: a colony ship of living wood, shaped like a long, swept hull with crescent wings (the White Star from Babylon 5 is the shape reference; never named in the game). At her heart grows the **Hearth Tree**: her drive, her mind (WARDEN) and her hydroponic garden at once, so all of Act I happens in and around it.
- No FTL: ships ride the ambient magic that saturates the universe at relativistic speed, inside magical ward-shields and with artificial gravity, and can turn on any axis without shear or friction. Halfway there Selene flips and brakes (Turnover: restore gravity, raise the wards, plot, then flip).
- **Seedlings** (were clones): disposable drones of WARDEN and the Hearth Tree, grown for a specific task with limited autonomy. Regrown as a new version once their program and body can be improved; what one learned seeps back through the roots.
- Terms: energy (unchanged), sap cells (were charge cells), deadwood (was salvage), grafts (Act II spare parts), sprout (was decant), return to the roots (was recycle).
- Act I order: Seedling Vaults (clone stock) -> Taproot Galleries (power) -> The Heartwood (navigation, WARDEN's mind) -> Canopy Gardens (food) -> Ember Crown (propulsion; Kindle the Hearth Tree ends Act I).

## Flow
- Act I = 5 sections. Kindling the Hearth Tree ends Act I; there is no restarting. Every seedling that kindles it carries on into Act II.
- Act II is linear, three parts, nine sections:
  1. The boarders: Bark Breach, Contested Boughs, The Hive Ship (finale: Cut the hive loose).
  2. The long watch: The Long Current, The Drift, The Long Dark (finale: Reach the turnover point).
  3. Arrival: Turnover (restore the artificial gravity, raise the ward-shields, plot the turnover, flip Selene end over end, bank and relight the Hearthfire, plot the approach, begin the braking burn), The Tessaly System (scan the gas giant, its moons, the asteroid belt, a comet tail, the radiation belt, the inner worlds; slingshot), Tessaly Orbit (orbit insertion, orbital survey, sweep debris; finale: Establish a safe orbit over Tessaly).
- Pacing: see playtest-notes.md (current: Act I 4.50 h, Act II 7.45 h in-game, lean bot).

## Difficulty
- Danger ramp (drain and hazards): x1.0 in the Seedling Vaults, +5% per Act I section; Act II x2.12 (Bark Breach) up to x2.60 (Tessaly Orbit) after the +18% retune.
- Stasis watch records cut drain: -10% across Act I, -50% in total.

## Ship wear and grafts (all of Act II)
- Deadwood doubles as grafts in Act II. Wear builds as a seedling works: a little in the Boarders, more over the Long Watch, most in Arrival (Grafter's toolkit x0.7). Each point of wear adds 8% drain.
- Repair: removes 1.5 wear for a fixed number of grafts (more in later sections), then a cooldown. Auto-repair (default on) and a Repair button under Grafts.
- Workshops: one action per Act II section (ws6..ws14), each shortens the repair cooldown, costs three repairs' worth of grafts, paid when work starts.
- Graft jobs are the forage: auto-scavenge (default on) works the best one when grafts run low. Fill-before-crossing tops up as before.
- Running out of grafts lets wear climb; a death with drain x2 or more from wear reads "Worn down with the ship".

## Legacy tasks (replace the old Act I reward points)
- Four themes, each with a set in every Act I section: Echo (Act I familiarity), Dampening (drain), Storage optimization (max energy), Overclock (game speed).
- Themes are revealed as Act II sections are first reached.
- Each set = five actions: two pairs (A1 -> A2, B1 -> B2), then a final that needs A2 and B2. Only the final gives the bonus. A1, B1 need the section's last regular action. LEGACY_LEN 0.6.
- Mandatory: once a theme is revealed, its finals are required for the section's crossing (and for kindling the Hearth Tree). Unrevealed themes don't block.
- Not auto-queued: a toast when parts first open in a life, and a dot on the Tasks tab. Once automated they join chains and section runs.
- One optional drill per set, training only that set's five parts.
- Quartermaster's cache: unlocked the first time the Hearth Tree is kindled.

## Section runs
- "Always run sections once ready" (global): a run starts by itself whenever the current section is fully automated, clears the queue's leftovers for its sections and is pinned at the top of the queue. Runs still stop at act ends.

## Honours: removed from the game (2026-11-04)
- No longer earned and no effects. Old save data (a2.hon, a2.lv) is kept but ignored.

## Energy and sap cells
- One sap-cell store (were rations, then charge cells); charging stations per section, with a reserve; one charger upgrade per section speeds up recharges.

---

# PARKED: Act III (do not build or decide until the user reopens it)

Everything below is stored for later. All open questions stay open until the user picks Act III up.

## Act III content held back from Act II (colony)
- Map the colony site, drop a site probe, warm the first pods, prepare the wake cycle, choose who wakes first, wake the first sleeper, the "First contact" record.

## Act II legacy tasks (from the old Honours), unlocked gradually over Act III
Same structure as the Act I legacy tasks (five-part sets, mandatory for crossings once revealed, warning instead of auto-queue, optional drill per set).
- Five themes:
  - Veteran template: hazard damage down (old: -25% per level, -75% max).
  - Long-watch rhythm: strain down (old: -13% per level, -40% max; strain no longer exists, needs a new effect).
  - Scavenger's eye: job deadwood up (old: +33% per level, x2 max).
  - Deep rest: rests divide strain by more (old: 2 -> 3.5 max; rests no longer exist, needs a new effect).
  - Field rations: recharges come more often (old: +17% per level, +50% max).
- Themes revealed as Act III sections are first reached, spread over Act III.

## Open questions (parked)
1. Placement: one set per theme in every Act II section (45 sets), or one per theme per Act II part (15 sets, at each part's last section)?
2. Strength outside Act II: how strong are these bonuses in Act I and Act III (the Act I legacy tasks use 10% in Act II)?
3. Which Act III section reveals which theme?
4. Act III structure, sections, length and pacing target.
