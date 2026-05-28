---
name: ha-persistable-sensors
description: Build or modify Home Assistant sensors/entities that must persist native values and custom attributes across restarts using RestoreSensor/RestoreEntity plus ExtraStoredData (e.g., history, timestamps, scenarios); apply when persistence of non-native fields is required.
---

# Home Assistant Persistable Sensors

## Quick Start
- Inherit from `RestoreSensor` (or `RestoreEntity` for other domains).
- Define an `ExtraStoredData` subclass to capture custom fields; keep it JSON-serializable.
- In `async_added_to_hass`, hydrate via `async_get_last_extra_data()` before first state write.
- Override `extra_restore_state_data` to always return current native value + custom fields.
- Bound lists (e.g., 50 entries) and keep consistent ordering (newest-first recommended).
- After any mutation, call `async_write_ha_state()` so HA persists updated state.

## Template
```python
from homeassistant.components.sensor import RestoreSensor
from homeassistant.helpers.restore_state import ExtraStoredData

class MyExtraData(ExtraStoredData):
    def __init__(self, native_value: str | None, history: list[dict[str, Any]]):
        self.native_value = native_value
        self.history = history

    def as_dict(self) -> dict[str, Any]:
        return {"native_value": self.native_value, "history": self.history}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MyExtraData:
        history = data.get("history", []) if isinstance(data.get("history"), list) else []
        history = history[:50]  # bound size, newest-first expected
        return cls(data.get("native_value"), history)

class MyPersistableSensor(RestoreSensor):
    _attr_has_entity_name = True
    _attr_native_value: str | None = None

    def __init__(self) -> None:
        self._history: list[dict[str, Any]] = []

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (extra := await self.async_get_last_extra_data()) is not None:
            restored = MyExtraData.from_dict(extra.as_dict())
            self._attr_native_value = restored.native_value
            self._history = restored.history

    @property
    def extra_restore_state_data(self) -> MyExtraData:
        return MyExtraData(self._attr_native_value, self._history)

    def add_entry(self, entry: dict[str, Any]) -> None:
        self._history.insert(0, entry)
        self._history = self._history[:50]
        self._attr_native_value = entry.get("summary")
        self.async_write_ha_state()
```

## Checklist (Do/Verify)
- Set `_attr_has_entity_name = True` and stable `_attr_unique_id`.
- Keep properties lightweight; avoid I/O in getters.
- Clamp list sizes and prefer newest-first ordering.
- Serialize timestamps as ISO strings; parse in `from_dict`.
- Always return `extra_restore_state_data`, even when empty fields are possible (handle defaults in `from_dict`).
- Call `async_write_ha_state()` after updates to trigger persistence.

## Notes
- Use `RestoreEntity` if the platform is not a sensor; adapt imports accordingly.
- For large attribute payloads, consider moving bulky data to dedicated entities instead of attributes to reduce recorder load.