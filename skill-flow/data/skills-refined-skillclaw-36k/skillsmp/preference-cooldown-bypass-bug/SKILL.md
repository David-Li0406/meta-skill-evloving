---
name: preference-cooldown-bypass-bug
description: |
  Fix for user preference rate limiting bypass vulnerability. Use when: (1) Users can reset
  rate limits by toggling preference settings, (2) Cooldown tracking uses preference.updatedAt
  field, (3) Email/notification spam prevention fails after preference changes, (4) Rate limit
  state stored in same record as enabled/disabled preference. Covers messaging cooldowns,
  notification throttling, and any preference-based rate limiting system.
author: Claude Code
version: 1.0.0
date: 2026-01-23
---

# Preference Cooldown Bypass Bug

## Problem

Using a preference record's `updatedAt` timestamp for rate limiting allows users to bypass
cooldowns by toggling the preference on/off. This creates a security vulnerability where spam
prevention can be circumvented.

## Context / Trigger Conditions

- Rate limiting implemented using preference `updatedAt` field
- Users can toggle preferences (enable/disable) that also track cooldown state
- Cooldown resets unexpectedly when user changes preference settings
- Email or notification spam occurs despite cooldown being in place
- Code pattern: `if (preference.updatedAt > cooldownThreshold)` for rate checks

**Example vulnerable code**:
```typescript
// VULNERABLE: Uses same preference for enabled state AND cooldown
const preference = await db.userPreference.findFirst({
  where: { userId, key: "email.notification.messaging" }
});

if (preference.value !== "true") {
  return { send: false }; // Disabled
}

// BUG: This gets reset when user toggles the preference!
const lastSent = preference.updatedAt;
const cooldownExpiry = new Date(lastSent.getTime() + COOLDOWN_MS);
if (new Date() < cooldownExpiry) {
  return { send: false }; // In cooldown
}
```

## Solution

**Separate Concerns**: Use dedicated preference records for cooldown tracking, independent
from enabled/disabled state preferences.

### Step 1: Add Dedicated Cooldown Preference Key

```typescript
export const EMAIL_PREFERENCE_KEYS = {
  MESSAGING: "email.notification.messaging",           // Enable/disable
  MESSAGE_RECEIVED_COOLDOWN: "email.notification.messaging.lastSent", // Cooldown tracking
} as const;
```

### Step 2: Query Both Preferences Separately

```typescript
async function shouldSendEmail(userId: string) {
  // Check if messaging notifications are enabled
  const preference = await db.userPreference.findFirst({
    where: { userId, key: EMAIL_PREFERENCE_KEYS.MESSAGING }
  });

  if (preference?.value !== "true") {
    return { send: false, reason: "Notifications disabled" };
  }

  // Check cooldown using separate preference (doesn't get reset on toggle)
  const cooldownPreference = await db.userPreference.findUnique({
    where: {
      userId_key: {
        userId,
        key: EMAIL_PREFERENCE_KEYS.MESSAGE_RECEIVED_COOLDOWN,
      },
    },
  });

  if (cooldownPreference) {
    const lastSent = new Date(cooldownPreference.value); // ISO timestamp in value field

    // Validate timestamp
    if (!isNaN(lastSent.getTime())) {
      const cooldownExpiry = new Date(lastSent.getTime() + COOLDOWN_MS);

      if (new Date() < cooldownExpiry) {
        const minutesRemaining = Math.ceil(
          (cooldownExpiry.getTime() - Date.now()) / (60 * 1000)
        );
        return {
          send: false,
          reason: `Cooldown active (${minutesRemaining} minutes remaining)`,
        };
      }
    }
  }

  return { send: true };
}
```

### Step 3: Update Cooldown After Successful Action

```typescript
async function updateCooldown(userId: string): Promise<void> {
  try {
    const now = new Date();
    await db.userPreference.upsert({
      where: {
        userId_key: {
          userId,
          key: EMAIL_PREFERENCE_KEYS.MESSAGE_RECEIVED_COOLDOWN,
        },
      },
      create: {
        userId,
        key: EMAIL_PREFERENCE_KEYS.MESSAGE_RECEIVED_COOLDOWN,
        value: now.toISOString(), // Store timestamp in value field
        category: PreferenceCategory.EMAIL_NOTIFICATION,
      },
      update: {
        value: now.toISOString(), // Update timestamp, not rely on updatedAt
        updatedAt: now,
      },
    });
  } catch (error) {
    console.error("Error updating cooldown:", error);
    // Non-fatal error, don't throw
  }
}
```

