# East UI

East UI is a UI component library for the East language.

## Purpose

East UI provides typed UI component definitions that return data structures describing UI layouts rather than rendering directly. This separation allows:

- **Portability**: UI definitions can be serialized and rendered in any environment
- **Type Safety**: Full compile-time checking of component structure and styling
- **Composability**: Components are just East functions that return typed values
- **Separation of Concerns**: UI logic (East UI) separate from rendering (renderers)

## Design

UI components in East UI return variant types that **describe** the UI structure. Rendering is deferred to a separate layer.

Components are built on East's type system:
- Base styling enums are East variant types (FontWeight, TextAlign, etc.)
- All style properties accept East expressions for dynamic styling
- Components return structs/variants that can be serialized as East IR
- Compatible with Chakra UI for rendering in React applications

## Structure

East UI is a TypeScript package that depends on the East language package.

```
src/
  index.ts              # Main exports
  style.ts              # Common style types (FontWeight, TextAlign, Size, ColorScheme, etc.)
  component.ts          # UIComponentType recursive type definition

  buttons/
    index.ts            # Buttons category exports
    button/
      index.ts          # Button component
      types.ts          # ButtonType, ButtonStyleType definitions

  collections/
    index.ts            # Collections category exports
    data-list/
      index.ts          # DataList component
      types.ts          # DataListRootType, DataListItemType definitions

  container/
    index.ts            # Container category exports
    card/
      index.ts          # Card component (container with children)
      types.ts          # CardStyleType, CardVariantType definitions

  disclosure/
    index.ts            # Disclosure category exports
    accordion/
      index.ts          # Accordion component (container with children)
      types.ts          # AccordionStyleType, AccordionVariantType definitions

  display/
    index.ts            # Display category exports
    avatar/
      index.ts          # Avatar component
      types.ts          # AvatarType definitions
    badge/
      index.ts          # Badge component
      types.ts          # BadgeType, BadgeVariantType definitions
    stat/
      index.ts          # Stat component
      types.ts          # StatType, StatIndicatorType definitions
    tag/
      index.ts          # Tag component
      types.ts          # TagType definitions

  feedback/
    index.ts            # Feedback category exports
    alert/
      index.ts          # Alert component
      types.ts          # AlertType, AlertStatusType definitions
    progress/
      index.ts          # Progress component
      types.ts          # ProgressType definitions

  forms/
    index.ts            # Forms category exports
    checkbox/
      index.ts          # Checkbox component
      types.ts          # CheckboxType definitions
    input/
      index.ts          # Input component (String, Integer, Float, DateTime)
      types.ts          # StringInputType, IntegerInputType, etc. definitions
    select/
      index.ts          # Select component
      types.ts          # SelectRootType, SelectItemType definitions
    slider/
      index.ts          # Slider component
      types.ts          # SliderType definitions
    switch/
      index.ts          # Switch component
      types.ts          # SwitchType definitions

  layout/
    index.ts            # Layout category exports
    box/
      index.ts          # Box component (container with children)
      types.ts          # BoxStyleType definitions
    grid/
      index.ts          # Grid component (container with children)
      types.ts          # GridStyleType, GridAutoFlowType definitions
    separator/
      index.ts          # Separator component
      types.ts          # SeparatorStyleType definitions
    splitter/
      index.ts          # Splitter component (container with children)
      types.ts          # SplitterStyleType definitions
    stack/
      index.ts          # Stack, HStack, VStack components (container with children)
      types.ts          # StackStyleType definitions

  typography/
    index.ts            # Typography category exports
    text/
      index.ts          # Text component
      types.ts          # TextType definitions

test/
  platforms.spec.ts     # Test infrastructure
  component.spec.ts     # Tests for UIComponentType and complex compositions
  buttons/              # Button component tests
  collections/          # Collections component tests (DataList)
  container/            # Container component tests (Card)
  disclosure/           # Disclosure component tests (Accordion)
  display/              # Display component tests (Avatar, Badge, Stat, Tag)
  feedback/             # Feedback component tests
  forms/                # Forms component tests
  layout/               # Layout component tests
  typography/           # Typography component tests
```

- `/docs/DESIGN.md` - comprehensive design document with component specifications
- `/docs/CHAKRA_CHARTS_REFERENCE.md` - Chakra UI v3 charts API reference

