# Research: ideas from other open-source incremental games

Ideas only unless the licence allows reuse. Nothing here is approved until the owner picks it (HARD RULE). Started 2026-11-05.

## Licences at a glance
| Game | Repo | Licence | What we may take |
|---|---|---|---|
| Idle Loops | github.com/dmchurch/omsi-loops (active fork; older lloyd-delacroix/omsi-loops) | none in either fork | ideas only |
| wrtsc | github.com/deifactor/wrtsc | MIT (c) 2022 Ash | ideas; code with the MIT notice |
| Immortality Idle | github.com/immortalityidle/immortalityidle.github.io | no LICENSE file; README asks derived code to stay open | ideas only (unless Selene goes open source) |
| Progress Knight Quest | github.com/indomit/progress_knight_2 | no LICENSE file | ideas only |
| Progress Knight (original) | github.com/ihtasham42/progress-knight | Unlicense (public domain) | ideas and code |
| Antimatter Dimensions | github.com/IvarK/AntimatterDimensionsSourceCode | MIT (c) 2017 IvarK | ideas; code with the MIT notice |
| Trimps | github.com/Trimps/Trimps.github.io | GPL (license.txt says v2, main.js header says v3 or later) | ideas only |
| The Modding Tree | github.com/Acamaeda/The-Modding-Tree | MIT (c) 2020 Acamaeda, plus Prestige Tree MIT (c) 2020 Jacorb | ideas; code with both notices |
| ZzFX | github.com/KilledByAPixel/ZzFX | MIT (c) 2019 Frank Force | **used** (generator in the audio script, full MIT notice in the code, credited in Settings > Credits) |
| game-icons.net | github.com/game-icons/icons | CC BY 3.0 (Lorc, Delapouite, Skoll); CC0 only where marked | **used** (32 icons, credited in Settings > Credits and project/icons/README.md) |
| Fonts | github.com/google/fonts | SIL OFL 1.1 | **used** (renamed subsets; copyright and licence kept in each font's name table, credited in Credits) |
| Synergism | github.com/Pseudo-Corp/SynergismOfficial | MIT | ideas; code with the notice |
| Evolve | github.com/pmotschmann/Evolve | MPL-2.0 (file-level copyleft) | ideas only |
| Bitburner | github.com/bitburner-official/bitburner-src | Apache-2.0 + Commons Clause (no selling) | ideas only |
| Gooboo | github.com/Tendsty/gooboo | GPL-3.0-or-later | ideas only |
| Shark Game | github.com/Toby222/SharkGame | MIT | ideas; code with the notice |
| Kittens Game | github.com/nuclear-unicorn/kittensgame | "WET PAWS" (no derivative works, no commercial use) | ideas only, copy nothing |
| A Dark Room | github.com/doublespeakgames/adarkroom | MPL-2.0 | ideas only |
| Prestige Tree | github.com/Jacorb90/Prestige-Tree | MIT | ideas; code with the notice |

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
3. **Charging fallback instead of failing** (reasons on the Now line BUILT, chunk C) (Immortality Idle `autoRestUnlocked`): when the next row can't run, detour to a charging station and say why. Partly what auto-forage already does; the forecast now shows the effect.
4. **Life summary at death** (BUILT, chunk B) (Immortality Idle `life-summary/`): cause, then each permanent gain (familiarity per task, records, automation progress), a tip, and "show every life". Selene's death screen could list what carried over.
5. **This life vs all lives statistics** (time per task BUILT, chunk B) (Immortality Idle `statistics-panel/`): time per task this seedling and in total; "in-game time per real minute".
6. **Record column and pending bar** (PKQ; dropped: familiarity counts at once, and section bests are in the log tables): this seedling's count next to the best ever; a lighter "banked when this seedling ends" fill on familiarity.
7. **Pause before death** (BUILT, chunk A) (Immortality Idle `pauseBeforeDeath`): pause once shortly before the forecast death, to squeeze in last actions. Easy now that the forecast exists.
8. **Locked entries stay in the queue, greyed out** with a separate player "skip" flag (skip and Enable all / Disable all BUILT, chunk A) (Immortality Idle `disabled` vs `userDisabled`); Enable all / Disable all.
9. **Do once now** (dropped: tapping already runs a task at once), **x10 / x100 repeat steps** (BUILT as long-press + for copies, chunk C), **turbo bars** (Selene already does this for jobs), **safe import** (BUILT, chunk C), **keybinds** (Space pauses; arrows switch tabs: BUILT, chunk C).
10. Original Progress Knight's **auto-learn** (BUILT in adapted form as the Least familiar queue sort, chunk C) (train the lowest-level skill not excluded by a tick box; Unlicense, code reusable): a "spread familiarity" mode for drills.

Avoid: sprawl (Immortality Idle is 42k lines), rebirth costs that wipe gear, opaque soft caps, a second "banked time" currency, prestige layers that reset records (breaks the seedling-count design), huge numbers, progress-resetting challenges, date-based events (fear of missing out), one-key rebirths.

## Round 1c (owner's priority, 2026-11-05): Increlution, Your Chronicle, Idling to Rule the Gods, Terraformental
All four are closed source (ideas only, from store pages, wikis, patch notes and player threads). Increlution (Gniller, Steam) is Selene's closest relative; Terraformental (Shadowsand, galaxy.click/itch/Steam) is itself inspired by Increlution; Your Chronicle is by Samurai Games (not Hamster-on); ITRTG is by Shugasu.

Owner's picks (2026-11-05 07:54): all greens of the ranked list (forecast warning for starving settings, clear queue keeping the current task, icons on task cards, this-seedling vs kept tags) BUILT in build "forecast hints and icons"; a queue row that loads a preset and favourite/hide filters BUILT in build "preset rows and filters". Not picked: priority tiers, challenges (maybe after tuning), work-until-familiarity rows, lower thresholds, speed past x10, passive job share, manual crossing hold.

Combined top 8, best value first (status for Selene in brackets):
1. **Priority tiers for automated tasks** (Increlution: Off/Low/Medium/High; ties top to bottom; a low-health override). Fills gaps without queue edits. [open; Selene removed priorities for chains once, so this needs a design talk]
2. **Hold a crossing at 99%** / stop a chain before its last step (Increlution, Terraformental). [partly there: automated crossings already wait while work is pending; a manual "hold" toggle is open]
3. **Challenges with seedling-count or time milestones** (ITRTG, repeatable, bonus each time): "clear section N in K seedlings", "no gear". Rewards the key metric directly. [open; a bigger feature]
4. **A queue row that loads another preset** (Your Chronicle template chaining). [open; complements preset triggers]
5. **Chains graduating into one combined action** with a small bonus (Terraformental). [mostly there: linked chains and chain flow]
6. **Icons on tasks for one-time records, gear unlocks, crossings; favourite / hide filters** (Increlution, Terraformental). [open]
7. **Gather only what's needed for queued gear** (Increlution). [there: automated deadwood jobs gather up to the queued gear's cost]
8. **Long-press "x max"; clear the queue but keep the current task** (Your Chronicle, Increlution). [long-press copies BUILT; keep-current open]

