---
name: brand-email-manager
description: Ensures all outgoing emails follow THE LOST+UNFOUNDS branding guidelines using the standardized template in `lib/email-template.ts`.
---

# Brand Email Manager Skill

This skill ensures that every email sent by the application (transactional, newsletters, notifications) adheres to the official THE LOST+UNFOUNDS brand identity.

## Core Principles
1. **Never Hardcode HTML**: Do not write raw HTML for email bodies in handlers or servers.
2. **Use the Standard Template**: Always import and use `wrapEmailContent`, `generateNewsletterEmail`, or `generateTransactionalEmail` from `lib/email-template.ts`.
3. **Mandatory Banner**: Every email must start with the official full-width black banner image.
4. **Consistent Typography**: Use the `EMAIL_STYLES` constants for headings, paragraphs, and buttons.
5. **Centered Alignment**: Brand communication (Transactional and Newsletter) is CENTERED by default. (Exception: Internal/Admin logs).

## Usage Patterns

### 1. Transactional Emails (Orders, Welcomes)
Use `generateTransactionalEmail` to wrap your content. It includes the brand logo and footer but excludes the unsubscribe link.

```typescript
import { generateTransactionalEmail, EMAIL_STYLES } from '@/lib/email-template';

const body = `
  <h1 style="${EMAIL_STYLES.heading1}">ORDER CONFIRMED</h1>
  <p style="${EMAIL_STYLES.paragraph}">Thank you for your purchase.</p>
  <a href="${url}" style="${EMAIL_STYLES.button}">ACCESS GALLERY</a>
`;

const html = generateTransactionalEmail(body);
```

### 2. Newsletter Emails
Use `generateNewsletterEmail`. It automatically handles unsubscribe link injection.

```typescript
import { generateNewsletterEmail } from '@/lib/email-template';

const html = generateNewsletterEmail(campaignContent, subscriberEmail);
```

### 3. Verification & Auditing
- **Logo URL**: Always ensure the logo points to `https://nonaqhllakrckbtbawrb.supabase.co/storage/v1/object/public/brand-assets/1764772922060_IMG_1244.png`.
- **Colors**: Background should be `#000000`, text `#ffffff`.
- **Alignment**: Transactional emails often use centered headers but left-aligned paragraphs.

## Common Pitfalls
- **Missing Shell**: Forgetting to add `<!DOCTYPE html>` or `<html>` tags. `wrapEmailContent` handles this for you.
- **Inconsistent Buttons**: Using different padding or colors for buttons. Always use `EMAIL_STYLES.button`.
- **Relative URLs**: Emails must use absolute URLs for all links and images.
