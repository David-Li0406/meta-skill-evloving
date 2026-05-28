#!/usr/bin/env python3
"""
Get project onboarding documentation
"""
import argparse
import os
import sys
from pathlib import Path


def get_onboarding(project_root: str):
    """Get onboarding content"""
    
    onboarding_file = Path(project_root) / ".tmp" / ".serena-skills" / "onboarding.md"
    
    if not onboarding_file.exists():
        raise FileNotFoundError("Onboarding not found. Create it first with create_onboarding.py")
    
    return onboarding_file.read_text(encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description="Get project onboarding")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    
    args = parser.parse_args()
    
    try:
        content = get_onboarding(args.project_root)
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
