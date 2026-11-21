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
