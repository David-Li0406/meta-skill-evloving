---
name: spec-creation
description: Create comprehensive feature specifications for Claude Code projects using iterative refinement with ISO/IEC/IEEE 29148:2018 criteria. Use when user requests creating a technical specification (ТЗ) for a new feature or when starting workflow step "а" - Создание ТЗ. Automatically invoked via /spec-creation command or when explicitly asked to create a spec/ТЗ.
---

# Spec Creation Skill

Create comprehensive feature specifications for the Web Portal project through iterative requirement refinement based on ISO/IEC/IEEE 29148:2018 quality criteria.

## When to Use This Skill

- User requests creating a technical specification (ТЗ, техническое задание)
- User says "создай ТЗ", "напиши спецификацию", "создай spec"
- Starting workflow step "а" - Создание ТЗ (per CLAUDE.md workflow)
- User wants to document a feature before implementation

## Output Location

Specifications are created in `.ai/specs/` directory with naming pattern:
- `feature-{slug}.md` for new features
- `bugfix-{slug}.md` for bug fixes

## Core Principles

### Iterative Requirement Refinement

This skill uses **multi-round validation** with IEEE 29148:2018 quality criteria:

**Critical:** A specification is NOT complete until validation achieves ≥85% score.

### Progressive Disclosure

- Keep spec template concise in SKILL.md
- Reference detailed templates in `references/` directory
- Load templates only when needed

## IEEE 29148:2018 Quality Assessment Framework

The requirements quality score is calculated from 5 sections, each containing specific criteria with maximum weight of 5 per criterion.

### Section 1: Core Quality Attributes (40 points total)

| Criterion | Weight | Check |
|-----------|--------|-------|
| **Necessary** | 5 | Does the requirement define an essential capability/characteristic? |
| **Unambiguous** | 5 | Is there only one possible interpretation? |
| **Complete** | 5 | Are all necessary capabilities/characteristics/constraints described? |
| **Consistent** | 5 | Is it free of conflicts with other requirements? |
| **Singular** | 5 | Does it address only one concern (not compound)? |
| **Feasible** | 5 | Is it achievable with given constraints (time, budget, technology)? |
| **Traceable** | 5 | Can it be linked to stakeholder needs and business objectives? |
| **Verifiable** | 5 | Can fulfillment be measured through testing/inspection? |

### Section 2: Context & Rationale (20 points total)

| Criterion | Weight | Check |
|-----------|--------|-------|
| **Implementation-free** | 5 | Does it avoid dictating HOW to implement (WHAT vs HOW)? |
| **Affordable** | 5 | Is it within budget/resource constraints? |
| **Bounded** | 5 | Are scope boundaries clearly defined? |
| **Rationale stated** | 5 | Is the reason for this requirement explained? |

### Section 3: Completeness of Description (20 points total)

| Criterion | Weight | Check |
|-----------|--------|-------|
| **Inputs defined** | 5 | Are all inputs clearly specified (data, parameters, user actions)? |
| **Outputs defined** | 5 | Are expected outputs clearly described (return values, UI changes, side effects)? |
| **Constraints identified** | 5 | Are technical/business/environmental constraints noted? |
| **Edge cases covered** | 5 | Are error scenarios and boundary conditions addressed? |

### Section 4: Traceability & Stakeholders (10 points total)

| Criterion | Weight | Check |
|-----------|--------|-------|
| **Stakeholder mapping** | 5 | Can the requirement be linked to specific stakeholders/users? |
| **Business value** | 5 | Does it align with stated business objectives or user needs? |

### Section 5: Acceptance & Prioritization (10 points total)

| Criterion | Weight | Check |
|-----------|--------|-------|
| **Prioritization clear** | 5 | Is priority level specified (must-have vs nice-to-have)? |
| **Success criteria** | 5 | Are measurable acceptance criteria defined? |

**Maximum Score: 100 points**
**Threshold: 85 points minimum to proceed**

## Iterative Validation Process

### Round Structure

For each validation round:

