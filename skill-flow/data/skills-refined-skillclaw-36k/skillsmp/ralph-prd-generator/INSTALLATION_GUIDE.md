# Ralph PRD Generator - Installation & Usage Guide

## What This Skill Does

Creates detailed Product Requirements Documents (PRDs) using Claude Haiku for cost-effective planning. Can:

- ✅ Generate PRDs from feature descriptions
- ✅ Convert GitHub issues into structured PRDs
- ✅ Uses Claude Haiku model for economical document generation
- ✅ Saves to your project's `tasks/` directory

---

## Installation (Project-Local)

This skill is designed to be **project-specific** - installed in your project directory rather than globally.

### Step 1: Create Skills Directory in Your Project

```bash
# Navigate to your project root
cd ~/Work/htdocs/Enskiedutech  # or your project path

# Create the skills directory structure
mkdir -p .claude/skills/ralph-prd-generator
```

### Step 2: Copy the Skill File

```bash
# Copy the SKILL.md file to your project
cp /path/to/ralph-prd-generator/SKILL.md .claude/skills/ralph-prd-generator/
```

Or manually create `.claude/skills/ralph-prd-generator/SKILL.md` and paste the content.

### Step 3: Verify Installation

```bash
# Check the file exists
ls -la .claude/skills/ralph-prd-generator/

# Should see:
# SKILL.md
```

### Step 4: Create Tasks Directory

```bash
# Create the output directory for PRDs
mkdir -p tasks
```

Your project structure should now look like:

```
your-project/
├── .claude/
│   └── skills/
│       └── ralph-prd-generator/
│           └── SKILL.md
├── tasks/                    # PRDs will be saved here
│   └── (PRD files will appear here)
├── src/
├── package.json
└── ... (rest of your project)
```

---

## How to Use

### Method 1: Create PRD from Feature Description

Simply ask Claude Code to create a PRD:

```
"Create a PRD for a user authentication system with email and password login"
```

**What happens:**

1. Claude will ask 3-5 clarifying questions with multiple choice options
2. You answer (e.g., "1A, 2C, 3B")
3. Claude generates a complete PRD
4. Saves to `tasks/prd-[feature-name].md`

**Example conversation:**

```
You: "Create a PRD for adding email notifications to our app"

Claude: "I'll help you create a PRD for email notifications. A few clarifying questions:

1. What is the primary goal?
   A. Keep users informed of important updates
   B. Drive user engagement and retention
   C. Reduce support burden
   D. Other: [specify]

2. What events should trigger notifications?
   A. Account activity only (login, password change)
   B. Content updates (new messages, comments)
   C. System alerts (errors, warnings)
   D. All of the above

3. Scope for MVP?
   A. Basic email sending only
   B. Include email templates and customization
   C. Include user preferences/opt-out
   D. Full notification center with history"

You: "1A, 2B, 3C"

Claude: [Generates complete PRD and saves to tasks/prd-email-notifications.md]
```

---

### Method 2: Convert GitHub Issue to PRD

When you have an existing GitHub issue that needs a proper PRD:

```
"Convert GitHub issue #123 to a PRD"
```

Or provide the issue URL:

```
"Convert this GitHub issue to a PRD: https://github.com/user/repo/issues/123"
```

**What happens:**

1. Claude analyzes the GitHub issue content
2. Extracts key requirements and context
3. Asks 2-3 clarifying questions if needed
4. Generates structured PRD with all sections
5. Includes reference to original issue
6. Saves to `tasks/prd-[feature-name].md`

**Example:**

```
You: "Convert GitHub issue #45 to a PRD"

Claude: "I'll convert GitHub issue #45 into a structured PRD. The issue describes
adding dark mode support. A couple of clarifying questions:

1. Scope?
   A. MVP - basic light/dark toggle
   B. Full implementation with theme customization

2. Persistence?
   A. Session only
   B. Save user preference

You: "1A, 2B"

Claude: [Creates PRD from issue with reference link]
✓ Saved to tasks/prd-dark-mode-support.md
```

---

## Usage Patterns

### Pattern 1: Planning a New Feature

```
"Use ralph-prd-generator to create a PRD for [feature description]"
```

### Pattern 2: Converting Existing Issues

```
"Convert issue #[number] to PRD using ralph-prd-generator"
```

### Pattern 3: Quick PRD Generation

```
"Create a PRD for [feature]"
```

Claude Code will automatically use the skill when it detects PRD-related requests.

---

## What Gets Generated

Each PRD includes:

### 1. Introduction/Overview

- Feature description
- Problem statement
- If from GitHub: Source reference

### 2. Goals

- Measurable objectives
- Success criteria

### 3. User Stories

- Title and description
- Acceptance criteria (verifiable)
- Special note for UI stories: includes "Verify in browser using dev-browser skill"

### 4. Functional Requirements

- Numbered, specific requirements (FR-1, FR-2, etc.)

### 5. Non-Goals

- Explicit scope boundaries

### 6. Design Considerations

