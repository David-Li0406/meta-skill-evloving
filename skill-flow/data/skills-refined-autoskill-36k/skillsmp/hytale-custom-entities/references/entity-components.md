# Hytale Entity Components Reference

Complete reference for the Entity Component System (ECS) components in Hytale.

## ECS Architecture Overview

Hytale uses a data-oriented ECS architecture:

- **Component**: Pure data container, no logic
- **System**: Logic that operates on components
- **Entity (Holder)**: Container with archetype and component array
- **Archetype**: Defines which components an entity has
- **Store**: Storage for entities (EntityStore, WorldStore)

### Core Interfaces

```java
interface Component<Self extends Component<Self>> extends Cloneable {
    Self clone();
}

class ComponentType<T extends Component<T>> {
    ComponentRegistry<?> registry;
    int index;
}

class Holder<Store> {
    Archetype archetype;
    Component<?>[] components;
}
```

---

## Transform & Position Components

### TransformComponent

Core position and rotation for all entities.

| Field | Type | Description |
|-------|------|-------------|
| `position` | Vector3d | World position (x, y, z) |
| `rotation` | Vector3f | Rotation (pitch, yaw, roll) |
| `chunk` | ChunkRef | Current chunk reference |

### HeadRotation

Separate head rotation from body.

| Field | Type | Description |
|-------|------|-------------|
| `yaw` | float | Horizontal head rotation |
| `pitch` | float | Vertical head rotation |

---

## Visual Components

### ModelComponent

3D model reference for rendering.

| Field | Type | Description |
|-------|------|-------------|
| `modelId` | String | Reference to Model asset |
| `networkSync` | boolean | Sync model changes to clients |

### DisplayNameComponent

Entity display name above head.

| Field | Type | Description |
|-------|------|-------------|
| `name` | Message | Formatted display name |

### ActiveAnimationComponent

Currently playing animations.

| Field | Type | Description |
|-------|------|-------------|
| `slots` | AnimationSlot[] | Animation per slot |

### DynamicLight

Light emission from entity.

| Field | Type | Description |
|-------|------|-------------|
| `color` | Color | Light color (RGB) |
| `intensity` | float | Light brightness |
| `radius` | float | Light range |

---

## Physics Components

### BoundingBox

Collision volume for entity.

| Field | Type | Description |
|-------|------|-------------|
| `min` | Vector3f | Minimum corner |
| `max` | Vector3f | Maximum corner |
| `detailBoxes` | Map | Named detail boxes |

### Velocity

Movement velocity vector.

| Field | Type | Description |
|-------|------|-------------|
| `velocity` | Vector3d | Current velocity |
| `instructions` | List | Velocity modification instructions |

---

## Identity Components

### UUIDComponent

Unique entity identifier.

| Field | Type | Description |
|-------|------|-------------|
| `uuid` | UUID | Universally unique ID |

### NetworkIdComponent

Network synchronization ID.

| Field | Type | Description |
|-------|------|-------------|
| `networkId` | int | Network entity ID |

---

## State Components

### MovementStatesComponent

Current movement state flags.

| Field | Type | Description |
|-------|------|-------------|
| `isGrounded` | boolean | On ground |
| `isJumping` | boolean | Currently jumping |
| `isCrouching` | boolean | Crouched |
| `isSprinting` | boolean | Sprinting |
| `isSwimming` | boolean | In water swimming |
| `isFlying` | boolean | Flying (creative) |
| `isGliding` | boolean | Using glider |

### Marker Components (Singletons)

No-data marker components:

| Component | Purpose |
|-----------|---------|
| `Interactable` | Entity can be interacted with |
| `Intangible` | No collision |
| `Invulnerable` | Cannot take damage |

---

## Combat Components

### KnockbackComponent

Active knockback state.

| Field | Type | Description |
|-------|------|-------------|
| `velocity` | Vector3d | Knockback direction |
| `duration` | float | Remaining duration |
| `modifiers` | Map | Knockback modifications |

### DamageDataComponent

Combat timing and state.

| Field | Type | Description |
|-------|------|-------------|
| `lastDamageTime` | long | Last damage timestamp |
| `wieldingState` | boolean | Currently blocking |
| `invulnerabilityTime` | float | I-frames remaining |

### EffectControllerComponent

Active entity effects management.

| Field | Type | Description |
|-------|------|-------------|
| `activeEffects` | Map | Effect -> Duration |
| `sources` | Map | Effect -> Source entity |

### DeathComponent

Death state and information.

| Field | Type | Description |
|-------|------|-------------|
| `cause` | Damage | Damage that killed |
| `message` | Message | Death message |
| `itemsLost` | List | Dropped items |

---

## Item Components

### ItemComponent

For dropped item entities.

| Field | Type | Description |
|-------|------|-------------|
| `itemStack` | ItemStack | The item stack |
| `pickupDelay` | float | Delay before pickup |
| `mergeDelay` | float | Delay before merging |

