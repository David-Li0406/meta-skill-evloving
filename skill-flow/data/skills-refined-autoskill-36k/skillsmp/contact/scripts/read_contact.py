#!/usr/bin/env python3
"""
Reads contact info from src/lib/constants/contact.ts and outputs a compact summary.
Usage: python3 read_contact.py [format]
  format: summary (default), json
"""

import json
import re
import sys
from pathlib import Path

CONTACT_FILE = Path(__file__).parent.parent.parent.parent.parent / "src" / "lib" / "constants" / "contact.ts"


def read_contact() -> dict:
    """Read contact data from TypeScript file."""
    content = CONTACT_FILE.read_text()

    # Extract values using regex
    email = re.search(r'email:\s*["\']([^"\']+)["\']', content)
    linkedin = re.search(r'linkedin:\s*["\']([^"\']+)["\']', content)
    github = re.search(r'github:\s*["\']([^"\']+)["\']', content)
    instagram = re.search(r'instagram:\s*["\']([^"\']+)["\']', content)
    location = re.search(r'location:\s*["\']([^"\']+)["\']', content)

    return {
        "email": email.group(1) if email else "N/A",
        "linkedin": linkedin.group(1) if linkedin else "N/A",
        "github": github.group(1) if github else "N/A",
        "instagram": instagram.group(1) if instagram else "N/A",
        "location": location.group(1) if location else "N/A",
    }


def format_summary(data: dict) -> str:
    """Format contact data as a compact summary."""
    lines = ["CONTACT INFO"]
    lines.append(f"  Email: {data.get('email', 'N/A')}")
    lines.append(f"  LinkedIn: {data.get('linkedin', 'N/A')}")
    lines.append(f"  GitHub: {data.get('github', 'N/A')}")
    lines.append(f"  Instagram: {data.get('instagram', 'N/A')}")
    lines.append(f"  Location: {data.get('location', 'N/A')}")
    return '\n'.join(lines)


def main():
    fmt = sys.argv[1] if len(sys.argv) > 1 else "summary"

    data = read_contact()

    if fmt == "summary":
        print(format_summary(data))
    elif fmt == "json":
        print(json.dumps(data, indent=2))
    else:
        print(f"Unknown format: {fmt}")
        print("Usage: python3 read_contact.py [summary|json]")
        sys.exit(1)


if __name__ == "__main__":
    main()
