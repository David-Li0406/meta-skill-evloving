# Custom UI Pages Reference

Complete reference for creating custom UI pages in Hytale server plugins. Custom UI pages provide a flexible system for displaying interactive UI to players, separate from the Window system.

## Overview

Custom UI Pages are server-controlled UI screens that:
- Load `.ui` files dynamically via `UICommandBuilder`
- Bind UI element events to server callbacks via `UIEventBuilder`
- Handle typed event data through a `BuilderCodec<T>` pattern
- Support dynamic updates without full rebuilds

## Page Class Hierarchy

```
CustomUIPage (abstract)
├── BasicCustomUIPage          # Simple page, no typed events
└── InteractiveCustomUIPage<T> # Typed event handling (most common)
```

## CustomUIPage Base Class

The abstract base class for all custom pages.

```java
package com.hypixel.hytale.server.core.entity.entities.player.pages;

public abstract class CustomUIPage {
    @Nonnull protected final PlayerRef playerRef;
    @Nonnull protected CustomPageLifetime lifetime;
    
    // Constructor
    public CustomUIPage(@Nonnull PlayerRef playerRef, @Nonnull CustomPageLifetime lifetime);
    
    // Abstract - must implement
    public abstract void build(
        @Nonnull Ref<EntityStore> ref, 
        @Nonnull UICommandBuilder commandBuilder, 
        @Nonnull UIEventBuilder eventBuilder, 
        @Nonnull Store<EntityStore> store
    );
    
    // Lifecycle
    public void onDismiss(@Nonnull Ref<EntityStore> ref, @Nonnull Store<EntityStore> store);
    
    // Update methods
    protected void rebuild();                                              // Full rebuild with events
    protected void sendUpdate();                                           // Update without commands
    protected void sendUpdate(@Nullable UICommandBuilder commandBuilder);  // Update with commands
    protected void sendUpdate(@Nullable UICommandBuilder commandBuilder, boolean clear);
    
    // Close the page
    protected void close();
    
    // Lifetime management
    public void setLifetime(@Nonnull CustomPageLifetime lifetime);
    @Nonnull public CustomPageLifetime getLifetime();
}
```

## InteractiveCustomUIPage<T>

The most commonly used page type. Provides typed event handling through a `BuilderCodec<T>`.

```java
package com.hypixel.hytale.server.core.entity.entities.player.pages;

public abstract class InteractiveCustomUIPage<T> extends CustomUIPage {
    @Nonnull protected final BuilderCodec<T> eventDataCodec;
    
    // Constructor
    public InteractiveCustomUIPage(
        @Nonnull PlayerRef playerRef, 
        @Nonnull CustomPageLifetime lifetime, 
        @Nonnull BuilderCodec<T> eventDataCodec
    );
    
    // Override to handle typed events
    public void handleDataEvent(
        @Nonnull Ref<EntityStore> ref, 
        @Nonnull Store<EntityStore> store, 
        @Nonnull T data
    );
    
    // Extended update method with event builder
    protected void sendUpdate(
        @Nullable UICommandBuilder commandBuilder, 
        @Nullable UIEventBuilder eventBuilder, 
        boolean clear
    );
}
```

## BasicCustomUIPage

Simple page without typed event handling. Use when you only need to display static UI.

```java
package com.hypixel.hytale.server.core.entity.entities.player.pages;

public abstract class BasicCustomUIPage extends CustomUIPage {
    
    public BasicCustomUIPage(@Nonnull PlayerRef playerRef, @Nonnull CustomPageLifetime lifetime);
    
    // Simplified build method
    public abstract void build(UICommandBuilder commandBuilder);
}
```

## CustomPageLifetime Enum

Controls how the page can be closed by the player.

| Value | Description |
|-------|-------------|
| `CantClose` | Player cannot close the page (only server can close) |
| `CanDismiss` | Player can close with ESC/back button |
| `CanDismissOrCloseThroughInteraction` | Player can close via ESC or by interacting in the world |

