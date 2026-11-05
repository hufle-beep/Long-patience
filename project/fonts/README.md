# Fonts

The game embeds three fonts in `index.html` (`<style id="fonts">`), so it looks right offline and on first launch. All three are licensed under the SIL Open Font License 1.1 (licence texts in this folder) and come from https://github.com/google/fonts.

| In the game | Original | Weights | Copyright |
|---|---|---|---|
| Selene Display | Saira Condensed | 500, 600, 700 | 2016 The Saira Project Authors |
| Selene Text | IBM Plex Sans | 400, 500, 600 (fixed weights cut from the variable font) | 2017 IBM Corp. |
| Selene Mono | IBM Plex Mono | 400, 500 | 2017 IBM Corp. |

Changes from the originals: trimmed to printable ASCII, Latin-1 and the other characters the game uses, converted to WOFF2, and renamed, because "Saira" and "Plex" are Reserved Font Names under the OFL and a modified copy may not use them. The copyright and licence fields inside each font are kept.

Rebuild with `python3 project/tools/fontpack.py` (see its header for what it needs). Rerun it whenever new texts add characters outside the kept set; such characters would otherwise show in a system font.
