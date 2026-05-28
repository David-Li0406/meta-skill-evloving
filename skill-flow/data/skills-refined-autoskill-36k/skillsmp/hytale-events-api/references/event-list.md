# Hytale Events Reference

Complete reference for all event types in the Hytale server.

## Event System Overview

Hytale uses two event systems:

1. **General Event Bus** - Traditional publish/subscribe for server-wide events
2. **ECS Event System** - Entity Component System events for entities and world

---

## Player Events

### Connection Lifecycle

| Event | Type | Cancellable | Description |
|-------|------|-------------|-------------|
| `PlayerSetupConnectEvent` | IEvent | Yes | Player begins connecting (pre-auth) |
| `PlayerConnectEvent` | IEvent | No | Player successfully connected |
| `PlayerDisconnectEvent` | IEvent | No | Player disconnected |
| `PlayerSetupDisconnectEvent` | IEvent | No | Player disconnected during setup |
| `PlayerReadyEvent` | IEvent | No | Player ready to play |

### PlayerSetupConnectEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `username` | String | Player's username |
| `uuid` | UUID | Player's unique ID |
| `auth` | PlayerAuthentication | Auth data |
| `referralData` | byte[] | Server referral data |
| `reason` | String | Disconnect reason (settable) |

### PlayerConnectEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `holder` | Holder | Player entity holder |
| `playerRef` | PlayerRef | Player reference |
| `world` | World | Target world (settable) |

---

### World Transitions

| Event | Type | Cancellable | Description |
|-------|------|-------------|-------------|
| `AddPlayerToWorldEvent` | IEvent | No | Player added to world |
| `DrainPlayerFromWorldEvent` | IEvent | No | Player removed from world |

---

### Interactions

| Event | Type | Cancellable | Description |
|-------|------|-------------|-------------|
| `PlayerChatEvent` | IAsyncEvent | Yes | Player sends chat message |
| `PlayerInteractEvent` | IEvent | Yes | Player interacts (deprecated) |
| `PlayerMouseButtonEvent` | IEvent | Yes | Player presses mouse button |
| `PlayerMouseMotionEvent` | IEvent | Yes | Player moves mouse |
| `PlayerCraftEvent` | IEvent | No | Player crafts item (deprecated) |

### PlayerChatEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `sender` | PlayerRef | Message sender (settable) |
| `targets` | List | Recipients (settable) |
| `content` | String | Message text (settable) |
| `formatter` | Formatter | Message formatter (settable) |

---

## Entity Events

| Event | Type | Cancellable | Description |
|-------|------|-------------|-------------|
| `EntityRemoveEvent` | IEvent | No | Entity removed from world |
| `LivingEntityInventoryChangeEvent` | IEvent | No | Inventory changed |
| `LivingEntityUseBlockEvent` | IEvent | No | Entity uses block (deprecated) |

---

## ECS Block Events

All ECS block events are Entity Events (target specific entities).

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `BreakBlockEvent` | Yes | Entity breaks block |
| `PlaceBlockEvent` | Yes | Entity places block |
| `DamageBlockEvent` | Yes | Entity damages block (mining) |
| `UseBlockEvent.Pre` | Yes | Before block use |
| `UseBlockEvent.Post` | No | After block use |

### BreakBlockEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `itemInHand` | ItemStack | Tool used |
| `targetBlock` | Vector3i | Block position (settable) |
| `blockType` | BlockType | Type of block broken |

### PlaceBlockEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `itemInHand` | ItemStack | Item being placed |
| `targetBlock` | Vector3i | Placement position (settable) |
| `rotation` | RotationTuple | Block rotation (settable) |

### DamageBlockEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `targetBlock` | Vector3i | Block position |
| `blockType` | BlockType | Block type |
| `currentDamage` | float | Current damage level |
| `damage` | float | Damage to apply (settable) |

---

## ECS Item Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `DropItemEvent.Drop` | Yes | Entity drops item |
| `DropItemEvent.PlayerRequest` | Yes | Player requests drop |
| `InteractivelyPickupItemEvent` | Yes | Entity picks up item |
| `CraftRecipeEvent.Pre` | Yes | Before crafting |
| `CraftRecipeEvent.Post` | No | After crafting |

### DropItemEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `itemStack` | ItemStack | Item being dropped (settable) |
| `throwSpeed` | float | Throw velocity (settable) |

---

## ECS Player Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `ChangeGameModeEvent` | Yes | Game mode changes |
| `SwitchActiveSlotEvent` | Yes | Hotbar slot switches |
| `DiscoverZoneEvent.Display` | Yes | Zone discovery UI |
| `DiscoverInstanceEvent.Display` | Yes | Instance discovery UI |

### ChangeGameModeEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `gameMode` | GameMode | New game mode (settable) |

---

## Combat Events

### Damage Event

The primary damage event with extensive metadata support.

| Property | Type | Description |
|----------|------|-------------|
| `source` | Damage.Source | Damage source (settable) |
| `damageCauseIndex` | int | Cause index (settable) |
| `amount` | float | Damage amount (settable) |
| `initialAmount` | float | Original amount |

### Damage Meta Keys

