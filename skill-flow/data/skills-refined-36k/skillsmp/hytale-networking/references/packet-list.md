# Hytale Network Packets Reference

Complete reference for network packets in the Hytale server.

## Protocol Overview

- **Transport**: Netty-based TCP
- **Compression**: Zstd for applicable packets
- **Byte Order**: Little-endian
- **Integer Encoding**: VarInt for variable-length integers

---

## Packet Categories

| ID Range | Category | Description |
|----------|----------|-------------|
| 0-3 | Connection | Connection management |
| 10-18 | Auth | Authentication |
| 20-34 | Setup | World/game setup |
| 40-85 | Assets | Asset updates |
| 100-119 | Player | Player actions |
| 131-166 | World | World/chunk data |
| 170-179 | Inventory | Inventory operations |
| 200-204 | Window | GUI windows |
| 210-234 | Interface | Chat, notifications |
| 240-245 | WorldMap | Map system |
| 250-252 | ServerAccess | Server access control |
| 260-262 | Machinima | Recording/playback |
| 280-283 | Camera | Camera control |
| 290-294 | Interaction | Entity interactions |
| 300-355 | AssetEditor | Asset editor (dev) |
| 360-361 | PostProcessing | Visual effects |
| 400-423 | BuilderTools | Building tools |

---

## Connection Packets (0-3)

| ID | Name | Direction | Compressed | Description |
|----|------|-----------|------------|-------------|
| 0 | Connect | C→S | No | Initial connection request |
| 1 | Disconnect | Both | No | Disconnect notification |
| 2 | Ping | Both | No | Latency check request |
| 3 | Pong | Both | No | Latency check response |

### Connect Packet

```java
class Connect {
    String username;
    UUID uuid;
    int protocolVersion;
    byte[] referralData;
    // ... auth fields
}
```

### Disconnect Packet

```java
class Disconnect {
    DisconnectReason reason;
    String message;
}
```

---

## Auth Packets (10-18)

| ID | Name | Direction | Description |
|----|------|-----------|-------------|
| 10 | AuthToken | C→S | Authentication token |
| 11 | ConnectAccept | S→C | Connection accepted |
| 12 | Status | S→C | Connection status |
| 13 | ServerReferral | S→C | Redirect to server |
| 14 | PlayerInfo | S→C | Player information |
| 15 | OnlineState | S→C | Online state update |

### AuthToken Packet

```java
class AuthToken {
    byte[] token;
    long timestamp;
    byte[] signature;
}
```

---

## Setup Packets (20-34)

| ID | Name | Direction | Compressed | Description |
|----|------|-----------|------------|-------------|
| 20 | WorldSettings | S→C | Yes | World configuration |
| 21 | AssetInitialize | S→C | Yes | Asset system init |
| 22 | GameReady | S→C | No | Game ready to play |
| 23 | ClientReady | C→S | No | Client ready |
| 24 | SetEntityId | S→C | No | Assign entity ID |
| 25 | SetWorldId | S→C | No | Assign world ID |

### WorldSettings Packet

```java
class WorldSettings {
    String worldName;
    long seed;
    GameMode defaultGameMode;
    WorldType worldType;
    // ... world configuration
}
```

---

## Asset Update Packets (40-85)

| ID | Name | Compressed | Description |
|----|------|------------|-------------|
| 40 | UpdateItems | Yes | Item definitions |
| 41 | UpdateBlockTypes | Yes | Block type definitions |
| 42 | UpdateEntityTypes | Yes | Entity type definitions |
| 50 | UpdateModels | Yes | 3D model updates |
| 51 | UpdateAnimations | Yes | Animation updates |
| 60 | UpdateSoundEvents | Yes | Sound event definitions |
| 70 | UpdateParticleSystems | Yes | Particle system definitions |
| 80 | UpdateRecipes | Yes | Crafting recipes |

---

## Player Packets (100-119)

