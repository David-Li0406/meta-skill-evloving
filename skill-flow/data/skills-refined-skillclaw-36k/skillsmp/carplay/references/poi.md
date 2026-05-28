# Poi

Points of Interest (POI) allow you to display and interact with locations on the map.


---

# CPPointOfInterest

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
An object that describes a point of interest on the template's map and in its scrollable picker.

## API Reference

### Creating a Point of Interest
• **init(location:title:subtitle:summary:detailTitle:detailSubtitle:detailSummary:pinImage:)** - Creates a point of interest for a specific location.

### Managing the Map Annotation
• **location** - The map item that contains the point of interest's geographical information.
• **pinImage** - A custom image that the map annotation displays.

### Managing the Picker Item's Data
• **title** - The title that the picker's item displays.
• **subtitle** - The subtitle that the picker's item displays.
• **summary** - The summary that the picker's item displays.

### Managing the Detail Card's Data
• **detailTitle** - The detail card's title.
• **detailSubtitle** - The detail card's subtitle.
• **detailSummary** - The detail card's summary.

### Managing the Detail Card's Buttons
• **primaryButton** - The detail card's primary action button.
• **secondaryButton** - The detail card's secondary action button.

### Attaching Additional Context
• **userInfo** - An opaque value for the point of interest.

### Initializers
• **init(location:title:subtitle:summary:detailTitle:detailSubtitle:detailSummary:pinImage:selectedPinImage:)** -

### Instance Properties
• **selectedPinImage** -

### Type Properties
• **pinImageSize** -
• **selectedPinImageSize** -
