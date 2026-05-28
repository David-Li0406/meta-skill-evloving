# GHL Troubleshooting Guide

## "Contact not created in GHL"

**Check:**
1. API key valid? Test: `ghlClient.contacts.list()`
2. LocationId correct? Settings → Business Profile
3. Rate limited? Use Redis cache (100 req/10sec limit)
4. Webhook error? Settings → Integrations → Webhooks logs

## "Workflow not triggering"

**Check:**
1. Workflow "Published" not "Draft"?
2. Contact has required tags for trigger?
3. Contact opted out of emails?
4. Workflow conditions met? (e.g., "only if field X = Y")

## "Pipeline stage not updating"

**Check:**
1. Opportunity exists? (contact can exist without pipeline entry)
2. Stage IDs match? (get from GHL API or UI URL)
3. Workflow has permission to update pipeline?

## "Email deliverability issues"

**Solutions:**
- Use Resend for transactional (higher deliverability)
- Verify sender domain: Settings → Email Services
- Check spam score: mail-tester.com
- Avoid spam triggers: "free", "guarantee", excessive !!!!

## "Rate limit exceeded"

**Solutions:**
1. Implement retry with exponential backoff
2. Use Redis cache for repeated lookups
3. Batch operations where possible
4. Monitor headers:
   - `x-ratelimit-remaining`
   - `x-ratelimit-daily-remaining`

## "Webhook signature invalid"

**Check:**
1. Using correct secret from GHL webhook config
2. Body parsed as raw text (not JSON) before verification
3. HMAC using SHA256 algorithm
4. Comparing hex digest

## "Stripe payment not updating GHL"

**Check:**
1. Webhook URL correct in Stripe dashboard
2. Events selected: `checkout.session.completed`
3. Metadata includes `contactId`
4. GHL custom field names match exactly

## "Supabase user not syncing"

**Check:**
1. Trigger function deployed on auth.users
2. Environment variables set in Supabase
3. GHL API accessible from Supabase Edge Functions
4. Error logs in Supabase dashboard

## API Reference

- GHL Docs: https://marketplace.gohighlevel.com/docs/
- OAuth Helper: https://www.ghlapiv2.com/
- Webhook Docs: https://marketplace.gohighlevel.com/docs/webhook/
