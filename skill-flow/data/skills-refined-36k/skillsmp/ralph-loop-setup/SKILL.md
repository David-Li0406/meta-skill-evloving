---
name: ralph-loop-setup
description: Set up or update automated task implementation system with Ralph Wiggum Loop. Use when the user wants to create or update todolist.json, progress.txt, and ralph_wiggum_loop.sh files for automated AI-driven task-based development.
---

# Ralph Loop Setup Skill

You are helping the user set up or update the 3 files needed to run a Ralph Wiggum Loop - an automated task implementation system that uses an AI coding assistant (Claude Code or Codex) to intelligently work through a project todo list. The script auto-detects which CLI is available at runtime.

**Key Feature**: Rather than strictly following priority order, Claude analyzes the full todo list and uses AI judgment to select the most impactful task based on strategic value, dependencies, likelihood of success, and logical ordering.

**Important**: This skill sets up the files. It does not run the loop itself. After setup, the user runs the loop separately.

## What You Will Create/Update

The Ralph Wiggum Loop requires 3 files in the user's project:

1. **todolist.json** - Task State Memory: tracks tasks, priorities, dependencies, and status
2. **progress.txt** - Learning Memory: logs what happened in each session for future reference
3. **ralph_wiggum_loop.sh** - Orchestration script: runs the loop, launching fresh Claude sessions

## Step 0: Check for Existing Setup

**IMPORTANT**: Before starting the setup flow, check if the Ralph Wiggum Loop files already exist in the current working directory:

1. Check for `todolist.json`
2. Check for `progress.txt`
3. Check for `ralph_wiggum_loop.sh`

Use the Glob tool to check for these files in the current working directory.

### If All 3 Files Exist → UPDATE MODE

If all 3 files already exist, the user likely wants to update their todo list. Skip to **Update Mode** below.

### If Files Don't Exist → SETUP MODE

If any files are missing, proceed with the normal **Setup Flow** below.

---

## UPDATE MODE (Files Already Exist)

When the Ralph Wiggum Loop is already set up, ask the user how they want to update their todo list.

### Step U1: Show Current Status

First, read the existing `todolist.json` and show the user:
- Project name
- Current task statistics (pending, passed, failed)
- A brief summary of existing tasks

### Step U2: Ask What They Want to Do

Use the AskUserQuestion tool to ask:

**"Your Ralph Wiggum Loop is already set up. How would you like to update your todo list?"**

