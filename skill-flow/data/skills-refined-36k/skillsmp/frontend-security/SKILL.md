---
name: "frontend-security"
paths: "**/frontend/**/*.{ts,tsx}"
alwaysApply: false
description: Security guidelines for frontend code. Covers token storage, XSS prevention, authorization, and secure coding practices. CRITICAL INSTRUCTION You MUST ALWAYS use this skill before editing/writing any file matching "**/frontend/**/*.{ts,tsx}".
---

# Frontend Security Rules

## CRITICAL: Token Storage

**NEVER store tokens in localStorage or memory.** Tokens are managed via HTTP-only cookies and sent automatically by the browser.

```ts
// ❌ FORBIDDEN
localStorage.setItem("token", jwt);
sessionStorage.setItem("token", jwt);
const token = "Bearer " + jwt;

// ✅ CORRECT: Cookies handle token transport automatically
// No token management code needed in frontend
```

## CRITICAL: XSS Prevention

**NEVER use `innerHTML` with untrusted content.** Use framework bindings instead.

```ts
// ❌ FORBIDDEN
element.innerHTML = userInput;
this.renderer.setProperty(el, "innerHTML", data);

// ✅ CORRECT: Angular/React sanitizes automatically
<div>{userInput}</div>
<div [textContent]="userInput"></div>
```

## Authorization

**Guards are client-side only.** Always enforce permissions on the backend.

### Route Guards

Use route guards to control access to pages:

```ts
// ✅ Admin-only route
{
  path: 'admin',
  canActivate: [authenticatedGuard, roleGuard],
  data: { roles: ['admin'] }
}

// ✅ Multiple roles
{
  path: 'profile',
  canActivate: [authenticatedGuard, roleGuard],
  data: { roles: ['admin', 'user'] }
}

// ✅ Public routes: no guards
{ path: 'login', component: LoginComponent }
```

### UI Role-Based Visibility

**Hide unauthorized elements - never disable them.** Users should not see actions they cannot perform.

```ts
// ✅ CORRECT: Hide unauthorized actions
<button *ngIf="isAdmin()" (click)="deleteUser()">
  Delete User
</button>

// ❌ WRONG: Showing disabled button
<button [disabled]="!isAdmin()">Delete</button>
```

## External Links

**ALWAYS use `rel="noopener noreferrer"` with `target="_blank"`.**

```html
<!-- ❌ WRONG -->
<a href="https://external.com" target="_blank">Link</a>

<!-- ✅ CORRECT -->
<a href="https://external.com" target="_blank" rel="noopener noreferrer"
  >Link</a
>
```

## Input Validation

- **Validate** all user input before use
- **Sanitize** HTML content from untrusted sources
- Use **strict typing** for all API inputs/outputs
- **Mask** sensitive data before logging

## Error Handling

- Distinguish **technical** vs **business** errors
- **NEVER** expose raw HTTP errors or stack traces to the UI
- Show **minimal, user-friendly** error messages
- Use a **logging service** for error reporting (redact tokens, PII, and credentials)

**Remember**: UI security is for UX only. **Backend must always enforce all security rules.**
