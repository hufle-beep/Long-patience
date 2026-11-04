# Tools

Test bots, checks and screenshot scripts used to work on Selene: Tidelocked. They expect the repo at `/home/claude/long-patience` and themselves (plus `fixtures/`) in `/tmp/claude-0/sim/` (copy them there in a new workspace). Node bots accept `F=<path to index.html>`.

| Script | What it does | Pass |
|---|---|---|
| `sim11c.js` | Lean Act I bot | `TOTAL in-game h` about 5.70 (build "the Shattered Bark") |
| `simcomp2.js` | Completionist bot (all actions, drills 4/4, all gear). Stops when a seedling reaches section `UPTO` (a section id, default 2; route order 1, 2, 15, 3, 4, 5), or at seedling `MAXG` (default 60) | first `sec 2` seedling = 10 |
| `sim16c.js AB` | Whole game; Act II hours (long watch, Boarders, Arrival) and death causes | Act II about 8.69 h |
| `simsnap.js AB` | Save snapshot once section `STOPZ` (an id, compared by route) is reached (`STOPT`, `OUT`) | writes JSON |
| `sanity.py` | Data (incl. duplicate ids), long runs on six saves (incl. old Act II saves checked for kept legacy reveals) (incl. an old-build save past the Taproot: ward-lock and table migration), every tab and pop-up, leftover old words | `page errors: none`, `text problems: none` |
| `shots.py` | Screenshots of every screen to `/home/claude/shots` | no errors |
| `pw151-162.py` | Playwright checks: header/pause, stasis, death saves, names, cards, storage move, test speeds, FAQ unfolding and resets | `errors []` |
| `oneoff/` | Scripts that did the reskin, cleanup and comment rewording (reference) | - |
| `fixtures/` | `snap16.json` (The Mending), `snap4old.json` (built before the Shattered Bark, seedling in the Canopy Gardens), `snap7.json` (Contested Boughs), `snap12.json` (Turnover), `blank.html` | - |
