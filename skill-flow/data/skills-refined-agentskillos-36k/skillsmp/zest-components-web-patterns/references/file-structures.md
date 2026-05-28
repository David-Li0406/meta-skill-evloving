# File Structure Layouts

Complete directory layouts for different types of Zest components.

## Simple Component

**Use when**: Component has minimal complexity, straightforward props, single-level implementation.

**Examples**: Badge, Tag, Pill, Spinner, Divider

```
packages/zest/src/Badge/
├── Badge.tsx                    # Main component (150-200 lines)
├── index.ts                     # Simple export (2 lines)
├── types.ts                     # TypeScript types (20-30 lines)
├── styles.ts                    # Default styles (15-20 lines)
└── variants.ts                  # Variant configs (30-50 lines)
```

### File Sizes (Approximate)
- **Badge.tsx**: 150-200 lines
- **index.ts**: 2-5 lines
- **types.ts**: 20-30 lines
- **styles.ts**: 15-20 lines
- **variants.ts**: 30-50 lines
- **Total**: ~250-350 lines

### Directory Commands

```bash
# Create structure
mkdir -p packages/zest/src/Badge
cd packages/zest/src/Badge
touch Badge.tsx index.ts types.ts styles.ts variants.ts

# Verify structure
tree packages/zest/src/Badge
```

---

## Simple Component with Tests

**Use when**: Same as simple component, but with test coverage (recommended for all components).

**Examples**: Badge, Tag, Pill

```
packages/zest/src/Badge/
├── Badge.tsx
├── Badge.test.tsx               # Unit tests with snapshots
├── __snapshots__/
│   └── Badge.test.tsx.snap     # Jest snapshots
├── index.ts
├── types.ts
├── styles.ts
└── variants.ts
```

### File Sizes (Approximate)
- **Badge.test.tsx**: 100-150 lines
- **Badge.test.tsx.snap**: 50-100 lines (generated)
- **Other files**: Same as simple component
- **Total**: ~400-600 lines

### Directory Commands

```bash
# Create structure
mkdir -p packages/zest/src/Badge/__snapshots__
cd packages/zest/src/Badge
touch Badge.tsx Badge.test.tsx index.ts types.ts styles.ts variants.ts

# After running tests, snapshot is auto-generated:
# __snapshots__/Badge.test.tsx.snap
```

---

## Complex Component (Composition Pattern)

**Use when**: Component has multiple sub-components, uses React Context, compound component pattern.

**Examples**: Accordion, Modal, Tabs, Dropdown

```
packages/zest/src/Accordion/
├── index.tsx                    # Main component with context (100-150 lines)
├── Title.tsx                    # Sub-component (50-70 lines)
├── Description.tsx              # Sub-component (30-50 lines)
├── ButtonWrapper/               # Nested sub-component
│   ├── index.tsx               # Wrapper component (40-60 lines)
│   └── ChevronIcon.tsx         # Icon component (30-40 lines)
├── types.ts                     # All component types (40-60 lines)
├── styles.ts                    # Shared styles (20-30 lines)
├── Accordion.test.tsx           # Comprehensive tests (200-300 lines)
└── __snapshots__/
    └── Accordion.test.tsx.snap  # Snapshots (100-200 lines)
```

### File Sizes (Approximate)
- **index.tsx**: 100-150 lines
- **Title.tsx**: 50-70 lines
- **Description.tsx**: 30-50 lines
- **ButtonWrapper/index.tsx**: 40-60 lines
- **ButtonWrapper/ChevronIcon.tsx**: 30-40 lines
- **types.ts**: 40-60 lines
- **styles.ts**: 20-30 lines
- **Accordion.test.tsx**: 200-300 lines
- **Total**: ~500-900 lines

### Directory Commands

```bash
# Create structure
mkdir -p packages/zest/src/Accordion/ButtonWrapper/__snapshots__
cd packages/zest/src/Accordion
touch index.tsx Title.tsx Description.tsx types.ts styles.ts Accordion.test.tsx
touch ButtonWrapper/index.tsx ButtonWrapper/ChevronIcon.tsx

# Verify structure
tree packages/zest/src/Accordion
```

