---
name: Messenger & Chat
description: Real-time messaging, DMs, and group chats
---

# Messenger & Chat Skill

## Overview
Build real-time messaging with direct messages, group chats, and table chat.

## Message Types
| Type | Description |
|------|-------------|
| DM | Direct 1-on-1 message |
| GROUP | Group chat (2+ users) |
| TABLE | Poker table chat |
| CLUB | Club-wide chat |
| SYSTEM | System notifications |

## Database Schema
```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT DEFAULT 'DM', -- 'DM', 'GROUP', 'TABLE', 'CLUB'
  name TEXT, -- For groups
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_message_at TIMESTAMPTZ
);

CREATE TABLE conversation_members (
  conversation_id UUID REFERENCES conversations(id),
  user_id UUID REFERENCES auth.users(id),
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  last_read_at TIMESTAMPTZ,
  PRIMARY KEY (conversation_id, user_id)
);

CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id),
  sender_id UUID REFERENCES auth.users(id),
  content TEXT NOT NULL,
  message_type TEXT DEFAULT 'text', -- 'text', 'image', 'gif', 'system'
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  edited_at TIMESTAMPTZ
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at DESC);
```

## Send Message
```javascript
async function sendMessage(conversationId, senderId, content, type = 'text') {
  const { data: message, error } = await supabase
    .from('messages')
    .insert({
      conversation_id: conversationId,
      sender_id: senderId,
      content,
      message_type: type
    })
    .select(`
      *,
      sender:profiles!sender_id(username, avatar_url)
    `)
    .single();
  
  // Update conversation last_message_at
  await supabase.from('conversations')
    .update({ last_message_at: new Date() })
    .eq('id', conversationId);
  
  // Broadcast to channel
  await supabase.channel(`conversation:${conversationId}`)
    .send({
      type: 'broadcast',
      event: 'new_message',
      payload: message
    });
  
  return message;
}
```

## Real-time Listener
```javascript
function useMessages(conversationId) {
  const [messages, setMessages] = useState([]);
  
  useEffect(() => {
    // Fetch initial messages
    fetchMessages(conversationId).then(setMessages);
    
    // Subscribe to new messages
    const channel = supabase.channel(`conversation:${conversationId}`)
      .on('broadcast', { event: 'new_message' }, ({ payload }) => {
        setMessages(prev => [...prev, payload]);
      })
      .subscribe();
    
    return () => channel.unsubscribe();
  }, [conversationId]);
  
  return messages;
}
```

## Start Conversation
```javascript
async function startConversation(userId, recipientId) {
  // Check if DM exists
  const existing = await findExistingDM(userId, recipientId);
  if (existing) return existing;
  
  // Create new conversation
  const { data: conversation } = await supabase
    .from('conversations')
    .insert({ type: 'DM' })
    .select()
    .single();
  
  // Add members
  await supabase.from('conversation_members').insert([
    { conversation_id: conversation.id, user_id: userId },
    { conversation_id: conversation.id, user_id: recipientId }
  ]);
  
  return conversation;
}
```

## Unread Count
```javascript
async function getUnreadCount(userId) {
  const { data } = await supabase
    .from('conversation_members')
    .select(`
      conversation_id,
      last_read_at,
      conversations!inner(last_message_at)
    `)
    .eq('user_id', userId);
  
  return data.filter(c => 
    c.conversations.last_message_at > (c.last_read_at || new Date(0))
  ).length;
}
```

## Components
- `ConversationList.jsx` - List of chats
- `MessageThread.jsx` - Message display
- `MessageInput.jsx` - Compose message
- `ChatBubble.jsx` - Single message
- `OnlineIndicator.jsx` - User online status
