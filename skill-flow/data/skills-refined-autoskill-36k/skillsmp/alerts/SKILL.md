---
name: alerts
description: Send alerts and notifications using AppleScript - banners, modals, and text-to-speech
---

# Alerts Skill

Send alerts and notifications to Matt using AppleScript.

## When to Use

- Reminders that need immediate attention
- Completion notifications for long-running tasks
- Important alerts that shouldn't be missed

## Alert Types

### Non-Modal (Banner/Notification Center)

Use for informational alerts that don't require immediate action:

```bash
osascript /path/to/skill/alerts/notify.scpt "Title" "Message body here"
```

The notification appears briefly and goes to Notification Center.

### Modal (Dialog Box)

Use for alerts that require acknowledgement:

```bash
osascript /path/to/skill/alerts/dialog.scpt "Title" "Message body here"
```

This blocks until the user clicks OK. Use sparingly.

### Modal with Sound

For urgent alerts:

```bash
osascript /path/to/skill/alerts/dialog.scpt "Title" "Message body here" "Ping"
```

Available sounds: Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink

### Say (Text-to-Speech)

For hands-free alerts:

```bash
osascript /path/to/skill/alerts/say.scpt "Your meeting starts in 5 minutes"
```

## Script Locations

All scripts are in the same directory as this SKILL.md:

- `notify.scpt` - Non-modal banner notification
- `dialog.scpt` - Modal dialog (blocks until dismissed)
- `say.scpt` - Text-to-speech

## Guidelines

1. **Prefer non-modal** for most alerts - they're less disruptive
2. **Use modal** only when acknowledgement is required
3. **Use say** when Matt might not be looking at the screen
4. **Combine methods** for critical alerts (e.g., say + modal)

## Examples

```bash
# Reminder about a meeting
osascript ~/.opencode/skill/alerts/notify.scpt "Calendar" "Team sync in 15 minutes"

# Task completed
osascript ~/.opencode/skill/alerts/notify.scpt "Build Complete" "All tests passed"

# Urgent - needs action
osascript ~/.opencode/skill/alerts/dialog.scpt "Action Required" "PR review requested by Sarah" "Ping"

# Hands-free reminder
osascript ~/.opencode/skill/alerts/say.scpt "Don't forget to submit the form before noon"
```
