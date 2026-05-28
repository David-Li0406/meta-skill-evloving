---
name: github-issue-conventions
description: GitHub issue structure and naming conventions for the project
---

# GitHub Issue Conventions

This project uses a hierarchical issue tracking system with three levels: Roadmaps, Meta-issues, and Sub-issues.

## Issue Hierarchy

### 1. Roadmap Issues (Top Level)

Track overall component development progress.

**Fixed Roadmap Numbers:**
{{ROADMAP_LIST}}

**Structure:**

```markdown
Master tracking issue for [Component] development.

### Phase 1: [Phase Name]

- [ ] #74
- [ ] #80
- [ ] #81

### Phase 2: [Phase Name]

- [ ] #76
- [ ] #77

### Phase 3: [Phase Name]

- [ ] #78
- [ ] #79
```

**Labels:**

- `type: roadmap`
  {{LABEL_RULES}}

**Issue Reference Format:**

- Use ONLY issue numbers: `- [ ] #74`
- Do NOT include titles: ~~`- [ ] #74 [PREFIX]-AUTH: Authentication System`~~
- GitHub auto-renders titles when you use `#NUMBER`

---

### 2. Meta-Issues (Middle Level)

Group related sub-issues for a system or feature.

**Naming Pattern:**
`[COMPONENT]-[SYSTEM]: [System Name] Tracking`

**Examples:**

- `API-AUTH: Authentication System Tracking`
- `WEB-UI: User Interface Tracking`

**Component Prefixes:**
{{PREFIX_LIST}}

**Structure (< 5 sub-issues):**

```markdown
### Tasks

- [ ] #10
- [ ] #11
- [ ] #12
```

**Structure (5+ sub-issues):**

```markdown
Master tracking issue for [System] development.

### Dependencies

- #XX - Phase N must be complete

### Phase 1: [Phase Name]

- [ ] #10
- [ ] #11

### Phase 2: [Phase Name]

- [ ] #12
- [ ] #13
```

**Labels:**

- `type: feature`
  {{LABEL_RULES}}
- `priority: high` (Phase 1), `priority: medium` (Phase 2+)

**Dependencies Section Rules:**

- Optional - only add if dependencies exist
- Reference other meta-issues
- Specify phase if only specific phase needed
- Format: `- #XX - Phase N must be complete`

**Issue Reference Format:**

- Use ONLY issue numbers: `- [ ] #155`
- Do NOT include titles: ~~`- [ ] #155 [PREFIX]-ACC-001: Implement Password`~~
- GitHub auto-renders titles automatically

---

### 3. Sub-Issues (Lowest Level)

Individual implementation tasks.

**Naming Pattern:**
`[COMPONENT]-[SYSTEM]-[NNN]: [Action] [Target]`

**Examples:**

- `API-AUTH-001: Implement guest registration`
- `WEB-UI-001: Create login screen component`

**Numbering:**

- NNN = 001, 002, 003... (sequential within system)
- Never reuse numbers
- Start at 001 for each new system

**Structure (REQUIRED):**

```markdown
## Description

[1-3 sentences explaining what needs to be implemented]

### Requirements

- [ ] [Specific, testable requirement 1]
- [ ] [Specific, testable requirement 2]
- [ ] [Specific, testable requirement 3]

### Technical Notes

- [Implementation detail or constraint]
- [Dependency on other sub-issue]
- [Reference to existing pattern]
```

**Labels:**

- `type: enhancement`
  {{LABEL_RULES}}
- `priority: [high/medium/low]` (based on phase)

---

## Labels Reference

**Area (Required):**
{{LABEL_RULES}}

**Type (Required):**

- `type: roadmap` - Roadmap tracking issues
- `type: feature` - Meta-issue tracking
- `type: enhancement` - Sub-issue implementation
- `type: bug` - Bug fixes
- `type: chore` - Maintenance tasks
- `type: documentation` - Documentation updates

**Priority (Auto-assigned by phase):**

- `priority: critical` - Blocking issues
- `priority: high` - Phase 1 items
- `priority: medium` - Phase 2 items
- `priority: low` - Phase 3+ items

**Size (Optional):**

- `size: s` - Small (< 4 hours)
- `size: m` - Medium (1-2 days)
- `size: l` - Large (3+ days)

---

## Workflow Rules

### Creating Issues

1. **Sub-issues first** - Create all sub-issues to get their numbers
2. **Meta-issue second** - Reference sub-issue numbers in Tasks checklist (ONLY numbers, no titles)
3. **Update roadmap last** - Add meta-issue number to roadmap (ONLY number, no title)

### Working on Issues

