# Command Implementation Patterns

Advanced patterns and best practices for implementing Hytale commands.

## Command Base Classes

### CommandBase

The simplest command base. Use for general-purpose commands.

```java
public class PingCommand extends CommandBase {
    
    public PingCommand() {
        super("ping", "Check server latency");
    }
    
    @Override
    protected void execute(CommandContext ctx) {
        ctx.sendSuccess("Pong!");
    }
}
```

**When to use:**
- Simple commands without special requirements
- Commands that work from console and player
- Commands that don't need world context

### AbstractPlayerCommand

Enforces player-only execution. The execute method receives 5 parameters including Store, Ref, PlayerRef, and World.

```java
import com.hypixel.hytale.component.Ref;
import com.hypixel.hytale.component.Store;
import com.hypixel.hytale.server.core.command.system.CommandContext;
import com.hypixel.hytale.server.core.command.system.basecommands.AbstractPlayerCommand;
import com.hypixel.hytale.server.core.entity.entities.Player;
import com.hypixel.hytale.server.core.universe.PlayerRef;
import com.hypixel.hytale.server.core.universe.world.World;
import com.hypixel.hytale.server.core.universe.world.storage.EntityStore;
import javax.annotation.Nonnull;

public class InventoryCommand extends AbstractPlayerCommand {
    
    public InventoryCommand() {
        super("inventory", "View your inventory");
    }
    
    @Override
    protected void execute(
        @Nonnull CommandContext context,
        @Nonnull Store<EntityStore> store,
        @Nonnull Ref<EntityStore> ref,
        @Nonnull PlayerRef playerRef,
        @Nonnull World world
    ) {
        // Access player data through PlayerRef or get Player component
        world.execute(() -> {
            Player player = store.getComponent(ref, Player.getComponentType());
            context.sendMessage("Username: " + playerRef.getUsername());
        });
    }
}
```

**When to use:**
- Commands that only make sense for players
- Commands requiring player state (inventory, position, etc.)
- Commands with player-specific actions

**Error handling:** Automatically sends error if console tries to execute

### AbstractWorldCommand

Requires world context. Works from console if world is specified.

```java
public class WeatherCommand extends AbstractWorldCommand {
    
    private static final RequiredArg<String> WEATHER = 
        new RequiredArg<>("weather", ArgType.STRING);
    
    public WeatherCommand() {
        super("weather", "Set world weather");
        addArg(WEATHER);
    }
    
    @Override
    protected void execute(CommandContext ctx, World world) {
        String weather = ctx.get(WEATHER);
        world.setWeather(Weather.valueOf(weather.toUpperCase()));
        ctx.sendSuccess("Weather set to " + weather + " in " + world.getName());
    }
}
```

**World resolution:**
1. Player sender → Uses player's current world
2. Console → Must specify world via `--world` flag or world argument
3. No world context → Error

### AbstractTargetPlayerCommand

Commands that act on another player. Auto-completes player names.

```java
public class KickCommand extends AbstractTargetPlayerCommand {
    
    private static final OptionalArg<String> REASON = 
        new OptionalArg<>("reason", ArgType.GREEDY_STRING);
    
    public KickCommand() {
        super("kick", "Kick a player from the server");
        addArg(REASON);
    }
    
    @Override
    protected void execute(CommandContext ctx, Player target) {
        String reason = ctx.getOrDefault(REASON, "Kicked by administrator");
        target.kick(reason);
        ctx.sendSuccess("Kicked " + target.getName());
    }
}
```

**Target resolution:**
- First argument is always the target player
- Supports partial name matching
- Supports `@s` (self) and `@r` (random)

### AbstractAsyncCommand

For operations that shouldn't block the main thread.

```java
public class DatabaseQueryCommand extends AbstractAsyncCommand {
    
    private static final RequiredArg<String> QUERY = 
        new RequiredArg<>("query", ArgType.GREEDY_STRING);
    
    public DatabaseQueryCommand() {
        super("dbquery", "Execute database query");
        addArg(QUERY);
    }
    
    @Override
    protected CompletableFuture<Void> executeAsync(CommandContext ctx) {
        String query = ctx.get(QUERY);
        
        return CompletableFuture.runAsync(() -> {
            ctx.sendMessage("Executing query...");
            
            try {
                List<Result> results = database.query(query);
                ctx.sendSuccess("Found " + results.size() + " results");
            } catch (SQLException e) {
                ctx.sendError("Query failed: " + e.getMessage());
            }
        });
    }
}
```

**When to use:**
- Database operations
- File I/O operations
- Network requests
- Long computations

**Thread safety:**
- `ctx.sendMessage()` is thread-safe
- World/entity modifications should be scheduled back to main thread

