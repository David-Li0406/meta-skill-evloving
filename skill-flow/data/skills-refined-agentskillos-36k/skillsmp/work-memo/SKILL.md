---
name: work-memo
description: Personal work record management with multi-dimensional tracking (person, task, type, time, location, urgency, importance, difficulty). Natural language search, reports, and smart prioritization.
license: MIT
compatibility: opencode
metadata:
  version: "1.0"
  author: OpenCode
  category: productivity
---

# Work Memo Skill

Personal daily work tracking system with comprehensive search, scheduling, and recommendation capabilities.

## What I Do

- **Record Work**: Store work events with full dimensional tracking
- **Natural Language Search**: Query using natural language (e.g., "urgent tasks this week")
- **Flexible Filtering**: Filter by person, type, time, location, priority, status
- **Time Aggregation**: Generate daily, weekly, monthly reports
- **Smart Prioritization**: Eisenhower matrix and multi-factor scoring
- **Work Recommendations**: Get personalized suggestions based on priorities and deadlines

## When to Use Me

User wants to:
- **Record a work event** (memo-only - no task execution)
- Search for records using natural language queries
- Get summary reports (daily/weekly/monthly)
- Receive work suggestions and prioritization
- Organize work by any dimension (person, type, location, etc.)

## Simplified Interface (Recommended)

**IMPORTANT**: This skill is designed for **recording information only**, not executing tasks.

### Primary Usage: `/memo <自然语言描述>`

The simplest way to record work is using the `/memo` command with natural language:

```bash
# Basic usage - just describe what you need to record
/memo 紧急会议明天 #work @office
/memo 完成项目报告
/memo 修复登录bug #urgent
/memo 团队例会 #meeting
/memo 重要电话明天 @phone

# Advanced usage with explicit parameters
/memo "修复生产bug" --urgency 5 --importance 4 --type bugfix
/memo "代码审查" --type review --tags work
```

### Key Features of Memo Command