## Development

When making changes to the East UI codebase always run:

- `npm run build` - compile TypeScript to JavaScript
- `npm run test` - run the test suite (runs the compiled .js - requires build first)
- `npm run lint` - check code quality with ESLint (must pass before committing)

ESLint is configured to be compiler-friendly: `any` types are allowed due to type erasure needs and TypeScript's recursive type limitations.
Avoid `any` as much as possible.

Our development roadmap is found in `/docs/DESIGN.md`.

## Standards

**All development MUST follow the mandatory standards defined in [STANDARDS.md](./STANDARDS.md).**

STANDARDS.md contains comprehensive requirements for:
- TypeDoc documentation (platform functions, grouped exports, types)
- Testing with East code (using `describeEast` and `Test`)
- Code quality and compliance


## Component Architecture

### Component Export Pattern

Each component follows a consistent export pattern. Components are organized into subdirectories with separate files for the component logic and type definitions.

#### File Structure

```
src/category/component-name/
  index.ts    # Component logic, factory functions, namespace export
  types.ts    # East types (ComponentType, ComponentStyleType) - NO import from component.ts
```

**Important:** `types.ts` must NOT import from `component.ts` to avoid circular dependencies.
The types in `types.ts` are imported by `component.ts`, so any reverse import creates a cycle.
The `index.ts` file CAN import from `component.ts` because it only uses `UIComponentType` in function bodies (runtime), not at module load time.

#### Container vs Leaf Components

Components fall into two categories:

**Leaf Components** (no UI children): Badge, Tag, Avatar, Stat, Text, Button, Progress, Alert, inputs, etc.
- Their main type (e.g., `BadgeType`) is defined in `types.ts`
- `component.ts` imports the type directly: `Badge: BadgeType`

**Container Components** (have UI children): Box, Stack, Card, Grid, Splitter, Accordion
- Their main type is defined **inline** in `component.ts` using `node` for recursion
- Only style types go in `types.ts` (e.g., `CardStyleType`, `BoxStyleType`)
- This is required because children need `ArrayType(node)` which only exists inside `RecursiveType`

Example in `component.ts`:
```typescript
export const UIComponentType = RecursiveType(node => VariantType({
    // Leaf - import type directly
    Badge: BadgeType,

    // Container - define inline with node
    Card: StructType({
        title: OptionType(StringType),
        description: OptionType(StringType),
        body: ArrayType(node),  // Children are UIComponents
        style: OptionType(CardStyleType),  // Style type from types.ts
    }),

    Accordion: StructType({
        items: ArrayType(StructType({
            value: StringType,
            trigger: StringType,
            content: ArrayType(node),  // Children are UIComponents
            disabled: OptionType(BooleanType),
        })),
        style: OptionType(AccordionStyleType),
    }),
}));
```

#### types.ts Pattern

The types file exports:
1. East StructTypes/VariantTypes for component data and styling
2. TypeScript interfaces for style options (accepts `SubtypeExprOrValue<T>`)
3. Helper functions for creating variant values (optional)

```typescript
// types.ts - NO import from component.ts!
import { type SubtypeExprOrValue, OptionType, StringType, StructType, VariantType, NullType } from "@elaraai/east";
import { FlexDirectionType, AlignItemsType } from "../../style.js";

/**
 * Variant type for component visual style.
 *
 * @property solid - Solid filled variant
 * @property outline - Outlined variant with border
 * @property subtle - Subtle/light background variant
 */
export const ComponentVariantType = VariantType({
    solid: NullType,
    outline: NullType,
    subtle: NullType,
});
export type ComponentVariantType = typeof ComponentVariantType;

/**
 * East StructType for serialized style data.
 *
 * @property direction - Flex direction for layout
 * @property gap - Gap between items (Chakra spacing token)
 * @property align - Cross-axis alignment of items
 * @property variant - Visual style variant
 */
export const ComponentStyleType = StructType({
    direction: OptionType(FlexDirectionType),
    gap: OptionType(StringType),
    align: OptionType(AlignItemsType),
    variant: OptionType(ComponentVariantType),
});
export type ComponentStyleType = typeof ComponentStyleType;

/**
 * TypeScript interface for Component style options.
 *
 * @property direction - Flex direction for layout
 * @property gap - Gap between items (Chakra spacing token)
 * @property align - Cross-axis alignment of items
 * @property variant - Visual style variant
 */
export interface ComponentStyle {
    /** Flex direction for layout */
    direction?: SubtypeExprOrValue<FlexDirectionType>;
    /** Gap between items (Chakra spacing token) */
    gap?: SubtypeExprOrValue<StringType>;
    /** Cross-axis alignment of items */
    align?: SubtypeExprOrValue<AlignItemsType>;
    /** Visual style variant (solid, outline, subtle) */
    variant?: SubtypeExprOrValue<ComponentVariantType> | "solid" | "outline" | "subtle";
}
```

