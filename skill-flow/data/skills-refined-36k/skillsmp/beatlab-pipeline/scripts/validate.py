#!/usr/bin/env python3
"""
BeatLab Beat JSON Validator & Normalizer

Usage:
    python3 validate.py <beat.json> [--inplace]

Exit codes:
    0 = valid
    1 = invalid (errors printed to stderr)
"""

import json
import sys
from typing import Any

ALLOWED_NOTES = ["C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4", "B3", "A3", "G3"]
ALLOWED_DRUMS = ["Kick", "Snare", "HiHat", "Clap", "OpenHat", "Tom", "Crash", "Ride", "Shaker", "Cowbell"]
VALID_STEPS = set(range(16))


def validate_and_normalize(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Validate and normalize beat JSON. Returns (normalized_data, errors)."""
    errors: list[str] = []

    # Check required keys
    if "pianoSequence" not in data:
        errors.append("Missing 'pianoSequence' key")
    if "drumSequence" not in data:
        errors.append("Missing 'drumSequence' key")

    if errors:
        return data, errors

    # Validate and normalize pianoSequence
    piano = data.get("pianoSequence", {})
    if not isinstance(piano, dict):
        errors.append("'pianoSequence' must be an object")
    else:
        # Check for invalid keys
        for key in piano.keys():
            if key not in ALLOWED_NOTES:
                errors.append(f"Invalid piano note: '{key}'. Allowed: {ALLOWED_NOTES}")

        # Normalize: ensure all allowed notes exist, validate steps
        normalized_piano = {}
        for note in ALLOWED_NOTES:
            steps = piano.get(note, [])
            if not isinstance(steps, list):
                errors.append(f"pianoSequence['{note}'] must be an array")
                normalized_piano[note] = []
            else:
                valid_steps = []
                for step in steps:
                    if not isinstance(step, int):
                        errors.append(f"pianoSequence['{note}'] contains non-integer: {step}")
                    elif step not in VALID_STEPS:
                        errors.append(f"pianoSequence['{note}'] contains invalid step: {step} (must be 0-15)")
                    else:
                        valid_steps.append(step)
                # Deduplicate and sort
                normalized_piano[note] = sorted(set(valid_steps))
        data["pianoSequence"] = normalized_piano

    # Validate and normalize drumSequence
    drums = data.get("drumSequence", {})
    if not isinstance(drums, dict):
        errors.append("'drumSequence' must be an object")
    else:
        # Check for invalid keys
        for key in drums.keys():
            if key not in ALLOWED_DRUMS:
                errors.append(f"Invalid drum sound: '{key}'. Allowed: {ALLOWED_DRUMS}")

        # Normalize: ensure all allowed drums exist, validate steps
        normalized_drums = {}
        for drum in ALLOWED_DRUMS:
            steps = drums.get(drum, [])
            if not isinstance(steps, list):
                errors.append(f"drumSequence['{drum}'] must be an array")
                normalized_drums[drum] = []
            else:
                valid_steps = []
                for step in steps:
                    if not isinstance(step, int):
                        errors.append(f"drumSequence['{drum}'] contains non-integer: {step}")
                    elif step not in VALID_STEPS:
                        errors.append(f"drumSequence['{drum}'] contains invalid step: {step} (must be 0-15)")
                    else:
                        valid_steps.append(step)
                # Deduplicate and sort
                normalized_drums[drum] = sorted(set(valid_steps))
        data["drumSequence"] = normalized_drums

    # Validate bpm if present
    if "bpm" in data:
        bpm = data["bpm"]
        if not isinstance(bpm, (int, float)):
            errors.append(f"'bpm' must be a number, got: {type(bpm).__name__}")
        elif not (30 <= bpm <= 300):
            errors.append(f"'bpm' should be between 30-300, got: {bpm}")

    # Validate swing if present
    if "swing" in data:
        swing = data["swing"]
        if not isinstance(swing, (int, float)):
            errors.append(f"'swing' must be a number, got: {type(swing).__name__}")
        elif not (0.0 <= swing <= 1.0):
            errors.append(f"'swing' should be between 0.0-1.0, got: {swing}")

    return data, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <beat.json> [--inplace]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    inplace = "--inplace" in sys.argv

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    normalized, errors = validate_and_normalize(data)

    if errors:
        print("Validation errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if inplace:
        with open(filepath, "w") as f:
            json.dump(normalized, f, indent=2)
        print(f"Validated and normalized: {filepath}")
    else:
        print(json.dumps(normalized, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
