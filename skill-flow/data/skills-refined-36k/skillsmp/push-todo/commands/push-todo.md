---
description: Show active voice tasks from Push iOS app
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Push Voice Tasks

This command fetches and displays your active voice tasks from the Push iOS app.

## Usage

- `/push-todo` - Show active tasks for current project
- `/push-todo #427` - Jump directly to task #427
- `/push-todo review` - Review existing tasks and mark completed ones
- `/push-todo connect` - Configure your Push connection

> **Note:** To see tasks from all projects, ask explicitly: "show tasks from all projects"

## Instructions

When this command is invoked:

1. **Check for connect**: First verify the config exists:
   ```bash
   test -f ~/.config/push/config && echo "configured" || echo "not configured"
   ```

2. **If not configured**: Run the connect flow (see [Connect Mode](#connect-mode) below)

3. **If configured**: Fetch tasks:
   ```bash
   source ~/.config/push/config && python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py
   ```

4. Present the tasks and ask which one to work on

5. When user selects a task, mark it as started and begin working

## Review Mode

When `/push-todo review` is invoked, use **session context** to identify completed tasks:

### Step 1: Analyze Session Context

First, recall what was worked on in this session (or the previous compacted session):
- What tasks were explicitly mentioned? (e.g., "work on #701")
- What features were implemented or bugs fixed?
- What files were edited and why?

### Step 2: Fetch Pending Tasks

```bash
source ~/.config/push/config && python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py --all --json
```

### Step 3: Match Session Work Against Tasks

For each pending task, check if it matches work done in this session:

**Explicit Match**: Task number was mentioned (e.g., "worked on #701")
- These should be marked complete unless work is clearly unfinished

**Implicit Match**: Work done aligns with task content semantically
- Compare task summary/content against session work
- Example: Task says "add review parameter to slash command" and we just added that feature

**No Match**: Task wasn't worked on this session
- Skip these (don't search codebase unnecessarily)

### Step 4: Present Findings

```
## Session Review

Based on this session, I found:

### ✅ Completed This Session
- #701 "Add review parameter" - We implemented this feature (explicit)
- #427 "Fix login bug" - We fixed the auth issue in LoginView.swift (implicit match)

### ❓ Not Worked On
- #351 "Test on smaller phone" - No related work this session
- #682 "Rework recording overlay" - No related work this session

Should I mark #701 and #427 as completed?
```

### Step 5: Mark Confirmed Tasks

```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py --mark-completed TASK_UUID
```

### Key Principle

**Session context is primary** - don't grep the entire codebase for every task. Use conversation history to identify what was actually worked on, then match against tasks semantically. This catches both:
- Explicit: User said "work on #701" but forgot to mark complete
- Implicit: User fixed something that matches a task they didn't mention

## Connect Mode

When `/push-todo connect` is invoked, generate project-specific keywords BEFORE running the connect script.

### Why Keywords Matter

Keywords help the AI route voice todos to the correct project. Generic keywords like "coding" or "programming" don't differentiate between projects. We need UNIQUE keywords that identify THIS specific project.

### Step 1: Understand the Project

Read the project context to generate meaningful keywords:

1. **Check for CLAUDE.md**:
   ```bash
   test -f CLAUDE.md && echo "found" || echo "not found"
   ```

2. **If CLAUDE.md exists**, read the header section:
   ```bash
   head -80 CLAUDE.md
   ```

3. **If no CLAUDE.md**, check for README.md:
   ```bash
   test -f README.md && head -50 README.md
   ```

### Step 2: Generate Unique Keywords

Based on the project context, generate 5-10 keywords.

**MUST include:**
- Project name and common nicknames users would say
- Domain-specific terms (e.g., "voice todo" for a voice app)
- Distinctive tech if relevant (e.g., "whisper" for speech recognition)

**MUST NOT include (these are useless for differentiation):**
- Generic terms: "coding", "programming", "development"
- Tool terms: "mac", "terminal", "cli", "ai", "task"
- Any term that applies to ALL code projects

**Think:** "What would the user SAY when creating a task for THIS project?"

### Step 3: Generate Description

Generate a short (5-15 words) description that captures what makes this project unique. NOT generic like "coding tasks" or "development work".

### Step 4: Run Connect with Keywords

```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py \
  --keywords "keyword1,keyword2,keyword3,..." \
  --description "Short unique description of this project"
```

### Examples

**For a voice todo app (Push):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py \
  --keywords "push,voice,todo,whisper,ios,swiftui,recording,speech,transcription" \
  --description "Voice-powered todo app for iOS with whisper speech recognition"
```

**For a web scraping project:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py \
  --keywords "scraper,crawler,beautifulsoup,selenium,extraction,parsing" \
  --description "Web scraping tool for data extraction"
```

**For a game engine:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py \
  --keywords "engine,graphics,rendering,physics,ecs,vulkan,gamedev" \
  --description "Custom game engine with Vulkan renderer"
```

### Fallback (No Documentation)

If no CLAUDE.md or README.md exists, generate minimal keywords from:
- Folder name
- Git repo name
- Primary file extensions (`.swift` → iOS, `.py` → Python, `.rs` → Rust)

## What is Push?

Push is a voice-powered todo app for iOS. Users capture tasks by speaking on their phone, and those tasks sync to Claude Code for implementation.

Learn more: https://pushto.do
