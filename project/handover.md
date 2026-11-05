# Handover: Selene: Tidelocked

Last updated: 2026-11-05 05:00 (build "queue summaries", chunk B of three approved queue chunks). New in chunk B: a **life summary** on the death screen (records found, now automatable, closest automations, next to the familiarity gains), a **next-automation line** in each section header (from the forecast: "this seedling" or "about N more seedlings"), and **time spent per task** (this seedling and all seedlings, in-game) on the Mastery tab. Chunk A (build "queue triggers"): preset triggers, skip toggles, pause before the forecast death. Earlier (build "queue forecast"): the forecast, Undo, queue as text, named presets, death-screen-if-unfinished, "new" marks, regression tests. Chunk C (Now-line reasons, safe import, arrow keys, "least familiar first", long-press +) comes next. No balance change. Fallback build on branch `fallback/2026-11-05-embedded-fonts`. Seedling Vaults and Taproot Galleries FROZEN. Update this file in every push.

## 1. What the game is
An incremental "clone-loop" game in one HTML file (like Increlution/Incremortal). You are K-7, a **seedling** (disposable drone of WARDEN and the Hearth Tree) aboard **Selene**, a living-wood colony ship of the Root-Kin of Earth. Each seedling works tasks until its energy runs out; familiarity, records and automation carry over to the next one.

