# Email Systems

## Patterns


---
  #### **Name**
Transactional Email Queue
  #### **Description**
Queue all transactional emails with retry logic and monitoring
  #### **When**
Sending any critical email (password reset, receipts, confirmations)
  #### **Example**
    // Don't block request on email send
    await queue.add('email', {
      template: 'password-reset',
      to: user.email,
      data: { resetToken, expiresAt }
    }, {
      attempts: 3,
      backoff: { type: 'exponential', delay: 2000 }
    });
    

---
  #### **Name**
Email Event Tracking
  #### **Description**
Track delivery, opens, clicks, bounces, and complaints
  #### **When**
Any email campaign or transactional flow
  #### **Example**
    # Track lifecycle:
    - Queued: Email entered system
    - Sent: Handed to provider
    - Delivered: Reached inbox
    - Opened: Recipient viewed
    - Clicked: Recipient engaged
    - Bounced: Permanent failure
    - Complained: Marked as spam
    

---
  #### **Name**
Template Versioning
  #### **Description**
Version email templates for rollback and A/B testing
  #### **When**
Changing production email templates
  #### **Example**
    templates/
      password-reset/
        v1.tsx (current)
        v2.tsx (testing 10%)
        v1-deprecated.tsx (archived)
    
    # Deploy new version gradually
    # Monitor metrics before full rollout
    

---
  #### **Name**
Bounce Handling State Machine
  #### **Description**
Automatically handle bounces to protect sender reputation
  #### **When**
Processing bounce and complaint webhooks
  #### **Example**
    switch (bounceType) {
      case 'hard':
        await markEmailInvalid(email);
        break;
      case 'soft':
        await incrementBounceCount(email);
        if (count >= 3) await markEmailInvalid(email);
        break;
      case 'complaint':
        await unsubscribeImmediately(email);
        break;
    }
    

---
  #### **Name**
React Email Components
  #### **Description**
Build emails with reusable React components
  #### **When**
Creating email templates
  #### **Example**
    import { Button, Html } from '@react-email/components';
    
    export default function WelcomeEmail({ userName }) {
      return (
        <Html>
          <h1>Welcome {userName}!</h1>
          <Button href="https://app.com/start">
            Get Started
          </Button>
        </Html>
      );
    }
    

---
  #### **Name**
Preference Center
  #### **Description**
Let users control email frequency and topics
  #### **When**
Building marketing or notification systems
  #### **Example**
    Preferences:
    ☑ Product updates (weekly)
    ☑ New features (monthly)
    ☐ Marketing promotions
    ☑ Account notifications (always)
    
    # Respect preferences in all sends
    # Required for GDPR compliance
    

## Anti-Patterns


---
  #### **Name**
HTML email soup
  #### **Description**
Complex HTML with broken rendering across clients
  #### **Example**
Tables nested 10 deep, custom fonts, complex CSS
  #### **Why Bad**
Email clients render differently. Outlook breaks everything.
  #### **Fix**
Use email-first frameworks (MJML, React Email). Test in Litmus/Email on Acid.

---
  #### **Name**
No plain text fallback
  #### **Description**
Sending HTML-only emails
  #### **Example**
Only HTML version, no text/plain multipart
  #### **Why Bad**
Some clients strip HTML. Accessibility issues. Spam signal.
  #### **Fix**
Always include plain text version with key info.

---
  #### **Name**
Huge image emails
  #### **Description**
Emails that are mostly images with little text
  #### **Example**
One big image as the entire email body
  #### **Why Bad**
Images blocked by default. Spam trigger. Slow loading.
  #### **Fix**
Real text with images as enhancement. Alt text on images.

---
  #### **Name**
No monitoring
  #### **Description**
Sending emails without tracking deliverability
  #### **Example**
Fire and forget, no bounce handling, no feedback loops
  #### **Why Bad**
Silent failures. List decay. Reputation damage.
  #### **Fix**
Track bounces, complaints, opens. Remove bad addresses. Set up feedback loops.

---
  #### **Name**
Personalization theater
  #### **Description**
Fake personalization that insults intelligence
  #### **Example**
"Hi {first_name}," with nothing else personalized
  #### **Why Bad**
Token personalization is transparent. Actually annoying.
  #### **Fix**
Real personalization based on behavior, or don't fake it.