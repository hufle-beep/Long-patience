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
- **Sanity check** (sanity.py): data duplicates, a long in-page run on a fresh game, an old-key save and two Act II saves, every tab and pop-up, and a scan for leftover old words.

### Per-section knobs
ZDAYS (section length; internal name), drill lengths, danger (drain and hazards), cell storage (STORE_CAP), station reserve (stationMax: RESERVE_K x section length, min 10 (Seedling Vaults 15); Act II x0.5), crossing cost into the section, which action opens the station, records/gear placed there.

### Current values (build "the Hearth Tree", 2026-11-04; balance unchanged since "Act II danger +18%")
Seedlings = seedlings that first reached the next section minus those that first reached this one (lean bot, unless noted). Bot counts for sections 2-14 are from build "cleanup" (before stasis tuning) and need re-running per section.

| # | Section | Length factor | Danger | Cell storage | Station reserve | Crossing cost in | Bot seedlings | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Seedling Vaults | 2.212 (drills base 25) | 1.00 | 5 | 15 | - | completionist 10, lean 4-5; **user 9** | **FROZEN 2026-11-04** |
| 2 | Taproot Galleries | 1.158 | 1.05 | 20 | 10 | 8% | 23 | next to retune |
| 3 | The Heartwood | 0.686 | 1.10 | 35 | 15 | 11% | 21 | |
| 4 | Canopy Gardens | 0.606 | 1.15 | 60 | 30 | 14% | 10 | |
| 5 | Ember Crown | 0.372 | 1.20 | 90 | 30 | 17% | 7 | |
| 6 | Bark Breach | 0.677 | 2.12 | 25 | 10 | 20% | 3 | |
| 7 | Contested Boughs | 0.877 | 2.18 | 25 | 10 | 23% | 12 | |
| 8 | The Hive Ship | 0.877 | 2.24 | 30 | 10 | 26% | 17 | |
| 9 | The Long Current | 0.593 | 2.30 | 25 | 10 | 29% | 4 | |
| 10 | The Drift | 0.796 | 2.36 | 25 | 10 | 32% | 6 | |
| 11 | The Long Dark | 0.796 | 2.42 | 30 | 10 | 35% | 8 | |
| 12 | Turnover | 0.756 | 2.48 | 30 | 10 | 38% | 4 | |
| 13 | The Tessaly System | 0.756 | 2.54 | 30 | 15 | 41% | 5 | |
| 14 | Tessaly Orbit | 0.756 | 2.60 | 35 | 10 | 44% | 3 | |

Lean bot totals:
- Build "cleanup": Act I 4.71 h in-game, 66 seedlings; Act II 7.84 h, 62 seedlings.
- Build "stasis tuning": Act I 4.50 h, 63 seedlings; Act II 7.00 h (Boarders 3.12, Long Watch 2.01, Arrival 1.87), 44 deaths.
- Build "Act II danger +18%" and "the Hearth Tree" (current): Act I 4.50 h; Act II 7.45 h (Boarders 3.38, Long Watch 2.22, Arrival 1.85), 55 deaths. Trial levels: +5% 7.22 h / 48, +12% 7.29 h / 52, +24% 7.61 h / 59, +30% 7.74 h / 62.

Global: DRAIN_X 3.2, RESERVE_K 0.15 (Act II x0.5), energy bar 100 base, +100 Act I, +100 Boarders, +100 Long Watch, +100 legacy (cap 500). No fault, no patches. No away time: the game stops when hidden.

**Stasis watch ladder** (records Stasis watch I-XIV, one per section, each makes energy drain slower): 1, 1.5, 2, 2.5, 3 % (Act I, total -10%) | 3, 3.5, 4, 4, 4.5, 4.5, 5, 5.5, 6 % (Act II) = **-50% total**. Replaced the old +8 h of time away.

### Seedling Vaults tuning log
- Build "energy cap 500": completionist needed **29 seedlings** (each drill session about 30 s in-game after the 6.5x stretch); lean bot 10.
- Tested: drills 1/4 + reserve 10 -> completionist 15 / lean 10; drills 1/4 + reserve 20 -> 8 / 5; drills 1/4 + reserve 15 -> 11 / 6; **drills 1/4 + section x0.9 + reserve 15 -> 10 / 5 (applied as retune 1)**.
- User playtest on "retune 1": 9 seedlings. Re-run on "Act II danger +18%": 9 seedlings (below). User froze it.

### Frozen sections
- **1 · Seedling Vaults: FROZEN 2026-11-04** (build "Act II danger +18%"; unchanged by the renames). Requirement: every action, both drills 4/4 and all four gear done, root-lock iris forced by about seedling 9-10. Values: length factor 2.212, drills base 25, danger 1.00, cell storage 5, station reserve 15, Stasis watch I = -1% drain.

---

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