### Context Pattern

```typescript
// index.tsx structure
const AccordionContext = createContext<AccordionContextType | undefined>(undefined);

export const useAccordionContext = () => {
  const context = useContext(AccordionContext);
  if (!context) throw new Error('Must be used within Accordion');
  return context;
};

const Accordion: React.FC<AccordionProps> = ({ children }) => {
  return <AccordionContext.Provider>{children}</AccordionContext.Provider>;
};

// Export as compound component
export default Object.assign(Accordion, { Title, Description, ButtonWrapper });
```

---

## Component with Multiple Variants

**Use when**: Component has multiple distinct visual variants, each potentially with separate wrapper components.

**Examples**: Button (Primary, Secondary, Tertiary), Alert, Card

```
packages/zest/src/Button/
├── BaseButton.tsx               # Base implementation (200-250 lines)
├── PrimaryButton.tsx            # Variant wrapper (30-40 lines)
├── SecondaryButton.tsx          # Variant wrapper (30-40 lines)
├── TertiaryButton.tsx           # Variant wrapper (30-40 lines)
├── index.tsx                    # Exports all variants (15-20 lines)
├── types.ts                     # All button types (60-80 lines)
├── defaultStyles.ts             # Base styles (30-40 lines)
├── variants/                    # Variant-specific styles
│   ├── index.ts                # Combines all variants (10-15 lines)
│   ├── brandVariants.ts        # Brand color variants (60-80 lines)
│   ├── negativeVariants.ts     # Negative/error variants (40-50 lines)
│   ├── neutralVariants.ts      # Neutral variants (40-50 lines)
│   └── sizeVariants.ts         # Size variants (40-50 lines)
├── BaseButton.test.tsx          # Tests for all variants (300-400 lines)
└── __snapshots__/
    └── BaseButton.test.tsx.snap # Snapshots (200-300 lines)
```

