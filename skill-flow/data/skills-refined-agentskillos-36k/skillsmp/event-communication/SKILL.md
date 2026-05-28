---
name: event-communication
description: Event bus patterns for GUTTERS modules. Use when modules need to communicate, react to cosmic events, or trigger synthesis updates via Redis pub/sub.
---

# Event Communication Pattern

Redis pub/sub event bus for module communication. Modules publish events, subscribe to events, no direct dependencies.

## Publishing Events
```python
from app.core.events import event_bus

await event_bus.publish(
    "cosmic.solar_storm.detected",
    {
        "kp_index": 8,
        "severity": "G4",
        "timestamp": datetime.now(UTC).isoformat(),
        "user_id": user_id  # or None for global
    }
)
```

## Subscribing (in module.initialize())
```python
class SolarModule(BaseModule):
    async def initialize(self):
        await super().initialize()
        
        # Subscribe to events
        event_bus.subscribe(
            "user.birth_data.updated",
            self.recalculate
        )
    
    async def recalculate(self, event_data: dict):
        """Triggered when user updates birth data."""
        user_id = event_data["user_id"]
        # Recalculate solar data for user
```

## Event Naming

Format: `{scope}.{entity}.{action}`

Examples:
- `cosmic.solar_storm.detected`
- `user.birth_data.updated`
- `module.profile.calculated`
- `synthesis.updated`

## Common Events
```python
# User events
"user.created"
"user.birth_data.updated"
"user.preferences.changed"

# Module events  
"module.profile.calculated"
"module.error"

# Cosmic events
"cosmic.solar_storm.detected"
"cosmic.full_moon"
"cosmic.transit.exact"

# Synthesis events
"synthesis.triggered"
"synthesis.completed"
```

## Event Data Structure
```python
{
    "event_type": "cosmic.solar_storm.detected",
    "user_id": "uuid-or-none",  # None = global event
    "data": {
        # Event-specific data
    },
    "timestamp": "2026-01-21T14:30:00Z",
    "module": "solar_tracking"  # Which module published
}
```

## Integration with Active Memory
```python
# Event triggers synthesis update
@event_bus.subscribe("cosmic.solar_storm.detected")
async def update_synthesis(event_data):
    # Update Active Working Memory
    await active_memory.invalidate_cache(user_id)
    # Trigger synthesis
    await synthesis_engine.generate(user_id)
```

## Critical Rules

- NEVER call modules directly (use events)
- Events are fire-and-forget (don't await responses)
- Keep event data minimal (IDs, not full objects)
- Log all events to `events_log` table