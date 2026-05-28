# Video Transcript Analyzer - Reference Guide

## Video URL Handling

The skill will always prompt for a video URL if one wasn't provided in the initial context:
- Check user's message and conversation history for any URLs
- If no URL found, ask: "Do you have a link to the video recording? If so, please share it and I'll include it in the analysis."
- Wait for user response before continuing with analysis
- If user says "no" or "not available", proceed with "Not provided" in output
- If user provides URL, include it in the Video section

## SRT Format Detection

SRT files have this structure:
```
1
00:00:55,620 --> 00:00:59,300
Hi, Emma. Hi, how are you,
Hannah? I'm doing well.

2
00:00:59,300 --> 00:01:00,580
Nice to meet you. How are you?
```

**Key indicators:**
- Sequential numbers at start of each block
- Timestamps in format: `HH:MM:SS,mmm --> HH:MM:SS,mmm`
- Text dialogue follows timestamps
- Blank lines separate entries

**Plain text** lacks timestamps and typically shows speaker names:
```
Interviewer: Thanks for joining today.
Customer: Happy to be here.
```

## Timestamp Adjustment

If user mentions adjusting timestamps (e.g., "I cut off the first 55 seconds"):
1. Ask for the offset amount
2. Subtract that offset from every timestamp
3. Recalculate chapter markers accordingly
4. Include adjusted timestamps in final output
5. Note the adjustment in the document: "Timestamps adjusted: -55 seconds from original"

## Quote Selection Guidelines

**Good quotes:**
- Express emotion or urgency ("panic moment", "heart sinks", "powerless")
- Provide specific examples with numbers or details
- Show impact on workflow or business
- Reveal perception or sentiment shifts
- Demonstrate pain points clearly
- Are self-contained and understandable without additional context

**Avoid:**
- Agreeing sounds ("yeah", "uh-huh", "right")
- Partial thoughts or incomplete sentences
- References that require too much context
- Generic statements without specificity
- Interviewer questions (focus on interviewee responses)

## Topic Organization Strategies

### Chronological vs Thematic

**Chronological** (timestamp order):
- Use when conversation follows a clear arc
- Good for demos or walkthroughs
- Preserves narrative flow

**Thematic** (grouped by topic):
- Use when same topic discussed multiple times
- Better for multi-issue feedback sessions
- Groups related pain points together
- More useful for product/research teams

**Hybrid approach** (recommended):
- Start chronologically for intro/context
- Switch to thematic for main content
- Group related issues that appear at different times
- Use timestamps to show where each theme first appears

### Example Topic Structures

**Product Feedback:**
- Feature-specific issues (grouping by product area)
- Workflow impacts
- Comparison to competitors
- Business/ROI impacts
- Perception and sentiment

**User Research:**
- User goals and motivations
- Pain points by workflow stage
- Workarounds and hacks
- Feature requests
- Usability observations

**Customer Interview:**
- Background and context
- Current state problems
- Impact and consequences
- Desired future state
- Decision criteria

## Timestamp Formatting

**For chapter markers:**
- Use format: `**HH:MM:SS - Topic Title**`
- Start from `00:00:00` even if original SRT starts later
- Round to nearest second (drop milliseconds)
- Use 24-hour format
- Always use two digits for hours (e.g., `00:05:30` not `0:5:30`)

**Examples:**
```markdown
**00:00:00 - Introduction**
**00:02:57 - First Major Topic**
**00:15:45 - Another Topic**
**01:23:15 - Topic After One Hour**
```

## Call Summary Structure

### Paragraph 1: Who and Context
- Who was on the call (names, roles, companies)
- Their background or relationship to the product
- What prompted the call or interview

### Paragraph 2: What Was Discussed
- High-level overview of main topics
- Key themes that emerged
- General scope of conversation

### Paragraph 3: Outcomes and Impact
- Main takeaways or conclusions
- Next steps or action items
- Overall sentiment or trajectory

**Example:**
> Emma is the main HubSpot admin at AX, where she's worked for 4 years (using HubSpot since 2015). She supports multiple departments and has seen significant evolution in how the company uses HubSpot - shifting from set marketing campaigns to operational projects focused on streamlining business processes.
>
> The conversation focused on moments of disconnection Emma experiences in HubSpot, particularly where features don't integrate as expected or where data can't be used consistently across different areas. Three major pain points emerged: membership/registration management limitations, the disconnect between lists and views, and the isolation of the leads object from other HubSpot functionality.
>
> These disconnections create significant time costs, force reliance on support for basic administrative tasks, and undermine HubSpot's core value proposition of unified data. Emma emphasized that these issues particularly impact administrators who work across multiple HubSpot areas and need to support various departments efficiently.