- **Act I** (six sections, all inside the Hearth Tree; route by section id 1, 2, 15, 3, 4, 5): Seedling Vaults -> Taproot Galleries (power) -> **The Shattered Bark** (id 15: the hull, the meteor wounds) -> The Heartwood (navigation, WARDEN's mind) -> Canopy Gardens (food) -> Ember Crown (propulsion). Ends with "Kindle the Hearth Tree", which WARDEN's ward-lock seals until the same seedling has done "Lift the ward-lock on the Hearth Tree's fire" (the Shattered Bark crossing).
- **Act II** (linear, route `ACT2R` = 9, 10, 11, 12, 6, 7, 8, 16, 13, 14): The long watch (The Long Current, The Drift, The Long Dark, Turnover; finale Drop out of relativistic speed = part B), Boarders (Bark Breach, Contested Boughs, The Hive Ship, **The Mending** id 16; finale Rekindle the Hearthfire = part A), Arrival (The Tessaly System, Tessaly Orbit; finale Establish a safe orbit = part C).
- **Act III**: parked (see design.md).

Play: https://hufle-beep.github.io/Long-patience/ · Android APK: release `android-latest`, file `LongPatience.apk`.

## 2. Repository
- `index.html`: the whole game (~4,100 lines, ~535 KB, of which ~160 KB is the embedded fonts in `<style id="fonts">` at the top). Three scripts:
  - `<script id="logic">` (from ~line 486): data and simulation. The test bots eval this block.
  - `<script id="audio">` (~2084): music and sound.
  - `<script id="ui">` (~2253): rendering, saves, menus.
- `android/`: the WebView app (MainActivity.java with `AndroidBridge` for file export and in-app updates, `colors.xml`, `strings.xml`, keystore `longpatience.keystore` in repo).
- `.github/workflows/android.yml`: builds the APK on every push that touches `index.html`, `android/**` or the workflow, then:
  - uploads it to the `android-latest` release as LongPatience-next.apk, then swaps it in (retries);
  - updates the release title "Selene: Tidelocked for Android (build N)" (the app reads N from the title);
  - keeps a backup copy as release `android-build-N` and deletes backup releases beyond the newest 5.
- `.github/workflows/restore-points.yml`: on every push, keeps `restore/<date>-<commit>` tags on the newest 5 commits (tags can't be created from Claude's workspace).
- GitHub Pages serves the repo root (the "pages build and deployment" workflow runs on every push).
- `saves/`: playtest saves uploaded by the owner (format `LPZ1:` + base64 gzip JSON).
- `project/`: these docs and `tools/`.

## 3. Core systems (where to look in index.html)
- **Time:**
  - `DPS = 8` ticks per real second at x1; `TPD = 80` ticks per internal "day unit" (10 s in-game).
  - Players only ever see in-game time (blue `.tgm`) and real time (amber `.trl`); remaining time is red. `fmtDays(ticks)` formats an in-game clock.
  - The game stops when the tab or app is hidden. There is no away time.
  - Speed menu x1/x2/x5: `SPEEDS`. Unlocks are kept in localStorage and in the save (`S.spdUnl`). **Test version:** `TEST_ALL_SPEEDS = true` opens every speed from the start without recording an unlock (`speedOpen` vs `earnedSpeed`); it goes off before release.
- **Energy:**
  - `drainNow(haz, wear, z)` = min((HUNGER + haz) x danger, MAX_DRAIN x danger) x DRAIN_X(3.2) x (1 - stasis) / drainDiv() / vitDiv().
  - `danger(z)` comes from `DANGER`.
  - `vitDiv` is the death award ("efficiency patch from run and memory analysis"): it grows with `S.vit`.
  - Stasis is the sum of the Stasis watch records: -10% across Act I, -50% in total.
  - Max energy: 100 base, +100 from Act I records/gear, +100 Long Watch, +100 Boarders, +100 legacy Storage optimization (cap 500).
- **Sections and the route (from build "the Shattered Bark"):**
  - Section ids never change (saves store progress by them); new sections get new ids (the Shattered Bark is 15, The Mending will be 16).
  - Order comes from the route, never from id arithmetic: `ACT1 = [1, 2, 15, 3, 4, 5]`, `ACT2R = [9, 10, 11, 12, 6, 7, 8, 16, 13, 14]`, `ROUTE` (both), `ACT_ENDS` (runs stop there: 5, 12, 16, 14), `pathOf()`, `nextZone(z)`, `zBefore`/`zAfter`, `act1No(z)` (Act I position 1-6). `ZN(id)` looks a zone up by id (`ZBY`); `isA2(z)` reads the zone's `act`.
  - Crossings take `t.to` or `nextZone(t.z)`; gear opened by a crossing belongs to the section it leads into (`gearZone`).
  - Seedling tables: `fin` arrays (hist, `bestSec`, `bestAll`) have one entry per Act I route position, each the time the next section (or the kindling) was reached; hist `sec` is the Act I position, 7 = kindled. Saves from before the Shattered Bark are migrated once (`S.hullv`): an empty 'reached the Shattered Bark' entry is inserted at position 2 and positions 3+ move up one.
- **Sap cells and stations:**
  - Cells are stored in `L.food.ration` (store id `ration`, display name "Sap cells"); storage is `STORE_CAP` per section.
  - Charging stations are `kind:'job'` tasks with `prod.rations`. Each holds `stationMax(z)` (RESERVE_K 0.15, Act II x0.5).
  - Recharges have a cooldown `MEAL_CD`; charger upgrades (`MEAL_UP`) shorten it.
  - Crossings cost `crossCost(z)` of the cells carried: an explicit table `CROSS_COST` by section id (Shattered Bark 9.5%).
  - Auto-forage is standard. "Charge when needed" is `S.set.autoFeed`, and the threshold is `foodPct`.
- **Deadwood and grafts:**
  - Stored in `L.salvage`. `salW(z)` gives the display word: "deadwood" in Act I, "grafts" in Act II.
  - Gear (`ITEMS`) is built from it, with assembly tasks `b:<id>` (`BT`).
  - Act II wear (`WEAR_RATE`, by route: least early in the long watch, most in Arrival) adds drain. Repairs cost grafts. There are workshops ws6-ws14 and ws16; their tiers (`REPAIR_UP`) and the charger tiers (`MEAL_UP`) rise in route order.
- **Crossing hold and fill:** `holdCross`/`crossHeld` (`CROSS_HOLD`) stop a queued or automated crossing just short of finishing while `pendingActs`, `pendingGearJob` or `fillJob` has work. `fillJob` tops sap cells to the auto-charge stop level, then deadwood/grafts to full carry (`M.salCap`), both acts; skipped for deadwood while under 1 sap cell and energy under the charge threshold (`foodPct` of max energy). `FILL_RESUME 0.85`. The bots queue their crossings, so they do go through the hold and the fill.
- **Familiarity (Mastery tab):**
  - Stored in `S.fam[id]`. Speed is 1 + 9 x min(1, fam/famNeed) (`MASTER_MIN 0.1`).
  - Drills (`kind:'train'`, `TRAIN_CAP 4`) spread familiarity across a section: each session adds `DRILL_CREDIT` (0.1 since 2026-11-05, was 0.04) of a completion to every regular task there (`drillCredit`); legacy drills train their own set. With the usual x1.5 familiarity records that is about 0.17% per session, 1.3% for a life of both drills. The drill card shows the live per-session gain; familiarity on cards has one decimal (`pctTxt1`).
  - Chain flow `flowMul()` speeds up chained work.
- **Automation (Auto tab):**
  - A task is automatable after 10 lives' worth (`AUTO_LIVES`, `S.prac`); gear after being built in 10 lives (`S.gprac`, `gearNeed`). Jobs are never automated.
  - Links need x2 familiarity (`LINK_F`); one-click section runs need x5 (`SECTION_F`).
  - "Always run sections once ready" is `S.set.autoRun`; chains are pinned at the top of the queue.
- **Voyage clock:** every zone has `yr` (voyage year, 480-year voyage `VOYAGE`); `voyTxt(z)` gives "Year N · P% of the voyage", shown as a second line in section headers (Tasks and Auto tabs). Act I is all year 120; the long watch 120-240; Boarders 477-478; Arrival 479-480. FAQ "Selene's voyage" opens with Act II.
- **Queue forecast (build "queue forecast"):** the logic script plays the current seedling forward on a JSON copy of `S` with the real `step()` (no randomness), so it matches the real run exactly (tests check the death tick and cause). `fcStart()` snapshots `S` and the queue rows; `fcRun(ms)` runs a time slice (every 4 steps it checks the clock), swapping `S`, `M`, `HALT`, `chainCache` and every `HOOK` method out and back in a `try/finally` (chainCache's miss path calls `absorbChains()`, which changes `S`). Rows are matched by counting: when an id's copies in the copy's queue drop, its earliest open rows are resolved ('done' with energy and in-game day, or 'left' when dropped unfinished). The end is 'dead' (`dieRow`, `dieHere`: the row covering the last task worked, else the next open row), 'idle' (time would stop) or 'cap' (2 h in-game, `FC_MAX`). `forecast()` runs one in a go (tests). UI: `fcTick()` in `updateHud` restarts on `fcSigNow()` changes (queue, now, job, hold, run, settings, automation counts), otherwise every `fcWait` (3 s, or 20x the last forecast's cost), 6 ms a frame (12 ms on the first slice); `fcShow` is the last finished one and only marks rows while its queue matches. `updateQueueFc()` fills each row's `.qfc` span and toggles `.fnr` (red) / `.fdie` in place (never in the rebuild key). The header time left, `lastSvT` (red ETAs) and the Outlook line use it once ready; `survival()` is the fallback. Turnover forecasts cost ~0.3 s in total (node), spread over frames: no long frames at 4x CPU slowdown.
- **Queue tools (UI):** `qSnap(label)` before every queue edit (add, remove, move, drag, clear, load preset, paste) and `qUndoNow()` (one step, same seedling only; entries finished meanwhile are dropped by `qLive`). `qText()`/`qParse()`/`qTextPanel()`: the queue as numbered lines of names (gear "Build ...", chains "Chain: a → b"); pasting matches names case-insensitively (either apostrophe), skips chain lines (chains queue themselves) and reports unknown names. Preset names: `S.qpnames[i]` (24 chars), tap a preset's number. Setting `deathQueue` (pref): with the death screen off, a death with non-automated queue rows left still shows the death screen. Never-finished tasks (not in `S.ever`) get `.nev` ("• new").
- **Skip and preset triggers (logic, build "queue triggers"):** `L.qskip[id]` (every copy of that id; carried to the next seedling with the kept queue): `active()`'s queue loop, `plannedTicks`, `salvageNeed` and `legacyIdle` ignore skipped rows; the forecast keeps them out of "queue done" and the dying row (`FC.skip`). UI: the row name is a `.qtn` button (`data-qskip`), `.qskipbar` with `data-qskipall` 0/1; Undo restores skips. `qLive(id)` and `qLoadPreset(i)` moved into the logic script. `S.qtrig` (up to `QTRIG` 5 rules `{when:'new'}` or `{when:'sec', z}`, `p` preset index) fire through `qTriggers(ev, z)` from `decant()` (before a section run starts) and `enterZone()`, once per seedling (`L.qtf`), and call `HOOK.trig` (toast); the forecast plays them too. Panel `qTrigPanel()` (selects `data-tw`/`data-tp`; sections offered: the first one plus those reached, `trigSecs`). Setting `pauseDeath` (pref): `fcTick` pauses once per seedling (`L.pdOnce`) when the shown forecast death is 5 s in-game away.
- **Summaries (build "queue summaries"):** `newLife` snapshots `L.prac0` (automation progress) and `L.perk0` (records held) next to `L.fam0`; `lifeSummary(L)` adds records found, now automatable and the three closest automations to `showDeath()` (skipped for lives begun before this build). `nextAuto(z)` / `nextAutoHtml(z)`: the unautomated act/drill closest to automation in the section; "this seedling" when the shown forecast's end state (`fcShow.s.prac`) reaches `autoNeed`, else about `ceil(missing / per life)` more seedlings (an action's reps or `TRAIN_CAP` per life); shown in `#nxa` in the section header and refreshed in place (`updateTasks`, every 400 ms). `work()` adds time to `L.tt[id]` and `S.tt[id]` (in-game ticks; counted from this build); the Mastery tab shows both (`.sktm`).
- **Task cards:** they show `% to x10 / % to auto` (violet/green). These numbers (task and gear cards, the `.pp` span) are refreshed in place every frame by `updateTasks()` (`refs[].pp`, `gRefs`) and are **not** part of `renderTasks()`'s rebuild key: a full rebuild of the list repaints it and flickered on Android whenever familiarity ticked up (build "no flicker"). Keep anything that changes several times a second out of that key. Effects show "?" until the task has been finished once in this save (`S.ever`). Full effects are listed on the Mastery tab. `effectHtml(t, full)`.
- **Records (Archive):**
  - `PERKS`, permanent, found the first time certain actions are finished.
  - Stasis watch I-XV, one per section end, numbered in route order (record ids watch1-watch15 kept; watch15 is the Shattered Bark, shown as III).
  - Legacy themes (Echo, Dampening, Storage optimization, Overclock, Hardened grain): five-part sets in every Act I section (six sections, so six finals per theme; `ngpLv` divides by the number of finals), revealed by Act II progress (`LEGACY_REVEAL`; by route position: Storage optimization at The Drift, Dampening at Turnover, Echo at Contested Boughs, Hardened grain at The Mending, Overclock at the Tessaly System; revealed themes are kept in `S.a2run.lrev`, and saves keep what the old rule had revealed) and needed for crossings once revealed (`legacy`, `lset`, `lfin`, `LEGACY_LEN 0.6`, `NGP_MAX 3`). Hardened grain: `wearAt(level)` multiplies `wearRate`, x0.6 at full.
