---
name: p6-gui-automation
description: Expert Python and GUI automation skill for controlling Oracle Primavera P6 Professional desktop application. This skill should be used when building voice-driven agents, automating P6 GUI interactions via pywinauto, implementing Whisper-based voice transcription, or developing AI tools for schedule management through direct GUI control. Includes pywinauto patterns, P6 hotkeys, threading guidelines, and tool definitions.
---

# P6 GUI Automation Expert Skill

This skill provides specialized knowledge for building automation tools that control Oracle Primavera P6 Professional through direct GUI interaction, with optional voice control via OpenAI Whisper.

## When to Use This Skill

Use this skill when:

- Building voice-driven AI agents for P6 Professional
- Automating P6 GUI interactions via pywinauto
- Implementing keyboard navigation in P6 grids
- Creating overlay interfaces for voice commands
- Developing LLM tool definitions for GUI control
- Troubleshooting pywinauto window detection issues
- Implementing threading patterns for Whisper transcription

## 3-Layer Architecture

All P6 GUI automation follows a strict 3-layer architecture:

### Layer 1: Directive (The Goal)

- **Source**: PRD.md or user voice command
- **Role**: Defines WHAT to accomplish
- **Example**: "Change activity A1010 duration to 15 days"

### Layer 2: Orchestration (The Brain)

- **Source**: `src/ai/agent.py` or LLM with tool definitions
- **Role**: Decides WHICH tools to call and in what order
- **Key File**: `P6 GUI Automation/src/ai/gui_tools.py`
- **System Prompt**: Must explicitly state the agent controls GUI directly, not SQL

### Layer 3: Execution (The Tools)

Two sub-systems exist at this layer:

#### A. The "Hands" (GUI Automation)

- **Key File**: `src/automation/activities.py`
- **Library**: pywinauto
- **Pattern**: Keyboard navigation (TAB, HOME, hotkeys) over mouse clicks
- **Safety**: All operations check SAFE_MODE before execution

#### B. The "Ears" (Voice Input)

- **Key File**: `P6 GUI Automation/src/gui/whisper_handler.py`
- **Library**: openai-whisper + pyaudio
- **Critical**: Whisper transcribe() MUST run in daemon thread

## Core Workflows

### Connecting to P6 Professional

To connect to a running P6 instance:

```python
from src.automation.base import P6AutomationBase

# Create automation instance
p6 = P6AutomationBase(safe_mode=True)

# Connect to running P6
p6.connect(start_if_not_running=False)

# Verify connection
if p6.is_connected():
    print(f"Connected: {p6.get_window_title()}")
```

Window title pattern for P6: `"Primavera P6 Professional - *"` or `"Oracle Primavera P6 - *"`

### Navigating to Activities

To select an activity by ID using keyboard navigation:

```python
from src.automation.activities import P6ActivityManager

manager = P6ActivityManager(p6.main_window, safe_mode=True)

# Select by ID using Ctrl+F find
success = manager.select_activity("A1010")

# Navigate to specific columns using TAB
columns = manager.get_visible_columns()
target_index = columns.index("Original Duration")
# Use HOME to reset, then TAB to target column
```

Reference [references/pywinauto-patterns.md](references/pywinauto-patterns.md) for detailed navigation patterns.

### Editing Activity Fields

To edit a field value in the P6 grid:

```python
# Edit using keyboard navigation
success = manager.edit_activity_field(
    activity_id="A1010",
    field_name="Original Duration",
    value="15d"
)
```

The edit flow:
1. Select activity via Ctrl+F
2. Get visible columns and calculate TAB count
3. Press HOME then TAB to target column
4. Press F2 to enter edit mode
5. Type value and press ENTER

### Voice-Driven Command Flow

Complete voice command workflow:

```python
from P6_GUI_Automation.src.gui.whisper_handler import AsyncWhisperTranscriber
from P6_GUI_Automation.src.ai.gui_tools import P6GUITools, P6GUIAgent

# Initialize with callbacks
transcriber = AsyncWhisperTranscriber(
    model_name="base",
    on_model_loaded=lambda: print("Whisper ready"),
    on_transcription=handle_command
)

# Load model in background (non-blocking)
transcriber.load_model_async()

# When user releases record button:
def on_record_release():
    transcriber.stop_and_transcribe_async()  # Returns via callback

# Handle transcribed command
def handle_command(text: str):
    agent = P6GUIAgent(main_window, safe_mode=True)
    result = agent.execute_command(text)
    update_overlay_status(result)
```

Reference [references/threading-guidelines.md](references/threading-guidelines.md) for threading patterns.

## Available GUI Tools

The P6GUITools class provides 12 tools for LLM function calling:

### Selection Tools
- `select_activity(activity_id)` - Select single activity via Ctrl+F
- `select_all_activities()` - Select all activities (Ctrl+A)
- `clear_selection()` - Clear current selection

### Navigation Tools
- `go_to_first_activity()` - Navigate to first activity (Ctrl+HOME)
- `go_to_last_activity()` - Navigate to last activity (Ctrl+END)
- `navigate_to_activity(activity_id)` - Jump to specific activity

### Editing Tools (require unsafe mode)
- `update_activity_gui(activity_id, field, value)` - Edit field value
- `add_activity_gui(wbs_path)` - Add new activity
- `delete_activity_gui(activity_id)` - Delete activity
- `set_activity_constraint(activity_id, constraint_type, date)` - Set constraint
- `clear_activity_constraint(activity_id)` - Remove constraint

### Scheduling Tools (require unsafe mode)
- `reschedule_project_gui()` - Run F9 schedule calculation

