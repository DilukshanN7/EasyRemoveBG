from __future__ import annotations

from io import BytesIO
from pathlib import Path

from .errors import DependencyError, EasyRemoveBGError


def resolve_input_path(path_value: str | Path) -> Path:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise EasyRemoveBGError(f"Input file was not found: {path}")
    return path


def build_output_path(
    input_path: Path,
    *,
    suffix: str,
    output_path: str | Path | None = None,
    overwrite: bool = False,
) -> Path:
    if output_path is not None:
        candidate = Path(output_path).expanduser()
        if candidate.suffix and candidate.suffix.lower() != ".png":
            raise EasyRemoveBGError("Output path must use the .png extension.")
        if not candidate.suffix:
            candidate = candidate.with_suffix(".png")
    else:
        candidate = input_path.with_name(f"{input_path.stem}_{suffix}.png")

    candidate.parent.mkdir(parents=True, exist_ok=True)
    return _avoid_collision(candidate, overwrite=overwrite)


def remove_background(
    input_path: str | Path,
    *,
    output_path: str | Path | None = None,
    overwrite: bool = False,
) -> Path:
    source = resolve_input_path(input_path)
    destination = build_output_path(
        source,
        suffix="rembg",
        output_path=output_path,
        overwrite=overwrite,
    )

    try:
        from PIL import Image
    except ImportError as exc:
        raise DependencyError("Pillow is required. Install the project dependencies first.") from exc

    try:
        from rembg import remove
    except ImportError as exc:
        raise DependencyError("rembg is required. Install the project dependencies first.") from exc

    try:
        input_bytes = source.read_bytes()
        output_bytes = remove(input_bytes)
        with Image.open(BytesIO(output_bytes)) as image:
            image.convert("RGBA").save(destination, format="PNG")
    except EasyRemoveBGError:
        raise
    except Exception as exc:
        raise EasyRemoveBGError(f"Background removal failed for {source.name}: {exc}") from exc

    return destination


def remove_logo_background(
    input_path: str | Path,
    *,
    output_path: str | Path | None = None,
    overwrite: bool = False,
    tolerance: float | None = None,
) -> Path:
    source = resolve_input_path(input_path)
    destination = build_output_path(
        source,
        suffix="logo",
        output_path=output_path,
        overwrite=overwrite,
    )

    cv2, np = _load_cv2_stack()

    image = cv2.imread(str(source), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise EasyRemoveBGError(f"Could not open image data from {source}")

    bgra_image = _to_bgra(image, cv2)
    rgb_image = cv2.cvtColor(bgra_image[:, :, :3], cv2.COLOR_BGR2RGB)
    lab_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2LAB).astype(np.float32)

    border_pixels = _sample_border_pixels(lab_image, np)
    background_color = np.median(border_pixels, axis=0)
    border_distances = np.linalg.norm(border_pixels - background_color, axis=1)
    dynamic_threshold = float(np.percentile(border_distances, 95)) + 8.0
    threshold = tolerance if tolerance is not None else max(12.0, dynamic_threshold)

    distances = np.linalg.norm(lab_image - background_color, axis=2)
    mask = np.where(distances > threshold, 255, 0).astype(np.uint8)

    kernel_size = _kernel_size(mask.shape[0], mask.shape[1])
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    blur_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
    alpha_channel = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
    alpha_channel = cv2.min(alpha_channel, bgra_image[:, :, 3])
    bgra_image[:, :, 3] = alpha_channel

    if not cv2.imwrite(str(destination), bgra_image):
        raise EasyRemoveBGError(f"Could not write output image to {destination}")

    return destination


def _avoid_collision(path: Path, *, overwrite: bool) -> Path:
    if overwrite or not path.exists():
        return path

    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def _load_cv2_stack():
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise DependencyError(
            "opencv-python-headless and numpy are required. Install the project dependencies first."
        ) from exc

    return cv2, np


def _to_bgra(image, cv2):
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
    if image.shape[2] == 4:
        return image.copy()
    if image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    raise EasyRemoveBGError("Unsupported image format.")


def _sample_border_pixels(lab_image, np):
    height, width = lab_image.shape[:2]
    border = max(1, min(height, width) // 20)
    top = lab_image[:border, :, :]
    bottom = lab_image[-border:, :, :]
    left = lab_image[border:-border or None, :border, :]
    right = lab_image[border:-border or None, -border:, :]

    return np.concatenate(
        [
            top.reshape(-1, 3),
            bottom.reshape(-1, 3),
            left.reshape(-1, 3),
            right.reshape(-1, 3),
        ],
        axis=0,
    )


def _kernel_size(height: int, width: int) -> int:
    smallest_side = min(height, width)
    if smallest_side >= 1200:
        return 7
    if smallest_side >= 300:
        return 5
    return 3
