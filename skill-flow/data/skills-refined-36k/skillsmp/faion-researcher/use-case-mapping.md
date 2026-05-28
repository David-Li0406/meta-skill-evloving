---
id: use-case-mapping
name: "Use Case Mapping"
domain: RES
skill: faion-researcher
category: "research"
---

# Use Case Mapping

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Beginner |
| **Tags** | #research, #use-cases, #requirements |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-persona-builder-agent |

---

## Problem

Products get built without clear understanding of how users will actually use them. Issues:
- Features disconnected from real workflows
- Missing critical paths users need
- Edge cases overlooked until production
- No shared understanding across team

**The root cause:** No documented mapping between user goals and system behavior.

---

## Framework

### What is Use Case Mapping?

Use case mapping is documenting specific ways users interact with your product to achieve goals. It answers: "What exactly will users do with this?"

### Use Case Components

**Essential elements:**

| Element | Description | Example |
|---------|-------------|---------|
| Actor | Who performs the action | Freelancer, Admin, Guest |
| Goal | What they want to achieve | Create an invoice |
| Preconditions | What must be true before | User is logged in |
| Main Flow | Happy path steps | Step 1, 2, 3... |
| Alternative Flows | Variations | If payment fails... |
| Postconditions | Result when complete | Invoice sent |

### Use Case Discovery Process

#### Step 1: Identify Actors

**Actor types:**

| Type | Description | Examples |
|------|-------------|----------|
| Primary | Main beneficiary | Customer, user |
| Secondary | Supports process | Admin, moderator |
| External | System actors | Payment gateway, API |

**Questions:**
- Who will use this system?
- Who benefits from it?
- Who administers it?
- What external systems interact?

#### Step 2: List Goals

For each actor, identify goals:

**Template:**
```
Actor: [Name]
Goals:
1. [Primary goal 1]
2. [Primary goal 2]
3. [Secondary goal 1]
```

**Goal levels:**

| Level | Description | Example |
|-------|-------------|---------|
| Summary | High-level objective | Manage business finances |
| User | Specific session goal | Create invoice for client |
| Subfunction | Sub-step within goal | Add line item |

#### Step 3: Map Main Flows

For each use case, document the happy path:

```
Use Case: [Name]
Actor: [Who]
Goal: [What they want]

Preconditions:
- [Condition 1]
- [Condition 2]

Main Flow:
1. Actor [action]
2. System [response]
3. Actor [action]
4. System [response]
5. [Continue...]

Postconditions:
- [Result 1]
- [Result 2]
```

#### Step 4: Identify Alternatives

**Types of alternative flows:**

| Type | Description | Example |
|------|-------------|---------|
| Extension | Additional options | "2a. If large file, show progress" |
| Exception | Error handling | "3a. If validation fails, show error" |
| Branch | Different path | "4a. If recurring, set schedule" |

#### Step 5: Create Use Case Diagram

Visual representation:

```
┌─────────────────────────────────────────┐
│              SYSTEM                      │
│                                          │
│    (Use Case 1)  ────── (Use Case 2)    │
│         │                    │           │
│         │                    │           │
└─────────│────────────────────│───────────┘
          │                    │
     ┌────┴────┐          ┌────┴────┐
     │  Actor  │          │  Actor  │
     │    A    │          │    B    │
     └─────────┘          └─────────┘
```

---

## Templates

### Use Case Specification

```markdown
## Use Case: [UC-XXX] [Name]

### Metadata
- **ID:** UC-XXX
- **Actor:** [Primary actor]
- **Level:** [Summary/User/Subfunction]
- **Priority:** [Must/Should/Could]
- **Status:** [Draft/Reviewed/Approved]

### Description
[Brief description of what this use case accomplishes]

### Preconditions
- [ ] [Condition 1]
- [ ] [Condition 2]

### Triggers
- [What initiates this use case]

### Main Success Scenario

| Step | Actor/System | Action |
|------|--------------|--------|
| 1 | Actor | [Action] |
| 2 | System | [Response] |
| 3 | Actor | [Action] |
| 4 | System | [Response] |
| 5 | System | [Final action] |

### Alternative Flows

**2a. [Condition]**
1. [Alternative step]
2. [Alternative step]
3. Return to step 3 of main flow

**3a. [Condition]**
1. [Alternative step]
2. Use case ends (failure)

### Postconditions
**Success:**
- [Outcome when successful]

**Failure:**
- [Outcome when failed]

### Business Rules
- [BR-XXX]: [Rule description]

### Related Use Cases
- [UC-XXX]: [Included/Extended/Related]

### UI Mockup
[Link or embedded image]

### Notes
[Additional context]
```

