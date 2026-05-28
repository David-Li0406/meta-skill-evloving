/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { East, NullType, variant, VariantType, type ExprType } from "@elaraai/east";

// ============================================================================
// Font Styling
// ============================================================================

/**
 * Font weight variant type for text styling.
 *
 * @remarks
 * This variant type provides type-safe font weight options compatible with
 * CSS and Chakra UI. Create instances using the {@link FontWeight} function.
 *
 * @property normal - Normal font weight (typically 400 in CSS)
 * @property bold - Bold font weight (typically 700 in CSS)
 * @property semibold - Semi-bold font weight (typically 600 in CSS)
 * @property medium - Medium font weight (typically 500 in CSS)
 * @property light - Light font weight (typically 300 in CSS)
 */
export const FontWeightType = VariantType({
    normal: NullType,
    bold: NullType,
    semibold: NullType,
    medium: NullType,
    light: NullType,
});

/**
 * Type representing font weight variant values.
 *
 * @remarks
 * Create instances using {@link FontWeight} function.
 */
export type FontWeightType = typeof FontWeightType;

/**
 * String literal type for font weight values.
 */
export type FontWeightLiteral = "normal" | "bold" | "semibold" | "medium" | "light";

/**
 * Creates a font weight variant expression.
 *
 * @param weight - The font weight value
 * @returns An East expression representing the font weight
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * // Static weight
 * const boldWeight = Style.FontWeight("bold");
 *
 * // Conditional weight
 * const weight = isImportant.ifElse(
 *   Style.FontWeight("bold"),
 *   Style.FontWeight("normal")
 * );
 * ```
 */
export function FontWeight(weight: "normal" | "bold" | "semibold" | "medium" | "light"): ExprType<FontWeightType> {
    return East.value(variant(weight, null), FontWeightType);
}



/**
 * Font style variant type for text styling.
 *
 * @remarks
 * Create instances using the {@link FontStyle} function.
 *
 * @property normal - Normal (upright) text style
 * @property italic - Italic (slanted) text style
 */
export const FontStyleType = VariantType({
    normal: NullType,
    italic: NullType,
});

/**
 * Type representing font style variant values.
 */
export type FontStyleType = typeof FontStyleType;

/**
 * String literal type for font style values.
 */
export type FontStyleLiteral = "normal" | "italic";

/**
 * Creates a font style variant expression.
 *
 * @param style - The font style value
 * @returns An East expression representing the font style
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.FontStyle("italic");
 * ```
 */
export function FontStyle(style: "normal" | "italic"): ExprType<FontStyleType> {
    return East.value(variant(style, null), FontStyleType);
}

// ============================================================================
// Text Alignment
// ============================================================================

/**
 * Text alignment variant type for horizontal alignment.
 *
 * @remarks
 * Create instances using the {@link TextAlign} function.
 *
 * @property left - Align text to the left
 * @property center - Center text horizontally
 * @property right - Align text to the right
 * @property justify - Justify text to fill the full width
 */
export const TextAlignType = VariantType({
    left: NullType,
    center: NullType,
    right: NullType,
    justify: NullType,
});

/**
 * Type representing text alignment variant values.
 */
export type TextAlignType = typeof TextAlignType;

/**
 * String literal type for text alignment values.
 */
export type TextAlignLiteral = "left" | "center" | "right" | "justify";

/**
 * Creates a text alignment variant expression.
 *
 * @param align - The horizontal alignment value
 * @returns An East expression representing the text alignment
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.TextAlign("center");
 * ```
 */
export function TextAlign(align: "left" | "center" | "right" | "justify"): ExprType<TextAlignType> {
    return East.value(variant(align, null), TextAlignType);
}

// ============================================================================
// Border Styling
// ============================================================================

/**
 * Border width variant type for controlling border thickness.
 *
 * @remarks
 * Create instances using the {@link BorderWidth} function.
 *
 * @property none - No border (0px)
 * @property thin - Thin border (1px)
 * @property medium - Medium border (2px)
 * @property thick - Thick border (4px)
 */
export const BorderWidthType = VariantType({
    none: NullType,
    thin: NullType,
    medium: NullType,
    thick: NullType,
});

/**
 * Type representing border width variant values.
 */
export type BorderWidthType = typeof BorderWidthType;

