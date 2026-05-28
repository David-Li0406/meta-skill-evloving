#!/usr/bin/env python3
"""
Clean Microsoft Teams transcript and format for Obsidian.

Usage:
    python clean_transcript.py <meeting_file.md>

This script:
1. Extracts the raw transcript section from a meeting file
2. Parses speaker names, timestamps, and content
3. Removes metadata, images, and unwanted formatting
4. Outputs clean formatted transcript to replace original
"""

import re
import sys
from pathlib import Path


def parse_transcript(raw_transcript, speakers):
    """
    Parse raw Teams transcript into structured entries.
    
    Args:
        raw_transcript: Raw transcript text
        speakers: Dict mapping "Last, First" to "First Last"
    
    Returns:
        List of dicts with speaker, display_name, timestamp, content
    """
    blocks = [b.strip() for b in raw_transcript.split('\n\n') if b.strip()]
    
    entries = []
    current_speaker = None
    current_timestamp = None
    current_content = []
    
    for block in blocks:
        # Skip unwanted content
        if (block in ['____', '## Transcript', 'PK', 'SM'] or
            'started transcription' in block or 
            'stopped transcription' in block or
            'https://nam.loki.delve' in block or 
            'Use arrow keys' in block or
            'AI-generated' in block):
            continue
        
        # Speaker name
        if block in speakers:
            # Save previous entry
            if current_speaker and current_timestamp and current_content:
                entries.append({
                    'speaker': current_speaker,
                    'display_name': speakers[current_speaker],
                    'timestamp': current_timestamp,
                    'content': '\n\n'.join(current_content)
                })
            current_speaker = block
            current_timestamp = None
            current_content = []
            continue
        
        # Timestamp line (contains "X minutes Y seconds" and "X:YY")
        if current_speaker and re.search(r'\d+ minutes? \d+ seconds?\d+:\d+', block):
            ts_match = re.search(r'(\d{1,2}:\d{2})$', block)
            if ts_match:
                current_timestamp = ts_match.group(1)
            continue
        
        # Skip duplicate "Speaker timestamp" line
        if current_speaker and current_speaker in block and re.search(r'\d+ minutes?', block):
            continue
        
        # Content
        if current_speaker and current_timestamp:
            current_content.append(block)
    
    # Save last entry
    if current_speaker and current_timestamp and current_content:
        entries.append({
            'speaker': current_speaker,
            'display_name': speakers[current_speaker],
            'timestamp': current_timestamp,
            'content': '\n\n'.join(current_content)
        })
    
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
        print("Usage: python clean_transcript.py <meeting_file.md>")
        sys.exit(1)
    
    meeting_file = Path(sys.argv[1])
    
    if not meeting_file.exists():
        print(f"Error: File not found: {meeting_file}")
        sys.exit(1)
    
    # Read meeting file
    with open(meeting_file, 'r') as f:
        lines = f.readlines()
    
    # Find transcript section
    transcript_start = None
    for i, line in enumerate(lines):
        if line.strip() == '## Transcript':
            transcript_start = i
            break
    
    if transcript_start is None:
        print("Error: No '## Transcript' section found in meeting file")
        sys.exit(1)
    
    # Extract raw transcript
    raw_transcript = ''.join(lines[transcript_start:])
    
    # Get speaker mapping from attendee list
    speakers = get_speakers_from_attendees(meeting_file)
    
    if not speakers:
        print("Error: No speakers found in attendee list")
        sys.exit(1)
    
    # Parse transcript
    entries = parse_transcript(raw_transcript, speakers)
    
    if not entries:
        print("Warning: No transcript entries parsed")
        sys.exit(0)
    
    # Format clean transcript
    formatted_transcript = format_transcript(entries)
    
    # Replace transcript in meeting file
    output = ''.join(lines[:transcript_start]) + formatted_transcript + '\n'
    
    # Remove separator lines
    output_lines = output.split('\n')
    cleaned = [line for line in output_lines if line.strip() != '____']
    output = '\n'.join(cleaned)
    
    # Write back
    with open(meeting_file, 'w') as f:
        f.write(output)
    
    print(f"✓ Cleaned transcript: {len(entries)} entries formatted")
    for entry in entries[:3]:
        print(f"  - {entry['display_name']} at {entry['timestamp']}")
    if len(entries) > 3:
        print(f"  ... and {len(entries) - 3} more")


if __name__ == '__main__':
    main()
