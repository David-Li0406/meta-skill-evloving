# Command Argument Types

Complete reference for all available argument types in the Hytale command system.

## Overview

Arguments are defined using the `ArgType` enum and wrapped in argument kind classes (`RequiredArg`, `OptionalArg`, `DefaultArg`, `FlagArg`). Each argument type handles parsing, validation, and tab completion automatically.

## Primitive Types

### STRING

Basic text input. Stops at whitespace unless quoted.

```java
RequiredArg<String> name = new RequiredArg<>("name", ArgType.STRING);
```

**Input examples:**
- `hello` → `"hello"`
- `"hello world"` → `"hello world"` (quoted for spaces)

**Tab completion:** None (accepts any input)

### INTEGER

Whole number, positive or negative.

```java
RequiredArg<Integer> count = new RequiredArg<>("count", ArgType.INTEGER);
DefaultArg<Integer> amount = new DefaultArg<>("amount", ArgType.INTEGER, 1);
```

**Input examples:**
- `42` → `42`
- `-10` → `-10`
- `3.14` → Error (not an integer)

**Validation:** Fails if input is not a valid integer

### FLOAT

Decimal number.

```java
RequiredArg<Float> speed = new RequiredArg<>("speed", ArgType.FLOAT);
```

**Input examples:**
- `3.14` → `3.14f`
- `42` → `42.0f`
- `-0.5` → `-0.5f`

### BOOLEAN

True/false value.

```java
RequiredArg<Boolean> enabled = new RequiredArg<>("enabled", ArgType.BOOLEAN);
```

**Input examples:**
- `true` → `true`
- `false` → `false`
- `yes` → `true`
- `no` → `false`
- `1` → `true`
- `0` → `false`

**Tab completion:** `true`, `false`

### GREEDY_STRING

Captures all remaining input as a single string. Must be the last argument.

```java
OptionalArg<String> reason = new OptionalArg<>("reason", ArgType.GREEDY_STRING);
```

**Input examples:**
- `/ban player This is the full reason` → `"This is the full reason"`

**Use cases:**
- Ban/kick reasons
- Chat messages
- Descriptions

## Entity Reference Types

### PLAYER_REF

Reference to an online player. Returns `PlayerRef` which must be resolved.

```java
RequiredArg<PlayerRef> target = new RequiredArg<>("target", ArgType.PLAYER_REF);

// In execute()
Player player = ctx.get(target).resolve();
if (player == null) {
    ctx.sendError("Player not found or offline");
    return;
}
```

**Input examples:**
- `PlayerName` → Exact match
- `Play` → Partial match (if unambiguous)
- `@s` → Self (command sender)
- `@r` → Random online player

**Tab completion:** Online player names

### ENTITY_TYPE_ID

Entity type identifier.

```java
RequiredArg<EntityTypeId> type = new RequiredArg<>("entity", ArgType.ENTITY_TYPE_ID);
```

**Input examples:**
- `hytale:zombie` → Full identifier
- `zombie` → Assumes `hytale:` namespace

**Tab completion:** All registered entity types

## Item and Block Types

### ITEM_ID

Item identifier.

```java
RequiredArg<ItemId> item = new RequiredArg<>("item", ArgType.ITEM_ID);
```

**Input examples:**
- `hytale:iron_sword`
- `iron_sword` → Assumes `hytale:` namespace

**Tab completion:** All registered item IDs

### BLOCK_ID

Block identifier.

```java
RequiredArg<BlockId> block = new RequiredArg<>("block", ArgType.BLOCK_ID);
```

**Input examples:**
- `hytale:stone`
- `grass` → Assumes `hytale:` namespace

**Tab completion:** All registered block IDs

## Position Types

### RELATIVE_INT_POSITION

Block position with relative coordinate support.

```java
RequiredArg<RelativeIntPosition> pos = new RequiredArg<>("position", ArgType.RELATIVE_INT_POSITION);

// In execute()
RelativeIntPosition relPos = ctx.get(pos);
IntVector3 absolutePos = relPos.resolve(ctx.getSenderPosition());
```

**Input examples:**
- `100 64 -200` → Absolute position
- `~ ~ ~` → Sender's position
- `~10 ~5 ~-10` → Offset from sender
- `~10 64 ~` → Mixed absolute and relative

**Tab completion:** `~` for each component

### RELATIVE_POSITION

Precise position (float) with relative coordinate support.

```java
RequiredArg<RelativePosition> pos = new RequiredArg<>("position", ArgType.RELATIVE_POSITION);

// In execute()
RelativePosition relPos = ctx.get(pos);
Vector3 absolutePos = relPos.resolve(ctx.getSenderPosition());
```

**Input examples:**
- `100.5 64.0 -200.5` → Absolute position
- `~0.5 ~1.5 ~0.5` → Offset with decimals

## World Types

### WORLD

World name reference.

```java
RequiredArg<World> world = new RequiredArg<>("world", ArgType.WORLD);
```

**Input examples:**
- `world_overworld`
- `my_custom_world`

**Tab completion:** Loaded world names

### DIRECTION

Cardinal or vertical direction.

```java
RequiredArg<Direction> dir = new RequiredArg<>("direction", ArgType.DIRECTION);
```

