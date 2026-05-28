# Registry Patterns

Advanced patterns for using Hytale plugin registries.

## Registry Architecture

All plugin registries implement `IRegistry` with automatic cleanup:

```java
public interface IRegistry {
    void shutdown();
}
```

Registries are proxy wrappers that:
1. Track all registrations
2. Forward to server registries
3. Automatically unregister on plugin shutdown

## Command Registry

### Basic Command

```java
public class GreetCommand extends Command {
    public GreetCommand() {
        super("greet", "Greet a player");
        setAliases("hello", "hi");
        setPermission("myplugin.greet");
        
        addArg(EntityArg.player("target"));
        addArg(StringArg.word("message").optional());
    }
    
    @Override
    public void execute(CommandContext ctx) {
        Player target = ctx.get("target");
        String message = ctx.getOrDefault("message", "Hello!");
        target.sendMessage(message);
    }
}
```

### Argument Types

| Type | Class | Description |
|------|-------|-------------|
| Player | `EntityArg.player()` | Online player |
| Entity | `EntityArg.entity()` | Any entity |
| Integer | `IntArg.number()` | Integer with range |
| Float | `FloatArg.number()` | Float with range |
| String | `StringArg.word()` | Single word |
| Greedy String | `StringArg.greedy()` | Rest of input |
| Boolean | `BoolArg.bool()` | true/false |
| Position | `PositionArg.position()` | World coordinates |
| Block Type | `BlockTypeArg.blockType()` | Block type ID |
| Item Type | `ItemArg.item()` | Item type ID |

### Subcommands

```java
public class AdminCommand extends Command {
    public AdminCommand() {
        super("admin", "Admin commands");
        
        addSubCommand(new BanSubCommand());
        addSubCommand(new KickSubCommand());
        addSubCommand(new TeleportSubCommand());
    }
}

public class BanSubCommand extends Command {
    public BanSubCommand() {
        super("ban", "Ban a player");
        addArg(EntityArg.player("target"));
        addArg(StringArg.greedy("reason").optional());
    }
    
    @Override
    public void execute(CommandContext ctx) {
        // /admin ban <player> [reason]
    }
}
```

## Event Registry

### Registration Types

```java
// Global - receives ALL events of this type
getEventRegistry().registerGlobal(EventClass.class, handler);

// Keyed - receives events with specific key
getEventRegistry().register(EventClass.class, keyValue, handler);

// Unhandled - receives events no keyed handler processed
getEventRegistry().registerUnhandled(EventClass.class, handler);

// Priority-based
getEventRegistry().registerGlobal(EventPriority.FIRST, EventClass.class, handler);
getEventRegistry().register(EventPriority.LAST, EventClass.class, key, handler);
```

### Priority Order

```java
public enum EventPriority {
    FIRST((short)-21844),   // Runs earliest
    EARLY((short)-10922),
    NORMAL((short)0),       // Default
    LATE((short)10922),
    LAST((short)21844);     // Runs latest
}
```

### Async Events

```java
// For IAsyncEvent types
getEventRegistry().registerAsyncGlobal(
    AsyncEventClass.class,
    future -> future.thenApply(event -> {
        // Process async event
        return event;
    })
);
```

### Event Cancellation

```java
private void onBlockBreak(BreakBlockEvent event) {
    if (shouldPrevent(event)) {
        event.setCancelled(true);
    }
}
```

### Unregistration

```java
private EventRegistration registration;

@Override
protected void setup() {
    registration = getEventRegistry().registerGlobal(SomeEvent.class, this::handler);
}

public void disableFeature() {
    if (registration != null) {
        registration.unregister();
        registration = null;
    }
}
```

## Entity Store Registry (ECS)

### Component Registration

```java
// Simple component
ComponentType<EntityStore, MyComponent> type = 
    getEntityStoreRegistry().registerComponent(
        MyComponent.class,
        MyComponent::new  // Factory
    );

// With serialization
ComponentType<EntityStore, MyComponent> type = 
    getEntityStoreRegistry().registerComponent(
        MyComponent.class,
        "myComponentId",    // Unique ID for serialization
        MyComponent.CODEC   // Serialization codec
    );

// With custom serializer
ComponentType<EntityStore, MyComponent> type = 
    getEntityStoreRegistry().registerComponent(
        MyComponent.class,
        "myComponentId",
        MyComponent.CODEC,
        MyComponent::new,           // Factory
        MyComponent::copyFrom       // Copy function
    );
```

### Component Class Pattern

```java
public class MyComponent implements Component<EntityStore> {
    public static final BuilderCodec<MyComponent> CODEC = BuilderCodec.builder(
        Codec.INT.required().fieldOf("Value"),
        Codec.STRING.optionalFieldOf("Name", "default")
    ).constructor(MyComponent::new);
    
    private int value;
    private String name;
    
    public MyComponent() {
        this(0, "default");
    }
    
    public MyComponent(int value, String name) {
        this.value = value;
        this.name = name;
    }
    
    // Getters and setters
    public int getValue() { return value; }
    public void setValue(int value) { this.value = value; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
```

### System Registration

```java
// Register a system
getEntityStoreRegistry().registerSystem(new MyTickSystem());

// System with dependencies
getEntityStoreRegistry().registerSystem(new MyEventSystem(), SystemPhase.PRE_TICK);
```

### System Class Pattern

