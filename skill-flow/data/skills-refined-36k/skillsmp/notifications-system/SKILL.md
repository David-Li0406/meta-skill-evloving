---
name: Notifications System
description: Push notifications, in-app notifications, and real-time alerts
---

# Notifications System Skill

## Overview
Implement comprehensive notification system with in-app, push, and email notifications.

## Notification Types
| Type | Channel | Example |
|------|---------|---------|
| LIKE | In-app | "John liked your post" |
| COMMENT | In-app + Push | "Sarah commented on your post" |
| FOLLOW | In-app | "Mike started following you" |
| GAME_INVITE | In-app + Push | "Join the $100 tournament!" |
| LEVEL_UP | In-app + Push | "You reached Level 5!" |
| DAILY_BONUS | Push | "Claim your daily diamonds!" |
| TOURNAMENT_START | Push | "Tournament starting in 5 minutes" |

## Database Schema
```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT,
  data JSONB DEFAULT '{}',
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_unread 
ON notifications(user_id, is_read) WHERE is_read = FALSE;
```

## Create Notification
```javascript
async function createNotification(userId, type, title, body, data = {}) {
  await supabase.from('notifications').insert({
    user_id: userId,
    type,
    title,
    body,
    data
  });
  
  // Broadcast via realtime
  await supabase.channel(`user:${userId}`)
    .send({
      type: 'broadcast',
      event: 'notification',
      payload: { type, title, body, data }
    });
}
```

## Fetch Notifications
```javascript
async function getNotifications(userId, unreadOnly = false) {
  let query = supabase
    .from('notifications')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
    .limit(50);
  
  if (unreadOnly) {
    query = query.eq('is_read', false);
  }
  
  return query;
}

async function markAsRead(notificationIds) {
  await supabase
    .from('notifications')
    .update({ is_read: true })
    .in('id', notificationIds);
}
```

## Real-time Listener
```javascript
function useNotifications(userId) {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  
  useEffect(() => {
    // Initial fetch
    fetchNotifications();
    
    // Subscribe to new notifications
    const channel = supabase.channel(`user:${userId}`)
      .on('broadcast', { event: 'notification' }, ({ payload }) => {
        setNotifications(prev => [payload, ...prev]);
        setUnreadCount(prev => prev + 1);
        showToast(payload);
      })
      .subscribe();
    
    return () => channel.unsubscribe();
  }, [userId]);
  
  return { notifications, unreadCount, markAsRead };
}
```

## Push Notifications (Web Push)
```javascript
// Register service worker
async function registerPushNotifications() {
  const registration = await navigator.serviceWorker.register('/sw.js');
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: VAPID_PUBLIC_KEY
  });
  
  // Save subscription to database
  await supabase.from('push_subscriptions').insert({
    user_id: userId,
    endpoint: subscription.endpoint,
    keys: subscription.toJSON().keys
  });
}
```

## Components
- `NotificationBell.jsx` - Header bell icon with count
- `NotificationDropdown.jsx` - Dropdown list
- `NotificationItem.jsx` - Single notification
- `NotificationToast.jsx` - Pop-up toast
