# Obsidian Meeting Scripts

Utility scripts for processing Obsidian meeting notes.

## Overview

Four scripts handle different Microsoft Teams transcript formats:

| Script | Format | Source |
|--------|--------|--------|
| `clean_transcript.py` | Direct paste from Teams | Copy-paste from Teams UI |
| `clean_transcript_downloaded.py` | Downloaded/exported | Downloaded VTT or exported file |
| `clean_transcript_docx.py` | Plain text from .docx | .docx export converted to text |
| `clean_transcript_simple.py` | Simple first-name markers | Basic transcript with [Name] format |

## clean_transcript.py

Cleans **direct paste** format from Microsoft Teams UI.

**Usage:**
```bash
python clean_transcript.py <meeting_file.md>
```

**Input format characteristics:**
- Speaker name on separate line: `Last, First`
- Verbose timestamp line: `0 minutes 3 seconds0:03`
- Duplicate speaker+timestamp line
- Profile image URLs on separate lines
- Separator lines (`____`)

**Example input:**
```markdown
## Transcript

____

![](https://nam.loki.delve.office.com/api/v2/personaphoto?...)

Luna, Gabriella

0 minutes 8 seconds0:08

Luna, Gabriella 0 minutes 8 seconds

No worries. Um, so I know we want to touch base on.
```

**What it does:**
- Extracts attendee names from meeting file to build speaker mapping
- Parses raw Teams transcript section (block-by-block)
- Removes profile images, metadata, navigation text, duplicate lines
- Formats speakers as linked names with timestamps
- Replaces transcript section in original file
- Removes separator lines

**Requirements:**
- Meeting file must have an `## Attendees` section with linked profiles
- Meeting file must have a `## Transcript` section
- Python 3.6+

**Example:**
```bash
python clean_transcript.py ~/Documents/Obsidian/HPE/Meetings/2026-01-08\ -\ Meeting.md
```

**Output:**
```
✓ Cleaned transcript: 15 entries formatted
  - Will Colton at 0:03
  - Kashish Pahwa at 2:51
  - Will Colton at 2:54
  ... and 12 more
```

## clean_transcript_downloaded.py

Cleans **downloaded/exported** format from Teams transcript files.

**Usage:**
```bash
python clean_transcript_downloaded.py <meeting_file.md>
```

**Input format characteristics:**
- Combined speaker+timestamp: `**Last, First**   timestamp`
- Embedded image URLs before each speaker
- Meeting header (title, date, duration)
- No separator lines
- Line breaks preserved with double spaces

**Example input:**
```markdown
## Transcript

**Green and Magenta Design Discussion-20260113_133528-Meeting Recording**

January 13, 2026, 6:35PM

1h 16m 5s

![](file:////Users/kevin/Library/Group%20Containers/...)**Bennett, Ryan** started transcription

![](file:////Users/kevin/Library/...)**Bennett, Ryan**   0:03  
Yeah, well, the recording has begun.  
Recording has begun.

![](file:////Users/kevin/Library/...)**Tronkowski, Kevin**   0:08  
Alright, let's look at those pages.
```

**What it does:**
- Extracts attendee names from meeting file to build speaker mapping
- Parses downloaded transcript format (line-by-line)
- Removes file:// image references and meeting header
- Removes transcription start/stop markers
- Formats speakers as linked names with timestamps
- Preserves line breaks within speeches
- Replaces transcript section in original file

**Requirements:**
- Meeting file must have an `## Attendees` section with linked profiles
- Meeting file must have a `## Transcript` section
- Python 3.6+

**Example:**
```bash
python clean_transcript_downloaded.py ~/Documents/Obsidian/HPE/Meetings/2026-01-13\ -\ Meeting.md
```

**Output:**
```
✓ Cleaned transcript successfully
  Processed 79 entries
  First: Ryan Bennett at 1:05
  Last: Ryan Bennett at 1:15
```

## clean_transcript_docx.py

Cleans **plain text from .docx export** format.

**Usage:**
```bash
python clean_transcript_docx.py <meeting_file.md>
```

**Input format characteristics:**
- Plain text (NO markdown bold): ` Last, First   timestamp content`
- Leading space before speaker name
- Content on same line as speaker and timestamp
- Meeting header (title, date, duration)
- No image URLs (stripped during .docx to text conversion)
- May have "started/stopped transcription" markers

**Example input:**
```markdown
## Transcript

Forecasting Sync-20260114_210016UTC-Meeting Recording
January 14, 2026, 9:00PM
27m 18s
 Willmschen, Royce   0:09 Thank you.
 Oh, Kyu   0:12 Erase.
    0:43 Hello.
 Tronkowski, Kevin   1:03 OK.
 Willmschen, Royce stopped transcription
```