#### index.ts Pattern

The index file contains:
1. Imports from `types.ts` (and re-exports them)
2. A private factory function (can import `UIComponentType` from `component.ts`)
3. A public namespace object with `Root`, optional sub-factories, and `Types`
4. Optional convenience exports for commonly used sub-components (e.g., `HStack`, `VStack`)

```typescript
// index.ts
import {
    type ExprType,
    East,
    ArrayType,
    variant,
    type SubtypeExprOrValue,
} from "@elaraai/east";

import { UIComponentType } from "../../component.js";  // OK - only used in function body
import { ComponentStyleType, type ComponentStyle } from "./types.js";

// Re-export types
export { ComponentStyleType, type ComponentStyle } from "./types.js";

// For container components, define ComponentType locally (needs UIComponentType)
export const ComponentType = StructType({
    children: ArrayType(UIComponentType),
    style: OptionType(ComponentStyleType),
});
export type ComponentType = typeof ComponentType;

// Private factory function
function createComponent(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: ComponentStyle
): ExprType<UIComponentType> {
    // Convert string literals to East values
    const variantValue = style?.variant
        ? (typeof style.variant === "string"
            ? East.value(variant(style.variant, null), ComponentVariantType)
            : style.variant)
        : undefined;

    return East.value(variant("Component", {
        children: children,
        style: style ? variant("some", East.value({
            variant: variantValue ? variant("some", variantValue) : variant("none", null),
            gap: style.gap ? variant("some", style.gap) : variant("none", null),
        }, ComponentStyleType)) : variant("none", null),
    }), UIComponentType);
}

// Public namespace export
export const Component = {
    Root: createComponent,
    Item: createComponentItem,  // Sub-component factory for compound components
    Variant: ComponentVariant,  // Optional helper for creating variant values
    Types: {
        Component: ComponentType,
        Item: ComponentItemType,
        Style: ComponentStyleType,
        Variant: ComponentVariantType,
    },
} as const;
```

**Compound Component Pattern:**

For components with sub-components (like Accordion, Select, Grid), all factories are in the namespace:

```typescript
// Accordion example
export const Accordion = {
    Root: createAccordionRoot,
    Item: createAccordionItem,  // Accordion.Item(value, trigger, children, style?)
    Variant: AccordionVariant,
    Types: {
        Root: AccordionRootType,
        Item: AccordionItemType,
        Style: AccordionStyleType,
        Variant: AccordionVariantType,
    },
} as const;

// Usage:
Accordion.Root([
    Accordion.Item("section-1", "Section 1", [
        Text.Root("Content for section 1"),
    ]),
    Accordion.Item("section-2", "Section 2", [
        Text.Root("Content for section 2"),
    ]),
], {
    variant: "enclosed",
    collapsible: true,
});
```

#### Category Index Pattern

Category index files (e.g., `display/index.ts`) export namespace objects and re-export types:

```typescript
// display/index.ts
export { Badge } from "./badge/index.js";
export { Tag } from "./tag/index.js";
export { Avatar } from "./avatar/index.js";
export { Stat } from "./stat/index.js";
```

Users access types through the namespace:
```typescript
Badge.Types.Badge    // East type
Badge.Root(...)      // Factory function
```

#### Namespace Structure

All components export a namespace object with:

| Property | Description |
|----------|-------------|
| `Root` | Main factory function to create the component |
| `Types` | Object containing East types for the component |
| `Types.Component` | The East StructType for the component data |
| `Types.Style` | The East StructType for the component style (if applicable) |

Additional factory functions may be added for compound components:
- `Stack.HStack` / `Stack.VStack` - Direction-specific stack variants
- `Grid.Item` - Grid item factory
- `DataList.Item` - Data list item factory

