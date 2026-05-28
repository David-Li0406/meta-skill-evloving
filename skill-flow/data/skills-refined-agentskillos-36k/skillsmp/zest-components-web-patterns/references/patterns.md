# Step-by-Step Implementation Patterns

This document provides detailed workflows for adding new components and updating existing components in the Zest design system.

## Pattern 1: Adding a New Component

### Prerequisites
- Figma design file with component specifications
- Component name decided (PascalCase, e.g., "ProgressBar")
- JIRA ticket number

### Step 1: Create Component Directory

```bash
cd packages/zest/src
mkdir ComponentName
cd ComponentName
```

### Step 2: Create Core Files

Create these files in order:

#### 2.1 Create `types.ts`
Define TypeScript interfaces first to establish the component's API.

```typescript
import type { CSSProperties } from 'react';

export type ComponentNameProps = {
  /**
   * Visual variant of the component
   * @default 'neutral'
   */
  variant?: 'neutral' | 'brand' | 'error' | 'success';

  /**
   * Size of the component
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Content to display
   */
  children: React.ReactNode;

  /**
   * Test identifier
   */
  'data-testid'?: string;
} & Omit<React.HTMLAttributes<HTMLDivElement>, keyof CSSProperties | 'style'>;
```

#### 2.2 Create `styles.ts`
Define default styles using design tokens.

```typescript
import type { BoxProps } from '../Box/BoxWithNewTokens';

export default {
  display: 'flex',
  alignItems: 'center',
  borderRadius: 'components.componentname.border-radius.default',
  padding: 'components.componentname.spacing.padding',
  gap: 'components.componentname.spacing.gap',
} as BoxProps;
```

#### 2.3 Create `variants.ts` (if needed)
Define variant configurations.

```typescript
import type { Variant, UseNewTokens } from '@/libs/zest-support';

const variants: Variant<UseNewTokens>[] = [
  {
    prop: 'variant',
    variants: {
      neutral: {
        bg: 'components.componentname.color.neutral.background',
        color: 'components.componentname.color.foreground',
      },
      brand: {
        bg: 'components.componentname.color.brand.background',
        color: 'components.componentname.color.foreground',
      },
      error: {
        bg: 'components.componentname.color.negative.background',
        color: 'components.componentname.color.foreground',
      },
      success: {
        bg: 'components.componentname.color.positive.background',
        color: 'components.componentname.color.foreground',
      },
    },
  },
  {
    prop: 'size',
    variants: {
      sm: {
        height: '1.5rem',
        fontSize: 'global.sm',
      },
      md: {
        height: '2rem',
        fontSize: 'global.md',
      },
      lg: {
        height: '2.5rem',
        fontSize: 'global.lg',
      },
    },
  },
];

export default variants;
```

#### 2.4 Create `ComponentName.tsx`
Main component implementation.

```typescript
// Figma: [FIGMA_URL_HERE]
import React, { Ref, forwardRef } from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import variants from './variants';
import defaultStyles from './styles';
import { ComponentNameProps } from './types';

/**
 * ### ComponentName
 * Brief description of what this component does.
 *
 * See the [docs](https://www-staging.yourcompany.com/zest-docs/ComponentName) for more information.
 *
 * #### Usage
 *
    ```js
    import { ComponentName } from '@/libs/zest';

    return (
      <ComponentName variant="brand" size="md">
        Content
      </ComponentName>
    )
    ```
  */

const ComponentName = forwardRef((props: ComponentNameProps, ref?: Ref<HTMLDivElement>) => {
  const { children, variant = 'neutral', size = 'md', ...rest } = props;

  return (
    <Box
      ref={ref}
      variants={variants}
      variant={variant}
      size={size}
      role="status"  // or appropriate ARIA role
      aria-label="Component name"
      {...rest}
      {...defaultStyles}
    >
      {children}
    </Box>
  );
});

ComponentName.displayName = 'ComponentName';

export default ComponentName;
```

**Important**: Replace `[FIGMA_URL_HERE]` with the actual Figma file URL.

#### 2.5 Create `index.ts`
Export the component.

```typescript
import ComponentName from './ComponentName';
export default ComponentName;
```

### Step 3: Create Tests

Create `ComponentName.test.tsx`:

