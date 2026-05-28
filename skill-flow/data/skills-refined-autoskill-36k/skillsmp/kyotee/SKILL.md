---
name: kyotee
description: |
  Resilient, spec-driven code generation with phased orchestration.
  Like Wile E. Coyote - keeps going until it's done, even when things go wrong.

  Use when: user wants to "build a project", "create an app", needs "multi-phase
  implementation", wants "spec-driven development", or mentions "kyotee".
---

# Kyotee - Spec-Driven Development

Kyotee orchestrates complex development through structured phases.

## Main Menu

When invoked with `/kyotee`, show the main menu using `AskUserQuestion`:

```
What would you like to do?

Options:
1. Build something new - Start discovery for a new project
2. Resume project - Continue an existing .kyotee/ project
3. Manage patterns - List, edit, or add tech stack patterns
4. Help - Learn how Kyotee works
```

### Option 1: Build Something New
→ Go to DISCOVERY MODE

### Option 2: Resume Project
Check for `.kyotee/` directory in current folder:
- If exists: Read state and summarize progress, ask to continue
- If not: "No project found. Would you like to start a new one?"

### Option 3: Manage Patterns
Show pattern management menu:

```
Pattern Management

Options:
1. List patterns - Show available tech stack patterns
2. View pattern - Read a specific pattern's content
3. Edit pattern - Modify an existing pattern
4. Create pattern - Add a new tech stack pattern
5. Back - Return to main menu
```

#### List Patterns
Read files from `~/.claude/skills/kyotee/references/` and display:
```
Available Patterns:
- hono-datastar.md - Hono + Datastar on Cloudflare Workers
- go-gin.md - Go + Gin REST APIs
- nextjs.md - Next.js + Tailwind
- fastapi.md - Python + FastAPI
- [any custom patterns]
```

#### View Pattern
Ask which pattern to view, then read and display its contents.

#### Edit Pattern
Ask which pattern to edit, read current content, then use Edit tool to modify based on user instructions.

#### Create Pattern
Ask for:
1. Pattern name (e.g., "rust-axum")
2. Framework/stack description
3. Key conventions to include

Then create a new markdown file in `~/.claude/skills/kyotee/references/` following the pattern template structure.

### Option 4: Help
Display a summary of how Kyotee works:
- Discovery → Spec → Implementation flow
- Available patterns
- How to add custom patterns

---

# DISCOVERY MODE

Goal: Build a complete spec through conversation before writing any code.

## Discovery Flow

Use `AskUserQuestion` to gather requirements iteratively:

### Step 1: Project Type
```
What would you like to build?

Options:
- Web Application
- CLI Tool
- API/Backend
- Library/Package
```

### Step 2: Tech Stack
Based on project type, ask about tech stack:

For Web Apps:
```
What tech stack?

Options:
- Hono + Cloudflare Workers (edge, fast)
- Next.js + Vercel (React, full-stack)
- Go + Templ + HTMX (server-rendered)
- Other (specify)
```

### Step 3: Features
```
What are the core features? (Select all that apply)

Options will vary by project type...
```

### Step 4: Additional Details
Ask clarifying questions based on previous answers:
- Authentication needed?
- Database/storage?
- Specific integrations?
- Styling preferences?

### Step 5: Spec Confirmation
Once enough info gathered, generate and display the spec:

```markdown
# Project Spec

## Overview
[One-line description]

## Tech Stack
- Language: [X]
- Framework: [Y]
- Deployment: [Z]

## Features
1. [Feature 1]
2. [Feature 2]
...

## Requirements
- [Specific requirement 1]
- [Specific requirement 2]
```

Then ask:
```
Ready to implement?

Options:
- Yes, start building
- Edit spec first
- Save spec and exit
```

If "Yes" → Transition to Execute Mode
If "Edit" → Let user modify, then re-confirm
If "Save" → Write spec to `.kyotee/spec.md` and exit

---

# EXECUTE MODE

## The 5 Phases (MUST be followed in order)

```
┌─────────┐    ┌──────┐    ┌───────────┐    ┌────────┐    ┌─────────┐
│ CONTEXT │ →  │ PLAN │ →  │ IMPLEMENT │ →  │ VERIFY │ →  │ DELIVER │
└─────────┘    └──────┘    └───────────┘    └────────┘    └─────────┘
                                ↑                │
                                └────────────────┘
                                  (loop on failure)
```

### Phase 1: CONTEXT (Explore Agent)

**Purpose**: Understand codebase, identify matching skill, validate requirements.

Launch Task with `subagent_type: "Explore"`:

