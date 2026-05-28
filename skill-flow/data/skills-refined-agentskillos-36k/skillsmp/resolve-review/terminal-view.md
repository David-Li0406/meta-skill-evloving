# Terminal View

How Items are rendered during the CC session.

## Item List (After File Generation)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENERATED 5 items → <tmp>/owner-repo/123/2026-01-16/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
01-null-check-missing.md     2 threads  @copilot
02-type-cast-needed.md       1 thread   @copilot
03-aria-labels.md            3 threads  @copilot
04-loading-state.md          comment    @reviewer  part 1/2
05-error-handling.md         comment    @reviewer  part 2/2

Open in editor, modify responses, then: /resolve-review --apply
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Columns:

- Filename
- Count: `N threads` or `comment`
- Authors
- Part indicator (comment-parts only)

## Single Item (Detailed View)

### Thread Item

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITEM 1 of 5 (2 threads)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Author: @copilot
File: src/user.ts:45
URL: https://github.com/owner/repo/pull/123#discussion_r456

Comment:
> The `user.name` property is accessed without checking
> if `user` is defined. This could cause a runtime error.

Diff context:
@@ -42,6 +42,8 @@
   const name = user.name;

─── Also in this item ────────────────────────────────────────────
File: src/user.ts:52
URL: https://github.com/owner/repo/pull/123#discussion_r789

Comment:
> Same pattern on line 52 with `user.email`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

─── Analysis ──────────────────────────────────────────────────────
ADDRESS
  reason:   Valid - null check is missing before property access
  response: Fix both locations, resolve with thumbs up
───────────────────────────────────────────────────────────────────
```

Header format:

- `ITEM N of M` always
- `(K threads)` only if item has multiple grouped threads

### Comment-Part Item

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITEM 4 of 5                                        COMMENT · part 1/2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Author: @reviewer
URL: https://github.com/owner/repo/pull/123#issuecomment-456

Full comment:
> Can we add a loading state? Also the error handling
> seems incomplete.

This part:
> Can we add a loading state?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

─── Analysis ──────────────────────────────────────────────────────
ADDRESS
  reason:   Valid - no loading indicator during async operation
  response: Add loading state, resolve comment when all parts done
───────────────────────────────────────────────────────────────────
```

Header badge: `COMMENT · part N/M` right-aligned

### Warnings

If `outdated: true`:

```
⚠️  OUTDATED: This thread may reference code that has changed.
```

If feedback contains GitHub suggestion block:

```
📝 Contains code suggestion - can be applied directly if approved.
```

## Analysis Block

```
─── Analysis ──────────────────────────────────────────────────────
<ACTION>
  reason:   <why this action>
  evidence: <commits, policies, code refs - if applicable>
  response: <what happens on GitHub>
  note:     <caveats, follow-up ideas - if applicable>
───────────────────────────────────────────────────────────────────
```

Omit fields with no value.

## Summary (After Apply)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY                                          5 items → 7 threads
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

─── CLOSED (6 threads) ───────────────────────────────────────────

#1  ADDRESSED  @copilot
    ├─ "Null check missing on user.name"
    │   https://github.com/owner/repo/pull/123#discussion_r456
    └─ "Same pattern on line 52"
        https://github.com/owner/repo/pull/123#discussion_r789

    > Added null checks before property access.

#2  DISMISSED  @copilot
    ├─ "aria-label for filter button"
    ├─ "aria-label for dropdown"
    └─ "ARIA menu roles"

    > Out of scope - accessibility strategy pending.

─── REMAINS OPEN (1 thread) ──────────────────────────────────────

#3  DEFERRED  @reviewer
    └─ "Complex refactor needed"
        https://github.com/owner/repo/pull/123#discussion_r999

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Tree connectors: `├─` / `└─` / `│`

## Box Drawing Reference

| Element          | Character |
| ---------------- | --------- |
| Heavy horizontal | `━`       |
| Light horizontal | `─`       |
| Tree branch      | `├─`      |
| Tree end         | `└─`      |
| Tree vertical    | `│`       |
