# Restore points

**Nothing is ever deleted from the git history**, so every past version can always be recovered. For quick rollbacks, the newest 5 restore points are also kept as named tags, and the newest 5 Android builds as separate downloads. Update this list in every push: add the new point on top and keep 5. Removing an old tag only removes the label; the commit stays in history.

## Game versions (git tags)
| Tag | Commit | What it is |
|---|---|---|
| `restore/2026-11-04-project-docs` | `05e5518` | Project docs and tools in the repo, backup builds in the workflow; game same as "cleanup" |
| `restore/2026-11-04-cleanup` | `4b28cfd` | Code cleanup: patch tasks, fault, boost/NG+ leftovers removed; comments and README |
| `restore/2026-11-04-hearth-tree` | `92183c1` | Hearth Tree reskin, lore, palette, new Act I order, Act II names |
| `restore/2026-11-04-rename-selene` | `e0187fb` | Renamed to Selene: Tidelocked; storage keys moved to `selene.*` |
| `restore/2026-11-04-compact-cards` | `9ed0f4b` | Compact task cards; gear on the Mastery and Auto tabs |

### How to roll back the game
- **See an old version:** on GitHub, open the tag and then `index.html`.
- **Put an old version back** (this needs the owner's go-ahead, like any change): `git checkout restore/<name> -- index.html`, then commit and push.
  - The web version and the app rebuild from that commit.
  - Saves stay compatible, as long as the restore point is from after the `selene.*` key move (2026-11-04 20:33). Older points use `long-patience.*` keys, and newer saves would not be seen by them.

## Android builds
- **Current:** release `android-latest`, file `LongPatience.apk` (the in-app updater uses this one).
- **Backups:** releases named `android-build-N`, marked pre-release. The newest 5 are kept automatically by the workflow. To roll back a phone, download the backup's `LongPatience.apk` and install it over the current app; saves are kept, because every build has the same signing key.
- Backups start with the first build after this file was added. Earlier APKs were replaced in place and can't be downloaded any more, but any earlier game version can be rebuilt from its commit.
