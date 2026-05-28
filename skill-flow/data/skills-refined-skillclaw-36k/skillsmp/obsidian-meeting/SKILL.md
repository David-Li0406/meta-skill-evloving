---
name: obsidian-meeting
description: Process Obsidian meeting notes from Teams transcripts. **Use when** user asks to "process meeting", "process obsidian meeting", "clean up transcript", "extract attendees", or "summarize meeting". Handles attendee extraction from screenshots, People profile creation, transcript cleaning/formatting, and meeting summary generation. Supports date references and batch processing.
---

# Obsidian Meeting Attendee Processor

Extract attendees from Teams screenshots, create People profiles with aliases, update meeting notes with linked lists, clean up Microsoft Teams transcripts, and generate meeting summaries.

## Quick Start

**"Process the obsidian meeting"** or **"Process meeting"** = Complete workflow:
1. Extract attendees from Teams screenshot
2. Create missing People profiles
3. Update meeting note with linked attendee list
4. Clean up transcript (remove images, metadata, format speakers)
5. Generate meeting summary from transcript:
   - **If existing summary sections found** (e.g., `# Decisions`, `# Open questions`, `# Meeting notes`): Augment them with additional detail from transcript
   - **If no existing summary found**: Insert new structured summary in `# Notes` section

This is the default behavior - all processing steps are performed automatically unless you request a specific step only.

## Capabilities

1. **Extract Attendees**: Process Teams screenshots to identify meeting participants
2. **Create People Profiles**: Generate linked profiles with proper aliases
3. **Clean Transcripts**: Format Microsoft Teams transcripts for Obsidian readability
4. **Generate Summaries**: Analyze cleaned transcript and create structured meeting notes
5. **Augment Existing Summaries**: Enhance pre-existing summary sections with additional detail from transcript analysis

## Additional Resources

- **[reference.md](reference.md)** - Obsidian markdown syntax reference for meeting notes
- **[examples.md](examples.md)** - Complete examples of formatted meeting notes
- **[scripts/README.md](scripts/README.md)** - Documentation for utility scripts

## Finding Meetings

Meeting files use format: `YYYY-MM-DD - meeting name.md` in `~/Documents/Obsidian/HPE/Meetings/`

### Find by date reference

```bash
# Today's meetings
find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*.md"

# Specific date
find ~/Documents/Obsidian/HPE/Meetings -name "2026-01-05*.md"

# Date range (last week)
find ~/Documents/Obsidian/HPE/Meetings -name "*.md" -newermt "$(date -v-7d +%Y-%m-%d)" ! -newermt "$(date +%Y-%m-%d)"

# Date range (specific week)
find ~/Documents/Obsidian/HPE/Meetings -name "*.md" -newermt "2026-01-01" ! -newermt "2026-01-08"
```

### Find by name

```bash
# Case-insensitive search
find ~/Documents/Obsidian/HPE/Meetings -iname "*aruba*interlock*.md"
```

### Batch processing

For multiple meetings, process each sequentially, reporting progress.

## Processing Workflow

### Step 1: Extract Attendees from Image

1. Locate image reference: `![[SCR-YYYYMMDD-xxxxx.png]]` (in "Notable Attendees" section)
2. View image from `~/Documents/Obsidian/HPE/Media/`
3. Extract names in "Last, First" format:
   - **In Meeting**: Present attendees (green checkmarks in image)
   - **Invited/Other**: Invited/declined/mentioned in transcript

### Step 2: Extract Avatar Images

Extract individual avatar images from the screenshot for each attendee:

1. Get image dimensions: `sips -g pixelWidth -g pixelHeight SCR-YYYYMMDD-xxxxx.png`
2. Extract each avatar using sips crop (avatars are typically ~40x40 pixels):
   ```bash
   # Example for first attendee
   sips -c 40 40 --cropOffset Y_OFFSET X_OFFSET SCR-YYYYMMDD-xxxxx.png \
     --out Last-First-avatar.png
   ```
