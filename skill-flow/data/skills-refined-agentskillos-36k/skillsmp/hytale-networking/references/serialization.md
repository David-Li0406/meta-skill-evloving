# Hytale Network Serialization Reference

Detailed reference for packet serialization in the Hytale protocol.

## Serialization Overview

Hytale uses a custom binary serialization protocol built on Netty's ByteBuf.

### Byte Order

All multi-byte values use **little-endian** byte order:

```java
buf.order(ByteOrder.LITTLE_ENDIAN);
```

---

## Primitive Types

### Fixed-Size Types

| Type | Size | Java Type | Read | Write |
|------|------|-----------|------|-------|
| Byte | 1 | byte | `readByte()` | `writeByte(v)` |
| Boolean | 1 | boolean | `readBoolean()` | `writeBoolean(v)` |
| Short | 2 | short | `readShortLE()` | `writeShortLE(v)` |
| Int | 4 | int | `readIntLE()` | `writeIntLE(v)` |
| Long | 8 | long | `readLongLE()` | `writeLongLE(v)` |
| Float | 4 | float | `readFloatLE()` | `writeFloatLE(v)` |
| Double | 8 | double | `readDoubleLE()` | `writeDoubleLE(v)` |

### Unsigned Types

| Type | Size | Range | Read | Write |
|------|------|-------|------|-------|
| UByte | 1 | 0-255 | `readUnsignedByte()` | `writeByte(v)` |
| UShort | 2 | 0-65535 | `readUnsignedShortLE()` | `writeShortLE(v)` |
| UInt | 4 | 0-4294967295 | `readUnsignedIntLE()` | `writeIntLE(v)` |

---

## Variable-Length Integers (VarInt)

Compact encoding for integers that are typically small.

### Encoding

```java
public static void writeVarInt(ByteBuf buf, int value) {
    while ((value & ~0x7F) != 0) {
        buf.writeByte((value & 0x7F) | 0x80);
        value >>>= 7;
    }
    buf.writeByte(value);
}
```

### Decoding

```java
public static int readVarInt(ByteBuf buf) {
    int value = 0;
    int shift = 0;
    byte b;
    do {
        b = buf.readByte();
        value |= (b & 0x7F) << shift;
        shift += 7;
        if (shift > 35) {
            throw new RuntimeException("VarInt too large");
        }
    } while ((b & 0x80) != 0);
    return value;
}
```

### Size by Value

| Value Range | Bytes |
|-------------|-------|
| 0 - 127 | 1 |
| 128 - 16383 | 2 |
| 16384 - 2097151 | 3 |
| 2097152 - 268435455 | 4 |
| 268435456 - 2147483647 | 5 |

---

## Variable-Length Long (VarLong)

Same principle as VarInt but for 64-bit values.

```java
public static void writeVarLong(ByteBuf buf, long value) {
    while ((value & ~0x7FL) != 0) {
        buf.writeByte((int)(value & 0x7F) | 0x80);
        value >>>= 7;
    }
    buf.writeByte((int)value);
}

public static long readVarLong(ByteBuf buf) {
    long value = 0;
    int shift = 0;
    byte b;
    do {
        b = buf.readByte();
        value |= (long)(b & 0x7F) << shift;
        shift += 7;
    } while ((b & 0x80) != 0);
    return value;
}
```

---

## Strings

Strings use VarInt length prefix with UTF-8 encoding.

### Writing

```java
public static void writeString(ByteBuf buf, String str) {
    byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
    writeVarInt(buf, bytes.length);
    buf.writeBytes(bytes);
}
```

### Reading

```java
public static String readString(ByteBuf buf) {
    int length = readVarInt(buf);
    byte[] bytes = new byte[length];
    buf.readBytes(bytes);
    return new String(bytes, StandardCharsets.UTF_8);
}
```

### With Maximum Length

```java
public static String readString(ByteBuf buf, int maxLength) {
    int length = readVarInt(buf);
    if (length > maxLength) {
        throw new RuntimeException("String too long: " + length);
    }
    byte[] bytes = new byte[length];
    buf.readBytes(bytes);
    return new String(bytes, StandardCharsets.UTF_8);
}
```

---

## UUID

UUIDs are serialized as two longs (16 bytes).

```java
public static void writeUUID(ByteBuf buf, UUID uuid) {
    buf.writeLongLE(uuid.getMostSignificantBits());
    buf.writeLongLE(uuid.getLeastSignificantBits());
}

public static UUID readUUID(ByteBuf buf) {
    long msb = buf.readLongLE();
    long lsb = buf.readLongLE();
    return new UUID(msb, lsb);
}
```