```java
public class MyTickSystem extends TickSystem<EntityStore> {
    private ComponentAccess<EntityStore, MyComponent> myComponents;
    private ComponentAccess<EntityStore, TransformComponent> transforms;
    
    @Override
    protected void register(Store<EntityStore> store) {
        myComponents = registerComponent(MyComponent.class);
        transforms = registerComponent(TransformComponent.class);
    }
    
    @Override
    public void tick(
        int index,
        ArchetypeChunk<EntityStore> chunk,
        Store<EntityStore> store,
        CommandBuffer<EntityStore> buffer
    ) {
        MyComponent myComp = myComponents.get(chunk, index);
        TransformComponent transform = transforms.get(chunk, index);
        
        // Process entity
        myComp.setValue(myComp.getValue() + 1);
    }
}
```

### Event System Pattern

```java
public class MyDamageHandler extends EntityEventSystem<EntityStore, Damage> {
    private ComponentAccess<EntityStore, MyComponent> myComponents;
    
    public MyDamageHandler() {
        super(Damage.class);
    }
    
    @Override
    protected void register(Store<EntityStore> store) {
        myComponents = registerComponent(MyComponent.class);
    }
    
    @Override
    public void handle(
        int index,
        ArchetypeChunk<EntityStore> chunk,
        Store<EntityStore> store,
        CommandBuffer<EntityStore> buffer,
        Damage damage
    ) {
        MyComponent comp = myComponents.getOptional(chunk, index);
        if (comp != null && comp.getValue() > 100) {
            damage.setCancelled(true); // Prevent damage
        }
    }
}
```

## Chunk Store Registry

For per-chunk data:

```java
ComponentType<ChunkStore, MyChunkData> chunkDataType = 
    getChunkStoreRegistry().registerComponent(
        MyChunkData.class,
        "myChunkData",
        MyChunkData.CODEC
    );
```

## Codec Registry

Register custom serializable types:

```java
// Register custom interaction
getCodecRegistry(Interaction.CODEC).register(
    "MyInteraction",
    MyInteraction.class,
    MyInteraction.CODEC
);

// Register custom NPC action
getCodecRegistry(Action.CODEC).register(
    "MyAction",
    MyAction.class,
    MyAction.CODEC
);

// Register custom sensor
getCodecRegistry(Sensor.CODEC).register(
    "MySensor",
    MySensor.class,
    MySensor.CODEC
);
```

## Asset Registry

Register custom asset stores:

```java
@Override
protected void setup() {
    HytaleAssetStore<String, MyAsset, DefaultAssetMap<String, MyAsset>> store = 
        new HytaleAssetStore<>(
            MyAsset.class,
            "myassets",           // Directory name
            ".myasset",           // File extension
            MyAsset.CODEC,
            DefaultAssetMap::new
        );
    
    getAssetRegistry().register(store);
}
```

## Task Registry

Schedule async tasks:

```java
// One-time task
getTaskRegistry().runAsync(() -> {
    // Runs on thread pool
    loadExternalData();
});

// Delayed task
getTaskRegistry().runLater(() -> {
    // Runs after delay
}, 100, TimeUnit.MILLISECONDS);

// Repeating task
getTaskRegistry().scheduleAtFixedRate(() -> {
    // Runs every interval
}, 0, 1, TimeUnit.SECONDS);
```

## Block State Registry

Register custom block state types:

```java
BlockStateType<Integer> myStateType = 
    getBlockStateRegistry().register(
        "my_rotation",
        Integer.class,
        0,  // Default value
        Codec.INT
    );
```

## Entity Registry

Register custom entity types:

```java
@Override
protected void setup() {
    getEntityRegistry().register(
        "my_entity",
        MyEntity.class,
        MyEntity::new,
        MyEntity.CODEC
    );
}
```

## Pattern: Lazy Initialization

```java
public class MyPlugin extends JavaPlugin {
    private ComponentType<EntityStore, MyComponent> myComponentType;
    
    @Override
    protected void setup() {
        // Registration happens once during setup
        myComponentType = getEntityStoreRegistry().registerComponent(
            MyComponent.class,
            MyComponent::new
        );
    }
    
    // Accessor for other classes
    public ComponentType<EntityStore, MyComponent> getMyComponentType() {
        return myComponentType;
    }
}
```

## Pattern: Feature Toggles

```java
public class MyPlugin extends JavaPlugin {
    private final Config<MyConfig> config = withConfig(MyConfig.CODEC);
    
    @Override
    protected void setup() {
        MyConfig cfg = config.get();
        
        if (cfg.enableFeatureA()) {
            getCommandRegistry().registerCommand(new FeatureACommand());
            getEventRegistry().registerGlobal(SomeEvent.class, this::handleFeatureA);
        }
        
        if (cfg.enableFeatureB()) {
            getEntityStoreRegistry().registerSystem(new FeatureBSystem());
        }
    }
}
```

## Pattern: Cross-Plugin Communication

```java
// Plugin A exposes API
public class PluginA extends JavaPlugin {
    private static PluginA instance;
    
    public static PluginA getInstance() {
        return instance;
    }
    
    @Override
    protected void start() {
        instance = this;
    }
    
    public void doSomething(Player player) {
        // Public API method
    }
}

// Plugin B uses it (with dependency declared)
public class PluginB extends JavaPlugin {
    @Override
    protected void start() {
        PluginA pluginA = PluginA.getInstance();
        if (pluginA != null) {
            pluginA.doSomething(player);
        }
    }
}
```
