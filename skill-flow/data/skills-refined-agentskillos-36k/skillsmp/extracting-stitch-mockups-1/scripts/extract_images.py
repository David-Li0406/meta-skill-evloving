#!/usr/bin/env python3
"""
Utility functions for extracting mockup images from Google Stitch project pages.

This script provides utility functions for:
- Resolving feature directories
- Normalizing feature names
- Downloading images from URLs
- Saving images to the correct directory structure

Note: The actual extraction uses Cursor's built-in browser (MCP browser tools).
The AI assistant navigates to the Stitch URL, extracts image URLs from the DOM snapshot,
and then uses these utilities to download and save the images.

Usage:
    python extract_images.py <image_urls...> [--feature <name>] [--output <dir>]
    
    # Or use as a module:
    from extract_images import resolve_output_dir, download_images
    
    output_dir = resolve_output_dir(project_title="My Project", feature=None)
    download_images(image_urls=["url1", "url2"], output_dir=output_dir)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path


def get_repo_root():
    """Get git repository root directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        return Path.cwd()


def normalize_feature_name(name):
    """Convert name to feature directory format."""
    # Lowercase
    name = name.lower()
    # Replace whitespace with hyphens
    name = re.sub(r'\s+', '-', name)
    # Strip non-alphanumeric except hyphens
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Collapse duplicate hyphens
    name = re.sub(r'-+', '-', name)
    # Trim ends
    name = name.strip('-')
    return name


def find_existing_features(repo_root):
    """Find existing feature directories in design-intent/google-stitch/."""
    stitch_dir = repo_root / "design-intent" / "google-stitch"
    if not stitch_dir.exists():
        return []

    features = []
    for item in stitch_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            features.append(item.name)
    return sorted(features)


def match_feature_directory(project_title, existing_features):
    """Try to match project title to existing feature directory."""
    normalized = normalize_feature_name(project_title)

    # Exact match
    if normalized in existing_features:
        return normalized

    # Partial match (project title contains feature name or vice versa)
    matches = []
    for feature in existing_features:
        if feature in normalized or normalized in feature:
            matches.append(feature)

    if len(matches) == 1:
        return matches[0]

    return None


def resolve_output_dir(project_title, feature=None, output_dir=None):
    """Resolve output directory for saving images."""
    repo_root = get_repo_root()
    
    # Determine output directory
    if output_dir:
        return Path(output_dir)
    elif feature:
        return repo_root / "design-intent" / "google-stitch" / feature / "exports"
    else:
        # Try to auto-detect feature directory
        existing_features = find_existing_features(repo_root)
        matched_feature = match_feature_directory(project_title, existing_features)

        if matched_feature:
            return repo_root / "design-intent" / "google-stitch" / matched_feature / "exports"
        elif existing_features:
            print("\nCould not auto-detect feature directory.")
            print("Existing feature directories:")
            for i, feat in enumerate(existing_features, 1):
                print(f"  {i}. {feat}")
            print("\nPlease specify --feature <name> to set target directory.")
            return None
        else:
            # No existing features, create based on project title
            feature_name = normalize_feature_name(project_title)
            return repo_root / "design-intent" / "google-stitch" / feature_name / "exports"


def download_images(image_urls, output_dir):
    """Download images from URLs and save to output directory."""
    if not image_urls:
        print("No image URLs provided.")
        return []

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nDownloading {len(image_urls)} mockup images...")
    saved_files = []
    
    for i, img_url in enumerate(image_urls, 1):
        try:
            filename = f"mockup-{i}.png"
            filepath = output_dir / filename
            
            # Download image
            urllib.request.urlretrieve(img_url, filepath)
            saved_files.append(filename)
            print(f"  ✓ Saved: {filename}")
        except Exception as e:
            print(f"  ✗ Failed to download image {i}: {e}")
    
    return saved_files


def extract_project_title_from_url(url):
    """Extract project title from Stitch URL (fallback)."""
    try:
        project_id = url.split("/projects/")[-1].split("/")[0].split("?")[0]
        return f"stitch-project-{project_id}"
    except Exception:
        return "stitch-project"


def main():
    parser = argparse.ArgumentParser(
        description="Download and save mockup images from Google Stitch project pages."
    )
    parser.add_argument(
        "image_urls",
        nargs="+",
        help="Image URLs to download (extracted from Stitch page)"
    )
    parser.add_argument(
        "--project-title",
        help="Project title for directory resolution"
    )
    parser.add_argument(
        "--feature",
        help="Target feature directory name (e.g., 'dashboard')"
    )
    parser.add_argument(
        "--output", "--output-dir",
        dest="output",
        help="Custom output directory path"
    )

    args = parser.parse_args()

    # Resolve output directory
    project_title = args.project_title or "stitch-project"
    output_dir = resolve_output_dir(
        project_title=project_title,
        feature=args.feature,
        output_dir=args.output
    )
    
    if not output_dir:
        sys.exit(1)

    print(f"✓ Output directory: {output_dir}")

    # Download images
    saved_files = download_images(
        image_urls=args.image_urls,
        output_dir=output_dir
    )

    if not saved_files:
        print("No images were downloaded.")
        sys.exit(1)

    result = {
        "project_title": project_title,
        "output_dir": str(output_dir),
        "files": saved_files
    }

    # Print summary
    print(f"\nDownloaded {len(saved_files)} mockups")
    print(f"Saved to: {output_dir.relative_to(get_repo_root())}")

    # Output JSON for programmatic use
    if os.environ.get("OUTPUT_JSON"):
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
