#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DEFAULT_EXTENSIONS = {".m4b"}
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


def natural_key(text: str) -> List[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", text)]


def parse_index(value: object) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value)
    match = re.search(r"\d+", text)
    if not match:
        return None
    return int(match.group(0))


def collect_files(root: Path, recursive: bool, extensions: set[str]) -> List[Path]:
    if recursive:
        candidates = [p for p in root.rglob("*") if p.is_file()]
    else:
        candidates = [p for p in root.iterdir() if p.is_file()]
    files = [p for p in candidates if p.suffix.lower() in extensions]
    files.sort(key=lambda p: natural_key(str(p.relative_to(root))))
    return files


def load_exiftool(paths: List[Path]) -> Dict[Path, Dict[str, object]]:
    args = [
        "exiftool",
        "-j",
        "-TrackNumber",
        "-DiskNumber",
        "-Title",
        "-Album",
        "-Artist",
        "-AlbumArtist",
        "-Duration",
        "-CoverArt",
        "-Picture",
        "-APIC",
        "-FileName",
    ] + [str(p) for p in paths]
    result = subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    data = json.loads(result.stdout)
    mapping: Dict[Path, Dict[str, object]] = {}
    for item in data:
        source = item.get("SourceFile")
        if not source:
            continue
        mapping[Path(source)] = item
    return mapping


def load_ffprobe(path: Path) -> Dict[str, object]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:format_tags=track,disc,title,album,artist,album_artist",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    data = json.loads(result.stdout)
    tags = (data.get("format") or {}).get("tags") or {}
    duration = (data.get("format") or {}).get("duration")
    return {
        "TrackNumber": tags.get("track"),
        "DiskNumber": tags.get("disc"),
        "Title": tags.get("title"),
        "Album": tags.get("album"),
        "Artist": tags.get("artist"),
        "AlbumArtist": tags.get("album_artist"),
        "Duration": duration,
        "FileName": path.name,
    }


def load_metadata(paths: List[Path]) -> Dict[Path, Dict[str, object]]:
    if shutil.which("exiftool"):
        try:
            return load_exiftool(paths)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
            print("exiftool failed, falling back to ffprobe.", file=sys.stderr)
            if isinstance(exc, subprocess.CalledProcessError):
                print(exc.stderr, file=sys.stderr)
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe is required when exiftool is unavailable.")

    mapping: Dict[Path, Dict[str, object]] = {}
    for path in paths:
        try:
            mapping[path] = load_ffprobe(path)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
            print(f"ffprobe failed for {path}: {exc}", file=sys.stderr)
    return mapping


def compute_order(
    files: List[Path],
    metadata: Dict[Path, Dict[str, object]],
    root: Path,
) -> Tuple[List[Path], List[str]]:
    warnings: List[str] = []
    entries = []
    has_track = False
    missing_track = False
    for path in files:
        info = metadata.get(path, {})
        track = parse_index(info.get("TrackNumber"))
        disc = parse_index(info.get("DiskNumber")) or 1
        if track is None:
            missing_track = True
        else:
            has_track = True
        entries.append((path, disc, track))

    if has_track:
        if missing_track:
            warnings.append("Some files are missing track numbers; ordering may be incomplete.")
        ordered = sorted(
            entries,
            key=lambda item: (
                item[1],
                item[2] if item[2] is not None else 10**9,
                natural_key(str(item[0].relative_to(root))),
            ),
        )
        return [item[0] for item in ordered], warnings

    warnings.append("No track numbers detected; falling back to filename order.")
    return files, warnings


def metadata_score(info: Dict[str, object]) -> int:
    score = 0
    for key in ("Title", "Album", "Artist", "AlbumArtist"):
        value = info.get(key)
        if value:
            score += 1
    return score


def choose_metadata_source(
    ordered: List[Path],
    metadata: Dict[Path, Dict[str, object]],
) -> Optional[Path]:
    best_path = None
    best_score = -1
    for path in ordered:
        score = metadata_score(metadata.get(path, {}))
        if score > best_score:
            best_score = score
            best_path = path
    if best_score <= 0:
        return None
    return best_path


def has_embedded_cover(info: Dict[str, object]) -> bool:
    for key in ("CoverArt", "Picture", "APIC"):
        value = info.get(key)
        if value:
            return True
    return False


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


