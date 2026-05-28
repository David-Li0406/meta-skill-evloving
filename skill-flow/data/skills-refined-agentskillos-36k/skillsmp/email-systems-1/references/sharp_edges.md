# Email Systems - Sharp Edges

## No Authentication Records

### **Id**
no-authentication-records
### **Summary**
Missing SPF, DKIM, or DMARC records
### **Severity**
critical
### **Situation**
  Sending emails without authentication. Emails going to spam folder.
  Low open rates. No idea why. Turns out DNS records were never set up.
  
### **Why**
  Email authentication (SPF, DKIM, DMARC) tells receiving servers you're
  legit. Without them, you look like a spammer. Modern email providers
  increasingly require all three.
  
### **Solution**
  # Required DNS records:
  
  ## SPF (Sender Policy Framework)
  TXT record: v=spf1 include:_spf.google.com include:sendgrid.net ~all
  
  ## DKIM (DomainKeys Identified Mail)
  TXT record provided by your email provider
  Adds cryptographic signature to emails
  
  ## DMARC (Domain-based Message Authentication)
  TXT record: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
  
  # Verify setup:
  - Send test email to mail-tester.com
  - Check MXToolbox for record validation
  - Monitor DMARC reports
  
### **Symptoms**
  - Emails going to spam
  - Low deliverability rates
  - mail-tester.com score below 8
  - No DMARC reports received
### **Detection Pattern**


## Shared Ip Reputation

### **Id**
shared-ip-reputation
### **Summary**
Using shared IP for transactional email
### **Severity**
high
### **Situation**
  Password resets going to spam. Using free tier of email provider.
  Some other customer on your shared IP got flagged for spam.
  Your reputation is ruined by association.
  
### **Why**
  Shared IPs share reputation. One bad actor affects everyone. For
  critical transactional email, you need your own IP or a provider
  with strict shared IP policies.
  
### **Solution**
  # Transactional email strategy:
  
  ## Option 1: Dedicated IP (high volume)
  - Get dedicated IP from your provider
  - Warm it up slowly (start with 100/day)
  - Maintain consistent volume
  
  ## Option 2: Transactional-only provider
  - Postmark (very strict, great reputation)
  - Includes shared pool with high standards
  
  ## Separate concerns:
  - Transactional: Postmark or Resend
  - Marketing: ConvertKit or Customer.io
  - Never mix marketing and transactional
  
### **Symptoms**
  - Transactional emails in spam
  - Inconsistent delivery
  - Using same provider for marketing and transactional
### **Detection Pattern**


## No Bounce Handling

### **Id**
no-bounce-handling
### **Summary**
Not processing bounce notifications
### **Severity**
high
### **Situation**
  Emailing same dead addresses over and over. Bounce rate climbing.
  Email provider threatening to suspend account. List is 40% dead.
  
### **Why**
  Bounces damage sender reputation. Email providers track bounce rates.
  Above 2% and you start looking like a spammer. Dead addresses must
  be removed immediately.
  
### **Solution**
  # Bounce handling requirements:
  
  ## Hard bounces:
  Remove immediately on first occurrence
  Invalid address, domain doesn't exist
  
  ## Soft bounces:
  Retry 3 times over 72 hours
  After 3 failures, treat as hard bounce
  
  ## Implementation:
  ```typescript
  // Webhook handler for bounces
  app.post('/webhooks/email', (req, res) => {
    const event = req.body;
    if (event.type === 'bounce') {
      await markEmailInvalid(event.email);
      await removeFromAllLists(event.email);
    }
  });
  ```
  
  ## Monitor:
  Track bounce rate by campaign
  Alert if bounce rate exceeds 1%
  
### **Symptoms**
  - Bounce rate above 2%
  - No webhook handlers for bounces
  - Same emails failing repeatedly
### **Detection Pattern**


## No Unsubscribe

### **Id**
no-unsubscribe
### **Summary**
Missing or hidden unsubscribe link
### **Severity**
critical
### **Situation**
  Users marking as spam because they cannot unsubscribe. Spam complaints
  rising. CAN-SPAM violation. Email provider suspends account.
  
