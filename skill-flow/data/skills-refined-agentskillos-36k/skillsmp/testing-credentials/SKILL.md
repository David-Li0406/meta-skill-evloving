---
name: Testing Credentials
description: Saved test account for real-time E2E verification
---

# Testing Credentials

## Primary Test Account
Use this account for all real-time E2E testing of authentication, session persistence, and user flows.

```
Email: Daniel@bekavactrading.com
Password: Bek454545!!
```

## Usage
When running browser E2E tests that require authentication:
1. Navigate to https://smarter.poker/auth/login
2. Enter email: Daniel@bekavactrading.com
3. Enter password: Bek454545!!
4. Click login button
5. Verify session persists across navigation

## Test Scenarios
- Auth handshake verification
- Session persistence across pages
- AbortError monitoring
- Cross-orb navigation (Hub → Training → Social → back)
