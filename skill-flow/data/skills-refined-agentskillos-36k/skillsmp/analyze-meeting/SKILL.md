---
name: analyze-meeting
description: Extract insights from a meeting transcript including summary, action items, decisions, and key topics. Use when the user wants to analyze a transcript, extract meeting notes, find action items, or summarize a meeting.
---

# Analyze Meeting Transcript

Parse a VTT transcript and extract structured insights.

## Instructions

1. Read the transcript from `projects/{project}/transcripts/{date}.vtt`
2. Parse the VTT format and extract the conversation
3. Analyze the content and extract:

### Required Extractions

- **Summary**: 2-3 sentence overview of the meeting
- **Attendees**: List of participants (from speaker labels like "Speaker 1:", names, etc.)
- **Key Topics**: Main subjects discussed (3-7 bullet points)
- **Decisions Made**: Any explicit decisions or agreements reached
- **Action Items**: Tasks mentioned with:
  - Task description
  - Owner (if mentioned)
  - Deadline (if mentioned)
- **Open Questions**: Unresolved questions or concerns raised
- **Next Steps**: Follow-up items or future meeting topics

4. Save the analysis to `projects/{project}/analysis/{date}.json`

## VTT Format Reference

WebVTT files contain timestamped captions:
```
WEBVTT

00:00:00.000 --> 00:00:05.000
Speaker 1: Hello everyone, let's get started.

00:00:05.000 --> 00:00:12.000
Speaker 2: Sure, first item on the agenda is...
```

Extract speaker names from labels like "Speaker 1:", "John:", "[John Smith]", etc.
