/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type ExprType,
    type SubtypeExprOrValue,
    East,
    variant,
    ArrayType,
    OptionType,
    StructType,
    IntegerType,
    BooleanType,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";
import { OrientationType } from "../../style.js";
import {
    CarouselStyleType,
    type CarouselStyle,
} from "./types.js";

// Re-export types
export {
    CarouselStyleType,
    OrientationType,
    type CarouselStyle,
    type OrientationLiteral,
} from "./types.js";

// ============================================================================
// Carousel Root Type
// ============================================================================

/**
 * Type for Carousel component data.
 *
 * @remarks
 * Carousel displays a slideshow of content items.
 *
 * @property items - Array of carousel slide items
 * @property index - Controlled current slide index
 * @property defaultIndex - Initial slide index
 * @property slidesPerView - Number of visible slides
 * @property slidesPerMove - Number of slides to advance per step
 * @property loop - Whether to enable infinite scrolling
 * @property autoplay - Whether to enable automatic advancement
 * @property allowMouseDrag - Whether to allow mouse drag navigation
 * @property showIndicators - Whether to show dot indicators
 * @property showControls - Whether to show prev/next controls
 * @property style - Optional styling configuration
 */
export const CarouselRootType: StructType<{
    items: ArrayType<UIComponentType>,
    index: OptionType<IntegerType>,
    defaultIndex: OptionType<IntegerType>,
    slidesPerView: OptionType<IntegerType>,
    slidesPerMove: OptionType<IntegerType>,
    loop: OptionType<BooleanType>,
    autoplay: OptionType<BooleanType>,
    allowMouseDrag: OptionType<BooleanType>,
    showIndicators: OptionType<BooleanType>,
    showControls: OptionType<BooleanType>,
    style: OptionType<CarouselStyleType>,
}> = StructType({
    items: ArrayType(UIComponentType),
    index: OptionType(IntegerType),
    defaultIndex: OptionType(IntegerType),
    slidesPerView: OptionType(IntegerType),
    slidesPerMove: OptionType(IntegerType),
    loop: OptionType(BooleanType),
    autoplay: OptionType(BooleanType),
    allowMouseDrag: OptionType(BooleanType),
    showIndicators: OptionType(BooleanType),
    showControls: OptionType(BooleanType),
    style: OptionType(CarouselStyleType),
});

/**
 * Type representing the Carousel structure.
 */
export type CarouselRootType = typeof CarouselRootType;

// ============================================================================
// Carousel Factory
// ============================================================================

/**
 * Creates a Carousel component.
 *
 * @param items - Array of carousel items/slides
 * @param style - Optional style and configuration options
 * @returns An East expression representing the Carousel component
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Carousel, Box, Text, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     return Carousel.Root([
 *         Box.Root([Text.Root("Slide 1")]),
 *         Box.Root([Text.Root("Slide 2")]),
 *         Box.Root([Text.Root("Slide 3")]),
 *     ], {
 *         loop: true,
 *         showIndicators: true,
 *         showControls: true,
 *     });
 * });
 * ```
 */
