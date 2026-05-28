# Import and Export Patterns

Implementation patterns and anti-patterns for organizing TypeScript imports and exports.

## Pattern: ESLint-Enforced Import Ordering

Imports are automatically organized by ESLint in groups with blank lines between them.

✅ **Good:**
```typescript
// Group 1: React/React Native
import { useEffect, useState } from 'react';
import { View, ScrollView } from 'react-native';

// Group 2: External libraries
import { useQuery } from '@tanstack/react-query';

// Group 3: Internal aliases (alphabetized)
import { useRecipeData } from '@data-access/query';
import { useT9n } from '@libs/localization';

// Group 4: Zest design system
import { Button, Text } from '@zest/react-native';

// Group 5: Local imports
import { FAQ_ITEMS } from './constants';

// Group 6: Type imports (always last)
import type { FaqItem } from './types';
```

❌ **Bad:**
```typescript
// No grouping, mixed order
import { FAQ_ITEMS } from './constants';
import { View } from 'react-native';
import type { FaqItem } from './types';
import { useT9n } from '@libs/localization';
import { useQuery } from '@tanstack/react-query';
```

**Why:** Automatic organization ensures consistency, makes dependencies scannable, and reduces cognitive load when reviewing imports.

**ESLint Rule:**
```javascript
'import/order': [
  'error',
  {
    groups: [
      'builtin',
      'external',
      'internal',
      'parent',
      'sibling',
      'index',
      'type',
    ],
    pathGroups: [
      { pattern: 'react', group: 'builtin', position: 'before' },
      { pattern: 'react-native', group: 'builtin', position: 'before' },
      { pattern: '@libs/**', group: 'internal' },
      { pattern: '@modules/**', group: 'internal' },
      { pattern: '@data-access/**', group: 'internal' },
      { pattern: '@zest/**', group: 'internal', position: 'after' },
    ],
    'newlines-between': 'always',
    alphabetize: { order: 'asc', caseInsensitive: true },
  },
],
```

## Pattern: Named Exports Only

Always use named exports, never default exports.

✅ **Good:**
```typescript
// Component exports
export const UserProfile = ({ user }: UserProps) => {
  return <View>...</View>;
};

export const UserAvatar = ({ avatarUrl }: AvatarProps) => {
  return <Image source={{ uri: avatarUrl }} />;
};

// Function exports
export const calculateTotal = (items: Item[]) => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

// Type exports
export type { UserProps, AvatarProps, Item };
```

❌ **Bad:**
```typescript
// Default exports
const UserProfile = () => <View />;
export default UserProfile;

// Mixed default and named
export default UserProfile;
export { UserAvatar };

// Default with rename
const Profile = () => <View />;
export { Profile as default };
```

**Why:** Named exports provide:
- **Better IDE support**: Autocomplete, refactoring, find-all-references work correctly
- **Explicit imports**: Can't arbitrarily rename at import site
- **Better tree-shaking**: Bundlers can remove unused exports more reliably
- **No naming conflicts**: Import name must match export name
- **Easier refactoring**: Renaming in one place updates all imports

**ESLint Rule:**
```javascript
'import/no-default-export': 'error',
```

## Pattern: Type-Only Imports

Use `import type` for type-only imports to reduce bundle size.

✅ **Good:**
```typescript
// Dedicated type imports
import type { User, Subscription } from '@data-access/graphql';
import type { ComponentProps } from './types';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

// Inline type imports (when importing values too)
import { useQuery, type UseQueryOptions } from '@tanstack/react-query';
import { View, type ViewStyle, type ImageStyle } from 'react-native';
```

❌ **Bad:**
```typescript
// Importing types as values
import { User, Subscription } from '@data-access/graphql';
import { ComponentProps } from './types';

// Separate imports when could be combined
import { useQuery } from '@tanstack/react-query';
import type { UseQueryOptions } from '@tanstack/react-query';
```

**Why:** Type-only imports are erased at compile time, reducing JavaScript bundle size. TypeScript can optimize builds by skipping type-only modules.

**ESLint Rule:**
```javascript
'@typescript-eslint/consistent-type-imports': [
  'error',
  {
    prefer: 'type-imports',
    fixStyle: 'inline-type-imports',
  },
],
```

## Pattern: Path Aliases Over Relative Imports

Use configured path aliases instead of relative paths for cross-module imports.

✅ **Good:**
```typescript
import { ScreenCommonProvider } from '@entry-providers';
import { AuthForm } from '@features/auth-form';
import { useSignIn } from '@operations/auth';
import { signIn } from '@data-access/native/auth';
import { usePerformanceTracker } from '@libs/observability';
import { Button } from '@zest/react-native';
```

