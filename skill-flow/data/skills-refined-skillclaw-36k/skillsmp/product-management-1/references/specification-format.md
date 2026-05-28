# Specification Format

## Template

```markdown
# Feature: [Clear, business-focused title]

## Context

[Summary of codebase investigation - what exists, what patterns to follow]

## Complexity Assessment

| Factor           | Score    | Notes          |
| ---------------- | -------- | -------------- |
| Files affected   | X/3      | [which files]  |
| New dependencies | X/3      | [which deps]   |
| Database changes | X/3      | [what changes] |
| External APIs    | X/3      | [which APIs]   |
| Business logic   | X/3      | [complexity]   |
| Risk level       | X/3      | [why]          |
| **Total**        | **X/18** |                |

**Workflow**: [Simple | Medium | Complex]
**Parallel Execution**: [Yes/No - if yes, describe split]

## User Story

As a [user type]
I want to [capability]
So that [business value]

## MVP Scope

**In Scope:**

- [Essential capability 1]
- [Essential capability 2]

**Deferred:**

- [Nice-to-have 1] → Future iteration
- [Nice-to-have 2] → Future iteration

## Acceptance Criteria

### Scenario: [Happy path use case]

Given [initial context/state]
When [action/trigger]
Then [expected outcome]
And [additional outcomes if needed]

### Scenario: [Edge case]

Given [different context]
When [problematic action]
Then [graceful handling]

### Scenario: [Error condition]

Given [context leading to failure]
When [invalid action]
Then [appropriate error response]

## Non-Functional Requirements

- Performance: [specific, measurable criteria]
- Security: [specific requirements]
- UX: [specific expectations]

## Technical Notes

[Observations from codebase investigation relevant to implementation]

## Implementation Plan

[Only for parallel execution or complex features]

- [ ] Part 1: [description] → specs/[feature]-part1.md
- [ ] Part 2: [description] → specs/[feature]-part2.md

## Success Metrics

- [Measurable outcome 1]
- [Measurable outcome 2]

## Open Questions

- [Any unresolved items requiring user input]
```

---

## Section Guidelines

### Context

Document what you discovered during codebase investigation:

```markdown
## Context

The application uses Laravel 11 with PostgreSQL. Existing user management
lives in `app/Http/Controllers/UserController.php` with Eloquent models
in `app/Models/User.php`. Authentication uses Laravel Sanctum.

Current patterns:

- Form Requests for validation
- Service classes for business logic
- Repository pattern for complex queries
```

### Complexity Assessment

**Always score before deciding workflow:**

```markdown
## Complexity Assessment

| Factor           | Score    | Notes                                          |
| ---------------- | -------- | ---------------------------------------------- |
| Files affected   | 2/3      | Controller, Service, Model, Migration, 2 Views |
| New dependencies | 1/3      | None needed                                    |
| Database changes | 2/3      | New `preferences` table with FK to users       |
| External APIs    | 1/3      | None                                           |
| Business logic   | 2/3      | Validation rules, default handling             |
| Risk level       | 1/3      | Low - isolated feature                         |
| **Total**        | **9/18** |                                                |

**Workflow**: Medium (Coder → QA)
**Parallel Execution**: No - tightly coupled
```

**For parallel execution:**

```markdown
## Complexity Assessment

| Factor           | Score     | Notes                             |
| ---------------- | --------- | --------------------------------- |
| Files affected   | 3/3       | 4 API files + 5 React components  |
| New dependencies | 2/3       | react-dropzone (frontend only)    |
| Database changes | 2/3       | New `documents` table             |
| External APIs    | 2/3       | AWS S3 integration                |
| Business logic   | 2/3       | Upload validation, access control |
| Risk level       | 2/3       | Medium - file handling            |
| **Total**        | **13/18** |                                   |

**Workflow**: Complex (Feature-Refiner → Coder → QA)
**Parallel Execution**: Yes

- API/Backend: S3 service, upload endpoints, migrations
- UI/Frontend: Upload component, document list, progress UI
```

### User Story

Keep it focused on a single user goal:

**Good:**

```
As a team admin
I want to invite new members via email
So that I can grow my team without manual account creation
```

**Bad (too many goals):**

```
As a team admin
I want to invite members, manage roles, and configure permissions
So that I can fully administer my team
```

### MVP Scope

Be explicit about what's in and out:

