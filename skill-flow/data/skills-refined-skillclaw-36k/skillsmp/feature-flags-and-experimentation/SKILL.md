---
name: Feature Flags and Experimentation
description: This skill should be used when the user asks to "feature flag, A/B testing, feature toggle, experimentation, LaunchDarkly, gradual rollout, canary release, percentage rollout, feature management", or needs help with Feature toggles, A/B testing, and gradual rollouts.
version: 1.0.0
---

# Feature Flags and Experimentation

Comprehensive guidance for implementing feature flags, A/B testing, gradual rollouts, and experimentation platforms.

## Feature Flag Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Feature Flag Service                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Admin UI  │  │  Rules      │  │  Analytics & Metrics    │ │
│  │  Dashboard  │  │  Engine     │  │  Collection             │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │  Backend │    │ Frontend │    │  Mobile  │
       │   SDK    │    │   SDK    │    │   SDK    │
       └──────────┘    └──────────┘    └──────────┘
```

## OpenFeature Standard

### Server-Side Implementation

```typescript
// featureFlags.ts - OpenFeature with custom provider
import { OpenFeature, Client } from '@openfeature/server-sdk';
import { LaunchDarklyProvider } from '@launchdarkly/openfeature-node-server';

// Initialize OpenFeature with provider
async function initializeFeatureFlags() {
    const ldClient = await LaunchDarklyProvider.create(process.env.LD_SDK_KEY!);
    await OpenFeature.setProviderAndWait(ldClient);
}

// Get feature flag client
export function getFeatureFlagClient(context?: EvaluationContext): Client {
    return OpenFeature.getClient();
}

// Usage in application
const client = getFeatureFlagClient();

const showNewUI = await client.getBooleanValue('new-ui-enabled', false, {
    targetingKey: user.id,
    email: user.email,
    plan: user.plan,
});

if (showNewUI) {
    renderNewUI();
} else {
    renderLegacyUI();
}
```

### React Integration

```tsx
// providers/FeatureFlagProvider.tsx
import { OpenFeature, OpenFeatureProvider, useFlag } from '@openfeature/react-sdk';
import { LaunchDarklyWebProvider } from '@launchdarkly/openfeature-client-provider';

// Initialize
const ldProvider = new LaunchDarklyWebProvider(process.env.NEXT_PUBLIC_LD_CLIENT_ID!, {
    kind: 'user',
    key: 'anonymous',
});

OpenFeature.setProvider(ldProvider);

// Provider wrapper
export function FeatureFlagProvider({ children }: { children: React.ReactNode }) {
    return (
        <OpenFeatureProvider>
            {children}
        </OpenFeatureProvider>
    );
}

// Hook usage
function FeatureComponent() {
    const { value: showBetaFeature, isLoading } = useFlag('beta-feature', false);

    if (isLoading) return <Spinner />;

    return showBetaFeature ? <BetaFeature /> : <StableFeature />;
}
```

## Custom Feature Flag Service

### Backend Service

```typescript
// services/featureFlag.ts
import Redis from 'ioredis';

interface FeatureFlag {
    key: string;
    enabled: boolean;
    rolloutPercentage: number;
    targetingRules: TargetingRule[];
    variants?: Variant[];
}

interface TargetingRule {
    attribute: string;
    operator: 'eq' | 'neq' | 'contains' | 'in' | 'gte' | 'lte';
    value: any;
    enabled: boolean;
}

interface Variant {
    key: string;
    weight: number;
    payload?: Record<string, any>;
}

interface UserContext {
    userId: string;
    email?: string;
    plan?: string;
    country?: string;
    attributes?: Record<string, any>;
}

class FeatureFlagService {
    private redis: Redis;
    private localCache: Map<string, { flag: FeatureFlag; expiry: number }>;
    private cacheTTL = 60000; // 1 minute

    constructor(redis: Redis) {
        this.redis = redis;
        this.localCache = new Map();
    }

    async isEnabled(flagKey: string, context: UserContext): Promise<boolean> {
        const flag = await this.getFlag(flagKey);

        if (!flag || !flag.enabled) {
            return false;
        }

        // Check targeting rules
        if (flag.targetingRules.length > 0) {
            const matchesRule = this.evaluateRules(flag.targetingRules, context);
            if (matchesRule !== null) {
                return matchesRule;
            }
        }

        // Percentage rollout
        if (flag.rolloutPercentage < 100) {
            return this.isInRollout(flagKey, context.userId, flag.rolloutPercentage);
        }

        return true;
    }

