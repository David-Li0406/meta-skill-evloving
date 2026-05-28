---
name: mapkit-implementation
description: Use this skill when you need to implement MapKit features in macOS or iOS applications, including displaying maps, showing user locations, adding markers, and handling location permissions.
---

# MapKit Implementation Guide

This guide provides instructions for implementing MapKit features in macOS (14+) and iOS (17+) applications using SwiftUI. It covers displaying maps, user location tracking, route calculations, and nearby searches.

## Quick Start Checklist

### 1. Info.plist Configuration
- For macOS:
  - `NSLocationUsageDescription` - Reason for accessing location.
- For iOS:
  - `NSLocationWhenInUseUsageDescription` - Reason for accessing location when in use.
  - `NSLocationAlwaysAndWhenInUseUsageDescription` - Reason for accessing location always (if needed).

### 2. Entitlements Configuration (App Sandbox for macOS)
- `com.apple.security.personal-information.location` - Access to location services.
- `com.apple.security.network.client` - Network access for location services.

### 3. Framework Import
```swift
import MapKit
import CoreLocation
```

### 4. Requesting Location Permissions
- Check authorization status with `CLLocationManager.authorizationStatus`.
- Request permission using `requestWhenInUseAuthorization()`.

### 5. Displaying the Map
- Use SwiftUI's Map view to display the map.
- Control position and zoom with `MapCameraPosition`.

## Core Components

### Map (SwiftUI macOS 14+ and iOS 17+)
Utilize the refreshed Map API for both platforms.

```swift
@State private var position: MapCameraPosition = .automatic

var body: some View {
    Map(position: $position) {
        Marker("Tokyo", coordinate: .tokyo)
        UserAnnotation()
    }
    .mapStyle(.standard(elevation: .realistic))
    .mapControls {
        MapUserLocationButton()
        MapCompass()
        MapScaleView()
        // Add MapZoomStepper for macOS if needed
    }
}
```

**Key Properties:**
- `position` - Camera position options: `.automatic`, `.userLocation()`, `.region()`, `.camera()`.
- `mapStyle` - Map style options: `.standard`, `.imagery`, `.hybrid`.
- `interactionModes` - Interaction modes: `.all`, `.pan`, `.zoom`, `.rotate`, `.pitch`.

### MapCameraPosition
Control the camera position with the following examples:

```swift
// Follow user location
let position: MapCameraPosition = .userLocation(fallback: .automatic)

// Display a specific region
let position: MapCameraPosition = .region(MKCoordinateRegion(
    center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
))

// Specify camera angle
let position: MapCameraPosition = .camera(MapCamera(
    centerCoordinate: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    altitude: 1000,
    heading: 0,
    pitch: 0
))
```

This skill consolidates the implementation details for both macOS and iOS, ensuring a comprehensive approach to using MapKit across platforms.