### AbstractCommandCollection

Groups related subcommands under a parent command.

```java
public class WarpCommands extends AbstractCommandCollection {
    
    private final WarpManager warpManager;
    
    public WarpCommands(WarpManager warpManager) {
        super("warp", "Warp management commands");
        this.warpManager = warpManager;
        
        addSubCommand(new SetSubCommand());
        addSubCommand(new DeleteSubCommand());
        addSubCommand(new ListSubCommand());
        addSubCommand(new TeleportSubCommand());
    }
    
    private class SetSubCommand extends AbstractPlayerCommand {
        
        private static final RequiredArg<String> NAME = 
            new RequiredArg<>("name", ArgType.STRING);
        
        public SetSubCommand() {
            super("set", "Create a warp at your location");
            addArg(NAME);
        }
        
        @Override
        protected void execute(
            @Nonnull CommandContext context,
            @Nonnull Store<EntityStore> store,
            @Nonnull Ref<EntityStore> ref,
            @Nonnull PlayerRef playerRef,
            @Nonnull World world
        ) {
            String name = context.get(NAME);
            world.execute(() -> {
                Player player = store.getComponent(ref, Player.getComponentType());
                warpManager.setWarp(name, player.getTransform().getPosition());
                context.sendSuccess("Warp '" + name + "' created!");
            });
        }
    }
    
    private class TeleportSubCommand extends AbstractPlayerCommand {
        
        private static final RequiredArg<String> NAME = 
            new RequiredArg<>("name", ArgType.STRING);
        
        public TeleportSubCommand() {
            super("tp", "Teleport to a warp");
            addArg(NAME);
        }
        
        @Override
        protected void execute(
            @Nonnull CommandContext context,
            @Nonnull Store<EntityStore> store,
            @Nonnull Ref<EntityStore> ref,
            @Nonnull PlayerRef playerRef,
            @Nonnull World world
        ) {
            String name = context.get(NAME);
            Vector3 pos = warpManager.getWarp(name);
            
            if (pos == null) {
                context.sendError("Warp not found: " + name);
                return;
            }
            
            world.execute(() -> {
                Player player = store.getComponent(ref, Player.getComponentType());
                player.teleport(pos);
                context.sendSuccess("Teleported to " + name);
            });
        }
    }
}
```

**Usage:**
- `/warp set home`
- `/warp tp home`
- `/warp delete home`
- `/warp list`

## Permission Patterns

### Permission Hierarchy

```java
public class ModeratorCommands extends AbstractCommandCollection {
    
    public ModeratorCommands() {
        super("mod", "Moderator commands");
        
        // Base permission for all subcommands
        setPermission("server.moderator");
        
        addSubCommand(new WarnCommand());  // Inherits base + .warn
        addSubCommand(new MuteCommand());  // Inherits base + .mute
        addSubCommand(new BanCommand());   // Separate permission
    }
    
    private class BanCommand extends CommandBase {
        public BanCommand() {
            super("ban", "Ban a player");
            // Override with higher permission
            setPermission("server.admin.ban");
        }
    }
}
```

### Dynamic Permission Checks

```java
@Override
protected void execute(CommandContext ctx) {
    Player target = ctx.get(TARGET).resolve();
    
    // Check if sender can target this player
    if (target.hasPermission("immune.moderation")) {
        if (!ctx.hasPermission("bypass.immunity")) {
            ctx.sendError("You cannot moderate this player");
            return;
        }
    }
    
    // Proceed with action
}
```

### Permission Node Standards

Use consistent naming:

```
plugin.category.action
plugin.category.action.target

Examples:
mymod.warp.create
mymod.warp.delete
mymod.warp.delete.others
mymod.admin.reload
mymod.admin.debug
```

## Error Handling Patterns

### Comprehensive Error Handling

```java
@Override
protected void execute(CommandContext ctx) {
    try {
        Player target = ctx.get(TARGET).resolve();
        
        if (target == null) {
            ctx.sendError("Player not found or offline");
            return;
        }
        
        int amount = ctx.get(AMOUNT);
        if (amount < 1 || amount > MAX_AMOUNT) {
            ctx.sendError("Amount must be between 1 and " + MAX_AMOUNT);
            return;
        }
        
        performAction(target, amount);
        ctx.sendSuccess("Action completed successfully");
        
    } catch (InsufficientFundsException e) {
        ctx.sendError("Not enough currency: need " + e.getRequired());
    } catch (CooldownException e) {
        ctx.sendError("On cooldown. Try again in " + e.getRemainingSeconds() + "s");
    } catch (Exception e) {
        ctx.sendError("An unexpected error occurred");
        getLogger().atSevere().withCause(e).log("Command error in %s", getName());
    }
}
```

