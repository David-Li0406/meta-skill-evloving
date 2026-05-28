# Hytale Block States Reference

Complete reference for the block state system in the Hytale server.

## Overview

Hytale's block state system has multiple layers:

1. **StateData** - Named states mapping to BlockType variants
2. **Rotation System** - Block orientation (yaw, pitch, roll)
3. **VariantRotation** - Valid rotation configurations per block type
4. **BlockStateInfo** - Component system for block entity data

---

## State Data System

### StateData Class

Defines named states that map to different block type variants.

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Unique state definition ID |
| `stateToBlock` | Map | State name → Block type key |
| `blockToState` | Map | Block type key → State name (auto-generated) |

### State Name Constants

```java
NULL_STATE_ID = "default"  // Default state identifier
```

### State Operations

```java
// Get block type for a state name
String blockKey = stateData.getBlockForState("open");

// Get state name for a block type
String stateName = stateData.getStateForBlock(blockTypeKey);
```

### Example: Door States

```json
{
  "Id": "DoorStates",
  "StateToBlock": {
    "default": "Door_Closed",
    "open": "Door_Open"
  }
}
```

---

## Rotation System

### Rotation Enum

Four cardinal rotations in 90° increments:

| Value | Degrees | Direction |
|-------|---------|-----------|
| `None` | 0° | North (-Z) |
| `Ninety` | 90° | West (-X) |
| `OneEighty` | 180° | South (+Z) |
| `TwoSeventy` | 270° | East (+X) |

### Rotation Operations

```java
// Add rotations
Rotation result = rotation1.add(rotation2);

// Subtract rotations
Rotation result = rotation1.subtract(rotation2);

// Flip 180°
Rotation flipped = rotation.flip();

// From degrees
Rotation rot = Rotation.ofDegrees(90);

// Closest match
Rotation rot = Rotation.closestOfDegrees(45.5f);
```

### Axis Rotation

Rotate vectors around specific axes:

```java
// Rotate around Y axis (yaw)
Vector3i rotated = rotation.rotateY(input, output);

// Rotate around X axis (pitch)
Vector3i rotated = rotation.rotateX(input, output);

// Rotate around Z axis (roll)
Vector3i rotated = rotation.rotateZ(input, output);
```

---

## RotationTuple

Combined yaw, pitch, roll rotation.

### Structure

```java
record RotationTuple(int index, Rotation yaw, Rotation pitch, Rotation roll)
```

### Constants

```java
RotationTuple.NONE        // (0, None, None, None)
RotationTuple.NONE_INDEX  // 0
```

### Factory Methods

```java
// Create from components
RotationTuple rot = RotationTuple.of(yaw, pitch, roll);
RotationTuple rot = RotationTuple.of(yaw, pitch);  // roll = None

// Get by index (0-63)
RotationTuple rot = RotationTuple.get(index);

// Compute index
int index = RotationTuple.index(yaw, pitch, roll);
```

### Index Calculation

64 possible combinations (4³):
```
index = yaw.ordinal() + (pitch.ordinal() * 4) + (roll.ordinal() * 16)
```

---

## Variant Rotation

Defines valid rotation configurations per block type.

### Variants

| Variant | Description | Orientations |
|---------|-------------|--------------|
| `None` | No rotation | 1 |
| `Wall` | Wall-mounted | 2 pitch |
| `UpDown` | Vertical | 2 (normal + inverted) |
| `Pipe` | Log-like | 3 axes |
| `DoublePipe` | Extended pipe | 6 |
| `NESW` | Cardinal | 4 yaw |
| `UpDownNESW` | Full directional | 8 |
| `Debug` | Extended debug | 16 |
| `All` | Complete freedom | 64 |

### Variant Operations

```java
// Get valid rotations for variant
RotationTuple[] validRotations = variant.getRotations();

// Verify and constrain to valid
RotationTuple valid = variant.verify(tuple);

// Rotate within variant constraints
RotationTuple rotated = variant.rotateX(tuple, rotation);
RotationTuple rotated = variant.rotateZ(tuple, rotation);
```

---

## Block Flip Type

How blocks behave when mirrored.

| Type | Description |
|------|-------------|
| `ORTHOGONAL` | Asymmetric - rotation adjusts |
| `SYMMETRIC` | Symmetric - simple flip |

---

## Block State Storage

### In Chunks

Block rotation stored per-block in chunk sections:

```java
// Get rotation
int rotationIndex = chunk.getRotationIndex(x, y, z);
RotationTuple rotation = chunk.getRotation(x, y, z);

// Set block with rotation
chunk.setBlock(x, y, z, blockId, blockType, rotationIndex, filler, settings);

// Place with rotation
chunk.placeBlock(x, y, z, blockTypeKey, rotationTuple, settings, validate);
```

### Block Entity Component

For blocks with persistent data:

```java
class BlockStateInfo implements Component<ChunkStore> {
    int index;           // Block index in chunk column
    Ref<ChunkStore> chunkRef;  // Chunk reference
    
    void markNeedsSaving();
}
```

---

## Common State Patterns

### State Variant Switching

```java
// Get current state
String currentState = blockType.getStateForBlock(blockType);

// Switch to new state
BlockType newType = blockType.getBlockForState("newState");
if (newType != null) {
    int rotationIndex = chunk.getRotationIndex(x, y, z);
    chunk.setBlock(x, y, z, newType.getId(), newType, rotationIndex, 0, settings);
}
```

### Interaction State Changes

For interactive blocks (doors, containers):

```java
// Open container
chunk.setBlockInteractionState(pos, blockType, "OpenWindow");

// Close container
chunk.setBlockInteractionState(pos, blockType, "CloseWindow");

// Toggle door
String current = blockType.getStateForBlock(blockType);
String newState = "default".equals(current) ? "Open" : "default";
world.setBlockInteractionState(pos, blockType, newState);
```

### Common Interaction States

| State | Usage |
|-------|-------|
| `"default"` | Normal/closed |
| `"OpenWindow"` | Container open |
| `"CloseWindow"` | Container closed |
| `"DoorBlocked"` | Door cannot open |
| `"Processing"` | Bench active |
| `"ProcessCompleted"` | Crafting done |
| `"Produce_Ready"` | Has output |

### Block Entity Creation

```java
// Create block entity from template
Holder<ChunkStore> holder = blockType.getBlockEntity().clone();

// Add position reference
int blockIndex = ChunkUtil.indexBlockInColumn(x, y, z);
holder.putComponent(BlockStateInfo.TYPE, new BlockStateInfo(blockIndex, chunkRef));

// Add custom components
holder.putComponent(MyComponent.TYPE, new MyComponent());

// Spawn in world
Ref<ChunkStore> ref = store.addEntity(holder, AddReason.SPAWN);
```

### Rotated Block Placement

```java
// Calculate rotation from player facing
Rotation yaw = Rotation.closestOfDegrees(playerYaw);
RotationTuple rotation = RotationTuple.of(yaw, Rotation.None);

// Verify for block type
RotationTuple verified = blockType.getVariantRotation().verify(rotation);

// Place block
chunk.placeBlock(x, y, z, blockTypeKey, verified, settings, true);
```

---

## Farming Block State

For crops and growing blocks:

```java
class FarmingBlockState implements Component<ChunkStore> {
    String baseCrop;
    Instant stageStart;
    String currentFarmingStageSetName;
    int currentFarmingStageIndex;
    Instant[] stageCompletionTimes;
    float spreadRate = 1.0f;
}
```

---

## Network Serialization

### BlockRotation (Protocol)

```java
class BlockRotation {
    Rotation rotationYaw = Rotation.None;
    Rotation rotationPitch = Rotation.None;
    Rotation rotationRoll = Rotation.None;
    
    // 3 bytes (1 per axis)
    static final int FIXED_BLOCK_SIZE = 3;
}
```

### RandomRotation Modes

| Mode | Description |
|------|-------------|
| `None` | No random rotation |
| `YawPitchRollStep1` | All axes, 1° steps |
| `YawStep1` | Yaw only, 1° steps |
| `YawStep1XZ` | Yaw with X/Z variation |
| `YawStep90` | Yaw in 90° steps |

---

## Source Files

- `com/hypixel/hytale/server/core/asset/type/blocktype/config/StateData.java`
- `com/hypixel/hytale/server/core/asset/type/blocktype/config/Rotation.java`
- `com/hypixel/hytale/server/core/asset/type/blocktype/config/RotationTuple.java`
- `com/hypixel/hytale/server/core/asset/type/blocktype/config/VariantRotation.java`
- `com/hypixel/hytale/server/core/asset/type/blocktype/config/BlockFlipType.java`
- `com/hypixel/hytale/server/core/modules/block/BlockModule.java`
- `com/hypixel/hytale/protocol/BlockRotation.java`
- `com/hypixel/hytale/server/core/universe/world/chunk/BlockRotationUtil.java`