1. **Record-Only**: No task execution, just information storage
2. **Natural Language**: Supports tags (#work), contexts (@office), dates (today, tomorrow)
3. **Priority Tracking**: Automatically calculates Eisenhower quadrant
4. **Quick Search**: Fast natural language search across all records
5. **Structured Output**: Returns JSON-formatted results for easy parsing

### What Gets Recorded

Each memo captures:
- **Title**: Work description
- **Type**: task/meeting/call/email/review/coding/design/etc.
- **Priority**: Urgency (1-5), Importance (1-5)
- **Tags**: Flexible categorization (#tag)
- **Contexts**: Location/context tags (@office, @home)
- **Dates**: Creation time, optional due date
- **Eisenhower**: Automatically calculated quadrant (Q1-Q4)

### What Does NOT Happen

The memo command **does NOT**:
- Execute any tasks or actions
- Send notifications
- Schedule reminders
- Assign work to others
- Create follow-up tasks
- Perform any automated actions

It's purely a **recording system** for information.

## Quick Start

```bash
# The simplest way - just use /memo with natural language
/memo 紧急会议今天 #work @office
/memo 完成项目报告
/memo 重要任务 #urgent @dev

# For advanced operations, use the CLI directly
python scripts/cli.py search "urgent"
python scripts/cli.py report --daily
python scripts/cli.py list --quadrant Q1
```

## Data Dimensions

Each work record supports these dimensions:

| Dimension | Type | Description |
|-----------|--------|-------------|
| **Person** | Multiple | assignee (who's doing it), reporter (who created), participants |
| **Task/Event** | Text | title (brief), description (detailed) |
| **Type** | Enum | task, meeting, call, email, review, coding, design, writing, research, planning, documentation, bugfix, feature, other |
| **Time** | ISO 8601 | created_at, updated_at, start_date, due_date, completed_at |
| **Location** | Object | place, address, coordinates |
| **Urgency** | 1-5 | 1=least urgent, 5=most urgent |
| **Importance** | 1-5 | 1=least important, 5=most important |
| **Difficulty** | 1-10 | 1=easiest, 10=hardest |
| **Tags** | List[str] | Flexible categorization (#tag) |
| **Projects** | List[str] | Project assignments (project:name) |
| **Contexts** | List[str] | Contexts like @office, @home, @phone |
| **Dependencies** | List[str] | depends_on, blocks |

## Workflow

### Step 1: Add Work Record

Use natural language for quick input:
```bash
python scripts/cli.py memo "Urgent meeting with team tomorrow #work @office"
```

Or use full command for precise control:
```bash
python scripts/cli.py add "Review project proposal" \
  --type review \
  --urgency 4 \
  --importance 4 \
  --due-date "2026-01-25"
```

### Step 2: Search Records

```bash
# Basic search
python scripts/cli.py search "urgent"

# By tag
python scripts/cli.py search "#work"

# By date
python scripts/cli.py search "tasks this week"

# Complex query
python scripts/cli.py search "urgent work tasks this week #important @office"
```

### Step 3: Generate Reports

```bash
# Daily report
python scripts/cli.py report --daily 2026-01-18

# Weekly report
python scripts/cli.py report --weekly

# Monthly report
python scripts/cli.py report --monthly
```

### Step 4: Get Recommendations

```bash
# Get top 10 suggestions
python scripts/cli.py suggest

# Get top 5 suggestions
python scripts/cli.py suggest --limit 5
```

## Natural Language Query Syntax

### Date Queries
```
today
tomorrow
this week
next week
this month
next month
due 2026-01-25
```

### Priority Queries
```
urgent / very urgent
important / very important
not urgent / low urgency
not important / low importance
```

### Tag and Context Queries
```
#work #urgent
@office @home
project:Q1-Planning
```

### Combined Examples
```
"Show me urgent tasks this week"
"What did I do today with @office"
"High priority tasks for John due this month"
"This week's work for project Q1-Planning"
```

## Priority Scoring

Multi-factor scoring uses these weights by default:
- **Urgency**: 35% - How soon it needs to be done
- **Importance**: 30% - How valuable it is
- **Effort** (inverse difficulty): 20% - Quick wins get higher scores
- **Dependencies**: 15% - Tasks blocking others get higher priority

**Priority Score Formula**:
```
score = (urgency/5 * 0.35) +
        (importance/5 * 0.30) +
        ((11 - difficulty)/10 * 0.20) +
        (blocking_count * 0.15)
```

## Eisenhower Matrix

Tasks are categorized into 4 quadrants based on urgency and importance:

```
       Important                  Not Important
      _______                  ___________
     |       |                |          |
Urgent|   Q1   |   Do Now   |   Q3    |  Delegate
     | Urgent &|             | Urgent &  |
     | Important|             | Not Import.|
     |_________|_______________|__________|
     |       |                |          |
Not  |   Q2   |  Schedule   |   Q4    | Eliminate
Urgent| Not Urg.|             | Not Urgent|
     |& Import.|             | & Not Imp.|
     |_________|_______________|__________|
```

**Quadrant Actions**:
- **Q1 (Do Now)**: Execute immediately
- **Q2 (Schedule)**: Plan for later
- **Q3 (Delegate)**: Assign to someone else
- **Q4 (Eliminate)**: Delete or archive

## Testing

Run the test suite to verify functionality:

```bash
python test_memo.py
```

Expected results:
- Total tests: 65
- Pass rate: 100%

## Documentation

- **README.md**: User-facing documentation with detailed examples
- **USER_GUIDE.md**: Complete usage guide (Chinese)
- **TEST_REPORT.md**: Test execution report
- **DEVELOPMENT.md**: Development guide for contributors

## Technical Details

### Dependencies
- Python 3.9+
- TinyDB 4.8.0+ (pip install tinydb)

### Storage
- Location: `~/.workmemo/db.json`
- Format: JSON
- Backup: Manual backup recommended

### API Reference

See `scripts/schema.py`, `scripts/storage.py`, `scripts/query_parser.py`, `scripts/reporting.py` for complete API documentation.

## CLI Commands Reference

```bash
# Add work record
python scripts/cli.py add "Title" --type task --urgency 4 --importance 4

# Quick add with natural language
python scripts/cli.py memo "Urgent meeting today #work @office"

# Search records
python scripts/cli.py search "urgent tasks this week"

# List all records
python scripts/cli.py list

# List by Eisenhower quadrant
python scripts/cli.py list --quadrant Q1

# Generate reports
python scripts/cli.py report --daily 2026-01-18
python scripts/cli.py report --weekly
python scripts/cli.py report --monthly

# Get suggestions
python scripts/cli.py suggest --limit 10
```

## Support

For detailed usage instructions, see USER_GUIDE.md.
For testing information, see TEST_REPORT.md.
For development details, see DEVELOPMENT.md.