```java
import com.hypixel.hytale.protocol.packets.interface_.CustomPageLifetime;

// Examples
CustomPageLifetime.CanDismiss                       // Most common
CustomPageLifetime.CantClose                        // Forced dialogs
CustomPageLifetime.CanDismissOrCloseThroughInteraction  // Loose modals
```

## PageManager

Manages custom pages for a player. Access via `Player.getPageManager()`.

### Key Methods

```java
// Open a custom page
void openCustomPage(
    @Nonnull Ref<EntityStore> ref, 
    @Nonnull Store<EntityStore> store, 
    @Nonnull CustomUIPage page
);

// Open a custom page with windows (inventory-based UIs)
boolean openCustomPageWithWindows(
    @Nonnull Ref<EntityStore> ref, 
    @Nonnull Store<EntityStore> store, 
    @Nonnull CustomUIPage page, 
    @Nonnull Window... windows
);

// Set a built-in page type (closes current custom page)
void setPage(
    @Nonnull Ref<EntityStore> ref, 
    @Nonnull Store<EntityStore> store, 
    @Nonnull Page page
);

// Set page with windows
boolean setPageWithWindows(
    @Nonnull Ref<EntityStore> ref, 
    @Nonnull Store<EntityStore> store, 
    @Nonnull Page page, 
    boolean canCloseThroughInteraction, 
    @Nonnull Window... windows
);

// Update the current custom page
void updateCustomPage(@Nonnull CustomPage page);

// Get current custom page (nullable)
@Nullable CustomUIPage getCustomPage();
```

### Closing Pages

```java
// From within the page:
this.close();

// From PageManager:
playerComponent.getPageManager().setPage(ref, store, Page.None);
```

## UICommandBuilder

Builds commands to manipulate UI elements. Commands are sent to the client to load UI files and set property values.

### Methods

| Method | Description |
|--------|-------------|
| `append(documentPath)` | Append UI file to root |
| `append(selector, documentPath)` | Append UI file as child of selector |
| `appendInline(selector, document)` | Append inline UI code |
| `insertBefore(selector, documentPath)` | Insert UI file before selector |
| `insertBeforeInline(selector, document)` | Insert inline UI before selector |
| `clear(selector)` | Remove all children of selector |
| `remove(selector)` | Remove element by selector |
| `set(selector, value)` | Set property value (String, int, float, boolean, etc.) |
| `setNull(selector)` | Set property to null |
| `setObject(selector, object)` | Set complex object (Area, ItemStack, etc.) |

### Selectors

Selectors target UI elements by ID or indexed children:

```java
"#ElementId"                    // Element with ID
"#Parent #Child"                // Nested element
"#Parent[0]"                    // First child of parent
"#Parent[2] #Label"             // Element inside 3rd child
"#Element.PropertyName"         // Property of element
```

### Property Paths

```java
"#Label.Text"                   // Text property
"#Button.Visible"               // Visibility
"#Slider.Value"                 // Slider value
"#Container.Background"         // Background
"#Element.Anchor"               // Anchor/positioning
```

### Usage Examples

```java
UICommandBuilder commandBuilder = new UICommandBuilder();

// Load main page UI file (files in resources/Common/UI/Custom/)
commandBuilder.append("MyPage.ui");

// Set property values
commandBuilder.set("#TitleLabel.Text", "Welcome!");
commandBuilder.set("#CountDisplay.Text", String.valueOf(count));
commandBuilder.set("#EnableOption.Value", true);
commandBuilder.set("#VolumeSlider.Value", 0.75f);

// Show/hide elements
commandBuilder.set("#LoadingSpinner.Visible", false);
commandBuilder.set("#ContentArea.Visible", true);

// Append child elements dynamically
for (int i = 0; i < items.size(); i++) {
    commandBuilder.append("#ItemList", "ItemEntry.ui");
    commandBuilder.set("#ItemList[" + i + "] #Name.Text", items.get(i).getName());
    commandBuilder.set("#ItemList[" + i + "] #Icon.AssetPath", items.get(i).getIcon());
}

// Clear children before rebuilding
commandBuilder.clear("#ItemList");

// Remove specific element
commandBuilder.remove("#TemporaryMessage");

// Inline UI (for simple cases)
commandBuilder.appendInline("#Container", "Label { Text: \"Dynamic text\"; }");
```