```typescript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentName from './ComponentName';

describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<ComponentName>Test Content</ComponentName>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('should render with different variants', () => {
    const { rerender } = render(<ComponentName variant="neutral">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();

    rerender(<ComponentName variant="brand">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();

    rerender(<ComponentName variant="error">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('should render with different sizes', () => {
    const { rerender } = render(<ComponentName size="sm">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();

    rerender(<ComponentName size="md">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();

    rerender(<ComponentName size="lg">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('should handle custom props', () => {
    render(<ComponentName data-testid="custom-component">Test</ComponentName>);
    expect(screen.getByTestId('custom-component')).toBeInTheDocument();
  });

  it('should match snapshot', () => {
    const { container } = render(
      <ComponentName variant="brand" size="md">
        Snapshot Test
      </ComponentName>
    );
    expect(container).toMatchSnapshot();
  });
});
```

### Step 4: Update Main Index

Edit `packages/zest/src/index.ts`:

```typescript
// Find the appropriate alphabetical location and add:
export { default as ComponentName } from './ComponentName';

// In the types section:
export type { ComponentNameProps } from './ComponentName/types';
```

### Step 5: Create Storybook Documentation

Create `apps/zest-docs/stories/ComponentName.stories.tsx`:

```typescript
import type { Meta, StoryObj } from '@storybook/nextjs';
import { ComponentName } from '@/packages/zest';

const meta: Meta<typeof ComponentName> = {
  title: 'Components/Category/ComponentName',  // Choose appropriate category
  component: ComponentName,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['neutral', 'brand', 'error', 'success'],
      description: 'Visual variant of the component',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Size of the component',
    },
    children: {
      control: 'text',
      description: 'Content to display inside the component',
    },
  },
  parameters: {
    docs: {
      description: {
        component: 'Detailed description of the component and its use cases.',
      },
    },
  },
};

export default meta;
type Story = StoryObj<typeof ComponentName>;

export const Default: Story = {
  args: {
    variant: 'neutral',
    size: 'md',
    children: 'Default Example',
  },
};

export const Variants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexDirection: 'column' }}>
      <ComponentName variant="neutral">Neutral</ComponentName>
      <ComponentName variant="brand">Brand</ComponentName>
      <ComponentName variant="error">Error</ComponentName>
      <ComponentName variant="success">Success</ComponentName>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'All available variants of the component.',
      },
    },
  },
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <ComponentName size="sm">Small</ComponentName>
      <ComponentName size="md">Medium</ComponentName>
      <ComponentName size="lg">Large</ComponentName>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Different sizes available for the component.',
      },
    },
  },
};
```

### Step 6: Run Tests

```bash
# Run tests
yarn test ComponentName.test.tsx

# Update snapshots
yarn test ComponentName.test.tsx -u

# Run all tests
yarn test
```

### Step 7: Verify in Storybook

```bash
# Start Storybook
yarn storybook

# Navigate to Components/Category/ComponentName
```

### Step 8: Create Pull Request

```bash
# Create branch
git checkout -b feature/TICKET-123-add-componentname

# Stage changes
git add packages/zest/src/ComponentName/
git add packages/zest/src/index.ts
git add apps/zest-docs/stories/ComponentName.stories.tsx

# Commit
git commit -m "[TICKET-123] Add ComponentName Zest component"

# Push
git push -u origin feature/TICKET-123-add-componentname

# Create PR using gh CLI
gh pr create --title "[TICKET-123] Add ComponentName Zest component" --body "## Summary
- Added new ComponentName component to Zest
- Includes all variants: neutral, brand, error, success
- Includes all sizes: sm, md, lg
- Full test coverage with snapshots
- Storybook documentation

## Figma
[Figma URL]

## Test Plan
- [ ] Run \`yarn test\` - all tests pass
- [ ] Run \`yarn storybook\` - component renders correctly
- [ ] Verify all variants render correctly
- [ ] Verify all sizes render correctly
- [ ] Verify accessibility (keyboard navigation, screen readers)

## Rollback Difficulty
Easy - new component, no dependencies"
```

---

## Pattern 2: Updating an Existing Component

### Prerequisites
- Figma design file with updated specifications
- Component name (existing)
- JIRA ticket number
- Understanding of what needs to change

### Step 1: Analyze Current Implementation

