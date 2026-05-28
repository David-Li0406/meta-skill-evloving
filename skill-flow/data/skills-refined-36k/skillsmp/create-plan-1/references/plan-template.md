# Plan Template

Use this template structure when creating implementation plans. All sections are required unless marked optional.

---

## Contents
- Plan Title
- Overview
- Context
- Exploration Findings
- Design Decisions
- Implementation
- Files Summary
- Verification
- Resources
- Open Questions (Optional)
- Appendix
- IMPORTANT (Handoff Test) IMPORTANT
- Self-Containment Checklist

# [Plan Title]

> Auto-generated: [timestamp]
> Status: Draft | Ready for Implementation

## Overview

[One paragraph summary of what this plan accomplishes. Should answer: What are we building? Why? What's the expected outcome?]

## Context

### Background
[Business or technical context that motivated this work. Why is this needed now?]

### Current State
[Description of relevant existing functionality, if any. What does the system look like today?]

### Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

### Non-Goals (Out of Scope)
- Item explicitly excluded from this work
- Another excluded item

## Exploration Findings

Document what was discovered during codebase investigation.

### Relevant Files Discovered
| File | Relevance |
|------|-----------|
| `path/to/file.py` | Contains X which we'll extend |
| `path/to/tests.py` | Test patterns to follow |

### Existing Patterns to Follow
- Pattern 1: How similar features are implemented
- Pattern 2: Error handling approach used elsewhere

### Constraints Discovered
- Constraint 1: Must work with existing X
- Constraint 2: Cannot modify Y due to Z

## Design Decisions

Document all significant decisions made during planning with their rationale.

### Decision 1: [Topic]

**Chosen:** [The selected approach]

**Rationale:** [Why this was selected given the requirements and constraints]

### Decision 2: [Topic]

**Chosen:** [The selected approach]

**Rationale:** [Explanation]

## Implementation

### Phase 1: [Phase Name] (if multi-phase)

#### Step 1.1: [Step Name]

**Description:** [One sentence: what this step accomplishes]

**Files to modify:**
| File | Function/Class | Change Description |
|------|----------------|-------------------|
| `path/to/file.py` | `function_name()` | Add parameter X, modify return type |
| `path/to/other.py` | `ClassName` | Add new method `do_thing()` |

**Files to create:**
| File | Purpose | Key Contents |
|------|---------|--------------|
| `path/to/new.py` | Implements X | Classes: A, B. Functions: c(), d() |

**Technical approach:**
- Approach detail 1
- Approach detail 2

**Integration points:**
- How this connects to step X.Y
- What must be true before this step
- What this enables for later steps

**Verification for this step:**
- [ ] Specific check that this step succeeded

---

#### Step 1.2: [Step Name]

**Description:** [One sentence: what this step accomplishes]

**Files to modify:**
| File | Function/Class | Change Description |
|------|----------------|-------------------|
| ... | ... | ... |

**Technical approach:**
- ...

**Verification for this step:**
- [ ] ...

---

### Phase 2: [Phase Name] (if needed)

[Repeat step structure]

---

## Files Summary

### Files to Create
| File | Purpose |
|------|---------|
| `path/to/new_file.py` | Brief description |

### Files to Modify
| File | Changes |
|------|---------|
| `path/to/existing.py` | What's being changed |

### Files to Delete (if any)
| File | Reason |
|------|--------|
| `path/to/old_file.py` | Replaced by X |

## Verification

### Acceptance Criteria

- [ ] Criterion 1: [Specific, testable condition]
- [ ] Criterion 2: [Specific, testable condition]
- [ ] Criterion 3: [Specific, testable condition]

### Test Commands

```bash
# Unit tests
pytest tests/unit/test_feature.py -v

# Integration tests
pytest tests/integration/test_feature_integration.py -v

# Manual verification
curl -X POST http://localhost:8000/api/endpoint -d '{"test": "data"}'
```

### Test Cases to Add

| Test | Description | File |
|------|-------------|------|
| `test_feature_happy_path` | Tests normal operation | `tests/test_feature.py` |
| `test_feature_error_handling` | Tests error conditions | `tests/test_feature.py` |

## Resources

### External Documentation
- [Link to relevant docs](url)
- [Library documentation](url)

### Related Code
- `path/to/related/implementation.py` - Similar pattern we can follow
- `path/to/tests/example.py` - Test patterns to emulate

## Open Questions (Optional)

[Any remaining uncertainties - should be minimal in a finalized plan]

- Question 1: [If unresolved, note who should answer]
- Question 2: [If unresolved, note who should answer]

## Appendix 

### Diagrams

[ASCII diagrams, mermaid diagrams, or references to external diagrams]

### Additional Context

[Any extra information that didn't fit elsewhere but is relevant]

---


## IMPORTANT (Handoff Test) IMPORTANT

**The plan passes if a developer who never saw the original conversation could:**

1. **Understand the goal** - Read the Overview and know exactly what success looks like
2. **Execute without asking** - Follow Implementation steps without needing clarification
3. **Make the same decisions** - Design Decisions explain WHY, not just WHAT
4. **Verify correctly** - Acceptance Criteria are unambiguous pass/fail
5. **Handle surprises** - Edge cases and error scenarios are documented

### Self-Containment Checklist

- [ ] No pronouns without antecedents ("it", "this", "that" are defined)
- [ ] No assumed context ("as discussed" - include what was discussed)
- [ ] Every file path is complete and absolute from project root
- [ ] Every function/class name is specified, not described
- [ ] Acceptance criteria can be verified without reading the conversation
- [ ] Someone unfamiliar with the project could find all mentioned files