- **Archive:** only recovered records are listed (`hasPerk`); the counts (x of y, per section x/y) still show how many exist.
- **Log:**
  - `S.log` holds the story entries, taken from tasks' `log:` text.
  - First-time entries pop up (`S.storyQ`).
  - `refreshLog()` rewrites old saves' entries to the current text (`OLD_LOG` maps renamed titles).
  - The run history `S.hist`, the section unlock times, the run totals `S.firstAt` (rebuilt for old saves by `rebuildTotals`) and the best clone/section are also in the log.
- **Saves (UI script):**
  - Five slots `selene.slot.1-5`. Each has a linked death save `selene.slot.dN`, written at every death and playable without touching the slot; this is for testing, and the final version gets one global death save.
  - Save names: `S.name`, up to 30 characters.
  - Overwrite warnings: `askOverwrite()` panels.
  - Export/import JSON, copy as text, and share to the GitHub `saves/` folder.
  - On first launch, `long-patience.*` keys are moved to `selene.*` once (top of the logic script).
  - Preferences are device-wide: `selene.prefs.v1` (`PREF_KEYS`).
  - `mergeState()` migrates old saves.
- **FAQ:** unfolds with progress. `FAQ_GATE` maps each entry to an unlock (`start`, `queue`, `death`, `gear`, `sections`, `auto`, `won`, `a2`); `FAQ_TEST` checks them about every 2 s. Unlocks and opened entries are kept on the device (`selene.faq.v1`), never in a save, so a new game keeps them; loading a save unlocks what it reached. The tab gets a dot and entries a "new" tag until opened.
- **Reset** (bottom of Settings): "Reset settings and unlocks, keep saves" clears `SOFT_KEYS`; "Reset everything" clears every `selene.*` / `long-patience.*` key after two warnings and an "Export all saves first" option (`exportAll()`: one file with every slot and death save; importing it restores them all). `wiping` stops saves being written back before the reload. In the test version every speed stays open.
- **Palette:** "Amber resin" brown base (`--bg #1a140c`, `--panel #241b10`, `--panel2 #2e2316`, `--line #4a3920`, `--fg #f2e6c9`, `--dim #b39b6c`). The bright accents are unchanged. The Android `colors.xml` and WebView background match.
- **Fonts (embedded since build "embedded fonts"):** `<style id="fonts">` holds WOFF2 copies as data URIs: Selene Display (Saira Condensed 500/600/700), Selene Text (IBM Plex Sans 400/500/600), Selene Mono (IBM Plex Mono 400/500), used through `--f-disp`, `--f-body`, `--f-mono`. They are trimmed to ASCII, Latin-1 and the game's other characters and renamed, because "Saira" and "Plex" are OFL Reserved Font Names; licences and details in `project/fonts/`. **Rerun `python3 project/tools/fontpack.py` when new texts add characters** (it rewrites the block in place). No outside request at startup; the page looks the same offline.

