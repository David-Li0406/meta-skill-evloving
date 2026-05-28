---
id: ai-assisted-specification-writing
name: "AI-Assisted Specification Writing"
domain: SDD
skill: faion-sdd
category: "best-practices-2026"
---

# AI-Assisted Specification Writing

### Problem

Traditional specification writing is slow, inconsistent, and often neglected. Developers struggle to articulate requirements clearly, leading to:
- Ambiguous requirements causing implementation delays
- Inconsistent spec formats across teams
- Specifications that become outdated immediately
- Bottleneck shifted from implementation to specification

**Key insight from 2025:** "AI can handle much of the implementation, and suddenly the bottleneck has shifted upstream" - specification skills have atrophied.

### Framework

#### The SDD-AI Workflow (2025)

```
INTENT -> SPEC -> PLAN -> EXECUTION -> REVIEW
   |        |       |         |          |
 human    AI+human  AI      AI agent   human
 input   collab   generate  execute    verify
```

#### Core Principles

1. **Specification First** - Expected behaviors, edge cases, and constraints captured upfront
2. **One Source of Truth** - Spec anchors entire project (tests, docs, design trace back)
3. **Built-in Testability** - Spec defines "what done looks like"
4. **Iterative by Design** - Specs evolve with feedback, maintaining traceability

#### AI-Assisted Spec Writing Process

| Phase | Human Role | AI Role |
|-------|------------|---------|
| Intent capture | Describe problem, constraints | Structure and clarify |
| Requirement extraction | Validate completeness | Generate from context |
| Edge case identification | Confirm relevance | Enumerate possibilities |
| Acceptance criteria | Approve criteria | Draft testable conditions |
| Format standardization | Choose format | Apply template consistently |

#### Supported Formats

- **Natural language** (most common)
- **Structured formats** (YAML, JSON, Markdown)
- **Formal specifications** (OpenAPI, JSON Schema for APIs)
- **BDD format** (Given-When-Then)

### Templates

#### AI Prompt for Spec Generation

```markdown
Generate a specification for [FEATURE_NAME]:

**Context:**
- Product: [product description]
- Target users: [user personas]
- Constraints: [technical/business constraints]

**Requirements:**
1. Generate functional requirements (FR-X format)
2. Identify edge cases
3. Write acceptance criteria
4. Note dependencies
5. Flag potential risks

**Format:** Use standard spec.md template
```

#### Spec Review Checklist (AI-Assisted)

```markdown
## AI Spec Review

- [ ] All functional requirements have acceptance criteria
- [ ] Edge cases identified and documented
- [ ] Dependencies explicitly listed
- [ ] Constraints are testable/measurable
- [ ] Scope is clearly bounded (what's NOT included)
- [ ] User stories follow format: As [user], I want [action], so that [benefit]
```

### Best Practices

| Practice | Description |
|----------|-------------|
| **Tight scoping** | Keep specs focused; use multiple specs for different concerns (arch, docs, testing) |
| **Lessons learned file** | Maintain file AI learns from past hiccups |
| **Sprint integration** | Include spec requirements in user stories; schedule spec writing in sprint planning |
| **Iterative refinement** | Start with rough spec, refine through AI dialogue |
| **Human approval gates** | All AI-generated specs require human review before implementation |

### Tools (2025-2026)

| Tool | Type | Key Features |
|------|------|--------------|
| **AWS Kiro** | Enterprise IDE | 3-phase: Specify -> Plan -> Execute; AWS integration |
| **Claude Code** | CLI Agent | Long context, autonomous coding, Git integration |
| **GitHub Spec-Kit** | Extension | GitHub-native spec workflow |
| **Cursor** | AI IDE | Inline spec editing |
| **Windsurf** | AI IDE | Multi-file spec awareness |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Accepting AI spec without review | Always verify AI-generated specs against domain knowledge |
| Over-relying on AI for domain context | Provide rich context; AI lacks your business knowledge |
| Specs too large for context window | Break into focused, modular specs |
| Ignoring AI suggestions | Review all suggestions; AI catches edge cases humans miss |
