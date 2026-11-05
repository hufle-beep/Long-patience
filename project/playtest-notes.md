# Selene: Tidelocked: playtest notes for fine tuning

Renamed 2026-11-04 (build "the Hearth Tree"): the game was Long Patience. Clones are now **seedlings**, salvage is **deadwood**, Act II spare parts are **grafts**, charge cells are **sap cells**. Section names below are the new ones; the Act I story order is now power, then mind and navigation, then food, then propulsion, but every section kept its tasks, timings and balance values (names only).

| # | New name | Old name |
|---|---|---|
| 1 | Seedling Vaults | Vat Bay |
| 2 | Taproot Galleries (power) | Hydroponics Ring |
| 3 | The Heartwood (navigation, WARDEN's mind) | Engineering Spine |
| 4 | Canopy Gardens (food) | Command Deck |
| 5 | Ember Crown (propulsion, the Hearth Tree) | Main Drive |
| 6 | Bark Breach | Hull Breach |
| 7 | Contested Boughs | Contested Decks |
| 9 | The Long Current | The Cruise |

Sections 8 and 10-14 kept their names.

## Reporting rule (user, 2026-11-04)
**No ship days anywhere**: not in the game, not in tests, not in reports. Track and report only **in-game time** (time at normal speed x1; 1 old ship day = 10 s in-game) and **real time** (at the chosen speed). Test bots print in-game clocks (m:ss or h:mm:ss) and hours.

## Testing-only features to change before the final version
- **Death saves (build "five slots and death saves", 2026-11-04):** each of the five regular slots has its own linked death save (written at every death, loadable, never overwrites a regular slot). This is for testing. **The final version keeps only one global death save** (user, 2026-11-04).

## Section-by-section retune (started 2026-11-04)
Goal: retune one section at a time from the user's playtests, then **freeze** it. **Seedling count per section is the most important target**; task times are malleable. The end result should stay close to the current totals (Act I about 63-72 seedlings / 4.5-4.8 h in-game, Act II about 55-70 seedlings / 7.5-8 h in-game).

**Target play style (user, 2026-11-04):** a section counts as done the user's way only when **every possible action in it is finished** (all actions, drills to their cap, all gear built) by the target seedling. Lean "skip drills and gear" routes are not the yardstick.

**Freezing rule:** only freeze a section when the user says so. If a retune doesn't work in play, keep tuning; never freeze on a test-bot result alone.

### Process
1. The user plays a section on a fresh run (or carries on) and uploads a save to `saves/` right after the crossing.
2. Claude reads the save: seedlings used in that section, life lengths (in-game and real), causes of death, cells and energy on arrival, gear, records, familiarity.
3. Claude proposes changes **only to that section's knobs** (below), waits for approval, applies them, and checks the test bot that nothing earlier moved.
4. When the user says so, the section is marked **FROZEN** here with its values. Frozen sections are not touched again unless the user reopens them.

### Test bots (in /tmp/claude-0/sim, rebuilt per session if needed)
- **Lean bot** (sim11bv / sim11c / simtrace / simlean): quickest action first, crosses when nothing else fits, no drills, gear only if affordable.
- **Completionist bot** (simcomp / simcomp2): does every action, all drills to 4/4, builds all of the section's gear, then crosses. This is the one matching the user's style.
- **Act II bot**: `node sim16c.js AB` (runs the whole game through Arrival; prints death causes and Boarders / Long Watch / Arrival hours). Without `AB` it stops after Boarders. `simsnap.js` (STOPZ, STOPT, OUT) writes a save snapshot once a section is reached, for screenshots.
- **Milestone table** (`node milestones.js`, about 50 s): runs the lean whole-game bot and the completionist bot (Act I up to the Heartwood), writes `project/tools/milestones.md` (seedlings used and in-game time per section, next to each target) and prints what changed since the last table; flags a section the lean bot used more than 3x its target (and at least 10 over) or never crossed (exit code 2). Commit the table with each balance change.
- **Sanity check** (sanity.py): data duplicates, a long in-page run on a fresh game, an old-key save and two Act II saves, every tab and pop-up, and a scan for leftover old words.

### Section targets (in the game since build "section targets", 2026-11-05; badge only)
`TARGETS` in index.html: Seedling Vaults 9 and Taproot Galleries 14 (owner, frozen); Shattered Bark 11, Heartwood 6, Canopy Gardens 7, Ember Crown 4 (completionist bot, build "queue history"); Act II from the lean bot (no completionist Act II bot): Long Current 2, Drift 5, Long Dark 8, Turnover 6, Bark Breach 1, Contested Boughs 3, Hive Ship 4, Mending 1, Tessaly System 2, Tessaly Orbit 1. Counted as the seedling that first reached the next section minus the one that first reached this one (0 for the Vaults). **Update a section's target when it is frozen.**

### Per-section knobs
ZDAYS (section length; internal name), drill lengths, danger (drain and hazards), cell storage (STORE_CAP), station reserve (stationMax: RESERVE_K x section length, min 10 (Seedling Vaults 15); Act II x0.5), crossing cost into the section, which action opens the station, records/gear placed there.

### Current values (build "the Hearth Tree", 2026-11-04; balance unchanged since "Act II danger +18%")
Seedlings = seedlings that first reached the next section minus those that first reached this one (lean bot, unless noted). Bot counts for sections 2-14 are from build "cleanup" (before stasis tuning) and need re-running per section.

| # | Section | Length factor | Danger | Cell storage | Station reserve | Crossing cost in | Bot seedlings | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Seedling Vaults | **2.81** (was 2.212; drills base 25) | 1.00 | 5 | 15 | - | completionist **10** (2.212: 7 after one drill per section; was 10, then 9), lean 8; **user 9** at freeze, **user 6** on the replay at 2.212 | **retuned (B) 2026-11-05**: freeze again when the owner says |
| 2 | Taproot Galleries | 1.158 | 1.05 | 20 | 10 | 8% | lean 22, completionist 13 (14 before the longer Vaults); **user 14** | **FROZEN 2026-11-05** |
| 15 | **The Shattered Bark** (new, after the Taproot) | 1.0 | 1.075 | 25 | 10 | 9.5% | lean 21, completionist 14 | new, untuned; next to retune |
| 3 | The Heartwood | 0.686 | 1.10 | 35 | 15 | 11% | 21 | |
| 4 | Canopy Gardens | 0.606 | 1.15 | 60 | 30 | 14% | 10 | |
| 5 | Ember Crown | 0.372 | 1.20 | 90 | 30 | 17% | 7 | |
| 9 | The Long Current (long watch, first in Act II) | 0.593 | 2.12 | 25 | 10 | 20% | 3 | |
| 10 | The Drift | 0.796 | 2.18 | 25 | 10 | 23% | 9 | |
| 11 | The Long Dark | 0.796 | 2.24 | 30 | 10 | 26% | 13 | |
| 12 | Turnover (ends the long watch) | 0.756 | 2.30 | 30 | 10 | 29% | 9 | |
| 6 | Bark Breach (Boarders) | 0.677 | 2.36 | 25 | 10 | 32% | 2 | |
| 7 | Contested Boughs | 0.877 | 2.42 | 25 | 10 | 35% | 5 | |
| 8 | The Hive Ship | 0.877 | 2.48 | 30 | 10 | 38% | 6 | |
| 16 | **The Mending** (new, ends the Boarders) | 1.0 | 2.51 | 30 | 10 | 39.5% | 1 | new, untuned |
| 13 | The Tessaly System (Arrival) | 0.756 | 2.54 | 30 | 15 | 41% | 3 | |
| 14 | Tessaly Orbit | 0.756 | 2.60 | 35 | 10 | 44% | 2 | |

One drill per section (2026-11-05, build "one drill per section", owner: S1, A, double the single ones too): the second drill of each of the 14 pairs removed (the one that opens later), the kept drill and the Drift's and Hive Ship's give **0.2** per session (legacy drills 0.1). Completionist bot: Seedling Vaults 9 -> **7**, Taproot 14, Shattered Bark 11 (unchanged); lean bot and Act II bot unchanged (they skip drills). Both freezes stay (owner's replay judges them).

Drill credit (2026-11-05, build "stronger drills"): 0.04 -> **0.1** of a completion per session to every task of the section (owner: drills gave no visible familiarity). Completionist bot Seedling Vaults / Taproot / Shattered Bark: 0.04 -> 10 / 15 / 12; 0.1 -> **9 / 14 / 11**; 0.2 (tested only) -> 8 / 13 / 10. Lean bot skips drills: unchanged.

Lean bot totals:
- Build "charge after work" (2026-11-05, current): Act I **5.85 h**; Act II **11.12 h** (long watch 6.43, Boarders 3.21, Arrival 1.48). Completionist: Seedling Vaults 11, Taproot 13, Shattered Bark 9, Heartwood 6 (was 9 / 11 / 9 / 5). Lean: Vaults 15, Taproot 19, Shattered Bark 16, Heartwood 10. Auto-charge no longer charges ahead of queued work.
- Build "act ii twice act i" (2026-11-05, current; design rule: Act II about 2x Act I): Act I **5.59 h**, Act II **11.20 h** (long watch 6.36, Boarders 3.31, Arrival 1.53). Length factors: Shattered Bark 1.6, Heartwood 1.098, Canopy Gardens 0.97, Ember Crown 0.595, Act II x2.78. Completionist: Vaults 9, Taproot 11, Shattered Bark 9, Heartwood 5.
- Mechanics consolidation (2026-11-05, builds "automation at practiced", "one upgrade", "gear built when paid"; hard reset point `fallback/2026-11-05-before-mechanics`): completionist Vaults 10 -> 9, Taproot 13 -> 11, Shattered Bark 10 -> 8, Heartwood 7 -> 4; lean Act I 5.51 -> 4.37 h, Act II 7.08 -> 4.49 h; then "free crossings": Shattered Bark 7, lean Act I 4.26 h, Act II 4.32 h. The frozen Taproot moved (13 -> 11); owner 15:52 (2A): accepted for now, judged on the replay.
- Build "auto-gear gathers" (2026-11-05, current): Act I unchanged (5.40 h, 65 seedlings); Act II **7.11 h** (long watch 3.96, Boarders 2.11, Arrival 1.04). Completionist unchanged (9 / 14 / 11). Automated gear gathers its own deadwood during the life again.
- Build "crossing fill" (2026-11-05): Act I **5.40 h, 65 seedlings** (Seedling Vaults 4, Taproot 23, Shattered Bark 14, Heartwood 9, Canopy 9, Ember Crown 6); Act II **7.30 h** (long watch 3.98, Boarders 2.29, Arrival 1.03). Completionist: Seedling Vaults 10, Taproot 15, Shattered Bark 12. The bots queue their crossings, so they do use the hold: arriving with full deadwood starts each section's gear at once.
- Build "Act II reordered" (2026-11-05): Act I 5.70 h, 79 seedlings (unchanged); Act II **8.69 h** (long watch 4.89, Boarders 2.41, Arrival 1.39), 53 deaths (unchanged). The long watch now comes first, before any Act II part is finished (each finished part lowers the Act II familiarity threshold) and with Storage optimization and Dampening revealed early, so it takes most of the time; Boarders and Arrival got faster.
- Build "the Shattered Bark" (2026-11-05): Act I **5.70 h, 79 seedlings** (Seedling Vaults 4, Taproot 23, Shattered Bark 21, Heartwood 16, Canopy 8, Ember Crown 6); Act II 7.72 h (Boarders 3.49, Long Watch 2.46, Arrival 1.78), 53 deaths. Completionist: Seedling Vaults 10 (unchanged), Taproot 16, Shattered Bark 14. With Hardened grain forced on (revealed at Contested Boughs, test only): level 2.47, wear x0.67, Act II 8.20 h (its sets add Act I work).
- Build "cleanup": Act I 4.71 h in-game, 66 seedlings; Act II 7.84 h, 62 seedlings.
- Build "stasis tuning": Act I 4.50 h, 63 seedlings; Act II 7.00 h (Boarders 3.12, Long Watch 2.01, Arrival 1.87), 44 deaths.
- Build "Act II danger +18%" and "the Hearth Tree": Act I 4.50 h; Act II 7.45 h (Boarders 3.38, Long Watch 2.22, Arrival 1.85), 55 deaths. Trial levels: +5% 7.22 h / 48, +12% 7.29 h / 52, +24% 7.61 h / 59, +30% 7.74 h / 62.

Global: DRAIN_X 3.2, RESERVE_K 0.15 (Act II x0.5), energy bar 100 base, +100 Act I (Resin pressure suit +10, Tessaly's promise now +10), +100 Boarders, +100 Long Watch, +100 legacy (cap 500). No fault, no patches. No away time: the game stops when hidden.

Act II progression values (danger, crossing cost, wear, charger and workshop tiers, Stasis watches) follow the route since build "Act II reordered": wear 0.4, 0.5, 0.6, 0.9 (long watch), 1.0, 1.1, 1.3, 1.0 (Boarders, The Mending), 1.1, 1.2 (Arrival); workshop tiers 1.15 to 2.50; charger tiers 2.55 to 3.55.

**Stasis watch ladder** (records Stasis watch I-XVI, one per section in route order, each makes energy drain slower): 1, 1.5, 1.5 (Shattered Bark), 2, 2, 2 % (Act I, total -10%; was 1, 1.5, 2, 2.5, 3 before the Shattered Bark) | 3, 3, 3.5, 3.5 (long watch), 4, 4, 4.5, 4.5 (Boarders, The Mending), 5, 5 (Arrival) % (Act II, route order; Stasis watch VII-XVI) = **-50% total**. Replaced the old +8 h of time away.

### Seedling Vaults tuning log
- **2026-11-05 replay** (save `saves/hufle2-2026-11-05-1121-clone6.txt`, build with one drill per section, length 2.212): completionist clear (all 8 actions, drill 4/4, all four gear) by **seedling 6**. Lives 0:39, 1:12, 1:13, 1:23, 1:27 in-game, seedling 6 crossed at 1:48; section 7:43 in-game / 3:51 real at x2 (frozen run: 13:02). All deaths "Drained faster than it could recharge". Time spent: charging 2:13, deadwood 1:48, drill 1:25, actions about 2:20. Cause: the single drill at 0.2 per session (bot 10 -> 7; owner 9 -> 6; the owner runs about one seedling under the bot).
- Options tried on the completionist bot (Vaults / Taproot): length +20% 9/-, +27% **10/13**, +35% 11, +50% 12; station reserve 15 -> 10: 10/17; danger 1.0 -> 1.1: 10/15; drill 0.1 in the Vaults only: 8. **Owner's pick B (2026-11-05 11:32): length factor 2.212 -> 2.81.** Lean Act I 5.40 -> 5.51 h; Act II 7.11 -> 7.08 h. Completionist Shattered Bark 11 -> 10.
- Build "energy cap 500": completionist needed **29 seedlings** (each drill session about 30 s in-game after the 6.5x stretch); lean bot 10.
- Tested: drills 1/4 + reserve 10 -> completionist 15 / lean 10; drills 1/4 + reserve 20 -> 8 / 5; drills 1/4 + reserve 15 -> 11 / 6; **drills 1/4 + section x0.9 + reserve 15 -> 10 / 5 (applied as retune 1)**.
- User playtest on "retune 1": 9 seedlings. Re-run on "Act II danger +18%": 9 seedlings (below). User froze it.

### Frozen sections
Note 2026-11-05 (build "crossing fill"): crossings fill deadwood to full carry again before moving on (base design; Act I had lost it on 2026-11-04 06:07). Both freezes below were played without it. They stay frozen; the owner replays the whole game from the start to judge whether a retune is needed.
- **1 · Seedling Vaults: FROZEN 2026-11-04, reopened and retuned 2026-11-05 (B: length 2.81; see the tuning log), freeze again when the owner says.** Original freeze (build "Act II danger +18%"; unchanged by the renames): Requirement: every action, both drills 4/4 and all four gear done, root-lock iris forced by about seedling 9-10. Values: length factor 2.212, drills base 25, danger 1.00, cell storage 5, station reserve 15, Stasis watch I = -1% drain.
- **2 · Taproot Galleries: FROZEN 2026-11-05** (build "voyage clock"; untouched since "the Hearth Tree"). Requirement: every action, both drills 4/4 and all four gear (baton, doser, chitinarm, lace) done, crossing by about seedling 14 of the section. Values: length factor 1.158, danger 1.05, cell storage 20, station reserve 10, crossing cost in 8%, Stasis watch II = -1.5% drain.

---

## 2026-11-05 · Taproot Galleries freeze run (build "voyage clock")
Save: `saves/hufle2-2026-11-05-0101-clone24.txt` (fresh test save "test1"). User verdict: **14 is fine for a completionist first run; freeze it.**

- Seedling 10 reached the Taproot Galleries (Seedling Vaults took 9 again). **Seedling 24 crossed into the Shattered Bark** 3:02 in-game into its life, with everything done: all actions, both drills 4/4, all four Taproot gear (plus the Vaults gear). Arrived with 21.8 energy, 0.14 sap cells, almost no deadwood.
- Seedlings 10-23 died in the section: 12 ran out of energy, 2 killed while harvesting deadwood (seedlings 10 and 18). Lives (in-game): seedlings 10-18 about 1:48-1:59; seedlings 19-23 about 2:55-3:09.
- Section time: 33:34 in-game / 16:47 real (x2). Run total to the Shattered Bark: 46:47 in-game / 23:24 real.
- Records so far: watch1, watch2, seedbank, chitin, medrec, telomere, transit and the Vaults records. Efficiency patch at vit 199.2. Settings: x2, charge threshold 62%, always run sections.

## 2026-11-04 · Seedling Vaults freeze run (build "Act II danger +18%", then called the Vat Bay)
Save: `saves/hufle2-2026-11-04-1241-clone10.txt`. User verdict: **freeze this as the Section 1 requirement.**

- **Seedling 9 forced the root-lock iris** (then: the pressure hatch) 1:52 in-game into its life (0:56 real at x2), with everything done: all actions, both drills 4/4, Bark-knife kit, Sap-line spigot, Moss rebreather, Woven cell sling.
- Seedlings 1-8 died in the section, all "Drained faster than it could recharge": lives (in-game / real at x2) 0:59/0:29, 1:03/0:31, 1:13/0:37, 1:23/0:42, 1:27/0:44, 1:28/0:44, 1:39/0:50, 1:58/0:59.
- Seedling 9 was later returned to the roots by choice in the Taproot Galleries; seedling 10 is current there (31.6/100 energy, 3.5 sap cells, 0 deadwood).
- Run totals: the Taproot Galleries were first reached at 13:02 in-game / 6:31 real. Total so far about 14:44 in-game, 7:22 real.
- Records: Sprouting cache, Maintenance manual, Root memory, Stasis watch I. Efficiency patch at vit 58.4.
- Settings: speed x2, charge threshold 62%, always run sections, keep queue.

## 2026-11-04 · Seedling Vaults on a fresh save (build "longer vat bay", before the fault was removed)
User verdict then: **finishing section 1 with 10 seedlings is perfect.**

Save: `saves/hufle2-2026-11-04-0828-clone10.txt`.

- Seedling 10 reached section 2 at 2:34 in-game into its life (1:17 real at x2 speed). Total play time so far 12:12 real.
- Seedlings 1-9 all died in section 1 of "Ran out of energy": lives (in-game / real) 1:16/0:38, 2:25/1:12, 2:32/1:16, 2:34/1:17, 2:35/1:17, 2:36/1:18, 2:37/1:18, 2:38/1:19, 2:38/1:19.
- Seedling 10 arrived in section 2 with 0 cells, 0 deadwood and 29/100 energy.
