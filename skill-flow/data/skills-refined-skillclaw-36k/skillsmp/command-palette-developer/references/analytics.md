# Analytics & Telemetry

Tracking command usage, search patterns, and user behavior (reference only - not included in examples).

## Event Tracking

```typescript
interface AnalyticsEvent {
  type: 'palette_opened' | 'command_executed' | 'search_performed';
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

function trackEvent(event: AnalyticsEvent) {
  // Send to your analytics service
  analytics.track(event.type, {
    ...event.metadata,
    timestamp: event.timestamp,
  });
}

// Usage
function CommandPalette() {
  const { setOpen } = useCommandStore();

  function openPalette() {
    setOpen(true);
    trackEvent({ type: 'palette_opened', timestamp: new Date() });
  }

  return <Palette onOpen={openPalette} />;
}
```

## Metrics to Track

- **Command usage frequency:** Which commands are used most
- **Search queries:** What users search for (identify missing commands)
- **Time to select:** How long users take to find commands
- **Abandonment rate:** Users who open but don't select
- **Popular shortcuts:** Which keyboard shortcuts are used

## Privacy Considerations

- **Opt-in:** Ask users before tracking
- **Anonymize:** Don't track PII or sensitive search terms
- **Transparency:** Document what's tracked and why
- **Control:** Allow users to disable tracking

```typescript
const TRACKING_ENABLED = getUserPreference('analytics_enabled');

function trackEvent(event: AnalyticsEvent) {
  if (!TRACKING_ENABLED) return;
  // ... track event
}
```
