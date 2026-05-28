#!/usr/bin/env python3
"""
Calculate affine transformation for plate georeferencing.

Converts between pixel coordinates and lat/lon using control points.

Usage:
    python calculate_transform.py --points control_points.json --output georef.json
"""

import argparse
import json
import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class ControlPoint:
    """A control point with pixel and geographic coordinates."""
    pixel_x: float
    pixel_y: float
    latitude: float
    longitude: float
    name: str = ""
    accuracy: str = "medium"


class PlateGeoreference:
    """
    Affine transformation for plate georeferencing.

    Transforms between pixel coordinates and lat/lon:
        lon = A * x + B * y + C
        lat = D * x + E * y + F
    """

    def __init__(self, a: float, b: float, c: float,
                 d: float, e: float, f: float):
        self.a, self.b, self.c = a, b, c
        self.d, self.e, self.f = d, e, f

    def pixel_to_latlon(self, x: float, y: float) -> tuple[float, float]:
        """Convert pixel coordinates to lat/lon."""
        lon = self.a * x + self.b * y + self.c
        lat = self.d * x + self.e * y + self.f
        return lat, lon

    def latlon_to_pixel(self, lat: float, lon: float) -> tuple[float, float]:
        """Convert lat/lon to pixel coordinates."""
        det = self.a * self.e - self.b * self.d
        if abs(det) < 1e-10:
            raise ValueError("Transformation matrix is singular")

        x = (self.e * (lon - self.c) - self.b * (lat - self.f)) / det
        y = (self.a * (lat - self.f) - self.d * (lon - self.c)) / det
        return x, y

    @classmethod
    def from_control_points(cls, points: list[ControlPoint],
                           weights: Optional[list[float]] = None) -> 'PlateGeoreference':
        """
        Compute affine transform from control points using least squares.

        Minimum 3 points required; 4+ recommended for error estimation.
        """
        n = len(points)
        if n < 3:
            raise ValueError("At least 3 control points required")

        # Default equal weights
        if weights is None:
            weights = [1.0] * n

        # Build matrices for weighted least squares
        # A * params = b
        # where params = [a, b, c, d, e, f]

        A = []
        b_lon = []
        b_lat = []

        for i, pt in enumerate(points):
            w = weights[i]
            A.append([w * pt.pixel_x, w * pt.pixel_y, w])
            b_lon.append(w * pt.longitude)
            b_lat.append(w * pt.latitude)

        # Solve using normal equations
        # A^T * A * x = A^T * b
        ATA = [[0.0] * 3 for _ in range(3)]
        ATb_lon = [0.0] * 3
        ATb_lat = [0.0] * 3

        for i in range(n):
            for j in range(3):
                for k in range(3):
                    ATA[j][k] += A[i][j] * A[i][k]
                ATb_lon[j] += A[i][j] * b_lon[i]
                ATb_lat[j] += A[i][j] * b_lat[i]

        # Solve for longitude coefficients (a, b, c)
        lon_params = _solve_3x3(ATA, ATb_lon)

        # Solve for latitude coefficients (d, e, f)
        lat_params = _solve_3x3(ATA, ATb_lat)

        return cls(
            a=lon_params[0], b=lon_params[1], c=lon_params[2],
            d=lat_params[0], e=lat_params[1], f=lat_params[2]
        )

    def calculate_error(self, points: list[ControlPoint]) -> dict:
        """Calculate transformation error statistics."""
        errors = []

        for pt in points:
            pred_lat, pred_lon = self.pixel_to_latlon(pt.pixel_x, pt.pixel_y)

            # Calculate error in nautical miles
            error_nm = _haversine_nm(pt.latitude, pt.longitude,
                                     pred_lat, pred_lon)
            errors.append(error_nm)

        rms = math.sqrt(sum(e * e for e in errors) / len(errors))
        max_error = max(errors)
        mean_error = sum(errors) / len(errors)

        return {
            'rms_error_nm': rms,
            'max_error_nm': max_error,
            'mean_error_nm': mean_error,
            'errors': errors,
        }

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            'a': self.a, 'b': self.b, 'c': self.c,
            'd': self.d, 'e': self.e, 'f': self.f,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PlateGeoreference':
        """Deserialize from dictionary."""
        return cls(
            a=data['a'], b=data['b'], c=data['c'],
            d=data['d'], e=data['e'], f=data['f'],
        )


def _solve_3x3(A: list[list[float]], b: list[float]) -> list[float]:
    """Solve 3x3 linear system using Cramer's rule."""
    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
                m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
                m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    d = det3(A)
    if abs(d) < 1e-10:
        raise ValueError("Matrix is singular")

    result = []
    for i in range(3):
        Ai = [row[:] for row in A]
        for j in range(3):
            Ai[j][i] = b[j]
        result.append(det3(Ai) / d)

    return result


def _haversine_nm(lat1: float, lon1: float,
                  lat2: float, lon2: float) -> float:
    """Calculate distance in nautical miles."""
    R = 3440.065  # Earth radius in NM

    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2)

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def main():
    parser = argparse.ArgumentParser(description='Calculate plate georef transform')
    parser.add_argument('--points', '-p', required=True, help='Control points JSON file')
    parser.add_argument('--output', '-o', help='Output georef JSON file')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    # Load control points
    with open(args.points) as f:
        data = json.load(f)

    points = [
        ControlPoint(
            pixel_x=p['pixel_x'],
            pixel_y=p['pixel_y'],
            latitude=p['latitude'],
            longitude=p['longitude'],
            name=p.get('name', ''),
        )
        for p in data['points']
    ]

    print(f"Loaded {len(points)} control points")

    # Calculate transformation
    georef = PlateGeoreference.from_control_points(points)

    # Calculate error
    error = georef.calculate_error(points)
    print(f"\nTransformation quality:")
    print(f"  RMS Error:  {error['rms_error_nm']:.4f} nm")
    print(f"  Max Error:  {error['max_error_nm']:.4f} nm")
    print(f"  Mean Error: {error['mean_error_nm']:.4f} nm")

    if args.verbose:
        print("\nPer-point errors:")
        for i, pt in enumerate(points):
            print(f"  {pt.name or f'Point {i}'}: {error['errors'][i]:.4f} nm")

    # Save output
    if args.output:
        output_data = {
            'transform': georef.to_dict(),
            'error': {
                'rms_nm': error['rms_error_nm'],
                'max_nm': error['max_error_nm'],
            },
            'control_points': len(points),
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nSaved to {args.output}")


if __name__ == '__main__':
    main()
