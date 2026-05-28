# Hytale AI Sensors Reference

Complete reference for NPC AI sensors in the Hytale server.

## Sensor Overview

Sensors detect conditions in the game world. When a sensor returns true, its instruction's actions and motions execute.

### Sensor Interface

```java
interface Sensor {
    boolean update(NPCEntity npc, Blackboard blackboard);
    InfoProvider getInfoProvider();
}
```

---

## Entity Detection Sensors

### SensorPlayer

Detects players within range.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Range` | Float | Detection radius |
| `LineOfSight` | Boolean | Require line of sight |
| `AttitudeFilter` | List | Filter by attitude (Hostile, Neutral, Friendly) |

**InfoProvider Output**: Target player reference

### SensorEntity

Detects NPCs and entities within range.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Range` | Float | Detection radius |
| `GetPlayers` | Boolean | Include players |
| `GetNPCs` | Boolean | Include NPCs |
| `ExcludeOwnType` | Boolean | Exclude same NPC type |
| `EntityTypes` | List | Specific entity types to detect |
| `AttitudeFilter` | List | Filter by attitude |
| `LineOfSight` | Boolean | Require visibility |

### SensorTarget

Checks if a marked target exists and meets criteria.

| Parameter | Type | Description |
|-----------|------|-------------|
| `TargetExists` | Boolean | Target must exist |
| `InRange` | Float | Max distance to target |
| `LineOfSight` | Boolean | Must see target |
| `IsAlive` | Boolean | Target must be alive |

### SensorSelf

Evaluates conditions on the NPC itself.

| Parameter | Type | Description |
|-----------|------|-------------|
| `StatConditions` | Map | Stat value conditions |
| `HasEffects` | List | Required active effects |
| `MovementState` | String | Required movement state |

### SensorBeacon

Detects beacon entities.

| Parameter | Type | Description |
|-----------|------|-------------|
| `BeaconType` | String | Beacon type to find |
| `Range` | Float | Search radius |

### SensorKill

Detects when NPC kills a target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `KillType` | Enum | Type of kill to detect |

---

## Combat Sensors

### SensorDamage

Detects damage taken.

| Parameter | Type | Description |
|-----------|------|-------------|
| `CombatDamage` | Boolean | Detect combat damage |
| `FriendlyDamage` | Boolean | Detect friendly fire |
| `DrowningDamage` | Boolean | Detect drowning |
| `EnvironmentDamage` | Boolean | Detect environmental |
| `OtherDamage` | Boolean | Detect other sources |
| `MinDamage` | Float | Minimum damage threshold |

**InfoProvider Output**: Damage source, amount, attacker reference

### SensorIsBackingAway

Checks if NPC is backing away from target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

---

## World/Environment Sensors

### SensorPath

Finds patrol paths.

| Parameter | Type | Description |
|-----------|------|-------------|
| `PathType` | Enum | `WorldPath`, `CurrentPrefabPath`, `AnyPrefabPath`, `TransientPath` |
| `PathId` | String | Specific path ID |
| `Range` | Float | Search radius |

### SensorBlock

Finds blocks from a BlockSet within range.

| Parameter | Type | Description |
|-----------|------|-------------|
| `BlockSet` | String | Block set reference |
| `Range` | Float | Search radius |
| `MinCount` | Integer | Minimum blocks to find |

### SensorBlockType

Checks block type at position.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Position` | Vector3i | Block position |
| `BlockTypes` | List | Block types to check |
| `Relative` | Boolean | Position relative to NPC |

### SensorBlockChange

Detects block changes in range.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Range` | Float | Detection radius |
| `ChangeType` | Enum | `Place`, `Break`, `Any` |
| `BlockTypes` | List | Filter block types |

### SensorTime

Checks time of day/year.

| Parameter | Type | Description |
|-----------|------|-------------|
| `MinTime` | Integer | Minimum time (0-24000) |
| `MaxTime` | Integer | Maximum time |
| `Season` | String | Required season |

### SensorWeather

Checks weather conditions.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Weather` | Enum | `Clear`, `Rain`, `Storm`, `Snow` |

### SensorLight

Checks light levels.

| Parameter | Type | Description |
|-----------|------|-------------|
| `LightType` | Enum | `Light`, `SkyLight`, `Sunlight` |
| `MinLevel` | Integer | Minimum light (0-15) |
| `MaxLevel` | Integer | Maximum light |

### SensorLeash

Checks if beyond leash range.

| Parameter | Type | Description |
|-----------|------|-------------|
| `LeashRange` | Float | Maximum distance from origin |
| `LeashPosition` | Vector3d | Leash center point |

### SensorInWater

Checks if in water.

| Parameter | Type | Description |
|-----------|------|-------------|
| `MinDepth` | Float | Minimum water depth |

### SensorCanPlace

Checks if can place block at target.

| Parameter | Type | Description |
|-----------|------|-------------|
| `BlockType` | String | Block to place |
| `Position` | Vector3i | Target position |

### SensorSearchRay

Raycasting sensor.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Direction` | Vector3f | Ray direction |
| `MaxDistance` | Float | Ray length |
| `HitBlock` | Boolean | Detect block hits |
| `HitEntity` | Boolean | Detect entity hits |

---

## Movement Sensors

### SensorNav

Navigation state sensor.

| Parameter | Type | Description |
|-----------|------|-------------|
| `NavState` | Enum | `Idle`, `Pathing`, `Arrived`, `Stuck`, `NoPath` |

### SensorInAir