```
Analyze this project for implementing: {SPEC_SUMMARY}

Tasks:
1. Search codebase for existing relevant files
2. Identify tech stack from spec:
   - Language: {LANGUAGE}
   - Framework: {FRAMEWORK}
   - Deployment: {DEPLOYMENT}

3. Check for matching skill in ~/.kyotee/skills/:
   - Read skill files to find best match
   - If no match, note that we need generic patterns

4. Check if existing code matches spec:
   - If mismatch (e.g., static HTML when spec says Hono), FLAG IT
   - Do NOT assume existing code is "acceptable"

5. List required setup:
   - Config files needed
   - Dependencies to install
   - Entry points to create

Report:
- skill_to_use: [skill name or "none"]
- tech_stack_match: true/false
- blocking_issues: [list]
- required_setup: [list]
```

**Output**: Context pack with skill selection and setup requirements.

### Phase 2: PLAN (Plan Agent)

**Purpose**: Create step-by-step implementation plan.

First, if a skill was identified, READ it:
```
Read ~/.kyotee/skills/{skill_name}.toml
```

Launch Task with `subagent_type: "Plan"`:

```
Create implementation plan for: {SPEC_SUMMARY}

Tech Stack: {LANGUAGE} + {FRAMEWORK} on {DEPLOYMENT}
Skill Patterns: {SKILL_CONTENT or "none - use best practices"}

Requirements from spec:
{REQUIREMENTS_LIST}

Your plan MUST:
1. Include infrastructure setup FIRST:
   - package.json / go.mod / requirements.txt
   - Config files (tsconfig.json, wrangler.toml, etc.)
   - Entry point file with framework bootstrap

2. Map EVERY requirement to a plan step
   - No requirement should be missing

3. Follow skill patterns for:
   - Project structure
   - File naming conventions
   - Code patterns

Output step-by-step plan with:
- step_number
- description
- files_to_create: [list]
- files_to_modify: [list]
```

**Output**: Ordered list of implementation steps.

### Phase 3: IMPLEMENT (Direct Tool Use)

**Purpose**: Write all code files.

Do NOT spawn an agent. Use Write/Edit tools directly.

**Order of operations**:
1. **Config files first**:
   - package.json / go.mod / Cargo.toml
   - tsconfig.json / pyproject.toml
   - wrangler.toml / vercel.json / Dockerfile

2. **Entry point**:
   - src/index.ts / main.go / app.py
   - Must use the framework from spec (not static HTML!)

3. **Core modules**:
   - Routes, handlers, components
   - Follow skill patterns if available

4. **Features**:
   - Implement each feature from plan
   - Check off requirements as completed

5. **Assets**:
   - Styles, static files
   - Follow skill conventions for paths

**Critical Rules**:
- NEVER skip config files
- NEVER generate static HTML when spec says "use framework X"
- ALWAYS follow skill patterns when available
- If unsure, READ the skill file again

### Phase 4: VERIFY (Code Reviewer Agent)

**Purpose**: Validate implementation matches spec exactly.

Launch Task with `subagent_type: "feature-dev:code-reviewer"`:

```
Review implementation against spec:

Spec Requirements:
{SPEC_SUMMARY}

Expected Tech Stack:
- Language: {LANGUAGE}
- Framework: {FRAMEWORK}
- Deployment: {DEPLOYMENT}

Verify:
1. Tech Stack Compliance:
   - Is {FRAMEWORK} actually imported and used?
   - Do config files exist and are they valid?
   - Are dependencies correct?

2. Feature Completeness:
   For each requirement:
   {REQUIREMENTS_CHECKLIST}
   - Is it implemented? Where?

3. File Structure:
   - Does it match skill's project structure?
   - Are all expected files present?

4. Run checks if possible:
   - Type check (tsc --noEmit)
   - Lint check
   - Build check

Report:
- all_passed: true/false
- tech_stack_verified: true/false
- missing_requirements: [list]
- failures: [list with details]
- suggested_fixes: [list]
```

**If failures exist**: Loop back to Phase 3 (Implement) to fix issues.

**If skill pattern caused issues**: Note it for skill improvement.

### Phase 5: DELIVER

**Purpose**: Summarize completion and next steps.

Output format:
```markdown
# Implementation Complete ✓

## What Was Built
{SUMMARY}

## Files Created
{FILE_LIST}

## Tech Stack
- {LANGUAGE} + {FRAMEWORK}
- Deployment: {DEPLOYMENT}

## Next Steps
1. {INSTALL_COMMAND}
2. {DEV_COMMAND}
3. {DEPLOY_COMMAND}

## Skill Used
{SKILL_NAME} from ~/.kyotee/skills/
```

