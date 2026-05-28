---
title: Task Prompt Template
description: Ralph-loop prompt template for task execution workflow
file-type: template
skill: executing-tasks
---

# Task Execution Prompt Template

Use this template when starting a Ralph-loop or subagent for task execution.

## Template

```
Execute task [TASK_ID] from story [STORY_ID].

## Task Details
- Title: [TASK_TITLE]
- Type: [code|test|docs|refactor|bugfix|config]
- Estimated: [DURATION]
- Dependencies: [DEPENDENCY_LIST or "none"]

## Context
- Story spec: [PATH_TO_STORY_MD]
- Affected files: [FILE_LIST]
- Related tests: [TEST_FILE_LIST]

## Acceptance Criteria
[PASTE_RELEVANT_GHERKIN_OR_CRITERIA]

## Constraints
- Follow 6-phase task-execution workflow
- Make atomic commits with conventional format
- Update PROGRESS.yaml on completion
- Document learnings if blockers encountered

## Success Criteria
- All acceptance criteria verified
- Quality gates pass (typecheck, lint, test)
- PROGRESS.yaml updated to completed
- Commits reference task ID
```

## Usage

1. Copy template above
2. Replace bracketed placeholders with actual values
3. Use as prompt for Ralph-loop or Task() subagent
4. Verify completion against success criteria

## Placeholder Reference

| Placeholder | Source |
|-------------|--------|
| TASK_ID | PROGRESS.yaml task id |
| STORY_ID | Story folder name |
| TASK_TITLE | PROGRESS.yaml task title |
| DURATION | PROGRESS.yaml estimated time |
| DEPENDENCY_LIST | PROGRESS.yaml dependencies |
| PATH_TO_STORY_MD | story.md file path |
| FILE_LIST | From task planning or story design |
| TEST_FILE_LIST | Related test files |
| GHERKIN_OR_CRITERIA | From story.md gherkin section |
