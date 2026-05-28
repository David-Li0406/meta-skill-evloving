---
name: summary-generator
description: Generates session summaries with resume prompts and self-reflection. Use when completing features, before context limits (~50% capacity), or when user says "summary", "wrap up", "save progress", "end session". Creates markdown in .claude/summaries/ with completed work, remaining tasks, and lessons learned.
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git log:*), Bash(git status:*), Write
---

# Session Summary Generator

## Overview

This skill creates comprehensive session summaries for complex multi-session work, enabling seamless resumption of tasks. It generates a markdown file in `.claude/summaries/` with a standardized format.

## MANDATORY Sections

Every summary MUST include these critical sections:

1. **Resume Prompt** - Copy-paste ready prompt with:
   - Remaining tasks as numbered list
   - Options for next direction (if applicable)
   - Key files to review first
   - Any blockers or decisions needed

2. **Self-Reflection** - Learning from the session:
   - What worked well (patterns to repeat)
   - What failed and why (patterns to avoid)
   - Specific improvements for next session
   - Command/tool usage lessons

## When to Use

### Trigger Phrases (User Says)

**To Generate Summary:**
- "wrap up"
- "generate summary"
- "save progress"
- "end session"
- "let's wrap up"

**To Resume Previous Session:**
- "resume from last session"
- "continue from where we left off"
- "pick up where we stopped"
- "resume session"

### Auto-Suggest Triggers

Proactively suggest generating a summary when:
- Multiple files have been modified in the session
- A feature implementation is complete
- The conversation has been long (many exchanges)
- User mentions ending their work session

## Resuming Sessions

When user says "resume from last session":

1. **Find the latest summary:**
   ```bash
   # Find most recent summary folder and file
   ls -td .claude/summaries/*/ | head -1 | xargs -I {} sh -c 'ls -t {}*.md | head -1'
   ```

2. **Read the summary file** and extract the Resume Prompt section

3. **Present to user:**
   - Show what was completed last session
   - List remaining tasks
   - Ask which task to start with (if options exist)

4. **Continue from the Resume Prompt** as if it were the user's initial message

## Output Location

Session summaries are stored in: `.claude/summaries/MM-DD-YYYY/YYYYMMDD-HHmm_feature-name.md`

Example: `.claude/summaries/01-05-2026/20260105-1430_phase1-foundation.md`

## Instructions

### Step 1: Analyze Current Work

Run these commands to understand what was done:

```bash
git status
git diff --stat
git log --oneline -10
```

Review the conversation history to identify:
- What was accomplished
- Key decisions made
- Files created or modified
- Any remaining tasks

### Step 2: Generate Summary File

Create the summary using the template in [TEMPLATE.md](TEMPLATE.md).

Key sections to include:
1. **Overview**: Brief description of session focus
2. **Completed Work**: Bullet points of accomplishments
3. **Key Files Modified**: Table of files and changes
4. **Design Patterns Used**: Important architectural decisions
5. **Remaining Tasks**: What's left to do
6. **Resume Prompt**: Copy-paste instructions for next session

### Step 3: Create Resume Prompt (REQUIRED)

The resume prompt is the MOST IMPORTANT part of the summary. It must be:
- **Copy-paste ready** - User can start a new session with this exact text
- **Self-contained** - Includes all context needed to continue
- **Action-oriented** - Clear next steps, not just status

**Required Elements:**

```markdown
## Resume Prompt

Resume [PROJECT_NAME] - [FEATURE_NAME]

### Context
Previous session completed:
- [Accomplishment 1]
- [Accomplishment 2]

Summary file: .claude/summaries/MM-DD-YYYY/YYYYMMDD-HHmm_feature-name.md

### Key Files
Review these first:
- [path/to/file.tsx] - [why it matters]
- [path/to/file.ts] - [why it matters]

### Remaining Tasks
1. [ ] [Task with enough detail to start immediately]
2. [ ] [Next task]
3. [ ] [Following task]

### Options (if applicable)
Choose one direction:
A) [Option A description] - [trade-offs]
B) [Option B description] - [trade-offs]

### Blockers/Decisions Needed
- [Any blockers that need resolution]
- [Decisions user needs to make]

### Environment
- Port: [if applicable]
- Database: [migration status]
- Other setup: [any requirements]
```

### Step 4: Analyze Token Usage

Review the conversation for token efficiency opportunities using [analyzers/token-analyzer.md](analyzers/token-analyzer.md) and [guidelines/token-optimization.md](guidelines/token-optimization.md).

**Look for:**
1. **File Reading Patterns**
   - Files read multiple times → Suggest caching or using Grep
   - Large files read fully when Grep would suffice
   - Reading generated files (node_modules, build artifacts)

2. **Search Inefficiencies**
   - Redundant searches → Recommend consolidating queries
   - Overly broad glob patterns
   - Multiple searches that could be combined

