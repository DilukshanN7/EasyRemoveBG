from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .errors import EasyRemoveBGError
from .processing import remove_background, remove_logo_background
from .windows_integration import install_context_menu, uninstall_context_menu


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="easyremovebg",
        description="Remove image backgrounds from photos and logos.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    remove_bg = subparsers.add_parser("remove-bg", help="Remove the background from a general image.")
    _add_file_arguments(remove_bg)
    remove_bg.set_defaults(handler=_handle_remove_bg)

    remove_logo = subparsers.add_parser("remove-logo", help="Remove a flat or near-flat logo background.")
    _add_file_arguments(remove_logo)
    remove_logo.add_argument(
        "--tolerance",
        type=_positive_float,
        help="Override the automatic background distance threshold.",
    )
    remove_logo.set_defaults(handler=_handle_remove_logo)

    install_menu = subparsers.add_parser("install-windows-menu", help="Install the per-user Explorer context menu.")
    install_menu.add_argument(
        "--python",
        dest="python_executable",
        type=Path,
        help="Override the Python executable written to the registry.",
    )
    install_menu.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the registry commands without writing them.",
    )
    install_menu.set_defaults(handler=_handle_install_menu)

    uninstall_menu = subparsers.add_parser(
        "uninstall-windows-menu",
        help="Remove the per-user Explorer context menu.",
    )
    uninstall_menu.set_defaults(handler=_handle_uninstall_menu)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        return 2

    try:
        return args.handler(args)
    except EasyRemoveBGError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Error: operation cancelled.", file=sys.stderr)
        return 130


def _add_file_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("input_path", type=Path, help="Image file to process.")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        type=Path,
        help="Optional output PNG path.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the target file instead of creating a numbered filename.",
    )


def _handle_remove_bg(args: argparse.Namespace) -> int:
    destination = remove_background(
        args.input_path,
        output_path=args.output_path,
        overwrite=args.overwrite,
    )
    print(destination)
    return 0


def _handle_remove_logo(args: argparse.Namespace) -> int:
    destination = remove_logo_background(
        args.input_path,
        output_path=args.output_path,
        overwrite=args.overwrite,
        tolerance=args.tolerance,
    )
    print(destination)
    return 0


def _handle_install_menu(args: argparse.Namespace) -> int:
    entries = install_context_menu(args.python_executable, dry_run=args.dry_run)
    if args.dry_run:
        for entry in entries:
            print(f"{entry.label}: {entry.command}")
        return 0

    for entry in entries:
        print(f"Installed {entry.label}")
    return 0


def _handle_uninstall_menu(args: argparse.Namespace) -> int:
    removed = uninstall_context_menu()
    print(f"Removed {removed} context menu entr{'y' if removed == 1 else 'ies'}")
    return 0


def _positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("Value must be greater than zero.")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
