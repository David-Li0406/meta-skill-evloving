/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    StringType,
    variant,
    some,
    none,
} from "@elaraai/east";

import { ColorSchemeType, StyleVariantType } from "../../style.js";
import { UIComponentType } from "../../component.js";
import { TagType, TagSizeType, type TagStyle } from "./types.js";

// Re-export types
export { TagType, TagSizeType, type TagStyle, type TagSizeLiteral } from "./types.js";

// ============================================================================
// Tag Function
// ============================================================================

/**
 * Creates a Tag component with label and optional styling.
 *
 * @param label - The tag text content
 * @param style - Optional styling configuration
 * @returns An East expression representing the tag component
 *
 * @remarks
 * Tag is used for categorization and filtering. Common uses include
 * filter chips, labels, and removable categories.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Tag, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Tag.Root("Featured", {
 *         colorPalette: "blue",
 *         variant: "solid",
 *     });
 * });
 * ```
 */
function createTag(
    label: SubtypeExprOrValue<StringType>,
    style?: TagStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), StyleVariantType)
            : style.variant)
        : undefined;

    const colorPaletteValue = style?.colorPalette
        ? (typeof style.colorPalette === "string"
            ? East.value(variant(style.colorPalette, null), ColorSchemeType)
            : style.colorPalette)
        : undefined;

    const sizeValue = style?.size
        ? (typeof style.size === "string"
            ? East.value(variant(style.size, null), TagSizeType)
            : style.size)
        : undefined;

    return East.value(variant("Tag", {
        label: label,
        variant: variantValue ? some(variantValue) : none,
        colorPalette: colorPaletteValue ? some(colorPaletteValue) : none,
        size: sizeValue ? some(sizeValue) : none,
        closable: style?.closable !== undefined ? some(style.closable) : none,
        onClose: style?.onClose ? some(style.onClose) : none,
        opacity: style?.opacity !== undefined ? some(style.opacity) : none,
        color: style?.color ? some(style.color) : none,
        background: style?.background ? some(style.background) : none,
    }), UIComponentType);
}

/**
 * Tag component for categorization, filtering, and labeling.
 *
 * @remarks
 * Use `Tag.Root(label, style)` to create a tag, or access `Tag.Types.Tag` for the East type.
 */
export const Tag = {
    /**
     * Creates a Tag component with label and optional styling.
     *
     * @param label - The tag text content
     * @param style - Optional styling configuration
     * @returns An East expression representing the tag component
     *
     * @remarks
     * Tag is used for categorization and filtering. Common uses include
     * filter chips, labels, and removable categories.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Tag, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Tag.Root("Featured", {
     *         colorPalette: "blue",
     *         variant: "solid",
     *     });
     * });
     * ```
     */
    Root: createTag,
    Types: {
        /**
         * Type for Tag component data.
         *
         * @remarks
         * Tag is used for categorization, filtering, and labeling items.
         * Unlike Badge, Tags can be closable/removable.
         *
         * @property label - The tag text content
         * @property variant - Visual variant (solid, subtle, outline)
         * @property colorPalette - Color scheme for the tag
         * @property size - Size of the tag (sm, md, lg, xl)
         * @property closable - Whether the tag shows a close button
         */
        Tag: TagType,
        /**
         * Size variant type for Tag component.
         *
         * @remarks
         * Tag supports sm, md, lg, and xl sizes (no xs).
         *
         * @property sm - Small size
         * @property md - Medium size (default)
         * @property lg - Large size
         * @property xl - Extra large size
         */
        Size: TagSizeType,
    },
} as const;
