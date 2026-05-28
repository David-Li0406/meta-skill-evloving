# Templates

CarPlay templates are the building blocks of your CarPlay app's user interface. Each template provides a specific layout and interaction pattern optimized for in-car use.


---

# CPTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An abstract base class for interface templates.

## API Reference

### Accessing Template Information
• **userInfo** - Any custom data or object that you want to associate with the template.

### Accessing Tab Information
• **tabTitle** - A short title that describes the content of the tab.
• **tabImage** - An image that represents the content of the tab.
• **tabSystemItem** - A system object that provides a title and image for common tab content, such as contacts or favorite...
• **showsTabBadge** - An indicator you use to call attention to the tab.


---

# CPListTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A template that displays and manages a list of items.

## API Reference

### Creating a List Template
• **init(title:sections:)** - Creates a list template with an array of list sections and optional title.
• **init(title:sections:assistantCellConfiguration:)** - Creates a sectioned list template that optionally displays the assistant cell.

### Managing Sections
• **maximumSectionCount** - The maximum number of sections that the template can display.
• **sectionCount** - The number of sections in the list.
• **sections** - The sections that the list displays.
• **updateSections(_:)** - Adds, removes, reorders, or updates the list's sections.
• **CPListSection** - A container that groups your list items into sections.

### Managing the Assistant Cell
• **assistantCellConfiguration** - The object that provides the configuration attributes for the assistant cell.
• **CPAssistantCellConfiguration** - An object that provides the configuration attributes for the assistant cell.

### Managing an Empty List
• **emptyViewTitleVariants** - An array of title variants for the template's empty view.
• **emptyViewSubtitleVariants** - An array of subtitle variants for the template's empty view.

### Getting Supplementary Information
• **maximumItemCount** - The maximum number of items, across all sections, that the template can display.
• **itemCount** - The total number of items, across all sections, in the list.
• **indexPath(for:)** - Returns the index path for the specified item.
• **title** - The title that the navigation bar displays when the template is visible.

### Responding to List Events
• **delegate** - The object that serves as the delegate to the list template.
• **CPListTemplateDelegate** - The interface an object implements to serve as the delegate for a list template.

### Initializers
• **init(title:sections:assistantCellConfiguration:headerGridButtons:)** - Initialize a list template with one or more grid buttons to displayed in a list header.

### Instance Properties
• **headerGridButtons** - Assigning to this property will dynamically update the List Template and show the new header.
• **showsSpinnerWhileEmpty** - If YES, a spinning activity indicator will be displayed while the list template contains no items. T...

### Type Properties
• **maximumGridButtonImageSize** - The expected image size for your @c CPGridButton.
• **maximumHeaderGridButtonCount** - The maximum number of grid buttons that may appear in a @c CPListTemplate.


---

# CPGridTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A template that displays and manages a grid of items.

## API Reference

### Creating a Grid Template
• **init(title:gridButtons:)** - Creates a grid template with a title and a set of buttons.
• **CPGridButton** - A menu item button displayed on a grid template.

### Getting the Grid Title
• **title** - The title shown in the grid template's navigation bar.

### Getting the Grid Buttons
• **gridButtons** - The array of grid buttons displayed on the template.

### Instance Methods
• **updateGridButtons(_:)** -
• **updateTitle(_:)** -

### Type Properties
• **maximumGridButtonImageSize** - The expected image size for your @c CPGridButton.


---

# CPTabBarTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A container template that displays and manages other templates, presenting them as tabs.

## API Reference

### Creating a Tab Bar Template
• **init(templates:)** - Creates a tab bar template that displays the provided root templates as tabs.

### Managing Tab Bar Interactions
• **delegate** - The object that acts as the template's delegate.
• **CPTabBarTemplateDelegate** - The methods an object implements to act as the delegate for a tab bar template.

### Managing the Templates
• **templates** - The tab bar's templates.
• **updateTemplates(_:)** - Adds, removes, reorders, or updates the tab bar's templates.
• **maximumTabCount** - The maximum number of tabs that the template can display.

### Getting the Selected Template
• **selectedTemplate** - The currently selected template in the tab bar.

### Instance Methods
• **select(_:)** -
• **selectTemplate(at:)** -


---

# CPAlertTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A template that displays a modal alert.

## API Reference

### Creating an Alert Template
• **init(titleVariants:actions:)** - Creates an alert template.
• **maximumActionCount** - The maximum number of actions allowed in an alert template.

### Getting the Alert Information
• **titleVariants** - The array of title variants.
• **actions** - The array of actions available on the alert.


---

# CPSearchTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A template that provides the ability to search for a destination and see a list of search results.

## API Reference

### Providing a Search Template Delegate
• **delegate** - The object that serves as the search template's delegate.
• **CPSearchTemplateDelegate** - The interface for an object that serves as the search template's delegate.


---

# CPInformationTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A template that provides information for a point of interest, food order, parking location, or charging location.

## API Reference

### Creating an Information Template
• **init(title:layout:items:actions:)** - Creates an information template that displays the provided items using the chosen layout.

### Accessing the Layout
• **layout** - The layout that the template uses to arrange its items.
• **CPInformationTemplateLayout** - The layout that an information template uses to arrange its items.

### Managing the Title
• **title** - The template's title.

### Managing the Items
• **items** - The items that the template displays.
• **CPInformationItem** - A data object that provides content for an information template.
• **CPInformationRatingItem** - A data object that provides rated content for an information template.

### Managing the Actions
• **actions** - The actions that the template displays.


---

# CPActionSheetTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A template that displays a modal action sheet.

## API Reference

### Creating an Action Sheet Template
• **init(title:message:actions:)** - Creates an action sheet template.

### Getting Action Sheet Template Information
• **title** - The title of the action sheet.
• **message** - The descriptive message providing details about the reason for displaying the action sheet.
• **actions** - The list of actions available on the action sheet.


---

# CPVoiceControlTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A template that displays a voice control indicator during audio input.

## API Reference

### Creating a Voice Control Template
• **init(voiceControlStates:)** - Creates a voice control template with a list of voice control states.
• **CPVoiceControlState** - A voice control state containing title variants and images for use by a voice control template.

### Activating a State
• **activateVoiceControlState(withIdentifier:)** - Changes the template's state to the one matching the specified identifier.
• **activeStateIdentifier** - The identifier of the template's current voice control state.

### Getting Available States
• **voiceControlStates** - The array of voice control states available to the template.


---

# CPContactTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A template that displays information about a person or a business.

## API Reference

### Creating a Contact Template
• **init(contact:)** - Creates a contact template that displays the provided contact.

### Configuring the Contact
• **contact** - The contact that the template displays.
• **CPContact** - A data object that contains information about a contact.


---

# CPPointOfInterestTemplate

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A template that displays a map with selectable points of interest.

## API Reference

### Creating a Point of Interest Template
• **init(title:pointsOfInterest:selectedIndex:)** - Creates a Point of Interest template with a title, the points of interest to display, and the initia...
• **CPPointOfInterest** - An object that describes a point of interest on the template's map and in its scrollable picker.

### Handling Template Events
• **pointOfInterestDelegate** - The object that serves as the template's delegate.
• **CPPointOfInterestTemplateDelegate** - The methods to handle a Point of Interest template's events.

### Managing the Picker's Title
• **title** - The scrollable picker's title.

### Managing the Points of Interest
• **pointsOfInterest** - The points of interest the template displays on the map and in the scrollable picker.
• **setPointsOfInterest(_:selectedIndex:)** - Updates the points of interest and the current selection.
• **selectedIndex** - The current selection's index.
