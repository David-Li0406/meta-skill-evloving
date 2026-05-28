---
name: musubix-sdd-workflow
description: Use this skill when asked to develop features using the MUSUBIX methodology, create requirements, designs, or implement code following the 9 constitutional articles.
---

# MUSUBIX SDD Workflow Skill

This skill guides you through the complete SDD workflow for MUSUBIX projects.

## Prerequisites

Before starting any development task:

1. Read the `steering/` directory for project context.
2. Check `steering/rules/constitution.md` for the 9 constitutional articles.
3. Review existing specs in `storage/specs/`.

## Complete Workflow

### Phase 1: Requirements Definition

#### Step 1: Create Requirements Document (Article IV - EARS Format)

Create requirements using EARS patterns:

```markdown
# REQ-[CATEGORY]-[NUMBER]

**種別**: [UBIQUITOUS|EVENT-DRIVEN|STATE-DRIVEN|UNWANTED|OPTIONAL]  
**優先度**: [P0|P1|P2]

**要件**:  
[EARS形式の要件文]

**トレーサビリティ**: DES-XXX, TEST-XXX
```

EARS Patterns:
- **Ubiquitous**: `THE [system] SHALL [requirement]`
- **Event-driven**: `WHEN [event], THE [system] SHALL [response]`
- **State-driven**: `WHILE [state], THE [system] SHALL [response]`
- **Unwanted**: `THE [system] SHALL NOT [behavior]`
- **Optional**: `IF [condition], THEN THE [system] SHALL [response]`

#### Step 2: Requirements Review Loop

Review requirements for:
- EARS format compliance
- Completeness and clarity
- Testability
- Traceability readiness

**Repeat until no issues remain.**

### Phase 2: Design

#### Step 3: Create Design Document (Article VII - Design Patterns)

Create C4 model design documents:

1. **Context Level**: System boundaries and external actors.
2. **Container Level**: Technology choices and container composition.
3. **Component Level**: Internal structure of containers.
4. **Code Level**: Implementation details.

Design document template:
```markdown
# DES-[CATEGORY]-[NUMBER]

## トレーサビリティ
- 要件: REQ-XXX

## C4モデル
### Level 2: Container
[PlantUML diagram]

## コンポーネント設計
[Component details]
```

#### Step 4: Design Review Loop

Review design for:
- Requirement coverage
- SOLID principles compliance
- Design pattern appropriateness
- Traceability to requirements

**Repeat until no issues remain.**

### Phase 3: Task Decomposition

#### Step 5: Generate Tasks

Generate implementation tasks from design:

```markdown
# TSK-[CATEGORY]-[NUMBER]

## 関連設計: DES-XXX
## 関連要件: REQ-XXX

## タスク内容
[Implementation task description]

## 受入基準
- [ ] Criterion 1
- [ ] Criterion 2
```

### Step 6: Implementation (Article III - Test-First)

Follow the Red-Green-Blue cycle:

1. **Red**: Write a failing test first.
2. **Green**: Write minimal code to pass.
3. **Blue**: Refactor while keeping tests green.

### Step 7: Traceability Validation (Article V)

Ensure 100% traceability:
```
REQ-* → DES-* → TSK-* → Code → Test
```

Add requirement IDs in code comments:
```typescript
/**
 * @see REQ-INT-001 - Neuro-Symbolic Integration
 */
```

## CLI Commands

```bash
# Requirements
npx musubix requirem
```