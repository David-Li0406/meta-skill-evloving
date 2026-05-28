# Agenda Builder - Implementation Guide

## Architecture

**AI does the thinking. Python does the rendering.**

```
Planning Transcript
       ↓
   [Claude analyzes]
       ↓
   Structured JSON
       ↓
[Python renders DOCX]
       ↓
   agenda.docx
```

## Phase 0: Context Check (NEW)

**ALWAYS do this first**: Check if engagement folder exists in workspace and read:
- README.md (timeline, use cases, constraints)
- engagement_metadata.json (structure, dates, attendees)
- qualification_notes.md or scoping notes

This context informs the agenda structure (single/multi-day, parallel tracks, use case count).

## Phase 1: Claude Extracts Data

Claude reads transcript and creates structured JSON following AGENT_INSTRUCTIONS.MD.

### Extraction Logic

**Customer Name**:
- Extract external organization name
- NEVER use "Microsoft" 
- Examples: "AstraZeneca", "FBI", "State Department"

**Date**:
- Extract specific date if mentioned in transcript
- Format: "Month Day, Year" (e.g., "January 20, 2026")
- DO NOT default to "To be confirmed" if date exists

**Title**:
- Specific, concise, transcript-driven
- Focus on customer objective/topic
- Omit customer name (it's in `customer` field)
- Avoid generic terms and jargon

**Summary**:
- Why this session matters
- Impact and outcomes
- Synthesize purpose, don't list agenda items

**Agenda Items**:
- Standard items: Use predefined descriptions
- Custom topics: Detailed, transcript-specific, exact phrasing
- Include lunch for 6+ hour sessions

## Phase 2: Show Preview

Before creating JSON, show text preview:

```
PREVIEW: [Title]
Customer: [Name]
Date: [Date]
Time: [Time]

TEAM:
Primary: [Names and roles]
Supporting: [Names and roles]

AGENDA:
[Time] | [Topic] [Owner]
  [Description]

[...all items...]

Confirm: Team, Date/Time, Customer name correct?
```

User can request changes before JSON generation.

## Phase 3: Create JSON

After user confirmation, create JSON file:

```python
agenda_data = {
    "customer": "AstraZeneca",
    "date": "January 20, 2026",
    "time": "9:00 AM - 1:00 PM",
    "title": "Copilot Studio Use Case Validation",
    "summary": "Advisory scoping session to validate four Copilot Studio use cases against business requirements and technical feasibility...",
    "primaries": [
        {"name": "Brendon Colburn", "role": "Solution Architect"},
        {"name": "Arslaan Khan", "role": "UK Lead"}
    ],
    "supporting": [
        {"name": "Alex Johnson", "role": "Licensing Specialist"}
    ],
    "agenda_items": [
        {
            "time": "9:00 AM - 9:15 AM",
            "owner": "Microsoft",
            "topic": "Introductions & Session Objectives",
            "description": "Brief participant introductions. Overview of session goals and desired outcomes. Logistics and housekeeping."
        },
        {
            "time": "9:15 AM - 10:30 AM",
            "owner": "Microsoft & Customer",
            "topic": "Discovery: Current Copilot Studio Maturity",
            "description": "Collaborative discovery of AstraZeneca's current Copilot Studio environment including the 5,000+ existing agents, governance challenges with 16,500 users, connector approval process, and evaluation of Agent 365 for expanded use cases."
        },
        {
            "time": "10:30 AM - 11:00 AM",
            "owner": "Microsoft",
            "topic": "Use Case 1: Regulatory Compliance Assistant",
            "description": "Deep dive on first use case: automated regulatory compliance checking across pharmaceutical submissions. Discussion of data sources, compliance rules engine, approval workflows, and integration with existing quality management systems."
        }
        // ...more items
    ]
}

# Save to engagement folder
import json
output_path = 'Engagements/AstraZeneca-2026-01-20/agenda_data.json'
with open(output_path, 'w') as f:
    json.dump(agenda_data, f, indent=2)
```

## Phase 4: Render DOCX

Use scripts/core.py to render:

```python
from scripts.core import create_agenda_doc

template_path = 'assets/agenda_template.docx'
output_docx = 'Engagements/AstraZeneca-2026-01-20/agenda.docx'

create_agenda_doc(
    data=agenda_data,
    template_path=template_path,
    output_path=output_docx,
    logo_path=None  # Optional: path to logo file
)
```

### What create_agenda_doc Does

1. **Load template**: Opens the DOCX template using docxtpl
2. **Prepare context**: Maps JSON fields to template variables
3. **Handle logo** (optional): Processes logo file or base64 image
4. **Render template**: Fills template with context data
5. **Post-process**: Adjusts table column widths
6. **Save**: Writes final DOCX file

### Template Variables

The template expects these Jinja2 variables:

```
{{ customer }}
{{ date }}
{{ title }}
{{ summary }}

{% for person in primaries %}
  {{ person.name }} - {{ person.role }}
{% endfor %}

{% for person in supporting %}
  {{ person.name }} - {{ person.role }}
{% endfor %}

{% for item in agenda_items %}
  {{ item.time }}
  {{ item.owner }}
  {{ item.topic }}
  {{ item.description }}
{% endfor %}

{% if has_logo %}
  {{ logo }}
{% endif %}
```

## Standard Descriptions

Use these exact descriptions for standard items:

### Introductions
```
Brief participant introductions. Overview of session goals and desired outcomes. Logistics and housekeeping.
```

### Discovery
```
Collaborative discovery of [Customer]'s current [domain] environment, processes, and challenges. Focus on understanding pain points, requirements, and business context.
```

**Note**: Replace `[Customer]` and `[domain]` with specifics from transcript.

**Owner**: `"All"` or `"Microsoft and [Customer]"` (use actual customer name, not generic "Customer")

**Encoding**: Use ASCII-safe punctuation - 'and' not '&', hyphens not em-dashes

### Lunch Break
```
Working lunch - informal discussions and Q&A
```

**Owner**: `"All"`

**Duration**: 1 hour

**Include**: Only for 6+ hour sessions

### Next Steps
```
Review key takeaways from the session. Define next steps, action items with owners and timelines. Schedule follow-up sessions as needed.
```

**Position**: Last item

## Custom Topic Descriptions

For topics extracted from transcript:

**Good Example** (specific, detailed):
```
{
  "topic": "Power Automate Integration with AI Builder",
  "description": "Technical deep-dive on integrating Power Automate flows with AI Builder for automated form processing. Discussion of the customer's current 95,000+ monthly Form 4473 submissions, custom model training requirements, confidence score thresholds, human-in-loop approval workflow, and integration with existing NICS database systems."
}
```

**Bad Example** (generic, vague):
```
{
  "topic": "AI Integration",
  "description": "Discuss AI capabilities and integration options"
}
```

## Time Calculations

### Duration Helper

```python
def calculate_duration(time_slot):
    """
    Calculate duration in minutes from time slot string.
    
    Example: "9:00 AM - 10:30 AM" → 90 minutes
    """
    from datetime import datetime
    
    start, end = time_slot.split(' - ')
    start_time = datetime.strptime(start.strip(), '%I:%M %p')
    end_time = datetime.strptime(end.strip(), '%I:%M %p')
    
    duration = (end_time - start_time).total_seconds() / 60
    return int(duration)
```

### Time Allocation Guidelines

- **Intro**: 15 minutes
- **Discovery**: 60-90 minutes
- **Custom topics**: 30-60 minutes each
- **Lunch**: 60 minutes (full-day only)
- **Next Steps**: 20-30 minutes

**Half-day** (4 hours): No lunch, 3-4 topics  
**Full-day** (6-7 hours): Include lunch, 5-7 topics

## Validation Checks

Before rendering, verify:

```python
def validate_agenda_data(data):
    """Validate agenda data before rendering"""
    
    # Critical checks
    assert data['customer'] != "Microsoft", "Customer must be external org"
    assert data['customer'] != "", "Customer name required"
    assert data['date'] != "", "Date required"
    
    # Check for lunch in full-day sessions
    duration = calculate_total_duration(data['agenda_items'])
    has_lunch = any('lunch' in item['topic'].lower() for item in data['agenda_items'])
    
    if duration >= 360 and not has_lunch:  # 6+ hours
        print("⚠️  Warning: Full-day session missing lunch break")
    
    # Check time overlaps
    times = [item['time'] for item in data['agenda_items']]
    for i in range(len(times) - 1):
        end_i = times[i].split(' - ')[1]
        start_i1 = times[i+1].split(' - ')[0]
        if end_i != start_i1:
            print(f"⚠️  Warning: Time gap between items {i} and {i+1}")
    
    return True
```

## Error Handling

### Common Issues

**Template not found**:
```python
if not os.path.exists(template_path):
    raise FileNotFoundError(f"Template not found: {template_path}")
```

**Invalid JSON**:
```python
try:
    data = json.loads(json_string)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
    # Show user which line has the error
```

**Logo processing failure**:
```python
# Fallback: Render without logo
try:
    create_agenda_doc(data, template_path, output_path, logo_path)
except Exception as e:
    logger.warning(f"Logo processing failed: {e}")
    create_agenda_doc(data, template_path, output_path, None)
```

## Post-Processing

After rendering, core.py automatically:

1. **Adjusts column widths**:
   - Time column: 0.8 inches
   - Owner column: 1.2 inches
   - Topic/Description: 4.0 inches

2. **Removes extra columns** (if template generated them)

3. **Saves final DOCX**

## Complete Example

```python
# Step 1: Claude creates JSON from transcript
agenda_data = {
    "customer": "AstraZeneca",
    "date": "January 20, 2026",
    "time": "9:00 AM - 1:00 PM",
    "title": "Copilot Studio Use Case Validation",
    "summary": "Advisory scoping session...",
    "primaries": [...],
    "supporting": [...],
    "agenda_items": [...]
}

# Step 2: Save JSON
with open('agenda_data.json', 'w') as f:
    json.dump(agenda_data, f, indent=2)

# Step 3: Render DOCX
from scripts.core import create_agenda_doc

create_agenda_doc(
    data=agenda_data,
    template_path='assets/agenda_template.docx',
    output_path='agenda.docx'
)

# Step 4: Verify output
assert os.path.exists('agenda.docx')
print("✅ Agenda generated successfully")
```

## Integration with Knowledge Graph

After successful generation:

```python
# Store topics from agenda
for item in agenda_data['agenda_items']:
    if item['topic'] not in ['Introductions', 'Lunch Break', 'Next Steps']:
        memory:create_entities([{
            "name": item['topic'],
            "entityType": "Topic",
            "observations": [
                f"Description: {item['description'][:200]}...",
                f"Duration: {calculate_duration(item['time'])} min",
                f"Customer: {agenda_data['customer']}"
            ]
        }])

# Update engagement with agenda status
memory:add_observations([{
    "entityName": f"{agenda_data['customer']} Engagement - {agenda_data['date']}",
    "contents": [
        "Agenda generated",
        f"Title: {agenda_data['title']}",
        f"Topics: {len(agenda_data['agenda_items']) - 3}"  # Exclude standard items
    ]
}])
```
