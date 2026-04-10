from __future__ import annotations

import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from easyremovebg import __version__


class DistributionAssetsTests(unittest.TestCase):
    def test_installer_targets_image_file_context_menu(self) -> None:
        installer_script = (ROOT / "installer" / "EasyRemoveBG.iss").read_text(encoding="utf-8")

        self.assertIn(r"Software\Classes\SystemFileAssociations\image\shell", installer_script)
        self.assertIn(r'"""{app}\{#MyAppExeName}"" remove-bg ""%1"""', installer_script)
        self.assertIn(r'"""{app}\{#MyAppExeName}"" remove-logo ""%1"""', installer_script)

    def test_pyinstaller_spec_targets_package_main(self) -> None:
        spec_file = (ROOT / "packaging" / "pyinstaller" / "EasyRemoveBG.spec").read_text(encoding="utf-8")

        self.assertIn('__main__.py")],', spec_file)
        self.assertIn('name="EasyRemoveBG"', spec_file)
        self.assertIn('collect_submodules("rembg")', spec_file)

    def test_pyproject_version_matches_package_version(self) -> None:
        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["version"], __version__)


if __name__ == "__main__":
    unittest.main()
