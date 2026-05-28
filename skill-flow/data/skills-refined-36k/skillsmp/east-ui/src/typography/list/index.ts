/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    type ExprType,
    East,
    StringType,
    variant,
    ArrayType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { ListType, ListVariantType, type ListStyle } from "./types.js";

// Re-export types
export { ListType, ListVariantType, type ListStyle } from "./types.js";

/**
 * Creates a List component.
 *
 * @param items - Array of list items (strings or config objects)
 * @param style - Optional styling configuration
 * @returns An East expression representing the list component
 */
function createList(
    items: SubtypeExprOrValue<ArrayType<StringType>>,
    style?: ListStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), ListVariantType)
            : style.variant)
        : undefined;

    return East.value(variant("List", {
        items,
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        gap: style?.gap ? variant("some", style.gap) : variant("none", null),
        colorPalette: style?.colorPalette ? variant("some", style.colorPalette) : variant("none", null),
    }), UIComponentType);
}

/**
 * List component for ordered and unordered lists.
 *
 * @remarks
 * Use `List.Root(items, style)` to create lists with an array of string items.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { List, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return List.Root([
 *         "First item",
 *         "Second item",
 *         "Third item",
 *     ], {
 *         variant: "unordered",
 *         gap: "2",
 *     });
 * });
 * ```
 */
export const List = {
    Root: createList,
    Types: {
        List: ListType,
        Variant: ListVariantType,
    },
} as const;
