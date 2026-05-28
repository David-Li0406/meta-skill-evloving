---
name: mapkit-implementation
description: Use this skill when implementing MapKit features in iOS or macOS applications, including displaying maps, user location, route calculations, and geocoding.
---

# MapKit Implementation

This guide covers the implementation of MapKit features for iOS 17+ and macOS 14+ applications using SwiftUI and AppKit. It supports functionalities such as displaying maps, user location tracking, route calculations, local searches, and geocoding.

## Quick Start Checklist

Essential steps for implementing MapKit features:

1. **Info.plist Configuration**
   - iOS: `NSLocationWhenInUseUsageDescription` and `NSLocationAlwaysAndWhenInUseUsageDescription` for location access.
   - macOS: `NSLocationUsageDescription` for location access reason.

2. **Framework Import**
   ```swift
   import MapKit
   import CoreLocation
   ```

3. **Location Permission Request**
   - Check status with `CLLocationManager.authorizationStatus`.
   - Request permission using `requestWhenInUseAuthorization()`.

4. **Display Map**
   - Use SwiftUI `Map` view for displaying maps.
   - Control position and zoom with `MapCameraPosition`.

## Core Components

### Map (SwiftUI iOS 17+ and macOS 14+)

Utilize the refreshed Map API.

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
    }
}
```

**Key Properties:**
- `position`: Camera position options (e.g., `.automatic`, `.userLocation()`, `.region()`, `.camera()`).
- `mapStyle`: Map appearance options (e.g., `.standard`, `.imagery`, `.hybrid`).

### Markers and Annotations

#### Marker

System-provided markers.

```swift
Map {
    Marker("Tokyo Station", coordinate: .tokyoStation)
    Marker("Restaurant", systemImage: "fork.knife", coordinate: location)
        .tint(.orange)
}
```

#### Annotation

Custom views displayed as markers.

```swift
Map {
    Annotation("Custom", coordinate: location) {
        VStack {
            Image(systemName: "star.fill")
                .foregroundStyle(.yellow)
            Text("Spot")
                .font(.caption)
        }
        .padding(4)
        .background(.white)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}
```

### CLLocationManager Setup

Setting up the location manager.

```swift
@MainActor
@Observable
final class LocationManager: NSObject, CLLocationManagerDelegate {
    var location: CLLocation?
    var authorizationStatus: CLAuthorizationStatus = .notDetermined

    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
    }

    func requestAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    func startUpdating() {
        manager.startUpdatingLocation()
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        Task { @MainActor in
            location = locations.last
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
        }
    }
}
```

### Route & Navigation

#### MKDirections

Perform route calculations.

```swift
func calculateRoute(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) async throws -> MKRoute {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile

    let directions = MKDirections(request: request)
    let response = try await directions.calculate()

    guard let route = response.routes.first else {
        throw MapError.noRouteFound
    }

    return route
}
```

### Local Search

#### MKLocalSearch

Execute nearby searches.

```swift
func searchNearby(query: String, region: MKCoordinateRegion) async throws -> [MKMapItem] {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = region

    let search = MKLocalSearch(request: request)
    let response = try await search.start()

    return response.mapItems
}
```

### Geocoding

#### Forward Geocoding (Address to Coordinates)

```swift
func geocode(address: String) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(address)

    guard let location = placemarks.first?.location else {
        throw MapError.geocodingFailed
    }

    return location.coordinate
}
```

#### Reverse Geocoding (Coordinates to Address)

```swift
func reverseGeocode(coordinate: CLLocationCoordinate2D) async throws -> String {
    let geocoder = CLGeocoder()
    let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
    let placemarks = try await geocoder.reverseGeocodeLocation(location)

    guard let placemark = placemarks.first else {
        throw MapError.geocodingFailed
    }

    return [placemark.locality, placemark.thoroughfare, placemark.subThoroughfare]
        .compactMap { $0 }
        .joined(separator: " ")
}
```

### Look Around (iOS 17+ and macOS 14+)

#### Scene Request

Retrieve Look Around scenes.

```swift
func getLookAroundScene(for coordinate: CLLocationCoordinate2D) async -> MKLookAroundScene? {
    let request = MKLookAroundSceneRequest(coordinate: coordinate)
    return try? await request.scene
}
```

### Custom Overlays

#### MapCircle

Circular overlay.

```swift
Map {
    MapCircle(center: coordinate, radius: 500)
        .foregroundStyle(.blue.opacity(0.3))
        .stroke(.blue, lineWidth: 2)
}
```

#### MapPolygon

Polygonal overlay.

```swift
Map {
    MapPolygon(coordinates: polygonCoordinates)
        .foregroundStyle(.green.opacity(0.3))
        .stroke(.green, lineWidth: 2)
}
```

## Error Handling

Common errors in MapKit/CoreLocation:

| Error | Cause | Action |
|-------|-------|--------|
| `CLError.denied` | Location access denied | Redirect to settings |
| `MKError.serverFailure` | Server error | Retry |
| `MKError.directionsNotFound` | Route not found | Suggest alternatives |

## Quick Reference

| Component | Purpose | Key API |
|-----------|---------|---------|
| `Map` | Display map | `Map(position:) { }` |
| `Marker` | Display markers | `Marker(_:coordinate:)` |
| `CLLocationManager` | Manage location | `startUpdatingLocation()` |
| `MKDirections` | Route search | `calculate()` |
| `MKLocalSearch` | Nearby search | `start()` |
| `CLGeocoder` | Geocoding | `geocodeAddressString(_:)` |
| `LookAroundPreview` | Display Look Around | `LookAroundPreview(scene:)` |

## Additional Resources

### Reference Files

Refer to the following for detailed information:

- **`references/mapkit-swiftui.md`** - MapKit for SwiftUI API reference
- **`references/core-location.md`** - Core Location integration details
- **`references/geocoding.md`** - Geocoding configuration details
- **`references/directions.md`** - Directions API reference
- **`references/local-search.md`** - Local search details
- **`references/look-around.md`** - Look Around functionality details
- **`references/custom-overlays.md`** - Custom overlay implementation
- **`references/troubleshooting.md`** - Error codes and debugging methods

### Example Files

Refer to the `examples/` directory for implementation samples:

- **`examples/basic-map-view.swift`** - Basic map display
- **`examples/location-manager.swift`** - Location manager implementation
- **`examples/marker-annotation-view.swift`** - Marker/annotation implementation
- **`examples/directions-view.swift`** - Route search/navigation screen
- **`examples/local-search-view.swift`** - Local search UI
- **`examples/look-around-view.swift`** - Look Around integration