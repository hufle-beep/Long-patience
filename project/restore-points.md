# Restore points

**Nothing is ever deleted from the git history**, so every past version can always be recovered. For quick rollbacks, the newest 5 restore points are also kept as named tags, and the newest 5 Android builds as separate downloads. Update this list in every push: add the new point on top and keep 5. Removing an old tag only removes the label; the commit stays in history.

## Fallback branches (kept until the owner says otherwise)
Named branches that point at a known-good build, kept on purpose (unlike the rolling tags below):
- `fallback/2026-11-05-embedded-fonts` → `9c61ac5`, the last build before the queue forecast and queue tools. To play it again: check out that branch's `index.html` (see "How to roll back" below) or install the matching Android backup build. Saves stay compatible both ways (new fields like preset names are simply ignored by the older build).

## Game versions (git tags, kept automatically)
The **Restore points** workflow (`.github/workflows/restore-points.yml`) runs on every push to main. It keeps a tag on each of the **newest 5 commits**, named `restore/<date>-<commit>` (for example `restore/2026-11-04-4b28cfd`), and removes older restore tags. The current list is on GitHub under Tags (filter `restore/`).

What the recent commits are (newest first):
| Commit | What it is |
|---|---|
| (next) | Quieter audio: one reverb, audio sleeps, Android pauseTimers |
| `c5adfeb` | Lighter redraws: 10 Hz screen, 2 Hz paused, transform bars, autosave 15 s, no 700 face |
| `5f65d9a` | Credits: full ZzFX MIT text, Plex year, Inspired by; research round 4 |
| `a39673d` | Effects shown (test switch): task effects visible from the start |
| `5436a94` | Folds kept: Auto and Mastery folds remembered on the device |
| `dbbdd2f` | Map folds: foldable Map sections, folded by themselves once fully mapped |
| `b7e6119` | Publishing set: pause all automation, welcome back, Log filters, screen-reader announcements |
| `f768d3b` | Route overview, game-icons.net icons, Credits |
| `c7ab1c0` | Trigger table (on/off, through, every n-th seedling, priority) and FAQ (search, tab entry, keyboard shortcuts) |
| `5a75b97` | Event sounds: crossing, sprout, gear built, low energy (ZzFX generator) |
| `2ebbab7` | Save safety: rolling backups, broken-number guard, paste tips, average row |
| `ed251e6` | One drill per section, twice as strong |
| `75bb243` | Queue row that loads a preset, favourite and hide filters |
| `6d9a8d5` | Forecast hints, Clear queue keeps the current row, task icons, This seedling / Kept effects |
| `7c09ae3` | Fix: automated gear gathers its own deadwood during the life again |
| `d98d7a7` | Queue chunk C: Now-line reasons, safe import, arrow keys, Least familiar sort, long-press + |
| `35df058` | Queue chunk B: life summary, next-automation line, time per task |
| `d6aa739` | Queue chunk A: preset triggers, skip toggles, pause before the forecast death |
| `8b924e8` | Queue forecast, Undo, queue as text, named presets, regression tests |
| `9c61ac5` | Fonts embedded in the game (offline, same look). **Fallback branch** `fallback/2026-11-05-embedded-fonts` |
| `660a99a` | Fix: Tasks tab flicker (familiarity updates in place) |
| `f5f7ed6` | Stronger drills, gain shown, familiarity with one decimal |
| `a3e3259` | Fix: crossings fill deadwood to full carry again |
| `9bacd4f` | Taproot Galleries frozen (docs only) |
| `edb1d3f` | Meteor shower Stage 3: voyage clock and timeline texts |
| `af19a30` | Meteor shower Stage 2: Act II reordered, The Mending |
| `d9a6eb3` | Meteor shower Stage 1: The Shattered Bark, ward-lock, Hardened grain (hidden); route-based section order |
| `01d6b4a` | Archive hides unrecovered records; Longest life in in-game time; last drive wording; meteor redesign written down |
| `2dd542f` | Fix: the death screen's Sprout button works again; page locked behind pop-ups |
| `443fcae` | FAQ unfolds with progress (kept on the device); Reset in Settings; export/restore all saves |
| `8c63e56` | Test speed switch: x1/x2/x5 open from the start (test version only) |
| `10c323a` | Restore points doc note |
| `10d77dc` | Restore-point workflow; project docs updated |
| `b12d331` | Restore points recorded in the docs |
| `05e5518` | Project docs and tools in the repo; Android backup builds (game same as "cleanup") |
| `4b28cfd` | Code cleanup: patch tasks, fault, boost/NG+ leftovers removed; comments and README |
| `92183c1` | Hearth Tree reskin, lore, palette, new Act I order, Act II names |
| `e0187fb` | Renamed to Selene: Tidelocked; storage keys moved to `selene.*` (older than the newest 5: no tag, still in history) |

Tags can't be created from Claude's workspace (GitHub refuses it there), which is why the workflow does it. GitHub also refuses the workflow a tag on a commit whose workflow files differ from today's, so commits from before 2026-11-04 21:40 (4b28cfd, 92183c1 and older) have no tag. They are still in history; within a few pushes the newest 5 are all tagged.

### How to roll back the game
- **See an old version:** on GitHub, open the tag and then `index.html`.
- **Put an old version back** (this needs the owner's go-ahead, like any change): `git checkout restore/<date>-<commit> -- index.html` (or any commit hash), then commit and push.
  - The web version and the app rebuild from that commit.
  - Saves stay compatible, as long as the restore point is from after the `selene.*` key move (2026-11-04 20:33). Older points use `long-patience.*` keys, and newer saves would not be seen by them.

## Android builds
- **Current:** release `android-latest`, file `LongPatience.apk` (the in-app updater uses this one).
- **Backups:** releases named `android-build-N`, marked pre-release. The newest 5 are kept automatically by the workflow. To roll back a phone, download the backup's `LongPatience.apk` and install it over the current app; saves are kept, because every build has the same signing key.
- Backups start with the first build after this file was added. Earlier APKs were replaced in place and can't be downloaded any more, but any earlier game version can be rebuilt from its commit.
