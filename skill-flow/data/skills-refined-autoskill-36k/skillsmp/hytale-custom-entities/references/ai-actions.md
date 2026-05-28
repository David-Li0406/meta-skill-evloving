# Hytale AI Actions Reference

Complete reference for NPC AI actions and motions in the Hytale server.

## Action Overview

Actions are executed when a sensor returns true. They modify NPC state, interact with the world, or trigger behaviors.

### Action Interface

```java
interface Action {
    void execute(NPCEntity npc, Blackboard blackboard, InfoProvider info);
}
```

---

## Combat Actions

### ActionAttack

Executes attacks.

| Parameter | Type | Description |
|-----------|------|-------------|
| `AttackType` | Enum | `Primary`, `Secondary`, `Ability1-3` |
| `BallisticMode` | Boolean | Use ballistic aiming |
| `AimTime` | Float | Time to aim before firing |
| `ChargeTime` | Float | Charge duration |
| `UseInfoTarget` | Boolean | Attack sensor's target |

### ActionApplyEntityEffect

Applies effects to entities.

| Parameter | Type | Description |
|-----------|------|-------------|
| `EffectType` | String | Effect to apply |
| `Duration` | Float | Effect duration |
| `Target` | Enum | `Self`, `MarkedTarget`, `InfoTarget` |
| `Amount` | Float | Effect amount |

---

## Lifecycle Actions

### ActionSpawn

Spawns new NPCs.

| Parameter | Type | Description |
|-----------|------|-------------|
| `NPCType` | String | NPC type to spawn |
| `Count` | Range | Number to spawn |
| `Direction` | Vector3f | Spawn direction |
| `Distance` | Float | Spawn distance |
| `Delay` | Float | Delay between spawns |
| `JoinFlock` | Boolean | Join NPC's flock |

### ActionDespawn

Despawns the NPC.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

### ActionDelayDespawn

Delayed despawn.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Delay` | Float | Seconds until despawn |

### ActionDie

Trigger death.

| Parameter | Type | Description |
|-----------|------|-------------|
| `DeathCause` | String | Death cause type |

### ActionRemove

Instantly remove NPC.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

### ActionRole

Changes NPC role.

| Parameter | Type | Description |
|-----------|------|-------------|
| `RoleId` | String | New role reference |

---

## State Actions

### ActionState

Sets state/substate.

| Parameter | Type | Description |
|-----------|------|-------------|
| `State` | String | New state |
| `SubState` | String | New substate |

### ActionParentState

Sets parent state.

| Parameter | Type | Description |
|-----------|------|-------------|
| `State` | String | Parent state |

### ActionToggleStateEvaluator

Toggles state evaluator.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Enabled` | Boolean | Enable/disable evaluator |

---

## World Actions

### ActionPlaceBlock

Places blocks.

| Parameter | Type | Description |
|-----------|------|-------------|
| `BlockType` | String | Block to place |
| `Position` | Vector3i | Target position |
| `Relative` | Boolean | Position relative to NPC |

### ActionMakePath

Creates transient paths.

| Parameter | Type | Description |
|-----------|------|-------------|
| `PathId` | String | Path identifier |
| `Points` | List | Path waypoints |

### ActionResetPath

Resets path state.

| Parameter | Type | Description |
|-----------|------|-------------|
| `PathId` | String | Path to reset |

### ActionSetLeashPosition

Sets leash point.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Position` | Vector3d | New leash center |
| `Range` | Float | Leash radius |

### ActionStorePosition

Stores position for later use.

| Parameter | Type | Description |
|-----------|------|-------------|
| `PositionId` | String | Storage key |
| `Position` | Vector3d | Position to store |

### ActionSetBlockToPlace

Sets block to place.

| Parameter | Type | Description |
|-----------|------|-------------|
| `BlockType` | String | Block type reference |

### ActionResetBlockSensors

Resets block sensors.

| Parameter | Type | Description |
|-----------|------|-------------|
| `SensorIds` | List | Sensors to reset |

### ActionResetSearchRays

Resets search ray sensors.

| Parameter | Type | Description |
|-----------|------|-------------|
| `RayIds` | List | Rays to reset |

### ActionTriggerSpawners

Triggers nearby spawners.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Range` | Float | Search radius |
| `SpawnerTypes` | List | Spawner types to trigger |

---

## Audio/Visual Actions

### ActionPlayAnimation

Plays animations.

