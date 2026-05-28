/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    BooleanType,
    IntegerType,
    OptionType,
    StructType,
    ArrayType,
    variant,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import {
    ActionBarItemType,
    ActionBarStyleType,
    type ActionBarStyle,
} from "./types.js";

// Re-export types
export {
    ActionBarItemType,
    ActionBarStyleType,
    type ActionBarStyle,
} from "./types.js";

// ============================================================================
// ActionBar Type
// ============================================================================

/**
 * East StructType for ActionBar component.
 *
 * @remarks
 * ActionBar is a floating bar that appears when items are selected.
 * It displays the selection count and provides batch action buttons.
 *
 * @property items - Array of action items (actions or separators)
 * @property selectionCount - Number of selected items
 * @property selectionLabel - Label for selection (e.g., "items selected")
 * @property style - Optional style configuration
 */
export const ActionBarType: StructType<{
    items: ArrayType<ActionBarItemType>,
    selectionCount: OptionType<IntegerType>,
    selectionLabel: OptionType<StringType>,
    style: OptionType<ActionBarStyleType>,
}> = StructType({
    items: ArrayType(ActionBarItemType),
    selectionCount: OptionType(IntegerType),
    selectionLabel: OptionType(StringType),
    style: OptionType(ActionBarStyleType),
});

/**
 * Type alias for ActionBarType.
 */
export type ActionBarType = typeof ActionBarType;

// ============================================================================
// ActionBar Item Factory
// ============================================================================

/**
 * Creates an Action item for the ActionBar.
 *
 * @param value - Unique identifier for the action
 * @param label - Display label for the action button
 * @param disabled - Whether the action is disabled
 * @returns An East expression representing the action item
 */
function createAction(
    value: SubtypeExprOrValue<StringType>,
    label: SubtypeExprOrValue<StringType>,
    disabled?: SubtypeExprOrValue<BooleanType>
): ExprType<ActionBarItemType> {
    return East.value(variant("Action", {
        value: value,
        label: label,
        disabled: disabled !== undefined ? variant("some", disabled) : variant("none", null),
    }), ActionBarItemType);
}

/**
 * Creates a Separator item for the ActionBar.
 *
 * @returns An East expression representing a separator
 */
function createSeparator(): ExprType<ActionBarItemType> {
    return East.value(variant("Separator", null), ActionBarItemType);
}

// ============================================================================
// ActionBar Function
// ============================================================================

/**
 * Creates an ActionBar component with action items.
 *
 * @param items - Array of action items (use ActionBar.Action and ActionBar.Separator)
 * @param style - Optional styling configuration
 * @returns An East expression representing the action bar component
 *
 * @remarks
 * ActionBar displays a floating bar with batch actions for selected items.
 * Typically used in data tables or lists with multi-select functionality.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { ActionBar, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return ActionBar.Root([
 *         ActionBar.Action("delete", "Delete"),
 *         ActionBar.Separator(),
 *         ActionBar.Action("archive", "Archive"),
 *     ], {
 *         selectionCount: 5n,
 *         selectionLabel: "items selected",
 *     });
 * });
 * ```
 */
function createActionBar(
    items: SubtypeExprOrValue<ArrayType<ActionBarItemType>>,
    style?: ActionBarStyle
): ExprType<UIComponentType> {
    const hasStyle = style?.onSelect !== undefined || style?.onOpenChange !== undefined;

    return East.value(variant("ActionBar", {
        items: items,
        selectionCount: style?.selectionCount !== undefined ? variant("some", style.selectionCount) : variant("none", null),
        selectionLabel: style?.selectionLabel !== undefined ? variant("some", style.selectionLabel) : variant("none", null),
        style: hasStyle
            ? variant("some", East.value({
                onSelect: style?.onSelect !== undefined ? variant("some", style.onSelect) : variant("none", null),
                onOpenChange: style?.onOpenChange !== undefined ? variant("some", style.onOpenChange) : variant("none", null),
            }, ActionBarStyleType))
            : variant("none", null),
    }), UIComponentType);
}

/**
 * ActionBar component for batch actions on selected items.
 *
 * @remarks
 * Use `ActionBar.Root(items, style)` to create an action bar, or use
 * `ActionBar.Action()` and `ActionBar.Separator()` to create items.
 */
export const ActionBar = {
    /**
     * Creates an ActionBar component with action items.
     *
     * @param items - Array of action items (use ActionBar.Action and ActionBar.Separator)
     * @param style - Optional styling configuration
     * @returns An East expression representing the action bar component
     *
     * @remarks
     * ActionBar displays a floating bar with batch actions for selected items.
     * Typically used in data tables or lists with multi-select functionality.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { ActionBar, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return ActionBar.Root([
     *         ActionBar.Action("delete", "Delete"),
     *         ActionBar.Separator(),
     *         ActionBar.Action("archive", "Archive"),
     *     ], {
     *         selectionCount: 5n,
     *         selectionLabel: "items selected",
     *     });
     * });
     * ```
     */
    Root: createActionBar,
    /**
     * Creates an Action item for the ActionBar.
     *
     * @param value - Unique identifier for the action
     * @param label - Display label for the action button
     * @param disabled - Whether the action is disabled
     * @returns An East expression representing the action item
     *
     * @remarks
     * Action items are clickable buttons within an ActionBar. Each action
     * has a unique value for identification and a label for display.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { ActionBar, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return ActionBar.Root([
     *         ActionBar.Action("edit", "Edit"),
     *         ActionBar.Action("delete", "Delete", true), // disabled
     *     ], {
     *         selectionCount: 3n,
     *     });
     * });
     * ```
     */
    Action: createAction,
    /**
     * Creates a Separator item for visual grouping.
     *
     * @returns An East expression representing a separator
     *
     * @remarks
     * Separators create visual dividers between groups of actions.
     * Use them to organize related actions within an ActionBar.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { ActionBar, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return ActionBar.Root([
     *         ActionBar.Action("copy", "Copy"),
     *         ActionBar.Action("paste", "Paste"),
     *         ActionBar.Separator(),
     *         ActionBar.Action("delete", "Delete"),
     *     ], {
     *         selectionCount: 2n,
     *     });
     * });
     * ```
     */
    Separator: createSeparator,
    Types: {
        /**
         * East StructType for ActionBar component.
         *
         * @remarks
         * ActionBar is a floating bar that appears when items are selected.
         * It displays the selection count and provides batch action buttons.
         *
         * @property items - Array of action items (actions or separators)
         * @property selectionCount - Number of selected items
         * @property selectionLabel - Label for selection (e.g., "items selected")
         * @property style - Optional style configuration
         */
        ActionBar: ActionBarType,
        /**
         * Action bar item variant type.
         *
         * @property Action - A clickable action with value and label
         * @property Separator - A visual separator between actions
         */
        Item: ActionBarItemType,
        /**
         * Style type for ActionBar component.
         *
         * @remarks
         * ActionBar has fixed styling - no size/variant options.
         */
        Style: ActionBarStyleType,
    },
} as const;
