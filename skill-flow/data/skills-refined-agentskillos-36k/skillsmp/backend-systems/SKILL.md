---
name: backend-systems
description: Security and architecture rules for Node.js and Firebase Cloud Functions. Use when modifying API endpoints or triggers.
---

# Backend Systems

Detailed instructions for Node.js, Express, and Firebase Cloud Functions.

## When to use this skill

- Use this when modifying `functions/src/` or `server/src/`.
- This is helpful for creating new API endpoints, HTTP triggers, or background jobs.
- Use this when debugging server logs or permission errors.

## How to use it

### 1. Security First
- **Validation**: All endpoints must validate inputs (e.g., using `zod` or explicit checks).
- **Authentication**: Check `req.user` for authentication state before proceeding.
- **Authorization**: Explicitly check roles (e.g., `user.role === 'owner'`) for admin actions.

### 2. Architecture
- **Service Layer**: Business logic belongs in `services/`, not controllers/routers.
- **Types**: Always import shared types from `src/types` to ensure frontend/backend parity.
- **Region**: All resources must be in `us-west1`.

### 3. Error Handling
- Use `console.error` for exceptions (Google Cloud Error Reporting picks this up).
- Return structured JSON errors: `{ error: string, code: string }`.
