---
name: update-docs
description: Review and update documentation after implementation changes. Syncs docs/ and .claude/ with current codebase state. Auto-triggers on "update docs", "sync documentation", "fix docs", "docs out of date", "update the documentation".
---

# Documentation Update Guide

You are helping update RentPath documentation to reflect recent implementation changes.

## Arguments

This skill accepts optional arguments to scope the update:

| Usage                            | Behavior                              |
| -------------------------------- | ------------------------------------- |
| `/update-docs`                   | Review all docs, find discrepancies   |
| `/update-docs applications`      | Focus on application-related docs     |
| `/update-docs docs/modules/`     | Update only files in that directory   |
| `/update-docs wizard validation` | Update wizard and validation docs     |
| `/update-docs .claude/`          | Update only Claude configuration docs |

When arguments are provided, focus the review on those specific areas instead of scanning everything.

## Before You Start

1. **Understand what changed**: Review recent code changes or ask the user
2. **Identify affected docs**: Use the documentation map below
3. **Check for discrepancies**: Compare code behavior with documented behavior

## Documentation Map

### Project Documentation (`docs/`)

| File            | Content                                             |
| --------------- | --------------------------------------------------- |
| `docs/INDEX.md` | Documentation navigation, update if adding new docs |
| `docs/TODO.md`  | Roadmap, mark completed items                       |
| `docs/IDEAS.md` | Future ideas, move implemented ones to TODO         |

#### Architecture (`docs/architecture/`)

| File                            | Content                                       |
| ------------------------------- | --------------------------------------------- |
| `docs/architecture/overview.md` | Domain structure, tech stack, key decisions   |
| `docs/architecture/storage.md`  | S3/CloudFront, signed URLs, storage patterns  |
| `docs/architecture/i18n.md`     | Multi-language support, translation structure |

#### Modules (`docs/modules/`)

| File                           | Content                                     |
| ------------------------------ | ------------------------------------------- |
| `docs/modules/users.md`        | User, PropertyManager, TenantProfile models |
| `docs/modules/properties.md`   | Property listings, types, specs, visibility |
| `docs/modules/applications.md` | Application workflow, status transitions    |
| `docs/modules/leads.md`        | Lead tracking, conversion funnel            |
| `docs/modules/tokens.md`       | Invite tokens, access control               |

#### Patterns (`docs/patterns/`)

| File                          | Content                                      |
| ----------------------------- | -------------------------------------------- |
| `docs/patterns/wizard.md`     | Multi-step wizard architecture, step locking |
| `docs/patterns/validation.md` | Laravel Precognition, FormRequest as truth   |
| `docs/patterns/user-flows.md` | PM and tenant user journeys                  |

### Claude Configuration (`.claude/`)

| File/Folder         | Content                                    |
| ------------------- | ------------------------------------------ |
| `.claude/CLAUDE.md` | Project overview, key files, instructions  |
| `.claude/rules/`    | Laravel conventions, tool usage, pipelines |
| `.claude/skills/`   | Reusable procedural knowledge              |
| `.claude/agents/`   | Specialized subagent definitions           |

#### Rules (`.claude/rules/`)

| File                 | Content                                   |
| -------------------- | ----------------------------------------- |
| `laravel-boost.md`   | Laravel/PHP conventions, package versions |
| `tool-usage.md`      | When to use which tool, agent selection   |
| `agent-pipelines.md` | Multi-agent coordination patterns         |

#### Skills (`.claude/skills/`)

| Skill           | Purpose                                   |
| --------------- | ----------------------------------------- |
| `new-feature/`  | Full feature implementation workflow      |
| `test-feature/` | Pest PHP testing patterns                 |
| `refactor/`     | Service layer extraction guide            |
| `wizard-field/` | Adding fields to wizard forms             |
| `db-explore/`   | Safe database exploration                 |
| `update-docs/`  | This skill - documentation updates        |
| `commit/`       | Session-scoped commits, no AI attribution |

