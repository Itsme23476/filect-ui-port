# Startup sequence from the macOS app's main.py (ai_file_organizer/main.py, ~line 436).
# Put this in your Windows app's startup, AFTER QApplication is created and BEFORE
# the first window is shown. Order matters: load fonts FIRST, then apply the theme.
#
# This is the piece that is usually missing on the Windows side — without it the app
# falls back to Segoe UI and does not look like the redesign.

# --- Load bundled brand fonts (Inter + Sora) ---------------------------------
# Byte-based load (addApplicationFontFromData), NOT addApplicationFont(path):
# macOS/CoreText rejects some path-based calls; byte-loading is cross-platform-safe.
try:
    from PySide6.QtGui import QFontDatabase
    from PySide6.QtCore import QByteArray
    import os as _os
    import app.ui as _appui
    _fonts_dir = _os.path.join(_os.path.dirname(_appui.__file__), 'fonts')
    for _fn in ('Inter-Regular.ttf', 'Inter-Medium.ttf', 'Inter-SemiBold.ttf',
                'Sora-SemiBold.ttf', 'Sora-Bold.ttf'):
        try:
            with open(_os.path.join(_fonts_dir, _fn), 'rb') as _fh:
                QFontDatabase.addApplicationFontFromData(QByteArray(_fh.read()))
        except Exception:
            pass
except Exception as e:
    print(f"Font load failed: {e}")

# --- Apply saved theme (dark/light) ------------------------------------------
# theme_manager is a singleton. apply_theme() with no arg uses the saved setting
# (defaults to 'dark'). It loads styles.qss / styles_light.qss, sets the QPalette,
# the tooltip style, and the Windows 11 title-bar color, then emits theme_changed.
try:
    from app.ui.theme_manager import theme_manager
    theme_manager.apply_theme()
except Exception as e:
    print(f"Failed to apply theme: {e}")

# PyInstaller note: bundle styles.qss, styles_light.qss AND fonts/*.ttf in the
# spec's `datas` so they ship inside the frozen .exe. theme_manager already resolves
# the bundled path via sys._MEIPASS.
