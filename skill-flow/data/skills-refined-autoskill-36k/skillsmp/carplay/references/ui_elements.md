# Ui Elements

UI elements are the individual components you use to build your CarPlay interface.


---

# CPGridButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A menu item button displayed on a grid template.

## API Reference

### Creating a Grid Button
• **init(titleVariants:image:handler:)** - Creates a grid button with the specified title variants, image, and action handler.

### Controlling the Grid Button
• **isEnabled** - A Boolean value that enables and disables the grid button.

### Obtaining Grid Button Information
• **titleVariants** - An array of title variants for the button.
• **image** - The image displayed on the button.

### Initializers
• **init(titleVariants:image:messageConfiguration:handler:)** - Initialize a button with a title, image, and message configuration.

### Instance Properties
• **messageConfiguration** -

### Instance Methods
• **updateImage(_:)** -
• **updateTitleVariants(_:)** -


---

# CPListItem

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A selectable row in a list template.

## API Reference

### Creating a List Item
• **init(text:detailText:)** - Creates a list item with primary and secondary text.
• **init(text:detailText:image:)** - Creates a list item with primary text, secondary text, and an image.
• **init(text:detailText:image:accessoryImage:accessoryType:)** - Creates a list item that displays an accessory beside its content.

### Managing Configuration
• **isEnabled** - A Boolean value that indicates if the item is enabled.
• **handler** - An optional closure that CarPlay invokes when the user selects the list item.
• **userInfo** - An opaque value for the list item.

### Managing Accessories
• **accessoryType** - The accessory that the list item displays in its trailing region.
• **CPListItemAccessoryType** - The accessory types that a list item can display.
• **accessoryImage** - The image that the list item displays in its trailing region.
• **setAccessoryImage(_:)** - Updates the list item's accessory image.

### Managing Content
• **text** - The list item's primary text.
• **setText(_:)** - Updates the list item's primary text.
• **detailText** - The list item's secondary text.
• **setDetailText(_:)** - Updates the list item's secondary text.
• **image** - The image that the list item displays in its leading region.

### Managing Playback Information
• **isExplicitContent** - A Boolean value that determines whether the list item displays its explicit content indicator.
• **isPlaying** - A Boolean value that determines whether the list item displays its Now Playing indicator.
• **playingIndicatorLocation** - The location where the list item displays its Now Playing indicator.
• **CPListItemPlayingIndicatorLocation** - The locations where a list item can display the Now Playing indicator.
• **playbackProgress** - The playback progress status for the content that the list item represents.

### Managing the Assistant Cell
• **CPListItem.AssistantCellPosition** - Constants to specify the position of the assistant cell.
• **CPListItem.AssistantCellVisibility** - Constants to specify the visibility of the assistant cell.

### Deprecated
• **Deprecated Symbols** - Review unsupported symbols and their replacements.


---

# CPListSection

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A container that groups your list items into sections.

## API Reference

### Creating a Section
• **init(items:header:headerSubtitle:headerImage:headerButton:sectionIndexTitle:)** - Creates a section with list items, a header, a section index title, and section header details.
• **CPListTemplateItem** - A description of the common properties of all list item types.
• **CPSelectableListItem** - A description of a selectable list item.
• **CPListItem** - A selectable row in a list template.
• **CPListImageRowItem** - A list template row that displays a series of images.

### Getting Supplementary Information
• **header** - The section's header text.
• **sectionIndexTitle** - The section's index title.

### Getting Items
• **items** - The list of items for the section.
• **index(of:)** - Returns the index of the specified item.
• **item(at:)** - Returns the item at the specified index.

### Configuring Section Headers
• **headerButton** - A button that the section header displays.
• **headerImage** - An image that the section header displays.
• **headerSubtitle** - A string that the header displays as a subtitle.

### Initializers
• **init(items:)** -
• **init(items:header:sectionIndexTitle:)** -


---

# CPListImageRowItem

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A list template row that displays a series of images.

## API Reference

### Creating a List Image Row Item
• **init(text:images:)** - Creates a list item that displays a row of images.
• **init(text:images:imageTitles:)** - Creates a list item that displays a row of images with a title below each image.

### Managing Content
• **text** - The list item's primary text.
• **gridImages** - The images that appear in the list item's image row.
• **update(_:)** - Adds, removes, reorders, or updates the images in the list item's image row.
• **maximumImageSize** - The maximum size of an image that an image row can display.
• **CPMaximumNumberOfGridImages** - The maximum number of images that an image row can contain.

### Managing Selection
• **listImageRowHandler** - An optional closure that CarPlay invokes when the user selects an image.
• **handler** - An optional closure that CarPlay invokes when the user selects the list item.

### Managing Supplementary Information
• **userInfo** - An opaque value for the list item.

### Enabling Items
• **isEnabled** - A Boolean value that indicates if the item is enabled.


---

# CPInformationItem

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A data object that provides content for an information template.

## API Reference

### Creating an Information Item
• **init(title:detail:)** - Creates an information item with a title and detail text.