function createCarousel(
    items: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: CarouselStyle
): ExprType<UIComponentType> {
    // Convert string literal orientation to East value
    const orientationValue = style?.orientation
        ? (typeof style.orientation === "string"
            ? East.value(variant(style.orientation, null), OrientationType)
            : style.orientation)
        : undefined;

    // Build style object if any style properties are provided
    const hasStyleProps = orientationValue || style?.spacing || style?.padding || style?.onIndexChange !== undefined;
    const styleValue = hasStyleProps
        ? variant("some", East.value({
            orientation: orientationValue ? variant("some", orientationValue) : variant("none", null),
            spacing: style?.spacing !== undefined ? variant("some", style.spacing) : variant("none", null),
            padding: style?.padding !== undefined ? variant("some", style.padding) : variant("none", null),
            onIndexChange: style?.onIndexChange !== undefined ? variant("some", style.onIndexChange) : variant("none", null),
        }, CarouselStyleType))
        : variant("none", null);

    return East.value(variant("Carousel", {
        items: items,
        index: style?.index !== undefined ? variant("some", style.index) : variant("none", null),
        defaultIndex: style?.defaultIndex !== undefined ? variant("some", style.defaultIndex) : variant("none", null),
        slidesPerView: style?.slidesPerView !== undefined ? variant("some", style.slidesPerView) : variant("none", null),
        slidesPerMove: style?.slidesPerMove !== undefined ? variant("some", style.slidesPerMove) : variant("none", null),
        loop: style?.loop !== undefined ? variant("some", style.loop) : variant("none", null),
        autoplay: style?.autoplay !== undefined ? variant("some", style.autoplay) : variant("none", null),
        allowMouseDrag: style?.allowMouseDrag !== undefined ? variant("some", style.allowMouseDrag) : variant("none", null),
        showIndicators: style?.showIndicators !== undefined ? variant("some", style.showIndicators) : variant("none", null),
        showControls: style?.showControls !== undefined ? variant("some", style.showControls) : variant("none", null),
        style: styleValue,
    }), UIComponentType);
}

// ============================================================================
// Carousel Namespace Export
// ============================================================================

/**
 * Carousel component namespace.
 *
 * @remarks
 * Carousel provides a slideshow component for cycling through content.
 */
export const Carousel = {
    /**
     * Creates a Carousel component for sliding content.
     *
     * @param items - Array of UI components to display as slides
     * @param style - Optional styling and behavior configuration
     * @returns An East expression representing the carousel component
     *
     * @remarks
     * Carousel displays a slideshow of content items with optional navigation
     * controls, indicators, autoplay, and infinite loop support. Supports
     * multiple slides per view for gallery layouts.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Carousel, Box, Text, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Carousel.Root([
     *         Box.Root([Text.Root("Slide 1")]),
     *         Box.Root([Text.Root("Slide 2")]),
     *     ], {
     *         showControls: true,
     *         showIndicators: true,
     *     });
     * });
     * ```
     */
    Root: createCarousel,
    Types: {
        /**
         * The concrete East type for Carousel container data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Carousel
         * component. Contains the array of slides and all configuration options for
         * navigation, display, and behavior.
         *
         * @property items - Array of UI components to display as slides (ArrayType<UIComponentType>)
         * @property index - Controlled current slide index (OptionType<IntegerType>)
         * @property defaultIndex - Initial slide index (OptionType<IntegerType>)
         * @property slidesPerView - Number of visible slides at once (OptionType<IntegerType>)
         * @property slidesPerMove - Number of slides to advance per navigation step (OptionType<IntegerType>)
         * @property loop - Whether to enable infinite scrolling (OptionType<BooleanType>)
         * @property autoplay - Whether to enable automatic slide advancement (OptionType<BooleanType>)
         * @property allowMouseDrag - Whether to allow mouse drag navigation (OptionType<BooleanType>)
         * @property showIndicators - Whether to show dot indicators (OptionType<BooleanType>)
         * @property showControls - Whether to show prev/next controls (OptionType<BooleanType>)
         * @property style - Optional styling configuration (OptionType<CarouselStyleType>)
         */
        Root: CarouselRootType,
        /**
         * The concrete East type for Carousel style configuration.
         *
         * @remarks
         * This struct type defines the visual styling configuration for a Carousel
         * component. Controls the slide direction, spacing between slides, and
         * viewport padding.
         *
         * @property orientation - Slide direction: horizontal or vertical (OptionType<OrientationType>)
         * @property spacing - Gap between slides as Chakra spacing token (OptionType<StringType>)
         * @property padding - Padding around the carousel viewport (OptionType<StringType>)
         */
        Style: CarouselStyleType,
    },
} as const;
