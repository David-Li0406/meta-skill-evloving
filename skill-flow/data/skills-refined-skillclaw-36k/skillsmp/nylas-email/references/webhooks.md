# Webhooks

## Email-Related Triggers

- `message.created`
- `message.updated`
- `message.send_success`
- `message.send_failed`
- `message.opened` (tracking)
- `message.link_clicked` (tracking)
- `message.bounce_detected`
- `thread.replied` (tracking)
- `folder.created`
- `folder.updated`
- `folder.deleted`

## Bounce Detection

- Supports hard bounces: `mailbox_unavailable`, `domain_not_found`
- Only for messages sent through Nylas
- Bounced message must be properly threaded