## UIEventBuilder

Binds UI element events to server callbacks. When the event fires, the server receives the data.

### Method Signatures

```java
// Basic binding (locks interface by default)
UIEventBuilder addEventBinding(CustomUIEventBindingType type, String selector);

// With lock control
UIEventBuilder addEventBinding(CustomUIEventBindingType type, String selector, boolean locksInterface);

// With event data
UIEventBuilder addEventBinding(CustomUIEventBindingType type, String selector, EventData data);

// Full control
UIEventBuilder addEventBinding(CustomUIEventBindingType type, String selector, @Nullable EventData data, boolean locksInterface);
```

### locksInterface Parameter

- `true` (default): Client waits for server acknowledgment before allowing more input
- `false`: Client continues immediately (use for search fields, sliders)

### CustomUIEventBindingType Enum

| Type | Description |
|------|-------------|
| `Activating` | Button clicked / element activated |
| `RightClicking` | Right-click on element |
| `DoubleClicking` | Double-click on element |
| `MouseEntered` | Mouse entered element bounds |
| `MouseExited` | Mouse exited element bounds |
| `ValueChanged` | Input value changed (TextField, Slider, etc.) |
| `ElementReordered` | Drag-reorder in list |
| `Validating` | Form validation trigger |
| `Dismissing` | Back button / ESC pressed |
| `FocusGained` | Element received focus |
| `FocusLost` | Element lost focus |
| `KeyDown` | Key pressed while focused |
| `MouseButtonReleased` | Mouse button released |
| `SlotClicking` | Inventory slot clicked |
| `SlotDoubleClicking` | Inventory slot double-clicked |
| `SlotMouseEntered` | Mouse entered slot |
| `SlotMouseExited` | Mouse exited slot |
| `DragCancelled` | Drag operation cancelled |
| `Dropped` | Item dropped |
| `SlotMouseDragCompleted` | Slot drag completed |
| `SlotMouseDragExited` | Slot drag exited |
| `SlotClickReleaseWhileDragging` | Click release during drag |
| `SlotClickPressWhileDragging` | Click press during drag |
| `SelectedTabChanged` | Tab selection changed |

### Usage Examples

```java
UIEventBuilder eventBuilder = new UIEventBuilder();

// Button click with static data
eventBuilder.addEventBinding(
    CustomUIEventBindingType.Activating, 
    "#ConfirmButton", 
    EventData.of("Action", "Confirm")
);

// Button with item identifier
eventBuilder.addEventBinding(
    CustomUIEventBindingType.Activating, 
    "#ItemList[" + i + "]", 
    EventData.of("ItemId", item.getId()),
    false  // Don't lock interface
);

// Text input changes (capture input value)
eventBuilder.addEventBinding(
    CustomUIEventBindingType.ValueChanged, 
    "#SearchInput", 
    EventData.of("@SearchQuery", "#SearchInput.Value")
);

// Slider value (capture numeric value)
eventBuilder.addEventBinding(
    CustomUIEventBindingType.ValueChanged, 
    "#VolumeSlider", 
    EventData.of("@Volume", "#VolumeSlider.Value"),
    false  // Don't lock for smooth sliding
);

// Multiple data fields
eventBuilder.addEventBinding(
    CustomUIEventBindingType.Activating, 
    "#SubmitButton", 
    EventData.of("Action", "Submit")
        .append("@Name", "#NameInput.Value")
        .append("@Amount", "#AmountInput.Value")
);
```

