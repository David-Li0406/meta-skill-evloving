---
name: agenda-builder
description: Creates engagement agendas from planning transcripts or notes. Extracts structured agenda data into JSON format, then renders DOCX using templates. Use when building agendas, processing planning calls, or when user mentions transcripts, Discovery, Architecture Review, POC, Executive Briefing, Deep Dive sessions, or agenda generation.
---

# Agenda Builder

**Architecture**: Claude analyzes transcript → Creates JSON → Python renders DOCX

Claude does the intelligent extraction. Python just renders the template.

## Workflow

```
AI Agenda Building Process:
- [ ] Check for existing engagement folder and read README/metadata/notes first
- [ ] Analyze planning transcript/notes
- [ ] Extract structured data following AGENT_INSTRUCTIONS.MD
- [ ] ⚠️ MANDATORY CHECKPOINT: Show preview to user for confirmation
- [ ] ⚠️ MANDATORY: Get user approval/corrections (DO NOT PROCEED WITHOUT THIS)
- [ ] ONLY AFTER APPROVAL: Create JSON with customer, date, title, summary, agenda_items
- [ ] Save JSON to engagement folder
- [ ] Automatically install required Python packages (if not already installed)
- [ ] Call scripts/core.py to render DOCX
- [ ] Update knowledge graph with topics
```

## Step 1: Analyze Transcript (Claude Does This)

Read full planning transcript or qualification notes.

Follow rules from [references/AGENT_INSTRUCTIONS.MD](references/AGENT_INSTRUCTIONS.MD):
- **CRITICAL**: `customer` = external org (NEVER "Microsoft")
- Extract specific date if mentioned
- Use transcript terminology for topics/descriptions
- Standard items get standard descriptions
- Custom topics get detailed, transcript-specific descriptions

## Step 2: Understand JSON Structure (DO NOT CREATE YET)

⚠️ **CRITICAL - DO NOT EXECUTE THIS STEP YET**

This section shows the JSON structure you will create AFTER user approves the preview in Step 4.

**MANDATORY WORKFLOW:**
1. Analyze transcript/materials (Step 1)
2. Show text preview to user (Step 4) ← YOU MUST DO THIS NEXT
3. Get user approval
4. ONLY THEN create this JSON structure
5. Render DOCX (Step 5)

Required structure:

```json
{
  "customer": "External Organization Name",
  "date": "Month Day, Year",
  "time": "9:30 AM - 4:00 PM",
  "title": "Specific, Transcript-Driven Title",
  "summary": "Why this session matters (synthesize, don't list items)",
  "primaries": [
    {"name": "Person Name", "role": "Role"}
  ],
  "supporting": [
    {"name": "Person Name", "role": "Role"}  
  ],
  "agenda_items": [
    {
      "time": "9:30 AM - 9:45 AM",
      "owner": "Microsoft",
      "topic": "Introductions & Session Objectives",
      "description": "Brief participant introductions. Overview of session goals and logistics."
    },
    {
      "time": "9:45 AM - 11:00 AM",
      "owner": "Microsoft & Customer",
      "topic": "Discovery: Current State & Challenges",
      "description": "Collaborative discovery of Customer's current environment..."
    }
  ]
}
```

## Step 3: Agenda Item Rules

**Sequence**: MUST follow:
1. Intro/Goals (15 min)
2. Discovery (~1 hour, customer-led)
3. Custom topics from transcript
4. Lunch (1 hour, for full-day only)
5. More custom topics
6. Next Steps (20-30 min)

**Standard Items** (use these exact descriptions):

**Introductions**:
```
"Brief participant introductions. Overview of session goals and desired outcomes. Logistics and housekeeping."
```
**Note**: Use ASCII-safe punctuation only (hyphens not em-dashes, 'and' not '&')

**Discovery**:
```
"Collaborative discovery of [Customer]'s current [domain] environment, processes, and challenges. Focus on understanding pain points, requirements, and business context."
```
Owner: `"All"` or `"Microsoft and [Customer]"`