```markdown
## MVP Scope

**In Scope:**

- Send email invitation with unique link
- Accept invitation via link
- Basic rate limiting (10 invites/hour)

**Deferred:**

- Bulk invite from CSV → v2
- Custom invitation message → v2
- Invitation expiry configuration → v2
- Invitation templates → Future
```

### Acceptance Criteria

#### Happy Path

```gherkin
Scenario: User successfully invites team member
Given I am logged in as a team admin
And I have remaining invitation quota
When I enter a valid email address and click "Send Invite"
Then an invitation email is sent to that address
And the invitation appears in my "Pending Invitations" list
And my remaining quota decreases by 1
```

#### Edge Cases

```gherkin
Scenario: User invites already-existing member
Given I am logged in as a team admin
And john@example.com is already a team member
When I try to invite john@example.com
Then I see "This user is already a member of your team"
And no invitation is sent
```

#### Error Conditions

```gherkin
Scenario: User exceeds invitation rate limit
Given I am logged in as a team admin
And I have sent 10 invitations in the past hour
When I try to send another invitation
Then I see "Rate limit exceeded. Try again in X minutes"
And the invitation form is disabled
```

### Non-Functional Requirements

**Good (measurable):**

```markdown
- Performance: Invitation API responds in <200ms p95
- Security: Invitation tokens expire after 7 days
- Security: Rate limit: 10 invitations per hour per admin
- UX: Email delivered within 30 seconds of request
```

**Bad (vague):**

```markdown
- Performance: Should be fast
- Security: Should be secure
- UX: Should be user-friendly
```

### Technical Notes

Reference actual codebase findings:

```markdown
## Technical Notes

- Use existing `EmailService` in `app/Services/EmailService.php`
- Follow pattern in `app/Models/Invite.php` (similar structure)
- Rate limiting via existing `RateLimiter` middleware
- Database migrations follow existing Laravel pattern
```

### Implementation Plan

**Only for complex/parallel features:**

```markdown
## Implementation Plan

### Part 1: Backend/API (specs/invites-api.md)

- [ ] Create Invite model and migration
- [ ] InviteService with send/accept logic
- [ ] API endpoints: POST /invites, GET /invites/:token
- [ ] Rate limiting middleware

### Part 2: Frontend/UI (specs/invites-ui.md)

- [ ] InviteForm component
- [ ] PendingInvites list
- [ ] Accept invitation page
- [ ] Success/error notifications

**Execution**: Parallel (no shared state until integration)
```

### Success Metrics

```markdown
## Success Metrics

- 80% of invitations accepted within 48 hours
- <1% invitation delivery failures
- Zero security incidents related to invitation tokens
- Admin can invite 5 users in under 2 minutes
```

### Open Questions

```markdown
## Open Questions

- Should invitations expire? If so, after how long?
- Can non-admins invite? (Currently assuming no)
- Should we notify admin when invitation is accepted?
```

---

## Writing Good Scenarios

### Be Specific

```gherkin
# Bad
Given a user
When they do something
Then it works

# Good
Given I am logged in as a team admin with "manage_members" permission
When I submit the invitation form with email "new@example.com"
Then a POST request is sent to /api/invitations
And the response status is 201 Created
And the response includes the invitation ID
```

### Cover State Transitions

```gherkin
Scenario: Invitation state changes on accept
Given an invitation exists for "user@example.com" with status "pending"
When the user clicks the invitation link
And completes the signup form
Then the invitation status changes to "accepted"
And a new user account is created
And the user is added to the team
```

### Include Validation Rules

```gherkin
Scenario: Email validation rules
Given I am on the invitation form
When I enter an email with these characteristics:
  | Input           | Result  |
  | user@domain.com | Valid   |
  | user@domain     | Invalid |
  | @domain.com     | Invalid |
Then validation feedback appears inline
```

---

## Sub-Spec Template (for Parallel Execution)

When splitting a feature for parallel execution, create sub-specs:

```markdown
# Feature: [Parent Feature] - [Part Name]

## Parent Spec

See: specs/[parent-feature].md

## Scope (This Part Only)

- [What this part covers]
- [Boundaries with other parts]

## Integration Points

- Depends on: [nothing | other part]
- Provides: [what other parts need from this]

## Acceptance Criteria

[Only criteria relevant to this part]

## Technical Notes

[Part-specific notes]
```
