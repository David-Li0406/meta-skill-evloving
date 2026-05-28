---
name: api-security-basics
description: Use this skill when applying security best practices for API keys and access control across various platforms.
---

# API Security Basics

## Overview
This skill provides security best practices for managing API keys, tokens, and access control across different platforms such as Groq, Vercel, and Exa.

## Prerequisites
- Relevant SDK installed (Groq, Vercel, Exa)
- Understanding of environment variables
- Access to the respective dashboard

## Instructions

### Step 1: Configure Environment Variables
```bash
# .env (NEVER commit to git)
API_KEY=sk_live_***
SECRET=***

# .gitignore
.env
.env.local
.env.*.local
```

### Step 2: Implement Secret Rotation
```bash
# 1. Generate new key in the respective dashboard
# 2. Update environment variable
export API_KEY="new_key_here"

# 3. Verify new key works
curl -H "Authorization: Bearer ${API_KEY}" \
  https://api.example.com/health

# 4. Revoke old key in the dashboard
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
  reader: new ApiClient({
    apiKey: process.env.READ_KEY,
  }),
  writer: new ApiClient({
    apiKey: process.env.WRITE_KEY,
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