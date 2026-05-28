# East UI Development Standards

**This document is MANDATORY and MUST be followed for all East UI development.**

All contributors MUST follow these standards for documentation and testing. These standards ensure consistency, correctness, and maintainability across the East UI codebase.

---

## Table of Contents

- [TypeDoc Documentation Standards](#typedoc-documentation-standards)
  - [Component Namespace Objects](#component-namespace-objects)
  - [Factory Functions](#factory-functions)
  - [Types (StructType/VariantType)](#types-structtypevarianttype)
  - [TypeScript Interfaces](#typescript-interfaces)
  - [General Rules](#general-rules)
- [TypeDoc Example Validation](#typedoc-example-validation)
- [Testing Standards](#testing-standards)

---

## TypeDoc Documentation Standards

All public APIs MUST include TypeDoc comments following these precise rules.

### CRITICAL: Example Validation Requirement

**ALL `@example` blocks MUST:**
1. Use `East.function()` - NO inline code examples, EVER
2. Be copied to the corresponding `examples/[module].ts` file
3. Compile and execute successfully via `.toIR().compile([])()`

If an example is not validated in `examples/[module].ts`, it will break. Examples that cannot be validated MUST NOT be added.

### Gold Standard

East UI focuses on **UI Components** that return typed data structures describing UI layouts. The gold standard for documentation is the Button component:
- `/src/buttons/button/index.ts` - Component factory and namespace
- `/src/buttons/button/types.ts` - East types and TypeScript interfaces
- `/examples/buttons.ts` - Validated TypeDoc examples

### Component Namespace Objects

Each component exports a namespace object (e.g., `export const Button = { ... }`). This is the **standard pattern** for East UI components.

**Requirements:**
- Namespace-level documentation with overview and simple examples
- `Root` property with factory function documentation
- `Types` object with documented type properties
- Examples showing `Component.Root(...)` usage and `Component.Types.X` access

**Example (from `/src/buttons/button/index.ts`):**

```typescript
/**
 * Button component for triggering actions.
 *
 * @remarks
 * Use `Button.Root(label, style)` to create a button, or access `Button.Types.Button` for the East type.
 */
export const Button = {
    /**
     * Creates a Button component with a label and optional styling.
     *
     * @param label - The text to display on the button
     * @param style - Optional styling configuration
     * @returns An East expression representing the styled button component
     *
     * @remarks
     * Button is an interactive component for triggering actions.
     * It supports multiple variants, color schemes, and sizes.
     *
     * @example
     * ```ts
     * import { East } from "@elaraai/east";
     * import { Button, UIComponentType } from "@elaraai/east-ui";
     *
     * const example = East.function([], UIComponentType, $ => {
     *     return Button.Root("Save", {
     *         variant: "solid",
     *         colorPalette: "blue",
     *         size: "md",
     *     });
     * });
     * ```
     */
    Root: createButton,
    Types: {
        /**
         * The concrete East type for Button component data.
         *
         * @remarks
         * This struct type represents the serializable data structure for a Button component.
         *
         * @property label - The text displayed on the button
         * @property style - Optional styling configuration wrapped in OptionType
         */
        Button: ButtonType,
        /**
         * Style type for Button component configuration.
         *
         * @remarks
         * This struct type defines the styling configuration for a Button component.
         *
         * @property variant - Button appearance variant (solid, subtle, outline, ghost)
         * @property colorPalette - Color scheme for the button
         * @property size - Size of the button (xs, sm, md, lg)
         * @property loading - Whether the button shows a loading state
         * @property disabled - Whether the button is disabled
         */
        Style: ButtonStyleType,
        /**
         * Variant type for Button appearance styles.
         *
         * @remarks
         * Create instances using string literals like "solid", "outline", etc.
         *
         * @property solid - Solid filled button (default)
         * @property subtle - Subtle/light background button
         * @property outline - Outlined button with border
         * @property ghost - Transparent button, visible on hover
         */
        Variant: ButtonVariantType,
    },
} as const;
```

**Rules for namespace objects:**

1. **Namespace-level docs** - Brief description with `@remarks` explaining usage
2. **Root property docs** - Full documentation with `@param`, `@returns`, `@remarks`, and `@example`
3. **Types property docs** - Each type in `Types` has its own documentation with `@property` tags
4. **All examples use `East.function()`** - Examples MUST be wrapped in `East.function()` so they can be validated

### Factory Functions

The private factory function (e.g., `createButton`) should also be documented, as it serves as the implementation for `Component.Root`.

**Requirements:**
- Start with a verb describing what the function does
- Document all parameters with `@param name - description`
- Document return value with `@returns description`
- Include `@remarks` for component behavior notes
- Include `@example` with `East.function()` - ALL examples MUST be validatable

**Example:**

```typescript
/**
 * Creates a Button component with a label and optional styling.
 *
 * @param label - The text to display on the button
 * @param style - Optional styling configuration
 * @returns An East expression representing the styled button component
 *
 * @remarks
 * Button is an interactive component for triggering actions.
 * It supports multiple variants, color schemes, and sizes.
 *
 * @example
 * ```ts
 * import { East } from "@elaraai/east";
 * import { Button, UIComponentType } from "@elaraai/east-ui";
 *
 * const example = East.function([], UIComponentType, $ => {
 *     const counter = $.let(0);
 *     return Button.Root("Save", {
 *         variant: "solid",
 *         colorPalette: "blue",
 *         onClick: _$ => {
 *             $.assign(counter, counter.add(1));
 *         },
 *     });
 * });
 * ```
 */
function createButton(
    label: SubtypeExprOrValue<StringType>,
    style?: ButtonStyle
): ExprType<UIComponentType> { ... }
```

### Types (StructType/VariantType)

East types defined with `StructType` or `VariantType` MUST use `@property` tags in the JSDoc comment block. TypeDoc does NOT see inline comments inside function call arguments.

**Requirements:**
- Summary describing what the type represents
- `@remarks` for important usage notes
- `@property` tag for EACH property/variant in the type
- Type alias exported alongside the const

**Example (from `/src/buttons/button/types.ts`):**

```typescript
/**
 * Variant type for Button appearance styles.
 *
 * @remarks
 * Create instances using string literals like "solid", "outline", etc.
 *
 * @property solid - Solid filled button (default)
 * @property subtle - Subtle/light background button
 * @property outline - Outlined button with border
 * @property ghost - Transparent button, visible on hover
 */
export const ButtonVariantType = VariantType({
    solid: NullType,
    subtle: NullType,
    outline: NullType,
    ghost: NullType,
});

/**
 * Type representing button variant values.
 */
export type ButtonVariantType = typeof ButtonVariantType;

/**
 * String literal type for button variant values.
 */
export type ButtonVariantLiteral = "solid" | "subtle" | "outline" | "ghost";
```

```typescript
/**
 * Style type for Button component configuration.
 *
 * @remarks
 * This struct type defines the styling configuration for a Button component.
 *
 * @property variant - Button appearance variant (solid, subtle, outline, ghost)
 * @property colorPalette - Color scheme for the button
 * @property size - Size of the button (xs, sm, md, lg)
 * @property loading - Whether the button shows a loading state
 * @property disabled - Whether the button is disabled
 * @property onClick - Callback triggered when the button is clicked
 */
export const ButtonStyleType = StructType({
    variant: OptionType(ButtonVariantType),
    colorPalette: OptionType(ColorSchemeType),
    size: OptionType(SizeType),
    loading: OptionType(BooleanType),
    disabled: OptionType(BooleanType),
    onClick: OptionType(FunctionType([], NullType)),
});

/**
 * Type representing the Button style structure.
 */
export type ButtonStyleType = typeof ButtonStyleType;
```

### TypeScript Interfaces

TypeScript interfaces for style options need BOTH `@property` tags in the JSDoc AND inline comments for each property.

**Requirements:**
- Summary describing the interface purpose
- `@remarks` for usage notes
- `@property` tag for each property (provides quick reference)
- Inline `/** comment */` for each property (provides hover documentation)

**Example (from `/src/buttons/button/types.ts`):**

```typescript
/**
 * TypeScript interface for Button style options.
 *
 * @remarks
 * Use this interface when creating Button components.
 *
 * @property variant - Button appearance variant
 * @property colorPalette - Color scheme for theming
 * @property size - Size of the button
 * @property loading - Shows loading spinner when true
 * @property disabled - Disables button interaction when true
 * @property onClick - Callback triggered when the button is clicked
 */
export interface ButtonStyle {
    /** Button appearance variant (solid, subtle, outline, ghost) */
    variant?: SubtypeExprOrValue<ButtonVariantType> | ButtonVariantLiteral;
    /** Color scheme for theming */
    colorPalette?: SubtypeExprOrValue<ColorSchemeType> | ColorSchemeLiteral;
    /** Size of the button */
    size?: SubtypeExprOrValue<SizeType> | SizeLiteral;
    /** Shows loading spinner when true */
    loading?: SubtypeExprOrValue<BooleanType>;
    /** Disables button interaction when true */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Callback triggered when the button is clicked */
    onClick?: SubtypeExprOrValue<FunctionType<[], NullType>>;
}
```

### General Rules

**MUST follow:**
- Write in present tense ("Creates a button" not "Will create a button")
- Be concise but complete - avoid redundant information
- Use proper markdown formatting for code references: `Type`, `null`, etc.
- Use `{@link SymbolName}` to create links to other documented types
- Include `@internal` for implementation details not part of public API

**Linking Example:**

```typescript
/**
 * Style type for Slider component.
 *
 * @remarks
 * See {@link SliderStyle} for the TypeScript interface.
 * Uses {@link ColorSchemeType} for color options.
 */
export const SliderStyleType = StructType({ ... });
```

---

## TypeDoc Example Validation

All TypeDoc `@example` blocks that contain compilable East code MUST be validated by including them in the appropriate examples file.

### Per-Module Example Files

Example validation files are organized **per module** in the `/examples/` directory:

```
examples/
  buttons.ts      # Button, IconButton examples
  display.ts      # Avatar, Badge, Icon, Stat, Tag examples
  forms.ts        # Input, Select, Checkbox, etc. examples
  layout.ts       # Box, Stack, Grid, Splitter examples
  collections.ts  # Table, TreeView, DataList, Gantt examples
  overlays.ts     # Dialog, Drawer, Popover, Menu examples
  ...
```

### Example File Format

Each example file follows this structure:

```typescript
/**
 * [Module Name] TypeDoc Examples
 *
 * This file contains compilable versions of all TypeDoc @example blocks
 * from the [module name] module ([Component1], [Component2], ...).
 *
 * Each example is compiled AND executed to verify correctness.
 *
 * Format: Each example has a comment indicating:
 *   - File path
 *   - Export property (e.g., Button.Root, IconButton.Root)
 */

import { East } from "@elaraai/east";
import { Button, IconButton, UIComponentType } from "../src/index.js";

// ============================================================================
// BUTTON
// ============================================================================

// File: src/buttons/button/index.ts
// Export: Button.Root
const buttonRootExample = East.function([], UIComponentType, $ => {
    let counter = $.let(0)
    return Button.Root("Save", {
        variant: "solid",
        colorPalette: "blue",
        size: "md",
        onClick: (_$) => {
            // increment counter
            $.assign(counter, counter.add(1));
        }
    });
});
buttonRootExample.toIR().compile([])();

// ============================================================================
// ICON BUTTON
// ============================================================================

// File: src/buttons/icon-button/index.ts
// Export: IconButton.Root (basic example)
const iconButtonRootExample = East.function([], UIComponentType, $ => {
    return IconButton.Root("fas", "xmark");
});
iconButtonRootExample.toIR().compile([])();

// File: src/buttons/icon-button/index.ts
// Export: IconButton.Root (styled example with callback)
const iconButtonStyledExample = East.function([], UIComponentType, $ => {
    let counter = $.let(0)
    return IconButton.Root("fas", "bars", {
        variant: "ghost",
        size: "lg",
        onClick: (_$) => {
            // increment counter
            $.assign(counter, counter.add(1));
        }
    });
});
iconButtonStyledExample.toIR().compile([])();

console.log("[Module Name] TypeDoc examples compiled and executed successfully!");
```

### Example Validation Rules

1. **One file per module** - Group related components together (e.g., all button components in `buttons.ts`)
2. **Comment each example** - Include file path and export property being validated
3. **Always use `East.function()`** - All examples MUST be wrapped in `East.function()` and compiled/executed with `.toIR().compile([])()`
4. **Include callback examples** - Show realistic usage with callbacks using `$.let()` and `$.assign()`
5. **Console log at end** - Confirm successful execution
6. **Run during build/test** - Examples are validated as part of `npm run build`

### Adding New Examples

When adding documentation to a component:

1. Write the TypeDoc `@example` block in the source file
2. Copy the example code to the appropriate `examples/[module].ts` file
3. Add the file path and export property comment
4. Run `npm run build` to verify the example compiles and executes

---

## Testing Standards

All East UI functionality MUST be thoroughly tested using East code.

### Test File Structure

**Requirements:**
- One test file per component: `test/[category]/[component].spec.ts`
- Import `describeEast` and `Assert` from `@elaraai/east-node-std`
- Test bodies MUST be written in East code using the `$` block builder
- Use `Assert.equal()`, `Assert.is()`, etc. for assertions

**Example:**

```typescript
import { East, variant } from "@elaraai/east";
import { Button } from "../../src/index.js";
import { describeEast, Assert } from "@elaraai/east-node-std";

describeEast("Button", (test) => {
    test("creates button with label", $ => {
        const button = $.let(Button.Root("Click me"));
        $(Assert.equal(button.unwrap("Button").label, "Click me"));
    });

    test("creates button with style", $ => {
        const button = $.let(Button.Root("Save", {
            variant: "solid",
            colorPalette: "blue",
        }));
        $(Assert.equal(button.unwrap("Button").label, "Save"));
        $(Assert.equal(
            button.unwrap("Button").style.unwrap("some").variant.unwrap("some").getTag(),
            "solid"
        ));
    });
});
```

### Test Coverage Requirements

**MUST test:**
- **Basic operations**: Core component creation with typical inputs
- **Style options**: All style properties are correctly applied
- **Edge cases**: Empty values, boundary conditions
- **Type access**: Verify `Component.Types.X` types are accessible

---

## Compliance

**These standards are MANDATORY.**

- All pull requests MUST comply with these standards
- Code review MUST verify compliance
- No exceptions without explicit approval from the project maintainer

**Before committing:**
1. All public APIs have TypeDoc comments following these standards
2. All TypeDoc examples compile successfully (validated in `examples/[module].ts`)
3. `@property` tags are present for all StructType/VariantType definitions
4. TypeScript interfaces have both `@property` tags AND inline comments
5. All new functionality has comprehensive test coverage
6. All tests pass: `npm run test`
7. Build succeeds: `npm run build`
8. Linting passes: `npm run lint`

**Gold Standard Reference:**
- `/src/buttons/button/index.ts` - Component namespace and factory documentation
- `/src/buttons/button/types.ts` - East types and TypeScript interface documentation
- `/examples/buttons.ts` - TypeDoc example validation
