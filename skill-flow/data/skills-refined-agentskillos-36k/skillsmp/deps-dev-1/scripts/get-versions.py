#!/usr/bin/env python3
"""
Get latest versions of packages from deps.dev API.

Usage:
    python3 get-versions.py <system> <package1> [package2] ...
    python3 get-versions.py npm express lodash @types/node
    python3 get-versions.py pypi requests django flask
    python3 get-versions.py go github.com/gin-gonic/gin

Supported systems: npm, pypi, go, cargo, maven, nuget

Output: JSON object with package versions
"""

import json
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed


API_BASE = "https://api.deps.dev/v3alpha/systems"


def get_latest_version(system: str, package: str) -> dict:
    """Fetch the latest version of a package from deps.dev API."""
    encoded_name = urllib.parse.quote(package, safe="")
    url = f"{API_BASE}/{system}/packages/{encoded_name}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        for version in data.get("versions", []):
            if version.get("isDefault"):
                return {
                    "package": package,
                    "version": version["versionKey"]["version"],
                    "publishedAt": version.get("publishedAt", ""),
                    "isDeprecated": version.get("isDeprecated", False),
                }

        # No default version found, return the last one
        versions = data.get("versions", [])
        if versions:
            last = versions[-1]
            return {
                "package": package,
                "version": last["versionKey"]["version"],
                "publishedAt": last.get("publishedAt", ""),
                "isDeprecated": last.get("isDeprecated", False),
                "note": "No default version, using latest available",
            }

        return {"package": package, "error": "No versions found"}

    except urllib.error.HTTPError as e:
        return {"package": package, "error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"package": package, "error": f"Network error: {e.reason}"}
    except json.JSONDecodeError:
        return {"package": package, "error": "Invalid JSON response"}
    except Exception as e:
        return {"package": package, "error": str(e)}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: get-versions.py <system> <package1> [package2] ...",
            "systems": ["npm", "pypi", "go", "cargo", "maven", "nuget"],
        }))
        sys.exit(1)

    system = sys.argv[1].upper()
    packages = sys.argv[2:]

    # Validate system
    valid_systems = ["NPM", "PYPI", "GO", "CARGO", "MAVEN", "NUGET"]
    if system not in valid_systems:
        print(json.dumps({
            "error": f"Invalid system: {sys.argv[1]}",
            "valid_systems": [s.lower() for s in valid_systems],
        }))
        sys.exit(1)

    # Fetch versions in parallel
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(get_latest_version, system, pkg): pkg
            for pkg in packages
        }
        for future in as_completed(futures):
            results.append(future.result())

    # Sort results to match input order
    pkg_order = {pkg: i for i, pkg in enumerate(packages)}
    results.sort(key=lambda x: pkg_order.get(x["package"], 999))

    output = {
        "system": system.lower(),
        "packages": results,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