#### Usage Pattern

```typescript
import { Stack, Text } from "@elaraai/east-ui";

// Create component using .Root()
const stack = Stack.Root([
    Text.Root("Hello"),
    Text.Root("World"),
], {
    gap: "4",
    direction: "row",
});

// Access East types via .Types
const stackType = Stack.Types.Stack;
const styleType = Stack.Types.Style;
```

### Base Variant Types (`src/style.ts`)

Base styling variants are reusable across all UI components:

**Font Styling:**
- `FontWeight` - normal, bold, semibold, medium, light
- `FontStyle` - normal, italic

**Text Alignment:**
- `TextAlign` - left, center, right, justify
- `VerticalAlign` - top, middle, bottom, baseline

**Text Behavior:**
- `TextOverflow` - clip, ellipsis
- `WhiteSpace` - normal, nowrap, pre, pre_wrap
- `WordBreak` - normal, break_word, break_all

**Table-Specific:**
- `TableVariant` - simple, striped, unstyled
- `TableSize` - sm, md, lg
- `ColorScheme` - gray, red, orange, yellow, green, teal, blue, cyan, purple, pink
- `TextTransform` - uppercase, lowercase, capitalize, none

All variants are created using East's `variant` function:
```typescript
const bold = variant("bold", null);
const center = variant("center", null);
```

### Table Components (`src/table/`)

**Table.Cell** - Creates a cell variant with typed value and optional styling
```typescript
Table.Cell(value, {
  color: "blue.500",
  textAlign: variant("right", null),
  fontWeight: variant("bold", null),
});
```

**Table.Row** - Creates a row struct from a record of cells with optional row styling
```typescript
Table.Row({
  name: Table.Cell(row.name),
  age: Table.Cell(row.age),
}, {
  key: row.id,
  hoverBackground: "gray.50",
});
```

**Table.Root** - Maps an array of data to an array of rows using a builder function
```typescript
Table.Root(
  data,
  ($, row) => Table.Row({...}),
  {
    variant: variant("striped", null),
    size: variant("md", null),
  }
);
```

All table components return East data structures that can be:
- Serialized to JSON as East IR
- Compiled to executable functions
- Rendered in any environment (React, HTML, etc.)

## Testing

Tests follow the East testing pattern using Node.js `test` with East values:

```typescript
import { East, StructType, StringType, IntegerType } from "@elaraai/east";
import { Table, FontWeight, TextAlign, variant } from "../src/index.js";
import { describeEast as describe, Assert as assert } from "@elaraai/east-node-std";

describe("Table", (test) => {
    test("Table.Cell creation", $ => {
        const person = $.let(East.value({ name: "Alice", age: 30n }));

        // Simple cell
        const cell = $.let(Table.Cell(person.name));
        $(assert.equal(cell.unwrap("Cell").value, "Alice"));

        // Cell with styling
        const styledCell = $.let(Table.Cell(person.age, {
            textAlign: variant("right", null),
            fontWeight: variant("bold", null),
        }));
        $(assert.equal(styledCell.unwrap("Cell").value, 30n));
        $(assert.equal(styledCell.unwrap("Cell").textAlign.unwrap("right"), null));
    });

    test("Variant type usage", $ => {
        const bold = $.let(variant("bold", null), FontWeight);
        $(assert.equal(bold.getTag(), "bold"));
        $(assert.equal(bold.hasTag("bold"), true));
        $(assert.equal(bold.hasTag("normal"), false));
    });
});
```

### Test Files Structure