Checks if in air.

| Parameter | Type | Description |
|-----------|------|-------------|
| `MinTime` | Float | Minimum air time |

### SensorOnGround

Checks if on ground.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

### SensorMotionController

Checks motion controller state.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ControllerType` | String | Controller type |
| `State` | Enum | Controller state |

---

## State/Logic Sensors

### SensorState

Checks current state/substate.

| Parameter | Type | Description |
|-----------|------|-------------|
| `State` | String | Required state |
| `SubState` | String | Required substate |

### SensorIsBusy

Checks if NPC is busy with action.

| Parameter | Type | Description |
|-----------|------|-------------|
| `None` | - | No parameters |

### SensorFlag

Checks boolean flag.

| Parameter | Type | Description |
|-----------|------|-------------|
| `FlagName` | String | Flag identifier |
| `Value` | Boolean | Expected value |

### SensorAnd

Logical AND of multiple sensors.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Sensors` | List | Child sensors (all must pass) |

### SensorOr

Logical OR of multiple sensors.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Sensors` | List | Child sensors (any must pass) |

### SensorNot

Logical NOT of sensor.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Sensor` | Sensor | Sensor to invert |

### SensorRandom

Random true/false.

| Parameter | Type | Description |
|-----------|------|-------------|
| `TrueChance` | Float | Probability (0-1) |
| `TrueDuration` | Float | Min time true |
| `FalseDuration` | Float | Min time false |

### SensorSwitch

Switch-like sensor.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Cases` | Map | Condition -> Result mapping |
| `Default` | Boolean | Default result |

### SensorEval

Expression evaluation.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Expression` | String | Math/logic expression |
| `Variables` | Map | Variable bindings |

---

## Timer/Lifecycle Sensors

### SensorTimer

Checks timer state.

| Parameter | Type | Description |
|-----------|------|-------------|
| `TimerId` | String | Timer identifier |
| `State` | Enum | `Running`, `Expired`, `Stopped` |

### SensorAlarm

Alarm-based sensor.

| Parameter | Type | Description |
|-----------|------|-------------|
| `AlarmId` | String | Alarm identifier |
| `Triggered` | Boolean | Check if triggered |

### SensorAge

Checks NPC age.

| Parameter | Type | Description |
|-----------|------|-------------|
| `MinAge` | Float | Minimum age (seconds) |
| `MaxAge` | Float | Maximum age |

---

## Interaction Sensors

### SensorCanInteract

Checks if interaction is possible.

| Parameter | Type | Description |
|-----------|------|-------------|
| `InteractionType` | Enum | Type of interaction |
| `Target` | String | Target type |

### SensorHasInteracted

Checks if interaction occurred.

| Parameter | Type | Description |
|-----------|------|-------------|
| `InteractionType` | Enum | Type of interaction |
| `WithinTime` | Float | Time window (seconds) |

### SensorInteractionContext

Interaction context sensor.

| Parameter | Type | Description |
|-----------|------|-------------|
| `ContextKey` | String | Context key to check |
| `ContextValue` | Object | Expected value |

### SensorAnimation

Checks animation state.

| Parameter | Type | Description |
|-----------|------|-------------|
| `AnimationSlot` | Integer | Animation slot |
| `AnimationId` | String | Animation identifier |
| `State` | Enum | `Playing`, `Finished`, `Idle` |

---

## Item Sensors

### SensorDroppedItem

Detects dropped items nearby.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Range` | Float | Detection radius |
| `ItemTypes` | List | Filter item types |
| `MinCount` | Integer | Minimum item count |

---

## JSON Configuration Examples

### Basic Entity Detection

```json
{
  "Sensor": {
    "Type": "SensorPlayer",
    "Range": 16.0,
    "LineOfSight": true,
    "AttitudeFilter": ["Hostile"]
  }
}
```

### Compound Logic

```json
{
  "Sensor": {
    "Type": "SensorAnd",
    "Sensors": [
      { "Type": "SensorTime", "MinTime": 13000 },
      { "Type": "SensorLight", "MaxLevel": 7 },
      { "Type": "SensorOnGround" }
    ]
  }
}
```

### Damage Response

```json
{
  "Sensor": {
    "Type": "SensorDamage",
    "CombatDamage": true,
    "MinDamage": 1.0
  }
}
```

---

## Source Files

- `com/hypixel/hytale/server/npc/instructions/Sensor.java`
- `com/hypixel/hytale/server/npc/corecomponents/SensorBase.java`
- `com/hypixel/hytale/server/npc/corecomponents/entity/SensorPlayer.java`
- `com/hypixel/hytale/server/npc/corecomponents/entity/SensorEntity.java`
- `com/hypixel/hytale/server/npc/corecomponents/entity/SensorTarget.java`
- `com/hypixel/hytale/server/npc/corecomponents/combat/SensorDamage.java`
- `com/hypixel/hytale/server/npc/corecomponents/world/SensorBlock.java`
- `com/hypixel/hytale/server/npc/corecomponents/world/SensorTime.java`
- `com/hypixel/hytale/server/npc/corecomponents/statemachine/SensorState.java`
- `com/hypixel/hytale/server/npc/corecomponents/timer/SensorTimer.java`
- `com/hypixel/hytale/server/npc/corecomponents/utility/SensorAnd.java`
- `com/hypixel/hytale/server/npc/corecomponents/utility/SensorOr.java`
- `com/hypixel/hytale/server/npc/corecomponents/utility/SensorNot.java`
