# Api Reference

Core API classes and controllers for managing CarPlay interfaces.


---

# CPInterfaceController

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A controller that manages the templates for constructing a scene's user interface.

## API Reference

### Configuring the Interface Controller
• **delegate** - An object that serves as the delegate to the interface controller.
• **CPInterfaceControllerDelegate** - The interface that an object implements to serve as a delegate to an interface controller.
• **prefersDarkUserInterfaceStyle** - A Boolean value that determines whether the system draws the user interface in Dark Mode.
• **setRootTemplate(_:animated:completion:)** - Sets the root template of the navigation hierarchy.

### Accessing the Trait Collection
• **carTraitCollection** - The trait collection of the vehicle's primary screen.

### Accessing Templates
• **rootTemplate** - The root template in the navigation hierarchy.
• **topTemplate** - The top-most template in the navigation hierarchy.
• **templates** - The contents of the navigation hierarchy.

### Adding and Removing Templates
• **pushTemplate(_:animated:completion:)** - Adds the specified template to the navigation hierarchy and displays it.
• **popTemplate(animated:completion:)** - Removes the top-most template from the navigation hierarchy.
• **popToRootTemplate(animated:completion:)** - Removes all of the templates from the navigation hierarchy except the root template.
• **pop(to:animated:completion:)** - Removes each template from the navigation hierarchy until the specified template becomes visible.

### Displaying Templates Modally
• **presentTemplate(_:animated:completion:)** - Presents a template modally.
• **dismissTemplate(animated:completion:)** - Dismisses a modal template.
• **presentedTemplate** - The interface controller's current modal template.

### Deprecated
• **Deprecated Symbols** - Review unsupported symbols and their replacements.


---

# CPWindow

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 12.0, iPadOS 12.0, Mac Catalyst 13.1

## Overview
A window for displaying content on the CarPlay screen.

## API Reference

### Creating a Window
• **init(templateApplicationScene:)** - Creates a window that corresponds with the provided scene.

### Getting the Map Button Safe Area
• **mapButtonSafeAreaLayoutGuide** - The layout guide for the map button safe area.


---

# CPTemplateApplicationScene

**Technology:** CarPlay
**Type:** class
**Platforms:** iOS 13.0, iPadOS 13.0, Mac Catalyst 13.1

## Overview
A scene for managing CarPlay app user interfaces.

## API Reference

### Managing the Activation State
• **activationState** - The activation state of the scene.
• **UIScene.ActivationState** - Constants that indicate the execution state of an app scene.

### Managing the Scene Delegate
• **delegate** - The object that acts as the delegate of the template application scene.
• **CPTemplateApplicationSceneDelegate** - The methods for handling events that affect the scene, including a CarPlay connection and disconnection.

### Managing the Scene Session
• **session** - The session object for the scene.
• **UISceneSession** - An object that contains information about one of your app's scenes.

### Managing the Interface Controller
• **interfaceController** - The interface controller for managing templates.
• **CPInterfaceController** - A controller that manages the templates for constructing a scene's user interface.

### Managing the Car Window
• **carWindow** - The window the system displays on the car's screen.
• **CPWindow** - A window for displaying content on the CarPlay screen.

### Getting Content Style
• **contentStyle** - The current interface style for the content displayed by the template app.
• **CPContentStyle** - The interface styles for content that a template app displays.
