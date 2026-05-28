# Codex Consult Output Format

## Overview

The codex-consult skill produces structured output in three main sections, designed to provide actionable guidance for implementation tasks.

## Output Structure

### 1. Summary Section

The summary provides a high-level overview of the proposed approach.

**Contents:**
- What changes are being proposed
- Key assumptions made
- Prerequisites and dependencies
- Impact analysis (files affected, potential risks)

**Example:**
```markdown
## Summary

This implementation adds JWT-based authentication to the API.

**Assumptions:**
- Using RS256 algorithm for token signing
- Tokens expire after 1 hour
- Refresh tokens are stored in HTTP-only cookies

**Prerequisites:**
- jsonwebtoken package installed
- RSA key pair generated

**Impact:**
- Modifies: src/middleware/auth.ts, src/routes/login.ts
- Creates: src/utils/jwt.ts, src/types/auth.ts
```

### 2. Implementation/Changes Section

#### Plan Mode
Provides step-by-step implementation strategy without actual code changes.

**Example:**
```markdown
## Implementation Approach

### Step 1: Create JWT utility module
- File: src/utils/jwt.ts
- Functions: generateToken(), verifyToken(), refreshToken()
- Handle key loading and error cases

### Step 2: Implement auth middleware
- File: src/middleware/auth.ts
- Extract token from Authorization header
- Verify and decode token
- Attach user info to request object

### Step 3: Update login route
- File: src/routes/login.ts
- Validate credentials
- Generate and return tokens
```

#### Patch Mode
Provides concrete code changes in unified diff format.

**Example:**
```markdown
## Proposed Changes

### src/utils/jwt.ts (new file)
\`\`\`diff
--- /dev/null
+++ b/src/utils/jwt.ts
@@ -0,0 +1,25 @@
+import jwt from 'jsonwebtoken';
+import { readFileSync } from 'fs';
+
+const privateKey = readFileSync('./keys/private.pem');
+const publicKey = readFileSync('./keys/public.pem');
+
+export function generateToken(payload: object): string {
+  return jwt.sign(payload, privateKey, {
+    algorithm: 'RS256',
+    expiresIn: '1h'
+  });
+}
\`\`\`

### src/middleware/auth.ts
\`\`\`diff
--- a/src/middleware/auth.ts
+++ b/src/middleware/auth.ts
@@ -1,5 +1,20 @@
+import { verifyToken } from '../utils/jwt';
+
 export function authMiddleware(req, res, next) {
-  // TODO: implement
+  const authHeader = req.headers.authorization;
+  if (!authHeader?.startsWith('Bearer ')) {
+    return res.status(401).json({ error: 'No token provided' });
+  }
+
+  const token = authHeader.slice(7);
+  try {
+    const decoded = verifyToken(token);
+    req.user = decoded;
+    next();
+  } catch (error) {
+    return res.status(401).json({ error: 'Invalid token' });
+  }
 }
\`\`\`
```

### 3. Verification Section

Provides steps to validate the implementation.

**Example:**
```markdown
## Verification Steps

### Automated Tests
\`\`\`bash
# Run unit tests
npm test src/utils/jwt.test.ts

# Run integration tests
npm test src/routes/login.test.ts
\`\`\`

### Manual Verification
1. Start the development server: `npm run dev`
2. Test login endpoint:
   \`\`\`bash
   curl -X POST http://localhost:3000/login \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "test123"}'
   \`\`\`
3. Use returned token for authenticated request:
   \`\`\`bash
   curl http://localhost:3000/api/profile \
     -H "Authorization: Bearer <token>"
   \`\`\`

### Edge Cases to Check
- [ ] Expired token returns 401
- [ ] Malformed token returns 401
- [ ] Missing Authorization header returns 401
- [ ] Valid token allows access
- [ ] Token refresh works correctly
```

## Output Files

| File | Purpose |
|------|---------|
| `/tmp/codex-consult.last.md` | Final Codex response |
| `/tmp/codex-consult.run.log` | Execution log with metadata |

## Parsing Tips

### Extract Summary
```bash
sed -n '/^## Summary/,/^## /p' /tmp/codex-consult.last.md | head -n -1
```

### Extract Diffs
```bash
grep -A 100 '```diff' /tmp/codex-consult.last.md | grep -B 100 '```'
```

### Check for Errors
```bash
if grep -q "Error:" /tmp/codex-consult.run.log; then
  echo "Execution had errors"
fi
```
