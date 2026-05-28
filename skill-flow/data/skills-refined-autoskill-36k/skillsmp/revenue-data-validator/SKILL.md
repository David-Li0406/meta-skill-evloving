---
name: revenue-data-validator
description: Identifies and filters test/dummy revenue data from real customer transactions across all revenue streams (affiliates, gallery, subscriptions).
---

# Revenue Data Validator Skill

This skill helps identify test/dummy data vs. real customer revenue across the platform.

## Problem Statement

The platform currently shows inflated revenue numbers because test data exists in:
- **Affiliates table**: Test earnings showing $9,609.49
- **Photo orders**: Test gallery purchases
- **Subscriptions**: Admin account subscription ($9.99/month)

**Current Reality**: $0 in actual revenue, but dashboard shows thousands in test data.

## Solution: Revenue Validation Rules

### 1. Affiliate Revenue Validation

**Test Data Indicators:**
- [ ] Earnings created before official launch date
- [ ] Affiliate accounts with test/dummy email patterns (e.g., `test@`, `admin@`, `demo@`)
- [ ] Round number earnings (e.g., $100.00, $500.00, $1000.00)
- [ ] Earnings without corresponding click/conversion records
- [ ] Affiliate IDs that match known test accounts

**SQL to Identify Test Affiliates:**
```sql
-- Find test affiliate accounts
SELECT id, email, total_earnings, created_at
FROM affiliates
WHERE 
  email LIKE '%test%' 
  OR email LIKE '%demo%'
  OR email LIKE '%admin%'
  OR total_earnings::numeric % 100 = 0  -- Round numbers
  OR created_at < '2026-01-01'  -- Before launch
ORDER BY total_earnings DESC;
```

**SQL to Get Real Affiliate Revenue:**
```sql
-- Get only real affiliate revenue
SELECT COALESCE(SUM(total_earnings), 0) as real_revenue
FROM affiliates
WHERE 
  email NOT LIKE '%test%' 
  AND email NOT LIKE '%demo%'
  AND email NOT LIKE '%admin%'
  AND created_at >= '2026-01-01'  -- Adjust to actual launch date
  AND total_earnings > 0;
```

### 2. Gallery Revenue Validation

**Test Data Indicators:**
- [ ] Orders from test email addresses
- [ ] Orders created during development/testing phase
- [ ] Orders with test payment IDs (PayPal sandbox transactions)
- [ ] Orders from admin/developer accounts

**SQL to Identify Test Gallery Orders:**
```sql
-- Find test photo orders
SELECT id, email, total_amount_cents, payment_status, created_at
FROM photo_orders
WHERE 
  email LIKE '%test%'
  OR email LIKE '%demo%'
  OR email LIKE '%admin%'
  OR created_at < '2026-01-01'  -- Before launch
ORDER BY total_amount_cents DESC;
```

**SQL to Get Real Gallery Revenue:**
```sql
-- Get only real gallery revenue (in dollars)
SELECT COALESCE(SUM(total_amount_cents), 0) / 100.0 as real_revenue
FROM photo_orders
WHERE 
  email NOT LIKE '%test%'
  AND email NOT LIKE '%demo%'
  AND email NOT LIKE '%admin%'
  AND created_at >= '2026-01-01'  -- Adjust to actual launch date
  AND payment_status = 'completed';
```

### 3. Subscription Revenue Validation

**Test Data Indicators:**
- [ ] Admin account subscriptions
- [ ] Test user subscriptions
- [ ] Subscriptions created during development

**SQL to Identify Test Subscriptions:**
```sql
-- Find test subscriptions
SELECT ps.id, ps.user_id, u.email, ps.tier, ps.created_at
FROM platform_subscriptions ps
JOIN auth.users u ON u.id = ps.user_id
WHERE 
  u.email LIKE '%test%'
  OR u.email LIKE '%demo%'
  OR u.email LIKE '%admin%'
  OR ps.created_at < '2026-01-01'  -- Before launch
ORDER BY ps.created_at DESC;
```

## Implementation in Dashboard

### Update Admin.tsx Revenue Calculation

Add a launch date constant and filter logic:

