#!/usr/bin/env python3
"""
BeatLab ASCII Grid Renderer

Usage:
    python3 render_grid.py <beat.json>

Outputs a 16-step ASCII grid to stdout.
"""

import json
import sys

ALLOWED_NOTES = ["C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "B3", "A3", "G3"]
ALLOWED_DRUMS = ["Kick", "Snare", "HiHat", "Clap", "OpenHat", "Tom", "Crash", "Ride", "Shaker", "Cowbell"]


def render_grid(data: dict) -> str:
    """Render beat data as ASCII grid."""
    lines = []

    # Header
    bpm = data.get("bpm", "?")
    swing = data.get("swing", 0)
    lines.append(f"BPM: {bpm}  Swing: {swing}")
    lines.append("")

    # Step numbers header
    step_header = "            |" + "|".join(f"{i:2}" for i in range(16)) + "|"
    lines.append(step_header)

    # Separator
    separator = "------------+" + "+".join(["--"] * 16) + "+"
    lines.append(separator)

    # Drums section
    drum_seq = data.get("drumSequence", {})
    for drum in ALLOWED_DRUMS:
        steps = set(drum_seq.get(drum, []))
        row = f"{drum:11} |" + "|".join(" X" if i in steps else "  " for i in range(16)) + "|"
        lines.append(row)

    # Separator between drums and piano
    lines.append(separator)

    # Piano section
    piano_seq = data.get("pianoSequence", {})
    for note in ALLOWED_NOTES:
        steps = set(piano_seq.get(note, []))
        row = f"{note:11} |" + "|".join(" O" if i in steps else "  " for i in range(16)) + "|"
        lines.append(row)

    lines.append(separator)

    # Beat markers (1-based for readability)
    beat_row = "Beat        |" + "|".join(f"{(i//4)+1} " if i % 4 == 0 else "  " for i in range(16)) + "|"
    lines.append(beat_row)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 render_grid.py <beat.json>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    grid = render_grid(data)
    print(grid)


if __name__ == "__main__":
    main()