Options:
1. **Add tasks from a file** - Import tasks from markdown, text, or other files
2. **Add tasks manually** - Describe new tasks to add (I'll help break them down)
3. **Review and modify existing tasks** - View, edit priorities, or remove tasks
4. **Reset todo list** - Clear all tasks and start fresh (keeps progress.txt history)

### Step U3: Handle the User's Choice

**Option 1: Add tasks from a file**
1. Ask the user to provide the file path(s) or paste the content
2. Read and parse the files to understand the new tasks
3. Extract task information (name, description, dependencies, priorities)
4. Ask about categorization and priorities
5. Show proposed new tasks and confirm with user
6. Merge new tasks into existing todolist.json (assign new IDs that don't conflict)
7. Update statistics

**Option 2: Add tasks manually**
1. Ask: "What new tasks do you want to add? Describe the features or work items."
2. Help break them down into well-structured tasks
3. Ask about dependencies on existing tasks
4. Show proposed tasks and confirm
5. Add to todolist.json with appropriate IDs and priorities
6. Update statistics

**Option 3: Review and modify existing tasks**
1. Display all tasks with their status, priority, and dependencies
2. Ask what changes they want to make:
   - Change task priority
   - Edit task description or acceptance criteria
   - Mark tasks as skipped
   - Remove tasks entirely
   - Reset failed tasks back to pending
3. Apply changes and update statistics

**Option 4: Reset todo list**
1. Confirm this is what they want (this removes all tasks)
2. Ask about their new tasks (same as Step 2B in Setup Flow)
3. Create fresh todolist.json
4. Keep progress.txt as historical record (add a separator noting the reset)

After any update, show the updated statistics and remind them how to run the loop.

---

## SETUP MODE (Fresh Setup)

## Setup Flow

### Step 1: Understand the User's Situation

First, ask the user which scenario applies to them:

**Option A**: They have existing todo list file(s) (markdown, text, notion export, etc.) that they want to convert into a structured todo list.

**Option B**: They don't have a todo list yet and want help breaking down their project into tasks.

Use the AskUserQuestion tool to present these options clearly.

### Step 2A: If User Has Existing Files

If the user has existing todo list files:

1. Ask them to provide the file path(s) or paste the content
2. Read and parse the files to understand the tasks
3. For each task/item found, extract:
   - Task name
   - Description (if available)
   - Any dependencies mentioned
   - Priority hints
4. Ask clarifying questions about:
   - Project name and description
   - Build command (e.g., `npm run build`, `go build`, `cargo build`)
   - Test command (e.g., `npm test`, `pytest`, `go test`)
   - Any special instructions for Claude
5. Ask about task categorization and priorities if not clear from the source

### Step 2B: If User Wants to Create from Scratch

If the user doesn't have existing files, conduct a discovery interview:

1. **Project Understanding**:
   - "What is the name of your project?"
   - "Can you describe what this project does in 1-2 sentences?"
   - "What technology stack are you using?" (language, framework, etc.)

2. **Goal Identification**:
   - "What is the main goal or feature you want to implement?"
   - "Are there multiple major features? If so, list them."

3. **Task Breakdown**:
   For each major goal/feature, help break it down:
   - "What are the logical steps to implement [feature]?"
   - "What needs to be done first before other tasks?"
   - "Are there any infrastructure/setup tasks needed?"

4. **Technical Details**:
   - "What command builds your project?"
   - "What command runs your tests?"
   - "Any specific coding patterns or conventions Claude should follow?"

5. **Priority and Dependencies**:
   - Help establish which tasks depend on others
   - Assign priorities (1 = highest)

### Step 3: Ask Where to Save Files

Ask the user where they want to set up the Ralph Loop files. Default to the current working directory.

### Step 4: Ask About Automated Permissions (Security Consent)

**IMPORTANT**: Before creating the files, you MUST ask the user about automated permissions. The Ralph Wiggum Loop runs Claude autonomously, which means Claude needs to perform file operations without interactive permission prompts.

Use the AskUserQuestion tool to present this consent question:

**"The Ralph Wiggum Loop runs Claude autonomously without user interaction. To work properly, it uses the `--dangerously-skip-permissions` flag, which allows Claude to create, modify, and delete files without asking for permission each time.**

**This is necessary because:**
- The loop runs non-interactively (output goes to logs, not your terminal)
- Without this flag, Claude would hang waiting for permission that never comes
- Autonomous operation is the core value of this tool

**Security implications:**
- Claude will have unrestricted file access within the working directory
- You should only run this in project directories you trust
- Review the todolist.json tasks before running to understand what changes will be made

**Do you consent to running Claude with automated permissions (--dangerously-skip-permissions)?"**

Options:
1. **Yes, enable automated permissions** - I understand the implications and want autonomous operation (Recommended)
2. **No, require manual permissions** - I want to approve each file operation manually

**If user selects Option 1 (Yes):**
- Proceed with creating the files as normal (the script already includes the flag)
- Note in the setup completion message that automated permissions are enabled

**If user selects Option 2 (No):**
- Warn the user: "Without automated permissions, the loop will hang when Claude needs to create or modify files. You would need to run Claude interactively instead of using the loop."
- Ask if they want to proceed anyway or reconsider
- If they still want to proceed, create a modified version of the script without the `--dangerously-skip-permissions` flag (though this is not recommended)

### Step 5: Create All 3 Files

#### File 1: Create ralph_wiggum_loop.sh

Create the orchestration script. You can find the full script content in the reference directory, or create it with these key features:
- Reads tasks from todolist.json
- Runs Claude Code for each task
- Updates progress.txt after each task
- Handles timeouts and retries

#### File 2: Create todolist.json

Create a customized version with the user's tasks:

```json
{
  "metadata": {
    "project": "PROJECT_NAME",
    "version": "1.0.0",
    "created": "YYYY-MM-DD",
    "last_updated": "YYYY-MM-DD",
    "description": "PROJECT_DESCRIPTION",
    "build_command": "BUILD_COMMAND_OR_EMPTY",
    "test_command": "TEST_COMMAND_OR_EMPTY",
    "extra_instructions": "ANY_SPECIAL_INSTRUCTIONS"
  },
  "priority_guidelines": {
    "description": "Priority is determined by: 1) Setup tasks first, 2) Core functionality before enhancements, 3) Foundation tasks before dependent tasks",
    "scale": "1-10 where 1 is highest priority"
  },
  "tasks": [
    {
      "id": "CATEGORY-001",
      "name": "Task name",
      "description": "Detailed description of what to implement",
      "category": "category",
      "priority": 1,
      "status": "pending",
      "failure_count": 0,
      "dependencies": [],
      "acceptance_criteria": [
        "Criterion 1",
        "Criterion 2"
      ],
      "files_likely_affected": [
        "src/file.js"
      ],
      "notes": ""
    }
  ],
  "statistics": {
    "total_tasks": N,
    "pending": N,
    "in_progress": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0
  }
}
```

**Task ID Conventions** - Use meaningful prefixes:
- `SETUP-XXX` - Setup/infrastructure tasks
- `CORE-XXX` - Core functionality
- `FEAT-XXX` - Features
- `BUG-XXX` - Bug fixes
- `UI-XXX` - User interface
- `API-XXX` - API-related
- `TEST-XXX` - Testing
- `DOC-XXX` - Documentation

#### File 3: Create progress.txt

Create the progress log file:

```
# PROJECT_NAME - Task Implementation Progress Log
# ==========================================
# This file tracks the progress of automated task implementation.
# Each entry contains: timestamp, task ID, status, summary, and lessons learned.
#
# Generated by Ralph Wiggum Loop
# Created: YYYY-MM-DD

================================================================================
```

### Step 6: Verify Setup and Provide Instructions

After creating all files, verify they exist and provide usage instructions:

```
Setup Complete! Created 3 files:

1. todolist.json - Your task list with X tasks
2. progress.txt - Progress log (empty, will be filled as tasks complete)
3. ralph_wiggum_loop.sh - The automation script

Security Note: Automated permissions (--dangerously-skip-permissions) are ENABLED.
Claude will create/modify files without asking for permission each time.
Only run this in project directories you trust.

To run the Ralph Wiggum Loop:

   ./ralph_wiggum_loop.sh [max_iterations] [todo_file]

Examples:
   ./ralph_wiggum_loop.sh              # Run until all tasks done
   ./ralph_wiggum_loop.sh 10           # Run at most 10 iterations
   ./ralph_wiggum_loop.sh 5 ./my.json  # 5 iterations with custom todo file

The loop will:
- Claude reads the todo list each iteration
- AI selects the best pending task (considering priority, dependencies, impact)
- Implements the task completely
- Updates todolist.json status and logs to progress.txt
- Repeats until all tasks completed
```

## Best Practices to Share with Users

When creating tasks, advise users to:

1. **Be Specific**: Each task should have a clear, measurable outcome
2. **Keep Tasks Small**: Tasks should be completable in under 30 minutes
3. **Define Dependencies**: Ensure foundation tasks come before dependent ones
4. **Write Clear Acceptance Criteria**: How will Claude know when it's done?
5. **Hint at Files**: The `files_likely_affected` field helps Claude focus
6. **Keep CLAUDE.md Updated**: Document your project's file organization in CLAUDE.md so Claude can find files even after reorganization
7. **Don't Worry About Outdated Paths**: The loop now uses adaptive file searching - if paths in tasks become outdated after reorganization, Claude will use Glob/Grep to locate the correct files

## Important Notes

- Always confirm the generated todo list with the user before writing files
- Offer to adjust priorities or add/remove tasks
- Make sure dependencies form a valid DAG (no circular dependencies)
- Statistics should accurately reflect the task counts
- Use today's date for created/last_updated fields
