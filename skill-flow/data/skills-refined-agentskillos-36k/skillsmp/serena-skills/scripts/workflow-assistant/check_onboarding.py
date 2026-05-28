#!/usr/bin/env python3
"""
Check if project has onboarding documentation
"""
import argparse
import json
import os
import sys
from pathlib import Path


def check_onboarding(project_root: str):
    """Check if onboarding exists"""
    
    onboarding_file = Path(project_root) / ".tmp" / ".serena-skills" / "onboarding.md"
    
    return {
        "exists": onboarding_file.exists(),
        "path": str(onboarding_file)
    }


def main():
    parser = argparse.ArgumentParser(description="Check project onboarding status")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    
    args = parser.parse_args()
    
    try:
        result = check_onboarding(args.project_root)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