1. **Display Current Requirements Version** - Show the accumulated requirements in markdown format
2. **Calculate IEEE 29148 Score** - Evaluate each criterion and calculate total
3. **Decision Point**:
   - If score ≥ 85: Proceed to next phase
   - If score < 85: Use `AskUserQuestion` to clarify gaps
4. **Enrich & Re-evaluate** - Update requirements with answers and re-score

### Round 1: Core Requirements Validation

**Initial Requirements Gathering:**

```
## Initial Requirements

### Feature Overview
- **Feature name**: {from user}
- **Type**: {new feature/bug fix/enhancement}
- **Vision**: {one sentence}

### Core Requirements
- {Must-have requirements from user}

### Stakeholders
- {Target users, roles}

### Constraints
- {Technical/business constraints}
```

**Evaluate using Section 1 (Core Quality Attributes) + Section 2 (Context & Rationale)**

**Common Gaps to Address via AskUserQuestion:**
- Unambiguous: "Which specific notification channels?" (email, in-app, SMS?)
- Complete: "What data needs to be stored for each notification?"
- Feasible: "Are there rate limits or API constraints?"
- Implementation-free: "What business outcome, not which library?"

### Round 2: Technical Completeness Validation

**Extended Requirements:**

```
## Technical Requirements

### Functional Requirements
- {Specific functional behaviors}

### Non-Functional Requirements
- {Performance, security, usability}

### API & Database Changes
- {Endpoints, schemas, migrations}

### Frontend Changes
- {Pages, components, templates}
```

**Evaluate using Section 3 (Completeness of Description)**

**Common Gaps to Address:**
- Inputs defined: "What parameters does the API accept?"
- Outputs defined: "What response format/status codes?"
- Constraints identified: "Are there authentication requirements?"
- Edge cases covered: "What happens if the external service is down?"

### Round 3: Traceability & Acceptance Validation

**Final Requirements:**

```
## Implementation Plan

### Stages
- {Logical breakdown with dependencies}

### Acceptance Criteria per Stage
- {Measurable, testable criteria}

### File Changes
- {Concrete paths: src/...}

### Documentation Updates
- {ARCHITECTURE.md, API docs, etc.}
```

**Evaluate using Section 4 (Traceability) + Section 5 (Acceptance)**

**Common Gaps to Address:**
- Stakeholder mapping: "Which user role triggers this workflow?"
- Business value: "What problem does this solve for the user?"
- Success criteria: "How do we verify this works?" (not "it works")
- Prioritization: "Is this must-have for MVP or can it wait?"

## Output Format

After all validation rounds pass, generate the specification file:

```markdown
# {Feature Name} - Feature Specification

> **Дата создания:** {YYYY-MM-DD}
> **Ветка:** `feature/{slug}`
> **Статус:** В разработке

---

## Видение

{Vision statement}

**Ключевые требования:**
- {Bullet list of must-haves}

---

## План реализации

### Этап 1: {Stage Name} (~{lines} строк)
**Статус:** В разработке

**Цель:** {Purpose}

**Задачи:**
- [ ] {Task 1}
- [ ] {Task 2}

**Файлы:**
- `path/to/file.py` (create/modify)

**Критерий приёмки:**
- {Testable criterion}

---

## История изменений

| Дата | Этап | Коммит | Описание |
| ---- | ---- | ------ | -------- |
| {date} | - | - | ТЗ создано |
```

## Validation Examples

### Example 1: Ambiguous Requirement

**Initial:** "System should be fast"

**IEEE 29148 Evaluation:**
- Unambiguous: 0/5 (what is "fast"?)
- Verifiable: 0/5 (how to measure?)
- **Score: 2/100**

**AskUserQuestion:**
```
What performance target do you need?
- Response time < 200ms
- Throughput > 100 req/sec
- Page load < 3s
```

**Refined:** "API endpoint must respond within 200ms for 95th percentile"

**IEEE 29148 Evaluation:**
- Unambiguous: 5/5 (clear metric)
- Verifiable: 5/5 (can measure)
- **Score: 90/100**