| Parameter | Type | Description |
|-----------|------|-------------|
| `AnimationId` | String | Animation reference |
| `Slot` | Integer | Animation slot |
| `Speed` | Float | Playback speed |
| `Loop` | Boolean | Loop animation |

### ActionPlaySound

Plays sounds.

| Parameter | Type | Description |
|-----------|------|-------------|
| `SoundEvent` | String | Sound event reference |
| `Volume` | Float | Volume multiplier |
| `Pitch` | Float | Pitch multiplier |

### ActionSpawnParticles

Spawns particles.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ParticleSystem` | String | Particle system reference |
| `Position` | Vector3d | Spawn position |
| `Count` | Integer | Particle count |

### ActionAppearance

Changes appearance.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Appearance` | String | Appearance reference |

### ActionDisplayName

Sets display name.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Name` | String | Display name text |
| `Visible` | Boolean | Show/hide name |

### ActionModelAttachment

Manages model attachments.

| Parameter | Type | Description |
|-----------|------|-------------|
| `AttachmentId` | String | Attachment reference |
| `Operation` | Enum | `Attach`, `Detach` |
| `BoneName` | String | Bone to attach to |

---

## Entity Actions

### ActionSetStat

Sets entity stats.

| Parameter | Type | Description |
|-----------|------|-------------|
| `StatType` | String | Stat to modify |
| `Value` | Float | New value |
| `Operation` | Enum | `Set`, `Add`, `Multiply` |

### ActionNotify

Sends notifications.

| Parameter | Type | Description |
|-----------|------|-------------|
| `NotificationType` | String | Notification type |
| `Data` | Object | Notification data |

### ActionSetMarkedTarget

Sets marked target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Enum | `InfoTarget`, `Closest`, `None` |

### ActionReleaseTarget

Releases marked target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

### ActionOverrideAttitude

Overrides attitude toward entity.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Ref | Target entity |
| `Attitude` | Enum | `Hostile`, `Neutral`, `Friendly` |
| `Duration` | Float | Override duration |

### ActionIgnoreForAvoidance

Marks entity to ignore for avoidance.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Ref | Entity to ignore |
| `Duration` | Float | Ignore duration |

### ActionBeacon

Beacon-related actions.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Operation` | Enum | `Create`, `Destroy`, `Update` |
| `BeaconType` | String | Beacon type |

---

## Item Actions

### ActionPickUpItem

Picks up items.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Delay` | Float | Pickup delay |
| `Range` | Float | Pickup range |

### ActionDropItem

Drops items.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Delay` | Float | Drop delay |
| `ItemSlot` | Integer | Slot to drop from |
| `ThrowSpeed` | Float | Throw velocity |

### ActionInventory

Inventory management.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Operation` | Enum | `Clear`, `Add`, `Remove`, `Swap` |
| `ItemType` | String | Item type |
| `Slot` | Integer | Target slot |

---

## Timer Actions

### ActionTimer

Timer management.

| Parameter | Type | Description |
|-----------|------|-------------|
| `TimerId` | String | Timer identifier |
| `Operation` | Enum | `Start`, `Stop`, `Reset` |
| `Duration` | Float | Timer duration |

### ActionSetAlarm

Sets alarms.

| Parameter | Type | Description |
|-----------|------|-------------|
| `AlarmId` | String | Alarm identifier |
| `Time` | Float | Alarm time |

---

## Movement Actions

### ActionRecomputePath

Recomputes pathfinding.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

### ActionCrouch

Crouching control.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Crouch` | Boolean | Enable/disable crouch |

### ActionOverrideAltitude

Overrides altitude for flying.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Altitude` | Float | Target altitude |
| `Duration` | Float | Override duration |

---

## Interaction Actions

### ActionSetInteractable

Sets interactability.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Interactable` | Boolean | Enable/disable interaction |

### ActionLockOnInteractionTarget

Locks on interaction target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Duration` | Float | Lock duration |

---

## Utility Actions

### ActionSequence

Executes actions in sequence.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Actions` | List | Actions to execute |
| `Delay` | Float | Delay between actions |

### ActionRandom

Random action selection.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Actions` | List | Action pool |
| `Weights` | List | Selection weights |

### ActionTimeout

Timeout with delay.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Delay` | Float | Timeout duration |
| `Action` | Action | Action after timeout |

### ActionNothing

No-op action.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

### ActionSetFlag

Sets boolean flags.

