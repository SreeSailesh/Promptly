# -*- mode: python ; coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────────────
#  Promptly.spec  —  PyInstaller build specification
#
#  Produces:  dist/Promptly.exe
#  Run with:  pyinstaller Promptly.spec
# ─────────────────────────────────────────────────────────────────────

block_cipher = None

a = Analysis(
    ['Promptly.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'windows_toasts',
        'winrt',
        'winrt.windows.ui.notifications',
        'winrt.windows.data.xml.dom',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'scipy',
        'tkinter', 'PySide6', 'wx',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Promptly',               # → Promptly.exe
    icon='Promptly.ico',           # Bell+lightning icon in Explorer & taskbar
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,                 # no black console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