Also noted: lower automation thresholds after a related task (Increlution); a passive share of job work as a legacy theme (Increlution); per-life vs permanent parts of a bonus (Your Chronicle); "work until familiarity X, then the next row" (ITRTG, unverified); after the x10 cap, turn speed into shorter real time (Terraformental); a forecast warning when a setting would starve the seedling (Terraformental's "do not use" bottles).

Avoid: very high automation thresholds; automation that fails silently; offline bonuses; paid queue slots; daily grinds; many overlapping currencies; settings that reset every loop; tedious opening steps every loop; one mistake ruining a long run; multipliers that stop mattering.

Sources: [Increlution on Steam](https://store.steampowered.com/app/1593350), [Your Chronicle on Steam](https://store.steampowered.com/app/1546320), [ITRTG wiki](https://itrtg.wiki.gg/wiki/New_Players_Guide), [Terraformental on galaxy.click](https://galaxy.click/play/490), [Terraformental on itch.io](https://sh4dowsand.itch.io/terraformental).

## Rounds 2 and 3 (2026-11-05): Antimatter Dimensions, Trimps; The Modding Tree, ZzFX/ZzFXM, game-icons.net
Licences checked in the repos: Antimatter Dimensions MIT (IvarK/AntimatterDimensionsSourceCode); Trimps GPL v2 or later (Trimps/Trimps.github.io; ideas only); The Modding Tree MIT (Acamaeda/The-Modding-Tree; its `drawTreeBranch` says it was taken from Antimatter Dimensions, so don't copy it); ZzFX MIT (KilledByAPixel/ZzFX), ZzFXM MIT (keithclark/ZzFXM); game-icons.net CC BY 3.0 per author (credit "Icons made by {author}. Available on https://game-icons.net", reachable from a menu, with the licence link; a few authors are CC0).

Owner's picks (2026-11-05 08:36): **all green and yellow except challenges**, built in five chunks: 1 save safety (BUILT, build "save safety"), 2 sound (BUILT, build "event sounds"), 3 triggers and FAQ (BUILT, build "trigger table"), 4 map and icons (BUILT, build "route and icons"), 5 before-publishing set (BUILT, build "publishing set").

Ranked (🟢 worth it now · 🟡 maybe later · 🔴 not worth it · ⚪ already in the game):
- 🟢 **Rolling backups per slot** (AD `storage.js` `AutoBackupSlots`, `saveToReserveSlot`): 5 min / 30 min / 2 h of play, plus one just before a slot is replaced. BUILT (chunk 1).
- 🟢 **Never save broken numbers** (AD `checkPlayerObject`, TMT `NaNcheck`). BUILT (chunk 1).
- 🟢 **Fix tips when pasting a queue** (AD automator errors with a tip, unlock-aware): "did you mean", "locked: opens after". BUILT (chunk 1).
- 🟢 **Sounds for crossing, sprout, gear built, low energy** (ZzFX generator only, on the game's own audio context; prebuilt; about 1.3 KB). BUILT (chunk 2, build "event sounds").
- 🟢 **Average row on the run history** (AD past-runs `averageRun`). BUILT (chunk 1).
- 🟡 **Fuller trigger table** (Trimps Map at Zone: on/off, from/through, every N, priority). BUILT (chunk 3, build "trigger table").
- 🟡 **FAQ search, open on the current tab, a hotkey table listed in the FAQ** (AD h2p, `hotkeys.js`; TMT hotkeys as data). BUILT (chunk 3, build "trigger table").
- 🟡 **Route overview on the Map tab** (TMT tree as a 2-D array with ghost nodes; unreached sections hidden). BUILT (chunk 4, build "route and icons").
- 🟡 **Icons from game-icons.net plus a Credits page** (Lorc, Delapouite, Skoll...; keep icons under ~2 KB). BUILT (chunk 4, build "route and icons").
- 🟡 **Welcome-back recap** (AD catch-up modal), **Log filter chips** (Trimps message filters), **screen-reader announcements** (Trimps `screenReaderAssert`), **pause all automation** (AD global autobuyer toggle). BUILT (chunk 5, build "publishing set").
- 🟡 Challenges (TMT): not picked (Act III is parked).
- 🔴 AD's Automator language (scripting creep), ZzFXM music (pre-renders tens of MB, loses the live mood filter), bundling Vue / TMT's framework, A/B rule-set swaps (presets cover it), a news ticker, offline backups, per-task ratio caps.
- ⚪ Named slots, a save prefix (`LPZ1:`), import summary, tab dots, toasts, FAQ unfolding with progress, overwrite panels, the Map tab, preset triggers, life summary, run history.

Avoid (seen there): lossy editor conversions (AD text to blocks drops lines with errors), a second copy of every setting per act (Trimps U2), explanations behind a Shift key, magic-number settings, UIs built from huge HTML strings, oversized flavour systems, offline-progress machinery, caps shown only by hiding a button, scripting creep.

## Round 4 (2026-11-05): licence recheck, new repos, performance
Owner's picks (2026-11-05 10:23): **all** (C1-C3, P1-P9, U1-U8, D1), built in six chunks: 1 credits and docs, 2 UI performance, 3 sound and Android timers, 4 save safety and export, 5 queue and info, 6 section targets.

### Credits audit
- What Selene ships from others: ZzFXMicro 1.4.0 (MIT), 32 game-icons.net icons (CC BY 3.0), three OFL font families. No code from any game.
- ZzFX: MIT requires the full permission notice in copies; the code comment had a paraphrase. Fixed (C1): full MIT text in the comment.
- Fonts: all 8 embedded faces keep name IDs 0 (copyright), 13 (licence) and 14 (licence URL), which OFL clause 2 allows; renamed as OFL 2.6 requires. IBM Plex Sans 3.201 says (c) 2019, Credits said 2017: fixed (C2) to 2017-2019.
- Icons: Credits name the authors, the site, the licence link, the changes and no endorsement, as CC BY 3.0 and game-icons.net ask.
- Ideas need no credit; a courtesy line "Inspired by Increlution (Gniller), Idle Loops, Immortality Idle and Progress Knight" was added (C3), as is usual for loop games (wrtsc credits Idle Loops the same way).

### Rechecked repos: notable since round 1-3
- Idle Loops (dmchurch fork, 3P.1.3, 2026-10-29): forecast in a Web Worker (`predictor-worker.js`); pause before restart / on failed loop / on complete (`driver.js` `prepareRestart`); per-minute rate of a tracked stat (`predictor.js` `trackedStats`); merged repeated log lines (`actionLog.js`).
- Immortality Idle (2026-11-04): mobile work; clearer messages when a task can't be queued.
- Progress Knight Quest 2.7.0: offline progress bar that stops on death; save migration fixes; mobile layout.
- Antimatter Dimensions: buy-10 toggle, iOS app. Trimps: ScreenReader.html mode. ZzFX 1.4.0 is current.

### New repos: ideas
- Synergism: reset history table with "load this setup" (`src/History.ts`); export file names with version and time; Android share export (`ImportExport.ts`).
- Evolve: blocker shown per queue item (`functions.js` `timeCheck`); this run / all time stats.
- Bitburner: compare saves before import (`ImportSaveComparison.tsx`); recovery mode when loading crashes (`RecoveryRoot.tsx`); what's new on version change.
- Gooboo: save checksum and refusing newer-version saves (`savefile.js`); stat breakdown (`StatBreakdown.vue`); backup reminder by play time; short unlock notes.
- Shark Game: par time per world with a reward (`gateway.js` `getPar`); death text by progress.
- Kittens Game: capped queue rows marked; warning before a self-defeating action.
- A Dark Room: messages held per screen; swipe navigation.

### Performance (measured headless, 412x900, x5 speed; "4x" = CPU slowed four times, like a phone)
- The UI redrew at 60 fps whether or not anything changed, also while paused (paused 933 ms/s of main-thread work vs running 908 at 4x). Late save (Contested Boughs, 39 queued) at 4x: 37 fps, 41 long tasks over 50 ms in 20 s. The simulation (`step`) is about 3% of samples.
- A 10 Hz UI: 908 -> 271 ms/s (-70%), same simulation rate.
- `renderTasks` spent 70-99% of its time building its 2-3 KB change key (rebuilds were rare); it was also called twice every 0.4 s.
- 19-27 DOM writes per frame of unchanged values (HUD, Now line, buttons, card titles), one layout per frame.
- Forecast slices overshot (up to 33 ms at 4x; clock checked every 4 steps); `JSON.stringify(S.set)` every frame.
- `save()` 9.4 ms at 4x every 5 s; storage about 110 K characters per full slot with backups (far under quota). gzip (CompressionStream) is fine; lz-string not worth it.
- Audio: the music graph runs even with music off; the two convolver reverbs are 87% of its cost (about 12% of a core).
- Startup 876 ms to DOMContentLoaded at 4x; fonts cost about 94 ms; the 700 weight of Selene Display is used only by the header title.
- Android: `hardwareAccelerated` on; `onPause` never calls `pauseTimers()`.
- Others: Antimatter Dimensions (MIT) batches UI updates per tick and saves every 30 s; Synergism (MIT) updates the HUD every 100 ms on mobile; Trimps and Evolve stagger slower work over longer loops; Evolve ticks in a Web Worker.

### Avoid (round 4)
Huge flat stat lists, hover-only tooltips, two parallel layouts, many reset layers and currencies, pacing-changing modes (hyper mode), cloud sync tied to one provider.

Sources: [Idle Loops fork](https://github.com/dmchurch/omsi-loops), [wrtsc](https://github.com/deifactor/wrtsc), [Synergism](https://github.com/Pseudo-Corp/SynergismOfficial), [Evolve](https://github.com/pmotschmann/Evolve), [Bitburner](https://github.com/bitburner-official/bitburner-src), [Gooboo](https://github.com/Tendsty/gooboo), [Shark Game](https://github.com/Toby222/SharkGame), [Kittens Game](https://github.com/nuclear-unicorn/kittensgame), [A Dark Room](https://github.com/doublespeakgames/adarkroom), [ZzFX](https://github.com/KilledByAPixel/ZzFX), [game-icons.net about](https://game-icons.net/about.html), [OFL FAQ mirror](https://www.github.com/theleagueof/licenses/blob/master/OFL-FAQ.md), [WebView onPause vs pauseTimers](https://plateaukao.github.io/blog/posts/differences-between-onpause-and-pausetimers-for-android-webview/).
