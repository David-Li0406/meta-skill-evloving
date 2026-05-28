# Email Service

An email service using **Resend** with **Effect-TS** integration for type-safe, functional email sending.

## Libraries

| Package                   | Purpose                           |
| ------------------------- | --------------------------------- |
| `resend`                  | Email API client                  |
| `effect`                  | Functional programming primitives |
| `@react-email/components` | React Email templates (optional)  |

## File Structure

```
lib/services/email/
├── index.ts         # Effect service with Resend client
└── templates/       # React Email templates (optional)
    └── otp.tsx

lib/schemas/
└── email.ts         # Email validation schema
```

## Scaffolding from Scratch

### 1. Install Dependencies

```bash
npm install resend effect
# Optional: React Email for templates
npm install @react-email/components
```

### 2. Create Tagged Errors

```typescript
// lib/services/email/errors.ts
import { Data } from 'effect'

export class EmailConfigError extends Data.TaggedError('EmailConfigError')<{
  message: string
}> {}

export class SendEmailError extends Data.TaggedError('SendEmailError')<{
  message: string
  cause?: unknown
}> {}
```

### 3. Create the Effect Service (`lib/services/email/index.ts`)

```typescript
import {
  Resend as ResendClient,
  CreateEmailOptions,
  CreateEmailRequestOptions,
  CreateEmailResponseSuccess
} from 'resend'
import { Context, Data, Effect, Layer, Config, Redacted } from 'effect'

// Error types
export class EmailConfigError extends Data.TaggedError('EmailConfigError')<{
  message: string
}> {}

export class SendEmailError extends Data.TaggedError('SendEmailError')<{
  message: string
  cause?: unknown
}> {}

// Configuration service
export class EmailConfig extends Context.Tag('@app/EmailConfig')<
  EmailConfig,
  {
    readonly apiKey: Redacted.Redacted<string>
  }
>() {}

// Configuration layer
const EmailConfigLive = Layer.effect(
  EmailConfig,
  Effect.gen(function* () {
    const apiKey = yield* Config.redacted('RESEND_API_KEY').pipe(
      Effect.mapError(() => new EmailConfigError({ message: 'RESEND_API_KEY not found' }))
    )
    return { apiKey }
  })
)

// Service interface
export class Email extends Context.Tag('@app/Email')<
  Email,
  {
    readonly sendEmail: (
      payload: CreateEmailOptions,
      options?: CreateEmailRequestOptions
    ) => Effect.Effect<CreateEmailResponseSuccess, SendEmailError, never>
  }
>() {}

// Service implementation
const EmailServiceLive = Layer.effect(
  Email,
  Effect.gen(function* () {
    const config = yield* EmailConfig
    const resendClient = new ResendClient(Redacted.value(config.apiKey))

    const sendEmail = (payload: CreateEmailOptions, options?: CreateEmailRequestOptions) =>
      Effect.gen(function* () {
        // Annotate span for observability
        yield* Effect.annotateCurrentSpan({
          operation: 'email.send',
          'email.to': Array.isArray(payload.to) ? payload.to.join(',') : payload.to,
          'email.subject': payload.subject ?? 'none'
        })

        const { data, error } = yield* Effect.promise(() =>
          resendClient.emails.send(payload, options)
        )

        if (error) {
          return yield* new SendEmailError({
            message: error.message,
            cause: error
          })
        }

        // Annotate with result
        yield* Effect.annotateCurrentSpan({ 'email.id': data.id })

        return data
      }).pipe(
        Effect.withSpan('email.send'),
        Effect.tapError(error =>
          Effect.logError('Email send failed', {
            to: Array.isArray(payload.to) ? payload.to.join(',') : payload.to,
            subject: payload.subject,
            error
          })
        )
      )

    return { sendEmail }
  })
)

// Composed layer for export
export const EmailLive = EmailServiceLive.pipe(Layer.provide(EmailConfigLive))
```

### 4. Create Email Validation Schema (`lib/schemas/email.ts`)

```typescript
import { Schema } from 'effect'

export const EmailSchema = Schema.compose(Schema.Trim, Schema.NonEmptyString).pipe(
  Schema.pattern(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/),
  Schema.annotations({
    title: 'Email',
    description: 'A valid email address'
  }),
  Schema.brand('Email')
)

export type Email = Schema.Schema.Type<typeof EmailSchema>

// Validation helper
export const parseEmail = Schema.decodeUnknown(EmailSchema)
```

