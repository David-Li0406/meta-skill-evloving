# ``handheld``

Plan and navigate sightseeing trips with ease.

@Metadata {
    @DisplayName("Handheld")
    @PageColor(blue)
}

## Overview

handheld is an iOS application that helps users discover nearby attractions,
plan optimal sightseeing routes, and navigate using Apple's Look Around preview.

Built with SwiftUI and MapKit, handheld provides a seamless experience for
travelers who want to make the most of their time exploring new places.

![App hero image showing the main interface](hero-image)

@Row {
    @Column {
        ### Route Planning
        Create optimized routes between multiple destinations.
    }
    
    @Column {
        ### Look Around
        Preview locations before visiting with immersive imagery.
    }
    
    @Column {
        ### Favorites
        Save and organize your favorite spots for future trips.
    }
}

## Featured

@Links(visualStyle: detailedGrid) {
    - <doc:GettingStarted>
    - <doc:RoutePlanning>
    - <doc:FavoriteSpots>
}

## Topics

### Essentials

- <doc:GettingStarted>
- <doc:Architecture>

### Views

- ``ContentView``
- ``MapView``
- ``PlaceDetailView``
- ``RouteView``
- ``FavoritesView``

### View Models

- ``ContentViewModel``
- ``PlanGeneratorViewModel``
- ``LocationSearchViewModel``
- ``FavoriteSpotsViewModel``

### Models

- ``Place``
- ``PlaceCategory``
- ``Route``
- ``SightseeingPlan``
- ``FavoriteSpot``

### Services

- ``LocationManager``
- ``DirectionsService``
- ``LookAroundService``
- ``GeocodingService``

### Data Layer

- ``PlaceRepository``
- ``PlaceRepositoryProtocol``
- ``CacheService``

### Errors

- ``PlaceError``
- ``RoutingError``
- ``LocationError``
