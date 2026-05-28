#!/usr/bin/env python3
"""
Split linkedin-frameworks.md into category-based reference files.
Each framework is preserved in its entirety.
"""

import re
from pathlib import Path

# Category mappings - framework numbers to categories
# Numbers 101+ are "Framework N:" format (offset by 100)
CATEGORIES = {
    "engagement": [
        1, 5, 8, 9, 29, 76, 91, 94,  # Original
        10, 28, 37, 38, 45, 55, 61,  # Added: Impresses, Trivia, Pick This/That, Would You, Question
        101,  # Framework 1: Fill-In-The-Blank
    ],
    "story": [
        2, 6, 13, 14, 15, 17, 35, 46, 73, 81, 84, 85,  # Original
        4, 19, 27, 50, 60, 74, 97,  # Added: Work/Life, Out of Office, Unexpected, Values, Goals
        107, 109, 111, 117, 119,  # Framework 7,9,11,17,19: Conversation, Career, Day in Life, Regret, Behind Scenes
    ],
    "list": [
        16, 18, 31, 32, 36, 44, 48, 51, 89, 92,  # Original
        30, 43, 71,  # Added: Spreadsheet, Flow Chart, What Gets Axe
        102, 106, 112, 114,  # Framework 2,6,12,14: DOs/DONTs, 10-Min Tweak, Skills, Three Types
    ],
    "contrarian": [
        3, 34, 42, 52, 57, 59, 68, 80, 86, 98,  # Original
        41, 53, 66, 70, 72, 83,  # Added: 3 Things, Doesn't Want to Hear, Rant, Bad Boss, Never Say
        108, 110, 115, 118,  # Framework 8,10,15,18: Bold Truth, Hot Take, No One Tells You, Get Wrong
    ],
    "authority": [
        22, 23, 24, 25, 47, 56, 82, 87, 88, 96,  # Original (removed 89 - duplicate)
        11, 12, 21, 33, 39, 54, 58, 63, 67, 77, 90, 95,  # Added: Screenshot, Quote, Infographic, News, Script, Secret
        105, 113, 116, 120,  # Framework 5,13,16,20: Sports, Wish I'd Known, Tested It, Success Requires
    ],
    "community": [
        7, 20, 40, 62, 64, 65, 75, 78, 79, 93,  # Original
        26, 49, 69,  # Added: Comedy, Why Get Fired, Mistake
        103, 104,  # Framework 3,4: Humble Brag, Compensation Poll
    ],
}

# Frameworks that don't fit neatly - put in "other"
# Will catch anything not explicitly categorized

def extract_framework_number(heading):
    """Extract framework number from heading like '## 1. The "Agree or Disagree" Post'"""
    match = re.match(r'##\s*(\d+)\.', heading)
    if match:
        return int(match.group(1))
    # Handle "Framework N:" format
    match = re.match(r'##\s*Framework\s*(\d+)', heading)
    if match:
        return int(match.group(1)) + 100  # Offset to avoid collision
    return None

def split_frameworks(input_file):
    """Split the file into individual frameworks."""
    content = input_file.read_text()

    # Split on ## headers (framework boundaries)
    parts = re.split(r'(^## .+$)', content, flags=re.MULTILINE)

    frameworks = {}
    current_heading = None

    for part in parts:
        if part.startswith('## '):
            current_heading = part
        elif current_heading:
            num = extract_framework_number(current_heading)
            if num:
                frameworks[num] = current_heading + '\n' + part
            current_heading = None

    return frameworks

def get_category(num):
    """Get category for a framework number."""
    for cat, nums in CATEGORIES.items():
        if num in nums:
            return cat
    return "other"

def main():
    # Paths
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    source_file = Path("/home/user/OpenEd-Vault/.claude/skills/social-content-creation/references/linkedin-frameworks.md")
    refs_dir = skill_dir / "references"

    # Parse frameworks
    print(f"Reading {source_file}...")
    frameworks = split_frameworks(source_file)
    print(f"Found {len(frameworks)} frameworks")

    # Group by category
    categorized = {}
    for num, content in frameworks.items():
        cat = get_category(num)
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append((num, content))

    # Sort each category by framework number
    for cat in categorized:
        categorized[cat].sort(key=lambda x: x[0])

    # Write category files
    for cat, items in categorized.items():
        output_file = refs_dir / f"{cat}-frameworks.md"

        header = f"# {cat.title()} Frameworks\n\n"
        header += f"**{len(items)} frameworks in this category.**\n\n"
        header += "---\n\n"

        body = "\n---\n\n".join([content for _, content in items])

        output_file.write_text(header + body)
        print(f"Wrote {output_file.name}: {len(items)} frameworks")

    print("\nDone!")

if __name__ == "__main__":
    main()
