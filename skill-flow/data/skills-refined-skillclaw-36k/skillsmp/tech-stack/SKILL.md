---
name: tech-stack
description: "WHAT: React Native tech stack reference with specific library versions. WHEN: choosing libraries, checking versions, adding dependencies. KEYWORDS: tech stack, versions, zustand, tanstack query, apollo, zest, react navigation, jest, i18next."
---

# Tech Stack

## Core Principles

**Always use Zest Design System (@zest/react-native 1.3.1).** All UI components must use Zest - it's mandatory, not optional. Never implement custom buttons, inputs, or typography. Zest provides useZestTheme and useZestStyles hooks for styling.

**Always use specified library versions.** The tech stack defines exact versions for all dependencies. Never upgrade libraries independently. Version consistency prevents conflicts across the monorepo.

**Always prefer Zustand for client state, TanStack Query for server state.** Zustand (5.0.3) handles UI state, selections, and app state. TanStack Query (5.59.16) handles REST API caching, mutations, and loading states. Apollo Client (3.13.6) handles GraphQL operations when schema is available.

**Always consult tech-stack before adding new dependencies.** The tech stack is the authoritative reference. Don't add alternative libraries (e.g., Redux, Mobx, React Query alternatives) without tech lead approval. Architecture decisions must align with existing choices.

**Why**: Consistent tech stack ensures library compatibility, reduces bundle size through shared dependencies, enables code reuse across features, maintains architectural consistency, and simplifies maintenance through standardized patterns.

## When to Use This Skill

Use this reference when:

- Choosing libraries for new features
- Installing dependencies for components
- Upgrading existing dependencies
- Resolving library version conflicts
- Implementing state management (Zustand vs TanStack Query decision)
- Selecting UI components (always Zest)
- Setting up testing (Jest + @testing-library/react-native)
- Adding internationalization (i18next)
- Implementing analytics (OpenTelemetry)
- Choosing animation libraries (react-native-reanimated)
- Integrating with native code (iOS/Android patterns)

## Application Framework

### React Native & TypeScript

The project uses React Native 0.75.4 with TypeScript 5.1.6 in strict mode.

```json
{
  "dependencies": {
    "react-native": "0.75.4",
    "typescript": "5.1.6"
  },
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "noImplicitAny": true
  }
}
```

**Why**: React Native 0.75.4 provides cross-platform mobile support. TypeScript 5.1.6 strict mode enforces type safety. Metro bundler handles asset bundling. React Native Builder Bob 0.30.2 builds native modules.

### Build System

Yarn 4.5.0 with Yarn Workspaces for monorepo management. Turbo 2.5.6 for build orchestration.

```json
{
  "packageManager": "yarn@4.5.0",
  "devDependencies": {
    "turbo": "2.5.6"
  }
}
```

**Why**: Yarn Workspaces enable monorepo with shared dependencies. Turbo provides incremental builds and caching. Node.js 22+ LTS managed via nvm ensures consistent environment.

## State Management

### Client State: Zustand 5.0.3

Use Zustand for UI state, selections, forms, and app-level state.

```typescript
import { create } from 'zustand';

const useStore = create<State>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

**When to use Zustand:**
- UI state (modal visibility, drawer state)
- User selections (cart items, filters)
- Form state
- App-level state (authentication status)

**Why**: Zustand 5.0.3 provides simple, performant client state. Shallow selectors prevent unnecessary re-renders. No providers needed.

### Server State: TanStack Query 5.59.16

Use TanStack Query for REST API data fetching, caching, and mutations.

```typescript
import { useQuery, useMutation } from '@tanstack/react-query';

const { data, isLoading, error } = useQuery({
  queryKey: ['recipes'],
  queryFn: fetchRecipes,
});

const mutation = useMutation({
  mutationFn: createRecipe,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['recipes'] }),
});
```

**When to use TanStack Query:**
- REST API data fetching
- Server state caching
- Loading and error states
- Optimistic updates
- Pagination and infinite scroll

**Why**: TanStack Query 5.59.16 handles server state, caching, and background refetching automatically. Replaces manual loading state management.

### GraphQL State: Apollo Client 3.13.6

Use Apollo Client for GraphQL operations when schema is available.

```typescript
import { useQuery, useMutation } from '@apollo/client';
import { GET_RECIPES } from './queries.graphql';

const { data, loading, error } = useQuery(GET_RECIPES);

const [createRecipe] = useMutation(CREATE_RECIPE, {
  refetchQueries: [GET_RECIPES],
});
```

**When to use Apollo Client:**
- GraphQL API operations
- Schema-driven data fetching
- GraphQL subscriptions
- Normalized caching

**Why**: Apollo Client 3.13.6 provides GraphQL-specific features like normalized cache, subscriptions, and schema validation.

## UI & Design System

### Zest Design System (MANDATORY)

Always use @zest/react-native 1.3.1 for all UI components.

```typescript
import { Button, Text, Icon, useZestTheme, useZestStyles } from '@zest/react-native';