## EventData

Defines data sent to the server when an event fires.

### Value Types

| Syntax | Description |
|--------|-------------|
| `"StaticValue"` | Literal string value |
| `"#Element.Property"` | Read property from UI element |

### Key Prefixes

| Prefix | Meaning |
|--------|---------|
| `@Key` | Codec field name (maps to BuilderCodec) |
| No prefix | Static key name |

### Usage

```java
// Static value only
EventData.of("Action", "ButtonClicked");

// Read UI element value
EventData.of("@SearchQuery", "#SearchInput.Value");

// Multiple fields
EventData.of("Action", "Save")
    .append("@Name", "#NameField.Value")
    .append("@Enabled", "#EnableCheckbox.Value")
    .append("ItemType", "weapon");

// Enum value
EventData.of("@Category", myEnum);  // Calls enumValue.name()
```

## BuilderCodec<T> Pattern

Define a typed data class with codec for parsing event data.

### Basic Structure

```java
public class MyPageEventData {
    // Field names match EventData keys (with @ prefix removed)
    private String action;
    private String searchQuery;
    private Integer amount;
    
    // Codec definition
    @Nonnull
    public static final BuilderCodec<MyPageEventData> CODEC = BuilderCodec.builder(
            MyPageEventData.class, 
            MyPageEventData::new
        )
        .append(new KeyedCodec<>("Action", Codec.STRING), 
                (entry, s) -> entry.action = s, 
                entry -> entry.action)
        .add()
        .append(new KeyedCodec<>("@SearchQuery", Codec.STRING), 
                (entry, s) -> entry.searchQuery = s, 
                entry -> entry.searchQuery)
        .add()
        .append(new KeyedCodec<>("@Amount", Codec.INTEGER), 
                (entry, i) -> entry.amount = i, 
                entry -> entry.amount)
        .add()
        .build();
    
    // Getters
    public String getAction() { return this.action; }
    public String getSearchQuery() { return this.searchQuery; }
    public Integer getAmount() { return this.amount; }
}
```

### Available Codec Types

```java
Codec.STRING      // String values
Codec.INTEGER     // Integer values
Codec.BOOLEAN     // Boolean values
Codec.FLOAT       // Float values
Codec.DOUBLE      // Double values
```

## Complete Example: Warp List Page

A full working example of an interactive page with search and list selection.

### Page Class

