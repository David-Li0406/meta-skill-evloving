# Draft Template

```markdown
═══════════════════════════════════════════════════════════════════
Pull Request Draft
═══════════════════════════════════════════════════════════════════

Title: Add user authentication with OAuth 2.0

Branch: feat-auth → main

─────────────────────────────────────────────────────────────────────

## Summary

Adds user authentication using OAuth 2.0, supporting GitHub and Google
providers. Includes login/logout flows, session management, and profile access.

## What Changed

### Key Features
- OAuth 2.0 integration with GitHub and Google
- Secure session management with httpOnly cookies
- User profile endpoint with auth middleware

### Files Modified
- `src/auth/oauth.py`: OAuth provider implementation
- `src/auth/middleware.py`: Auth middleware
- `src/api/routes.py`: Login/logout/profile endpoints

## Technical Approach

Chose OAuth 2.0 over JWT-based auth for better security and simpler
implementation. OAuth handles token refresh automatically and provides
better user experience with provider-managed consent screens.

## Implementation Details

### Phase 1: OAuth Integration
- ✅ Implement OAuth provider classes
- ✅ Add callback URL handling
- ✅ Store tokens securely

### Phase 2: Session Management
- ✅ Create session middleware
- ✅ Implement logout functionality

## Testing

- Added 15 unit tests for OAuth providers
- Verified login/logout flows manually
- Tested with both GitHub and Google accounts

## Spec Reference

- Spec: `specs/completed/<spec-id>.json`

## Commits

- abc1234: task-1-1: Implement OAuth providers
- def5678: task-1-2: Add session middleware
- ghi9012: task-2-1: Create profile endpoint

─────────────────────────────────────────────────────────────────────
```
