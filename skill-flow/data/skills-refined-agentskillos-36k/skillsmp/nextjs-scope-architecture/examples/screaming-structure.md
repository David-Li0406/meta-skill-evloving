# Example: Screaming App Structure (Next.js 15+)

This example shows a Next.js application where the folder hierarchy clearly communicates **business intent**.

## Principles demonstrated

* App Router only
* Feature-based route groups
* Private folders for feature internals
* Shared code only when used by multiple features

---

## Folder structure

```txt
src/
  app/
    (auth)/
      login/
        page.tsx
        _components/
          login-form.tsx
      register/
        page.tsx
        _components/
          register-form.tsx
      _components/
        social-login.tsx
      _actions/
        auth-actions.ts
      layout.tsx

    (dashboard)/
      dashboard/
        page.tsx
        loading.tsx
        _components/
          stats-card.tsx
      profile/
        page.tsx
        _components/
          profile-form.tsx
      layout.tsx

  shared/
    components/
      ui/
        button.tsx
        card.tsx
```

---

## Why this is correct

* `social-login.tsx` is shared **only inside `(auth)`** → remains a private feature component
* `button.tsx` and `card.tsx` are used across multiple features → promoted to `shared/`
* No technical folders (`components`, `hooks`, `utils`) at the root of `app/`
* Route groups clearly express **business domains**, not implementation details

---

## What this avoids

* God `shared/` folders
* Premature abstraction
* Unclear ownership
* Client-side bloat at the root level
