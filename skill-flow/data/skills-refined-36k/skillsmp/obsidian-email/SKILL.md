---
name: obsidian-email
description: Process Obsidian notes containing email chains. **Use when** user asks to "process email", "process email chain", "extract email participants", or "summarize email". Handles participant extraction from email headers, People profile creation, and email chain summarization.
---

# Obsidian Email Chain Processor

Extract participants from email chains, create People profiles, and generate summaries from email thread content.

## Quick Start

**"Process the email"** or **"Process email chain"** = Complete workflow:
1. Extract participants from email chain (From headers only, not To/CC)
2. Create missing People profiles
3. Update note with linked participant list
4. Generate summary from email chain content and insert into Summary section

This is the default behavior - all processing steps are performed automatically unless you request a specific step only.

## Capabilities

1. **Extract Participants**: Parse email From headers to identify senders
2. **Create People Profiles**: Generate linked profiles for email participants
3. **Generate Summaries**: Analyze email chain and create structured summary

## File Structure

Email chain notes use format: `YYYY-MM-DD - topic name.md` in `~/Documents/Obsidian/HPE/Notes/`

### Expected Structure

```markdown
---
when: YYYY-MM-DD
tags:
  - note
---
# Participants


# Summary



# Email Chain

[Raw email content here]
```

## Finding Email Notes

```bash
# Today's email notes
find ~/Documents/Obsidian/HPE/Notes -name "$(date +%Y-%m-%d)*.md"

# Search for files with "Email Chain" section
find ~/Documents/Obsidian/HPE/Notes -type f -name "*.md" -exec grep -l "# Email Chain" {} \;

# Specific email note by name
find ~/Documents/Obsidian/HPE/Notes -iname "*ops*ramp*.md"
```

## Processing Workflow

### Step 1: Extract Participants from Email Chain

Parse the email chain to extract unique senders:

1. Look for `From:` or `**From:**` headers in email chain
2. Extract name in "Last, First" format (e.g., "Vobbilisetty, Suresh")
3. Build list of unique senders (ignore To/CC lists)
4. Maintain chronological order (first sender first)

**Email header patterns to match:**
```
From: Last, First <email@hpe.com>
**From:** Last, First <email@hpe.com>
```

### Step 2: Create/Update People Profiles

For each unique sender:

1. Check if profile exists: `~/Documents/Obsidian/HPE/People/Last, First.md`
2. If missing, create new profile:
   ```markdown
   ---
   tags:
     - person
   ---
   
   # Last, First
   
   ## Contact
   - Email: email@hpe.com
   
   ## Aliases
   - [[Last, First|First Last]]
   ```
3. Extract email address from From header
4. If profile exists but email missing, add it to Contact section

### Step 3: Update Participants Section

Replace empty `# Participants` section with linked list:

```markdown
# Participants

- [[Vobbilisetty, Suresh|Suresh Vobbilisetty]]
- [[Sadananda, Ravi Kiran Srirangam|Ravi Kiran Sadananda]]
- [[Daniel, Binu|Binu Daniel]]
- [[Vanteru, Bhanu|Bhanu Vanteru]]
```

**Format rules:**
- Link format: `[[Last, First|First Last]]`
- Listed in order of first appearance in email chain
- One participant per line with bullet point

### Step 4: Generate Email Chain Summary

Analyze the email thread and generate a structured summary:

1. Read the entire email chain content
2. Identify key topics, issues, action items, and decisions
3. Generate structured summary with sections:
   - **Overview**: Brief description of the email thread topic
   - **Key Issues**: Main problems or concerns discussed
   - **Action Items**: Tasks assigned or next steps identified
   - **Timeline**: Important dates or deadlines mentioned
   - **Participants' Perspectives**: Key points from different senders (optional)

**Summary format:**
```markdown
# Summary

## Overview
Brief description of what this email chain is about.

## Key Issues
- Issue 1: Description
- Issue 2: Description

## Action Items
- [ ] Person to do X by date
- [ ] Team to review Y

## Timeline
- Date: Event or deadline

## Important Context
Any other relevant information.
```

### When to Use

- User requests "process email", "extract participants", or "summarize email"
- Note file contains `# Email Chain` section with email content
- After creating note from copied email thread

## Script Usage

```bash
# Process email chain note
python ~/.copilot/skills/obsidian-email/scripts/process_email.py "email-note-file.md"
```

**The script automatically:**
1. Parses email headers to extract unique senders
2. Creates missing People profiles with email addresses
3. Updates Participants section with linked names
4. Generates comprehensive summary from email content
5. Updates Summary section in the note

**Example output:**
```
✓ Extracted 5 unique participants
  - Vobbilisetty, Suresh (suresh.vobbilisetty@hpe.com)
  - Sadananda, Ravi Kiran Srirangam (ravikiransrirangam.sadananda@hpe.com)
  - Daniel, Binu (binu.daniel@hpe.com)
  - Vanteru, Bhanu (bhanu.vanteru@hpe.com)
  - Yun, Stella (xiaoyang.yun@hpe.com)
✓ Created 2 new People profiles
✓ Updated Participants section
✓ Generated summary (4 sections)
✓ Updated email note
```

## Email Header Formats

The script handles multiple email header formats:

### Format 1: Plain text with colon
```
From: Last, First <email@hpe.com>
Date: Friday, January 23, 2026 at 7:43 AM
To: Person1 <email1@hpe.com>, Person2 <email2@hpe.com>
```

### Format 2: Bold markdown
```
**From:** Last, First <email@hpe.com>
**Sent:** Friday, January 23, 2026 5:42 AM
**To:** Person1 <email1@hpe.com>
```

### Format 3: Mixed (Outlook style)
```
From: Last, First <email@hpe.com>
Date: Friday, January 23, 2026 at 7:43 AM

---

**From:** Last, First <email@hpe.com>
**Sent:** Friday, January 23, 2026 12:48 PM
```

## Name Format Handling

The script handles various name formats:

- **Standard**: `Last, First` → `[[Last, First|First Last]]`
- **Middle names**: `Last, First Middle` → `[[Last, First Middle|First Middle Last]]`
- **Multi-part last names**: `Last Name, First` → `[[Last Name, First|First Last Name]]`

## Email Address Extraction

Extracts email from patterns:
- `<email@domain.com>` - Standard format
- `[email@domain.com](mailto:...)` - Markdown link format
- `email@domain.com` - Plain text format

## Integration with People Profiles

The script maintains consistency with existing People profiles:

1. **Check existing profiles** before creating new ones
2. **Add email to Contact section** if profile exists but email missing
3. **Use same formatting** as obsidian-meeting skill for consistency
4. **Create aliases section** for proper Obsidian linking

## Example Workflow

```bash
# 1. Find the email note
find ~/Documents/Obsidian/HPE/Notes -iname "*ops*ramp*email*.md"

# 2. Process it
python ~/.copilot/skills/obsidian-email/scripts/process_email.py \
  "~/Documents/Obsidian/HPE/Notes/2026-01-23 - Ops Ramp Issues Email.md"

# Output shows progress and results
```

## Common Issues

### "No email chain found"
- Ensure the note has a `# Email Chain` section
- Check that email content is below the header

### "No senders extracted"
- Verify email has From: headers
- Check email format matches supported patterns

### "Failed to parse name"
- Name should be in "Last, First" format in From header
- Script will skip invalid formats and continue

## Related Skills

- **obsidian-meeting**: Process meeting transcripts with similar participant extraction
- Both skills maintain consistent People profile format and linking conventions
