---
name: documentation-writing
description: Write documentation using the four-types system (Tutorial, How-to, Reference, Explanation). Each type serves a distinct purpose - don't mix them. Use when creating docs, README files, guides, or any technical writing. Based on the Divio documentation system.
---

# Documentation Writing

Write clear, focused documentation by choosing the right type and sticking to it.

## When to Use

**Use this skill when:**
- Creating new documentation files
- Writing README files
- Adding tutorials or guides
- Documenting APIs or CLIs
- Writing how-to guides
- Explaining design decisions

## The Four Types

There isn't one thing called "documentation" - there are four distinct types:

| Type | Purpose | User State | Naming |
|------|---------|------------|--------|
| **Tutorial** | Teach by doing | New user learning | `getting-started.md`, `hello-world.md` |
| **How-to** | Solve a problem | User with a goal | `howto-*.md` |
| **Reference** | Look up facts | User needs details | `specification.md`, `api.md`, `cli.md` |
| **Explanation** | Deepen understanding | User wants context | `rationale.md`, `philosophy.md` |

**Critical rule:** Pick ONE type per document. Don't mix.

---

## 1. Tutorials

**Purpose:** Teach users by walking them through steps to complete a project.

**Do:**
- Enable learners to *do* things from the start
- Show immediate, visible results for every action
- Progress from simple to complex gradually
- Keep it concrete - lead from particulars to principles
- Provide minimal explanation - link elsewhere for details

**Don't:**
- Make users perform actions without visible results
- Include extended discussions or theory
- Cover alternative methods or advanced options

**Example structure:**
```markdown
# Getting Started with MyTool

## Installation
pip install mytool

## Hello World
1. Create a config file:
   echo "name: example" > config.yaml

2. Run the tool:
   mytool run config.yaml

3. You should see: "Project created successfully"
```

---

## 2. How-to Guides

**Purpose:** Help users solve a specific problem. Goal-oriented recipes.

**Do:**
- Address a specific question: "How do I...?"
- Provide ordered, sequential steps
- Focus on practical outcomes
- Title clearly: "How to create X" not "Creating X"
- Link to explanations rather than embedding them

**Don't:**
- Explain concepts - link to explanation docs instead
- Be overly specific to one exact use case
- Include tangential information

**Example structure:**
```markdown
# How to Validate a Configuration File

Use the `validate` command to check your config for errors.

## Steps

1. Run validation:
   mytool validate config.yaml

2. Fix any reported errors

3. Re-run until validation passes

## Common Errors

**Missing required field:** Add the `name` field to your config.
**Invalid format:** See [configuration reference](./reference/config.md).
```

---

## 3. Technical Reference

**Purpose:** Describe the machinery. Accurate, complete, no opinions.

**Do:**
- Mirror the codebase structure in documentation structure
- Maintain uniform format and tone throughout
- Include basic usage (how to instantiate, invoke)
- Note precautions and potential problems
- Keep examples brief

