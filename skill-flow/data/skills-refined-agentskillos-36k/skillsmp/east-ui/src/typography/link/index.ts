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
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { LinkType, LinkVariantType, type LinkStyle } from "./types.js";

// Re-export types
export { LinkType, LinkVariantType, type LinkStyle } from "./types.js";

// ============================================================================
// Link Component
// ============================================================================

/**
 * Creates a Link component for navigation.
 *
 * @param value - The link text to display
 * @param href - URL the link points to
 * @param style - Optional styling configuration
 * @returns An East expression representing the link component
 */
function createLink(
    value: SubtypeExprOrValue<StringType>,
    href: SubtypeExprOrValue<StringType>,
    style?: LinkStyle
): ExprType<UIComponentType> {
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), LinkVariantType)
            : style.variant)
        : undefined;

    const externalValue = style?.external !== undefined
        ? (typeof style.external === "boolean"
            ? style.external
            : style.external)
        : undefined;

    return East.value(variant("Link", {
        value: value,
        href: href,
        external: externalValue !== undefined ? variant("some", externalValue) : variant("none", null),
        variant: variantValue ? variant("some", variantValue) : variant("none", null),
        colorPalette: style?.colorPalette ? variant("some", style.colorPalette) : variant("none", null),
    }), UIComponentType);
}

/**
 * Link component for accessible navigation.
 *
 * @remarks
 * Use `Link.Root(value, href, style)` to create navigation links.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Link, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Link.Root("Visit our site", "https://example.com", {
 *         external: true,
 *         colorPalette: "blue",
 *     });
 * });
 * ```
 */
export const Link = {
    Root: createLink,
    Types: {
        Link: LinkType,
        Variant: LinkVariantType,
    },
} as const;