### PickupItemComponent

Item pickup animation state.

| Field | Type | Description |
|-------|------|-------------|
| `targetEntity` | Ref | Entity picking up |
| `progress` | float | Animation progress |

---

## Projectile Component

### ProjectileComponent

Projectile physics and damage.

| Field | Type | Description |
|-------|------|-------------|
| `owner` | Ref | Entity that fired |
| `damage` | float | Damage on hit |
| `gravity` | float | Gravity multiplier |
| `speed` | float | Projectile speed |
| `lifetime` | float | Max lifetime |
| `penetration` | int | Entities to pierce |
| `particles` | String | Trail particles |
| `onHit` | List | Effects on hit |

---

## Mount Components

### MountedComponent

Entity is riding something (rider side).

| Field | Type | Description |
|-------|------|-------------|
| `mount` | Ref | Entity being ridden |
| `seatIndex` | int | Seat position |

### MountedByComponent

Entity is being ridden (mount side).

| Field | Type | Description |
|-------|------|-------------|
| `passengers` | List<Ref> | Entities riding |

### NPCMountComponent

NPC mount configuration.

| Field | Type | Description |
|-------|------|-------------|
| `mountSpeed` | float | Movement speed |
| `mountJump` | float | Jump power |
| `steerability` | float | Turn rate |

---

## Lifecycle Components

### NewSpawnComponent

Recently spawned entity.

| Field | Type | Description |
|-------|------|-------------|
| `spawnTime` | long | When spawned |
| `spawnWindow` | float | Protection duration |

### DespawnComponent

Scheduled for despawn.

| Field | Type | Description |
|-------|------|-------------|
| `despawnTime` | long | When to despawn |
| `reason` | String | Despawn reason |

---

## Audio Component

### AudioComponent

Sound event associations.

| Field | Type | Description |
|-------|------|-------------|
| `soundEvents` | List<String> | Sound event IDs |
| `currentSound` | String | Currently playing |

---

## Common Entity Archetypes

### Player Entity

```
TransformComponent, HeadRotation, UUIDComponent, NetworkIdComponent,
ModelComponent, BoundingBox, Velocity, MovementStatesComponent,
EffectControllerComponent, DamageDataComponent, PlayerComponent,
InventoryComponent, HotbarComponent
```

### NPC Entity

```
TransformComponent, HeadRotation, UUIDComponent, NetworkIdComponent,
ModelComponent, BoundingBox, Velocity, MovementStatesComponent,
EffectControllerComponent, DamageDataComponent, NPCComponent,
RoleComponent, AIBlackboardComponent
```

### Dropped Item

```
TransformComponent, UUIDComponent, NetworkIdComponent,
ItemComponent, Velocity, Intangible, DespawnComponent
```

### Projectile

```
TransformComponent, UUIDComponent, NetworkIdComponent,
ProjectileComponent, Velocity, BoundingBox
```

### Mount

```
TransformComponent, HeadRotation, UUIDComponent, NetworkIdComponent,
ModelComponent, BoundingBox, Velocity, MountedByComponent,
Interactable, NPCMountComponent
```

---

## Component Access Patterns

### Getting Components

```java
// From holder
TransformComponent transform = holder.get(TransformComponent.TYPE);

// Check if has component
if (holder.has(VelocityComponent.TYPE)) {
    Velocity vel = holder.get(VelocityComponent.TYPE);
}
```

### Modifying Components

```java
// Components are mutable data
TransformComponent transform = holder.get(TransformComponent.TYPE);
transform.position.x += 1.0;
// No setter needed - direct mutation
```

### Adding/Removing Components

```java
// Archetypes are immutable - create new holder with different archetype
Archetype newArchetype = archetype.with(NewComponent.TYPE);
holder = store.changeArchetype(holder, newArchetype);
```

---

## Source Files

- `com/hypixel/hytale/component/Component.java`
- `com/hypixel/hytale/component/ComponentType.java`
- `com/hypixel/hytale/component/ComponentRegistry.java`
- `com/hypixel/hytale/component/Holder.java`
- `com/hypixel/hytale/server/core/modules/entity/component/TransformComponent.java`
- `com/hypixel/hytale/server/core/modules/entity/component/ModelComponent.java`
- `com/hypixel/hytale/server/core/modules/entity/component/BoundingBox.java`
- `com/hypixel/hytale/server/core/modules/physics/component/Velocity.java`
- `com/hypixel/hytale/server/core/entity/UUIDComponent.java`
- `com/hypixel/hytale/server/core/entity/KnockbackComponent.java`
- `com/hypixel/hytale/server/core/entity/EffectControllerComponent.java`
- `com/hypixel/hytale/server/core/entity/ProjectileComponent.java`
- `com/hypixel/hytale/server/core/modules/entity/item/ItemComponent.java`
- `com/hypixel/hytale/builtin/mounts/MountedComponent.java`
- `com/hypixel/hytale/builtin/mounts/MountedByComponent.java`