3. Typical layout in Teams screenshots:
   - Avatars are on the left side (~16 pixels from left edge)
   - Spaced vertically (typically ~52-54 pixels between avatars)
   - First avatar starts around y=12-20 pixels from top
4. Save avatars with naming convention: `{Last}-{First}-avatar.png` in Media folder

**Example extraction commands:**
```bash
cd ~/Documents/Obsidian/HPE/Media

# First attendee (top of list)
sips -c 40 40 --cropOffset 12 12 SCR-20260113-jshz.png \
  --out Tronkowski-Kevin-avatar.png

# Second attendee (~54 pixels down)
sips -c 40 40 --cropOffset 66 12 SCR-20260113-jshz.png \
  --out De-Anirban-avatar.png

# Third attendee (~54 pixels down)
sips -c 40 40 --cropOffset 120 12 SCR-20260113-jshz.png \
  --out Holden-Edward-avatar.png
```

### Step 3: Create People Profiles with Avatars

Check `~/Documents/Obsidian/HPE/People/{Last}, {First}.md` - create if missing:

```markdown
---
aliases:
  - {First} {Last}
tags:
  - People
---
![[{Last}-{First}-avatar.png]]
```

**Important**: Only add avatar if the profile doesn't already have one. Check for existing `![[` image reference in the file first.

Example: `Pahwa, Kashish.md` → alias "Kashish Pahwa" + avatar image

### Step 4: Update Meeting Note

Replace image reference with attendee list using link format `[[{Last}, {First}|{First} {Last}]]`:

```markdown
# Attendees

## In Meeting (5)
- [[Tronkowski, Kevin|Kevin Tronkowski]]
- [[Pahwa, Kashish|Kashish Pahwa]]

## Invited/Other Participants (3)
- [[Luna, Gabriella|Gabriella Luna]]
```

**Important**: Remove the `![[SCR-YYYYMMDD-xxxxx.png]]` image reference after extracting attendees.

## Directory Structure

```
~/Documents/Obsidian/HPE/
├── Meetings/YYYY-MM-DD - name.md
├── People/{Last}, {First}.md
└── Media/SCR-YYYYMMDD-xxxxx.png
```

## Common Patterns

**"Process the obsidian meeting"** or **"Process meeting"**
- Default: Complete workflow (attendees + profiles + transcript)
- Finds most recent meeting or prompts for clarification
- Example: "Process the obsidian meeting" → processes today's latest meeting with all steps

**"Process the meeting with transcript from ~/Downloads/Meeting.docx"**
1. Convert .docx to text: `textutil -convert txt ~/Downloads/Meeting.docx -output ~/tmp/transcript.txt`
2. Add transcript to meeting file's `## Transcript` section
3. Run full workflow (extract attendees, create profiles, clean transcript, generate summary)
4. Use Format 3 cleaner (`clean_transcript_docx.py`) for plain text format

**"Process today's aruba meeting"**
1. Find: `find ~/Documents/Obsidian/HPE/Meetings -name "$(date +%Y-%m-%d)*aruba*.md"`
2. Extract attendees from image
3. Create missing People profiles
4. Update meeting note
5. Clean up transcript

**"Process all meetings from last week"**
1. Find: `find ~/Documents/Obsidian/HPE/Meetings -name "*.md" -newermt "$(date -v-7d +%Y-%m-%d)"`
2. Process each meeting sequentially (full workflow)
3. Report: "Processed 5 meetings, created 12 new profiles, cleaned 5 transcripts"

**"Process the 2026-01-05 aruba interlock meeting"**
1. Find: `find ~/Documents/Obsidian/HPE/Meetings -name "2026-01-05*aruba*.md"`
2. Single meeting - full workflow

**"Just clean up the transcript"** (specific step only)
1. Skip attendee processing
2. Only clean transcript section

## Important Rules