### **Why**
  Users who cannot unsubscribe will mark as spam. Spam complaints hurt
  reputation more than unsubscribes. Also it is literally illegal.
  CAN-SPAM, GDPR all require clear unsubscribe.
  
### **Solution**
  # Unsubscribe requirements:
  
  ## Visible:
  - Above the fold in email footer
  - Clear text, not hidden
  - Not styled to be invisible
  
  ## One-click:
  - Link directly unsubscribes
  - No login required
  - No "are you sure" hoops
  
  ## List-Unsubscribe header:
  ```
  List-Unsubscribe: <mailto:unsubscribe@example.com>,
    <https://example.com/unsubscribe?token=xxx>
  List-Unsubscribe-Post: List-Unsubscribe=One-Click
  ```
  
  ## Preference center:
  Option to reduce frequency instead of full unsubscribe
  
### **Symptoms**
  - Hidden unsubscribe links
  - Multi-step unsubscribe process
  - No List-Unsubscribe header
  - High spam complaint rate
### **Detection Pattern**


## Html Only Emails

### **Id**
html-only-emails
### **Summary**
Sending HTML without plain text alternative
### **Severity**
medium
### **Situation**
  Some users see blank emails. Spam filters flagging emails. Accessibility
  issues for screen readers. Email clients that strip HTML show nothing.
  
### **Why**
  Not everyone can render HTML. Screen readers work better with plain text.
  Spam filters are suspicious of HTML-only. Multipart is the standard.
  
### **Solution**
  # Always send multipart:
  ```typescript
  await resend.emails.send({
    from: 'you@example.com',
    to: 'user@example.com',
    subject: 'Welcome!',
    html: '<h1>Welcome!</h1><p>Thanks for signing up.</p>',
    text: 'Welcome!\n\nThanks for signing up.',
  });
  ```
  
  # Auto-generate text from HTML:
  Use html-to-text library as fallback
  But hand-crafted plain text is better
  
  # Plain text should be readable:
  Not just HTML stripped of tags
  Actual formatted text content
  
### **Symptoms**
  - No text/plain part in emails
  - Blank emails for some users
  - Lower engagement in some segments
### **Detection Pattern**
html:.*(?!text:)

## No Warm Up

### **Id**
no-warm-up
### **Summary**
Sending high volume from new IP immediately
### **Severity**
high
### **Situation**
  Just switched providers. Started sending 50,000 emails/day immediately.
  Massive deliverability issues. New IP has no reputation. Looks like spam.
  
### **Why**
  New IPs have no reputation. Sending high volume immediately looks
  like a spammer who just spun up. You need to gradually build trust.
  
### **Solution**
  # IP warm-up schedule:
  
  Week 1: 50-100 emails/day
  Week 2: 200-500 emails/day
  Week 3: 500-1000 emails/day
  Week 4: 1000-5000 emails/day
  Continue doubling until at volume
  
  # Best practices:
  - Start with most engaged users
  - Send to Gmail/Microsoft first (they set reputation)
  - Maintain consistent volume
  - Don't spike and drop
  
  # During warm-up:
  - Monitor deliverability closely
  - Check feedback loops
  - Adjust pace if issues arise
  
### **Symptoms**
  - New IP/provider
  - Sending high volume immediately
  - Sudden deliverability drop
### **Detection Pattern**


## Sending Without Permission

### **Id**
sending-without-permission
### **Summary**
Emailing people who did not opt in
### **Severity**
critical
### **Situation**
  Bought an email list. Scraped emails from LinkedIn. Added conference
  contacts. Spam complaints through the roof. Provider suspends account.
  Maybe a lawsuit.
  
### **Why**
  Permission-based email is not optional. It is the law (CAN-SPAM, GDPR).
  It is also effective - unwilling recipients hurt your metrics and
  reputation more than they help.
  
### **Solution**
  # Permission requirements:
  
  ## Explicit opt-in:
  - User actively chooses to receive email
  - Not pre-checked boxes
  - Clear what they are signing up for
  
  ## Double opt-in:
  - Confirmation email with link
  - Only add to list after confirmation
  - Best practice for marketing lists
  
  ## What you cannot do:
  - Buy email lists
  - Scrape emails from websites
  - Add conference contacts without consent
  - Use partner/customer lists without consent
  
  ## Transactional exception:
  Password resets, receipts, account alerts
  do not need marketing opt-in
  