```typescript
// Add at top of file
const PLATFORM_LAUNCH_DATE = '2026-01-15'; // Adjust to actual launch date

// In the revenue calculation section:
const isTestEmail = (email: string) => {
  const testPatterns = ['test', 'demo', 'admin', 'dev', 'staging'];
  return testPatterns.some(pattern => 
    email?.toLowerCase().includes(pattern)
  );
};

// Filter affiliates
if (affiliates) {
  affiliateRevenueTotal = affiliates
    .filter(a => {
      // Add email field to the select query first
      return !isTestEmail(a.email) && 
             new Date(a.created_at) >= new Date(PLATFORM_LAUNCH_DATE);
    })
    .reduce((sum, a) => {
      const earnings = typeof a.total_earnings === 'string' 
        ? parseFloat(a.total_earnings) 
        : (a.total_earnings || 0);
      return sum + (isNaN(earnings) ? 0 : earnings);
    }, 0);
}

// Filter gallery orders
if (orders) {
  galleryRevenueTotal = orders
    .filter(o => {
      // Add email field to the select query first
      return !isTestEmail(o.email) && 
             new Date(o.created_at) >= new Date(PLATFORM_LAUNCH_DATE) &&
             o.payment_status === 'completed';
    })
    .reduce((sum, o) => sum + (o.total_amount_cents || 0), 0) / 100;
}
```

### Update Supabase Queries

Modify the queries to include email and created_at fields:

```typescript
// Affiliate query
const { data: affiliates, error: affError } = await supabase
  .from('affiliates')
  .select('total_earnings, email, created_at');

// Gallery orders query
const { data: orders, error: ordersError } = await supabase
  .from('photo_orders')
  .select('total_amount_cents, email, created_at, payment_status');
```

## Quick Cleanup Commands

### Option 1: Mark Test Data (Recommended)
Add a `is_test_data` boolean column to track test records:

```sql
-- Add column to affiliates
ALTER TABLE affiliates ADD COLUMN IF NOT EXISTS is_test_data BOOLEAN DEFAULT false;

-- Mark test affiliates
UPDATE affiliates 
SET is_test_data = true
WHERE 
  email LIKE '%test%' 
  OR email LIKE '%demo%'
  OR email LIKE '%admin%'
  OR created_at < '2026-01-01';

-- Add column to photo_orders
ALTER TABLE photo_orders ADD COLUMN IF NOT EXISTS is_test_data BOOLEAN DEFAULT false;

-- Mark test orders
UPDATE photo_orders 
SET is_test_data = true
WHERE 
  email LIKE '%test%'
  OR email LIKE '%demo%'
  OR email LIKE '%admin%'
  OR created_at < '2026-01-01';
```

Then filter in queries:
```typescript
.eq('is_test_data', false)
```

### Option 2: Delete Test Data (Use with Caution)
```sql
-- BACKUP FIRST!
-- Delete test affiliate data
DELETE FROM affiliates 
WHERE 
  email LIKE '%test%' 
  OR email LIKE '%demo%'
  OR email LIKE '%admin%';

-- Delete test gallery orders
DELETE FROM photo_orders 
WHERE 
  email LIKE '%test%'
  OR email LIKE '%demo%'
  OR email LIKE '%admin%';
```

## Monitoring & Alerts

Add alerts when test data is detected:

```typescript
// In Admin.tsx alerts generation
if (affiliateRevenueTotal > 0) {
  // Check if any test data exists
  const hasTestData = affiliates?.some(a => isTestEmail(a.email));
  if (hasTestData) {
    newAlerts.push({
      id: Date.now() + 100,
      type: 'warning',
      message: 'Test affiliate data detected - revenue may be inflated',
      time: 'Just now',
      read: false
    });
  }
}
```

## Best Practices

1. **Always use launch date filtering** - Set `PLATFORM_LAUNCH_DATE` to when you actually started accepting real customers
2. **Mark, don't delete** - Use `is_test_data` flag instead of deleting test records (useful for debugging)
3. **Email pattern matching** - Maintain a list of test email patterns
4. **Regular audits** - Periodically check for new test data that slipped through
5. **Separate test environment** - Use different Supabase projects for dev/staging/production

## Current Action Items

1. ✅ Set `PLATFORM_LAUNCH_DATE = '2026-01-15'` (or actual launch date)
2. ✅ Update affiliate query to include `email, created_at`
3. ✅ Update gallery query to include `email, created_at, payment_status`
4. ✅ Add `isTestEmail()` helper function
5. ✅ Add filtering logic to revenue calculations
6. ⏳ Run SQL to mark test data with `is_test_data = true`
7. ⏳ Verify dashboard shows $0.00 for all revenue streams