- Always check existing profiles before creating
- Preserve existing profile content when found
- Use exact format: filename `{Last}, {First}.md`, alias `{First} {Last}`
- Include counts in section headers: `## In Meeting (5)`
- Process meetings in date order when batch processing

---

## Transcript Cleanup

Clean up Microsoft Teams transcripts by removing profile pictures, metadata, and formatting for Obsidian readability.

### Two Transcript Formats

Microsoft Teams transcripts can be obtained in two different formats:

#### Format 1: Direct Paste from Teams (Original Format)
**Source**: Copy-paste directly from Teams meeting transcript view

**Characteristics**:
- Speaker names on their own line: `Last, First`
- Timestamp line with verbose format: `0 minutes 3 seconds0:03`
- Duplicate speaker+timestamp line: `Last, First 0 minutes 3 seconds`
- Profile image URLs on separate lines
- Metadata and navigation text
- Separator lines `____`

**Example:**
```markdown
## Transcript

____

![](https://nam.loki.delve.office.com/api/v2/personaphoto?AadObjectId=...)

Luna, Gabriella

0 minutes 8 seconds0:08

Luna, Gabriella 0 minutes 8 seconds

No worries. Um, so I know we want to touch base on.
```

**Script**: `clean_transcript.py` (existing)

#### Format 2: Downloaded/Exported from Teams (New Format)
**Source**: Downloaded VTT file converted to text, or exported from Teams

**Characteristics**:
- Combined speaker and timestamp on one line: `**Bennett, Ryan**   0:03`
- Embedded image references before each speaker: `![](file:////Users/kevin/Library/Group%20Containers/...)`
- Meeting header info (title, date, duration)
- No separator lines
- Content follows immediately after speaker line

**Example:**
```markdown
## Transcript

**Green and Magenta Design Discussion-20260113_133528-Meeting Recording**

January 13, 2026, 6:35PM

1h 16m 5s

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image002.jpg)**Bennett, Ryan** started transcription

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image004.jpg)**Bennett, Ryan**   0:03  
Yeah, well, the recording has begun.  
Recording has begun.

![](file:////Users/kevin/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image006.jpg)**Tronkowski, Kevin**   0:08  
Alright, let's look at those pages.
```

**Script**: `clean_transcript_downloaded.py` (new - for downloaded format)

#### Format 3: Plain Text from .docx Export (Converted Format)
**Source**: Teams transcript exported to .docx, then converted to plain text via `textutil` or similar

**Characteristics**:
- Plain text format (NO bold markdown): ` Last, First   timestamp content`
- Leading space before speaker name
- Meeting header info (title, date, duration) at top
- No image references (stripped during conversion)
- Content on same line as speaker and timestamp
- May have "started/stopped transcription" markers

**Example:**
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

**Script**: `clean_transcript_docx.py` (new - for .docx converted format)

#### Format 4: Simple First Name Markers (No Timestamps)
**Source**: Simple transcript format with basic speaker markers

**Characteristics**:
- Speaker markers on own line: `[FirstName]`
- No timestamps
- Content on following lines until next speaker marker
- May have unknown speakers like `[Speaker 3]` to skip
- Blank lines between speakers

**Example:**
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

**Script**: `clean_transcript_simple.py` (new - for simple first-name format)

### When to Use

- User requests "clean up transcript", "process transcript", or "format transcript"
- Meeting note contains raw Teams transcript with image URLs and metadata
- After processing attendees, offer to clean transcript

### Transcript Cleanup Workflow

**Auto-detect format and use appropriate script:**

```bash
# For Format 1 (direct paste from Teams)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript.py "meeting-file.md"

# For Format 2 (downloaded/exported)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript_downloaded.py "meeting-file.md"

# For Format 3 (.docx converted to text)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript_docx.py "meeting-file.md"

# For Format 4 (simple first-name markers)
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript_simple.py "meeting-file.md"
```

