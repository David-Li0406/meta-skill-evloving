# East UI API Reference

Complete function signatures, types, and arguments for all UI components.

---

## Table of Contents

- [Layout](#layout)
- [Typography](#typography)
- [Buttons](#buttons)
- [Forms](#forms)
- [Display](#display)
- [Feedback](#feedback)
- [Collections](#collections)
- [Charts](#charts)
- [Disclosure](#disclosure)
- [Overlays](#overlays)
- [State](#state)
- [Style Types](#style-types)

---

## Layout

Layout components for arranging content: Box, Flex, Stack, Grid, Separator, Splitter.

**Import:**
```typescript
import { Box, Flex, Stack, Grid, Separator, Splitter, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Box.Root(children: ArrayType<UIComponentType>, style?: BoxStyle): UIComponentType` | Basic container with padding, margin, background |
| `Box.Padding(top: String, right: String, bottom: String, left: String): PaddingType` | Create padding configuration |
| `Box.Margin(top: String, right: String, bottom: String, left: String): MarginType` | Create margin configuration |
| `Flex.Root(children: ArrayType<UIComponentType>, style?: FlexStyle): UIComponentType` | Flexbox container with direction, justify, align |
| `Stack.Root(children: ArrayType<UIComponentType>, style?: StackStyle): UIComponentType` | Stack with configurable direction |
| `Stack.HStack(children: ArrayType<UIComponentType>, style?: StackStyle): UIComponentType` | Horizontal stack (row direction) |
| `Stack.VStack(children: ArrayType<UIComponentType>, style?: StackStyle): UIComponentType` | Vertical stack (column direction) |
| `Grid.Root(items: ArrayType<GridItemType>, style?: GridStyle): UIComponentType` | CSS grid container |
| `Grid.Item(content: UIComponentType, style?: GridItemStyle): GridItemType` | Grid item with span/position |
| `Separator.Root(style?: SeparatorStyle): UIComponentType` | Visual divider line |
| `Splitter.Root(panels: ArrayType<SplitterPanelType>, defaultSize: ArrayType<Float>, style?: SplitterStyle): UIComponentType` | Resizable panel container |

**East Types:**

| Type | Definition |
|------|------------|
| `BoxStyleType` | `StructType({ display: OptionType<DisplayType>, width: OptionType<String>, height: OptionType<String>, minHeight: OptionType<String>, minWidth: OptionType<String>, maxHeight: OptionType<String>, maxWidth: OptionType<String>, overflow: OptionType<OverflowType>, overflowX: OptionType<OverflowType>, overflowY: OptionType<OverflowType>, padding: OptionType<PaddingType>, margin: OptionType<MarginType>, background: OptionType<String>, color: OptionType<String>, borderRadius: OptionType<String>, flexDirection: OptionType<FlexDirectionType>, justifyContent: OptionType<JustifyContentType>, alignItems: OptionType<AlignItemsType>, gap: OptionType<String> })` |
| `PaddingType` | `StructType({ top: OptionType<String>, right: OptionType<String>, bottom: OptionType<String>, left: OptionType<String> })` |
| `MarginType` | `StructType({ top: OptionType<String>, right: OptionType<String>, bottom: OptionType<String>, left: OptionType<String> })` |
| `StackStyleType` | `StructType({ direction: OptionType<FlexDirectionType>, gap: OptionType<String>, align: OptionType<AlignItemsType>, justify: OptionType<JustifyContentType>, wrap: OptionType<FlexWrapType>, padding: OptionType<PaddingType>, margin: OptionType<MarginType>, background: OptionType<String>, width: OptionType<String>, height: OptionType<String>, minHeight: OptionType<String>, minWidth: OptionType<String>, maxHeight: OptionType<String>, maxWidth: OptionType<String>, overflow: OptionType<OverflowType>, overflowX: OptionType<OverflowType>, overflowY: OptionType<OverflowType> })` |
| `FlexStyleType` | `StructType({ direction: OptionType<FlexDirectionType>, justify: OptionType<JustifyContentType>, align: OptionType<AlignItemsType>, wrap: OptionType<FlexWrapType>, gap: OptionType<String>, padding: OptionType<PaddingType>, margin: OptionType<MarginType>, background: OptionType<String>, width: OptionType<String>, height: OptionType<String> })` |
| `GridStyleType` | `StructType({ width: OptionType<String>, height: OptionType<String>, minHeight: OptionType<String>, minWidth: OptionType<String>, maxHeight: OptionType<String>, maxWidth: OptionType<String>, padding: OptionType<PaddingType>, templateColumns: OptionType<String>, templateRows: OptionType<String>, templateAreas: OptionType<String>, gap: OptionType<String>, columnGap: OptionType<String>, rowGap: OptionType<String>, justifyItems: OptionType<JustifyContentType>, alignItems: OptionType<AlignItemsType>, justifyContent: OptionType<JustifyContentType>, alignContent: OptionType<AlignItemsType>, autoColumns: OptionType<String>, autoRows: OptionType<String>, autoFlow: OptionType<GridAutoFlowType> })` |
| `SeparatorStyleType` | `StructType({ orientation: OptionType<OrientationType>, size: OptionType<SizeType> })` |
| `DisplayType` | `VariantType({ block, inline, "inline-block", flex, "inline-flex", grid, "inline-grid", none })` |
| `OverflowType` | `VariantType({ visible, hidden, scroll, auto })` |
| `FlexDirectionType` | `VariantType({ row, column, "row-reverse", "column-reverse" })` |
| `JustifyContentType` | `VariantType({ "flex-start", "flex-end", center, "space-between", "space-around", "space-evenly" })` |
| `AlignItemsType` | `VariantType({ "flex-start", "flex-end", center, baseline, stretch })` |
| `FlexWrapType` | `VariantType({ nowrap, wrap, "wrap-reverse" })` |
| `GridAutoFlowType` | `VariantType({ row, column, dense, "row dense", "column dense" })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `BoxStyle` | `{ display?: DisplayType \| DisplayLiteral, width?: String, height?: String, minHeight?: String, minWidth?: String, maxHeight?: String, maxWidth?: String, overflow?: OverflowType \| OverflowLiteral, padding?: String \| PaddingType, margin?: String \| MarginType, background?: String, color?: String, borderRadius?: String, flexDirection?: FlexDirectionType \| FlexDirectionLiteral, justifyContent?: JustifyContentType \| JustifyContentLiteral, alignItems?: AlignItemsType \| AlignItemsLiteral, gap?: String }` |
| `FlexStyle` | `{ direction?: FlexDirectionType \| FlexDirectionLiteral, justify?: JustifyContentType \| JustifyContentLiteral, align?: AlignItemsType \| AlignItemsLiteral, wrap?: FlexWrapType \| FlexWrapLiteral, gap?: String, padding?: String \| PaddingType, margin?: String \| MarginType, background?: String, width?: String, height?: String }` |
| `StackStyle` | `{ direction?: FlexDirectionType \| FlexDirectionLiteral, gap?: String, align?: AlignItemsType \| AlignItemsLiteral, justify?: JustifyContentType \| JustifyContentLiteral, wrap?: FlexWrapType \| FlexWrapLiteral, padding?: String \| PaddingType, margin?: String \| MarginType, background?: String, width?: String, height?: String }` |
| `GridStyle` | `{ templateColumns?: String, templateRows?: String, templateAreas?: String, gap?: String, columnGap?: String, rowGap?: String, justifyItems?: JustifyContentLiteral, alignItems?: AlignItemsLiteral, autoColumns?: String, autoRows?: String, autoFlow?: GridAutoFlowLiteral, width?: String, height?: String, padding?: String \| PaddingType }` |
| `SeparatorStyle` | `{ orientation?: OrientationType \| OrientationLiteral, size?: SizeType \| SizeLiteral }` |

---

## Typography

Text display components: Text, Heading, Code, CodeBlock, Link, Highlight, Mark, List.

**Import:**
```typescript
import { Text, Heading, Code, CodeBlock, Link, Highlight, Mark, List, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Text.Root(value: String, style?: TextStyle): UIComponentType` | Basic text with styling |
| `Heading.Root(value: String, style?: HeadingStyle): UIComponentType` | Semantic heading (h1-h6) |
| `Code.Root(value: String, style?: CodeStyle): UIComponentType` | Inline code snippet |
| `CodeBlock.Root(value: String, style?: CodeBlockStyle): UIComponentType` | Syntax-highlighted code block |
| `Link.Root(children: String, href: String, style?: LinkStyle): UIComponentType` | Clickable hyperlink |
| `Highlight.Root(value: String, style?: HighlightStyle): UIComponentType` | Highlighted text span |
| `Mark.Root(value: String, style?: MarkStyle): UIComponentType` | Marked/annotated text |
| `List.Ordered(items: ArrayType<String>, style?: ListStyle): UIComponentType` | Numbered list |
| `List.Unordered(items: ArrayType<String>, style?: ListStyle): UIComponentType` | Bulleted list |

**East Types:**

| Type | Definition |
|------|------------|
| `TextType` | `StructType({ value: String, color: OptionType<String>, background: OptionType<String>, fontWeight: OptionType<FontWeightType>, fontStyle: OptionType<FontStyleType>, fontSize: OptionType<SizeType>, textTransform: OptionType<TextTransformType>, textAlign: OptionType<TextAlignType>, textOverflow: OptionType<TextOverflowType>, whiteSpace: OptionType<WhiteSpaceType>, overflow: OptionType<OverflowType>, borderWidth: OptionType<BorderWidthType>, borderStyle: OptionType<BorderStyleType>, borderColor: OptionType<String> })` |
| `HeadingType` | `StructType({ value: String, size: OptionType<HeadingSizeType>, color: OptionType<String> })` |
| `CodeType` | `StructType({ value: String, colorPalette: OptionType<ColorSchemeType> })` |
| `CodeBlockType` | `StructType({ value: String, language: OptionType<String>, showLineNumbers: OptionType<Boolean> })` |
| `LinkType` | `StructType({ children: String, href: String, isExternal: OptionType<Boolean>, colorPalette: OptionType<ColorSchemeType> })` |
| `HighlightType` | `StructType({ value: String, colorPalette: OptionType<ColorSchemeType> })` |
| `MarkType` | `StructType({ value: String, colorPalette: OptionType<ColorSchemeType> })` |
| `ListType` | `StructType({ items: ArrayType<String>, ordered: Boolean })` |
| `FontWeightType` | `VariantType({ normal, bold, semibold, medium, light })` |
| `FontStyleType` | `VariantType({ normal, italic })` |
| `TextAlignType` | `VariantType({ left, center, right, justify })` |
| `TextTransformType` | `VariantType({ uppercase, lowercase, capitalize, none })` |
| `TextOverflowType` | `VariantType({ clip, ellipsis })` |
| `WhiteSpaceType` | `VariantType({ normal, nowrap, pre, "pre-wrap", "pre-line" })` |
| `SizeType` | `VariantType({ xs, sm, md, lg })` |
| `HeadingSizeType` | `VariantType({ xs, sm, md, lg, xl, "2xl", "3xl", "4xl" })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `TextStyle` | `{ color?: String, background?: String, fontWeight?: FontWeightType \| FontWeightLiteral, fontStyle?: FontStyleType \| FontStyleLiteral, fontSize?: SizeType \| SizeLiteral, textTransform?: TextTransformType \| TextTransformLiteral, textAlign?: TextAlignType \| TextAlignLiteral, textOverflow?: TextOverflowType \| TextOverflowLiteral, whiteSpace?: WhiteSpaceType \| WhiteSpaceLiteral, overflow?: OverflowType \| OverflowLiteral, borderWidth?: BorderWidthType \| BorderWidthLiteral, borderStyle?: BorderStyleType \| BorderStyleLiteral, borderColor?: String }` |
| `HeadingStyle` | `{ size?: HeadingSizeType \| HeadingSizeLiteral, color?: String }` |
| `CodeStyle` | `{ colorPalette?: ColorSchemeType \| ColorSchemeLiteral }` |
| `CodeBlockStyle` | `{ language?: String, showLineNumbers?: Boolean }` |
| `LinkStyle` | `{ isExternal?: Boolean, colorPalette?: ColorSchemeType \| ColorSchemeLiteral }` |
| `HighlightStyle` | `{ colorPalette?: ColorSchemeType \| ColorSchemeLiteral }` |
| `MarkStyle` | `{ colorPalette?: ColorSchemeType \| ColorSchemeLiteral }` |
| `ListStyle` | `{ gap?: String }` |

---

## Buttons

Interactive button components: Button, IconButton.

**Import:**
```typescript
import { Button, IconButton, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Button.Root(label: String, style?: ButtonStyle): UIComponentType` | Clickable button with label |
| `IconButton.Root(icon: String, style?: IconButtonStyle): UIComponentType` | Icon-only button |

**East Types:**

| Type | Definition |
|------|------------|
| `ButtonType` | `StructType({ label: String, style: OptionType<ButtonStyleType> })` |
| `ButtonStyleType` | `StructType({ variant: OptionType<ButtonVariantType>, colorPalette: OptionType<ColorSchemeType>, size: OptionType<SizeType>, loading: OptionType<Boolean>, disabled: OptionType<Boolean>, onClick: OptionType<FunctionType<[], Null>> })` |
| `IconButtonType` | `StructType({ icon: String, style: OptionType<IconButtonStyleType> })` |
| `IconButtonStyleType` | `StructType({ variant: OptionType<ButtonVariantType>, colorPalette: OptionType<ColorSchemeType>, size: OptionType<SizeType>, loading: OptionType<Boolean>, disabled: OptionType<Boolean>, onClick: OptionType<FunctionType<[], Null>> })` |
| `ButtonVariantType` | `VariantType({ solid, subtle, outline, ghost })` |
| `ColorSchemeType` | `VariantType({ gray, red, orange, yellow, green, teal, blue, cyan, purple, pink })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `ButtonStyle` | `{ variant?: ButtonVariantType \| ButtonVariantLiteral, colorPalette?: ColorSchemeType \| ColorSchemeLiteral, size?: SizeType \| SizeLiteral, loading?: Boolean, disabled?: Boolean, onClick?: ($: BlockBuilder) => void }` |
| `IconButtonStyle` | `{ variant?: ButtonVariantType \| ButtonVariantLiteral, colorPalette?: ColorSchemeType \| ColorSchemeLiteral, size?: SizeType \| SizeLiteral, loading?: Boolean, disabled?: Boolean, onClick?: ($: BlockBuilder) => void }` |

---

## Forms

Form input components: Input, Textarea, Select, Checkbox, Switch, Slider, Field, FileUpload, TagsInput.

**Import:**
```typescript
import { Input, Textarea, Select, Checkbox, Switch, Slider, Field, FileUpload, TagsInput, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Input.String(value: String, style?: StringInputStyle): UIComponentType` | Text input for strings |
| `Input.Integer(value: Integer, style?: IntegerInputStyle): UIComponentType` | Numeric input for integers |
| `Input.Float(value: Float, style?: FloatInputStyle): UIComponentType` | Numeric input for floats |
| `Input.DateTime(value: DateTime, style?: DateTimeInputStyle): UIComponentType` | Date/time picker input |
| `Textarea.Root(value: String, style?: TextareaStyle): UIComponentType` | Multi-line text input |
| `Select.Root(items: ArrayType<SelectItemType>, style?: SelectStyle): UIComponentType` | Dropdown selection |
| `Checkbox.Root(checked: Boolean, style?: CheckboxStyle): UIComponentType` | Boolean checkbox |
| `Switch.Root(checked: Boolean, style?: SwitchStyle): UIComponentType` | Toggle switch |
| `Slider.Root(value: ArrayType<Float>, style?: SliderStyle): UIComponentType` | Range slider with min, max, step |
| `Field.Root(control: UIComponentType, style?: FieldStyle): UIComponentType` | Form field wrapper with label, error |
| `FileUpload.Root(style?: FileUploadStyle): UIComponentType` | File upload input |
| `TagsInput.Root(value: ArrayType<String>, style?: TagsInputStyle): UIComponentType` | Tag input with add/remove |

**East Types:**

| Type | Definition |
|------|------------|
| `StringInputType` | `StructType({ value: String, placeholder: OptionType<String>, variant: OptionType<InputVariantType>, size: OptionType<SizeType>, maxLength: OptionType<Integer>, pattern: OptionType<String>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[String], Null>>, onBlur: OptionType<FunctionType<[], Null>>, onFocus: OptionType<FunctionType<[], Null>> })` |
| `IntegerInputType` | `StructType({ value: Integer, min: OptionType<Integer>, max: OptionType<Integer>, step: OptionType<Integer>, variant: OptionType<InputVariantType>, size: OptionType<SizeType>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[Integer], Null>>, onBlur: OptionType<FunctionType<[], Null>>, onFocus: OptionType<FunctionType<[], Null>> })` |
| `FloatInputType` | `StructType({ value: Float, min: OptionType<Float>, max: OptionType<Float>, step: OptionType<Float>, precision: OptionType<Integer>, variant: OptionType<InputVariantType>, size: OptionType<SizeType>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[Float], Null>>, onBlur: OptionType<FunctionType<[], Null>>, onFocus: OptionType<FunctionType<[], Null>> })` |
| `DateTimeInputType` | `StructType({ value: DateTime, min: OptionType<DateTime>, max: OptionType<DateTime>, precision: OptionType<DateTimePrecisionType>, format: OptionType<ArrayType<DateTimeFormatTokenType>>, variant: OptionType<InputVariantType>, size: OptionType<SizeType>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[DateTime], Null>>, onBlur: OptionType<FunctionType<[], Null>>, onFocus: OptionType<FunctionType<[], Null>> })` |
| `TextareaType` | `StructType({ value: String, placeholder: OptionType<String>, variant: OptionType<InputVariantType>, size: OptionType<SizeType>, rows: OptionType<Integer>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[String], Null>> })` |
| `SelectRootType` | `StructType({ items: ArrayType<SelectItemType>, value: OptionType<String>, placeholder: OptionType<String>, variant: OptionType<InputVariantType>, size: OptionType<SizeType>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[String], Null>> })` |
| `SelectItemType` | `StructType({ value: String, label: String, disabled: OptionType<Boolean> })` |
| `CheckboxType` | `StructType({ checked: Boolean, label: OptionType<String>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[Boolean], Null>> })` |
| `SwitchType` | `StructType({ checked: Boolean, label: OptionType<String>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[Boolean], Null>> })` |
| `SliderType` | `StructType({ value: ArrayType<Float>, min: Float, max: Float, step: OptionType<Float>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[ArrayType<Float>], Null>> })` |
| `FieldType` | `StructType({ control: UIComponentType, label: OptionType<String>, helperText: OptionType<String>, errorText: OptionType<String>, required: OptionType<Boolean>, invalid: OptionType<Boolean> })` |
| `FileUploadType` | `StructType({ accept: OptionType<String>, maxFiles: OptionType<Integer>, maxFileSize: OptionType<Integer>, disabled: OptionType<Boolean>, onFileChange: OptionType<FunctionType<[ArrayType<FileType>], Null>> })` |
| `TagsInputRootType` | `StructType({ value: ArrayType<String>, placeholder: OptionType<String>, max: OptionType<Integer>, disabled: OptionType<Boolean>, onChange: OptionType<FunctionType<[ArrayType<String>], Null>> })` |
| `InputVariantType` | `VariantType({ outline, subtle, flushed })` |
| `DateTimePrecisionType` | `VariantType({ date, time, datetime })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `StringInputStyle` | `{ placeholder?: String, variant?: InputVariantType \| InputVariantLiteral, size?: SizeType \| SizeLiteral, maxLength?: Integer, pattern?: String, disabled?: Boolean, onChange?: ($: BlockBuilder, value: StringExpr) => void, onBlur?: ($: BlockBuilder) => void, onFocus?: ($: BlockBuilder) => void }` |
| `IntegerInputStyle` | `{ min?: Integer, max?: Integer, step?: Integer, variant?: InputVariantType \| InputVariantLiteral, size?: SizeType \| SizeLiteral, disabled?: Boolean, onChange?: ($: BlockBuilder, value: IntegerExpr) => void, onBlur?: ($: BlockBuilder) => void, onFocus?: ($: BlockBuilder) => void }` |
| `FloatInputStyle` | `{ min?: Float, max?: Float, step?: Float, precision?: Integer, variant?: InputVariantType \| InputVariantLiteral, size?: SizeType \| SizeLiteral, disabled?: Boolean, onChange?: ($: BlockBuilder, value: FloatExpr) => void, onBlur?: ($: BlockBuilder) => void, onFocus?: ($: BlockBuilder) => void }` |
| `DateTimeInputStyle` | `{ min?: DateTime, max?: DateTime, precision?: DateTimePrecisionType \| DateTimePrecisionLiteral, variant?: InputVariantType \| InputVariantLiteral, size?: SizeType \| SizeLiteral, disabled?: Boolean, onChange?: ($: BlockBuilder, value: DateTimeExpr) => void }` |
| `TextareaStyle` | `{ placeholder?: String, variant?: InputVariantType \| InputVariantLiteral, size?: SizeType \| SizeLiteral, rows?: Integer, disabled?: Boolean, onChange?: ($: BlockBuilder, value: StringExpr) => void }` |
| `SelectStyle` | `{ value?: String, placeholder?: String, variant?: InputVariantType \| InputVariantLiteral, size?: SizeType \| SizeLiteral, disabled?: Boolean, onChange?: ($: BlockBuilder, value: StringExpr) => void }` |
| `CheckboxStyle` | `{ label?: String, disabled?: Boolean, onChange?: ($: BlockBuilder, checked: BooleanExpr) => void }` |
| `SwitchStyle` | `{ label?: String, disabled?: Boolean, onChange?: ($: BlockBuilder, checked: BooleanExpr) => void }` |
| `SliderStyle` | `{ min: Float, max: Float, step?: Float, disabled?: Boolean, onChange?: ($: BlockBuilder, value: ArrayExpr<FloatType>) => void }` |
| `FieldStyle` | `{ label?: String, helperText?: String, errorText?: String, required?: Boolean, invalid?: Boolean }` |
| `FileUploadStyle` | `{ accept?: String, maxFiles?: Integer, maxFileSize?: Integer, disabled?: Boolean, onFileChange?: ($: BlockBuilder, files: ArrayExpr<FileType>) => void }` |
| `TagsInputStyle` | `{ placeholder?: String, max?: Integer, disabled?: Boolean, onChange?: ($: BlockBuilder, value: ArrayExpr<StringType>) => void }` |

---

## Display

Display components: Badge, Tag, Avatar, Icon, Stat.

**Import:**
```typescript
import { Badge, Tag, Avatar, Icon, Stat, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Badge.Root(value: String, style?: BadgeStyle): UIComponentType` | Small badge label |
| `Tag.Root(value: String, style?: TagStyle): UIComponentType` | Tag with optional close button |
| `Avatar.Root(style?: AvatarStyle): UIComponentType` | User avatar image/initials |
| `Icon.Root(name: String, style?: IconStyle): UIComponentType` | FontAwesome or custom icon |
| `Stat.Root(label: String, value: String, style?: StatStyle): UIComponentType` | Statistic with label and value |

**East Types:**

| Type | Definition |
|------|------------|
| `BadgeType` | `StructType({ value: String, variant: OptionType<StyleVariantType>, colorPalette: OptionType<ColorSchemeType>, size: OptionType<SizeType> })` |
| `TagType` | `StructType({ value: String, variant: OptionType<StyleVariantType>, colorPalette: OptionType<ColorSchemeType>, size: OptionType<SizeType>, closable: OptionType<Boolean>, onClose: OptionType<FunctionType<[], Null>> })` |
| `AvatarType` | `StructType({ name: OptionType<String>, src: OptionType<String>, size: OptionType<SizeType>, colorPalette: OptionType<ColorSchemeType> })` |
| `IconType` | `StructType({ name: String, size: OptionType<SizeType>, color: OptionType<String> })` |
| `StatType` | `StructType({ label: String, value: String, helpText: OptionType<String>, indicator: OptionType<StatIndicatorType>, colorPalette: OptionType<ColorSchemeType> })` |
| `StyleVariantType` | `VariantType({ subtle, solid, outline })` |
| `StatIndicatorType` | `VariantType({ up, down })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `BadgeStyle` | `{ variant?: StyleVariantType \| StyleVariantLiteral, colorPalette?: ColorSchemeType \| ColorSchemeLiteral, size?: SizeType \| SizeLiteral }` |
| `TagStyle` | `{ variant?: StyleVariantType \| StyleVariantLiteral, colorPalette?: ColorSchemeType \| ColorSchemeLiteral, size?: SizeType \| SizeLiteral, closable?: Boolean, onClose?: ($: BlockBuilder) => void }` |
| `AvatarStyle` | `{ name?: String, src?: String, size?: SizeType \| SizeLiteral, colorPalette?: ColorSchemeType \| ColorSchemeLiteral }` |
| `IconStyle` | `{ size?: SizeType \| SizeLiteral, color?: String }` |
| `StatStyle` | `{ helpText?: String, indicator?: StatIndicatorType \| StatIndicatorLiteral, colorPalette?: ColorSchemeType \| ColorSchemeLiteral }` |

---

## Feedback

User feedback components: Alert, Progress.

**Import:**
```typescript
import { Alert, Progress, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Alert.Root(title: String, style?: AlertStyle): UIComponentType` | Alert message (info, success, warning, error) |
| `Progress.Root(value: Float, style?: ProgressStyle): UIComponentType` | Progress bar or circular progress |

**East Types:**

| Type | Definition |
|------|------------|
| `AlertType` | `StructType({ title: String, description: OptionType<String>, status: OptionType<AlertStatusType>, variant: OptionType<AlertVariantType> })` |
| `ProgressType` | `StructType({ value: Float, max: OptionType<Float>, size: OptionType<SizeType>, colorPalette: OptionType<ColorSchemeType>, striped: OptionType<Boolean>, animated: OptionType<Boolean> })` |
| `AlertStatusType` | `VariantType({ info, success, warning, error })` |
| `AlertVariantType` | `VariantType({ subtle, solid, outline })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `AlertStyle` | `{ description?: String, status?: AlertStatusType \| AlertStatusLiteral, variant?: AlertVariantType \| AlertVariantLiteral }` |
| `ProgressStyle` | `{ max?: Float, size?: SizeType \| SizeLiteral, colorPalette?: ColorSchemeType \| ColorSchemeLiteral, striped?: Boolean, animated?: Boolean }` |

---

## Collections

Data display components: Table, DataList, TreeView, Gantt, Planner.

**Import:**
```typescript
import { Table, DataList, TreeView, Gantt, Planner, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Table.Root(data: ArrayType<RowType>, columns: ArrayType<ColumnConfig>, style?: TableStyle): UIComponentType` | Data table with columns, sorting, selection |
| `DataList.Root(items: ArrayType<DataListItemType>, style?: DataListStyle): UIComponentType` | Label-value pair list |
| `TreeView.Root(nodes: ArrayType<TreeNodeType>, style?: TreeViewStyle): UIComponentType` | Hierarchical tree with expand/collapse |
| `Gantt.Root(rows: ArrayType<GanttRowType>, columns: ArrayType<ColumnConfig>, style?: GanttStyle): UIComponentType` | Gantt chart for scheduling/timelines |
| `Planner.Root(rows: ArrayType<PlannerRowType>, columns: ArrayType<ColumnConfig>, style?: PlannerStyle): UIComponentType` | Event planner/calendar |

**East Types:**

| Type | Definition |
|------|------------|
| `TableStyleType` | `StructType({ variant: OptionType<TableVariantType>, size: OptionType<TableSizeType>, striped: OptionType<Boolean>, interactive: OptionType<Boolean>, stickyHeader: OptionType<Boolean>, showColumnBorder: OptionType<Boolean>, colorPalette: OptionType<ColorSchemeType>, onCellClick: OptionType<FunctionType<[TableCellClickEventType], Null>>, onCellDoubleClick: OptionType<FunctionType<[TableCellClickEventType], Null>>, onRowClick: OptionType<FunctionType<[TableRowClickEventType], Null>>, onRowDoubleClick: OptionType<FunctionType<[TableRowClickEventType], Null>>, onRowSelectionChange: OptionType<FunctionType<[TableRowSelectionEventType], Null>>, onSortChange: OptionType<FunctionType<[TableSortEventType], Null>> })` |
| `TableVariantType` | `VariantType({ line, outline })` |
| `TableSizeType` | `VariantType({ sm, md, lg })` |
| `TableColumnType` | `StructType({ key: String, dataType: EastTypeType, valueType: EastTypeType, header: OptionType<String>, width: OptionType<String>, minWidth: OptionType<String>, maxWidth: OptionType<String> })` |
| `TableCellClickEventType` | `StructType({ rowIndex: Integer, columnKey: String, cellValue: LiteralValueType })` |
| `TableRowClickEventType` | `StructType({ rowIndex: Integer })` |
| `TableRowSelectionEventType` | `StructType({ rowIndex: Integer, selected: Boolean, selectedRowsIndices: ArrayType<Integer> })` |
| `TableSortEventType` | `StructType({ columnKey: String, sortIndex: Integer, sortDirection: TableSortDirectionType })` |
| `TableSortDirectionType` | `VariantType({ asc, desc })` |
| `DataListRootType` | `StructType({ items: ArrayType<DataListItemType>, orientation: OptionType<OrientationType> })` |
| `DataListItemType` | `StructType({ label: String, value: String })` |
| `TreeNodeType` | `RecursiveType(inner => VariantType({ Item: StructType({ value: String, label: String, indicator: OptionType<IconType> }), Branch: StructType({ value: String, label: String, indicator: OptionType<IconType>, children: ArrayType<inner>, disabled: OptionType<Boolean> }) }))` |
| `TreeViewStyleType` | `StructType({ size: OptionType<SizeType>, selectionMode: OptionType<SelectionModeType> })` |
| `SelectionModeType` | `VariantType({ single, multiple })` |
| `GanttEventType` | `StructType({ id: String, start: DateTime, end: DateTime, label: OptionType<String>, colorPalette: OptionType<ColorSchemeType> })` |
| `GanttStyleType` | `StructType({ variant: OptionType<TableVariantType>, size: OptionType<TableSizeType>, showColumnBorder: OptionType<Boolean>, timelineStart: OptionType<DateTime>, timelineEnd: OptionType<DateTime> })` |
| `PlannerEventType` | `StructType({ id: String, start: DateTime, end: DateTime, label: OptionType<String>, colorPalette: OptionType<ColorSchemeType> })` |
| `PlannerStyleType` | `StructType({ variant: OptionType<TableVariantType>, size: OptionType<TableSizeType>, showColumnBorder: OptionType<Boolean> })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `TableStyle` | `{ variant?: TableVariantType \| TableVariantLiteral, size?: TableSizeType \| TableSizeLiteral, striped?: Boolean, interactive?: Boolean, stickyHeader?: Boolean, showColumnBorder?: Boolean, colorPalette?: ColorSchemeType \| ColorSchemeLiteral, onCellClick?: ($: BlockBuilder, event: TableCellClickEventExpr) => void, onRowClick?: ($: BlockBuilder, event: TableRowClickEventExpr) => void, onRowSelectionChange?: ($: BlockBuilder, event: TableRowSelectionEventExpr) => void, onSortChange?: ($: BlockBuilder, event: TableSortEventExpr) => void }` |
| `DataListStyle` | `{ orientation?: OrientationType \| OrientationLiteral }` |
| `TreeViewStyle` | `{ size?: SizeType \| SizeLiteral, selectionMode?: SelectionModeType \| SelectionModeLiteral, defaultExpandedValue?: ArrayType<String>, defaultSelectedValue?: ArrayType<String> }` |
| `GanttStyle` | `{ variant?: TableVariantType \| TableVariantLiteral, size?: TableSizeType \| TableSizeLiteral, showColumnBorder?: Boolean, timelineStart?: DateTime, timelineEnd?: DateTime }` |
| `PlannerStyle` | `{ variant?: TableVariantType \| TableVariantLiteral, size?: TableSizeType \| TableSizeLiteral, showColumnBorder?: Boolean }` |

---

## Charts

Data visualization components: Chart.Line, Chart.Bar, Chart.Area, Chart.Scatter, Chart.Pie, Chart.Radar, Chart.BarList, Chart.BarSegment, Sparkline.

**Import:**
```typescript
import { Chart, Sparkline, TickFormat, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Chart.Line(data: ArrayType<DataPointType>, series: DictType<String, ChartSeriesType>, style?: LineChartStyle): UIComponentType` | Line chart (single/multi series) |
| `Chart.LineMulti(data: DictType<String, ArrayType<DataPointType>>, series: DictType<String, ChartSeriesType>, style?: LineChartStyle): UIComponentType` | Multi-series line chart with separate data |
| `Chart.Bar(data: ArrayType<DataPointType>, series: DictType<String, ChartSeriesType>, style?: BarChartStyle): UIComponentType` | Bar chart (single/multi series) |
| `Chart.BarMulti(data: DictType<String, ArrayType<DataPointType>>, series: DictType<String, ChartSeriesType>, style?: BarChartStyle): UIComponentType` | Multi-series bar chart with separate data |
| `Chart.Area(data: ArrayType<DataPointType>, series: DictType<String, ChartSeriesType>, style?: AreaChartStyle): UIComponentType` | Area chart (single/multi series) |
| `Chart.AreaMulti(data: DictType<String, ArrayType<DataPointType>>, series: DictType<String, ChartSeriesType>, style?: AreaChartStyle): UIComponentType` | Multi-series area chart with separate data |
| `Chart.Scatter(data: ArrayType<DataPointType>, series: DictType<String, ChartSeriesType>, style?: ScatterChartStyle): UIComponentType` | Scatter plot (single/multi series) |
| `Chart.ScatterMulti(data: DictType<String, ArrayType<DataPointType>>, series: DictType<String, ChartSeriesType>, style?: ScatterChartStyle): UIComponentType` | Multi-series scatter plot with separate data |
| `Chart.Pie(data: ArrayType<PieDataPointType>, style?: PieChartStyle): UIComponentType` | Pie/donut chart |
| `Chart.Radar(data: ArrayType<DataPointType>, series: DictType<String, ChartSeriesType>, style?: RadarChartStyle): UIComponentType` | Radar/spider chart |
| `Chart.BarList(data: ArrayType<BarListDataPointType>, style?: BarListStyle): UIComponentType` | Horizontal bar list |
| `Chart.BarSegment(data: ArrayType<BarSegmentDataPointType>, style?: BarSegmentStyle): UIComponentType` | Segmented bar |
| `Sparkline.Root(data: ArrayType<Float>, style?: SparklineStyle): UIComponentType` | Inline trend visualization |
| `TickFormat.Number(options?: NumberFormat): TickFormatType` | Number tick format |
| `TickFormat.Currency(options: CurrencyFormat): TickFormatType` | Currency tick format |
| `TickFormat.Percent(options?: PercentFormat): TickFormatType` | Percent tick format |
| `TickFormat.Compact(options?: CompactFormat): TickFormatType` | Compact notation (1K, 1M) |
| `TickFormat.Unit(options: UnitFormat): TickFormatType` | Unit format (gigabyte, kilometer) |
| `TickFormat.Date(options?: DateFormat): TickFormatType` | Date format |
| `TickFormat.Time(options?: TimeFormat): TickFormatType` | Time format |
| `TickFormat.DateTime(options?: DateTimeFormat): TickFormatType` | Combined date/time format |

**East Types:**

| Type | Definition |
|------|------------|
| `ChartSeriesType` | `StructType({ name: String, color: OptionType<String>, stackId: OptionType<String>, label: OptionType<String>, stroke: OptionType<String>, strokeWidth: OptionType<Integer>, fill: OptionType<String>, fillOpacity: OptionType<Float>, strokeDasharray: OptionType<String> })` |
| `ChartAxisType` | `StructType({ dataKey: OptionType<String>, label: OptionType<String>, tickFormat: OptionType<TickFormatType>, domain: OptionType<ArrayType<Float>>, hide: OptionType<Boolean>, axisLine: OptionType<Boolean>, tickLine: OptionType<Boolean>, tickMargin: OptionType<Integer>, strokeColor: OptionType<String>, orientation: OptionType<AxisOrientationType>, axisId: OptionType<String> })` |
| `ChartGridType` | `StructType({ show: OptionType<Boolean>, vertical: OptionType<Boolean>, horizontal: OptionType<Boolean>, strokeColor: OptionType<String>, strokeDasharray: OptionType<String> })` |
| `ChartLegendType` | `StructType({ show: OptionType<Boolean>, layout: OptionType<LegendLayoutType>, align: OptionType<LegendAlignType>, verticalAlign: OptionType<LegendVerticalAlignType> })` |
| `ChartTooltipType` | `StructType({ show: OptionType<Boolean>, cursor: OptionType<TooltipCursorType>, animationDuration: OptionType<Integer> })` |
| `ChartMarginType` | `StructType({ top: OptionType<Integer>, right: OptionType<Integer>, bottom: OptionType<Integer>, left: OptionType<Integer> })` |
| `TickFormatType` | `VariantType({ number: NumberFormatType, currency: CurrencyFormatType, percent: PercentFormatType, compact: CompactFormatType, unit: UnitFormatType, scientific: Null, engineering: Null, date: DateFormatType, time: TimeFormatType, datetime: DateTimeFormatType })` |
| `NumberFormatType` | `StructType({ minimumFractionDigits: OptionType<Integer>, maximumFractionDigits: OptionType<Integer>, signDisplay: OptionType<SignDisplayType> })` |
| `CurrencyFormatType` | `StructType({ currency: CurrencyCodeType, display: OptionType<CurrencyDisplayType>, minimumFractionDigits: OptionType<Integer>, maximumFractionDigits: OptionType<Integer> })` |
| `PercentFormatType` | `StructType({ minimumFractionDigits: OptionType<Integer>, maximumFractionDigits: OptionType<Integer>, signDisplay: OptionType<SignDisplayType> })` |
| `CompactFormatType` | `StructType({ display: OptionType<CompactDisplayType> })` |
| `UnitFormatType` | `StructType({ unit: UnitType, display: OptionType<UnitDisplayType> })` |
| `DateFormatType` | `StructType({ style: OptionType<DateTimeStyleType> })` |
| `TimeFormatType` | `StructType({ style: OptionType<DateTimeStyleType>, hour12: OptionType<Boolean> })` |
| `DateTimeFormatType` | `StructType({ dateStyle: OptionType<DateTimeStyleType>, timeStyle: OptionType<DateTimeStyleType>, hour12: OptionType<Boolean> })` |
| `CurveType` | `VariantType({ linear, natural, monotone, step, stepBefore, stepAfter })` |
| `StackOffsetType` | `VariantType({ none, expand, wiggle, silhouette })` |
| `BarLayoutType` | `VariantType({ horizontal, vertical })` |
| `AxisOrientationType` | `VariantType({ top, bottom, left, right })` |
| `LegendLayoutType` | `VariantType({ horizontal, vertical })` |
| `LegendAlignType` | `VariantType({ left, center, right })` |
| `LegendVerticalAlignType` | `VariantType({ top, middle, bottom })` |
| `SignDisplayType` | `VariantType({ auto, never, always, exceptZero })` |
| `CompactDisplayType` | `VariantType({ short, long })` |
| `CurrencyDisplayType` | `VariantType({ code, symbol, narrowSymbol, name })` |
| `UnitDisplayType` | `VariantType({ short, narrow, long })` |
| `DateTimeStyleType` | `VariantType({ full, long, medium, short })` |
| `SparklineType` | `StructType({ data: ArrayType<Float>, color: OptionType<String>, height: OptionType<Integer>, showDots: OptionType<Boolean>, showArea: OptionType<Boolean> })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `LineChartStyle` | `{ xAxis?: ChartAxisConfig, yAxis?: ChartAxisConfig, grid?: ChartGridConfig, legend?: ChartLegendConfig, tooltip?: ChartTooltipConfig, margin?: ChartMarginConfig, height?: Integer, curve?: CurveType \| CurveLiteral, showDots?: Boolean }` |
| `BarChartStyle` | `{ xAxis?: ChartAxisConfig, yAxis?: ChartAxisConfig, grid?: ChartGridConfig, legend?: ChartLegendConfig, tooltip?: ChartTooltipConfig, margin?: ChartMarginConfig, height?: Integer, layout?: BarLayoutType \| BarLayoutLiteral, stackOffset?: StackOffsetType \| StackOffsetLiteral, barSize?: Integer }` |
| `AreaChartStyle` | `{ xAxis?: ChartAxisConfig, yAxis?: ChartAxisConfig, grid?: ChartGridConfig, legend?: ChartLegendConfig, tooltip?: ChartTooltipConfig, margin?: ChartMarginConfig, height?: Integer, curve?: CurveType \| CurveLiteral, stackOffset?: StackOffsetType \| StackOffsetLiteral }` |
| `ScatterChartStyle` | `{ xAxis?: ChartAxisConfig, yAxis?: ChartAxisConfig, grid?: ChartGridConfig, legend?: ChartLegendConfig, tooltip?: ChartTooltipConfig, margin?: ChartMarginConfig, height?: Integer }` |
| `PieChartStyle` | `{ legend?: ChartLegendConfig, tooltip?: ChartTooltipConfig, height?: Integer, innerRadius?: Float, outerRadius?: Float, paddingAngle?: Float, startAngle?: Float, endAngle?: Float, showLabels?: Boolean }` |
| `RadarChartStyle` | `{ legend?: ChartLegendConfig, tooltip?: ChartTooltipConfig, height?: Integer, outerRadius?: Float }` |
| `BarListStyle` | `{ height?: Integer, showValue?: Boolean, colorPalette?: ColorSchemeType \| ColorSchemeLiteral }` |
| `BarSegmentStyle` | `{ height?: Integer, showValue?: Boolean, showLabel?: Boolean }` |
| `SparklineStyle` | `{ color?: String, height?: Integer, showDots?: Boolean, showArea?: Boolean }` |
| `ChartAxisConfig` | `{ dataKey?: String, label?: String, tickFormat?: TickFormatType, domain?: ArrayType<Float>, hide?: Boolean, axisLine?: Boolean, tickLine?: Boolean, tickMargin?: Integer, strokeColor?: String, orientation?: AxisOrientationType \| AxisOrientationLiteral, axisId?: String }` |
| `ChartGridConfig` | `{ show?: Boolean, vertical?: Boolean, horizontal?: Boolean, strokeColor?: String, strokeDasharray?: String }` |
| `ChartLegendConfig` | `{ show?: Boolean, layout?: LegendLayoutType \| LegendLayoutLiteral, align?: LegendAlignType \| LegendAlignLiteral, verticalAlign?: LegendVerticalAlignType \| LegendVerticalAlignLiteral }` |
| `ChartTooltipConfig` | `{ show?: Boolean, cursor?: TooltipCursorType \| TooltipCursorLiteral, animationDuration?: Integer }` |
| `ChartMarginConfig` | `{ top?: Integer, right?: Integer, bottom?: Integer, left?: Integer }` |

---

## Disclosure

Expandable/collapsible components: Accordion, Tabs, Carousel.

**Import:**
```typescript
import { Accordion, Tabs, Carousel, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Accordion.Root(items: ArrayType<AccordionItemType>, style?: AccordionStyle): UIComponentType` | Expandable sections |
| `Tabs.Root(items: ArrayType<TabItemType>, style?: TabsStyle): UIComponentType` | Tabbed interface |
| `Carousel.Root(items: ArrayType<UIComponentType>, style?: CarouselStyle): UIComponentType` | Image/content carousel |

**East Types:**

| Type | Definition |
|------|------------|
| `AccordionItemType` | `StructType({ value: String, trigger: String, content: ArrayType<UIComponentType>, disabled: OptionType<Boolean> })` |
| `TabItemType` | `StructType({ value: String, trigger: String, content: ArrayType<UIComponentType>, disabled: OptionType<Boolean> })` |
| `AccordionStyleType` | `StructType({ collapsible: OptionType<Boolean>, multiple: OptionType<Boolean>, variant: OptionType<AccordionVariantType>, size: OptionType<SizeType>, defaultValue: OptionType<ArrayType<String>>, value: OptionType<ArrayType<String>>, onValueChange: OptionType<FunctionType<[ArrayType<String>], Null>> })` |
| `AccordionVariantType` | `VariantType({ outline, subtle, enclosed, plain })` |
| `TabsStyleType` | `StructType({ variant: OptionType<TabsVariantType>, size: OptionType<SizeType>, fitted: OptionType<Boolean>, justify: OptionType<TabsJustifyType>, orientation: OptionType<OrientationType>, onValueChange: OptionType<FunctionType<[String], Null>> })` |
| `TabsVariantType` | `VariantType({ line, enclosed, outline, plain })` |
| `TabsJustifyType` | `VariantType({ start, center, end })` |
| `CarouselStyleType` | `StructType({ slidesPerView: OptionType<Integer>, slidesPerMove: OptionType<Integer>, loop: OptionType<Boolean>, autoplay: OptionType<Boolean>, allowMouseDrag: OptionType<Boolean>, showIndicators: OptionType<Boolean>, showControls: OptionType<Boolean> })` |
| `OrientationType` | `VariantType({ horizontal, vertical })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `AccordionStyle` | `{ collapsible?: Boolean, multiple?: Boolean, variant?: AccordionVariantType \| AccordionVariantLiteral, size?: SizeType \| SizeLiteral, defaultValue?: ArrayType<String>, value?: ArrayType<String>, onValueChange?: ($: BlockBuilder, value: ArrayExpr<StringType>) => void }` |
| `TabsStyle` | `{ variant?: TabsVariantType \| TabsVariantLiteral, size?: SizeType \| SizeLiteral, fitted?: Boolean, justify?: TabsJustifyType \| TabsJustifyLiteral, orientation?: OrientationType \| OrientationLiteral, value?: String, defaultValue?: String, onValueChange?: ($: BlockBuilder, value: StringExpr) => void }` |
| `CarouselStyle` | `{ slidesPerView?: Integer, slidesPerMove?: Integer, loop?: Boolean, autoplay?: Boolean, allowMouseDrag?: Boolean, showIndicators?: Boolean, showControls?: Boolean, index?: Integer, defaultIndex?: Integer }` |

---

## Overlays

Floating content components: Dialog, Drawer, Popover, Tooltip, Menu, HoverCard, ActionBar, ToggleTip.

**Import:**
```typescript
import { Dialog, Drawer, Popover, Tooltip, Menu, HoverCard, ActionBar, ToggleTip, UIComponentType } from "@elaraai/east-ui";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `Dialog.Root(config: DialogConfig): UIComponentType` | Modal dialog with trigger, body, title, footer |
| `Drawer.Root(config: DrawerConfig): UIComponentType` | Side drawer panel |
| `Popover.Root(config: PopoverConfig): UIComponentType` | Positioned popover |
| `Tooltip.Root(trigger: UIComponentType, content: String, style?: TooltipStyle): UIComponentType` | Hover tooltip |
| `Menu.Root(trigger: UIComponentType, items: ArrayType<MenuItemType>, style?: MenuStyle): UIComponentType` | Context/dropdown menu |
| `HoverCard.Root(config: HoverCardConfig): UIComponentType` | Hover-triggered card |
| `ActionBar.Root(items: ArrayType<ActionBarItemType>, style?: ActionBarStyle): UIComponentType` | Bottom action bar |
| `ToggleTip.Root(trigger: UIComponentType, content: String, style?: ToggleTipStyle): UIComponentType` | Toggle-triggered tooltip |

**East Types:**

| Type | Definition |
|------|------------|
| `DialogStyleType` | `StructType({ size: OptionType<DialogSizeType>, placement: OptionType<DialogPlacementType>, scrollBehavior: OptionType<DialogScrollBehaviorType>, motionPreset: OptionType<DialogMotionPresetType>, role: OptionType<DialogRoleType>, onOpenChange: OptionType<FunctionType<[Boolean], Null>>, onExitComplete: OptionType<FunctionType<[], Null>>, onEscapeKeyDown: OptionType<FunctionType<[], Null>>, onInteractOutside: OptionType<FunctionType<[], Null>> })` |
| `DialogSizeType` | `VariantType({ xs, sm, md, lg, xl, cover, full })` |
| `DialogPlacementType` | `VariantType({ center, top, bottom })` |
| `DialogScrollBehaviorType` | `VariantType({ inside, outside })` |
| `DialogMotionPresetType` | `VariantType({ scale, "slide-in-bottom", "slide-in-top", "slide-in-left", "slide-in-right", none })` |
| `DialogRoleType` | `VariantType({ dialog, alertdialog })` |
| `DrawerStyleType` | `StructType({ size: OptionType<DialogSizeType>, placement: OptionType<DrawerPlacementType>, onOpenChange: OptionType<FunctionType<[Boolean], Null>>, onExitComplete: OptionType<FunctionType<[], Null>> })` |
| `DrawerPlacementType` | `VariantType({ start, end, top, bottom })` |
| `PopoverStyleType` | `StructType({ placement: OptionType<PlacementType>, autoFocus: OptionType<Boolean>, modal: OptionType<Boolean>, onOpenChange: OptionType<FunctionType<[Boolean], Null>> })` |
| `HoverCardStyleType` | `StructType({ placement: OptionType<PlacementType>, openDelay: OptionType<Integer>, closeDelay: OptionType<Integer> })` |
| `ActionBarStyleType` | `StructType({ open: OptionType<Boolean>, closeOnSelect: OptionType<Boolean> })` |
| `ActionBarItemType` | `StructType({ value: String, label: String, icon: OptionType<String>, onClick: OptionType<FunctionType<[], Null>> })` |
| `ToggleTipStyleType` | `StructType({ placement: OptionType<PlacementType> })` |
| `PlacementType` | `VariantType({ top, "top-start", "top-end", bottom, "bottom-start", "bottom-end", left, "left-start", "left-end", right, "right-start", "right-end" })` |
| `MenuItemType` | `VariantType({ item: StructType({ value: String, label: String, icon: OptionType<String>, disabled: OptionType<Boolean>, onClick: OptionType<FunctionType<[], Null>> }), separator: Null, group: StructType({ label: String, items: ArrayType<MenuItemType> }) })` |

**TypeScript Interfaces (function parameters):**

| Interface | Fields |
|-----------|--------|
| `DialogConfig` | `{ trigger: UIComponentType, body: ArrayType<UIComponentType>, title?: String, description?: String, footer?: ArrayType<UIComponentType>, style?: DialogStyle }` |
| `DialogStyle` | `{ size?: DialogSizeType \| DialogSizeLiteral, placement?: DialogPlacementType \| DialogPlacementLiteral, scrollBehavior?: DialogScrollBehaviorType \| DialogScrollBehaviorLiteral, motionPreset?: DialogMotionPresetType \| DialogMotionPresetLiteral, role?: DialogRoleType \| DialogRoleLiteral, onOpenChange?: ($: BlockBuilder, open: BooleanExpr) => void, onExitComplete?: ($: BlockBuilder) => void, onEscapeKeyDown?: ($: BlockBuilder) => void, onInteractOutside?: ($: BlockBuilder) => void }` |
| `DrawerConfig` | `{ trigger: UIComponentType, body: ArrayType<UIComponentType>, title?: String, description?: String, style?: DrawerStyle }` |
| `DrawerStyle` | `{ size?: DialogSizeType \| DialogSizeLiteral, placement?: DrawerPlacementType \| DrawerPlacementLiteral, onOpenChange?: ($: BlockBuilder, open: BooleanExpr) => void, onExitComplete?: ($: BlockBuilder) => void }` |
| `PopoverConfig` | `{ trigger: UIComponentType, body: ArrayType<UIComponentType>, title?: String, description?: String, style?: PopoverStyle }` |
| `PopoverStyle` | `{ placement?: PlacementType \| PlacementLiteral, autoFocus?: Boolean, modal?: Boolean, onOpenChange?: ($: BlockBuilder, open: BooleanExpr) => void }` |
| `TooltipStyle` | `{ placement?: PlacementType \| PlacementLiteral, hasArrow?: Boolean }` |
| `MenuStyle` | `{ placement?: PlacementType \| PlacementLiteral }` |
| `HoverCardConfig` | `{ trigger: UIComponentType, body: ArrayType<UIComponentType>, style?: HoverCardStyle }` |
| `HoverCardStyle` | `{ placement?: PlacementType \| PlacementLiteral, openDelay?: Integer, closeDelay?: Integer }` |
| `ActionBarStyle` | `{ open?: Boolean, closeOnSelect?: Boolean, selectionCount?: Integer, selectionLabel?: String }` |
| `ToggleTipStyle` | `{ placement?: PlacementType \| PlacementLiteral }` |

---

## State

Reactive state management for UI components.

**Import:**
```typescript
import { State } from "@elaraai/east-ui";
import { IntegerType, StringType, variant } from "@elaraai/east";
```

**Functions:**

| Signature | Description |
|-----------|-------------|
| `State.readTyped(key: String, type: EastType)(): OptionType<T>` | Read typed state value |
| `State.writeTyped(key: String, option: OptionType<T>, type: EastType)(): Null` | Write typed state value |
| `State.initTyped(key: String, value: T, type: EastType)(): Null` | Initialize state if not exists |
| `State.has(key: String)(): Boolean` | Check if state key exists |

**Usage Pattern:**
```typescript
import { East, IntegerType, variant } from "@elaraai/east";
import { Stack, Text, Button, State, UIComponentType } from "@elaraai/east-ui";

const counter = East.function([], UIComponentType, $ => {
    // Initialize state
    $(State.initTyped("count", 0n, IntegerType)());

    // Read state
    const count = $.let($(State.readTyped("count", IntegerType)()));

    return Stack.VStack([
        Text.Root(East.str`Count: ${count.unwrap("some")}`),
        Button.Root("Increment", {
            onClick: (_$) => {
                // Write state
                $(_$.exec(State.writeTyped("count", variant("some", count.unwrap("some").add(1n)), IntegerType)()));
            },
        }),
    ], { gap: "4" });
});
```

---

## Style Types

Common style types used across components.

**Import:**
```typescript
import { SizeType, ColorSchemeType, FontWeightType, FlexDirectionType } from "@elaraai/east-ui";
```

**Types:**

| Type | Definition |
|------|------------|
| `SizeType` | `VariantType({ xs, sm, md, lg })` |
| `ColorSchemeType` | `VariantType({ gray, red, orange, yellow, green, teal, blue, cyan, purple, pink })` |
| `FontWeightType` | `VariantType({ normal, bold, semibold, medium, light })` |
| `FontStyleType` | `VariantType({ normal, italic })` |
| `TextAlignType` | `VariantType({ left, center, right, justify })` |
| `TextTransformType` | `VariantType({ uppercase, lowercase, capitalize, none })` |
| `FlexDirectionType` | `VariantType({ row, column, "row-reverse", "column-reverse" })` |
| `JustifyContentType` | `VariantType({ "flex-start", "flex-end", center, "space-between", "space-around", "space-evenly" })` |
| `AlignItemsType` | `VariantType({ "flex-start", "flex-end", center, baseline, stretch })` |
| `FlexWrapType` | `VariantType({ nowrap, wrap, "wrap-reverse" })` |
| `DisplayType` | `VariantType({ block, inline, "inline-block", flex, "inline-flex", grid, "inline-grid", none })` |
| `OverflowType` | `VariantType({ visible, hidden, scroll, auto })` |
| `OrientationType` | `VariantType({ horizontal, vertical })` |
| `BorderWidthType` | `VariantType({ none, thin, medium, thick })` |
| `BorderStyleType` | `VariantType({ solid, dashed, dotted, double, none })` |
| `StyleVariantType` | `VariantType({ subtle, solid, outline })` |

---

## UIComponentType

The recursive type representing any UI component.

**Import:**
```typescript
import { UIComponentType } from "@elaraai/east-ui";
```

**Type:**
```typescript
UIComponentType = RecursiveType(node => VariantType({
    // Typography
    Text: TextType,
    Code: CodeType,
    Heading: HeadingType,
    Link: LinkType,
    Highlight: HighlightType,
    Mark: MarkType,
    List: ListType,
    CodeBlock: CodeBlockType,

    // Buttons
    Button: ButtonType,
    IconButton: IconButtonType,

    // Layout
    Box: StructType({ children: ArrayType<node>, style: OptionType<BoxStyleType> }),
    Flex: StructType({ children: ArrayType<node>, style: OptionType<FlexStyleType> }),
    Stack: StructType({ children: ArrayType<node>, style: OptionType<StackStyleType> }),
    Separator: SeparatorStyleType,
    Grid: StructType({ items: ArrayType<GridItemType>, style: OptionType<GridStyleType> }),
    Splitter: StructType({ panels: ArrayType<SplitterPanelType>, defaultSize: ArrayType<Float>, style: OptionType<SplitterStyleType> }),

    // Forms
    StringInput: StringInputType,
    IntegerInput: IntegerInputType,
    FloatInput: FloatInputType,
    DateTimeInput: DateTimeInputType,
    Checkbox: CheckboxType,
    Switch: SwitchType,
    Select: SelectRootType,
    Slider: SliderType,
    FileUpload: FileUploadType,
    Field: FieldType,
    Textarea: TextareaType,
    TagsInput: TagsInputRootType,

    // Feedback
    Progress: ProgressType,
    Alert: AlertType,

    // Display
    Badge: BadgeType,
    Tag: TagType,
    Avatar: AvatarType,
    Stat: StatType,
    Icon: IconType,

    // Container
    Card: StructType({ header: OptionType<node>, body: ArrayType<node>, footer: OptionType<node>, style: OptionType<CardStyleType> }),
    DataList: DataListRootType,

    // Charts
    Sparkline: SparklineType,
    AreaChart: AreaChartType,
    BarChart: BarChartType,
    LineChart: LineChartType,
    ScatterChart: ScatterChartType,
    PieChart: PieChartType,
    RadarChart: RadarChartType,
    BarList: BarListType,
    BarSegment: BarSegmentType,

    // Collections
    TreeView: StructType({ nodes: ArrayType<TreeNodeType>, label: OptionType<String>, style: OptionType<TreeViewStyleType> }),
    Table: StructType({ rows: ArrayType<TableRowType>, columns: ArrayType<TableColumnType>, style: OptionType<TableStyleType> }),
    Gantt: StructType({ rows: ArrayType<GanttRowType>, columns: ArrayType<TableColumnType>, style: OptionType<GanttStyleType> }),
    Planner: StructType({ rows: ArrayType<PlannerRowType>, columns: ArrayType<TableColumnType>, style: OptionType<PlannerStyleType> }),

    // Disclosure
    Accordion: StructType({ items: ArrayType<AccordionItemType>, style: OptionType<AccordionStyleType> }),
    Carousel: StructType({ items: ArrayType<node>, style: OptionType<CarouselStyleType> }),
    Tabs: StructType({ items: ArrayType<TabItemType>, value: OptionType<String>, defaultValue: OptionType<String>, style: OptionType<TabsStyleType> }),

    // Overlays
    Tooltip: StructType({ trigger: node, content: String, placement: OptionType<PlacementType>, hasArrow: OptionType<Boolean> }),
    Menu: StructType({ trigger: node, items: ArrayType<MenuItemType>, placement: OptionType<PlacementType> }),
    Dialog: StructType({ trigger: node, body: ArrayType<node>, title: OptionType<String>, description: OptionType<String>, style: OptionType<DialogStyleType> }),
    Drawer: StructType({ trigger: node, body: ArrayType<node>, title: OptionType<String>, description: OptionType<String>, style: OptionType<DrawerStyleType> }),
    Popover: StructType({ trigger: node, body: ArrayType<node>, title: OptionType<String>, description: OptionType<String>, style: OptionType<PopoverStyleType> }),
    HoverCard: StructType({ trigger: node, body: ArrayType<node>, style: OptionType<HoverCardStyleType> }),
    ActionBar: StructType({ items: ArrayType<ActionBarItemType>, selectionCount: OptionType<Integer>, selectionLabel: OptionType<String>, style: OptionType<ActionBarStyleType> }),
    ToggleTip: StructType({ trigger: node, content: String, style: OptionType<ToggleTipStyleType> }),

    // Reactive
    ReactiveComponent: StructType({ render: FunctionType<[], node> }),
}))
```
