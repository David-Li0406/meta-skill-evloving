/**
 * Overlays TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the overlays module (ActionBar, Dialog, Drawer, Popover, etc.).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., ActionBar.Root, Dialog.Root)
 */

import { East } from "@elaraai/east";
import { ActionBar, Avatar, Button, Dialog, Drawer, HoverCard, IconButton, Menu, Popover, Text, ToggleTip, Tooltip, UIComponentType } from "../src/index.js";

// ============================================================================
// ACTION BAR
// ============================================================================

// File: src/overlays/action-bar/index.ts
// Export: createActionBar (private function)
const actionBarExample = East.function([], UIComponentType, $ => {
    return ActionBar.Root([
        ActionBar.Action("delete", "Delete"),
        ActionBar.Separator(),
        ActionBar.Action("archive", "Archive"),
    ], {
        selectionCount: 5n,
        selectionLabel: "items selected",
    });
});
actionBarExample.toIR().compile([])();

// File: src/overlays/action-bar/index.ts
// Export: ActionBar.Root
const actionBarRootExample = East.function([], UIComponentType, $ => {
    return ActionBar.Root([
        ActionBar.Action("delete", "Delete"),
        ActionBar.Separator(),
        ActionBar.Action("archive", "Archive"),
    ], {
        selectionCount: 5n,
        selectionLabel: "items selected",
    });
});
actionBarRootExample.toIR().compile([])();

// File: src/overlays/action-bar/index.ts
// Export: ActionBar.Action
const actionBarActionExample = East.function([], UIComponentType, $ => {
    return ActionBar.Root([
        ActionBar.Action("edit", "Edit"),
        ActionBar.Action("delete", "Delete", true), // disabled
    ], {
        selectionCount: 3n,
    });
});
actionBarActionExample.toIR().compile([])();

// File: src/overlays/action-bar/index.ts
// Export: ActionBar.Separator
const actionBarSeparatorExample = East.function([], UIComponentType, $ => {
    return ActionBar.Root([
        ActionBar.Action("copy", "Copy"),
        ActionBar.Action("paste", "Paste"),
        ActionBar.Separator(),
        ActionBar.Action("delete", "Delete"),
    ], {
        selectionCount: 2n,
    });
});
actionBarSeparatorExample.toIR().compile([])();

// ============================================================================
// DIALOG
// ============================================================================

// File: src/overlays/dialog/index.ts
// Export: createDialog (private function)
const dialogExample = East.function([], UIComponentType, $ => {
    return Dialog.Root(
        Button.Root("Open Dialog"),
        [Text.Root("Dialog content here")],
        { title: "My Dialog" }
    );
});
dialogExample.toIR().compile([])();

// File: src/overlays/dialog/index.ts
// Export: Dialog.Root
const dialogRootExample = East.function([], UIComponentType, $ => {
    return Dialog.Root(
        Button.Root("Open Dialog"),
        [Text.Root("Dialog content here")],
        { title: "My Dialog" }
    );
});
dialogRootExample.toIR().compile([])();

// File: src/overlays/dialog/index.ts
// Export: Dialog.Root (with size and placement)
const dialogStyledExample = East.function([], UIComponentType, $ => {
    return Dialog.Root(
        Button.Root("Settings"),
        [Text.Root("Settings content")],
        {
            title: "Settings",
            size: "lg",
            placement: "center",
        }
    );
});
dialogStyledExample.toIR().compile([])();

// ============================================================================
// DRAWER
// ============================================================================

// File: src/overlays/drawer/index.ts
// Export: createDrawer (private function)
const drawerExample = East.function([], UIComponentType, $ => {
    return Drawer.Root(
        Button.Root("Open Menu"),
        [Text.Root("Menu content")],
        { title: "Navigation", placement: "start" }
    );
});
drawerExample.toIR().compile([])();

// File: src/overlays/drawer/index.ts
// Export: Drawer.Root
const drawerRootExample = East.function([], UIComponentType, $ => {
    return Drawer.Root(
        Button.Root("Open Drawer"),
        [Text.Root("Drawer content")],
        { title: "Settings", placement: "end" }
    );
});
drawerRootExample.toIR().compile([])();

