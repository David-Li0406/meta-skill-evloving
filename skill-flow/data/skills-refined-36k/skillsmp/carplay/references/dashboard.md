# Dashboard and Instrument Cluster

CarPlay Dashboard and Instrument Cluster features for advanced navigation apps (iOS 13.4+ and iOS 15.4+).


---

# CPDashboardButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 13.4, iPadOS 13.4, Mac Catalyst 13.4

## Overview
A shortcut button for placement on the CarPlay Dashboard.

## API Reference

### Creating a Dashboard Button
• **init(titleVariants:subtitleVariants:image:handler:)** - Creates a dashboard button that displays a title, an optional subtitle, and an image.

### Accessing the Button Configuration
• **titleVariants** - The array of title variants for the button.
• **subtitleVariants** - The array of subtitle variants for the button.
• **image** - The image the button displays.


---

# CPDashboardController

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 13.4, iPadOS 13.4, Mac Catalyst 13.4

## Overview
A controller that provides shortcut buttons for the CarPlay Dashboard.

## API Reference

### Providing Dashboard Buttons
• **shortcutButtons** - An array of shortcut buttons to display on the CarPlay Dashboard.
• **CPDashboardButton** - A shortcut button for placement on the CarPlay Dashboard.


---

# CPTemplateApplicationDashboardScene

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 13.4, iPadOS 13.4, Mac Catalyst 13.4

## Overview
A CarPlay scene that controls your app's dashboard navigation window.

## API Reference

### Responding to the Dashboard Scene Life Cycle
• **delegate** - The object that receives the dashboard scene's life-cycle events.
• **CPTemplateApplicationDashboardSceneDelegate** - The methods for responding to the life-cycle events of your navigation app's dashboard scene.

### Accessing the Dashboard Controller
• **dashboardController** - The controller that manages the dashboard scene's shortcut buttons.
• **CPDashboardController** - A controller that provides shortcut buttons for the CarPlay Dashboard.

### Accessing the Dashboard Window
• **dashboardWindow** - The window that belongs to the dashboard scene.


---

# CPTemplateApplicationDashboardSceneDelegate

**Technology:** CarPlay
**Type:** protocol
**Platforms:** iOS 13.4, iPadOS 13.4, Mac Catalyst 13.4

## Overview
The methods for responding to the life-cycle events of your navigation app's dashboard scene.

## API Reference

### Responding to the Scene Life Cycle
• **templateApplicationDashboardScene(_:didConnect:to:)** - Tells the delegate about the addition of a CarPlay Dashboard scene to your navigation app.
• **templateApplicationDashboardScene(_:didDisconnect:from:)** - Tells the delegate when CarPlay removes the dashboard scene from your navigation app.


---

# CPInstrumentClusterController

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 15.4, iPadOS 15.4, Mac Catalyst 15.4

## Overview
A controller for managing the instrument cluster display in supported vehicles.

## API Reference

### Instance Properties
• **attributedInactiveDescriptionVariants** - Attributed string variants for inactive state descriptions.
• **compassSetting** - The compass display configuration.
• **delegate** - The object that serves as the delegate for instrument cluster events.
• **inactiveDescriptionVariants** - String variants for inactive state descriptions.
• **instrumentClusterWindow** - The window for displaying instrument cluster content.


---

# CPTemplateApplicationInstrumentClusterScene

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 15.4, iPadOS 15.4, Mac Catalyst 15.4

## Overview
A CarPlay scene that controls your app's instrument cluster display.

## API Reference

### Instance Properties
• **contentStyle** - The current content style for the instrument cluster.
• **delegate** - The object that receives the instrument cluster scene's life-cycle events.
• **instrumentClusterController** - The controller that manages the instrument cluster display.


---

# CPTemplateApplicationInstrumentClusterSceneDelegate

**Technology:** CarPlay
**Type:** protocol
**Platforms:** iOS 15.4, iPadOS 15.4, Mac Catalyst 15.4

## Overview
The methods for responding to the life-cycle events of your app's instrument cluster scene.

## API Reference

### Instance Methods
• **contentStyleDidChange(_:)** - Tells the delegate when the content style changes.
• **templateApplicationInstrumentClusterScene(_:didConnect:)** - Tells the delegate about the addition of an instrument cluster scene.
• **templateApplicationInstrumentClusterScene(_:didDisconnectInstrumentClusterController:)** - Tells the delegate when CarPlay removes the instrument cluster scene.


---

# CPRouteInformation

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 17.4, iPadOS 17.4, Mac Catalyst 17.4

## Overview
A class that describes the characteristic elements of a route.

## API Reference

### Initializers
• **init(maneuvers:laneGuidances:currentManeuvers:currentLaneGuidance:trip:maneuverTravelEstimates:)** - Initializes a new route information object with maneuvers, lane guidances, the current maneuvers, the current lane guidance, trip details, and maneuver travel estimates.

### Properties
• **currentLaneGuidance** - A lane guidance object that describes the current lane guidance.
• **currentManeuvers** - An array of maneuver objects that describes the current maneuvers.
• **laneGuidances** - An array of lane guidance objects.
• **maneuverTravelEstimates** - An object that describes the time and distance estimates for a maneuver.
• **maneuvers** - An array of maneuver objects.
• **trip** - The trip object associated with this route.


---

# CPManeuverDisplayStyle

**Technology:** CarPlay
**Type:** struct
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A display style that determines the visual layout for a maneuver.

## API Reference

### Display Styles
• **leadingSymbol** - The symbol appears before the instructions for the maneuver.
• **trailingSymbol** - The symbol appears after the instructions for the maneuver.
• **instructionOnly** - Only the instructions appear for the maneuver.
• **symbolOnly** - Only the symbol appears for the maneuver.

### Initializers
• **init(rawValue:)** - Initializes a maneuver display style using the specified raw value.
