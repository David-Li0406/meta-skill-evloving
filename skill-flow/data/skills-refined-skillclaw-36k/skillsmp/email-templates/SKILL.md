---
name: email-templates
description: Transactional email design using React Email and integration with email providers like Resend or AWS SES
---

# Email Templates Skill

Transactional email design using React Email and integration with email providers like Resend or AWS SES.

## Core Principles

1. **Responsive Design**: Emails work on all devices
2. **Accessibility**: Proper semantic HTML and alt text
3. **Plain Text Fallback**: Always include plain text version
4. **Deliverability**: Follow best practices to avoid spam
5. **Testing**: Preview emails before sending

## Installation

```bash
# React Email
npm install react-email @react-email/components

# Email provider (choose one)
npm install resend  # Recommended
npm install @aws-sdk/client-ses
```

## React Email Setup

### 1. Create Email Templates Directory

```
emails/
├── welcome.tsx
├── reset-password.tsx
├── verify-email.tsx
├── receipt.tsx
└── components/
    ├── layout.tsx
    └── button.tsx
```

### 2. Base Layout Component

```typescript
// emails/components/layout.tsx
import {
  Html,
  Head,
  Preview,
  Body,
  Container,
  Section,
  Text,
} from "@react-email/components"

interface LayoutProps {
  preview: string
  children: React.ReactNode
}

export function EmailLayout({ preview, children }: LayoutProps) {
  return (
    <Html>
      <Head />
      <Preview>{preview}</Preview>
      <Body style={main}>
        <Container style={container}>
          {children}
          <Section style={footer}>
            <Text style={footerText}>
              © 2026 Your Company. All rights reserved.
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  )
}

const main = {
  backgroundColor: "#f6f9fc",
  fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Ubuntu,sans-serif',
}

const container = {
  backgroundColor: "#ffffff",
  margin: "0 auto",
  padding: "20px 0 48px",
  marginBottom: "64px",
}

const footer = {
  color: "#8898aa",
  fontSize: "12px",
  lineHeight: "16px",
  marginTop: "32px",
}

const footerText = {
  margin: "0",
  textAlign: "center" as const,
}
```

### 3. Reusable Button Component

```typescript
// emails/components/button.tsx
import { Button as ReactEmailButton } from "@react-email/components"

interface ButtonProps {
  href: string
  children: React.ReactNode
}

export function Button({ href, children }: ButtonProps) {
  return (
    <ReactEmailButton href={href} style={button}>
      {children}
    </ReactEmailButton>
  )
}

const button = {
  backgroundColor: "#5469d4",
  borderRadius: "4px",
  color: "#fff",
  fontSize: "16px",
  fontWeight: "bold",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "block",
  padding: "12px 24px",
}
```

## Email Templates

### Welcome Email

```typescript
// emails/welcome.tsx
import {
  Section,
  Heading,
  Text,
} from "@react-email/components"
import { EmailLayout } from "./components/layout"
import { Button } from "./components/button"

interface WelcomeEmailProps {
  name: string
  dashboardUrl: string
}

export default function WelcomeEmail({ name, dashboardUrl }: WelcomeEmailProps) {
  return (
    <EmailLayout preview={`Welcome to our platform, ${name}!`}>
      <Section style={content}>
        <Heading style={heading}>Welcome aboard, {name}!</Heading>
        
        <Text style={paragraph}>
          We're excited to have you on board. Your account has been successfully created.
        </Text>
        
        <Text style={paragraph}>
          Here's what you can do next:
        </Text>
        
        <ul style={list}>
          <li>Complete your profile</li>
          <li>Explore the dashboard</li>
          <li>Invite your team members</li>
        </ul>
        
        <Button href={dashboardUrl}>
          Go to Dashboard
        </Button>
        
        <Text style={paragraph}>
          If you have any questions, feel free to reply to this email.
        </Text>
      </Section>
    </EmailLayout>
  )
}

const content = {
  padding: "24px",
}

const heading = {
  fontSize: "24px",
  lineHeight: "32px",
  fontWeight: "700",
  margin: "0 0 16px",
}

const paragraph = {
  fontSize: "16px",
  lineHeight: "24px",
  margin: "0 0 16px",
}

const list = {
  fontSize: "16px",
  lineHeight: "24px",
  marginBottom: "16px",
}
```

