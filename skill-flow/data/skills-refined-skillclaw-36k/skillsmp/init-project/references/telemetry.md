# Telemetry Service

A comprehensive observability stack with **Sentry** for error tracking and tracing, **PostHog** for product analytics, and **OpenTelemetry** bridging Effect-TS spans.

## Libraries

| Package                   | Purpose                                 |
| ------------------------- | --------------------------------------- |
| `@sentry/nextjs`          | Error tracking and tracing for Next.js  |
| `@sentry/opentelemetry`   | Bridge OpenTelemetry spans to Sentry    |
| `@effect/opentelemetry`   | Bridge Effect-TS spans to OpenTelemetry |
| `@opentelemetry/sdk-logs` | OpenTelemetry logging SDK               |
| `posthog-js`              | Client-side product analytics           |
| `posthog-node`            | Server-side PostHog client (optional)   |
| `effect`                  | Functional programming primitives       |

## File Structure

```
# Project root
instrumentation.ts          # Server-side Sentry init
instrumentation-client.ts   # Client-side PostHog init

# Telemetry service
lib/services/telemetry/
├── live-layer.ts           # OpenTelemetry Effect Layer
├── report-error.ts         # Error reporting utility
└── report-warning.ts       # Warning reporting utility

# PostHog service (optional)
lib/services/posthog/
├── service.ts              # PostHog service interface
├── live-layer.ts           # PostHog Effect implementation
└── errors.ts               # Tagged errors

# Utilities
lib/utils/
└── db-retry-policy.ts      # Retry policy with warning telemetry
```

## Scaffolding from Scratch

### 1. Install Dependencies

```bash
# Core telemetry
npm install @sentry/nextjs @sentry/opentelemetry @effect/opentelemetry @opentelemetry/sdk-logs

# Product analytics
npm install posthog-js

# Server-side PostHog (optional)
npm install posthog-node
```

### 2. Initialize Sentry

Run the Sentry wizard:

```bash
npx @sentry/wizard@latest -i nextjs
```

Or manually create `instrumentation.ts`:

```typescript
// instrumentation.ts (project root)
import * as Sentry from '@sentry/nextjs'

export async function register() {
  const isProduction = process.env.NODE_ENV === 'production'
  const telemetryEnabled = isProduction || process.env.ENABLE_TELEMETRY === 'true'

  Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV,
    enabled: telemetryEnabled,

    // Tracing
    tracesSampleRate: isProduction ? 0.1 : 1.0, // 10% in prod, 100% in dev

    // Session Replay (optional, can use PostHog instead)
    replaysSessionSampleRate: 0,
    replaysOnErrorSampleRate: 0,

    debug: false
  })
}
```

### 3. Initialize PostHog (`instrumentation-client.ts`)

```typescript
// instrumentation-client.ts (project root)
import posthog from 'posthog-js'

if (typeof window !== 'undefined') {
  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
    // Reverse proxy to bypass ad-blockers
    api_host: '/ph',
    ui_host: 'https://us.posthog.com', // or 'https://eu.posthog.com'

    person_profiles: 'always',
    capture_pageview: true,
    capture_pageleave: true
  })
}
```

### 4. Create OpenTelemetry Layer (`lib/services/telemetry/live-layer.ts`)

```typescript
import { NodeSdk } from '@effect/opentelemetry'
import { SentrySpanProcessor } from '@sentry/opentelemetry'
import { BatchLogRecordProcessor, ConsoleLogRecordExporter } from '@opentelemetry/sdk-logs'

export const TelemetryLayer = NodeSdk.layer(() => {
  const environment = process.env.NODE_ENV || 'development'
  const serviceVersion = process.env.npm_package_version || '1.0.0'

  return {
    resource: {
      serviceName: 'my-app',
      serviceVersion,
      attributes: {
        'deployment.environment': environment
      }
    },

    // Sentry receives all spans via OpenTelemetry bridge
    spanProcessor: new SentrySpanProcessor(),

    // Logs go to console (Sentry captures as breadcrumbs)
    logRecordProcessor: new BatchLogRecordProcessor(new ConsoleLogRecordExporter()),

    // Shutdown timeout for serverless
    shutdownTimeout: '5 seconds'
  }
})
```