| ID | Name | Direction | Compressed | Description |
|----|------|-----------|------------|-------------|
| 100 | ClientMovement | C→S | No | Player movement (fixed 153 bytes) |
| 101 | ServerMovement | S→C | No | Entity movement sync |
| 102 | ClientPlaceBlock | C→S | No | Block placement request |
| 103 | ClientBreakBlock | C→S | No | Block break request |
| 104 | MouseInteraction | C→S | No | Mouse click interaction |
| 105 | KeyInteraction | C→S | No | Keyboard interaction |
| 110 | ClientUseItem | C→S | No | Item use request |
| 111 | SwitchSlot | C→S | No | Hotbar slot change |

### ClientMovement Packet

Fixed-size 153 bytes for efficiency:

```java
class ClientMovement {
    long timestamp;          // 8 bytes
    Vector3d position;       // 24 bytes
    Vector3f rotation;       // 12 bytes
    Vector3d velocity;       // 24 bytes
    // ... movement state flags
}
```

### ClientPlaceBlock Packet

```java
class ClientPlaceBlock {
    Vector3i position;
    Direction face;
    int blockTypeId;
    RotationTuple rotation;
}
```

---

## World Packets (131-166)

| ID | Name | Direction | Compressed | Description |
|----|------|-----------|------------|-------------|
| 131 | SetChunk | S→C | Yes | Full chunk data |
| 132 | UnloadChunk | S→C | No | Chunk unload |
| 133 | ServerSetBlock | S→C | No | Single block update |
| 134 | ServerSetBlocks | S→C | Yes | Multiple block updates |
| 140 | UpdateTime | S→C | No | Time/weather update |
| 150 | EntityUpdates | S→C | Yes | Entity state batch |
| 151 | PlayAnimation | S→C | No | Play entity animation |
| 160 | SpawnEntity | S→C | Yes | Entity spawn |
| 161 | DespawnEntity | S→C | No | Entity despawn |

### SetChunk Packet

Compressed chunk data:

```java
class SetChunk {
    int chunkX, chunkZ;
    int[] heightmap;
    byte[] blockData;      // Compressed
    byte[] lightData;      // Compressed
    NBT[] blockEntities;
}
```

### ServerSetBlock Packet

```java
class ServerSetBlock {
    Vector3i position;
    int blockTypeId;
    int blockState;
    RotationTuple rotation;
}
```

### EntityUpdates Packet

Batched entity state updates:

```java
class EntityUpdates {
    EntityUpdate[] updates;
    
    class EntityUpdate {
        int entityId;
        Vector3d position;
        Vector3f rotation;
        byte flags;          // Movement state flags
        // ... component updates
    }
}
```

---

## Inventory Packets (170-179)

| ID | Name | Direction | Description |
|----|------|-----------|-------------|
| 170 | UpdatePlayerInventory | S→C | Full inventory sync |
| 171 | MoveItemStack | C→S | Move item between slots |
| 172 | InventoryUpdate | S→C | Partial inventory update |
| 175 | DropItem | C→S | Drop item request |

### UpdatePlayerInventory Packet

```java
class UpdatePlayerInventory {
    InventorySection[] sections;
    
    class InventorySection {
        int sectionId;
        ItemStack[] slots;
    }
}
```

---

## Window Packets (200-204)

| ID | Name | Direction | Description |
|----|------|-----------|-------------|
| 200 | OpenWindow | S→C | Open GUI window |
| 201 | CloseWindow | Both | Close window |
| 202 | UpdateWindow | S→C | Update window contents |
| 203 | WindowInteraction | C→S | Window click/action |

### OpenWindow Packet

```java
class OpenWindow {
    int windowId;
    String windowType;
    Message title;
    byte[] windowData;      // Window-specific data
}
```

---

## Interface Packets (210-234)

| ID | Name | Direction | Description |
|----|------|-----------|-------------|
| 210 | ChatMessage | C→S | Client chat message |
| 211 | ServerMessage | S→C | Server chat/system message |
| 215 | Notification | S→C | UI notification |
| 220 | ActionBar | S→C | Action bar text |
| 225 | Title | S→C | Title/subtitle display |
| 230 | Scoreboard | S→C | Scoreboard update |

