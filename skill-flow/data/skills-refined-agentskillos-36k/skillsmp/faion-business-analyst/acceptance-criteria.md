---
id: acceptance-criteria
name: "Acceptance Criteria"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Acceptance Criteria

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Beginner
- **Tags:** #methodology #babok #acceptance-criteria #testing #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

"Done" means different things to different people. Developers think a feature is complete but users disagree. Testing cannot verify requirements because there is nothing to test against. Acceptance meetings become debates about what was actually required.

Without acceptance criteria:
- Unclear "done" definition
- Subjective acceptance
- Untestable requirements
- Disputes about completion

---

## Framework

### What are Acceptance Criteria?

Acceptance criteria define the conditions that must be met for a requirement to be accepted as complete. They answer: "How do we know when this is done?"

### Characteristics of Good Acceptance Criteria

| Attribute | Description |
|-----------|-------------|
| **Testable** | Can create a test to verify |
| **Clear** | No ambiguity |
| **Concise** | Brief and focused |
| **Achievable** | Technically feasible |
| **Relevant** | Related to the requirement |

### Step 1: Understand the Requirement

Before writing acceptance criteria:
- What is the user trying to do?
- What outcome do they expect?
- What could go wrong?
- What are the boundaries?

### Step 2: Choose a Format

**Given-When-Then (BDD style):**
```
Given [precondition]
When [action]
Then [expected result]
```

**Rule-based:**
```
- The system must [behavior]
- The system must not [behavior]
- The system should [behavior]
```

**Checklist:**
```
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

### Step 3: Write Acceptance Criteria

For each requirement, cover:

| Category | Question |
|----------|----------|
| **Happy path** | What happens when everything works? |
| **Alternatives** | What are valid variations? |
| **Boundaries** | What are the limits? |
| **Errors** | What happens when things go wrong? |
| **Security** | Are there access controls? |
| **Performance** | Are there speed requirements? |

### Step 4: Validate with Stakeholders

Review criteria with:
- Product Owner (business correctness)
- Developers (technical feasibility)
- QA (testability)

### Step 5: Use for Testing

Acceptance criteria become test cases:
- Each criterion = at least one test
- Automated where possible
- Part of Definition of Done

---

## Templates

### Acceptance Criteria Template (BDD)

```markdown
# Acceptance Criteria: [Story/Requirement ID]

**Requirement:** [Brief description]
**Author:** [Name]
**Date:** [Date]

## Scenarios

### Scenario 1: [Happy Path Name]
**Given** [precondition/context]
**And** [additional precondition]
**When** [action taken]
**Then** [expected outcome]
**And** [additional outcome]

### Scenario 2: [Alternative Path Name]
**Given** [precondition/context]
**When** [action taken]
**Then** [expected outcome]

### Scenario 3: [Error Handling Name]
**Given** [precondition/context]
**When** [action that causes error]
**Then** [error handling behavior]

## Non-Functional Criteria
- Performance: [Specific performance criteria]
- Security: [Specific security criteria]

## Out of Scope
- [What is NOT covered by these criteria]
```

### Acceptance Criteria Template (Rule-based)

```markdown
# Acceptance Criteria: [Story/Requirement ID]

**Requirement:** [Brief description]

## Functional Criteria
- [ ] System must [behavior 1]
- [ ] System must [behavior 2]
- [ ] System must not [behavior 3]
- [ ] When [condition], system must [behavior]
- [ ] If [condition], then [behavior], else [alternative]

## Validation Criteria
- [ ] [Field] is required
- [ ] [Field] must be [format/type]
- [ ] [Field] must be between [min] and [max]

## Error Handling Criteria
- [ ] When [error condition], display [error message]
- [ ] When [error condition], system must [recovery behavior]

## Performance Criteria
- [ ] [Action] must complete within [time]
- [ ] System must support [number] concurrent [users/transactions]

## Security Criteria
- [ ] Only [role] can [action]
- [ ] [Sensitive data] must be [encrypted/masked]
```

---

## Examples

### Example 1: Login Feature

**User Story:** As a user, I want to log in so that I can access my account.

**Acceptance Criteria:**

**Scenario 1: Successful login**
- Given I am on the login page
- And I have a valid account
- When I enter my email and password
- And click "Login"
- Then I am redirected to the dashboard
- And I see a welcome message with my name

**Scenario 2: Invalid credentials**
- Given I am on the login page
- When I enter incorrect email or password
- And click "Login"
- Then I see an error message "Invalid email or password"
- And I remain on the login page
- And the password field is cleared

**Scenario 3: Account locked**
- Given I have failed login 5 times
- When I attempt to login again
- Then I see a message "Account locked. Please try again in 30 minutes"
- And login is disabled for my account

**Non-functional:**
- Login must complete within 2 seconds
- Password must not be logged or displayed

### Example 2: Shopping Cart

**User Story:** As a customer, I want to add items to my cart.

**Acceptance Criteria:**
- [ ] User can add product to cart from product page
- [ ] User can add product to cart from search results
- [ ] Cart icon shows number of items
- [ ] Adding same product increases quantity (not duplicate line)
- [ ] Maximum quantity per product is 99
- [ ] User sees confirmation when item added
- [ ] Cart persists for 30 days for logged-in users
- [ ] Cart persists for session duration for guests

---

## Common Mistakes

1. **Too vague** - "User can log in" (what does this mean exactly?)
2. **Implementation details** - "Store in MySQL database" (how, not what)
3. **Missing scenarios** - Only happy path covered
4. **Untestable** - "System is user-friendly" (subjective)
5. **Too many** - 50 criteria for one story (break it down)

---

## Acceptance Criteria vs. Other Artifacts

| Artifact | Purpose | Level |
|----------|---------|-------|
| **Requirement** | What the system must do | High-level |
| **Acceptance Criteria** | How we know it is done | Detailed |
| **Test Case** | How we verify it works | Implementation |

**Relationship:**
```
1 Requirement → Multiple Acceptance Criteria → Multiple Test Cases
```

---

## Guidelines by Story Type

### Feature Stories
- Focus on user outcomes
- Cover happy path + key alternatives
- Include error handling
- Add performance if relevant

### Bug Fixes
- Describe expected vs. actual behavior
- Include reproduction steps
- Define "fixed" state

### Technical Stories
- Focus on technical outcomes
- Include measurable criteria
- Define verification method

---

## Definition of Done Integration

Acceptance criteria fit within Definition of Done:

**Definition of Done:**
- [ ] Code complete
- [ ] Unit tests pass
- [ ] Acceptance criteria verified ← Individual story criteria
- [ ] Code reviewed
- [ ] Documentation updated

---

## Next Steps

After writing acceptance criteria:
1. Review with team
2. Estimate story
3. Create test cases
4. Develop feature
5. Connect to Requirements Validation methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Acceptance Criteria Guidelines
