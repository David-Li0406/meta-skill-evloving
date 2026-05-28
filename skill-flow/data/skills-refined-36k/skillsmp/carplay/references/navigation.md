# Navigation

CarPlay provides comprehensive navigation support including maps, routes, maneuvers, and points of interest.


---

# CPMapTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A template that displays a navigation overlay that your app draws on the map.

## API Reference

### Configuring Map Templates
• **automaticallyHidesNavigationBar** - A Boolean value that indicates whether the template should automatically hide the navigation bar.
• **hidesButtonsWithNavigationBar** - A Boolean value that tells the system to hide the map buttons when hiding the navigation bar.
• **guidanceBackgroundColor** - The background color the map template uses when displaying guidance.

### Handling Map Template Events
• **mapDelegate** - The object that serves as the delegate of the map template.
• **CPMapTemplateDelegate** - The protocol an object implements to handle events from a map template.

### Managing Map Buttons
• **mapButtons** - An array of map buttons on the trailing bottom corner of the map template.
• **CPMapButton** - A button that represents an action that a map template displays on the CarPlay screen.

### Displaying Trip Previews
• **showTripPreviews(_:textConfiguration:)** - Displays the preview for one or more trips, and allows route selection.
• **showTripPreviews(_:selectedTrip:textConfiguration:)** - Displays the previews for a collection of trips, with a single selected trip.
• **hideTripPreviews()** - Hides the display of trip previews.
• **showRouteChoicesPreview(for:textConfiguration:)** - Displays the route choices for a single trip.
• **CPTripPreviewTextConfiguration** - A configuration object for changing the button titles on a trip preview.

### Navigating a Trip
• **startNavigationSession(for:)** - Begins navigational guidance for a trip.
• **CPNavigationSession** - An object that represents an active route guidance session.

### Providing Trip Estimates
• **updateEstimates(_:for:)** - Updates travel estimates, such as arrival time and the remaining time and distance for a trip.
• **update(_:for:with:)** - Updates travel estimates, such as arrival time and the remaining time and distance for a trip, with ...
• **CPTimeRemainingColor** - The color the system uses when displaying the time remaining for a trip.
• **tripEstimateStyle** - The style that the map template uses when displaying trip estimates during active nagivation.
• **CPTripEstimateStyle** - The set of display styles for trip estimates.

### Displaying a Navigation Alert
• **present(navigationAlert:animated:)** - Displays a navigation alert on the map template.
• **dismissNavigationAlert(animated:completion:)** - Tells the map template to dismiss the visable navigation alert.
• **currentNavigationAlert** - The visible navigation alert.
• **CPNavigationAlert** - An alert that displays map- or navigation-related information to the user.

### Panning the Map
• **showPanningInterface(animated:)** - Shows the panning interface on the map.
• **dismissPanningInterface(animated:)** - Dismisses the panning interface.
• **isPanningInterfaceVisible** - A Boolean value that indicates whether the map template is displaying the panning interface.


---

# CPTrip

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An object that represents a journey between an origin and a destination.

## API Reference

### Creating a Trip
• **init(origin:destination:routeChoices:)** - Creates a trip with an origin, destination, and route choices.
• **CPRouteChoice** - A possible route for a trip.

### Getting the Trip's Origin and Destination
• **origin** - The trip's origin.
• **destination** - The trip's destination.

### Getting Route Choices
• **routeChoices** - The list of route choices for the trip.
• **destinationNameVariants** - An array of strings that represents the names of the destination for this trip, arranged from most to least specific.

### Providing Additional Information
• **userInfo** - A custom object associated with the trip.


---

# CPNavigationSession

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An object that represents an active route guidance session.

## API Reference

### Getting the Trip
• **trip** - The trip associated with the navigation session.
• **CPTrip** - An object that represents a journey between an origin and a destination.

### Managing Trip Navigation
• **cancelTrip()** - Tells the navigation session to cancel the trip.
• **finishTrip()** - Tells the navigation session to finish the trip.
• **pauseTrip(for:description:)** - Tells the navigation session to pause the trip for the specified reason.
• **pauseTrip(for:description:turnCardColor:)** -
• **CPNavigationSession.PauseReason** - A set of reasons for pausing a trip.

### Managing Upcoming Maneuvers
• **upcomingManeuvers** - The next set of maneuvers the user should perform while following the current route.
• **maneuverState** - The current maneuver state.
• **currentRoadNameVariants** - An array of strings that describe variants of the current road name.
• **currentLaneGuidance** - The current lane guidance to use for navigation metadata.
• **add(_:)** - Adds one or more maneuvers, in chronological order, to the navigation session.

### Updating Travel Estimates
• **updateEstimates(_:for:)** - Updates the travel estimates for the specified maneuver.
• **CPTravelEstimates** - An object that describes the time and distance remaining for a maneuver in a navigation session.


---

# CPManeuver

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An object that describes a single navigation instruction.

## API Reference

### Providing instructions
• **dashboardInstructionVariants** - An array of instruction variants for the CarPlay dashboard.
• **notificationInstructionVariants** - An array of instruction variants for notification banners.

### Providing attributed instructions
• **attributedInstructionVariants** - An array of attributed instruction variants for the maneuver.
• **dashboardAttributedInstructionVariants** - An array of attributed instruction variants for the CarPlay dashboard.
• **notificationAttributedInstructionVariants** - An array of attributed instruction variants for notification banners.