**Input examples:**
- `north`, `south`, `east`, `west`
- `up`, `down`
- `n`, `s`, `e`, `w`, `u`, `d` → Shortcuts

**Tab completion:** All direction names

## Time Types

### DURATION

Time duration with unit suffix.

```java
RequiredArg<Duration> duration = new RequiredArg<>("time", ArgType.DURATION);
DefaultArg<Duration> timeout = new DefaultArg<>("timeout", ArgType.DURATION, Duration.ofMinutes(5));
```

**Input examples:**
- `10s` → 10 seconds
- `5m` → 5 minutes
- `2h` → 2 hours
- `1d` → 1 day
- `30` → 30 seconds (default unit)

**Units:**
| Suffix | Unit |
|--------|------|
| `s` | Seconds |
| `m` | Minutes |
| `h` | Hours |
| `d` | Days |
| `w` | Weeks |

## Data Types

### JSON

Parses JSON object from input.

```java
RequiredArg<JsonObject> data = new RequiredArg<>("data", ArgType.JSON);
```

**Input examples:**
- `{"key":"value","count":42}`
- `{"nested":{"object":true}}`

**Use cases:**
- Complex data input
- Configuration overrides
- Entity NBT data

## Argument Kinds

### RequiredArg

Must be provided. Command fails if missing.

```java
private static final RequiredArg<String> NAME = 
    new RequiredArg<>("name", ArgType.STRING);

// Get value (never null for required args)
String name = ctx.get(NAME);
```

### OptionalArg

Can be omitted. Returns null if not provided.

```java
private static final OptionalArg<Integer> COUNT = 
    new OptionalArg<>("count", ArgType.INTEGER);

// Check and get
Integer count = ctx.get(COUNT); // May be null
if (count != null) {
    // Use count
}

// Or use getOrDefault
int count = ctx.getOrDefault(COUNT, 10);
```

### DefaultArg

Uses default value if not provided.

```java
private static final DefaultArg<Integer> AMOUNT = 
    new DefaultArg<>("amount", ArgType.INTEGER, 1);

// Always returns a value (default if not provided)
int amount = ctx.get(AMOUNT);
```

### FlagArg

Boolean flag with optional short form.

```java
private static final FlagArg SILENT = new FlagArg("silent", "s");
private static final FlagArg FORCE = new FlagArg("force", "f");

// Check if flag is present
boolean silent = ctx.has(SILENT);
boolean force = ctx.has(FORCE);
```

**Input examples:**
- `/cmd --silent` → silent = true
- `/cmd -s` → silent = true (short form)
- `/cmd -sf` → silent = true, force = true (combined)
- `/cmd` → silent = false

## Custom Argument Types

Create custom argument types by extending base classes:

```java
public class GameModeArg extends RequiredArg<GameMode> {
    
    public GameModeArg(String name) {
        super(name, ArgType.STRING);
    }
    
    @Override
    public GameMode parse(String input) throws ArgumentParseException {
        try {
            return GameMode.valueOf(input.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new ArgumentParseException("Invalid game mode: " + input);
        }
    }
    
    @Override
    public List<String> getSuggestions(CommandContext ctx, String partial) {
        return Arrays.stream(GameMode.values())
            .map(gm -> gm.name().toLowerCase())
            .filter(name -> name.startsWith(partial.toLowerCase()))
            .toList();
    }
}

// Usage
private static final GameModeArg MODE = new GameModeArg("mode");
```

## Argument Ordering

Arguments must be ordered correctly:

1. **Required arguments** first
2. **Optional/Default arguments** after required
3. **Flag arguments** can appear anywhere in input
4. **Greedy string** must be last

```java
public MyCommand() {
    super("example", "Example command");
    
    // Correct order
    addArg(REQUIRED_TARGET);      // Required first
    addArg(REQUIRED_ITEM);        // Required
    addArg(OPTIONAL_AMOUNT);      // Optional after required
    addArg(DEFAULT_COUNT);        // Default
    addArg(SILENT_FLAG);          // Flags
    addArg(GREEDY_REASON);        // Greedy last
}
```

## Validation Patterns

### Range Validation

```java
@Override
protected void execute(CommandContext ctx) {
    int amount = ctx.get(AMOUNT);
    
    if (amount < 1) {
        ctx.sendError("Amount must be at least 1");
        return;
    }
    
    if (amount > 64) {
        ctx.sendError("Amount cannot exceed 64");
        return;
    }
    
    // Proceed with valid amount
}
```

### Null Checking for Optional Args

```java
@Override
protected void execute(CommandContext ctx) {
    Player target = ctx.getOrDefault(TARGET, ctx.getPlayerSender().orElse(null));
    
    if (target == null) {
        ctx.sendError("Must specify a target or be a player");
        return;
    }
    
    // Proceed with target
}
```

### Permission-Based Argument Availability

```java
@Override
protected void execute(CommandContext ctx) {
    int amount = ctx.get(AMOUNT);
    
    // Limit for non-admins
    if (!ctx.hasPermission("admin.unlimited") && amount > 10) {
        ctx.sendError("You can only give up to 10 items");
        return;
    }
    
    // Proceed
}
```
