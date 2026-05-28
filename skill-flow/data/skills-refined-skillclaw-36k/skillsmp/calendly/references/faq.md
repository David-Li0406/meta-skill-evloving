# Calendly API FAQ

## Subscription & Access

### What API access do I have on the Free plan?
Developers can make GET and POST requests to most API endpoints on any subscription plan, including Free. However, webhooks require Standard, Teams, or Enterprise plans. Some Enterprise-specific endpoints are restricted to Enterprise accounts.

### Do I need admin access for organization endpoints?
Yes, organization-level endpoints (like listing all members) require admin or owner permissions. These permissions are managed through the People/Admin Management page in Calendly.

## Authentication

### When are personal access tokens revoked?
Tokens are automatically revoked when you:
- Change your email address
- Change your password
- Change your login method (e.g., from Google to password-based)

### How do I revoke OAuth tokens?
OAuth tokens can be revoked programmatically via the API revocation endpoint. Personal access tokens must be revoked through your API & Webhooks page in Calendly settings.

### Can I have multiple personal access tokens?
Yes, and it's recommended to create separate tokens for each application or integration. This allows you to revoke access to specific integrations without affecting others.

## Event Management

### Can I create events via the API?
No, the API does not support creating scheduled events directly. To allow booking, use the embed widgets (inline, popup, or badge) on your website. Users must go through the scheduling flow to create events.

### Can I cancel events via the API?
Yes, use the cancel event endpoint. This cancels the entire event and all invitees. You cannot cancel individual invitees within a group event.

### Can I reschedule events via the API?
There's no direct reschedule endpoint. However, the invitee resource includes `cancel_url` and `reschedule_url` that you can provide to users. These URLs also appear in webhook payloads.

### Why does rescheduling trigger two webhook events?
Rescheduling is handled as a cancellation of the original event plus creation of a new event. You'll receive:
1. `invitee.canceled` for the original booking
2. `invitee.created` for the new booking

The new invitee payload will reference the old event in the `old_invitee` field.

## Event Types & Availability

### Can I create or edit event types via the API?
No, event type management is only available through the Calendly UI. To manage event types, users must visit their Event Types page within their Calendly account.

### Can I set availability via the API?
No, availability scheduling is not supported via the API. Users must set their availability through the Event Types page in Calendly. You can read availability schedules and busy times via the API, but not modify them.

## Data Retrieval

### How do I get user and organization URIs?
Call the `/users/me` endpoint:
- User URI is in the `uri` field
- Organization URI is in the `current_organization` field

For other users in your organization, use the `/organization_memberships` endpoint with admin permissions.

### How do I get complete invitee information?
The webhook payload contains basic invitee info. For complete details (including all custom question responses), use the Get Event Invitee endpoint:
```
GET /scheduled_events/{event_uuid}/invitees/{invitee_uuid}
```

### Can I see events for users who left the organization?
Yes, if you're an admin/owner. Events for removed users remain visible when querying with the organization parameter instead of the user parameter.

## Webhooks

### Why aren't my webhooks working?
Common issues:
1. **Plan limitation**: Webhooks require Standard, Teams, or Enterprise
2. **HTTPS required**: Your endpoint must use HTTPS
3. **Response timeout**: Return 200 status within 10 seconds
4. **Incorrect scope**: Ensure webhook scope matches your needs

### How do I track where bookings come from?
Use UTM parameters in your scheduling links:
```
https://calendly.com/your-link?utm_source=email&utm_campaign=outreach
```

These values appear in:
- Webhook payloads under `payload.tracking`
- Invitee listings via the API

Available parameters: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`

## Scheduling Links

### Do single-use scheduling links expire?
Yes, single-use links expire after 90 days, even if unused.

### Can I create scheduling links programmatically?
Yes, use the `/scheduling_links` endpoint to create single-use links tied to specific event types.

## API Limits

### Is there rate limiting?
Yes, Calendly implements rate limiting. If you receive a 429 status code, implement exponential backoff in your requests.

### What's the maximum results per page?
Most list endpoints return 20 results by default, with a maximum of 100. Use the `count` parameter and pagination tokens for larger datasets.

## Migration

### Is API v1 still supported?
API v1 support is being phased out starting May 2025. All new integrations should use API v2, and existing v1 integrations should be migrated.

### Is API v2 backwards compatible with v1?
No, API v2 is not backwards compatible. Data structures, endpoints, and authentication methods have changed. You must update your code to work with v2 responses.

### How do I migrate from v1 to v2?
1. Update authentication from API key to Personal Access Token or OAuth
2. Update endpoint URLs to v2 format
3. Update code to handle v2 response structures
4. Update webhook subscriptions to v2 format
5. Test thoroughly before switching production traffic

## Support

### Where can I get help?
- Documentation: https://developer.calendly.com/
- Help Center: https://help.calendly.com/
- Developer Support: support+developer@calendly.com