### 5. Create Error Reporting (`lib/services/telemetry/report-error.ts`)

```typescript
import { Effect } from 'effect'
import * as Sentry from '@sentry/nextjs'

export const reportError = <E extends { _tag: string; message: string }>(
  error: E,
  context?: Record<string, unknown>
) =>
  Effect.gen(function* () {
    const errorTag = error._tag
    const errorMessage = error.message

    // Log to console
    yield* Effect.logError(errorMessage, {
      error_type: errorTag,
      ...context
    })

    // Capture in Sentry
    yield* Effect.sync(() =>
      Sentry.captureException(error, {
        tags: {
          error_type: errorTag
        },
        extra: {
          ...context,
          errorDetails: error
        }
      })
    )
  })
```

### 6. Create Warning Reporting (`lib/services/telemetry/report-warning.ts`)

```typescript
import { Effect } from 'effect'
import * as Sentry from '@sentry/nextjs'

export const reportWarning = <W extends { _tag: string; message: string }>(
  warning: W,
  context?: Record<string, unknown>
) =>
  Effect.gen(function* () {
    const warningTag = warning._tag
    const warningMessage = warning.message

    // Log to console
    yield* Effect.logWarning(warningMessage, {
      warning_type: warningTag,
      ...context
    })

    // Send to Sentry at warning level
    yield* Effect.sync(() =>
      Sentry.captureMessage(warningMessage, {
        level: 'warning',
        tags: { warning_type: warningTag },
        extra: { ...context, warningDetails: warning }
      })
    )
  })
```

### 7. Create Retry Policy with Telemetry (`lib/utils/db-retry-policy.ts`)

```typescript
import { Schedule, Effect } from 'effect'
import { reportWarning } from '@/lib/services/telemetry/report-warning'

// Base policy without telemetry
export const dbRetryPolicy = Schedule.exponential('500 millis', 2.0).pipe(
  Schedule.intersect(Schedule.recurs(3))
)

// Policy with automatic warning on each retry
export const dbRetryPolicyWithWarning = (operation: string, context?: Record<string, unknown>) =>
  Schedule.exponential('500 millis', 2.0).pipe(
    Schedule.intersect(Schedule.recurs(3)),
    Schedule.tapInput((error: { _tag: string; message: string }) =>
      reportWarning(error, {
        operation: `${operation}-retry`,
        note: 'Operation required retry due to transient failure',
        ...context
      })
    )
  )
```

### 8. Create Layer Composition (`lib/layers.ts`)

```typescript
import { Layer } from 'effect'
import { TelemetryLayer } from './services/telemetry/live-layer'
import { DbLayer } from './services/db'
import { AuthLayer } from './services/auth'

export const AppLayer = Layer.mergeAll(TelemetryLayer, DbLayer, AuthLayer)
```

### 9. Configure PostHog Reverse Proxy (Next.js)

Create a rewrite in `next.config.js`:

```javascript
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/ph/static/:path*',
        destination: 'https://us-assets.i.posthog.com/static/:path*'
      },
      {
        source: '/ph/:path*',
        destination: 'https://us.i.posthog.com/:path*'
      }
    ]
  }
}
```

## Usage Patterns

### Creating Spans

```typescript
import { Effect } from 'effect'

export const createUser = (data: UserInput) =>
  Effect.gen(function* () {
    // Add context at operation start
    yield* Effect.annotateCurrentSpan({
      operation: 'user.create',
      'user.email': data.email
    })

    const user = yield* insertUser(data)

    // Add result context
    yield* Effect.annotateCurrentSpan({
      'user.id': user.id
    })

    return user
  }).pipe(
    Effect.retry(dbRetryPolicyWithWarning('create-user')),
    Effect.withSpan('user.create'),
    Effect.tapError(error => reportError(error, { operation: 'create-user' }))
  )
```