### Providing travel estimates
• **initialTravelEstimates** - An object that describes the distance and time remaining before the maneuver completes.

### Providing symbol images
• **symbolImage** - An image that represents the maneuver.
• **dashboardSymbolImage** - An image for the CarPlay dashboard that represents the maneuver.
• **notificationSymbolImage** - An image for notification banners that represents the maneuver.
• **symbolSet** - An image set that represents the maneuver.

### Providing junction images
• **junctionImage** - An image that represents an upcoming junction.
• **dashboardJunctionImage** - An image for the CarPlay dashboard that represents an upcoming junction.

### Providing junction information
• **junctionType** - A value that represents the type of junction associated with this maneuver.
• **junctionExitAngle** - The angle of the exit road of this junction.
• **junctionElementAngles** - A set of angles for the rest of the roads of this junction.

### Providing maneuver information
• **maneuverType** - A value that represents the type of maneuver.
• **roadFollowingManeuverVariants** - An array of strings that represent the names of the road following this maneuver, arranged from most...
• **linkedLaneGuidance** - A value that represents lane guidance associated with this maneuver.
• **highwayExitLabel** - A string that describes a highway exit.
• **trafficSide** - A value that represents which side of the road the traffic drives on.

### Providing additional information
• **userInfo** - A custom object associated with the maneuver.

### Instance properties
• **cardBackgroundColor** -
• **instructionVariants** - An array of instruction variants for the maneuver.


---

# CPTravelEstimates

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An object that describes the time and distance remaining for a maneuver in a navigation session.

## API Reference

### Creating a Travel Estimates Object
• **init(distanceRemaining:timeRemaining:)** - Creates travel estimates with the remaining distance and time.
• **init(distanceRemaining:distanceRemainingToDisplay:timeRemaining:)** - Creates a travel estimates instance with the distance remaining that the framework displays to a per...

### Getting Travel Estimates
• **distanceRemaining** - The remaining distance for the travel estimate.
• **distanceRemainingToDisplay** - The distance remaining that the framework displays to a person, in the default units of measurement.
• **timeRemaining** - The remaining time for the travel estimate.


---

# CPRouteChoice

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A possible route for a trip.

## API Reference

### Creating a Route Choice
• **init(summaryVariants:additionalInformationVariants:selectionSummaryVariants:)** - Creates a route choice.

### Getting Variants
• **summaryVariants** - An array of summary variants.
• **additionalInformationVariants** - An array of variants providing additional information about the route choice.
• **selectionSummaryVariants** - An array of selection summary variants.

### Providing Additional Information
• **userInfo** - An object containing custom information associated with the route choice.


---

# CPLane

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 17.4, iPadOS 17.4, Mac Catalyst 17.4

## Overview
A class that describes characteristics of a lane on a roadway.

## API Reference

### Properties
• **primaryAngle** - A value that represents the angle the framework highlights if this lane is preferred or good.
• **secondaryAngles** - A list of the remaining angles of this lane guidance.
• **status** - A value that describes the lane's status.

### Lane status
• **CPLaneStatus** - Values that describe the status or preferability of a lane.

### Initializers
• **init()** -
• **init(angles:)** -
• **init(angles:highlightedAngle:isPreferred:)** -

### Instance Properties
• **angles** -
• **highlightedAngle** -


---

# CPLaneGuidance

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 17.4, iPadOS 17.4, Mac Catalyst 17.4

## Overview
A class that provides information that describes the number of lanes on a roadway and navigation instruction variants.

## API Reference

### Properties
• **instructionVariants** - An array of strings that represent the instruction for this lane guidance, arranged from most- to le...
• **lanes** - An array of lane objects, each describing a single lane.


---

# CPMapButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A button that represents an action that a map template displays on the CarPlay screen.

## API Reference

### Creating a Map Button
• **init(handler:)** - Creates a new map button.

### Providing Button Images
• **image** - The image to display on the button.
• **focusedImage** - The image to display when focus is on the button.

### Controlling the Button
• **isEnabled** - A Boolean value that enables and disables the map button.
• **isHidden** - A Boolean value that hides and shows the map button.


---

# CPNavigationAlert

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An alert that displays map- or navigation-related information to the user.

## API Reference

### Creating a Navigation Alert
• **init(titleVariants:subtitleVariants:image:primaryAction:secondaryAction:duration:)** - Creates a navigation alert.
• **init(titleVariants:subtitleVariants:imageSet:primaryAction:secondaryAction:duration:)** - Creates a navigation alert.

### Getting Titles
• **titleVariants** - An array of title strings.
• **subtitleVariants** - An array of subtitle strings.
• **updateTitleVariants(_:subtitleVariants:)** - Updates title and subtitle variants.

### Getting the Alert Image
• **image** - An image displayed in the navigation alert.
• **imageSet** - An image set displayed in the navigation alert.

### Getting the Actions
• **primaryAction** - The primary action, and button, for the navigation alert.
• **secondaryAction** - An optional secondary action, and button, for the navigation alert.

### Getting the Alert Duration
• **duration** - The amount of time, in seconds, that the alert is visible.
• **CPNavigationAlertMinimumDuration** - A constant that defines the minimum amount of time that an alert is visible.

### Enumerations
• **CPNavigationAlert.DismissalContext** - A set of reasons for dismissing a navigation alert.
