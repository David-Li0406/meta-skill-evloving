---
name: security-basics
description: Use this skill when applying security best practices for API keys and access control across various platforms like Groq, Vercel, and Exa.
---

# Security Basics

## Overview
This skill provides security best practices for managing API keys, tokens, and access control across different platforms.

## Prerequisites
- SDK for the respective platform (Groq, Vercel, Exa) installed
- Understanding of environment variables
- Access to the respective platform's dashboard

## Instructions

### Step 1: Configure Environment Variables
```bash
# .env (NEVER commit to git)
PLATFORM_API_KEY=sk_live_***
PLATFORM_SECRET=***

# .gitignore
.env
.env.local
.env.*.local
```

### Step 2: Implement Secret Rotation
```bash
# 1. Generate new key in the platform's dashboard
# 2. Update environment variable
export PLATFORM_API_KEY="new_key_here"

# 3. Verify new key works
curl -H "Authorization: Bearer ${PLATFORM_API_KEY}" \
  https://api.platform.com/health

# 4. Revoke old key in dashboard
```

### Step 3: Apply Least Privilege
| Environment | Recommended Scopes |
|-------------|-------------------|
| Development | `read:*` |
| Staging | `read:*, write:limited` |
| Production | `Only required scopes` |

## Output
- Secure API key storage
- Environment-specific access controls
- Audit logging enabled

## Error Handling
| Security Issue | Detection | Mitigation |
|----------------|-----------|------------|
| Exposed API key | Git scanning | Rotate immediately |
| Excessive scopes | Audit logs | Reduce permissions |
| Missing rotation | Key age check | Schedule rotation |

## Examples

### Service Account Pattern
```typescript
const clients = {
  reader: new PlatformClient({
    apiKey: process.env.PLATFORM_READ_KEY,
  }),
  writer: new PlatformClient({
    apiKey: process.env.PLATFORM_WRITE_KEY,
  }),
};
```

### Webhook Signature Verification
```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  payload: string, signature: string, secret: string
): boolean {
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

### Security Checklist
- [ ] API keys in environment variables
- [ ] `.env` files in `.gitignore`
- [ ] Different keys for dev/staging/prod
- [ ] Minimal scopes per environment
- [ ] Webhook signatures validated
- [ ] Audit logging enabled

### Audit Logging
```typescript
interface AuditEntry {
  timestamp: Date;
  action: string;
  userId: string;
  resource: string;
  result: 'success' | 'failure';
  metadata?: Record<string, any>;
}

async function auditLog(entry: Omit<AuditEntry, 'timestamp'>): Promise<void> {
  const log: AuditEntry = { ...entry, timestamp: new Date() };

  // Log to platform analytics
  await platformClient.track('audit', log);

  // Also log locally for compliance
  console.log('[AUDIT]', JSON.stringify(log));
}

// Usage
await auditLog({
  action: 'platform.api.call',
  userId: currentUser.id,
  resource: '/v1/resource',
  result: 'success',
});
```

## Resources
- [Platform Security Guide](https://docs.platform.com/security)
- [Platform API Scopes](https://docs.platform.com/scopes)

## Next Steps
For production deployment, see the respective platform's production checklist.