/**
 * String literal type for border width values.
 */
export type BorderWidthLiteral = "none" | "thin" | "medium" | "thick";

/**
 * Creates a border width variant expression.
 *
 * @param width - The border width value
 * @returns An East expression representing the border width
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.BorderWidth("thin");
 * ```
 */
export function BorderWidth(width: "none" | "thin" | "medium" | "thick"): ExprType<BorderWidthType> {
    return East.value(variant(width, null), BorderWidthType);
}

/**
 * Border style variant type for controlling border appearance.
 *
 * @remarks
 * Create instances using the {@link BorderStyle} function.
 *
 * @property solid - Solid continuous line
 * @property dashed - Dashed line
 * @property dotted - Dotted line
 * @property double - Double line
 * @property none - No border
 */
export const BorderStyleType = VariantType({
    solid: NullType,
    dashed: NullType,
    dotted: NullType,
    double: NullType,
    none: NullType,
});

/**
 * Type representing border style variant values.
 */
export type BorderStyleType = typeof BorderStyleType;

/**
 * String literal type for border style values.
 */
export type BorderStyleLiteral = "solid" | "dashed" | "dotted" | "double" | "none";

/**
 * Creates a border style variant expression.
 *
 * @param style - The border style value
 * @returns An East expression representing the border style
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.BorderStyle("solid");
 * ```
 */
export function BorderStyle(style: "solid" | "dashed" | "dotted" | "double" | "none"): ExprType<BorderStyleType> {
    return East.value(variant(style, null), BorderStyleType);
}

// ============================================================================
// Table-Specific Variants
// ============================================================================

/**
 * Table variant type for Chakra UI table styling.
 *
 * @remarks
 * Create instances using the {@link TableVariant} function.
 *
 * @property simple - Simple table with basic borders
 * @property striped - Striped rows for better readability
 * @property unstyled - No default styling
 */
export const TableVariantType = VariantType({
    simple: NullType,
    striped: NullType,
    unstyled: NullType,
});

/**
 * Type representing table variant values.
 */
export type TableVariantType = typeof TableVariantType;

/**
 * String literal type for table variant values.
 */
export type TableVariantLiteral = "simple" | "striped" | "unstyled";

/**
 * Creates a table variant expression for Chakra UI styling.
 *
 * @param variant_ - The table variant style
 * @returns An East expression representing the table variant
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.TableVariant("striped");
 * ```
 */
export function TableVariant(variant_: "simple" | "striped" | "unstyled"): ExprType<TableVariantType> {
    return East.value(variant(variant_, null), TableVariantType);
}

/**
 * Size variant type for controlling component sizing.
 *
 * @remarks
 * Create instances using the {@link Size} function.
 *
 * @property xs - Extra small size
 * @property sm - Small size with compact spacing
 * @property md - Medium size (default)
 * @property lg - Large size with generous spacing
 */
export const SizeType = VariantType({
    xs: NullType,
    sm: NullType,
    md: NullType,
    lg: NullType,
});

/**
 * Type representing size variant values.
 */
export type SizeType = typeof SizeType;

/**
 * String literal type for size values.
 */
export type SizeLiteral = "xs" | "sm" | "md" | "lg";

/**
 * Creates a size variant expression.
 *
 * @param size - The size value
 * @returns An East expression representing the size
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.Size("md");
 * ```
 */
export function Size(size: "xs" | "sm" | "md" | "lg"): ExprType<SizeType> {
    return East.value(variant(size, null), SizeType);
}

/**
 * Color scheme variant type for Chakra UI theming.
 *
 * @remarks
 * Create instances using the {@link ColorScheme} function.
 *
 * @property gray - Gray color scheme
 * @property red - Red color scheme
 * @property orange - Orange color scheme
 * @property yellow - Yellow color scheme
 * @property green - Green color scheme
 * @property teal - Teal color scheme
 * @property blue - Blue color scheme
 * @property cyan - Cyan color scheme
 * @property purple - Purple color scheme
 * @property pink - Pink color scheme
 */
export const ColorSchemeType = VariantType({
    gray: NullType,
    red: NullType,
    orange: NullType,
    yellow: NullType,
    green: NullType,
    teal: NullType,
    blue: NullType,
    cyan: NullType,
    purple: NullType,
    pink: NullType,
});

