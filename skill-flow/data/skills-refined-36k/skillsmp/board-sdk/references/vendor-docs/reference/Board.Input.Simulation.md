# Board.Input.Simulation Namespace

Editor simulation tools for testing touch input without hardware.

## Classes

- [BoardContactSimulation](#boardcontactsimulation)
- [BoardContactSimulationIcon](#boardcontactsimulationicon)
- [BoardContactSimulationSettings](#boardcontactsimulationsettings)
- [BoardSimulationContact](#boardsimulationcontact)

## Structs

- [BoardContactSimulation.InputActionReferenceState](#boardcontactsimulationinputactionreferencestate)

---

## BoardContactSimulation

Provides a mechanism to simulate input on a Board device in the Unity Editor.

```csharp
public class BoardContactSimulation
```

**Inheritance:** `Object` → `BoardContactSimulation`

**Remarks:** Access via Unity menu: Board > Input > Simulator

### Key Features

- Place, move, touch, lift, and rotate virtual Pieces
- Simulate finger touches
- Test with up to 1000 simultaneous contacts
- Generates identical BoardContact events as real hardware

---

## BoardContactSimulationIcon

Represents an icon used for Board input simulation.

```csharp
public class BoardContactSimulationIcon : ScriptableObject
```

**Inheritance:** `ScriptableObject` → `BoardContactSimulationIcon`

**Remarks:** Create via: Create > Board > Simulation > Icon

### Properties

- Display Name - Name shown in simulator palette
- Contact Type - Finger or Glyph
- Glyph ID - Which Piece this represents (Glyph type only)
- Sprite - Visual for the icon
- Size - Render size relative to 1920×1080
- Alpha Hit Test Minimum Threshold - Minimum alpha for click detection

---

## BoardContactSimulationSettings

Encapsulates settings for Board input simulation.

```csharp
public class BoardContactSimulationSettings : ScriptableObject
```

**Inheritance:** `ScriptableObject` → `BoardContactSimulationSettings`

**Remarks:** Access via: Edit > Project Settings > Board > Simulation Settings

### Settings Categories

#### Input Controls

- Touch - Left mouse button (hold)
- Place - Left click
- Lift - Left click on contact
- Cancel - Escape
- Snap Rotate CW/CCW - +/- keys
- Rotate - Scroll wheel
- Fast Rotate - Shift + scroll

#### Appearance

- Icon outline colors and thickness
- Lifted icon appearance
- Touched icon appearance
- Shadow effects

#### Rotation

- Snap rotation degrees
- Rotation speed
- Fast rotation speed modifier

---

## BoardSimulationContact

Represents a visual representation of a simulated BoardContact.

```csharp
public class BoardSimulationContact
```

**Inheritance:** `Object` → `BoardSimulationContact`

**Remarks:** Runtime representation of simulated contacts in the Game view.

---

## BoardContactSimulation.InputActionReferenceState

Encapsulates state information for Input System action references.

```csharp
public struct BoardContactSimulation.InputActionReferenceState
```

**Remarks:** Used internally by [BoardContactSimulationSettings](#boardcontactsimulationsettings) to manage references to `UnityEngine.InputSystem.InputAction` assets. Tracks the enabled/disabled state of input actions used by the simulator.

### Properties

#### actionReference

Gets the Input System action reference.

```csharp
public InputActionReference actionReference { get; }
```

**Type:** `InputActionReference`

---

#### wasEnabled

Gets whether the action was enabled before simulation started.

```csharp
public bool wasEnabled { get; }
```

**Type:** `bool`

**Remarks:** Used to restore the original state when simulation ends.

---

## See Also

- [Board.Input](Board.Input.md) - Touch input system
- [Simulator Guide](../guides/simulator.md) - Complete simulation guide
