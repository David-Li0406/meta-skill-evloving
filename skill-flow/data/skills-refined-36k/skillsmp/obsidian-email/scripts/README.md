# Email Processing Scripts

Script for processing Obsidian notes containing email chains.

## process_email.py

Process email chain notes to extract participants, create People profiles, and generate summaries.

### Usage

```bash
python process_email.py <email_note_file.md>
```

### What It Does

1. **Extracts Participants**
   - Parses `From:` and `**From:**` headers in email chain
   - Extracts name and email address from each sender
   - Maintains list of unique participants in order of first appearance
   - Ignores To/CC lists (only processes senders)

2. **Creates/Updates People Profiles**
   - Checks if profile exists in `~/Documents/Obsidian/HPE/People/`
   - Creates new profiles with email addresses
   - Adds email to existing profiles if missing
   - Uses consistent format with obsidian-meeting skill

3. **Updates Participants Section**
   - Replaces empty `# Participants` section
   - Formats as linked list: `- [[Last, First|First Last]]`
   - Maintains order of first appearance in email chain

4. **Generates Summary**
   - Extracts key information from email thread
   - Creates structured summary with sections:
     - Overview: Topic and participant count
     - Key Points: Main discussion items
     - Action Items: Tasks and follow-ups
     - Context: Additional information
   - Identifies referenced tickets (e.g., GLCP-12345)
   - Updates `# Summary` section in note

### Email Format Support

The script handles multiple email header formats:

#### Format 1: Plain Text (Standard)
```
From: Last, First <email@domain.com>
Date: Monday, January 20, 2026 at 2:30 PM
To: Person <email@domain.com>
Subject: Topic
```

#### Format 2: Bold Markdown (Outlook)
```
**From:** Last, First <email@domain.com>
**Sent:** Monday, January 20, 2026 2:30 PM
**To:** Person <email@domain.com>
**Subject:** Topic
```

#### Format 3: Mixed
```
From: Last, First <email@domain.com>
Date: Monday, January 20, 2026 at 2:30 PM

---

**From:** Last, First <email@domain.com>
**Sent:** Monday, January 20, 2026 3:45 PM
```

All formats are automatically detected and parsed correctly.

### Name Format Handling

The script handles various name formats:

- **Simple**: `Smith, John` → `[[Smith, John|John Smith]]`
- **Middle name**: `Smith, John Michael` → `[[Smith, John Michael|John Michael Smith]]`
- **Multi-part last name**: `Van Der Berg, Jan` → `[[Van Der Berg, Jan|Jan Van Der Berg]]`

### Email Address Extraction

Extracts emails from these patterns:
- `<email@domain.com>` - Standard angle brackets
- `[email@domain.com](mailto:email@domain.com)` - Markdown links (preserved from paste)
- `email@domain.com` - Plain text

### Requirements

- Python 3.6 or higher
- Email note must have three sections:
  - `# Participants`
  - `# Summary`
  - `# Email Chain`
- People directory must exist at `../People/` relative to Notes directory

### Example

**Before:**
```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants


# Summary



# Email Chain

From: Smith, John <john.smith@hpe.com>
Date: Monday, January 20, 2026 at 2:30 PM

Message content here.
```

**Command:**
```bash
python process_email.py ~/Documents/Obsidian/HPE/Notes/2026-01-23\ -\ Email.md
```

**Output:**
```
✓ Extracted 1 unique participants
  - Smith, John (john.smith@hpe.com)
✓ Created 1 new People profiles
✓ Updated Participants section
✓ Generated summary (4 sections)
✓ Updated 2026-01-23 - Email.md
```

**After:**
```markdown
---
when: 2026-01-23
tags:
  - note
---
# Participants

- [[Smith, John|John Smith]]

# Summary

## Overview
Email thread regarding: [Subject]

Thread contains 1 messages from 1 participants.

## Key Points
- Discussion involves multiple stakeholders across teams

## Action Items
- Review email chain for specific action items and deadlines
- Follow up on open issues discussed

## Context
See full email chain below for complete discussion details.


# Email Chain

[Original content unchanged]
```

### Error Handling

**"No email chain found"**
- File must have `# Email Chain` section
- Check spelling and formatting of header

**"No participants extracted"**
- Ensure emails have `From:` headers
- Check format: `From: Last, First <email>`
- Name must include comma separator

**"People directory not found"**
- Check that `~/Documents/Obsidian/HPE/People/` exists
- Verify note is in correct location under Notes directory

**"Failed to create profile"**
- Check file permissions
- Ensure name format is valid (contains comma)

### Integration with Obsidian

The script maintains compatibility with Obsidian conventions:

1. **Wikilinks**: Uses `[[Last, First|First Last]]` format
2. **Tags**: People profiles get `person` tag
3. **Aliases**: Created for bidirectional linking
4. **Contact info**: Standardized format in People profiles

### Comparison with obsidian-meeting

Both skills share similar design patterns:

| Feature | obsidian-meeting | obsidian-email |
|---------|------------------|----------------|
| Input source | Teams screenshots | Email headers |
| Profile creation | From screenshot OCR | From From: headers |
| Summary generation | From transcript | From email chain |
| People format | Consistent | Consistent |
| Contact info | No email | Includes email |

### Future Enhancements

Potential improvements:
- AI-powered summary generation (GPT/Claude)
- Extract action items with natural language processing
- Parse meeting times/dates from email content
- Link to related meeting notes or other emails
- Extract and categorize discussed topics
