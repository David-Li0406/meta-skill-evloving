# Hytale ECS Events Reference

Detailed reference for the Entity Component System event architecture.

## ECS Event Architecture

ECS events operate differently from general events:
- **Entity Events**: Target specific entity holders
- **World Events**: Target the entire world
- Events flow through ECS systems, not traditional event bus

---

## ECS Event Base Classes

### EcsEvent

Base class for all ECS events.

```java
abstract class EcsEvent {
    // Base event, no fields
}
```

### CancellableEcsEvent

Extends EcsEvent with cancellation support.

```java
abstract class CancellableEcsEvent extends EcsEvent 
    implements ICancellableEcsEvent {
    
    boolean isCancelled();
    void setCancelled(boolean cancelled);
}
```

### ICancellableEcsEvent

Interface for cancellable ECS events.

```java
interface ICancellableEcsEvent {
    boolean isCancelled();
    void setCancelled(boolean cancelled);
}
```

---

## Entity Event Types

Entity events target specific entity holders.

### Registration

```java
// In ECS system
entityEventSystem.registerEntityEventType(
    BreakBlockEvent.class,
    BreakBlockEvent::new
);

// Listener
entityEventSystem.register(BreakBlockEvent.class, (holder, event) -> {
    // holder = entity that triggered event
    // event = event data
});
```

### Event Flow

1. System creates event instance
2. Event dispatched to entity's holder
3. All registered listeners receive event
4. If cancellable, cancellation checked

---

## World Event Types

World events target the entire world.

### Registration

```java
// In ECS system
worldEventSystem.registerWorldEventType(
    ChunkSaveEvent.class,
    ChunkSaveEvent::new
);

// Listener
worldEventSystem.register(ChunkSaveEvent.class, (world, event) -> {
    // world = world instance
    // event = event data
});
```

---

## Block-Related ECS Events

### BreakBlockEvent

Fired when an entity breaks a block.

**Type**: Entity Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `itemInHand` | ItemStack | No | Tool used to break |
| `targetBlock` | Vector3i | Yes | Block position |
| `blockType` | BlockType | No | Type of block |

```java
entityEventSystem.register(BreakBlockEvent.class, (holder, event) -> {
    if (event.getBlockType().getId().equals("Bedrock")) {
        event.setCancelled(true);
    }
});
```

### PlaceBlockEvent

Fired when an entity places a block.

**Type**: Entity Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `itemInHand` | ItemStack | No | Item being placed |
| `targetBlock` | Vector3i | Yes | Placement position |
| `rotation` | RotationTuple | Yes | Block rotation |

### DamageBlockEvent

Fired during block mining (per damage tick).

**Type**: Entity Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `itemInHand` | ItemStack | No | Mining tool |
| `targetBlock` | Vector3i | Yes | Block position |
| `blockType` | BlockType | No | Block being mined |
| `currentDamage` | float | No | Current damage progress |
| `damage` | float | Yes | Damage this tick |

```java
entityEventSystem.register(DamageBlockEvent.class, (holder, event) -> {
    // Speed up mining
    event.setDamage(event.getDamage() * 2.0f);
});
```

### UseBlockEvent

Two-phase event for block usage.

**UseBlockEvent.Pre** - Before use (Cancellable)
**UseBlockEvent.Post** - After use (Not cancellable)

| Property | Type | Description |
|----------|------|-------------|
| `interactionType` | InteractionType | Type of interaction |
| `context` | InteractionContext | Interaction context |
| `targetBlock` | Vector3i | Block position |
| `blockType` | BlockType | Block type |

---

## Item-Related ECS Events

### DropItemEvent

Fired when an entity drops an item.

**Type**: Entity Event, Cancellable

**DropItemEvent.Drop** - Actual drop

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `itemStack` | ItemStack | Yes | Item being dropped |
| `throwSpeed` | float | Yes | Throw velocity |

**DropItemEvent.PlayerRequest** - Player initiates drop

| Property | Type | Description |
|----------|------|-------------|
| `inventorySectionId` | int | Inventory section |
| `slotId` | short | Slot being dropped |

### InteractivelyPickupItemEvent

Fired when entity picks up item through interaction.

**Type**: Entity Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `itemStack` | ItemStack | Yes | Item being picked up |

### CraftRecipeEvent

Two-phase crafting event.

**CraftRecipeEvent.Pre** - Before crafting (Cancellable)
**CraftRecipeEvent.Post** - After crafting

| Property | Type | Description |
|----------|------|-------------|
| `craftedRecipe` | CraftingRecipe | Recipe being crafted |
| `quantity` | int | Amount to craft |

---

## Player-Related ECS Events

### ChangeGameModeEvent

Fired when player game mode changes.

**Type**: Entity Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `gameMode` | GameMode | Yes | New game mode |

```java
entityEventSystem.register(ChangeGameModeEvent.class, (holder, event) -> {
    if (event.getGameMode() == GameMode.CREATIVE) {
        // Restrict creative mode
        event.setCancelled(true);
    }
});
```

