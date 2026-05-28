---
name: transcript-summary
description: Create structured markdown summaries from presentation, talk, or video transcripts. Use when the user provides a transcript and asks to summarize, analyze, or create notes from a presentation, lecture, conference talk, or video. Triggers on phrases like "summarize this transcript", "create notes from this talk", "overview of this presentation", or when a transcript file is uploaded with a request for analysis.
---

# Transcript Summary Skill

Transform presentation transcripts into structured, actionable markdown summaries.

## Output Structure

Create a markdown file with these sections in order:

### Frontmatter
- `#` header: Event/video name (if known)
- Session number and topic (if known)  
- Presenter name (if stated)
- `#_inbox` tag on its own line
- Horizontal rule before Executive Summary

### Executive Summary (## header)
Two paragraphs:
1. Main framework/approach and core message
2. Practical value and key themes—focus on what readers can implement

### Key Points Breakdown (## header)
Identify 6-10 major themes, each with a `###` header:
- **Highlights**: 5-7 bullets of key concepts
- **Summary**: 2 paragraphs (100-200 words) emphasizing actionable advice
- Include `[MM:SS]` timestamp at start if timecodes available
- Add horizontal rule after each key point

### Q&A Section (## header)
Include only if Q&A exists in transcript:
- Format: `Question [MM:SS]: [full question]` followed by `Answer: [complete response]`
- Preserve context and nuance from responses

## Style Guidelines

- Clear, professional language accessible to all levels
- Emphasize practical application over theory
- Use specific examples from the transcript
- Maintain presenter's voice and terminology
- Every sentence adds value—be comprehensive but concise
- Focus on what someone can DO, not just KNOW
- Ignore housekeeping (intros, thank yous, scheduling)

## Formatting Rules

- Bold for key terms only
- Bullets ONLY in Highlights sections—all summaries in prose
- Footer: "Created from original transcript"

See `references/template.md` for exact output format.