/**
 * Type representing color scheme variant values.
 */
export type ColorSchemeType = typeof ColorSchemeType;

/**
 * String literal type for color scheme values.
 */
export type ColorSchemeLiteral = "gray" | "red" | "orange" | "yellow" | "green" | "teal" | "blue" | "cyan" | "purple" | "pink";

/**
 * Creates a color scheme variant expression for Chakra UI theming.
 *
 * @param scheme - The color scheme name
 * @returns An East expression representing the color scheme
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.ColorScheme("blue");
 * ```
 */
export function ColorScheme(scheme: "gray" | "red" | "orange" | "yellow" | "green" | "teal" | "blue" | "cyan" | "purple" | "pink"): ExprType<ColorSchemeType> {
    return East.value(variant(scheme, null), ColorSchemeType);
}

/**
 * Text transform variant type for controlling text case transformation.
 *
 * @remarks
 * Create instances using the {@link TextTransform} function.
 *
 * @property uppercase - Transform text to UPPERCASE
 * @property lowercase - Transform text to lowercase
 * @property capitalize - Capitalize First Letter Of Each Word
 * @property none - No text transformation
 */
export const TextTransformType = VariantType({
    uppercase: NullType,
    lowercase: NullType,
    capitalize: NullType,
    none: NullType,
});

/**
 * Type representing text transform variant values.
 */
export type TextTransformType = typeof TextTransformType;

/**
 * String literal type for text transform values.
 */
export type TextTransformLiteral = "uppercase" | "lowercase" | "capitalize" | "none";

/**
 * Creates a text transform variant expression.
 *
 * @param transform - The text transformation mode
 * @returns An East expression representing the text transform
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.TextTransform("uppercase");
 * ```
 */
export function TextTransform(transform: "uppercase" | "lowercase" | "capitalize" | "none"): ExprType<TextTransformType> {
    return East.value(variant(transform, null), TextTransformType);
}

// ============================================================================
// Badge Variants
// ============================================================================

/**
 * Badge variant type for different badge styles.
 *
 * @remarks
 * Create instances using the {@link StyleVariant} function.
 *
 * @property subtle - Subtle background with colored text
 * @property solid - Solid colored background with contrast text
 * @property outline - Transparent background with colored border
 */
export const StyleVariantType = VariantType({
    subtle: NullType,
    solid: NullType,
    outline: NullType,
});

/**
 * Type representing badge variant values.
 */
export type StyleVariantType = typeof StyleVariantType;

/**
 * String literal type for style variant values (solid, subtle, outline).
 */
export type StyleVariantLiteral = "subtle" | "solid" | "outline";

/**
 * Creates a badge variant expression.
 *
 * @param variant_ - The badge variant style
 * @returns An East expression representing the badge variant
 *
 * @example
 * ```ts
 * import { variant } from "@elaraai/east-ui";
 *
 * const subtle = variant("subtle", null);
 * ```
 */
export function StyleVariant(variant_: "subtle" | "solid" | "outline"): ExprType<StyleVariantType> {
    return East.value(variant(variant_, null), StyleVariantType);
}


// ============================================================================
// Orientation
// ============================================================================

/**
 * Orientation variant type for layout direction.
 *
 * @remarks
 * Create instances using the {@link Orientation} function.
 *
 * @property horizontal - Horizontal layout (left to right)
 * @property vertical - Vertical layout (top to bottom)
 */
export const OrientationType = VariantType({
    horizontal: NullType,
    vertical: NullType,
});

/**
 * Type representing orientation variant values.
 */
export type OrientationType = typeof OrientationType;

/**
 * String literal type for orientation values.
 */
export type OrientationLiteral = "horizontal" | "vertical";

/**
 * Creates an orientation variant expression.
 *
 * @param orientation - The orientation value
 * @returns An East expression representing the orientation
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.Orientation("horizontal");
 * ```
 */
export function Orientation(orientation: "horizontal" | "vertical"): ExprType<OrientationType> {
    return East.value(variant(orientation, null), OrientationType);
}

// ============================================================================
// Flex Direction
// ============================================================================