```java
package com.example.myplugin.pages;

import com.hypixel.hytale.codec.Codec;
import com.hypixel.hytale.codec.KeyedCodec;
import com.hypixel.hytale.codec.builder.BuilderCodec;
import com.hypixel.hytale.component.Ref;
import com.hypixel.hytale.component.Store;
import com.hypixel.hytale.protocol.packets.interface_.CustomPageLifetime;
import com.hypixel.hytale.protocol.packets.interface_.CustomUIEventBindingType;
import com.hypixel.hytale.protocol.packets.interface_.Page;
import com.hypixel.hytale.server.core.entity.entities.Player;
import com.hypixel.hytale.server.core.entity.entities.player.pages.InteractiveCustomUIPage;
import com.hypixel.hytale.server.core.ui.builder.EventData;
import com.hypixel.hytale.server.core.ui.builder.UICommandBuilder;
import com.hypixel.hytale.server.core.ui.builder.UIEventBuilder;
import com.hypixel.hytale.server.core.universe.PlayerRef;
import com.hypixel.hytale.server.core.universe.world.storage.EntityStore;
import java.util.Collections;
import java.util.List;
import java.util.function.Consumer;
import javax.annotation.Nonnull;

public class WarpListPage extends InteractiveCustomUIPage<WarpListPage.PageEventData> {
    
    private final Consumer<String> callback;
    private final List<String> warpNames;
    @Nonnull
    private String searchQuery = "";
    
    public WarpListPage(@Nonnull PlayerRef playerRef, List<String> warpNames, Consumer<String> callback) {
        super(playerRef, CustomPageLifetime.CanDismiss, PageEventData.CODEC);
        this.warpNames = warpNames;
        this.callback = callback;
    }
    
    @Override
    public void build(
        @Nonnull Ref<EntityStore> ref, 
        @Nonnull UICommandBuilder commandBuilder, 
        @Nonnull UIEventBuilder eventBuilder, 
        @Nonnull Store<EntityStore> store
    ) {
        // Load main page UI (file in resources/Common/UI/Custom/)
        commandBuilder.append("WarpListPage.ui");
        
        // Bind search input
        eventBuilder.addEventBinding(
            CustomUIEventBindingType.ValueChanged, 
            "#SearchInput", 
            EventData.of("@SearchQuery", "#SearchInput.Value")
        );
        
        // Build the list
        buildWarpList(commandBuilder, eventBuilder);
    }
    
    private void buildWarpList(UICommandBuilder commandBuilder, UIEventBuilder eventBuilder) {
        // Clear existing list
        commandBuilder.clear("#WarpList");
        
        // Filter and sort warps
        List<String> filtered = warpNames.stream()
            .filter(w -> searchQuery.isEmpty() || w.toLowerCase().contains(searchQuery))
            .sorted()
            .toList();
        
        if (filtered.isEmpty()) {
            commandBuilder.appendInline("#WarpList", 
                "Label { Text: %server.customUI.warpListPage.noWarps; Style: (Alignment: Center); }");
            return;
        }
        
        // Add each warp entry
        for (int i = 0; i < filtered.size(); i++) {
            String warp = filtered.get(i);
            String selector = "#WarpList[" + i + "]";
            
            // Append the UI component
            commandBuilder.append("#WarpList", "WarpEntryButton.ui");
            
            // Set properties
            commandBuilder.set(selector + " #Name.Text", warp);
            
            // Bind click event
            eventBuilder.addEventBinding(
                CustomUIEventBindingType.Activating, 
                selector, 
                EventData.of("Warp", warp),
                false
            );
        }
    }
    
    @Override
    public void handleDataEvent(
        @Nonnull Ref<EntityStore> ref, 
        @Nonnull Store<EntityStore> store, 
        @Nonnull PageEventData data
    ) {
        if (data.getWarp() != null) {
            // Warp selected - close page and trigger callback
            Player player = store.getComponent(ref, Player.getComponentType());
            player.getPageManager().setPage(ref, store, Page.None);
            callback.accept(data.getWarp());
        } 
        else if (data.getSearchQuery() != null) {
            // Search query changed - rebuild list
            this.searchQuery = data.getSearchQuery().trim().toLowerCase();
            
            UICommandBuilder commandBuilder = new UICommandBuilder();
            UIEventBuilder eventBuilder = new UIEventBuilder();
            buildWarpList(commandBuilder, eventBuilder);
            
            // Send incremental update
            this.sendUpdate(commandBuilder, eventBuilder, false);
        }
    }
    
    // Event data class with codec
    public static class PageEventData {
        @Nonnull
        public static final BuilderCodec<PageEventData> CODEC = BuilderCodec.builder(
                PageEventData.class, 
                PageEventData::new
            )
            .append(new KeyedCodec<>("Warp", Codec.STRING), 
                    (e, s) -> e.warp = s, e -> e.warp)
            .add()
            .append(new KeyedCodec<>("@SearchQuery", Codec.STRING), 
                    (e, s) -> e.searchQuery = s, e -> e.searchQuery)
            .add()
            .build();
        
        private String warp;
        private String searchQuery;
        
        public String getWarp() { return warp; }
        public String getSearchQuery() { return searchQuery; }
    }
}
```

### Opening the Page from a Command

