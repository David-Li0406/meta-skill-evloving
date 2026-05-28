# Networking in Udon

In Udon, objects with `UdonBehavior` or `UdonSharpBehavior` that are network-synced have the concept of an `Owner`.
In VRChat, the player called the `Owner` is responsible for syncing that object’s data. The `Owner` keeps the master data and sends it to other clients that are not the `Owner`.
Only the `Owner` can modify synced data. Non-owners can only read it.

## Owner lookup

To get the owner of a specific GameObject, use:
`VRCPlayerAPI Networking.GetOwner(GameObject obj)`

To check whether the local player is the owner, use:
`bool Networking.IsOwner(VRCPlayerApi player, GameObject obj)`

To transfer ownership to a specific player, use:
`Networking.SetOwner(VRCPlayerApi player, GameObject obj)`

When ownership is transferred, the following callback is invoked:

```cs
public void override OnOwnershipTransferred(VRCPlayerApi player)
{
    Debug.Log($"Ownership Transferred {player.displayName}");
}
```

When `SetOwner` is called, the previous owner receives a callback to approve or deny the request:

```cs
public bool override OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner)
{
    return true;
}
```

## Sync modes

Sync mode determines how data is synchronized. In UdonSharp, set the `UdonBehaviorSyncMode` attribute on a class that inherits `UdonSharpBehavior`.

```cs
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Example : UdonSharpBehaviour 
{ 
}
```

`UdonSharp.BehaviourSyncMode`

|Name|Summary|
|---|---|
|None|Enforces no synced variables on the behaviour and hides the selection dropdown in the UI for the sync mode. Nothing is synced and SendCustomNetworkEvent will not work on the behaviour.|
|Continuous|Synced variables will be updated automatically at a very frequent rate, but may not always reliably update to save bandwidth.|
|Manual|Synced variables are updated manually by the user less frequently, but ensures that updates are reliable when requested.|
|NoVariableSync|Enforces that there are no synced variables on the behaviour, hides the sync mode selection dropdown, and allows you to use the behaviours on GameObjects that use either Manual or Continuous sync.|

For performance reasons, use `Manual` whenever possible. Use `Continuous` only when you need frequent updates such as position syncing with interpolation.

## Synced variables

Synced variables are the parameters on an `UdonBehavior` component that are actually synchronized.
In UdonSharp, declare them with the `UdonSynced` attribute.

```cs
[UdonSynced]
public bool synchronizedBoolean;

[UdonSynced(UdonSyncMode.Linear)]
public float synchronizedFloat;
```

Available `UdonSyncMode` options:

|Name|Summary|
|---|---|
|NotSynced||
|None|No interpolation (Default)|
|Linear|Lerp|
|Smooth|Some kind of smoothed syncing|

`Linear` and `Smooth` only take effect when the sync mode is `Continuous`. With `Manual`, use `None` in most cases.

### Supported synced types

#### Boolean types
| Type | Size    |
| ---- | ------- |
| bool | 1 byte  |
#### Integral numeric types
| Type   | Range                           | Size    |
|--------|---------------------------------|---------|
| sbyte  | -128 to 127                     | 1 byte  |
| byte   | 0 to 255                        | 1 byte  |
| short  | -32,768 to 32,767               | 2 bytes |
| ushort | 0 to 65,535                     | 2 bytes |
| int    | -2,147,483,648 to 2,147,483,647 | 4 bytes |
| uint   | 0 to 4,294,967,295              | 4 bytes |
| long   | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | 8 bytes |
| ulong  | 0 to 18,446,744,073,709,551,615 | 8 bytes |
#### Floating-point numeric types
| Type   | Approximate range             | Precision     | Size    |
|--------|-------------------------------|---------------|---------|
| float  | ±1.5 x 10^(−45) to ±3.4 x 10^(38)   | ~6-9 digits   | 4 bytes |
| double | ±5.0 × 10^(−324) to ±1.7 × 10^(308) | ~15-17 digits | 8 bytes |
#### Vector mathematics types and structures (Unity)
| Type        | Range         | Size     |
|-------------|---------------|----------|
| Vector2   | same as float | 8 bytes  |
| Vector3   | same as float | 12 bytes  |
| Vector4   | same as float | 16 bytes |
| Quaternion| same as float | 16 bytes  |
#### Color structures
| Type     | Range / Precision | Size    |
|----------|-------------------|---------|
| Color  | same as float     | 16 bytes |
| Color32| same as byte      | 4 bytes |
#### Text types and structures
| Type   | Range            | Size           |
|--------|------------------|----------------|
| char   | U+0000 to U+FFFF | 2 bytes        |
| string | same as char     | 2 bytes / char |
#### Other structures
| Type   | Range            | Size           |
|--------|------------------|----------------|
| VRCUrl | U+0000 to U+FFFF | 2 bytes / char |