### Step 4: Update Tests to Mock Both Queries

```typescript
it("should skip when within cooldown window", async () => {
  const thirtyMinutesAgo = new Date(Date.now() - 30 * 60 * 1000);

  // Mock findFirst for enabled/disabled check
  mockDb.userPreference.findFirst = vi.fn().mockImplementation(({ where }) => {
    if (where.key === EMAIL_PREFERENCE_KEYS.MESSAGING) {
      return Promise.resolve({
        userId,
        key: EMAIL_PREFERENCE_KEYS.MESSAGING,
        value: "true", // Enabled
      });
    }
    return Promise.resolve(null);
  });

  // Mock findUnique for cooldown timestamp check
  mockDb.userPreference.findUnique = vi.fn().mockImplementation(({ where }) => {
    if (where.userId_key?.key === EMAIL_PREFERENCE_KEYS.MESSAGE_RECEIVED_COOLDOWN) {
      return Promise.resolve({
        userId,
        key: EMAIL_PREFERENCE_KEYS.MESSAGE_RECEIVED_COOLDOWN,
        value: thirtyMinutesAgo.toISOString(), // Recent timestamp
      });
    }
    return Promise.resolve(null);
  });

  const result = await sendWithCooldown();

  expect(result.skipped).toBe(true);
  expect(result.reason).toContain("cooldown");
});
```

## Verification

1. **Test Bypass Scenario**:
   ```typescript
   // User receives email at T0
   await sendEmail(); // Success

   // User toggles preference OFF then ON at T+30min
   await updatePreference(userId, "email.notification.messaging", "false");
   await updatePreference(userId, "email.notification.messaging", "true");

   // Attempt to send email at T+35min (within 1-hour cooldown)
   const result = await sendEmail();

   // Should still be blocked by cooldown
   expect(result.skipped).toBe(true);
   expect(result.reason).toContain("cooldown");
   ```

2. **Verify Separation**: Check database - toggling enabled preference should NOT update
   the cooldown preference record.

3. **Test Cooldown Expiry**: After cooldown period (e.g., 1 hour), email should send even
   if preference was toggled during cooldown.

## Example

**Real-World Scenario**: Messaging notification system with 1-hour cooldown to prevent spam.

**Before (Vulnerable)**:
```typescript
// User receives message email at 10:00 AM
// User dislikes email, disables messaging notifications at 10:30 AM
// User re-enables messaging notifications at 10:35 AM
// Another message arrives at 10:40 AM
// BUG: User receives email (cooldown was reset at 10:35 AM)
// Result: User gets spammed with emails every time they toggle preferences
```

**After (Fixed)**:
```typescript
// User receives message email at 10:00 AM (cooldown set to 11:00 AM)
// User dislikes email, disables messaging notifications at 10:30 AM
// User re-enables messaging notifications at 10:35 AM
// Another message arrives at 10:40 AM
// CORRECT: Email is blocked (cooldown still active until 11:00 AM)
// Result: User protected from spam regardless of preference toggles
```

## Notes

- **Storage Pattern**: Store ISO timestamp in `value` field, not `updatedAt` field
- **Query Pattern**: Use `findUnique` with composite key for cooldown checks (more efficient)
- **Error Handling**: Validate timestamp with `!isNaN(date.getTime())` before using
- **Non-Fatal Updates**: Cooldown update failures should log errors but not block main operation
- **Database Design**: Consider adding index on `userId_key` composite for performance
- **Migration Path**: Existing systems need data migration to separate cooldown records

## References

- [Rate Limiting Best Practices - Cloudflare](https://developers.cloudflare.com/waf/rate-limiting-rules/best-practices/)
- [10 Best Practices for API Rate Limiting in 2025 - Zuplo](https://zuplo.com/learning-center/10-best-practices-for-api-rate-limiting-in-2025)
- [Rate Limiting Fundamentals - ByteByteGo](https://blog.bytebytego.com/p/rate-limiting-fundamentals)