#### Agents (`.claude/agents/`)

| Agent                | Purpose                                  |
| -------------------- | ---------------------------------------- |
| `architect.md`       | System design, module boundaries         |
| `domain-expert.md`   | Business rules, workflows                |
| `feature-analyst.md` | Feature mapping, implementation planning |
| `frontend.md`        | React/UI implementation                  |
| `testing-expert.md`  | Test strategy, Pest patterns             |
| `code-reviewer.md`   | Quality review, security                 |
| `infrastructure.md`  | AWS, Terraform, DevOps                   |

## Update Process

### Step 1: Identify Changed Areas

```bash
# See what files changed
git diff --name-only

# See what's staged
git diff --staged --name-only
```

Map code changes to documentation:

| Code Area Changed        | Update These Docs                              |
| ------------------------ | ---------------------------------------------- |
| Models/migrations        | `docs/modules/[entity].md`                     |
| Controllers/routes       | `docs/modules/`, `docs/patterns/user-flows.md` |
| Validation/FormRequests  | `docs/patterns/validation.md`                  |
| Wizard steps             | `docs/patterns/wizard.md`                      |
| Storage/S3               | `docs/architecture/storage.md`                 |
| i18n/translations        | `docs/architecture/i18n.md`                    |
| New patterns/conventions | `.claude/rules/`, `docs/architecture/`         |
| New skills/agents        | Update this skill's documentation map          |

### Step 2: Review Documentation

For each affected doc:

1. **Read current state** - Understand what's documented
2. **Compare with code** - Identify discrepancies
3. **List changes needed**:
    - Add new concepts/features
    - Remove deprecated content
    - Fix incorrect information
    - Update examples/code snippets

### Step 3: Make Updates

**Principles:**

- Keep docs concise - remove redundancy
- Use tables for structured information
- Include code examples where helpful
- Cross-reference related docs
- Update the INDEX.md if adding new docs

**Common updates:**

```markdown
## Adding a new field

- Update model documentation with field description
- Update validation docs if new rules
- Update wizard docs if wizard field

## Adding a new endpoint

- Update module docs with route
- Update user-flows if changes journey

## Changing architecture

- Update overview.md
- Update relevant pattern docs
- Update .claude/rules if convention changes
```

### Step 4: Verify Consistency

Check for cross-document consistency:

- [ ] Field names match between docs and code
- [ ] Status values/enums are current
- [ ] Route paths are accurate
- [ ] Code examples compile/work
- [ ] Related docs reference each other correctly

## Quick Reference: What to Update When

| Change Type            | Primary Doc                     | Secondary Docs                        |
| ---------------------- | ------------------------------- | ------------------------------------- |
| New database field     | `docs/modules/[entity].md`      | Factory docs if test-related          |
| New API endpoint       | `docs/modules/[entity].md`      | `docs/patterns/user-flows.md`         |
| New model              | Create in `docs/modules/`       | `docs/INDEX.md`, overview             |
| New validation pattern | `docs/patterns/validation.md`   | -                                     |
| New wizard step        | `docs/patterns/wizard.md`       | `docs/modules/applications.md`        |
| New skill              | Create in `.claude/skills/`     | This skill's map, `tool-usage.md`     |
| New agent              | Create in `.claude/agents/`     | `agent-pipelines.md`, `tool-usage.md` |
| Architecture change    | `docs/architecture/overview.md` | Affected pattern docs                 |
| Convention change      | `.claude/rules/`                | `CLAUDE.md` if significant            |

## Output Format

After updating, provide summary:

```markdown
## Documentation Updates

### Updated Files

- `docs/modules/applications.md` - Added new `visit_notes` field
- `docs/patterns/wizard.md` - Updated step 5 description

### Removed Content

- Removed deprecated `legacy_status` field from applications docs

### Added Content

- New section on visit scheduling workflow

### Cross-Reference Fixes

- Fixed broken link in INDEX.md
```
