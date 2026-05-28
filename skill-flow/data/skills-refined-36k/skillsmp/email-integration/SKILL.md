---
name: Email Integration
description: Transactional emails, templates, and email service integration
---

# Email Integration Skill

## Email Services

### Resend (Recommended)
```bash
npm install resend
```

```javascript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendEmail({ to, subject, html }) {
  const { data, error } = await resend.emails.send({
    from: 'Smarter.Poker <noreply@smarter.poker>',
    to,
    subject,
    html
  });
  
  if (error) throw error;
  return data;
}
```

### SendGrid
```javascript
import sgMail from '@sendgrid/mail';
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

await sgMail.send({
  to: 'user@example.com',
  from: 'noreply@smarter.poker',
  subject: 'Welcome to Smarter.Poker',
  html: '<h1>Welcome!</h1>'
});
```

### Nodemailer (SMTP)
```javascript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
});

await transporter.sendMail({
  from: 'noreply@smarter.poker',
  to: 'user@example.com',
  subject: 'Test',
  html: '<p>Hello</p>'
});
```

## React Email Templates
```bash
npm install @react-email/components react-email
```

```jsx
// emails/welcome.tsx
import { Html, Head, Body, Container, Text, Button } from '@react-email/components';

export default function WelcomeEmail({ username }) {
  return (
    <Html>
      <Head />
      <Body style={main}>
        <Container>
          <Text>Welcome to Smarter.Poker, {username}!</Text>
          <Button href="https://smarter.poker/training">
            Start Training
          </Button>
        </Container>
      </Body>
    </Html>
  );
}

const main = {
  backgroundColor: '#f6f9fc',
  fontFamily: 'sans-serif'
};
```

### Render Template
```javascript
import { render } from '@react-email/render';
import WelcomeEmail from './emails/welcome';

const html = render(<WelcomeEmail username="Dan" />);
```

## Common Email Types

### Welcome Email
```javascript
export const sendWelcomeEmail = async (user) => {
  await sendEmail({
    to: user.email,
    subject: 'Welcome to Smarter.Poker! 🎰',
    html: render(<WelcomeEmail user={user} />)
  });
};
```

### Password Reset
```javascript
export const sendPasswordReset = async (email, resetLink) => {
  await sendEmail({
    to: email,
    subject: 'Reset Your Password',
    html: render(<PasswordResetEmail resetLink={resetLink} />)
  });
};
```

### Transaction Receipt
```javascript
export const sendReceipt = async (user, purchase) => {
  await sendEmail({
    to: user.email,
    subject: `Receipt for Order #${purchase.id}`,
    html: render(<ReceiptEmail purchase={purchase} />)
  });
};
```

## Supabase Auth Emails
Supabase handles auth emails automatically. Customize in:
- Dashboard > Authentication > Email Templates

## Best Practices
- Use a verified sending domain (SPF, DKIM, DMARC)
- Keep emails mobile-friendly
- Include unsubscribe links for marketing
- Track opens/clicks for analytics
- Use transactional emails for user-triggered actions only