### Use Case Summary Table

```markdown
## Use Case Map: [Product]

### Actors

| Actor | Description | Use Cases |
|-------|-------------|-----------|
| [Actor 1] | [Description] | UC-001, UC-002 |
| [Actor 2] | [Description] | UC-003, UC-004 |

### Use Cases by Priority

#### Must Have
| ID | Name | Actor | Goal |
|----|------|-------|------|
| UC-001 | [Name] | [Actor] | [Goal] |
| UC-002 | [Name] | [Actor] | [Goal] |

#### Should Have
| ID | Name | Actor | Goal |
|----|------|-------|------|
| UC-003 | [Name] | [Actor] | [Goal] |

#### Could Have
| ID | Name | Actor | Goal |
|----|------|-------|------|
| UC-004 | [Name] | [Actor] | [Goal] |

### Use Case Dependencies

```
UC-001 ──────► UC-002
              │
              ▼
         UC-003 ◄──── UC-004
```

### Coverage Matrix

| Feature | UC-001 | UC-002 | UC-003 |
|---------|--------|--------|--------|
| Login | X | | |
| Create | X | X | |
| Edit | | X | X |
| Delete | | | X |
```

---

## Examples

### Example 1: Invoice Creation

```markdown
## Use Case: UC-003 Create Invoice

### Metadata
- **Actor:** Freelancer
- **Level:** User goal
- **Priority:** Must

### Preconditions
- [ ] User is logged in
- [ ] At least one client exists

### Main Success Scenario

| Step | Actor/System | Action |
|------|--------------|--------|
| 1 | Freelancer | Clicks "New Invoice" |
| 2 | System | Shows invoice form with auto-number |
| 3 | Freelancer | Selects client from dropdown |
| 4 | System | Populates client details |
| 5 | Freelancer | Adds line items (service, hours, rate) |
| 6 | System | Calculates subtotal and tax |
| 7 | Freelancer | Sets due date and clicks "Send" |
| 8 | System | Sends invoice email to client |

### Alternative Flows

**3a. Client doesn't exist**
1. Freelancer clicks "Add New Client"
2. System shows client form (UC-002)
3. Return to step 4

**7a. Save as draft**
1. Freelancer clicks "Save Draft"
2. System saves invoice with draft status
3. Use case ends (draft saved)

### Postconditions
**Success:**
- Invoice sent to client
- Invoice appears in "Sent" list
- Payment link included in email
```

### Example 2: User Registration

```markdown
## Use Case: UC-001 Register Account

### Metadata
- **Actor:** Visitor
- **Level:** User goal
- **Priority:** Must

### Main Success Scenario

| Step | Actor/System | Action |
|------|--------------|--------|
| 1 | Visitor | Clicks "Sign Up" |
| 2 | System | Shows registration form |
| 3 | Visitor | Enters email and password |
| 4 | System | Validates email format and password strength |
| 5 | Visitor | Clicks "Create Account" |
| 6 | System | Creates account, sends verification email |
| 7 | Visitor | Clicks link in email |
| 8 | System | Marks email verified, redirects to onboarding |

### Alternative Flows

**4a. Email already exists**
1. System shows "Email already registered"
2. System offers password reset option
3. Use case ends (no new account)

**4b. Password too weak**
1. System shows password requirements
2. Visitor enters stronger password
3. Return to step 4

**7a. Link expired**
1. System shows "Link expired"
2. System offers to resend verification
3. Return to step 6
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too vague | Be specific about each step |
| Missing alternatives | Always document error cases |
| System-centric | Write from actor's perspective |
| Too detailed | Stay at user goal level |
| No preconditions | Always state what must be true |
| Skipping validation | Review with actual users |

---

## Related Methodologies

- **jobs-to-be-done:** Jobs to Be Done
- **user-story-mapping:** User Story Mapping
- **writing-specifications:** Writing Specifications
- **user-journey-mapping:** User Journey Mapping
- **requirements-elicitation:** Requirements Elicitation

---

## Agent

**faion-persona-builder-agent** helps with use cases. Invoke with:
- "Map use cases for [product]"
- "Write use case for [goal]"
- "What alternative flows should [use case] have?"
- "Review my use case: [specification]"

---

*Methodology | Research | Version 1.0*
