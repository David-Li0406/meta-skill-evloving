# Video Transcript Analyzer Skill

## Overview
This Claude Skill analyzes customer interview and feedback call transcripts to generate comprehensive structured documents with thematic analysis, key insights, chapter markers, and full transcripts.

## What It Does
Takes video transcripts (SRT or plain text format) and produces a single markdown document containing:
- Video link (if provided)
- Call summary (2-3 paragraphs)
- Key verbatim quotes from customer/interviewee (5-8 quotes)
- Topical breakdown with detailed context bullets
- Chapter markers with timestamps (if SRT format)
- Complete original transcript

## When Claude Will Use This Skill
Claude automatically uses this skill when:
- You provide an SRT or plain text transcript file
- You say "analyze this customer call/interview"
- You ask for "chapter markers" or "topical breakdown"
- You want to extract insights from a recorded conversation

## How to Use

### Basic Usage
```
Upload: customer-call.srt
Message: "Can you analyze this transcript?"
```

### With Video Link
```
Upload: transcript.srt
Message: "Here's the video: https://zoom.us/rec/abc123 - please analyze"
```

### Without Video Link
If you don't provide a video URL initially, Claude will prompt you for one:
```
Upload: transcript.srt
Message: "Analyze this transcript"

Claude: "Do you have a link to the video recording? If so, please share it and I'll include it in the analysis."

You: "https://vimeo.com/123456" (or "No, not available")
```

### Timestamp Adjustment
```
Upload: transcript.srt
Message: "I cut off the first 55 seconds, can you adjust the timestamps and analyze?"
```

## Example Output Structure

**Output filename:**
- With last name: `YYYY-MM-DD_FirstName_LastName_CompanyName.md`
  - Example: `2025-11-15_Martin_McKenna_HubSpot.md`
- Without last name: `YYYY-MM-DD_FirstName_CompanyName.md`
  - Example: `2025-11-11_Emma_Ax.md`

```markdown
# Customer Call Title

## Video
[Link or "Not provided"]

## Call Summary
[2-3 paragraphs covering who, what, why, and outcomes]

## Key Quotes
> "Verbatim quote from customer"
>
> — Speaker, context

[5-8 total quotes]

## Topical Breakdown

**00:02:57 - Topic Title** (if SRT)
Brief description of topic.
- Detailed bullet with specifics
- Another bullet with context
- Impact or consequence
[3-6 bullets per topic]

## Full Transcript
[Complete original transcript]
```

## Features

### Smart Format Detection
- Automatically detects SRT (with timestamps) vs plain text
- Parses timestamps and dialogue from SRT files
- Handles various transcript formats

### Thematic Organization
- Groups related topics even if discussed at different times
- Organizes chronologically for intro/context
- Switches to thematic grouping for main issues
- Ideal for product feedback and research synthesis

### Verbatim Quotes
- Preserves exact customer language (no paraphrasing)
- Selects quotes showing emotion, specifics, and impact
- Provides brief context for each quote
- Focuses on customer voice, not interviewer questions

### Comprehensive Output
- Everything in one file: analysis + original transcript
- Easy to share with team members
- Reference original transcript while reading analysis
- Includes video link for full context

## Files in This Skill

- **Skill.md** - Main skill definition with instructions for Claude
- **resources/EXAMPLES.md** - Full annotated examples of inputs and outputs
- **resources/REFERENCE.md** - Detailed guide for transcript analysis patterns
- **README.md** - This file (usage documentation)

## Tips for Best Results

### Provide Context
If participant names aren't clear in transcript, tell Claude:
```
"This is a call between Hannah (HubSpot researcher) and Emma (customer admin)"
```

### Request Timestamp Adjustments
If you edited the video:
```
"I removed the first 2 minutes where no one was talking, subtract 120 seconds from all timestamps"
```

### Specify Focus Areas
If you want emphasis on certain topics:
```
"Focus on pain points and feature requests in your analysis"
```

### Plain Text Format
If providing plain text without speaker labels:
```
"This is a transcript of an interview. Interviewer questions start with 'Q:' and responses with 'A:'"
```

## What This Skill Doesn't Do

- Won't create transcripts from audio/video files (needs pre-transcribed text)
- Won't translate or clean up transcript errors
- Won't add information not present in the transcript
- Won't paraphrase quotes (always verbatim)
- Won't remove sensitive information (unless explicitly requested)

## Output Format

All outputs are markdown-formatted documents suitable for:
- Sharing with product/research teams
- Publishing to internal wikis or documentation
- Converting to PDF or other formats
- Using as input for further analysis

## Privacy and Security

- Customer names and company information are preserved as-is
- Warn if transcript contains credentials or sensitive PII
- Don't modify quotes or sanitize content
- Full transcript always included (nothing redacted by default)

## Examples

See `resources/EXAMPLES.md` for:
- Complete SRT analysis with all sections
- Plain text transcript analysis
- Minimal input handling

See `resources/REFERENCE.md` for:
- Detailed format specifications
- Quote selection guidelines
- Topic organization strategies
- Quality check criteria