### Password Reset Email

```typescript
// emails/reset-password.tsx
import {
  Section,
  Heading,
  Text,
  Hr,
} from "@react-email/components"
import { EmailLayout } from "./components/layout"
import { Button } from "./components/button"

interface ResetPasswordEmailProps {
  name: string
  resetUrl: string
  expiresIn: string
}

export default function ResetPasswordEmail({
  name,
  resetUrl,
  expiresIn,
}: ResetPasswordEmailProps) {
  return (
    <EmailLayout preview="Reset your password">
      <Section style={content}>
        <Heading style={heading}>Reset your password</Heading>
        
        <Text style={paragraph}>Hi {name},</Text>
        
        <Text style={paragraph}>
          We received a request to reset your password. Click the button below to choose a new password.
        </Text>
        
        <Button href={resetUrl}>
          Reset Password
        </Button>
        
        <Text style={paragraph}>
          This link will expire in {expiresIn}.
        </Text>
        
        <Hr style={hr} />
        
        <Text style={small}>
          If you didn't request a password reset, you can safely ignore this email.
        </Text>
      </Section>
    </EmailLayout>
  )
}

const content = {
  padding: "24px",
}

const heading = {
  fontSize: "24px",
  lineHeight: "32px",
  fontWeight: "700",
  margin: "0 0 16px",
}

const paragraph = {
  fontSize: "16px",
  lineHeight: "24px",
  margin: "0 0 16px",
}

const hr = {
  borderColor: "#e6ebf1",
  margin: "20px 0",
}

const small = {
  fontSize: "14px",
  lineHeight: "20px",
  color: "#6b7280",
}
```

### Receipt Email

```typescript
// emails/receipt.tsx
import {
  Section,
  Heading,
  Text,
  Hr,
  Row,
  Column,
} from "@react-email/components"
import { EmailLayout } from "./components/layout"

interface ReceiptEmailProps {
  name: string
  orderId: string
  date: string
  items: Array<{
    name: string
    quantity: number
    price: number
  }>
  total: number
}

export default function ReceiptEmail({
  name,
  orderId,
  date,
  items,
  total,
}: ReceiptEmailProps) {
  return (
    <EmailLayout preview={`Receipt for order ${orderId}`}>
      <Section style={content}>
        <Heading style={heading}>Thanks for your order!</Heading>
        
        <Text style={paragraph}>Hi {name},</Text>
        
        <Text style={paragraph}>
          Your order has been confirmed. Here's a summary:
        </Text>
        
        <Section style={orderInfo}>
          <Text style={label}>Order ID: <strong>{orderId}</strong></Text>
          <Text style={label}>Date: {date}</Text>
        </Section>
        
        <Hr style={hr} />
        
        {items.map((item, index) => (
          <Row key={index} style={itemRow}>
            <Column>
              <Text style={itemName}>{item.name}</Text>
              <Text style={itemQuantity}>Qty: {item.quantity}</Text>
            </Column>
            <Column style={itemPriceColumn}>
              <Text style={itemPrice}>${item.price.toFixed(2)}</Text>
            </Column>
          </Row>
        ))}
        
        <Hr style={hr} />
        
        <Row style={totalRow}>
          <Column>
            <Text style={totalLabel}>Total</Text>
          </Column>
          <Column style={totalPriceColumn}>
            <Text style={totalPrice}>${total.toFixed(2)}</Text>
          </Column>
        </Row>
      </Section>
    </EmailLayout>
  )
}

const content = { padding: "24px" }
const heading = { fontSize: "24px", fontWeight: "700", margin: "0 0 16px" }
const paragraph = { fontSize: "16px", margin: "0 0 16px" }
const orderInfo = { backgroundColor: "#f6f9fc", padding: "16px", borderRadius: "4px", marginBottom: "16px" }
const label = { fontSize: "14px", margin: "4px 0" }
const hr = { borderColor: "#e6ebf1", margin: "20px 0" }
const itemRow = { marginBottom: "12px" }
const itemName = { fontSize: "16px", margin: "0" }
const itemQuantity = { fontSize: "14px", color: "#6b7280", margin: "4px 0 0" }
const itemPriceColumn = { textAlign: "right" as const }
const itemPrice = { fontSize: "16px", margin: "0" }
const totalRow = { marginTop: "8px" }
const totalLabel = { fontSize: "18px", fontWeight: "700", margin: "0" }
const totalPriceColumn = { textAlign: "right" as const }
const totalPrice = { fontSize: "18px", fontWeight: "700", margin: "0" }
```