## 4. Balance state (details in playtest-notes.md)
- Lean bot (build "stronger drills", current; it skips drills, so same as "crossing fill"): Act I 5.40 h, 65 seedlings; Act II 7.30 h (long watch 3.98, Boarders 2.29, Arrival 1.03). Completionist: 9 / 14 / 11 for the first three sections (was 10 / 15 / 12 with drill credit 0.04).
- Lean bot (build "Act II reordered"): Act I 5.70 h in-game, 79 seedlings (Shattered Bark 21 of them, untuned); Act II 8.69 h (long watch 4.89, Boarders 2.41, Arrival 1.39), 53 deaths. Build "the Shattered Bark" had Act II 7.72 h in the old order. Before the new section: Act I 4.50 h / 63, Act II 7.45 h.
- Section 1 (Seedling Vaults) is **FROZEN**: completionist clears at seedling 10; the owner cleared it with 9.
- Section 2 (Taproot Galleries) is **FROZEN** (2026-11-05): the owner cleared it completionist with 14 seedlings (bot 16).
- Next: the Shattered Bark (completionist bot 14 seedlings, untuned), from the owner's playtest save.

## 5. Tools and how to run them (project/tools)
Set up in a fresh workspace:
1. Clone the repo to `/home/claude/long-patience`.
2. Copy `project/tools/*` and `project/tools/fixtures/*` to `/tmp/claude-0/sim/`. The scripts use these paths; the bots accept `F=<path to index.html>`.
3. Fonts for true-to-phone screenshots and for `fontpack.py`: the game embeds its own fonts, so screenshots already render right. To rebuild the font block you need the source fonts and brotli:
   - `GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:none --sparse https://github.com/google/fonts /home/claude/google/fonts && git -C /home/claude/google/fonts sparse-checkout set ofl/sairacondensed ofl/ibmplexsans ofl/ibmplexmono` (fontpack.py does this itself if missing; the full repo is several GB, never clone it whole).
   - brotli (PyPI has none here): `git clone -q --depth 1 --branch v1.1.0 https://github.com/google/brotli <scratch>/brotli-src && pip install -q --break-system-packages --no-build-isolation <scratch>/brotli-src`.
   - Optional: copy the `.ttf` files to `~/.fonts` and run `fc-cache -f` so other pages can use them too.