// File: src/overlays/drawer/index.ts
// Export: Drawer.Root (with size)
const drawerSizedExample = East.function([], UIComponentType, $ => {
    return Drawer.Root(
        Button.Root("Open Large Drawer"),
        [Text.Root("Large drawer content")],
        {
            title: "Large Panel",
            placement: "end",
            size: "lg",
        }
    );
});
drawerSizedExample.toIR().compile([])();

// ============================================================================
// HOVER CARD
// ============================================================================

// File: src/overlays/hover-card/index.ts
// Export: createHoverCard (private function)
const hoverCardExample = East.function([], UIComponentType, $ => {
    return HoverCard.Root(
        Text.Root("@username"),
        [
            Avatar.Root({ name: "John Doe" }),
            Text.Root("Software Engineer"),
        ],
        { openDelay: 200n }
    );
});
hoverCardExample.toIR().compile([])();

// File: src/overlays/hover-card/index.ts
// Export: HoverCard.Root
const hoverCardRootExample = East.function([], UIComponentType, $ => {
    return HoverCard.Root(
        Text.Root("@username"),
        [
            Avatar.Root({ name: "John Doe" }),
            Text.Root("Software Engineer"),
        ],
        { openDelay: 200n }
    );
});
hoverCardRootExample.toIR().compile([])();

// File: src/overlays/hover-card/index.ts
// Export: HoverCard.Root (with placement)
const hoverCardPlacementExample = East.function([], UIComponentType, $ => {
    return HoverCard.Root(
        Text.Root("View Profile"),
        [
            Text.Root("User Information"),
            Text.Root("Additional details here"),
        ],
        { placement: "bottom", hasArrow: true }
    );
});
hoverCardPlacementExample.toIR().compile([])();

// ============================================================================
// MENU
// ============================================================================

// File: src/overlays/menu/index.ts
// Export: createMenuItem (private function)
const menuItemExample = East.function([], UIComponentType, $ => {
    return Menu.Root(
        Button.Root("Actions"),
        [
            Menu.Item("edit", "Edit"),
            Menu.Item("delete", "Delete", true),
        ]
    );
});
menuItemExample.toIR().compile([])();

// File: src/overlays/menu/index.ts
// Export: createMenuSeparator (private function)
const menuSeparatorExample = East.function([], UIComponentType, $ => {
    return Menu.Root(
        Button.Root("File"),
        [
            Menu.Item("new", "New"),
            Menu.Separator(),
            Menu.Item("exit", "Exit"),
        ]
    );
});
menuSeparatorExample.toIR().compile([])();

// File: src/overlays/menu/index.ts
// Export: createMenu (private function)
const menuExample = East.function([], UIComponentType, $ => {
    return Menu.Root(
        Button.Root("Actions"),
        [
            Menu.Item("edit", "Edit"),
            Menu.Separator(),
            Menu.Item("delete", "Delete"),
        ],
        { placement: "bottom-start" }
    );
});
menuExample.toIR().compile([])();

// File: src/overlays/menu/index.ts
// Export: Menu.Root
const menuRootExample = East.function([], UIComponentType, $ => {
    return Menu.Root(
        Button.Root("Actions"),
        [
            Menu.Item("edit", "Edit"),
            Menu.Separator(),
            Menu.Item("delete", "Delete"),
        ]
    );
});
menuRootExample.toIR().compile([])();

// File: src/overlays/menu/index.ts
// Export: Menu.Item
const menuItemExample2 = East.function([], UIComponentType, $ => {
    return Menu.Root(
        Button.Root("Actions"),
        [
            Menu.Item("edit", "Edit"),
            Menu.Item("delete", "Delete", true), // disabled
        ]
    );
});
menuItemExample2.toIR().compile([])();

