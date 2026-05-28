# Monitoring Pitfalls

## Monitoring Pitfalls

### Pitfall 16: Alert Fatigue
```yaml
# ❌ BAD: Alert on every error
alert_rules:
  - condition: any_error
    action: email_team  # Hundreds of emails!

# ✅ GOOD: Threshold-based alerts
alert_rules:
  - condition: error_rate > 5%
    action: slack_warning
  - condition: error_rate > 20%
    action: pagerduty_critical
```

### Pitfall 17: Ignoring Release Health
```typescript
// ❌ BAD: No release tracking
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  // No release specified
});

// ✅ GOOD: Track releases
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: `myapp@${process.env.GIT_SHA}`,
  autoSessionTracking: true,
});
```