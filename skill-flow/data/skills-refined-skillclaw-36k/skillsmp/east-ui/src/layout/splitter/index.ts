/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    OptionType,
    StructType,
    ArrayType,
    variant,
    StringType,
    FloatType,
    BooleanType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { OrientationType } from "../../style.js";
import {
    SplitterStyleType,
    type SplitterStyle,
    type SplitterPanelStyle,
    SplitterResizeDetailsType,
} from "./types.js";

// Re-export style types
export {
    SplitterStyleType,
    SplitterPanelStyleType,
    SplitterResizeDetailsType,
    type SplitterStyle,
    type SplitterPanelStyle,
} from "./types.js";

// ============================================================================
// Splitter Panel Type
// ============================================================================

/**
 * The concrete East type for Splitter panel data.
 *
 * @remarks
 * This struct type represents a single panel within a Splitter.
 * Each panel has an identifier, content, and optional sizing constraints.
 *
 * @property id - Unique identifier for the panel
 * @property content - The UI component to render in this panel
 * @property minSize - Minimum size as a percentage (0-100)
 * @property maxSize - Maximum size as a percentage (0-100)
 * @property collapsible - Whether the panel can be collapsed
 * @property defaultCollapsed - Whether the panel starts collapsed
 */
export const SplitterPanelType: StructType<{
    id: StringType,
    content: UIComponentType,
    minSize: OptionType<FloatType>,
    maxSize: OptionType<FloatType>,
    collapsible: OptionType<BooleanType>,
    defaultCollapsed: OptionType<BooleanType>,
}> = StructType({
    id: StringType,
    content: UIComponentType,
    minSize: OptionType(FloatType),
    maxSize: OptionType(FloatType),
    collapsible: OptionType(BooleanType),
    defaultCollapsed: OptionType(BooleanType),
});

/**
 * Type representing the Splitter panel structure.
 */
export type SplitterPanelType = typeof SplitterPanelType;

// ============================================================================
// Splitter Type
// ============================================================================

/**
 * The concrete East type for Splitter component data.
 *
 * @remarks
 * This struct type represents the serializable data structure for a Splitter component.
 * Splitter provides resizable panels with draggable dividers between them.
 *
 * @property panels - Array of panel configurations
 * @property defaultSize - Initial sizes for each panel as percentages
 * @property style - Optional styling configuration wrapped in OptionType
 */
export const SplitterType: StructType<{
    panels: ArrayType<SplitterPanelType>,
    defaultSize: ArrayType<FloatType>,
    style: OptionType<SplitterStyleType>,
}> = StructType({
    panels: ArrayType(SplitterPanelType),
    defaultSize: ArrayType(FloatType),
    style: OptionType(SplitterStyleType),
});

/**
 * Type representing the Splitter component structure.
 */
export type SplitterType = typeof SplitterType;

// ============================================================================
// Splitter Panel Function
// ============================================================================

/**
 * Creates a Splitter panel with content and configuration.
 *
 * @param content - The UI component to render in this panel
 * @param config - Panel configuration including id and optional constraints
 * @returns An East expression representing the splitter panel
 *
 * @remarks
 * Splitter panels can have size constraints and collapsibility settings.
 * The id is used to identify the panel for resize triggers.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Splitter, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Splitter.Root(
 *         [
 *             Splitter.Panel(Text.Root("Sidebar"), { id: "sidebar", minSize: 20 }),
 *             Splitter.Panel(Text.Root("Main"), { id: "main", collapsible: true }),
 *         ],
 *         [30.0, 70.0],
 *         { orientation: "horizontal" }
 *     );
 * });
 * ```
 */
function SplitterPanel(
    content: SubtypeExprOrValue<UIComponentType>,
    config: SplitterPanelStyle
): ExprType<SplitterPanelType> {
    const toFloatOption = (value: SubtypeExprOrValue<FloatType> | undefined) => {
        if (value === undefined) return variant("none", null);
        return variant("some", value);
    };

    const toBoolOption = (value: SubtypeExprOrValue<BooleanType> | undefined) => {
        if (value === undefined) return variant("none", null);
        return variant("some", value);
    };

    return East.value({
        id: config.id,
        content: content,
        minSize: toFloatOption(config.minSize),
        maxSize: toFloatOption(config.maxSize),
        collapsible: toBoolOption(config.collapsible),
        defaultCollapsed: toBoolOption(config.defaultCollapsed),
    }, SplitterPanelType);
}

// ============================================================================
// Splitter Root Function
// ============================================================================

/**
 * Creates a Splitter container with panels and optional styling.
 *
 * @param panels - Array of panels created with Splitter.Panel
 * @param defaultSize - Array of initial sizes (percentages) for each panel
 * @param style - Optional styling configuration for the splitter
 * @returns An East expression representing the styled splitter component
 *
 * @remarks
 * Splitter provides resizable panels with draggable dividers.
 * The defaultSize array must have the same length as the panels array,
 * with values representing percentages that should sum to 100.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Splitter, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Splitter.Root(
 *         [
 *             Splitter.Panel(Text.Root("Left Panel"), { id: "left" }),
 *             Splitter.Panel(Text.Root("Right Panel"), { id: "right" }),
 *         ],
 *         [50.0, 50.0],
 *         { orientation: "horizontal" }
 *     );
 * });
 * ```
 */
