# Selene: Tidelocked: Act II design (updated 2026-11-04, names as of build "the Hearth Tree")

## APPROVED: meteor shower redesign (owner, 2026-11-04 23:37). Stage 1 BUILT 2026-11-05 (build "the Shattered Bark"); Stage 2 BUILT 2026-11-05 (build "Act II reordered"); Stage 3 BUILT 2026-11-05 (build "voyage clock")
Build in three stages, each tested and pushed on its own (HARD RULE: confirm the exact changes of each stage before building).

**Lore**
- K-7 is woken because a **meteor shower** damaged Selene a quarter of the way to Tessaly.
- WARDEN has sealed the Ember Crown behind a **ward-lock** (safety lock): the injury is serious, and kindling the Hearth Tree, even for a partial burn, would destroy the ship. The Ember Crown's crossing/finale shows "Sealed by WARDEN's ward-lock" until the hull is mended.

**Timeline: 480-year voyage**
- Meteor shower at **year 120**, a quarter of the way. All of Act I happens within days.
- Turnover (midpoint flip) at **year 240**.
- Boarders about **2-3 years before arrival**, years ~477-478.
- Arrival at **year 480**.
- Fix the Heartwood log "61 years behind schedule" to fit this, for example "120 years out; the shower knocked her off her current".
- Add a voyage clock: each section header shows the year and the share of the way. The Act screens and a new FAQ entry "Selene's voyage" give the timeline.

**Stage 1: new Act I section, position P1 (right after power): BUILT** (owner's picks 2026-11-05: danger 1.075 and crossing 9.5% slotted in, nothing else moved; Resin pressure suit +10 energy and Tessaly's promise 20 -> 10; old-save seedlings past the Taproot stay sealed out of the kindling; Hardened grain built but hidden until The Mending, id 16)
- As built: section id 15; actions scars, breachmap, resinseal, bracebough, greatgraft (needs bracebough and breachmap), sapcoax, barkcharger (charger upgrade 1.70), crossing wardlift (800, +15 deadwood carry, to the Heartwood); drills barkseal and graftdrill; jobs sapheal (cells 0.085) and barkstrip (deadwood 0.04); gear mendkit (20) and resinsuit (30); records hullog (hazard -10%) and watch15 (Stasis watch III, 1.5%). Regular work 3,150 units, length factor 1.0, cell storage 25, station reserve 10. Kindle the Hearth Tree also needs wardlift in the same life.
- Act I Stasis watch ladder 1 / 1.5 / 1.5 / 2 / 2 / 2 %; display numerals renumbered in route order (ids kept).
- Legacy level = share of a theme's six finals (was five). Shattered Bark set ids lgb*; Hardened grain set ids lg1w*, lg2w*, lgbw*, lg3w*, lg4w*, lg5w* (theme key `wear`, effect x(1 - 0.4 x level/3) on Act II wear).
- New order: Seedling Vaults -> Taproot Galleries -> **The Shattered Bark** (subtitle "Hull · the meteor wounds") -> The Heartwood -> Canopy Gardens -> Ember Crown.
- Content:
  - **2x2 interlocking steps before the crossing:** Map the meteor breaches -> Seal the smaller breaches with resin; Brace the split boughs -> Graft living bark over the great wound. Both pairs feed the crossing "Lift the ward-lock on the Hearth Tree's fire".
  - **Other actions:** for example Survey the scars, Coax sap back into the scarred wood.
  - **Drills (at least 2):** Pressure-seal drills on the outer bark; Grafting drills on dead boughs. (One drill per section from 2026-11-05: Grafting drills removed, Pressure-seal drills counts double.)
  - **Energy:** charging station "Charge off the healing sap" and charger upgrade "Root a charger in the healing bark".
  - **Deadwood job:** Strip the shattered bark.
  - **Gear (at least 1):** Bark-mender's kit (work here faster); Resin pressure suit (energy, less hazard).
  - **Archive record (at least 1):** "Hull integrity log" (for example hazard -10%), plus its own Stasis watch.
- **New fifth legacy theme "Hardened grain", effect E2:** Act II wear builds slower, up to -40% at full. It has a five-part set (+ optional drill) in every Act I section, like the others, and is revealed on first reaching **The Mending** (Act II).
- **Implementation notes:**
  - Give new sections NEW internal ids (do not renumber 1-14: saves store progress by section id and task ids).
  - Ordering through the section path (`pathOf`, `zBefore`/`zAfter`, `t.to`), not id arithmetic. Check every `z + 1`, `isA2(z)` (z >= 6), the five-entry `fin` arrays (hist, bestSec, bestAll), `firstAt`, run-total columns and log tables.
  - Stasis watch ladder re-spread: still -10% across Act I and -50% in total.
  - The energy cap stays at +100 for Act I.
  - The new section is untuned: it joins the section-by-section retune. Seedling Vaults stays FROZEN.

