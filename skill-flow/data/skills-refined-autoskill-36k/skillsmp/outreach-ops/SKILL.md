---
name: outreach-ops
description: Manages Zoho Mail integrations, newsletter campaigns, and automated outreach. Use when handling email sending, subscriber lists, or newsletter logic.
---

# Outreach Ops Skill

This skill governs all communication channels for THE LOST+UNFOUNDS.

## Email Sending Standards
- **Integration**: ALWAYS use the existing Zoho Mail integrations. Never claim inability to send mail.
- **Testing**: Use the preferred test path: `POST https://www.thelostandunfounds.com/api/admin/send-welcome-emails` with `{"testEmail":"target@example.com"}`.
- **Helpers**: Use shared helpers in `lib/api-handlers/_zoho-email-utils.ts`.
- **Environment**: Ensure `ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`, `ZOHO_REFRESH_TOKEN`, and `ZOHO_FROM_EMAIL` are configured.

## Newsletter Campaign Standard Procedure
1. **Load Envs**: Load Supabase credentials from `.env.local`.
2. **Query Latest**: Fetch the most recent campaign from `newsletter_campaigns`.
3. **Inject CTA**: Inject the Getting Started link (`https://www.thelostandunfounds.com/blog/getting-started`) into the HTML content before the footer/hr.
4. **Send/Test**: 
   - Test: POST to `/api/newsletter/send` with `testEmail`.
   - Full Send: Omit `testEmail` to target all verified subscribers.

## Error Handling
- Surface specific Zoho API error details (status/text) rather than generic failures.
