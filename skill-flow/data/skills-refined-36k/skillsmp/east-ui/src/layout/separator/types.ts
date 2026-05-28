/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StringType,
    StructType,
    VariantType,
    NullType,
} from "@elaraai/east";

import {
    OrientationType,
    SizeType,
} from "../../style.js";
import type {
    OrientationLiteral,
    SizeLiteral,
} from "../../style.js";

/**
 * Separator variant type for line style.
 *
 * @remarks
 * Create instances using East's variant function.
 *
 * @property solid - Solid continuous line
 * @property dashed - Dashed line
 * @property dotted - Dotted line
 */
export const SeparatorVariantType = VariantType({
    solid: NullType,
    dashed: NullType,
    dotted: NullType,
});

/**
 * Type representing separator variant values.
 */
export type SeparatorVariantType = typeof SeparatorVariantType;

/**
 * String literal type for separator variant values.
 */
export type SeparatorVariantLiteral = "solid" | "dashed" | "dotted";

/**
 * Style configuration for Separator components.
 *
 * @remarks
 * Separator is a visual divider between content sections.
 *
 * @property orientation - Orientation (horizontal or vertical)
 * @property variant - Line style variant (solid, dashed, dotted)
 * @property size - Thickness size
 * @property color - Color (Chakra UI color token or CSS color)
 * @property label - Optional label text in the middle of the separator
 */
export type SeparatorStyle = {
    /** Orientation (horizontal or vertical) */
    orientation?: SubtypeExprOrValue<OrientationType> | OrientationLiteral;
    /** Line style variant */
    variant?: SubtypeExprOrValue<SeparatorVariantType> | SeparatorVariantLiteral;
    /** Thickness size */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Color (Chakra UI color token or CSS color) */
    color?: SubtypeExprOrValue<StringType>;
    /** Optional label text in the middle of the separator */
    label?: SubtypeExprOrValue<StringType>;
};

/**
 * The concrete East type for Separator component style data.
 *
 * @remarks
 * All properties are optional and wrapped in {@link OptionType}.
 *
 * @property orientation - Orientation (horizontal or vertical)
 * @property variant - Line style variant (solid, dashed, dotted)
 * @property size - Thickness size
 * @property color - Color (Chakra UI color token or CSS color)
 * @property label - Optional label text in the middle of the separator
 */
export const SeparatorStyleType = StructType({
    orientation: OptionType(OrientationType),
    variant: OptionType(SeparatorVariantType),
    size: OptionType(SizeType),
    color: OptionType(StringType),
    label: OptionType(StringType),
});

/**
 * Type representing Separator style structure.
 */
export type SeparatorStyleType = typeof SeparatorStyleType;
