# Board.Input.Debug Namespace

Debug visualization for touch input.

## Classes

- [BoardContactDebugView](#boardcontactdebugview)
- [BoardInputDebugView](#boardinputdebugview)

---

## BoardInputDebugView

Provides a mechanism to display debug information about Board input.

```csharp
public class BoardInputDebugView
```

**Inheritance:** `Object` → `BoardInputDebugView`

**Remarks:** Enable via `BoardInput.enableDebugView = true`. Only functions in Development builds.

**See Also:** [BoardInput.enableDebugView](Board.Input.md#enabledebugview)

---

## BoardContactDebugView

Provides a mechanism to display debug information about a BoardContact.

```csharp
public class BoardContactDebugView
```

**Inheritance:** `Object` → `BoardContactDebugView`

**Remarks:** Individual contact visualization within the debug overlay.

---

## See Also

- [Board.Input](Board.Input.md) - Touch input system
- [Board.Input.Simulation](Board.Input.Simulation.md) - Editor simulation
