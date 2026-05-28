# Captcha Service: Simple Single-Provider Example

## Table of Contents

1. [Overview](#overview)
2. [Complete File Structure](#complete-file-structure)
3. [Step-by-Step Walkthrough](#step-by-step-walkthrough)
4. [Key Takeaways](#key-takeaways)

## Overview

The captcha service demonstrates the simplest form of the Modular Service Design Pattern with a single provider (Google reCAPTCHA). This is an excellent starting point for understanding the pattern before moving to more complex multi-provider scenarios.

**Why This Is a Good Example:**

- Single provider keeps it simple
- All 7 steps clearly implemented
- Production-ready code from real codebase
- Clean separation of concerns
- Easy to extend with new providers (hCaptcha, Turnstile)

**Location:** `/src/services/captcha/`

## Complete File Structure

```text
src/services/captcha/
├── index.ts                    # Public API (4 lines)
├── captcha.ts                  # Generic interface (16 lines)
├── config.ts                   # Configuration interface (15 lines)
├── factory.ts                  # Factory function (15 lines)
└── recaptcha/                  # Provider implementation
    ├── index.ts                # Provider exports (2 lines)
    ├── recaptcha.ts            # Concrete implementation (49 lines)
    ├── config.ts               # reCAPTCHA-specific config (15 lines)
    └── result.ts               # API response type (11 lines)
```

**Total Lines:** ~127 lines for complete service integration

## Step-by-Step Walkthrough

### Step 1: Feature Isolation

All CAPTCHA-related code lives under `/src/services/captcha/`, completely isolated from business logic.

### Step 2: Interface Abstraction

**File:** `captcha.ts`

```typescript
/**
 * Interface for CAPTCHA validation services.
 *
 * Provides a contract for different CAPTCHA implementations
 * (Google reCAPTCHA, hCaptcha, Cloudflare Turnstile, etc.).
 */
export interface Captcha {
  /**
   * Validates a CAPTCHA token.
   *
   * @param token - The CAPTCHA token to validate.
   * @throws {AppError} When token is invalid or validation fails.
   * @returns Promise that resolves when validation succeeds.
   */
  validate: (token: string) => Promise<void>
}
```

**Key Design Decision:** Interface has single method `validate()` that throws on failure (void return). This is simpler than returning boolean, as error details can be included in exceptions.

### Step 2: Configuration Interface

**File:** `config.ts`

```typescript
/**
 * Generic CAPTCHA configuration interface.
 *
 * This can be extended by specific CAPTCHA providers
 * (reCAPTCHA, hCaptcha, Cloudflare Turnstile, etc.).
 */
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

**Key Design Decision:** Configuration includes all necessary fields for HTTP requests (baseUrl, path, headers, timeout) plus provider-specific secret.

### Step 3: Helper Interfaces

**File:** `recaptcha/result.ts`

```typescript
/**
 * reCAPTCHA API validation result structure.
 *
 * Response from Google's reCAPTCHA verification endpoint.
 */
export interface Result {
  'success': boolean
  'challenge_ts'?: string
  'hostname'?: string
  'error-codes'?: string[]
}
```

**Key Design Decision:** Result type matches Google's API response exactly. Quoted keys used for kebab-case fields (`'error-codes'`).

### Step 4: Concrete Implementation

**File:** `recaptcha/recaptcha.ts`

```typescript
import { AppError, ErrorCode } from '@/errors'
import { HttpClient } from '@/net/http/client'

import type { Captcha } from '../captcha'
import type { Config } from '../config'
import type { Result } from './result'

/**
 * Google reCAPTCHA v2 (invisible) verification service.
 *
 * Implements the Captcha interface for Google's reCAPTCHA service.
 */
export class Recaptcha implements Captcha {
  private httpClient: HttpClient
  private config: Config

  constructor(config: Config) {
    this.config = config
    this.httpClient = new HttpClient(
      config.baseUrl,
      config.options,
    )
  }

  async validate(token: string): Promise<void> {
    // Input validation
    if (!token || typeof token !== 'string') {
      throw new AppError(ErrorCode.CaptchaInvalidToken)
    }

    // Make API request
    const body = this.createBody(token)
    const result = await this.httpClient.post<Result>(this.config.path, body)

    // Check result and throw domain error if validation failed
    if (!result.success) {
      const errorCodes = result['error-codes'] || []
      const hostname = result.hostname || 'unknown'
      const message
        = `reCAPTCHA token validation failed. Error codes: ${errorCodes.join(', ')}. Hostname: ${hostname}`

      throw new AppError(ErrorCode.CaptchaValidationFailed, message)
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

**Key Design Decisions:**

- Constructor injection for config
- HttpClient for requests (reusable utility)
- Input validation before external call
- Convert provider errors to domain errors (AppError)
- Private helper method for request body
- Detailed error messages including error codes and hostname

### Step 4: Provider Configuration

**File:** `recaptcha/config.ts`

```typescript
import env from '@/env'

import type { Config } from '../config'

export const recaptchaConfig: Config = {
  baseUrl: 'https://www.google.com',
  path: '/recaptcha/api/siteverify',
  options: {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    timeout: 5000,
  },
  secret: env.CAPTCHA_SECRET_KEY,
}
```

**Key Design Decisions:**

- Configuration object exported as const
- Implements generic Config interface
- Loads secret from environment variables
- Content-Type header for URL-encoded form data
- 5-second timeout for external API call

### Step 5: Factory Pattern

**File:** `factory.ts`

```typescript
import type { Captcha } from './captcha'

import { Recaptcha, recaptchaConfig } from './recaptcha/'

/**
 * Factory function to create a CAPTCHA verification service instance.
 *
 * Currently returns a Google reCAPTCHA verifier, but can be extended
 * to support different CAPTCHA providers based on configuration.
 *
 * @returns {Captcha} CAPTCHA verification service instance.
 */
export const createCaptchaVerifier = (): Captcha => {
  return new Recaptcha(recaptchaConfig)
}
```

**Key Design Decisions:**

- Returns Captcha interface type (not Recaptcha class)
- Single provider for now, but comment indicates extensibility
- No parameters needed (uses environment config)

**Future Extension Example:**

```typescript
export const createCaptchaVerifier = (type?: 'recaptcha' | 'hcaptcha'): Captcha => {
  const providerType = type || 'recaptcha'

  switch (providerType) {
    case 'recaptcha':
      return new Recaptcha(recaptchaConfig)
    case 'hcaptcha':
      return new HCaptcha(hcaptchaConfig)
    default:
      throw new Error(`Unknown CAPTCHA provider: ${providerType}`)
  }
}
```

### Step 6: Encapsulation Strategy

**File:** `index.ts`

```typescript
export type { Captcha } from './captcha'

export { createCaptchaVerifier } from './factory'
```

**What's Exported:**

- `Captcha` interface (type-only export)
- `createCaptchaVerifier` factory function

**What's NOT Exported:**

- `Recaptcha` class (concrete implementation)
- `Config` interface (internal detail)
- `recaptchaConfig` object (internal detail)
- `Result` type (provider-specific)

**Why This Matters:** Consumers can only depend on the interface and factory, not implementation details. This makes it safe to change providers without breaking code.

### Step 7: Usage Pattern

**File:** `/src/middleware/captcha/captcha.ts`

```typescript
import type { MiddlewareHandler } from 'hono'
import { createMiddleware } from 'hono/factory'

import type { AppContext } from '@/context'

import { AppError, ErrorCode } from '@/errors'
import { createCaptchaVerifier } from '@/services'

interface CaptchaBody {
  captcha: {
    token: string
  }
}

interface CaptchaInput {
  in: { json: CaptchaBody }
  out: { json: CaptchaBody }
}

/**
 * CAPTCHA validation middleware for protecting auth endpoints from bot attacks.
 *
 * Validates CAPTCHA token from request body using the CAPTCHA service.
 * Should be applied after request validation but before the main handler.
 *
 * Expects `captcha.token` to be present in the validated request body.
 */
const captchaMiddleware = (): MiddlewareHandler<AppContext> => {
  // Create single instance once (closure pattern)
  const captchaVerifier = createCaptchaVerifier()

  return createMiddleware<AppContext, string, CaptchaInput>(async (c, next) => {
    try {
      // Uses validated data from upstream validator
      const { captcha } = c.req.valid('json')

      await captchaVerifier.validate(captcha.token)
    } catch (error) {
      if (error instanceof AppError) {
        throw error
      }

      throw new AppError(ErrorCode.CaptchaValidationFailed)
    }

    await next()
  })
}

export default captchaMiddleware
```

**Key Usage Patterns:**

- Factory called once in middleware factory (closure creates singleton)
- Service instance reused across all requests (performance)
- No knowledge of Recaptcha class or Google API
- Only depends on Captcha interface
- Error handling wraps non-AppError exceptions

**Request Flow:**

1. Middleware factory called once on server startup
2. `createCaptchaVerifier()` creates Recaptcha instance
3. Middleware handler returned (closure captures instance)
4. Each request uses same Recaptcha instance
5. `validate()` called with token from request body
6. AppError thrown on validation failure

## Key Takeaways

**What Makes This Implementation Clean:**

1. **Complete Isolation:** All CAPTCHA code in one directory
2. **Clear Contracts:** Interface defines exactly what consumers need
3. **Easy Testing:** Mock Captcha interface, test Recaptcha separately
4. **Easy Extension:** Add new provider by implementing Captcha interface
5. **Type Safety:** Full TypeScript support with no `any` types
6. **Error Handling:** Provider errors converted to domain errors
7. **Performance:** Singleton instance pattern avoids repeated instantiation

**Lessons Learned:**

- Start simple with single provider
- Design interface based on business needs, not provider capabilities
- Use constructor injection for configuration
- Convert external errors to domain errors at boundary
- Factory pattern provides future flexibility
- Closure pattern creates efficient singletons
- Export only what consumers need

**When to Use This Pattern:**

- Any external service integration (payment, SMS, analytics)
- Multiple providers exist or are planned
- Service logic should be tested independently
- Provider might change in the future
