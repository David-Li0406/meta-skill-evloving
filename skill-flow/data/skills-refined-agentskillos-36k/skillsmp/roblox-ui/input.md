# Input Reference

## Contents
- [Gamepad input](#gamepad-input)
- [Input](#input)
- [Input Action System](#input-action-system)
- [Mobile input](#mobile-input)
- [Mouse and keyboard input](#mouse-and-keyboard-input)

---

## Gamepad input

import ControllerEmulator from '../includes/studio/controller-emulator.md'

Roblox accepts input from gamepads such as Xbox and PlayStation controllers. To simplify [cross‑platform](../projects/cross-platform.md) inputs, including gamepads, Roblox provides the [Input Action System](../input/input-action-system.md) to define **actions** such as "jump," "sprint," or "shoot" and set up **bindings** for multiple hardware inputs to drive those actions.

When binding gamepad inputs, see [common control schemas](#common-control-schemas) to create a consistent gamepad experience for players. After inputs are set, you can enhance the player's experience by including [haptic feedback](#haptic-feedback) on supported controllers.

As you build out support for gamepads, remember to test frequently using a connected gamepad or the [Controller&nbsp;Emulator](#controller-emulation) in Studio.

## Input type detection

In cross‑platform development, it's important that you determine and respond to the `Class.UserInputService.PreferredInput|PreferredInput` type a player is using, normally to ensure that [UI&nbsp;elements](../ui/index.md#ui-objects) like on-screen buttons and menus work elegantly and support interaction across devices.

For example, a console assumes that gamepads are the default input, but a player on PC or laptop may also choose to connect a bluetooth gamepad. In this case, mouse/keyboard remains a valid input for that player, but you can assume they want to switch to the connected gamepad as the **primary** input type.

See [input type detection](./index.md#input-type-detection) for more information.

<Alert severity="info">
For alternative gamepad detection methods, see the `Class.UserInputService.GamepadEnabled` property and the `Class.UserInputService.GamepadConnected|GamepadConnected`/`Class.UserInputService.GamepadDisconnected|GamepadDisconnected` events.
</Alert>

## Common control schemas

When considering specific control bindings for the [Input Action Syst

[Content truncated - see full docs]

---

## Input

import DefaultBindings from '../includes/default-bindings.md'

Every experience needs to receive user input for players to interact and view their environment. Roblox supports nearly all forms of input, including [mouse/keyboard](../input/mouse-and-keyboard.md), [touch](../input/mobile.md), [gamepads](../input/gamepad.md), and VR.

## Cross-platform input

Roblox is inherently [cross‑platform](../projects/cross-platform.md), as players can discover and join experiences on their phone or tablet, then later continue where they left off on their PC or console. Input is especially important as part of your cross‑platform development plan.

To simplify this process, Roblox provides the [Input Action System](../input/input-action-system.md) to define **actions** such as "jump," "sprint," or "shoot" and set up **bindings** for multiple hardware inputs to drive those actions. This frees you from thinking of all the technical aspects of hardware inputs and allows you to simply define which inputs perform which actions.

<img src="../assets/publishing/cross-platform/Input-Actions-Jump.png" />

## Input type detection

In cross‑platform development, it's important that you determine and respond to the **primary** input type a player is using, normally to ensure that [UI&nbsp;elements](../ui/index.md#ui-objects) like on‑screen buttons and menus work elegantly across devices.

For example, a touch‑enabled device assumes touch is the default input and that touch buttons may appear for actions, but if a player connects an additional bluetooth keyboard/mouse or gamepad, you can assume they want to switch to that as the **primary** input type and possibly use touch as a backup input for on‑screen UI. The read‑only `Class.UserInputService.PreferredInput` property is a convenient way to test for and adapt to multiple input types across multiple device types, based on anticipated player behavior.

<Tabs>
<TabItem label="Behavior">
The value of `Class.UserInputService.PreferredInput|Pre

[Content truncated - see full docs]

---

## Input Action System

import DefaultBindings from '../includes/default-bindings.md'

The cross-platform **Input Action System** lets you connect [actions](#input-actions) and arrange [bindings](#input-bindings) across various hardware inputs at edit time. Combined with [contexts](#input-contexts), you can easily configure and edit a modular input system that works on any device in any phase of play. Use cases include:

- A first-person shooter system with actions dynamically swapping in and out depending on if the player is in battle mode or spectator mode.
- A comprehensive driving system equipped with acceleration/deceleration, car boosters, and refuel stations.
- Hotkeys for an abilities system in a fighting game to swap out moves seamlessly without players missing a punch.

## Input contexts

An `Class.InputContext` is a collection of actions which holds related [input actions](#input-actions), for example `PlayContext` for in‑experience character controls and `NavContext` for controls to navigate around UI menus. You can enable or disable contexts (and their corresponding actions) through their `Class.InputContext.Enabled|Enabled` property, such as to enable the `NavContext` when an inventory menu is open and then change to the `PlayContext` when the player closes the menu and returns to primary gameplay.

Even if an experience may not use multiple input contexts initially, best practice is to create a primary context at the top level of any input system, for example the `PlayContext` instance for input that occurs during gameplay.

1. Insert a new `Class.InputContext` into `Class.StarterGui`.
2. Rename it to `PlayContext`.

   <img src="../assets/studio/explorer/StarterGui-InputContext.png" width="320" alt="New InputContext instance inside StarterGui, renamed to PlayContext" />

## Input actions

An `Class.InputAction` defines a gameplay action mechanic such as "Jump," "Sprint," or "Shoot." These actions are then mapped to hardware inputs using [input bindings](#input-bindings).

A

[Content truncated - see full docs]

---

## Mobile input

The majority of Roblox sessions are played on mobile devices, so it's important to consider the mobile [device orientation](#device-orientation) and other [cross‑platform](../projects/cross-platform.md) factors when designing an experience for a wide audience.

To simplify cross‑platform inputs, including player interaction with virtual buttons, Roblox provides the [Input Action System](../input/input-action-system.md) to define **actions** such as "jump," "sprint," or "shoot" and set up **bindings** for multiple hardware inputs to drive those actions.

Roblox also supports native mobile features like [haptic feedback](#haptic-feedback), touch gestures such as `Class.UserInputService.TouchSwipe|TouchSwipe` and `Class.UserInputService.TouchPinch|TouchPinch`, or accelerometer and gyroscope functionality on `Class.UserInputService.AccelerometerEnabled|AccelerometerEnabled` and `Class.UserInputService.GyroscopeEnabled|GyroscopeEnabled` devices.

## Input type detection

In cross‑platform development, it's important that you determine and respond to the `Class.UserInputService.PreferredInput|PreferredInput` type a player is using, normally to ensure that [UI&nbsp;elements](../ui/index.md#ui-objects) like on-screen buttons and menus work elegantly and support interaction across devices.

For example, a touch-enabled device assumes touch is the default input and that touch-buttons may appear for actions, but a player may choose to connect a bluetooth gamepad. In this case, touch remains a valid input, but you can assume the player wants to switch to the connected gamepad as the **primary** input type and possibly use touch as a backup input for on-screen UI.

See [input type detection](./index.md#input-type-detection) for more information.

## Device orientation

By default, Roblox experiences run in **landscape** mode, allowing the experience to switch between landscape "left" and landscape "right" as the player's device rotates. However, experiences can be locked to a pa

[Content truncated - see full docs]

---

## Mouse and keyboard input

A large percentage of Roblox sessions are played on devices with a mouse and keyboard, so it's important to support these inputs when designing an experience for a wide audience.

To simplify [cross‑platform](../projects/cross-platform.md) inputs, including mouse/keyboard, Roblox provides the [Input Action System](../input/input-action-system.md) to define **actions** such as "jump," "sprint," or "shoot" and set up **bindings** for multiple hardware inputs to drive those actions.

Roblox also supports general mouse/keyboard input through `Class.UserInputService` events like `Class.UserInputService.InputBegan|InputBegan` and `Class.UserInputService.InputEnded|InputEnded` and methods like `Class.UserInputService:IsKeyDown()|IsKeyDown()` to check if a particular key is pressed on a keyboard.

## Input type detection

In cross‑platform development, it's important that you determine and respond to the `Class.UserInputService.PreferredInput|PreferredInput` type a player is using, normally to ensure that [UI&nbsp;elements](../ui/index.md#ui-objects) like on-screen buttons and menus work elegantly and support interaction across devices.

For example, a PC or laptop assumes mouse/keyboard is the default input, but a player may choose to connect a bluetooth gamepad. In this case, mouse/keyboard remains a valid input, but you can assume the player wants to switch to the connected gamepad as the **primary** input type.

See [input type detection](./index.md#input-type-detection) for more information.

## Generic mouse/key input

Beyond the [Input Action System](../input/input-action-system.md), you can capture mouse and keyboard inputs using `Class.UserInputService`. The following `Class.LocalScript`, when placed in `Class.StarterPlayerScripts`, captures the began and ended phases of key and mouse clicks and prints the result to the [Output](../studio/output.md) window.

```lua title="LocalScript - Output Key/Mouse Began and Ended"
local UserInputService = game:GetService("User

[Content truncated - see full docs]

---

