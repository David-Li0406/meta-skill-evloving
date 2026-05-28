---
name: platform-detection
description: "WHAT: Platform detection with PlatformIs utility and Platform.select. WHEN: conditional rendering, platform-specific values, detecting iOS vs Android. KEYWORDS: platform, PlatformIs, Platform.OS, Platform.select, ios, android, conditional, detection, version."
---

# Platform Detection

## Core Principles

**Use PlatformIs utility for readable platform checks.** The `PlatformIs.ios()` and `PlatformIs.android()` functions are more readable than `Platform.OS === 'ios'` and provide consistent API across the codebase with type safety.

**Use Platform.OS for direct comparisons.** When PlatformIs is unavailable, use `Platform.OS === 'ios'` or `Platform.OS === 'android'` with strict equality (===) and lowercase platform strings.

**Use Platform.select for platform-specific values.** Platform.select provides type-safe selection of values based on platform, avoiding repetitive conditional logic for constants, styles, or configuration.

**Use platform-specific file extensions for major differences.** Files with `.ios.tsx` or `.android.tsx` extensions are automatically loaded by platform, completely separating platform-specific implementations.

**Why**: Platform detection enables conditional behavior, UI adjustments, and API usage tailored to iOS and Android. Following these patterns ensures readable, maintainable, and testable cross-platform code.

## When to Use This Skill

Use these patterns when:

- Rendering platform-specific components or UI
- Implementing platform-specific business logic
- Using platform-specific APIs or native modules
- Setting platform-specific configuration values
- Defining platform-specific styles or dimensions
- Conditionally importing platform-specific modules
- Testing platform-specific code paths
- Supporting platform-specific features
- Handling platform-specific edge cases
- Creating platform-specific file implementations

## PlatformIs Utility

### PlatformIs Implementation

```typescript
// libs/utils/platform.ts
import { Platform } from 'react-native';

export const PlatformIs = {
  android: (): boolean => Platform.OS === 'android',
  ios: (): boolean => Platform.OS === 'ios',
} as const;
```

**Why**: Centralized platform detection prevents typos, provides consistent boolean checks, and is easier to mock in tests.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/utils/platform.ts:1`

### Using PlatformIs

```typescript
import { PlatformIs } from '@libs/utils/platform';

// ✅ Readable boolean check
if (PlatformIs.ios()) {
  return <IOSOnlyFeature />;
}

// ✅ Early return pattern
if (!PlatformIs.android()) {
  return null;
}

return <AndroidOnlyFeature />;
```

**Why**: Function call syntax (`PlatformIs.ios()`) is more readable than string comparison (`Platform.OS === 'ios'`). Boolean return value works naturally in conditionals.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/utils/components/PlatformStatusBar.tsx:1`

### PlatformIs in Component Guards

```typescript
import { PlatformIs } from '@libs/utils/platform';

export const PlatformStatusBar = ({
  barStyle = 'light-content',
  backgroundColor,
}) => {
  const theme = useZestTheme();

  if (!PlatformIs.android()) {
    return null;
  }

  return (
    <StatusBar
      barStyle={barStyle}
      backgroundColor={
        backgroundColor || theme.alias.color.brand.background.default
      }
    />
  );
};
```

**Why**: Early return with `!PlatformIs.android()` prevents Android-only component from rendering on iOS. Clearer intent than nested conditionals.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/utils/components/PlatformStatusBar.tsx:1`

## Platform.OS Direct Comparison

### Platform.OS Boolean Checks

```typescript
import { Platform } from 'react-native';

// ✅ Direct boolean comparison
const isIOS = Platform.OS === 'ios';
const isAndroid = Platform.OS === 'android';

// ✅ Inline conditional
const behavior = Platform.OS === 'ios' ? 'padding' : 'height';

// ✅ Platform-specific constant
export const USE_WEBKIT = Platform.OS === 'ios';
```

**Why**: `Platform.OS === 'ios'` returns boolean directly. Use strict equality (===) and lowercase platform strings ('ios', 'android').

**Production Example**: `git-resources/shared-mobile-modules/src/modules/programs/screens/programs-home/constants.ts:1`

### Platform.OS in JSX

```typescript
import { Platform, KeyboardAvoidingView } from 'react-native';

<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
>
  {children}
</KeyboardAvoidingView>
```

**Why**: Ternary operator with `Platform.OS` comparison provides platform-specific props inline. iOS gets 'padding' behavior, Android gets 'height'.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/edit-recipe/EditRecipeScreen.tsx:288`

### Platform.OS in Constants

