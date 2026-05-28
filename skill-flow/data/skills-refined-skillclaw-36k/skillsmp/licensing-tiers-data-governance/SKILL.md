---
name: licensing-tiers-data-governance
description: Implement subscription tiers with field-level access control, feature gating, rate limiting, and compliance tracking. Design data governance systems that enforce different access levels, retention policies, and regulatory requirements based on user subscription tier (Free, Pro, Enterprise).
---

# Licensing Tiers & Data Governance

Comprehensive framework for implementing subscription-based access control with field-level permissions, feature gating, and tier-specific compliance requirements.

## When to Use

- Building SaaS products with Free/Pro/Enterprise tiers
- Implementing field-level access control based on subscription
- Enforcing API rate limits by tier
- Managing data retention policies per tier
- Tracking compliance requirements (SOC 2, HIPAA, GDPR) by tier
- Auditing tier changes and feature access
- Migrating users between subscription tiers

## Core Concepts

### Subscription Tier Hierarchy

```
Free Tier
  ├─ Basic features
  ├─ Limited data access
  ├─ Public data only
  └─ Rate limits: 100 req/day

Pro Tier
  ├─ All Free features
  ├─ Extended data fields
  ├─ Private data access
  ├─ Rate limits: 10K req/day
  └─ 90-day data retention

Enterprise Tier
  ├─ All Pro features
  ├─ Full data access
  ├─ Sensitive PII fields
  ├─ Unlimited API calls
  ├─ Custom retention policies
  └─ SOC 2 / HIPAA compliance
```

### Field-Level Access Control

Different tiers see different fields for the same entity:

```typescript
// User entity - field visibility by tier
interface User {
  // FREE: Public fields
  id: string;
  username: string;
  created_at: Date;

  // PRO: Private fields
  email?: string;              // ← Pro+ only
  phone?: string;              // ← Pro+ only
  last_login?: Date;           // ← Pro+ only

  // ENTERPRISE: Sensitive fields
  ip_address?: string;         // ← Enterprise only
  payment_method?: string;     // ← Enterprise only
  tax_id?: string;             // ← Enterprise only
}
```

---

## Schema Design

### 1. Subscription Management

```sql
-- Subscription tiers
CREATE TABLE subscription_tiers (
  id SERIAL PRIMARY KEY,
  tier_name VARCHAR(50) NOT NULL UNIQUE, -- 'free', 'pro', 'enterprise'
  tier_level INT NOT NULL UNIQUE,        -- 1=Free, 2=Pro, 3=Enterprise
  display_name VARCHAR(100) NOT NULL,

  -- Rate limits
  api_requests_per_day INT,
  api_requests_per_minute INT,

  -- Data retention
  data_retention_days INT,               -- NULL = unlimited

  -- Feature flags
  features JSONB NOT NULL DEFAULT '{}',  -- {"export": true, "api": true}

  -- Compliance
  compliance_level VARCHAR(50)[],        -- ['SOC2', 'HIPAA', 'GDPR']

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User subscriptions
CREATE TABLE user_subscriptions (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tier_id INT NOT NULL REFERENCES subscription_tiers(id),

  -- Subscription lifecycle
  status VARCHAR(20) NOT NULL DEFAULT 'active', -- 'active', 'cancelled', 'expired'
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ,                       -- NULL = no expiration

  -- Billing
  billing_cycle VARCHAR(20),                    -- 'monthly', 'annual'
  price_cents INT,
  currency VARCHAR(3) DEFAULT 'USD',

  -- Trial tracking
  is_trial BOOLEAN DEFAULT FALSE,
  trial_ends_at TIMESTAMPTZ,

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(user_id, tier_id)
);

CREATE INDEX idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX idx_user_subscriptions_status ON user_subscriptions(status);
CREATE INDEX idx_user_subscriptions_expires_at ON user_subscriptions(expires_at);
```

### 2. Field-Level Access Control