### Synced arrays

You can also sync arrays of the above types.
Only one-dimensional arrays are supported; jagged arrays are not synced.
Arrays must be initialized with `new`, even if the length is 0.

## Manual sync of synced variables

If the sync mode is `Manual`, the owner must explicitly request sync.
Calling this as a non-owner has no effect.

```cs
RequestSerialization();
```

When a sync is requested, the owner receives these callbacks in order:

```cs
public override void OnPreSerialization()
{
    Debug.Log("Processing before data transfer");
}
```

```cs
public override void OnPostSerialization(VRC.Udon.Common.SerializationResult result)
{
    Debug.Log("Processing after data transfer");
}
```

On non-owners, the following callback is invoked:
```cs
public override void OnDeserialization()
{
    Debug.Log("Received synced data");
}
```
When this is called, synced variables are updated to the received values.

## FieldChangeCallback

`OnDeserialization()` fires for changes to all synced variables in the class.
To react only to a specific synced variable, use `FieldChangeCallback`:

```cs
[UdonSynced, FieldChangeCallback(nameof(SyncedToggle))]
private bool _syncedToggle;

public bool SyncedToggle
{
    set
    {
        Debug.Log("toggling the object...");
        _syncedToggle = value;
        toggleObject.SetActive(value);
    }
    get => _syncedToggle;
}
```

This callback fires even for the owner (unlike `OnDeserialization()`).

Note: For arrays, this callback does not fire when elements change. It only fires when the array object itself changes.

## SendCustomNetworkEvent

`SendCustomNetworkEvent` executes a function across the network without using synced variables.
It can only target public functions.

```cs

public Function()
{
    Debug.Log("Show All Player!");
}


SendCustomNetworkEvent(NetworkEventTarget.All, nameof(Function));


```

`NetworkEventTarget` specifies who executes the function.

|Name|Summary|
|---|---|
|All|All players in the instance|
|Owner|Owner of the game object|
|Others|All players except yourself|
|Self|Only yourself|

This is mainly used for simultaneous, temporary events like sounds or effects.
It is not appropriate for state changes that must persist. Use synced variables for state changes.

You can also pass arguments by using the `NetworkCallable` attribute.

```cs
void Start()
{
    SendCustomNetworkEvent(NetworkEventTarget.All, nameof(Greet), "hogehoge");
}

[NetworkCallable]
public void Greet(string name)
{
    Debug.Log(name + " さん、こんにちは！");
}

```

## Designing network logic

### Reduce sync frequency as much as possible

High-frequency sync can hit bandwidth limits and cause backlog.
For example, instead of syncing remaining time every second, sync the time when the timer ends. Then show the remaining time by comparing with local time. This reduces sync to a single transmission.

### Choosing between SendCustomNetworkEvent and synced variables

Decide based on whether late-joining players must see the result.

For example, sounds and effects that trigger at the same time do not need to play for late joiners, so use `SendCustomNetworkEvent`.

Conversely, game state or object positions that must be reproduced for late joiners should be implemented with synced variables.
