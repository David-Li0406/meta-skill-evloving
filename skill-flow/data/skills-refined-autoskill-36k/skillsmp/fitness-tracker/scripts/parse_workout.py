# /// script
# requires-python = ">=3.9"
# dependencies = ["duckdb"]
# ///
# ABOUTME: Parses workout markdown files into CSV and supports DuckDB queries.
# ABOUTME: Usage: uv run parse_workout.py <input> [-o output.csv] [--query "SQL"]

import argparse
import csv
import difflib
import json
import re
import sys
from pathlib import Path


def load_exercises():
    """Load known exercises from reference/exercises.md."""
    script_dir = Path(__file__).parent
    exercises_path = script_dir.parent / "reference" / "exercises.md"

    exercises = []
    if exercises_path.exists():
        with open(exercises_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("- "):
                    exercises.append(line[2:].strip())
    return exercises


def validate_exercises(rows, known_exercises):
    """Check for unrecognized exercises and suggest matches."""
    if not known_exercises:
        return

    unique_exercises = set(row["exercise"] for row in rows)
    known_lower = {e.lower(): e for e in known_exercises}
    unrecognized = []

    for exercise in unique_exercises:
        if exercise.lower() not in known_lower:
            matches = difflib.get_close_matches(
                exercise.lower(),
                known_lower.keys(),
                n=1,
                cutoff=0.6
            )
            if matches:
                suggestion = known_lower[matches[0]]
                unrecognized.append(f"  '{exercise}' - did you mean '{suggestion}'?")
            else:
                unrecognized.append(f"  '{exercise}' - no close match found")

    if unrecognized:
        print("\nUnrecognized exercises:", file=sys.stderr)
        for msg in sorted(unrecognized):
            print(msg, file=sys.stderr)
        print(file=sys.stderr)


def load_config():
    """Load config from config.json in scripts directory."""
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"

    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def parse_duration(text):
    """Parse duration strings like '30m', '1h', '1h30m' into minutes."""
    text = text.strip().lower()
    total_minutes = 0

    hours_match = re.search(r'(\d+)h', text)
    mins_match = re.search(r'(\d+)m', text)

    if hours_match:
        total_minutes += int(hours_match.group(1)) * 60
    if mins_match:
        total_minutes += int(mins_match.group(1))

    return total_minutes if total_minutes > 0 else None


def parse_set_line(line, current_date, current_exercise, set_counter):
    """Parse a set line and return list of row dicts (one per set)."""
    rows = []

    # Extract comment if present
    notes = ""
    if "//" in line:
        line, notes = line.split("//", 1)
        notes = notes.strip()

    line = line.strip().lstrip("-").strip()

    # Check if it's a duration (e.g., "30m", "1h30m")
    if re.match(r'^[\d]+[hm]', line) or re.match(r'^\d+h\d+m$', line):
        duration = parse_duration(line)
        rows.append({
            "date": current_date,
            "exercise": current_exercise,
            "set_num": set_counter,
            "weight": "",
            "reps": "",
            "duration_min": duration,
            "notes": notes
        })
        return rows, set_counter + 1

    # Check for weight - reps pattern (e.g., "135 - 10, 10")
    weight_match = re.match(r'^(\d+(?:\.\d+)?)\s*-\s*(.+)$', line)
    if weight_match:
        weight = weight_match.group(1)
        reps_part = weight_match.group(2)
    else:
        weight = ""
        reps_part = line

    # Parse comma-separated reps
    reps_list = [r.strip() for r in reps_part.split(",") if r.strip()]

    for reps in reps_list:
        # Handle rep counts (could be just numbers)
        if reps.isdigit():
            rows.append({
                "date": current_date,
                "exercise": current_exercise,
                "set_num": set_counter,
                "weight": weight,
                "reps": int(reps),
                "duration_min": "",
                "notes": notes if set_counter == 1 or len(reps_list) == 1 else ""
            })
            set_counter += 1

    return rows, set_counter


def extract_date_from_filename(filepath):
    """Extract date from filename like 2026-01-02.md."""
    name = Path(filepath).stem
    if re.match(r'^\d{4}-\d{2}-\d{2}$', name):
        return name
    return None


def parse_workout_file(filepath):
    """Parse a workout markdown file and return list of row dicts."""
    rows = []
    current_date = extract_date_from_filename(filepath)
    current_exercise = None
    set_counter = 1

    with open(filepath, "r") as f:
        for line in f:
            line = line.rstrip()

            # Skip empty lines
            if not line.strip():
                continue

            # Date header: ## YYYY-MM-DD
            date_match = re.match(r'^##\s+(\d{4}-\d{2}-\d{2})', line)
            if date_match:
                current_date = date_match.group(1)
                current_exercise = None
                continue

            # Skip other headers
            if line.startswith("#"):
                continue

            # Set line (starts with -)
            if line.strip().startswith("-"):
                if current_date and current_exercise:
                    new_rows, set_counter = parse_set_line(
                        line, current_date, current_exercise, set_counter
                    )
                    rows.extend(new_rows)
                continue

            # Exercise name (non-empty line that doesn't start with - or #)
            if line.strip() and not line.strip().startswith("-"):
                current_exercise = line.strip()
                set_counter = 1

    return rows


def parse_workouts(input_path):
    """Parse workout file(s) from path (file or directory)."""
    input_path = Path(input_path)
    all_rows = []

    if input_path.is_file():
        all_rows.extend(parse_workout_file(input_path))
    elif input_path.is_dir():
        for md_file in sorted(input_path.glob("????-??-??.md")):
            all_rows.extend(parse_workout_file(md_file))
    else:
        raise FileNotFoundError(f"Path not found: {input_path}")

    return all_rows


def write_csv(rows, output_path):
    """Write rows to CSV file."""
    fieldnames = ["date", "exercise", "set_num", "weight", "reps", "duration_min", "notes"]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_csv(csv_path, new_rows):
    """Update CSV by replacing rows for dates in new_rows, keeping other dates."""
    fieldnames = ["date", "exercise", "set_num", "weight", "reps", "duration_min", "notes"]
    dates_to_replace = set(row["date"] for row in new_rows)

    existing = []
    csv_path = Path(csv_path)
    if csv_path.exists():
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            existing = [row for row in reader if row["date"] not in dates_to_replace]

    all_rows = existing + new_rows
    all_rows.sort(key=lambda r: (r["date"], r["exercise"], int(r["set_num"])))
    write_csv(all_rows, csv_path)


def run_query(csv_path, query):
    """Run a DuckDB query against the CSV file."""
    try:
        import duckdb
    except ImportError:
        print("Error: duckdb not installed. Run script with: uv run parse_workout.py", file=sys.stderr)
        sys.exit(1)

    # Replace 'workouts' table reference with the CSV file path
    query = query.replace("workouts", f"'{csv_path}'")

    result = duckdb.query(query)
    print(result)


def main():
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Parse workout markdown files into CSV and query with DuckDB"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=config.get("obsidian_workout_dir", ""),
        help="Workout markdown file or directory (default: from config.json)"
    )
    parser.add_argument(
        "-o", "--output",
        default="workouts.csv",
        help="Output CSV file (default: workouts.csv)"
    )
    parser.add_argument(
        "--append", "-a",
        action="store_true",
        help="Update existing CSV: replace rows for parsed dates, keep others"
    )
    parser.add_argument("--query", "-q", help="Run DuckDB query after parsing")

    args = parser.parse_args()

    if not args.input:
        print("Error: No input path provided. Set obsidian_workout_dir in config.json or pass as argument.", file=sys.stderr)
        sys.exit(1)

    # Load known exercises for validation
    known_exercises = load_exercises()

    # Parse workouts
    rows = parse_workouts(args.input)

    if not rows:
        print("No workout data found.", file=sys.stderr)
        sys.exit(1)

    # Validate exercise names
    validate_exercises(rows, known_exercises)

    # Write CSV
    if args.append:
        update_csv(args.output, rows)
        print(f"Updated {args.output} with {len(rows)} sets")
    else:
        write_csv(rows, args.output)
        print(f"Wrote {len(rows)} sets to {args.output}")

    # Run query if provided
    if args.query:
        print()
        run_query(args.output, args.query)


if __name__ == "__main__":
    main()
