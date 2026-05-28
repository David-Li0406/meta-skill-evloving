# Examples

### Quick Performance Wrapper
```typescript
const withPerformance = <T>(name: string, fn: () => Promise<T>) =>
  measuredVercelCall(name, () =>
    cachedVercelRequest(`cache:${name}`, fn)
  );
```