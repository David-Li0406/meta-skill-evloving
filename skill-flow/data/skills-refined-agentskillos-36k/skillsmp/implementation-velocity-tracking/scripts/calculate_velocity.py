#!/usr/bin/env python3
"""
Calculate velocity metrics from wave completion data.

Usage:
    python calculate_velocity.py --wave wave-5.1.1 --estimated 24 --actual 28
    python calculate_velocity.py --wave-data wave-data.json --velocity-db velocity-db.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def calculate_wave_velocity(estimated: float, actual: float) -> float:
    """Calculate velocity for a single wave."""
    if estimated == 0:
        return 0.0
    return round(actual / estimated, 2)


def calculate_team_velocity(velocities: List[float], window: int = 8) -> Dict:
    """Calculate rolling average team velocity."""
    if not velocities:
        return {"average": 0.0, "std_dev": 0.0, "count": 0}

    # Use last N waves for rolling average
    recent = velocities[-window:] if len(velocities) > window else velocities

    average = sum(recent) / len(recent)
    variance = sum((v - average) ** 2 for v in recent) / len(recent)
    std_dev = variance ** 0.5

    return {
        "average": round(average, 2),
        "std_dev": round(std_dev, 2),
        "count": len(recent),
        "window": window
    }


def determine_trend(velocities: List[float], window: int = 5) -> str:
    """Determine if velocity is improving, stable, or worsening."""
    if len(velocities) < window:
        return "insufficient_data"

    recent = velocities[-window:]
    older = velocities[-(window * 2):-window] if len(velocities) >= window * 2 else velocities[:-window]

    if not older:
        return "insufficient_data"

    recent_avg = sum(recent) / len(recent)
    older_avg = sum(older) / len(older)

    diff = abs(recent_avg - older_avg)

    # Improving = getting closer to 1.0
    target = 1.0
    recent_distance = abs(recent_avg - target)
    older_distance = abs(older_avg - target)

    if diff < 0.05:
        return "stable"
    elif recent_distance < older_distance:
        return "improving"
    else:
        return "worsening"


def load_velocity_db(db_path: Path) -> Dict:
    """Load velocity database from JSON file."""
    if not db_path.exists():
        return {"waves": [], "team_velocity": {"average": 0.0}}

    try:
        with open(db_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading velocity database: {e}", file=sys.stderr)
        return {"waves": [], "team_velocity": {"average": 0.0}}


def save_velocity_db(db_path: Path, data: Dict):
    """Save velocity database to JSON file."""
    try:
        with open(db_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving velocity database: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate velocity metrics from wave completion data"
    )

    # Option 1: Individual wave data
    parser.add_argument("--wave", type=str,
                       help="Wave ID (e.g., wave-5.1.1)")
    parser.add_argument("--estimated", type=float,
                       help="Estimated hours for wave")
    parser.add_argument("--actual", type=float,
                       help="Actual hours worked on wave")
    parser.add_argument("--defects", type=int, default=0,
                       help="Number of defects found")
    parser.add_argument("--coverage", type=float, default=0.0,
                       help="Test coverage percentage")
    parser.add_argument("--rework", type=float, default=0.0,
                       help="Rework hours")

    # Option 2: JSON input
    parser.add_argument("--wave-data", type=str,
                       help="Path to JSON file with wave data")

    # Velocity database
    parser.add_argument("--velocity-db", type=str, default="velocity-db.json",
                       help="Path to velocity database file")

    # Window size for rolling average
    parser.add_argument("--window", type=int, default=8,
                       help="Number of waves for rolling average (default: 8)")

    # Output format
    parser.add_argument("--format", type=str, default="text",
                       choices=["text", "json"],
                       help="Output format")

    args = parser.parse_args()

    # Load wave data
    if args.wave_data:
        try:
            with open(args.wave_data, 'r') as f:
                wave_data = json.load(f)
                wave_id = wave_data.get("wave")
                estimated = wave_data.get("estimated", 0)
                actual = wave_data.get("actual", 0)
                defects = wave_data.get("defects", 0)
                coverage = wave_data.get("coverage", 0.0)
                rework = wave_data.get("rework", 0.0)
        except Exception as e:
            print(f"Error loading wave data: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if not args.wave or args.estimated is None or args.actual is None:
            print("Error: Must specify --wave, --estimated, and --actual", file=sys.stderr)
            sys.exit(1)

        wave_id = args.wave
        estimated = args.estimated
        actual = args.actual
        defects = args.defects
        coverage = args.coverage
        rework = args.rework

    # Load velocity database
    db_path = Path(args.velocity_db)
    velocity_db = load_velocity_db(db_path)

    # Calculate wave velocity
    wave_velocity = calculate_wave_velocity(estimated, actual)

    # Calculate quality metrics
    rework_pct = (rework / actual * 100) if actual > 0 else 0.0

    # Add to database
    wave_entry = {
        "wave_id": wave_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "estimated_hours": estimated,
        "actual_hours": actual,
        "velocity": wave_velocity,
        "defects": defects,
        "coverage": coverage,
        "rework_hours": rework,
        "rework_percentage": round(rework_pct, 1)
    }

    velocity_db["waves"].append(wave_entry)

    # Calculate team velocity
    all_velocities = [w["velocity"] for w in velocity_db["waves"]]
    team_velocity = calculate_team_velocity(all_velocities, args.window)

    # Determine trend
    trend = determine_trend(all_velocities, window=5)

    # Calculate defect density trend
    recent_defects = [w["defects"] for w in velocity_db["waves"][-args.window:]]
    avg_defects = sum(recent_defects) / len(recent_defects) if recent_defects else 0.0

    # Calculate coverage trend
    recent_coverage = [w["coverage"] for w in velocity_db["waves"][-args.window:] if w["coverage"] > 0]
    avg_coverage = sum(recent_coverage) / len(recent_coverage) if recent_coverage else 0.0

    # Update database
    velocity_db["team_velocity"] = team_velocity
    velocity_db["trend"] = trend
    velocity_db["avg_defects_per_wave"] = round(avg_defects, 1)
    velocity_db["avg_coverage"] = round(avg_coverage, 1)
    velocity_db["last_updated"] = datetime.now().isoformat()

    # Save database
    save_velocity_db(db_path, velocity_db)

    # Output
    if args.format == "json":
        result = {
            "wave": wave_entry,
            "team_velocity": team_velocity,
            "trend": trend,
            "quality": {
                "avg_defects_per_wave": velocity_db["avg_defects_per_wave"],
                "avg_coverage": velocity_db["avg_coverage"]
            }
        }
        print(json.dumps(result, indent=2))
    else:
        variance_pct = (wave_velocity - 1.0) * 100

        print(f"Wave: {wave_id}")
        print(f"")
        print(f"Velocity Metrics:")
        print(f"  Estimated Hours: {estimated}")
        print(f"  Actual Hours: {actual}")
        print(f"  Wave Velocity: {wave_velocity} ({variance_pct:+.0f}%)")
        print(f"")
        print(f"Team Velocity (last {team_velocity['count']} waves):")
        print(f"  Average: {team_velocity['average']}")

        trend_symbol = {
            "improving": "↓",
            "stable": "→",
            "worsening": "↑",
            "insufficient_data": "?"
        }
        print(f"  Trend: {trend_symbol.get(trend, '?')} {trend.replace('_', ' ').title()}")
        print(f"  Standard Deviation: {team_velocity['std_dev']}")
        print(f"")
        print(f"Quality Metrics:")
        print(f"  Defects Found: {defects}")
        print(f"  Defect Density: {velocity_db['avg_defects_per_wave']} per wave")
        print(f"  Test Coverage: {coverage}%")
        print(f"  Avg Coverage: {velocity_db['avg_coverage']}%")
        print(f"  Rework: {rework} hours ({rework_pct:.0f}%)")
        print(f"")
        print(f"Updated Velocity Database: {db_path}")


if __name__ == "__main__":
    main()
