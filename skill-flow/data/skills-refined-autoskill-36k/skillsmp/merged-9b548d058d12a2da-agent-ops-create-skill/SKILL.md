---
name: agent-ops-create-skill
description: "Create new AgentOps skills via interactive interview, supporting both from-scratch and clone modes with tiered complexity."
---

# Create Skill Workflow

## Purpose

Guide users through creating new AgentOps skills with consistent structure and quality. This process reduces friction for skill ecosystem growth while enforcing standards.

## Mode Selection

Present mode options at the start:

| Mode | Description | Use When |
|------|-------------|----------|
| **A) From scratch** | Start with a blank template | Creating entirely new capability |
| **B) Clone existing** | Use an existing skill as a base | New skill similar to an existing one |

### Clone Mode Procedure

1. List available skills from `.github/skills/`
2. User selects one to clone
3. Read that skill's SKILL.md as a base
4. Interview focuses on what to change/customize

## Complexity Tiers

After mode selection, assess complexity:

| Tier | Questions | Criteria |
|------|-----------|----------|
| **Simple** | 5 | Single procedure, minimal dependencies, clear scope |
| **Complex** | 10+ | Multiple procedures, decision trees, error handling, many dependencies |

### Complexity Assessment Questions

Ask the user:
1. "Does this skill have a single main procedure, or multiple branching paths?"
2. "Does it need to invoke other skills or handle errors specially?"

**If answers suggest simple** → Simple tier (5 questions)  
**If answers suggest complex** → Complex tier (10+ questions)

---

## Interview Questions

### Simple Tier (5 Questions)

Use `agent-ops-interview` skill for one-question-at-a-time flow.

| # | Question | Field | Validation |
|---|----------|-------|------------|
| 1 | "What should this skill be called? (use kebab-case, e.g., `my-custom-skill`)" | `name` | Kebab-case, unique in `.github/skills/`. **Must NOT start with `agent-ops-`** (reserved for bundled assets). |
| 2 | "Describe in one sentence what this skill does:" | `description` | Non-empty, < 200 chars |
| 3 | "What is the main procedure? Describe the step-by-step workflow:" | Procedure section | Non-empty |
| 4 | "What state files does it read and write? (e.g., focus.md, issues/*)" | `state_files` | Valid file paths or patterns |
| 5 | "Should this skill have an accompanying prompt file for slash command usage? (yes/no)" | `create_prompt` | Boolean - if yes, generate `.github/prompts/{name}.prompt.md` |

**IMPORTANT**: If user provides a name starting with `agent-ops-`, respond with:
> ❌ Cannot create skill with `agent-ops-` prefix. This prefix is reserved for bundled assets managed by `aoc bundle install`. Please choose a different name (e.g., `my-tags` instead of `agent-ops-tags`).

### Category Assignment (After Q2)

After collecting the skill name and description, assess and assign category:

**Step 1: Auto-detect category** based on description keywords:

| Keywords | Suggested Category |
|----------|-------------------|
| git, branch, commit, merge, repo | `git` |
| review, analyze, audit, inspect, map | `analysis` |
| doc, documentation, readme, changelog | `docs` |
| core, workflow, baseline, constitution | `core` |
| state, focus, issue, task, housekeeping | `core` |
| utility, helper, tool, interview | `utility` |
| (none matched) | `extended` |

**Step 2: Assess certainty**

| Certainty | Condition | Action |
|-----------|-----------|--------|
| HIGH | 2+ keyword matches | Auto-assign, display for confirmation |
| LOW | 0-1 keyword matches | Ask user to choose |

**Step 3: Display category assignment**

Always show the category before proceeding:

```markdown
📂 **Category Assignment**

Based on your description, this skill fits the **{category}** category.

Available categories:
- **core**: Essential workflow skills
- **git**: Git operations and branch management  
- **analysis**: Code analysis and review
- **docs**: Documentation management
- **utility**: Supporting utilities and helpers
- **extended**: Specialized/domain-specific skills

Is **{category}** correct? (yes / or type a different category)
```

**If certainty is LOW**, present as a question instead:

```markdown
📂 **Category Selection**

I couldn't confidently determine the category from your description.

Available categories:
- **core**: Essential workflow skills (constitution, baseline, planning...)
- **git**: Git operations (git, branch-workflow, selective-copy...)
- **analysis**: Code analysis (context-map, code-review, project-sections...)
- **docs**: Documentation (docs, mkdocs, versioning...)
- **utility**: Supporting utilities (interview, guide, tools, debugging...)
- **extended**: Specialized skills (api-review, docker-review, research...)

Which category fits best?
```

**Step 4: Record final category** for use in frontmatter generation.

### Complex Tier Additional Questions (6-10+)

| # | Question | Field |
|---|----------|-------|
| 6 | "What other skills does this invoke? (comma-separated)" | `invokes` |
| 7 | "What skills might invoke this one? (comma-separated)" | `invoked_by` |
| 8 | "Are there multiple procedures or modes? If yes, describe each:" | Additional sections |
| 9 | "Are there decision points or branching logic? Describe:" | Decision tree |
| 10 | "How should errors be handled? Any recovery procedures?" | Error handling section |

