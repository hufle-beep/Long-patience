# Selene: Tidelocked

A sci-fi clone-loop incremental game in the vein of Increlution and Incremortal.

You are K-7, a disposable maintenance clone aboard the colony ship *Selene*, named for the Greek goddess of the Moon. Her crew sleeps in stasis; WARDEN, the ship's overseer, decants clones to keep the ship alive. Repair the food system, the energy system and the stardrive so the crew can be woken. Each body lasts days, and what it learns echoes into the next one.

## Play

Open `index.html` in any browser, on a phone or a PC. Once GitHub Pages is enabled, it is playable at:

https://hufle-beep.github.io/Long-patience/

Progress saves in your browser's local storage.

## Android app

An Android version is built automatically every time the game changes. It is not on Google Play; share this link with friends:

**https://github.com/hufle-beep/long-patience/releases/download/android-latest/LongPatience.apk**

Installing: open the link on an Android phone (Android 8 or newer), download the file, and tap it. Android will ask to allow installs from your browser or file manager the first time; allow it.

Updating: install the new APK over the old one. Saves are kept, because every build is signed with the same key. The app also tells you, in its menu, when a newer build is available.

Saves live on the phone. Use **Archive → Save file** to export a save as a JSON file or import one, or **Save as text** to copy and paste it.

The app is built by `.github/workflows/android.yml` from the `android/` folder, with `index.html` copied in. It is signed with `android/longpatience.keystore`, which is in this repository for convenience. For a private key, add repository secrets `LP_KEYSTORE_B64` (the keystore as base64), `LP_STORE_PASS`, `LP_KEY_ALIAS` and `LP_KEY_PASS`; note that switching keys means everyone must uninstall once, which deletes their saves, so export them first.

## Saves

Saves are stored only on the device: in the browser's local storage, or inside the Android app. Back them up or move them with **Archive → Save file** (export/import a JSON file) or **Save as text** (copy and paste).

## How it works

- **Jobs** repeat and produce rations or salvage. **Actions** are one-off tasks that unlock new areas.
- Tap a task to do it now, or **+** to queue it. The last job you tapped runs whenever the queue is empty.
- You eat 1 ration a day. Hazardous tasks cost health. Old age, starvation or hazards end a life.
- Skill levels reset each life; the highest level ever reached becomes an **echo** that multiplies XP gain.
- **Archive records** are permanent unlocks found the first time you finish certain actions.

Single file, plain HTML/CSS/JavaScript, no build step.
