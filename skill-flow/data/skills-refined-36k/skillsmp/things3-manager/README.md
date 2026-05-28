# Things3 Manager Skill

An [Agent Skill](https://github.com/anthropics/skills) for Claude that provides full task management integration with [Things3](https://culturedcode.com/things/) on macOS.

## What it does

This skill lets Claude read, create, update, complete, cancel, delete, and batch-organize your Things3 tasks, projects, and areas through natural conversation.

**Example prompts:**
- "Show me my Today list"
- "What's overdue?"
- "Add a task to call Alex tomorrow tagged personal"
- "Mark 'Send invoice' as done"
- "Delete that old task"
- "Cancel the Harmony Hash project"
- "Move that task to my Work project"
- "Help me reorganize my tasks for the week"
- "Reschedule all these overdue tasks to next Monday"
- "Create a project for Q1 Planning with some starter tasks"

## How it works

| Operation | Method |
|-----------|--------|
| **Reading** | [things.py](https://github.com/thingsapi/things.py) — Python library that queries Things3's SQLite database directly |
| **Writing** | [Things URL Scheme](https://culturedcode.com/things/support/articles/2803573/) — Native `things:///` URLs for creating/updating tasks |
| **Deleting** | AppleScript — For moving items to Trash |
| **Batch ops** | Sequential URL scheme calls with configurable delay |

This hybrid approach gives you fast reads (direct database) and reliable writes (official API).

## Features

- ✅ **Read**: Inbox, Today, Upcoming, Anytime, Someday, Logbook, projects, areas, tags
- ✅ **Create**: To-dos with tags, deadlines, checklists, notes; Projects with starter tasks
- ✅ **Update**: Reschedule, move between projects, add notes, change tags
- ✅ **Complete/Cancel**: Mark tasks done or canceled
- ✅ **Delete**: Move items to Trash
- ✅ **Batch operations**: Complete, cancel, reschedule, move, or tag multiple items at once
- ✅ **Sync**: Auto-activates Things before reading to ensure fresh data
- ✅ **Search**: Find tasks by keyword

## Requirements

- **macOS** with Things3 installed
- **Python 3** with `things.py` library
- **Things URLs enabled**: Things → Settings → General → Enable Things URLs

## Installation

### 1. Install the skill

```bash
# Clone to your Claude skills folder
git clone https://github.com/YOUR_USERNAME/things3-manager.git ~/.claude/skills/things3-manager
```

### 2. Install the Python dependency

```bash
pip install things.py
```

### 3. Enable Things URLs

Open Things3 → Settings → General → Enable Things URLs

## Skill Structure

```
things3-manager/
├── SKILL.md                    # Instructions for Claude
├── README.md                   # This file
├── scripts/
│   ├── things3_dashboard.py    # Fast full overview (single call)
│   ├── things3_read.py         # Individual read queries
│   ├── things3_write.py        # Create/update/complete/delete/batch operations
│   └── things3_utils.py        # Sync and token utilities
└── references/
    └── url_scheme.md           # URL scheme quick reference
```

## Example Usage

Once installed, just talk to Claude naturally:

> **You:** What do I have due this week?
> 
> **Claude:** *fetches deadlines and shows you a summary*

> **You:** Add "Review PR" to my Dev project for tomorrow
> 
> **Claude:** *creates the task in Things3*

> **You:** That Minilogue task has been overdue forever, push it to next month
> 
> **Claude:** *updates the deadline*

> **You:** Delete all those old Ableton effect tasks
> 
> **Claude:** *confirms which ones, then deletes them*

> **You:** Mark all my inbox items as someday
> 
> **Claude:** *batch updates the items*

## Sync Behavior

The dashboard script automatically activates Things briefly before reading to ensure the SQLite database is up to date. Use `--no-sync` to skip this if you need maximum speed and don't mind potentially stale data.

## iOS/iPad/Watch Compatibility

Things syncs across all your devices via Things Cloud. Changes Claude makes on your Mac will sync to your iPhone, iPad, and Apple Watch automatically.

Note: The Claude mobile app cannot run these scripts directly — this skill only works in Claude.ai on Mac or Claude Code.

## About Agent Skills

This skill follows the [Agent Skills](https://agentskills.io/) open standard — a simple format for extending AI agents with specialized capabilities. Skills are just folders with a `SKILL.md` file containing instructions and optional scripts/resources.

## License

MIT

## Credits

- [things.py](https://github.com/thingsapi/things.py) by thingsapi for the Python database interface
- [Things3](https://culturedcode.com/things/) by Cultured Code for the excellent task manager
- Inspired by [things3-agent-skill](https://github.com/eugenepyvovarov/things3-agent-skill) by eugenepyvovarov
