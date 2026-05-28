#!/usr/bin/env python3
"""
Geocoding using Mapbox API - forward (address to coords) and reverse (coords to address).

Usage:
    uv run geocode.py "1600 Pennsylvania Ave NW, Washington, DC"
    uv run geocode.py --reverse "38.8977,-77.0365"
    uv run geocode.py "Paris" --country fr --types place --limit 3 --json

Environment:
    MAPBOX_API_KEY must be set
"""

import argparse
import json
import os
import sys

from mapbox import Geocoder


def setup_credentials() -> None:
    """Map MAPBOX_API_KEY to MAPBOX_ACCESS_TOKEN for SDK."""
    os.environ["MAPBOX_ACCESS_TOKEN"] = os.environ.get("MAPBOX_API_KEY", "")


def geocode_forward(
    query: str,
    country: list[str] | None = None,
    types: list[str] | None = None,
    limit: int = 5,
    bbox: tuple[float, float, float, float] | None = None,
) -> list[dict]:
    """
    Forward geocode an address to coordinates.

    Args:
        query: Address or place name to geocode
        country: ISO 3166-1 alpha-2 country codes to filter results
        types: Feature types to filter (address, poi, place, etc.)
        limit: Maximum number of results (1-10)
        bbox: Bounding box (min_lng, min_lat, max_lng, max_lat)

    Returns:
        List of geocoding results with coordinates and metadata
    """
    setup_credentials()
    geocoder = Geocoder()

    kwargs: dict = {"limit": min(limit, 10)}
    if country:
        kwargs["country"] = country
    if types:
        kwargs["types"] = types
    if bbox:
        kwargs["bbox"] = list(bbox)

    response = geocoder.forward(query, **kwargs)

    if response.status_code != 200:
        raise RuntimeError(f"API error: {response.status_code} - {response.text}")

    features = response.geojson().get("features", [])

    results = []
    for feature in features:
        lng, lat = feature["geometry"]["coordinates"]
        results.append(
            {
                "place_name": feature.get("place_name", ""),
                "latitude": lat,
                "longitude": lng,
                "relevance": feature.get("relevance", 0),
                "type": feature.get("place_type", []),
                "context": [
                    {"type": c.get("id", "").split(".")[0], "text": c.get("text", "")}
                    for c in feature.get("context", [])
                ],
            }
        )

    return results


def geocode_reverse(
    latitude: float,
    longitude: float,
    types: list[str] | None = None,
    limit: int = 1,
) -> list[dict]:
    """
    Reverse geocode coordinates to an address.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        types: Feature types to filter
        limit: Maximum number of results

    Returns:
        List of reverse geocoding results with addresses
    """
    setup_credentials()
    geocoder = Geocoder()

    kwargs: dict = {}
    if types:
        kwargs["types"] = types
        kwargs["limit"] = min(limit, 5)  # limit only works with types specified

    response = geocoder.reverse(lon=longitude, lat=latitude, **kwargs)

    if response.status_code != 200:
        raise RuntimeError(f"API error: {response.status_code} - {response.text}")

    features = response.geojson().get("features", [])

    results = []
    for feature in features:
        lng, lat = feature["geometry"]["coordinates"]
        results.append(
            {
                "place_name": feature.get("place_name", ""),
                "latitude": lat,
                "longitude": lng,
                "type": feature.get("place_type", []),
                "address": feature.get("address", ""),
                "context": [
                    {"type": c.get("id", "").split(".")[0], "text": c.get("text", "")}
                    for c in feature.get("context", [])
                ],
            }
        )

    return results


def parse_coordinates(coord_str: str) -> tuple[float, float]:
    """Parse 'lat,lng' string into (latitude, longitude) tuple."""
    parts = coord_str.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: {coord_str}. Expected 'lat,lng'")
    return float(parts[0].strip()), float(parts[1].strip())


def main():
    parser = argparse.ArgumentParser(
        description="Geocode addresses to coordinates or reverse geocode coordinates to addresses"
    )
    parser.add_argument(
        "query",
        help="Address to geocode, or coordinates for reverse ('lat,lng')",
    )
    parser.add_argument(
        "--reverse",
        "-r",
        action="store_true",
        help="Reverse geocode (query should be 'lat,lng')",
    )
    parser.add_argument(
        "--country",
        "-c",
        nargs="+",
        help="Filter by country codes (e.g., us ca)",
    )
    parser.add_argument(
        "--types",
        "-t",
        nargs="+",
        help="Filter by feature types (address, poi, place, region, country)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=5,
        help="Maximum results (default: 5)",
    )
    parser.add_argument(
        "--bbox",
        help="Bounding box: 'min_lng,min_lat,max_lng,max_lat'",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    try:
        if args.reverse:
            lat, lng = parse_coordinates(args.query)
            results = geocode_reverse(
                latitude=lat,
                longitude=lng,
                types=args.types,
                limit=args.limit,
            )
        else:
            bbox = None
            if args.bbox:
                bbox_parts = [float(x.strip()) for x in args.bbox.split(",")]
                if len(bbox_parts) == 4:
                    bbox = (bbox_parts[0], bbox_parts[1], bbox_parts[2], bbox_parts[3])

            results = geocode_forward(
                query=args.query,
                country=args.country,
                types=args.types,
                limit=args.limit,
                bbox=bbox,
            )

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            if not results:
                print("No results found")
            else:
                for i, result in enumerate(results, 1):
                    print(f"\n=== Result {i} ===")
                    print(f"Place: {result['place_name']}")
                    print(f"Coordinates: {result['latitude']}, {result['longitude']}")
                    if result.get("relevance"):
                        print(f"Relevance: {result['relevance']:.2f}")
                    print(f"Type: {', '.join(result.get('type', []))}")

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