```typescript
import { Platform } from 'react-native';
import DeviceInfo from 'react-native-device-info';

export const USE_WEBKIT = Platform.OS === 'ios';

export const APP_VERSION =
  `${DeviceInfo.getReadableVersion()}${[Platform.OS]}` || '1.0.0';
```

**Why**: Platform.OS in string templates for platform-tagged versions. USE_WEBKIT boolean flag simplifies conditional checks throughout codebase.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/programs/screens/programs-home/constants.ts:1`

### Platform.OS in Headers

```typescript
import { setContext } from '@apollo/client/link/context';
import { Platform } from 'react-native';
import DeviceInfo from 'react-native-device-info';

export const apolloHeadersLink = setContext((_, { headers }) => {
  const appName = DeviceInfo.getApplicationName();
  const appVersion = DeviceInfo.getReadableVersion();

  return {
    headers: {
      ...headers,
      ['apollographql-client-name']: appName,
      ['apollographql-client-version']: appVersion,
      ['apollographql-client-platform']: Platform.OS,
    },
  };
});
```

**Why**: Platform.OS string value ('ios' or 'android') used directly in HTTP headers for backend tracking and analytics.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/graphql/links/apolloHeaders.ts:1`

## Platform.select for Values

### Platform.select Basic Usage

```typescript
import { Platform, StyleSheet } from 'react-native';

const HEADER_HEIGHT = Platform.select({
  ios: 44,
  android: 56,
  default: 50,
});

const FONT_FAMILY = Platform.select({
  ios: 'System',
  android: 'Roboto',
  default: 'System',
});

const styles = StyleSheet.create({
  header: {
    height: HEADER_HEIGHT,
    fontFamily: FONT_FAMILY,
  },
});
```

**Why**: `Platform.select` chooses values based on platform in one expression. Type-safe alternative to multiple conditionals. Always include `default` for unknown platforms.

### Platform.select with Styles

```typescript
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
      },
      android: {
        elevation: 5,
      },
    }),
  },
});
```

**Why**: Spread operator with `Platform.select` merges platform-specific style objects. iOS gets shadow properties, Android gets elevation.

### Platform.select with Functions

```typescript
import { Platform } from 'react-native';

const getNavigationOptions = Platform.select({
  ios: () => ({
    headerStyle: { backgroundColor: '#FFFFFF' },
    headerTransparent: false,
  }),
  android: () => ({
    headerStyle: { backgroundColor: '#1A1A1A', elevation: 0 },
  }),
  default: () => ({}),
});

// Call selected function
const options = getNavigationOptions();
```

**Why**: `Platform.select` with functions defers execution until needed. Useful for expensive operations or dynamic values.

## Conditional Rendering Patterns

### Early Return Pattern

```typescript
import { PlatformIs } from '@libs/utils/platform';

const IOSOnlyComponent = () => {
  if (!PlatformIs.ios()) {
    return null;
  }

  return <IOSFeature />;
};
```

**Why**: Early return exits function immediately on wrong platform. Clearer intent than nested conditionals. Guards entire component body.

### Ternary Operator Pattern

```typescript
import { Platform } from 'react-native';

const MyComponent = () => {
  return (
    <View>
      {Platform.OS === 'ios' ? (
        <IOSComponent />
      ) : (
        <AndroidComponent />
      )}
    </View>
  );
};
```

**Why**: Ternary operator provides inline conditional rendering. Works well for small, focused differences between platforms.

### JSX && Pattern

```typescript
import { Platform } from 'react-native';

const MyComponent = () => {
  return (
    <View>
      {Platform.OS === 'android' && <AndroidOnlyFeature />}
      <SharedContent />
    </View>
  );
};
```

**Why**: `&&` operator only renders when condition is true. Concise syntax for optional platform-specific elements.

### Multiple Platform Checks

```typescript
import { PlatformIs } from '@libs/utils/platform';

const MyComponent = () => {
  if (PlatformIs.ios()) {
    return <IOSVersion />;
  }

  if (PlatformIs.android()) {
    return <AndroidVersion />;
  }

  return <DefaultVersion />;
};
```

**Why**: Sequential checks provide clear control flow. Easy to add more platforms. Explicit default case.

## Platform-Specific Files

### File Extensions

React Native automatically loads platform-specific files:

```
MyComponent.tsx        # Shared implementation
MyComponent.ios.tsx    # iOS-specific (auto-loaded on iOS)
MyComponent.android.tsx # Android-specific (auto-loaded on Android)
```

**How it works**:
- Import uses base name: `import { MyComponent } from './MyComponent'`
- iOS loads `MyComponent.ios.tsx` if it exists, otherwise `MyComponent.tsx`
- Android loads `MyComponent.android.tsx` if it exists, otherwise `MyComponent.tsx`
- Webpack/Metro bundler handles resolution automatically

