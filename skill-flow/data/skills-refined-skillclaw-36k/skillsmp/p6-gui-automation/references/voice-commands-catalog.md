# Voice Commands Catalog

Complete catalog of supported voice commands for the P6 Voice-Driven Smart Agent.

## Overview

Voice commands are transcribed by Whisper and interpreted by the LLM agent to determine which GUI tools to call. The agent uses natural language understanding, so exact phrasing is not required.

## Activity Selection Commands

### Select by ID

| Voice Command | Tool Called | Parameters | Example Response |
|---------------|-------------|------------|------------------|
| "Select activity A1010" | `select_activity` | `activity_id="A1010"` | "Selected activity A1010" |
| "Find activity MT-002" | `select_activity` | `activity_id="MT-002"` | "Found and selected MT-002" |
| "Go to activity 1000" | `navigate_to_activity` | `activity_id="1000"` | "Navigated to activity 1000" |

### Bulk Selection

| Voice Command | Tool Called | Parameters | Example Response |
|---------------|-------------|------------|------------------|
| "Select all activities" | `select_all_activities` | - | "Selected 145 activities" |
| "Clear selection" | `clear_selection` | - | "Selection cleared" |

## Navigation Commands

### Basic Navigation

| Voice Command | Tool Called | Notes |
|---------------|-------------|-------|
| "Go to the first activity" | `go_to_first_activity` | Ctrl+HOME |
| "Go to first" | `go_to_first_activity` | Short form |
| "Navigate to the beginning" | `go_to_first_activity` | Alternative |
| "Go to the last activity" | `go_to_last_activity` | Ctrl+END |
| "Go to the end" | `go_to_last_activity` | Short form |
| "Jump to bottom" | `go_to_last_activity` | Alternative |

### Activity-Specific Navigation

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Find and go to A1010" | `navigate_to_activity` | `activity_id="A1010"` |
| "Navigate to activity MT-003" | `navigate_to_activity` | `activity_id="MT-003"` |
| "Show me activity 2000" | `navigate_to_activity` | `activity_id="2000"` |

## Editing Commands

### Duration Editing

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Change duration to 15 days" | `update_activity_gui` | `field="Duration"`, `value="15d"` |
| "Set duration to 10 working days" | `update_activity_gui` | `field="Duration"`, `value="10d"` |
| "Update duration to 3 weeks" | `update_activity_gui` | `field="Duration"`, `value="15d"` |
| "Make it 5 days long" | `update_activity_gui` | `field="Duration"`, `value="5d"` |

### Activity Name/Description

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Rename activity to Install HVAC" | `update_activity_gui` | `field="Activity Name"`, `value="Install HVAC"` |
| "Change description to Pour concrete" | `update_activity_gui` | `field="Description"`, `value="Pour concrete"` |

### Date Editing

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Set start date to January 15" | `update_activity_gui` | `field="Start"`, `value="15-Jan-25"` |
| "Change finish to March 1st" | `update_activity_gui` | `field="Finish"`, `value="01-Mar-25"` |

### Resource Assignment

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Assign 8 hours of labor" | `update_activity_gui` | `field="Budgeted Units"`, `value="8h"` |
| "Set planned cost to 5000" | `update_activity_gui` | `field="Budgeted Cost"`, `value="5000"` |

## Constraint Commands

### Setting Constraints

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Set constraint start on or after January 15" | `set_activity_constraint` | `type="START_ON_OR_AFTER"`, `date="2025-01-15"` |
| "Must start on February 1st" | `set_activity_constraint` | `type="MUST_START_ON"`, `date="2025-02-01"` |
| "Must finish by March 15" | `set_activity_constraint` | `type="MUST_FINISH_ON_OR_BEFORE"`, `date="2025-03-15"` |
| "Set as late as possible" | `set_activity_constraint` | `type="AS_LATE_AS_POSSIBLE"`, `date=None` |
| "Finish no later than April 30" | `set_activity_constraint` | `type="FINISH_ON_OR_BEFORE"`, `date="2025-04-30"` |

