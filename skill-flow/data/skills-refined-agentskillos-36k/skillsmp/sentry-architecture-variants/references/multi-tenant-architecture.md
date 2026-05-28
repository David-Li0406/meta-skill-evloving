# Multi-Tenant Architecture

## Multi-Tenant Architecture

### Tenant Isolation
```typescript
Sentry.init({
  dsn: process.env.SENTRY_DSN,

  beforeSend(event) {
    // Add tenant context
    const tenantId = getCurrentTenantId();
    if (tenantId) {
      event.tags = {
        ...event.tags,
        tenant_id: tenantId,
      };
      event.user = {
        ...event.user,
        tenant: tenantId,
      };
    }
    return event;
  },
});

// Filter by tenant in dashboard
// Query: tags.tenant_id:acme-corp
```

### Per-Tenant Projects (Enterprise)
```
Organization: mycompany
├── Project: platform-shared      # Platform errors
├── Project: tenant-acme         # ACME Corp errors
├── Project: tenant-globex       # Globex errors
└── Project: tenant-initech      # Initech errors
```