The tools:
- `node sim11c.js`: lean Act I bot. It prints `TOTAL in-game h` and death causes.
- `node simcomp2.js`: completionist bot. Look for the first seedling with `sec 2` to get the section 1 count. `UPTO=<section id> MAXG=<n>` runs further (for example `UPTO=3` stops when a seedling reaches the Heartwood; the route is 1, 2, 15, 3, 4, 5).
- `node sim16c.js AB`: whole-game Act II bot. It prints long watch / Boarders / Arrival hours (route order) and death causes.
- `STOPZ=7 STOPT=600 OUT=snap.json node simsnap.js AB`: writes a save snapshot once a section is reached (for screenshots). `STOPZ` is a section id compared by route order (15 = the Shattered Bark).
- `python3 sanity.py`: the full sanity check. It checks:
  - duplicate or empty names;
  - a long in-page run on a fresh game, an old-key save and two Act II saves;
  - every tab and pop-up;
  - a scan for leftover old words.
  
  It also checks that every `data-*` button marker has code that reacts to it, and really taps the intro, story, death, menu and settings buttons. It must print `page errors: none`, `text problems: none`, `data markers without a handler: none` and all pop-up taps `ok`.
  Lesson (2026-11-04): a text-renaming pass once renamed the death button's marker (`data-decant`), which trapped every player at the first death; calling functions directly in tests did not catch it.
