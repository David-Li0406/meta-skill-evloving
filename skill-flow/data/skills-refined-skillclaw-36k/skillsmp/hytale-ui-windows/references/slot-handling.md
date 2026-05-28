# Slot Handling Reference

Complete reference for item containers, sorting, and inventory handling in window systems.

## ItemContainer Overview

`ItemContainer` is the abstract base class for all inventory systems. Windows implement `ItemContainerWindow` to expose their container to the window system.

```java
public interface ItemContainerWindow {
    @Nonnull ItemContainer getItemContainer();
}
```

## ItemContainer Implementations

| Class | Description |
|-------|-------------|
| `SimpleItemContainer` | Standard inventory with fixed capacity |
| `CombinedItemContainer` | Combines multiple containers into one |
| `ItemStackItemContainer` | Container backed by an ItemStack (bags) |
| `DelegateItemContainer` | Wraps another container with custom behavior |
| `EmptyItemContainer` | Empty/read-only container |

## Basic Item Operations

### Getting and Setting Items

```java
ItemContainer container = window.getItemContainer();

// Get item in slot (returns null if empty)
ItemStack item = container.getItemStack((short) slot);

// Set item in slot (returns transaction)
ItemStackSlotTransaction tx = container.setItemStackForSlot((short) slot, itemStack);
if (tx.succeeded()) {
    // Item was set successfully
}

// Set with filter (check slot filters)
ItemStackSlotTransaction tx = container.setItemStackForSlot((short) slot, itemStack, true);
```

### Adding Items

```java
// Add item to any available slot
ItemStackTransaction tx = container.addItemStack(itemStack);
if (tx.succeeded()) {
    ItemStack remainder = tx.getRemainder(); // Items that didn't fit
}

// Add to specific slot
ItemStackSlotTransaction tx = container.addItemStackToSlot((short) slot, itemStack);

// Check if item can be added
boolean canAdd = container.canAddItemStack(itemStack);

// Add multiple items
List<ItemStack> items = List.of(item1, item2, item3);
ListTransaction<ItemStackTransaction> tx = container.addItemStacks(items);
```

### Removing Items

```java
// Remove all items from slot
SlotTransaction tx = container.removeItemStackFromSlot((short) slot);

// Remove specific quantity from slot
ItemStackSlotTransaction tx = container.removeItemStackFromSlot((short) slot, quantity);

// Remove matching itemstack
ItemStackTransaction tx = container.removeItemStack(itemStack);

// Check if items can be removed
boolean canRemove = container.canRemoveItemStack(itemStack);

// Remove multiple items
ListTransaction<ItemStackTransaction> tx = container.removeItemStacks(items);
```

### Moving Items Between Containers

```java
// Move from slot to another container
MoveTransaction<ItemStackTransaction> tx = container.moveItemStackFromSlot(
    (short) slot, 
    targetContainer
);

// Move specific quantity
MoveTransaction<ItemStackTransaction> tx = container.moveItemStackFromSlot(
    (short) slot, 
    quantity,
    targetContainer
);

// Move to specific slot
MoveTransaction<SlotTransaction> tx = container.moveItemStackFromSlotToSlot(
    (short) fromSlot,
    quantity,
    targetContainer,
    (short) toSlot
);

// Move all items matching predicate
ListTransaction<MoveTransaction<ItemStackTransaction>> tx = container.moveAllItemStacksTo(
    itemStack -> itemStack.hasTag(TagIndex),
    targetContainer
);

// Quick stack (only items that already exist in target)
ListTransaction<MoveTransaction<ItemStackTransaction>> tx = container.quickStackTo(targetContainer);
```

### Clearing and Replacing

```java
// Clear all items
ClearTransaction tx = container.clear();

// Replace item in slot (conditional on existing item)
ItemStackSlotTransaction tx = container.replaceItemStackInSlot(
    (short) slot,
    expectedItem,  // Must match current item (null for empty)
    newItem
);

// Replace all items with function
ListTransaction<ItemStackSlotTransaction> tx = container.replaceAll(
    (slot, existing) -> transformItem(existing)
);
```

