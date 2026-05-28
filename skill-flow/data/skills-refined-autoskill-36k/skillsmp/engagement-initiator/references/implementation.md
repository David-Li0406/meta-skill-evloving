# Engagement Initiator - Implementation Guide

## Core Function

Bootstrap engagements from minimal information and create complete folder structure.

## Key Scripts

### business_days.py
- `calculate_business_days(target_date, days_offset)` - Calculate T-X dates
- `generate_task_timeline(customer, date)` - Generate all 15 tasks
- `format_task_summary(tasks)` - Format for display

## Process Flow

```python
def initialize_engagement(customer, date, context=None):
    """
    1. Parse inputs (handle flexible formats)
    2. Calculate timeline position (where are we now?)
    3. Create OneDrive folder structure
    4. Generate tasks with business_days.py
    5. Create metadata file
    6. Store in knowledge graph
    7. Return status summary
    """
    
    # Example
    timeline_position = calculate_business_days_between(today, engagement_date)
    
    if timeline_position < -28:
        status = "Early - no tasks yet"
        overdue = []
    else:
        # Find overdue tasks
        overdue = [task for task in TASKS if timeline_position < task.offset]
    
    return {
        "folder": folder_path,
        "timeline_position": f"T{timeline_position:+d}",
        "overdue": overdue,
        "upcoming": upcoming_tasks,
        "files_created": file_list
    }
```

## OneDrive Structure

Always create:
```
C:\Users\{user}\OneDrive - Microsoft\Engagements\{Customer}-{Date}\
├── tasks.csv (from business_days.py)
├── engagement_metadata.json (structured data)
├── README.md (timeline reference)
└── [additional files based on input]
```

## Metadata Schema

```json
{
  "customer": "string",
  "engagement_date": "YYYY-MM-DD",
  "engagement_type": "string or null",
  "created": "YYYY-MM-DD",
  "timeline_position": "T-X or T+X",
  "status": "planned|active|past",
  "cehub_link": "string or null",
  "cehub_event_id": "string or null",
  "tasks_generated": true,
  "qualification_notes_captured": boolean,
  "agenda_generated": boolean
}
```

## Knowledge Graph Integration

```python
# Create customer entity
memory:create_entities([{
    "name": customer_name,
    "entityType": "Customer",
    "observations": [
        f"Industry: {industry}",
        f"Customer type: {customer_type}",
        "Context from qualification notes"
    ]
}])

# Create engagement entity
memory:create_entities([{
    "name": f"{customer_name} Engagement - {date}",
    "entityType": "Engagement",
    "observations": [
        f"Date: {date}",
        f"Type: {engagement_type}",
        f"Status: planned",
        f"Timeline position: {timeline_position}"
    ]
}])

# Link them
memory:create_relations([{
    "from": engagement_name,
    "to": customer_name,
    "relationType": "conducted_for"
}])
```

## Input Parsing

Handle these flexibly:
- "Customer Name, Date"
- "Customer Date CEHub: [link]"
- "[paste qualification notes]"
- Just basic context

Extract:
- Customer name (required)
- Date (required)
- CEHub link (optional)
- Engagement type (optional)
- Context (optional)

## Timeline Status Logic

```python
def get_timeline_status(engagement_date, today):
    days = calculate_business_days_between(today, engagement_date)
    
    if days > 28:
        return "Early planning", "low urgency"
    elif days >= 14:
        return "Active planning", "medium urgency"
    elif days >= 0:
        return "Final prep", "high urgency"
    elif days >= -3:
        return "Post-engagement", "medium urgency"
    else:
        return "Follow-up complete", "low urgency"
```

## Output Format

Always show:
```
✅ Created: Engagements/{Customer}-{Date}/
✅ Tasks generated ({count} tasks)
✅ Stored in knowledge graph

📊 Timeline Status: T{position} ({phase})

[If overdue tasks:]
OVERDUE:
❗ T-28: Schedule Internal Precall
❗ T-22: Research customer

[If upcoming:]
DUE THIS WEEK:
📅 T-14: Execute Customer Precall

📋 Next Actions:
1. Import tasks.csv to Planner
2. [specific recommendations]
```

## Integration Points

- Called first in any engagement workflow
- Internally calls task-generator
- Creates folder that other skills use
- Updates knowledge graph for other skills to query