### ChatMessage Packet

```java
class ChatMessage {
    String content;
    ChatChannel channel;
}
```

### ServerMessage Packet

```java
class ServerMessage {
    Message content;         // Formatted message
    MessageType type;        // CHAT, SYSTEM, ANNOUNCEMENT
    PlayerRef sender;        // Optional sender
}
```

---

## Interaction Packets (290-294)

| ID | Name | Direction | Description |
|----|------|-----------|-------------|
| 290 | PlayInteractionFor | S→C | Trigger interaction on client |
| 291 | SyncInteractionChains | S→C | Sync interaction state |
| 292 | InteractionComplete | C→S | Interaction finished |

### PlayInteractionFor Packet

```java
class PlayInteractionFor {
    int entityId;
    String interactionId;
    InteractionType type;
    byte[] interactionData;
}
```

---

## Important Plugin Packets

### Chat System

```java
// Send chat message to player
ServerMessage packet = new ServerMessage();
packet.content = Message.of("Hello, player!");
packet.type = MessageType.CHAT;
sendPacket(player, packet);
```

### Block Updates

```java
// Update block for all nearby players
ServerSetBlock packet = new ServerSetBlock();
packet.position = new Vector3i(x, y, z);
packet.blockTypeId = blockRegistry.getId("Stone");
broadcastPacket(world, position, packet);
```

### Entity Sync

```java
// Spawn entity for player
SpawnEntity packet = new SpawnEntity();
packet.entityId = entity.getNetworkId();
packet.entityType = entity.getType().getId();
packet.position = entity.getPosition();
sendPacket(player, packet);
```

---

## Serialization

### VarInt Encoding

Variable-length integer encoding:

```java
// Write VarInt
void writeVarInt(ByteBuf buf, int value) {
    while ((value & ~0x7F) != 0) {
        buf.writeByte((value & 0x7F) | 0x80);
        value >>>= 7;
    }
    buf.writeByte(value);
}

// Read VarInt
int readVarInt(ByteBuf buf) {
    int value = 0;
    int shift = 0;
    byte b;
    do {
        b = buf.readByte();
        value |= (b & 0x7F) << shift;
        shift += 7;
    } while ((b & 0x80) != 0);
    return value;
}
```

### String Encoding

```java
// Strings: VarInt length + UTF-8 bytes
void writeString(ByteBuf buf, String str) {
    byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
    writeVarInt(buf, bytes.length);
    buf.writeBytes(bytes);
}
```

### Compression

Zstd compression for applicable packets:

```java
byte[] compressed = Zstd.compress(data);
writeVarInt(buf, compressed.length);
writeVarInt(buf, data.length);  // Uncompressed size
buf.writeBytes(compressed);
```

---

## Packet Handler Pattern

### Server-Side Handler

```java
public class CustomPacketHandler extends SubPacketHandler {
    
    @Override
    public void handle(PacketContext ctx, CustomPacket packet) {
        Player player = ctx.getPlayer();
        
        // Process packet
        processPacket(player, packet);
        
        // Send response if needed
        ctx.sendPacket(new ResponsePacket(...));
    }
}
```

### Registration

```java
@Override
public void onSetup() {
    getPacketRegistry().register(
        CustomPacket.class,
        CustomPacket.ID,
        CustomPacketHandler::new
    );
}
```

---

## Source Files

- `com/hypixel/hytale/protocol/Packet.java`
- `com/hypixel/hytale/protocol/PacketRegistry.java`
- `com/hypixel/hytale/protocol/io/PacketIO.java`
- `com/hypixel/hytale/protocol/io/VarInt.java`
- `com/hypixel/hytale/protocol/packets/connection/*.java`
- `com/hypixel/hytale/protocol/packets/player/*.java`
- `com/hypixel/hytale/protocol/packets/world/*.java`
- `com/hypixel/hytale/protocol/packets/entities/*.java`
- `com/hypixel/hytale/server/core/io/handlers/game/GamePacketHandler.java`
