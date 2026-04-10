from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .errors import EasyRemoveBGError
from .processing import remove_background, remove_logo_background


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


def _positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("Value must be greater than zero.")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