**Lunch Break** (full-day only):
```
"Working lunch - informal discussions and Q&A"
```
Owner: `"All"`

**Next Steps**:
```
"Review key takeaways from the session. Define next steps, action items with owners and timelines. Schedule follow-up sessions as needed."
```

**Custom Topics** (transcript-driven):
- Use EXACT phrasing from transcript
- Highly detailed descriptions
- Specific technologies, frameworks, use cases mentioned
- NO generic summaries

## Step 3.5: Multi-Day Workshops

**For multi-day engagements**: Always create ONE combined agenda document with all days included.

**Metadata Validation**: Before rendering, check engagement_metadata.json if it exists:
- Verify use case count matches
- Confirm dates align
- Validate attendee lists

## Step 4: Show Preview to User ⚠️ MANDATORY CHECKPOINT

🛑 **STOP - You MUST complete this step before creating JSON or rendering DOCX**

**Never skip this step.** Always show a text preview and wait for user confirmation.

**Why this matters:** User may want to adjust timing, attendee lists, descriptions, or overall structure. Generating the document without approval wastes time and creates rework.

Show text preview:

```
PREVIEW: AstraZeneca Copilot Studio Validation
Date: January 20, 2026
Time: 9:00 AM - 1:00 PM

AGENDA:
9:00-9:15 | Introductions & Objectives [Microsoft]
  Brief intros, session goals, logistics

9:15-10:30 | Discovery: Current Copilot Studio Maturity [Microsoft & Customer]
  Deep dive on existing 5,000+ agents, governance challenges with 
  16,500 users, connector approval process, Agent 365 evaluation...

[...remaining items...]

Confirm: Team list, Date/Time, Customer name?
```

## Step 5: Create JSON and Render DOCX (Only After User Approval)

✅ **PREREQUISITE:** User must have approved the preview from Step 4.

After user confirms, save JSON and render.

**CRITICAL**: DO NOT create custom render scripts or separate .py files. Use ONLY the inline Python one-liner approach shown below.

**Workflow for rendering**:
1. Install dependencies: `pip install --quiet docxtpl>=0.16.0 python-docx>=1.1.0 Pillow>=10.0.0`
   - Pip automatically skips packages that are already installed
   - The `--quiet` flag minimizes output
2. Save the JSON data to agenda_data.json in the engagement folder (JSON already created above)
3. Execute the rendering using a Python one-liner (DO NOT create a separate .py file)

**Required one-liner template**:
```bash
python -c "import json, sys; sys.path.insert(0, r'SKILLS_PATH\.github\skills\agenda-builder'); from scripts.core import create_agenda_doc; agenda_data = json.load(open(r'ENGAGEMENT_PATH\agenda_data.json')); create_agenda_doc(agenda_data, r'SKILLS_PATH\.github\skills\agenda-builder\assets\agenda_template.docx', r'ENGAGEMENT_PATH\OUTPUT_FILENAME.docx', None); print('Agenda created successfully')"
```

**Example for Windows**:
```bash
python -c "import json, sys; sys.path.insert(0, r'c:\Projects\copilot-skills-1\.github\skills\agenda-builder'); from scripts.core import create_agenda_doc; agenda_data = json.load(open(r'c:\Users\brecol\OneDrive - Microsoft\Engagements\Customer-2026-01-20\agenda_data.json')); create_agenda_doc(agenda_data, r'c:\Projects\copilot-skills-1\.github\skills\agenda-builder\assets\agenda_template.docx', r'c:\Users\brecol\OneDrive - Microsoft\Engagements\Customer-2026-01-20\Customer_Agenda.docx', None); print('Agenda created successfully')"
```

