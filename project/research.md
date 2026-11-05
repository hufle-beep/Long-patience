# Research: ideas from other open-source incremental games

Ideas only unless the licence allows reuse. Nothing here is approved until the owner picks it (HARD RULE). Started 2026-11-05.

## Licences at a glance
| Game | Repo | Licence | What we may take |
|---|---|---|---|
| Idle Loops | (round 1) | none | ideas only |
| wrtsc | (round 1) | MIT | ideas; code with the MIT notice |
| Immortality Idle | github.com/immortalityidle/immortalityidle.github.io | no LICENSE file; README asks derived code to stay open | ideas only (unless Selene goes open source) |
| Progress Knight Quest | github.com/indomit/progress_knight_2 | no LICENSE file | ideas only |
| Progress Knight (original) | github.com/ihtasham42/progress-knight | Unlicense (public domain) | ideas and code |

## Round 1 (Idle Loops, wrtsc), best value first
1. **Queue preview / forecast**: BUILT (build "queue forecast", 2026-11-05).
2. Repeat counts on queue entries (+/−, split, cap at what's still useful, skip toggle): not built. The queue already takes several copies of a task (one copy per repetition); a count control would mostly save taps. Open.
3. Failure reasons on blocked rows (partly there already: "waiting for its requirements", "needs bigger deadwood storage"...), a per-row summary of what each finished row used and gained: open. "Pause if the queue wasn't finished": BUILT as the setting "Stop at the death screen if the queue wasn't finished".
4. Named presets: BUILT. One-step undo: BUILT. Plain-text queue export/import: BUILT ("Copy / paste" under Presets).
5. "Resets each seedling" vs "permanent" tags: open. Highlight on tasks never finished in any life: BUILT ("• new").
6. Bots as regression tests (`node --test`): BUILT (`project/tools/tests`).

## Round 1b (owner's priority, 2026-11-05): Immortality Idle and Progress Knight Quest
Immortality Idle is the closest match to Selene (repeating schedule, ageing and death, permanent "aptitude" from each life's gains, stamina exhaustion).

Best value first (combined):
1. **Preset triggers** (BUILT, chunk A) (Immortality Idle, `checkTriggers()` / `loopChangeTriggers` in `activity.service.ts`): an ordered list of "when X reaches N, load preset Y", each firing at most once per life, the first one on every new life. For Selene: "new seedling: load *Opening*; on reaching the Shattered Bark: load *Hull*; energy above 40%: load *Drills*". Builds on the named presets.
2. **Per-goal ETA with a "won't make it this life" warning** (BUILT as the next-automation line, chunk B) (Progress Knight Quest, `updateRequiredRows()` / `findNextRequirement()`): one row per category for the next unlock, with progress and an in-game/real ETA, red when it won't happen this life. For Selene: in each section header, "next automation: 7/10 completions, about 3 seedlings". The forecast could supply "this life".
3. **Charging fallback instead of failing** (Immortality Idle `autoRestUnlocked`): when the next row can't run, detour to a charging station and say why. Partly what auto-forage already does; the forecast now shows the effect.
4. **Life summary at death** (BUILT, chunk B) (Immortality Idle `life-summary/`): cause, then each permanent gain (familiarity per task, records, automation progress), a tip, and "show every life". Selene's death screen could list what carried over.
5. **This life vs all lives statistics** (time per task BUILT, chunk B) (Immortality Idle `statistics-panel/`): time per task this seedling and in total; "in-game time per real minute".
6. **Record column and pending bar** (PKQ; dropped: familiarity counts at once, and section bests are in the log tables): this seedling's count next to the best ever; a lighter "banked when this seedling ends" fill on familiarity.
7. **Pause before death** (BUILT, chunk A) (Immortality Idle `pauseBeforeDeath`): pause once shortly before the forecast death, to squeeze in last actions. Easy now that the forecast exists.
8. **Locked entries stay in the queue, greyed out** with a separate player "skip" flag (skip and Enable all / Disable all BUILT, chunk A) (Immortality Idle `disabled` vs `userDisabled`); Enable all / Disable all.
9. **Do once now** (one tick, schedule untouched), **x10 / x100 repeat steps** (long-press on mobile), **turbo bars** (bar shown full when a level takes under 0.4 s; Selene already does this for jobs), **safe import** (validate keys, stop loops, write, reload), **keybinds** (Space pauses; arrows switch tabs).
10. Original Progress Knight's **auto-learn** (train the lowest-level skill not excluded by a tick box; Unlicense, code reusable): a "spread familiarity" mode for drills.

Avoid: sprawl (Immortality Idle is 42k lines), rebirth costs that wipe gear, opaque soft caps, a second "banked time" currency, prestige layers that reset records (breaks the seedling-count design), huge numbers, progress-resetting challenges, date-based events (fear of missing out), one-key rebirths.

## Still to study (rounds)
- Round 2: Antimatter Dimensions (MIT: saves, automation UI, mobile release); Trimps (GPL, ideas only: automation).
- Round 3: The Modding Tree (MIT, for Act III later); ZzFX/ZzFXM (MIT, sound); game-icons.net (CC BY 3.0, needs a credit line).
