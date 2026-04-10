from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from easyremovebg.cli import build_parser


class CliParserTests(unittest.TestCase):
    def test_remove_bg_command_is_available(self) -> None:
        parser = build_parser()

        args = parser.parse_args(["remove-bg", "image.jpg"])

        self.assertEqual(args.command, "remove-bg")
        self.assertEqual(args.input_path.name, "image.jpg")

    def test_install_command_is_no_longer_exposed(self) -> None:
        parser = build_parser()

        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as exc:
                parser.parse_args(["install-windows-menu"])

        self.assertEqual(exc.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
