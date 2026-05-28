# East UI Developer Guide

Usage guide for East UI component definitions.

---

## Table of Contents

- [Quick Start](#quick-start)
- [UIComponentType](#uicomponenttype)
- [Style Types](#style-types)
- [Layout](#layout)
- [Typography](#typography)
- [Buttons](#buttons)
- [Forms](#forms)
- [Collections](#collections)
- [Charts](#charts)
- [Display](#display)
- [Feedback](#feedback)
- [Disclosure](#disclosure)
- [Overlays](#overlays)
- [Container](#container)
- [State Management](#state-management)
- [Reactive Components](#reactive-components)

---

## Quick Start

East UI is a typed UI component library for East. Components return data structures describing UI layouts rather than rendering directly.

```typescript
import { East } from "@elaraai/east";
import { Stack, Text, Button, UIComponentType } from "@elaraai/east-ui";

const MyComponent = East.function([], UIComponentType, $ => {
    return Stack.VStack([
        Text.Root("Hello, World!", { fontSize: "lg", fontWeight: "bold" }),
        Button.Root("Click Me", { variant: "solid", colorPalette: "blue" }),
    ], { gap: "4" });
});

const ir = MyComponent.toIR();
```

---

## UIComponentType

`UIComponentType` is the recursive variant type representing any UI component in East UI. It is exported from `@elaraai/east-ui` and used as the return type for East functions that produce UI.

```typescript
import { East } from "@elaraai/east";
import { UIComponentType, Text, Stack } from "@elaraai/east-ui";

// Use as return type for East functions
const MyUI = East.function([], UIComponentType, $ => {
    return Text.Root("Hello");
});

// Container components accept arrays of UIComponentType
Stack.Root([
    Text.Root("Child 1"),
    Button.Root("Child 2"),
], { gap: "4" });
```

The recursive structure allows container components (Box, Stack, Card, Grid, etc.) to have children that are also `UIComponentType`.

---

## Style Types

Common style variant types exported from `@elaraai/east-ui`. Style properties accept string literals (e.g., `"bold"`), Style helpers (e.g., `Style.FontWeight("bold")`), East variants (e.g., `variant("bold", null)`), or East expressions for dynamic styling.

| Type | Values |
|------|--------|
| `FontWeightType` | `normal`, `medium`, `semibold`, `bold`, `light` |
| `FontStyleType` | `normal`, `italic` |
| `TextAlignType` | `left`, `center`, `right`, `justify` |
| `SizeType` | `xs`, `sm`, `md`, `lg` |
| `ColorSchemeType` | `gray`, `red`, `orange`, `yellow`, `green`, `teal`, `blue`, `cyan`, `purple`, `pink` |
| `FlexDirectionType` | `row`, `column`, `row-reverse`, `column-reverse` |
| `JustifyContentType` | `flex-start`, `flex-end`, `center`, `space-between`, `space-around`, `space-evenly` |
| `AlignItemsType` | `flex-start`, `flex-end`, `center`, `baseline`, `stretch` |
| `FlexWrapType` | `nowrap`, `wrap`, `wrap-reverse` |
| `DisplayType` | `block`, `inline`, `inline-block`, `flex`, `inline-flex`, `grid`, `inline-grid`, `none` |
| `OrientationType` | `horizontal`, `vertical` |
| `TableVariantType` | `simple`, `line`, `outline` |
| `TextOverflowType` | `clip`, `ellipsis` |
| `WhiteSpaceType` | `normal`, `nowrap`, `pre`, `pre-wrap`, `pre-line` |
| `OverflowType` | `visible`, `hidden`, `scroll`, `auto` |
| `BorderWidthType` | `none`, `thin`, `medium`, `thick` |
| `BorderStyleType` | `solid`, `dashed`, `dotted`, `double`, `none` |
| `TextTransformType` | `uppercase`, `lowercase`, `capitalize`, `none` |

---

## Layout

### Box

Generic container with flexible styling. Maps to a div element.

```typescript
import { East } from "@elaraai/east";
import { Box, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Box.Root([Text.Root("Content")], { padding: "4", background: "gray.100" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Box.Root(children: SubtypeExprOrValue<ArrayType<UIComponentType>>, style?: BoxStyle): ExprType<UIComponentType>` | Create box container with children | `Box.Root([Text.Root("Hi")], { padding: "4" })` |
| `Box.Padding(config: PaddingConfig): ExprType<PaddingType>` | Create padding configuration | `Box.Padding({ top: "2", bottom: "4" })` |
| `Box.Margin(config: MarginConfig): ExprType<MarginType>` | Create margin configuration | `Box.Margin({ left: "4", right: "4" })` |
| `Box.Types.Box` | East StructType for Box component | `Box.Types.Box` |
| `Box.Types.Style` | East StructType for Box style | `Box.Types.Style` |
| `Box.Types.Padding` | East StructType for padding | `Box.Types.Padding` |
| `Box.Types.Margin` | East StructType for margin | `Box.Types.Margin` |

**BoxStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `display` | `SubtypeExprOrValue<DisplayType> \| DisplayLiteral` | CSS display property |
| `width` | `SubtypeExprOrValue<StringType>` | Width (Chakra token or CSS) |
| `height` | `SubtypeExprOrValue<StringType>` | Height (Chakra token or CSS) |
| `padding` | `SubtypeExprOrValue<PaddingType> \| string` | Padding (use `Box.Padding()` or string) |
| `margin` | `SubtypeExprOrValue<MarginType> \| string` | Margin (use `Box.Margin()` or string) |
| `background` | `SubtypeExprOrValue<StringType>` | Background color |
| `color` | `SubtypeExprOrValue<StringType>` | Text color |
| `borderRadius` | `SubtypeExprOrValue<StringType>` | Border radius |
| `flexDirection` | `SubtypeExprOrValue<FlexDirectionType> \| FlexDirectionLiteral` | Flex direction |
| `justifyContent` | `SubtypeExprOrValue<JustifyContentType> \| JustifyContentLiteral` | Justify content |
| `alignItems` | `SubtypeExprOrValue<AlignItemsType> \| AlignItemsLiteral` | Align items |
| `gap` | `SubtypeExprOrValue<StringType>` | Gap between children |

---

### Stack

Flexbox-based stack layout.

```typescript
import { East } from "@elaraai/east";
import { Stack, Text, Button, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Stack.VStack([
        Text.Root("Item 1"),
        Text.Root("Item 2"),
        Stack.HStack([Button.Root("Left"), Button.Root("Right")], { gap: "2" }),
    ], { gap: "4" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Stack.Root(children: SubtypeExprOrValue<ArrayType<UIComponentType>>, style?: StackStyle): ExprType<UIComponentType>` | Create stack container | `Stack.Root([...], { gap: "4" })` |
| `Stack.HStack(children: SubtypeExprOrValue<ArrayType<UIComponentType>>, style?: Omit<StackStyle, "direction">): ExprType<UIComponentType>` | Horizontal stack (direction: row) | `Stack.HStack([...], { gap: "2" })` |
| `Stack.VStack(children: SubtypeExprOrValue<ArrayType<UIComponentType>>, style?: Omit<StackStyle, "direction">): ExprType<UIComponentType>` | Vertical stack (direction: column) | `Stack.VStack([...], { gap: "4" })` |
| `Stack.Padding(config: PaddingConfig): ExprType<PaddingType>` | Create padding configuration | `Stack.Padding({ x: "4" })` |
| `Stack.Margin(config: MarginConfig): ExprType<MarginType>` | Create margin configuration | `Stack.Margin({ y: "2" })` |
| `Stack.Types.Stack` | East StructType for Stack component | `Stack.Types.Stack` |
| `Stack.Types.Style` | East StructType for Stack style | `Stack.Types.Style` |

**StackStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `direction` | `SubtypeExprOrValue<FlexDirectionType> \| FlexDirectionLiteral` | Stack direction |
| `gap` | `SubtypeExprOrValue<StringType>` | Gap between items |
| `align` | `SubtypeExprOrValue<AlignItemsType> \| AlignItemsLiteral` | Cross-axis alignment |
| `justify` | `SubtypeExprOrValue<JustifyContentType> \| JustifyContentLiteral` | Main-axis alignment |
| `wrap` | `SubtypeExprOrValue<FlexWrapType> \| FlexWrapLiteral` | Flex wrap behavior |
| `padding` | `SubtypeExprOrValue<PaddingType> \| string` | Padding |
| `margin` | `SubtypeExprOrValue<MarginType> \| string` | Margin |
| `background` | `SubtypeExprOrValue<StringType>` | Background color |
| `width` | `SubtypeExprOrValue<StringType>` | Width |
| `height` | `SubtypeExprOrValue<StringType>` | Height |

---

### Grid

CSS Grid layout component.

```typescript
import { East } from "@elaraai/east";
import { Grid, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Grid.Root([
        Grid.Item(Text.Root("Cell 1"), { colSpan: "2" }),
        Grid.Item(Text.Root("Cell 2")),
        Grid.Item(Text.Root("Cell 3")),
    ], { templateColumns: "repeat(3, 1fr)", gap: "4" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Grid.Root(items: SubtypeExprOrValue<ArrayType<GridItemType>>, style?: GridStyle): ExprType<UIComponentType>` | Create grid container | `Grid.Root([Grid.Item(...)], { gap: "4" })` |
| `Grid.Item(content: ExprType<UIComponentType>, style?: GridItemStyle): ExprType<GridItemType>` | Create grid item wrapping a component | `Grid.Item(Text.Root("Cell"), { colSpan: "2" })` |
| `Grid.Types.Grid` | East StructType for Grid component | `Grid.Types.Grid` |
| `Grid.Types.Item` | East StructType for Grid item | `Grid.Types.Item` |
| `Grid.Types.Style` | East StructType for Grid style | `Grid.Types.Style` |

**GridStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `templateColumns` | `SubtypeExprOrValue<StringType>` | Grid template columns (e.g., "repeat(3, 1fr)") |
| `templateRows` | `SubtypeExprOrValue<StringType>` | Grid template rows |
| `gap` | `SubtypeExprOrValue<StringType>` | Gap between cells |
| `columnGap` | `SubtypeExprOrValue<StringType>` | Column gap |
| `rowGap` | `SubtypeExprOrValue<StringType>` | Row gap |
| `alignItems` | `SubtypeExprOrValue<AlignItemsType> \| AlignItemsLiteral` | Align items |
| `justifyItems` | `SubtypeExprOrValue<JustifyContentType> \| JustifyContentLiteral` | Justify items |

**GridItemStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `colSpan` | `SubtypeExprOrValue<StringType>` | Columns to span |
| `rowSpan` | `SubtypeExprOrValue<StringType>` | Rows to span |
| `colStart` | `SubtypeExprOrValue<StringType>` | Starting column |
| `colEnd` | `SubtypeExprOrValue<StringType>` | Ending column |
| `rowStart` | `SubtypeExprOrValue<StringType>` | Starting row |
| `rowEnd` | `SubtypeExprOrValue<StringType>` | Ending row |

---

### Splitter

Resizable split pane layout.

```typescript
import { East } from "@elaraai/east";
import { Splitter, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Splitter.Root([
        Splitter.Panel("left", Text.Root("Left"), { minSize: 20 }),
        Splitter.Panel("right", Text.Root("Right")),
    ], [50, 50], { orientation: "horizontal" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Splitter.Root(panels: SplitterPanel[], defaultSize: number[], style?: SplitterStyle): ExprType<UIComponentType>` | Create splitter container | `Splitter.Root([...], [50, 50])` |
| `Splitter.Panel(id: string, content: ExprType<UIComponentType>, style?: PanelStyle): SplitterPanel` | Create splitter panel | `Splitter.Panel("left", Text.Root("Left"))` |

---

### Separator

Visual divider between content.

```typescript
import { East } from "@elaraai/east";
import { Separator, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Separator.Root({ orientation: "horizontal", variant: "solid" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Separator.Root(style?: SeparatorStyle): ExprType<UIComponentType>` | Create separator | `Separator.Root({ variant: "dashed" })` |

**SeparatorStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `orientation` | `SubtypeExprOrValue<OrientationType> \| OrientationLiteral` | "horizontal" or "vertical" |
| `variant` | `SubtypeExprOrValue<SeparatorVariantType> \| SeparatorVariantLiteral` | "solid" or "dashed" |

---

## Typography

### Text

Text display with comprehensive styling.

```typescript
import { East } from "@elaraai/east";
import { Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Text.Root("Hello", { fontSize: "lg", fontWeight: "bold", color: "blue.600" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Text.Root(value: SubtypeExprOrValue<StringType>, style?: TextStyle): ExprType<UIComponentType>` | Create text component | `Text.Root("Hello", { fontWeight: "bold" })` |
| `Text.Types.Text` | East StructType for Text component | `Text.Types.Text` |

**TextStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `color` | `SubtypeExprOrValue<StringType>` | Text color |
| `background` | `SubtypeExprOrValue<StringType>` | Background color |
| `fontWeight` | `SubtypeExprOrValue<FontWeightType> \| FontWeightLiteral` | Font weight |
| `fontStyle` | `SubtypeExprOrValue<FontStyleType> \| FontStyleLiteral` | Font style |
| `fontSize` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Font size |
| `textAlign` | `SubtypeExprOrValue<TextAlignType> \| TextAlignLiteral` | Text alignment |
| `textTransform` | `SubtypeExprOrValue<TextTransformType> \| TextTransformLiteral` | Text transform |
| `textOverflow` | `SubtypeExprOrValue<TextOverflowType> \| TextOverflowLiteral` | Text overflow |
| `whiteSpace` | `SubtypeExprOrValue<WhiteSpaceType> \| WhiteSpaceLiteral` | White space handling |
| `overflow` | `SubtypeExprOrValue<OverflowType> \| OverflowLiteral` | Overflow behavior |
| `borderWidth` | `SubtypeExprOrValue<BorderWidthType> \| BorderWidthLiteral` | Border width |
| `borderStyle` | `SubtypeExprOrValue<BorderStyleType> \| BorderStyleLiteral` | Border style |
| `borderColor` | `SubtypeExprOrValue<StringType>` | Border color |

---

### Code

Inline code snippet display.

```typescript
import { East } from "@elaraai/east";
import { Code, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Code.Root("const x = 1", { variant: "surface", colorPalette: "blue" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Code.Root(value: SubtypeExprOrValue<StringType>, style?: CodeStyle): ExprType<UIComponentType>` | Create inline code | `Code.Root("console.log()", { variant: "subtle" })` |
| `Code.Types.Code` | East StructType for Code component | `Code.Types.Code` |
| `Code.Types.Variant` | East VariantType for code variant | `Code.Types.Variant` |

**CodeStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `variant` | `SubtypeExprOrValue<CodeVariantType> \| CodeVariantLiteral` | "subtle", "surface", "outline" |
| `colorPalette` | `SubtypeExprOrValue<StringType>` | Color palette (e.g., "gray", "blue") |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Code text size |

---

### Heading

Semantic heading component with extended size options.

```typescript
import { East } from "@elaraai/east";
import { Heading, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Heading.Root("Documentation", { size: "4xl", as: "h1" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Heading.Root(value: SubtypeExprOrValue<StringType>, style?: HeadingStyle): ExprType<UIComponentType>` | Create heading | `Heading.Root("Title", { size: "3xl", as: "h1" })` |
| `Heading.Types.Heading` | East StructType for Heading component | `Heading.Types.Heading` |
| `Heading.Types.Size` | East VariantType for heading size | `Heading.Types.Size` |
| `Heading.Types.As` | East VariantType for semantic level | `Heading.Types.As` |

**HeadingStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `size` | `SubtypeExprOrValue<HeadingSizeType> \| HeadingSizeLiteral` | "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl" |
| `as` | `SubtypeExprOrValue<HeadingAsType> \| HeadingAsLiteral` | Semantic level: "h1", "h2", "h3", "h4", "h5", "h6" |
| `color` | `SubtypeExprOrValue<StringType>` | Text color |
| `textAlign` | `SubtypeExprOrValue<TextAlignType> \| TextAlignLiteral` | Text alignment |

---

### Link

Hyperlink component for navigation.

```typescript
import { East } from "@elaraai/east";
import { Link, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Link.Root("Documentation", "https://docs.example.com", { external: true });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Link.Root(value: SubtypeExprOrValue<StringType>, href: SubtypeExprOrValue<StringType>, style?: LinkStyle): ExprType<UIComponentType>` | Create link | `Link.Root("Click", "/page", { external: true })` |
| `Link.Types.Link` | East StructType for Link component | `Link.Types.Link` |
| `Link.Types.Variant` | East VariantType for link variant | `Link.Types.Variant` |

**LinkStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `external` | `SubtypeExprOrValue<BooleanType> \| boolean` | Open in new tab |
| `variant` | `SubtypeExprOrValue<LinkVariantType> \| LinkVariantLiteral` | "underline", "plain" |
| `colorPalette` | `SubtypeExprOrValue<StringType>` | Color palette (e.g., "blue", "teal") |

---

### Highlight

Text with highlighted search terms.

```typescript
import { East } from "@elaraai/east";
import { Highlight, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Highlight.Root("React is a JavaScript library", ["React", "JavaScript"]);
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Highlight.Root(value: SubtypeExprOrValue<StringType>, query: SubtypeExprOrValue<ArrayType<StringType>>, style?: HighlightStyle): ExprType<UIComponentType>` | Create highlight | `Highlight.Root("text", ["term"])` |
| `Highlight.Types.Highlight` | East StructType for Highlight component | `Highlight.Types.Highlight` |

**HighlightStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `color` | `SubtypeExprOrValue<StringType>` | Background color for highlighted portions |

---

### Mark

Inline text mark/highlight.

```typescript
import { East } from "@elaraai/east";
import { Mark, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Mark.Root("Important", { variant: "solid", colorPalette: "green" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Mark.Root(value: SubtypeExprOrValue<StringType>, style?: MarkStyle): ExprType<UIComponentType>` | Create mark | `Mark.Root("text", { variant: "solid" })` |
| `Mark.Types.Mark` | East StructType for Mark component | `Mark.Types.Mark` |
| `Mark.Types.Variant` | East VariantType for mark variant | `Mark.Types.Variant` |

**MarkStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `variant` | `SubtypeExprOrValue<MarkVariantType> \| MarkVariantLiteral` | "subtle", "solid", "text", "plain" |
| `colorPalette` | `SubtypeExprOrValue<StringType>` | Color palette (e.g., "yellow", "green") |

---

### List

Ordered and unordered lists.

```typescript
import { East } from "@elaraai/east";
import { List, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return List.Root(["Step 1", "Step 2", "Step 3"], { variant: "ordered", gap: "2" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `List.Root(items: SubtypeExprOrValue<ArrayType<StringType>>, style?: ListStyle): ExprType<UIComponentType>` | Create list | `List.Root(["A", "B"], { variant: "ordered" })` |
| `List.Types.List` | East StructType for List component | `List.Types.List` |
| `List.Types.Variant` | East VariantType for list variant | `List.Types.Variant` |

**ListStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `variant` | `SubtypeExprOrValue<ListVariantType> \| ListVariantLiteral` | "ordered", "unordered" |
| `gap` | `SubtypeExprOrValue<StringType>` | Spacing between items |
| `colorPalette` | `SubtypeExprOrValue<StringType>` | Color for list markers |

---

### CodeBlock

Multi-line code block with syntax highlighting.

```typescript
import { East } from "@elaraai/east";
import { CodeBlock, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return CodeBlock.Root(`function hello() {\n  console.log("Hello!");\n}`, {
        language: "typescript",
        showLineNumbers: true,
        title: "example.ts",
        showCopyButton: true,
    });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `CodeBlock.Root(code: SubtypeExprOrValue<StringType>, style?: CodeBlockStyle): ExprType<UIComponentType>` | Create code block | `CodeBlock.Root("code", { language: "typescript" })` |
| `CodeBlock.Types.CodeBlock` | East StructType for CodeBlock component | `CodeBlock.Types.CodeBlock` |
| `CodeBlock.Types.Language` | East VariantType for language | `CodeBlock.Types.Language` |

**CodeBlockStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `language` | `SubtypeExprOrValue<CodeLanguageType> \| CodeLanguage` | Syntax highlighting: "typescript", "javascript", "json", "html", "css", "python", "rust", "go", "sql", "bash", "markdown", "yaml", "xml", "plaintext" |
| `showLineNumbers` | `SubtypeExprOrValue<BooleanType> \| boolean` | Display line numbers |
| `highlightLines` | `SubtypeExprOrValue<ArrayType<IntegerType>>` | Array of line numbers to highlight (bigint[]) |
| `maxHeight` | `SubtypeExprOrValue<StringType>` | Maximum height with scroll (e.g., "400px") |
| `showCopyButton` | `SubtypeExprOrValue<BooleanType> \| boolean` | Show copy-to-clipboard button in header |
| `title` | `SubtypeExprOrValue<StringType>` | Title displayed in header (e.g., filename) |

---

## Buttons

### Button

Interactive button component.

```typescript
import { East } from "@elaraai/east";
import { Button, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Button.Root("Submit", { variant: "solid", colorPalette: "blue" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Button.Root(label: SubtypeExprOrValue<StringType>, style?: ButtonStyle): ExprType<UIComponentType>` | Create button | `Button.Root("Click", { variant: "solid" })` |
| `Button.Types.Button` | East StructType for Button component | `Button.Types.Button` |
| `Button.Types.Style` | East StructType for Button style | `Button.Types.Style` |
| `Button.Types.Variant` | East VariantType for button variant | `Button.Types.Variant` |

**ButtonStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `variant` | `SubtypeExprOrValue<ButtonVariantType> \| ButtonVariantLiteral` | "solid", "subtle", "outline", "ghost", "plain" |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Button size |
| `disabled` | `SubtypeExprOrValue<BooleanType>` | Disabled state |
| `loading` | `SubtypeExprOrValue<BooleanType>` | Loading state |

---

### IconButton

Button with icon instead of text.

```typescript
import { East } from "@elaraai/east";
import { IconButton, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return IconButton.Root("search", { ariaLabel: "Search", variant: "ghost" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `IconButton.Root(icon: SubtypeExprOrValue<StringType>, style?: IconButtonStyle): ExprType<UIComponentType>` | Create icon button | `IconButton.Root("menu", { ariaLabel: "Menu" })` |

---

## Forms

### Input

Text input with multiple types.

```typescript
import { East } from "@elaraai/east";
import { Input, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Input.String("", { placeholder: "Enter text" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Input.String(value: SubtypeExprOrValue<StringType>, style?: InputStyle): ExprType<UIComponentType>` | String input | `Input.String("", { placeholder: "Name" })` |
| `Input.Integer(value: SubtypeExprOrValue<IntegerType>, style?: InputStyle): ExprType<UIComponentType>` | Integer input | `Input.Integer(0n, { placeholder: "Age" })` |
| `Input.Float(value: SubtypeExprOrValue<FloatType>, style?: InputStyle): ExprType<UIComponentType>` | Float input | `Input.Float(0.0)` |
| `Input.DateTime(value: SubtypeExprOrValue<DateTimeType>, style?: InputStyle): ExprType<UIComponentType>` | DateTime input | `Input.DateTime(new Date())` |

**InputStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `placeholder` | `SubtypeExprOrValue<StringType>` | Placeholder text |
| `disabled` | `SubtypeExprOrValue<BooleanType>` | Disabled state |
| `readOnly` | `SubtypeExprOrValue<BooleanType>` | Read-only state |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Input size |
| `variant` | `SubtypeExprOrValue<InputVariantType> \| InputVariantLiteral` | "outline", "subtle", "flushed" |

---

### Select

Dropdown selection component.

```typescript
import { East } from "@elaraai/east";
import { Select, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Select.Root("", [
        Select.Item("us", "United States"),
        Select.Item("uk", "United Kingdom"),
    ], { placeholder: "Select country" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Select.Root(value: SubtypeExprOrValue<StringType>, items: SubtypeExprOrValue<ArrayType<SelectItemType>>, style?: SelectStyle): ExprType<UIComponentType>` | Create select | `Select.Root("", [Select.Item(...)])` |
| `Select.Item(value: SubtypeExprOrValue<StringType>, label: SubtypeExprOrValue<StringType>, style?: SelectItemStyle): ExprType<SelectItemType>` | Create select item | `Select.Item("us", "United States")` |
| `Select.Types.Root` | East StructType for Select component | `Select.Types.Root` |
| `Select.Types.Item` | East StructType for SelectItem | `Select.Types.Item` |

**SelectStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `placeholder` | `SubtypeExprOrValue<StringType>` | Placeholder text when no selection |
| `multiple` | `SubtypeExprOrValue<BooleanType> \| boolean` | Allow multiple selections |
| `disabled` | `SubtypeExprOrValue<BooleanType> \| boolean` | Disabled state |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Select size |

**SelectItemStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `disabled` | `SubtypeExprOrValue<BooleanType> \| boolean` | Disabled state for item |

---

### Checkbox

Checkbox input component for boolean selections.

```typescript
import { East } from "@elaraai/east";
import { Checkbox, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Checkbox.Root(false, { label: "Accept terms", colorPalette: "blue" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Checkbox.Root(checked: SubtypeExprOrValue<BooleanType>, style?: CheckboxStyle): ExprType<UIComponentType>` | Create checkbox | `Checkbox.Root(true, { label: "Accept" })` |
| `Checkbox.Types.Checkbox` | East StructType for Checkbox component | `Checkbox.Types.Checkbox` |

**CheckboxStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `label` | `SubtypeExprOrValue<StringType>` | Label text displayed next to checkbox |
| `indeterminate` | `SubtypeExprOrValue<BooleanType> \| boolean` | Show indeterminate state (partial selection) |
| `disabled` | `SubtypeExprOrValue<BooleanType> \| boolean` | Disabled state |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Checkbox size |

---

### Switch

Toggle switch component for on/off states.

```typescript
import { East } from "@elaraai/east";
import { Switch, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Switch.Root(false, { label: "Enable notifications", colorPalette: "blue" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Switch.Root(checked: SubtypeExprOrValue<BooleanType>, style?: SwitchStyle): ExprType<UIComponentType>` | Create switch | `Switch.Root(true, { label: "Dark mode" })` |
| `Switch.Types.Switch` | East StructType for Switch component | `Switch.Types.Switch` |

**SwitchStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `label` | `SubtypeExprOrValue<StringType>` | Label text displayed next to switch |
| `disabled` | `SubtypeExprOrValue<BooleanType> \| boolean` | Disabled state |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Switch size |

---

### Slider

Range slider component.

```typescript
import { East } from "@elaraai/east";
import { Slider, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Slider.Root({ min: 0, max: 100, value: 50, step: 1 });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Slider.Root(style?: SliderStyle): ExprType<UIComponentType>` | Create slider | `Slider.Root({ min: 0, max: 100 })` |

---

## Collections

### Table

Data table component with typed rows.

```typescript
import { East } from "@elaraai/east";
import { Table, Badge, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    const data = $.let([
        { name: "Alice", email: "alice@example.com", role: "Admin" },
        { name: "Bob", email: "bob@example.com", role: "User" },
    ]);
    return Table.Root(data, {
        name: { header: "Name" },
        email: { header: "Email" },
        role: { header: "Role", render: value => Badge.Root(value, { colorPalette: "blue" }) },
    }, { variant: "line", striped: true });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Table.Root<T>(data: T, columns: ColumnSpec<T>, style?: TableStyle): ExprType<UIComponentType>` | Create table from data array | `Table.Root(data, ["name", "age"])` |
| `Table.Types.Root` | East StructType for Table component | `Table.Types.Root` |
| `Table.Types.Style` | East StructType for Table style | `Table.Types.Style` |
| `Table.Types.Column` | East StructType for table column | `Table.Types.Column` |
| `Table.Types.Cell` | East StructType for table cell | `Table.Types.Cell` |

**Parameters:**
- `data` - Array of struct data (e.g., `[{ name: "Alice", age: 30n }]`)
- `columns` - Array of field names `["name", "email"]` OR object config `{ name: { header: "Name", render?: val => ... } }`
- `style` - Optional table styling

**TableColumnConfig Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `header` | `SubtypeExprOrValue<StringType>` | Column header text (defaults to field name) |
| `render` | `(value: ExprType<FieldType>) => ExprType<UIComponentType>` | Custom render function |

**TableStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `variant` | `SubtypeExprOrValue<TableVariantType> \| TableVariantLiteral` | "simple", "line", "outline" |
| `size` | `SubtypeExprOrValue<TableSizeType> \| TableSizeLiteral` | "sm", "md", "lg" |
| `striped` | `SubtypeExprOrValue<BooleanType>` | Alternating row colors |
| `interactive` | `SubtypeExprOrValue<BooleanType>` | Hover effects |
| `stickyHeader` | `SubtypeExprOrValue<BooleanType>` | Sticky header |
| `showColumnBorder` | `SubtypeExprOrValue<BooleanType>` | Column borders |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |

---

### Gantt

Gantt chart for project timelines.

```typescript
import { East } from "@elaraai/east";
import { Gantt, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    const data = $.let([
        { task: "Design", start: new Date("2024-01-01"), end: new Date("2024-01-15") },
        { task: "Development", start: new Date("2024-01-10"), end: new Date("2024-02-01") },
    ]);
    return Gantt.Root(data, { task: { header: "Task" } }, row => [
        Gantt.Task({ start: row.start, end: row.end, colorPalette: "blue" }),
    ], { variant: "line", showToday: true });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Gantt.Root<T>(data: T, columns: ColumnSpec<T>, events: (row) => GanttEvent[], style?: GanttStyle): ExprType<UIComponentType>` | Create Gantt chart | `Gantt.Root(data, {...}, row => [...])` |
| `Gantt.Task(input: TaskInput): GanttEvent` | Create task bar | `Gantt.Task({ start, end })` |
| `Gantt.Milestone(input: MilestoneInput): GanttEvent` | Create milestone marker | `Gantt.Milestone({ date, label })` |

**TaskInput Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `start` | `SubtypeExprOrValue<DateTimeType>` | Start date |
| `end` | `SubtypeExprOrValue<DateTimeType>` | End date |
| `label` | `SubtypeExprOrValue<StringType>` | Optional label on task bar |
| `progress` | `SubtypeExprOrValue<IntegerType>` | Progress percentage (0-100) |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |

**MilestoneInput Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `date` | `SubtypeExprOrValue<DateTimeType>` | Milestone date |
| `label` | `SubtypeExprOrValue<StringType>` | Optional label |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |

---

### DataList

Key-value data display.

```typescript
import { East } from "@elaraai/east";
import { DataList, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return DataList.Root([
        DataList.Item("Name", "Alice"),
        DataList.Item("Email", "alice@example.com"),
    ], { orientation: "horizontal" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `DataList.Root(items: DataListItem[], style?: DataListStyle): ExprType<UIComponentType>` | Create data list | `DataList.Root([...])` |
| `DataList.Item(label: string, value: SubtypeExprOrValue<StringType>): DataListItem` | Create data list item | `DataList.Item("Name", "Alice")` |

---

### TreeView

Hierarchical tree display.

```typescript
import { East } from "@elaraai/east";
import { TreeView, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return TreeView.Root([
        TreeView.Branch("folder-1", "Documents", [
            TreeView.Item("file-1", "Resume.pdf"),
            TreeView.Item("file-2", "Cover Letter.docx"),
        ]),
        TreeView.Item("file-3", "README.md"),
    ]);
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `TreeView.Root(nodes: TreeNode[], style?: TreeViewStyle): ExprType<UIComponentType>` | Create tree view | `TreeView.Root([...])` |
| `TreeView.Branch(value: string, label: string, children: TreeNode[], style?: BranchStyle): TreeNode` | Create branch node | `TreeView.Branch("id", "Folder", [...])` |
| `TreeView.Item(value: string, label: string, style?: ItemStyle): TreeNode` | Create leaf node | `TreeView.Item("id", "File.txt")` |

---

## Charts

Access all charts through the `Chart` namespace.

### Chart.Line

```typescript
import { East } from "@elaraai/east";
import { Chart, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    const data = $.let([{ month: "Jan", revenue: 186 }, { month: "Feb", revenue: 305 }]);
    return Chart.Line(data, { revenue: { color: "teal.solid" } }, {
        xAxis: { dataKey: "month" },
        grid: Chart.Grid({ show: true }),
    });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Chart.Line<T>(data: T, series: SeriesConfig, style?: ChartStyle): ExprType<UIComponentType>` | Create line chart | `Chart.Line(data, { revenue: {...} })` |
| `Chart.Bar<T>(data: T, series: SeriesConfig, style?: BarChartStyle): ExprType<UIComponentType>` | Create bar chart | `Chart.Bar(data, { value: {...} })` |
| `Chart.Area<T>(data: T, series: SeriesConfig, style?: ChartStyle): ExprType<UIComponentType>` | Create area chart | `Chart.Area(data, {...})` |
| `Chart.Scatter<T>(data: T, series: SeriesConfig, style?: ChartStyle): ExprType<UIComponentType>` | Create scatter chart | `Chart.Scatter(data, {...})` |
| `Chart.Pie<T>(data: T, style?: PieChartStyle): ExprType<UIComponentType>` | Create pie chart | `Chart.Pie(data, {...})` |
| `Chart.Radar<T>(data: T, series: SeriesConfig, style?: ChartStyle): ExprType<UIComponentType>` | Create radar chart | `Chart.Radar(data, {...})` |
| `Chart.BarList<T>(data: T, style?: BarListStyle): ExprType<UIComponentType>` | Create bar list | `Chart.BarList(data)` |
| `Chart.BarSegment<T>(data: T, style?: BarSegmentStyle): ExprType<UIComponentType>` | Create bar segment | `Chart.BarSegment(data)` |

**Chart Helpers:**

| Signature | Description | Example |
|-----------|-------------|---------|
| `Chart.Axis(options: AxisConfig): AxisConfig` | Create axis configuration | `Chart.Axis({ dataKey: "month" })` |
| `Chart.Grid(options: GridConfig): GridConfig` | Create grid configuration | `Chart.Grid({ show: true })` |
| `Chart.Legend(options: LegendConfig): LegendConfig` | Create legend configuration | `Chart.Legend({ show: true })` |
| `Chart.Tooltip(options: TooltipConfig): TooltipConfig` | Create tooltip configuration | `Chart.Tooltip({ show: true })` |
| `Chart.TickFormat.Number(options): TickFormatter` | Number tick formatter | `Chart.TickFormat.Number({ compact: true })` |
| `Chart.TickFormat.Currency(options): TickFormatter` | Currency tick formatter | `Chart.TickFormat.Currency({ currency: "USD" })` |
| `Chart.TickFormat.Percent(options): TickFormatter` | Percent tick formatter | `Chart.TickFormat.Percent()` |
| `Chart.TickFormat.Date(options): TickFormatter` | Date tick formatter | `Chart.TickFormat.Date({ format: "MMM" })` |

---

### Sparkline

Compact inline trend visualization.

```typescript
import { East } from "@elaraai/east";
import { Sparkline, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Sparkline.Root([1.2, 2.4, 1.8, 3.1, 2.9], { type: "area", color: "teal.500" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Sparkline.Root(data: number[], style?: SparklineStyle): ExprType<UIComponentType>` | Create sparkline | `Sparkline.Root([1, 2, 3])` |

---

## Display

### Badge

```typescript
import { East } from "@elaraai/east";
import { Badge, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Badge.Root("New", { variant: "solid", colorPalette: "green" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Badge.Root(label: SubtypeExprOrValue<StringType>, style?: BadgeStyle): ExprType<UIComponentType>` | Create badge | `Badge.Root("Active", { colorPalette: "blue" })` |

---

### Tag

```typescript
import { East } from "@elaraai/east";
import { Tag, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Tag.Root("JavaScript", { variant: "subtle", closable: true });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Tag.Root(label: SubtypeExprOrValue<StringType>, style?: TagStyle): ExprType<UIComponentType>` | Create tag | `Tag.Root("React", { closable: true })` |

---

### Avatar

User profile image or initials display.

```typescript
import { East } from "@elaraai/east";
import { Avatar, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Avatar.Root({ name: "Alice Brown", colorPalette: "blue", size: "lg" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Avatar.Root(style?: AvatarStyle): ExprType<UIComponentType>` | Create avatar | `Avatar.Root({ name: "Alice" })` |
| `Avatar.Types.Avatar` | East StructType for Avatar component | `Avatar.Types.Avatar` |

**AvatarStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `src` | `SubtypeExprOrValue<StringType>` | Image URL for the avatar |
| `name` | `SubtypeExprOrValue<StringType>` | User name (used for initials fallback) |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Avatar size |
| `variant` | `SubtypeExprOrValue<StyleVariantType> \| StyleVariantLiteral` | "solid", "subtle", "outline" |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme for fallback |

---

### Stat

Key metric display with optional trend indicator.

```typescript
import { East } from "@elaraai/east";
import { Stat, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Stat.Root("Revenue", "$45,000", { helpText: "vs last month", indicator: "up" });
});
```

| Signature | Description |
|-----------|-------------|
| `Stat.Root(label, value, style?): ExprType<UIComponentType>` | Create stat display |
| `Stat.Indicator(direction): ExprType<StatIndicatorType>` | Create indicator value ("up" or "down") |

**StatStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `helpText` | `SubtypeExprOrValue<StringType>` | Help text or trend description |
| `indicator` | `SubtypeExprOrValue<StatIndicatorType> \| "up" \| "down"` | Trend indicator direction |

---

### Icon

Font Awesome icon component with typesafe prefix and name.

```typescript
import { East } from "@elaraai/east";
import { Icon, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Icon.Root("fas", "check", { size: "lg", color: "green.500" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Icon.Root(prefix: IconPrefix, name: IconName, style?: IconStyle): ExprType<UIComponentType>` | Create icon | `Icon.Root("fas", "search")` |
| `Icon.Types.Icon` | East StructType for Icon component | `Icon.Types.Icon` |
| `Icon.Types.Size` | East VariantType for icon size | `Icon.Types.Size` |

**IconStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `size` | `SubtypeExprOrValue<IconSizeType> \| IconSizeLiteral` | "xs", "sm", "md", "lg", "xl", "2xl" |
| `color` | `SubtypeExprOrValue<StringType>` | Icon color (CSS or Chakra token) |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |

**Icon Prefixes:**

| Prefix | Description |
|--------|-------------|
| `fas` | Solid icons (filled) |
| `far` | Regular icons (outlined) |
| `fab` | Brand icons (logos) |

---

## Feedback

### Alert

```typescript
import { East } from "@elaraai/east";
import { Alert, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Alert.Root({ status: "success", title: "Saved", description: "Changes saved successfully" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Alert.Root(style?: AlertStyle): ExprType<UIComponentType>` | Create alert | `Alert.Root({ status: "error", title: "Error" })` |

**AlertStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `status` | `SubtypeExprOrValue<AlertStatusType> \| AlertStatusLiteral` | "info", "warning", "error", "success" |
| `title` | `SubtypeExprOrValue<StringType>` | Alert title |
| `description` | `SubtypeExprOrValue<StringType>` | Alert description |
| `variant` | `SubtypeExprOrValue<AlertVariantType> \| AlertVariantLiteral` | "subtle", "solid", "outline" |

---

### Progress

Progress bar for displaying completion status.

```typescript
import { East } from "@elaraai/east";
import { Progress, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Progress.Root(75.0, { colorPalette: "green", size: "md", striped: true });
});
```

| Signature | Description |
|-----------|-------------|
| `Progress.Root(value, style?): ExprType<UIComponentType>` | Create progress bar |

**ProgressStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `min` | `SubtypeExprOrValue<FloatType>` | Minimum value (default 0) |
| `max` | `SubtypeExprOrValue<FloatType>` | Maximum value (default 100) |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Size variant |
| `striped` | `SubtypeExprOrValue<BooleanType>` | Show striped pattern |
| `animated` | `SubtypeExprOrValue<BooleanType>` | Animate the progress |
| `label` | `SubtypeExprOrValue<StringType>` | Label text |
| `valueText` | `SubtypeExprOrValue<StringType>` | Value display text |

---

## Disclosure

### Accordion

```typescript
import { East } from "@elaraai/east";
import { Accordion, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Accordion.Root([
        Accordion.Item("section-1", "Section 1", [Text.Root("Content 1")]),
        Accordion.Item("section-2", "Section 2", [Text.Root("Content 2")]),
    ], { variant: "enclosed", collapsible: true });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Accordion.Root(items: AccordionItem[], style?: AccordionStyle): ExprType<UIComponentType>` | Create accordion | `Accordion.Root([...])` |
| `Accordion.Item(value: string, trigger: string, content: UIComponent[], style?: AccordionItemStyle): AccordionItem` | Create accordion item | `Accordion.Item("id", "Title", [...])` |

**AccordionStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `multiple` | `SubtypeExprOrValue<BooleanType>` | Whether multiple items can be open at once |
| `collapsible` | `SubtypeExprOrValue<BooleanType>` | Whether all items can be collapsed |
| `variant` | `SubtypeExprOrValue<AccordionVariantType> \| AccordionVariantLiteral` | "enclosed", "plain", "subtle" |

**AccordionItemStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `disabled` | `SubtypeExprOrValue<BooleanType>` | Whether this item is disabled |

---

### Tabs

```typescript
import { East } from "@elaraai/east";
import { Tabs, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Tabs.Root([
        Tabs.Tab("tab-1", "Overview", [Text.Root("Overview content")]),
        Tabs.Tab("tab-2", "Details", [Text.Root("Details content")]),
    ], { variant: "line", fitted: true });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Tabs.Root(items: TabItem[], style?: TabsStyle): ExprType<UIComponentType>` | Create tabs | `Tabs.Root([...])` |
| `Tabs.Tab(value: string, trigger: string, content: UIComponent[], style?: TabsItemStyle): TabItem` | Create tab item | `Tabs.Tab("id", "Label", [...])` |

**TabsStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `variant` | `SubtypeExprOrValue<TabsVariantType> \| TabsVariantLiteral` | "line", "subtle", "enclosed", "outline", "plain" |
| `size` | `SubtypeExprOrValue<TabsSizeType> \| TabsSizeLiteral` | "sm", "md", "lg" |
| `orientation` | `SubtypeExprOrValue<OrientationType> \| OrientationLiteral` | "horizontal", "vertical" |
| `fitted` | `SubtypeExprOrValue<BooleanType>` | Whether tabs take equal width |
| `justify` | `SubtypeExprOrValue<TabsJustifyType> \| TabsJustifyLiteral` | "start", "center", "end" |
| `colorPalette` | `SubtypeExprOrValue<ColorSchemeType> \| ColorSchemeLiteral` | Color scheme |
| `lazyMount` | `SubtypeExprOrValue<BooleanType>` | Mount content only when selected |

**TabsItemStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `disabled` | `SubtypeExprOrValue<BooleanType>` | Whether this tab is disabled |

---

### Carousel

```typescript
import { East } from "@elaraai/east";
import { Carousel, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Carousel.Root([
        Text.Root("Slide 1"),
        Text.Root("Slide 2"),
    ], { loop: true, autoplay: true, showIndicators: true });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Carousel.Root(items: UIComponent[], style?: CarouselStyle): ExprType<UIComponentType>` | Create carousel | `Carousel.Root([...], { loop: true })` |

**CarouselStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `orientation` | `SubtypeExprOrValue<OrientationType> \| OrientationLiteral` | "horizontal", "vertical" |
| `spacing` | `SubtypeExprOrValue<StringType>` | Gap between slides |
| `loop` | `SubtypeExprOrValue<BooleanType>` | Enable infinite scrolling |
| `autoplay` | `SubtypeExprOrValue<BooleanType>` | Enable automatic advancement |
| `slidesPerView` | `SubtypeExprOrValue<IntegerType>` | Number of visible slides |
| `showIndicators` | `SubtypeExprOrValue<BooleanType>` | Show dot indicators |
| `showControls` | `SubtypeExprOrValue<BooleanType>` | Show prev/next controls |

---

## Overlays

### Dialog

```typescript
import { East } from "@elaraai/east";
import { Dialog, Button, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Dialog.Root(
        Button.Root("Open Dialog"),
        [Text.Root("Dialog content")],
        { title: "Confirm Action", size: "md" }
    );
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Dialog.Root(trigger: UIComponent, body: UIComponent[], style?: DialogStyle): ExprType<UIComponentType>` | Create dialog | `Dialog.Root(Button.Root("Open"), [...])` |

**DialogStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `title` | `SubtypeExprOrValue<StringType>` | Dialog title |
| `description` | `SubtypeExprOrValue<StringType>` | Dialog description |
| `size` | `SubtypeExprOrValue<DialogSizeType> \| DialogSizeLiteral` | "xs", "sm", "md", "lg", "xl", "cover", "full" |
| `placement` | `SubtypeExprOrValue<DialogPlacementType> \| DialogPlacementLiteral` | "center", "top", "bottom" |
| `motionPreset` | `SubtypeExprOrValue<DialogMotionPresetType> \| DialogMotionPresetLiteral` | "scale", "slide-in-bottom", "slide-in-top", "none" |
| `closeOnInteractOutside` | `SubtypeExprOrValue<BooleanType>` | Close when clicking outside |
| `closeOnEscape` | `SubtypeExprOrValue<BooleanType>` | Close on escape key |

---

### Drawer

```typescript
import { East } from "@elaraai/east";
import { Drawer, Button, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Drawer.Root(
        Button.Root("Open Drawer"),
        [Text.Root("Drawer content")],
        { title: "Settings", placement: "end" }
    );
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Drawer.Root(trigger: UIComponent, body: UIComponent[], style?: DrawerStyle): ExprType<UIComponentType>` | Create drawer | `Drawer.Root(Button.Root("Open"), [...])` |

**DrawerStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `title` | `SubtypeExprOrValue<StringType>` | Drawer title |
| `description` | `SubtypeExprOrValue<StringType>` | Drawer description |
| `size` | `SubtypeExprOrValue<DrawerSizeType> \| DrawerSizeLiteral` | "xs", "sm", "md", "lg", "xl", "full" |
| `placement` | `SubtypeExprOrValue<DrawerPlacementType> \| DrawerPlacementLiteral` | "start", "end", "top", "bottom" |
| `contained` | `SubtypeExprOrValue<BooleanType>` | Render within parent container |
| `closeOnInteractOutside` | `SubtypeExprOrValue<BooleanType>` | Close when clicking outside |
| `closeOnEscape` | `SubtypeExprOrValue<BooleanType>` | Close on escape key |

---

### Tooltip

```typescript
import { East } from "@elaraai/east";
import { Tooltip, Button, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Tooltip.Root(Button.Root("Hover me"), "Helpful information");
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Tooltip.Root(trigger: UIComponent, content: SubtypeExprOrValue<StringType>, style?: TooltipStyle): ExprType<UIComponentType>` | Create tooltip | `Tooltip.Root(Button.Root("?"), "Help text")` |

**TooltipStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `placement` | `SubtypeExprOrValue<PlacementType> \| PlacementLiteral` | "top", "bottom", "left", "right" (with -start/-end variants) |
| `hasArrow` | `SubtypeExprOrValue<BooleanType>` | Show arrow pointing to trigger |

---

### Popover

```typescript
import { East } from "@elaraai/east";
import { Popover, Button, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Popover.Root(
        Button.Root("Click me"),
        [Text.Root("Popover content")],
        { title: "More Info", placement: "bottom" }
    );
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Popover.Root(trigger: UIComponent, body: UIComponent[], style?: PopoverStyle): ExprType<UIComponentType>` | Create popover | `Popover.Root(Button.Root("Info"), [...])` |

**PopoverStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `title` | `SubtypeExprOrValue<StringType>` | Popover title |
| `description` | `SubtypeExprOrValue<StringType>` | Popover description |
| `size` | `SubtypeExprOrValue<PopoverSizeType> \| PopoverSizeLiteral` | "xs", "sm", "md", "lg" |
| `placement` | `SubtypeExprOrValue<PlacementType> \| PlacementLiteral` | Position relative to trigger |
| `hasArrow` | `SubtypeExprOrValue<BooleanType>` | Show arrow pointing to trigger |
| `closeOnInteractOutside` | `SubtypeExprOrValue<BooleanType>` | Close when clicking outside |
| `closeOnEscape` | `SubtypeExprOrValue<BooleanType>` | Close on escape key |

---

### Menu

```typescript
import { East } from "@elaraai/east";
import { Menu, Button, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Menu.Root(Button.Root("Actions"), [
        Menu.Item("edit", "Edit"),
        Menu.Separator(),
        Menu.Item("delete", "Delete"),
    ]);
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Menu.Root(trigger: UIComponent, items: MenuItem[], style?: MenuStyle): ExprType<UIComponentType>` | Create menu | `Menu.Root(Button.Root("..."), [...])` |
| `Menu.Item(value: string, label: string, disabled?: boolean): MenuItem` | Create menu item | `Menu.Item("edit", "Edit")` |
| `Menu.Separator(): MenuItem` | Create separator | `Menu.Separator()` |

**MenuStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `placement` | `SubtypeExprOrValue<PlacementType> \| PlacementLiteral` | Position relative to trigger |

---

## Container

### Card

Content card with header and body.

```typescript
import { East } from "@elaraai/east";
import { Card, Text, UIComponentType } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    return Card.Root([
        Text.Root("Card content here"),
    ], { title: "Card Title", description: "Optional description", variant: "elevated" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Card.Root(body: UIComponent[], style?: CardStyle): ExprType<UIComponentType>` | Create card | `Card.Root([...], { title: "Title" })` |

**CardStyle Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `title` | `SubtypeExprOrValue<StringType>` | Card title |
| `description` | `SubtypeExprOrValue<StringType>` | Card description |
| `variant` | `SubtypeExprOrValue<CardVariantType> \| CardVariantLiteral` | "elevated", "outline", "subtle" |
| `size` | `SubtypeExprOrValue<SizeType> \| SizeLiteral` | Card size |

---

## State Management

East UI provides reactive state management through the `State` namespace. State is stored as Beast2-encoded blobs, allowing any East type to be stored and retrieved.

### State.readTyped / State.writeTyped

Typed convenience wrappers that handle Beast2 encoding automatically.

```typescript
import { East, IntegerType, NullType, some } from "@elaraai/east";
import { State, Button, Text, Stack, UIComponentType } from "@elaraai/east-ui";

const counter = East.function([], UIComponentType, $ => {
    // Initialize state (only writes if key doesn't exist)
    $(State.initTyped("counter", 0n, IntegerType)());

    // Read typed value - returns Option<Integer>
    const count = $.let(State.readTyped("counter", IntegerType)());

    return Stack.VStack([
        Text.Root(East.str`Count: ${count.unwrap("some")}`),
        Button.Root("Increment", {
            onClick: East.function([], NullType, $ => {
                const current = $.let(State.readTyped("counter", IntegerType)());
                $(State.writeTyped("counter", some(current.unwrap("some").add(1n)), IntegerType)());
            })
        }),
    ], { gap: "4" });
});

// Compile with State.Implementation to enable state functionality
const compiled = counter.toIR().compile(State.Implementation);
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `State.readTyped(key: string, type: EastType)(): ExprType<OptionType<T>>` | Read typed value from state | `State.readTyped("counter", IntegerType)()` |
| `State.writeTyped(key: string, value: Option<T>, type: EastType)(): ExprType<NullType>` | Write typed value to state | `State.writeTyped("key", some(42n), IntegerType)()` |
| `State.initTyped(key: string, defaultValue: T, type: EastType)(): ExprType<NullType>` | Initialize state if not set | `State.initTyped("counter", 0n, IntegerType)()` |
| `State.has(key: string): ExprType<BooleanType>` | Check if key exists | `State.has("counter")` |
| `State.Implementation` | Platform functions for compile | `ir.compile(State.Implementation)` |
| `State.store` | Singleton UI store instance | `State.store.subscribe(...)` |

**Important:** The `readTyped`, `writeTyped`, and `initTyped` functions return East functions that must be invoked with `()`:

```typescript
// Correct - invoke the returned function
const value = $.let(State.readTyped("key", IntegerType)());
$(State.writeTyped("key", some(42n), IntegerType)());

// Wrong - missing ()
const value = $.let(State.readTyped("key", IntegerType));  // Error!
```

### State.read / State.write (Low-level)

Low-level functions for manual Beast2 encoding/decoding.

```typescript
import { East, IntegerType, NullType, some } from "@elaraai/east";
import { State, UIComponentType, Text } from "@elaraai/east-ui";

const example = East.function([], UIComponentType, $ => {
    // Read raw blob
    const count = $.let(0n);
    $.match($(State.read("counter")), {
        some: ($, blob) => $.assign(count, blob.decodeBeast(IntegerType, "v2")),
    });

    // Write raw blob
    const onClick = East.function([], NullType, $ => {
        const newBlob = East.Blob.encodeBeast(East.value(42n), "v2");
        $(State.write("counter", some(newBlob)));
    });

    return Text.Root(East.str`Count: ${count}`);
});
```

---

## Reactive Components

`Reactive.Root` creates components that re-render independently when their state dependencies change. This enables efficient updates where only affected parts of the UI re-render.

### Reactive.Root

```typescript
import { East, IntegerType, NullType, some } from "@elaraai/east";
import { Reactive, State, Text, Button, Stack, UIComponentType } from "@elaraai/east-ui";

const app = East.function([], UIComponentType, $ => {
    // Initialize state
    $(State.initTyped("counter", 0n, IntegerType)());

    return Stack.VStack([
        // This component re-renders only when "counter" changes
        Reactive.Root($ => {
            const count = $.let(State.readTyped("counter", IntegerType)());
            return Text.Root(East.str`Count: ${count.unwrap("some")}`);
        }),

        // Button triggers state update
        Button.Root("Increment", {
            onClick: East.function([], NullType, $ => {
                const current = $.let(State.readTyped("counter", IntegerType)());
                $(State.writeTyped("counter", some(current.unwrap("some").add(1n)), IntegerType)());
            })
        }),
    ], { gap: "4" });
});
```

| Signature | Description | Example |
|-----------|-------------|---------|
| `Reactive.Root(body: ($) => UIComponentType): ExprType<UIComponentType>` | Create reactive component | `Reactive.Root($ => Text.Root("Hi"))` |

**Important Constraints:**

The body function passed to `Reactive.Root` must be a **free function** with no captures from parent East scope:

```typescript
// ✅ Correct - no captures, state read inside body
Reactive.Root($ => {
    const count = $.let(State.readTyped("counter", IntegerType)());
    return Text.Root(East.str`Count: ${count.unwrap("some")}`);
});

// ❌ Wrong - captures 'parentValue' from parent scope
const parentValue = $.let(42n);
Reactive.Root($ => {
    return Text.Root(East.str`Value: ${parentValue}`);  // Error! Capture detected
});
```

**What IS allowed inside Reactive.Root:**
- Platform functions (`State.readTyped`, `State.writeTyped`, etc.)
- Module-level constants and functions
- Callbacks defined inside the body (`East.function`)
- Variables defined inside the body (`$.let`)

**What is NOT allowed:**
- Parent East function scope variables (`$.let`, parameters)
- Any variable captured from enclosing East function scope

If you need to share data between parent and reactive components, use `State` for that shared data.

---

## License

Dual-licensed under AGPL-3.0 (open source) and commercial license. See [LICENSE.md](LICENSE.md).
