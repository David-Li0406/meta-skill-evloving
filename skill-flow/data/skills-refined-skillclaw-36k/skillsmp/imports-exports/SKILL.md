---
name: imports-exports
description: "WHAT: TypeScript import ordering and export conventions. WHEN: organizing imports, creating barrel exports, reviewing import structure. KEYWORDS: imports, exports, named exports, import type, barrel, index.ts, path aliases, ESLint, ordering."
---

# Import and Export Standards

Standards for organizing imports and exports in TypeScript/React Native files.

## When to Use

Use these standards when:
- Writing new TypeScript/React Native files
- Reviewing code for proper import organization
- Setting up path aliases in tsconfig.json
- Configuring ESLint rules for imports
- Creating barrel exports (index.ts files)
- Refactoring module structure

## Core Principles

### ESLint-Enforced Import Order

Imports are automatically organized by ESLint with these groups:

1. **React and React Native** - Built-in frameworks
2. **External libraries** - node_modules packages
3. **Internal path aliases** - @libs, @modules, @data-access, @zest
4. **Parent imports** - ../
5. **Sibling imports** - ./
6. **Type imports** - Always last in each group

**Between groups**: Blank lines required

**Within groups**: Alphabetized (case-insensitive)

✅ **Good:**
```typescript
// Group 1: React/React Native
import { useEffect, useState, useMemo } from 'react';
import { View, ScrollView, TouchableOpacity } from 'react-native';

// Group 2: External libraries
import { useQuery } from '@tanstack/react-query';

// Group 3: Internal aliases (alphabetized)
import { useRecipeData } from '@data-access/query';
import { useT9n } from '@libs/localization';
import { useNavigation } from '@libs/navigation';

// Group 3: Zest design system
import { Accordion, Text, useZestStyles } from '@zest/react-native';

// Group 4: Local imports
import { FAQ_ITEMS } from './constants';
import { stylesConfig } from './styles';

// Group 5: Type imports (always last)
import type { FaqItem } from './types';
```

❌ **Bad:**
```typescript
// Disorganized - mixed groups
import { stylesConfig } from './styles';
import { View } from 'react-native';
import type { FaqItem } from './types';
import { useT9n } from '@libs/localization';
import { useQuery } from '@tanstack/react-query';
```

**Why:** Automatic organization ensures consistency and makes dependencies scannable.

### Named Exports Only

**Never use default exports. Always use named exports.**

✅ **Good:**
```typescript
export const UserProfile = ({ user }: UserProps) => {
  return <View>...</View>;
};

export const calculateTotal = (items: Item[]) => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

export type { UserProps, Item };
```

❌ **Bad:**
```typescript
export default UserProfile;  // NEVER

const UserProfile = () => <View />;
export { UserProfile as default };  // Still default export
```

