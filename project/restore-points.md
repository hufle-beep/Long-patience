# Restore points

**Nothing is ever deleted from the git history**, so every past version can always be recovered. For quick rollbacks, the newest 5 restore points are also kept as named tags, and the newest 5 Android builds as separate downloads. Update this list in every push: add the new point on top and keep 5. Removing an old tag only removes the label; the commit stays in history.

## Game versions (git tags, kept automatically)
The **Restore points** workflow (`.github/workflows/restore-points.yml`) runs on every push to main. It keeps a tag on each of the **newest 5 commits**, named `restore/<date>-<commit>` (for example `restore/2026-11-04-4b28cfd`), and removes older restore tags. The current list is on GitHub under Tags (filter `restore/`).

What the recent commits are (newest first):
| Commit | What it is |
|---|---|
| (next) | Fix: Tasks tab flicker (familiarity updates in place) |
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
