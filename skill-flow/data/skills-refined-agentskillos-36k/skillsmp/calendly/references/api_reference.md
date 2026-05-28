# Calendly API v2 Reference

Base URL: `https://api.calendly.com`

All requests require authentication via Bearer token.

## Users

### Get Current User
```
GET /users/me
```

Returns the current authenticated user's information including scheduling URL, organization, and profile data.

**Response Fields:**
- `uri` - User's unique identifier URI
- `name` - Display name
- `email` - Email address
- `slug` - URL slug for scheduling page
- `scheduling_url` - Direct link to scheduling page
- `timezone` - User's timezone
- `current_organization` - Organization URI

### Get User by URI
```
GET /users/{user_uuid}
```

Retrieve a specific user's information.

## Organizations

### List Organization Memberships
```
GET /organization_memberships
```

**Query Parameters:**
- `organization` (required) - Organization URI
- `user` (optional) - Filter by user URI
- `count` (optional) - Number of results (default 20, max 100)
- `page_token` (optional) - Pagination token

Returns all members of an organization with their roles and user information.

### Get Organization Invitation
```
GET /organizations/{org_uuid}/invitations/{invitation_uuid}
```

### List Organization Invitations
```
GET /organizations/{org_uuid}/invitations
```

## Event Types

### List Event Types
```
GET /event_types
```

**Query Parameters:**
- `user` (optional) - User URI to filter by
- `organization` (optional) - Organization URI
- `active` (optional) - Filter by active status (true/false)
- `count` (optional) - Results per page
- `page_token` (optional) - Pagination token
- `sort` (optional) - Sort order

**Response includes:**
- Event type name and description
- Duration
- Scheduling URL
- Color
- Active status
- Custom questions

### Get Event Type
```
GET /event_types/{event_type_uuid}
```

## Scheduled Events

### List Scheduled Events
```
GET /scheduled_events
```

**Query Parameters:**
- `user` (optional) - User URI
- `organization` (optional) - Organization URI
- `invitee_email` (optional) - Filter by invitee email
- `status` (optional) - "active" or "canceled"
- `min_start_time` (optional) - ISO 8601 datetime
- `max_start_time` (optional) - ISO 8601 datetime
- `count` (optional) - Results per page
- `page_token` (optional) - Pagination token
- `sort` (optional) - Sort field:order

**Response includes:**
- Event URI and name
- Start and end times
- Status (active/canceled)
- Location information
- Event type reference
- Invitees collection URI

### Get Scheduled Event
```
GET /scheduled_events/{event_uuid}
```

### Cancel Scheduled Event
```
POST /scheduled_events/{event_uuid}/cancellation
```

**Request Body:**
```json
{
  "reason": "Optional cancellation reason"
}
```

**Notes:**
- Cancels entire event including all invitees
- Cannot cancel individual invitees in group events
- Sends cancellation notification to invitees

## Invitees

### List Event Invitees
```
GET /scheduled_events/{event_uuid}/invitees
```

**Query Parameters:**
- `status` (optional) - Filter by status
- `email` (optional) - Filter by email
- `count` (optional) - Results per page
- `page_token` (optional) - Pagination token
- `sort` (optional) - Sort order

### Get Event Invitee
```
GET /scheduled_events/{event_uuid}/invitees/{invitee_uuid}
```

**Response includes:**
- Invitee name and email
- Timezone
- UTM parameters (if provided)
- Custom question responses
- Cancel and reschedule URLs
- Created/updated timestamps

## Webhooks

### Create Webhook Subscription
```
POST /webhook_subscriptions
```

**Request Body:**
```json
{
  "url": "https://your-domain.com/webhooks/calendly",
  "events": ["invitee.created", "invitee.canceled"],
  "organization": "https://api.calendly.com/organizations/ORG_UUID",
  "scope": "organization",
  "signing_key": "optional_signing_key"
}
```

**Scope options:**
- `user` - Events for specific user
- `organization` - Events for entire organization

### List Webhook Subscriptions
```
GET /webhook_subscriptions
```

**Query Parameters:**
- `organization` (required) - Organization URI
- `scope` (required) - "user" or "organization"
- `user` (optional) - User URI (if scope is user)

### Get Webhook Subscription
```
GET /webhook_subscriptions/{webhook_uuid}
```

### Delete Webhook Subscription
```
DELETE /webhook_subscriptions/{webhook_uuid}
```

## Scheduling Links

### Create Single-Use Scheduling Link
```
POST /scheduling_links
```

**Request Body:**
```json
{
  "max_event_count": 1,
  "owner": "https://api.calendly.com/event_types/EVENT_TYPE_UUID",
  "owner_type": "EventType"
}
```

**Notes:**
- Single-use links expire after 90 days
- Link becomes invalid after being used

## Availability

### Get User Availability Schedules
```
GET /user_availability_schedules
```

**Query Parameters:**
- `user` (required) - User URI

### Get User Busy Times
```
GET /user_busy_times
```

**Query Parameters:**
- `user` (required) - User URI
- `start_time` (required) - ISO 8601 datetime
- `end_time` (required) - ISO 8601 datetime

## Pagination

API responses use cursor-based pagination:

```json
{
  "collection": [...],
  "pagination": {
    "count": 20,
    "next_page": "https://api.calendly.com/...?page_token=abc123",
    "previous_page": null,
    "next_page_token": "abc123",
    "previous_page_token": null
  }
}
```

Use `page_token` query parameter for subsequent requests.

## Error Responses

```json
{
  "title": "Resource Not Found",
  "message": "The resource you requested does not exist.",
  "details": []
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Unprocessable Entity
- `429` - Rate Limited
- `500` - Internal Server Error
