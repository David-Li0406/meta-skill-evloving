#!/usr/bin/env python3
"""
Optimize multi-stop routes using Mapbox Optimization API v1.

Usage:
    uv run optimize_route.py "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652"
    uv run optimize_route.py "38.8977,-77.0365" "40.7484,-73.9857" --no-roundtrip
    uv run optimize_route.py "38.8977,-77.0365" "40.7484,-73.9857" "39.9526,-75.1652" --steps --json

Environment:
    MAPBOX_API_KEY must be set
"""

import argparse
import json
import os
import sys

import httpx


def get_access_token() -> str:
    """Get Mapbox access token from environment."""
    token = os.environ.get("MAPBOX_API_KEY", "")
    if not token:
        raise RuntimeError("MAPBOX_API_KEY environment variable not set")
    return token


def optimize_route(
    locations: list[tuple[float, float]],
    roundtrip: bool = True,
    source: str = "first",
    destination: str = "last",
    profile: str = "driving",
    steps: bool = False,
    geometries: str = "geojson",
) -> dict:
    """
    Optimize a multi-stop route using Optimization API v1.

    Args:
        locations: List of (latitude, longitude) tuples. First is start point.
        roundtrip: Return to starting location (default: True)
        source: Which coordinate is the start - "first", "last", or "any"
        destination: Which coordinate is the end - "first", "last", or "any"
        profile: Routing profile (driving, driving-traffic, walking, cycling)
        steps: Include turn-by-turn instructions
        geometries: Geometry format (geojson, polyline, polyline6)

    Returns:
        Dictionary with optimized route, waypoint order, distances, and durations
    """
    access_token = get_access_token()

    # Build coordinates string (API expects lng,lat order, semicolon-separated)
    coords_str = ";".join(f"{lng},{lat}" for lat, lng in locations)

    # Build profile string
    profile_map = {
        "driving": "mapbox/driving",
        "driving-traffic": "mapbox/driving-traffic",
        "walking": "mapbox/walking",
        "cycling": "mapbox/cycling",
    }
    full_profile = profile_map.get(profile, f"mapbox/{profile}")

    # Build URL with query parameters
    base_url = f"https://api.mapbox.com/optimized-trips/v1/{full_profile}/{coords_str}"

    params = {
        "access_token": access_token,
        "roundtrip": str(roundtrip).lower(),
        "source": source,
        "destination": destination,
        "geometries": geometries,
        "overview": "full",
    }

    if steps:
        params["steps"] = "true"

    try:
        response = httpx.get(base_url, params=params, timeout=30.0)
        response.raise_for_status()
    except httpx.TimeoutException:
        raise RuntimeError("Request timed out")
    except httpx.HTTPStatusError as e:
        error_detail: str | dict = ""
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = e.response.text
        raise RuntimeError(f"API error {e.response.status_code}: {error_detail}")

    data = response.json()

    # Check for API-level errors
    if data.get("code") != "Ok":
        raise RuntimeError(f"Optimization failed: {data.get('code')} - {data.get('message', '')}")

    if "trips" not in data or not data["trips"]:
        raise RuntimeError(f"No trips returned: {data}")

    trip = data["trips"][0]
    waypoints = data.get("waypoints", [])

    result: dict = {
        "input_locations": [
            {"index": i, "latitude": lat, "longitude": lng}
            for i, (lat, lng) in enumerate(locations)
        ],
        "roundtrip": roundtrip,
        "profile": profile,
        "total_distance_meters": trip.get("distance", 0),
        "total_distance_km": round(trip.get("distance", 0) / 1000, 2),
        "total_duration_seconds": trip.get("duration", 0),
        "total_duration_minutes": round(trip.get("duration", 0) / 60, 1),
        "optimized_order": [],
        "geometry": trip.get("geometry") if geometries == "geojson" else None,
    }

    # Extract optimized waypoint order
    for wp in waypoints:
        wp_idx = wp.get("waypoint_index", 0)
        orig_idx = waypoints.index(wp)  # Original input index
        # Find which input location this waypoint corresponds to
        wp_loc = wp.get("location", [0, 0])
        result["optimized_order"].append(
            {
                "stop_number": wp_idx,
                "original_index": orig_idx,
                "name": wp.get("name", ""),
                "longitude": wp_loc[0],
                "latitude": wp_loc[1],
            }
        )

    # Sort by optimized order
    result["optimized_order"].sort(key=lambda x: x["stop_number"])

    # Include legs if steps were requested
    if steps and "legs" in trip:
        result["legs"] = []
        for leg in trip["legs"]:
            leg_data: dict = {
                "distance_meters": leg.get("distance", 0),
                "duration_seconds": leg.get("duration", 0),
                "summary": leg.get("summary", ""),
            }
            if "steps" in leg:
                leg_data["steps"] = [
                    {
                        "instruction": step.get("maneuver", {}).get("instruction", ""),
                        "distance_meters": step.get("distance", 0),
                        "duration_seconds": step.get("duration", 0),
                    }
                    for step in leg["steps"]
                ]
            result["legs"].append(leg_data)

    return result