**Stage 2: Act II reordered: BUILT** (owner's picks 2026-11-05: progression values re-assigned by route position with The Mending slotted in, Arrival's end unchanged; story text the new order breaks fixed now, years wait for Stage 3)
- As built: route 9, 10, 11, 12, 6, 7, 8, 16, 13, 14 (`ACT2R`). Kindling leads into The Long Current; Reach the turnover point is a crossing into Turnover; Drop out of relativistic speed is the long-watch finale (part B) into Bark Breach; Cut the hive loose is a crossing into The Mending; Rekindle the Hearthfire is the Boarders finale (part A) into the Tessaly System; Establish a safe orbit stays part C. Runs stop at 5, 12, 16, 14.
- The Mending (id 16): tally, cutscars, clearhusks, resapline, groveheal, emberbed, mendcharger (3.40), ws16, finale rekindle (650); drills menddrill, emberdrill (emberdrill removed 2026-11-05: one drill per section); jobs mendsap (cells 0.19), husktrim (grafts 0.19); gear mendframe (260, The Mending 30% faster); records hearthlog (Act II wear -10%), watch16 (Stasis watch XIV, 4.5%). About 2,620 units, length factor 1.0, danger 2.51, crossing 39.5%, wear 1.0.
- Legacy reveals by route position: Storage optimization at The Drift, Dampening at Turnover, Echo at Contested Boughs, Hardened grain at The Mending, Overclock at the Tessaly System. Revealed themes are kept in the save (`a2run.lrev`); saves keep what the old rule revealed.
1. **The long watch:** The Long Current, The Drift, The Long Dark, **Turnover** (moves here: the flip is at the midpoint).
2. **Boarders** (2-3 years before Tessaly, while braking): Bark Breach, Contested Boughs, The Hive Ship, **new: The Mending**. The Mending repairs the boarders' damage: lighter than the meteor shower (shorter, lower hazards). Its finale is **"Rekindle the Hearthfire"**.
3. **Arrival:** The Tessaly System, Tessaly Orbit.

Notes:
- Re-assign legacy reveals, Stasis watches, parts/finales (`a2run.done`), energy-cap steps (+100 Boarders, +100 Long Watch) and danger ramps to the new order.
- Saves already in Act II continue from their current section in the new order.