### Query Tools
- `get_visible_columns()` - Get current column headers

Reference tool definitions in `P6 GUI Automation/src/ai/gui_tools.py`.

## P6 Hotkeys Reference

Essential keyboard shortcuts for P6 automation:

| Action | Hotkey | Notes |
|--------|--------|-------|
| Find Activity | Ctrl+F | Opens find dialog |
| Edit Cell | F2 | Enter edit mode |
| Confirm Edit | ENTER | Save and exit cell |
| Cancel Edit | ESC | Discard changes |
| Schedule (F9) | F9 | Run schedule calculation |
| First Activity | Ctrl+HOME | Navigate to top |
| Last Activity | Ctrl+END | Navigate to bottom |
| Select All | Ctrl+A | Select all visible |
| Next Cell | TAB | Move right in grid |
| Previous Cell | Shift+TAB | Move left in grid |
| Add Activity | INSERT | Add new row |
| Delete Activity | DELETE | Delete selected |

Full reference in [references/p6-hotkeys-reference.md](references/p6-hotkeys-reference.md).

## Voice Commands Catalog

Example voice commands and their mappings:

| Voice Command | Tool Called | Parameters |
|---------------|-------------|------------|
| "Select activity A1010" | select_activity | activity_id="A1010" |
| "Go to first activity" | go_to_first_activity | - |
| "Change duration to 15 days" | update_activity_gui | field="Duration", value="15d" |
| "Run the schedule" | reschedule_project_gui | - |
| "Set start on or after January 15" | set_activity_constraint | constraint_type="SOOA", date="2025-01-15" |

Reference [references/voice-commands-catalog.md](references/voice-commands-catalog.md) for full catalog.

## Safety Guidelines

### SAFE_MODE Protection

All destructive operations check SAFE_MODE before execution:

```python
# In automation methods
def edit_activity_field(self, activity_id, field_name, value):
    self._check_safe_mode("edit activity field")
    # ... proceed with edit
```

Set via environment variable:
```bash
export SAFE_MODE=true   # Block all edits (default)
export SAFE_MODE=false  # Allow edits
```

Or programmatically:
```python
manager = P6ActivityManager(main_window, safe_mode=True)
```

### Logging Requirements

All operations must be logged:

```python
from src.utils import logger

logger.info(f"Selecting activity: {activity_id}")
logger.debug(f"Visible columns: {columns}")
logger.warning(f"SAFE_MODE blocked: {operation}")
logger.error(f"Failed to find activity: {activity_id}")
```

Logs written to `logs/app.log`.

### Error Recovery

If automation fails:
1. Capture screenshot via `capture_error_screenshot()`
2. Log full error context
3. Attempt recovery via ESC key to cancel dialogs
4. Re-detect P6 main window
5. Report failure to user

## Threading Guidelines

### Critical Rule

Whisper `transcribe()` is CPU-intensive and BLOCKING. It MUST run in a daemon thread:

```python
import threading

def transcribe_in_background(audio_data, callback):
    def worker():
        text = whisper_model.transcribe(audio_data)
        # Use tkinter's after() to update UI from main thread
        root.after(0, lambda: callback(text))
    
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
```

### UI Update Pattern

Never update tkinter widgets from background threads:

```python
# WRONG - will crash
def on_transcription(text):
    label.config(text=text)  # Called from worker thread!

# CORRECT - schedule on main thread
def on_transcription(text):
    root.after(0, lambda: label.config(text=text))
```

Reference [references/threading-guidelines.md](references/threading-guidelines.md) for patterns.

## Development Workflow

### Testing P6 Connection

Use the validation script:

```bash
python .claude/skills/p6-gui-automation/scripts/validate_p6_connection.py
```

### Discovering UI Elements

To discover P6 control identifiers:

```bash
python .claude/skills/p6-gui-automation/scripts/capture_ui_elements.py
```

### Testing Voice Integration

Verify Whisper and microphone:

```bash
python .claude/skills/p6-gui-automation/scripts/test_voice_integration.py
```

### Running the Voice Agent

```bash
cd "P6 GUI Automation"
python main.py --safe-mode      # Safe mode (recommended for testing)
python main.py --unsafe         # Allow edits
python main.py --model small    # Use larger Whisper model
python main.py --no-whisper     # Test UI without Whisper
```

## Bundled Resources Reference

- **[references/pywinauto-patterns.md](references/pywinauto-patterns.md)**: pywinauto patterns for P6 window detection and control
- **[references/p6-hotkeys-reference.md](references/p6-hotkeys-reference.md)**: Complete P6 keyboard shortcut reference
- **[references/voice-commands-catalog.md](references/voice-commands-catalog.md)**: Supported voice commands and mappings
- **[references/threading-guidelines.md](references/threading-guidelines.md)**: Threading patterns for Whisper and tkinter
- **[scripts/validate_p6_connection.py](scripts/validate_p6_connection.py)**: Test P6 automation connectivity
- **[scripts/capture_ui_elements.py](scripts/capture_ui_elements.py)**: Discover P6 UI controls
- **[scripts/test_voice_integration.py](scripts/test_voice_integration.py)**: Test Whisper integration
- **[assets/example-prd.md](assets/example-prd.md)**: Example PRD for voice agent tasks

## Notes

- Never guess P6 hotkeys; verify against official documentation or test manually
- P6 grids are finicky; if TAB navigation fails, reset cursor position via Ctrl+F
- Always test automation with SAFE_MODE=true before enabling edits
- Whisper model loading takes 5-30 seconds depending on model size
- Use "base" model for speed/accuracy balance; "small" for better accuracy
- Ensure ffmpeg is installed (required by Whisper)
