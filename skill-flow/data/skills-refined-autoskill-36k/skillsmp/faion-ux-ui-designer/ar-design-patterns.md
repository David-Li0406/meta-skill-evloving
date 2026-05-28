# AR Design Patterns

### Problem

AR must blend seamlessly with the real world.

### Solution: Context-Aware AR Design

**AR Use Cases:**

| Use Case | Pattern |
|----------|---------|
| Navigation | Ground-level overlays, arrows |
| Shopping | Product visualization at scale |
| Training | Step-by-step guidance |
| Collaboration | Shared annotations |
| Information | Contextual labels, data |

**Placement Strategies:**
```
Surface detection:
→ Tables, floors, walls
→ Content snaps to surfaces
→ Respect physical boundaries

Object recognition:
→ Attach to real objects
→ Scale appropriately
→ Update with movement
```

**Design Principles:**
```
→ Respect the real environment
→ Use lighting to integrate
→ Don't occlude important reality
→ Provide clear virtual/real distinction
→ Allow environment scanning
```