### **Symptoms**
  - Purchased email lists
  - Scraped contacts
  - High unsubscribe rate on first send
  - Spam complaints above 0.1%
### **Detection Pattern**


## Image Heavy Emails

### **Id**
image-heavy-emails
### **Summary**
Emails that are mostly or entirely images
### **Severity**
medium
### **Situation**
  Beautiful designed email that is one big image. Users with images
  blocked see nothing. Spam filters flag it. Mobile loading is slow.
  No one can copy text.
  
### **Why**
  Images are blocked by default in many clients. Spam filters are
  suspicious of image-only emails. Accessibility suffers. Load times
  increase.
  
### **Solution**
  # Balance images and text:
  
  ## 60/40 rule:
  - At least 60% text content
  - Images for enhancement, not content
  
  ## Always include:
  - Alt text on every image
  - Key message in text, not just image
  - Fallback for images-off view
  
  ## Test:
  - Preview with images disabled
  - Should still be usable
  
  # Example:
  ```html
  <img
    src="hero.jpg"
    alt="Save 50% this week - use code SAVE50"
    style="max-width: 100%"
  />
  <p>Use code <strong>SAVE50</strong> to save 50% this week.</p>
  ```
  
### **Symptoms**
  - Single image emails
  - No text content visible
  - Missing or generic alt text
  - Low engagement when images blocked
### **Detection Pattern**


## No Preview Text

### **Id**
no-preview-text
### **Summary**
Missing or default preview text
### **Severity**
medium
### **Situation**
  Inbox shows "View this email in browser" or random HTML as preview.
  Lower open rates. First impression wasted on boilerplate.
  
### **Why**
  Preview text is prime real estate - appears right after subject line.
  Default or missing preview text wastes this space. Good preview text
  increases open rates 10-30%.
  
### **Solution**
  # Add explicit preview text:
  
  ## In HTML:
  ```html
  <div style="display:none;max-height:0;overflow:hidden;">
    Your preview text here. This appears in inbox preview.
    <!-- Add whitespace to push footer text out -->
    &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
  </div>
  ```
  
  ## With React Email:
  ```tsx
  <Preview>
    Your preview text here. This appears in inbox preview.
  </Preview>
  ```
  
  ## Best practices:
  - Complement the subject line
  - 40-100 characters optimal
  - Create curiosity or value
  - Different from first line of email
  
### **Symptoms**
  - View in browser as preview
  - HTML code visible in preview
  - No preview component in template
### **Detection Pattern**


## Batch Sending Errors

### **Id**
batch-sending-errors
### **Summary**
Not handling partial send failures
### **Severity**
high
### **Situation**
  Sending to 10,000 users. API fails at 3,000. No tracking of what sent.
  Either double-send or lose 7,000. No way to know who got the email.
  
### **Why**
  Bulk sends fail partially. APIs timeout. Rate limits hit. Without
  tracking individual send status, you cannot recover gracefully.
  
### **Solution**
  # Track each send individually:
  
  ```typescript
  async function sendCampaign(emails: string[]) {
    const results = await Promise.allSettled(
      emails.map(async (email) => {
        try {
          const result = await resend.emails.send({ to: email, ... });
          await db.emailLog.create({
            email,
            status: 'sent',
            messageId: result.id,
          });
          return result;
        } catch (error) {
          await db.emailLog.create({
            email,
            status: 'failed',
            error: error.message,
          });
          throw error;
        }
      })
    );
  
    const failed = results.filter(r => r.status === 'rejected');
    // Retry failed sends or alert
  }
  ```
  
  # Best practices:
  - Log every send attempt
  - Include message ID for tracking
  - Build retry queue for failures
  - Monitor success rate per campaign
  
### **Symptoms**
  - No per-recipient send logging
  - Cannot tell who received email
  - Double-sending issues
  - No retry mechanism
### **Detection Pattern**