| Key | Type | Description |
|-----|------|-------------|
| `HIT_LOCATION` | Vector4d | Hit position |
| `HIT_ANGLE` | Float | Hit angle |
| `IMPACT_PARTICLES` | Particles | Hit particles |
| `IMPACT_SOUND_EFFECT` | Sound | Hit sound |
| `CAMERA_EFFECT` | Effect | Camera shake |
| `DEATH_ICON` | String | Kill feed icon |
| `BLOCKED` | Boolean | Attack blocked |
| `KNOCKBACK_COMPONENT` | Component | Knockback data |

### Damage Sources

| Source Type | Description |
|-------------|-------------|
| `EntitySource` | Damage from entity |
| `ProjectileSource` | Damage from projectile |
| `EnvironmentSource` | Environmental damage |
| `CommandSource` | Command-inflicted damage |

### KillFeedEvent

| Subtype | Cancellable | Description |
|---------|-------------|-------------|
| `DecedentMessage` | Yes | Death message for victim |
| `KillerMessage` | Yes | Message for killer |
| `Display` | Yes | Kill feed display |

---

## World Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `ChunkSaveEvent` | Yes | Chunk being saved |
| `ChunkUnloadEvent` | Yes | Chunk being unloaded |
| `MoonPhaseChangeEvent` | No | Moon phase changed |

---

## Server Lifecycle Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `BootEvent` | No | Server boots up |
| `ShutdownEvent` | No | Server shuts down |
| `PrepareUniverseEvent` | No | Universe preparation (deprecated) |

### ShutdownEvent Priority Constants

```java
DISCONNECT_PLAYERS = -48
UNBIND_LISTENERS = -40
SHUTDOWN_WORLDS = -32
```

---

## Permission Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `PlayerPermissionChangeEvent.GroupAdded` | No | Player added to group |
| `PlayerPermissionChangeEvent.GroupRemoved` | No | Player removed from group |
| `PlayerPermissionChangeEvent.PermissionsAdded` | No | Permissions granted |
| `PlayerPermissionChangeEvent.PermissionsRemoved` | No | Permissions revoked |
| `GroupPermissionChangeEvent.Added` | No | Group permissions added |
| `GroupPermissionChangeEvent.Removed` | No | Group permissions removed |

---

## Plugin Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `PluginSetupEvent` | No | Plugin setup phase |

---

## Asset Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `LoadedAssetsEvent` | No | Assets loaded |
| `RemovedAssetsEvent` | No | Assets removed |
| `GenerateAssetsEvent` | No | Generate dynamic assets |
| `RegisterAssetStoreEvent` | No | Asset store registered |
| `RemoveAssetStoreEvent` | No | Asset store removed |
| `AssetStoreMonitorEvent` | No | Asset files changed |

### GenerateAssetsEvent Methods

```java
// Add generated child asset
addChildAsset(key, asset, parentKey)

// Add with multiple parents
addChildAsset(key, asset, parent1, parent2, ...)

// Add with cross-type reference
addChildAssetWithReference(key, asset, parentKey, referenceType)
```

---

## Prefab Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `PrefabPasteEvent` | Yes | Prefab pasted into world |
| `PrefabPlaceEntityEvent` | No | Entity placed from prefab |

---

## I18n Events

| Event | Cancellable | Description |
|-------|-------------|-------------|
| `MessagesUpdated` | No | Translations updated |
| `GenerateDefaultLanguageEvent` | No | Generate default translations |

---

## Event Priority Levels

| Priority | Value | Description |
|----------|-------|-------------|
| `FIRST` | -21844 | Executes first |
| `EARLY` | -10922 | Executes early |
| `NORMAL` | 0 | Default priority |
| `LATE` | 10922 | Executes late |
| `LAST` | 21844 | Executes last |

---

## Event Registration Examples

### General Event

```java
@Override
public void onEnable() {
    getEventBus().register(PlayerChatEvent.class, this::onChat);
}

private void onChat(PlayerChatEvent event) {
    if (event.getContent().contains("banned_word")) {
        event.setCancelled(true);
    }
}
```

### With Priority

```java
getEventBus().register(EventPriority.EARLY, PlayerChatEvent.class, event -> {
    // Process early
});
```

### Async Event

```java
getEventBus().registerAsync(PlayerChatEvent.class, future -> {
    return future.thenApply(event -> {
        // Async processing
        return event;
    });
});
```

### ECS Entity Event

```java
// Register for entity events
entityEventSystem.register(BreakBlockEvent.class, (holder, event) -> {
    BlockType type = event.getBlockType();
    // Handle block break
});
```

### ECS World Event

```java
// Register for world events
worldEventSystem.register(ChunkSaveEvent.class, (world, event) -> {
    WorldChunk chunk = event.getChunk();
    // Handle chunk save
});
```

---

## Source Files

- `com/hypixel/hytale/event/IEvent.java`
- `com/hypixel/hytale/event/IAsyncEvent.java`
- `com/hypixel/hytale/event/ICancellable.java`
- `com/hypixel/hytale/event/EventPriority.java`
- `com/hypixel/hytale/component/system/EcsEvent.java`
- `com/hypixel/hytale/server/core/event/events/player/*.java`
- `com/hypixel/hytale/server/core/event/events/entity/*.java`
- `com/hypixel/hytale/server/core/event/events/ecs/*.java`
- `com/hypixel/hytale/server/core/modules/entity/damage/Damage.java`