## Sending Emails

### Using Resend (Recommended)

```typescript
// lib/email.server.ts
import { Resend } from "resend"
import { render } from "@react-email/render"
import WelcomeEmail from "~/emails/welcome"

const resend = new Resend(process.env.RESEND_API_KEY)

export async function sendWelcomeEmail(to: string, name: string, dashboardUrl: string) {
  const html = render(<WelcomeEmail name={name} dashboardUrl={dashboardUrl} />)
  
  await resend.emails.send({
    from: "noreply@yourapp.com",
    to,
    subject: "Welcome to Your App!",
    html,
  })
}

// Alternative: Using Resend with React component directly
export async function sendWelcomeEmailDirect(to: string, name: string, dashboardUrl: string) {
  await resend.emails.send({
    from: "noreply@yourapp.com",
    to,
    subject: "Welcome to Your App!",
    react: <WelcomeEmail name={name} dashboardUrl={dashboardUrl} />,
  })
}
```

### Using AWS SES

```typescript
// lib/email.server.ts
import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses"
import { render } from "@react-email/render"
import WelcomeEmail from "~/emails/welcome"

const ses = new SESClient({ region: "us-east-1" })

export async function sendWelcomeEmail(to: string, name: string, dashboardUrl: string) {
  const html = render(<WelcomeEmail name={name} dashboardUrl={dashboardUrl} />)
  const text = render(<WelcomeEmail name={name} dashboardUrl={dashboardUrl} />, {
    plainText: true,
  })
  
  const command = new SendEmailCommand({
    Source: "noreply@yourapp.com",
    Destination: { ToAddresses: [to] },
    Message: {
      Subject: { Data: "Welcome to Your App!" },
      Body: {
        Html: { Data: html },
        Text: { Data: text },
      },
    },
  })
  
  await ses.send(command)
}
```

## SST Integration

```typescript
// sst.config.ts
import { Config } from "sst/constructs"

export default {
  stacks(app) {
    app.stack(function Email({ stack }) {
      // Option 1: Resend API key
      const RESEND_API_KEY = new Config.Secret(stack, "RESEND_API_KEY")
      
      // Option 2: SES (no additional config needed)
      // Lambda functions automatically get SES permissions
      
      new RemixSite(stack, "site", {
        bind: [RESEND_API_KEY],
      })
    })
  },
}
```

## Email Best Practices

### Deliverability

```typescript
// 1. Verify sender domain
// Add SPF, DKIM, DMARC records to your DNS

// 2. Use proper from address
from: "Your Name <noreply@yourapp.com>"

// 3. Include unsubscribe link
<Link href={unsubscribeUrl} style={unsubscribeLink}>
  Unsubscribe
</Link>

// 4. Authenticate email domain
// With Resend: verify domain in dashboard
// With SES: verify domain and configure DKIM
```

### Content Guidelines

