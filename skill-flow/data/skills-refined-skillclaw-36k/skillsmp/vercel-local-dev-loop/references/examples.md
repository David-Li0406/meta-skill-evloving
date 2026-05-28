# Examples

### Mock Vercel Responses
```typescript
vi.mock('vercel', () => ({
  VercelClient: vi.fn().mockImplementation(() => ({
    // Mock methods here
  })),
}));
```

### Debug Mode
```bash
# Enable verbose logging
DEBUG=VERCEL=* npm run dev
```