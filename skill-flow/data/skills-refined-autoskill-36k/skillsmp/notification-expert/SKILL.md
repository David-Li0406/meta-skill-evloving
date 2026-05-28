---
name: notification-expert
description: Push notification and UNUserNotificationCenter expert. Use when working with APNs, actionable notifications, notification categories, or local notifications on watchOS/iOS.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Push Notification Expert

## Instructions

When working with notifications:

1. Understand the notification flow (APNs -> App -> User)
2. Properly configure notification categories and actions
3. Handle both foreground and background delivery
4. Test notification handling thoroughly

## watchOS Notification Patterns

### Permission Request
```swift
UNUserNotificationCenter.current().requestAuthorization(
    options: [.alert, .sound, .badge]
) { granted, error in
    if granted {
        // Register for remote notifications
        WKExtension.shared().registerForRemoteNotifications()
    }
}
```

### Notification Categories
```swift
// Define actions
let approveAction = UNNotificationAction(
    identifier: "APPROVE",
    title: "Approve",
    options: [.foreground]
)

let rejectAction = UNNotificationAction(
    identifier: "REJECT",
    title: "Reject",
    options: [.destructive]
)

// Create category
let category = UNNotificationCategory(
    identifier: "ACTION_CATEGORY",
    actions: [approveAction, rejectAction],
    intentIdentifiers: [],
    options: [.customDismissAction]
)

// Register
UNUserNotificationCenter.current().setNotificationCategories([category])
```

### Handling Responses
```swift
extension AppDelegate: UNUserNotificationCenterDelegate {
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse,
        withCompletionHandler completionHandler: @escaping () -> Void
    ) {
        switch response.actionIdentifier {
        case "APPROVE":
            // Handle approval
        case "REJECT":
            // Handle rejection
        case UNNotificationDefaultActionIdentifier:
            // User tapped notification body
        case UNNotificationDismissActionIdentifier:
            // User dismissed notification
        default:
            break
        }
        completionHandler()
    }
}
```

### Local Notifications
```swift
let content = UNMutableNotificationContent()
content.title = "Action Required"
content.body = "Claude needs your approval"
content.categoryIdentifier = "ACTION_CATEGORY"
content.userInfo = ["action_id": "abc123"]

let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: trigger)

UNUserNotificationCenter.current().add(request)
```

## Best Practices
- Always handle notification permissions gracefully
- Use actionable notifications for quick responses
- Include relevant data in `userInfo` dictionary
- Test with both app foreground and background
- Handle notification dismissal appropriately
