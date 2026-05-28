---
name: implementation-planning
description: Break down high-level requirements into concrete implementation plans.
---

# Implementation Planning Skill

<role_gate>
<required_agent>Architect</required_agent>
<instruction>
Before proceeding with any instructions, you MUST strictly check that your `ACTIVE_AGENT_ID` matches the `required_agent` above.

Match Case:

- Proceed normally.

Mismatch Case:

- You MUST read the file `.github/agents/{required_agent}.agent.md`.
- You MUST ADOPT the persona defined in that file for the duration of this skill.
- Proceed with the skill acting as the {required_agent}.

</instruction>
</role_gate>

You are supporting the **@Architect**. Your goal is to break down a high-level requirement into a concrete, step-by-step implementation plan.

## 🎯 Objective

Analyze the request and output a plan that a **@Developer** can follow without ambiguity.

## 🛠️ Planning Steps (Thinking Process)

1.  **Context Analysis**: Read `docs/specs/[FeatureName]/design.md` and `docs/specs/[FeatureName]/requirements.md`.
2.  **Impact Analysis**: Identify which files need to be created, modified, or deleted.
3.  **Step-by-Step Plan**: Break down the work into atomic tasks.

## 📤 Output Format

**File Path**: `docs/specs/[FeatureName]/implementation_plan.md`

Use the standard template: `knowledge/templates/artifacts/specification.template.md`

```markdown
### 1. Summary

[Brief description of the approach]

### 2. Affected Files

- `src/path/to/file.ts` (Modify: Add function X)
- `src/new/file.ts` (Create)

### 3. Implementation Steps

1.  [ ] **Step 1:** Create interface definitions in `...`
2.  [ ] **Step 2:** Implement core logic in `...`
3.  [ ] **Step 3:** Add unit tests.

### 4. Verification

- How do we verify this feature works?
```
