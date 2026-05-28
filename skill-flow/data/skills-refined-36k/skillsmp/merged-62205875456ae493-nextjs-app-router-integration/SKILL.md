---
name: nextjs-app-router-integration
description: Use this skill to integrate PostHog analytics into Next.js App Router applications.
---

# PostHog Integration for Next.js App Router

This skill helps you add PostHog analytics to Next.js App Router applications.

## Workflow

Follow these steps in order to complete the integration:

1. `basic-integration-1.0-begin.md` - PostHog Setup - Begin ← **Start here**
2. `basic-integration-1.1-edit.md` - PostHog Setup - Edit
3. `basic-integration-1.2-revise.md` - PostHog Setup - Revise
4. `basic-integration-1.3-conclude.md` - PostHog Setup - Conclusion

## Reference Files

- `EXAMPLE.md` - Next.js App Router example project code
- `next-js.md` - Next.js documentation
- `identify-users.md` - Identify users documentation
- `basic-integration-1.0-begin.md` - PostHog setup - begin
- `basic-integration-1.1-edit.md` - PostHog setup - edit
- `basic-integration-1.2-revise.md` - PostHog setup - revise
- `basic-integration-1.3-conclude.md` - PostHog setup - conclusion

The example project shows the target implementation pattern. Consult the documentation for API details.

## Key Principles

- **Environment Variables**: Always use environment variables for PostHog keys. Never hardcode them.
- **Minimal Changes**: Add PostHog code alongside existing integrations. Don't replace or restructure existing code.
- **Match the Example**: Your implementation should follow the example project's patterns as closely as possible.

## Framework Guidelines

- Never use `useEffect()` for analytics capture; it's brittle and causes errors.
- Prefer event handlers or routing mechanisms to trigger analytics calls.
- Add handlers where user actions occur rather than reacting to state changes.
- Remember that source code is available in the `node_modules` directory.
- Check `package.json` for type checking or build scripts to validate changes.
- Use `posthog-js` as the JavaScript SDK package name.

## Identifying Users

Identify users during login and signup events. Refer to the example code and documentation for the correct identify pattern for this framework. If both frontend and backend code exist, pass the client-side session and distinct ID using `X-POSTHOG-DISTINCT-ID` and `X-POSTHOG-SESSION-ID` headers to maintain correlation.

## Error Tracking

Add PostHog error tracking to relevant files, particularly around critical user flows and API boundaries.