**Detection logic:**
1. Check for pattern `[FirstName]` on own line (no timestamp following) → Format 4 (simple markers)
2. Check for pattern `**Last, First**   timestamp` → Format 2 (downloaded with markdown bold)
3. Check for pattern ` Last, First   timestamp content` (leading space, no bold) → Format 3 (.docx converted)
4. Check for pattern `Last, First` on own line + timestamp on next line → Format 1 (direct paste)
5. If unsure, try Format 2 first, then Format 3, then Format 4, then Format 1

The script automatically:
1. Extracts the transcript section
2. Parses speakers, timestamps, and content
3. Removes all metadata, images, and unwanted formatting
4. Replaces the transcript with clean formatted output
5. Removes separator lines (`____`)

**What the script does:**
- Reads attendee list to build speaker name mapping
- Parses raw Teams transcript block-by-block
- Extracts clean timestamps from complex format (e.g., "0 minutes 3 seconds0:03" → "0:03")
- Skips all unwanted content (images, metadata, duplicates, separators)
- Formats as: `**[[Last, First|First Last]]** timestamp` + content
- Writes back to original file

**Example usage:**
```bash
# Process single meeting
python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript.py \
  ~/Documents/Obsidian/HPE/Meetings/2026-01-08\ -\ SIC-PCE\ Syncup.md

# Output:
# ✓ Cleaned transcript: 15 entries formatted
#   - Will Colton at 0:03
#   - Kashish Pahwa at 2:51
#   - Will Colton at 2:54
#   ... and 12 more
```

### Transcript Format Rules

- **Speaker format**: `**[[Last, First|First Last]]** timestamp`
- **Timestamp format**: Keep original clean timestamp (e.g., `0:03`, `2:26`, `28:56`)
- **Paragraph breaks**: Blank line between speakers
- **Multi-paragraph speeches**: Blank line between paragraphs from same speaker at same timestamp
- **Section header**: Use `## Transcript` (not `# Transcript`)
- **No separators**: Remove all `____` lines
- **No images**: Remove all profile picture URLs and attendee screenshot references

### Items to Remove from Raw Transcript

- Profile picture image URLs (`![](https://nam.loki.delve.office.com/api/v2/personaphoto?...`)
- Navigation text ("Transcript. Use arrow keys to navigate...")
- Metadata lines ("AI-generated content may be incorrect")
- "started transcription" / "stopped transcription" markers
- Duplicate timestamp labels (e.g., "0 minutes 3 seconds0:03")
- Duplicate "Speaker timestamp" lines (e.g., "Luna, Gabriella 0 minutes 8 seconds")
- Speaker initials without context (e.g., "PK", "SM")
- Separator lines (`____`)
- Empty blocks

### Example: Before and After

**Before (Raw Teams):**
```markdown
## Transcript

____

Transcript. Use arrow keys...

AI-generated content may be incorrect

![](https://nam.loki.delve.office.com/api/v2/personaphoto?AadObjectId=...)

Luna, Gabriella

0 minutes 8 seconds0:08

Luna, Gabriella 0 minutes 8 seconds

No worries. Um, so I know we want to touch base on.

![](https://nam.loki.delve.office.com/api/v2/personaphoto?AadObjectId=...)

Colton, Will

0 minutes 19 seconds0:19

Colton, Will 0 minutes 19 seconds

And had some things they want it cleaned up.
```

**After (Cleaned):**
```markdown
## Transcript

**[[Luna, Gabriella|Gabriella Luna]]** 0:08

No worries. Um, so I know we want to touch base on.

**[[Colton, Will|Will Colton]]** 0:19

And had some things they want it cleaned up.
```

### Processing Combined Workflow

**Default behavior** when user says "process meeting" or "process the obsidian meeting":