- `python3 fontpack.py`: rebuilds the embedded font block in index.html (see Fonts in §3 and step 3 above).
- `python3 shots.py`: screenshots of every screen to `/home/claude/shots`, at device scale 2.
- `pw161.py`: test speed switch (x5 open, no unlock written).
- `pw162.py`: FAQ unfolding, both resets, export-all and restore-all.
- `pw163.py`: plays a fresh seedling to its first death in real time, taps Sprout, and checks the page can't scroll behind a pop-up.
- `pw151/152/153/158/159/160.py`: Playwright checks (header and pause, stasis, death saves, save names, compact cards, storage migration). Each must print `errors []`.
- `oneoff/`: the scripts that did the Hearth Tree reskin, cleanup and comment rewording (history and reference only).

- `tests/` (**regression tests**, `node --test project/tools/tests/*.test.js`, about 70 s; `QUICK=1` skips the Act II run): forecast = real run (fresh game, 12 lives; four fixture saves; the forecast leaves `S` untouched), frozen sections (completionist first seedlings: Vaults 9, Taproot 14, Shattered Bark 11), Act totals (lean Act I 5.40 h; Act II 3.98 / 2.29 / 1.03 h). They run the bots from `project/tools` against the repo's index.html (or `F=`). **Update the expected numbers in the same commit as any deliberate balance change** (and when a section is retuned or frozen).

Run before every push: the syntax check below, sanity.py, the pw tests and the regression tests.

```
node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');[...h.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].forEach(m=>new Function(m[1]));console.log('syntax ok')"
```

## 6. Environment gotchas (cloud workspace)
- Network allowlist:
  - **Works:** GitHub (git, `gh api` REST) and PyPI. **Any public GitHub repo can be cloned** (anonymous reads through the proxy; use sparse, blob-less clones for big ones), and **GitHub release downloads** (`github.com/<owner>/<repo>/releases/download/...`) work, so prebuilt tools from release pages and libraries built from source are available. `gh api` only covers repos attached to the session (this one; attach others with push access through the session if ever needed).
  - **Blocked:** Google, Maven, Gradle (so the APK can't be built locally: Gradle and the Android SDK don't come from GitHub), npm DNS, Google Fonts, itch.io, the GitHub GraphQL API, raw.githubusercontent.com and codeload.github.com (source zips): use git clone instead.
  - **Pushing:** if `git push` is refused by the git proxy ("not in this session's authorized repository set"), attach hufle-beep/Long-patience to the session with push access, then push again.
  - **Through this workspace's GitHub access:** the Pages builds API, workflow dispatch, creating tags (git push of tags and the refs API) and cancelling queued runs are all blocked.
  - **Pages deploys can fail with "in progress deployment"** after an outage. The next push (or an empty commit, with the owner's OK) republishes.
- Use `gh api repos/hufle-beep/Long-patience/...` (REST), not `gh run list`/`gh release view` (GraphQL).
- Foreground `sleep N; cmd` is blocked: use bounded `until`/`for` loops.
- `git push` prints "This repository moved" (case-insensitive name): harmless.
- In Playwright, `text=Overwrite slot 2` can match the panel heading: click by `[data-ow="c0"]`.
- Inline `//` comments inside one-line object literals once broke the syntax: use `/* */`.
- `pkill` in the same shell command killed the command (exit 144): run it separately.

## 7. Communication
- The owner is in Europe/Budapest. They playtest on Android (app) and in the browser, and upload saves to `saves/`.
- Reports: short, with in-game and real time only. Options before changes (HARD RULE).
- Commit attribution lines (end of every commit message):
  - `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  - `Claude-Session: https://claude.ai/code/session_018oeHsg2asa6ZHp9dePfUUu` (use the current session's link in a new chat)