### Accessing the Item's Attributes
• **title** - The text that the template displays as the item's title.
• **detail** - The text that the template displays below or beside the item's title.


---

# CPMessageListItem

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A list template row that represents a conversation or contact.

## API Reference

### Creating a Message List Item
• **init(conversationIdentifier:text:leadingConfiguration:trailingConfiguration:detailText:trailingText:)** - Creates a list item that represents an existing conversation.
• **init(fullName:phoneOrEmailAddress:leadingConfiguration:trailingConfiguration:detailText:trailingText:)** - Creates a list item that represents a contact.

### Managing the Message Context
• **conversationIdentifier** - The conversation's unique identifier.
• **phoneOrEmailAddress** - The contact's phone number or email address.

### Managing Content
• **text** - The list item's primary text.
• **detailText** - The list item's secondary text.
• **trailingText** - The list item's supplementary text.

### Managing Leading and Trailing Configurations
• **leadingConfiguration** - The configuration of the list item's leading region.
• **CPMessageListItemLeadingConfiguration** - An object that describes the appearance of a message list item's leading region.
• **trailingConfiguration** - The configuration of the list item's trailing region.
• **CPMessageListItemTrailingConfiguration** - An object that describes the appearance of a message list item's trailing region.

### Managing Supplementary Information
• **userInfo** - An opaque value for the list item.

### Enabling Items
• **isEnabled** - A Boolean value that indicates if the item is enabled.


---

# CPAlertAction

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
An object that encapsulates an action the user can perform on an action sheet or alert.

## API Reference

### Creating an Alert Action
• **init(title:style:handler:)** - Creates an alert action with a title, style, and action handler.

### Getting the Title
• **title** - The action button's title.

### Getting the Action Style
• **style** - The display style for the action button.
• **CPAlertAction.Style** - Display styles for an alert's action button.

### Getting the Action Handler
• **handler** - The closure that CarPlay invokes after the user taps the action button.
• **CPAlertActionHandler** - The declaration for an alert action handler.


---

# CPImageSet

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
Light and dark representations of an image.

## API Reference

### Creating an Image Set
• **init(lightContentImage:darkContentImage:)** - Creates an image set with light and dark versions of an image.

### Getting Content Images
• **lightContentImage** - The image the system displays when the user interface style is light.
• **darkContentImage** - The image the system displays when the user interface style is dark.


---

# CPContact

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A data object that contains information about a contact.

## API Reference

### Creating a Contact
• **init(name:image:)** - Creates a contact with a name and an image.

### Configuring the Contact's Attributes
• **image** - The contact's image.
• **name** - The contact's name.
• **subtitle** - A subtitle that the template displays in addition to the contact's name.
• **informativeText** - Additional text that the template displays.

### Managing Interactions with the Contact
• **actions** - The actions that the template displays for this contact.
• **CPContactCallButton** - A button for calling the contact.
• **CPContactDirectionsButton** - A button for getting directions to the contact's location.
• **CPContactMessageButton** - A button that activates Siri and initiates the compose message flow.


---

# CPTextButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A button that displays a stylized title.

## API Reference

### Creating a Text Button
• **init(text:textStyle:handler:)** - Creates a text button with title, style, and handler.

### Managing the Button's Title and Style
• **text** - The button's text string.
• **textStyle** - The button's text style.
• **CPTextButtonStyle** - The styles that the text button applies to its text string.

### Deprecated
• **Deprecated Symbols** - Review unsupported symbols and their replacements.


---

# CPBarButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A button for placement in a navigation bar.

## API Reference

### Creating a Bar Button
• **init(title:handler:)** - Creates a bar button with a title string and a handler.
• **init(image:handler:)** - Creates a bar button with an image and a handler.
• **init(type:handler:)** - Creates a bar button with a button type and a handler.
• **CPBarButtonType** - The system button types you can assign to a bar button.

### Customizing the Bar Button
• **isEnabled** - A Boolean value that indicates whether the bar button is enabled.
• **image** - An image the bar button displays.
• **title** - A title the bar button displays.
• **buttonType** - The type of the bar button.


---

# CPButton

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 14.0, iPadOS 14.0, Mac Catalyst 14.0

## Overview
A button that displays an image.

## API Reference

### Creating a Button
• **init(image:handler:)** - Creates a button that displays an image and invokes a handler.

### Managing the Button's Image
• **image** - The image that the button displays.

### Managing the Button State
• **isEnabled** - A Boolean value that indicates whether the button is in an enabled state.


---

# CPAssistantCellConfiguration

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 15.0, iPadOS 15.0, Mac Catalyst 15.0

## Overview
An object that provides the configuration attributes for the assistant cell.

## API Reference

### Creating an Assistant Cell Configuration
• **init(position:visibility:assistantAction:)** - Creates a configuration object with the specified position, visibility, and action.

### Getting the Configuration Attributes
• **position** - The position of the assistant cell in the list template.
• **visibility** - The visibility of the assistant cell in the list template.
• **assistantAction** - The action that Siri performs when the user selects the assistant cell.
• **CPAssistantCellActionType** - The supported Siri actions of the assistant cell.