```
test/
  platforms.spec.ts     # Test infrastructure (from East)
  style.spec.ts         # Tests for style types (FontWeight, TextAlign, etc.)
  component.spec.ts     # Tests for UIComponentType and complex compositions
  buttons/
    button.spec.ts      # Button component tests
  collections/
    data-list.spec.ts   # DataList component tests
  container/
    card.spec.ts        # Card component tests
  disclosure/
    accordion.spec.ts   # Accordion component tests
  display/
    avatar.spec.ts      # Avatar component tests
    badge.spec.ts       # Badge component tests
    stat.spec.ts        # Stat component tests
    tag.spec.ts         # Tag component tests
  feedback/
    alert.spec.ts       # Alert component tests
    progress.spec.ts    # Progress component tests
  forms/
    checkbox.spec.ts    # Checkbox component tests
    input.spec.ts       # Input component tests
    select.spec.ts      # Select component tests
    slider.spec.ts      # Slider component tests
    switch.spec.ts      # Switch component tests
  layout/
    box.spec.ts         # Box component tests
    grid.spec.ts        # Grid component tests
    separator.spec.ts   # Separator component tests
    splitter.spec.ts    # Splitter component tests
    stack.spec.ts       # Stack component tests
  typography/
    text.spec.ts        # Text component tests
```

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Export test IR for cross-platform testing
npm run test:export
```

Test IR can be exported and run on other East implementations to ensure compatibility.

## Type System Integration

East UI builds on East's type system:

- All components work with East's core types (Integer, String, Boolean, Struct, Variant, etc.)
- Styling enums are East variant types for type safety and pattern matching
- Style properties use `SubtypeExprOrValue<T>` to accept both static values and expressions
- Optional styles use `OptionType<T>` to handle presence/absence
- Dynamic styling uses East's conditional expressions (`ifElse`, `match`)

See [East's USAGE.md](../East/USAGE.md) for details on East's type system and expression API.

## SubtypeExprOrValue Pattern

`SubtypeExprOrValue<T>` is a key type that enables ergonomic APIs by accepting **either** plain JavaScript values **or** East expressions. This eliminates the need to wrap simple values with `East.value()`.

### Why SubtypeExprOrValue?

Without `SubtypeExprOrValue`, users would need to write:
```typescript
// Verbose - requires wrapping every value
Button.Root(East.value("Click me", StringType), {
    variant: East.value(variant("solid", null), ButtonVariantType),
    disabled: East.value(false, BooleanType),
});
```

With `SubtypeExprOrValue`, the same code becomes:
```typescript
// Ergonomic - plain values accepted directly
Button.Root("Click me", {
    variant: "solid",
    disabled: false,
});
```

### When to Use SubtypeExprOrValue

Use `SubtypeExprOrValue<T>` for function parameters that should accept both static values and dynamic expressions:

```typescript
interface ButtonStyle {
    // Accept plain strings OR East string expressions
    label?: SubtypeExprOrValue<StringType>;

    // Accept plain booleans OR East boolean expressions
    disabled?: SubtypeExprOrValue<BooleanType>;

    // Accept string literals OR East variant expressions
    variant?: SubtypeExprOrValue<ButtonVariantType> | "solid" | "subtle" | "outline";

    // Accept plain arrays OR East array expressions
    children?: SubtypeExprOrValue<ArrayType<UIComponentType>>;
}
```

### String Literal Unions for Variants

For variant types, add string literal unions to allow shorthand syntax:
```typescript
// Users can write either:
variant: "solid"           // String literal (ergonomic)
variant: variant("solid", null)  // Explicit variant (when needed)
variant: someCondition.ifElse(variant("solid", null), variant("outline", null))  // Dynamic
```

### Component Function Signatures

All component factory functions should use `SubtypeExprOrValue` for their parameters:

```typescript
// Good - accepts plain values
function createButton(
    label: SubtypeExprOrValue<StringType>,
    style?: ButtonStyle
): ExprType<UIComponentType>

// Usage:
Button.Root("Click me")                    // Plain string
Button.Root(row.name)                      // East expression
Button.Root(count.greater(0).ifElse("Active", "Inactive"))  // Conditional
```

### Arrays and Collections

`SubtypeExprOrValue` works with array types too:

```typescript
// Component accepting array of children
function createBox(
    children: SubtypeExprOrValue<ArrayType<UIComponentType>>,
    style?: BoxStyle
): ExprType<UIComponentType>

// Usage:
Box.Root([Text.Root("Hello"), Button.Root("Click")])  // Plain array
Box.Root(data.map(item => Text.Root(item.name)))      // East mapped array
```

### Testing with Plain Values

Tests should use plain values for clarity:
```typescript
// Good - clear and readable
test("creates button with label", $ => {
    const button = $.let(Button.Root("Click me"));
    $(Assert.equal(button.unwrap("Button").label, "Click me"));
});

// Avoid - unnecessarily verbose
test("creates button with label", $ => {
    const button = $.let(Button.Root(East.value("Click me", StringType)));
    // ...
});
```
