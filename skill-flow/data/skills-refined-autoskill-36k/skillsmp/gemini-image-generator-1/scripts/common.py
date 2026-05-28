import base64
import io
import os
import sys
from datetime import datetime
from urllib.parse import urlparse

import requests
from PIL import Image
from google.genai import types

ASPECT_RATIOS = {
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
}

IMAGE_SIZES = {"1K", "2K", "4K"}

MODEL_MAP = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def load_image(source: str) -> Image.Image:
    if is_url(source):
        response = requests.get(source, timeout=30)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    return Image.open(source)


def validate_aspect_ratio(aspect: str) -> None:
    if aspect not in ASPECT_RATIOS:
        raise ValueError(f"Unsupported aspect ratio: {aspect}")


def validate_count(count: int) -> None:
    if count < 1 or count > 3:
        raise ValueError("--count must be between 1 and 3")


def validate_reference_count(reference_count: int) -> None:
    if reference_count > 14:
        raise ValueError("--reference supports up to 14 images")


def choose_model(requested: str, size: str | None, force_pro: bool, reference_count: int) -> tuple[str, str | None]:
    needs_pro = force_pro or bool(size) or reference_count >= 2
    model = requested
    if model == "flash" and needs_pro:
        model = "pro"
        reason = "logo overlay" if force_pro else "reference images" if reference_count >= 2 else "--size"
        print(f"Switching to Pro because {reason} requires it.", file=sys.stderr)
    if model == "pro" and not size:
        size = "1K"
    if model == "flash" and size:
        print("Ignoring --size because Flash does not support image_size.", file=sys.stderr)
        size = None
    return model, size


def build_config(aspect: str, model: str, size: str | None, response_modalities: list[str]) -> types.GenerateContentConfig:
    image_config = types.ImageConfig(aspect_ratio=aspect)
    if model == "pro" and size:
        image_config.image_size = size
    return types.GenerateContentConfig(
        response_modalities=response_modalities,
        image_config=image_config,
    )


def get_parts(response):
    if getattr(response, "parts", None):
        return response.parts
    candidates = getattr(response, "candidates", None)
    if not candidates:
        return []
    content = getattr(candidates[0], "content", None)
    return getattr(content, "parts", []) if content else []


def inline_data_bytes(part):
    inline = getattr(part, "inline_data", None) or getattr(part, "inlineData", None)
    if inline is None:
        return None
    data = getattr(inline, "data", None)
    if data is None and isinstance(inline, dict):
        data = inline.get("data")
    if data is None:
        return None
    if isinstance(data, str):
        return base64.b64decode(data)
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, bytes):
        return data
    return None


def save_response_images(response, out_dir: str, prefix: str, image_index: int) -> tuple[list[str], int]:
    os.makedirs(out_dir, exist_ok=True)
    saved_paths = []
    for part in get_parts(response):
        data = inline_data_bytes(part)
        if not data:
            continue
        filename = f"{prefix}_{image_index:02d}.png"
        path = os.path.join(out_dir, filename)
        with open(path, "wb") as f:
            f.write(data)
        saved_paths.append(path)
        image_index += 1
    return saved_paths, image_index


def make_timestamp_prefix() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H%M%S")
