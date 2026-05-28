#!/usr/bin/env python3
"""Split video into chunks under a specified size limit."""

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path


def get_video_info(video_path: str) -> dict:
    """Get video duration and size using ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")

    data = json.loads(result.stdout)
    return {
        "duration": float(data["format"]["duration"]),
        "size": int(data["format"]["size"]),
        "bitrate": int(data["format"]["bit_rate"])
    }


def split_video(
    input_path: str,
    output_dir: str,
    max_size_mb: int = 200,
    output_prefix: str = None
) -> list[str]:
    """
    Split video into chunks under max_size_mb.

    Args:
        input_path: Path to input video file
        output_dir: Directory for output files
        max_size_mb: Maximum size per chunk in MB
        output_prefix: Prefix for output filenames (defaults to input filename)

    Returns:
        List of output file paths
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if output_prefix is None:
        output_prefix = input_path.stem

    # Get video info
    info = get_video_info(str(input_path))
    duration = info["duration"]
    file_size = info["size"]

    # Calculate number of parts needed
    max_size_bytes = max_size_mb * 1024 * 1024
    num_parts = math.ceil(file_size / max_size_bytes)

    # Add safety margin (30%) for variable bitrate sections
    num_parts = math.ceil(num_parts * 1.3)

    segment_duration = duration / num_parts

    print(f"Video duration: {duration:.1f}s ({duration/3600:.1f} hours)")
    print(f"File size: {file_size / (1024*1024):.1f} MB")
    print(f"Target max size: {max_size_mb} MB")
    print(f"Splitting into {num_parts} parts (~{segment_duration:.1f}s each)")

    output_files = []

    for i in range(num_parts):
        start_time = i * segment_duration
        output_file = output_dir / f"{output_prefix}_part{i+1:02d}.mp4"

        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output
            "-i", str(input_path),
            "-ss", str(start_time),
            "-t", str(segment_duration),
            "-c", "copy",  # Copy streams without re-encoding (fast)
            "-avoid_negative_ts", "make_zero",
            str(output_file)
        ]

        print(f"\nCreating part {i+1}/{num_parts}: {output_file.name}")
        print(f"  Start: {start_time:.1f}s, Duration: {segment_duration:.1f}s")

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: ffmpeg returned non-zero for part {i+1}")
            print(result.stderr[-500:] if result.stderr else "No error output")

        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"  Output size: {size_mb:.1f} MB")
            output_files.append(str(output_file))
        else:
            print(f"  Warning: Output file not created")

    return output_files


def main():
    parser = argparse.ArgumentParser(
        description="Split video into chunks under a specified size limit"
    )
    parser.add_argument("input", help="Input video file")
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory (default: same as input)",
        default=None
    )
    parser.add_argument(
        "-s", "--max-size",
        type=int,
        default=200,
        help="Maximum size per chunk in MB (default: 200)"
    )
    parser.add_argument(
        "-p", "--prefix",
        help="Output filename prefix (default: input filename)",
        default=None
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    output_dir = args.output_dir or input_path.parent

    try:
        output_files = split_video(
            str(input_path),
            str(output_dir),
            args.max_size,
            args.prefix
        )
        print(f"\n✅ Successfully created {len(output_files)} parts:")
        for f in output_files:
            print(f"  - {f}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
