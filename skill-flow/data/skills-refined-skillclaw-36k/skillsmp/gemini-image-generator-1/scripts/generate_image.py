#!/usr/bin/env python3
import argparse
import sys

from google import genai

from common import (
    IMAGE_SIZES,
    MODEL_MAP,
    build_config,
    choose_model,
    make_timestamp_prefix,
    save_response_images,
    validate_aspect_ratio,
    validate_count,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images with Gemini Nano Banana."
    )
    parser.add_argument(
        "--prompt", required=True, help="Text prompt for image generation."
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
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    model, size = choose_model(
        requested=args.model,
        size=args.size,
        force_pro=False,
        reference_count=0,
    )
    config = build_config(args.aspect, model, size, response_modalities=["IMAGE"])

    client = genai.Client()
    timestamp = make_timestamp_prefix()
    saved_paths = []
    image_index = 1

    for _ in range(args.count):
        response = client.models.generate_content(
            model=MODEL_MAP[model],
            contents=args.prompt,
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