- UI/UX requirements
- Component reuse

### 7. Technical Considerations

- Dependencies
- Constraints
- Integration points

### 8. Success Metrics

- Measurable outcomes

### 9. Open Questions

- Remaining clarifications

---

## Example PRDs Generated

After using the skill, you'll have files like:

```
tasks/
├── prd-user-authentication.md
├── prd-email-notifications.md
├── prd-dark-mode-support.md
└── prd-payment-integration.md
```

Each file is a complete, actionable PRD ready for implementation.

---

## Why Haiku Model?

This skill uses **Claude Haiku** (claude-haiku-4-5-20251001) because:

- ✅ **Cost-effective** - PRDs don't need Opus/Sonnet power
- ✅ **Fast generation** - Quick turnaround for planning documents
- ✅ **Excellent at structured output** - Perfect for templated documents
- ✅ **Sufficient for planning** - Maintains quality while saving costs

For a typical PRD:

- **Haiku cost:** ~$0.05 per PRD
- **Sonnet cost:** ~$0.30 per PRD
- **Savings:** 83% cost reduction

---

## Tips for Best Results

### 1. Be Specific in Your Request

```
# Vague
"Create a PRD for notifications"

# Better
"Create a PRD for email and in-app notifications for order status updates"
```

### 2. Answer Clarifying Questions Quickly

Use the letter format: `"1A, 2C, 3B"` for rapid iteration

### 3. Review and Refine

After generation:

```
"Add more detail to the Technical Considerations section"
"Expand user story US-002 with more acceptance criteria"
```

### 4. Keep Issues Updated

When converting from GitHub issues, keep the issue updated as the PRD evolves.

---

## Integration with Other Skills

### Works Great With:

**Compound Engineering:**

- Use ralph-prd-generator to create the PRD
- Use `/compound-engineering:work` to execute it

**Dev Browser:**

- PRDs include "Verify in browser" for UI stories
- Automatically suggests using dev-browser for testing

---

## Troubleshooting

### Issue: Skill Not Found

**Problem:** Claude doesn't recognize the skill

**Solution:** Make sure you're in the project directory:

```bash
cd ~/Work/htdocs/Enskiedutech
ls .claude/skills/ralph-prd-generator/SKILL.md  # Should exist
```

### Issue: Tasks Directory Not Created

**Problem:** Error saving PRD

**Solution:**

```bash
mkdir -p tasks
```

### Issue: Wrong Model Used

**Problem:** Claude uses Sonnet instead of Haiku

**Solution:** Check the SKILL.md has this line:

```yaml
model: claude-haiku-4-5-20251001
```

### Issue: GitHub Issue Not Converting

**Problem:** Can't extract issue content

**Solution:** Either:

- Provide the issue URL directly
- Copy/paste the issue content in your message
- Ensure you have access to the repository

---

## Advanced Usage

### Custom Output Directory

To save PRDs elsewhere, modify the request:

```
"Create a PRD for [feature] and save it to docs/planning/prd-[name].md"
```

### Batch Conversion

Convert multiple issues:

```
"Convert GitHub issues #45, #46, and #47 to PRDs"
```

### PRD Updates

Update existing PRDs:

```
"Update tasks/prd-authentication.md to include OAuth providers"
```

---

## Example Workflow

Here's a complete workflow from issue to implementation:

### Step 1: Convert Issue

```
You: "Convert issue #123 to PRD"
Claude: [Creates tasks/prd-feature-name.md]
```

### Step 2: Review PRD

```
You: "Review the PRD and suggest improvements"
Claude: [Analyzes and suggests enhancements]
```

### Step 3: Refine

```
You: "Add more technical details about database schema"
Claude: [Updates the PRD]
```

### Step 4: Execute (with Compound Engineering)

```
You: "/compound-engineering:work tasks/prd-feature-name.md"
Claude: [Executes the plan systematically]
```

---

## Cost Comparison

### Per PRD (typical ~3000 tokens):

| Model     | Input Cost | Output Cost | Total      |
| --------- | ---------- | ----------- | ---------- |
| **Haiku** | $0.003     | $0.045      | **~$0.05** |
| Sonnet    | $0.015     | $0.225      | ~$0.24     |
| Opus      | $0.075     | $0.375      | ~$0.45     |

**Annual savings** (50 PRDs): ~$20 (Haiku) vs ~$22.50 (Sonnet)

Haiku is perfect for this task!

---

## Summary

**Installation:**

1. Create `.claude/skills/ralph-prd-generator/` in your project
2. Copy SKILL.md to that directory
3. Create `tasks/` directory

**Usage:**

```
# From description
"Create a PRD for [feature]"

# From GitHub issue
"Convert issue #123 to PRD"
```

**Output:**
Structured PRD saved to `tasks/prd-[feature-name].md`

**Benefits:**

- ✅ Fast, cost-effective planning
- ✅ Consistent PRD format
- ✅ Ready for implementation
- ✅ GitHub issue integration

Ready to create your first PRD! 🚀