**Example for Unix/Mac**:
```bash
python -c "import json, sys; sys.path.insert(0, '/path/to/copilot-skills/.github/skills/agenda-builder'); from scripts.core import create_agenda_doc; agenda_data = json.load(open('/path/to/engagement/agenda_data.json')); create_agenda_doc(agenda_data, '/path/to/copilot-skills/.github/skills/agenda-builder/assets/agenda_template.docx', '/path/to/engagement/Customer_Agenda.docx', None); print('Agenda created successfully')"
```

This one-liner approach ensures the skill works without creating extra files or requiring virtual environment setup.

## JSON Schema Details

**Required Fields**:
- `customer` (string): External organization name
- `date` (string): "Month Day, Year" format
- `time` (string): "Start - End" format  
- `title` (string): Specific, concise title
- `summary` (string): Why this session matters
- `primaries` (array): Primary team members
- `supporting` (array): Supporting team members
- `agenda_items` (array): Agenda items with time/owner/topic/description

**Optional Fields**:
- `logo` (string): Path to logo file or base64 image

## Example JSON

See [assets/example_agenda.json](assets/example_agenda.json) for complete example.

## Knowledge Graph Integration

After generating agenda, store topics:

```python
for item in agenda_data['agenda_items']:
    if item['topic'] not in ['Introductions', 'Lunch Break', 'Next Steps']:
        memory:create_entities([{
            "name": item['topic'],
            "entityType": "Topic",
            "observations": [
                f"Description: {item['description']}",
                f"Duration: {calculate_duration(item['time'])}",
                f"Used in {customer} {engagement_type}"
            ]
        }])
```

## Quality Checks (Before Rendering)

Verify:
- [ ] `customer` is external org (NOT "Microsoft")
- [ ] `date` is specific if mentioned in transcript
- [ ] Custom topics have detailed, transcript-specific descriptions
- [ ] Lunch included for full-day sessions (6+ hours)
- [ ] Standard items use standard descriptions
- [ ] Time slots don't overlap
- [ ] Owner is appropriate ("Microsoft", "Microsoft & Customer", "All")

## Common Patterns by Type

**Discovery**:
- 60-90 min customer-led discovery
- Focus on current state, pain points
- More listening than presenting

**Architecture Review**:
- Current architecture overview
- Technical deep-dives with whiteboarding
- Architecture recommendations

**POC Kickoff**:
- Clear success criteria
- Technical requirements
- POC timeline and milestones

**Executive Briefing** (shorter):
- Business value focus
- High-level overview
- Strategic alignment

**Deep Dive**:
- Multiple technical sessions
- Hands-on components
- Detailed action items

**Multi-Day Parallel Track Workshop**:
- Day headers as agenda items (e.g., "DAY 1 - Feb 3, 2026")
- Parallel breakout sessions (Tracks A/B/C)
- Scheduled show-and-tell syncs
- Daily wrap-ups and planning
- See AstraZeneca workshop example in references/

## Dependencies

**Automatic Installation**: Dependencies are automatically installed when rendering agendas.

The skill uses these Python packages (versions from `requirements.txt`):
- docxtpl>=0.16.0 (DOCX templating)
- python-docx>=1.1.0 (DOCX manipulation)
- Pillow>=10.0.0 (Image processing)

**No manual setup required** - the skill automatically runs:
```bash
pip install --quiet docxtpl>=0.16.0 python-docx>=1.1.0 Pillow>=10.0.0
```

**Note**: These versions use minimum version requirements (>=) as defined in requirements.txt. This allows compatible updates while maintaining a minimum baseline. Pip automatically skips packages that are already installed and meet the version requirements, making repeated runs efficient.

This ensures the skill "just works" like it does in Claude Desktop, without requiring virtual environment setup.

## Reference Files

- [references/AGENT_INSTRUCTIONS.MD](references/AGENT_INSTRUCTIONS.MD) - Complete extraction rules
- [references/agent_instructions.md](references/agent_instructions.md) - Additional agenda patterns
- [references/implementation.md](references/implementation.md) - Technical details
- [assets/example_agenda.json](assets/example_agenda.json) - Example output
