# User Story Format Reference

## Template

```markdown
# US-XXX: [Story Title]

## User Story

As a [user type],
I want [goal],
So that [benefit].

## Context

[Background information, related stories, dependencies]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes

[Any technical considerations, constraints, or recommendations]

## Edge Cases

- [ ] Edge case 1: [Expected behavior]
- [ ] Edge case 2: [Expected behavior]

## Out of Scope

- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## UI/UX Notes

[Wireframes, mockups, or design references]

## Testing Notes

[Specific testing considerations]
```

## Example: Complete User Story

```markdown
# US-007: User Login

## User Story

As a registered user,
I want to log in with my email and password,
So that I can access my personal dashboard.

## Context

This is part of the authentication epic. Depends on US-001 (User Registration).
Must work with the existing session management system.

## Acceptance Criteria

- [ ] User can enter email and password
- [ ] Valid credentials redirect to dashboard
- [ ] Invalid credentials show error message
- [ ] "Remember me" option extends session to 30 days
- [ ] Forgot password link navigates to reset flow
- [ ] Login button shows loading state during authentication
- [ ] Form validates email format before submission

## Technical Notes

- Use JWT tokens stored in httpOnly cookies
- Rate limit to 5 attempts per minute per IP
- Log failed attempts for security monitoring

## Edge Cases

- [ ] Empty email: Show "Email is required" error
- [ ] Empty password: Show "Password is required" error
- [ ] Invalid email format: Show "Enter a valid email" error
- [ ] Account locked: Show "Account locked, contact support" message
- [ ] Network error: Show "Unable to connect, try again" message

## Out of Scope

- Social login (OAuth) - separate story US-012
- Two-factor authentication - separate story US-015
- Password strength indicator - separate story US-008

## UI/UX Notes

- Center form on page
- Max width 400px
- Show/hide password toggle
- Auto-focus email field on load

## Testing Notes

- Test with valid/invalid credentials
- Test rate limiting behavior
- Test "remember me" session duration
- Test accessibility with screen reader
```
