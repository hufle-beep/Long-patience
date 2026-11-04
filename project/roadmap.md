# Roadmap: Selene: Tidelocked

Last updated: 2026-11-04. Update in every push.

## Order of work (owner, 2026-11-04)
1. **Section-by-section playtesting and tuning** (now). Section 1 frozen; next the Taproot Galleries, then sections 3-14 one by one: the owner plays and uploads a save after each crossing, Claude proposes options for that section's knobs only, the owner freezes it.
2. **A full play of all available content**, start to end.
3. **Polishing: mechanics first.**
4. **Texts and story:** a friend of the owner will write texts and story to replace the AI-generated ones (then the owner's own story beats and flavour texts fit in here too).
5. **Then either Act III, or publishing** on Google Play, itch.io and galaxy.click (see "Later" below).

## Next up
- **Meteor shower redesign (approved 2026-11-04, see design.md):** Stage 1 new Act I section The Shattered Bark (after the Taproot Galleries) + fifth legacy theme Hardened grain; Stage 2 Act II reordered (long watch with Turnover first, Boarders + new The Mending with Rekindle the Hearthfire, then Arrival); Stage 3 480-year voyage clock and texts. Confirm each stage's exact changes before building.
- Section 2 (Taproot Galleries) retune: waiting for the owner's playtest save.

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
- 2026-11-04: Hearth Tree reskin and lore (Root-Kin, Selene she/her, seedlings, sap cells, deadwood, grafts); new Act I order; Act II names; gravity and wards before the flip; Amber resin palette; intro rewrite; code cleanup; five save slots with names, death saves and overwrite panels; run totals; compact task cards; stasis watch ladder; Section 1 frozen.
