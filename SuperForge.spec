# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None
root = Path.cwd()

a = Analysis(
    ['mfgforge_launcher.py'],
    pathex=[str(root)],
    binaries=[],
    datas=[('schema.sql', '.')],
    hiddenimports=[
        'click',
        'flask',
        'jinja2',
        'werkzeug',
        'app',
        'superforge_app',
        'mfgforge_intelligence',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='SuperForge',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
