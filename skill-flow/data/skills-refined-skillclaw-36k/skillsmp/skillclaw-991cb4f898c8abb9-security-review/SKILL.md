---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. It provides a comprehensive security checklist and patterns to ensure best practices.
---

# Security Review Skill

This skill ensures all code follows security best practices and identifies potential vulnerabilities.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Implementing payment features
- Storing or transmitting sensitive data
- Integrating third-party APIs

## Security Checklist

### 1. Secrets Management

#### ❌ NEVER Do This
```typescript
const apiKey = "sk-proj-xxxxx"; // Hardcoded secret
const dbPassword = "password123"; // In source code
```

#### ✅ ALWAYS Do This
```typescript
const apiKey = process.env.OPENAI_API_KEY;
const dbUrl = process.env.DATABASE_URL;

// Verify secrets exist
if (!apiKey) {
  throw new Error("OPENAI_API_KEY not configured");
}
```

#### Verification Steps
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets in environment variables
- [ ] `.env.local` in .gitignore
- [ ] No secrets in git history
- [ ] Production secrets in hosting platform (Vercel, Railway)

### 2. Input Validation

#### Always Validate User Input
```typescript
import { z } from "zod";

// Define validation schema
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150),
});

// Validate before processing
export async function createUser(input: unknown) {
  try {
    const validated = CreateUserSchema.parse(input);
    return await db.users.create(validated);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors };
    }
    throw error;
  }
}
```

#### File Upload Validation
```typescript
function validateFileUpload(file: File) {
  // Size check (5MB max)
  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) {
    throw new Error("File too large (max 5MB)");
  }

  // Type check
  const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
  if (!allowedTypes.includes(file.type)) {
    throw new Error("Invalid file type");
  }

  // Extension check
  const allowedExtensions = [".jpg", ".jpeg", ".png", ".gif"];
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0];
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error("Invalid file extension");
  }

  return true;
}
```

### 3. SQL Injection Prevention

#### ❌ NEVER Do This
```typescript
// Dangerous - SQL injection vulnerability
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;
await db.query(query);
```

#### ✅ ALWAYS Use Parameterized Queries
```typescript
const query = 'SELECT * FROM users WHERE email = ?';
await db.query(query, [userEmail]);
```