```sql
-- Define which fields are visible at each tier
CREATE TABLE field_access_policies (
  id SERIAL PRIMARY KEY,

  -- Target entity
  table_name VARCHAR(100) NOT NULL,
  field_name VARCHAR(100) NOT NULL,

  -- Access level required
  min_tier_level INT NOT NULL REFERENCES subscription_tiers(tier_level),

  -- Field classification
  classification VARCHAR(50) NOT NULL, -- 'public', 'private', 'sensitive', 'pii'

  -- Compliance requirements
  requires_compliance VARCHAR(50)[],   -- ['SOC2', 'HIPAA']

  created_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(table_name, field_name)
);

-- Example policies
INSERT INTO field_access_policies (table_name, field_name, min_tier_level, classification) VALUES
  ('users', 'id', 1, 'public'),
  ('users', 'username', 1, 'public'),
  ('users', 'email', 2, 'private'),              -- Pro+
  ('users', 'phone', 2, 'private'),              -- Pro+
  ('users', 'ip_address', 3, 'sensitive'),       -- Enterprise only
  ('users', 'payment_method', 3, 'pii');         -- Enterprise only
```

### 3. Feature Gating

```sql
-- Features that require specific tiers
CREATE TABLE feature_gates (
  id SERIAL PRIMARY KEY,
  feature_key VARCHAR(100) NOT NULL UNIQUE,
  feature_name VARCHAR(200) NOT NULL,

  -- Access requirements
  min_tier_level INT NOT NULL REFERENCES subscription_tiers(tier_level),

  -- Rate limits for this feature
  rate_limit_per_day INT,
  rate_limit_per_hour INT,

  -- Metadata
  description TEXT,
  enabled BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Example features
INSERT INTO feature_gates (feature_key, feature_name, min_tier_level, rate_limit_per_day) VALUES
  ('export_csv', 'CSV Export', 2, 100),                    -- Pro+
  ('api_access', 'API Access', 2, 10000),                  -- Pro+
  ('custom_reports', 'Custom Reports', 2, 50),             -- Pro+
  ('sso_integration', 'SSO Integration', 3, NULL),         -- Enterprise
  ('dedicated_support', 'Dedicated Support', 3, NULL),     -- Enterprise
  ('audit_logs', 'Audit Logs', 3, NULL);                   -- Enterprise
```

### 4. API Rate Limiting

```sql
-- Track API usage per user
CREATE TABLE api_usage (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- Request details
  endpoint VARCHAR(200) NOT NULL,
  method VARCHAR(10) NOT NULL,

  -- Timing
  request_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  response_time_ms INT,

  -- Rate limiting
  tier_level INT NOT NULL,
  rate_limit_hit BOOLEAN DEFAULT FALSE,

  -- Status
  status_code INT,
  error_message TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_api_usage_user_time ON api_usage(user_id, request_time DESC);
CREATE INDEX idx_api_usage_endpoint ON api_usage(endpoint);

-- Materialized view for rate limit checking (refresh every minute)
CREATE MATERIALIZED VIEW user_api_usage_today AS
SELECT
  user_id,
  COUNT(*) as request_count,
  MAX(request_time) as last_request,
  DATE(request_time) as request_date
FROM api_usage
WHERE request_time >= CURRENT_DATE
GROUP BY user_id, DATE(request_time);

CREATE UNIQUE INDEX idx_user_api_usage_today ON user_api_usage_today(user_id, request_date);
```

### 5. Audit Trail

