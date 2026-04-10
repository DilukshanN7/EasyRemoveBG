from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from easyremovebg.errors import EasyRemoveBGError
from easyremovebg.processing import build_output_path


class BuildOutputPathTests(unittest.TestCase):
    def test_default_output_uses_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "photo.jpg"
            source.write_bytes(b"data")

            output = build_output_path(source, suffix="rembg")

            self.assertEqual(output.name, "photo_rembg.png")

    def test_existing_file_gets_numbered_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "photo.jpg"
            source.write_bytes(b"data")
            existing = Path(tmpdir) / "photo_rembg.png"
            existing.write_bytes(b"taken")

            output = build_output_path(source, suffix="rembg")

            self.assertEqual(output.name, "photo_rembg_2.png")

    def test_custom_output_requires_png_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "photo.jpg"
            source.write_bytes(b"data")

            with self.assertRaises(EasyRemoveBGError):
                build_output_path(source, suffix="rembg", output_path=Path(tmpdir) / "output.jpg")


if __name__ == "__main__":
    unittest.main()
