---
plan: NN
task_group: [group-name]
depends_on: []
source_tasks: ["N.1", "N.2", "N.3"]
---

<objective>
[From task group description and spec context]

Purpose: [Why this matters]
Output: [What will be created]
</objective>

<context>
@agent-os/specs/[spec-name]/spec.md
@agent-os/specs/[spec-name]/planning/requirements.md
</context>

<constraints>
[Constraints extracted from spec - boundaries, rules, limitations]
</constraints>

<tasks>

<task type="auto">
  <name>Task 1: [Action-oriented name]</name>
  <files>[exact/paths.ts]</files>
  <action>[Specific implementation with what to avoid and WHY]</action>
  <verify>[Executable command]</verify>
  <done>[Measurable acceptance criteria]</done>
</task>

</tasks>

<verification>
- [ ] [Overall check 1]
- [ ] [Overall check 2]
</verification>

<success_criteria>
- All tasks completed
- All verification checks pass
- [Spec-specific criteria]
</success_criteria>

<output>
Create .long-run/summaries/[NN]-SUMMARY.md
</output>