```sql
-- Track all tier changes and feature access
CREATE TABLE tier_change_audit (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- Change details
  old_tier_id INT REFERENCES subscription_tiers(id),
  new_tier_id INT NOT NULL REFERENCES subscription_tiers(id),

  -- Reason
  change_reason VARCHAR(50) NOT NULL, -- 'upgrade', 'downgrade', 'trial', 'cancel', 'expire'
  initiated_by VARCHAR(50) NOT NULL,  -- 'user', 'admin', 'system'
  admin_user_id BIGINT REFERENCES users(id),

  -- Billing impact
  refund_amount_cents INT,
  prorated_amount_cents INT,

  -- Metadata
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tier_change_user ON tier_change_audit(user_id, created_at DESC);

-- Track feature access attempts (especially denials)
CREATE TABLE feature_access_audit (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- Feature details
  feature_key VARCHAR(100) NOT NULL,
  access_granted BOOLEAN NOT NULL,

  -- Denial reason
  denial_reason VARCHAR(100),        -- 'tier_too_low', 'rate_limit', 'expired'
  required_tier_level INT,
  user_tier_level INT NOT NULL,

  -- Context
  ip_address INET,
  user_agent TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feature_access_user ON feature_access_audit(user_id, created_at DESC);
CREATE INDEX idx_feature_access_denied ON feature_access_audit(access_granted, created_at DESC) WHERE access_granted = FALSE;
```

---

## Implementation Patterns

### 1. Field-Level Access Helper

```typescript
interface FieldAccessOptions {
  tableName: string;
  userTierLevel: number;
  requiresCompliance?: string[];
}

export async function filterFieldsByTier<T extends Record<string, any>>(
  data: T,
  options: FieldAccessOptions
): Promise<Partial<T>> {
  // Get field access policies for this table
  const policies = await db.query(`
    SELECT field_name, min_tier_level, classification, requires_compliance
    FROM field_access_policies
    WHERE table_name = $1
  `, [options.tableName]);

  const filtered: Partial<T> = {};

  for (const [key, value] of Object.entries(data)) {
    const policy = policies.find(p => p.field_name === key);

    if (!policy) {
      // No policy = public field
      filtered[key as keyof T] = value;
      continue;
    }

    // Check tier level
    if (options.userTierLevel < policy.min_tier_level) {
      continue; // User tier too low
    }

    // Check compliance requirements
    if (policy.requires_compliance?.length > 0 && options.requiresCompliance) {
      const hasCompliance = policy.requires_compliance.every(
        (req: string) => options.requiresCompliance!.includes(req)
      );
      if (!hasCompliance) {
        continue; // Compliance not met
      }
    }

    filtered[key as keyof T] = value;
  }

  return filtered;
}

// Usage
const user = await db.users.findOne({ id: userId });
const filteredUser = await filterFieldsByTier(user, {
  tableName: 'users',
  userTierLevel: currentUser.tierLevel,
  requiresCompliance: currentUser.complianceCertifications
});
```

### 2. Feature Gate Middleware

```typescript
export function requireFeature(featureKey: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user; // from auth middleware

    // Get feature requirements
    const feature = await db.featureGates.findOne({
      feature_key: featureKey
    });

    if (!feature) {
      return res.status(500).json({ error: 'Feature not found' });
    }

    if (!feature.enabled) {
      return res.status(503).json({ error: 'Feature temporarily disabled' });
    }

    // Check tier level
    if (user.tierLevel < feature.min_tier_level) {
      await logFeatureAccessDenial(user.id, featureKey, 'tier_too_low');

      return res.status(403).json({
        error: 'Feature not available in your subscription tier',
        feature: feature.feature_name,
        required_tier: feature.min_tier_level,
        upgrade_url: `/upgrade?feature=${featureKey}`
      });
    }

    // Check rate limit
    if (feature.rate_limit_per_day) {
      const usage = await getFeatureUsageToday(user.id, featureKey);

      if (usage >= feature.rate_limit_per_day) {
        await logFeatureAccessDenial(user.id, featureKey, 'rate_limit');

        return res.status(429).json({
          error: 'Daily rate limit exceeded',
          limit: feature.rate_limit_per_day,
          reset_at: getTomorrowMidnight()
        });
      }
    }

    // Log successful access
    await logFeatureAccess(user.id, featureKey);

    next();
  };
}

// Usage in routes
app.post('/api/export',
  requireAuth,
  requireFeature('export_csv'),
  async (req, res) => {
    // Export logic here
  }
);
```

### 3. API Rate Limiter