### 5. Create Layer Composition (`lib/layers.ts`)

```typescript
import { Layer } from 'effect'
import { EmailLive } from './services/email'

export const AppLayer = Layer.mergeAll(
  EmailLive
  // ... other layers
)
```

## Usage Patterns

### Basic Email Sending

```typescript
import { Effect } from 'effect'
import { Email } from '@/lib/services/email'

export const sendWelcomeEmail = (to: string, name: string) =>
  Effect.gen(function* () {
    const emailService = yield* Email

    return yield* emailService.sendEmail({
      from: 'App <hello@yourapp.com>',
      to,
      subject: `Welcome, ${name}!`,
      html: `<h1>Welcome to our app, ${name}!</h1><p>We're glad to have you.</p>`
    })
  }).pipe(Effect.withSpan('email.welcome'))
```

### With React Email Templates

First, create a template:

```typescript
// lib/services/email/templates/welcome.tsx
import { Html, Head, Body, Container, Text, Button } from '@react-email/components'

interface WelcomeEmailProps {
  name: string
  loginUrl: string
}

export function WelcomeEmail({ name, loginUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'sans-serif' }}>
        <Container>
          <Text>Welcome, {name}!</Text>
          <Text>Click below to get started:</Text>
          <Button href={loginUrl} style={{ background: '#000', color: '#fff', padding: '12px 24px' }}>
            Get Started
          </Button>
        </Container>
      </Body>
    </Html>
  )
}
```

Then use it:

```typescript
import { Effect } from 'effect'
import { Email } from '@/lib/services/email'
import { WelcomeEmail } from '@/lib/services/email/templates/welcome'

export const sendWelcomeEmail = (to: string, name: string) =>
  Effect.gen(function* () {
    const emailService = yield* Email

    return yield* emailService.sendEmail({
      from: 'App <hello@yourapp.com>',
      to,
      subject: `Welcome, ${name}!`,
      react: <WelcomeEmail name={name} loginUrl="https://yourapp.com/login" />
    })
  }).pipe(Effect.withSpan('email.welcome'))
```

### OTP Email

```typescript
export const sendOTPEmail = (to: string, otp: string) =>
  Effect.gen(function* () {
    const emailService = yield* Email

    return yield* emailService.sendEmail({
      from: 'App <login@yourapp.com>',
      to,
      subject: 'Your login code',
      html: `
        <div style="font-family: sans-serif; max-width: 400px; margin: 0 auto;">
          <h2>Your login code</h2>
          <p style="font-size: 32px; font-weight: bold; letter-spacing: 4px; color: #000;">
            ${otp}
          </p>
          <p style="color: #666;">This code expires in 5 minutes.</p>
        </div>
      `
    })
  }).pipe(Effect.withSpan('email.otp'))
```

### With Attachments

```typescript
export const sendReportEmail = (to: string, pdfBuffer: Buffer) =>
  Effect.gen(function* () {
    const emailService = yield* Email

    return yield* emailService.sendEmail({
      from: 'App <reports@yourapp.com>',
      to,
      subject: 'Your monthly report',
      html: '<p>Please find your monthly report attached.</p>',
      attachments: [
        {
          filename: 'report.pdf',
          content: pdfBuffer
        }
      ]
    })
  }).pipe(Effect.withSpan('email.report'))
```

### Batch Sending

```typescript
import { Effect, Array } from 'effect'

export const sendBulkEmail = (recipients: string[], subject: string, html: string) =>
  Effect.gen(function* () {
    const emailService = yield* Email

    // Send in parallel with concurrency limit
    const results = yield* Effect.forEach(
      recipients,
      to => emailService.sendEmail({ from: 'App <hello@yourapp.com>', to, subject, html }),
      { concurrency: 5 } // Max 5 concurrent sends
    )

    return results
  }).pipe(Effect.withSpan('email.bulk'))
```

### In Server Actions

```typescript
'use server'

import { Effect, Layer } from 'effect'
import { NextEffect } from '@/lib/next-effect'
import { AppLayer } from '@/lib/layers'
import { sendWelcomeEmail } from '@/lib/services/email/operations'

