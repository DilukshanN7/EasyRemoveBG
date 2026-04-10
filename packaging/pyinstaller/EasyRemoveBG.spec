# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules


PROJECT_ROOT = Path(SPECPATH).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

hiddenimports = []
hiddenimports += collect_submodules("easyremovebg")
hiddenimports += collect_submodules("rembg")
hiddenimports += collect_submodules("onnxruntime")

datas = []
datas += collect_data_files("rembg")
datas += collect_data_files("PIL")

binaries = []
binaries += collect_dynamic_libs("cv2")
binaries += collect_dynamic_libs("onnxruntime")


a = Analysis(
    [str(SRC_DIR / "easyremovebg" / "__main__.py")],
    pathex=[str(SRC_DIR)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="EasyRemoveBG",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="EasyRemoveBG",
)