3. **Response Verbosity**
   - Verbose explanations → Note opportunities for conciseness
   - Repeated explanations of same concepts
   - Unnecessary multi-paragraph responses for simple tasks

4. **Good Practices to Acknowledge**
   - Effective use of Grep before Read
   - Targeted searches with appropriate scope
   - Concise, actionable responses
   - Efficient agent usage

**Generate token usage report with:**
- Estimated total tokens (use chars/4 approximation)
- Token breakdown by category (file ops, code gen, explanations, searches)
- Efficiency score (0-100) using scoring system from token-analyzer.md
- Top 5 optimization opportunities (prioritized by impact)
- Notable good practices observed

See [analyzers/token-analyzer.md](analyzers/token-analyzer.md) for detailed analysis methodology.

### Step 5: Analyze Command Accuracy

Review tool calls for accuracy and error patterns using [analyzers/command-analyzer.md](analyzers/command-analyzer.md) and [guidelines/command-accuracy.md](guidelines/command-accuracy.md).

**Look for:**
1. **Failed Commands and Causes**
   - Path errors (backslashes, wrong case, file not found)
   - Import errors (wrong module path, wrong import style)
   - Type errors (property doesn't exist, type mismatch)
   - Edit errors (string not found, whitespace issues)

2. **Error Patterns**
   - Categorize by type: path, syntax, permission, logic
   - Identify recurring issues (same mistake multiple times)
   - Note severity: critical, high, medium, low
   - Calculate time wasted on failures and retries

3. **Recovery and Improvements**
   - How quickly errors were fixed
   - Whether verification prevented errors
   - Improvements from previous sessions
   - Good patterns that prevented errors

**Generate command accuracy report with:**
- Total commands executed
- Success rate percentage
- Failure breakdown by category
- Top 3 recurring issues with root cause analysis
- Actionable recommendations for prevention
- Improvements observed from past sessions

See [analyzers/command-analyzer.md](analyzers/command-analyzer.md) for detailed analysis methodology.

### Step 6: Self-Reflection (REQUIRED)

This section captures learnings to improve future sessions. Be honest and specific.

**Required Elements:**

#### What Worked Well (Patterns to Repeat)
Identify 2-3 approaches that were effective:
- Efficient tool usage patterns
- Good decision-making moments
- Successful problem-solving strategies

#### What Failed and Why (Patterns to Avoid)
Be specific about failures:
- Commands that failed and root cause
- Approaches that wasted time
- Assumptions that were wrong

#### Specific Improvements for Next Session
Actionable items:
- [ ] Verify X before doing Y
- [ ] Use tool A instead of B for this type of task
- [ ] Check file exists before editing

#### Session Learning Summary

Create a brief "lessons learned" that could be added to CLAUDE.md if the pattern is important enough:

```markdown
## Session Learning

### Successes
- [Pattern]: [Why it worked]

### Failures
- [Error]: [Root cause] → [Prevention]

### Recommendations
- [Specific actionable improvement]
```

**Self-Reflection Questions to Answer:**
1. What commands failed? Why? How to prevent?
2. What took longer than expected? Why?
3. What would I do differently if starting over?
4. What patterns should be documented for future sessions?
5. Were there any "aha moments" worth remembering?

## Example Usage

When user says: "Let's wrap up for today" or "wrap up"

Response:
1. Analyze git changes and conversation history
2. Create `.claude/summaries/12-30-2025/20251230-1645_enrollment-improvements.md`
3. Provide the resume prompt for the next session
4. Suggest: "When context gets long, consider starting a new chat with the resume prompt"

When user says: "resume from last session"

Response:
1. Find the latest summary file in `.claude/summaries/`
2. Read and parse the Resume Prompt section
3. Present remaining tasks and ask which to start with
4. Continue as if the Resume Prompt was the user's request

## Tips

- Keep summaries focused on a single feature or area
- Include exact file paths for easy navigation
- Note any environmental setup needed (database migrations, etc.)
- Flag any blocking issues or decisions made
- Reference the CLAUDE.md file patterns when applicable

## Quality Checklist

Before finalizing the summary, verify:

- [ ] **Resume Prompt** is copy-paste ready with all context
- [ ] **Remaining Tasks** are numbered and actionable
- [ ] **Options** are provided if there are multiple valid directions
- [ ] **Self-Reflection** includes honest assessment of failures
- [ ] **Improvements** are specific and actionable (not vague)
- [ ] **Key Files** have clickable paths for navigation
- [ ] **Environment** notes any setup requirements (port, migrations)

## Anti-Patterns to Avoid

- Generic summaries like "made progress on feature"
- Resume prompts that require reading the full summary
- Self-reflection that only mentions successes
- Vague improvements like "be more careful"
- Missing blockers or decisions that will stall next session
