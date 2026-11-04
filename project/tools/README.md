# Tools

Test bots, checks and screenshot scripts used to work on Selene: Tidelocked. They expect the repo at `/home/claude/long-patience` and themselves (plus `fixtures/`) in `/tmp/claude-0/sim/` (copy them there in a new workspace). Node bots accept `F=<path to index.html>`.

| Script | What it does | Pass |
|---|---|---|
| `sim11c.js` | Lean Act I bot | `TOTAL in-game h` about 4.50 |
| `simcomp2.js` | Completionist bot (all actions, drills 4/4, all gear) | first `sec 2` seedling = 10 |
| `sim16c.js AB` | Whole game; Act II hours and death causes | Act II about 7.45 h |
| `simsnap.js AB` | Save snapshot once `STOPZ` is reached (`STOPT`, `OUT`) | writes JSON |
| `sanity.py` | Data, long runs on four saves, every tab and pop-up, leftover old words | `page errors: none`, `text problems: none` |
| `shots.py` | Screenshots of every screen to `/home/claude/shots` | no errors |
| `pw151-160.py` | Playwright checks: header/pause, stasis, death saves, names, cards, storage move | `errors []` |
| `oneoff/` | Scripts that did the reskin, cleanup and comment rewording (reference) | - |
| `fixtures/` | `snap7.json` (Contested Boughs), `snap12.json` (Turnover), `blank.html` | - |