    async getVariant(flagKey: string, context: UserContext): Promise<string | null> {
        const flag = await this.getFlag(flagKey);

        if (!flag || !flag.enabled || !flag.variants) {
            return null;
        }

        // Consistent hashing for variant assignment
        const hash = this.hashUserFlag(context.userId, flagKey);
        const bucket = hash % 100;

        let cumulative = 0;
        for (const variant of flag.variants) {
            cumulative += variant.weight;
            if (bucket < cumulative) {
                return variant.key;
            }
        }

        return flag.variants[0]?.key || null;
    }

    private async getFlag(key: string): Promise<FeatureFlag | null> {
        // Check local cache
        const cached = this.localCache.get(key);
        if (cached && cached.expiry > Date.now()) {
            return cached.flag;
        }

        // Fetch from Redis
        const data = await this.redis.get(`feature:${key}`);
        if (!data) return null;

        const flag = JSON.parse(data) as FeatureFlag;

        // Update local cache
        this.localCache.set(key, {
            flag,
            expiry: Date.now() + this.cacheTTL,
        });

        return flag;
    }

    private evaluateRules(rules: TargetingRule[], context: UserContext): boolean | null {
        for (const rule of rules) {
            if (!rule.enabled) continue;

            const value = this.getContextValue(context, rule.attribute);
            const matches = this.evaluateCondition(value, rule.operator, rule.value);

            if (matches) {
                return true;
            }
        }
        return null;
    }

    private evaluateCondition(value: any, operator: string, target: any): boolean {
        switch (operator) {
            case 'eq': return value === target;
            case 'neq': return value !== target;
            case 'contains': return String(value).includes(target);
            case 'in': return Array.isArray(target) && target.includes(value);
            case 'gte': return value >= target;
            case 'lte': return value <= target;
            default: return false;
        }
    }

    private getContextValue(context: UserContext, attribute: string): any {
        if (attribute in context) {
            return (context as any)[attribute];
        }
        return context.attributes?.[attribute];
    }

    private isInRollout(flagKey: string, userId: string, percentage: number): boolean {
        const hash = this.hashUserFlag(userId, flagKey);
        return (hash % 100) < percentage;
    }

    private hashUserFlag(userId: string, flagKey: string): number {
        const str = `${userId}:${flagKey}`;
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash);
    }

    // Admin methods
    async createFlag(flag: FeatureFlag): Promise<void> {
        await this.redis.set(`feature:${flag.key}`, JSON.stringify(flag));
        this.localCache.delete(flag.key);
    }

    async updateFlag(key: string, updates: Partial<FeatureFlag>): Promise<void> {
        const existing = await this.getFlag(key);
        if (!existing) throw new Error('Flag not found');

        const updated = { ...existing, ...updates };
        await this.redis.set(`feature:${key}`, JSON.stringify(updated));
        this.localCache.delete(key);

        // Publish change event for other instances
        await this.redis.publish('feature-flag-updates', JSON.stringify({ key, action: 'update' }));
    }

    async deleteFlag(key: string): Promise<void> {
        await this.redis.del(`feature:${key}`);
        this.localCache.delete(key);
    }
}

export const featureFlags = new FeatureFlagService(redis);
```

### Express Middleware

```typescript
// middleware/featureFlags.ts
import { Request, Response, NextFunction } from 'express';
import { featureFlags } from '../services/featureFlag';

declare global {
    namespace Express {
        interface Request {
            features: {
                isEnabled: (flagKey: string) => Promise<boolean>;
                getVariant: (flagKey: string) => Promise<string | null>;
            };
        }
    }
}

export function featureFlagMiddleware(req: Request, res: Response, next: NextFunction) {
    const context = {
        userId: req.user?.id || req.sessionID,
        email: req.user?.email,
        plan: req.user?.plan,
        country: req.headers['cf-ipcountry'] as string,
        attributes: {
            userAgent: req.headers['user-agent'],
            platform: req.query.platform,
        },
    };

    req.features = {
        isEnabled: (flagKey: string) => featureFlags.isEnabled(flagKey, context),
        getVariant: (flagKey: string) => featureFlags.getVariant(flagKey, context),
    };

    next();
}

// Usage in route
app.get('/api/dashboard', async (req, res) => {
    const showNewDashboard = await req.features.isEnabled('new-dashboard');

    if (showNewDashboard) {
        return res.json(await getNewDashboardData());
    }
    return res.json(await getLegacyDashboardData());
});
```

## A/B Testing

### Experiment Configuration

```typescript
// experiments/config.ts
interface Experiment {
    key: string;
    name: string;
    description: string;
    variants: ExperimentVariant[];
    metrics: string[];
    startDate: Date;
    endDate?: Date;
    targetAudience?: TargetingRule[];
}

interface ExperimentVariant {
    key: string;
    name: string;
    weight: number;
    isControl: boolean;
}

