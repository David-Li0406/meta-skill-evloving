# Front API Schemas

Reference for building typed SDK. These map to the OpenAPI spec.

## Core Types

### Conversation

```ts
const ConversationSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      events: z.string(),
      followers: z.string(),
      messages: z.string(),
      comments: z.string(),
      inboxes: z.string(),
    }),
  }),
  id: z.string(),  // cnv_xxx
  subject: z.string(),
  status: z.enum(['archived', 'unassigned', 'assigned', 'deleted', 'snoozed', 'invisible']),
  assignee: TeammateSchema.nullable(),
  recipient: RecipientSchema,
  tags: z.array(TagSchema),
  links: z.array(LinkSchema),
  custom_fields: z.record(z.string(), z.unknown()).optional(),
  created_at: z.number(),
  waiting_since: z.number().optional(),
  is_private: z.boolean(),
  scheduled_reminders: z.array(ReminderSchema).optional(),
  metadata: z.object({
    external_conversation_ids: z.array(z.string()).optional(),
  }).optional(),
})
```

### Message

```ts
const MessageSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      conversation: z.string(),
      message_replied_to: z.string().optional(),
    }),
  }),
  id: z.string(),  // msg_xxx
  type: z.enum(['email', 'tweet', 'sms', 'smooch', 'facebook', 'intercom', 'call', 'custom']),
  is_inbound: z.boolean(),
  is_draft: z.boolean(),
  error_type: z.string().nullable(),
  version: z.string().nullable(),
  created_at: z.number(),
  subject: z.string().nullable(),
  blurb: z.string(),
  body: z.string(),
  text: z.string().nullable(),
  author: AuthorSchema.nullable(),
  recipients: z.array(RecipientSchema),
  attachments: z.array(AttachmentSchema),
  signature: SignatureSchema.nullable().optional(),
  metadata: z.object({
    headers: z.record(z.string(), z.string()).optional(),
    thread_ref: z.string().optional(),
    is_forward: z.boolean().optional(),
  }).optional(),
})
```

### Draft

```ts
const DraftSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      conversation: z.string(),
      message_replied_to: z.string().optional(),
    }),
  }),
  id: z.string(),  // msg_xxx (drafts are messages)
  version: z.string(),
  author: AuthorSchema,
  recipients: z.array(RecipientSchema),
  body: z.string(),
  subject: z.string().nullable(),
  attachments: z.array(AttachmentSchema),
  created_at: z.number(),
  channel_id: z.string().optional(),
})
```

### Recipient

```ts
const RecipientSchema = z.object({
  _links: z.object({
    related: z.object({
      contact: z.string().optional(),
    }).optional(),
  }).optional(),
  handle: z.string(),
  role: z.enum(['from', 'to', 'cc', 'bcc']),
  name: z.string().nullable().optional(),
})
```

### Author (Teammate)

```ts
const AuthorSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      inboxes: z.string(),
      conversations: z.string(),
    }),
  }).optional(),
  id: z.string(),  // tea_xxx
  email: z.string(),
  username: z.string().optional(),
  first_name: z.string().optional(),
  last_name: z.string().optional(),
  is_admin: z.boolean().optional(),
  is_available: z.boolean().optional(),
  is_blocked: z.boolean().optional(),
})
```

### Teammate

```ts
const TeammateSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      inboxes: z.string(),
      conversations: z.string(),
    }),
  }),
  id: z.string(),  // tea_xxx
  email: z.string(),
  username: z.string(),
  first_name: z.string(),
  last_name: z.string(),
  is_admin: z.boolean(),
  is_available: z.boolean(),
  is_blocked: z.boolean(),
  custom_fields: z.record(z.string(), z.unknown()).optional(),
})
```

### Tag

