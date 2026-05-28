#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

DEFAULT_EXTENSIONS = {
    ".mp3",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
    ".wav",
    ".m4b",
}


def natural_key(text: str) -> List[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", text)]


def reorder_person_name(name: str) -> str:
    parts = [part for part in name.split() if part]
    if len(parts) < 2:
        return name.strip()
    return " ".join([parts[-1]] + parts[:-1])


def reorder_name_list(value: str) -> str:
    names = [part.strip() for part in re.split(r"[;,]", value) if part.strip()]
    reordered = [reorder_person_name(name) for name in names]
    return ", ".join(reordered)


def sanitize_filename(name: str) -> str:
    invalid = set('<>:"/\\|?*')
    cleaned = []
    for char in name:
        if char in invalid or ord(char) < 32:
            cleaned.append("_")
        else:
            cleaned.append(char)
    result = "".join(cleaned).strip().rstrip(". ")
    if not result:
        result = "book"
    reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }
    if result.upper() in reserved:
        result = f"_{result}"
    return result


def build_output_name(author: Optional[str], title: Optional[str]) -> Optional[str]:
    if author and title:
        return f"{author} - {title}.m4b"
    return None


def probe_output_tags(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format_tags=album,album_artist,artist,title",
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
    return (data.get("format") or {}).get("tags") or {}


def derive_metadata_defaults(files: List[Path], root: Path) -> Tuple[str, str, str]:
    author = ""
    title = ""
    narrator = ""
    if files and shutil.which("ffprobe"):
        try:
            tags = probe_output_tags(files[0])
            artist = str(tags.get("artist") or "").strip()
            author = str(tags.get("album_artist") or artist or "").strip()
            title = str(tags.get("album") or tags.get("title") or "").strip()
            narrator = artist if artist and artist != author else ""
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            author = ""
            title = ""
            narrator = ""

    if not author or not title:
        root_name = root.name.strip()
        if " - " in root_name:
            left, right = root_name.split(" - ", 1)
            author = author or left.strip()
            title = title or right.strip()
        else:
            title = title or root_name

    if not author:
        author = "Unknown Author"
    if not title:
        title = "Unknown Title"

    return author, title, narrator


def build_atomicparsley_command(
    output_m4b: Path,
    author: Optional[str],
    title: Optional[str],
    narrator: Optional[str],
    cover_path: Optional[Path],
) -> List[str]:
    cmd = ["AtomicParsley", str(output_m4b), "--stik", "Audiobook"]
    if narrator:
        cmd += ["--artist", narrator]
    if author:
        cmd += ["--albumArtist", author]
    if title:
        cmd += ["--album", title, "--title", title]
    if cover_path:
        cmd += ["--artwork", str(cover_path)]
    cmd += ["--overWrite"]
    return cmd


def collect_files(root: Path, recursive: bool, extensions: set[str]) -> List[Path]:
    if recursive:
        candidates = [p for p in root.rglob("*") if p.is_file()]
    else:
        candidates = [p for p in root.iterdir() if p.is_file()]

    files = [p for p in candidates if p.suffix.lower() in extensions]
    files.sort(key=lambda p: natural_key(str(p.relative_to(root))))
    return files


def write_concat_list(files: Iterable[Path], output_path: Path) -> None:
    for path in files:
        if "'" in str(path):
            raise ValueError(f"file path contains a single quote: {path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for path in files:
            handle.write(f"file '{path.resolve()}'\n")


def probe_duration_and_title(path: Path) -> Tuple[int, str]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:format_tags=title",
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
    fmt = data.get("format") or {}
    duration = fmt.get("duration")
    if not duration:
        raise ValueError(f"No duration found for {path}")
    title = (fmt.get("tags") or {}).get("title") or ""
    seconds = float(duration)
    return int(round(seconds * 1000)), str(title).strip()


def chapter_title_from_dir(path: Path, root: Path) -> str:
    relative = path.parent.relative_to(root)
    if str(relative) == ".":
        return root.name or "Root"
    return relative.as_posix()


def build_chapters(
    files: List[Path],
    root: Path,
    chapter_mode: str,
) -> List[tuple[int, int, str]]:
    if chapter_mode == "none":
        return []

    durations_ms: List[int] = []
    titles: List[str] = []
    for path in files:
        duration_ms, title = probe_duration_and_title(path)
        durations_ms.append(duration_ms)
        titles.append(title)

    if chapter_mode == "file":
        chapters: List[tuple[int, int, str]] = []
        start_ms = 0
        for path, duration_ms, title in zip(files, durations_ms, titles):
            end_ms = start_ms + duration_ms
            chapter_title = title if title and not title.isdigit() else path.stem
            chapters.append((start_ms, end_ms, chapter_title))
            start_ms = end_ms
        return chapters

    chapters = []
    chapter_starts: List[int] = []
    chapter_titles: List[str] = []
    current_key = None
    cumulative_ms = 0

    for path, duration_ms in zip(files, durations_ms):
        dir_title = chapter_title_from_dir(path, root)
        if dir_title != current_key:
            chapter_titles.append(dir_title)
            chapter_starts.append(cumulative_ms)
            current_key = dir_title
        cumulative_ms += duration_ms

    total_ms = cumulative_ms
    for index, title in enumerate(chapter_titles):
        start_ms = chapter_starts[index]
        end_ms = chapter_starts[index + 1] if index + 1 < len(chapter_starts) else total_ms
        chapters.append((start_ms, end_ms, title))

    return chapters


def write_ffmetadata(chapters: List[tuple[int, int, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(";FFMETADATA1\n")
        for start_ms, end_ms, title in chapters:
            handle.write("[CHAPTER]\n")
            handle.write("TIMEBASE=1/1000\n")
            handle.write(f"START={start_ms}\n")
            handle.write(f"END={end_ms}\n")
            handle.write(f"title={title}\n")


def build_ffmpeg_command(
    files_out: Path,
    meta_out: Path,
    output_m4b: Path,
    include_meta: bool,
    audio_codec: str,
    bitrate: str,
    threads: str,
) -> List[str]:
    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(files_out)]
    if include_meta:
        cmd += ["-f", "ffmetadata", "-i", str(meta_out)]
    cmd += [
        "-map",
        "0:a:0",
        "-vn",
        "-c:a",
        audio_codec,
        "-b:a",
        bitrate,
        "-threads",
        threads,
    ]
    if include_meta:
        cmd += ["-map_metadata", "1", "-map_chapters", "1"]
    cmd += ["-movflags", "+faststart", str(output_m4b)]
    return cmd


def write_ffmpeg_command(command: List[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{shlex.join(command)}\n", encoding="utf-8")


def write_atomicparsley_command(command: List[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{shlex.join(command)}\n", encoding="utf-8")


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate ffmpeg concat and chapter metadata files for M4B builds.",
    )
    parser.add_argument("--root", default=".", help="Root directory containing audio files.")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories and keep natural order.",
    )
    parser.add_argument(
        "--chapter-mode",
        choices=["dir", "file", "none"],
        default="dir",
        help="Create chapters per directory, per file, or not at all.",
    )
    parser.add_argument(
        "--extensions",
        default=",".join(sorted(ext.lstrip(".") for ext in DEFAULT_EXTENSIONS)),
        help="Comma-separated extensions to include.",
    )
    parser.add_argument("--files-out", default="files.txt", help="Concat list output file.")
    parser.add_argument("--meta-out", default="meta.txt", help="FFMETADATA output file.")
    parser.add_argument(
        "--ffmpeg-out",
        default="ffmpeg.sh",
        help="Output file for a ready-to-run ffmpeg command line.",
    )
    parser.add_argument(
        "--no-ffmpeg-out",
        action="store_true",
        help="Skip writing the ffmpeg command output file.",
    )
    parser.add_argument(
        "--output-m4b",
        default="book.m4b",
        help="Output M4B filename for the generated ffmpeg command (adds .m4b if missing).",
    )
    parser.add_argument(
        "--output-author",
        help="Author name for building a default output filename.",
    )
    parser.add_argument(
        "--output-title",
        help="Title for building a default output filename.",
    )
    parser.add_argument(
        "--name-order",
        choices=["last-first", "keep"],
        default="last-first",
        help="Reorder names to 'Last First' format when building output filename.",
    )
    parser.add_argument(
        "--audio-codec",
        default="aac",
        help="Audio codec for the generated ffmpeg command.",
    )
    parser.add_argument(
        "--audio-bitrate",
        default="96k",
        help="Audio bitrate for the generated ffmpeg command.",
    )
    parser.add_argument(
        "--audio-threads",
        default="0",
        help="Threads setting for the generated ffmpeg command.",
    )
    parser.add_argument(
        "--output-narrator",
        help="Narrator/performer name for the AtomicParsley command.",
    )
    parser.add_argument(
        "--atomicparsley-out",
        default="atomicparsley.sh",
        help="Output file for a ready-to-run AtomicParsley command line.",
    )
    parser.add_argument(
        "--no-atomicparsley-out",
        action="store_true",
        help="Skip writing the AtomicParsley command output file.",
    )
    parser.add_argument(
        "--cover-path",
        default="cover.jpg",
        help="Cover image path for the AtomicParsley command.",
    )

    args = parser.parse_args()
    root = Path(args.root).resolve()
    extensions = parse_extensions(args.extensions)

    files = collect_files(root, args.recursive, extensions)
    if not files:
        print("No matching audio files found.", file=sys.stderr)
        return 2

    files_out = Path(args.files_out)
    meta_out = Path(args.meta_out)
    ffmpeg_out = Path(args.ffmpeg_out)
    atomicparsley_out = Path(args.atomicparsley_out)
    cover_path = Path(args.cover_path)

    derived_author, derived_title, derived_narrator = derive_metadata_defaults(files, root)
    author = args.output_author or derived_author
    title = args.output_title or derived_title
    narrator = args.output_narrator or derived_narrator
    if args.name_order == "last-first":
        if author:
            author = reorder_name_list(author)
        if narrator:
            narrator = reorder_name_list(narrator)

    output_name = args.output_m4b
    if args.output_m4b == "book.m4b":
        output_name = build_output_name(author, title) or args.output_m4b
    if not output_name.lower().endswith(".m4b"):
        output_name = f"{output_name}.m4b"
    output_path = Path(output_name)
    output_m4b = output_path.with_name(sanitize_filename(output_path.name))

    try:
        write_concat_list(files, files_out)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    if args.chapter_mode == "none":
        if not args.no_ffmpeg_out:
            command = build_ffmpeg_command(
                files_out,
                meta_out,
                output_m4b,
                include_meta=False,
                audio_codec=args.audio_codec,
                bitrate=args.audio_bitrate,
                threads=args.audio_threads,
            )
            write_ffmpeg_command(command, ffmpeg_out)
        if not args.no_atomicparsley_out:
            cover = cover_path if cover_path.exists() else None
            command = build_atomicparsley_command(
                output_m4b,
                author,
                title,
                narrator,
                cover,
            )
            write_atomicparsley_command(command, atomicparsley_out)
        return 0

    try:
        chapters = build_chapters(files, root, args.chapter_mode)
    except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as exc:
        print("ffprobe failed; ensure ffmpeg/ffprobe are installed.", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError):
            print(exc.stderr, file=sys.stderr)
        else:
            print(str(exc), file=sys.stderr)
        return 4

    write_ffmetadata(chapters, meta_out)

    if not args.no_ffmpeg_out:
        command = build_ffmpeg_command(
            files_out,
            meta_out,
            output_m4b,
            include_meta=True,
            audio_codec=args.audio_codec,
            bitrate=args.audio_bitrate,
            threads=args.audio_threads,
        )
        write_ffmpeg_command(command, ffmpeg_out)
    if not args.no_atomicparsley_out:
        cover = cover_path if cover_path.exists() else None
        command = build_atomicparsley_command(
            output_m4b,
            author,
            title,
            narrator,
            cover,
        )
        write_atomicparsley_command(command, atomicparsley_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
