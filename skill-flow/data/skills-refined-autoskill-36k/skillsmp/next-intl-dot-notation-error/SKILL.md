---
name: next-intl-dot-notation-error
description: |
  Fix "INVALID_KEY: Namespace keys can not contain the character '.'" error in next-intl.
  Use when: (1) Getting INVALID_KEY error with dots in translation keys, (2) Migrating from
  flat key structure to next-intl, (3) Keys like "email.notification.booking" failing,
  (4) Error message lists specific keys with dots as invalid. Solution: Convert flat keys
  with literal dots to nested object structure. Applies to Next.js i18n with next-intl library.
author: Claude Code
version: 1.0.0
date: 2026-01-23
---

# next-intl Dot Notation Error Fix

## Problem

next-intl throws `INVALID_KEY: Namespace keys can not contain the character "."` when
translation JSON files use dots as literal characters in key names instead of for object
nesting.

## Context / Trigger Conditions

**Exact error message:**
```
INVALID_KEY: Namespace keys can not contain the character "." as this is used to
express nesting. Please remove it or replace it with another character.

Invalid keys: email.notification.booking (at unsubscribe.categories), ...
```

**When this occurs:**
- Translation files use flat structure with dots in key names
- Keys like `"email.notification.booking": "Booking"` instead of nested objects
- Error appears when Next.js app starts or when loading translation namespace
- Typically happens at `getTranslations()` call or page metadata generation

**Common scenarios:**
- Migrating from other i18n libraries that allow literal dots
- Using preference keys or enum values as translation keys
- Trying to match database field names that contain dots

## Solution

Convert flat key structure to nested object structure. next-intl uses dot notation
**exclusively** for traversing nested objects—this is a fundamental design decision
and cannot be configured differently.

### Step-by-Step Fix

**Before (❌ Invalid):**
```json
{
  "unsubscribe": {
    "categories": {
      "email.notification.booking": "Booking",
      "email.notification.payment": "Payment",
      "email.notification.messaging": "Messaging"
    }
  }
}
```

**After (✅ Valid):**
```json
{
  "unsubscribe": {
    "categories": {
      "email": {
        "notification": {
          "booking": "Booking",
          "payment": "Payment",
          "messaging": "Messaging"
        }
      }
    }
  }
}
```

### Automated Conversion (Optional)

For large translation files, use lodash's `set` function to convert:

```javascript
import { set } from "lodash";

const flatInput = {
  "one.one": "1.1",
  "one.two": "1.2",
  "two.one.one": "2.1.1"
};

const nestedOutput = Object.entries(flatInput).reduce(
  (acc, [key, value]) => set(acc, key, value),
  {}
);

// Result:
// {
//   "one": { "one": "1.1", "two": "1.2" },
//   "two": { "one": { "one": "2.1.1" } }
// }
```

### Update Code References

If your code constructs translation keys dynamically, ensure they use dot notation
to access nested structure:

```typescript
// This still works - dot notation accesses nested objects
const categoryKey = `categories.${category}` as const;
// e.g., "categories.email.notification.booking"
const categoryName = t(categoryKey);
```

## Verification

1. **Dev server starts without error**: `npm run dev` succeeds
2. **Translations load**: `getTranslations({ locale, namespace: "..." })` works
3. **All language files updated**: Apply changes to all locale files (en.json, ar.json, etc.)
4. **Dynamic key access works**: Template strings like `t(\`categories.${category}\`)` resolve correctly

## Example

**Real-world scenario**: Email notification preferences with category keys

```json
// ❌ Before (causes error)
{
  "preferences": {
    "categories": {
      "email.notification.booking": "Booking Notifications",
      "email.notification.payment": "Payment Notifications"
    }
  }
}

// ✅ After (works correctly)
{
  "preferences": {
    "categories": {
      "email": {
        "notification": {
          "booking": "Booking Notifications",
          "payment": "Payment Notifications"
        }
      }
    }
  }
}

// Usage in component (unchanged)
const category = "email.notification.booking";
const categoryKey = `preferences.categories.${category}`;
const label = t(categoryKey); // Correctly resolves to "Booking Notifications"
```

## Notes

### Why Dots Are Reserved

- **Design decision**: next-intl uses dots exclusively for nested object traversal
- **No configuration**: There is no option to use a different separator character
- **Intentional limitation**: Using dots as literal characters would create ambiguous cases
- **Consistent behavior**: All translation tools and next-intl features rely on this convention

### Migration Strategy

When migrating from flat structures:

1. **Identify all files**: Search for `.json` files in your strings/locales directory
2. **Find problematic keys**: Search for keys containing dots that aren't meant for nesting
3. **Convert systematically**: Update all locale files together to maintain consistency
4. **Test thoroughly**: Load all namespaces in development to catch any missed keys
5. **Consider naming**: If keys match database fields, create a mapping layer instead
   of forcing database fields to match translation structure

### Alternative Approaches

If you need to preserve dot notation for other reasons:

1. **Use hyphens or underscores**: `email-notification-booking` or `email_notification_booking`
2. **Create mapping object**: Map database keys to translation keys separately
3. **Nested structure benefits**: Embrace nesting—it improves organization and type safety

### Common Gotchas

- **Partial nesting doesn't work**: You can't mix `"email.notification": {...}` with
  `"email.notification.booking": "..."` at the same level
- **Case sensitivity matters**: `Email.Notification.Booking` is different from
  `email.notification.booking`
- **Update all locales**: If you have multiple language files, update all of them
  or translations will fail for some languages

## References

- [next-intl: Using translations](https://next-intl.dev/docs/usage/translations)
- [GitHub Discussion #148: Dot notation keys without namespaces](https://github.com/amannn/next-intl/discussions/148)
- [GitHub Issue #907: Allow using dots in locale keys](https://github.com/amannn/next-intl/issues/907)
- [GitHub Issue #560: Disable translations keys nesting](https://github.com/amannn/next-intl/issues/560)