### Validation Helper Methods

```java
public abstract class ValidatedCommand extends CommandBase {
    
    protected boolean validatePlayer(CommandContext ctx, PlayerRef ref, String argName) {
        Player player = ref.resolve();
        if (player == null) {
            ctx.sendError(argName + " is not online");
            return false;
        }
        return true;
    }
    
    protected boolean validateRange(CommandContext ctx, int value, int min, int max, String argName) {
        if (value < min || value > max) {
            ctx.sendError(argName + " must be between " + min + " and " + max);
            return false;
        }
        return true;
    }
    
    protected boolean validatePermission(CommandContext ctx, String permission, String message) {
        if (!ctx.hasPermission(permission)) {
            ctx.sendError(message);
            return false;
        }
        return true;
    }
}
```

## Cooldown Pattern

```java
public abstract class CooldownCommand extends CommandBase {
    
    private final Map<UUID, Instant> cooldowns = new ConcurrentHashMap<>();
    private final Duration cooldownDuration;
    
    protected CooldownCommand(String name, String description, Duration cooldown) {
        super(name, description);
        this.cooldownDuration = cooldown;
    }
    
    @Override
    protected final void execute(CommandContext ctx) {
        if (!ctx.isPlayer()) {
            executeWithCooldown(ctx);
            return;
        }
        
        UUID playerId = ctx.getPlayerSender().get().getUniqueId();
        Instant lastUse = cooldowns.get(playerId);
        
        if (lastUse != null) {
            Duration elapsed = Duration.between(lastUse, Instant.now());
            if (elapsed.compareTo(cooldownDuration) < 0) {
                Duration remaining = cooldownDuration.minus(elapsed);
                ctx.sendError("Cooldown: " + remaining.getSeconds() + "s remaining");
                return;
            }
        }
        
        cooldowns.put(playerId, Instant.now());
        executeWithCooldown(ctx);
    }
    
    protected abstract void executeWithCooldown(CommandContext ctx);
}

// Usage
public class HomeCommand extends CooldownCommand {
    
    public HomeCommand() {
        super("home", "Teleport home", Duration.ofSeconds(30));
    }
    
    @Override
    protected void executeWithCooldown(CommandContext ctx) {
        // Teleport logic
    }
}
```

## Confirmation Pattern

```java
public abstract class ConfirmableCommand extends CommandBase {
    
    private final Map<UUID, PendingAction> pendingActions = new ConcurrentHashMap<>();
    private static final Duration CONFIRM_TIMEOUT = Duration.ofSeconds(30);
    
    private record PendingAction(Runnable action, Instant createdAt) {}
    
    protected void requireConfirmation(CommandContext ctx, String message, Runnable action) {
        if (!ctx.isPlayer()) {
            action.run();
            return;
        }
        
        UUID playerId = ctx.getPlayerSender().get().getUniqueId();
        pendingActions.put(playerId, new PendingAction(action, Instant.now()));
        
        ctx.sendWarning(message);
        ctx.sendMessage("Type /" + getName() + " confirm within 30 seconds to proceed");
    }
    
    protected boolean handleConfirm(CommandContext ctx) {
        if (!ctx.isPlayer()) return false;
        
        UUID playerId = ctx.getPlayerSender().get().getUniqueId();
        PendingAction pending = pendingActions.remove(playerId);
        
        if (pending == null) {
            ctx.sendError("Nothing to confirm");
            return true;
        }
        
        if (Duration.between(pending.createdAt(), Instant.now()).compareTo(CONFIRM_TIMEOUT) > 0) {
            ctx.sendError("Confirmation expired");
            return true;
        }
        
        pending.action().run();
        return true;
    }
}

// Usage
public class ResetCommand extends ConfirmableCommand {
    
    private static final FlagArg CONFIRM = new FlagArg("confirm");
    
    public ResetCommand() {
        super("reset", "Reset all data");
        addArg(CONFIRM);
    }
    
    @Override
    protected void execute(CommandContext ctx) {
        if (ctx.has(CONFIRM)) {
            if (handleConfirm(ctx)) return;
        }
        
        requireConfirmation(ctx, 
            "WARNING: This will delete all data!",
            () -> {
                performReset();
                ctx.sendSuccess("Data has been reset");
            }
        );
    }
}
```

## Pagination Pattern

