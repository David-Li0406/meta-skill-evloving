#!/usr/bin/env python3
import argparse
import sys

from google import genai

from common import (
    IMAGE_SIZES,
    MODEL_MAP,
    build_config,
    choose_model,
    load_image,
    make_timestamp_prefix,
    save_response_images,
    validate_aspect_ratio,
    validate_count,
)

DEFAULT_PROMPT = (
    "Take the first image as the base. Add the logo from the second image onto a natural, "
    "appropriate surface (for example: a shirt, sign, device, or packaging). Preserve the "
    "subject's identity and all existing details. Match lighting, perspective, and texture so "
    "the logo appears printed or applied to the surface. Do not alter faces or key features."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Overlay a logo onto a base image.")
    parser.add_argument("--base", required=True, help="Base image path or URL.")
    parser.add_argument("--logo", required=True, help="Logo image path or URL.")
    parser.add_argument(
        "--prompt", default=DEFAULT_PROMPT, help="Prompt override for logo placement."
    )
    parser.add_argument(
        "--aspect", default="9:16", help="Aspect ratio (e.g., 9:16, 16:9)."
    )
    parser.add_argument(
        "--count", type=int, default=1, help="Number of images to generate (max 3)."
    )
    parser.add_argument(
        "--model", choices=MODEL_MAP.keys(), default="pro", help="Model: flash or pro."
    )
    parser.add_argument(
        "--size", choices=sorted(IMAGE_SIZES), help="Image size (Pro only): 1K, 2K, 4K."
    )
    parser.add_argument(
        "--out-dir", default="outputs", help="Output directory for images."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        validate_aspect_ratio(args.aspect)
        validate_count(args.count)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        base_image = load_image(args.base)
        logo_image = load_image(args.logo)
    except Exception as exc:
        print(f"Failed to load images: {exc}", file=sys.stderr)
        return 2

    model, size = choose_model(
        requested=args.model,
        size=args.size,
        force_pro=True,
        reference_count=0,
    )
    config = build_config(
        args.aspect, model, size, response_modalities=["TEXT", "IMAGE"]
    )

    client = genai.Client()
    timestamp = make_timestamp_prefix()
    saved_paths = []
    image_index = 1

    contents = [args.prompt, base_image, logo_image]
    for _ in range(args.count):
        response = client.models.generate_content(
            model=MODEL_MAP[model],
            contents=contents,
            config=config,
        )
        new_paths, image_index = save_response_images(
            response,
            args.out_dir,
            timestamp,
            image_index,
        )
        saved_paths.extend(new_paths)

    if not saved_paths:
        print("No image data returned by the API.", file=sys.stderr)
        return 1

    for path in saved_paths:
        print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
