#!/usr/bin/env python3
"""
Clean Microsoft Teams .docx exported transcript format and format for Obsidian.

This handles the format from .docx files converted to plain text where:
- Speaker and timestamp are on one line with content: " Last, First   timestamp content"
- Leading space before speaker name
- NO bold markdown (plain text)
- Meeting header info is present
- No image URLs (stripped during conversion)

Usage:
    python clean_transcript_docx.py <meeting_file.md>

This script:
1. Extracts the raw transcript section from a meeting file
2. Parses speaker names, timestamps, and content
3. Removes metadata and unwanted formatting
4. Outputs clean formatted transcript to replace original
"""

import re
import sys
from pathlib import Path


def parse_docx_transcript(raw_transcript, speakers):
    """
    Parse .docx converted Teams transcript format into structured entries.
    
    Format:  Last, First   timestamp content
    
    Args:
        raw_transcript: Raw transcript text
        speakers: Dict mapping "Last, First" to "First Last"
    
    Returns:
        List of dicts with speaker, display_name, timestamp, content
    """
    lines = raw_transcript.split('\n')
    entries = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip header info
        if ('Meeting Recording' in line or 
            re.match(r'^[A-Z][a-z]+ \d+, \d{4}', line) or  # "January 13, 2026"
            re.match(r'^\d+[hm]\s+\d+[ms]\s+\d+s', line)):  # "1h 16m 5s"
            continue
        
        # Skip transcription markers
        if 'started transcription' in line or 'stopped transcription' in line:
            continue
        
        # Parse speaker lines with format: " Last, First   timestamp content"
        # Pattern: optional leading space, Last, First, spaces, timestamp, space, content
        match = re.match(r'\s*([A-Z][a-z]+(?:-[A-Z][a-z]+)?),\s+([A-Z][a-z]+)\s+(\d{1,2}:\d{2})\s+(.+)', line)
        if match:
            last = match.group(1)
            first = match.group(2)
            timestamp = match.group(3)
            content = match.group(4).strip()
            
            last_first = f"{last}, {first}"
            
            # Get display name from speakers dict or construct it
            if last_first in speakers:
                display_name = speakers[last_first]
            else:
                display_name = f"{first} {last}"
            
            # Only add if there's actual content
            if content:
                entries.append({
                    'speaker': last_first,
                    'display_name': display_name,
                    'timestamp': timestamp,
                    'content': content
                })
    
    return entries


def extract_speakers_from_attendees(meeting_content):
    """
    Extract speaker mapping from attendee list in meeting file.
    
    Returns:
        Dict mapping "Last, First" to "First Last"
    """
    speakers = {}
    
    # Find attendee sections
    attendee_pattern = r'##\s+(?:In Meeting|Invited/Other Participants).*?\n((?:- \[\[.*?\]\]\n?)+)'
    matches = re.finditer(attendee_pattern, meeting_content, re.DOTALL)
    
    for match in matches:
        attendee_block = match.group(1)
        # Parse links: [[Last, First|First Last]]
        links = re.findall(r'\[\[([^|]+)\|([^\]]+)\]\]', attendee_block)
        for last_first, first_last in links:
            speakers[last_first] = first_last
    
    return speakers


def clean_transcript(meeting_file):
    """
    Main function to clean transcript in meeting file.
    
    Args:
        meeting_file: Path to meeting markdown file
    """
    meeting_path = Path(meeting_file)
    
    if not meeting_path.exists():
        print(f"Error: Meeting file not found: {meeting_file}")
        sys.exit(1)
    
    # Read meeting file
    with open(meeting_path, 'r') as f:
        content = f.read()
    
    # Extract speakers from attendee list
    speakers = extract_speakers_from_attendees(content)
    
    if not speakers:
        print("Error: No speakers found in attendee list")
        sys.exit(1)
    
    # Find transcript section
    transcript_match = re.search(r'(## Transcript\n\n)(.+?)(?=\n##|\Z)', content, re.DOTALL)
    
    if not transcript_match:
        print("Warning: No transcript section found")
        sys.exit(0)
    
    transcript_header = transcript_match.group(1)
    raw_transcript = transcript_match.group(2)
    
    # Parse transcript entries
    entries = parse_docx_transcript(raw_transcript, speakers)
    
    if not entries:
        print("Warning: No transcript entries parsed")
        sys.exit(0)
    
    # Build cleaned transcript
    cleaned_lines = [transcript_header.rstrip()]
    
    for entry in entries:
        cleaned_lines.append(f"\n**[[{entry['speaker']}|{entry['display_name']}]]** {entry['timestamp']}\n")
        cleaned_lines.append(f"{entry['content']}\n")
    
    cleaned_transcript = '\n'.join(cleaned_lines)
    
    # Replace transcript section in original content
    new_content = re.sub(
        r'## Transcript\n\n.+?(?=\n##|\Z)',
        cleaned_transcript,
        content,
        flags=re.DOTALL
    )
    
    # Write back to file
    with open(meeting_path, 'w') as f:
        f.write(new_content)
    
    # Print summary
    print(f"✓ Cleaned transcript: {len(entries)} entries formatted")
    for i, entry in enumerate(entries[:5]):
        print(f"  - {entry['display_name']} at {entry['timestamp']}")
    if len(entries) > 5:
        print(f"  ... and {len(entries) - 5} more")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python clean_transcript_docx.py <meeting_file.md>")
        sys.exit(1)
    
    clean_transcript(sys.argv[1])