## Slot Iteration

```java
short capacity = container.getCapacity();

// Iterate with forEach
container.forEach((slot, itemStack) -> {
    if (!ItemStack.isEmpty(itemStack)) {
        // Process item
    }
});

// With metadata
container.forEachWithMeta((slot, itemStack, context) -> {
    // slot is short, itemStack is ItemStack
}, contextObject);
```

## Slot Filters

Filters control what items can be placed in slots:

### Global Filter

```java
// Set filter for entire container
container.setGlobalFilter(FilterType.ALLOW_ALL);
container.setGlobalFilter(FilterType.DENY_ALL);
```

### Slot-Specific Filters

```java
// Set filter for specific slot
container.setSlotFilter(
    FilterActionType.ADD,    // Filter for add operations
    (short) slot,
    new SlotFilter() {
        @Override
        public boolean test(ItemStack item) {
            return item.hasTag(ItemTags.FUEL);
        }
    }
);

// Filter action types:
// - FilterActionType.ADD: Filter items being added
// - FilterActionType.REMOVE: Filter items being removed
// - FilterActionType.DROP: Filter items being dropped
```

## Transaction System

All operations return Transaction objects that indicate success/failure:

```java
public interface Transaction {
    boolean succeeded();
}

public class ItemStackSlotTransaction extends SlotTransaction {
    short getSlot();
    ItemStack getSlotBefore();
    ItemStack getSlotAfter();
    ItemStack getOutput();      // Items removed
    ItemStack getRemainder();   // Items that didn't fit
}

public class ItemStackTransaction extends Transaction {
    ItemStack getInput();
    ItemStack getOutput();
    ItemStack getRemainder();
}

public class MoveTransaction<T extends Transaction> extends Transaction {
    T getFromTransaction();
    T getAddTransaction();
    ItemContainer getOtherContainer();
}
```

### Transaction Usage

```java
ItemStackTransaction tx = container.addItemStack(itemStack);

if (tx.succeeded()) {
    // Full or partial success
    if (ItemStack.isEmpty(tx.getRemainder())) {
        // All items added
    } else {
        // Some items didn't fit
        ItemStack remainder = tx.getRemainder();
    }
} else {
    // Complete failure
}
```

### All-Or-Nothing Operations

```java
// Second parameter: allOrNothing
ItemStackTransaction tx = container.addItemStack(
    itemStack, 
    true,   // allOrNothing: fail if can't add all
    false,  // fullStacks: only add full stacks
    true    // filter: apply slot filters
);
```

## Sorting

Containers support sorting with different strategies:

```java
// Sort the container
container.sort(SortType.NAME);
container.sort(SortType.TYPE);
container.sort(SortType.RARITY);
```

### SortType Enum

```java
public enum SortType {
    NAME,    // Sort by item translation key (alphabetical)
    TYPE,    // Sort by item type (Weapon, Armor, Tool, Item, Special)
    RARITY;  // Sort by quality value (reversed, rarest first)
    
    // Convert to/from protocol types
    public com.hypixel.hytale.protocol.SortType toPacket();
    public static SortType fromPacket(com.hypixel.hytale.protocol.SortType sortType);
}
```

### Handling SortItemsAction

```java
@Override
public void handleAction(Ref<EntityStore> ref, Store<EntityStore> store, WindowAction action) {
    if (action instanceof SortItemsAction sort) {
        SortType serverSortType = SortType.fromPacket(sort.sortType);
        getItemContainer().sort(serverSortType);
        invalidate();
    }
}
```

## Change Events

Register listeners for container changes:

```java
// Register change listener
EventRegistration registration = container.registerChangeEvent(event -> {
    // Container was modified
    window.invalidate();
});

// With priority
container.registerChangeEvent(EventPriority.LAST, event -> {
    // Called after other handlers
});

// Unregister when done
registration.unregister();
```

**Note:** `WindowManager` automatically registers change events for `ItemContainerWindow` instances and unregisters them on close.