def choose_cover_source(
    root: Path,
    recursive: bool,
    ordered: List[Path],
    metadata: Dict[Path, Dict[str, object]],
    image_names: set[str],
) -> Optional[str]:
    sidecar = find_sidecar(root, recursive, image_names)
    if sidecar:
        return f"sidecar:{sidecar.relative_to(root)}"

    for path in ordered:
        info = metadata.get(path, {})
        if has_embedded_cover(info):
            return f"embedded:{path.relative_to(root)}"
    return None


def format_summary(
    ordered: List[Path],
    metadata: Dict[Path, Dict[str, object]],
    root: Path,
    warnings: List[str],
    metadata_source: Optional[Path],
    cover_source: Optional[str],
) -> str:
    lines = []
    lines.append("Proposed order:")
    for idx, path in enumerate(ordered, start=1):
        info = metadata.get(path, {})
        track = info.get("TrackNumber")
        disc = info.get("DiskNumber")
        title = info.get("Title")
        rel = path.relative_to(root)
        detail = []
        if disc:
            detail.append(f"disc={disc}")
        if track:
            detail.append(f"track={track}")
        if title:
            detail.append(f"title={title}")
        suffix = f" ({', '.join(detail)})" if detail else ""
        lines.append(f"  {idx:02d}. {rel}{suffix}")

    if warnings:
        lines.append("")
        lines.append("Warnings:")
        for warning in warnings:
            lines.append(f"- {warning}")

    lines.append("")
    lines.append("Action plan (confirm before merging):")
    lines.append(f"- Inputs: {len(ordered)} file(s) under {root}")
    lines.append("- Order: use the proposed sequence above")
    if metadata_source:
        lines.append(
            f"- Metadata source: {metadata_source.relative_to(root)} (most complete tags, normalize to UTF-8)"
        )
    else:
        lines.append("- Metadata source: none detected (supply manually or choose a source file)")
    if cover_source:
        lines.append(f"- Cover source: {cover_source}")
    else:
        lines.append("- Cover source: none detected (supply a cover image)")
    lines.append("- Chapters: choose dir/file/none or merge existing chapters")
    lines.append("- Encoding: normalize non-UTF-8 text as Russian to UTF-8")
    lines.append("- Output: build final M4B after user confirmation")

    return "\n".join(lines)


def write_concat_list(ordered: List[Path], output_path: Path) -> None:
    for path in ordered:
        if "'" in str(path):
            raise ValueError(f"file path contains a single quote: {path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for path in ordered:
            handle.write(f"file '{path.resolve()}'\n")


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


def parse_names(value: str) -> set[str]:
    names = set()
    for item in value.split(","):
        item = item.strip().lower()
        if item:
            names.add(item)
    return names


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Propose an M4B part order using metadata and filenames.",
    )
    parser.add_argument("--root", default=".", help="Root directory containing M4B parts.")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories for M4B files.",
    )
    parser.add_argument(
        "--extensions",
        default=",".join(sorted(ext.lstrip(".") for ext in DEFAULT_EXTENSIONS)),
        help="Comma-separated extensions to include.",
    )
    parser.add_argument(
        "--image-names",
        default=",".join(sorted(DEFAULT_IMAGE_NAMES)),
        help="Comma-separated sidecar image filenames to search for.",
    )
    parser.add_argument(
        "--files-out",
        help="Optional path to write ffmpeg concat list in proposed order.",
    )

    args = parser.parse_args()
    root = Path(args.root).resolve()
    extensions = parse_extensions(args.extensions)
    image_names = parse_names(args.image_names)

    files = collect_files(root, args.recursive, extensions)
    if not files:
        print("No matching M4B files found.", file=sys.stderr)
        return 2

    try:
        metadata = load_metadata(files)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    ordered, warnings = compute_order(files, metadata, root)
    metadata_source = choose_metadata_source(ordered, metadata)
    cover_source = choose_cover_source(root, args.recursive, ordered, metadata, image_names)
    print(format_summary(ordered, metadata, root, warnings, metadata_source, cover_source))

    if args.files_out:
        try:
            write_concat_list(ordered, Path(args.files_out))
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
