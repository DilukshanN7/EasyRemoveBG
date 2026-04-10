# EasyRemoveBG

EasyRemoveBG is a small Windows-focused utility for removing image backgrounds from photos and logos. It now ships as an installable Python package with a CLI, descriptive helper scripts, and a per-user Windows context-menu installer.

## Features

- `remove-bg`: uses `rembg` for general photo background removal
- `remove-logo`: removes flat or near-flat logo backgrounds with an alpha mask
- predictable PNG output naming with collision handling
- per-user Windows Explorer context-menu installation without editing registry paths by hand
- helper scripts: `remove_background.py` and `remove_logo_background.py`

## Install

From the project directory:

```bash
py -m pip install .
```

To install the Windows Explorer context menu:

```bash
py install_context_menu.py
```

The bundled `install_windows.bat` runs both steps for you on Windows.

## Usage

```bash
easyremovebg remove-bg path\to\photo.jpg
easyremovebg remove-logo path\to\logo.png
easyremovebg remove-logo path\to\logo.png --tolerance 18
easyremovebg remove-bg path\to\photo.jpg --output path\to\custom-name.png
```

The helper scripts also work directly:

```bash
py remove_background.py path\to\photo.jpg
py remove_logo_background.py path\to\logo.png
```

## Output Behavior

- Output is always written as PNG.
- Default output names are `<original>_rembg.png` and `<original>_logo.png`.
- If a target file already exists, the CLI appends `_2`, `_3`, and so on unless `--overwrite` is used.

## Windows Context Menu

Preferred installation:

```bash
py install_context_menu.py
```

Removal:

```bash
py uninstall_context_menu.py
```

`windows_context_menu.reg` is kept as a simple fallback if you already installed the package and want a static registry file, but the Python installer is the primary supported path.

## Test

```bash
python3 -m unittest discover -s tests
```