def parse_coordinates(coord_str: str) -> tuple[float, float]:
    """Parse 'lat,lng' string into (latitude, longitude) tuple."""
    parts = coord_str.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: {coord_str}. Expected 'lat,lng'")
    return float(parts[0].strip()), float(parts[1].strip())


def main():
    parser = argparse.ArgumentParser(
        description="Optimize multi-stop routes using Mapbox Optimization API"
    )
    parser.add_argument(
        "locations",
        nargs="+",
        help="Locations as 'lat,lng' (2-12 coordinates). First is start point.",
    )
    parser.add_argument(
        "--roundtrip",
        action="store_true",
        default=True,
        help="Return to starting location (default: True)",
    )
    parser.add_argument(
        "--no-roundtrip",
        action="store_true",
        help="Do not return to starting location",
    )
    parser.add_argument(
        "--source",
        choices=["first", "last", "any"],
        default="first",
        help="Which coordinate is the start (default: first)",
    )
    parser.add_argument(
        "--destination",
        choices=["first", "last", "any"],
        default="last",
        help="Which coordinate is the end (default: last)",
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
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    if len(args.locations) < 2:
        print("Error: At least 2 locations required", file=sys.stderr)
        sys.exit(1)

    if len(args.locations) > 12:
        print("Error: Maximum 12 locations allowed", file=sys.stderr)
        sys.exit(1)

    try:
        locations = [parse_coordinates(loc) for loc in args.locations]
        roundtrip = not args.no_roundtrip

        result = optimize_route(
            locations=locations,
            roundtrip=roundtrip,
            source=args.source,
            destination=args.destination,
            profile=args.profile,
            steps=args.steps,
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n=== Optimization Summary ===")
            print(f"Profile: {result['profile']}")
            print(f"Roundtrip: {result['roundtrip']}")
            print(f"Total Distance: {result['total_distance_km']} km")
            print(f"Total Duration: {result['total_duration_minutes']} min")

            print("\n--- Optimized Stop Order ---")
            for stop in result["optimized_order"]:
                orig_idx = stop["original_index"]
                stop_num = stop["stop_number"]
                name = stop["name"] or f"({stop['latitude']:.4f}, {stop['longitude']:.4f})"
                print(f"  {stop_num + 1}. [Input #{orig_idx}] {name}")

            if "legs" in result:
                print("\n--- Route Legs ---")
                for i, leg in enumerate(result["legs"]):
                    dist_km = round(leg["distance_meters"] / 1000, 2)
                    dur_min = round(leg["duration_seconds"] / 60, 1)
                    print(f"  Leg {i + 1}: {dist_km} km, {dur_min} min")
                    if "steps" in leg:
                        for step in leg["steps"][:3]:
                            print(f"    - {step['instruction']}")
                        if len(leg["steps"]) > 3:
                            print(f"    ... and {len(leg['steps']) - 3} more steps")

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
