---
name: skill-writer
description: Create and refine Agent Skills following the agentskills.io specification. Use when user asks to write a skill, create a skill, or build automation workflows for AI agents.
---

# Skill Writer

Create well-structured Agent Skills following the [agentskills.io specification](https://agentskills.io/specification). Skills are reusable instruction sets that extend AI agent capabilities with specialized knowledge and workflows.

## Trigger

When user asks to:

- Create a new skill
- Write a skill for a specific workflow
- Build an agent automation
- Document a repeatable process as a skill
- Refine or improve an existing skill

## Core Principles

### 1. Concise is Key

The context window is a shared resource. Every token competes with conversation history.

**Default assumption**: Claude is already very smart. Only add context Claude doesn't already have.

Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

### 2. Set Appropriate Degrees of Freedom

Match specificity to the task's fragility:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple approaches valid | Code review guidelines |
| **Medium** (pseudocode/templates) | Preferred pattern exists | Report generation |
| **Low** (specific scripts) | Fragile operations, consistency critical | Database migrations |

### 3. Progressive Disclosure

Structure skills so agents load only what they need:

1. **Metadata** (~100 tokens): Name and description loaded at startup
2. **Instructions** (<5000 tokens): Full SKILL.md loaded when activated
3. **Resources** (as needed): Reference files loaded only when required

---

## Process

### Step 1: Check for Existing Skills

**CRITICAL: Before creating any skill, check if one already exists.**

```bash
# List all existing skills
ls skills/*/

# Search for similar skills by keyword
grep -ri "<keyword>" skills/*/SKILL.md --include="*.md" -l

# Check the skills README for the full catalog
cat skills/README.md
```

**Review existing skills for:**
- Same or similar purpose (avoid duplicates)
- Overlapping functionality (consider merging)
- Related skills that could be extended instead

**If a similar skill exists:**
1. Consider extending/improving the existing skill
2. If truly distinct, ensure clear differentiation in description
3. Document relationship in "Related Skills" section

### Step 2: Understand the Skill's Purpose

Ask clarifying questions:

- What task or workflow does this skill automate?
- Who is the target user/audience?
- What tools or MCP servers are required?
- Are there existing scripts or templates to bundle?
- What's the expected output or outcome?

### Step 3: Choose the Category

Skills are organized into category folders. Choose the appropriate category:

| Category | Purpose | Examples |
|----------|---------|----------|
| `research-strategy/` | Research, planning, architecture | deep-research, technical-architect |
| `github-workflow/` | Git, GitHub, PRs, issues | pr-review, github-issue-creator |
| `frontend-development/` | Vue, TypeScript, UI code | vue-component, api-integration |
| `testing/` | Unit tests, E2E, debugging | playwright-test, unit-testing |
| `documentation/` | Writing docs, skills | docs-writing, skill-writer |
| `design/` | UI/UX design, design tools | frontend-design, designer |
| `infrastructure/` | DevOps, databases, tools | mongodb-development, viya-dev-environment |
| `codebase-structures/` | Project structure documentation | viya-app-structure |

**When to create a new category:**
- 3+ skills would fit the new category
- Existing categories are clearly wrong fit
- Get team consensus first

### Step 4: Choose the Skill Name

Requirements:
- Max 64 characters
- Lowercase letters, numbers, and hyphens only
- Must not start or end with hyphen
- No consecutive hyphens (`--`)
- Directory name must match skill name

**Naming conventions** (prefer gerund form):
- `processing-pdfs` (gerund - preferred)
- `pdf-processing` (noun phrase - acceptable)

**Avoid**: `helper`, `utils`, `tools` (too vague)

### Step 5: Write the Description

The description is critical for skill discovery. Claude uses it to select the right skill from potentially 100+ available skills.

Requirements:
- Max 1024 characters
- Non-empty
- **Always write in third person** (not "I can help" or "You can use")
- Include both what the skill does AND when to use it
- Include specific keywords/triggers

**Good example**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad example**:
```yaml
description: Helps with documents.
```

### Step 6: Structure the SKILL.md

Use this template:

```markdown
---
name: <skill-name>
description: <what it does and when to use it>
---

# <Skill Title>

<1-2 sentence overview>

## Trigger

When user asks to:
- <trigger 1>
- <trigger 2>

## Process

### Step 1: <First Step>
<Instructions>

### Step 2: <Second Step>
<Instructions>

## Output to User

<What to provide when complete>

## Error Handling

<How to handle failures>

## Related Skills

| Skill | When to Use Instead |
|-------|---------------------|
| **skill-name** | <when that skill is more appropriate> |
```

### Step 7: Apply Size Guidelines

**Keep SKILL.md under 500 lines.** For larger skills:

1. Move detailed patterns/examples to `reference/` folder
2. Keep core workflow in main SKILL.md
3. Reference files are loaded on-demand

```
my-skill/
├── SKILL.md              # Main instructions (<500 lines)
└── reference/
    ├── patterns.md       # Detailed patterns/examples
    └── troubleshooting.md # Common issues
```

**In SKILL.md, add a note:**
```markdown
> **Detailed patterns**: See [reference/patterns.md](reference/patterns.md) for extended examples.
```

### Step 8: Create the Skill Files

**Location**: Create in the appropriate category folder:

```bash
# Create skill directory
mkdir -p skills/<category>/<skill-name>

# Create the SKILL.md
# Write content to skills/<category>/<skill-name>/SKILL.md
```

### Step 9: Create the Symlink

**CRITICAL: OpenCode requires a flat symlink structure to load skills.**

After creating the skill, add a symlink in `.opencode/skills/`:

```bash
# Navigate to .opencode/skills/
cd .opencode/skills/

# Create symlink (relative path to skill directory)
ln -s ../../skills/<category>/<skill-name> <skill-name>

# Verify symlink
ls -la <skill-name>
```

**Example:**
```bash
cd .opencode/skills/
ln -s ../../skills/documentation/my-new-skill my-new-skill
```

**Why symlinks?**
- Skills are organized in category folders: `skills/research-strategy/technical-architect/`
- OpenCode expects flat structure: `.opencode/skills/technical-architect/`
- Symlinks bridge this gap while preserving organization

### Step 10: Test the Skill

**MANDATORY: Always test the skill before considering it complete.**

#### Test 1: Verify Symlink Works

```bash
# Check symlink resolves correctly
ls -la .opencode/skills/<skill-name>
cat .opencode/skills/<skill-name>/SKILL.md | head -20
```

#### Test 2: Load the Skill

Use the skill tool to verify it loads:

```
Load the <skill-name> skill
```

Expected output: Full SKILL.md content displayed with "Base directory" header.

**If skill doesn't load:**
1. Check symlink exists: `ls -la .opencode/skills/<skill-name>`
2. Check symlink target: `readlink .opencode/skills/<skill-name>`
3. Check SKILL.md exists: `ls skills/<category>/<skill-name>/SKILL.md`

#### Test 3: Verify Skill Execution

Test the skill with a realistic scenario:
1. Start a new conversation or clear context
2. Ask a question that should trigger the skill
3. Verify the skill provides appropriate guidance
4. Check that any referenced files/commands work

#### Test 4: Run Link Checker

If the skill contains internal links:

```bash
./tools/check-links.sh
```

### Step 11: Update Documentation

After creating a skill:

1. **Update skills/README.md** - Add to Quick Reference table and category section
2. **Update skills/USAGE.md** - Add empty tracking table for the new skill

---

## Quality Checklist

Before finalizing any skill:

**Core Quality:**
- [ ] Checked for existing similar skills (no duplicates)
- [ ] Placed in correct category folder
- [ ] Description is specific with keywords
- [ ] Description includes what + when to use
- [ ] SKILL.md body <500 lines
- [ ] Consistent terminology
- [ ] Concrete examples (not abstract)
- [ ] Related Skills section added

**File Structure:**
- [ ] Created in `skills/<category>/<skill-name>/SKILL.md`
- [ ] Large content extracted to `reference/` folder
- [ ] Symlink created in `.opencode/skills/`

**Testing:**
- [ ] Symlink resolves correctly
- [ ] Skill loads via skill tool
- [ ] Skill provides useful guidance for test scenario
- [ ] Link checker passes (if applicable)

**Documentation:**
- [ ] Added to skills/README.md Quick Reference
- [ ] Added to skills/README.md category section
- [ ] Added tracking table in skills/USAGE.md

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Duplicate skill | Confusion, maintenance burden | Search existing skills first |
| Wrong category | Hard to find | Match to existing categories |
| Missing symlink | Skill won't load | Always create .opencode/skills/ symlink |
| No testing | Broken skill | Test load + execution |
| Too verbose | Wastes context tokens | Assume Claude knows basics |
| Vague description | Poor skill discovery | Include specific keywords |
| >500 lines | Slow loading, context bloat | Extract to reference/ folder |

---

## Skill Templates by Type

### Workflow Automation Skill

```markdown
---
name: <workflow-name>
description: <Automate X process>. Use when user asks to <trigger>.
---

# <Workflow Name>

## Trigger

When user asks to <action>.

## Prerequisites

- Tool/MCP: <required>
- Access: <required permissions>

## Process

### Step 1: Gather Input
<...>

### Step 2: Execute Workflow
<...>

### Step 3: Verify Results
<...>

## Output to User

<summary of what was done>

## Related Skills

| Skill | When to Use Instead |
|-------|---------------------|
```

### Tool Integration Skill

```markdown
---
name: <tool-name>-integration
description: <Integrate with X tool>. Use when user works with <tool>.
---

# <Tool> Integration

## Trigger

When user asks to use <tool> or <related tasks>.

## Setup

<One-time setup instructions>

## Available Operations

| Operation | Command/Tool | Description |
|-----------|--------------|-------------|
| <op1> | `<command>` | <desc> |

## Troubleshooting

<Common issues and fixes>

## Related Skills

| Skill | When to Use Instead |
|-------|---------------------|
```

---

## Reference: Specification Summary

From [agentskills.io/specification](https://agentskills.io/specification):

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars, lowercase alphanumeric + hyphens |
| `description` | Yes | Max 1024 chars, non-empty |
| `license` | No | License name or file reference |
| `compatibility` | No | Max 500 chars, environment requirements |
| `metadata` | No | Key-value pairs for custom data |

**Directory structure:**
```
skills/
├── <category>/
│   └── <skill-name>/
│       ├── SKILL.md          # Main instructions
│       └── reference/        # Optional detailed docs
└── README.md                 # Catalog of all skills

.opencode/skills/
└── <skill-name> -> ../../skills/<category>/<skill-name>  # Symlinks
```