**Don't:**
- Explain basic concepts or theory
- Provide task-oriented instructions (that's how-to)
- Include opinions or speculation

**Example structure:**
```markdown
# Configuration Reference

## Required Fields

### `name` (string)
Project identifier. Must be alphanumeric with underscores.

### `version` (string)
Semantic version. Format: "MAJOR.MINOR.PATCH"

## Optional Fields

### `description` (string)
Human-readable project description. Default: empty.
```

---

## 4. Explanation

**Purpose:** Clarify and illuminate. Broaden understanding.

**Do:**
- Adopt a discursive, relaxed style
- Provide background, history, and context
- Explain design decisions and constraints
- Explore alternatives and trade-offs
- Write for leisurely reading

**Don't:**
- Teach how to perform specific tasks
- Provide step-by-step guidance
- Include technical reference details

**Example structure:**
```markdown
# Why We Use YAML

## Background

Configuration files need to balance human readability with machine parseability...

## Alternatives Considered

We evaluated JSON, TOML, and INI formats. JSON lacks comments, TOML is less widely known...

## Design Decisions

We chose YAML because our target users are already familiar with it from other tools...
```

---

## Quick Decision Guide

| If the user needs to... | Write a... |
|-------------------------|-----------|
| Learn how to use the tool | Tutorial |
| Accomplish a specific task | How-to Guide |
| Look up a parameter or option | Reference |
| Understand why something works that way | Explanation |

---

## Tutorial vs How-to: The Practical Test

These two types are often confused. Here's how to tell them apart:

**Tutorial:** "Let me teach you about X by building something together"
- Reader is a **newcomer** learning the system
- Walks through a **complete project** from start to finish
- Focus is on **learning**, not accomplishing a specific goal
- Example: "Getting Started with Django" that builds a blog

**How-to:** "You want to accomplish X, here's how"
- Reader **already knows** what they want to do
- Addresses a **specific goal** the reader came with
- Focus is on **accomplishing**, not teaching fundamentals
- Example: "How to add authentication to your Django app"

**The practical test:** Ask yourself:
> "Did the reader arrive with a goal, or are they here to learn?"

If they arrived with a goal → **How-to**
If they're here to learn → **Tutorial**

**Reality check:** Most practical documentation is how-to. True tutorials are rare and valuable - they're for onboarding newcomers. If you're writing about "how to do X with Y", it's probably a how-to, even if you call it a tutorial.

---

## Organizing Documentation Sites

The four types guide **how you write** each document. But **site navigation** is a separate concern - optimize nav for how users find things, not for categorizing doc types.

### Audience-First Organization

When your tool has distinct user personas (e.g., "users" vs "server operators"), organize by audience at the top level:

```yaml
# Audience-first (recommended when personas differ)
- Using the tool:        # For end users
    - Getting started
    - Working with data
    - Exporting results
- Hosting the tool:      # For server operators
    - Database setup
    - Adding API routes
    - Compliance testing
- Reference:             # Shared
    - CLI reference
    - API reference
- Explanation:           # Shared
    - Architecture
    - Design decisions
```

**Why audience-first?**
- Users find "their" section immediately
- All relevant content is grouped together
- Reduces cognitive load ("Am I a user or operator?")

**Key insight:** Reference and Explanation are typically **shared** across audiences - they don't need splitting.

### Types-First Organization

When your tool has a single primary audience, types-first works well:

```yaml
# Types-first (when audience is uniform)
- Tutorials:
    - Getting started
    - Building your first app
- How-to guides:
    - How to validate config
    - How to export data
- Reference:
    - CLI reference
    - Config options
- Explanation:
    - Architecture overview
```

### Choosing an Approach

| Situation | Recommended |
|-----------|-------------|
| Distinct user personas (users vs operators) | Audience-first |
| Single primary audience | Types-first |
| Complex tool with many features | Audience-first with sub-grouping |
| Simple tool or library | Types-first |

---

## Writing Style

### Words to Avoid

| Avoid | Why |
|-------|-----|
| "easy", "simple", "straightforward" | What's easy for you may not be for the reader |
| "obviously", "of course", "clearly" | Makes readers feel stupid |
| "just", "simply" | Minimizes difficulty |

**Instead:** State facts without judgment.

### Link Text

**Bad:** To learn more, click here.

**Good:** See the [configuration reference](link) for details.

### Be Concise

- Get to the point
- Use code examples over prose
- Break up text with headers and lists
- Cut everything unnecessary

### Keep Examples Working

- Test all code examples
- Provide complete, copy-paste-able code
- Update examples when the codebase changes

---

## README Best Practices

READMEs answer "what and why" - full docs answer "how".

**Structure:**
1. Title + subtitle (what is this?)
2. Problem statement (what problem does it solve?)
3. Quick example (show, don't just tell)
4. Installation (few lines max)
5. Basic usage
6. Link to full documentation

**Don't:** Put all documentation in the README. Point to docs instead.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mixing tutorial with reference | Split into separate documents |
| Mixing how-to with explanation | Link to explanation from how-to |
| Embedding reference tables in how-tos | Extract tables to reference docs, link to them |
| Labeling how-tos as "tutorials" | Ask: "Did reader arrive with a goal?" If yes → how-to |
| Organizing nav by doc type when audiences differ | Use audience-first nav, doc types guide writing |
| Putting everything in README | Create proper docs, README points to them |
| Incomplete steps | Test by following your own instructions |
| Stale examples | Update docs with code changes |

---

## Minimum Viable Documentation

> "A small set of fresh and accurate docs is better than a large assembly of documentation in various states of disrepair."

- Prioritize brevity and accuracy over volume
- Delete obsolete content - dead docs mislead and create distrust
- Accept "good enough" - perfect documentation doesn't exist

---

## Checklist

When writing documentation:

- [ ] Identified which of the four types I'm writing
- [ ] Stuck to ONE type throughout
- [ ] Avoided words like "easy", "simply", "obviously"
- [ ] Used descriptive link text
- [ ] Tested all code examples
- [ ] Cut unnecessary content
- [ ] Named file appropriately for its type
