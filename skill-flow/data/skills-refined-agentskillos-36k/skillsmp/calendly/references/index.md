# Calendly API Documentation Index

This skill contains comprehensive documentation for integrating with Calendly's scheduling platform.

## Reference Files

### [getting_started.md](getting_started.md)
Introduction to Calendly's APIs, authentication methods, and first steps for integration.
- API v2, Embed API, and Webhook API overview
- Personal Access Tokens vs OAuth 2.0
- First API call examples
- Subscription requirements

### [api_reference.md](api_reference.md)
Complete API v2 endpoint documentation with request/response examples.
- User and organization endpoints
- Event types and scheduled events
- Invitees and availability
- Webhook subscription management
- Pagination and error handling

### [webhooks.md](webhooks.md)
Real-time event notifications via webhooks.
- Webhook setup and configuration
- Event types (invitee.created, invitee.canceled)
- Payload structure and examples
- Signature verification
- Code examples (Node.js, Python)

### [embedding.md](embedding.md)
Adding Calendly scheduling widgets to your website.
- Inline, popup, and badge widgets
- JavaScript initialization
- Prefilling invitee data
- UTM tracking
- Event listeners
- React and Vue.js integration

### [faq.md](faq.md)
Common questions and troubleshooting.
- Subscription and access requirements
- Authentication questions
- Event management limitations
- Webhook troubleshooting
- API limits and rate limiting

### [migration.md](migration.md)
Guide for migrating from API v1 to v2.
- Key differences between versions
- Step-by-step migration process
- Code migration examples
- New v2 capabilities

## Quick Links

- [Calendly Developer Portal](https://developer.calendly.com/)
- [API Reference](https://developer.calendly.com/api-docs)
- [Help Center](https://help.calendly.com/)
- Developer Support: support+developer@calendly.com

## Common Tasks

| Task | Reference |
|------|-----------|
| Authenticate API requests | [getting_started.md](getting_started.md) |
| List scheduled events | [api_reference.md](api_reference.md) |
| Set up webhooks | [webhooks.md](webhooks.md) |
| Embed scheduling widget | [embedding.md](embedding.md) |
| Migrate from v1 to v2 | [migration.md](migration.md) |
