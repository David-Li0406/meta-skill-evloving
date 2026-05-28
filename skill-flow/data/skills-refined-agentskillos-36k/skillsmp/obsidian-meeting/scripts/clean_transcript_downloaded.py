#!/usr/bin/env python3
"""
Clean Microsoft Teams DOWNLOADED transcript format and format for Obsidian.

This handles the format from downloaded/exported Teams transcripts where:
- Speaker and timestamp are on one line: **Last, First**   timestamp
- Image URLs precede each speaker line
- Meeting header info is present

Usage:
    python clean_transcript_downloaded.py <meeting_file.md>

This script:
1. Extracts the raw transcript section from a meeting file
2. Parses speaker names (from **Name**), timestamps, and content
3. Removes metadata, images, and unwanted formatting
4. Outputs clean formatted transcript to replace original
"""

import re
import sys
from pathlib import Path


def parse_downloaded_transcript(raw_transcript, speakers):
    """
    Parse downloaded Teams transcript format into structured entries.
    
    Format: **Last, First**   timestamp
    
    Args:
        raw_transcript: Raw transcript text
        speakers: Dict mapping "Last, First" to "First Last"
    
    Returns:
        List of dicts with speaker, display_name, timestamp, content
    """
    lines = raw_transcript.split('\n')
    entries = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
            
        # Skip image references
        if line.startswith('![](file://') or line.startswith('![](https://'):
            i += 1
            continue
        
        # Skip header info
        if ('Meeting Recording' in line or 
            re.match(r'^[A-Z][a-z]+ \d+, \d{4}', line) or  # "January 13, 2026"
            re.match(r'^\d+h \d+m \d+s', line)):  # "1h 16m 5s"
            i += 1
            continue
        
        # Skip transcription markers
        if 'started transcription' in line or 'stopped transcription' in line:
            i += 1
            continue
        
        # Parse speaker lines with format: **Last, First**   timestamp
        speaker_match = re.match(r'\*\*([A-Za-z]+, [A-Za-z]+)\*\*\s+(\d{1,2}:\d{2})', line)
        if speaker_match:
            last_first = speaker_match.group(1)
            timestamp = speaker_match.group(2)
            
            # Get display name from speakers dict or construct it
            if last_first in speakers:
                display_name = speakers[last_first]
            else:
                parts = last_first.split(', ')
                display_name = f"{parts[1]} {parts[0]}"
            
            # Collect content until next speaker or image
            i += 1
            content_lines = []
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line:
                    i += 1
                    continue
                if next_line.startswith('![](file://') or next_line.startswith('![](https://'):
                    i += 1
                    break
                if re.match(r'\*\*[A-Za-z]+, [A-Za-z]+\*\*', next_line):
                    break
                content_lines.append(next_line)
                i += 1
            
            if content_lines:
                entries.append({
                    'speaker': last_first,
                    'display_name': display_name,
                    'timestamp': timestamp,
                    'content': '  \n'.join(content_lines)  # Preserve line breaks within speech
                })
            continue
        
        i += 1
    
    return entries


def format_transcript(entries):
    """Format parsed entries into clean markdown."""
    formatted = ['## Transcript', '']
    
    for entry in entries:
        formatted.append(f"**[[{entry['speaker']}|{entry['display_name']}]]** {entry['timestamp']}")
        formatted.append('')
        formatted.append(entry['content'])
        formatted.append('')
    
    return '\n'.join(formatted)


def get_speakers_from_attendees(meeting_file):
    """Extract speaker mapping from attendee list in meeting file."""
    with open(meeting_file, 'r') as f:
        content = f.read()
    
    speakers = {}
    
    # Find attendee section
    attendee_pattern = r'\[\[([^|]+)\|([^\]]+)\]\]'
    for match in re.finditer(attendee_pattern, content):
        formal_name = match.group(1)  # "Last, First"
        display_name = match.group(2)  # "First Last"
        speakers[formal_name] = display_name
    
    return speakers


def main():
    if len(sys.argv) != 2:
        print("Usage: python clean_transcript_downloaded.py <meeting_file.md>")
        sys.exit(1)
    
    meeting_file = Path(sys.argv[1])
    
    if not meeting_file.exists():
        print(f"Error: File not found: {meeting_file}")
        sys.exit(1)
    
    # Read meeting file
    with open(meeting_file, 'r') as f:
        content = f.read()
    
    # Find transcript section
    transcript_match = re.search(r'(## Transcript.*)', content, re.DOTALL)
    if not transcript_match:
        print("Error: No '## Transcript' section found in meeting file")
        sys.exit(1)
    
    before_transcript = content[:transcript_match.start()]
    raw_transcript = transcript_match.group(1)
    
    # Get speaker mapping from attendee list
    speakers = get_speakers_from_attendees(meeting_file)
    
    if not speakers:
        print("Error: No speakers found in attendee list")
        sys.exit(1)
    
    # Parse transcript
    entries = parse_downloaded_transcript(raw_transcript, speakers)
    
    if not entries:
        print("Warning: No transcript entries parsed")
        sys.exit(0)
    
    # Format clean transcript
    clean_transcript = format_transcript(entries)
    
    # Write back to file
    new_content = before_transcript + clean_transcript
    with open(meeting_file, 'w') as f:
        f.write(new_content)
    
    # Summary output
    print(f"✓ Cleaned transcript successfully")
    print(f"  Processed {len(entries)} entries")
    if entries:
        print(f"  First: {entries[0]['display_name']} at {entries[0]['timestamp']}")
        if len(entries) > 1:
            print(f"  Last: {entries[-1]['display_name']} at {entries[-1]['timestamp']}")


if __name__ == '__main__':
    main()