const Component = () => {
  const theme = useZestTheme();
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      <Text type="headline-md">Hello Zest</Text>
      <Button variant="primary" onPress={onPress}>
        Click me
      </Button>
      <Icon icon="CloseOutline24" altText="Close" />
    </View>
  );
};
```

**Zest components (use these):**
- Button (variants: primary, secondary, tertiary)
- Text (typography types: headline-md, body-md-regular)
- Icon (24px and 16px sizes)
- IconButton (clickable icons)
- InputField (form inputs)
- Card, Badge, Tag, InlineMessage
- useZestTheme (access theme tokens)
- useZestStyles (themed styling)

**Why**: Zest 1.3.1 ensures brand consistency, accessibility compliance, and design system alignment. Mandatory across all features.

### Navigation

Use @react-navigation/native 7.0.13 with native-stack 7.1.14.

```typescript
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

<Stack.Navigator>
  <Stack.Screen name="Home" component={HomeScreen} />
  <Stack.Screen name="Details" component={DetailsScreen} />
</Stack.Navigator>
```

**Why**: React Navigation 7.0.13 provides native-feeling navigation. Native stack navigator uses native transitions.

### Animations

Use react-native-reanimated 3.16.7 for animations.

```typescript
import Animated, { useSharedValue, useAnimatedStyle, withTiming } from 'react-native-reanimated';

const Component = () => {
  const opacity = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: withTiming(opacity.value, { duration: 300 }),
  }));

  return <Animated.View style={animatedStyle}>Content</Animated.View>;
};
```

**Why**: Reanimated 3.16.7 runs animations on UI thread for 60fps performance. Preferred over React Native Animated API.

## Testing

### Jest & Testing Library

Use Jest 29.7.0 with @testing-library/react-native 12.9.0.

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';

describe('<Component />', () => {
  it('renders correctly', () => {
    render(<Component />);
    expect(screen.getByText('Hello')).toBeTruthy();
  });

  it('handles press', () => {
    const onPress = jest.fn();
    render(<Component onPress={onPress} />);
    fireEvent.press(screen.getByTestId('button'));
    expect(onPress).toHaveBeenCalled();
  });
});
```

**Why**: Jest 29.7.0 provides fast test execution. Testing Library 12.9.0 encourages accessibility-first testing patterns.

## Localization

### i18next

Use i18next 24.2.1 with react-i18next 15.4.0 for internationalization.

```typescript
import { useT9n } from '@libs/localization';

const Component = () => {
  const { translateRaw } = useT9n('feature-name');

  return (
    <Text>{translateRaw('feature.screen.title')}</Text>
  );
};
```

**Why**: i18next 24.2.1 provides comprehensive internationalization. Namespace-based organization prevents key collisions.

## Observability

### OpenTelemetry

Use OpenTelemetry 2.0.1 for distributed tracing.

```typescript
import { useTracer } from '@libs/telemetry';

const Component = () => {
  const { createEventSpan } = useTracer();

  const handleAction = () => {
    createEventSpan('user_action', { userId: user.id });
  };
};
```

**Why**: OpenTelemetry 2.0.1 provides vendor-neutral tracing. Distributed tracing across mobile and backend.

## Validation & Utilities

### Schema Validation

Use zod 3.23.8 for runtime schema validation.

```typescript
import { z } from 'zod';

const RecipeSchema = z.object({
  id: z.string(),
  title: z.string(),
  servings: z.number().positive(),
});

const recipe = RecipeSchema.parse(data);
```

**Why**: zod 3.23.8 provides TypeScript-first schema validation. Type inference from schemas.

### Utilities

- **lodash 4.17.21** - Utility functions (map, filter, debounce)
- **immer 10.1.1** - Immutable state updates
- **date-fns 4.1.0** - Date manipulation and formatting

## Content Rendering

### HTML Rendering

Use react-native-render-html 6.3.4 with sanitize-html 2.17.0.

```typescript
import { RenderSanitizedHTML } from '@libs/render-sanitized-html';

<RenderSanitizedHTML
  source={{ html: '<p>Hello <strong>World</strong></p>' }}
/>
```

**Why**: react-native-render-html 6.3.4 renders HTML in React Native. sanitize-html 2.17.0 prevents XSS attacks.

## Platform Integration

### Device APIs

- **react-native-device-info 14.0.4** - Device information (model, OS version)
- **react-native-safe-area-context 4.14.1** - Safe area insets
- **react-native-mmkv 2.12.2** - Fast key-value storage

### Native Modules

- **iOS Integration:** Xcode, Swift interop, XCFramework builds
- **Android Integration:** Android Studio, Kotlin/Java interop, Gradle AAR publishing

## Code Quality

### Linting & Formatting