**Why:** Named exports provide:
- Better IDE support (autocomplete, refactoring)
- Explicit imports (can't rename arbitrarily)
- Better tree-shaking
- No naming conflicts

### Type-Only Imports

Use `import type` for type-only imports.

✅ **Good:**
```typescript
import type { User } from '@data-access/graphql';
import type { ComponentProps } from './types';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
```

❌ **Bad:**
```typescript
import { User } from '@data-access/graphql';  // Use 'import type'
```

**Why:** Type-only imports are erased at compile time, reducing bundle size.

## Path Aliases

Use configured path aliases instead of relative paths for cross-module imports.

**Available aliases:**

| Alias | Maps To | Usage |
|-------|---------|-------|
| `@assets/*` | `src/assets/*` | Static assets |
| `@data-access/*` | `src/data-access/*` | API layer |
| `@entry-providers/*` | `src/entry-providers/*` | Entry providers |
| `@features/*` | `src/features/*` | UI features |
| `@libs/*` | `src/libs/*` | Infrastructure |
| `@modules/*` | `src/modules/*` | Modules |
| `@navigation/*` | `src/navigation/*` | Navigation |
| `@operations/*` | `src/operations/*` | Business logic |
| `@types/*` | `src/types/*` | Shared types |
| `@zest/*` | `@zest/react-native` | Design system |

✅ **Good:**
```typescript
import { useT9n } from '@libs/localization';
import { RecipeCard } from '@features/recipe-card';
import { useGetRecipes } from '@data-access/query';
```

❌ **Bad:**
```typescript
import { useT9n } from '../../../libs/localization';
import { RecipeCard } from '../../features/recipe-card';
```

**Why:** Path aliases remain stable during refactoring and are easier to read.

## Restricted Imports

### No Deep Imports

Import from public APIs, not internal modules.

✅ **Good:**
```typescript
import { helper } from '@libs/localization';
import { parser } from '@data-access/query';
```

❌ **Bad:**
```typescript
import { helper } from '@libs/localization/utils/helper';
import { parser } from '@data-access/query/helpers/parser';
```

**Exceptions** (one level allowed):
- `@libs/native-modules/*`
- `@data-access/native/*`
- `@data-access/query/*`
- `@data-access/graphql/*`

**Why:** Deep imports bypass public APIs and create tight coupling.

### GraphQL gql Import

Always import `gql` from the data-access layer.

✅ **Good:**
```typescript
import { gql } from '@data-access/graphql';
```

❌ **Bad:**
```typescript
import { gql } from '@apollo/client';
```

**Why:** Centralizing graphql imports enables consistent configuration.

## Grouping Related Imports

Group related imports from the same package on a single line.

✅ **Good:**
```typescript
import { View, ScrollView, TouchableOpacity, FlatList } from 'react-native';
import { Button, Text, Input, useZestStyles } from '@zest/react-native';
import { useState, useEffect, useMemo, useCallback } from 'react';
```

❌ **Bad:**
```typescript
import { View } from 'react-native';
import { ScrollView } from 'react-native';
import { TouchableOpacity } from 'react-native';
```

**Why:** Grouped imports reduce line count and clarify package dependencies.

## Barrel Exports (index.ts)

Use barrel exports to create clean public APIs.

### Module Barrel
```typescript
// src/modules/social-recipe-bridge/index.ts
export * from './stacks';
export * from './screens';
export * from './hooks';
export * from './stores';
export type * from './types';
```

### Component Barrel
```typescript
// src/features/product-card-feature/index.ts
export { ProductCard } from './ProductCard';
export { LoadingProductCard } from './variants/loading';
export type { ProductCardProps, ProductVariant } from './types';
```

### Screen Directory Barrel with Plop
```typescript
// src/modules/social-recipe-bridge/screens/index.ts
export * from './cookbook-faq';
export * from './onboarding';
export * from './add-recipe-link-drawer';
// @PLOP_INSERT_SCREEN_EXPORT
```

**Why:** Barrel exports hide internal structure and enable simpler imports.

## Inline Type Imports

Combine value and type imports when importing from the same source.

✅ **Good:**
```typescript
import { View, type ImageStyle } from 'react-native';
import { useQuery, type UseQueryOptions } from '@tanstack/react-query';
```

❌ **Bad:**
```typescript
import { View } from 'react-native';
import type { ImageStyle } from 'react-native';
```

**Why:** Inline type imports reduce line count while maintaining type-only semantics.

## Platform-Specific Imports

Use platform-specific file extensions instead of conditional imports.

✅ **Good:**
```typescript
// File structure:
// libs/navigation/useNavigation.ts - Interface
// libs/navigation/useNavigation.rnsm.ts - React Native impl
// libs/navigation/useNavigation.web.ts - Web impl

// Usage:
import { useNavigation } from '@libs/navigation';
```

❌ **Bad:**
```typescript
import { Platform } from 'react-native';

const useNavigation =
  Platform.OS === 'ios'
    ? require('./useNavigation.ios').useNavigation
    : require('./useNavigation.android').useNavigation;
```

**Why:** Build tools automatically select the correct file, eliminating runtime overhead.

### Platform Extension Priority

Metro resolves files in this order:
1. `{filename}.{platform}.{ext}` (e.g., `Button.ios.tsx`)
2. `{filename}.native.{ext}` (React Native)
3. `{filename}.rnsm.{ext}` (RNSM modules)
4. `{filename}.{ext}` (fallback)

## Testing Imports

Test files follow the same rules with testing libraries first.

```typescript
// Group 1: React testing libraries
import { render, screen, fireEvent } from '@testing-library/react-native';

// Group 2: External libraries
import { QueryClientProvider } from '@tanstack/react-query';

// Group 3: Test utilities
import { queryClient } from '@libs/query';

// Group 4: Component under test
import { SnapOnboardingScreen } from './SnapOnboardingScreen';

// Group 5: Test data and types
import { SNAP_ONBOARDING_SLIDES } from './constants';
import type { SnapOnboardingSlide } from './types';
```

### Mock Imports

```typescript
// Mocks must be at the top, before imports
jest.mock('@react-navigation/native');

import { renderHook } from '@testing-library/react-native';
import { useNavigation } from './useNavigation';
```

**Why:** Jest requires mocks before imports. ESLint allows this exception.

## Common Mistakes

### ❌ Don't Mix Import Styles

```typescript
// ❌ Bad
import React from 'react';
import { useState } from 'react';
const View = require('react-native').View;

// ✅ Good
import { useState, useEffect } from 'react';
import { View, Text } from 'react-native';
```

**Why:** Mixing styles prevents ESLint auto-fix and bypasses tree-shaking.

### ❌ Don't Skip Blank Lines

```typescript
// ❌ Bad - no separation
import { View } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { useT9n } from '@libs/localization';

// ✅ Good - blank lines between groups
import { View } from 'react-native';

import { useQuery } from '@tanstack/react-query';

import { useT9n } from '@libs/localization';
```

**Why:** Visual separation makes dependencies scannable.

### ❌ Don't Import Unused Dependencies

```typescript
// ❌ Bad - unused imports
import { View, Text, ScrollView, FlatList } from 'react-native';

export const Component = () => (
  <View>
    <Text>Hello</Text>
  </View>
);

// ✅ Good - only what's needed
import { View, Text } from 'react-native';

export const Component = () => (
  <View>
    <Text>Hello</Text>
  </View>
);
```

**Why:** ESLint catches unused imports with `@typescript-eslint/no-unused-vars`.

### ❌ Don't Use Side Effect Imports

```typescript
// ❌ Bad
import './polyfills';

// ✅ Good
import { initializePolyfills } from './polyfills';

initializePolyfills();
```

**Why:** Side effect imports make dependencies unclear and harder to test.

## Automatic Formatting

### ESLint Auto-fix

```bash
# Auto-fix import ordering
yarn lint --fix

# Check TypeScript
yarn typecheck
```

### IDE Integration

**VSCode** (`.vscode/settings.json`):
```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.formatOnSave": true
}
```

**Why:** Automatic formatting prevents manual organization and reduces review friction.

## ESLint Rules Reference

| Rule | Purpose |
|------|---------|
| `import/order` | Enforce import ordering with path groups |
| `import/no-default-export` | Prevent default exports |
| `@typescript-eslint/consistent-type-imports` | Use `import type` for types |
| `no-restricted-imports` | Prevent deep imports |
| `@typescript-eslint/no-unused-vars` | Remove unused imports |

## Quick Reference

**Import Order:**
1. React/React Native
2. External libraries
3. Internal aliases (@libs, @modules, @data-access, @zest)
4. Parent/sibling imports
5. Type imports (last)

**Export Rules:**
- ✅ Always use named exports
- ❌ Never use default exports
- ✅ Use `export type` for types
- ✅ Use barrel exports (index.ts)

**Commands:**
```bash
yarn lint --fix      # Auto-fix imports
yarn typecheck       # Check TypeScript
```

## Additional Resources

For detailed examples and patterns, see:
- [references/examples.md](references/examples.md) - Real import/export examples
- [references/patterns.md](references/patterns.md) - Import patterns and anti-patterns
