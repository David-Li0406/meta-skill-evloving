#!/usr/bin/env python3
"""
Get directions between waypoints using Mapbox Directions API.

Usage:
    uv run get_directions.py "38.8977,-77.0365" "40.7484,-73.9857"
    uv run get_directions.py "38.8977,-77.0365" "39.9526,-75.1652" "40.7484,-73.9857" --profile driving-traffic
    uv run get_directions.py "38.8977,-77.0365" "40.7484,-73.9857" --steps --alternatives --json

Environment:
    MAPBOX_API_KEY must be set
"""

import argparse
import json
import os
import sys

from mapbox import Directions


def setup_credentials() -> None:
    """Map MAPBOX_API_KEY to MAPBOX_ACCESS_TOKEN for SDK."""
    os.environ["MAPBOX_ACCESS_TOKEN"] = os.environ.get("MAPBOX_API_KEY", "")


def get_directions(
    waypoints: list[tuple[float, float]],
    profile: str = "driving",
    steps: bool = False,
    alternatives: bool = False,
    geometries: str = "geojson",
) -> dict:
    """
    Get directions between waypoints.

    Args:
        waypoints: List of (latitude, longitude) tuples
        profile: Routing profile (driving, driving-traffic, walking, cycling)
        steps: Include turn-by-turn instructions
        alternatives: Request alternative routes
        geometries: Geometry format (geojson, polyline, polyline6)

    Returns:
        Dictionary with routes, distance, duration, and optionally steps
    """
    setup_credentials()
    directions = Directions()

    # Convert waypoints to GeoJSON features (SDK expects lng, lat order)
    features = [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
        for lat, lng in waypoints
    ]

    profile_map = {
        "driving": "mapbox/driving",
        "driving-traffic": "mapbox/driving-traffic",
        "walking": "mapbox/walking",
        "cycling": "mapbox/cycling",
    }
    full_profile = profile_map.get(profile, f"mapbox/{profile}")

    response = directions.directions(
        features,
        profile=full_profile,
        geometries=geometries,
        steps=steps,
        alternatives=alternatives,
    )

    if response.status_code != 200:
        raise RuntimeError(f"API error: {response.status_code} - {response.text}")

    data = response.geojson()
    routes = data.get("features", [])

    result: dict = {
        "waypoints": [{"latitude": lat, "longitude": lng} for lat, lng in waypoints],
        "profile": profile,
        "routes": [],
    }

    for i, route in enumerate(routes):
        props = route.get("properties", {})
        route_data: dict = {
            "index": i,
            "distance_meters": props.get("distance", 0),
            "distance_km": round(props.get("distance", 0) / 1000, 2),
            "duration_seconds": props.get("duration", 0),
            "duration_minutes": round(props.get("duration", 0) / 60, 1),
        }

        if steps and "legs" in props:
            route_data["legs"] = []
            for leg in props["legs"]:
                leg_data: dict = {
                    "distance_meters": leg.get("distance", 0),
                    "duration_seconds": leg.get("duration", 0),
                    "steps": [],
                }
                for step in leg.get("steps", []):
                    step_data = {
                        "instruction": step.get("maneuver", {}).get("instruction", ""),
                        "distance_meters": step.get("distance", 0),
                        "duration_seconds": step.get("duration", 0),
                        "maneuver_type": step.get("maneuver", {}).get("type", ""),
                        "maneuver_modifier": step.get("maneuver", {}).get("modifier", ""),
                    }
                    leg_data["steps"].append(step_data)
                route_data["legs"].append(leg_data)

        # Include geometry if geojson
        if geometries == "geojson":
            route_data["geometry"] = route.get("geometry")

        result["routes"].append(route_data)

    return result


def parse_coordinates(coord_str: str) -> tuple[float, float]:
    """Parse 'lat,lng' string into (latitude, longitude) tuple."""
    parts = coord_str.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: {coord_str}. Expected 'lat,lng'")
    return float(parts[0].strip()), float(parts[1].strip())


def main():
    parser = argparse.ArgumentParser(
        description="Get directions between waypoints using Mapbox API"
    )
    parser.add_argument(
        "waypoints",
        nargs="+",
        help="Waypoints as 'lat,lng' (minimum 2 required)",
    )
    parser.add_argument(
        "--profile",
        "-p",
        choices=["driving", "driving-traffic", "walking", "cycling"],
        default="driving",
        help="Routing profile (default: driving)",
    )
    parser.add_argument(
        "--steps",
        "-s",
        action="store_true",
        help="Include turn-by-turn instructions",
    )
    parser.add_argument(
        "--alternatives",
        "-a",
        action="store_true",
        help="Request alternative routes",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    if len(args.waypoints) < 2:
        print("Error: At least 2 waypoints required", file=sys.stderr)
        sys.exit(1)

    try:
        waypoints = [parse_coordinates(wp) for wp in args.waypoints]

        result = get_directions(
            waypoints=waypoints,
            profile=args.profile,
            steps=args.steps,
            alternatives=args.alternatives,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n=== Route Summary ===")
            print(f"Profile: {result['profile']}")
            print(f"Waypoints: {len(result['waypoints'])}")

            for route in result["routes"]:
                print(f"\n--- Route {route['index'] + 1} ---")
                print(f"Distance: {route['distance_km']} km")
                print(f"Duration: {route['duration_minutes']} min")

                if "legs" in route:
                    for leg_idx, leg in enumerate(route["legs"]):
                        print(f"\n  Leg {leg_idx + 1}:")
                        for step in leg["steps"][:5]:  # First 5 steps
                            print(f"    - {step['instruction']}")
                        if len(leg["steps"]) > 5:
                            print(f"    ... and {len(leg['steps']) - 5} more steps")

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
