# Examples

### Mock Supabase Responses
```typescript
vi.mock('@supabase/supabase-js', () => ({
  SupabaseClient: vi.fn().mockImplementation(() => ({
    // Mock methods here
  })),
}));
```

### Debug Mode
```bash
# Enable verbose logging
DEBUG=SUPABASE=* npm run dev
```