```typescript
import Redis from 'ioredis';

const redis = new Redis();

export async function checkRateLimit(
  userId: number,
  tierLevel: number
): Promise<{ allowed: boolean; remaining: number; resetAt: Date }> {
  // Get tier limits
  const tier = await db.subscriptionTiers.findOne({ tier_level: tierLevel });

  if (!tier.api_requests_per_day) {
    return {
      allowed: true,
      remaining: Infinity,
      resetAt: new Date()
    };
  }

  const today = new Date().toISOString().split('T')[0];
  const key = `rate_limit:${userId}:${today}`;

  // Increment request count
  const count = await redis.incr(key);

  // Set expiration on first request of the day
  if (count === 1) {
    await redis.expireat(key, getTomorrowMidnightTimestamp());
  }

  const remaining = Math.max(0, tier.api_requests_per_day - count);
  const allowed = count <= tier.api_requests_per_day;

  if (!allowed) {
    // Log rate limit hit
    await db.apiUsage.create({
      user_id: userId,
      endpoint: 'rate_limit_check',
      method: 'N/A',
      tier_level: tierLevel,
      rate_limit_hit: true
    });
  }

  return {
    allowed,
    remaining,
    resetAt: getTomorrowMidnight()
  };
}

// Middleware
export async function rateLimitMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const user = req.user;

  const { allowed, remaining, resetAt } = await checkRateLimit(
    user.id,
    user.tierLevel
  );

  // Add rate limit headers
  res.setHeader('X-RateLimit-Limit', user.tier.api_requests_per_day);
  res.setHeader('X-RateLimit-Remaining', remaining);
  res.setHeader('X-RateLimit-Reset', resetAt.toISOString());

  if (!allowed) {
    return res.status(429).json({
      error: 'API rate limit exceeded',
      limit: user.tier.api_requests_per_day,
      reset_at: resetAt,
      upgrade_url: '/upgrade'
    });
  }

  next();
}
```

### 4. Tier Migration Handler

```typescript
interface TierChangeOptions {
  userId: number;
  newTierId: number;
  reason: 'upgrade' | 'downgrade' | 'trial' | 'cancel' | 'expire';
  initiatedBy: 'user' | 'admin' | 'system';
  adminUserId?: number;
  notes?: string;
}

export async function changeTier(
  options: TierChangeOptions
): Promise<{ success: boolean; message: string }> {
  const { userId, newTierId, reason, initiatedBy } = options;

  // Get current subscription
  const currentSub = await db.userSubscriptions.findOne({
    user_id: userId,
    status: 'active'
  });

  const oldTier = await db.subscriptionTiers.findOne({
    id: currentSub.tier_id
  });
  const newTier = await db.subscriptionTiers.findOne({
    id: newTierId
  });

  // Start transaction
  await db.transaction(async (trx) => {
    // 1. Create audit record
    await trx.tierChangeAudit.create({
      user_id: userId,
      old_tier_id: currentSub.tier_id,
      new_tier_id: newTierId,
      change_reason: reason,
      initiated_by: initiatedBy,
      admin_user_id: options.adminUserId,
      notes: options.notes
    });

    // 2. Update subscription
    await trx.userSubscriptions.update(
      { id: currentSub.id },
      {
        tier_id: newTierId,
        updated_at: new Date()
      }
    );

    // 3. Handle downgrade - check data retention
    if (newTier.tier_level < oldTier.tier_level) {
      await handleDowngradeDataRetention(trx, userId, newTier);
    }

    // 4. Handle upgrade - unlock features
    if (newTier.tier_level > oldTier.tier_level) {
      await unlockTierFeatures(trx, userId, newTier);
    }

    // 5. Clear rate limit cache
    const today = new Date().toISOString().split('T')[0];
    await redis.del(`rate_limit:${userId}:${today}`);
  });

  return {
    success: true,
    message: `Successfully changed from ${oldTier.display_name} to ${newTier.display_name}`
  };
}

async function handleDowngradeDataRetention(
  trx: Transaction,
  userId: number,
  newTier: SubscriptionTier
) {
  if (!newTier.data_retention_days) return;

  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - newTier.data_retention_days);

  // Archive or delete old data based on retention policy
  await trx.query(`
    UPDATE user_data
    SET archived = TRUE, archived_at = NOW()
    WHERE user_id = $1
      AND created_at < $2
      AND archived = FALSE
  `, [userId, cutoffDate]);

  // Log data retention action
  logger.info({
    userId,
    tierName: newTier.tier_name,
    retentionDays: newTier.data_retention_days,
    cutoffDate
  }, 'Applied data retention policy on tier downgrade');
}
```

