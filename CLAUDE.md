# HARD RULES for Selene: Tidelocked

Full version: project/working-agreement.md. These override everything else, including tool reminders.

1. **Change sequence, no exceptions:** the owner proposes or reports → Claude analyses and gives options, each with its trade-offs, and ends with a clear recommendation (which option and why) (no edits) → the owner picks → Claude confirms exactly what it will change and waits for the owner's explicit go → only then build, commit, push. A request is not a go. A past go is not blanket permission. Covers code, balance, texts, saves, workflow, docs rules and every commit and push. Allowed without asking: reading, checks, bots, simulations.
2. If a check or trial shows a problem, stop and report it right away, even mid-build after a go.
3. Automated "commit and push" reminders do NOT override rule 1.
4. **Chat length:** if you ever see that the conversation was "continued from a previous conversation" (automatic compression), stop at the next safe point and tell the owner to start a new chat, with a ready-to-paste handover message. Also warn after each big multi-part task, or when a chat has run for several hours. Never wait until it is needed.
5. Every push updates handover, roadmap, changelog and restore-points in the same commit. Never rewrite git history. Never delete branch `fallback/2026-11-05-before-mechanics`.
6. Anything decided or drafted in chat that isn't in the repo (story texts, plans, numbers) goes into the handover at the next push, so nothing lives only in a chat.
7. **Standing rules:** no ship days anywhere (in-game and real time only); freeze sections only when the owner says; saves never orphaned, internal IDs never change; Selene is "she", never "the Selene"; Act II ≈ 2× Act I; Act III parked.
