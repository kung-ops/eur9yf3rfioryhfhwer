#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Small, reversible Husk build adjustments for Codemagic / real APKs.

Run after cloning Husk source. Only changes defaults for newly imported apps;
all existing per-app settings continue to win. No APKs or gameplay are mocked.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def replace_once(path, old, new, label):
    file = ROOT / path
    if not file.is_file():
        raise SystemExit(f"Missing Husk source file: {path}. Import source first.")
    text = file.read_text(encoding="utf-8")
    if new in text:
        print(f"[already] {label}")
        return
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Cannot safely apply {label}: expected one upstream match, found {count}. Review source changes.")
    file.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"[patched] {label}")

def strip_ps4_dependency():
    """PS4 uses two external trees unavailable to Codemagic and is unrelated to Android APKs."""
    file = ROOT / "src/app/project.yml"
    text = file.read_text(encoding="utf-8")
    snippet = (
        "      - framework: ../../build/ios-arm64/lib/libhuskps4.dylib\n"
        "        embed: true\n"
        "        codeSign: true\n"
        "        link: false\n"
    )
    if snippet not in text:
        print("[already] no PS4-only dylib dependency")
        return
    if text.count(snippet) != 1:
        raise SystemExit("Multiple PS4 dependencies: cannot safely modify")
    file.write_text(text.replace(snippet, "", 1), encoding="utf-8")
    print("[patched] omit unrelated PS4 dylib from Android APK build")

def main():
    replace_once(
        "src/app/Husk/TLAppSettings.swift",
        "    var resolution: Resolution = .high\n",
        """    // Modified 2026-11-21: Lower render scale by default to reduce GPU work
    // for actual APKs. Users can pick High/Native per game at any time.
    // Resolution is saved per game, so existing settings are preserved.
    static var performanceDefaultResolution: Resolution {
        ProcessInfo.processInfo.physicalMemory <= 3 * 1024 * 1024 * 1024 ? .low : .medium
    }
    var resolution: Resolution = TLAppSettings.performanceDefaultResolution
""",
        "adaptive resolution default",
    )
    replace_once(
        "src/app/Husk/TLAppSettings.swift",
        "resolution = try c.decodeIfPresent(Resolution.self, forKey: .resolution) ?? .high",
        "resolution = try c.decodeIfPresent(Resolution.self, forKey: .resolution) ?? TLAppSettings.performanceDefaultResolution",
        "adaptive missing-settings fallback",
    )
    replace_once(
        "src/app/Husk/TLAppSettings.swift",
        'case .high: return "2 pixels per point. The default."',
        'case .high: return "2 pixels per point. Sharper, but heavier."',
        "resolution help text",
    )
    strip_ps4_dependency()
    replace_once(
        "scripts/package_ipa.sh",
        "for lib in libqemu-aarch64-softmmu.dylib libANGLE-shared.dylib libhuskps4.dylib; do",
        "for lib in libqemu-aarch64-softmmu.dylib libANGLE-shared.dylib; do",
        "skip PS4 validation for Android-only IPA",
    )
    print("Husk Android APK build changes ready (no compatibility guarantees).")

if __name__ == "__main__":
    main()