### 5. Compliance Level Tracking

```typescript
export async function getUserComplianceLevel(
  userId: number
): Promise<string[]> {
  const subscription = await db.userSubscriptions.findOne({
    user_id: userId,
    status: 'active'
  });

  const tier = await db.subscriptionTiers.findOne({
    id: subscription.tier_id
  });

  return tier.compliance_level || [];
}

export async function requireCompliance(
  required: string[]
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;

    const userCompliance = await getUserComplianceLevel(user.id);

    const hasAllRequired = required.every(
      req => userCompliance.includes(req)
    );

    if (!hasAllRequired) {
      const missing = required.filter(
        req => !userCompliance.includes(req)
      );

      return res.status(403).json({
        error: 'Compliance level too low',
        required: required,
        missing: missing,
        upgrade_url: '/upgrade?compliance=true'
      });
    }

    next();
  };
}

// Usage: Endpoints that require SOC 2 compliance
app.get('/api/enterprise/audit-logs',
  requireAuth,
  requireCompliance(['SOC2']),
  async (req, res) => {
    // Audit logs logic
  }
);
```

---

## Common Patterns

### Free → Pro → Enterprise Progression

```typescript
const TIER_HIERARCHY = {
  free: {
    level: 1,
    features: ['basic_search', 'public_data'],
    rateLimit: 100,
    dataRetention: 30,
    compliance: []
  },
  pro: {
    level: 2,
    features: ['advanced_search', 'export', 'api_access', 'private_data'],
    rateLimit: 10000,
    dataRetention: 90,
    compliance: ['GDPR']
  },
  enterprise: {
    level: 3,
    features: ['all_features', 'sso', 'dedicated_support', 'custom_reports'],
    rateLimit: null, // unlimited
    dataRetention: null, // custom
    compliance: ['SOC2', 'HIPAA', 'GDPR']
  }
};
```

### Usage-Based Soft Limits

```typescript
// Don't hard-block at limit, but warn user
export async function checkUsageWithWarning(
  userId: number,
  featureKey: string
): Promise<{ allowed: boolean; warning?: string }> {
  const usage = await getFeatureUsageThisMonth(userId, featureKey);
  const limit = await getFeatureLimit(userId, featureKey);

  if (!limit) {
    return { allowed: true };
  }

  const percentUsed = (usage / limit) * 100;

  if (percentUsed >= 100) {
    return {
      allowed: false,
      warning: 'Monthly limit exceeded. Upgrade to continue.'
    };
  }

  if (percentUsed >= 80) {
    return {
      allowed: true,
      warning: `You've used ${percentUsed.toFixed(0)}% of your monthly ${featureKey} quota.`
    };
  }

  return { allowed: true };
}
```

### Grandfather Legacy Users

```typescript
// Some users on old plans should keep their benefits
CREATE TABLE legacy_user_overrides (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,

  -- Override specific limits
  override_rate_limit INT,
  override_features JSONB,
  override_data_retention INT,

  -- Reason for override
  reason VARCHAR(200) NOT NULL, -- 'early_adopter', 'beta_tester', 'lifetime_deal'
  granted_by BIGINT REFERENCES users(id),
  granted_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ,

  notes TEXT
);

