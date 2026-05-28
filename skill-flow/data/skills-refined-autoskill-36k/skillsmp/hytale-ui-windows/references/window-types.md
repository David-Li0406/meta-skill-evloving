# Window Types Reference

Complete reference for all window types and their configuration options.

## WindowType Enum

```java
public enum WindowType {
    Container(0),          // Basic item container
    PocketCrafting(1),     // Field/pocket crafting (inventory crafting)
    BasicCrafting(2),      // Simple workbench crafting
    DiagramCrafting(3),    // Diagram-based crafting (anvil, advanced benches)
    StructuralCrafting(4), // Structural/block transformation crafting
    Processing(5),         // Furnace/smelter type processing
    Memories(6);           // Memories/achievements window
    
    public int getValue();
    public static WindowType fromValue(int value);
}
```

| Type | Value | Description | Implementing Class |
|------|-------|-------------|-------------------|
| `Container` | 0 | Generic item storage | `ContainerWindow`, `ContainerBlockWindow` |
| `PocketCrafting` | 1 | Field/inventory crafting | `FieldCraftingWindow` |
| `BasicCrafting` | 2 | Standard workbench crafting | `SimpleCraftingWindow` |
| `DiagramCrafting` | 3 | Blueprint-based crafting | `DiagramCraftingWindow` |
| `StructuralCrafting` | 4 | Block transformation | `StructuralCraftingWindow` |
| `Processing` | 5 | Time-based processing | `ProcessingBenchWindow` |
| `Memories` | 6 | Read-only display | `MemoriesWindow` |

## Container Windows

### ContainerWindow

Simple item container (not tied to a block). Implements `ItemContainerWindow`.

```java
public class ContainerWindow extends Window implements ItemContainerWindow {
    private final ItemContainer itemContainer;
    private final JsonObject windowData = new JsonObject();
    
    public ContainerWindow(int size) {
        super(WindowType.Container);
        this.itemContainer = new SimpleItemContainer(size);
    }
    
    @Override
    public JsonObject getData() { return windowData; }
    
    @Override
    public ItemContainer getItemContainer() { return itemContainer; }
    
    @Override
    protected boolean onOpen0() { return true; }
    
    @Override
    protected void onClose0() { }
}
```

**Use cases:**
- Backpacks (ItemStackContainerWindow)
- Virtual inventories
- Trading interfaces
- Reward displays

### ContainerBlockWindow

Container tied to a block in the world. Extends `BlockWindow`, implements `ItemContainerWindow`.

```java
public class ContainerBlockWindow extends BlockWindow implements ItemContainerWindow {
    
    public ContainerBlockWindow(int x, int y, int z, int rotationIndex, BlockType blockType, int size) {
        super(WindowType.Container, x, y, z, rotationIndex, blockType);
        // ...
    }
    
    // Handles SortItemsAction for sorting inventory
    @Override
    public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
        if (action instanceof SortItemsAction sort) {
            // Sort inventory
        }
    }
}
```

**Window Data:**
- `blockItemId` - Block's item ID

**Features:**
- Automatic distance validation (default 7.0 blocks)
- Block existence validation
- Supports `SortItemsAction`

### ItemStackContainerWindow

Container tied to an ItemStack (e.g., bags). Implements `ItemContainerWindow`.

```java
public class ItemStackContainerWindow extends Window implements ItemContainerWindow {
    // Auto-closes when parent item becomes invalid
}
```

## FieldCraftingWindow (PocketCrafting)

Pocket/inventory crafting. Extends `Window` directly (not BlockWindow).

```java
public class FieldCraftingWindow extends Window {
    
    public FieldCraftingWindow() {
        super(WindowType.PocketCrafting);
    }
    
    // Handles CraftRecipeAction
    @Override
    public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
        if (action instanceof CraftRecipeAction craft) {
            // Handle fieldcraft recipe
        }
    }
}
```

**Window Data:**
- `type` - BenchType.Crafting ordinal
- `id` - "Fieldcraft"
- `name` - Translation key
- `categories` - Fieldcraft categories with recipes
- `worldMemoriesLevel` - World memories level

