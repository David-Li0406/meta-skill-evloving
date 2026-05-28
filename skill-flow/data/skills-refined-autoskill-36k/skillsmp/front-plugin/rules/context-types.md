# Front Plugin Context Types

## Context Base

All contexts include:

```ts
interface ApplicationContextBase {
  id: string                    // Unique context ID
  entryPointId: string          // Entry point this context came from
  teammate: ApplicationTeammate // Current Front user
  preferences: object           // User preferences for this app
  authentication: {
    status?: 'authorized'
  }
}
```

## Conversation Contexts

### NoConversationContext

```ts
interface NoConversationContext extends ApplicationContextBase {
  type: 'noConversation'
}
```

### SingleConversationContext

Most common - one conversation selected:

```ts
interface SingleConversationContext extends ApplicationContextBase {
  type: 'singleConversation'
  conversation: ApplicationSingleConversation

  // Methods
  fetchDraft(draftId): Promise<ApplicationDraft | undefined>
  listMessages(paginationToken?): Promise<ApplicationMessageList>
  listComments(paginationToken?): Promise<ApplicationCommentList>
  listRecipients(paginationToken?): Promise<ApplicationRecipientList>
  downloadAttachment(messageOrCommentId, attachmentId): Promise<File | undefined>
}
```

### MultiConversationsContext

Multiple conversations selected:

```ts
interface MultiConversationsContext extends ApplicationContextBase {
  type: 'multiConversations'
  conversations: ReadonlyArray<ApplicationConversation>
}
```

### MessageComposerContext

Composer plugin context:

```ts
interface MessageComposerContext extends ApplicationContextBase {
  type: 'messageComposer'
  draft: ApplicationDraft
  conversation: ApplicationSingleConversation | undefined  // undefined for new compose

  // Methods
  listMessages(paginationToken?): Promise<ApplicationMessageList>
  listComments(paginationToken?): Promise<ApplicationCommentList>
  listRecipients(paginationToken?): Promise<ApplicationRecipientList>
  downloadComposerAttachment(attachmentId): Promise<File | undefined>
  close(): Promise<void>
  closeDraft(): Promise<void>
}
```

## Data Types

### ApplicationTeammate

```ts
interface ApplicationTeammate {
  id: string      // tea_xxx
  name: string
  username: string
  email: string
}
```

### ApplicationConversation

```ts
interface ApplicationConversation {
  id: string                          // cnv_xxx
  type: 'email' | 'whatsapp' | 'frontChat' | 'internal' | ...
  status: 'open' | 'archived' | 'trashed' | 'spam'
  subject: string | undefined
  blurb: string | undefined
  assignee: ApplicationTeammate | undefined
  recipient: ApplicationRecipient | undefined
  inboxes: ReadonlyArray<ApplicationInbox>
  tags: ReadonlyArray<ApplicationTag>
  links: ReadonlyArray<ApplicationLink>
  closedAt: number | undefined
  statusCategory: 'open' | 'waiting' | 'resolved' | undefined
}
```

### ApplicationSingleConversation

Extends ApplicationConversation with:

```ts
interface ApplicationSingleConversation extends ApplicationConversation {
  draftId: string | undefined  // ID of draft if one exists
}
```

### ApplicationMessage

```ts
interface ApplicationMessage {
  id: string                    // msg_xxx
  subject: string | undefined
  date: Date
  status: 'inbound' | 'outbound'
  from: ApplicationRecipient
  to: ReadonlyArray<ApplicationRecipient>
  cc: ReadonlyArray<ApplicationRecipient> | undefined
  bcc: ReadonlyArray<ApplicationRecipient> | undefined
  replyTo: ApplicationRecipient | undefined
  content: {
    body: string
    type: 'html' | 'text'
    attachments: ReadonlyArray<ApplicationAttachment>
  } | undefined
}
```

### ApplicationDraft

```ts
interface ApplicationDraft {
  id: string                    // dra_xxx
  channel: ApplicationChannel
  to: ReadonlyArray<ApplicationRecipient>
  cc: ReadonlyArray<ApplicationRecipient> | undefined
  bcc: ReadonlyArray<ApplicationRecipient> | undefined
  subject: string | undefined
  content: {
    body: string
    type: 'html' | 'text'
    attachments: ReadonlyArray<ApplicationDraftAttachment>
  }
  isEditable: boolean
}
```

### ApplicationRecipient

```ts
interface ApplicationRecipient {
  handle: string
  name: string | undefined
  contact: ApplicationContact | undefined
  type: string
}
```

### ApplicationAttachment

```ts
interface ApplicationAttachment {
  id: string
  name: string
  contentType: string
  size: number
  inlineCid: string | undefined  // For inline attachments
}
```