## Topic Bullet Guidelines

Each topic should have:
- **3-6 detailed bullets** (not just one-liners)
- Specific examples mentioned in the conversation
- Impact or consequences described
- Numbers or scale when provided
- Sub-issues or related concerns
- Workarounds currently being used

**Good bullets:**
- "Training 2,000+ dealer groups via memberships (1,000 unregistered)"
- "Support dependency creates timeline risks during campaigns"
- "Must export reports as spreadsheets instead of creating lists"

**Weak bullets:**
- "Has problems with memberships"
- "Doesn't like the interface"
- "Wants improvements"

## Common Transcript Patterns

### Participant Identification

Look for:
- Self-introductions ("I'm [name], I'm the [role]")
- Address by name ("Hi Emma", "Thanks Sarah")
- Role descriptions ("as an admin", "our team")

If unclear, use generic labels:
- Interviewer / Interviewee
- Moderator / Participant
- Host / Guest

### Demonstrations and Screen Shares

Indicators:
- "Let me show you..."
- "Do you want me to share my screen?"
- "As you can see here..."
- "If I click this button..."

**Handle by:**
- Note what was demonstrated in topic bullets
- Mention "demonstrated [feature/issue]" in description
- Include specific UI elements mentioned
- Capture the problem being shown

### Emotional Indicators

Words/phrases that signal importance:
- "panic moment"
- "heart sinks"
- "powerless"
- "frustrated"
- "excited"
- "concerned"
- "confused"

**Use these to:**
- Select quotes
- Identify high-impact issues
- Understand severity and urgency
- Convey user sentiment in summary

## Output Formatting

### Markdown Best Practices

**Headers:**
```markdown
# Title (H1) - Only once at top
## Main Sections (H2) - Video, Summary, Quotes, etc.
**Timestamp - Topic** (Bold) - For chapter markers
```

**Quotes:**
```markdown
> "Quote text here, exactly as spoken."
>
> — Speaker Name, brief context if needed

[blank line between quotes]

> "Next quote text."
>
> — Speaker Name
```

**Lists:**
```markdown
- Detailed bullet with full context and specifics
- Another bullet that explains the issue completely
- Include numbers, examples, and impact where mentioned
```

### Document Flow

1. Title (# H1)
2. Video link (## H2 section)
3. Call Summary (## H2 section, 2-3 paragraphs)
4. Key Quotes (## H2 section, 5-8 blockquotes)
5. Topical Breakdown (## H2 section, with subsections)
6. Full Transcript (## H2 section, raw content)

## Quality Checks

Before delivering output, verify:

- [ ] All quotes are verbatim (exact wording from transcript)
- [ ] Timestamps match original SRT (or note adjustment)
- [ ] Video link included if provided
- [ ] 5-8 quotes minimum
- [ ] 2-3 paragraph summary
- [ ] Each topic has descriptive title + 3-6 bullets
- [ ] Topics are thematically organized (not just chronological)
- [ ] Full transcript included at end
- [ ] Markdown formatting is clean and consistent
- [ ] No customer info redacted unless requested

## Edge Cases

### Multiple Participants
If 3+ people on call:
- Identify key speakers in summary
- Focus quotes on non-interviewer voices
- Note who said what in quote attribution

### Poor Quality Transcripts
If transcript has errors or unclear sections:
- Note in summary: "Transcript quality varies in sections"
- Include quotes exactly as transcribed
- Don't try to fix or interpret unclear sections
- Mark unclear sections in transcript if severe: `[unclear]`

### Very Long Transcripts (60+ minutes)
- May need 8-12 topics instead of 5-7
- Consider grouping into larger themes with sub-sections
- Summary can be 3-4 paragraphs
- Still aim for 5-8 key quotes (not more)

### Very Short Transcripts (<10 minutes)
- May only have 2-4 main topics
- Fewer quotes (3-5 may be sufficient)
- Summary can be 1-2 paragraphs
- Still include full structure

### Technical Demos
If heavy on screen sharing/clicking:
- Describe what was shown in bullet points
- Capture UI elements or features mentioned
- Note the problem being demonstrated
- Include user's commentary about the demo

### Multiple Topics Discussed Simultaneously
If conversation jumps between topics:
- Group thematically, not chronologically
- Note in bullets: "Also discussed at [timestamp]"
- Cross-reference related topics when helpful