const experiments: Experiment[] = [
    {
        key: 'checkout-flow-v2',
        name: 'New Checkout Flow',
        description: 'Testing simplified checkout process',
        variants: [
            { key: 'control', name: 'Current Flow', weight: 50, isControl: true },
            { key: 'treatment', name: 'Simplified Flow', weight: 50, isControl: false },
        ],
        metrics: ['conversion_rate', 'cart_abandonment', 'time_to_purchase'],
        startDate: new Date('2024-01-15'),
        endDate: new Date('2024-02-15'),
    },
];
```

### Analytics Integration

```typescript
// analytics/experiments.ts
import { Analytics } from '@segment/analytics-node';

const analytics = new Analytics({ writeKey: process.env.SEGMENT_WRITE_KEY! });

interface ExperimentEvent {
    userId: string;
    experimentKey: string;
    variantKey: string;
    properties?: Record<string, any>;
}

export function trackExperimentExposure(event: ExperimentEvent) {
    analytics.track({
        userId: event.userId,
        event: 'Experiment Viewed',
        properties: {
            experiment_key: event.experimentKey,
            variant_key: event.variantKey,
            ...event.properties,
        },
    });
}

export function trackExperimentConversion(
    userId: string,
    experimentKey: string,
    variantKey: string,
    metricName: string,
    value: number = 1
) {
    analytics.track({
        userId,
        event: 'Experiment Conversion',
        properties: {
            experiment_key: experimentKey,
            variant_key: variantKey,
            metric_name: metricName,
            metric_value: value,
        },
    });
}

// React hook for experiments
function useExperiment(experimentKey: string) {
    const { userId } = useUser();
    const [variant, setVariant] = useState<string | null>(null);

    useEffect(() => {
        async function loadVariant() {
            const v = await featureFlags.getVariant(experimentKey, { userId });
            setVariant(v);

            // Track exposure
            if (v) {
                trackExperimentExposure({
                    userId,
                    experimentKey,
                    variantKey: v,
                });
            }
        }
        loadVariant();
    }, [experimentKey, userId]);

    return { variant, isLoading: variant === null };
}

// Usage
function CheckoutPage() {
    const { variant } = useExperiment('checkout-flow-v2');

    return variant === 'treatment' ? <NewCheckout /> : <CurrentCheckout />;
}
```

## Gradual Rollout Strategies

### Percentage Rollout

```typescript
// Gradually increase rollout
async function incrementRollout(flagKey: string, increment: number = 10) {
    const flag = await featureFlags.getFlag(flagKey);
    const newPercentage = Math.min(100, flag.rolloutPercentage + increment);

    await featureFlags.updateFlag(flagKey, {
        rolloutPercentage: newPercentage,
    });

    console.log(`Rollout for ${flagKey}: ${flag.rolloutPercentage}% -> ${newPercentage}%`);
}

// Automated rollout with monitoring
async function automatedRollout(flagKey: string, config: {
    targetPercentage: number;
    incrementSize: number;
    intervalMinutes: number;
    errorThreshold: number;
}) {
    const { targetPercentage, incrementSize, intervalMinutes, errorThreshold } = config;

    while (true) {
        const flag = await featureFlags.getFlag(flagKey);

        if (flag.rolloutPercentage >= targetPercentage) {
            console.log('Rollout complete');
            break;
        }

        // Check error rates before proceeding
        const errorRate = await getErrorRateForFlag(flagKey);
        if (errorRate > errorThreshold) {
            console.error(`Error rate ${errorRate}% exceeds threshold. Halting rollout.`);
            await alertOncall(flagKey, errorRate);
            break;
        }

        await incrementRollout(flagKey, incrementSize);
        await sleep(intervalMinutes * 60 * 1000);
    }
}
```

### Ring-Based Rollout

```typescript
// Deployment rings
const ROLLOUT_RINGS = {
    canary: {
        percentage: 1,
        users: ['internal-testers'],
        duration: '1h',
    },
    earlyAdopters: {
        percentage: 5,
        attributes: { plan: 'enterprise' },
        duration: '4h',
    },
    beta: {
        percentage: 25,
        attributes: { betaOptIn: true },
        duration: '24h',
    },
    general: {
        percentage: 100,
        duration: null,
    },
};

async function ringRollout(flagKey: string, ring: keyof typeof ROLLOUT_RINGS) {
    const ringConfig = ROLLOUT_RINGS[ring];

    await featureFlags.updateFlag(flagKey, {
        rolloutPercentage: ringConfig.percentage,
        targetingRules: ringConfig.attributes ? [
            {
                attribute: Object.keys(ringConfig.attributes)[0],
                operator: 'eq',
                value: Object.values(ringConfig.attributes)[0],
                enabled: true,
            },
        ] : [],
    });

    console.log(`Rolled out ${flagKey} to ring: ${ring}`);
}
```

## Feature Flag Management UI

```typescript
// pages/api/admin/flags/[key].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { featureFlags } from '@/services/featureFlag';
import { requireAdmin } from '@/middleware/auth';