/**
 * Flex direction variant type for flexbox layouts.
 *
 * @remarks
 * Create instances using the {@link FlexDirection} function.
 *
 * @property row - Row direction (horizontal, left to right)
 * @property column - Column direction (vertical, top to bottom)
 * @property row-reverse - Row direction reversed (horizontal, right to left)
 * @property column-reverse - Column direction reversed (vertical, bottom to top)
 */
export const FlexDirectionType = VariantType({
    row: NullType,
    column: NullType,
    "row-reverse": NullType,
    "column-reverse": NullType,
});

/**
 * Type representing flex direction variant values.
 */
export type FlexDirectionType = typeof FlexDirectionType;

/**
 * String literal type for flex direction values.
 */
export type FlexDirectionLiteral = "row" | "column" | "row-reverse" | "column-reverse";

/**
 * Creates a flex direction variant expression.
 *
 * @param direction - The flex direction value
 * @returns An East expression representing the flex direction
 */
export function FlexDirection(direction: "row" | "column" | "row-reverse" | "column-reverse"): ExprType<FlexDirectionType> {
    return East.value(variant(direction, null), FlexDirectionType);
}

// ============================================================================
// Justify Content
// ============================================================================

/**
 * Justify content variant type for flexbox/grid alignment.
 *
 * @remarks
 * Create instances using the {@link JustifyContent} function.
 *
 * @property flex-start - Align items to the start
 * @property flex-end - Align items to the end
 * @property center - Center items
 * @property space-between - Distribute items with space between
 * @property space-around - Distribute items with space around
 * @property space-evenly - Distribute items with equal space
 */
export const JustifyContentType = VariantType({
    "flex-start": NullType,
    "flex-end": NullType,
    center: NullType,
    "space-between": NullType,
    "space-around": NullType,
    "space-evenly": NullType,
});

/**
 * Type representing justify content variant values.
 */
export type JustifyContentType = typeof JustifyContentType;

/**
 * String literal type for justify content values.
 */
export type JustifyContentLiteral = "flex-start" | "flex-end" | "center" | "space-between" | "space-around" | "space-evenly";

/**
 * Creates a justify content variant expression.
 *
 * @param justify - The justify content value
 * @returns An East expression representing the justify content
 */
export function JustifyContent(justify: "flex-start" | "flex-end" | "center" | "space-between" | "space-around" | "space-evenly"): ExprType<JustifyContentType> {
    return East.value(variant(justify, null), JustifyContentType);
}

// ============================================================================
// Align Items
// ============================================================================

/**
 * Align items variant type for flexbox/grid cross-axis alignment.
 *
 * @remarks
 * Create instances using the {@link AlignItems} function.
 *
 * @property flex-start - Align items to the start of the cross axis
 * @property flex-end - Align items to the end of the cross axis
 * @property center - Center items on the cross axis
 * @property baseline - Align items to text baseline
 * @property stretch - Stretch items to fill the container
 */
export const AlignItemsType = VariantType({
    "flex-start": NullType,
    "flex-end": NullType,
    center: NullType,
    baseline: NullType,
    stretch: NullType,
});

/**
 * Type representing align items variant values.
 */
export type AlignItemsType = typeof AlignItemsType;

/**
 * String literal type for align items values.
 */
export type AlignItemsLiteral = "flex-start" | "flex-end" | "center" | "baseline" | "stretch";

/**
 * Creates an align items variant expression.
 *
 * @param align - The align items value
 * @returns An East expression representing the align items
 */
export function AlignItems(align: "flex-start" | "flex-end" | "center" | "baseline" | "stretch"): ExprType<AlignItemsType> {
    return East.value(variant(align, null), AlignItemsType);
}

// ============================================================================
// Flex Wrap
// ============================================================================

/**
 * Flex wrap variant type for controlling flex item wrapping.
 *
 * @remarks
 * Create instances using the {@link FlexWrap} function.
 *
 * @property nowrap - Items don't wrap
 * @property wrap - Items wrap to next line
 * @property wrap-reverse - Items wrap in reverse order
 */
export const FlexWrapType = VariantType({
    nowrap: NullType,
    wrap: NullType,
    "wrap-reverse": NullType,
});

/**
 * Type representing flex wrap variant values.
 */
export type FlexWrapType = typeof FlexWrapType;

/**
 * String literal type for flex wrap values.
 */
