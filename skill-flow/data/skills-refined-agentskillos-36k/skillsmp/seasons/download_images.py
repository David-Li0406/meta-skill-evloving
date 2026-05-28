#!/usr/bin/env python3
"""Download images for the 72 Japanese micro-seasons from Unsplash.

Usage:
    uv run download_images.py          # Download all missing images
    uv run download_images.py 70       # Download specific kō number
    uv run download_images.py 70 71 72 # Download multiple kō numbers

Setup:
    1. Sign up at https://unsplash.com/developers (free)
    2. Create an app to get your Access Key
    3. Set environment variable: export UNSPLASH_ACCESS_KEY="your-key-here"
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from seasons_utils import IMAGES_DIR, Ko, get_image_filename, load_ko_dict

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")

# Unsplash search queries for each kō (filenames derived from seasons_data.json)
SEARCH_QUERIES = {
    1: "melting ice spring",
    2: "japanese bush warbler bird",
    3: "fish under ice winter",
    4: "rain wet soil spring",
    5: "morning mist valley",
    6: "tree buds spring sprouting",
    7: "insects emerging spring",
    8: "peach blossom pink flower",
    9: "butterfly metamorphosis",
    10: "sparrow nest building",
    11: "cherry blossom japan sakura",
    12: "spring thunder storm",
    13: "barn swallow bird",
    14: "wild geese flying migration",
    15: "rainbow nature",
    16: "reeds wetland spring",
    17: "rice seedlings paddy",
    18: "peony flower bloom",
    19: "japanese tree frog green",
    20: "earthworm soil",
    21: "bamboo shoots forest",
    22: "silkworm mulberry leaves",
    23: "safflower orange bloom",
    24: "wheat field golden harvest",
    25: "praying mantis green",
    26: "firefly night japan",
    27: "japanese plum ume fruit",
    28: "self heal plant purple flower",
    29: "iris flower purple japanese",
    30: "pinellia plant green",
    31: "summer wind warm breeze",
    32: "lotus flower pink bloom",
    33: "hawk flying learning",
    34: "paulownia tree seeds",
    35: "humid summer earth",
    36: "summer rain storm",
    37: "cool autumn breeze",
    38: "cicada evening tree",
    39: "dense fog morning",
    40: "cotton flower bloom white",
    41: "late summer sunset field",
    42: "rice field golden ripe",
    43: "morning dew grass droplets",
    44: "wagtail bird",
    45: "swallows migrating autumn",
    46: "autumn sky quiet",
    47: "insects hiding autumn",
    48: "rice paddy draining",
    49: "wild geese returning autumn",
    50: "chrysanthemum flower japanese",
    51: "cricket insect autumn",
    52: "first frost morning",
    53: "light rain autumn drizzle",
    54: "maple leaves red autumn japan",
    55: "camellia flower red japanese",
    56: "frozen ground frost",
    57: "daffodil winter bloom",
    58: "winter sky grey clouds",
    59: "wind blowing leaves autumn",
    60: "tangerine citrus orange fruit",
    61: "winter cold sky snow",
    62: "bear hibernating cave",
    63: "salmon swimming upstream",
    64: "self heal plant winter sprout",
    65: "deer antler shedding",
    66: "wheat sprout snow winter",
    67: "japanese parsley herb green",
    68: "natural spring water flowing",
    69: "pheasant bird colorful",
    70: "butterbur flower winter japan",
    71: "frozen stream ice winter",
    72: "hen chicken eggs",
}


def search_unsplash(query: str) -> str | None:
    """Search Unsplash and return the first image URL."""
    if not UNSPLASH_ACCESS_KEY:
        print("  Warning: UNSPLASH_ACCESS_KEY not set")
        return None

    url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(query)}&per_page=1&orientation=landscape"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
            "Accept-Version": "v1",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            if data.get("results"):
                # Get the regular size (1080px width)
                return data["results"][0]["urls"]["regular"]
    except Exception as e:
        print(f"  Unsplash search failed: {e}")

    return None


def download_image(url: str, filepath: Path) -> bool:
    """Download image from URL to filepath."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            filepath.write_bytes(data)
            print(f"  Saved {filepath.name} ({len(data):,} bytes)")
            return True
    except Exception as e:
        print(f"  Download failed: {e}")
        return False


def process_ko(ko_num: int, ko_data: dict[int, Ko]) -> bool:
    """Download image for a specific kō number."""
    if ko_num not in ko_data:
        print(f"  No data for kō {ko_num}")
        return False
    if ko_num not in SEARCH_QUERIES:
        print(f"  No search query for kō {ko_num}")
        return False

    ko = ko_data[ko_num]
    filename = get_image_filename(ko)
    filepath = IMAGES_DIR / filename

    if filepath.exists():
        print(f"  {filename} already exists, skipping")
        return True

    search_query = SEARCH_QUERIES[ko_num]
    print(f"  Searching Unsplash for: {search_query}")
    image_url = search_unsplash(search_query)

    if image_url:
        return download_image(image_url, filepath)
    else:
        print(f"  No image found for kō {ko_num}")
        return False


def main() -> None:
    """Download images for specified kō numbers (or all if none specified)."""
    IMAGES_DIR.mkdir(exist_ok=True)

    if not UNSPLASH_ACCESS_KEY:
        print("ERROR: UNSPLASH_ACCESS_KEY environment variable not set")
        print()
        print("Setup:")
        print("  1. Sign up at https://unsplash.com/developers (free)")
        print("  2. Create an app to get your Access Key")
        print("  3. Run: export UNSPLASH_ACCESS_KEY='your-key-here'")
        print()
        sys.exit(1)

    ko_data = load_ko_dict()

    # Determine which kō to download
    if len(sys.argv) > 1:
        ko_numbers = [int(arg) for arg in sys.argv[1:]]
    else:
        ko_numbers = list(range(1, 73))

    print(f"Downloading images to {IMAGES_DIR}")
    print(f"Kō numbers: {ko_numbers}")
    print()

    success = 0
    for ko_num in ko_numbers:
        print(f"Kō {ko_num}:")
        if process_ko(ko_num, ko_data):
            success += 1
        print()

    print(f"Downloaded {success}/{len(ko_numbers)} images")


if __name__ == "__main__":
    main()
