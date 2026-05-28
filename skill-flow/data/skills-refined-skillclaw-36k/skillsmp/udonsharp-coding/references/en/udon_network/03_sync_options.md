# Supplement: Sync Options / Callbacks

This page contains supplemental information for implementation.

## 1. UdonSyncMode (interpolation)

`UdonSyncMode` is mainly effective with `Continuous`.

- `None`: no interpolation (default)
- `Linear`: linear interpolation (Lerp)
- `Smooth`: smoothed interpolation

```cs
[UdonSynced(UdonSyncMode.Linear)]
public float synchronizedFloat;
```

## 2. FieldChangeCallback

Use this when you want to react only to a specific synced variable.

```cs
[UdonSynced, FieldChangeCallback(nameof(SyncedToggle))]
private bool _syncedToggle;

public bool SyncedToggle
{
    set
    {
        _syncedToggle = value;
        toggleObject.SetActive(value);
    }
    get => _syncedToggle;
}
```

### Notes

- This does **not** fire when array elements change.
- It only fires when the array object itself changes.
