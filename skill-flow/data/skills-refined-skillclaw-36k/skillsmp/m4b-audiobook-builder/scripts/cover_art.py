#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
import re
from typing import Iterable, List, Optional

DEFAULT_AUDIO_EXTENSIONS = {
    ".m4b",
    ".m4a",
    ".mp3",
    ".aac",
    ".flac",
    ".ogg",
    ".wav",
}

DEFAULT_IMAGE_NAMES = {
    "cover.jpg",
    "cover.jpeg",
    "folder.jpg",
    "front.jpg",
    "artwork.jpg",
    "cover.png",
    "folder.png",
    "front.png",
    "artwork.png",
}

EXIFTOOL_TAGS = ["CoverArt", "Picture", "APIC"]


def natural_key(text: str) -> List[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\\d+)", text)]


def collect_files(root: Path, recursive: bool, extensions: set[str]) -> List[Path]:
    if recursive:
        candidates = [p for p in root.rglob("*") if p.is_file()]
    else:
        candidates = [p for p in root.iterdir() if p.is_file()]
    files = [p for p in candidates if p.suffix.lower() in extensions]
    files.sort(key=lambda p: natural_key(str(p.relative_to(root))))
    return files


def find_sidecar(root: Path, recursive: bool, names: set[str]) -> Optional[Path]:
    if recursive:
        candidates = [p for p in root.rglob("*") if p.is_file()]
    else:
        candidates = [p for p in root.iterdir() if p.is_file()]
    matches = [p for p in candidates if p.name.lower() in names]
    if not matches:
        return None
    matches.sort(key=lambda p: natural_key(str(p.relative_to(root))))
    return matches[0]


def extract_cover_with_exiftool(source: Path, output: Path) -> bool:
    for tag in EXIFTOOL_TAGS:
        result = subprocess.run(
            ["exiftool", "-b", f"-{tag}", str(source)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            continue
        if not result.stdout:
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(result.stdout)
        if output.stat().st_size > 0:
            return True
    return False


def extract_cover(
    root: Path,
    recursive: bool,
    output: Path,
    image_names: set[str],
    extensions: set[str],
) -> Optional[Path]:
    sidecar = find_sidecar(root, recursive, image_names)
    if sidecar:
        output.parent.mkdir(parents=True, exist_ok=True)
        if sidecar.resolve() != output.resolve():
            shutil.copyfile(sidecar, output)
        return output

    if not shutil.which("exiftool"):
        return None

    audio_files = collect_files(root, recursive, extensions)
    audio_files.sort(
        key=lambda p: (
            0 if p.suffix.lower() == ".m4b" else 1,
            natural_key(str(p.relative_to(root))),
        )
    )

    for path in audio_files:
        if extract_cover_with_exiftool(path, output):
            return output

    return None


def embed_cover(cover: Path, target: Path) -> bool:
    if not shutil.which("AtomicParsley"):
        return False
    result = subprocess.run(
        ["AtomicParsley", str(target), "--artwork", str(cover), "--overWrite"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode == 0


def parse_extensions(value: str) -> set[str]:
    extensions = set()
    for item in value.split(","):
        item = item.strip().lower()
        if not item:
            continue
        if not item.startswith("."):
            item = f".{item}"
        extensions.add(item)
    return extensions


def parse_image_names(value: str) -> set[str]:
    names = set()
    for item in value.split(","):
        item = item.strip().lower()
        if item:
            names.add(item)
    return names


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract cover art from sidecar images or embedded metadata.",
    )
    parser.add_argument("--root", default=".", help="Root directory to scan.")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories for images and audio files.",
    )
    parser.add_argument(
        "--output",
        default="cover.jpg",
        help="Output image path for extracted cover art.",
    )
    parser.add_argument(
        "--embed",
        help="Optional target M4B to embed cover art via AtomicParsley.",
    )
    parser.add_argument(
        "--extensions",
        default=",".join(sorted(ext.lstrip(".") for ext in DEFAULT_AUDIO_EXTENSIONS)),
        help="Comma-separated audio extensions to search for embedded art.",
    )
    parser.add_argument(
        "--image-names",
        default=",".join(sorted(DEFAULT_IMAGE_NAMES)),
        help="Comma-separated sidecar image filenames to search for.",
    )

    args = parser.parse_args()
    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    extensions = parse_extensions(args.extensions)
    image_names = parse_image_names(args.image_names)

    cover = extract_cover(root, args.recursive, output, image_names, extensions)
    if not cover:
        print("No cover art found in sidecar images or embedded metadata.", file=sys.stderr)
        return 2

    print(f"Cover art saved to {cover}")

    if args.embed:
        target = Path(args.embed).resolve()
        if not target.exists():
            print(f"Target M4B not found: {target}", file=sys.stderr)
            return 3
        if not embed_cover(cover, target):
            print("AtomicParsley failed to embed cover art.", file=sys.stderr)
            return 4
        print(f"Embedded cover art into {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
