# Tools

Test bots, checks and screenshot scripts used to work on Selene: Tidelocked. They expect the repo at `/home/claude/long-patience` and themselves (plus `fixtures/`) in `/tmp/claude-0/sim/` (copy them there in a new workspace). Node bots accept `F=<path to index.html>`.

| Script | What it does | Pass |
|---|---|---|
| `sim11c.js` | Lean Act I bot | `TOTAL in-game h` about 5.51 |
| `simcomp2.js` | Completionist bot (all actions, drills 4/4, all gear). Stops when a seedling reaches section `UPTO` (a section id, default 2; route order 1, 2, 15, 3, 4, 5), or at seedling `MAXG` (default 60) | first `sec 2` seedling = 10 |
| `sim16c.js AB` | Whole game; Act II hours (long watch, Boarders, Arrival) and death causes | Act II about 7.08 h |
| `simsnap.js AB` | Save snapshot once section `STOPZ` (an id, compared by route) is reached (`STOPT`, `OUT`) | writes JSON |
| `sanity.py` | Data (incl. duplicate ids), long runs on six saves (incl. old Act II saves checked for kept legacy reveals) (incl. an old-build save past the Taproot: ward-lock and table migration), every tab and pop-up, leftover old words | `page errors: none`, `text problems: none` |
| `fontpack.py` | Rebuilds the embedded font block (`<style id="fonts">`) in index.html from google/fonts: trims, renames (OFL Reserved Font Names), WOFF2. Needs fonttools and brotli (see handover §5) | `fonts: 7 faces, ~104 KB woff2` |
| `shots.py` | Screenshots of every screen to `/home/claude/shots` | no errors |
| `pw151-179.py` | Playwright checks: header/pause, stasis, death saves, names, cards, storage move, test speeds, FAQ unfolding and resets, first death, archive, drill merge (pw165), save safety: backups, broken-number guard, paste tips, average row (pw166), event sounds (pw167), trigger table and FAQ (pw168), route, icons and Credits (pw169), publishing set (pw170), map folds (pw171), redraw cadence, unchanged writes, transform bars, autosave 15 s (pw172), audio sleep and shared reverb (pw173), save checks and recovery (pw174), queue history, pause when the queue is finished, pace, speed breakdown (pw175), section targets (pw176), clearer buttons (pw177), tooltips (pw178), folds by section and act, Ship log order (pw179) | `errors []` |
| `tests/` | Regression tests: `node --test project/tools/tests/*.test.js` (~70 s; `QUICK=1` skips the Act II run). Forecast = real run, frozen sections' seedling counts, Act totals. Update expected values with any deliberate balance change | `# fail 0` |
| `oneoff/` | Scripts that did the reskin, cleanup and comment rewording (reference) | - |
| `fixtures/` | `snap16.json` (The Mending), `snap4old.json` (built before the Shattered Bark, seedling in the Canopy Gardens), `snap7.json` (Contested Boughs), `snap12.json` (Turnover), `blank.html` | - |
