# Trunk-Based Development: High-Velocity Engineering (2026)

Trunk-Based Development (TBD) is the preferred workflow for elite agile teams in 2026. It focuses on small, frequent merges to a single `main` branch to minimize integration hell.

## 1. Core Principles

-   **Short-Lived Branches**: Branches should exist for hours, not days.
-   **Continuous Integration**: Code is merged to `main` at least once a day.
-   **Feature Flags**: Incomplete features are merged behind flags to keep `main` always deployable.

## 2. The TBD Workflow

1.  **Pull**: Always start with `git pull --rebase origin main`.
2.  **Branch**: Create a tiny branch: `git checkout -b fix/auth-header`.
3.  **Code**: Implement the change and add tests.
4.  **Validate**: Run `bun x tsc --noEmit` and `bun test`.
5.  **Merge**: Push and merge immediately after PR approval.

## 3. Managing Incomplete Work (Feature Flags)

Instead of long-lived "Feature Branches," use flags:

```typescript
if (flags.isEnabled('new-checkout-flow')) {
  return <NewCheckout />;
}
return <LegacyCheckout />;
```

This allows you to merge the `NewCheckout` code into `main` safely while it's still in progress.

## 4. When to Use TBD

-   **Small to Mid-sized Teams**: Fast communication and high trust.
-   **Microservices**: Isolated domains where breaking changes have a limited blast radius.
-   **SaaS Products**: Environments requiring multiple deployments per day.

## 5. Anti-Patterns

-   **Merging Broken Code**: TBD requires 100% test pass rate on `main`.
-   **Large PRs**: Defeats the purpose of rapid integration.
-   **Ignoring the Build**: A red `main` branch must be the team's #1 priority to fix.

---
*Updated: January 22, 2026 - 18:55*