### Example 2: Incomplete Requirement

**Initial:** "Users receive notifications"

**IEEE 29148 Evaluation:**
- Complete: 1/5 (missing what, when, how)
- Inputs defined: 0/5
- **Score: 15/100**

**After AskUserQuestion rounds:**
"Logged-in users receive in-app notifications when wallet balance changes, with notification storing: user_id, message, timestamp, is_read flag"

**IEEE 29148 Evaluation:**
- Complete: 5/5
- Inputs defined: 5/5
- Outputs defined: 5/5
- Verifiable: 5/5
- **Score: 88/100**

## Required Templates by Round

### Round 1 Questions (Core Requirements)
1. What specific problem does this solve for the user?
2. Who are the target users/stakeholders? (roles, permissions)
3. What are the essential capabilities (must-haves)?
4. What defines "done" for this feature?
5. Are there technical/business constraints?

### Round 2 Questions (Technical Details)
1. Which modules/services are affected?
2. What database changes are needed (tables, migrations)?
3. What API endpoints (new or modified)?
4. What frontend pages/components change?
5. What external dependencies or integrations?

### Round 3 Questions (Implementation)
1. Can this be broken into 3-9 logical stages?
2. What are the dependencies between stages?
3. What are measurable acceptance criteria for each stage?
4. Which files will be modified (concrete paths)?

## Reference Templates

- [spec_template.md](references/spec_template.md) - Full spec template with placeholders
- [stage_templates.md](references/stage_templates.md) - Common stage patterns (DB, API, Frontend)
- [question_templates.md](references/question_templates.md) - Question templates by feature type

## Common Pitfalls

1. **Accepting vague requirements**: "Make it faster" → "What latency target?"
2. **Compound requirements**: "User logs in and sees dashboard" → Split into two
3. **Implementation details in requirements**: "Use Redis" → "Cache with <100ms latency"
4. **Skipping rounds**: Must complete ALL 3 validation rounds with ≥85%
5. **Generic acceptance criteria**: "It works" → "API returns 200 with valid JSON schema"

## Example Workflow

```
User: "Создай ТЗ для новой фичи уведомлений"

Claude: [Displays Initial Requirements]
## Initial Requirements
- Feature: Notifications
- Type: New feature
- Vision: Users receive notifications for events
- Must-have: Notifications for events

Claude: [Evaluates - Score: 18/100]
❌ Unambiguous: 0/5 (what events? what channels?)
❌ Complete: 1/5 (missing what, when, how)
❌ Verifiable: 0/5 (no acceptance criteria)

Claude: [Uses AskUserQuestion]
1. What types of events trigger notifications? → "Wallet changes, meeting reminders"
2. Which notification channels? → "Email + in-app"
3. Who receives notifications? → "Logged-in users, based on their preferences"

Claude: [Re-displays Requirements v2]
## Requirements v2
- Event types: wallet_balance_change, meeting_reminder
- Channels: email, in-app
- Recipients: users based on preferences

Claude: [Re-evaluates - Score: 42/100]
✅ Stakeholder mapping: 5/5
✅ Necessary: 5/5
❌ Inputs defined: 2/5 (what data in notification?)
❌ Outputs defined: 2/5 (what does user see?)
❌ Edge cases: 0/5

Claude: [Uses AskUserQuestion - Round 2]
1. What data for each notification type?
2. What if email service is down?
3. How are notifications stored/displayed?

[... continues until score ≥85 ...]

Claude: [Final Score: 87/100] ✅
Proceeds to generate .ai/specs/feature-notifications.md
```

## Final Validation Checklist

Before saving specification, verify:
1. ✅ All 3 validation rounds passed with ≥85% score
2. ✅ File follows project spec format
3. ✅ Each stage has concrete file paths and acceptance criteria
4. ✅ Russian language used for vision/tasks/criteria
5. ✅ Technical terms in English (API, database, etc.)
6. ✅ Requirements are implementation-free (WHAT, not HOW)
