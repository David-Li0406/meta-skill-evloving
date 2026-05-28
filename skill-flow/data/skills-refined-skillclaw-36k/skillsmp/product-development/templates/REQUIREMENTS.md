# Requirements Templates

## User Persona Template

```markdown
## Persona: [Name]

### Demographics
| Attribute | Value |
|-----------|-------|
| Role | [Job title/function] |
| Technical Level | [Novice / Intermediate / Expert] |
| Industry | [If relevant] |
| Team Size | [If relevant] |

### Goals & Motivations
**Primary Goal**: [What they ultimately want to achieve]
**Secondary Goals**:
- [Goal 1]
- [Goal 2]

### Pain Points
- [Current frustration 1]
- [Current frustration 2]
- [Workaround they currently use]

### Success Metrics
- [How they measure if the product is helping]
- [KPIs they care about]

### Context of Use
- **When**: [When do they use the product]
- **Where**: [Environment - office, mobile, etc.]
- **Frequency**: [How often]
- **Duration**: [Typical session length]

### Quote
> "[A representative quote that captures their mindset]"
```

## User Story Template

```markdown
## User Story: [US-XXX]

### Story
**As a** [persona name]
**I expect to** [action/capability]
**So that** [benefit/outcome]

### Acceptance Criteria
Given [precondition]
When [action]
Then [expected result]

Given [precondition]
When [alternative action]
Then [alternative result]

### Priority
- [ ] Must Have (MVP)
- [ ] Should Have
- [ ] Could Have
- [ ] Won't Have (this release)

### Estimation
- **Complexity**: [1-5 or T-shirt size]
- **Dependencies**: [Other stories this depends on]

### Notes
[Any additional context or constraints]
```

## Technical Requirement Template

```markdown
## Technical Requirement: [TR-XXX]

### Traceability
**Derived From**: [US-XXX, US-YYY]
**Related To**: [TR-ZZZ]

### Requirement
The system shall [specific capability using RFC 2119 language: SHALL/SHOULD/MAY]

### Technical Specification
| Aspect | Specification |
|--------|---------------|
| Input | [What the system receives] |
| Processing | [What the system does] |
| Output | [What the system produces] |
| Performance | [Timing/throughput requirements] |
| Security | [Security considerations] |

### Validation
**Test Approach**: [Unit / Integration / E2E / Manual]
**Validation Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Constraints
- [Technical constraint 1]
- [Technical constraint 2]

### Assumptions
- [Assumption 1]
- [Assumption 2]
```

## Non-Functional Requirement Template

```markdown
## NFR: [NFR-XXX] - [Category]

### Categories
- [ ] Performance
- [ ] Scalability
- [ ] Reliability
- [ ] Security
- [ ] Maintainability
- [ ] Usability
- [ ] Compliance

### Requirement
[Clear statement of the non-functional requirement]

### Metrics
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [Metric 1] | [Target value] | [How measured] |
| [Metric 2] | [Target value] | [How measured] |

### Test Scenarios
| Scenario | Expected Outcome |
|----------|-----------------|
| [Scenario 1] | [Expected] |
| [Scenario 2] | [Expected] |

### Trade-offs
[What we sacrifice to achieve this NFR]

### Dependencies
[Other NFRs this affects or is affected by]
```

## Requirements Traceability Matrix Template

```markdown
## Traceability Matrix

| User Story | Technical Req | NFR | Test Case | Status |
|------------|---------------|-----|-----------|--------|
| US-001 | TR-001, TR-002 | NFR-001 | TC-001 | ✅ |
| US-002 | TR-003 | - | TC-002 | ✅ |
| US-003 | TR-004, TR-005 | NFR-002 | TC-003, TC-004 | ⚠️ Gap |
| US-004 | (pending) | - | - | ❌ Not started |

### Coverage Summary
| Artifact | Total | Traced | Coverage |
|----------|-------|--------|----------|
| User Stories | [X] | [Y] | [Z]% |
| Technical Reqs | [X] | [Y] | [Z]% |
| Test Cases | [X] | [Y] | [Z]% |

### Gaps Identified
| Gap ID | Description | Resolution |
|--------|-------------|------------|
| GAP-001 | [Description] | [How to address] |
```