- **ESLint 8.51.0** - Code linting with TypeScript rules
- **Prettier 3.0.3** - Code formatting
- **Husky 9.1.7** - Git hooks
- **lint-staged 15.2.10** - Pre-commit linting

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\"",
    "typecheck": "tsc --noEmit"
  }
}
```

**Why**: Consistent code style across monorepo. TypeScript strict mode catches errors at compile time.

## External Services

### Marketing & Analytics

- **@iterable/react-native-sdk 2.0.2** - Marketing automation
- **Cloudinary** - Image optimization (custom lib)
- **@react-native-cookies/cookies 6.2.1** - Cookie management
- **react-native-webview 13.15.0** - WebView support

## Build & Deployment

### Code Generation

- **Plop 4.0.1** - Component scaffolding
- **@graphql-codegen/cli 5.0.5** - GraphQL type generation
- **quicktype 23.0.170** - JSON to TypeScript

### CI/CD

- **GitHub Actions** - Continuous integration
- **Bitrise** - Mobile-specific CI/CD (bitrise.yml)
- **Quality Gates:** ESLint, Prettier, TypeScript, Jest

## Version Management

**Never upgrade libraries independently.** All version upgrades must be coordinated across:
- Monorepo packages
- Shell app dependencies
- Feature module dependencies
- Native iOS/Android dependencies

**How to check versions:**
```bash
# Check installed versions
yarn why <package-name>

# Check for updates (don't auto-upgrade)
yarn outdated

# Verify monorepo consistency
yarn workspaces list
```

## Common Mistakes to Avoid

❌ **Don't use alternative state management**:

```typescript
// ❌ Wrong - using Redux, Mobx, or other alternatives
import { createStore } from 'redux';

// ❌ Wrong - custom state solution
const [state, setState] = useState();
```

**Why**: Project uses Zustand + TanStack Query. Alternative state libraries add bundle size and architectural inconsistency.

✅ **Do use Zustand and TanStack Query**:

```typescript
// ✅ Correct - Zustand for client state
import { create } from 'zustand';

// ✅ Correct - TanStack Query for server state
import { useQuery } from '@tanstack/react-query';
```

❌ **Don't implement custom UI components**:

```typescript
// ❌ Wrong - custom button
const CustomButton = ({ children, onPress }) => (
  <TouchableOpacity onPress={onPress}>
    <Text>{children}</Text>
  </TouchableOpacity>
);
```

**Why**: Zest Design System is mandatory. Custom components break brand consistency and accessibility.

✅ **Do use Zest components**:

```typescript
// ✅ Correct - Zest Button
import { Button } from '@zest/react-native';

<Button variant="primary" onPress={onPress}>
  {children}
</Button>
```

❌ **Don't add dependencies without consulting tech-stack**:

```bash
# ❌ Wrong - adding alternative libraries
yarn add axios  # Use TanStack Query instead
yarn add moment  # Use date-fns 4.1.0 instead
yarn add react-redux  # Use Zustand 5.0.3 instead
```

**Why**: Tech stack defines approved libraries. Alternatives create duplication and version conflicts.

✅ **Do use tech-stack approved libraries**:

```typescript
// ✅ Correct - approved libraries
import { useQuery } from '@tanstack/react-query';  // Server state
import { format } from 'date-fns';  // Date formatting
import { create } from 'zustand';  // Client state
```

❌ **Don't upgrade versions independently**:

```bash
# ❌ Wrong - upgrading single library
yarn add react-native@latest
```

**Why**: Version upgrades affect monorepo stability. Must be coordinated across all packages.

✅ **Do coordinate version upgrades**:

```bash
# ✅ Correct - consult with tech lead first
# Check current version in tech-stack
# Verify compatibility with other dependencies
# Update across all monorepo packages
```

## Quick Reference

**State Management:**
- Client state → Zustand 5.0.3
- Server state (REST) → TanStack Query 5.59.16
- Server state (GraphQL) → Apollo Client 3.13.6

**UI Components:**
- Design system → @zest/react-native 1.3.1 (MANDATORY)
- Navigation → @react-navigation/native 7.0.13
- Animations → react-native-reanimated 3.16.7

**Testing:**
- Framework → Jest 29.7.0
- Library → @testing-library/react-native 12.9.0

**Internationalization:**
- Library → i18next 24.2.1

**Observability:**
- Tracing → OpenTelemetry 2.0.1

**Validation:**
- Schema → zod 3.23.8

**Utilities:**
- Functions → lodash 4.17.21
- Immutability → immer 10.1.1
- Dates → date-fns 4.1.0

**Content:**
- HTML → react-native-render-html 6.3.4
- Sanitization → sanitize-html 2.17.0

**Platform:**
- Device info → react-native-device-info 14.0.4
- Safe areas → react-native-safe-area-context 4.14.1
- Storage → react-native-mmkv 2.12.2

**Code Quality:**
- Linting → ESLint 8.51.0
- Formatting → Prettier 3.0.3
- Type checking → TypeScript 5.1.6 strict mode

**Full tech stack reference**: `previous-standards/global/tech-stack.md`
