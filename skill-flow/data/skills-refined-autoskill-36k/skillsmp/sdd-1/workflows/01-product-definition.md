# Phase 1: Product Definition Workflow

## Purpose

Create `memory/product.md` - a user-centric product definition that captures WHO the users are, WHAT problems they have, and WHY the product exists. NO technical details.

**Command**: `/define-product`
**Output**: `memory/product.md`
**Next**: Manual progression to Phase 2 (`/generate-constitution`)

---

## Prerequisites

- Repository with existing code or documentation
- User available for clarification questions

---

## Step 1: Intelligence Gathering

**Execute BEFORE asking questions:**

```bash
# 1. Scan for existing documentation
project-intel.mjs --search "README" --json
project-intel.mjs --search "product" --json
project-intel.mjs --search "user" --type md --json

# 2. Check for existing memory files
ls memory/*.md 2>/dev/null || echo "No memory files"

# 3. Look for user research artifacts
project-intel.mjs --search "persona" --json
project-intel.mjs --search "journey" --json
```

**Review existing artifacts for:**
- Product vision statements
- User descriptions
- Problem statements
- Feature lists (extract user needs)

---

## Step 2: User Clarification (Max 5 Questions)

**Select 3-5 questions based on gaps found:**

| Category | Question | Purpose |
|----------|----------|---------|
| **Users** | "Who is the primary user of this product?" | Identify target persona |
| **Problem** | "What problem does this solve for them?" | Core value proposition |
| **Context** | "When/where do they experience this problem?" | Usage context |
| **Alternative** | "How do they solve this today?" | Competition/baseline |
| **Success** | "How will you know users are happy?" | Success metrics |
| **Scope** | "What's explicitly NOT in scope for MVP?" | Boundaries |

**Use AskUserQuestion tool:**
```
AskUserQuestion({
  questions: [
    {
      question: "Who is the primary user of this product?",
      header: "Target User",
      options: [
        { label: "Individual consumer", description: "B2C end user" },
        { label: "Business user", description: "B2B professional" },
        { label: "Developer", description: "Technical user" },
        { label: "Other", description: "Specify your user type" }
      ],
      multiSelect: false
    }
  ]
})
```

---

## Step 3: Create Personas

**For each user type identified:**

```markdown
## Persona: [Name]

**Role**: [Job title or role]
**Context**: [When/where they use the product]

### Goals
1. [Primary goal - what they want to achieve]
2. [Secondary goal]

### Frustrations
1. [Current pain point]
2. [What's blocking them today]

### Success Criteria
- [How they measure success]
```

**Limit**: 2-3 personas maximum for MVP

---

## Step 4: Jobs To Be Done (JTBD)

**Extract core jobs from user research:**

```markdown
## Jobs To Be Done

### Core Job
"When I [situation], I want to [motivation], so I can [outcome]."

### Related Jobs
1. "When I [situation], I want to [motivation], so I can [outcome]."
2. "When I [situation], I want to [motivation], so I can [outcome]."
```

**Example:**
- Core: "When I'm feeling lonely, I want to have a meaningful conversation, so I can feel connected."
- Related: "When I'm stressed, I want someone to listen, so I can process my emotions."

---

## Step 5: Generate product.md

**Use template:**

```markdown
# Product Definition: [Product Name]

**Created**: [timestamp]
**Version**: 1.0

---

## Vision

[One sentence describing what this product does and why it matters]

---

## Target Users

### Primary: [Persona Name]
[Summary from Step 3]

### Secondary: [Persona Name] (if applicable)
[Summary from Step 3]

---

## Core Problem

[Clear statement of the problem being solved]

**Current Solutions**: [How users solve this today]
**Why They Fail**: [Gaps in current solutions]

---

## Jobs To Be Done

### Primary Job
"When I [situation], I want to [motivation], so I can [outcome]."

### Supporting Jobs
1. [Job 2]
2. [Job 3]

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| [Metric 1] | [Target] | [How measured] |
| [Metric 2] | [Target] | [How measured] |

---

## Scope Boundaries

### In Scope (MVP)
- [Feature/capability 1]
- [Feature/capability 2]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

---

## Open Questions

- [ ] [Question requiring future clarification]
- [ ] [Question requiring user research]
```

---

## Quality Gates

| Gate | Requirement | Check |
|------|-------------|-------|
| User Focus | NO technical details in product.md | Grep for "API", "database", "code" |
| Clarity | Personas are specific, not generic | Names + concrete contexts |
| JTBD | At least 1 core job defined | Job statement present |
| Boundaries | In-scope AND out-of-scope defined | Both sections populated |
| Evidence | Based on intel gathering, not assumptions | References to existing docs |

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Including technical details | Pollutes product thinking | Review before saving |
| Generic personas | Can't drive decisions | Add specific names/contexts |
| Too many personas | Diffuse focus | Limit to 2-3 |
| Missing out-of-scope | Scope creep | Explicitly list exclusions |
| No success metrics | Can't measure progress | Define before finishing |

---

## Handoff to Phase 2

**After product.md is complete:**

```markdown
## Phase 1 → Phase 2 Handoff

✅ memory/product.md created
✅ Personas defined: [count]
✅ Core JTBD identified
✅ Scope boundaries set

**Ready for**: /generate-constitution
```

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
