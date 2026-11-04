# Handover: Selene: Tidelocked

Last updated: 2026-11-04 23:40 (build "hidden records"). Next big job: the meteor shower redesign (design.md, roadmap.md). Update this file in every push.

## 1. What the game is
An incremental "clone-loop" game in one HTML file (like Increlution/Incremortal). You are K-7, a **seedling** (disposable drone of WARDEN and the Hearth Tree) aboard **Selene**, a living-wood colony ship of the Root-Kin of Earth. Each seedling works tasks until its energy runs out; familiarity, records and automation carry over to the next one.

- **Act I** (sections 1-5, all inside the Hearth Tree): Seedling Vaults -> Taproot Galleries (power) -> The Heartwood (navigation, WARDEN's mind) -> Canopy Gardens (food) -> Ember Crown (propulsion). Ends with "Kindle the Hearth Tree".
- **Act II** (sections 6-14, linear): Boarders (Bark Breach, Contested Boughs, The Hive Ship), The long watch (The Long Current, The Drift, The Long Dark), Arrival (Turnover, The Tessaly System, Tessaly Orbit).
- **Act III**: parked (see design.md).

Play: https://hufle-beep.github.io/Long-patience/ · Android APK: release `android-latest`, file `LongPatience.apk`.

## 2. Repository
- `index.html`: the whole game (~4,100 lines, ~340 KB). Three scripts:
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
  - Max energy: 100 base, +100 from Act I records/gear, +100 Boarders, +100 Long Watch, +100 legacy Storage optimization (cap 500).
- **Sap cells and stations:**
  - Cells are stored in `L.food.ration` (store id `ration`, display name "Sap cells"); storage is `STORE_CAP` per section.
  - Charging stations are `kind:'job'` tasks with `prod.rations`. Each holds `stationMax(z)` (RESERVE_K 0.15, Act II x0.5).
  - Recharges have a cooldown `MEAL_CD`; charger upgrades (`MEAL_UP`) shorten it.
  - Crossings cost `crossCost(z)` of the cells carried.
  - Auto-forage is standard. "Charge when needed" is `S.set.autoFeed`, and the threshold is `foodPct`.
- **Deadwood and grafts:**
  - Stored in `L.salvage`. `salW(z)` gives the display word: "deadwood" in Act I, "grafts" in Act II.
  - Gear (`ITEMS`) is built from it, with assembly tasks `b:<id>` (`BT`).
  - Act II wear (`WEAR_RATE`) adds drain. Repairs cost grafts. There are workshops ws6-ws14.
- **Familiarity (Mastery tab):**
  - Stored in `S.fam[id]`. Speed is 1 + 9 x min(1, fam/famNeed) (`MASTER_MIN 0.1`).
  - Drills (`kind:'train'`, `TRAIN_CAP 4`) spread familiarity across a section.
  - Chain flow `flowMul()` speeds up chained work.
- **Automation (Auto tab):**
  - A task is automatable after 10 lives' worth (`AUTO_LIVES`, `S.prac`); gear after being built in 10 lives (`S.gprac`, `gearNeed`). Jobs are never automated.
  - Links need x2 familiarity (`LINK_F`); one-click section runs need x5 (`SECTION_F`).
  - "Always run sections once ready" is `S.set.autoRun`; chains are pinned at the top of the queue.
- **Task cards:** they show `% to x10 / % to auto` (violet/green). Effects show "?" until the task has been finished once in this save (`S.ever`). Full effects are listed on the Mastery tab. `effectHtml(t, full)`.
- **Records (Archive):**
  - `PERKS`, permanent, found the first time certain actions are finished.
  - Stasis watch I-XIV, one per section end.
  - Legacy themes (Echo, Dampening, Storage optimization, Overclock): five-part sets in every Act I section, revealed by Act II progress and needed for crossings once revealed (`legacy`, `lset`, `lfin`, `LEGACY_LEN 0.6`, `NGP_MAX 3`).
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
- **Fonts:** Saira Condensed, IBM Plex Sans and IBM Plex Mono from Google Fonts. The cloud workspace cannot load them, so its screenshots use fallback fonts.

## 4. Balance state (details in playtest-notes.md)
- Lean bot: Act I 4.50 h in-game, 63 seedlings; Act II 7.45 h (Boarders 3.38, Long Watch 2.22, Arrival 1.85), 55 deaths.
- Section 1 (Seedling Vaults) is **FROZEN**: completionist clears at seedling 10; the owner cleared it with 9.
- Next: section 2 (Taproot Galleries) retune, from the owner's playtest save.

## 5. Tools and how to run them (project/tools)
Set up in a fresh workspace:
1. Clone the repo to `/home/claude/long-patience`.
2. Copy `project/tools/*` and `project/tools/fixtures/*` to `/tmp/claude-0/sim/`. The scripts use these paths; the bots accept `F=<path to index.html>`.

The tools:
- `node sim11c.js`: lean Act I bot. It prints `TOTAL in-game h` and death causes.
- `node simcomp2.js`: completionist bot. Look for the first seedling with `sec 2` to get the section 1 count.
- `node sim16c.js AB`: whole-game Act II bot. It prints Boarders / Long Watch / Arrival hours and death causes.
- `STOPZ=7 STOPT=600 OUT=snap.json node simsnap.js AB`: writes a save snapshot once a section is reached (for screenshots).
- `python3 sanity.py`: the full sanity check. It checks:
  - duplicate or empty names;
  - a long in-page run on a fresh game, an old-key save and two Act II saves;
  - every tab and pop-up;
  - a scan for leftover old words.
  
  It also checks that every `data-*` button marker has code that reacts to it, and really taps the intro, story, death, menu and settings buttons. It must print `page errors: none`, `text problems: none`, `data markers without a handler: none` and all pop-up taps `ok`.
  Lesson (2026-11-04): a text-renaming pass once renamed the death button's marker (`data-decant`), which trapped every player at the first death; calling functions directly in tests did not catch it.
- `python3 shots.py`: screenshots of every screen to `/home/claude/shots`, at device scale 2.
- `pw161.py`: test speed switch (x5 open, no unlock written).
- `pw162.py`: FAQ unfolding, both resets, export-all and restore-all.
- `pw163.py`: plays a fresh seedling to its first death in real time, taps Sprout, and checks the page can't scroll behind a pop-up.
- `pw151/152/153/158/159/160.py`: Playwright checks (header and pause, stasis, death saves, save names, compact cards, storage migration). Each must print `errors []`.
- `oneoff/`: the scripts that did the Hearth Tree reskin, cleanup and comment rewording (history and reference only).

Run before every push: the syntax check below, sanity.py, the pw tests and the three bots.

```
node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');[...h.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].forEach(m=>new Function(m[1]));console.log('syntax ok')"
```

## 6. Environment gotchas (cloud workspace)
- Network allowlist:
  - **Works:** GitHub (git, `gh api` REST) and PyPI.
  - **Blocked:** Google, Maven, Gradle (so the APK can't be built locally), npm DNS, Google Fonts, itch.io and the GitHub GraphQL API.
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
  - `Claude-Session: https://claude.ai/code/session_018oeHscQg4SH2rn9DPkdUGg` (use the current session's link in a new chat)
