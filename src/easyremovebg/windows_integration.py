from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from .errors import UnsupportedPlatformError


ROOT_KEY = r"Software\Classes\*\shell"


@dataclass(frozen=True)
class ContextMenuEntry:
    key_name: str
    label: str
    command: str
    icon: str


def build_context_menu_entries(python_executable: str | Path | None = None) -> list[ContextMenuEntry]:
    python_path = Path(python_executable) if python_executable else Path(sys.executable)
    python_text = str(python_path)

    return [
        ContextMenuEntry(
            key_name="EasyRemoveBG.RemoveBackground",
            label="Remove Background",
            command=f'"{python_text}" -m easyremovebg.cli remove-bg "%1"',
            icon=python_text,
        ),
        ContextMenuEntry(
            key_name="EasyRemoveBG.RemoveLogoBackground",
            label="Remove Logo Background",
            command=f'"{python_text}" -m easyremovebg.cli remove-logo "%1"',
            icon=python_text,
        ),
    ]


def install_context_menu(
    python_executable: str | Path | None = None,
    *,
    dry_run: bool = False,
) -> list[ContextMenuEntry]:
    entries = build_context_menu_entries(python_executable)
    if dry_run:
        return entries

    _ensure_windows()

    import winreg

    for entry in entries:
        menu_path = fr"{ROOT_KEY}\{entry.key_name}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, menu_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, entry.label)
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, entry.icon)
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, fr"{menu_path}\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, entry.command)

    return entries


def uninstall_context_menu() -> int:
    _ensure_windows()

    import winreg

    removed = 0
    for entry in build_context_menu_entries():
        if _delete_tree(winreg, winreg.HKEY_CURRENT_USER, fr"{ROOT_KEY}\{entry.key_name}"):
            removed += 1
    return removed


def _ensure_windows() -> None:
    if sys.platform != "win32":
        raise UnsupportedPlatformError("Windows context menu installation is only supported on Windows.")


def _delete_tree(winreg, root, subkey: str) -> bool:
    try:
        with winreg.OpenKey(root, subkey, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            while True:
                try:
                    child = winreg.EnumKey(key, 0)
                except OSError:
                    break
                _delete_tree(winreg, root, fr"{subkey}\{child}")
    except FileNotFoundError:
        return False

    winreg.DeleteKey(root, subkey)
    return True