### File Sizes (Approximate)
- **BaseButton.tsx**: 200-250 lines
- **Variant wrappers (each)**: 30-40 lines × 3 = 90-120 lines
- **index.tsx**: 15-20 lines
- **types.ts**: 60-80 lines
- **defaultStyles.ts**: 30-40 lines
- **variants/*.ts**: 200-250 lines total
- **BaseButton.test.tsx**: 300-400 lines
- **Total**: ~1000-1400 lines

### Directory Commands

```bash
# Create structure
mkdir -p packages/zest/src/Button/variants/__snapshots__
cd packages/zest/src/Button
touch BaseButton.tsx PrimaryButton.tsx SecondaryButton.tsx TertiaryButton.tsx
touch index.tsx types.ts defaultStyles.ts BaseButton.test.tsx
touch variants/index.ts variants/brandVariants.ts variants/negativeVariants.ts
touch variants/neutralVariants.ts variants/sizeVariants.ts

# Verify structure
tree packages/zest/src/Button
```

### Variant Export Pattern

```typescript
// index.tsx structure
import PrimaryButton from './PrimaryButton';
import SecondaryButton from './SecondaryButton';
import TertiaryButton from './TertiaryButton';

const Button = {
  Primary: PrimaryButton,
  Secondary: SecondaryButton,
  Tertiary: TertiaryButton,
};

export default Button;

// Usage:
// <Button.Primary>Click</Button.Primary>
```

---

## Highly Complex Component

**Use when**: Component has multiple levels of nesting, extensive state management, many sub-components.

**Examples**: DataTable, Calendar, Form, Wizard

```
packages/zest/src/DataTable/
├── index.tsx                    # Main component (150-200 lines)
├── types.ts                     # Complex types (100-150 lines)
├── context.ts                   # Context provider (80-100 lines)
├── hooks/
│   ├── useTableState.ts        # State management (100-150 lines)
│   ├── useSorting.ts           # Sorting logic (80-100 lines)
│   └── useFiltering.ts         # Filtering logic (80-100 lines)
├── components/
│   ├── Header/
│   │   ├── index.tsx           # Header component (100-120 lines)
│   │   ├── HeaderCell.tsx      # Cell component (80-100 lines)
│   │   └── SortIcon.tsx        # Sort indicator (40-50 lines)
│   ├── Body/
│   │   ├── index.tsx           # Body component (80-100 lines)
│   │   ├── Row.tsx             # Row component (100-120 lines)
│   │   └── Cell.tsx            # Cell component (60-80 lines)
│   ├── Footer/
│   │   ├── index.tsx           # Footer component (80-100 lines)
│   │   └── Pagination.tsx      # Pagination controls (120-150 lines)
│   └── EmptyState.tsx          # Empty state (40-50 lines)
├── utils/
│   ├── sorting.ts              # Sorting utilities (100-120 lines)
│   ├── filtering.ts            # Filtering utilities (80-100 lines)
│   └── formatting.ts           # Data formatting (60-80 lines)
├── styles.ts                    # Shared styles (40-50 lines)
├── DataTable.test.tsx           # Component tests (400-500 lines)
├── hooks.test.tsx               # Hook tests (200-250 lines)
└── __snapshots__/
    ├── DataTable.test.tsx.snap  # Component snapshots
    └── hooks.test.tsx.snap      # Hook snapshots
```

### File Sizes (Approximate)
- **Main files**: ~500-700 lines
- **Hooks**: ~300-400 lines
- **Components**: ~700-900 lines
- **Utils**: ~250-300 lines
- **Tests**: ~600-750 lines
- **Total**: ~2500-3500 lines

### Directory Commands

```bash
# Create structure
mkdir -p packages/zest/src/DataTable/{hooks,components/{Header,Body,Footer},utils,__snapshots__}
cd packages/zest/src/DataTable

# Main files
touch index.tsx types.ts context.ts styles.ts

# Hooks
touch hooks/useTableState.ts hooks/useSorting.ts hooks/useFiltering.ts

# Components
touch components/Header/index.tsx components/Header/HeaderCell.tsx components/Header/SortIcon.tsx
touch components/Body/index.tsx components/Body/Row.tsx components/Body/Cell.tsx
touch components/Footer/index.tsx components/Footer/Pagination.tsx
touch components/EmptyState.tsx

# Utils
touch utils/sorting.ts utils/filtering.ts utils/formatting.ts

# Tests
touch DataTable.test.tsx hooks.test.tsx

# Verify structure
tree packages/zest/src/DataTable
```

---

## Migration: Side-by-Side Pattern

**Use when**: Migrating from legacy component to Zest, need temporary backward compatibility.

```
packages/
├── zest/src/ComponentName/     # New Zest component
│   ├── ComponentName.tsx
│   ├── index.ts
│   ├── types.ts
│   ├── styles.ts
│   └── variants.ts
└── legacy/                     # Legacy location (temporary)
    └── OldComponent/
        ├── OldComponent.js     # Legacy implementation
        ├── OldComponent.styles.js
        └── OldComponentAdapter.tsx  # Adapter to new component
```

### Adapter Pattern

```typescript
// OldComponentAdapter.tsx
import React from 'react';
import { ComponentName } from '@/libs/zest';

/**
 * @deprecated Use ComponentName from @/libs/zest instead
 * This adapter provides backward compatibility during migration.
 */
export const OldComponent = ({ isError, isSuccess, ...rest }) => {
  // Map old props to new props
  const variant = isError ? 'error' : isSuccess ? 'success' : 'neutral';

  console.warn(
    'OldComponent is deprecated. Please use ComponentName with variant prop instead.'
  );

  return <ComponentName variant={variant} {...rest} />;
};
```

---

## With Storybook Documentation

**Complete setup**: Component + Tests + Storybook stories

```
packages/zest/src/Badge/
├── Badge.tsx
├── Badge.test.tsx
├── __snapshots__/
│   └── Badge.test.tsx.snap
├── index.ts
├── types.ts
├── styles.ts
└── variants.ts

