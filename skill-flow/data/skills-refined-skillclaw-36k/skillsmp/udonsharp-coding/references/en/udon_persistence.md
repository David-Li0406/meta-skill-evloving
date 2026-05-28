# Udon Persistence

VRChat's Persistence feature allows you to save player-specific data in your world and retain it across sessions. This makes it possible to carry over high scores, inventories, settings, etc., to the next visit.

There are two main methods for persistence: **PlayerData** and **PlayerObject**.

## PlayerData

**PlayerData** is a simple database that stores data as key-value pairs for each player.

### Basic Usage

You use the static methods of the `VRC.SDK3.Persistence.PlayerData` class to read and write data.

**Saving Data:**
Use `PlayerData.SetType(key, value)`. Saving is done for the local player.

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Persistence;
using VRC.SDKBase;

public class ScoreSaver : UdonSharpBehaviour
{
    public void SaveScore(int score)
    {
        // Save an integer value to the key "playerScore"
        PlayerData.SetInt("playerScore", score);
        Debug.Log("Saved score: " + score);
    }
}
```

**Loading Data:**
Use `PlayerData.GetType(player, key)`. You must wait for the `OnPlayerRestored` event, which indicates that the data has been loaded, before attempting to read it.

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Persistence;
using VRC.SDKBase;

public class ScoreLoader : UdonSharpBehaviour
{
    private const string ScoreKey = "playerScore";

    // Event called after a player's persistent data has been loaded
    public override void OnPlayerRestored(VRCPlayerApi player)
    {
        if (player.isLocal)
        {
            if (PlayerData.HasKey(player, ScoreKey))
            {
                int loadedScore = PlayerData.GetInt(player, ScoreKey);
                Debug.Log($"Loaded score: {loadedScore}");
            }
            else
            {
                Debug.Log("No saved score found.");
            }
        }
    }
}
```

### Supported Data Types
Major types such as `Int`, `Float`, `String`, `Bool`, `Byte`, `Color`, `Vector2`, `Vector3`, `Vector4`, and `Quaternion` are supported.

## PlayerObject

**PlayerObject** is a GameObject that is automatically instantiated when a player joins. Synced variables (`[UdonSynced]`) on UdonBehaviours attached to this object can be persisted. This is suitable for saving data with complex structures, such as inventory contents.

### Setup Steps

1.  Create a GameObject in the scene and attach the `VRCPlayerObject` component to it.
2.  Attach an `UdonBehaviour` to that GameObject (or a child) and define synced variables (`[UdonSynced]`).
3.  Attach the `VRCEnablePersistence` component to the same GameObject as the `UdonBehaviour` whose variables you want to persist.
4.  You may need to register this object as a PlayerObject in the scene descriptor (VRCSceneDescriptor), etc. (Note: Current SDK specifications may handle this automatically in some cases, but please check the documentation). Generally, you make the created object a prefab and specify it in the scene management component.

### Confirming Data Load

For PlayerObjects as well, use the `OnPlayerRestored` event to know when the data has been restored.

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class InventoryPersistence : UdonSharpBehaviour
{
    [UdonSynced]
    public int[] inventoryItemIds;

    public override void OnPlayerRestored(VRCPlayerApi player)
    {
        // Data for the owner of this object (the corresponding player) has been restored
        if (Networking.GetOwner(gameObject) == player)
        {
            Debug.Log("Inventory data restored.");
            // Perform processing using the restored inventoryItemIds
        }
    }
}
```

### Getting PlayerObjects

To get the PlayerObjects associated with a specific player, use `Networking.GetPlayerObjects(player)`.

```csharp
public void FindPlayerObject(VRCPlayerApi player)
{
    GameObject[] objects = Networking.GetPlayerObjects(player);
    foreach (var obj in objects)
    {
        // Search for a specific component, etc.
        var inventory = obj.GetComponent<InventoryPersistence>();
        if (inventory != null)
        {
            Debug.Log($"Found inventory for {player.displayName}.");
        }
    }
}
```

## Notes and Best Practices

1.  **Wait for OnPlayerRestored**: Always ensure you read or write data after the `OnPlayerRestored` event has fired. Accessing it before this may result in reading/writing old data or default values.
2.  **Storage Limits**: Both PlayerData and PlayerObject have a limit of **100KB** per player.
3.  **Key Naming (PlayerData)**: PlayerData shares a key space across the entire world. It is recommended to add a prefix to keys to avoid collisions with other gimmicks (e.g., `MySystem_Score`, `AuthorName_Setting_Volume`).
4.  **Save Timing**: You cannot save data immediately before a player leaves the world (`OnPlayerLeft`). Save data whenever it changes or periodically.
5.  **PlayerObject vs PlayerData**:
    *   **PlayerData**: Suitable for simple numerical or string settings (scores, option settings, etc.).
    *   **PlayerObject**: Suitable for objects with complex states or data that needs synchronization (equipped items, etc.). PlayerObjects are synced individually, which also leads to bandwidth savings.

## References
*   [Persistence (VRChat Creators)](https://creators.vrchat.com/worlds/udon/persistence/)
*   [PlayerData](https://creators.vrchat.com/worlds/udon/persistence/player-data)
*   [PlayerObject](https://creators.vrchat.com/worlds/udon/persistence/player-object)