```bash
cd packages/zest/src/ComponentName

# Read all files to understand current structure
ls -la
```

Review:
- Current props and types
- Existing variants
- Current styling
- Test coverage
- Storybook stories

### Step 2: Identify Changes Needed

Determine what needs to be updated:
- **New props**: Add to `types.ts`
- **New variants**: Update `variants.ts`
- **Style changes**: Update `styles.ts` or `variants.ts`
- **Behavior changes**: Update `ComponentName.tsx`
- **Breaking changes**: Document in PR

### Step 3: Update Files

#### 3.1 Update `types.ts` (if adding props)

```typescript
export type ComponentNameProps = {
  // Existing props...

  /**
   * NEW: Additional prop description
   * @default 'default-value'
   */
  newProp?: string;

} & Omit<React.HTMLAttributes<HTMLDivElement>, keyof CSSProperties | 'style'>;
```

#### 3.2 Update `variants.ts` (if adding variants)

```typescript
const variants: Variant<UseNewTokens>[] = [
  {
    prop: 'variant',
    variants: {
      // Existing variants...

      // NEW: Add new variant
      info: {
        bg: 'components.componentname.color.info.background',
        color: 'components.componentname.color.foreground',
      },
    },
  },
  // Other variant groups...
];
```

#### 3.3 Update `ComponentName.tsx`

```typescript
// Update Figma reference if design changed
// Figma: [NEW_FIGMA_URL]

const ComponentName = forwardRef((props: ComponentNameProps, ref?: Ref<HTMLDivElement>) => {
  const {
    children,
    variant = 'neutral',
    size = 'md',
    newProp,  // NEW: Handle new prop
    ...rest
  } = props;

  return (
    <Box
      ref={ref}
      variants={variants}
      variant={variant}
      size={size}
      // NEW: Use new prop
      data-new-prop={newProp}
      {...rest}
      {...defaultStyles}
    >
      {children}
    </Box>
  );
});
```

### Step 4: Update Tests

Add new test cases for the changes:

```typescript
describe('ComponentName', () => {
  // Existing tests...

  // NEW: Test new prop
  it('should handle new prop', () => {
    render(<ComponentName newProp="test-value">Test</ComponentName>);
    const element = screen.getByText('Test');
    expect(element).toHaveAttribute('data-new-prop', 'test-value');
  });

  // NEW: Test new variant
  it('should render new info variant', () => {
    render(<ComponentName variant="info">Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  // Update snapshot test
  it('should match snapshot', () => {
    const { container } = render(
      <ComponentName variant="info" newProp="test">
        Snapshot Test
      </ComponentName>
    );
    expect(container).toMatchSnapshot();
  });
});
```

### Step 5: Update Storybook

Add stories for new features:

```typescript
// Add to existing stories file

export const NewVariant: Story = {
  render: () => (
    <ComponentName variant="info">New Info Variant</ComponentName>
  ),
  parameters: {
    docs: {
      description: {
        story: 'New info variant added in [TICKET-123].',
      },
    },
  },
};

export const WithNewProp: Story = {
  args: {
    variant: 'neutral',
    newProp: 'example-value',
    children: 'With New Prop',
  },
  parameters: {
    docs: {
      description: {
        story: 'Example using the new prop.',
      },
    },
  },
};
```

### Step 6: Update Main Index (if needed)

If you added new types that should be exported:

```typescript
// packages/zest/src/index.ts
export type { ComponentNameProps, NewTypeIfAdded } from './ComponentName/types';
```

### Step 7: Run Tests and Update Snapshots

```bash
# Run tests for the component
yarn test ComponentName.test.tsx

# Update snapshots (they will change if UI changed)
yarn test ComponentName.test.tsx -u

# Run all tests to ensure no regressions
yarn test
```

### Step 8: Verify No Regressions

```bash
# Search for all usages of the component
grep -r "ComponentName" packages/zest/src/
grep -r "ComponentName" apps/

# Check if any components import this one
# Test those components to ensure no breaks
```

### Step 9: Create Pull Request

