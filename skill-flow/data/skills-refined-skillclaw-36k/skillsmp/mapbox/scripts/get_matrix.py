#!/usr/bin/env python3
"""
Calculate distance/duration matrix using Mapbox Matrix API.

Usage:
    uv run get_matrix.py "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652"
    uv run get_matrix.py "38.8977,-77.0365" "40.7484,-73.9857" --sources 0 --destinations 1
    uv run get_matrix.py "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652" --profile walking --json

Environment:
    MAPBOX_API_KEY must be set
"""

import argparse
import json
import os
import sys

from mapbox import DirectionsMatrix


def setup_credentials() -> None:
    """Map MAPBOX_API_KEY to MAPBOX_ACCESS_TOKEN for SDK."""
    os.environ["MAPBOX_ACCESS_TOKEN"] = os.environ.get("MAPBOX_API_KEY", "")


def get_matrix(
    locations: list[tuple[float, float]],
    profile: str = "driving",
    sources: list[int] | None = None,
    destinations: list[int] | None = None,
) -> dict:
    """
    Calculate distance/duration matrix between locations.

    Args:
        locations: List of (latitude, longitude) tuples
        profile: Routing profile (driving, driving-traffic, walking, cycling)
        sources: Indices of source locations (default: all)
        destinations: Indices of destination locations (default: all)

    Returns:
        Dictionary with durations and distances matrices
    """
    setup_credentials()
    matrix = DirectionsMatrix()

    # Convert to GeoJSON features (SDK expects lng, lat order)
    features = [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
        for lat, lng in locations
    ]

    profile_map = {
        "driving": "mapbox/driving",
        "driving-traffic": "mapbox/driving-traffic",
        "walking": "mapbox/walking",
        "cycling": "mapbox/cycling",
    }
    full_profile = profile_map.get(profile, f"mapbox/{profile}")

    kwargs: dict = {"profile": full_profile}
    if sources is not None:
        kwargs["sources"] = sources
    if destinations is not None:
        kwargs["destinations"] = destinations

    response = matrix.matrix(features, **kwargs)

    if response.status_code != 200:
        raise RuntimeError(f"API error: {response.status_code} - {response.text}")

    data = response.json()

    # Determine effective sources and destinations
    effective_sources = sources if sources is not None else list(range(len(locations)))
    effective_destinations = (
        destinations if destinations is not None else list(range(len(locations)))
    )

    result: dict = {
        "locations": [
            {"latitude": lat, "longitude": lng, "index": i}
            for i, (lat, lng) in enumerate(locations)
        ],
        "profile": profile,
        "sources": effective_sources,
        "destinations": effective_destinations,
        "durations": [],
        "distances": [],
    }

    # Process durations (in seconds)
    raw_durations = data.get("durations", [])
    for i, src_idx in enumerate(effective_sources):
        row = []
        for j, dst_idx in enumerate(effective_destinations):
            duration = raw_durations[i][j] if raw_durations and i < len(raw_durations) else None
            row.append(
                {
                    "from": src_idx,
                    "to": dst_idx,
                    "duration_seconds": duration,
                    "duration_minutes": round(duration / 60, 1) if duration is not None else None,
                }
            )
        result["durations"].append(row)

    # Process distances (in meters) if available
    raw_distances = data.get("distances", [])
    for i, src_idx in enumerate(effective_sources):
        row = []
        for j, dst_idx in enumerate(effective_destinations):
            distance = (
                raw_distances[i][j] if raw_distances and i < len(raw_distances) else None
            )
            row.append(
                {
                    "from": src_idx,
                    "to": dst_idx,
                    "distance_meters": distance,
                    "distance_km": round(distance / 1000, 2) if distance is not None else None,
                }
            )
        result["distances"].append(row)

    return result


def parse_coordinates(coord_str: str) -> tuple[float, float]:
    """Parse 'lat,lng' string into (latitude, longitude) tuple."""
    parts = coord_str.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: {coord_str}. Expected 'lat,lng'")
    return float(parts[0].strip()), float(parts[1].strip())


def parse_indices(indices_str: str) -> list[int]:
    """Parse comma-separated indices string into list of integers."""
    return [int(x.strip()) for x in indices_str.split(",")]


def main():
    parser = argparse.ArgumentParser(
        description="Calculate distance/duration matrix using Mapbox API"
    )
    parser.add_argument(
        "locations",
        nargs="+",
        help="Locations as 'lat,lng' (minimum 2 required)",
    )
    parser.add_argument(
        "--profile",
        "-p",
        choices=["driving", "driving-traffic", "walking", "cycling"],
        default="driving",
        help="Routing profile (default: driving)",
    )
    parser.add_argument(
        "--sources",
        "-s",
        help="Source location indices (comma-separated, e.g., '0,1')",
    )
    parser.add_argument(
        "--destinations",
        "-d",
        help="Destination location indices (comma-separated, e.g., '2,3')",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    if len(args.locations) < 2:
        print("Error: At least 2 locations required", file=sys.stderr)
        sys.exit(1)

    try:
        locations = [parse_coordinates(loc) for loc in args.locations]
        sources = parse_indices(args.sources) if args.sources else None
        destinations = parse_indices(args.destinations) if args.destinations else None

        result = get_matrix(
            locations=locations,
            profile=args.profile,
            sources=sources,
            destinations=destinations,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n=== Matrix Summary ===")
            print(f"Profile: {result['profile']}")
            print(f"Locations: {len(result['locations'])}")

            print("\n--- Duration Matrix (minutes) ---")
            header = "From\\To  " + "  ".join(f"{d:>6}" for d in result["destinations"])
            print(header)
            for i, row in enumerate(result["durations"]):
                src = result["sources"][i]
                values = "  ".join(
                    f"{cell['duration_minutes']:>6.1f}"
                    if cell["duration_minutes"] is not None
                    else "  null"
                    for cell in row
                )
                print(f"   {src:>3}   {values}")

            if result["distances"] and result["distances"][0][0]["distance_meters"] is not None:
                print("\n--- Distance Matrix (km) ---")
                for i, row in enumerate(result["distances"]):
                    src = result["sources"][i]
                    values = "  ".join(
                        f"{cell['distance_km']:>6.1f}" if cell["distance_km"] is not None else "  null"
                        for cell in row
                    )
                    print(f"   {src:>3}   {values}")

    except ValueError as e:
        print(f"Input error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
