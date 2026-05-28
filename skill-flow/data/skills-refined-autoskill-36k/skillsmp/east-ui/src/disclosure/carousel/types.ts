/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    StringType,
    IntegerType,
    BooleanType,
    FunctionType,
    NullType,
} from "@elaraai/east";

import { OrientationType } from "../../style.js";
import type { OrientationLiteral } from "../../style.js";

// Re-export OrientationType for convenience
export { OrientationType, type OrientationLiteral } from "../../style.js";

// ============================================================================
// Carousel Style Type
// ============================================================================

/**
 * Style type for Carousel component.
 *
 * @remarks
 * Contains presentation options for the carousel.
 *
 * @property orientation - Slide direction (horizontal or vertical)
 * @property spacing - Gap between slides (Chakra spacing token)
 * @property padding - Viewport padding
 * @property onIndexChange - Callback triggered when active slide changes
 */
export const CarouselStyleType = StructType({
    /** Slide direction (horizontal or vertical) */
    orientation: OptionType(OrientationType),
    /** Gap between slides (Chakra spacing token) */
    spacing: OptionType(StringType),
    /** Viewport padding */
    padding: OptionType(StringType),
    /** Callback triggered when active slide changes */
    onIndexChange: OptionType(FunctionType([IntegerType], NullType)),
});

/**
 * Type representing the CarouselStyle structure.
 */
export type CarouselStyleType = typeof CarouselStyleType;

// ============================================================================
// Carousel Style Interface
// ============================================================================

/**
 * TypeScript interface for Carousel style options.
 *
 * @property orientation - Slide direction (horizontal or vertical)
 * @property spacing - Gap between slides (Chakra spacing token)
 * @property padding - Viewport padding
 * @property index - Controlled current slide index
 * @property defaultIndex - Initial slide index
 * @property slidesPerView - Number of visible slides
 * @property slidesPerMove - Number of slides to advance per step
 * @property loop - Whether to enable infinite scrolling
 * @property autoplay - Whether to enable automatic advancement
 * @property allowMouseDrag - Whether to allow mouse drag navigation
 * @property showIndicators - Whether to show dot indicators
 * @property showControls - Whether to show prev/next controls
 * @property onIndexChange - Callback triggered when active slide changes
 */
export interface CarouselStyle {
    /** Slide direction (horizontal or vertical) */
    orientation?: SubtypeExprOrValue<OrientationType> | OrientationLiteral;
    /** Gap between slides (Chakra spacing token) */
    spacing?: SubtypeExprOrValue<StringType>;
    /** Viewport padding */
    padding?: SubtypeExprOrValue<StringType>;
    /** Controlled current slide index */
    index?: SubtypeExprOrValue<IntegerType>;
    /** Initial slide index */
    defaultIndex?: SubtypeExprOrValue<IntegerType>;
    /** Number of visible slides */
    slidesPerView?: SubtypeExprOrValue<IntegerType>;
    /** Number of slides to advance per step */
    slidesPerMove?: SubtypeExprOrValue<IntegerType>;
    /** Whether to enable infinite scrolling */
    loop?: SubtypeExprOrValue<BooleanType>;
    /** Whether to enable automatic advancement */
    autoplay?: SubtypeExprOrValue<BooleanType>;
    /** Whether to allow mouse drag navigation */
    allowMouseDrag?: SubtypeExprOrValue<BooleanType>;
    /** Whether to show dot indicators */
    showIndicators?: SubtypeExprOrValue<BooleanType>;
    /** Whether to show prev/next controls */
    showControls?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when active slide changes */
    onIndexChange?: SubtypeExprOrValue<FunctionType<[IntegerType], NullType>>;
}
