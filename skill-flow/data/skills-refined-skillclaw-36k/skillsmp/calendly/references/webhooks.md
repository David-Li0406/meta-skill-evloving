# Calendly Webhooks

Webhooks provide real-time notifications when scheduling events occur in Calendly.

## Requirements

- **Subscription Plan**: Standard, Teams, or Enterprise (not available on Free plan)
- **HTTPS endpoint**: Your webhook URL must use HTTPS
- **Public accessibility**: Endpoint must be reachable from Calendly's servers

## Webhook Events

| Event | Description | When Triggered |
|-------|-------------|----------------|
| `invitee.created` | New meeting scheduled | Invitee completes booking |
| `invitee.canceled` | Meeting canceled | Invitee or host cancels |

**Note on Rescheduling**: When an invitee reschedules, Calendly fires:
1. `invitee.canceled` for the original event
2. `invitee.created` for the new event

## Creating a Webhook Subscription

```bash
POST https://api.calendly.com/webhook_subscriptions
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "url": "https://your-domain.com/webhooks/calendly",
  "events": ["invitee.created", "invitee.canceled"],
  "organization": "https://api.calendly.com/organizations/YOUR_ORG_UUID",
  "scope": "organization",
  "signing_key": "your_optional_signing_key"
}
```

### Scope Options

- **`organization`**: Receive events for all users in the organization
- **`user`**: Receive events only for a specific user

For user scope, include the `user` parameter:
```json
{
  "scope": "user",
  "user": "https://api.calendly.com/users/USER_UUID"
}
```

## Webhook Payload Structure

### invitee.created

```json
{
  "event": "invitee.created",
  "created_at": "2023-01-15T10:30:00.000000Z",
  "created_by": "https://api.calendly.com/users/USER_UUID",
  "payload": {
    "cancel_url": "https://calendly.com/cancellations/CANCEL_UUID",
    "created_at": "2023-01-15T10:30:00.000000Z",
    "email": "invitee@example.com",
    "event": "https://api.calendly.com/scheduled_events/EVENT_UUID",
    "first_name": "John",
    "last_name": "Doe",
    "name": "John Doe",
    "new_invitee": null,
    "old_invitee": null,
    "questions_and_answers": [
      {
        "answer": "Product Demo",
        "position": 0,
        "question": "What would you like to discuss?"
      }
    ],
    "reschedule_url": "https://calendly.com/reschedulings/RESCHEDULE_UUID",
    "rescheduled": false,
    "routing_form_submission": null,
    "status": "active",
    "text_reminder_number": null,
    "timezone": "America/New_York",
    "tracking": {
      "utm_campaign": "demo",
      "utm_source": "website",
      "utm_medium": "button",
      "utm_content": null,
      "utm_term": null,
      "salesforce_uuid": null
    },
    "updated_at": "2023-01-15T10:30:00.000000Z",
    "uri": "https://api.calendly.com/scheduled_events/EVENT_UUID/invitees/INVITEE_UUID"
  }
}
```

### invitee.canceled

```json
{
  "event": "invitee.canceled",
  "created_at": "2023-01-16T09:00:00.000000Z",
  "created_by": "https://api.calendly.com/users/USER_UUID",
  "payload": {
    "cancel_url": "https://calendly.com/cancellations/CANCEL_UUID",
    "cancellation": {
      "canceled_by": "John Doe",
      "reason": "Schedule conflict"
    },
    "created_at": "2023-01-15T10:30:00.000000Z",
    "email": "invitee@example.com",
    "event": "https://api.calendly.com/scheduled_events/EVENT_UUID",
    "name": "John Doe",
    "status": "canceled",
    "uri": "https://api.calendly.com/scheduled_events/EVENT_UUID/invitees/INVITEE_UUID"
  }
}
```

## Verifying Webhook Signatures

If you provided a `signing_key` when creating the subscription, verify payloads:

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, signing_key):
    expected = hmac.new(
        signing_key.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

The signature is sent in the `Calendly-Webhook-Signature` header.

## Handling Webhooks

### Node.js/Express Example

```javascript
const express = require('express');
const app = express();

app.post('/webhooks/calendly', express.json(), (req, res) => {
  const event = req.body;

  switch (event.event) {
    case 'invitee.created':
      console.log('New booking:', event.payload.name);
      // Add to CRM, send confirmation, etc.
      break;

    case 'invitee.canceled':
      console.log('Canceled:', event.payload.name);
      // Update records, notify team, etc.
      break;
  }

  res.status(200).send('OK');
});
```

### Python/Flask Example

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks/calendly', methods=['POST'])
def handle_webhook():
    event = request.json
    event_type = event.get('event')
    payload = event.get('payload')

    if event_type == 'invitee.created':
        print(f"New booking: {payload['name']} - {payload['email']}")
        # Process new booking

    elif event_type == 'invitee.canceled':
        print(f"Canceled: {payload['name']}")
        # Handle cancellation

    return jsonify({'status': 'received'}), 200
```

## UTM Tracking

Track the source of bookings using UTM parameters in scheduling links:

```
https://calendly.com/your-link?utm_source=email&utm_medium=newsletter&utm_campaign=january
```

These values appear in the webhook payload under `payload.tracking`:

```json
{
  "tracking": {
    "utm_source": "email",
    "utm_medium": "newsletter",
    "utm_campaign": "january",
    "utm_content": null,
    "utm_term": null
  }
}
```

## Getting Additional Event Data

The webhook payload includes the event URI. Use it to fetch complete event details:

```bash
GET https://api.calendly.com/scheduled_events/EVENT_UUID
Authorization: Bearer YOUR_TOKEN
```

This returns:
- Event start/end times
- Location details
- Event type information
- Full invitee list

## Managing Webhook Subscriptions

### List Subscriptions

```bash
GET https://api.calendly.com/webhook_subscriptions?organization=ORG_URI&scope=organization
Authorization: Bearer YOUR_TOKEN
```

### Delete Subscription

```bash
DELETE https://api.calendly.com/webhook_subscriptions/WEBHOOK_UUID
Authorization: Bearer YOUR_TOKEN
```

## Best Practices

1. **Respond quickly**: Return 200 status within 10 seconds
2. **Process asynchronously**: Queue webhook data for processing
3. **Handle duplicates**: Calendly may retry failed deliveries
4. **Verify signatures**: Use signing keys for security
5. **Log everything**: Keep records for debugging
6. **Use HTTPS**: Required for webhook endpoints