---

## Vectors

### Vector3i (Block Position)

```java
public static void writeVector3i(ByteBuf buf, Vector3i vec) {
    buf.writeIntLE(vec.x);
    buf.writeIntLE(vec.y);
    buf.writeIntLE(vec.z);
}

public static Vector3i readVector3i(ByteBuf buf) {
    return new Vector3i(
        buf.readIntLE(),
        buf.readIntLE(),
        buf.readIntLE()
    );
}
```

### Vector3f (Rotation/Direction)

```java
public static void writeVector3f(ByteBuf buf, Vector3f vec) {
    buf.writeFloatLE(vec.x);
    buf.writeFloatLE(vec.y);
    buf.writeFloatLE(vec.z);
}

public static Vector3f readVector3f(ByteBuf buf) {
    return new Vector3f(
        buf.readFloatLE(),
        buf.readFloatLE(),
        buf.readFloatLE()
    );
}
```

### Vector3d (Position)

```java
public static void writeVector3d(ByteBuf buf, Vector3d vec) {
    buf.writeDoubleLE(vec.x);
    buf.writeDoubleLE(vec.y);
    buf.writeDoubleLE(vec.z);
}

public static Vector3d readVector3d(ByteBuf buf) {
    return new Vector3d(
        buf.readDoubleLE(),
        buf.readDoubleLE(),
        buf.readDoubleLE()
    );
}
```

---

## Arrays and Collections

### Fixed-Length Array

```java
// Write
buf.writeIntLE(array.length);
for (T item : array) {
    writeItem(buf, item);
}

// Read
int length = buf.readIntLE();
T[] array = new T[length];
for (int i = 0; i < length; i++) {
    array[i] = readItem(buf);
}
```

### VarInt-Length Array

```java
// Write
writeVarInt(buf, array.length);
for (T item : array) {
    writeItem(buf, item);
}

// Read
int length = readVarInt(buf);
T[] array = new T[length];
for (int i = 0; i < length; i++) {
    array[i] = readItem(buf);
}
```

### Byte Array

```java
// Write
writeVarInt(buf, bytes.length);
buf.writeBytes(bytes);

// Read
int length = readVarInt(buf);
byte[] bytes = new byte[length];
buf.readBytes(bytes);
```

---

## Optional Values

### Nullable with Boolean Flag

```java
// Write
buf.writeBoolean(value != null);
if (value != null) {
    writeValue(buf, value);
}

// Read
if (buf.readBoolean()) {
    value = readValue(buf);
} else {
    value = null;
}
```

### Optional with VarInt (-1 for null)

```java
// Write
if (value != null) {
    writeVarInt(buf, value);
} else {
    writeVarInt(buf, -1);
}

// Read
int v = readVarInt(buf);
value = (v == -1) ? null : v;
```

---

## Enums

Enums typically serialized as VarInt ordinal.

```java
// Write
writeVarInt(buf, enumValue.ordinal());

// Read
EnumType value = EnumType.values()[readVarInt(buf)];
```

### With Validation

```java
public static <T extends Enum<T>> T readEnum(ByteBuf buf, Class<T> enumClass) {
    int ordinal = readVarInt(buf);
    T[] values = enumClass.getEnumConstants();
    if (ordinal < 0 || ordinal >= values.length) {
        throw new RuntimeException("Invalid enum ordinal: " + ordinal);
    }
    return values[ordinal];
}
```

---

## ItemStack Serialization

```java
public static void writeItemStack(ByteBuf buf, ItemStack stack) {
    if (stack == null || stack.isEmpty()) {
        buf.writeBoolean(false);
        return;
    }
    buf.writeBoolean(true);
    writeVarInt(buf, stack.getItemId());
    buf.writeByte(stack.getCount());
    writeVarInt(buf, stack.getDurability());
    writeNBT(buf, stack.getTag());
}

public static ItemStack readItemStack(ByteBuf buf) {
    if (!buf.readBoolean()) {
        return ItemStack.EMPTY;
    }
    int itemId = readVarInt(buf);
    int count = buf.readByte();
    int durability = readVarInt(buf);
    NBTCompound tag = readNBT(buf);
    return new ItemStack(itemId, count, durability, tag);
}
```

---

## NBT (Named Binary Tag)

NBT uses a tag-type prefix system.

### Tag Types