// Check overrides before applying tier limits
export async function getEffectiveLimits(userId: number) {
  const override = await db.legacyUserOverrides.findOne({ user_id: userId });

  if (override && (!override.expires_at || override.expires_at > new Date())) {
    return {
      rateLimit: override.override_rate_limit,
      features: override.override_features,
      dataRetention: override.override_data_retention
    };
  }

  // No override, use tier limits
  const subscription = await getCurrentSubscription(userId);
  return subscription.tier;
}
```

---

## Testing Strategy

### 1. Test Tier Boundaries

```typescript
describe('Field-level access control', () => {
  it('should hide email field for Free tier users', async () => {
    const user = await createUser({ tierLevel: 1 }); // Free

    const userData = { id: 1, username: 'test', email: 'test@example.com' };
    const filtered = await filterFieldsByTier(userData, {
      tableName: 'users',
      userTierLevel: user.tierLevel
    });

    expect(filtered.id).toBeDefined();
    expect(filtered.username).toBeDefined();
    expect(filtered.email).toBeUndefined();
  });

  it('should show email field for Pro tier users', async () => {
    const user = await createUser({ tierLevel: 2 }); // Pro

    const userData = { id: 1, username: 'test', email: 'test@example.com' };
    const filtered = await filterFieldsByTier(userData, {
      tableName: 'users',
      userTierLevel: user.tierLevel
    });

    expect(filtered.email).toBe('test@example.com');
  });
});

describe('Feature gates', () => {
  it('should block Free users from exporting', async () => {
    const user = await createUser({ tierLevel: 1 });

    const result = await checkFeatureAccess(user.id, 'export_csv');

    expect(result.allowed).toBe(false);
    expect(result.reason).toBe('tier_too_low');
  });

  it('should allow Pro users to export', async () => {
    const user = await createUser({ tierLevel: 2 });

    const result = await checkFeatureAccess(user.id, 'export_csv');

    expect(result.allowed).toBe(true);
  });
});
```

### 2. Test Rate Limits

```typescript
describe('API rate limiting', () => {
  it('should allow requests within limit', async () => {
    const user = await createUser({ tierLevel: 1, dailyLimit: 100 });

    for (let i = 0; i < 100; i++) {
      const result = await checkRateLimit(user.id, user.tierLevel);
      expect(result.allowed).toBe(true);
    }
  });

  it('should block requests exceeding limit', async () => {
    const user = await createUser({ tierLevel: 1, dailyLimit: 100 });

    // Make 100 requests
    for (let i = 0; i < 100; i++) {
      await makeRequest(user.id);
    }

    // 101st request should be blocked
    const result = await checkRateLimit(user.id, user.tierLevel);
    expect(result.allowed).toBe(false);
  });

  it('should reset rate limit at midnight', async () => {
    const user = await createUser({ tierLevel: 1, dailyLimit: 100 });

    // Make 100 requests today
    for (let i = 0; i < 100; i++) {
      await makeRequest(user.id);
    }

    // Simulate midnight reset
    await simulateMidnight();

    // Should allow requests again
    const result = await checkRateLimit(user.id, user.tierLevel);
    expect(result.allowed).toBe(true);
  });
});
```

### 3. Test Tier Migrations

```typescript
describe('Tier upgrades', () => {
  it('should unlock Pro features on upgrade', async () => {
    const user = await createUser({ tierLevel: 1 }); // Free

    // Can't export initially
    expect(await canUseFeature(user.id, 'export_csv')).toBe(false);

    // Upgrade to Pro
    await changeTier({
      userId: user.id,
      newTierId: PRO_TIER_ID,
      reason: 'upgrade',
      initiatedBy: 'user'
    });

    // Can export now
    expect(await canUseFeature(user.id, 'export_csv')).toBe(true);
  });

  it('should enforce data retention on downgrade', async () => {
    const user = await createUser({ tierLevel: 2 }); // Pro

    // Create data 100 days ago
    await createOldData(user.id, daysAgo(100));

    // Downgrade to Free (30-day retention)
    await changeTier({
      userId: user.id,
      newTierId: FREE_TIER_ID,
      reason: 'downgrade',
      initiatedBy: 'user'
    });

    // Old data should be archived
    const archivedData = await getArchivedData(user.id);
    expect(archivedData.length).toBeGreaterThan(0);
  });
});
```

---

## Monitoring & Alerts

### Key Metrics to Track

```sql
-- Users hitting rate limits
SELECT
  u.email,
  st.tier_name,
  COUNT(*) as rate_limit_hits,
  MAX(au.request_time) as last_hit
