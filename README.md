# Selene: Tidelocked

A sci-fi incremental game about short lives and long voyages, in the vein of Increlution and Incremortal.

You are K-7, a seedling: one of the disposable drones that WARDEN and the Hearth Tree grow for a single task. You serve aboard *Selene*, a colony ship grown from living wood by the Root-Kin of Earth and named for the Greek goddess of the Moon. Her 3,112 crew sleep in stasis. Restore her sap flow, WARDEN's mind and her star-charts, her gardens and, last, the Hearthfire, so the crew can be woken. A seedling lasts as long as it is needed; what it learned seeps back through the roots into the next one.

## Play

Open `index.html` in any browser, on a phone or a PC. It is playable at:

https://hufle-beep.github.io/Long-patience/

Progress saves in your browser's local storage.

## Android app

An Android version is built automatically every time the game changes. It is not on Google Play; share this link with friends:

**https://github.com/hufle-beep/long-patience/releases/download/android-latest/LongPatience.apk**

Installing: open the link on an Android phone (Android 8 or newer), download the file, and tap it. Android will ask to allow installs from your browser or file manager the first time; allow it.

Updating: install the new APK over the old one. Saves are kept, because every build is signed with the same key. The app also tells you, in its settings, when a newer build is available.

The app is built by `.github/workflows/android.yml` from the `android/` folder, with `index.html` copied in. It is signed with `android/longpatience.keystore`, which is in this repository for convenience. For a private key, add repository secrets `LP_KEYSTORE_B64` (the keystore as base64), `LP_STORE_PASS`, `LP_KEY_ALIAS` and `LP_KEY_PASS`; note that switching keys means everyone must uninstall once, which deletes their saves, so export them first.

## Saves

Saves are stored only on the device: in the browser's local storage, or inside the Android app. Open **☰ → Save Management** for the five save slots (each can be named), each slot's death save, and **Save files and transfer**: export or import a JSON file, copy the save as text, or share it to this repository's `saves` folder.

## How it works

- **Actions** are one-off tasks that open up the ship; **drills** train every task in their section; **jobs** run continuously: charging stations refill your sap cells, and deadwood jobs (grafts in Act II) supply gear and repairs.
- Tap a task to do it now, or **+** to queue it.
- Energy drains all the time and hazards drain it faster; recharging from sap cells puts it back. When energy runs out, the seedling withers and the next one sprouts.
- **Familiarity** carries over between lives: every task gets faster the more of it your seedlings have done, up to ×10, and well-practised tasks can be **automated**.
- **Archive records** are permanent unlocks found the first time you finish certain actions; **Stasis watch** records make energy drain slower.
- Act I ends when the Hearth Tree is kindled; Act II follows Selene through boarders, the long watch and the arrival at Tessaly. The **FAQ** tab in the game explains everything in detail.

Single file, plain HTML/CSS/JavaScript, no build step.