```java
package com.example.myplugin.commands;

import com.hypixel.hytale.component.Ref;
import com.hypixel.hytale.component.Store;
import com.hypixel.hytale.server.core.command.system.CommandContext;
import com.hypixel.hytale.server.core.command.system.basecommands.CommandBase;
import com.hypixel.hytale.server.core.entity.entities.Player;
import com.hypixel.hytale.server.core.universe.PlayerRef;
import com.hypixel.hytale.server.core.universe.world.World;
import com.hypixel.hytale.server.core.universe.world.storage.EntityStore;
import com.example.myplugin.pages.WarpListPage;
import java.util.List;

public class WarpListCommand extends CommandBase {
    
    public WarpListCommand() {
        super("warps", "server.commands.warps.desc");
    }
    
    @Override
    protected void executeSync(@Nonnull CommandContext context) {
        if (!context.isPlayer()) {
            context.sendMessage("This command requires a player");
            return;
        }
        
        Ref<EntityStore> ref = context.senderAsPlayerRef();
        if (ref == null || !ref.isValid()) {
            return;
        }
        
        Store<EntityStore> store = ref.getStore();
        World world = store.getExternalData().getWorld();
        
        // Execute on world thread
        world.execute(() -> {
            Player player = store.getComponent(ref, Player.getComponentType());
            PlayerRef playerRef = store.getComponent(ref, PlayerRef.getComponentType());
            
            List<String> warpNames = getWarpNames(); // Your method
            
            // Open the page
            player.getPageManager().openCustomPage(
                ref, 
                store, 
                new WarpListPage(playerRef, warpNames, warpName -> {
                    // Callback when warp is selected
                    teleportToWarp(ref, store, warpName);
                })
            );
        });
    }
}
```

## Best Practices

### 1. Always Use World Thread

```java
World world = store.getExternalData().getWorld();
world.execute(() -> {
    // Open page here
    player.getPageManager().openCustomPage(ref, store, page);
});
```

### 2. Incremental Updates

For search/filter changes, only update the affected UI elements:

```java
// Don't rebuild everything - just update the list
UICommandBuilder cmd = new UICommandBuilder();
UIEventBuilder evt = new UIEventBuilder();
buildListOnly(cmd, evt);
this.sendUpdate(cmd, evt, false);  // false = don't clear existing events
```

### 3. Use locksInterface Appropriately

```java
// Lock for submit buttons (prevent double-click)
eventBuilder.addEventBinding(type, "#SubmitBtn", data, true);

// Don't lock for search/filter inputs (smooth UX)
eventBuilder.addEventBinding(type, "#SearchInput", data, false);
```

### 4. Handle Null Event Data

Events may only contain some fields:

```java
@Override
public void handleDataEvent(..., PageEventData data) {
    if (data.getAction() != null) {
        handleAction(data.getAction());
    }
    if (data.getSearchQuery() != null) {
        handleSearch(data.getSearchQuery());
    }
}
```

### 5. Clean Up in onDismiss

```java
@Override
public void onDismiss(@Nonnull Ref<EntityStore> ref, @Nonnull Store<EntityStore> store) {
    // Cancel any scheduled tasks
    // Save state if needed
    // Clean up resources
}
```

## Troubleshooting

### Page Not Opening
1. Ensure you're on the world thread (`world.execute()`)
2. Verify `Ref` is valid (`ref.isValid()`)
3. Check PageManager is initialized

### Events Not Firing
1. Verify selector matches element ID in .ui file
2. Check EventData keys match codec field names
3. Ensure event type matches UI element (e.g., `ValueChanged` for inputs)

### Codec Parsing Errors
1. Keys must match exactly (including `@` prefix)
2. Types must match (STRING vs INTEGER)
3. Check codec is properly passed to constructor

### UI Not Updating
1. Call `sendUpdate()` or `rebuild()` after changes
2. Verify selectors target correct elements
3. Check `clear` parameter is correct
