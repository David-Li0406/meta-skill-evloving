---
name: security-review
description: Use this skill when implementing authentication, handling user input, managing sensitive information, creating API endpoints, or implementing payment features. It provides a comprehensive security checklist and patterns.
---

# Security Review Skill

This skill ensures that all code adheres to security best practices and identifies potential vulnerabilities.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Managing sensitive information or credentials
- Implementing payment features
- Storing or transmitting sensitive data
- Integrating third-party APIs

## Security Checklist

### 1. Secret Management

#### ❌ Never do this
```typescript
const apiKey = "sk-proj-xxxxx"  // Hardcoded secret
const dbPassword = "password123" // In source code
```

#### ✅ Always do this
```typescript
const apiKey = process.env.OPENAI_API_KEY
const dbUrl = process.env.DATABASE_URL

// Verify secret exists
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

#### Verification Steps
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets are in environment variables
- [ ] `.env.local` is in .gitignore
- [ ] No secrets in git history
- [ ] Production secrets configured in hosting platforms (Vercel, Railway)

### 2. Input Validation

#### Always validate user input
```typescript
import { z } from 'zod'

// Define validation schema
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

// Pre-processing validation
export async function createUser(input: unknown) {
  try {
    const validated = CreateUserSchema.parse(input)
    return await db.users.create(validated)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors }
    }
    throw error
  }
}
```

#### File Upload Validation
```typescript
function validateFileUpload(file: File) {
  // Size check (max 5MB)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('File too large (max 5MB)')
  }

  // Type check
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type')
  }

  // Extension check
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif']
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error('Invalid file extension')
  }

  return true
}
```

#### Verification Steps
- [ ] All user inputs are validated using schema
- [ ] File uploads are restricted (size, type, extension)
- [ ] User inputs are not used directly in queries
- [ ] Whitelist validation is used (not blacklist)
- [ ] Error messages do not leak sensitive information

### 3. SQL Injection Prevention

#### ❌ Never concatenate SQL
```typescript
// Dangerous - SQL injection vulnerability
const query = `SELECT * FROM users WHERE email = '${userEmail}'`
await db.query(query)
```

#### ✅ Always use parameterized queries
```typescript
// Safe - Parameterized query
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// Or using raw SQL
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
)
```

#### Verification Steps
- [ ] All database queries use parameterized queries
- [ ] No string concatenation in SQL
- [ ] ORM/query builder is used correctly
- [ ] Supabase queries are properly sanitized

### 4. Authentication and Authorization

#### JWT Token Handling
```typescript
// Example of handling JWT tokens
import jwt from 'jsonwebtoken';

const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
```

#### Verification Steps
- [ ] JWT tokens are signed and verified correctly
- [ ] Sensitive information is not included in tokens
- [ ] Token expiration is handled properly