❌ **Bad:**
```typescript
// Deep relative paths
import { ScreenCommonProvider } from '../../../entry-providers';
import { AuthForm } from '../../features/auth-form';
import { useSignIn } from '../operations/auth';

// Mixing relative and alias imports
import { AuthForm } from '@features/auth-form';
import { Button } from '../../zest/react-native';
```

**Why:** Path aliases:
- Remain stable during refactoring (file moves don't break imports)
- Are easier to read (clear tier boundaries)
- Are easier to search (consistent paths)
- Prevent errors from incorrect relative path depths

**Exception:** Use relative imports within the same module:
```typescript
// Within src/features/auth-form/
import { FormInput } from './components/FormInput';
import { useFormValidation } from './hooks/useFormValidation';
import { FORM_CONSTANTS } from './constants';
```

## Pattern: Barrel Exports for Public APIs

Use index.ts to export public APIs, hiding internal structure.

✅ **Good:**
```typescript
// src/features/product-card-feature/index.ts
export { ProductCard } from './ProductCard';
export { LoadingProductCard } from './variants/loading';
export type { ProductCardProps, ProductVariant } from './types';

// Usage
import { ProductCard, LoadingProductCard } from '@features/product-card-feature';
```

❌ **Bad:**
```typescript
// Direct imports bypassing barrel
import { ProductCard } from '@features/product-card-feature/ProductCard';
import { LoadingProductCard } from '@features/product-card-feature/variants/loading/LoadingProductCard';

// No barrel export - exposing internal structure
import { ProductCard } from '@features/product-card-feature/src/components/ProductCard';
```

**Why:** Barrel exports:
- Hide internal structure (can refactor without breaking imports)
- Provide a curated public API
- Make imports cleaner and shorter
- Enable deprecation of internal exports

**Pattern for Module Barrels:**
```typescript
// src/modules/social-recipe-bridge/index.ts
export * from './stacks';
export * from './screens';
export * from './hooks';
export type * from './types';
```

**Pattern for Screens Directory with Plop:**
```typescript
// src/modules/social-recipe-bridge/screens/index.ts
export * from './cookbook-faq';
export * from './onboarding';
export * from './add-recipe-link-drawer';
// @PLOP_INSERT_SCREEN_EXPORT
```

## Pattern: Grouped Related Imports

Group related imports from the same package on a single line.

✅ **Good:**
```typescript
// React hooks grouped
import { useState, useEffect, useMemo, useCallback, useRef } from 'react';

// React Native components grouped
import { View, ScrollView, TouchableOpacity, FlatList, Image } from 'react-native';

// Zest components grouped
import { Button, Text, Input, Card, useZestStyles } from '@zest/react-native';

// Multi-line when many imports (4+)
import {
  useReactivationEligibility,
  ReactivationBannerFeature,
  ReactivationBannerProvider,
  useReactivationHomeScreenStyle,
  GlobalReactivationButtonWithContext,
} from '@features/reactivation-banner-feature';
```

❌ **Bad:**
```typescript
// One import per line
import { View } from 'react-native';
import { ScrollView } from 'react-native';
import { TouchableOpacity } from 'react-native';
import { FlatList } from 'react-native';

// Ungrouped with duplicated sources
import { Button } from '@zest/react-native';
import { Text } from '@zest/react-native';
import { Input } from '@zest/react-native';
```

**Why:** Grouped imports:
- Reduce line count
- Clarify package dependencies
- Make it easier to see all imports from a package
- Reduce merge conflicts (fewer lines changed)

## Anti-Pattern: Mixed Import Styles

Don't mix ESM imports, CommonJS requires, and default imports.

❌ **Bad:**
```typescript
// Mixing styles
import React from 'react';
import { useState } from 'react';
const View = require('react-native').View;
import type { ViewProps } from 'react-native';

// Dynamic requires
const Component = condition
  ? require('./ComponentA').ComponentA
  : require('./ComponentB').ComponentB;
```

✅ **Good:**
```typescript
// Consistent ESM imports
import { useState, useEffect } from 'react';
import { View, Text } from 'react-native';
import type { ViewProps, TextProps } from 'react-native';

// For dynamic imports, use ESM
const { ComponentA } = await import('./ComponentA');
```

**Why:** Mixing styles:
- Prevents ESLint auto-fix from working
- Bypasses tree-shaking optimizations
- Makes code harder to understand
- Can cause subtle bugs with module resolution

## Anti-Pattern: Default Exports

Never use default exports in React Native projects.

❌ **Bad:**
```typescript
// Default export
const UserProfile = ({ user }: UserProps) => {
  return <View>...</View>;
};
export default UserProfile;

// Default with rename
export { UserProfile as default };

// Mixed default and named
export default UserProfile;
export { UserAvatar };
```

✅ **Good:**
```typescript
// Named exports only
export const UserProfile = ({ user }: UserProps) => {
  return <View>...</View>;
};

export const UserAvatar = ({ avatarUrl }: AvatarProps) => {
  return <Image source={{ uri: avatarUrl }} />;
};
```

**Why:** Default exports:
- Allow arbitrary renaming at import site (confusing)
- Break IDE refactoring tools
- Make search/replace harder
- Don't work well with re-exports
- Reduce tree-shaking effectiveness

## Anti-Pattern: Deep Imports

Don't import from internal modules, use public APIs.

❌ **Bad:**
```typescript
// Deep imports bypassing public API
import { helper } from '@libs/localization/utils/helper';
import { parser } from '@data-access/query/helpers/parser';
import { validator } from '@features/auth-form/components/Input/validators/email';

// Importing from sibling modules
import { RecipeCard } from '@modules/social-recipe-bridge/components/RecipeCard';
```

✅ **Good:**
```typescript
// Import from public APIs (barrel exports)
import { helper } from '@libs/localization';
import { parser } from '@data-access/query';
import { emailValidator } from '@features/auth-form';

// Extract reusable component to features
import { RecipeCard } from '@features/recipe-card';
```

**Exceptions** (one level allowed):
```typescript
// Allowed: One level for organized data access
import { useCustomerBalance } from '@data-access/query/payments';
import { signIn } from '@data-access/native/auth';
import { gql } from '@data-access/graphql';

// Allowed: Native modules
import { sendEvent } from '@libs/native-modules/events';
```

**Why:** Deep imports:
- Bypass public APIs (coupling to internal structure)
- Break when internal structure changes
- Violate encapsulation
- Make refactoring harder

**ESLint Rule:**
```javascript
'no-restricted-imports': [
  'error',
  {
    patterns: [
      {
        group: ['@libs/*/*/*'],
        message: 'Deep imports not allowed. Use public API from @libs/*',
      },
      {
        group: ['@data-access/query/*/*/*'],
        message: 'Deep imports not allowed. Use @data-access/query/*',
      },
    ],
  },
],
```

## Anti-Pattern: Side Effect Imports

Avoid imports that execute code on import.

❌ **Bad:**
```typescript
// Side effect import
import './polyfills';
import './register-handlers';

// Implicit execution
import 'react-native-gesture-handler';

// Global state modification
import './configure-analytics';
```

✅ **Good:**
```typescript
// Explicit initialization
import { initializePolyfills } from './polyfills';
import { registerHandlers } from './register-handlers';
import { configureAnalytics } from './configure-analytics';

// Call explicitly in entry point
initializePolyfills();
registerHandlers();
configureAnalytics();
```

**Why:** Side effect imports:
- Make dependencies unclear
- Hard to control execution order
- Difficult to test (can't mock)
- Can cause initialization bugs
- Make tree-shaking impossible

**Exception:** Required by library (e.g., react-native-gesture-handler requires side effect import):
```typescript
// Allowed: Required by library
import 'react-native-gesture-handler';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
```

## Anti-Pattern: Unused Imports

Don't leave unused imports in code.

❌ **Bad:**
```typescript
// Unused imports
import { View, Text, ScrollView, FlatList, Image, Button } from 'react-native';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useNavigation } from '@libs/navigation';

export const Component = () => (
  <View>
    <Text>Hello</Text>
  </View>
);
```

✅ **Good:**
```typescript
// Only what's needed
import { View, Text } from 'react-native';

export const Component = () => (
  <View>
    <Text>Hello</Text>
  </View>
);
```

**Why:** Unused imports:
- Increase bundle size unnecessarily
- Clutter the code
- Confuse readers about dependencies
- Slow down compilation

**ESLint Rule:**
```javascript
'@typescript-eslint/no-unused-vars': [
  'error',
  {
    argsIgnorePattern: '^_',
    varsIgnorePattern: '^_',
    ignoreRestSiblings: true,
  },
],
```

## Anti-Pattern: Missing Blank Lines Between Groups

Don't skip blank lines between import groups.

❌ **Bad:**
```typescript
// No separation between groups
import { View } from 'react-native';
import { useQuery } from '@tanstack/react-query';
import { useT9n } from '@libs/localization';
import { Button } from '@zest/react-native';
import { FAQ_ITEMS } from './constants';
```

✅ **Good:**
```typescript
// Blank lines between groups
import { View } from 'react-native';

import { useQuery } from '@tanstack/react-query';

import { useT9n } from '@libs/localization';

import { Button } from '@zest/react-native';

import { FAQ_ITEMS } from './constants';
```

**Why:** Visual separation:
- Makes dependencies scannable at a glance
- Groups related concerns
- Follows ESLint import/order conventions
- Reduces cognitive load when reading imports

## Platform-Specific Import Pattern

Use platform-specific file extensions instead of conditional imports.

✅ **Good:**
```typescript
// File structure:
// libs/navigation/useNavigation.ts       - Interface/common
// libs/navigation/useNavigation.rnsm.ts  - React Native impl
// libs/navigation/useNavigation.web.ts   - Web impl

// Usage (Metro resolves automatically):
import { useNavigation } from '@libs/navigation';
```

❌ **Bad:**
```typescript
// Conditional imports
import { Platform } from 'react-native';

const useNavigation =
  Platform.OS === 'ios'
    ? require('./useNavigation.ios').useNavigation
    : require('./useNavigation.android').useNavigation;

// Dynamic platform checks
import { useNavigation } from Platform.select({
  ios: () => require('./useNavigation.ios'),
  android: () => require('./useNavigation.android'),
})();
```

**Why:** Platform-specific extensions:
- Build tools automatically select correct file
- Eliminates runtime overhead
- Better tree-shaking (unused platforms excluded from bundle)
- Clearer separation of platform code
- No conditional logic needed

**Metro Resolution Order:**
1. `{filename}.{platform}.{ext}` (e.g., `Button.ios.tsx`)
2. `{filename}.native.{ext}` (React Native)
3. `{filename}.rnsm.{ext}` (RNSM modules)
4. `{filename}.{ext}` (fallback)

## Testing Import Pattern

Test files follow the same rules with testing libraries first.

✅ **Good:**
```typescript
// Group 1: React testing libraries
import { render, screen, fireEvent } from '@testing-library/react-native';

// Group 2: External libraries
import { QueryClientProvider } from '@tanstack/react-query';

// Group 3: Test utilities
import { createMockQueryClient } from '@libs/query/test-utils';

// Group 4: Component under test
import { SnapOnboardingScreen } from './SnapOnboardingScreen';

// Group 5: Test data and types
import { SNAP_ONBOARDING_SLIDES } from './constants';
import type { SnapOnboardingSlide } from './types';
```

❌ **Bad:**
```typescript
// Mixed order in tests
import { SnapOnboardingScreen } from './SnapOnboardingScreen';
import { render } from '@testing-library/react-native';
import type { SnapOnboardingSlide } from './types';
import { createMockQueryClient } from '@libs/query/test-utils';
```

**Mock Imports Exception:**
```typescript
// Mocks must be at the top, before imports
jest.mock('@react-navigation/native');
jest.mock('@libs/analytics');

// Then regular imports
import { renderHook } from '@testing-library/react-native';
import { useNavigation } from './useNavigation';
```

**Why:** Jest requires mocks before imports. ESLint allows this exception with:
```javascript
'import/first': ['error', 'disable-absolute-first'],
```

## GraphQL gql Import Pattern

Always import `gql` from the data-access layer, not directly from Apollo.

✅ **Good:**
```typescript
import { gql } from '@data-access/graphql';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
    }
  }
`;
```

❌ **Bad:**
```typescript
// Direct import from Apollo
import { gql } from '@apollo/client';

// Mixed imports
import { gql } from '@apollo/client';
import { useQuery } from '@data-access/graphql';
```

**Why:** Centralizing GraphQL imports:
- Enables consistent configuration (custom scalars, directives)
- Makes mocking easier in tests
- Allows version upgrades in one place
- Enforces architectural boundaries

## Automatic Formatting

Use ESLint auto-fix to maintain import ordering automatically.

```bash
# Auto-fix import ordering
yarn lint --fix

# Check TypeScript
yarn typecheck

# Both in CI
yarn lint && yarn typecheck
```

**VSCode Integration** (`.vscode/settings.json`):
```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.formatOnSave": true
}
```

**Why:** Automatic formatting:
- Prevents manual organization errors
- Reduces review friction
- Enforces consistency across team
- Saves time during development
- Catches mistakes before commit

## Summary

**Always:**
- ✅ Use ESLint-enforced import ordering
- ✅ Use named exports only
- ✅ Use `import type` for types
- ✅ Use path aliases over relative imports
- ✅ Use barrel exports (index.ts)
- ✅ Group related imports from same package
- ✅ Include blank lines between groups

**Never:**
- ❌ Use default exports
- ❌ Mix import styles (ESM/CommonJS)
- ❌ Use deep imports (bypass public APIs)
- ❌ Use side effect imports
- ❌ Leave unused imports
- ❌ Skip blank lines between groups
- ❌ Import `gql` from `@apollo/client`
