---
name: jira
description: Guidelines for creating and managing Jira tickets in the Greenhouse organization. Use when working with jira tickets, breaking down large tasks into sub-tasks, writing acceptance criteria, or setting Jira custom fields.
---

# Jira Ticket management

cloudId=28363aa1-5a3e-4e70-9ca4-7b347c22f288
projectIdOrKey=GREEN

## Overall approach

### Ticket Creation and modification Process

_ALWAYS_ show a diff and ask for confirmation before making changes.

#### 1. Initial Information Gathering
When asked to create a Jira ticket, I will:
- Start with a high-level understanding of the request
- Identify the core functionality or change needed
- Determine the affected systems or components
- Determine whether I have enough information to come up with BDD scenarios 

When asked to modify a Jira ticket, I will:
- Fetch the ticket first to get context
- Idntify the core functionality in the existing ticket
- Determine the affected systems or components requested in the modification

### Large Task Breakdown

For large tasks:

1. Propose a plan to break it down into smaller, releasable sub-tasks
2. Create each sub-task as a separate Jira ticket

### Required Information

Always ask for:

- `project_key`
- `issue_type`
- `component` field

For assignee, clarify if it's a user, group, or custom field.

Link to the correct epic if information is available.

## Custom Fields

**GREEN Project Values:**

- Squad: `Post-Hire Ecosystem`

## Linking tickets

Sometimes the user will ask me to link jira cards together with "blocks" or "blocked by" relationships.

For these requests, the jira is not sufficient because it has not way to set these relationships.

### Establishing/updating links

Use the `jira` cli issuelink subcommand
usage: jira issuelink [<flags>] <OUTWARDISSUE> <ISSUELINKTYPE> <INWARDISSUE>

### Determining which link types exist

Use the `jira` cli issuelinktypes subcommand
usage: jira issuelinktypes 

## Templates

Replace placeholder values by collecting the necessary information.

### Epic

**Summary**
Sould be short, descriptive, and represent the changes being made

**Description Field**
Start with a 1-2 sentence elevator pitch for this work. Why does it matter?
_Example: Today, customers have to manually reconcile support tickets across three systems, costing 15+ hours per week. This Epic delivers automated ticket sync, eliminating manual work and reducing errors._

**Contexst**

Explain the greater context of why the change is being made and what value it will provide.

**Acceptance Criteria**
- [ ] Criterion 1 - [concrete, measurable outcome]
- [ ] Criterion 2 - [what can be demoed or validated]
- [ ] Criterion 3 - [business or technical acceptance gate]

** BDD ** 
```gherkin
Given [precondition]
When [action]
Then [expected result]
```

**Scope**

List the high-level capabilities in this milestone:
- [User type] can [action/capability] - [context or value]
- [System/Feature] does [behavior] when [condition]
- [Specific functionality or integration to deliver]
- [User-facing capability or technical enabler]
- [Another concrete deliverable]

**Out of Scope**
- [Feature/capability explicitly excluded]
- [Work deferred to future Epic]
- [Edge case not addressed in this increment]
Technical Considerations (OPTIONAL)

**Architecture/Design Approach:**
- [High-level technical approach or pattern]
- [Key architectural decisions]

**Non-Functional Requirements:**
- **Performance:** [specific target - e.g., "API response < 200ms"]
- **Security:** [requirements - e.g., "OAuth 2.0 authentication required"]
- **Scalability:** [target - e.g., "Support 10k concurrent users"]

**Technical Constraints:**
- [Platform limitation or constraint]
- [Technology stack requirement]

**Integration Points:**
- [System A integration via REST API]
- [System B data sync requirement]

Use Issue Links for Epic-to-Epic dependencies (blocks/is blocked by), or list other dependencies below:

Outstanding Questions (OPTIONAL)
- **Q:** [Question that needs resolution] - **Owner:** [name] - **Target Resolution:** [date]
- **Q:** [Question that needs resolution] - **Owner:** [name] - **Target Resolution:** [date]

---
 Notes
[Any additional context, links to Confluence pages, related documents, or discussion notes]

### Story

issueTypeId=10301

**Summary**
Sould be short, descriptive, and represent the changes being made

**Description Field**
Start with a 1-2 sentence elevator pitch for this work. Why does it matter?
_Example: Today, customers have to manually reconcile support tickets across three systems, costing 15+ hours per week. This Epic delivers automated ticket sync, eliminating manual work and reducing errors._

**Acceptance Criteria**
- [ ] Criterion 1 - [concrete, measurable outcome]
- [ ] Criterion 2 - [what can be demoed or validated]
- [ ] Criterion 3 - [business or technical acceptance gate]

**Non-Functional Requirements:**
- **Performance:** [specific target - e.g., "API response < 200ms"]
- **Security:** [requirements - e.g., "OAuth 2.0 authentication required"]
- **Scalability:** [target - e.g., "Support 10k concurrent users"]
- **Other:** [It's got to be done faster than usual]


Use Issue Links for Epic-to-Epic dependencies (blocks/is blocked by), or list other dependencies below:

Outstanding Questions (OPTIONAL)
- **Q:** [Question that needs resolution] - **Owner:** [name] - **Target Resolution:** [date]
- **Q:** [Question that needs resolution] - **Owner:** [name] - **Target Resolution:** [date]

---
 Notes
[Any additional context, links to Confluence pages, related documents, or discussion notes]