export const inviteUserAction = async (email: string, name: string) => {
  return await NextEffect.runPromise(
    Effect.gen(function* () {
      // Create user in database...

      // Send welcome email
      yield* sendWelcomeEmail(email, name)

      return { success: true }
    }).pipe(
      Effect.withSpan('action.user.invite'),
      Effect.provide(AppLayer),
      Effect.scoped,
      Effect.matchEffect({
        onFailure: error => Effect.succeed({ success: false, error: error.message }),
        onSuccess: result => Effect.succeed(result)
      })
    )
  )
}
```

### Integration with Auth (OTP)

```typescript
// In lib/services/auth/index.ts
import { Email } from '../email'

export class BetterAuth extends Effect.Service<BetterAuth>()('@app/BetterAuth', {
  effect: Effect.gen(function* () {
    const emailService = yield* Email

    const auth = betterAuth({
      plugins: [
        emailOTP({
          async sendVerificationOTP({ email, otp, type }) {
            if (type !== 'sign-in') return

            await emailService
              .sendEmail({
                from: 'App <login@yourapp.com>',
                to: email,
                subject: 'Your login code',
                html: `Your code: <strong>${otp}</strong>`
              })
              .pipe(Effect.runPromise)
          }
        })
      ]
    })

    return { auth }
  })
}) {}
```

## Best Practices

### 1. Use Redacted for API Keys

Never expose API keys in logs:

```typescript
const apiKey = yield * Config.redacted('RESEND_API_KEY')
const client = new ResendClient(Redacted.value(apiKey))
```

### 2. Always Add Spans for Observability

Track email operations in your telemetry:

```typescript
Effect.gen(function* () {
  yield* Effect.annotateCurrentSpan({
    operation: 'email.send',
    'email.to': to,
    'email.subject': subject
  })
  // ...
}).pipe(Effect.withSpan('email.send'))
```

### 3. Handle Errors Gracefully

Don't let email failures crash your application:

```typescript
// In a server action
const result =
  yield *
  sendWelcomeEmail(email, name).pipe(
    Effect.catchTag('SendEmailError', error => {
      // Log but don't fail the entire operation
      yield * Effect.logWarning('Welcome email failed', { error, email })
      return Effect.succeed(null)
    })
  )
```

### 4. Use Branded Types for Validation

Ensure emails are validated before sending:

```typescript
import { parseEmail } from '@/lib/schemas/email'

export const sendEmail = (to: unknown, subject: string, html: string) =>
  Effect.gen(function* () {
    const validEmail = yield* parseEmail(to)
    // Now `validEmail` is guaranteed to be a valid email
  })
```

### 5. Use React Email for Complex Templates

For anything beyond simple text, use React Email:

```typescript
// Maintainable, type-safe templates
react: <WelcomeEmail name={name} loginUrl={url} />

// vs. error-prone string interpolation
html: `<div>Welcome ${name}! <a href="${url}">Login</a></div>`
```

### 6. Set Concurrency Limits for Bulk Sends

Avoid rate limiting with controlled concurrency:

```typescript
Effect.forEach(recipients, sendEmail, { concurrency: 5 })
```

### 7. Use Appropriate From Addresses

Different types of emails should come from different addresses:

```typescript
// Transactional
from: 'App <login@yourapp.com>'

// Marketing
from: 'App <hello@yourapp.com>'

// Support
from: 'App <support@yourapp.com>'
```

## Environment Variables

| Variable         | Required | Description    |
| ---------------- | -------- | -------------- |
| `RESEND_API_KEY` | Yes      | Resend API key |

## Email Types Supported

| Type  | Field   | Description           |
| ----- | ------- | --------------------- |
| HTML  | `html`  | Raw HTML string       |
| React | `react` | React Email component |
| Text  | `text`  | Plain text fallback   |

## Testing Emails

For development, Resend provides a test mode:

```typescript
// Use Resend's test domain for development
const testEmail = {
  from: 'onboarding@resend.dev',
  to: 'delivered@resend.dev',
  subject: 'Test',
  html: '<p>Test email</p>'
}
```

Or use environment-based configuration:

```typescript
const from =
  process.env.NODE_ENV === 'production' ? 'App <hello@yourapp.com>' : 'onboarding@resend.dev'
```

## Rate Limits

Resend has the following rate limits:

| Plan | Emails/day | Emails/second |
| ---- | ---------- | ------------- |
| Free | 100        | 1             |
| Pro  | 50,000+    | 10            |

Handle rate limits gracefully:

```typescript
const sendWithRetry = (payload: CreateEmailOptions) =>
  emailService
    .sendEmail(payload)
    .pipe(
      Effect.retry(Schedule.exponential('1 second', 2).pipe(Schedule.intersect(Schedule.recurs(3))))
    )
```