### When to Use Platform-Specific Files

```typescript
// ✅ Good use case: Completely different implementations
// MyComponent.ios.tsx
export const MyComponent = () => {
  return <IOSNativeModule />;
};

// MyComponent.android.tsx
export const MyComponent = () => {
  return <AndroidNativeModule />;
};

// ❌ Bad use case: Only minor prop differences
// Use conditional props instead
<MyComponent behavior={Platform.OS === 'ios' ? 'padding' : 'height'} />
```

**Why**: Platform-specific files are best for fundamentally different implementations. For small differences, use conditional props or Platform.select.

### Platform-Specific Exports

```typescript
// utils.ios.ts
export const getSystemInfo = () => {
  return {
    platform: 'iOS',
    usesWebKit: true,
  };
};

// utils.android.ts
export const getSystemInfo = () => {
  return {
    platform: 'Android',
    usesChrome: true,
  };
};

// MyComponent.tsx - same import for both
import { getSystemInfo } from './utils';
```

**Why**: Platform-specific exports maintain consistent API while providing different implementations. No platform checks needed at call site.

## Platform Version Checks

### Platform.Version Usage

```typescript
import { Platform } from 'react-native';

// iOS version check
if (Platform.OS === 'ios' && Platform.Version >= 14) {
  // Use iOS 14+ features
}

// Android API level check
if (Platform.OS === 'android' && Platform.Version >= 29) {
  // Use Android 10+ (API 29) features
}
```

**Why**: Platform.Version provides OS version (iOS) or API level (Android). Useful for feature detection and API availability checks.

### Combined Platform and Version Checks

```typescript
import { Platform } from 'react-native';

const isModernIOS = Platform.OS === 'ios' && Platform.Version >= 14;
const isModernAndroid = Platform.OS === 'android' && Platform.Version >= 29;

if (isModernIOS || isModernAndroid) {
  // Use modern features
} else {
  // Fall back to older implementation
}
```

**Why**: Boolean constants for combined checks improve readability. Avoid repeating complex conditions.

## Testing Platform-Specific Code

### Mock Platform.OS in Tests

```typescript
import { Platform } from 'react-native';

describe('PlatformComponent', () => {
  const originalOS = Platform.OS;

  afterEach(() => {
    Platform.OS = originalOS; // Always restore
  });

  it('renders iOS version on iOS', () => {
    Platform.OS = 'ios';

    const { getByTestId } = render(<PlatformComponent />);

    expect(getByTestId('ios-feature')).toBeDefined();
  });

  it('renders Android version on Android', () => {
    Platform.OS = 'android';

    const { getByTestId } = render(<PlatformComponent />);

    expect(getByTestId('android-feature')).toBeDefined();
  });
});
```

**Why**: Mocking Platform.OS enables testing both platforms without separate test runs. Always restore original value in `afterEach` to prevent test pollution.

**Production Example**: `git-resources/shared-mobile-modules/src/features/webview/hooks/useWebViewBackHandler.test.ts:1`

### Testing with Platform.select

```typescript
import { Platform } from 'react-native';

describe('platform-specific config', () => {
  const originalOS = Platform.OS;

  afterEach(() => {
    Platform.OS = originalOS;
  });

  it('returns iOS config on iOS', () => {
    Platform.OS = 'ios';

    const config = getConfig();

    expect(config.headerHeight).toBe(44);
    expect(config.fontFamily).toBe('System');
  });

  it('returns Android config on Android', () => {
    Platform.OS = 'android';

    const config = getConfig();

    expect(config.headerHeight).toBe(56);
    expect(config.fontFamily).toBe('Roboto');
  });
});
```

**Why**: Test both branches of Platform.select by mocking Platform.OS. Verify correct values returned for each platform.

## Common Mistakes to Avoid

❌ **Don't use case-sensitive platform strings**:

```typescript
// ❌ Wrong case
if (Platform.OS === 'iOS') {
  // Never matches - Platform.OS is lowercase
}

if (Platform.OS === 'Android') {
  // Never matches - Platform.OS is lowercase
}
```

**Why**: `Platform.OS` returns lowercase strings ('ios', 'android'). Case-sensitive comparison with uppercase ('iOS', 'Android') never matches.

✅ **Do use lowercase platform strings**:

```typescript
// ✅ Correct case
if (Platform.OS === 'ios') {
  // Matches on iOS
}

if (Platform.OS === 'android') {
  // Matches on Android
}
```

**Why**: Lowercase matches actual Platform.OS values. Consistent with React Native conventions.

