---
issue_type: ${ISSUE_TYPE}
created: ${DATE}
status: Active
claude_plan: ${CLAUDE_PLAN_PATH}
---

# ${SPEC_NAME}

## Goal

${GOAL_DESCRIPTION}

<!-- User Stories section: Include when Initiative issue type -->
## User Stories

> Include when: Initiative issue type

### P1 (Critical)

- US001: ${USER_STORY_1}
  - **Independent test:** ${HOW_TO_TEST_INDEPENDENTLY}

### P2 (Important)

- US002: ${USER_STORY_2}
  - **Independent test:** ${HOW_TO_TEST_INDEPENDENTLY}

### P3 (Nice to have)

- US003: ${USER_STORY_3}
  - **Independent test:** ${HOW_TO_TEST_INDEPENDENTLY}

<!-- End User Stories section -->

## Requirements

### Functional Requirements

- ${FUNCTIONAL_REQ_1}
- ${FUNCTIONAL_REQ_2}
- ${FUNCTIONAL_REQ_3}

### Technical Requirements

- ${TECHNICAL_REQ_1}
- ${TECHNICAL_REQ_2}

## Acceptance Criteria

- [ ] Given ${PRECONDITION_1}
  When ${ACTION_1}
  Then ${EXPECTED_RESULT_1}

- [ ] Given ${PRECONDITION_2}
  When ${ACTION_2}
  Then ${EXPECTED_RESULT_2}

- [ ] Given ${PRECONDITION_3}
  When ${ACTION_3}
  Then ${EXPECTED_RESULT_3}

<!-- API Contract section: Include when Feature/Initiative involves API changes -->
## API Contract

> Include when: Feature/Initiative involves API changes

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| ${METHOD} | ${PATH} | ${PURPOSE} |

### Request/Response

```yaml
# ${ENDPOINT_NAME}
request:
  ${REQUEST_SCHEMA}
response:
  ${RESPONSE_SCHEMA}
```

<!-- End API Contract section -->

<!-- Implementation Strategy section: Include when Initiative issue type -->
## Implementation Strategy

> Include when: Initiative issue type

### Approach

${APPROACH}  <!-- MVP First | Incremental | Parallel Team -->

### Phases Overview

- **Phase 1:** ${PHASE_1_GOAL} - MVP deliverable
- **Phase 2:** ${PHASE_2_GOAL} - Incremental value
- **Phase 3:** ${PHASE_3_GOAL} - Full feature

### Rollout

${ROLLOUT_STRATEGY}

<!-- End Implementation Strategy section -->

## Dependency Graph

> Machine-readable: [dependencies.yaml](dependencies.yaml)

```
Phase 1 (${PHASE_1_NAME})
├── ${TASK_1}
└── ${TASK_2}
        │
Phase 2 (${PHASE_2_NAME})
├── ${TASK_3} ◄── ${TASK_1}
└── ${TASK_4} ◄── ${TASK_2}
        │
Phase 3 (${PHASE_3_NAME})
└── ${TASK_5} ◄── ${TASK_3}, ${TASK_4}
```

## Non-Goals

- ${EXPLICIT_NON_GOAL_1}
- ${EXPLICIT_NON_GOAL_2}