async function handler(req: NextApiRequest, res: NextApiResponse) {
    const { key } = req.query;

    switch (req.method) {
        case 'GET':
            const flag = await featureFlags.getFlag(key as string);
            return res.json(flag);

        case 'PUT':
            await featureFlags.updateFlag(key as string, req.body);

            // Audit log
            await auditLog.create({
                action: 'feature_flag_updated',
                flagKey: key,
                changes: req.body,
                user: req.user.email,
            });

            return res.json({ success: true });

        case 'DELETE':
            await featureFlags.deleteFlag(key as string);
            return res.json({ success: true });

        default:
            res.setHeader('Allow', ['GET', 'PUT', 'DELETE']);
            return res.status(405).end();
    }
}

export default requireAdmin(handler);
```

## Best Practices

### Flag Lifecycle

```typescript
// Flag metadata with lifecycle
interface FlagMetadata {
    key: string;
    owner: string;
    team: string;
    createdAt: Date;
    expiresAt?: Date;
    jiraTicket?: string;
    description: string;
    type: 'release' | 'experiment' | 'ops' | 'permission';
}

// Cleanup stale flags
async function cleanupStaleFlags() {
    const flags = await featureFlags.listAll();
    const now = new Date();

    for (const flag of flags) {
        if (flag.expiresAt && new Date(flag.expiresAt) < now) {
            if (flag.rolloutPercentage === 100) {
                // Flag is fully rolled out - notify to remove code
                await notifyFlagRemoval(flag);
            } else if (flag.rolloutPercentage === 0) {
                // Flag never used - safe to delete
                await featureFlags.deleteFlag(flag.key);
            }
        }
    }
}
```

### Testing with Feature Flags

```typescript
// test/features.test.ts
describe('Feature: New Checkout', () => {
    beforeEach(() => {
        // Force flag state for tests
        jest.spyOn(featureFlags, 'isEnabled').mockImplementation(
            async (key) => key === 'new-checkout'
        );
    });

    it('shows new checkout when flag is enabled', async () => {
        render(<CheckoutPage />);
        expect(await screen.findByTestId('new-checkout')).toBeInTheDocument();
    });

    it('shows legacy checkout when flag is disabled', async () => {
        jest.spyOn(featureFlags, 'isEnabled').mockResolvedValue(false);

        render(<CheckoutPage />);
        expect(await screen.findByTestId('legacy-checkout')).toBeInTheDocument();
    });
});
```

### Monitoring Dashboard

```yaml
# Grafana dashboard queries
panels:
  - title: Feature Flag Evaluations
    query: |
      sum(rate(feature_flag_evaluations_total[5m])) by (flag_key, result)

  - title: Experiment Conversion Rates
    query: |
      sum(experiment_conversions_total) by (experiment_key, variant_key)
      /
      sum(experiment_exposures_total) by (experiment_key, variant_key)

  - title: Error Rate by Flag
    query: |
      sum(rate(http_errors_total{feature_flag!=""}[5m])) by (feature_flag)
      /
      sum(rate(http_requests_total{feature_flag!=""}[5m])) by (feature_flag)
```

## Integration Examples

### LaunchDarkly Setup

```typescript
// launchdarkly.ts
import LaunchDarkly from 'launchdarkly-node-server-sdk';

const client = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY!);

await client.waitForInitialization();

// Evaluate flag
const user = {
    key: userId,
    email: userEmail,
    custom: {
        plan: userPlan,
        createdAt: userCreatedAt,
    },
};

const showFeature = await client.variation('feature-key', user, false);
```

### Unleash Setup

```typescript
// unleash.ts
import { initialize, isEnabled } from 'unleash-client';

const unleash = initialize({
    url: 'https://unleash.example.com/api',
    appName: 'my-app',
    customHeaders: {
        Authorization: process.env.UNLEASH_API_TOKEN!,
    },
});

unleash.on('ready', () => {
    console.log('Unleash client ready');
});

// Check flag
const enabled = isEnabled('my-feature', {
    userId: user.id,
    properties: {
        email: user.email,
    },
});
```

## Summary

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| Simple Toggle | Kill switches, maintenance mode | Low |
| Percentage Rollout | Gradual releases | Medium |
| User Targeting | Beta users, specific segments | Medium |
| A/B Testing | Conversion optimization | High |
| Multivariate | Multiple variants testing | High |