### Span Naming Convention

Format: `{domain}.{entity}.{action}`

```typescript
// Data operations
Effect.withSpan('user.create')
Effect.withSpan('post.query.by-id')
Effect.withSpan('comment.delete')

// External services
Effect.withSpan('stripe.payment.create')
Effect.withSpan('s3.object.upload')

// Server actions
Effect.withSpan('action.user.invite')
Effect.withSpan('action.post.publish')
```

### Critical Pattern: Retry Before Span

The span must capture total duration including retries:

```typescript
// CORRECT
Effect.gen(function* () {
  yield* Effect.annotateCurrentSpan({ operation: 'entity.action' })
  return yield* someOperation()
}).pipe(
  Effect.retry(retryPolicy), // 1. Retry FIRST
  Effect.withSpan('domain.entity.op'), // 2. Span AFTER retry
  Effect.tapError(reportError) // 3. Report final errors
)

// WRONG - each retry creates separate span
Effect.withSpan('operation').pipe(Effect.retry(policy))
```

### Reporting Errors

```typescript
import { reportError } from '@/lib/services/telemetry/report-error'

export const deletePost = (postId: string) =>
  Effect.gen(function* () {
    // ... operation
  }).pipe(
    Effect.withSpan('post.delete'),
    Effect.tapError(error => reportError(error, { operation: 'delete-post', postId }))
  )
```

### Skipping Expected Errors

Don't report business logic errors (404, 401):

```typescript
Effect.tapError(error => {
  // Skip expected errors
  if (error._tag === 'NotFoundError') return Effect.void
  if (error._tag === 'UnauthenticatedError') return Effect.void
  if (error._tag === 'UnauthorizedError') return Effect.void

  // Report unexpected errors
  return reportError(error, { operation: 'some-operation' })
})
```

### Complete Server Action Pattern

```typescript
'use server'

import { Effect, Layer, Match } from 'effect'
import { NextEffect } from '@/lib/next-effect'
import { AppLayer } from '@/lib/layers'
import { getSessionEffect } from '@/lib/services/auth'
import { reportError } from '@/lib/services/telemetry/report-error'

export const deletePostAction = async (postId: string) => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      // 1. Annotate span with input
      yield* Effect.annotateCurrentSpan({
        'post.id': postId,
        operation: 'post.delete'
      })

      // 2. Auth check
      const { user } = yield* getSessionEffect()

      // 3. Annotate with user context
      yield* Effect.annotateCurrentSpan({
        'user.id': user.id,
        'user.role': user.role
      })

      // 4. Verify access
      const post = yield* verifyPostAccess(postId)

      // 5. Perform operation
      return yield* deletePost(postId)
    }).pipe(
      Effect.withSpan('action.post.delete'),
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error =>
          Match.value(error._tag).pipe(
            // Expected errors - redirect, don't report
            Match.when('UnauthenticatedError', () => NextEffect.redirect('/login')),
            Match.when('UnauthorizedError', () => NextEffect.redirect('/')),
            Match.when('PostNotFoundError', () =>
              Effect.succeed({ _tag: 'Error' as const, message: 'Post not found' })
            ),
            // Unexpected errors - report to Sentry
            Match.orElse(() => {
              reportError(error, { operation: 'action.post.delete', postId })
              return Effect.succeed({ _tag: 'Error' as const, message: 'Something went wrong' })
            })
          ),
        onSuccess: () =>
          Effect.sync(() => {
            revalidatePath('/posts')
            return { _tag: 'Success' as const }
          })
      })
    )
  )
}
```

### PostHog Client-Side Events

```typescript
'use client'

import posthog from 'posthog-js'

// Track custom event
posthog.capture('post_created', {
  post_id: '123',
  category: 'tech'
})

// Identify user
posthog.identify(userId, {
  email: user.email,
  name: user.name,
  plan: user.plan
})

// Track page view (usually automatic)
posthog.capture('$pageview')
```