**Stage 3: voyage clock and texts: BUILT** (owner's picks 2026-11-05: clock A, fixed year per section; FAQ entry gated to Act II)
- As built: `yr` on every zone, `VOYAGE = 480`, `voyTxt(z)` = "Year N · P% of the voyage" (P = round(N/480 x 100)), shown as a second header line on the Tasks and Auto tabs (not in the top bar). Years: Act I all 120 (25%); The Long Current 120, The Drift 160 (33%), The Long Dark 200 (42%), Turnover 240 (50%); Bark Breach 477 (99%), Contested Boughs 477, The Hive Ship 478 (100%), The Mending 478; The Tessaly System 479, Tessaly Orbit 480. The 240 -> 477 jump happens in Turnover's finale (Drop out of relativistic speed).
- Texts: Heartwood log "Its chronometer rings count 120 years out; the meteor shower knocked her off her current."; intro line "Year 120 of a 480-year voyage..."; kindling screen gives the 360 more years (turnover 240, Tessaly 480); halfway log "Ahead, Tessaly's sun, still only a bright star."; Flip Selene "For the first time in 240 years"; Drop out of relativistic speed opens "Two hundred and thirty-seven years of braking later"; FAQ "Selene's voyage" (gate `a2`); FAQ "Act II" now says ten more sections.
- Section headers, Act screens, the FAQ entry "Selene's voyage", and log texts that mention the timeline.

## World and lore (2026-11-04)
- The Root-Kin of Earth: a highly advanced techno-magical civilisation that grows its technology from specialised, magically hardened trees. Tools, cities, vehicles and ships are organic. No nation states, local cultures preserved; one World Government for thousands of years, a democracy with slight meritocratic elements.
- **Selene** (she/her, never "the Selene"), named for the Greek Moon goddess: a colony ship of living wood, shaped like a long, swept hull with crescent wings (the White Star from Babylon 5 is the shape reference; never named in the game). At her heart grows the **Hearth Tree**: her drive, her mind (WARDEN) and her hydroponic garden at once, so all of Act I happens in and around it.
- No FTL: ships ride the ambient magic that saturates the universe at relativistic speed, inside magical ward-shields and with artificial gravity, and can turn on any axis without shear or friction. Halfway there Selene flips and brakes (Turnover: restore gravity, raise the wards, plot, then flip).
- **Seedlings** (were clones): disposable drones of WARDEN and the Hearth Tree, grown for a specific task with limited autonomy. Regrown as a new version once their program and body can be improved; what one learned seeps back through the roots.
- Terms: energy (unchanged), sap cells (were charge cells), deadwood (was salvage), grafts (Act II spare parts), sprout (was decant), return to the roots (was recycle).
- Act I order: Seedling Vaults (clone stock) -> Taproot Galleries (power) -> The Shattered Bark (hull, the meteor wounds) -> The Heartwood (navigation, WARDEN's mind) -> Canopy Gardens (food) -> Ember Crown (propulsion; Kindle the Hearth Tree ends Act I).

## Flow
- **Pacing rule (owner 2026-11-05): Act II takes about twice as long as Act I** (lean bot, in-game time; `tests/totals.test.js` keeps the ratio within 1.8-2.2). Build "act ii twice act i": Act I 5.59 h, Act II 11.20 h.
- Act I = 6 sections (Seedling Vaults, Taproot Galleries, The Shattered Bark, The Heartwood, Canopy Gardens, Ember Crown). Kindling the Hearth Tree ends Act I; there is no restarting. Every seedling that kindles it carries on into Act II.
- Act II is linear, three parts, ten sections (from build "Act II reordered"):
  1. The long watch: The Long Current, The Drift, The Long Dark, Turnover (restore the artificial gravity, raise the ward-shields, plot the turnover, flip Selene end over end, bank and relight the Hearthfire, plot the approach, begin the braking burn; finale: Drop out of relativistic speed).
  2. The Boarders (while Selene brakes): Bark Breach, Contested Boughs, The Hive Ship, The Mending (finale: Rekindle the Hearthfire).
  3. Arrival: The Tessaly System (scan the gas giant, its moons, the asteroid belt, a comet tail, the radiation belt, the inner worlds; slingshot), Tessaly Orbit (orbit insertion, orbital survey, sweep debris; finale: Establish a safe orbit over Tessaly).
- Pacing: see playtest-notes.md (current: Act I 5.59 h, Act II 11.20 h in-game, lean bot).

## Difficulty
- Danger ramp (drain and hazards): x1.0 in the Seedling Vaults, +5% per Act I section (the Shattered Bark slotted in at x1.075); Act II x2.12 (Bark Breach) up to x2.60 (Tessaly Orbit) after the +18% retune.
- Stasis watch records cut drain: -10% across Act I, -50% in total.

## Ship wear and grafts (all of Act II)
- Deadwood doubles as grafts in Act II. Wear builds as a seedling works: a little in the Boarders, more over the Long Watch, most in Arrival (Grafter's toolkit x0.7). Each point of wear adds 8% drain.
- Repair: removes 1.5 wear for a fixed number of grafts (more in later sections), then a cooldown. Auto-repair (default on) and a Repair button under Grafts.
- Workshops: one action per Act II section (ws6..ws14), each shortens the repair cooldown, costs three repairs' worth of grafts, paid when work starts.
- Graft jobs are the forage: auto-scavenge (default on) works the best one when grafts run low. Fill-before-crossing fills grafts to full carry (see Section runs).
- Running out of grafts lets wear climb; a death with drain x2 or more from wear reads "Worn down with the ship".

## Legacy tasks (replace the old Act I reward points)
- Five themes, each with a set in every Act I section: Echo (Act I familiarity), Dampening (drain), Storage optimization (max energy), Overclock (game speed), Hardened grain (Act II wear, revealed at The Mending from Stage 2).
- Themes are revealed as Act II sections are first reached (route positions 2, 4, 6, 8, 9) and stay revealed.
- Each set = five actions: two pairs (A1 -> A2, B1 -> B2), then a final that needs A2 and B2. Only the final gives the bonus. A1, B1 need the section's last regular action. LEGACY_LEN 0.6.
- Mandatory: once a theme is revealed, its finals are required for the section's crossing (and for kindling the Hearth Tree). Unrevealed themes don't block.
- Not auto-queued: a toast when parts first open in a life, and a dot on the Tasks tab. Once automated they join chains and section runs.
- One optional drill per set, training only that set's five parts.
- Quartermaster's cache: unlocked the first time the Hearth Tree is kindled.

## Section runs
- **Crossing fill (base design, restored 2026-11-05):** a queued or automated crossing stops just short of finishing; the seedling finishes automated actions/drills, builds affordable automated gear, tops sap cells up to the auto-charge stop level, then **fills deadwood (grafts in Act II) to full carry**, so the next section's gear can start at once. It costs energy; that is the point. Safety net: a seedling with under 1 sap cell and energy under the charge threshold skips the deadwood and crosses. Tapping the crossing yourself crosses at once. (From 2026-11-04 06:07, `da78682`, until this fix, Act I crossings filled no deadwood: a regression.)
- "Always run sections once ready" (global): a run starts by itself whenever the current section is fully automated, clears the queue's leftovers for its sections and is pinned at the top of the queue. Runs still stop at act ends.

## Queue forecast and queue tools (2026-11-05, build "queue forecast")
- The forecast plays the current seedling forward with the real rules (queue, automation, recharges, crossings, wear) on a copy of the save. Each queue row shows the energy left when it is done and when; rows the seedling won't reach are red; "Dies here" (or "Dies before this") marks where it dies. The Outlook line and the header's time left use the forecast death and cause; the queue header shows when the queue is done, or how many rows this life gets through.
- Undo (one step) for queue edits; the queue as plain text (copy; add or replace from pasted names); presets can be named; a setting stops at the death screen when the queue wasn't finished (only with the death screen off); a "new" dot on tasks no seedling has finished yet.

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
