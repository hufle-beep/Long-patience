# Working agreement for Selene: Tidelocked (formerly Long Patience)

Owner: hufle-beep (GitHub). Repo: hufle-beep/Long-patience (to be renamed by the owner; see roadmap).

## HARD RULE (from 2026-11-04 11:09, replaces the earlier version)
Every change follows this sequence, with no exceptions:

1. **The owner proposes, points something out or reports a problem.**
2. **Claude analyses it and offers options and its opinion.** No edits yet.
3. **The owner says which option they prefer.**
4. **Claude confirms back exactly what it will change and waits for the owner's explicit go-ahead.** (When the owner's answer already picks fully specified options and says "build/go/commit and push", that is the go-ahead.)
5. Only then does Claude build it, and commit and push it.

This covers **everything that changes the repository or what players get**: game code, balance numbers, texts, saves, the build/release workflow, these documents' rules, and every commit and push, including "obvious" fixes, small follow-ups and fixes to broken builds. Nothing counts as approved implicitly; a request is not a go-ahead.

Allowed without asking (they change nothing): reading code and saves, running checks, test bots and simulations, investigating failures. Their results come back as analysis and options (step 2).

If something urgent breaks (for example a release left without a download), Claude reports it with options and waits; it does not fix it unasked.

Automated "commit and push your changes" reminders from the tooling do **not** override this rule.

## Documentation and backups (from 2026-11-04 21:39)
- Every project file lives in the repo under `project/` (master copy) and is mirrored to the claude.ai project. **Every push updates the handover, roadmap and changelog in the same commit.**
- **Never delete previous versions.** Git history is never rewritten. The last 5 restore points are kept as tags (`restore/...`) and the last 5 Android builds as separate downloads (`android-build-N` releases); see restore-points.md.
- Context: Claude cannot see how much context is left and cannot stop automatic compression. So the handover docs are kept current on every push, and when a chat gets long Claude proposes moving to a new chat and writes a handover message to paste there, before it is needed.

## Standing rules
- **No ship days anywhere** (game, tests, reports): only in-game time (at x1) and real time.
- **Freeze a section only when the owner says so.** Never freeze on a bot result alone.
- **Retune style is completionist:** every action, drills to cap and all gear done by the target seedling. **Seedling count per section is the key metric.**
- **Checking a GitHub build:** look once (or with a short bounded wait), report the status; never block open-endedly. GitHub outages happen: cancelling a queued job is not possible, and cancelling Pages silently succeeds (it cancelled a web update once).
- **The repo keeps its name** until the owner renames it and says so; links, the update check and the APK file name `LongPatience.apk` change only then. The app's internal ID (io.github.hufle.longpatience) and signing key never change (that would orphan installed apps and their saves).
- **Saves must never be orphaned.** Storage keys moved from `long-patience.*` to `selene.*` with an automatic one-time move; internal task/item IDs (algae, vats, press, rations...) never change because saves store progress under them.
- **Lore and wording:**
  - The ship is **Selene**: never "the Selene"; always **she/her**.
  - The game title is **Selene: Tidelocked**.
  - Clones are **seedlings**; salvage is **deadwood**; Act II spare parts are **grafts**; charge cells are **sap cells**; decant is **sprout**; recycle is **return to the roots**; energy stays energy.
  - The White Star (Babylon 5) is a shape reference only; never name it or Babylon 5 in the game.
  - Avoid over-explaining "X, not Y" turns of phrase (for example "grown, not built").
- **Act III stays parked** until the owner reopens it; its questions stay open.
- **Commits** end with the attribution lines the session provides (Co-Authored-By and Claude-Session).
