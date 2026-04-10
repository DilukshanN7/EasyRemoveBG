from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from easyremovebg.windows_integration import build_context_menu_entries


class BuildContextMenuEntriesTests(unittest.TestCase):
    def test_registry_commands_use_selected_python(self) -> None:
        entries = build_context_menu_entries(Path(r"C:\Python312\python.exe"))

        self.assertEqual(len(entries), 2)
        self.assertIn('-m easyremovebg.cli remove-bg "%1"', entries[0].command)
        self.assertIn('-m easyremovebg.cli remove-logo "%1"', entries[1].command)
        self.assertTrue(entries[0].command.startswith('"C:\\Python312\\python.exe"'))


if __name__ == "__main__":
    unittest.main()
