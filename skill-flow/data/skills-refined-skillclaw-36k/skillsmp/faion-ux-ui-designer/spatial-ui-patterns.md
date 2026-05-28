# Spatial UI Patterns

### Problem

Traditional UI components don't work in 3D space.

### Solution: Spatial UI Components

**Panel Types:**

| Type | Behavior | Use Case |
|------|----------|----------|
| World-locked | Fixed in space | Reference content |
| Head-locked | Follows gaze | HUD, notifications |
| Body-locked | Follows position | Menus, tools |
| Hand-attached | On hand/wrist | Quick access |

**Window Management:**
```
→ Multiple floating windows
→ Snap to surfaces
→ Group related windows
→ Minimize to dock
→ Spatial memory (return to position)
```

**Best Practices:**
```
DO:
→ Provide visual anchors
→ Maintain consistent scale
→ Use depth for hierarchy
→ Respect personal space

DON'T:
→ Place UI too close to face
→ Require constant arm raising
→ Use tiny touch targets
→ Ignore field of view limits
```