**Follow-up questions** (as needed based on answers):
- "What are the preconditions before this skill can run?"
- "What completion criteria determine success?"
- "What are common anti-patterns to avoid?"
- "Can you provide an example invocation?"

---

## Skill Template

After interview completion, generate SKILL.md using this template.

**CRITICAL: Do NOT wrap the output in code fences.** The SKILL.md file must be plain markdown starting directly with the `---` frontmatter delimiter. Never use `` ```skill ``, `` ```markdown ``, or any other fence around the generated content.

**Correct output** (raw markdown, no fence):
```
---
name: my-skill
description: "..."
...
```

**Wrong output** (wrapped in fence — NEVER do this):
```
```skill
---
name: my-skill
...
```  ← This fence breaks skill loading
```

### Template Structure

```markdown
---
name: {name}
description: "{description}"
category: extended
invokes: [{invokes}]
invoked_by: [{invoked_by}]
state_files:
  read: [{read_files}]
  write: [{write_files}]
---

# {Title} Workflow

## Purpose

{purpose_description}

## Procedure

{main_procedure}

## Completion Criteria

- [ ] {criterion_1}
- [ ] {criterion_2}

## Anti-patterns (avoid)

- ❌ {antipattern_1}
```

### Template Field Mapping

| Interview Answer | Template Field |
|------------------|----------------|
| Question 1 | `{name}`, directory name |
| Question 2 | `{description}`, `{purpose_description}` |
| Question 3 | `{category}` |
| Question 4 | `{main_procedure}` |
| Question 5 | `{read_files}`, `{write_files}` |
| Question 6 | `{invokes}` |
| Question 7 | `{invoked_by}` |
| Questions 8-10 | Additional sections as appropriate |

---

## Generation Procedure

1. **Validate answers**:
   - Name does NOT start with `agent-ops-` (reserved prefix)
   - Name is unique (check `.github/skills/` doesn't have directory)
   - Category is valid enum
   - Description is non-empty

2. **Create directory**:
   - Path: `.github/skills/{name}/`

3. **Generate SKILL.md**:
   - Populate template with interview answers
   - Add sections based on complexity tier

4. **Generate prompt file** (if requested):
   - Path: `.github/prompts/{name}.prompt.md`
   - Use prompt template (see below)

5. **Confirm with user**:
   - Show generated content
   - Ask "Does this look correct? (yes/edit/cancel)"

6. **Save file(s)**:
   - Write to `.github/skills/{name}/SKILL.md`
   - Write to `.github/prompts/{name}.prompt.md` (if requested)

---

## Prompt Template

When user requests a prompt file, generate using this template:

```markdown
Use the `{name}` skill for {short_description}.

## Quick Usage

{brief_usage_example}

## When to Use

- {use_case_1}
- {use_case_2}

## Options

{any_modes_or_options_from_skill}
```

**Mapping**:
- `{name}` → skill name from interview
- `{short_description}` → description from interview (lowercase, no period)
- `{brief_usage_example}` → derived from main procedure
- `{use_case_1/2}` → inferred from purpose

---

## Registration Procedure

After skill file is created, auto-register in SKILL-TIERS.md:

1. **Read** `.github/SKILL-TIERS.md`

2. **Determine tier** from category: extended Category | Tier |
   |----------|------|
   | core | Tier 1 |
   | utility | Tier 3 |
   | analysis | Tier 5 |
   | git | Tier 4 |
   | recovery | Tier 4 |

3. **Find table** for target tier (pattern: `### Tier {N}:`)

4. **Insert row** at end of table:
   ```markdown
   | `{name}` | {description} | {invoked_by or "User request"} |
   ```

5. **Save file**

6. **Confirm**: "✅ Skill registered in SKILL-TIERS.md under Tier {N}"

---

## Post-Creation Validation

After generation, verify:

- [ ] File exists at `.github/skills/{name}/SKILL.md`
- [ ] Frontmatter is valid YAML
- [ ] Name in frontmatter matches directory name
- [ ] Name does NOT start with `agent-ops-` (reserved prefix)
- [ ] Description is non-empty
- [ ] At least one procedure section exists
- [ ] State files declared (read/write)
- [ ] Registered in SKILL-TIERS.md
- [ ] Prompt file exists at `.github/prompts/{name}.prompt.md` (if requested)

**If validation fails**: Report specific failure, offer to fix or regenerate.

---

## Anti-patterns (avoid)

- ❌ Creating skill with reserved `agent-ops-` prefix
- ❌ Creating skill without interview (skipping validation)
- ❌ Registering skill in wrong tier based on category
- ❌ Creating duplicate skill name
- ❌ Generating SKILL.md without user confirmation
- ❌ Skipping validation checklist after creation