### Clearing Constraints

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Remove constraint" | `clear_activity_constraint` | - |
| "Clear the constraint" | `clear_activity_constraint` | - |
| "Delete constraint from A1010" | `clear_activity_constraint` | `activity_id="A1010"` |

### Constraint Type Mappings

| Natural Language | Constraint Type | Code |
|-----------------|-----------------|------|
| "start on or after" | Start On or After | `START_ON_OR_AFTER` |
| "finish on or before" | Finish On or Before | `FINISH_ON_OR_BEFORE` |
| "must start on" | Must Start On | `MUST_START_ON` |
| "must finish on" | Must Finish On | `MUST_FINISH_ON` |
| "as late as possible" | As Late As Possible | `AS_LATE_AS_POSSIBLE` |
| "as soon as possible" | As Soon As Possible | `AS_SOON_AS_POSSIBLE` |
| "start no earlier than" | Start On or After | `START_ON_OR_AFTER` |
| "finish no later than" | Finish On or Before | `FINISH_ON_OR_BEFORE` |

## Activity Management Commands

### Adding Activities

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Add a new activity" | `add_activity_gui` | `wbs_path=None` |
| "Create activity under WBS 1.2" | `add_activity_gui` | `wbs_path="1.2"` |
| "Insert new task" | `add_activity_gui` | `wbs_path=None` |

### Deleting Activities

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Delete this activity" | `delete_activity_gui` | `activity_id=current` |
| "Remove activity A1010" | `delete_activity_gui` | `activity_id="A1010"` |
| "Delete selected activities" | `delete_activity_gui` | `activity_id=selected` |

## Scheduling Commands

### Schedule Calculation

| Voice Command | Tool Called | Notes |
|---------------|-------------|-------|
| "Run the schedule" | `reschedule_project_gui` | Executes F9 |
| "Reschedule the project" | `reschedule_project_gui` | F9 with options |
| "Calculate schedule" | `reschedule_project_gui` | F9 |
| "Schedule project" | `reschedule_project_gui` | F9 |
| "F9" | `reschedule_project_gui` | Direct command |

## Query Commands

### Information Retrieval

| Voice Command | Tool Called | Response |
|---------------|-------------|----------|
| "What columns are visible?" | `get_visible_columns` | List of column names |
| "Show me the columns" | `get_visible_columns` | Column list |
| "List available columns" | `get_visible_columns` | Column list |

## Compound Commands

The agent can handle compound commands that require multiple tool calls:

| Voice Command | Tools Called | Sequence |
|---------------|--------------|----------|
| "Select activity A1010 and change duration to 10 days" | `select_activity` -> `update_activity_gui` | 1. Select, 2. Edit |
| "Go to first activity and set constraint" | `go_to_first_activity` -> user dialog for details | 1. Navigate, 2. Clarify |
| "Find A1020, change duration to 5 days, then run schedule" | `select_activity` -> `update_activity_gui` -> `reschedule_project_gui` | 1. Select, 2. Edit, 3. Schedule |

## Error Responses

When the agent cannot complete a command:

| Situation | Response |
|-----------|----------|
| Activity not found | "I couldn't find activity {id}. Please check the ID." |
| SAFE_MODE active | "This operation requires unsafe mode. Currently in safe mode." |
| Column not visible | "The column '{name}' is not visible. Please add it to the layout." |
| P6 not connected | "I can't connect to P6. Please ensure P6 is open." |
| Ambiguous command | "I'm not sure what you mean. Could you clarify?" |

## Tips for Voice Commands

### Be Specific

- Say "activity A1010" not just "A1010" for better recognition
- Include units: "10 days" not just "10"
- Use full constraint names: "start on or after" not just "after"

### Natural Language Works

These variations all work:
- "Change the duration to 15 days"
- "Set duration to 15 days"
- "Update duration: 15 days"
- "Make duration 15 days"
- "15 days duration"

### Dictating Activity IDs

For activity IDs, speak clearly:
- "A one zero one zero" for A1010
- "M T dash zero zero three" for MT-003
- "Alpha one zero two zero" for A1020

### Handling Dates

Supported date formats:
- "January 15th 2025"
- "January 15"
- "15 Jan 2025"
- "1/15/2025"
- "the 15th of January"
