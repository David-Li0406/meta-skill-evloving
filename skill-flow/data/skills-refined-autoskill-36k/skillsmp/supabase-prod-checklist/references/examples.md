# Examples

### Health Check Implementation
```typescript
async function healthCheck(): Promise<{ status: string; supabase: any }> {
  const start = Date.now();
  try {
    await supabaseClient.ping();
    return { status: 'healthy', supabase: { connected: true, latencyMs: Date.now() - start } };
  } catch (error) {
    return { status: 'degraded', supabase: { connected: false, latencyMs: Date.now() - start } };
  }
}
```

### Immediate Rollback
```bash
kubectl rollout undo deployment/supabase-integration
kubectl rollout status deployment/supabase-integration
```