#!/usr/bin/env python3
"""
Predict completion date using historical velocity.

Usage:
    python predict_completion.py \
      --remaining-waves 5 \
      --estimated-hours 120 \
      --velocity-db velocity-db.json \
      --team-size 2
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict


def load_velocity_db(db_path: Path) -> Dict:
    """Load velocity database from JSON file."""
    if not db_path.exists():
        print(f"Error: Velocity database not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(db_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading velocity database: {e}", file=sys.stderr)
        sys.exit(1)


def determine_confidence(wave_count: int) -> tuple:
    """Determine confidence level and buffer based on historical data."""
    if wave_count >= 15:
        return "HIGH", 1.0, "±1 day"
    elif wave_count >= 8:
        return "MEDIUM", 1.5, "±2 days"
    elif wave_count >= 5:
        return "LOW", 2.0, "±3 days"
    else:
        return "VERY_LOW", 3.0, "±5 days"


def predict_completion(
    remaining_waves: int,
    estimated_hours: float,
    team_velocity: float,
    team_size: int,
    hours_per_day: float = 8.0,
    start_date: datetime = None
) -> Dict:
    """Predict completion date based on velocity and team size."""

    # Adjust estimate by team velocity
    adjusted_hours = estimated_hours * team_velocity

    # Calculate person-hours
    person_hours = adjusted_hours / team_size if team_size > 0 else adjusted_hours

    # Calculate working days
    working_days = person_hours / hours_per_day

    # Use today if no start date provided
    if start_date is None:
        start_date = datetime.now()

    # Calculate completion date (accounting for weekends)
    days_added = 0
    current_date = start_date
    while days_added < working_days:
        current_date += timedelta(days=1)
        # Skip weekends
        if current_date.weekday() < 5:  # Monday=0, Friday=4
            days_added += 1

    return {
        "base_estimate": estimated_hours,
        "adjusted_estimate": round(adjusted_hours, 1),
        "velocity": team_velocity,
        "person_hours": round(person_hours, 1),
        "working_days": round(working_days, 1),
        "calendar_days": (current_date - start_date).days,
        "expected_completion": current_date.strftime("%Y-%m-%d")
    }


def main():
    parser = argparse.ArgumentParser(
        description="Predict completion date using historical velocity"
    )

    parser.add_argument("--remaining-waves", type=int, required=True,
                       help="Number of waves remaining")
    parser.add_argument("--estimated-hours", type=float, required=True,
                       help="Total estimated hours for remaining waves")
    parser.add_argument("--velocity-db", type=str, default="velocity-db.json",
                       help="Path to velocity database file")
    parser.add_argument("--team-size", type=int, default=1,
                       help="Number of developers on team")
    parser.add_argument("--hours-per-day", type=float, default=8.0,
                       help="Working hours per day (default: 8)")
    parser.add_argument("--start-date", type=str,
                       help="Start date (YYYY-MM-DD, default: today)")
    parser.add_argument("--format", type=str, default="text",
                       choices=["text", "json"],
                       help="Output format")

    args = parser.parse_args()

    # Load velocity database
    db_path = Path(args.velocity_db)
    velocity_db = load_velocity_db(db_path)

    # Get team velocity
    team_velocity = velocity_db.get("team_velocity", {}).get("average", 1.0)
    wave_count = len(velocity_db.get("waves", []))

    # Determine confidence level
    confidence, buffer_factor, buffer_desc = determine_confidence(wave_count)

    # Parse start date
    start_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format: {args.start_date}", file=sys.stderr)
            sys.exit(1)

    # Calculate prediction
    prediction = predict_completion(
        args.remaining_waves,
        args.estimated_hours,
        team_velocity,
        args.team_size,
        args.hours_per_day,
        start_date
    )

    # Add confidence and buffer
    prediction["confidence"] = confidence
    prediction["buffer_days"] = buffer_desc
    prediction["wave_count"] = wave_count

    # Output
    if args.format == "json":
        print(json.dumps(prediction, indent=2))
    else:
        print(f"Predictive Estimate:")
        print(f"")
        print(f"Remaining Waves: {args.remaining_waves}")
        print(f"Total Estimated Hours: {args.estimated_hours}")
        print(f"Team Velocity: {team_velocity}x")
        print(f"Adjusted Estimate: {prediction['adjusted_estimate']} hours")
        print(f"")
        print(f"Team Configuration:")
        print(f"  Team Size: {args.team_size} developer(s)")
        print(f"  Hours per Day: {args.hours_per_day}")
        print(f"  Person-Hours: {prediction['person_hours']}")
        print(f"")
        print(f"Timeline:")
        print(f"  Working Days: {prediction['working_days']}")
        print(f"  Calendar Days: {prediction['calendar_days']}")
        print(f"  Expected Completion: {prediction['expected_completion']} ({buffer_desc})")
        print(f"")
        print(f"Confidence: {confidence} (based on {wave_count} completed wave(s))")

        # Recommendations
        if confidence == "VERY_LOW":
            print(f"")
            print(f"⚠️  Low Confidence Warning:")
            print(f"   Need at least 5 completed waves for reliable predictions")
            print(f"   Current predictions have high uncertainty")
        elif confidence == "LOW":
            print(f"")
            print(f"⚠️  Moderate Confidence:")
            print(f"   Predictions will become more accurate with more completed waves")


if __name__ == "__main__":
    main()
