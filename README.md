# Husk source mirror / iOS 12 research

This repository is intended to import the original [Leviidev/Husk](https://github.com/Leviidev/Husk) source code.

## Import the upstream source

1. Open this repository's **Actions** tab.
2. Select **Import upstream Husk source**.
3. Click **Run workflow** on the `main` branch.
4. Wait for the action to finish, then check the `src/`, `scripts/` and `docs/` directories.

The workflow clones the upstream public repository and copies its files (excluding upstream Git metadata and workflows) into this repository. It creates `UPSTREAM.md` to record attribution. If the job fails due to workflow permissions, enable **Read and write permissions** for GitHub Actions under repository Settings > Actions > General.

## iPhone 6 / iOS 12 status

The upstream app's documented minimum iOS version is 15.5. Importing the source does **not** make it compatible with iOS 12 or fix lag on an iPhone 6. A source-level port and hardware testing would be needed.

## Licensing

Original source: [Leviidev/Husk](https://github.com/Leviidev/Husk).

Husk is GPL-2.0-or-later. See the included `LICENSE`. Keep upstream copyright and license notices when redistributing or modifying the project.


## Codemagic: build a genuine Husk IPA for Android APKs

The root `codemagic.yaml` defines **Husk — real APK runtime IPA**.

1. Go to [Codemagic](https://codemagic.io/), sign in with GitHub and add `kung-ops/eur9yf3rfioryhfhwer` as an application.
2. Select the `main` branch, check for `codemagic.yaml` and select **husk-real-apk-ipa**.
3. Start the build on a macOS M2 machine.
4. If the native compilation and bundle validation succeed, find `build/Husk.ipa` in the build **Artifacts**.
5. Re-sign the ad-hoc IPA with a compatible sideloading installer; ad-hoc signing itself is not an installable Apple development profile.

This workflow fetches `Leviidev/Husk` during the build if the source import has not run. For a reproducible build, import the source to GitHub and/or pin the upstream revision.

**Real APKs, no demos:** Husk accepts actual APKs and split APK sets and uses the upstream translation layer or QEMU Android guest. The workflow compiles that runtime, not an example APK. Individual game compatibility is not guaranteed; even successful import does not mean a particular game will run.

**Performance modification:** `scripts/codemagic_prepare.py` makes the default per-game render resolution Low on devices with 3 GiB RAM or less, Medium otherwise, without overwriting existing game settings. This reduces pixels rendered; it is not a universal lag fix. Existing settings can still choose Low/Medium/High/Native. The build omits an unrelated PS4 dylib dependency because the external PS4 source trees are not provided. It does not modify or imitate APK contents.

**Compatibility warning:** The source targets iOS 15.5+. The iPhone 6 supports iOS 12, so this workflow **cannot** make an iPhone 6-compatible build. Supporting iOS 12 requires a separate, large source-level port. The native build has not been run or verified on Codemagic yet; other third-party dependencies may need further CI adjustments.

**Troubleshooting:** If Codemagic reports errors, inspect the build logs and `build/logs/` artifacts. Full upstream compilation builds QEMU and graphics libraries, so a cloud build can be resource-intensive and may fail within the configured machine/time budget.