**What it does:**
- Extracts attendee names from meeting file to build speaker mapping
- Parses plain text transcript format (line-by-line)
- Removes meeting header and transcription markers
- Formats speakers as linked names with timestamps
- Replaces transcript section in original file

**Requirements:**
- Meeting file must have an `## Attendees` section with linked profiles
- Meeting file must have a `## Transcript` section
- Python 3.6+

**Typical workflow:**
```bash
# 1. Convert .docx to plain text
textutil -convert txt ~/Downloads/Meeting.docx -output ~/tmp/meeting-transcript.txt

# 2. Paste transcript into meeting file's ## Transcript section

# 3. Run script
python clean_transcript_docx.py ~/Documents/Obsidian/HPE/Meetings/2026-01-14\ -\ Meeting.md
```

**Output:**
```
✓ Cleaned transcript: 172 entries formatted
  - Royce Willmschen at 0:09
  - Kyu Oh at 0:12
  - Sue Huang at 0:50
  ... and 169 more
```

## clean_transcript_simple.py

Cleans **simple first-name marker** format with no timestamps.

**Usage:**
```bash
python clean_transcript_simple.py <meeting_file.md>
```

**Input format characteristics:**
- Speaker markers on separate line: `[FirstName]`
- No timestamps
- Content follows on next lines until next speaker
- May have unknown speakers like `[Speaker 3]` to skip
- Blank lines between speakers

**Example input:**
```markdown
## Transcript

[Kashish]  
Am I supposed to show it, but? Clearly, I am showing it.

[Stella]  
Somewhere. There is a gap.

[Speaker 3]  
Can you see it,

[Kevin]  
Yeah, yeah, yeah, you're exactly right.
```

**What it does:**
- Extracts attendee names from meeting file to build first name mapping
- Parses simple [Name] markers
- Skips unknown speakers (e.g., "Speaker 3")
- Maps first names to full names from attendee list
- Formats speakers as linked names (no timestamps)
- Joins multi-line content into single paragraphs
- Replaces transcript section in original file
- Creates backup (.bak) before modifying

**Requirements:**
- Meeting file must have an `## Attendees` section with linked profiles
- Meeting file must have a `## Transcript` section
- Python 3.6+

**Example:**
```bash
python clean_transcript_simple.py ~/Documents/Obsidian/HPE/Meetings/2026-01-23\ -\ Meeting.md
```

**Output:**
```
✓ Created backup: /path/to/Meeting.md.bak
✓ Cleaned 158 transcript entries
  - Stella Yun: 49 entries
  - Kashish Pahwa: 48 entries
  - Shaji Mohammed: 39 entries
  - Kevin Tronkowski: 22 entries
✓ Updated /path/to/Meeting.md
```

## Format Detection

When processing a meeting, detect which format to use:

```python
import re

def detect_transcript_format(transcript_text):
    """Detect which Teams transcript format is present."""
    
    # Check for simple first-name format: [Name]
    if re.search(r'^\[([A-Z][a-z]+)\]\s*$', transcript_text, re.MULTILINE):
        return 'simple'
    
    # Check for downloaded format: **Name**   timestamp
    if re.search(r'\*\*[A-Za-z]+, [A-Za-z]+\*\*\s+\d{1,2}:\d{2}', transcript_text):
        return 'downloaded'
    
    # Check for docx converted format: plain text with leading space
    # Pattern:  Name   timestamp content
    elif re.search(r'^\s+[A-Z][a-z]+, [A-Z][a-z]+\s+\d{1,2}:\d{2}\s+\w+', transcript_text, re.MULTILINE):
        return 'docx_converted'
    
    # Check for direct paste: Name on own line
    elif re.search(r'^[A-Za-z]+, [A-Za-z]+$', transcript_text, re.MULTILINE):
        return 'direct_paste'
    
    return 'unknown'
```

**Best practice**: Try formats in order:
1. Simple format (most basic, [Name] markers)
2. Downloaded format (most structured with timestamps)
3. .docx converted format (plain text)
4. Direct paste format (fallback)

## Output Format (All Scripts)

All scripts produce identical output format:

```markdown
## Transcript

**[[Last, First|First Last]]** timestamp

Content paragraph 1.

Content paragraph 2.

**[[Last, First|First Last]]** timestamp

More content.
```

**Note**: The simple format script omits timestamps since the source format has none:

```markdown
## Transcript

**[[Last, First|First Last]]**

Content paragraph.

**[[Last, First|First Last]]**

More content.
```

## Common Issues

### "No speakers found in attendee list"
- Ensure `# Attendees` section exists with proper `[[Last, First|First Last]]` links
- Run attendee extraction first if needed

### "No transcript entries parsed"
- Wrong script for transcript format (try the other one)
- Transcript may be empty or in unexpected format
- Check that `## Transcript` section exists

### Script doesn't modify file
- File permissions issue
- Check that file path is correct and accessible