```ts
const TagSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      conversations: z.string(),
      owner: z.string(),
      children: z.string().optional(),
    }),
  }),
  id: z.string(),  // tag_xxx
  name: z.string(),
  description: z.string().nullable().optional(),
  highlight: z.enum(['black', 'grey', 'pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple']).nullable().optional(),
  is_private: z.boolean(),
  is_visible_in_conversation_lists: z.boolean().optional(),
  created_at: z.number().optional(),
  updated_at: z.number().optional(),
})
```

### Inbox

```ts
const InboxSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      teammates: z.string(),
      conversations: z.string(),
      channels: z.string(),
      owner: z.string(),
    }),
  }),
  id: z.string(),  // inb_xxx
  name: z.string(),
  is_private: z.boolean(),
  is_public: z.boolean().optional(),
  address: z.string().optional(),  // For email inboxes
  send_as: z.string().optional(),
})
```

### Channel

```ts
const ChannelSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      inbox: z.string(),
      owner: z.string().optional(),
    }),
  }),
  id: z.string(),  // cha_xxx
  type: z.enum(['smtp', 'imap', 'twilio', 'twitter', 'facebook', 'intercom', 'truly', 'custom']),
  address: z.string(),
  send_as: z.string().optional(),
  name: z.string().optional(),
  is_private: z.boolean().optional(),
  is_valid: z.boolean().optional(),
})
```

### Attachment

```ts
const AttachmentSchema = z.object({
  id: z.string(),  // fil_xxx
  filename: z.string(),
  url: z.string(),
  content_type: z.string(),
  size: z.number(),
  metadata: z.object({
    is_inline: z.boolean(),
    cid: z.string().optional(),
  }),
})
```

### Message Template

```ts
const MessageTemplateSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      owner: z.string(),
      folder: z.string().optional(),
    }),
  }),
  id: z.string(),  // rsp_xxx
  name: z.string(),
  subject: z.string(),
  body: z.string(),
  is_available_for_all_inboxes: z.boolean(),
  attachments: z.array(AttachmentSchema).optional(),
  folder: z.string().nullable().optional(),  // fld_xxx
})
```

### Message Template Folder

```ts
const MessageTemplateFolderSchema = z.object({
  _links: z.object({
    self: z.string(),
  }),
  id: z.string(),  // fld_xxx
  name: z.string(),
})
```

### Link

```ts
const LinkSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      conversations: z.string(),
    }),
  }),
  id: z.string(),  // top_xxx (topic)
  name: z.string().nullable(),
  type: z.enum(['web']),
  external_url: z.string(),
})
```

### Contact

```ts
const ContactSchema = z.object({
  _links: z.object({
    self: z.string(),
    related: z.object({
      notes: z.string(),
      conversations: z.string(),
      owner: z.string().optional(),
    }),
  }),
  id: z.string(),  // crd_xxx or ctc_xxx
  name: z.string().nullable(),
  description: z.string().nullable(),
  avatar_url: z.string().nullable(),
  is_spammer: z.boolean(),
  links: z.array(z.string()),
  groups: z.array(z.object({
    _links: z.object({ self: z.string() }),
    id: z.string(),
    name: z.string(),
  })),
  handles: z.array(z.object({
    handle: z.string(),
    source: z.enum(['email', 'phone', 'twitter', 'facebook', 'intercom', 'front_chat', 'custom']),
  })),
  custom_fields: z.record(z.string(), z.unknown()),
  is_private: z.boolean().optional(),
})
```

## Pagination

All list endpoints return:

```ts
const PaginatedResponseSchema = <T>(itemSchema: z.ZodType<T>) =>
  z.object({
    _pagination: z.object({
      next: z.string().optional(),  // URL for next page
    }).optional(),
    _links: z.object({
      self: z.string(),
    }),
    _results: z.array(itemSchema),
  })
```

Usage:
```ts
const ConversationListSchema = PaginatedResponseSchema(ConversationSchema)
```

## Error Response

```ts
const ErrorResponseSchema = z.object({
  _error: z.object({
    status: z.number(),
    title: z.string(),
    message: z.string(),
    details: z.array(z.string()).optional(),
  }),
})
```