❌ **Don't use loose equality**:

```typescript
// ❌ Loose equality
if (Platform.OS == 'ios') {
  // Works but discouraged
}
```

**Why**: Loose equality (==) performs type coercion. Inconsistent with TypeScript best practices.

✅ **Do use strict equality**:

```typescript
// ✅ Strict equality
if (Platform.OS === 'ios') {
  // Type-safe comparison
}
```

**Why**: Strict equality (===) ensures type-safe comparison. Prevents unexpected coercion bugs.

❌ **Don't forget to restore Platform.OS in tests**:

```typescript
// ❌ Missing restoration
describe('MyComponent', () => {
  it('renders on iOS', () => {
    Platform.OS = 'ios';
    // Test code
    // Missing afterEach restoration!
  });
});
```

**Why**: Failing to restore Platform.OS pollutes subsequent tests. Next test may run with wrong platform value.

✅ **Do restore Platform.OS in afterEach**:

```typescript
// ✅ Proper restoration
describe('MyComponent', () => {
  const originalOS = Platform.OS;

  afterEach(() => {
    Platform.OS = originalOS;
  });

  it('renders on iOS', () => {
    Platform.OS = 'ios';
    // Test code
  });
});
```

**Why**: `afterEach` restoration ensures clean state for every test. Prevents test pollution.

❌ **Don't overuse platform-specific files**:

```typescript
// ❌ Overkill for minor differences
// Button.ios.tsx
export const Button = ({ title }) => {
  return <TouchableOpacity style={{ padding: 12 }}>{title}</TouchableOpacity>;
};

// Button.android.tsx
export const Button = ({ title }) => {
  return <TouchableOpacity style={{ padding: 10 }}>{title}</TouchableOpacity>;
};
```

**Why**: Platform-specific files duplicate code for trivial differences. Harder to maintain.

✅ **Do use Platform.select for minor differences**:

```typescript
// ✅ Single file with Platform.select
import { Platform, StyleSheet } from 'react-native';

const BUTTON_PADDING = Platform.select({
  ios: 12,
  android: 10,
  default: 10,
});

export const Button = ({ title }) => {
  return (
    <TouchableOpacity style={{ padding: BUTTON_PADDING }}>
      {title}
    </TouchableOpacity>
  );
};
```

**Why**: Single file with Platform.select maintains one implementation. Easier to maintain and understand.

❌ **Don't check platform multiple times for same value**:

```typescript
// ❌ Repetitive checks
<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
  enabled={Platform.OS === 'ios'}
>
```

**Why**: Multiple identical Platform.OS checks are redundant and harder to read.

✅ **Do extract platform boolean once**:

```typescript
// ✅ Extract boolean
const isIOS = Platform.OS === 'ios';

<KeyboardAvoidingView
  behavior={isIOS ? 'padding' : 'height'}
  keyboardVerticalOffset={isIOS ? 90 : 0}
  enabled={isIOS}
>
```

**Why**: Single boolean check improves readability. Consistent value across all uses.

## Quick Reference

**PlatformIs utility**:
```typescript
import { PlatformIs } from '@libs/utils/platform';

if (PlatformIs.ios()) {
  // iOS-specific code
}

if (PlatformIs.android()) {
  // Android-specific code
}
```

**Platform.OS comparison**:
```typescript
import { Platform } from 'react-native';

const isIOS = Platform.OS === 'ios';
const isAndroid = Platform.OS === 'android';
```

**Platform.select for values**:
```typescript
const VALUE = Platform.select({
  ios: 44,
  android: 56,
  default: 50,
});
```

**Early return pattern**:
```typescript
if (!PlatformIs.ios()) {
  return null;
}
```

**Ternary operator**:
```typescript
{Platform.OS === 'ios' ? <IOSComponent /> : <AndroidComponent />}
```

**JSX && pattern**:
```typescript
{Platform.OS === 'android' && <AndroidOnlyFeature />}
```

**Platform-specific files**:
```
MyComponent.tsx         # Shared
MyComponent.ios.tsx     # iOS (auto-loaded)
MyComponent.android.tsx # Android (auto-loaded)
```

**Platform.Version check**:
```typescript
if (Platform.OS === 'ios' && Platform.Version >= 14) {
  // iOS 14+ features
}
```

**Test mocking**:
```typescript
const originalOS = Platform.OS;

afterEach(() => {
  Platform.OS = originalOS;
});

it('test', () => {
  Platform.OS = 'ios';
  // Test code
});
```

**Key Libraries:**
- react-native 0.75.4

For production examples, see [references/examples.md](references/examples.md).
