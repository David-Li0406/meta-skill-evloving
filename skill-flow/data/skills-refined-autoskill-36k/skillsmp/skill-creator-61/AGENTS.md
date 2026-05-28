# Skill Creator Guidelines

**Version 1.0.0**  
aytordev's  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when creating,  
> maintaining, or refactoring AI agent skills. Humans may also find  
> it useful, but guidance here is optimized for automation and  
> consistency by AI-assisted workflows.

---

## Abstract

A comprehensive guide for creating effective AI agent skills. This skill provides rules and best practices for defining skill metadata, structuring documentation, and bundling resources efficiently.

---

## Table of Contents

1. [Core Principles](#1-core-principles) — **CRITICAL**
   - 1.1 [Concise is Key](#11-concise-is-key)
   - 1.2 [Progressive Disclosure](#12-progressive-disclosure)
   - 1.3 [Set Appropriate Degrees of Freedom](#13-set-appropriate-degrees-of-freedom)
2. [Anatomy of a Skill](#2-anatomy-of-a-skill) — **HIGH**
   - 2.1 [Exclude Auxiliary Files](#21-exclude-auxiliary-files)
   - 2.2 [SKILL.md Essentials](#22-skillmd-essentials)
   - 2.3 [Standard Directory Structure](#23-standard-directory-structure)
3. [Skill Content](#3-skill-content) — **HIGH**
   - 3.1 [Use Assets for Output](#31-use-assets-for-output)
   - 3.2 [Use References for Knowledge](#32-use-references-for-knowledge)
   - 3.3 [Use Scripts for Determinism](#33-use-scripts-for-determinism)
4. [Creation Process](#4-creation-process) — **MEDIUM**
   - 4.1 [Follow the Creation Process](#41-follow-the-creation-process)

---

## 1. Core Principles

**Impact: CRITICAL**

Fundamental rules for designing skills that are token-efficient and effective for AI agents.

### 1.1 Concise is Key

**Impact: CRITICAL (Context window is a scarce public good)**

Skills share the context window with the system prompt, conversation history, and user requests. Assume Claude is smart. Only add context Claude doesn't have. Challenge every paragraph: "Does this justify its token cost?"

**Incorrect: verbose explanation**

```markdown
# Instructions

It is very important to understand that when you are writing code, you should make sure that the code is clean and readable. This is because clean code is easier to maintain and debug. If you write messy code, it will be hard for others to understand simple concepts. Therefore, always strive to write code that is simple and direct.
```

**Correct: concise directive**

```markdown
# Instructions

Write clean, readable code. Prioritize maintainability and clarity.
```

### 1.2 Progressive Disclosure

**Impact: HIGH (Optimizes token usage)**

Use a three-level loading system to manage context:

1. Metadata (always loaded)

2. SKILL.md body (loaded on trigger)

3. References/Scripts (loaded only when needed)

**Incorrect: flat structure**

```markdown
<!-- SKILL.md (10,000 lines) -->

# Huge Manual

[...entire content of API docs included directly in SKILL.md...]
```

**Correct: progressive structure**

```markdown
<!-- SKILL.md (Concise) -->

# API Guide

For detailed endpoint definitions, see [references/api_docs.md](references/api_docs.md).
```

### 1.3 Set Appropriate Degrees of Freedom

**Impact: HIGH (Prevents hallucinations and errors in critical tasks)**

Match the specificity of your instructions to the fragility of the task. High freedom for creative choices, low freedom for fragile operations.

**Incorrect: mismatched freedom**

```markdown
<!-- High freedom for a fragile task -->

To deploy the database, just check the cloud console and try to find the right button. Maybe look for "Deploy" or "Start".
```

**Correct: matched freedom**

```markdown
<!-- Low freedom for a fragile task -->

To deploy the database, run the specific script: `scripts/deploy_db.sh --env=prod`. Do not attempt manual deployment.
```

---

## 2. Anatomy of a Skill

**Impact: HIGH**

precise requirements for file structure, resource organization, and content placement.

### 2.1 Exclude Auxiliary Files

**Impact: MEDIUM (Reduces clutter)**

Do not include README.md, CHANGELOG.md, or generic documentation. Only include files the agent needs to do the job.

**Incorrect: cluttered**

```text
skill/
├── README.md
├── CHANGELOG.md
├── INSTALL.md
└── SKILL.md
```

**Correct: focused**

```text
skill/
└── SKILL.md
```

### 2.2 SKILL.md Essentials

**Impact: CRITICAL (Primary interface for the agent)**

SKILL.md is the entry point. It requires YAML frontmatter (name/description) and a Markdown body.

**Incorrect: missing frontmatter**

```markdown
# My Skill

Here is how to use this skill...
```

**Correct: valid frontmatter**

```markdown
---
name: my-skill
description: Use this skill when...
---

# My Skill

Here is how to use this skill...
```

### 2.3 Standard Directory Structure

**Impact: CRITICAL (Ensures tools can parse the skill)**

Every skill must follow the standard directory structure with `SKILL.md` at the root and optional resources in specific folders.

**Incorrect: messy structure**

```text
my-skill/
├── README.txt
├── code.py
├── doc.pdf
└── skill_info.md
```

**Correct: standard structure**

```text
my-skill/
├── SKILL.md (required)
├── scripts/ (optional, executable code)
├── references/ (optional, documentation)
└── assets/ (optional, output files)
```

---

## 3. Skill Content

**Impact: HIGH**

Guidelines for writing SKILL.md, creating scripts, and organizing references.

### 3.1 Use Assets for Output

**Impact: MEDIUM (Provides resources for generation)**

Use `assets/` for files that should be part of the agent's output (templates, images, fonts).

**Incorrect: generating from scratch**

```markdown
Generate a logo pixel by pixel...
```

**Correct: using asset**

```markdown
Use the brand logo from `assets/logo.png`.
```

### 3.2 Use References for Knowledge

**Impact: HIGH (Keeps SKILL.md lean)**

Use `references/` for documentation, schemas, and policies. Do not duplicate this info in SKILL.md.

**Incorrect: bloated SKILL.md**

```markdown
# Database Schema

[...500 lines of schema definition...]
```

**Correct: referenced schema**

```markdown
# Database Schema

For table definitions, see [references/schema.md](references/schema.md).
```

### 3.3 Use Scripts for Determinism

**Impact: HIGH (Reliability and token efficiency)**

Use `scripts/` for tasks that require deterministic reliability or complex logic that is prone to hallucination if written as text instructions.

**Incorrect: complex logic in text**

```markdown
To rotate the PDF, first read the bytes, then look for the rotation matrix... [complex math instructions]
```

**Correct: delegated to script**

```markdown
To rotate the PDF, run: `scripts/rotate_pdf.py input.pdf output.pdf`
```

---

## 4. Creation Process

**Impact: MEDIUM**

Step-by-step workflow for understanding, planning, initializing, and refining skills.

### 4.1 Follow the Creation Process

**Impact: HIGH (Ensures quality and consistency)**

Follow the 6-step process to ensure high-quality skills:

1. **Understand**: Use concrete examples.

2. **Plan**: Identify reusable contents (scripts/references).

3. **Initialize**: Use `init_skill.py`.

4. **Edit**: Implement resources and SKILL.md.

5. **Package**: Use `package_skill.py`.

6. **Iterate**: Test and refine.

---

