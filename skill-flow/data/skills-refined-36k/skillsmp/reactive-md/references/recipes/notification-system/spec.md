---
title: Notification System PRD
author: @product-manager
status: draft
date: 2025-12-14
---

# Notification System

## Problem Statement

Users miss important updates because we lack a unified notification system. Currently, critical alerts are buried in email, leading to delayed responses and frustrated customers.

**Impact**:
- 40% of users report missing time-sensitive updates
- Average response time to critical alerts: 4+ hours
- Support tickets about "I didn't see that" up 25% QoQ

## User Stories

**As a user**, I want to see unread notifications at a glance, so I can prioritize what needs my attention.

**As a user**, I want to mark notifications as read, so my notification count stays accurate.

**As a user**, I want to click a notification to go directly to the relevant content.

---

## Load Custom Styles

```css live
@import "./styles.css";
```

---

## Proposed Solution

### Notification Bell with Badge

The primary entry point — a bell icon in the header with an animated unread count badge.

```jsx live
import NotificationBell from './NotificationBell.jsx';

function BellDemo() {
  const [count, setCount] = React.useState(3);
  
  return (
    <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
      <span className="text-sm text-gray-500">Click to simulate:</span>
      <button 
        onClick={() => setCount(c => c + 1)}
        className="px-3 py-1.5 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Add notification
      </button>
      <button 
        onClick={() => setCount(0)}
        className="px-3 py-1.5 text-sm bg-gray-200 rounded hover:bg-gray-300"
      >
        Clear all
      </button>
      
      <div className="ml-auto">
        <NotificationBell count={count} onClick={() => alert('Open dropdown!')} />
      </div>
    </div>
  );
}
```

### Notification List

When clicked, the bell reveals a dropdown with recent notifications:

```jsx live
import NotificationItem from './NotificationItem.jsx';

function NotificationList() {
  const [notifications, setNotifications] = React.useState([
    { id: 1, title: 'New comment on your post', description: 'Sarah replied to your comment', time: '2m ago', read: false },
    { id: 2, title: 'Your report is ready', description: 'Q4 analytics report has been generated', time: '1h ago', read: false },
    { id: 3, title: 'Team invitation accepted', description: 'John joined your workspace', time: '3h ago', read: true },
    { id: 4, title: 'Welcome to the platform!', description: 'Get started with our quick tutorial', time: '2d ago', read: true },
  ]);
  
  const markAsRead = (id) => {
    setNotifications(notifications.map(n => 
      n.id === id ? { ...n, read: true } : n
    ));
  };
  
  const markAllRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })));
  };
  
  const unreadCount = notifications.filter(n => !n.read).length;
  
  return (
    <div className="w-96 bg-white rounded-lg shadow-xl border notification-dropdown">
      <div className="p-4 border-b flex justify-between items-center">
        <span className="font-semibold">Notifications</span>
        {unreadCount > 0 && (
          <button 
            onClick={markAllRead}
            className="text-sm text-blue-500 hover:underline"
          >
            Mark all as read
          </button>
        )}
      </div>
      <div className="max-h-80 overflow-y-auto">
        {notifications.map((n, index) => (
          <NotificationItem 
            key={n.id}
            {...n}
            onMarkRead={() => markAsRead(n.id)}
          />
        ))}
      </div>
      <div className="p-3 border-t text-center">
        <button className="text-sm text-blue-500 hover:underline">
          View all notifications
        </button>
      </div>
    </div>
  );
}
```

---

## Toast Notifications

For immediate feedback, show toast notifications that auto-dismiss:

```jsx live
import { motion, AnimatePresence } from 'motion/react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

function ToastDemo() {
  const [toasts, setToasts] = React.useState([]);
  
  const addToast = (type) => {
    const id = Date.now();
    const messages = {
      success: 'Changes saved successfully!',
      error: 'Something went wrong. Please try again.',
      info: 'New updates are available.',
    };
    const icons = { success: CheckCircle, error: AlertCircle, info: Info };
    const colors = {
      success: 'bg-green-50 border-green-200 text-green-800',
      error: 'bg-red-50 border-red-200 text-red-800',
      info: 'bg-blue-50 border-blue-200 text-blue-800',
    };
    
    setToasts(prev => [...prev, { id, type, message: messages[type], Icon: icons[type], color: colors[type] }]);
    
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3000);
  };
  
  const removeToast = (id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };
  
  return (
    <div className="p-4">
      <div className="flex gap-2 mb-4">
        <button 
          onClick={() => addToast('success')}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Success Toast
        </button>
        <button 
          onClick={() => addToast('error')}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Error Toast
        </button>
        <button 
          onClick={() => addToast('info')}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Info Toast
        </button>
      </div>
      
      <div className="fixed top-4 right-4 space-y-2 z-50">
        <AnimatePresence>
          {toasts.map(({ id, Icon, message, color }) => (
            <motion.div
              key={id}
              initial={{ opacity: 0, x: 100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 100 }}
              className={`flex items-center gap-3 p-4 rounded-lg border shadow-lg ${color}`}
            >
              <Icon className="w-5 h-5" />
              <span className="flex-1">{message}</span>
              <button onClick={() => removeToast(id)} className="hover:opacity-70">
                <X className="w-4 h-4" />
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
```

---

## Edge Cases

### Empty State

When there are no notifications:

```jsx live
import { Bell } from 'lucide-react';

function EmptyNotifications() {
  return (
    <div className="w-80 bg-white rounded-lg shadow-xl border p-8 text-center">
      <Bell className="w-12 h-12 text-gray-300 mx-auto mb-4" />
      <h3 className="font-medium text-gray-900">All caught up!</h3>
      <p className="text-sm text-gray-500 mt-1">
        You have no new notifications.
      </p>
    </div>
  );
}
```

### Loading State

While fetching notifications:

```jsx live
function LoadingNotifications() {
  return (
    <div className="w-80 bg-white rounded-lg shadow-xl border p-4 space-y-3">
      {[1, 2, 3].map(i => (
        <div key={i} className="animate-pulse flex gap-3">
          <div className="w-10 h-10 bg-gray-200 rounded-full" />
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
          </div>
        </div>
      ))}
    </div>
  );
}
```

---

## Open Questions

1. **Notification persistence** — How long should we keep notifications? 30 days?
2. **Real-time delivery** — WebSockets or polling?
3. **Mobile push** — Should we integrate with native push notifications?
4. **Preferences** — Per-notification-type opt-out or global toggle?

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Time to notice critical alerts | 4+ hours | < 15 min |
| "Missed notification" tickets | 25% of support | < 5% |
| Daily active users checking notifications | N/A | > 60% |

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