| ID | Type | Description |
|----|------|-------------|
| 0 | End | End of compound |
| 1 | Byte | Single byte |
| 2 | Short | 16-bit integer |
| 3 | Int | 32-bit integer |
| 4 | Long | 64-bit integer |
| 5 | Float | 32-bit float |
| 6 | Double | 64-bit float |
| 7 | ByteArray | Byte array |
| 8 | String | UTF-8 string |
| 9 | List | Typed list |
| 10 | Compound | Key-value map |
| 11 | IntArray | Int array |
| 12 | LongArray | Long array |

### Compound Writing

```java
public static void writeNBT(ByteBuf buf, NBTCompound compound) {
    if (compound == null) {
        buf.writeByte(0);  // End tag = no data
        return;
    }
    buf.writeByte(10);     // Compound tag
    writeString(buf, "");  // Root name (empty)
    for (Map.Entry<String, NBTTag> entry : compound.entrySet()) {
        writeTag(buf, entry.getKey(), entry.getValue());
    }
    buf.writeByte(0);      // End tag
}
```

---

## Compression

### Zstd Compression

Used for large packets like chunks and asset updates.

```java
public static byte[] compress(byte[] data) {
    return Zstd.compress(data);
}

public static byte[] decompress(byte[] compressed, int uncompressedSize) {
    byte[] output = new byte[uncompressedSize];
    Zstd.decompress(output, compressed);
    return output;
}
```

### Compressed Packet Format

```
[VarInt packetId]
[VarInt compressedSize]
[VarInt uncompressedSize]
[byte[] compressedData]
```

### Reading Compressed Data

```java
int compressedSize = readVarInt(buf);
int uncompressedSize = readVarInt(buf);
byte[] compressed = new byte[compressedSize];
buf.readBytes(compressed);
byte[] data = decompress(compressed, uncompressedSize);
```

---

## Packet Structure

### Standard Packet

```
[VarInt packetId]
[... packet data ...]
```

### Compressed Packet

```
[VarInt packetId]
[VarInt compressedLength]
[VarInt uncompressedLength]
[byte[] compressedData]
```

### Packet with Length Prefix

```
[VarInt totalLength]
[VarInt packetId]
[... packet data ...]
```

---

## PacketIO Helper Class

The `PacketIO` class provides convenience methods:

```java
public class PacketIO {
    // Primitives
    public static void writeByte(ByteBuf buf, int value);
    public static int readByte(ByteBuf buf);
    
    // VarInt
    public static void writeVarInt(ByteBuf buf, int value);
    public static int readVarInt(ByteBuf buf);
    
    // Strings
    public static void writeString(ByteBuf buf, String str);
    public static String readString(ByteBuf buf);
    
    // Vectors
    public static void writeVector3i(ByteBuf buf, Vector3i vec);
    public static Vector3i readVector3i(ByteBuf buf);
    
    // ItemStack
    public static void writeItemStack(ByteBuf buf, ItemStack stack);
    public static ItemStack readItemStack(ByteBuf buf);
    
    // NBT
    public static void writeNBT(ByteBuf buf, NBTCompound nbt);
    public static NBTCompound readNBT(ByteBuf buf);
    
    // Compression
    public static byte[] compress(byte[] data);
    public static byte[] decompress(byte[] data, int size);
}
```

---

## Custom Packet Example

```java
public class CustomPacket implements Packet {
    public static final int ID = 500;
    
    private String message;
    private Vector3d position;
    private int[] values;
    
    @Override
    public void write(ByteBuf buf) {
        PacketIO.writeString(buf, message);
        PacketIO.writeVector3d(buf, position);
        PacketIO.writeVarInt(buf, values.length);
        for (int v : values) {
            PacketIO.writeVarInt(buf, v);
        }
    }
    
    @Override
    public void read(ByteBuf buf) {
        message = PacketIO.readString(buf);
        position = PacketIO.readVector3d(buf);
        int count = PacketIO.readVarInt(buf);
        values = new int[count];
        for (int i = 0; i < count; i++) {
            values[i] = PacketIO.readVarInt(buf);
        }
    }
    
    @Override
    public int getId() {
        return ID;
    }
}
```

---

## Source Files

- `com/hypixel/hytale/protocol/io/PacketIO.java`
- `com/hypixel/hytale/protocol/io/VarInt.java`
- `com/hypixel/hytale/protocol/Packet.java`
- `com/hypixel/hytale/protocol/PacketRegistry.java`
- `com/hypixel/hytale/nbt/NBTCompound.java`
- `com/hypixel/hytale/nbt/NBTTag.java`
