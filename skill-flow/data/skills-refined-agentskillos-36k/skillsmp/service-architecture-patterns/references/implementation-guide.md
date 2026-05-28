# Service Architecture Patterns: Implementation Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Step 1: Feature Isolation](#step-1-feature-isolation)
3. [Step 2: Interface Abstraction](#step-2-interface-abstraction)
4. [Step 3: Helper Interfaces](#step-3-helper-interfaces)
5. [Step 4: Concrete Implementation](#step-4-concrete-implementation)
6. [Step 5: Factory Pattern](#step-5-factory-pattern)
7. [Step 6: Encapsulation Strategy](#step-6-encapsulation-strategy)
8. [Step 7: Usage Pattern](#step-7-usage-pattern)
9. [Testing Strategy](#testing-strategy)

## Introduction

The Modular Service Design Pattern provides a systematic approach to integrating external services while maintaining clean architecture principles. This guide walks through all 7 steps with detailed explanations and code examples.

**Pattern Goals:**

- Decouple business logic from service provider details
- Enable easy provider swapping without code changes
- Facilitate testing through interface mocking
- Maintain type safety across all abstractions

**Comparison to Monolithic Approach:**

- Monolithic: Direct API calls scattered throughout codebase, hard to test, provider lock-in
- Modular: Centralized service logic, testable interfaces, easy provider switching

## Step 1: Feature Isolation

**Principle:** Each external service gets its own isolated directory under `/src/services/`.

**Directory Structure:**

```text
src/services/[service-name]/
├── index.ts              # Public API exports
├── [service].ts          # Generic interface
├── factory.ts            # Factory method
├── config.ts             # Configuration interface
└── [provider]/           # Provider implementations
    ├── index.ts          # Provider exports
    ├── [provider].ts     # Concrete class
    ├── config.ts         # Provider-specific config
    └── [types].ts        # Provider-specific types
```

**Why Isolation Matters:**

- Prevents service code from leaking into business logic
- Makes it easy to locate all provider-related code
- Enables independent testing and development
- Simplifies onboarding for new team members

**Naming Conventions:**

- Service directory: kebab-case (e.g., `captcha`, `email`, `file-storage`)
- Provider subdirectory: provider name in lowercase (e.g., `recaptcha`, `ethereal`)
- Files: kebab-case with descriptive names

**Example:**

```typescript
// Good: Isolated service structure
src/services/captcha/
  ├── captcha.ts
  ├── factory.ts
  └── recaptcha/

// Bad: Service code mixed with business logic
src/routes/auth/recaptcha-validator.ts
src/middleware/google-recaptcha.ts
```

## Step 2: Interface Abstraction

**Principle:** Define provider-agnostic interfaces that focus on WHAT, not HOW.

**Generic Interface Design:**

```typescript
// captcha.ts - Generic interface
/**
 * Interface for CAPTCHA validation services.
 * Supports multiple providers (reCAPTCHA, hCaptcha, Turnstile, etc.).
 */
export interface Captcha {
  /**
   * Validates a CAPTCHA token.
   * @throws {AppError} When validation fails
   */
  validate: (token: string) => Promise<void>
}
```

**Configuration Interface:**

```typescript
// config.ts - Generic configuration
export interface Config {
  baseUrl: string
  path: string
  options: {
    headers: Record<string, string>
    timeout: number
  }
  secret: string
}
```

**Key Principles:**

- Interface methods should be provider-agnostic
- Focus on business capabilities, not implementation details
- Use clear method names that express intent
- Document expected behavior and error conditions
- Keep interfaces minimal (Interface Segregation Principle)

**Good vs Bad Examples:**

```typescript
// Good: Provider-agnostic
interface EmailProvider {
  send: (payload: EmailPayload) => Promise<void>
}

// Bad: Provider-specific details leaked
interface EmailProvider {
  sendViaResendAPI: (payload: ResendPayload) => Promise<ResendResponse>
}
```

## Step 3: Helper Interfaces

**Principle:** Create supporting types for data structures, but keep them provider-specific when needed.

**When to Create Helpers:**

- Provider API response structures
- Request payload formats
- Provider-specific error codes
- Configuration sub-types

**Example: Provider-Specific Types**

```typescript
// recaptcha/result.ts
/**
 * reCAPTCHA API validation result structure.
 */
export interface Result {
  'success': boolean
  'challenge_ts'?: string
  'hostname'?: string
  'error-codes'?: string[]
}
```

**Guidelines:**

- Keep helper types close to where they're used
- Don't export provider-specific types from public API
- Use TypeScript utility types (Pick, Omit, Partial) when appropriate
- Document external API structures with links to documentation

## Step 4: Concrete Implementation

**Principle:** Implement the generic interface with provider-specific logic.

**Implementation Pattern:**

```typescript
// recaptcha/recaptcha.ts
import type { Captcha } from '../captcha'
import type { Config } from '../config'

export class Recaptcha implements Captcha {
  private httpClient: HttpClient
  private config: Config

  constructor(config: Config) {
    this.config = config
    this.httpClient = new HttpClient(config.baseUrl, config.options)
  }

  async validate(token: string): Promise<void> {
    if (!token || typeof token !== 'string') {
      throw new AppError(ErrorCode.CaptchaInvalidToken)
    }

    const body = this.createBody(token)
    const result = await this.httpClient.post<Result>(this.config.path, body)

    if (!result.success) {
      const errorCodes = result['error-codes'] || []
      throw new AppError(
        ErrorCode.CaptchaValidationFailed,
        `reCAPTCHA validation failed: ${errorCodes.join(', ')}`
      )
    }
  }

  private createBody(token: string): URLSearchParams {
    return new URLSearchParams({
      secret: this.config.secret,
      response: token,
    })
  }
}
```

**Key Implementation Principles:**

- Constructor injection for configuration
- Private helper methods for internal logic
- Convert provider-specific errors to domain errors
- Validate inputs before making external calls
- Use proper error handling and logging

**Error Handling Strategy:**

```typescript
// Good: Convert to domain errors
if (!result.success) {
  throw new AppError(ErrorCode.CaptchaValidationFailed)
}

// Bad: Leak provider-specific errors
if (!result.success) {
  throw new RecaptchaError(result['error-codes'])
}
```

## Step 5: Factory Pattern

**Principle:** Provide factory functions for service instantiation, hiding concrete implementations.

**Basic Factory:**

```typescript
// factory.ts
import type { Captcha } from './captcha'
import { Recaptcha, recaptchaConfig } from './recaptcha/'

/**
 * Factory function to create a CAPTCHA verification service.
 * Returns reCAPTCHA verifier configured from environment.
 */
export const createCaptchaVerifier = (): Captcha => {
  return new Recaptcha(recaptchaConfig)
}
```

**Advanced Factory with Environment Selection:**

```typescript
// factory.ts
export type ProviderType = 'recaptcha' | 'hcaptcha' | 'turnstile'

const getProviderType = (type?: ProviderType): ProviderType => {
  if (type) {
    return type
  }

  // Auto-select based on environment config
  if (env.HCAPTCHA_SECRET) {
    return 'hcaptcha'
  }
  if (env.TURNSTILE_SECRET) {
    return 'turnstile'
  }
  return 'recaptcha'
}

export const createCaptchaVerifier = (type?: ProviderType): Captcha => {
  const providerType = getProviderType(type)

  switch (providerType) {
    case 'recaptcha':
      return new Recaptcha(recaptchaConfig)
    case 'hcaptcha':
      return new HCaptcha(hcaptchaConfig)
    case 'turnstile':
      return new Turnstile(turnstileConfig)
    default:
      throw new Error(`Unknown CAPTCHA provider: ${providerType}`)
  }
}
```

**Factory Benefits:**

- Centralizes provider selection logic
- Hides concrete class constructors
- Enables environment-based configuration
- Simplifies testing (mock the factory return)

## Step 6: Encapsulation Strategy

**Principle:** Export only the public API via `index.ts`, hiding implementation details.

**Public API Definition:**

```typescript
// index.ts - Public exports only
export type { Captcha } from './captcha'
export { createCaptchaVerifier } from './factory'

// Implementation details (Recaptcha class, config, etc.) NOT exported
```

**What to Export:**

- Generic interfaces (type-only exports)
- Factory functions
- Public types used by consumers
- Error types specific to the service

**What NOT to Export:**

- Concrete implementation classes
- Provider-specific types
- Internal configuration objects
- Helper utilities

**Benefits:**

- Enforces programming to interfaces
- Prevents consumers from depending on implementations
- Makes breaking changes easier (only public API matters)
- Reduces coupling between modules

## Step 7: Usage Pattern

**Principle:** Consume services via factory methods and generic interfaces only.

**Singleton Instance Pattern (Middleware):**

```typescript
// middleware/captcha/captcha.ts
import type { MiddlewareHandler } from 'hono'
import { createCaptchaVerifier } from '@/services/captcha'

const captchaMiddleware = (): MiddlewareHandler => {
  // Create single instance for performance
  const captchaVerifier = createCaptchaVerifier()

  return async (c, next) => {
    const { captcha } = c.req.valid('json')
    await captchaVerifier.validate(captcha.token)
    await next()
  }
}

export default captchaMiddleware
```

**Singleton Facade Pattern (Advanced):**

```typescript
// services/email/email-agent.ts
export class EmailAgent {
  private static instance: EmailAgent | null = null
  private service: EmailService

  private constructor() {
    const provider = createEmailProvider()
    const registry = buildEmailRegistry()
    this.service = new EmailService(provider, registry)
  }

  static getInstance(): EmailAgent {
    if (!EmailAgent.instance) {
      EmailAgent.instance = new EmailAgent()
    }
    return EmailAgent.instance
  }

  async sendVerificationEmail(email: string, token: string) {
    await this.service.send(EmailType.VERIFICATION, email, { token })
  }
}

export const emailAgent = EmailAgent.getInstance()
```

**Per-Request Pattern:**

```typescript
// routes/auth/login.ts
const loginHandler = async (c: Context) => {
  const captcha = createCaptchaVerifier() // new instance per request
  await captcha.validate(c.req.json().captchaToken)
  // ... rest of login logic
}
```

**Performance Considerations:**

- Use singleton/closure pattern for stateless services (CAPTCHA, email)
- Use per-request instances for stateful services (database connections, transactions)
- Avoid creating instances in hot paths (inside loops)

## Testing Strategy

**Mocking Interfaces:**

```typescript
// __tests__/captcha.test.ts
import type { Captcha } from '@/services/captcha'

const mockCaptcha: Captcha = {
  validate: mock(async (token: string) => {
    if (token === 'invalid') {
      throw new AppError(ErrorCode.CaptchaValidationFailed)
    }
  })
}
```

**Testing Concrete Implementations:**

```typescript
// services/captcha/recaptcha/__tests__/recaptcha.test.ts
import { Recaptcha } from '../recaptcha'
import { recaptchaConfig } from '../config'

describe('Recaptcha', () => {
  it('should validate successful token', async () => {
    const recaptcha = new Recaptcha(recaptchaConfig)
    // Mock HTTP client response
    await expect(recaptcha.validate('valid-token')).resolves.not.toThrow()
  })
})
```

**Integration Testing:**

```typescript
// Test with real service (test environment only)
const captcha = createCaptchaVerifier()
await captcha.validate(testToken) // uses test CAPTCHA secret
```

**Testing Best Practices:**

- Mock interfaces for unit tests
- Test concrete implementations separately
- Use test environment configurations
- Verify error handling paths
- Test provider-specific edge cases

### Testing Factory Methods with Multiple Providers

**Testing Provider Selection:**

```typescript
// services/captcha/__tests__/factory.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'bun:test'
import { createCaptchaVerifier } from '../factory'
import type { Captcha } from '../captcha'

describe('createCaptchaVerifier', () => {
  let originalEnv: string | undefined

  beforeEach(() => {
    originalEnv = process.env.CAPTCHA_PROVIDER
  })

  afterEach(() => {
    if (originalEnv) {
      process.env.CAPTCHA_PROVIDER = originalEnv
    } else {
      delete process.env.CAPTCHA_PROVIDER
    }
  })

  it('should create reCAPTCHA verifier by default', () => {
    const verifier = createCaptchaVerifier()
    expect(verifier).toBeDefined()
    expect(verifier).toHaveProperty('validate')
  })

  it('should create hCaptcha verifier when specified', () => {
    const verifier = createCaptchaVerifier('hcaptcha')
    expect(verifier).toBeDefined()
    expect(verifier).toHaveProperty('validate')
  })

  it('should return same interface regardless of provider', () => {
    const recaptcha = createCaptchaVerifier('recaptcha')
    const hcaptcha = createCaptchaVerifier('hcaptcha')

    // Both should have the same interface
    expect(typeof recaptcha.validate).toBe('function')
    expect(typeof hcaptcha.validate).toBe('function')
  })
})
```

**Testing with Environment Variables:**

```typescript
// services/email/__tests__/factory.test.ts
import { describe, it, expect, beforeEach } from 'bun:test'
import { createEmailProvider } from '../providers/factory'

describe('createEmailProvider', () => {
  it('should select Resend when API key is set', () => {
    process.env.EMAIL_RESEND_API_KEY = 'test-key'

    const provider = createEmailProvider()
    // Provider should be Resend implementation
    expect(provider).toBeDefined()
  })

  it('should select Ethereal when no Resend key', () => {
    delete process.env.EMAIL_RESEND_API_KEY

    const provider = createEmailProvider()
    // Provider should be Ethereal implementation
    expect(provider).toBeDefined()
  })

  it('should allow explicit provider override', () => {
    process.env.EMAIL_RESEND_API_KEY = 'test-key'

    // Explicitly request Ethereal despite Resend key
    const provider = createEmailProvider('ethereal')
    expect(provider).toBeDefined()
  })
})
```