---

# SKILL SYSTEM

Skills are tech-stack specific knowledge stored in `~/.kyotee/skills/`.

## Skill File Format (TOML)

```toml
name = "Descriptive Name"
description = "When to use this skill"
tags = ["tag1", "tag2"]

[conventions]
project_structure = """
src/
  index.ts
  ...
"""
naming = "kebab-case for files, PascalCase for components"
file_extensions = ".ts, .tsx"

[patterns]
entry_point = """
// Code pattern for entry point
"""

component = """
// Code pattern for components
"""

[setup]
commands = [
  "bun install",
  "bun run dev"
]

[docs]
urls = ["https://..."]
```

## Finding Skills

During Context phase:
1. Read files in `~/.kyotee/skills/`
2. Match based on:
   - Tech stack keywords (hono, cloudflare, go, next)
   - Tags in skill file
   - Description matching

## Creating New Skills

If no matching skill exists for a tech stack:
1. Complete the implementation using best practices
2. After successful verify, offer to create a skill:

```
No skill existed for {TECH_STACK}. Want me to create one?

This will save patterns from this implementation to:
~/.kyotee/skills/{suggested-name}.toml

Options:
- Yes, create skill
- No, skip
```

## Improving Skills

If a skill caused issues during implementation:
1. Note the issue in Deliver phase
2. Offer to update the skill:

```
The {SKILL_NAME} skill had an issue:
{ISSUE_DESCRIPTION}

Want me to update the skill with the fix?

Options:
- Yes, update skill
- No, leave as is
```

---

# AUTONOMOUS EXECUTION

The goal is: **approve the spec, walk away, come back to working code.**

## Trust Boundary

```
┌──────────────────────────────────────────────┐
│  DISCOVERY (Interactive)                      │
│  User answers questions, reviews spec         │
│  ════════════════════════════════════════════│
│           ↓ TRUST BOUNDARY ↓                  │
│  ════════════════════════════════════════════│
│  EXECUTE (Autonomous)                         │
│  Context → Plan → Implement → Verify → Deliver│
│  Runs without prompts if permissions set      │
└──────────────────────────────────────────────┘
```

## Reducing Permission Prompts

For unattended execution, configure Claude Code permissions.

In `.claude/settings.json`:
```json
{
  "permissions": {
    "allow": [
      "Write(*)",
      "Edit(*)",
      "Bash(bun *)",
      "Bash(npm *)",
      "Bash(wrangler *)",
      "Bash(go *)",
      "Bash(tsc *)"
    ]
  }
}
```

See `references/reducing-prompts.md` for detailed configuration.

## Execution Behavior

Once spec is approved:
1. **Don't ask** - Just execute the phases
2. **Don't pause** - Move through phases automatically
3. **Loop on failure** - Fix issues and re-verify without asking
4. **Only stop** - On unrecoverable errors or max retries

---

# CRITICAL RULES

1. **NEVER skip phases** - Each phase validates the previous
2. **Spec is law** - Never deviate from the specified tech stack
3. **Skills guide, don't override** - Skills provide patterns, spec provides requirements
4. **Loop until correct** - If verify fails, go back to implement
5. **Improve skills** - Update skills when issues are found
6. **Infrastructure first** - Config files before features, always
7. **Autonomous after approval** - Don't ask permission during execute mode

---

# EXAMPLE SESSION

```
User: /kyotee

Kyotee: What would you like to build?
[AskUserQuestion: Web App / CLI / API / Library]

User: Web App

Kyotee: What tech stack?
[AskUserQuestion: Hono+Cloudflare / Next.js / Go+HTMX / Other]

User: Hono + Cloudflare

Kyotee: What's the purpose of this web app?

User: A marketing site for my CLI tool called "kyotee"

Kyotee: Any specific features needed?
[AskUserQuestion with options based on marketing sites]

User: Hero section, how it works, installation instructions, interactive demo

Kyotee: Here's your spec:

# Kyotee Marketing Website

## Tech Stack
- Language: TypeScript
- Framework: Hono
- Deployment: Cloudflare Workers
- Interactivity: Datastar

## Features
1. Hero section with ASCII art logo
2. "How it works" - 5 phase explanation
3. Installation instructions
4. Interactive demo

Ready to implement?
[AskUserQuestion: Yes / Edit / Save & Exit]

User: Yes

[Executes Context → Plan → Implement → Verify → Deliver]
[Uses cloudflare-hono-datastar skill for patterns]
[Creates all files, verifies, delivers summary]
```