**Features:**
- Accessible anywhere (no block required)
- Limited recipe set (fieldcraft recipes only)
- No bench tier system

## SimpleCraftingWindow (BasicCrafting)

Standard workbench crafting. Extends `CraftingWindow`, implements `MaterialContainerWindow`.

```java
public class SimpleCraftingWindow extends CraftingWindow implements MaterialContainerWindow {
    
    public SimpleCraftingWindow(BenchState benchState) {
        super(WindowType.BasicCrafting, benchState);
    }
    
    // Handles CraftRecipeAction, TierUpgradeAction
    @Override
    public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
        if (action instanceof CraftRecipeAction craft) {
            craftSimpleItem(store, ref, craftingManager, craft);
        } else if (action instanceof TierUpgradeAction) {
            handleTierUpgrade(ref, store);
        }
    }
}
```

**Window Data (inherited from BenchWindow):**
- `type` - Bench type ordinal
- `id` - Bench ID string
- `name` - Translation key
- `blockItemId` - Item ID
- `tierLevel` - Current tier level
- `worldMemoriesLevel` - World memories level
- `progress` - Crafting progress (0.0 - 1.0)
- `tierUpgradeProgress` - Tier upgrade progress
- `categories` - Array of bench categories

**Features:**
- Full recipe access based on bench type
- Category filtering
- Recipe book integration
- Tier upgrade support
- Extra materials section

## DiagramCraftingWindow (DiagramCrafting)

Blueprint/diagram-based crafting (e.g., anvil). Extends `CraftingWindow`, implements `ItemContainerWindow`.

```java
public class DiagramCraftingWindow extends CraftingWindow implements ItemContainerWindow {
    
    private String category;           // Current category
    private String itemCategory;       // Current item category
    private SimpleItemContainer inputPrimaryContainer;
    private SimpleItemContainer inputSecondaryContainer;
    private SimpleItemContainer outputContainer;
    private CombinedItemContainer combinedInputItemContainer;
    private CombinedItemContainer combinedItemContainer;
    
    public DiagramCraftingWindow(BenchState benchState) {
        super(WindowType.DiagramCrafting, benchState);
    }
    
    // Handles CancelCraftingAction, UpdateCategoryAction, CraftItemAction
    @Override
    public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
        if (action instanceof CancelCraftingAction) {
            cancelCurrentCraft();
        } else if (action instanceof UpdateCategoryAction update) {
            this.category = update.category;
            this.itemCategory = update.itemCategory;
            updateCategoryDisplay();
        } else if (action instanceof CraftItemAction) {
            confirmDiagramCraft();
        }
    }
}
```

**Window Data (additional):**
- `slots` - Slot data with:
  - `inventoryHint` - Item hints for empty slots
  - `requiredAmount` - Required item count
- `categories` - With nested `itemCategories`

**Features:**
- Visual diagram display
- Multi-slot input (primary + secondary containers)
- Category navigation
- Craft cancellation support

## StructuralCraftingWindow (StructuralCrafting)

Block transformation crafting (e.g., stonecutter). Extends `CraftingWindow`, implements `ItemContainerWindow`.

```java
public class StructuralCraftingWindow extends CraftingWindow implements ItemContainerWindow {
    
    public static final int MAX_OPTIONS = 64;
    
    private SimpleItemContainer inputContainer;
    private SimpleItemContainer optionsContainer;
    private CombinedItemContainer combinedItemContainer;
    private Int2ObjectMap<String> optionSlotToRecipeMap;
    private int selectedSlot;
    
    public StructuralCraftingWindow(BenchState benchState) {
        super(WindowType.StructuralCrafting, benchState);
    }
    
    // Handles SelectSlotAction, CraftRecipeAction, ChangeBlockAction
    @Override
    public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
        if (action instanceof SelectSlotAction select) {
            selectedSlot = select.slot;
            invalidate();
        } else if (action instanceof CraftRecipeAction craft) {
            craftSelectedRecipe(ref, store, craft);
        } else if (action instanceof ChangeBlockAction change) {
            cycleBlockType(change.down);
        }
    }
}
```

