#!/usr/bin/env python3
"""
Clean simple transcript format with [FirstName] markers.

Usage:
    python clean_transcript_simple.py <meeting_file.md>

This script handles transcripts with simple [FirstName] markers and no timestamps.
It maps first names to full names from the attendee list and formats with proper links.
"""

import re
import sys
from pathlib import Path


def parse_attendees(content):
    """
    Extract attendee mapping from the meeting note.
    
    Returns dict mapping lowercase first name to (full_name, display_name)
    e.g., {'kevin': ('Tronkowski, Kevin', 'Kevin Tronkowski')}
    """
    attendee_map = {}
    
    # Look for attendee section
    attendee_section = re.search(r'## Attendees\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if not attendee_section:
        return attendee_map
    
    # Parse linked names: [[Last, First|First Last]]
    for match in re.finditer(r'\[\[([^,]+),\s*([^\]|]+)\|([^\]]+)\]\]', attendee_section.group(1)):
        last, first, display = match.groups()
        first_name = first.strip().split()[0]  # Get first word of first name
        attendee_map[first_name.lower()] = (f"{last.strip()}, {first.strip()}", display.strip())
    
    return attendee_map


def clean_transcript(content):
    """Clean the transcript section."""
    attendee_map = parse_attendees(content)
    
    if not attendee_map:
        print("ERROR: No attendees found in meeting note")
        return None
    
    # Find transcript section
    transcript_match = re.search(r'(## Transcript\n\n)(.*?)(\n\n## |\Z)', content, re.DOTALL)
    if not transcript_match:
        print("ERROR: No transcript section found")
        return None
    
    before = content[:transcript_match.start(1)]
    header = transcript_match.group(1)
    transcript_content = transcript_match.group(2).strip()
    after = content[transcript_match.end(2):]
    
    # Parse transcript entries
    cleaned_entries = []
    lines = transcript_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for speaker marker [Name]
        speaker_match = re.match(r'^\[([^\]]+)\]\s*$', line)
        if speaker_match:
            speaker_raw = speaker_match.group(1).strip()
            speaker_lower = speaker_raw.lower()
            
            # Skip "Speaker N" markers
            if speaker_lower.startswith('speaker '):
                i += 1
                # Skip the content after Speaker N
                while i < len(lines) and not re.match(r'^\[([^\]]+)\]\s*$', lines[i].strip()):
                    i += 1
                continue
            
            # Map to full name or use as-is
            if speaker_lower in attendee_map:
                full_name, display = attendee_map[speaker_lower]
                speaker = f"**[[{full_name}|{display}]]**"
            else:
                speaker = f"**{speaker_raw}**"
            
            # Collect content until next speaker
            content_lines = []
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if re.match(r'^\[([^\]]+)\]\s*$', next_line):
                    break
                if next_line:  # Skip empty lines
                    content_lines.append(next_line)
                i += 1
            
            # Join content
            if content_lines:
                text = ' '.join(content_lines)
                cleaned_entries.append((speaker, text))
        else:
            i += 1
    
    # Format cleaned transcript
    cleaned_lines = []
    for speaker, text in cleaned_entries:
        cleaned_lines.append(f"{speaker}\n\n{text}\n")
    
    cleaned = '\n'.join(cleaned_lines)
    
    # Reconstruct file
    new_content = before + header + cleaned + after
    
    # Print summary
    speaker_counts = {}
    for speaker, _ in cleaned_entries:
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
    
    print(f"✓ Cleaned {len(cleaned_entries)} transcript entries")
    for speaker, count in sorted(speaker_counts.items(), key=lambda x: -x[1]):
        display = re.search(r'\[\[.*?\|(.+?)\]\]', speaker)
        name = display.group(1) if display else speaker.strip('*')
        print(f"  - {name}: {count} entries")
    
    return new_content


def main():
    if len(sys.argv) != 2:
        print("Usage: clean_transcript_simple.py <meeting-file.md>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make backup
    backup_path = filepath.with_suffix(filepath.suffix + '.bak')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created backup: {backup_path}")
    
    # Clean transcript
    cleaned = clean_transcript(content)
    if not cleaned:
        print("ERROR: Failed to clean transcript")
        sys.exit(1)
    
    # Write cleaned version
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"✓ Updated {filepath}")


if __name__ == '__main__':
    main()
