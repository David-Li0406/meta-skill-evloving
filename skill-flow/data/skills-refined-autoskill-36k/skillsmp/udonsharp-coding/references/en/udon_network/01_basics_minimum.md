# Minimum Implementation (Required)

This page lists only the minimum information required to implement networking.

## 1. Owner basics

- Network-synced objects have an `Owner`.
- Only the **Owner** can modify synced data. Non-owners are read-only.

## 2. Minimum Owner APIs

- Get owner: `Networking.GetOwner(GameObject obj)`
- Check owner: `Networking.IsOwner(VRCPlayerApi player, GameObject obj)`
- Set owner: `Networking.SetOwner(VRCPlayerApi player, GameObject obj)`

## 3. Defining synced variables

- Add `[UdonSynced]` to fields that should be synchronized.
- For syncing, use **Manual** with `UdonBehaviourSyncMode` as the baseline.

```cs
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Example : UdonSharpBehaviour
{
    [UdonSynced]
    public bool synchronizedFlag;
}
```

## 4. Manual sync flow (shortest)

- The Owner calls `RequestSerialization()` to send sync data.
- Non-owners receive `OnDeserialization()` and apply the new values.

```cs
public override void OnDeserialization()
{
    // Process after receiving synced data
}
```

## 5. Syncing temporary events

- Use `SendCustomNetworkEvent` for temporary events that don’t need to persist.
- Only public methods can be invoked.

```cs
public void PlayEffect()
{
    // Play effect, etc.
}

SendCustomNetworkEvent(NetworkEventTarget.All, nameof(PlayEffect));
```

## 6. Minimum checklist

- [ ] Only the `Owner` changes synced data
- [ ] Synced fields are marked with `[UdonSynced]`
- [ ] `Manual` sync uses `RequestSerialization()`
- [ ] Temporary events use `SendCustomNetworkEvent`
