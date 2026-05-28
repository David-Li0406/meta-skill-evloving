# Implementation (Practice)

This page summarizes design decisions and callback usage needed for implementation.

## 1. Choosing a sync mode

Specify the sync mode with `UdonBehaviourSyncMode`.

- `Manual`: Explicit syncing. **Recommended in most cases.**
- `Continuous`: Only when you need frequent updates like position interpolation.
- `None`: No synced variables are expected.
- `NoVariableSync`: No synced variables; only `SendCustomNetworkEvent`.

```cs
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Example : UdonSharpBehaviour { }
```

## 2. State sync vs temporary events

- **State must persist** → use `UdonSynced`
- **Temporary effects/sounds** → use `SendCustomNetworkEvent`

## 3. Ownership transfer and callbacks

Callbacks for ownership changes:

```cs
public override void OnOwnershipTransferred(VRCPlayerApi player)
{
    // Process when ownership changes
}
```

```cs
public override bool OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner)
{
    // Return true to allow the change
    return true;
}
```

## 4. Serialization hooks

You can hook into sync send/receive timing:

```cs
public override void OnPreSerialization()
{
    // Before sending
}

public override void OnPostSerialization(VRC.Udon.Common.SerializationResult result)
{
    // After sending
}

public override void OnDeserialization()
{
    // After receiving
}
```

## 5. Typical implementation flow

1. Check `IsOwner` before making changes
2. If needed, call `SetOwner` to acquire ownership
3. Update synced variables
4. Call `RequestSerialization()` to send updates
