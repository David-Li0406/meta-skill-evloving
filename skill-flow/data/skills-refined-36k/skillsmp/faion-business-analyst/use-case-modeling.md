---
id: use-case-modeling
name: "Use Case Modeling"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Use Case Modeling

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #use-case #modeling #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Requirements are written as features but nobody understands how users will actually use the system. Developers build functionality without understanding context. Testing cannot cover real user scenarios. Edge cases and exceptions are discovered during development.

Without use case modeling:
- Missing user context
- Incomplete scenarios
- Late discovery of edge cases
- Poor test coverage

---

## Framework

### What is a Use Case?

A use case describes a sequence of actions a system performs to provide value to an actor. It captures WHO does WHAT with the system and WHY.

### Use Case Components

| Component | Description |
|-----------|-------------|
| **Actor** | Who or what interacts with the system |
| **Use Case** | Specific goal the actor achieves |
| **System** | What is being built/analyzed |
| **Scenario** | Specific path through the use case |

### Step 1: Identify Actors

Who interacts with the system?

**Actor types:**
- **Primary actors:** Initiate use cases to achieve goals
- **Secondary actors:** Support the system (databases, services)
- **External systems:** Other systems that interact

**Questions to identify actors:**
- Who will use this system?
- What external systems connect?
- Who maintains the system?
- Who receives output?

### Step 2: Identify Use Cases

What do actors do with the system?

**For each actor, ask:**
- What tasks do they perform?
- What information do they need?
- What do they create or change?
- What events trigger their actions?

**Use case naming:** Verb + Noun
- "Place Order"
- "Generate Report"
- "Manage User Account"

### Step 3: Create Use Case Diagram

Visualize actors and use cases:

```
+----------------------------------+
|           System                 |
|  +-------------------------+     |
|  |  Use Case 1            |     |
|  +-------------------------+     |
|                                  |
|  +-------------------------+     |
Actor ---| Use Case 2            |     |
|  +-------------------------+     |
|                                  |
|  +-------------------------+     |
|  |  Use Case 3            |---- External System
|  +-------------------------+     |
+----------------------------------+
```

### Step 4: Write Use Case Specifications

Document each use case in detail:

**Essential elements:**
- Name and ID
- Description
- Actors
- Preconditions
- Main flow (happy path)
- Alternative flows
- Exception flows
- Postconditions
- Business rules

### Step 5: Validate Use Cases

Review with stakeholders:
- Are all actor goals covered?
- Is the main flow correct?
- Are alternatives complete?
- Are exceptions handled?

---

## Templates

### Use Case Specification Template

```markdown
# Use Case: [UC-XXX] [Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]
**Status:** [Draft/Review/Approved]

## Overview

**ID:** UC-[XXX]
**Name:** [Verb + Noun]
**Description:** [Brief description of what this use case accomplishes]
**Primary Actor:** [Actor name]
**Secondary Actors:** [Other actors involved]

## Preconditions
- [Condition that must be true before use case starts]
- [Another precondition]

## Postconditions
**Success:**
- [Condition that is true after successful completion]

**Failure:**
- [Condition that is true if use case fails]

## Triggers
- [What initiates this use case]

## Main Flow (Happy Path)

| Step | Actor Action | System Response |
|------|--------------|-----------------|
| 1 | [Actor does X] | [System does Y] |
| 2 | [Actor does X] | [System does Y] |
| 3 | [Actor does X] | [System does Y] |

## Alternative Flows

### AF-1: [Alternative Name]
**Trigger:** At step [X], [condition]
| Step | Actor Action | System Response |
|------|--------------|-----------------|
| 1a | [Action] | [Response] |

**Return:** [Where flow returns to main flow]

### AF-2: [Alternative Name]
[Same structure]

## Exception Flows

### EX-1: [Exception Name]
**Trigger:** At step [X], [error condition]
| Step | System Response |
|------|-----------------|
| 1 | [Error handling] |

**End State:** [How use case ends]

## Business Rules
- BR-[X]: [Business rule that applies]
- BR-[Y]: [Another business rule]

## Related Use Cases
- [UC-XXX]: [Relationship - includes/extends/related]

## Non-Functional Requirements
- [Performance, security, or other requirements]

## Notes
[Additional information]
```

### Use Case Diagram Template

```markdown
# Use Case Diagram: [System Name]

## Actors
- [Actor 1]: [Description]
- [Actor 2]: [Description]

## Use Cases

### Actor 1
- UC-001: [Use Case Name]
- UC-002: [Use Case Name]

### Actor 2
- UC-003: [Use Case Name]
- UC-004: [Use Case Name]

### Shared
- UC-005: [Use Case Name] - [Actors 1 and 2]

## Relationships
- UC-001 <<includes>> UC-010 (Login)
- UC-002 <<extends>> UC-001 (Optional: Apply Discount)
```

---

## Examples

### Example 1: Place Order Use Case

**UC-101: Place Order**

**Primary Actor:** Customer
**Description:** Customer places an order for products in their shopping cart.

**Preconditions:**
- Customer is logged in
- Shopping cart has at least one item

**Main Flow:**

| Step | Actor Action | System Response |
|------|--------------|-----------------|
| 1 | Customer clicks "Checkout" | System displays order summary |
| 2 | Customer confirms shipping address | System calculates shipping cost |
| 3 | Customer selects payment method | System displays payment form |
| 4 | Customer enters payment details | System validates payment |
| 5 | Customer clicks "Place Order" | System creates order and sends confirmation |

**Alternative Flows:**

**AF-1: New Shipping Address**
At step 2, customer enters new address.
System validates and saves new address.
Return to step 2.

**Exception Flows:**

**EX-1: Payment Declined**
At step 4, payment validation fails.
System displays error message.
Customer can retry or select different payment.

**Postconditions:**
- Order is created with status "Confirmed"
- Inventory is reduced
- Confirmation email sent

### Example 2: Use Case Diagram

```
+------------------------------------------------+
|              E-Commerce System                 |
|                                                |
|    +------------------+                        |
|    | Browse Products  |                        |
|    +------------------+                        |
|            |                                   |
|    +------------------+                        |
Customer---| Place Order     |                        |
|    +------------------+                        |
|            |  <<includes>>                     |
|    +------------------+                        |
|    | Process Payment  |--- Payment Gateway    |
|    +------------------+                        |
|                                                |
|    +------------------+                        |
Admin ---| Manage Inventory |                        |
|    +------------------+                        |
|                                                |
+------------------------------------------------+
```

---

## Common Mistakes

1. **Feature as use case** - "Display screen" is not a use case
2. **Missing actors** - Forgetting system actors
3. **No exceptions** - Only happy path documented
4. **Too detailed** - Including UI details in use case
5. **Too abstract** - "Use system" is too vague

---

## Use Case Relationships

| Relationship | Meaning | Example |
|--------------|---------|---------|
| **Include** | Always uses another use case | Place Order includes Process Payment |
| **Extend** | Optionally adds behavior | Place Order extended by Apply Coupon |
| **Generalization** | Specialized version | Pay with Credit Card generalizes Pay |

---

## Use Case Quality Checklist

- [ ] Each use case has clear actor
- [ ] Use case name is verb + noun
- [ ] Preconditions are verifiable
- [ ] Main flow achieves actor goal
- [ ] Alternative flows documented
- [ ] Exceptions handled
- [ ] Postconditions defined
- [ ] Business rules referenced
- [ ] Reviewed by stakeholders

---

## Next Steps

After use case modeling:
1. Validate with stakeholders
2. Use for test case creation
3. Input for UI design
4. Guide development
5. Connect to User Story Mapping methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Use Case Modeling Guidelines