apps/zest-docs/stories/
└── Badge.stories.tsx            # Storybook documentation (150-200 lines)
```

### Storybook File Location

Always create stories in `apps/zest-docs/stories/` with the same name as the component:

```bash
# Component location
packages/zest/src/Badge/

# Story location (matching name)
apps/zest-docs/stories/Badge.stories.tsx
```

---

## Decision Tree: Which Structure to Use?

```
Does the component have sub-components?
├─ NO
│  └─ Does it have multiple distinct variants (Primary, Secondary, etc.)?
│     ├─ YES → Use "Component with Multiple Variants" structure
│     └─ NO → Use "Simple Component" structure
│
└─ YES
   └─ Are sub-components deeply nested (3+ levels)?
      ├─ YES → Use "Highly Complex Component" structure
      └─ NO → Use "Complex Component (Composition Pattern)" structure
```

### Quick Reference

| Component Type | Structure | Example |
|----------------|-----------|---------|
| Simple, standalone | Simple Component | Badge, Spinner |
| Simple with variants | Multiple Variants | Button, Alert |
| Compound component | Complex Composition | Accordion, Tabs |
| Many nested parts | Highly Complex | DataTable, Form |

---

## File Naming Conventions

### Component Files
- **PascalCase**: `ComponentName.tsx`, `SubComponent.tsx`
- **Descriptive**: `HeaderCell.tsx`, not `Cell1.tsx`

### Type Files
- **Always**: `types.ts` (singular)
- **Never**: `types.d.ts` or `index.types.ts`

### Style Files
- **Default styles**: `styles.ts` or `defaultStyles.ts`
- **Variants**: `variants.ts` or `variants/` directory

### Test Files
- **Match component**: `ComponentName.test.tsx`
- **Hook tests**: `hooks.test.tsx`
- **Snapshots**: Auto-generated in `__snapshots__/`

### Index Files
- **Always**: `index.ts` or `index.tsx`
- **Purpose**: Exports only, minimal logic

---

## Common Mistakes

❌ **Don't use these structures:**

```
# Bad: Nested too deep without reason
Badge/
  src/
    components/
      Badge/
        Badge.tsx

# Bad: Inconsistent naming
Badge/
  badge.tsx        # lowercase
  BadgeTypes.ts    # inconsistent suffix
  badge-styles.ts  # kebab-case
```

✅ **Do use these structures:**

```
# Good: Flat, consistent
Badge/
  Badge.tsx
  types.ts
  styles.ts
  variants.ts

# Good: Organized by purpose
Button/
  BaseButton.tsx
  PrimaryButton.tsx
  variants/
    brandVariants.ts
    sizeVariants.ts
```

---

## Templates

### Quick Start: Simple Component

```bash
#!/bin/bash
# create-simple-component.sh

COMPONENT_NAME=$1

mkdir -p "packages/zest/src/$COMPONENT_NAME/__snapshots__"
cd "packages/zest/src/$COMPONENT_NAME"

# Create files
touch "${COMPONENT_NAME}.tsx"
touch "${COMPONENT_NAME}.test.tsx"
touch index.ts
touch types.ts
touch styles.ts
touch variants.ts

echo "Created component structure for $COMPONENT_NAME"
tree "packages/zest/src/$COMPONENT_NAME"
```

### Quick Start: Complex Component

```bash
#!/bin/bash
# create-complex-component.sh

COMPONENT_NAME=$1

mkdir -p "packages/zest/src/$COMPONENT_NAME/__snapshots__"
cd "packages/zest/src/$COMPONENT_NAME"

# Create main files
touch index.tsx types.ts styles.ts "${COMPONENT_NAME}.test.tsx"

# Create sub-components (customize as needed)
mkdir -p Title Description ButtonWrapper
touch Title/index.tsx
touch Description/index.tsx
touch ButtonWrapper/index.tsx

echo "Created complex component structure for $COMPONENT_NAME"
tree "packages/zest/src/$COMPONENT_NAME"
```

---

Use these structures as templates when creating new Zest components. Consistency in file organization makes the codebase easier to navigate and maintain.