function SplitterRoot(
    panels: SubtypeExprOrValue<ArrayType<SplitterPanelType>>,
    defaultSize: SubtypeExprOrValue<ArrayType<FloatType>>,
    style?: SplitterStyle
): ExprType<UIComponentType> {
    const panels_expr = East.value(panels, ArrayType(SplitterPanelType));
    const orientationValue = style?.orientation
        ? (typeof style.orientation === "string"
            ? East.value(variant(style.orientation, null), OrientationType)
            : style.orientation)
        : undefined;

    const hasStyle = orientationValue || style?.onResize !== undefined || style?.onResizeStart !== undefined || style?.onResizeEnd !== undefined;

    return East.value(variant("Splitter", {
        panels: panels_expr,
        defaultSize: defaultSize,
        style: hasStyle ? variant("some", East.value({
            orientation: orientationValue ? variant("some", orientationValue) : variant("none", null),
            onResize: style?.onResize !== undefined ? variant("some", style.onResize) : variant("none", null),
            onResizeStart: style?.onResizeStart !== undefined ? variant("some", style.onResizeStart) : variant("none", null),
            onResizeEnd: style?.onResizeEnd !== undefined ? variant("some", style.onResizeEnd) : variant("none", null),
        }, SplitterStyleType)) : variant("none", null),
    }), UIComponentType);
}

// ============================================================================
// Splitter Namespace Export
// ============================================================================

/**
 * Splitter compound component for resizable panel layouts.
 *
 * @remarks
 * Splitter provides resizable panels separated by draggable dividers.
 * Use `Splitter.Root(panels, defaultSize, style)` to create the container and `Splitter.Panel(content, config)` for each section.
 */
export const Splitter = {
    /**
     * Creates a Splitter container with panels and optional styling.
     *
     * @param panels - Array of panels created with Splitter.Panel
     * @param defaultSize - Array of initial sizes (percentages) for each panel
     * @param style - Optional styling configuration for the splitter
     * @returns An East expression representing the styled splitter component
     *
     * @remarks
     * Splitter provides resizable panels with draggable dividers.
     * The defaultSize array must have the same length as the panels array,
     * with values representing percentages that should sum to 100.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Splitter, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Splitter.Root(
     *         [
     *             Splitter.Panel(Text.Root("Left Panel"), { id: "left" }),
     *             Splitter.Panel(Text.Root("Right Panel"), { id: "right" }),
     *         ],
     *         [50.0, 50.0],
     *         { orientation: "horizontal" }
     *     );
     * });
     * ```
     */
    Root: SplitterRoot,
    /**
     * Creates a Splitter panel with content and configuration.
     *
     * @param content - The UI component to render in this panel
     * @param config - Panel configuration including id and optional constraints
     * @returns An East expression representing the splitter panel
     *
     * @remarks
     * Splitter panels can have size constraints and collapsibility settings.
     * The id is used to identify the panel for resize triggers.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Splitter, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Splitter.Root(
     *         [
     *             Splitter.Panel(Text.Root("Sidebar"), { id: "sidebar", minSize: 20 }),
     *             Splitter.Panel(Text.Root("Main"), { id: "main", collapsible: true }),
     *         ],
     *         [30.0, 70.0],
     *         { orientation: "horizontal" }
     *     );
     * });
     * ```
     */
    Panel: SplitterPanel,
    Types: {
        /**
         * The concrete East type for Splitter component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Splitter component.
         * Splitter provides resizable panels with draggable dividers between them.
         *
         * @property panels - Array of panel configurations
         * @property defaultSize - Initial sizes for each panel as percentages
         * @property style - Optional styling configuration wrapped in OptionType
         */
        Splitter: SplitterType,
        /**
         * The concrete East type for Splitter panel data.
         *
         * @remarks
         * This struct type represents a single panel within a Splitter.
         * Each panel has an identifier, content, and optional sizing constraints.
         *
         * @property id - Unique identifier for the panel
         * @property content - The UI component to render in this panel
         * @property minSize - Minimum size as a percentage (0-100)
         * @property maxSize - Maximum size as a percentage (0-100)
         * @property collapsible - Whether the panel can be collapsed
         * @property defaultCollapsed - Whether the panel starts collapsed
         */
        Panel: SplitterPanelType,
        /**
         * Style type for Splitter container configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for the Splitter container.
         * It controls the layout orientation of the panels.
         *
         * @property orientation - Layout orientation (horizontal or vertical)
         */
        Style: SplitterStyleType,
        /**
         * Resize details type for onResize callback.
         *
         * @remarks
         * This struct type contains the size array passed to resize callbacks.
         *
         * @property size - Array of panel sizes as percentages
         */
        ResizeDetails: SplitterResizeDetailsType,
    }
} as const;