**Window Data (additional):**
- `selected` - Selected option slot index
- `allowBlockGroupCycling` - Whether block cycling is allowed
- `alwaysShowInventoryHints` - Show hints on all slots
- `dividerIndex` - Divider between header and regular recipes
- `optionSlotRecipes` - Map of slot to recipe ID
- `inventoryHints` - Item hints for slots

**Features:**
- Grid of output options (up to 64)
- Slot selection for crafting
- Block group cycling (e.g., different wood types)
- Inventory hints display

## ProcessingBenchWindow (Processing)

Furnace/smelter type processing. Extends `BenchWindow`, implements `ItemContainerWindow`.

```java
public class ProcessingBenchWindow extends BenchWindow implements ItemContainerWindow {
    
    private CombinedItemContainer itemContainer;
    private float fuelTime;
    private int maxFuel;
    private float progress;
    private boolean active;
    private Set<Short> processingSlots;
    private Set<Short> processingFuelSlots;
    
    public ProcessingBenchWindow(BenchState benchState) {
        super(WindowType.Processing, benchState);
    }
    
    // State setters
    public void setActive(boolean active);
    public void setProgress(float progress);
    public void setFuelTime(float fuelTime);
    public void setMaxFuel(int maxFuel);
    public void setProcessingSlots(Set<Short> slots);
    public void setProcessingFuelSlots(Set<Short> slots);
    
    // Handles SetActiveAction, TierUpgradeAction
    @Override
    public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
        if (action instanceof SetActiveAction activeAction) {
            setActive(activeAction.state);
            invalidate();
        } else if (action instanceof TierUpgradeAction) {
            handleTierUpgrade(ref, store);
        }
    }
}
```

**Window Data (additional):**
- `active` - Processing active state
- `progress` - Current progress (0.0 - 1.0)
- `fuel` - Fuel slot data
- `maxFuel` - Maximum fuel capacity
- `fuelTime` - Current fuel remaining
- `processingSlots` - Bitmask of slots currently processing
- `processingFuelSlots` - Bitmask of fuel slots in use
- `outputSlotsCount` - Number of output slots
- `input` - Input slot data
- `inventoryHints` - Item hints for slots

**Features:**
- Progress bar display
- Fuel consumption tracking
- Time-based processing
- Multiple input/output slot support
- Active toggle control

## MemoriesWindow (Memories)

Read-only display for achievements/memories. Extends `Window` directly.

```java
public class MemoriesWindow extends Window {
    
    private final JsonObject windowData = new JsonObject();
    
    public MemoriesWindow() {
        super(WindowType.Memories);
    }
    
    @Override
    public JsonObject getData() {
        return windowData;
    }
    
    @Override
    protected boolean onOpen0() {
        loadMemories();
        return true;
    }
    
    @Override
    protected void onClose0() { }
}
```

**Window Data:**
- `capacity` - Memory capacity
- `memories` - Array of memory objects with:
  - `title` - Memory title
  - `tooltipText` - Tooltip description
  - `icon` - Memory icon
  - `categoryIcon` - Category icon

**Features:**
- Read-only display
- Visual representation of data
- No item manipulation
- Client-requestable (registered in MemoriesPlugin)

**Registration:**

```java
// In MemoriesPlugin.setup()
Window.CLIENT_REQUESTABLE_WINDOW_TYPES.put(
    WindowType.Memories,
    MemoriesWindow::new
);
```

## BenchWindow Base Class

Abstract base for all crafting bench windows.

```java
public abstract class BenchWindow extends BlockWindow implements MaterialContainerWindow {
    
    protected static final float CRAFTING_UPDATE_MIN_PERCENT = 0.05F;
    protected static final long CRAFTING_UPDATE_INTERVAL_MS = 500L;
    protected static final String BENCH_UPGRADING = "BenchUpgrading";
    
    protected final Bench bench;
    protected final BenchState benchState;
    protected final JsonObject windowData = new JsonObject();
    private MaterialExtraResourcesSection extraResourcesSection;
    
    // Inherited window data properties:
    // - type: bench type ordinal
    // - id: bench ID string
    // - name: translation key
    // - blockItemId: item ID
    // - tierLevel: current tier level
    
    public void updateCraftingJob(float percent);       // Update crafting progress
    public void updateBenchUpgradeJob(float percent);   // Update tier upgrade progress
    public void updateBenchTierLevel(int newValue);     // Handle tier level change
    
    protected int getBenchTierLevel();
    
    @Override
    public MaterialExtraResourcesSection getExtraResourcesSection();
    
    @Override
    public void invalidateExtraResources();
    
    @Override
    public boolean isValid();
}
```