```bash
# Create branch
git checkout -b feature/TICKET-456-update-componentname

# Stage changes
git add packages/zest/src/ComponentName/
git add packages/zest/src/index.ts  # if updated
git add apps/zest-docs/stories/ComponentName.stories.tsx

# Commit
git commit -m "[TICKET-456] Update ComponentName with new variant"

# Push
git push -u origin feature/TICKET-456-update-componentname

# Create PR
gh pr create --title "[TICKET-456] Update ComponentName with new variant" --body "## Summary
- Added new 'info' variant to ComponentName
- Added newProp for additional configuration
- Updated tests and snapshots
- Updated Storybook stories

## Changes
- NEW: Added 'info' variant
- NEW: Added 'newProp' prop
- UPDATED: Figma reference URL

## Figma
Before: [Old Figma URL]
After: [New Figma URL]

## Test Plan
- [ ] Run \`yarn test\` - all tests pass
- [ ] Verify existing usages still work
- [ ] Verify new variant renders correctly
- [ ] Verify no visual regressions

## Rollback Difficulty
Easy/Moderate/Hard - [Explain why]"
```

---

## Pattern 3: Migrating Legacy Component to Zest

### Step 1: Analyze Legacy Component

```bash
# Find the legacy component
find . -name "OldComponent.*"

# Read the implementation
cat path/to/OldComponent.js
```

Document:
- Current props (PropTypes)
- Current styling (CSS-in-JS, styled-components)
- Current behavior
- Current usages

### Step 2: Create Zest Component

Follow "Pattern 1: Adding a New Component" but map legacy props to new Zest patterns.

**Prop Mapping**:
- Boolean flags → Variants
  ```typescript
  // Old: isTotal={true}
  // New: variant="total"
  ```
- Inline styles → Design tokens
  ```typescript
  // Old: style={{ color: '#ff0000' }}
  // New: color="components.component.color.error.foreground"
  ```
- CSS classes → Box props
  ```typescript
  // Old: className="flex-row"
  // New: display="flex" flexDirection="row"
  ```

### Step 3: Create Migration Component (Temporary)

Create a wrapper that maintains backward compatibility:

```typescript
// OldComponent.tsx (temporary compatibility layer)
import React from 'react';
import { ComponentName } from '@/libs/zest';
import type { OldComponentProps } from './types';

/**
 * @deprecated Use ComponentName from @/libs/zest instead
 */
export const OldComponent: React.FC<OldComponentProps> = ({
  isTotal,  // Old prop
  isError,  // Old prop
  ...rest
}) => {
  // Map old props to new props
  const variant = isError ? 'error' : isTotal ? 'total' : 'neutral';

  return <ComponentName variant={variant} {...rest} />;
};
```

### Step 4: Update Usages Gradually

```bash
# Find all usages
grep -r "OldComponent" apps/
grep -r "OldComponent" packages/

# Update each usage:
# Before:
# <OldComponent isTotal={true} />

# After:
# <ComponentName variant="total" />
```

### Step 5: Remove Legacy Component

Once all usages are updated:

```bash
# Remove old component files
git rm path/to/OldComponent.js
git rm path/to/OldComponent.styles.js

# Commit
git commit -m "[TICKET-789] Complete migration from OldComponent to ComponentName"
```

---

## Common Workflows

### Adding a Sub-Component

For complex components like Accordion with Title and Description:

1. Create sub-component files in the main directory
2. Use React Context for shared state
3. Export via Object.assign pattern

```typescript
// Accordion/index.tsx
import Title from './Title';
import Description from './Description';

const Accordion: React.FC<AccordionProps> = ({ children }) => {
  return <AccordionContext.Provider>{children}</AccordionContext.Provider>;
};

export default Object.assign(Accordion, { Title, Description });
```

### Adding Nested Sub-Components

For components with deeply nested sub-components:

1. Create a subdirectory for the sub-component
2. Follow the same file structure pattern

```
ComponentName/
├── index.tsx
├── SubComponent/
│   ├── index.tsx
│   └── NestedPart.tsx
```

### Splitting Variants into Separate Files

For components with many variants:

1. Create `variants/` directory
2. One file per variant group
3. Combine in `variants/index.ts`

```
ComponentName/
├── variants/
│   ├── index.ts
│   ├── brandVariants.ts
│   ├── sizeVariants.ts
│   └── stateVariants.ts
```

---

These patterns cover 95% of Zest component work. Refer to [examples.md](./examples.md) for complete real-world implementations.