| Parameter | Type | Description |
|-----------|------|-------------|
| `FlagName` | String | Flag identifier |
| `Value` | Boolean | Flag value |

### ActionResetInstructions

Resets instruction state.

| Parameter | Type | Description |
|-----------|------|-------------|
| `InstructionIds` | List | Instructions to reset |

### ActionLog

Debug logging.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Message` | String | Log message |
| `Level` | Enum | `Debug`, `Info`, `Warning`, `Error` |

---

## Body Motion Types

### BodyMotionFind

Pathfinds to target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Enum | `InfoTarget`, `MarkedTarget`, `Position` |
| `StopDistance` | Float | Distance to stop at |
| `SlowdownDistance` | Float | Distance to start slowing |
| `AbortDistance` | Float | Distance to abort pathing |
| `HeightDifference` | Float | Max height difference |

### BodyMotionMoveAway

Moves away from target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Enum | Target to flee from |
| `Distance` | Float | Desired distance |
| `Speed` | Float | Movement speed |

### BodyMotionPath

Follows patrol paths.

| Parameter | Type | Description |
|-----------|------|-------------|
| `PathId` | String | Path reference |
| `Shape` | Enum | `Line`, `Loop`, `Points`, `Chain` |
| `Speed` | Float | Movement speed |

### BodyMotionWander

Random wandering.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Range` | Float | Wander radius |
| `Speed` | Float | Movement speed |
| `IdleTime` | Range | Pause duration |

### BodyMotionMaintainDistance

Maintains distance from target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Enum | Target entity |
| `MinDistance` | Float | Minimum distance |
| `MaxDistance` | Float | Maximum distance |

### BodyMotionTeleport

Teleportation motion.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Position` | Vector3d | Target position |
| `Effects` | List | Teleport effects |

---

## Head Motion Types

### HeadMotionWatch

Watches target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Enum | What to watch |
| `Speed` | Float | Turn speed |

### HeadMotionAim

Aims at target for combat.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Target` | Enum | What to aim at |
| `LeadTarget` | Boolean | Predict movement |

### HeadMotionObserve

Observes area.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Range` | Float | Observation range |
| `Speed` | Float | Look speed |

---

## JSON Configuration Examples

### Attack Sequence

```json
{
  "Actions": [
    {
      "Type": "ActionSetMarkedTarget",
      "Target": "InfoTarget"
    },
    {
      "Type": "ActionAttack",
      "AttackType": "Primary",
      "AimTime": 0.5
    }
  ],
  "BodyMotion": {
    "Type": "BodyMotionFind",
    "Target": "MarkedTarget",
    "StopDistance": 2.0
  },
  "HeadMotion": {
    "Type": "HeadMotionAim",
    "Target": "MarkedTarget"
  }
}
```

### Patrol Behavior

```json
{
  "Actions": [],
  "BodyMotion": {
    "Type": "BodyMotionPath",
    "PathId": "patrol_route_1",
    "Shape": "Loop",
    "Speed": 0.5
  },
  "HeadMotion": {
    "Type": "HeadMotionObserve",
    "Range": 10.0
  }
}
```

### Flee Behavior

```json
{
  "Actions": [
    {
      "Type": "ActionPlaySound",
      "SoundEvent": "NPC/Flee_Cry"
    }
  ],
  "BodyMotion": {
    "Type": "BodyMotionMoveAway",
    "Target": "MarkedTarget",
    "Distance": 20.0,
    "Speed": 1.5
  }
}
```

---

## Source Files

- `com/hypixel/hytale/server/npc/instructions/Action.java`
- `com/hypixel/hytale/server/npc/instructions/BodyMotion.java`
- `com/hypixel/hytale/server/npc/instructions/HeadMotion.java`
- `com/hypixel/hytale/server/npc/corecomponents/ActionBase.java`
- `com/hypixel/hytale/server/npc/corecomponents/BodyMotionBase.java`
- `com/hypixel/hytale/server/npc/corecomponents/HeadMotionBase.java`
- `com/hypixel/hytale/server/npc/corecomponents/combat/ActionAttack.java`
- `com/hypixel/hytale/server/npc/corecomponents/lifecycle/ActionSpawn.java`
- `com/hypixel/hytale/server/npc/corecomponents/movement/BodyMotionFind.java`
- `com/hypixel/hytale/server/npc/corecomponents/movement/BodyMotionPath.java`
- `com/hypixel/hytale/server/npc/corecomponents/movement/HeadMotionWatch.java`