### PostHog Server-Side (Optional)

```typescript
// lib/services/posthog/service.ts
import { PostHog } from 'posthog-node'
import { Context, Effect, Layer, Config } from 'effect'

export class PostHogClient extends Context.Tag('@app/PostHog')<PostHogClient, PostHog>() {}

export const PostHogLive = Layer.scoped(
  PostHogClient,
  Effect.gen(function* () {
    const apiKey = yield* Config.string('POSTHOG_API_KEY')

    const client = new PostHog(apiKey, {
      host: 'https://us.i.posthog.com'
    })

    // Ensure shutdown on scope close
    yield* Effect.addFinalizer(() => Effect.promise(() => client.shutdown()))

    return client
  })
)
```

## Best Practices

### 1. Always Annotate Spans with Context

Add relevant IDs and operation names:

```typescript
yield *
  Effect.annotateCurrentSpan({
    operation: 'post.create',
    'post.id': postId,
    'user.id': userId,
    'post.status': status
  })
```

### 2. Use Tagged Errors for Filtering

Tag errors to enable Sentry filtering:

```typescript
Sentry.captureException(error, {
  tags: { error_type: error._tag }
})

// In Sentry: error_type:DatabaseError
```

### 3. Report at Granular Failure Points

Report errors where they occur, not in orchestration:

```typescript
// Good - reports at failure point
export const createPost = (data) =>
  Effect.gen(function* () { ... })
    .pipe(Effect.tapError(error => reportError(error, { operation: 'create-post' })))

// Bad - reports all errors generically
export const handleRequest = () =>
  Effect.gen(function* () {
    yield* createPost(data)
    yield* sendEmail(data)
  }).pipe(Effect.tapError(reportError)) // No context about which operation failed
```

### 4. Don't Report Expected Business Errors

Skip 404s, 401s, validation errors:

```typescript
Effect.tapError(error => {
  if (['NotFoundError', 'UnauthorizedError', 'ValidationError'].includes(error._tag)) {
    return Effect.void
  }
  return reportError(error, context)
})
```

### 5. Use Warnings for Retries

Track when operations need retries (signals infrastructure issues):

```typescript
Schedule.tapInput(error => reportWarning(error, { operation: `${operationName}-retry` }))
```

### 6. Sample Traces in Production

Reduce costs with appropriate sampling:

```typescript
Sentry.init({
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0
})
```

### 7. Use PostHog Reverse Proxy

Bypass ad-blockers for accurate analytics:

```typescript
posthog.init(key, {
  api_host: '/ph' // Reverse proxy, not direct PostHog URL
})
```

## Environment Variables

| Variable                  | Required | Description                 |
| ------------------------- | -------- | --------------------------- |
| `SENTRY_DSN`              | Yes      | Sentry project DSN          |
| `NEXT_PUBLIC_POSTHOG_KEY` | Yes      | PostHog project API key     |
| `POSTHOG_API_KEY`         | No       | Server-side PostHog key     |
| `ENABLE_TELEMETRY`        | No       | Force enable in development |

## Data Flow

```
Browser                         Server
  |                               |
  |-- PostHog pageview ---------> PostHog (via /ph proxy)
  |                               |
  |                           [Effect.withSpan()]
  |                               |
  |                           [@effect/opentelemetry NodeSdk]
  |                               |
  |                           [SentrySpanProcessor]
  |                               |
  |                           --> Sentry (traces)
  |                               |
  |                           [reportError()]
  |                               |
  |                           --> Sentry (events)
  |                           --> Console (logs)
```

## Anti-Patterns to Avoid

1. **Never put `Effect.withSpan` BEFORE `Effect.retry`** - span must track total duration
2. **Never report expected errors** (NotFound, Unauthorized) - these are not bugs
3. **Never use top-level error reporting in actions** - report at granular failure points
4. **Never access Sentry directly in Effect generators** - use `Effect.sync()` wrapper
5. **Never forget to add operation context** to spans and error reports
