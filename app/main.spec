# app/main.spec
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hiddenimports = []
hiddenimports += collect_submodules("utils")
hiddenimports += collect_submodules("views")
hiddenimports += collect_submodules("controller")
hiddenimports += collect_submodules("popups")

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("assets", "assets"),
        ("version.txt", "."),
        ("changelog.json", "."),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="main",
    debug=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="main",
)