// File: src/overlays/menu/index.ts
// Export: Menu.Separator
const menuSeparatorExample2 = East.function([], UIComponentType, $ => {
    return Menu.Root(
        Button.Root("File"),
        [
            Menu.Item("new", "New"),
            Menu.Item("open", "Open"),
            Menu.Separator(),
            Menu.Item("exit", "Exit"),
        ]
    );
});
menuSeparatorExample2.toIR().compile([])();

// ============================================================================
// POPOVER
// ============================================================================

// File: src/overlays/popover/index.ts
// Export: createPopover (private function)
const popoverExample = East.function([], UIComponentType, $ => {
    return Popover.Root(
        Button.Root("Edit"),
        [Text.Root("Edit your profile")],
        { title: "Edit Profile" }
    );
});
popoverExample.toIR().compile([])();

// File: src/overlays/popover/index.ts
// Export: Popover.Root
const popoverRootExample = East.function([], UIComponentType, $ => {
    return Popover.Root(
        Button.Root("Show Info"),
        [Text.Root("Popover content here")],
        { title: "Information" }
    );
});
popoverRootExample.toIR().compile([])();

// File: src/overlays/popover/index.ts
// Export: Popover.Root (with placement and arrow)
const popoverStyledExample = East.function([], UIComponentType, $ => {
    return Popover.Root(
        Button.Root("Settings"),
        [Text.Root("Settings content")],
        {
            title: "Quick Settings",
            placement: "bottom-start",
            hasArrow: true,
        }
    );
});
popoverStyledExample.toIR().compile([])();

// ============================================================================
// TOGGLE TIP
// ============================================================================

// File: src/overlays/toggle-tip/index.ts
// Export: createToggleTip (private function)
const toggleTipExample = East.function([], UIComponentType, $ => {
    return ToggleTip.Root(
        Button.Root("?", { variant: "ghost", size: "sm" }),
        "Click to learn more about this feature"
    );
});
toggleTipExample.toIR().compile([])();

// File: src/overlays/toggle-tip/index.ts
// Export: ToggleTip.Root
const toggleTipRootExample = East.function([], UIComponentType, $ => {
    return ToggleTip.Root(
        IconButton.Root("fas", "circle-info"),
        "Click for more information about this feature"
    );
});
toggleTipRootExample.toIR().compile([])();

// File: src/overlays/toggle-tip/index.ts
// Export: ToggleTip.Root (with placement and arrow)
const toggleTipStyledExample = East.function([], UIComponentType, $ => {
    return ToggleTip.Root(
        Button.Root("Help"),
        "This provides additional context",
        { placement: "bottom", hasArrow: true }
    );
});
toggleTipStyledExample.toIR().compile([])();

// ============================================================================
// TOOLTIP
// ============================================================================

// File: src/overlays/tooltip/index.ts
// Export: createTooltip (private function)
const tooltipExample = East.function([], UIComponentType, $ => {
    return Tooltip.Root(
        Button.Root("Hover me"),
        "This is a helpful tip"
    );
});
tooltipExample.toIR().compile([])();

// File: src/overlays/tooltip/index.ts
// Export: Tooltip.Root
const tooltipRootExample = East.function([], UIComponentType, $ => {
    return Tooltip.Root(
        Button.Root("Hover me"),
        "This is a helpful tooltip",
        { placement: "top" }
    );
});
tooltipRootExample.toIR().compile([])();

// File: src/overlays/tooltip/types.ts
// Export: Placement helper function
const tooltipPlacementExample = East.function([], UIComponentType, $ => {
    return Tooltip.Root(
        Button.Root("Hover"),
        "Help text",
        { placement: Tooltip.Placement("top") }
    );
});
tooltipPlacementExample.toIR().compile([])();

// File: src/overlays/tooltip/index.ts
// Export: Tooltip.Root (with arrow)
const tooltipArrowExample = East.function([], UIComponentType, $ => {
    return Tooltip.Root(
        Button.Root("Save"),
        "Save your changes",
        { placement: "bottom", hasArrow: true }
    );
});
tooltipArrowExample.toIR().compile([])();

console.log("Overlays TypeDoc examples compiled and executed successfully!");
