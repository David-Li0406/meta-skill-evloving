# Getting Started

CarPlay scene management and configuration for iOS apps.


---

# CPSessionConfiguration

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An object that provides vehicle properties and configuration for the CarPlay environment.

## API Reference

### Creating a Session Configuration
• **init(delegate:)** - Creates a session configuration with a delegate.
• **CPSessionConfigurationDelegate** - A protocol for receiving notifications about changes to vehicle properties and configuration.

### Managing the Delegate
• **delegate** - An object that serves as the delegate to the session configuration.

### Getting the Content Style
• **contentStyle** - The content style that the vehicle selects.
• **CPContentStyle** - The types of content style that the vehicle allows.

### Getting the Limits
• **limitedUserInterfaces** - A bit mask value that indicates the user interface limits.
• **CPLimitableUserInterface** - The types of limitable user interface elements.


---

# CPTemplateApplicationSceneDelegate

**Technology:** CarPlay
**Type:** protocol
**Platforms:** iOS 13.0, iPadOS 13.0, Mac Catalyst 13.1

## Overview
The methods for responding to the life cycle events of your app's scene.

## API Reference

### Responding to the Scene Life Cycle
• **templateApplicationScene(_:didConnect:)** - Tells the delegate about the addition of a CarPlay scene to the app.
• **templateApplicationScene(_:didConnect:to:)** - Tells the delegate about the addition of a CarPlay scene to your navigation app.
• **templateApplicationScene(_:didDisconnectInterfaceController:)** - Tells the delegate when CarPlay removes a scene from the app.
• **templateApplicationScene(_:didDisconnect:from:)** - Tells the delegate when CarPlay removes a scene from your navigation app.

### Responding to User Actions
• **templateApplicationScene(_:didSelect:)** - Tells the delegate when the user selects a maneuver while the app is in the background.
• **templateApplicationScene(_:didSelect:)** - Tells the delegate when the user selects a navigation alert while the app is in the background.

### Instance Methods
• **contentStyleDidChange(_:)** -
