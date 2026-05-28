#!/usr/bin/env python3
"""
Compute Cosine Similarity between two vectors

Usage:
    python3 cosine_sim.py <vector1_json_file> <vector2_json_file>

    Vectors should be JSON arrays of floats.

Dependencies:
    pip install numpy (recommended)
"""

import sys
import argparse
import json
import math


def cosine_similarity(v1, v2):
    """
    Compute cosine similarity between two vectors.

    Args:
        v1 (list): First vector.
        v2 (list): Second vector.

    Returns:
        float: Cosine similarity score (-1.0 to 1.0).
    """
    if len(v1) != len(v2):
        raise ValueError(f"Vector dimensions do not match: {len(v1)} vs {len(v2)}")

    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a * a for a in v1))
    magnitude2 = math.sqrt(sum(b * b for b in v2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def load_vector(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading vector file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Compute cosine similarity")
    parser.add_argument("vector1_file", help="Path to first vector JSON file")
    parser.add_argument("vector2_file", help="Path to second vector JSON file")

    args = parser.parse_args()

    v1 = load_vector(args.vector1_file)
    v2 = load_vector(args.vector2_file)

    try:
        score = cosine_similarity(v1, v2)
        print(f"{score:.6f}")
    except Exception as e:
        print(f"Error calculating similarity: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
