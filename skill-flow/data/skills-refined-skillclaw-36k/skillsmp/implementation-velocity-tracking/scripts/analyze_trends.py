#!/usr/bin/env python3
"""
Analyze quality and velocity trends from historical data.

Usage:
    python analyze_trends.py \
      --velocity-db velocity-db.json \
      --metrics defect-density,coverage,velocity \
      --period 30
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


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


def filter_by_period(waves: List[Dict], days: int) -> List[Dict]:
    """Filter waves to those within the last N days."""
    if days == 0:
        return waves

    cutoff = datetime.now() - timedelta(days=days)

    filtered = []
    for wave in waves:
        try:
            wave_date = datetime.strptime(wave["date"], "%Y-%m-%d")
            if wave_date >= cutoff:
                filtered.append(wave)
        except (KeyError, ValueError):
            # Skip waves without valid date
            continue

    return filtered


def analyze_defect_trend(waves: List[Dict]) -> Dict:
    """Analyze defect density trend."""
    if not waves:
        return {"trend": "no_data", "current": 0, "previous": 0}

    # Split into two halves
    mid = len(waves) // 2
    if mid == 0:
        return {"trend": "insufficient_data", "current": 0, "previous": 0}

    older = waves[:mid]
    recent = waves[mid:]

    older_avg = sum(w.get("defects", 0) for w in older) / len(older)
    recent_avg = sum(w.get("defects", 0) for w in recent) / len(recent)

    # Determine trend
    diff = recent_avg - older_avg
    if abs(diff) < 0.5:
        trend = "stable"
    elif diff < 0:
        trend = "improving"
    else:
        trend = "worsening"

    return {
        "trend": trend,
        "current": round(recent_avg, 1),
        "previous": round(older_avg, 1),
        "change": round(diff, 1)
    }


def analyze_coverage_trend(waves: List[Dict]) -> Dict:
    """Analyze test coverage trend."""
    # Filter waves with coverage data
    with_coverage = [w for w in waves if w.get("coverage", 0) > 0]

    if not with_coverage:
        return {"trend": "no_data", "current": 0, "previous": 0}

    # Split into two halves
    mid = len(with_coverage) // 2
    if mid == 0:
        return {"trend": "insufficient_data", "current": 0, "previous": 0}

    older = with_coverage[:mid]
    recent = with_coverage[mid:]

    older_avg = sum(w["coverage"] for w in older) / len(older)
    recent_avg = sum(w["coverage"] for w in recent) / len(recent)

    # Determine trend
    diff = recent_avg - older_avg
    if abs(diff) < 2.0:
        trend = "stable"
    elif diff > 0:
        trend = "improving"
    else:
        trend = "worsening"

    return {
        "trend": trend,
        "current": round(recent_avg, 1),
        "previous": round(older_avg, 1),
        "change": round(diff, 1)
    }


def analyze_velocity_trend(waves: List[Dict]) -> Dict:
    """Analyze velocity trend."""
    if not waves:
        return {"trend": "no_data", "current": 0, "previous": 0}

    # Split into two halves
    mid = len(waves) // 2
    if mid == 0:
        return {"trend": "insufficient_data", "current": 0, "previous": 0}

    older = waves[:mid]
    recent = waves[mid:]

    older_avg = sum(w.get("velocity", 1.0) for w in older) / len(older)
    recent_avg = sum(w.get("velocity", 1.0) for w in recent) / len(recent)

    # Determine trend (closer to 1.0 is better)
    target = 1.0
    older_distance = abs(older_avg - target)
    recent_distance = abs(recent_avg - target)

    diff = recent_distance - older_distance

    if abs(diff) < 0.05:
        trend = "stable"
    elif diff < 0:
        trend = "improving"
    else:
        trend = "worsening"

    return {
        "trend": trend,
        "current": round(recent_avg, 2),
        "previous": round(older_avg, 2),
        "change": round(recent_avg - older_avg, 2)
    }


def identify_outliers(waves: List[Dict], metric: str, threshold: float = 2.0) -> List[Dict]:
    """Identify waves that are outliers for a given metric."""
    if not waves:
        return []

    values = [w.get(metric, 0) for w in waves]
    if not values:
        return []

    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    std_dev = variance ** 0.5

    outliers = []
    for wave in waves:
        value = wave.get(metric, 0)
        z_score = (value - avg) / std_dev if std_dev > 0 else 0

        if abs(z_score) > threshold:
            outliers.append({
                "wave_id": wave["wave_id"],
                "value": value,
                "avg": round(avg, 1),
                "z_score": round(z_score, 1)
            })

    return outliers


def main():
    parser = argparse.ArgumentParser(
        description="Analyze quality and velocity trends"
    )

    parser.add_argument("--velocity-db", type=str, default="velocity-db.json",
                       help="Path to velocity database file")
    parser.add_argument("--metrics", type=str, default="all",
                       help="Comma-separated metrics to analyze (defect-density,coverage,velocity,all)")
    parser.add_argument("--period", type=int, default=0,
                       help="Analyze last N days (0 = all data)")
    parser.add_argument("--find-outliers", action="store_true",
                       help="Identify outlier waves")
    parser.add_argument("--format", type=str, default="text",
                       choices=["text", "json"],
                       help="Output format")

    args = parser.parse_args()

    # Load velocity database
    db_path = Path(args.velocity_db)
    velocity_db = load_velocity_db(db_path)

    # Filter waves by period
    waves = filter_by_period(velocity_db.get("waves", []), args.period)

    if not waves:
        print("No wave data found in specified period", file=sys.stderr)
        sys.exit(1)

    # Parse metrics
    if args.metrics == "all":
        metrics_to_analyze = ["defect-density", "coverage", "velocity"]
    else:
        metrics_to_analyze = [m.strip() for m in args.metrics.split(",")]

    # Analyze trends
    trends = {}

    if "defect-density" in metrics_to_analyze:
        trends["defect_density"] = analyze_defect_trend(waves)

    if "coverage" in metrics_to_analyze:
        trends["coverage"] = analyze_coverage_trend(waves)

    if "velocity" in metrics_to_analyze:
        trends["velocity"] = analyze_velocity_trend(waves)

    # Find outliers
    outliers = {}
    if args.find_outliers:
        if "defect-density" in metrics_to_analyze:
            outliers["defect_outliers"] = identify_outliers(waves, "defects")
        if "velocity" in metrics_to_analyze:
            outliers["velocity_outliers"] = identify_outliers(waves, "velocity")

    # Output
    if args.format == "json":
        result = {
            "period_days": args.period,
            "waves_analyzed": len(waves),
            "trends": trends,
            "outliers": outliers
        }
        print(json.dumps(result, indent=2))
    else:
        period_str = f"Last {args.period} Days" if args.period > 0 else "All Time"
        print(f"Quality Trends ({period_str}):")
        print(f"Waves Analyzed: {len(waves)}")
        print(f"")

        trend_symbols = {
            "improving": "📈 IMPROVING",
            "stable": "→ STABLE",
            "worsening": "📉 WORSENING",
            "no_data": "❓ NO DATA",
            "insufficient_data": "⚠️ INSUFFICIENT DATA"
        }

        if "defect_density" in trends:
            dt = trends["defect_density"]
            symbol = trend_symbols.get(dt["trend"], "?")
            print(f"Defect Density:")
            print(f"  {symbol}: {dt['previous']} → {dt['current']} per wave")
            if dt["trend"] in ["improving", "worsening"]:
                print(f"  Change: {dt['change']:+.1f}")
            print(f"")

        if "coverage" in trends:
            ct = trends["coverage"]
            symbol = trend_symbols.get(ct["trend"], "?")
            print(f"Test Coverage:")
            print(f"  {symbol}: {ct['previous']}% → {ct['current']}%")
            if ct["trend"] in ["improving", "worsening"]:
                print(f"  Change: {ct['change']:+.1f}%")
            print(f"")

        if "velocity" in trends:
            vt = trends["velocity"]
            symbol = trend_symbols.get(vt["trend"], "?")
            print(f"Velocity:")
            print(f"  {symbol}: {vt['previous']} → {vt['current']}")
            if vt["trend"] in ["improving", "worsening"]:
                print(f"  Change: {vt['change']:+.2f}")

            if vt["current"] > 1.15:
                print(f"  ⚠️  Recommendation: Adjust estimates by {vt['current']}x")
            elif vt["current"] < 0.85:
                print(f"  ⚠️  Recommendation: Review if estimates too conservative")
            print(f"")

        # Print outliers
        if args.find_outliers and outliers:
            print(f"Outliers:")
            print(f"")

            if "defect_outliers" in outliers and outliers["defect_outliers"]:
                print(f"  Defect Outliers (>2 std dev):")
                for outlier in outliers["defect_outliers"]:
                    print(f"    - {outlier['wave_id']}: {outlier['value']} defects (avg: {outlier['avg']})")
                print(f"")

            if "velocity_outliers" in outliers and outliers["velocity_outliers"]:
                print(f"  Velocity Outliers (>2 std dev):")
                for outlier in outliers["velocity_outliers"]:
                    print(f"    - {outlier['wave_id']}: {outlier['value']} (avg: {outlier['avg']})")
                print(f"")


if __name__ == "__main__":
    main()