## Container Serialization

Containers serialize to protocol packets:

```java
// Convert to packet format
InventorySection packet = container.toPacket();

// Contains:
// - capacity: short
// - items: Map<Integer, ItemWithAllMetadata>
```

## SimpleItemContainer

The most common container implementation:

```java
// Create with capacity
SimpleItemContainer container = new SimpleItemContainer(27); // 3 rows

// Clone a container
ItemContainer copy = container.clone();

// Get capacity
short capacity = container.getCapacity();
```

## CombinedItemContainer

Combines multiple containers into one view:

```java
// Combine two containers
CombinedItemContainer combined = new CombinedItemContainer(
    inputContainer,
    outputContainer
);

// Slots are mapped sequentially:
// - Slots 0 to inputContainer.capacity-1 -> inputContainer
// - Slots inputContainer.capacity to total-1 -> outputContainer
```

## Common Patterns

### Input/Output Slots

```java
public class ProcessingWindow extends Window implements ItemContainerWindow {
    
    private SimpleItemContainer inputContainer = new SimpleItemContainer(1);
    private SimpleItemContainer outputContainer = new SimpleItemContainer(1);
    private CombinedItemContainer combinedContainer;
    
    public ProcessingWindow() {
        super(WindowType.Processing);
        this.combinedContainer = new CombinedItemContainer(inputContainer, outputContainer);
        
        // Set output slot as output-only (can't add items)
        outputContainer.setSlotFilter(FilterActionType.ADD, (short) 0, item -> false);
    }
    
    @Override
    public ItemContainer getItemContainer() {
        return combinedContainer;
    }
}
```

### Inventory with Sections

```java
public class ShopWindow extends Window implements ItemContainerWindow {
    
    private static final int DISPLAY_SLOTS = 45;  // 5 rows for display
    private static final int NAV_SLOTS = 9;       // 1 row for navigation
    
    private SimpleItemContainer container = new SimpleItemContainer(DISPLAY_SLOTS + NAV_SLOTS);
    
    public ShopWindow() {
        super(WindowType.Container);
        
        // Make all slots read-only
        for (short i = 0; i < container.getCapacity(); i++) {
            container.setSlotFilter(FilterActionType.ADD, i, item -> false);
            container.setSlotFilter(FilterActionType.REMOVE, i, item -> false);
        }
    }
    
    private void setupDisplay(List<ShopItem> items, int page) {
        int offset = page * DISPLAY_SLOTS;
        
        for (int i = 0; i < DISPLAY_SLOTS && offset + i < items.size(); i++) {
            ShopItem shopItem = items.get(offset + i);
            container.setItemStackForSlot((short) i, shopItem.createDisplayStack(), false);
        }
    }
}
```

### Validating Container State

```java
public boolean hasRequiredMaterials(List<ItemStack> required) {
    return container.canRemoveItemStacks(required);
}

public void consumeMaterials(List<ItemStack> materials) {
    ListTransaction<ItemStackTransaction> tx = container.removeItemStacks(materials);
    if (!tx.succeeded()) {
        // Handle failure
    }
}
```

## Best Practices

### Thread Safety

```java
// ItemContainer operations are thread-safe for single operations
// For multiple operations that must be atomic, use writeAction:
container.writeAction(() -> {
    container.removeItemStackFromSlot((short) 0);
    container.addItemStackToSlot((short) 1, newItem);
    return null;
});
```

### Efficient Updates

```java
// Batch multiple changes before invalidating
public void processMultipleItems() {
    // Do multiple operations
    container.addItemStack(item1);
    container.addItemStack(item2);
    container.addItemStack(item3);
    
    // Single invalidate at end (WindowManager handles this via change events)
    // The change event listener will mark window as dirty
}
```

### Checking Before Acting

```java
// Always check if operation will succeed before modifying
if (container.canAddItemStack(reward)) {
    container.addItemStack(reward);
    player.sendMessage("Reward added!");
} else {
    player.sendMessage("Inventory full!");
}
```
