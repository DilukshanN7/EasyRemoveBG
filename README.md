# EasyRemoveBG

EasyRemoveBG is a Windows-focused background-removal tool for photos and logos. The image processing stays in Python, but distribution is now designed around a packaged executable and a real Windows installer instead of loose helper scripts.

## Features

- `remove-bg`: uses `rembg` for general photo background removal
- `remove-logo`: removes flat or near-flat logo backgrounds with an alpha mask
- deterministic PNG output naming with collision handling
- Windows installer-managed Explorer context menu for image files
- packaged executable distribution via PyInstaller and Inno Setup

## End-User Install

Use the generated `EasyRemoveBG-Setup.exe` installer from the `installer/Output` directory after a release build. The installer:

- installs the packaged app under the current user's profile
- registers `Remove Background` and `Remove Logo Background` in the Explorer context menu for image files
- adds uninstall support

## Developer Usage

Install the project in a Python environment:

```bash
py -m pip install .
```

Run from Python during development:

```bash
py -m easyremovebg remove-bg path\to\photo.jpg
py -m easyremovebg remove-logo path\to\logo.png
py -m easyremovebg remove-logo path\to\logo.png --tolerance 18
py -m easyremovebg remove-bg path\to\photo.jpg --output path\to\custom-name.png
```

## Windows Build

Prerequisites:

- Windows
- Python 3.10+
- Inno Setup 6

Install build dependencies:

```bash
py -m pip install .[build]
```

Build the packaged executable:

```bash
py -m PyInstaller packaging\pyinstaller\EasyRemoveBG.spec --clean
```

Build the installer:

```bash
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer\EasyRemoveBG.iss"
```

The packaged app is produced in `dist\EasyRemoveBG`, and the installer is produced in `installer\Output`.

## Output Behavior

- Output is always written as PNG.
- Default output names are `<original>_rembg.png` and `<original>_logo.png`.
- If a target file already exists, the CLI appends `_2`, `_3`, and so on unless `--overwrite` is used.

## Test

```bash
python3 -m unittest discover -s tests
```
