---
name: calendly
description: Calendly API v2 documentation for scheduling automation, embedding Calendly widgets, webhooks, and building integrations with Calendly's scheduling platform
---

# Calendly API Skill

Complete reference for integrating with Calendly's scheduling platform using their REST API v2, Embed API, and Webhook API.

## When to Use This Skill

This skill should be triggered when:
- Integrating Calendly scheduling into an application
- Working with Calendly API endpoints
- Setting up webhooks for scheduling events
- Embedding Calendly scheduling widgets on websites
- Authenticating with Calendly using OAuth 2.0 or Personal Access Tokens
- Retrieving user, event, or organization data from Calendly
- Migrating from Calendly API v1 to v2

## Quick Reference

### Available APIs

| API | Purpose | Use Case |
|-----|---------|----------|
| **API v2** | REST API for data operations | Retrieve users, events, organizations |
| **Embed API** | Add scheduling pages to websites | Website integrations |
| **Webhook API** | Real-time event notifications | Automated workflows |

### Authentication Methods

**Personal Access Tokens** - For internal/private applications:
```bash
# Generate in Calendly: Integrations > API & Webhooks > Generate Token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.calendly.com/users/me
```

**OAuth 2.0** - For public applications serving multiple users:
```bash
# Authorization URL
https://auth.calendly.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=YOUR_REDIRECT_URI

# Token Exchange
POST https://auth.calendly.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&code=AUTH_CODE&client_id=YOUR_CLIENT_ID&client_secret=YOUR_SECRET&redirect_uri=YOUR_REDIRECT_URI
```

### Key API Endpoints

```bash
# Get Current User
GET https://api.calendly.com/users/me

# List Organization Memberships
GET https://api.calendly.com/organization_memberships?organization=ORG_URI

# List Event Types
GET https://api.calendly.com/event_types?user=USER_URI

# List Scheduled Events
GET https://api.calendly.com/scheduled_events?user=USER_URI

# Get Event Invitee Details
GET https://api.calendly.com/scheduled_events/{event_uuid}/invitees/{invitee_uuid}

# Cancel Event
POST https://api.calendly.com/scheduled_events/{event_uuid}/cancellation
```

### Embed Widget Examples

**Inline Embed:**
```html
<!-- Add Calendly CSS and JS -->
<link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
<script src="https://assets.calendly.com/assets/external/widget.js" type="text/javascript" async></script>

<!-- Container for the widget -->
<div class="calendly-inline-widget" style="min-width:320px;height:630px;" data-url="https://calendly.com/your-link"></div>
```

**JavaScript Initialization:**
```javascript
// Inline Widget
Calendly.initInlineWidget({
  url: 'https://calendly.com/your-link',
  parentElement: document.getElementById('calendly-container'),
  prefill: {
    name: 'John Doe',
    email: 'john@example.com'
  }
});

// Popup Widget
Calendly.initPopupWidget({
  url: 'https://calendly.com/your-link'
});

// Badge Widget
Calendly.initBadgeWidget({
  url: 'https://calendly.com/your-link',
  text: 'Schedule time with me',
  color: '#006bff',
  textColor: '#ffffff',
  branding: true
});
```

### Webhook Events

| Event | Trigger |
|-------|---------|
| `invitee.created` | New meeting scheduled |
| `invitee.canceled` | Meeting canceled |
| `invitee.rescheduled` | Meeting rescheduled (fires canceled + created) |

**Create Webhook Subscription:**
```bash
POST https://api.calendly.com/webhook_subscriptions
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "url": "https://your-domain.com/webhooks/calendly",
  "events": ["invitee.created", "invitee.canceled"],
  "organization": "https://api.calendly.com/organizations/YOUR_ORG_UUID",
  "scope": "organization"
}
```

### UTM Tracking Parameters

Pass tracking data through scheduling links:
```
https://calendly.com/your-link?utm_source=website&utm_medium=button&utm_campaign=demo
```

Available parameters: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`

These appear in webhook payloads and invitee listings.

## Subscription Requirements

| Feature | Plan Required |
|---------|---------------|
| API v2 GET/POST requests | Free (most endpoints) |
| Webhooks | Standard, Teams, or Enterprise |
| Enterprise endpoints | Enterprise |
| Admin-level permissions | Teams or Enterprise |

## Important Limitations

- **No event creation via API** - Use embed widgets instead
- **No availability management** - Set via Event Types page in Calendly
- **No event type creation/editing** - Manage in Calendly account
- **Single-use links expire** after 90 days

## Token Revocation Scenarios

Personal access tokens are revoked when:
- Email address changed
- Password changed
- Login method changed (e.g., Google to password)

OAuth tokens can be manually revoked via API endpoint.

## Reference Files

Detailed documentation in `references/`:
- **getting_started.md** - API overview and authentication setup
- **api_reference.md** - Complete endpoint documentation
- **webhooks.md** - Webhook setup and payload formats
- **embedding.md** - Widget implementation guide
- **faq.md** - Common questions and troubleshooting
- **migration.md** - API v1 to v2 migration guide

## Resources

- [Calendly Developer Portal](https://developer.calendly.com/)
- [API Reference](https://developer.calendly.com/api-docs)
- [Help Center](https://help.calendly.com/)
- Support: support+developer@calendly.com

## Notes

- API v1 support ends May 2025 - migrate to v2
- API v2 is not backwards compatible with v1
- Always use HTTPS for API calls
- Rate limiting applies - implement exponential backoff