### CraftingWindow Abstract Class

```java
public abstract class CraftingWindow extends BenchWindow {
    
    public static final int SET_BLOCK_SETTINGS = 6;
    protected static final String CRAFT_COMPLETED = "CraftCompleted";
    protected static final String CRAFT_COMPLETED_INSTANT = "CraftCompletedInstant";
    
    // Window data adds:
    // - categories: array of bench categories
    // - memoriesPerLevel: array of memory amounts
    
    protected void setBlockInteractionState(String state, World world, int setBlockSettings);
    
    public static void craftSimpleItem(
        Store<EntityStore> store,
        Ref<EntityStore> ref,
        CraftingManager craftingManager,
        CraftRecipeAction action
    );
}
```

## Window Interfaces

### ItemContainerWindow

Windows with item inventory slots.

```java
public interface ItemContainerWindow {
    @Nonnull ItemContainer getItemContainer();
}
```

**Automatic behaviors when implemented:**
- WindowManager registers change listener on container
- InventorySection included in OpenWindow/UpdateWindow packets
- Listener unregistered on window close

### MaterialContainerWindow

Windows with extra resource materials.

```java
public interface MaterialContainerWindow {
    @Nonnull MaterialExtraResourcesSection getExtraResourcesSection();
    void invalidateExtraResources();
    boolean isValid();
}
```

**Automatic behaviors when implemented:**
- ExtraResources included in OpenWindow/UpdateWindow packets (when invalid)

### ValidatedWindow

Windows that validate their state periodically.

```java
public interface ValidatedWindow {
    boolean validate();
}
```

**Automatic behaviors when implemented:**
- `WindowManager.validateWindows()` calls `validate()` on each
- Window is closed if `validate()` returns false

## Class Hierarchy Summary

```
Window (abstract)
├── ContainerWindow (implements ItemContainerWindow)
├── ItemStackContainerWindow (implements ItemContainerWindow)
├── FieldCraftingWindow
├── MemoriesWindow
└── BlockWindow (abstract, implements ValidatedWindow)
    ├── ContainerBlockWindow (implements ItemContainerWindow)
    └── BenchWindow (abstract, implements MaterialContainerWindow)
        ├── ProcessingBenchWindow (implements ItemContainerWindow)
        └── CraftingWindow (abstract)
            ├── SimpleCraftingWindow (implements MaterialContainerWindow)
            ├── DiagramCraftingWindow (implements ItemContainerWindow)
            └── StructuralCraftingWindow (implements ItemContainerWindow)
```

## Custom Window Implementation Pattern

For completely custom window behavior:

```java
public class CustomGameWindow extends Window implements ItemContainerWindow {
    
    private final JsonObject windowData = new JsonObject();
    private final SimpleItemContainer itemContainer;
    private final GameState state;
    
    public CustomGameWindow(GameState state) {
        super(WindowType.Container); // Use Container as base type
        this.state = state;
        this.itemContainer = new SimpleItemContainer(54);
        initializeGame();
    }
    
    @Override
    public JsonObject getData() {
        windowData.addProperty("score", state.getScore());
        windowData.addProperty("currentPlayer", state.getCurrentPlayer());
        return windowData;
    }
    
    @Override
    public ItemContainer getItemContainer() {
        return itemContainer;
    }
    
    private void initializeGame() {
        // Set up game board in item container
        placeGamePieces();
    }
    
    @Override
    public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
        if (action instanceof SelectSlotAction select) {
            if (!state.isPlayerTurn()) {
                sendMessage(ref, "Not your turn!");
                return;
            }
            
            processGameMove(select.slot);
            checkWinCondition();
            invalidate();
        }
    }
    
    @Override
    protected boolean onOpen0() {
        return true;
    }
    
    @Override
    protected void onClose0() {
        // Cleanup game state
    }
}
```
