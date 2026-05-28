# Plugin Lifecycle Deep Dive

Comprehensive documentation of the Hytale plugin lifecycle system.

## Lifecycle State Machine

```
       ┌─────────────────────────────────────────────────────┐
       │                                                     │
       ▼                                                     │
    ┌──────┐    ┌───────┐    ┌───────┐    ┌─────────┐       │
    │ NONE │───▶│ SETUP │───▶│ START │───▶│ ENABLED │       │
    └──────┘    └───────┘    └───────┘    └─────────┘       │
                                               │            │
                                               ▼            │
                                          ┌──────────┐      │
                                          │ SHUTDOWN │      │
                                          └──────────┘      │
                                               │            │
                                               ▼            │
                                          ┌──────────┐      │
                                          │ DISABLED │──────┘
                                          └──────────┘
                                            (reload)
```

## State Descriptions

### NONE
- Initial state after plugin instantiation
- Constructor has been called
- Plugin is not yet participating in server lifecycle

### SETUP
- `preLoad()` has completed (config files loaded)
- `setup()` is being or has been called
- Register: commands, events, components, systems, codecs
- **DO NOT**: Access game state, other plugins, or spawn entities

### START
- `start()` is being or has been called
- All plugins have completed setup phase
- Safe to interact with other plugins and game state
- Initialize runtime features, start tasks

### ENABLED
- Plugin is fully operational
- Normal runtime state
- Processing events, commands, and systems

### SHUTDOWN
- `shutdown()` is being called
- Cleanup resources, save data
- Called in **reverse** load order
- Cancel tasks, close connections

### DISABLED
- Plugin is no longer active
- All registrations have been cleaned up
- Can transition back to SETUP on reload

## Lifecycle Methods

### preLoad() - Async Configuration

```java
@Override
protected CompletableFuture<Void> preLoad() {
    return CompletableFuture.runAsync(() -> {
        // Load configuration files
        // This runs on a separate thread
        loadExternalData();
    });
}
```

**Purpose**: Load configuration and external data asynchronously before setup.

**Called**: Before `setup()`, on async thread pool

**Default**: Loads plugin config files via `withConfig()`

### setup() - Registration Phase

```java
@Override
protected void setup() {
    // Register commands
    getCommandRegistry().registerCommand(new MyCommand());
    
    // Register events
    getEventRegistry().registerGlobal(PlayerConnectEvent.class, this::onConnect);
    
    // Register ECS components
    getEntityStoreRegistry().registerComponent(MyComponent.class, MyComponent::new);
    
    // Register ECS systems
    getEntityStoreRegistry().registerSystem(new MySystem());
    
    // Register codecs
    getCodecRegistry(Interaction.CODEC).register("MyType", MyType.class, MyType.CODEC);
}
```

**Purpose**: Register all plugin components with the server.

**Called**: After `preLoad()` completes, on main thread

**Requirements**:
- DO NOT access game state (worlds, entities, players)
- DO NOT interact with other plugins
- DO NOT spawn entities or modify blocks

### start() - Activation Phase

```java
@Override
protected void start() {
    // Access other plugins
    Optional<PluginBase> otherPlugin = getPluginManager()
        .getPlugin(PluginIdentifier.of("Group", "Name"));
    
    // Start scheduled tasks
    scheduler.scheduleAtFixedRate(this::tick, 0, 50, TimeUnit.MILLISECONDS);
    
    // Initialize game state
    World world = HytaleServer.get().getUniverse().getWorld("main");
    if (world != null) {
        initializeWorld(world);
    }
    
    getLogger().atInfo().log("Plugin started successfully!");
}
```

**Purpose**: Activate plugin features and integrate with game.

**Called**: After ALL plugins complete `setup()`, on main thread

**Allowed**:
- Access and modify game state
- Interact with other plugins
- Spawn entities, modify blocks
- Start background tasks

### shutdown() - Cleanup Phase

```java
@Override
protected void shutdown() {
    // Cancel scheduled tasks
    if (tickTask != null) {
        tickTask.cancel(false);
    }
    
    // Save data
    savePlayerData();
    
    // Close connections
    if (databaseConnection != null) {
        databaseConnection.close();
    }
    
    getLogger().atInfo().log("Plugin shutdown complete");
}
```

**Purpose**: Clean up resources before plugin disables.