FROM api_usage au
JOIN users u ON u.id = au.user_id
JOIN user_subscriptions us ON us.user_id = u.id
JOIN subscription_tiers st ON st.id = us.tier_id
WHERE au.rate_limit_hit = TRUE
  AND au.request_time >= NOW() - INTERVAL '7 days'
GROUP BY u.email, st.tier_name
ORDER BY rate_limit_hits DESC
LIMIT 100;

-- Feature access denials (potential upsell opportunities)
SELECT
  faa.feature_key,
  COUNT(*) as denial_count,
  COUNT(DISTINCT faa.user_id) as unique_users,
  st.tier_name as user_tier
FROM feature_access_audit faa
JOIN users u ON u.id = faa.user_id
JOIN user_subscriptions us ON us.user_id = u.id
JOIN subscription_tiers st ON st.id = us.tier_id
WHERE faa.access_granted = FALSE
  AND faa.created_at >= NOW() - INTERVAL '7 days'
GROUP BY faa.feature_key, st.tier_name
ORDER BY denial_count DESC;

-- Tier distribution
SELECT
  st.tier_name,
  st.tier_level,
  COUNT(*) as user_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM user_subscriptions us
JOIN subscription_tiers st ON st.id = us.tier_id
WHERE us.status = 'active'
GROUP BY st.tier_name, st.tier_level
ORDER BY st.tier_level;

-- Churn risk (users repeatedly hitting limits)
SELECT
  u.id,
  u.email,
  st.tier_name,
  COUNT(DISTINCT DATE(au.request_time)) as days_with_rate_limits
FROM api_usage au
JOIN users u ON u.id = au.user_id
JOIN user_subscriptions us ON us.user_id = u.id
JOIN subscription_tiers st ON st.id = us.tier_id
WHERE au.rate_limit_hit = TRUE
  AND au.request_time >= NOW() - INTERVAL '30 days'
GROUP BY u.id, u.email, st.tier_name
HAVING COUNT(DISTINCT DATE(au.request_time)) >= 5
ORDER BY days_with_rate_limits DESC;
```

---

## Security Considerations

### 1. Prevent Tier Escalation Attacks

```typescript
// Never trust tier level from client
// WRONG:
app.post('/api/export', async (req, res) => {
  const { tierLevel } = req.body; // ❌ Client-controlled
  if (tierLevel >= 2) {
    // Allow export
  }
});

// CORRECT:
app.post('/api/export', requireAuth, async (req, res) => {
  const user = await db.users.findOne({ id: req.user.id });
  const subscription = await getCurrentSubscription(user.id);

  if (subscription.tier.tier_level < 2) {
    return res.status(403).json({ error: 'Upgrade required' });
  }

  // Allow export
});
```

### 2. Audit Tier Changes

```typescript
// Always log who changed a user's tier
await db.tierChangeAudit.create({
  user_id: userId,
  old_tier_id: oldTier.id,
  new_tier_id: newTier.id,
  change_reason: 'admin_override',
  initiated_by: 'admin',
  admin_user_id: req.admin.id, // ← Track admin
  notes: 'Customer support request #12345'
});
```

### 3. Rate Limit Admin Endpoints

```typescript
// Even admins should have rate limits
app.post('/admin/user/:id/change-tier',
  requireAuth,
  requireAdmin,
  rateLimitMiddleware({ limit: 100, window: '1h' }), // ← Admin limit
  async (req, res) => {
    // Tier change logic
  }
);
```

---

## Common Pitfalls

| Don't | Do |
|-------|-----|
| Trust tier level from client | Always query tier from database |
| Hard-code tier IDs in application | Use tier_level for logic, reference tiers by name |
| Block users at 100% of limit without warning | Show warnings at 80%, 90%, 95% |
| Delete data immediately on downgrade | Archive with grace period (7-30 days) |
| Let admins change tiers without audit trail | Log all tier changes with reason and admin ID |
| Use same rate limit for all endpoints | Different limits for expensive vs cheap operations |
| Forget to expire trial subscriptions | Run daily cron to check `trial_ends_at` |
| Allow unlimited free tier | Set reasonable limits to prevent abuse |

---

## Migration Strategies

### Introducing Tiers to Existing Product

```sql
-- 1. Create default Free tier for all existing users
INSERT INTO user_subscriptions (user_id, tier_id, started_at)
SELECT
  u.id,
  (SELECT id FROM subscription_tiers WHERE tier_name = 'free'),
  u.created_at