```typescript
// DO: Use plain, professional language
subject: "Your order #12345 has shipped"

// DON'T: Use spammy language
subject: "🔥 AMAZING DEAL!!! BUY NOW!!!"

// DO: Include clear CTAs
<Button href={url}>View Order</Button>

// DON'T: Use too many links
// Limit to 1-3 primary CTAs

// DO: Provide context
"You're receiving this because you signed up for updates on [date]"

// DON'T: Send without context
// Always explain why they're receiving the email
```

### Accessibility

```typescript
import { Img } from "@react-email/components"

// Always include alt text
<Img
  src="https://yourapp.com/logo.png"
  alt="Your App Logo"
  width="150"
  height="50"
/>

// Use semantic HTML
<Heading>Main Title</Heading>
<Text>Paragraph content</Text>

// Ensure good color contrast
const linkStyle = {
  color: "#0066cc",  // Good contrast with white background
  textDecoration: "underline",
}

// Use readable font sizes
const text = {
  fontSize: "16px",  // Minimum 14px
  lineHeight: "24px", // 1.5x font size
}
```

## Testing Emails

### Development Preview

```bash
# Start React Email dev server
npm run email:dev

# package.json
{
  "scripts": {
    "email:dev": "email dev"
  }
}

# Visit http://localhost:3000 to preview emails
```

### Send Test Emails

```typescript
// scripts/test-email.ts
import { sendWelcomeEmail } from "./lib/email.server"

await sendWelcomeEmail(
  "test@example.com",
  "Test User",
  "https://app.yourapp.com/dashboard"
)

console.log("Test email sent!")
```

### Email Testing Tools

```typescript
// Use Mailtrap for testing in development
const resend = new Resend(
  process.env.NODE_ENV === "production"
    ? process.env.RESEND_API_KEY
    : process.env.MAILTRAP_API_KEY
)

// Use Litmus or Email on Acid for rendering tests across clients
```

## Advanced Patterns

### Email with Attachments

```typescript
await resend.emails.send({
  from: "noreply@yourapp.com",
  to: email,
  subject: "Your Invoice",
  react: <InvoiceEmail />,
  attachments: [
    {
      filename: "invoice.pdf",
      content: pdfBuffer,
    },
  ],
})
```

### Scheduled Emails

```typescript
// Using EventBridge with SST
import { Cron } from "sst/constructs"

new Cron(stack, "DailySummary", {
  schedule: "cron(0 9 * * ? *)", // 9 AM daily
  job: "functions/send-daily-summary.handler",
})

// functions/send-daily-summary.ts
export async function handler() {
  const users = await getActiveUsers()
  
  for (const user of users) {
    await sendDailySummaryEmail(user.email, user.name, user.stats)
  }
}
```

### Email Analytics

```typescript
// Track opens and clicks with Resend
await resend.emails.send({
  from: "noreply@yourapp.com",
  to: email,
  subject: "Your Report",
  react: <ReportEmail />,
  tags: [
    { name: "category", value: "report" },
    { name: "user_id", value: userId },
  ],
})

// Query analytics
const analytics = await resend.emails.get(emailId)
console.log(analytics.opens, analytics.clicks)
```

## Common Email Types

```typescript
// Welcome series
export const welcomeEmails = [
  { delay: 0, template: "welcome", subject: "Welcome!" },
  { delay: 1, template: "getting-started", subject: "Getting Started Guide" },
  { delay: 3, template: "tips", subject: "Pro Tips for Success" },
]

// Transactional
- Welcome email
- Email verification
- Password reset
- Receipt/invoice
- Shipping notification
- Account changes

// Engagement
- Weekly summary
- Achievement unlocked
- Abandoned cart
- Re-engagement
- Product updates
```

## Resources

- [React Email Documentation](https://react.email/docs)
- [Resend Documentation](https://resend.com/docs)
- [AWS SES Best Practices](https://docs.aws.amazon.com/ses/latest/dg/best-practices.html)
- [Email on Acid](https://www.emailonacid.com/)
- [Can I email](https://www.caniemail.com/) - Email client support tables