### SwitchActiveSlotEvent

Fired when player switches hotbar slot.

**Type**: Entity Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `inventorySectionId` | int | No | Inventory section |
| `previousSlot` | int | No | Previous slot |
| `newSlot` | byte | Yes | New slot |
| `serverRequest` | boolean | No | Server-initiated |

### DiscoverZoneEvent.Display

Fired when zone discovery UI would show.

**Type**: Entity Event, Cancellable

| Property | Type | Description |
|----------|------|-------------|
| `discoveryInfo` | ZoneDiscoveryInfo | Zone discovery data |

### DiscoverInstanceEvent.Display

Fired when instance discovery UI would show.

**Type**: Entity Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `instanceWorldUuid` | UUID | No | Instance world UUID |
| `discoveryConfig` | InstanceDiscoveryConfig | No | Discovery config |
| `display` | boolean | Yes | Whether to show UI |

---

## Combat ECS Events

### Damage

Primary damage event with metadata support.

**Type**: Entity Event, Cancellable, MetaStore

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `source` | Damage.Source | Yes | Damage source |
| `damageCauseIndex` | int | Yes | Cause index |
| `amount` | float | Yes | Damage amount |
| `initialAmount` | float | No | Original amount |

#### Metadata Support

```java
entityEventSystem.register(Damage.class, (holder, event) -> {
    // Read metadata
    Vector4d hitLocation = event.getMeta(Damage.HIT_LOCATION);
    
    // Modify metadata
    event.setMeta(Damage.KNOCKBACK_COMPONENT, customKnockback);
});
```

### KillFeedEvent

Three-phase death message event.

**KillFeedEvent.DecedentMessage** - Message for victim (Cancellable)
**KillFeedEvent.KillerMessage** - Message for killer (Cancellable)
**KillFeedEvent.Display** - Broadcast display (Cancellable)

---

## World ECS Events

### ChunkSaveEvent

Fired when chunk is being saved.

**Type**: World Event, Cancellable

| Property | Type | Description |
|----------|------|-------------|
| `chunk` | WorldChunk | Chunk being saved |

### ChunkUnloadEvent

Fired when chunk is being unloaded.

**Type**: World Event, Cancellable

| Property | Type | Mutable | Description |
|----------|------|---------|-------------|
| `chunk` | WorldChunk | Chunk being unloaded |
| `resetKeepAlive` | boolean | Yes | Reset keep-alive timer |

### MoonPhaseChangeEvent

Fired when moon phase changes.

**Type**: World Event, Not Cancellable

| Property | Type | Description |
|----------|------|-------------|
| `newMoonPhase` | int | New phase (0-7) |

---

## Prefab ECS Events

### PrefabPasteEvent

Fired when prefab is pasted.

**Type**: Entity Event, Cancellable

| Property | Type | Description |
|----------|------|-------------|
| `prefabId` | int | Prefab identifier |
| `pasteStart` | boolean | Is start of paste operation |

### PrefabPlaceEntityEvent

Fired when entity placed from prefab.

**Type**: Entity Event, Not Cancellable

| Property | Type | Description |
|----------|------|-------------|
| `prefabId` | int | Prefab identifier |
| `holder` | Holder | Placed entity holder |

---

## ECS Event System Integration

### Creating Custom ECS Events

```java
public class CustomBlockEvent extends CancellableEcsEvent {
    private final BlockType blockType;
    private int customValue;
    
    public CustomBlockEvent(BlockType blockType) {
        this.blockType = blockType;
        this.customValue = 0;
    }
    
    public BlockType getBlockType() { return blockType; }
    public int getCustomValue() { return customValue; }
    public void setCustomValue(int value) { this.customValue = value; }
}
```

### Registering Custom Events

```java
// In your ECS system
@Override
public void onRegister() {
    entityEventSystem.registerEntityEventType(
        CustomBlockEvent.class,
        CustomBlockEvent::new
    );
}
```

### Dispatching Events

```java
// Create and dispatch event
CustomBlockEvent event = new CustomBlockEvent(blockType);
entityEventSystem.dispatch(holder, event);

if (!event.isCancelled()) {
    // Proceed with action
}
```

---

## Event Processing Order

1. **Event Created**: System creates event instance
2. **Pre-Processing**: Internal systems process first
3. **Listener Dispatch**: Registered listeners called
4. **Cancellation Check**: Check if event was cancelled
5. **Post-Processing**: Finalize based on event state

---

## Source Files

- `com/hypixel/hytale/component/system/EcsEvent.java`
- `com/hypixel/hytale/component/system/CancellableEcsEvent.java`
- `com/hypixel/hytale/component/system/ICancellableEcsEvent.java`
- `com/hypixel/hytale/component/event/EntityEventSystem.java`
- `com/hypixel/hytale/component/event/WorldEventSystem.java`
- `com/hypixel/hytale/server/core/event/events/ecs/*.java`
- `com/hypixel/hytale/server/core/modules/entity/damage/Damage.java`