FROM users u
WHERE NOT EXISTS (
  SELECT 1 FROM user_subscriptions WHERE user_id = u.id
);

-- 2. Grandfather power users to Pro tier
UPDATE user_subscriptions
SET tier_id = (SELECT id FROM subscription_tiers WHERE tier_name = 'pro')
WHERE user_id IN (
  SELECT user_id
  FROM api_usage
  WHERE request_time >= NOW() - INTERVAL '30 days'
  GROUP BY user_id
  HAVING COUNT(*) > 5000 -- Heavy users
);

-- 3. Create legacy overrides for lifetime deal customers
INSERT INTO legacy_user_overrides (user_id, reason, override_features)
SELECT
  id,
  'lifetime_deal',
  '{"all_features": true}'::jsonb
FROM users
WHERE purchased_lifetime_deal = TRUE;
```

---

## Examples

### SaaS Analytics Platform

```typescript
const TIERS = {
  free: {
    level: 1,
    features: ['basic_charts', 'last_30_days'],
    max_projects: 1,
    max_team_members: 1,
    api_requests_per_day: 100
  },
  starter: {
    level: 2,
    features: ['advanced_charts', 'last_90_days', 'export_csv'],
    max_projects: 3,
    max_team_members: 5,
    api_requests_per_day: 10000
  },
  professional: {
    level: 3,
    features: ['custom_dashboards', 'unlimited_history', 'api_access'],
    max_projects: 10,
    max_team_members: 20,
    api_requests_per_day: 100000
  },
  enterprise: {
    level: 4,
    features: ['sso', 'white_label', 'dedicated_support', 'sla'],
    max_projects: null,
    max_team_members: null,
    api_requests_per_day: null,
    compliance: ['SOC2', 'HIPAA']
  }
};
```

### Healthcare SaaS with HIPAA

```typescript
// Only Enterprise tier can access PHI
export async function requireHIPAACompliance() {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    const compliance = await getUserComplianceLevel(user.id);

    if (!compliance.includes('HIPAA')) {
      return res.status(403).json({
        error: 'HIPAA compliance required',
        message: 'Access to patient health information requires Enterprise plan',
        upgrade_url: '/upgrade?compliance=hipaa'
      });
    }

    // Log HIPAA data access for audit
    await db.hipaaAuditLog.create({
      user_id: user.id,
      action: 'accessed_phi',
      endpoint: req.path,
      ip_address: req.ip
    });

    next();
  };
}
```

---

## When NOT to Use This Skill

- **Simple projects** - If you only have 1-2 tiers, inline checks are fine
- **Internal tools** - No need for complex tiers if all users are employees
- **MVP stage** - Add tiers after product-market fit, not before
- **No monetization plan** - Don't build subscription infrastructure if you're not charging

---

## Related Skills

- `/scalable-data-schema` - Design schemas that support tier-based access
- `/data-provenance` - Track data lineage for compliance requirements
- `/api-design` - Design APIs with rate limiting and tier-based access
- `/security-review` - Audit tier enforcement for security vulnerabilities

---

**Last Updated**: 2026-01-22
**Version**: 1.0.0