**Called**: Before disable, in REVERSE load order

**Requirements**:
- Cancel all running tasks
- Save persistent data
- Close external connections
- Release resources

## Internal Lifecycle Methods

These are called by `PluginManager` and wrap the public lifecycle methods:

### setup0()

```java
void setup0() {
    try {
        setState(PluginState.SETUP);
        setup();
    } catch (Exception e) {
        logger.error("Error during setup", e);
        // Plugin may be disabled
    }
}
```

### start0()

```java
void start0() {
    try {
        setState(PluginState.START);
        start();
        setState(PluginState.ENABLED);
        
        // Register embedded asset pack if declared
        if (manifest.includesAssetPack()) {
            registerEmbeddedAssetPack();
        }
    } catch (Exception e) {
        logger.error("Error during start", e);
    }
}
```

### shutdown0(boolean shutdown)

```java
void shutdown0(boolean shutdown) {
    try {
        setState(PluginState.SHUTDOWN);
        shutdown();
    } finally {
        cleanup(shutdown);
        setState(PluginState.DISABLED);
    }
}
```

### cleanup(boolean shutdown)

Automatically unregisters all plugin registrations:

```java
void cleanup(boolean shutdown) {
    commandRegistry.shutdown();
    eventRegistry.shutdown();
    taskRegistry.shutdown();
    blockStateRegistry.shutdown();
    entityRegistry.shutdown();
    clientFeatureRegistry.shutdown();
    assetRegistry.shutdown();
    entityStoreRegistry.shutdown();
    chunkStoreRegistry.shutdown();
    // All codec registries...
}
```

## Load Order

Plugins are loaded in topological order based on:

1. **Required Dependencies** - Must load before dependent
2. **Optional Dependencies** - Load before if present
3. **LoadBefore** - This plugin loads before target
4. **Classpath vs External** - Classpath plugins load first

### Dependency Resolution

```java
// In PendingLoadPlugin.calculateLoadOrder()
for (PluginIdentifier dependency : manifest.getDependencies().keySet()) {
    addDependency(dependency, true);  // Required
}

for (PluginIdentifier dependency : manifest.getOptionalDependencies().keySet()) {
    addDependency(dependency, false); // Optional
}

for (PluginIdentifier target : manifest.getLoadBefore().keySet()) {
    // Target depends on this (load this first)
    target.addDependency(this.identifier, false);
}
```

### Circular Dependency Detection

```
MissingPluginDependencyException: Circular dependency detected:
  PluginA -> PluginB -> PluginC -> PluginA
```

## Hot Reload Support

Plugins can be reloaded at runtime:

```
/plugin reload MyPlugin
```

This triggers:
1. `shutdown()` called
2. Plugin JAR reloaded
3. New instance created
4. `preLoad()` -> `setup()` -> `start()`

### Reload-Safe Patterns

```java
public class MyPlugin extends JavaPlugin {
    private static Map<UUID, PlayerData> playerData = new ConcurrentHashMap<>();
    
    @Override
    protected void start() {
        // Restore data from previous instance
        // (static fields persist across reloads)
    }
    
    @Override
    protected void shutdown() {
        // Save data that should persist
        playerData.forEach(this::savePlayerData);
    }
}
```

## Event: PluginSetupEvent

Fired when a plugin completes setup:

```java
@Override
protected void setup() {
    getEventRegistry().register(
        PluginSetupEvent.class, 
        SomeOtherPlugin.class, 
        this::onOtherPluginSetup
    );
}

private void onOtherPluginSetup(PluginSetupEvent event) {
    // React to another plugin finishing setup
    SomeOtherPlugin plugin = (SomeOtherPlugin) event.getPlugin();
}
```

## Debugging Lifecycle Issues

### Enable Debug Logging

```java
@Override
protected void setup() {
    getLogger().atFine().log("Entering setup phase");
    getLogger().atFine().log("Registering %d commands", commands.size());
}
```

### State Inspection

```java
// Check current state
PluginState state = getState();
if (state == PluginState.ENABLED) {
    // Plugin is fully operational
}
```

### Lifecycle Timing

```java
private long setupStartTime;

@Override
protected void setup() {
    setupStartTime = System.currentTimeMillis();
    // ... registrations ...
    getLogger().atInfo().log("Setup completed in %dms", 
        System.currentTimeMillis() - setupStartTime);
}
```
