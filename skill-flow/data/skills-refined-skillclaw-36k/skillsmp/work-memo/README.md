# Work Memo

Personal work record management system with multi-dimensional tracking, natural language search, and smart prioritization.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-65%20passed-brightgreen.svg)](TEST_REPORT.md)

## Features

- **Multi-dimensional Work Tracking**: Record work events with full dimensional tracking (person, task, type, time, location, urgency, importance, difficulty)
- **Natural Language Search**: Query using natural language (e.g., "urgent tasks this week", "show me meetings today")
- **Flexible Filtering**: Filter by person, type, time, location, priority, status
- **Time Aggregation**: Generate daily, weekly, monthly reports with insights
- **Smart Prioritization**: Eisenhower matrix and multi-factor scoring
- **Work Recommendations**: Get personalized suggestions based on priorities and deadlines

## Quick Start

### Installation

```bash
# Install dependencies
pip install tinydb
```

### Basic Usage

#### Optimized Memo Command (Recommended for Quick Recording)

**Design Philosophy**: Record information only, no task execution.

```bash
# Navigate to scripts directory
cd scripts

# Record a work item (natural language) - QUICK & SIMPLE
python3 memo_command.py "Urgent meeting today #work @office"
python3 memo_command.py "完成项目报告"
python3 memo_command.py "Important call #urgent @phone"

# Record with explicit parameters
python3 memo_command.py "Fix login bug" --urgency 5 --importance 4 --type bugfix
python3 memo_command.py "Team meeting" --type meeting --tags work

# Search records
python3 memo_command.py --search "urgent"
python3 memo_command.py --search "#work"

# List records
python3 memo_command.py --list
python3 memo_command.py --list --quadrant Q1
python3 memo_command.py --list --status todo
```

**Key Features**:
- ✅ Record-only: No task execution
- ✅ Natural language: Supports tags (#work), contexts (@office), dates
- ✅ Priority tracking: Automatic Eisenhower calculation
- ✅ Quick search: Fast natural language queries

#### Full CLI (Advanced Features)

```bash
# Add a work record (natural language)
python scripts/cli.py memo "Urgent meeting today #work @office"

# Add a work record (detailed)
python scripts/cli.py add "Review project proposal" \
  --type review \
  --urgency 4 \
  --importance 4 \
  --due-date "2026-01-25"

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

# Get work suggestions
python scripts/cli.py suggest --limit 10
```

**When to use memo_command.py**:
- Quick information recording
- Simple command-line interface
- No task execution needed

**When to use cli.py**:
- Complete workflow management
- Interactive input needed
- Report generation required
- Work suggestions wanted

## Documentation

- **[MEMO_QUICK_REFERENCE.md](MEMO_QUICK_REFERENCE.md)**: Quick reference for memo command
- **[MEMO_COMMAND_README.md](MEMO_COMMAND_README.md)**: Complete guide for memo command
- **[USER_GUIDE.md](USER_GUIDE.md)**: Complete usage guide with examples (Chinese)
- **[TEST_REPORT.md](TEST_REPORT.md)**: Test execution report (65 tests, 100% pass rate)
- **[DEVELOPMENT.md](DEVELOPMENT.md)**: Development guide for contributors
- **[SKILL.md](SKILL.md)**: OpenCode skill definition

## Data Model

Each work record supports:

| Dimension | Type | Description |
|-----------|--------|-------------|
| **Person** | Multiple | assignee, reporter, participants |
| **Task/Event** | Text | title, description |
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

## Natural Language Query Examples

### Date Queries
```bash
"tasks today"
"tasks tomorrow"
"tasks this week"
"tasks this month"
```

### Priority Queries
```bash
"urgent tasks"
"high priority tasks"
"not urgent tasks"
```

### Tag and Context Queries
```bash
"#work #urgent"
"@office @home"
"project:Q1"
```

### Combined Examples
```bash
"urgent work tasks this week #important @office"
"What did I do today with @office"
"High priority tasks for project Q1 due next month"
```

## Priority Scoring

Multi-factor scoring uses:
- **Urgency**: 35% - How soon it needs to be done
- **Importance**: 30% - How valuable it is
- **Effort** (inverse difficulty): 20% - Quick wins get higher scores
- **Dependencies**: 15% - Tasks blocking others get higher priority

## Eisenhower Matrix

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

## Project Structure

```
work_memo/
├── SKILL.md              # OpenCode skill definition
├── package.json          # Project metadata
├── README.md            # This file
├── LICENSE              # MIT License
├── .gitignore          # Git ignore rules
├── MEMO_QUICK_REFERENCE.md     # Quick reference for memo command
├── MEMO_COMMAND_README.md      # Complete guide for memo command
├── USER_GUIDE.md        # Complete usage guide (Chinese)
├── TEST_REPORT.md       # Test execution report
├── DEVELOPMENT.md       # Development guide
├── test_memo.py        # Test suite
├── scripts/
│   ├── memo_command.py  # Optimized memo command (record-only)
│   ├── schema.py        # Data models
│   ├── storage.py       # TinyDB storage layer
│   ├── query_parser.py  # Natural language query parsing
│   ├── reporting.py     # Report generation
│   └── cli.py          # Full command-line interface
├── references/         # Additional documentation
└── assets/           # Static resources
```

## Requirements

- Python 3.9+
- TinyDB 4.8.0+

## Testing

Run the test suite:

```bash
python test_memo.py
```

Results:
- **Total tests**: 65
- **Passed**: 65
- **Pass rate**: 100%

## License

MIT

## Author

OpenCode
