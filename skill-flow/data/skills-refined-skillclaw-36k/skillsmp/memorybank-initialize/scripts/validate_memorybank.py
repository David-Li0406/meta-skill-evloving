#!/usr/bin/env python3
"""
Memory Bank Structure Validator

Validates that a project has a properly structured Memory Bank with all required files.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import json
from datetime import datetime


REQUIRED_FILES = [
    "projectbrief.md",
    "productContext.md",
    "techContext.md",
    "systemPatterns.md",
    "activeContext.md",
    "progress.md",
]

REQUIRED_SECTIONS = {
    "projectbrief.md": ["Project Name", "Core Purpose", "Key Objectives", "Scope", "Success Criteria"],
    "productContext.md": ["User Problems", "Solution Approach", "User Experience Goals", "Key Features"],
    "techContext.md": ["Technology Stack", "Development Setup", "Key Dependencies", "Constraints"],
    "systemPatterns.md": ["Architecture Overview", "Key Technical Decisions", "Design Patterns", "Component Relationships"],
    "activeContext.md": ["Current Focus", "Recent Changes", "Next Steps", "Blockers", "Learnings"],
    "progress.md": ["What's Working", "What's Left to Build", "Current Status", "Known Issues"],
}

MIN_FILE_SIZE = 50  # Minimum bytes for a file to be considered non-empty


def find_memory_bank(project_path: Path) -> Path:
    """Find the memory-bank directory in the project."""
    memory_bank_path = project_path / "memory-bank"

    if not memory_bank_path.exists():
        print(f"❌ Memory Bank not found at {memory_bank_path}")
        sys.exit(1)

    if not memory_bank_path.is_dir():
        print(f"❌ {memory_bank_path} exists but is not a directory")
        sys.exit(1)

    return memory_bank_path


def check_file_exists(memory_bank: Path, filename: str) -> Tuple[bool, str]:
    """Check if a required file exists and has content."""
    file_path = memory_bank / filename

    if not file_path.exists():
        return False, f"❌ Missing: {filename}"

    if not file_path.is_file():
        return False, f"❌ Not a file: {filename}"

    size = file_path.stat().st_size
    if size < MIN_FILE_SIZE:
        return False, f"⚠️  Too small ({size} bytes): {filename}"

    return True, f"✅ Found: {filename} ({size} bytes)"


def check_sections(memory_bank: Path, filename: str, required_sections: List[str]) -> Tuple[bool, List[str]]:
    """Check if a file contains required sections."""
    file_path = memory_bank / filename

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"❌ Cannot read {filename}: {e}"]

    missing_sections = []
    found_sections = []

    for section in required_sections:
        # Look for markdown headers with the section name
        if f"# {section}" in content or f"## {section}" in content:
            found_sections.append(section)
        else:
            missing_sections.append(section)

    messages = []
    if missing_sections:
        messages.append(f"⚠️  {filename} missing sections: {', '.join(missing_sections)}")
        return False, messages
    else:
        messages.append(f"✅ {filename} has all required sections")
        return True, messages


def validate_structure(memory_bank: Path, check_content: bool = True) -> Tuple[bool, Dict]:
    """Validate the complete Memory Bank structure."""
    results = {
        "valid": True,
        "files": {},
        "messages": [],
        "timestamp": datetime.now().isoformat(),
    }

    # Check all required files exist
    for filename in REQUIRED_FILES:
        exists, message = check_file_exists(memory_bank, filename)
        results["files"][filename] = {"exists": exists}
        results["messages"].append(message)

        if not exists:
            results["valid"] = False

    # If checking content, validate sections
    if check_content:
        for filename, sections in REQUIRED_SECTIONS.items():
            if results["files"].get(filename, {}).get("exists", False):
                has_sections, messages = check_sections(memory_bank, filename, sections)
                results["files"][filename]["has_sections"] = has_sections
                results["messages"].extend(messages)

                if not has_sections:
                    results["valid"] = False

    return results["valid"], results


def main():
    parser = argparse.ArgumentParser(
        description="Validate Memory Bank structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .
  %(prog)s /path/to/project
  %(prog)s . --no-content-check
  %(prog)s . --json
        """
    )

    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to project root containing memory-bank directory"
    )

    parser.add_argument(
        "--no-content-check",
        action="store_true",
        help="Only check if files exist, don't validate content"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Validate project path
    if not args.project_path.exists():
        print(f"❌ Project path does not exist: {args.project_path}")
        sys.exit(1)

    # Find and validate memory bank
    memory_bank = find_memory_bank(args.project_path)

    # Run validation
    is_valid, results = validate_structure(memory_bank, check_content=not args.no_content_check)

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Memory Bank Validation: {memory_bank}")
        print(f"{'='*60}\n")

        for message in results["messages"]:
            print(message)

        print(f"\n{'='*60}")
        if is_valid:
            print("✅ Memory Bank is valid")
            print(f"{'='*60}\n")
        else:
            print("❌ Memory Bank validation failed")
            print(f"{'='*60}\n")

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
