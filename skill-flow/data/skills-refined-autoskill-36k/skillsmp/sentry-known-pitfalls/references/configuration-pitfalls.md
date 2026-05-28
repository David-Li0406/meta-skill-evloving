# Configuration Pitfalls

## Configuration Pitfalls

### Pitfall 7: Hardcoded DSN
```typescript
// ❌ BAD: DSN in code
Sentry.init({
  dsn: 'https://abc123@sentry.io/123', // Exposed!
});

// ✅ GOOD: Environment variable
Sentry.init({
  dsn: process.env.SENTRY_DSN,
});
```

### Pitfall 8: 100% Sampling in Production
```typescript
// ❌ BAD: Full sampling = huge bills
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0, // 100% of all requests!
});

// ✅ GOOD: Production-appropriate rates
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
});
```

### Pitfall 9: Ignoring beforeSend Return
```typescript
// ❌ BAD: Not returning event
Sentry.init({
  beforeSend(event) {
    console.log('Event:', event);
    // Forgot to return! Event is dropped.
  },
});

// ✅ GOOD: Always return event (or null to drop)
Sentry.init({
  beforeSend(event) {
    console.log('Event:', event);
    return event; // Don't forget!
  },
});
```