# Email Service: Advanced Multi-Provider Example

## Table of Contents

1. [Overview](#overview)
2. [Complete File Structure](#complete-file-structure)
3. [Pattern Extensions Beyond Basic 7 Steps](#pattern-extensions-beyond-basic-7-steps)
4. [Step-by-Step Walkthrough](#step-by-step-walkthrough)
5. [Comparison to Captcha Service](#comparison-to-captcha-service)
6. [When to Add Complexity](#when-to-add-complexity)
7. [Progressive Enhancement Approach](#progressive-enhancement-approach)
8. [Key Takeaways](#key-takeaways)

## Overview

The email service demonstrates an advanced implementation of the Modular Service Design Pattern with multiple providers (Ethereal for development, Resend for production). It introduces additional patterns beyond the basic 7 steps:

- **Registry Pattern:** Maps email types to configurations
- **Singleton Facade:** EmailAgent provides simplified API
- **Environment-Based Selection:** Auto-selects provider based on configuration

**Why This Is More Complex:**

- Two providers with different APIs (SMTP vs HTTP)
- Email registry for template management
- Singleton facade for application-wide usage
- Development vs production behavior

**Location:** `/src/services/email/`

## Complete File Structure

```text
src/services/email/
├── index.ts                          # Public exports
├── email-agent.ts                    # Singleton facade
├── service.ts                        # Core email service
├── email-type.ts                     # Email type enum
├── providers/
│   ├── index.ts                      # Provider exports
│   ├── provider.ts                   # Generic interface
│   ├── factory.ts                    # Factory with environment selection
│   ├── payload.ts                    # Email payload type
│   ├── provider-ethereal.ts          # Ethereal (SMTP) implementation
│   └── provider-resend.ts            # Resend (HTTP API) implementation
├── registry/
│   ├── index.ts                      # Registry exports
│   ├── registry.ts                   # Registry interface
│   ├── registry-default.ts           # Default implementation
│   └── builder.ts                    # Registry builder
└── configs/
    ├── config.ts                     # Email config interface
    ├── email-verification.ts         # Verification email config
    └── password-reset.ts             # Password reset email config
```

## Pattern Extensions Beyond Basic 7 Steps

### 1. Registry Pattern

**Purpose:** Maps email types to their configurations (templates, subjects, renderers).

**Interface:**

```typescript
// registry/registry.ts
import type { EmailConfig } from '../configs/config'
import type { EmailType } from '../email-type'

export interface EmailRegistry {
  add: <T>(config: EmailConfig<T>) => void
  get: <T>(emailType: EmailType) => Promise<EmailConfig<T>>
}
```

**Implementation:**

```typescript
// registry/registry-default.ts
export class DefaultEmailRegistry implements EmailRegistry {
  private configs: Map<EmailType, EmailConfig<any>> = new Map()

  add<T>(config: EmailConfig<T>): void {
    this.configs.set(config.type, config)
  }

  async get<T>(emailType: EmailType): Promise<EmailConfig<T>> {
    const config = this.configs.get(emailType)
    if (!config) {
      throw new Error(`Email configuration not found for type: ${emailType}`)
    }
    return config as EmailConfig<T>
  }
}
```

**Builder:**

```typescript
// registry/builder.ts
import { emailVerificationConfig } from '../configs/email-verification'
import { passwordResetConfig } from '../configs/password-reset'
import { DefaultEmailRegistry } from './registry-default'

export const buildEmailRegistry = (): EmailRegistry => {
  const registry = new DefaultEmailRegistry()

  registry.add(emailVerificationConfig)
  registry.add(passwordResetConfig)

  return registry
}
```

**Why Registry Pattern:**

- Decouples email types from service logic
- Easy to add new email types without changing service
- Centralized template/config management
- Type-safe email type system

### 2. Singleton Facade Pattern

**Purpose:** Provides simplified, application-wide API for sending emails.

**Implementation:**

```typescript
// email-agent.ts
import type { UserPreferences } from '@/types'

import env from '@/env'

import { EmailType } from './email-type'
import { createEmailProvider } from './providers'
import { buildEmailRegistry } from './registry'
import { EmailService } from './service'

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

  async sendEmailVerificationEmail(
    firstName: string,
    email: string,
    token: string,
    preferences?: UserPreferences,
  ) {
    const verificationUrl = `${env.FE_BASE_URL}/verify-email?token=${token}`

    await this.service.send(EmailType.EMAIL_VERIFICATION, email, {
      firstName,
      verificationUrl,
    }, preferences)
  }

  async sendResetPasswordEmail(
    firstName: string,
    email: string,
    token: string,
    preferences?: UserPreferences,
  ) {
    const resetUrl = `${env.FE_BASE_URL}/reset-password?token=${token}`

    await this.service.send(EmailType.PASSWORD_RESET, email, {
      firstName,
      resetUrl,
    }, preferences)
  }
}

const emailAgent = EmailAgent.getInstance()

export { emailAgent }
```

**Why Singleton Facade:**

- Single initialization of provider and registry
- Simplified API for route handlers
- Hides complexity of email service internals
- Application-wide configuration consistency

**Usage in Routes:**

```typescript
import { emailAgent } from '@/services/email'

// Simple, high-level API
await emailAgent.sendEmailVerificationEmail(
  user.firstName,
  user.email,
  verificationToken
)
```

## Step-by-Step Walkthrough

### Step 2: Interface Abstraction

**Provider Interface:**

```typescript
// providers/provider.ts
import type { EmailPayload } from './payload'

export interface EmailProvider {
  send: (payload: EmailPayload) => Promise<void>
}
```

**Payload Definition:**

```typescript
// providers/payload.ts
export interface EmailPayload {
  to: string | string[]
  from: {
    email: string
    name: string
  }
  subject: string
  html: string
  text: string
}
```

**Key Design Decision:** Interface is extremely simple (just `send`), but payload structure is rich enough to support multiple providers.

### Step 5: Factory Pattern with Environment Selection

**File:** `providers/factory.ts`

```typescript
import env from '@/env'
import { logger } from '@/logging'

import type { EmailProvider } from './provider'

import { EtherealEmailProvider } from './provider-ethereal'
import { ResendEmailProvider } from './provider-resend'

export type EmailProviderType = 'resend' | 'ethereal'

const getProviderType = (type?: EmailProviderType): EmailProviderType => {
  if (type) {
    return type
  }

  // Use resend if API key is provided, otherwise ethereal
  return env.EMAIL_RESEND_API_KEY ? 'resend' : 'ethereal'
}

export const createEmailProvider = (type?: EmailProviderType): EmailProvider => {
  const providerType = getProviderType(type)

  logger.info(`📧 Email provider: ${providerType}`)

  switch (providerType) {
    case 'ethereal': {
      return new EtherealEmailProvider(
        env.EMAIL_ETHEREAL_HOST,
        env.EMAIL_ETHEREAL_PORT,
        env.EMAIL_ETHEREAL_USERNAME,
        env.EMAIL_ETHEREAL_PASSWORD,
      )
    }
    case 'resend': {
      return new ResendEmailProvider(env.EMAIL_RESEND_API_KEY)
    }
    default: {
      throw new Error(`Unknown email provider type: ${providerType as string}`)
    }
  }
}
```

**Key Factory Features:**

- Automatic provider selection based on environment
- Logs selected provider for debugging
- Can override provider via parameter
- Type-safe provider type enum

**Environment-Based Selection Logic:**

- If `EMAIL_RESEND_API_KEY` is set → use Resend (production)
- Otherwise → use Ethereal (development)

## Comparison to Captcha Service

### Similarities (Core Pattern)

- Interface abstraction (EmailProvider / Captcha)
- Concrete implementations (EtherealEmailProvider / Recaptcha)
- Factory pattern (createEmailProvider / createCaptchaVerifier)
- Encapsulation via index.ts exports
- Constructor injection for configuration

### Differences (Advanced Patterns)

| Aspect | Captcha | Email |
|--------|---------|-------|
| **Providers** | Single (reCAPTCHA) | Multiple (Ethereal, Resend) |
| **Factory Logic** | Simple instantiation | Environment-based selection |
| **Usage Pattern** | Closure singleton in middleware | Singleton facade (EmailAgent) |
| **Additional Patterns** | None | Registry + Singleton Facade |
| **Configuration** | Single config object | Registry + multiple configs |
| **Complexity** | ~127 lines | ~500+ lines |

## When to Add Complexity

### Start Simple (like Captcha)

- Single provider
- Direct factory usage
- No registry needed
- Use when: Service is straightforward, one provider sufficient

### Add Complexity (like Email)

- Multiple providers needed
- Registry for content management
- Singleton facade for simplified API
- Use when: Service has multiple providers, complex configuration, or needs application-wide instance

## Progressive Enhancement Approach

1. **Phase 1:** Start with single provider (like Captcha)
2. **Phase 2:** Add second provider when needed (update factory)
3. **Phase 3:** Add registry if multiple configurations grow
4. **Phase 4:** Add singleton facade if usage becomes repetitive

**Key Lesson:** Don't add complexity upfront. Start simple, enhance when pain points emerge.

## Key Takeaways

**Advanced Patterns:**

- Registry: Manages configurations for different email types
- Singleton Facade: Simplifies API for application code
- Environment Selection: Auto-detects provider based on config

**When to Use Advanced Patterns:**

- Multiple providers: Use factory with switch statement
- Multiple configurations: Use registry pattern
- Application-wide usage: Use singleton facade
- Environment-specific behavior: Use auto-selection in factory

**Architecture Lessons:**

- Core pattern stays the same (interface + factory + encapsulation)
- Additional patterns layer on top without breaking core
- Start simple, enhance progressively
- Each pattern solves specific problem (don't add without reason)