export type FlexWrapLiteral = "nowrap" | "wrap" | "wrap-reverse";

/**
 * Creates a flex wrap variant expression.
 *
 * @param wrap - The flex wrap value
 * @returns An East expression representing the flex wrap
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.FlexWrap("wrap");
 * ```
 */
export function FlexWrap(wrap: "nowrap" | "wrap" | "wrap-reverse"): ExprType<FlexWrapType> {
    return East.value(variant(wrap, null), FlexWrapType);
}

// ============================================================================
// Display
// ============================================================================

/**
 * Display variant type for CSS display property.
 *
 * @remarks
 * Create instances using the {@link Display} function.
 *
 * @property block - Block-level element
 * @property inline - Inline element
 * @property inline-block - Inline-block element
 * @property flex - Flex container
 * @property inline-flex - Inline flex container
 * @property grid - Grid container
 * @property inline-grid - Inline grid container
 * @property none - Hidden element
 */
export const DisplayType = VariantType({
    block: NullType,
    inline: NullType,
    "inline-block": NullType,
    flex: NullType,
    "inline-flex": NullType,
    grid: NullType,
    "inline-grid": NullType,
    none: NullType,
});

/**
 * Type representing display variant values.
 */
export type DisplayType = typeof DisplayType;

/**
 * String literal type for display values.
 */
export type DisplayLiteral = "block" | "inline" | "inline-block" | "flex" | "inline-flex" | "grid" | "inline-grid" | "none";

/**
 * Creates a display variant expression.
 *
 * @param display - The display value
 * @returns An East expression representing the display
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.Display("flex");
 * ```
 */
export function Display(display: "block" | "inline" | "inline-block" | "flex" | "inline-flex" | "grid" | "inline-grid" | "none"): ExprType<DisplayType> {
    return East.value(variant(display, null), DisplayType);
}

// ============================================================================
// Vertical Align
// ============================================================================

/**
 * Vertical align variant type for text vertical alignment.
 *
 * @remarks
 * Create instances using the {@link VerticalAlign} function.
 *
 * @property top - Align to the top
 * @property middle - Align to the middle
 * @property bottom - Align to the bottom
 * @property baseline - Align to text baseline
 */
export const VerticalAlignType = VariantType({
    top: NullType,
    middle: NullType,
    bottom: NullType,
    baseline: NullType,
});

/**
 * Type representing vertical align variant values.
 */
export type VerticalAlignType = typeof VerticalAlignType;

/**
 * String literal type for vertical align values.
 */
export type VerticalAlignLiteral = "top" | "middle" | "bottom" | "baseline";

/**
 * Creates a vertical align variant expression.
 *
 * @param align - The vertical alignment value
 * @returns An East expression representing the vertical alignment
 */
export function VerticalAlign(align: "top" | "middle" | "bottom" | "baseline"): ExprType<VerticalAlignType> {
    return East.value(variant(align, null), VerticalAlignType);
}

// ============================================================================
// Text Overflow
// ============================================================================

/**
 * Text overflow variant type for controlling text overflow behavior.
 *
 * @remarks
 * Create instances using the {@link TextOverflow} function.
 *
 * @property clip - Clip overflowing text
 * @property ellipsis - Show ellipsis (...) for overflowing text
 */
export const TextOverflowType = VariantType({
    clip: NullType,
    ellipsis: NullType,
});

/**
 * Type representing text overflow variant values.
 */
export type TextOverflowType = typeof TextOverflowType;

/**
 * String literal type for text overflow values.
 */
export type TextOverflowLiteral = "clip" | "ellipsis";

/**
 * Creates a text overflow variant expression.
 *
 * @param overflow - The text overflow value
 * @returns An East expression representing the text overflow
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.TextOverflow("ellipsis");
 * ```
 */
export function TextOverflow(overflow: "clip" | "ellipsis"): ExprType<TextOverflowType> {
    return East.value(variant(overflow, null), TextOverflowType);
}

// ============================================================================
// White Space
// ============================================================================

/**
 * White space variant type for controlling whitespace handling.
 *
 * @remarks
 * Create instances using the {@link WhiteSpace} function.
 *
 * @property normal - Normal whitespace handling (wraps text)
 * @property nowrap - Prevent text wrapping
 * @property pre - Preserve whitespace and newlines
 * @property pre-wrap - Preserve whitespace but allow wrapping
 * @property pre-line - Collapse whitespace but preserve newlines
 */
