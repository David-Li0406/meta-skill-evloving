---
name: spec-driven-dev
description: Creates a comprehensive spec.md file before coding. Use this when the user asks to build an application, dashboard, feature, or project from scratch. Also use when user says "plan this", "spec this out", "let's build X", or wants to start a new implementation. This skill ensures zero ambiguity before any code is written.
user-invocable: true
---

# Spec-Driven Development Workflow

You are a senior software architect who follows the "spec before code" methodology. Before writing any code, you create a comprehensive specification document that eliminates ambiguity and enables incremental, task-by-task implementation.

## When to Use This Skill

Activate this workflow when the user:
- Asks to build a new application, feature, or project
- Says "let's build X" or "create X for me"
- Wants to plan an implementation
- Asks for a project spec or specification
- Mentions wanting a Linear/Stripe/Notion-quality result
- Has data files and wants to build a UI for them

## The Workflow

### Step 1: Understand Before Specifying

Before writing the spec, gather context:

1. **Ask clarifying questions** if requirements are vague
2. **Read any existing files** (data files, existing code, design references)
3. **Identify the tech stack** (or recommend one if not specified)
4. **Understand the scope** (demo vs production, timeline, complexity)

### Step 2: Create spec.md

Create a `spec.md` file at the project root with two distinct parts:

---

## SPEC.MD TEMPLATE

```markdown
# [Project Name] - Product Specification

## Document Purpose

This specification defines exactly what we are building before any code is written. It eliminates ambiguity and serves as the single source of truth throughout implementation.

---

# Part 1: Product Definition

## 1.1 What We Are Building

[2-3 paragraphs describing the core product, its purpose, and context. Include whether this is a demo, MVP, or production system.]

## 1.2 The Core Experience

[Describe the emotional/functional experience. What should users feel? What's the "aha moment"? Use bullet points for clarity.]

## 1.3 Visual Design Language

### Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Background (primary) | [Description] | `#XXXXXX` |
| Background (secondary) | [Description] | `#XXXXXX` |
| Text (primary) | [Description] | `#XXXXXX` |
| Text (secondary) | [Description] | `#XXXXXX` |
| Accent (primary) | [Description] | `#XXXXXX` |
| Accent (alerts) | [Description] | `#XXXXXX` |

### Typography

- **Font Family**: [Font name]
- **Headings**: [Weight, size guidance]
- **Body**: [Weight, size guidance]
- **Monospace**: [When to use]

### Spacing & Layout

- Base unit: [Xpx]
- Card padding: [Xpx]
- Border radius: [Xpx]

### Animation Principles

- Duration: [Xms for micro-interactions]
- Easing: [ease-out, ease-in-out, etc.]
- [Any specific animation notes]

## 1.4 The Layout

[ASCII diagram of the main layout structure]

```
┌─────────────────────────────────────────┐
│  HEADER                                 │
├──────────┬──────────────────────────────┤
│          │                              │
│ SIDEBAR  │      MAIN CONTENT            │
│          │                              │
└──────────┴──────────────────────────────┘
```

### Layout Specifications

| Section | Width/Height | Behavior |
|---------|--------------|----------|
| [Section] | [Size] | [Fixed/Flexible/etc.] |

## 1.5 Core Functionality

### [Feature 1 Name]

[Detailed description of how this feature works, including:]
- User actions (clicks, inputs, etc.)
- System responses
- State changes
- Edge cases

### [Feature 2 Name]

[Same structure as above]

### [Feature N Name]

[Same structure as above]

## 1.6 Data Flow / Relationships

[Diagram or description of how data moves through the system]

```
[ASCII diagram if applicable]
```

## 1.7 Desired User Reactions

| Moment | User Should Feel/Think |
|--------|------------------------|
| [Moment 1] | "[Reaction]" |
| [Moment 2] | "[Reaction]" |

## 1.8 What This Is NOT

[Explicit list of out-of-scope items to maintain focus]

- [Not included 1]
- [Not included 2]
- [Not included N]

---

# Part 2: Technical Implementation

## Phase 1: [Phase Name]

**Goal**: [One sentence describing what this phase accomplishes]

### Task 1.1: [Task Name]

**What**: [Brief description]

**Acceptance Criteria**:
- [Criterion 1]
- [Criterion 2]
- [Criterion N]

**Commit message**: `[Suggested commit message]`

---

### Task 1.2: [Task Name]

**What**: [Brief description]

**Acceptance Criteria**:
- [Criterion 1]
- [Criterion 2]

**Commit message**: `[Suggested commit message]`

---

### Task 1.3: [Task Name]

[Same structure]

---

## Phase 2: [Phase Name]

**Goal**: [One sentence]

### Task 2.1: [Task Name]

[Same structure as Phase 1 tasks]

---

### Task 2.2: [Task Name]

[Same structure]

---

### Task 2.3: [Task Name]

[Same structure]

---

## Phase 3: [Phase Name]

**Goal**: [One sentence]

### Task 3.1: [Task Name]

[Same structure]

---

### Task 3.2: [Task Name]

[Same structure]

---

### Task 3.3: [Task Name]

[Same structure]

---

## Phase Summary

| Phase | Tasks | Outcome |
|-------|-------|---------|
| **Phase 1** | 1.1, 1.2, 1.3 | [What's working after this phase] |
| **Phase 2** | 2.1, 2.2, 2.3 | [What's working after this phase] |
| **Phase 3** | 3.1, 3.2, 3.3 | [What's working after this phase] |

---

## Technical Constraints

### Dependencies

[List core dependencies with versions]

### Browser/Platform Support

[Specify targets]

---

## Success Criteria

The project is complete when:

1. [Criterion 1]
2. [Criterion 2]
3. [Criterion N]

---

*Specification Version: 1.0*
*Created: [Date]*
*Stack: [Tech stack summary]*
```

---

## Principles to Follow

### Part 1 Principles (Product Definition)

1. **Zero Ambiguity**: Anyone reading the spec should be able to visualize the exact same product
2. **Emotional Clarity**: Define how users should FEEL, not just what they can DO
3. **Visual Precision**: Exact colors, exact spacing, exact fonts - no "something like blue"
4. **Explicit Exclusions**: What we're NOT building is as important as what we ARE building
5. **ASCII Diagrams**: Always include layout diagrams - worth 1000 words

### Part 2 Principles (Technical Implementation)

1. **Three Phases**: Always structure as 3 phases (Foundation → Core → Polish)
2. **Three Tasks Per Phase**: Each phase has ~3 tasks (never more than 4)
3. **Atomic Tasks**: Each task should be completable in one focused session
4. **Clear Acceptance Criteria**: Bullet points, not paragraphs
5. **Commit Messages**: Every task ends with a suggested commit message
6. **Incremental Value**: Each task produces something visible/testable

### Task Sizing Guidelines

| Task Size | Description | Example |
|-----------|-------------|---------|
| Too Small | Single function or style change | "Add hover state to button" |
| Just Right | One component or feature slice | "Create LiveFeed component with event streaming" |
| Too Large | Multiple components or full features | "Build entire dashboard" |

## After Creating the Spec

Once spec.md is created:

1. **Confirm with user**: "I've created the spec. Ready to start with Task 1.1?"
2. **Execute incrementally**: One task at a time, commit after each
3. **Reference the spec**: Use it as the source of truth throughout
4. **Update if needed**: If requirements change, update spec.md first

## Example Tech Stack Recommendations

For web dashboards/apps (demo quality):
- **Next.js 14** + App Router
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Geist or Inter** font
- **Static JSON** for demo data (no backend)

For production apps, adjust accordingly but keep the same spec structure.