1. Extract and process attendees from screenshot
2. **Extract individual avatar images** from screenshot for each attendee
3. Create missing People profiles with avatars (only add if not already present)
4. Update meeting note with attendee list
5. **Remove attendee screenshot** reference from meeting note
6. **Run transcript cleaner script**: `python ~/.copilot/skills/obsidian-meeting/scripts/clean_transcript.py "meeting-file.md"`
7. **Generate meeting summary from cleaned transcript**:
   - **Check for existing summary sections** (`# Decisions`, `# Open questions`, `# Agenda`, `# Meeting notes`, etc.)
   - **If found**: Augment existing sections with additional detail, add new subsections as needed
   - **If not found**: Insert new structured summary in `# Notes` section
8. **Insert or augment summary** based on detection results

**Individual steps** only performed when specifically requested:
- "Just extract attendees" → skip transcript cleanup and summary
- "Just clean up the transcript" → only run transcript cleaner script
- "Just summarize the meeting" → only generate summary from existing transcript
- "Augment the meeting summary" → enhance existing summary sections with transcript analysis
- "Create people profiles" → only profile creation

**Expected Results:**
- Attendee list with linked profiles and counts
- Individual avatar images extracted for each attendee (saved as `{Last}-{First}-avatar.png`)
- People profiles updated with avatars (only if they don't already have one)
- Clean, formatted transcript with speaker links and timestamps
- Comprehensive meeting summary (either new or augmented)
- No image references (attendee screenshots or speaker profile images)
- No temporary files (script cleans up automatically)
- All existing summary content preserved when augmenting

Use the full workflow by default unless the user explicitly requests a single step.

---

## Meeting Summary Generation

When a transcript is present, automatically generate a summary and insert/augment it in the Notes section.

### Summary Workflow

1. **Read cleaned transcript** (after cleanup step completes)
2. **Analyze content** to identify:
   - Meeting purpose/topic
   - Key discussion points and decisions
   - Technical details and requirements
   - Action items and follow-ups
   - Important context or background
3. **Check for existing summary content**:
   - Look for existing sections: `# Decisions`, `# Open questions`, `# Agenda`, `# Meeting notes`, `# Notes`, `# Take Aways`, `# Actions`
   - Identify which sections already exist and contain content
4. **Generate structured summary** in markdown format
5. **Augment or insert** based on existing content (see Augmentation Strategy below)

### Augmentation Strategy: Handling Existing Summaries

**Detection**: Check if any of these sections already exist with content:
- `# Decisions`
- `# Open questions`  
- `# Agenda`
- `# Meeting notes` (with subsections like `### Meeting tools and automation`)
- `# Notes` (with content beyond templates)
- `# Take Aways`
- `# Actions`

**When existing summary sections are found:**

1. **Keep all existing sections intact** - Do not replace or remove them
2. **Analyze existing content** to understand what's already covered
3. **Generate supplementary content** from the transcript that:
   - Adds detail to existing bullet points
   - Identifies topics not yet covered in existing sections
   - Extracts additional decisions, questions, or action items
4. **Augment each existing section** by:
   - Adding new items discovered from transcript analysis
   - Expanding brief items with additional context from transcript
   - Preserving all original content (never remove existing items)
5. **Fill in template sections** if they exist but are empty (e.g., `# Subject`, `# Take Aways`, `# Actions`)

**When NO existing summary sections are found:**

Insert a new structured summary in the `# Notes` section (standard workflow):

```markdown
# Notable Attendees

## In Meeting (5)
- [[Tronkowski, Kevin|Kevin Tronkowski]]
...

# Subject
- 

# Notes

## Meeting Purpose
[Generated summary content starts here]

## Key Discussion Points
...

## Media
-
```

### Augmentation Example

**Before augmentation:**
```markdown
# Decisions

- Enable facilitator agent for meeting recording.
- Merge secret scanning feature.

# Open questions

- Agreement needed on CXL cluster usage.

# Meeting notes

### Security automation

- Will confirmed changes were implemented.
```

**After augmentation (from transcript analysis):**
```markdown
# Decisions

- Enable facilitator agent for meeting recording and automated notes.
- Merge secret scanning feature and use Copilot for repo integration.
- Create separate story for secret scanning in all repos.
- Test agent-side work and coordinate for further development.
- Submit I18N header PR and hold review until implementation is ready.

# Open questions

- Agreement needed on CXL cluster usage for forecasting.
- Resolve ML pipeline build failures due to runner disk space.
- Investigate separating user input from prompts to pass Amazon guardrails.
- Analyze prompt aspects that trigger Amazon guardrails.

# Meeting notes

### Security automation

- Will confirmed that the changes based on Ryan's feedback have been implemented and successfully tested, and the secret scanning job received final approval from Kevin.

### Forecasting updates

- Kyu relayed the forecasting update to the green and magenta teams and noted ongoing discussions about using the CXL cluster
- Kyu reported that the ML forecasting PR checks are failing due to build space issues, and Thomas is working on adjustments to resolve this
```

**Note**: Items are added or enhanced, never removed. Original content is preserved.

### Summary Format Template

**For meetings WITHOUT existing summaries:**

```markdown
# Notes

## Meeting Purpose
[Brief 1-2 sentence overview of meeting topic]

## Key Discussion Points

### [Topic Area 1]
- **Current state**: [What exists now]
- **Requirements**: [What's needed]
- **Proposed solution**: [Approach discussed]
- **Status**: [Current progress/decisions]

### [Topic Area 2]
[Repeat structure for additional topics]

### [Team/Participant Context]
- Key stakeholders and their roles
- Relevant organizational information

### Follow-up Plans
- Action items with owners
- Timeline commitments
- Dependencies or blockers noted

### Additional Context
- Travel issues or attendance notes
- Related discussions or background
```

**For meetings WITH existing summaries (augmentation mode):**

Preserve existing section structure and add/enhance content within those sections:

```markdown
# Decisions
[Existing items kept as-is]
[New decisions extracted from transcript added below]

# Open questions
[Existing questions kept as-is]
[New questions from transcript added below]

# Agenda
[Usually kept as-is since it's pre-meeting]

# Meeting notes
[Existing subsections kept as-is]
[Enhance with additional detail from transcript]
[Add new subsections for topics not yet covered]

# Subject
[Fill in if empty, otherwise keep existing]

# Take Aways
[Fill in if empty or augment with key learnings from transcript]

# Actions
[Keep existing, add action items discovered in transcript]
```

### Summary Guidelines

- **Detect existing content**: Always check for pre-existing summary sections before generating
- **Augment, don't replace**: When existing sections are found, add to them rather than replacing
- **Be comprehensive**: Capture all significant discussion points from the transcript
- **Use bullet points**: Easy to scan and reference
- **Include specifics**: Names, systems, requirements, timelines
- **Maintain structure**: Use consistent heading hierarchy matching existing format
- **Preserve technical details**: System names, technologies, requirements
- **Note action items**: Who, what, when
- **Keep context**: Background information that adds understanding
- **Match existing style**: If existing summaries use a certain bullet format or structure, maintain consistency

### Example Summary Structure

Based on actual meeting (OpsRamp Collector - 2026-01-05):

```markdown
# Notes

## Meeting Purpose
Discussion about using OpsRamp Collector for SIC (Sustainability Insight Center) to collect power consumption data from non-centrally managed Aruba devices.

## Key Discussion Points

### OpsRamp Collector for SIC
- **Current state**: SIC already supports Aruba devices through Aruba Central
- **New requirement**: Need to support Aruba devices NOT managed by Aruba Central
- **Proposed solution**: Use OpsRamp Collector as lightweight solution
- **Status**: Very early stage - need POC to validate feasibility

### SIC Engineering Context
- Royce Willmschen: Engineering Manager for SIC
- Active roadmap item for non-central managed Aruba device support

### Follow-up Plans
- Schedule follow-up meeting in early February to review POC results
- Royce and Kevin (SIC team) to work on POC
```
