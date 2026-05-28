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
    validate_reference_count,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Edit images with Gemini Nano Banana.")
    parser.add_argument("--input", required=True, help="Base image path or URL.")
    parser.add_argument("--prompt", required=True, help="Edit instructions.")
    parser.add_argument(
        "--reference", action="append", default=[], help="Reference image path or URL."
    )
    parser.add_argument(
        "--aspect", default="9:16", help="Aspect ratio (e.g., 9:16, 16:9)."
    )
    parser.add_argument(
        "--count", type=int, default=1, help="Number of images to generate (max 3)."
    )
    parser.add_argument(
        "--model",
        choices=MODEL_MAP.keys(),
        default="flash",
        help="Model: flash or pro.",
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
        validate_reference_count(len(args.reference))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        base_image = load_image(args.input)
        reference_images = [load_image(path) for path in args.reference]
    except Exception as exc:
        print(f"Failed to load images: {exc}", file=sys.stderr)
        return 2

    model, size = choose_model(
        requested=args.model,
        size=args.size,
        force_pro=False,
        reference_count=len(reference_images),
    )
    config = build_config(
        args.aspect, model, size, response_modalities=["TEXT", "IMAGE"]
    )

    client = genai.Client()
    timestamp = make_timestamp_prefix()
    saved_paths = []
    image_index = 1

    contents = [args.prompt, base_image, *reference_images]
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
