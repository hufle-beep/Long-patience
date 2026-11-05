# Roadmap: Selene: Tidelocked

Last updated: 2026-11-05 14:20 (build "act choices"). Update in every push.

## Order of work (owner, 2026-11-04)
1. **Section-by-section playtesting and tuning** (now). Sections 1 and 2 frozen; next the Shattered Bark, then sections 3-14 one by one: the owner plays and uploads a save after each crossing, Claude proposes options for that section's knobs only, the owner freezes it.
2. **A full play of all available content**, start to end.
3. **Polishing: mechanics first.**
4. **Texts and story:** a friend of the owner will write texts and story to replace the AI-generated ones (then the owner's own story beats and flavour texts fit in here too).
5. **Then either Act III, or publishing** on Google Play, itch.io and galaxy.click (see "Later" below).

**Owner decision (2026-11-05):** polishing can come before tuning when its gains are immediate.

## Next up
- **Act choices (owner 17:34, go 17:36; parked 17:44, resumed 17:55): BUILT** (choices at the end of Act I and Act II, Act I replay, prestige restart, coloured saves with a run counter). Run bot: run 1 Act I 5.60 h / Act II 11.17 h (103 seedlings), run 2 0.94 / 5.39 h (8), run 3 0.79 / 3.50 h (6). Next: run history in the Log, then the sealed record (16 beats on section ends, from the replays).
- **Fix (owner playtest 17:44, go 17:46): no idle charging BUILT.** A seedling with nothing to do no longer charges or scavenges on its own. **Parked (owner 17:44):** the act-choices work (stash), to be resumed when the owner says.
- **Runs (owner 17:04 "the sections should be infinitely repeatable", go 17:08 with Claude's picks): step 1 BUILT** (run loop: ending pop-up, Begin the voyage again, main-menu New run, carry-over rules, run bonus x0.75 with floor, legacy in Act I from run 2, targets on run 1). **Finding:** the run bot plays run 2 and 3 in one seedling and about 13 in-game minutes each; options to the owner before step 2 (run history in the Log) and step 3 (the sealed record).
- **Two-part legacy (owner 16:30, A + length 1, go 16:34): BUILT.** Each legacy set is a step and a final (plus its drill): 60 parts instead of 150, same work per set. Act I 5.59 h, Act II 11.17 h, completionist 9 / 11 / 9.
- **Hidden story layer (owner 16:40; picks 16:43: U1, P2 "The Lure"):** six sealed story beats, one per Act I section, opened in order by the first legacy final done in that section; Claude drafts the six texts and the exact changes for the owner's go.
- **Act II about twice Act I (owner 16:00, design rule; Shape II 16:13, go): BUILT** (Shattered Bark to Ember Crown x1.6, Act II x2.78; lean Act I 5.59 h, Act II 11.20 h; ratio test added). Next: the owner's replay saves (the Shattered Bark first).
- **Mechanics consolidation (owner 15:00: G1 A, G2 A, G3 A, G4 A; G5 legacy stays as it is; G6, G7 kept; G8 A; both finds fixed; go 15:07), five chunks, each pushed on its own; hard reset point `fallback/2026-11-05-before-mechanics`:** 1 code only BUILT (single sap-cell store code, unused drain argument and `survival()` gone, comments, Now-line overflow fixed, no "the" before Turnover and Tessaly Orbit). 2 G1 automation at Practiced (x2 familiarity) BUILT: completionist Vaults 10 -> 9, Taproot 13 (unchanged), Shattered Bark 10 -> 8; lean Act I 5.51 -> 4.75 h, Act II 7.08 -> 5.33 h. 3 G2 no sap-cell crossing cost BUILT (owner 15:52: Safe harbour now +25% station reserve, 1A): completionist Shattered Bark 8 -> 7; lean Act I 4.26 h, Act II 4.32 h. **All five chunks built.** Owner 15:52 (2A): the new seedling counts (Vaults 9, Taproot 11 on the completionist bot) are accepted for now and judged on the replay. 4 G3 one Act II station upgrade per section BUILT (charger upgrade carries the workshop's repair tier; workshops removed): Act I unchanged; Act II 5.33 -> 5.07 h. 5 G4 gear built when paid BUILT (no assembly; costs raised by the assembly time's deadwood, written into the gear table): completionist Vaults 9, **Taproot 13 -> 11 (frozen section moved: options to the owner)**, Shattered Bark 8, Heartwood 4; lean Act I 4.37 h, Act II 4.49 h. Bot seedling counts reported after each; a move in the frozen Taproot or the retuned Vaults goes to the owner as options.
- **Cleanup and streamlining (owner 13:54, picks 14:01: all of Claude's suggestions, M10 kept), six chunks, each pushed on its own:** 1 settings merges BUILT (M1 one Auto-charge, M2 Pause at crossings choice, M3 At a death choice, M4 Pause when… chips). 2 guidance and pop-ups BUILT (M5 drop the idle and automation hints, M6 drop the Journal, M7 Welcome back and What's new in one pop-up). 3 tooltips and header BUILT (M8 card tooltips without the card text, M9 route tap opens the tooltip, M11 compact Tasks header). 4 orphan sweep BUILT (old priority and Map-fold code, dead handlers, unused settings, constants and HOOK stubs, stale texts and comments; also the second-task leftovers, the old gear Buy button, the reward-point toast and unread data fields). 5 logic-script tightening BUILT (no-op functions and always-1 modifiers removed, stale comments reworded; the script had little true duplication, so the gain is small). 6 UI-script and CSS tightening BUILT (layered CSS rules merged, a toggle-row helper, `near()`, the no-op `chips()` gone; checked with the new stylesnap.py: no visible change). **All six chunks built.** **Next (owner 14:13):** analyse the game mechanics themselves for consolidation and simplification, options only.
- **Research round 5 (owner 12:55: build all of R1-R39): BUILT in seven chunks** (1 robustness, 2 test tooling, 3 phone comfort and the Made with AI note, 4 queue tools, 5 information, 6 guidance, 7 runs) plus chunk 8 (Inspired by adds only Terraformental, research.md). **R14 forecast cache: dropped** (owner 13:45, pick B: a tail-only re-simulation can't be exact, and the time-sliced forecast is cheap enough).
- **Seedling Vaults retuned (owner's pick B, 2026-11-05 11:32):** length factor 2.212 -> 2.81 after the owner's 6-seedling replay (bot 7 -> 10, aiming at the owner's 9). Freeze again when the owner says. Button review BUILT (owner 11:46: all of B1-B4 and P1-P5, build "clearer buttons"). Tooltips BUILT (owner 12:00: H1 one game-styled bubble, C2 cards, icons, header, key buttons, route; L1 the + keeps its long-press). Ship log order and folds BUILT (owner 12:13: O1+O2, F1, M2, X2; build "folds"). **Next:** the owner's next replay saves (the Shattered Bark next; the Seedling Vaults freeze again when the owner says).
- **Research round 4 picks (owner 2026-11-05 10:23: all; go 10:25), six chunks, each pushed on its own:** 1 credits and docs BUILT (full ZzFX MIT text, Plex Sans 2017-2019, "Inspired by" line, research.md round 4). 2 UI performance BUILT (10 Hz text, 2 Hz paused, task-list change counter, no unchanged writes, forecast slices, autosave 15 s, no bold title weight). 3 BUILT: sound (one 2 s reverb, audio sleeps) and Android pauseTimers. 4 BUILT: save safety (checksum, save version, recovery screen) and export (Android share sheet, file names with build and time). 5 BUILT: queue and info (load a past queue, speed breakdown, pause when the queue is finished, completions per real minute, merged death lines). 6 BUILT: section targets (target seedlings per section, badge only). **All six chunks built.** **Then (owner 10:31, corrected 10:48):** buttons that deserve emphasis get brown text on yellow like the menu's Continue button (only where it makes sense; weigh every button in the game), slightly larger like the main screen; go through every menu and offer further interface polish (options first).
- **Research rounds 2 and 3 picks (owner 2026-11-05 08:36: all green and yellow except challenges; go 08:41), five chunks, each pushed on its own:** 1 save safety BUILT (rolling backups, broken-number guard, paste tips, average row). 2 sound BUILT (ZzFX generator: crossing, sprout, gear built, low energy at 15% once per seedling). 3 BUILT: trigger table (on/off, from/through section, every N seedlings, priority) and FAQ (search, opens on the current tab, Keys entry from one hotkey table). 4 BUILT: route overview on the Map tab (unreached sections hidden), game-icons.net icons, Credits in Settings. 5 BUILT: welcome-back recap, Log filter chips, screen-reader announcements, pause all automation. **All five chunks built.**
- **Round 1c picks (owner go-ahead 2026-11-05 07:54: "go, P3 yes"), two chunks:** chunk 1 BUILT (forecast names a starving setting, Clear queue keeps the current row, icons on task cards, effects grouped This seedling / Kept, "· P3" removed). Chunk 2 BUILT: a queue row "Load preset: name" (fires once every row above it is done, replaces itself and the rows below with the preset), favourite and hide filters (Edit list, favourites first in their section, hidden tasks fold into "N hidden", still run; crossings can't be hidden; kept in the save). Then research rounds 2 and 3.
- **Queue chunks (owner go-ahead 2026-11-05 02:54: "Go A-C, commit and push between chunks"):** A built (preset triggers, skip toggles, pause before the forecast death). B built (life summary on the death screen; next-automation line in each section header; time per task, this seedling and all, on the Mastery tab). C built (Now-line reasons, safe import, arrow keys, Least familiar sort, long-press + for copies). All three chunks done. Dropped as not fitting: pending bar, record column, do once now.
- **Ideas from other games (research.md):** round 1 (Idle Loops, wrtsc) and round 1b (Immortality Idle, Progress Knight Quest: owner's priority) studied. Built from them: queue forecast, undo, queue as text, named presets, death-screen-if-unfinished setting, "new" marks, regression tests. Also built: preset triggers, per-goal ETA (the next-automation line), life summary at death, pause before the forecast death, long-press + for copies. Open: repeat counts on queue entries; round 1c picks. Rounds 2 and 3 studied 2026-11-05 (research.md); picks being built in five chunks.
- **Full replay from the start (owner, 2026-11-05)** on build "embedded fonts" (deadwood filled to full carry at crossings; drills 2.5x stronger), to see whether the frozen sections and the rest need a retune.
- **Meteor shower redesign (approved 2026-11-04, see design.md):** **All three stages built 2026-11-05** (The Shattered Bark, ward-lock, Hardened grain; Act II reordered with The Mending; 480-year voyage clock and timeline texts). Was: Stage 2 Act II reordered (long watch with Turnover first, Boarders + new The Mending with Rekindle the Hearthfire, then Arrival); Stage 3 480-year voyage clock and texts. Confirm each stage's exact changes before building.
- Section retune: the Taproot Galleries FROZEN 2026-11-05 (owner, 14 seedlings). Next: the Shattered Bark (untuned: lean bot 21 seedlings, completionist 14), waiting for the owner's playtest save. Act II retune order now follows the new route (The Long Current first); The Mending is new and untuned. Lean bot Act II went from 7.72 h to 8.69 h with the reorder (long watch 4.89 h).

## Decided
- **No iOS app** (owner, 2026-11-04): share the web link instead; iPhones play it in Safari. Don't propose a home-screen web app or a TestFlight build again unless the owner asks.

## Waiting on the owner
- **Repo rename:** the owner renames hufle-beep/Long-patience and tells us the new name. Then update `GH_REPO`, `APK_URL`, the update-check URL, the README links, and later the APK file name (only once installed apps carry a build that knows the new name).
- **Hosting:**
  - **itch.io:** Draft mode (private) is possible; the owner uploads `index.html` as an HTML zip. Saves are separate per site. Claude cannot reach itch.io.
  - **galaxy.click:** an incremental-game site with a cloud-save API (iframe postMessage). Hidden or draft listing is unknown; the owner checks when signed in. Cloud saves would be a code change (proposal first).
- **Backup Android build** (on hold by the owner): GitLab mirror + GitLab CI, or a local Android Studio build, for GitHub outages.

## Before release (final version)
- Turn **`TEST_ALL_SPEEDS`** off (index.html, next to `SPEEDS`): in the test version x1/x2/x5 are open from the start; the final version unlocks x2 after Act I and x5 after Act II again. The switch never writes unlocks into saves or devices, so nothing leaks into the final version.
- Turn **`TEST_SHOW_EFFECTS`** off (index.html, under `TEST_ALL_SPEEDS`): in the test version task cards and the Mastery tab show every effect and "opens:" from the start; the final version shows "?" until a task is first finished (owner, 2026-11-05). Archive records stay hidden until found either way.
- Replace the five per-slot death saves with **one global death save** (owner's decision; per-slot is for testing only).
- Re-check every section freeze and the Act I/Act II totals.

## Later, once the game is mature (owner, 2026-11-04)
- **Google Play, private first.** Owner: a Play Console developer account (one-time fee, ID check); the app setup forms (content rating, data safety, target audience, ads, privacy policy link, basic listing with a 512x512 icon). Publish on **Internal testing** (up to 100 testers by email, not visible in the store); Closed testing is reviewed. Going public later needs a closed test with 12+ testers opted in for 14 days in a row (new personal accounts).
  Claude: (1) build an .aab next to the APK; (2) target API 36 (required for new apps/updates since 2026-08-31) and fix edge-to-edge insets; (3) a Play build without the self-updater and REQUEST_INSTALL_PACKAGES (Play forbids self-updating); (4) optional automatic upload to the internal track from GitHub with a Play service-account secret; a privacy policy page on GitHub Pages.
  Catch: Play re-signs with its own key, so the Play app and the GitHub APK can't install over each other and keep separate saves (move them with "Export all saves").
- **Android developer verification:** from 2027 (worldwide; 4 countries from 2026-09-30) certified phones install only apps from verified developers, sideloaded APKs included. A Play Console account covers it; a free "limited distribution" account allows up to 20 devices. Needed before 2027 if the GitHub APK keeps being shared.

## Ideas noted (not approved)
- **Chain names (owner, 2026-11-04, later):** generate an own name for every possible combination of chained tasks (shown on chain cards instead of the list of step names). Propose naming scheme first.
- Cap long "opens:" lists on task buttons further, if the owner wants (currently 3 names + "+N more").

## Parked: Act III (do not build or decide until the owner reopens it)
See design.md: colony content held back from Act II, the Act II legacy themes from the old Honours, and four open questions.

## Done recently (see changelog.md for all)
- 2026-11-05: act choices: replay Act I, move on, restart the whole game; coloured saves with a run counter.
- 2026-11-05: fix: an idle seedling no longer burns its life at a charging station.
- 2026-11-05: runs: the voyage can begin again from the Seedling Vaults after the safe orbit.
- 2026-11-05: two-part legacy sets (a step and a final, plus the drill).
- 2026-11-05: Act II about twice as long as Act I again (longer sections from the Shattered Bark on).
- 2026-11-05: free crossings (no sap-cell cost); Safe harbour now +25% station reserve.
- 2026-11-05: gear built when paid (no assembly step; costs a little higher).
- 2026-11-05: one upgrade per Act II section (workshops merged into the charger upgrades).
- 2026-11-05: automation at Practiced (x2 familiarity); one progress number on cards.
- 2026-11-05: one food store (code), Now-line overflow fixed, "Turnover" and "Tessaly Orbit" without "the"; hard reset point branch before the mechanics changes.
- 2026-11-05: ui tightened: CSS rules defined two or three times merged, settings rows from one helper, no-op chips() removed (no visible change).
- 2026-11-05: logic tightened: no-op `frailty()`, constant modifiers and unused flags removed; stale comments reworded (no behaviour change).
- 2026-11-05: orphans swept: dead code, settings, handlers, CSS and data fields removed (no behaviour change).
- 2026-11-05: tooltips trimmed: card tooltips add only what the card lacks, route taps open the tooltip, section headers two lines shorter.
- 2026-11-05: pop-ups merged: What's new inside Welcome back, Journal and two hints dropped.
- 2026-11-05: settings merged: one Auto-charge switch (Charge when needed folded in), At a death and Pause at crossings choices, Pause when… chips.
- 2026-11-05: R14 forecast cache dropped (owner, pick B); round 5 closed.
- 2026-11-05: round 5 write-up in research.md; Inspired by adds Terraformental.
- 2026-11-05: runs: best section runs kept and loadable (pin one), splits against your other games on this device, All on / All off per section in the Auto tab.
- 2026-11-05: guidance: next-step line, first-hour hints in the Log, controls revealed with progress, What's new after updates, tuned-up-to note, journal view, new-entry marks.
- 2026-11-05: information: timeline strip per seedling, pinned checklist, named familiarity steps, time saved on cards, ETA tooltips, drain breakdown, Show formulas, what a route section still holds.
- 2026-11-05: queue tools: pause once on first reaching a section, one-shot rows (1x), insert point and Next, hold remove for every copy, keys 1-5 load presets, Return to the roots on the Now line.
- 2026-11-05: phone comfort: text size, brighter red text, scroll kept per tab, close X on pop-ups, tooltips hide with their element, queue follows the running row, screen-reader labels; Made with AI note in Credits and README.
- 2026-11-05: test tooling: data-integrity tests, milestone table per section, old-save test.
- 2026-11-05: robustness: save failures reported with the export, safe slot load, export reminder, error catcher, clock clamp, tap guard.
- 2026-11-05: folds: Ship log oldest first by section; Map, Auto, Mastery, Archive and Ship log fold by section and by finished act.
- 2026-11-05: tooltips: hover on the web, hold on touch; cards, icons, header, key buttons, route.
- 2026-11-05: clearer buttons: yellow only for the action of the moment, clearer plain buttons, amber +, compact presets, split warnings, pop-up focus, Auto explanation folds.
- 2026-11-05: Seedling Vaults 27% longer (owner's pick B; bot 7 -> 10, aiming at the owner's 9).
- 2026-11-05: section targets: target seedlings per section in the header and route info, a star and Log entry when cleared within it.
- 2026-11-05: queue history: load a past seedling's starting queue, merged death rows, pause when the queue is finished, tasks per real minute, speed breakdown.
- 2026-11-05: save checks: format number and checksum, recovery screen, Android share sheet export, file names with time and build.
- 2026-11-05: quieter audio: one 2 s reverb, audio sleeps when silent, Android timers paused in the background.
- 2026-11-05: lighter redraws: 10 Hz screen, 2 Hz paused, no unchanged writes, transform bars, cheaper task list and forecast, autosave 15 s, no bold display face (about half the main-thread work running, a sixth paused).
- 2026-11-05: credits fixed (full ZzFX MIT text, Plex Sans year, Inspired by line); research round 4 written up.
- 2026-11-05: test version shows every task's effects and what it opens from the start (switch `TEST_SHOW_EFFECTS`, off before release).
- 2026-11-05: Auto and Mastery folds remembered on the device.
- 2026-11-05: Map sections fold (by tap, and by themselves once fully mapped; kept on the device).
- 2026-11-05: pause all automation, welcome back, Log filters with record/automation events, screen-reader announcements.
- 2026-11-05: route overview on the Map tab, game-icons.net icons, Credits in Settings.
- 2026-11-05: trigger table (on/off, through, every n-th seedling, priority); FAQ search, tab entry, keyboard shortcuts.
- 2026-11-05: event sounds for crossing, sprout, gear built and low energy (ZzFX generator).
- 2026-11-05: save safety: rolling backups per slot (5 min, 30 min, 2 h of play, before replace), broken-number guard, paste tips, average row; research rounds 2 and 3 written up.
- 2026-11-05: one drill per section, twice as strong (14 drills removed; automation progress merged); completionist Seedling Vaults 9 -> 7.
- 2026-11-05: queue row that loads a preset (+ Row), favourite and hide filters on the Tasks tab (Edit list).
- 2026-11-05: forecast hints (the Outlook line names a setting that starves the seedling), Clear queue keeps the current row, task icons (record, gear, crossing), effects grouped This seedling / Kept, gear "· P3" label removed.
- 2026-11-05: fix: automated gear gathers its own deadwood during the life again (lost on 2026-11-04 06:07); crossing stop and fill unchanged.
- 2026-11-05: queue chunk C: Now-line reasons, safe import, arrow keys for tabs, Least familiar sort, long-press + for copies.
- 2026-11-05: queue chunk B: life summary at death, next-automation line per section, time spent per task.
- 2026-11-05: queue chunk A: preset triggers, skip toggles on queue rows, pause just before the forecast death.
- 2026-11-05: queue forecast (energy per queue row, red unreached rows, "Dies here", forecast death on the Outlook line), queue Undo, queue as text, named presets, death-screen-if-unfinished setting, "new" marks on never-finished tasks, regression tests; previous build kept on branch `fallback/2026-11-05-embedded-fonts`.
- 2026-11-05: fonts embedded in index.html (offline, same look; OFL copies renamed Selene Display/Text/Mono).
- 2026-11-05: Tasks tab flicker fixed (familiarity and auto % update in place; the list rebuilds only when its contents change).
- 2026-11-05: stronger drills (credit 0.04 -> 0.1), per-session gain on the drill card, familiarity with one decimal.
- 2026-11-05: crossing fill restored: queued/automated crossings fill deadwood (grafts) to full carry, with a low-energy safety net.
- 2026-11-05: Taproot Galleries frozen (owner, 14 seedlings completionist).
- 2026-11-05: meteor shower Stage 3: voyage clock (year and share of the voyage in section headers), timeline texts, FAQ "Selene's voyage".
- 2026-11-05: meteor shower Stage 2: Act II reordered (long watch, Boarders with The Mending, Arrival), progression by route, legacy reveals by route.
- 2026-11-05: meteor shower Stage 1: The Shattered Bark, the ward-lock, Hardened grain (hidden), six legacy finals per theme, route-based section order.
- 2026-11-04: Hearth Tree reskin and lore (Root-Kin, Selene she/her, seedlings, sap cells, deadwood, grafts); new Act I order; Act II names; gravity and wards before the flip; Amber resin palette; intro rewrite; code cleanup; five save slots with names, death saves and overwrite panels; run totals; compact task cards; stasis watch ladder; Section 1 frozen.