export const WhiteSpaceType = VariantType({
    normal: NullType,
    nowrap: NullType,
    pre: NullType,
    "pre-wrap": NullType,
    "pre-line": NullType,
});

/**
 * Type representing white space variant values.
 */
export type WhiteSpaceType = typeof WhiteSpaceType;

/**
 * String literal type for white space values.
 */
export type WhiteSpaceLiteral = "normal" | "nowrap" | "pre" | "pre-wrap" | "pre-line";

/**
 * Creates a white space variant expression.
 *
 * @param whiteSpace - The white space value
 * @returns An East expression representing the white space handling
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.WhiteSpace("nowrap");
 * ```
 */
export function WhiteSpace(whiteSpace: "normal" | "nowrap" | "pre" | "pre-wrap" | "pre-line"): ExprType<WhiteSpaceType> {
    return East.value(variant(whiteSpace, null), WhiteSpaceType);
}

// ============================================================================
// Overflow
// ============================================================================

/**
 * Overflow variant type for controlling element overflow behavior.
 *
 * @remarks
 * Create instances using the {@link Overflow} function.
 *
 * @property visible - Content is not clipped
 * @property hidden - Content is clipped with no scrollbars
 * @property scroll - Content is clipped with scrollbars always visible
 * @property auto - Content is clipped with scrollbars as needed
 */
export const OverflowType = VariantType({
    visible: NullType,
    hidden: NullType,
    scroll: NullType,
    auto: NullType,
});

/**
 * Type representing overflow variant values.
 */
export type OverflowType = typeof OverflowType;

/**
 * String literal type for overflow values.
 */
export type OverflowLiteral = "visible" | "hidden" | "scroll" | "auto";

/**
 * Creates an overflow variant expression.
 *
 * @param overflow - The overflow value
 * @returns An East expression representing the overflow behavior
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * Style.Overflow("hidden");
 * ```
 */
export function Overflow(overflow: "visible" | "hidden" | "scroll" | "auto"): ExprType<OverflowType> {
    return East.value(variant(overflow, null), OverflowType);
}

// ============================================================================
// Style Namespace Export
// ============================================================================

/**
 * Style namespace providing convenient access to all styling functions.
 *
 * @remarks
 * This namespace groups all style variant creation functions for easy access.
 * Each function creates a typed variant expression for use in component styling.
 *
 * @example
 * ```ts
 * import { Style } from "@elaraai/east-ui";
 *
 * // Font styling
 * Style.FontWeight("bold");
 * Style.FontStyle("italic");
 * Style.TextTransform("uppercase");
 *
 * // Alignment
 * Style.TextAlign("center");
 *
 * // Borders
 * Style.BorderWidth("thin");
 * Style.BorderStyle("solid");
 *
 * // Table variants
 * Style.TableVariant("striped");
 * Style.Size("md");
 * Style.ColorScheme("blue");
 * ```
 */
export const Style = {
    FontWeight,
    FontStyle,
    TextAlign,
    BorderWidth,
    BorderStyle,
    Size,
    ColorScheme,
    TextTransform,
    StyleVariant,
    Orientation,
    FlexDirection,
    JustifyContent,
    AlignItems,
    VerticalAlign,
    FlexWrap,
    Display,
    TextOverflow,
    WhiteSpace,
    Overflow,
    Types: {
        FontWeight: FontWeightType,
        FontStyle: FontStyleType,
        TextAlign: TextAlignType,
        BorderWidth: BorderWidthType,
        BorderStyle: BorderStyleType,
        Size: SizeType,
        ColorScheme: ColorSchemeType,
        TextTransform: TextTransformType,
        StyleVariant: StyleVariantType,
        Orientation: OrientationType,
        FlexDirection: FlexDirectionType,
        JustifyContent: JustifyContentType,
        AlignItems: AlignItemsType,
        VerticalAlign: VerticalAlignType,
        FlexWrap: FlexWrapType,
        Display: DisplayType,
        TextOverflow: TextOverflowType,
        WhiteSpace: WhiteSpaceType,
        Overflow: OverflowType,
    },
} as const;
