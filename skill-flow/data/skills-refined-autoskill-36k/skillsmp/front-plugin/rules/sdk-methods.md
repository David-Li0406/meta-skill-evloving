# Front Plugin SDK Methods

## Conversation Actions

### Assign/Unassign

```ts
// Assign to teammate
await context.assign('tea_123')

// Unassign
await context.assign(null)
```

### Move to Inbox

```ts
await context.move('inb_456')
```

### Set Status

```ts
await context.setStatus('archived')  // Archive
await context.setStatus('open')      // Reopen
await context.setStatus('trashed')   // Trash
await context.setStatus('spam')      // Mark as spam
```

### Tags

```ts
// Add tags
await context.tag(['tag_123', 'tag_456'])

// Remove tags
await context.untag(['tag_123'])
```

### Links

```ts
// Add link to conversation
await context.addLink('https://example.com/order/123', 'Order #123')

// Remove link
await context.removeLink('top_789')
```

## Listing Data

### List Messages

```ts
const result = await context.listMessages()
// result.results: ApplicationMessage[]
// result.nextPageToken: string | undefined

// Pagination
const nextPage = await context.listMessages(result.nextPageToken)
```

### List Comments

```ts
const comments = await context.listComments()
```

### List Recipients

```ts
const recipients = await context.listRecipients()
```

### List Tags (All Available)

```ts
const tags = await context.listTags()
```

### List Teammates

```ts
const teammates = await context.listTeammates()
```

### List Inboxes

```ts
const inboxes = await context.listInboxes()
```

### List Channels

```ts
const channels = await context.listChannels()
```

## Draft Operations

### Create Draft

```ts
// Simple reply
await context.createDraft({
  content: {
    body: 'Hello!',
    type: 'text'
  },
  replyOptions: {
    type: 'reply',
    originalMessageId: 'msg_xxx'
  }
})

// Reply all with HTML
await context.createDraft({
  content: {
    body: '<p>Hello <strong>World</strong></p>',
    type: 'html'
  },
  replyOptions: {
    type: 'replyAll',
    originalMessageId: 'msg_xxx'
  }
})

// Forward
await context.createDraft({
  to: ['new@recipient.com'],
  content: {
    body: 'Forwarding this to you',
    type: 'text'
  },
  replyOptions: {
    type: 'forward',
    originalMessageId: 'msg_xxx'
  }
})

// New message (no replyOptions)
await context.createDraft({
  channelId: 'cha_xxx',
  to: ['recipient@example.com'],
  subject: 'New Message',
  content: {
    body: 'Content here',
    type: 'text'
  }
})

// With attachments
await context.createDraft({
  content: { body: 'See attached', type: 'text' },
  replyOptions: { type: 'reply', originalMessageId: 'msg_xxx' },
  attachments: [file1, file2]  // File objects
})
```

### Update Draft

```ts
// Replace entire content
await context.updateDraft('dra_xxx', {
  updateMode: 'replace',
  subject: 'New Subject',
  content: {
    body: 'Completely replaced content',
    type: 'text'
  }
})

// Insert at cursor position
await context.updateDraft('dra_xxx', {
  updateMode: 'insert',
  content: {
    body: '<p>Inserted text</p>',
    type: 'html'
  }
})

// Update recipients
await context.updateDraft('dra_xxx', {
  updateMode: 'replace',
  to: ['new@recipient.com'],
  cc: ['cc@recipient.com']
})
```

### Fetch Draft

```ts
const draft = await context.fetchDraft('dra_xxx')
```

## Navigation

### Open URL

```ts
// Open in new browser tab
await context.openUrl('https://example.com')

// Open internal Front URL
await context.openUrl('/open/msg_xxx')
```

### Open URL in Popup

```ts
// For modals/dialogs
await context.openUrlInPopup('https://example.com/modal', {
  width: 400,
  height: 300
})
```

### Open Conversation in Popup

```ts
await context.openConversationInPopup('cnv_xxx')
```

### Search

```ts
await context.search('query string')
```

## Attachments

### Download Message Attachment

```ts
const file = await context.downloadAttachment('msg_xxx', 'att_yyy')
// Returns File object or undefined
```

### Download Composer Attachment (Composer Plugin Only)

```ts
const file = await context.downloadComposerAttachment('att_yyy')
```

## Composer Plugin Specific

### Close Plugin

```ts
await context.close()
```

### Close Draft and Plugin

```ts
await context.closeDraft()
```

## HTTP Requests

### Send to App's Private API

```ts
const response = await context.sendHttp({
  verb: 'POST',
  path: '/api/my-endpoint',
  body: { data: 'value' }
})
// response.status, response.body, response.headers
```

### Relay HTTP (Proxied Request)

```ts
const response = await context.relayHttp({
  verb: 'GET',
  url: 'https://api.example.com/data',
  headers: { 'X-Custom': 'value' }
})
```

## Authentication

```ts
// Start OAuth flow
await context.authenticate()

// Clear stored credentials
await context.deauthenticate()
```
