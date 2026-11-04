# Restore points

**Nothing is ever deleted from the git history**, so every past version can always be recovered. For quick rollbacks, the newest 5 restore points are also kept as named tags, and the newest 5 Android builds as separate downloads. Update this list in every push: add the new point on top and keep 5. Removing an old tag only removes the label; the commit stays in history.

## Game versions (git tags, kept automatically)
The **Restore points** workflow (`.github/workflows/restore-points.yml`) runs on every push to main. It keeps a tag on each of the **newest 5 commits**, named `restore/<date>-<commit>` (for example `restore/2026-11-04-4b28cfd`), and removes older restore tags. The current list is on GitHub under Tags (filter `restore/`).

What the recent commits are (newest first):
| Commit | What it is |
|---|---|
| (this commit) | Restore-point workflow; project docs updated; republishes the web version |
| `b12d331` | Restore points recorded in the docs |
| `05e5518` | Project docs and tools in the repo; Android backup builds (game same as "cleanup") |
| `4b28cfd` | Code cleanup: patch tasks, fault, boost/NG+ leftovers removed; comments and README |
| `92183c1` | Hearth Tree reskin, lore, palette, new Act I order, Act II names |
| `e0187fb` | Renamed to Selene: Tidelocked; storage keys moved to `selene.*` (older than the newest 5: no tag, still in history) |

Tags can't be created from Claude's workspace (GitHub refuses it there), which is why the workflow does it.

### How to roll back the game
- **See an old version:** on GitHub, open the tag and then `index.html`.
- **Put an old version back** (this needs the owner's go-ahead, like any change): `git checkout restore/<date>-<commit> -- index.html` (or any commit hash), then commit and push.
  - The web version and the app rebuild from that commit.
  - Saves stay compatible, as long as the restore point is from after the `selene.*` key move (2026-11-04 20:33). Older points use `long-patience.*` keys, and newer saves would not be seen by them.

## Android builds
- **Current:** release `android-latest`, file `LongPatience.apk` (the in-app updater uses this one).
- **Backups:** releases named `android-build-N`, marked pre-release. The newest 5 are kept automatically by the workflow. To roll back a phone, download the backup's `LongPatience.apk` and install it over the current app; saves are kept, because every build has the same signing key.
- Backups start with the first build after this file was added. Earlier APKs were replaced in place and can't be downloaded any more, but any earlier game version can be rebuilt from its commit.
