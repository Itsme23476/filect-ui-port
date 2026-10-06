# Filect — macOS UI layer (clean redesign) for the Windows port

This repo is the **authoritative macOS UI layer** of Filect (PySide6/Qt), copied
verbatim from the `voice-streaming` branch. It is the "clean redesign" — dark + light
theme, Inter/Sora fonts, line-icons, the voice overlays, onboarding, and the themed
voice page.

**Both apps are the same framework (PySide6/Qt), so this ports by copy/diff — not rebuild.**

## How to use it (Windows side)

1. **Diff, don't blind-overwrite.** Your Windows app already has some of this (e.g. a
   working `theme_manager.py` / `.qss` and Windows-specific hotkey/title-bar code).
   Compare each file in `ui/` against your `app/ui/` and port the **deltas**, keeping
   your Windows-specific bits.
2. **Close the known gaps** (these are what's usually missing on Windows):
   - **Fonts aren't loaded.** Add the byte-based font load from
     `_startup_font_and_theme_init.py` at startup, and ship `ui/fonts/*.ttf`. Without
     this the app falls back to Segoe UI and doesn't look like the redesign.
   - **Voice page theming.** The Voice settings page re-themes on light/dark here via
     `main_window.py` (`_apply_voice_theme_styles`) + the per-card `apply_theme()`
     methods in `ui/voice_cards/*.py`. Port that so nothing stays stuck in the old
     theme when you toggle.
3. **PyInstaller:** bundle `styles.qss`, `styles_light.qss`, and `fonts/*.ttf` in the
   spec's `datas`. `theme_manager.py` already resolves the bundled path via `sys._MEIPASS`.

## Important: the floating overlays are dark HUDs **by design**

The dictation pill (`ui/dictation_overlay.py`) and the organize overlay
(`ui/organize_overlay.py`) use hardcoded dark colors (e.g. the pill background
`QColor(10,10,18,235)`) and stay dark in **both** light and dark mode — that's
intentional (HUD style). **Do not make them follow the light theme.** Only the main
window chrome and the settings pages theme.

## What's in here

- `ui/theme_manager.py` — palette tokens (`_DARK_COLORS` / `_LIGHT_COLORS`),
  `apply_theme()`, the `theme_changed` signal, and the Windows 11 title-bar code.
- `ui/styles.qss` / `ui/styles_light.qss` — the dark / light stylesheets.
- `ui/fonts/*.ttf` — Inter + Sora (with OFL license files).
- `ui/icons.py` — QPainter line-icons (cross-platform).
- `ui/main_window.py`, `ui/onboarding.py` — the redesigned shell + onboarding.
- `ui/voice_cards/*.py` — the themed voice settings cards.
- `ui/dictation_overlay.py`, `ui/organize_overlay.py`, `ui/quick_search_overlay.py` —
  the floating voice UI (dark HUDs; only `_configure_macos`/`mac_spaces` are Mac-only).
- `_startup_font_and_theme_init.py` — the exact startup sequence (font load → apply_theme).

mac-only files included for reference (swap for your Windows equivalents):
`mac_hotkey.py`, `mac_spaces.py` (Windows already has `win_hotkey.py`).