1. **Sequential order** - Work through sub-issues in order listed
2. **Complete ALL requirements** - Implement everything before checking boxes
3. **One sub-issue at a time** - Finish completely before moving to next
4. **Check ALL requirement boxes** - Update sub-issue body to check all Requirements
5. **Ask before closing** - Always ask about refactoring before closing

### Completing Sub-issues (CRITICAL ORDER)

**Follow this exact sequence:**

1. **Implement all requirements** - Complete all work first
2. **Check ALL boxes in sub-issue Requirements section**
   - Use `github_issue_write` to update the sub-issue body
   - Change `- [ ]` to `- [x]` for EVERY requirement
   - This is MANDATORY - never skip this step
3. **Ask about refactoring** - Give user chance to improve code
4. **Close the sub-issue** - Set state to closed
5. **Check box in meta-issue Tasks checklist** - Update meta-issue to mark sub-issue complete

**Common Mistake to Avoid:**

- ❌ Closing sub-issue without checking Requirements boxes first
- ✅ Always check Requirements boxes BEFORE closing

### Multi-component Work

1. **Execution Order** - Always work in this order: {{EXECUTION_FLOW}}
2. **Pass context** - Summarize changes from one component for the next
3. **Sequential completion** - Finish one component fully before next

---

## Issue Reference Format

**CRITICAL RULE: When referencing issues ANYWHERE in GitHub:**

**✅ CORRECT:**

```markdown
### Tasks

- [ ] #155
- [ ] #156

### Dependencies

- #74 - Phase 1 must be complete

### Phase 1: Core

- [ ] #10
- [ ] #11
```

**❌ INCORRECT:**

```markdown
### Tasks

- [ ] #155 [PREFIX]-ACC-001: Implement Change Password
- [ ] #156 [PREFIX]-ACC-002: Implement Admin Delete Account

### Dependencies

- #74 ([PREFIX]-AUTH: Authentication System) - Phase 1 must be complete
```

**Why:**

- GitHub automatically renders issue titles when you reference `#NUMBER`
- Including titles creates duplicate rendering: "Title #123 Title"
- Shorter references are cleaner and easier to maintain

**Applies to:**

- Roadmap checklists
- Meta-issue Tasks checklists
- Meta-issue Dependencies sections
- Any cross-references between issues
- Sub-issue Technical Notes

---

## System Naming Guidelines

Define 3-4 letter uppercase abbreviations for your systems. Document them in your component context skills or project README.

**Examples:**

- `AUTH` - Authentication
- `PAY` - Payments
- `UI` - User Interface
- `API` - API Routes

---

## Phase Naming Conventions

Use descriptive phase names that indicate progression:

**Common Phase Patterns:**

- Phase 1: Core Foundation / Core Systems / Data Structures
- Phase 2: World & Network / Advanced Mechanics / Integration
- Phase 3: Gameplay Systems / Advanced Features / Polish
- Phase 4: Social & Advanced / Optimization / Edge Cases

Choose names that fit the system being built.

---

## Dependency Management

**Meta-issue Dependencies:**

- List other meta-issues that must be complete (or specific phases)
- Update roadmap order if dependencies change
- Example: Crafting depends on Inventory Phase 1
- Format: `- #XX - Phase N must be complete` (ONLY issue number)

**Sub-issue Dependencies:**

- Note in Technical Notes section
- Reference specific sub-issues if needed
- Example: "Requires #10 completion" (ONLY issue number)

---

## Quick Reference

**Issue Naming:**

- Roadmap: `[Tracking] [Component] Development Roadmap`
- Meta: `[PREFIX]-[SYSTEM]: [Name] Tracking`
- Sub: `[PREFIX]-[SYSTEM]-[NNN]: [Action] [Target]`

**When to use Phases in Meta-issues:**

- 2-3 sub-issues → Flat Tasks list
- 5+ sub-issues → Group into Phases

**Label Combos:**

- Roadmap: `type: roadmap` + `area: [component]`
- Meta: `type: feature` + `area: [component]` + `priority: high`
- Sub: `type: enhancement` + `area: [component]` + `priority: [varies]`

**Execution Order:**

- {{EXECUTION_FLOW}} (always)
- Phase 1 → Phase 2 → Phase 3 (in roadmaps)
- Top → Bottom (in task lists)

**Completion Order (Sub-issues):**

1. Implement all requirements
2. Check ALL boxes in sub-issue Requirements
3. Ask about refactoring
4. Close sub-issue
5. Check box in meta-issue Tasks

**Issue References:**

- Always use: `#123`
- Never use: ~~`#123 Title`~~
