---
name: documentation-generator
description: Use this skill to generate comprehensive documentation from code, APIs, and specifications, including API docs, developer guides, architecture documentation, and user manuals.
---

# Documentation Generator Skill

## Purpose

This skill generates various types of documentation artifacts from implemented code, ensuring that the documentation is comprehensive, user-focused, and aligned with best practices.

## When to Use

### Highly Recommended
- **Public API additions**: New endpoints, methods, or interfaces
- **User-facing features**: Features end users will interact with
- **Substantial changes**: Multi-file implementations, new services
- **Complex logic**: Non-obvious algorithms or workflows
- **Configuration options**: New environment variables or settings

### Optional
- Internal refactoring (no API changes)
- Bug fixes (unless they change documented behavior)
- Test-only changes
- Minor UI tweaks

### Skip
- Documentation-only changes (already documented)
- Trivial single-line fixes

## Documentation Types

### API Documentation
For public endpoints and methods:

```markdown
## methodName

Brief description of what it does.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | What this parameter controls |

### Returns

`ReturnType` - Description of return value

### Errors

| Error | When |
|-------|-------|
| InvalidInputError | When param1 is empty |

### Example

\`\`\`typescript
const result = await service.methodName('value');
\`\`\`
```

### User Guides
For user-facing features:

```markdown
## Feature Name

What this feature does and why you'd use it.

### Getting Started

Step-by-step instructions for basic usage.

### Configuration

Available options and what they control.

### Examples

Common use cases with code/UI examples.

### Troubleshooting

Common issues and how to resolve them.
```

### Architecture Documentation
For complex systems:

```markdown
## Component Name

### Purpose

Why this component exists and what problem it solves.

### Design Decisions

Key decisions and their rationale.

### Data Flow

How data moves through the component.

### Dependencies

What this component depends on and why.
```

## Documentation Process

### Step 1: Identify Documentation Type
Determine documentation type:
- **API Documentation**: Endpoint references
- **Developer Guide**: Setup and usage
- **Architecture Docs**: System overview
- **User Manual**: Feature guides

### Step 2: Extract Information
Gather documentation content:
- Read code and comments
- Analyze API endpoints
- Extract examples
- Understand architecture

### Step 3: Generate Documentation
Create documentation:
- Follow documentation templates
- Include examples
- Add troubleshooting
- Create clear structure

### Step 4: Validate Documentation
Validate quality:
- Check completeness
- Verify examples work
- Ensure clarity
- Validate links

## Best Practices
1. **Extract from Code**: Use code as source of truth
2. **Include Examples**: Provide working examples
3. **Keep Updated**: Sync docs with code
4. **Clear Structure**: Organize logically
5. **User-Focused**: Write for users, not system

## Output Format
```markdown
## Documentation Complete

**Spec Group**: .claude/specs/groups/<spec-group-id>/

**Artifacts Created**:
- docs/api/services/auth.md (API reference)
- docs/guides/authentication.md (user guide)

**Coverage**:
- Public methods documented: 5/5
- Examples included: 3
- Error conditions documented: 4

**Validation**:
- Code examples: verified
- Links: verified
- Formatting: consistent
```

## Integration with Other Skills
- Uses this skill for documentation generation
- Ensures documentation quality
- Validates completeness

## Constraints
- Document what the code DOES, not what the spec SAYS.
- No code changes; only generate documentation.

## Examples

### Example 1: API Documentation
**Input**: New logout endpoint implementation

**Output**:
```markdown
# AuthService.logout()

Terminates the current user session and clears authentication state.

## Signature

\`\`\`typescript
async logout(): Promise<void>
\`\`\`

## Behavior

1. Calls server to invalidate session
2. Clears local authentication token
3. Updates auth state to unauthenticated
4. Triggers redirect to login page

## Errors

| Error | Cause |
|-------|-------|
| `NetworkError` | Cannot reach server |
| `LogoutError` | Server rejected logout |

## Example

\`\`\`typescript
import { authService } from '@/services/auth';

try {
  await authService.logout();
  // User is now logged out, redirect handled automatically
} catch (error) {
  if (error instanceof NetworkError) {
    showToast('Check your connection and try again');
  }
}
\`\`\`
```

### Example 2: User Guide
**Input**: New dashboard feature

**Output**:
```markdown
# Using the Dashboard

The dashboard provides an overview of your daily tasks and priorities.

## Getting Started

1. Log in to your account
2. Click "Dashboard" in the navigation menu
3. Your daily briefing appears automatically

## Features

### Daily Briefing
Shows your priorities for today, including:
- Urgent emails requiring response
- Upcoming calendar events
- Tasks due today

### Quick Actions
- **Snooze**: Postpone an item to later
- **Complete**: Mark a task as done
- **Delegate**: Assign to someone else

## Customization

Access Settings → Dashboard to configure:
- Briefing time (default: 9:00 AM)
- Priority thresholds
- Notification preferences
```

### Example 3: Architecture Doc
**Input**: New notification service

**Output**:
```markdown
# Notification Service Architecture

## Purpose

Centralizes all user notifications across channels (email, SMS, push).

## Design Decisions

**Why a separate service?**
- Decouples notification logic from business logic
- Enables channel-agnostic notification requests
- Supports future channels without core changes

**Why queue-based?**
- Handles burst traffic gracefully
- Enables retry logic for failed deliveries
- Provides delivery tracking

## Data Flow

\`\`\`
Business Logic → NotificationService.send()
                         ↓
                   Queue (Redis)
                         ↓
              Channel Adapters (Email, SMS, Push)
                         ↓
                 Delivery Status → Database
\`\`\`

## Dependencies

- **Redis**: Message queue
- **Telnyx**: SMS delivery
- **SendGrid**: Email delivery
- **Firebase**: Push notifications
```