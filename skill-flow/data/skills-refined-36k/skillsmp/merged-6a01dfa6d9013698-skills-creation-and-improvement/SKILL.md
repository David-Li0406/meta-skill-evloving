---
name: skills-creation-and-improvement
description: Use this skill when you need to create or improve Claude Agent Skills, following best practices for structuring SKILL.md files and guiding through iterative development.
---

# Skills Creation and Improvement

This skill serves as a guide for creating and improving Claude Agent Skills effectively.

## Goals
- Clarify the **purpose, triggers, and outputs** of the skill based on user input.
- Generate a correct `SKILL.md` (YAML frontmatter + Markdown body).
- Use progressive disclosure to include auxiliary files (reference/examples/templates) as needed.
- Output in a format ready for placement in `.claude/skills/` or `~/.claude/skills/`.

## Non-goals
- Development of implementation code itself (provide templates or pseudocode if necessary).
- Guessing company-specific confidential information (based solely on user input).

---

## How it works

### Step 0: Classify Input (Most Important)
Determine which category the user input is closest to:

1. **Document Generation** (PRD, mockups, specifications, meeting notes, etc.)
2. **Review** (PR reviews, document reviews, design reviews, etc.)
3. **Transformation/Formatting** (Markdown formatting, template application, summarization, etc.)
4. **Research** (compiling information, creating comparison tables, etc.)
5. **Operational Procedures** (deployment steps, operational runbooks, etc.)

This classification helps in deciding the skill's **outputs**, **inputs**, and **quality criteria**.

---

### Step 1: Fill in Missing Information (Minimize Questions)
If user input is sufficient, do not ask questions. If there are gaps, **assume and proceed**.

Commonly missing items (assume if absent and note in the body):
- Skill **outputs** (What will it produce?)
- Target users (Who will use it?)
- Input format (bullet points/URLs/pasted text/requirements/logs/screenshots, etc.)
- Output format (Markdown/Mermaid/JSON/CSV/diagrams/file structure)
- Constraints (e.g., "4 backticks", "source required", "minimal differences", etc.)
- Examples (phrases to trigger the skill).

---

### Step 2: Decide on Skill Name (Slug)
The `name` should be **lowercase/numbers/hyphens only, max 64 characters**.

Rules:
- Start with a short English slug: e.g., `screenflow-writer`, `prd-writer`.
- If it may conflict with existing skills, use a suffix: `-v2`, `-lite`, `-ja`.

---

### Step 3: Write a Strong Description
The description is crucial for discovery/activation. It should include:
- What the skill does (1 sentence).
- When to use it (trigger words + specific examples).
- What it outputs (results).

---

### Step 4: Generate SKILL.md Body (Concise and Clear)
The SKILL.md body must include:

- **Goals / Non-goals**
- **Inputs (expected input format)**
- **Outputs (format of the results)**
- **Instructions (step-by-step for reproducibility)**
- **Quality Checklist (self-review items)**
- **Examples (at least 3 triggering examples)**
- **References (if necessary)**

If details become lengthy, move them to `reference.md`, keeping SKILL.md as the entry point.

---

### Step 5: Use Progressive Disclosure
If the content exceeds 500 lines, separate it as follows:
- `reference.md`: criteria, detailed procedures, template explanations, glossary.
- `examples.md`: numerous examples, anti-patterns, good output examples.
- `templates/`: copy-paste templates.

Link from SKILL.md to these files (avoid deep link chains).

---

## Output Format
The output should be a **new skill folder structure** returned to the user, with each file in code blocks:

1) Directory tree
2) `SKILL.md`
3) If necessary, `reference.md` / `examples.md` / `templates/*`

---

## Quality Checklist (Self-Review After Generation)
- [ ] `name` is lowercase/numbers/hyphens only, within 64 characters.
- [ ] `description` includes trigger words and is clear on activation conditions.
- [ ] Inputs/outputs/instructions are written at a "reproducible granularity."
- [ ] Expected output format is clearly stated (Mermaid/Markdown, etc.).
- [ ] At least 3 examples are provided (mix of triggering and non-triggering).
- [ ] Long explanations are moved to reference (SKILL.md is the entry point).

---

## Examples

### Example 1 (Generation Request)
User: "Create a skill to generate PRDs in Claude Code."

→ A PRD generation skill folder is created (`prd-writer/`).

### Example 2 (Generation Request)
User: "Create a skill to make screen flow diagrams in Mermaid."

→ A screen flow generation skill folder is created (`screenflow-writer/`).

### Example 3 (Generation Request)
User: "I want to create a skill to minimally edit this text while preserving the original."

→ A minimal difference editing skill folder is created (`minimal-diff-editor/`).

### Example 4 (Non-target)
User: "Please review this text."

→ This is not a "skill generation" request but a "review execution" request. This skill does not activate; standard procedures apply.

---

## References
For detailed best practices: [BEST_PRACTICES.md](BEST_PRACTICES.md)
Template collection: [TEMPLATES.md](TEMPLATES.md)
Example samples: [EXAMPLES.md](EXAMPLES.md)