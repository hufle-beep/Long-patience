# Long Patience

A sci-fi clone-loop incremental game in the vein of Increlution and Incremortal.

You are K-7, clone stock aboard the derelict colony ship *Long Patience*. Each body lives a few years.
When it dies, its skills fade into an echo that speeds up learning for every later clone.
Work your way aft through five areas of the ship and light the main drive.

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

## Saving to GitHub

The Archive tab has a **GitHub save** panel that uploads your save to `saves/save.json` in this repository and loads it back on another device.

1. Create a [fine-grained personal access token](https://github.com/settings/personal-access-tokens/new) with access to **only this repository** and the permission **Contents: Read and write**.
2. In the game, open **Archive → GitHub save**, paste the token, and tap **Upload save**.
3. On another device, paste the same token and tap **Load from GitHub** (tap twice to confirm; it replaces local progress).

Turn on **Auto-upload** to upload every 10 minutes while the game is open. The token is stored only in that browser and is never written into the save file.

There is also a **Save code** panel for copying a save as text and pasting it elsewhere.

## How it works

- **Jobs** repeat and produce rations or salvage. **Actions** are one-off tasks that unlock new areas.
- Tap a task to do it now, or **+** to queue it. The last job you tapped runs whenever the queue is empty.
- You eat 1 ration a day. Hazardous tasks cost health. Old age, starvation or hazards end a life.
- Skill levels reset each life; the highest level ever reached becomes an **echo** that multiplies XP gain.
- **Archive records** are permanent unlocks found the first time you finish certain actions.

Single file, plain HTML/CSS/JavaScript, no build step.