```java
public class ListCommand extends CommandBase {
    
    private static final int PAGE_SIZE = 10;
    private static final DefaultArg<Integer> PAGE = 
        new DefaultArg<>("page", ArgType.INTEGER, 1);
    
    public ListCommand() {
        super("list", "List all items");
        addArg(PAGE);
    }
    
    @Override
    protected void execute(CommandContext ctx) {
        List<Item> allItems = getItems();
        int page = ctx.get(PAGE);
        int totalPages = (int) Math.ceil(allItems.size() / (double) PAGE_SIZE);
        
        if (page < 1 || page > totalPages) {
            ctx.sendError("Page must be between 1 and " + totalPages);
            return;
        }
        
        int start = (page - 1) * PAGE_SIZE;
        int end = Math.min(start + PAGE_SIZE, allItems.size());
        List<Item> pageItems = allItems.subList(start, end);
        
        ctx.sendMessage("--- Items (Page " + page + "/" + totalPages + ") ---");
        for (int i = 0; i < pageItems.size(); i++) {
            ctx.sendMessage((start + i + 1) + ". " + pageItems.get(i).getName());
        }
        
        if (page < totalPages) {
            ctx.sendMessage("Use /list " + (page + 1) + " for next page");
        }
    }
}
```

## Multi-Step Command Pattern

```java
public class SetupWizardCommand extends AbstractPlayerCommand {
    
    private final Map<UUID, SetupState> playerStates = new ConcurrentHashMap<>();
    
    private enum SetupStep { NAME, LOCATION, CONFIRM, DONE }
    
    private record SetupState(SetupStep step, Map<String, Object> data) {
        SetupState() { this(SetupStep.NAME, new HashMap<>()); }
    }
    
    private static final OptionalArg<String> INPUT = 
        new OptionalArg<>("input", ArgType.GREEDY_STRING);
    
    public SetupWizardCommand() {
        super("setup", "Interactive setup wizard");
        addArg(INPUT);
    }
    
    @Override
    protected void execute(
        @Nonnull CommandContext context,
        @Nonnull Store<EntityStore> store,
        @Nonnull Ref<EntityStore> ref,
        @Nonnull PlayerRef playerRef,
        @Nonnull World world
    ) {
        UUID playerId = playerRef.getUuid();
        SetupState state = playerStates.computeIfAbsent(playerId, k -> new SetupState());
        String input = context.get(INPUT);
        
        world.execute(() -> {
            Player player = store.getComponent(ref, Player.getComponentType());
            
            switch (state.step()) {
                case NAME -> handleNameStep(context, player, state, input);
                case LOCATION -> handleLocationStep(context, player, state, input);
                case CONFIRM -> handleConfirmStep(context, player, state, input);
                case DONE -> {
                    playerStates.remove(playerId);
                    context.sendMessage("Setup already complete. Starting new setup...");
                    playerStates.put(playerId, new SetupState());
                    promptName(context);
                }
            }
        });
    }
    
    private void handleNameStep(CommandContext ctx, Player player, SetupState state, String input) {
        if (input == null) {
            promptName(ctx);
            return;
        }
        
        state.data().put("name", input);
        playerStates.put(player.getUniqueId(), new SetupState(SetupStep.LOCATION, state.data()));
        ctx.sendMessage("Name set to: " + input);
        ctx.sendMessage("Now stand at the desired location and type /setup confirm");
    }
    
    private void promptName(CommandContext ctx) {
        ctx.sendMessage("=== Setup Wizard ===");
        ctx.sendMessage("Enter a name: /setup <name>");
    }
}
```

## Testing Commands

Create debug/test commands for development:

```java
public class DebugCommands extends AbstractCommandCollection {
    
    public DebugCommands() {
        super("debug", "Debug commands");
        setPermission("admin.debug");
        
        addSubCommand(new DumpCommand());
        addSubCommand(new StressTestCommand());
        addSubCommand(new MockEventCommand());
    }
    
    private class DumpCommand extends CommandBase {
        
        private static final RequiredArg<String> TYPE = 
            new RequiredArg<>("type", ArgType.STRING);
        
        public DumpCommand() {
            super("dump", "Dump debug information");
            addArg(TYPE);
        }
        
        @Override
        protected void execute(CommandContext ctx) {
            String type = ctx.get(TYPE);
            
            switch (type) {
                case "entities" -> dumpEntities(ctx);
                case "chunks" -> dumpChunks(ctx);
                case "memory" -> dumpMemory(ctx);
                default -> ctx.sendError("Unknown dump type: " + type);
            }
        }
        
        private void dumpMemory(CommandContext ctx) {
            Runtime rt = Runtime.getRuntime();
            long used = (rt.totalMemory() - rt.freeMemory()) / 1024 / 1024;
            long max = rt.maxMemory() / 1024 / 1024;
            ctx.sendMessage("Memory: " + used + "MB / " + max + "MB");
        }
    }
}
```
