# VR Design Patterns

### Problem

Full VR lacks real-world context and can cause discomfort.

### Solution: User-Centered VR Design

**VR Environment Design:**

| Element | Guideline |
|---------|-----------|
| Ground plane | Always visible for orientation |
| Horizon | Stable, expected position |
| Scale | Human-scale or clearly different |
| Lighting | Consistent, comfortable |
| Boundaries | Guardian/chaperone visible |

**Locomotion Methods:**

| Method | Comfort | Use Case |
|--------|---------|----------|
| Teleportation | High | General movement |
| Walking (room-scale) | High | Limited area |
| Controller movement | Medium | Exploration |
| Vehicle/seat | High | Seated experiences |
| Flying | Low-Medium | Specific use cases |

**UI in VR:**
```
→ UI panels float in space
→ Part of environment or attached to user
→ Never lock to head directly (causes nausea)
→ Provide spatial audio feedback
→ Use gaze + confirm for selection
```
