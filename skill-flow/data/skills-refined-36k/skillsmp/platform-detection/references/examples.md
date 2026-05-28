# Platform Detection - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating platform detection patterns.

## Example 1: PlatformIs Utility Implementation

**File**: `libs/utils/platform.ts:1`

This example shows the centralized PlatformIs utility used throughout the codebase.

```typescript
import { Platform } from 'react-native';

export const PlatformIs = {
  android: (): boolean => Platform.OS === 'android',
  ios: (): boolean => Platform.OS === 'ios',
} as const;
```

**Key patterns demonstrated:**
- Object with platform check functions
- Boolean return types
- Platform.OS comparison with strict equality (===)
- Lowercase platform strings ('ios', 'android')
- `as const` for type safety
- Export for reuse across codebase

## Example 2: PlatformIs in Component Guards

**File**: `libs/utils/components/PlatformStatusBar.tsx:1`

This example shows PlatformIs used for early return pattern in Android-only component.

```typescript
import { StatusBar } from 'react-native';
import { useZestTheme } from '@zest/react-native';
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

**Key patterns demonstrated:**
- PlatformIs.android() for readable boolean check
- Early return pattern with negation (!PlatformIs.android())
- Android-only component (StatusBar backgroundColor)
- Default parameter values
- Theme color fallback
- Component renders null on iOS

## Example 3: Platform.OS in Constants

**File**: `modules/programs/screens/programs-home/constants.ts:1`

This example shows Platform.OS used for platform-based constants and string interpolation.

```typescript
import { Platform } from 'react-native';
import DeviceInfo from 'react-native-device-info';

export const USE_WEBKIT = Platform.OS === 'ios';

export const APP_VERSION =
  `${DeviceInfo.getReadableVersion()}${[Platform.OS]}` || '1.0.0';
```

**Key patterns demonstrated:**
- Boolean constant from Platform.OS comparison (USE_WEBKIT)
- Platform.OS === 'ios' for iOS detection
- Platform.OS in string template for version tagging
- String interpolation with array syntax [Platform.OS]
- Fallback value with || operator
- Export constants for reuse

## Example 4: Platform.OS in HTTP Headers

**File**: `libs/graphql/links/apolloHeaders.ts:1`

This example shows Platform.OS used directly in HTTP headers for GraphQL tracking.

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

**Key patterns demonstrated:**
- Platform.OS string value used directly in headers
- No comparison needed (raw string 'ios' or 'android')
- Apollo Client link context setup
- Spread operator for existing headers
- Bracket notation for header names with hyphens
- DeviceInfo integration for app metadata
- Platform tracking for backend analytics

## Example 5: Platform.OS in KeyboardAvoidingView

**File**: `modules/social-recipe-bridge/screens/edit-recipe/EditRecipeScreen.tsx:288`

This example shows Platform.OS ternary operator for platform-specific props.

```typescript
import { KeyboardAvoidingView, Platform } from 'react-native';

<KeyboardAvoidingView
  style={styles.container}
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
>
  <ScrollView
    ref={scrollViewRef}
    style={styles.scrollView}
    contentContainerStyle={styles.scrollViewContent}
    keyboardShouldPersistTaps="handled"
    scrollEnabled={isScrollEnabled}
    keyboardDismissMode="interactive"
  >
    {/* Content */}
  </ScrollView>
</KeyboardAvoidingView>
```

**Key patterns demonstrated:**
- Ternary operator with Platform.OS comparison
- Platform-specific behavior prop ('padding' on iOS, 'height' on Android)
- Platform-specific numeric offset (90 on iOS, 0 on Android)
- Multiple platform checks for same component
- Inline conditional logic in JSX props
- KeyboardAvoidingView pattern for form screens

## Example 6: Testing with Platform.OS Mocking

**File**: `features/webview/hooks/useWebViewBackHandler.test.ts:1`

This example shows testing pattern for platform-specific code with Platform.OS mocking.

```typescript
import { Platform } from 'react-native';
import { renderHook } from '@testing-library/react-native';

import { useWebViewBackHandler } from './useWebViewBackHandler';

jest.mock('react-native/Libraries/Utilities/BackHandler', () => ({
  addEventListener: jest.fn(() => ({
    remove: jest.fn(),
  })),
}));

describe('useWebViewBackHandler', () => {
  const originalOS = Platform.OS;
  const webViewRef = { current: null };

  afterEach(() => {
    Platform.OS = originalOS;
    jest.clearAllMocks();
  });

  it('does not add event listener on iOS', () => {
    Platform.OS = 'ios';
    const { BackHandler } = require('react-native');

    renderHook(() => useWebViewBackHandler({ webViewRef }));

    expect(BackHandler.addEventListener).not.toHaveBeenCalled();
  });

  it('adds event listener on Android', () => {
    Platform.OS = 'android';
    const { BackHandler } = require('react-native');

    renderHook(() => useWebViewBackHandler({ webViewRef }));

    expect(BackHandler.addEventListener).toHaveBeenCalledWith(
      'hardwareBackPress',
      expect.any(Function)
    );
  });

  it('removes event listener on unmount', () => {
    Platform.OS = 'android';
    const mockRemove = jest.fn();
    const { BackHandler } = require('react-native');
    (BackHandler.addEventListener as jest.Mock).mockReturnValue({
      remove: mockRemove,
    });

    const { unmount } = renderHook(() =>
      useWebViewBackHandler({ webViewRef })
    );

    unmount();

    expect(mockRemove).toHaveBeenCalled();
  });
});
```

**Key patterns demonstrated:**
- Save original Platform.OS before tests
- Restore Platform.OS in afterEach
- Mock Platform.OS = 'ios' or 'android' per test
- Test both platforms with same test suite
- Mock BackHandler module with jest.mock
- jest.fn() for mock functions
- mockReturnValue for subscription pattern
- expect().not.toHaveBeenCalled() for iOS test
- expect().toHaveBeenCalledWith() for Android test
- renderHook for testing custom hooks
- unmount() to test cleanup

## Example 7: Combined Platform Patterns

This example demonstrates multiple platform detection patterns in a single component (composite example).

```typescript
import { Platform, StyleSheet, View, Text } from 'react-native';
import { PlatformIs } from '@libs/utils/platform';

// Constants with Platform.OS
const USE_WEBKIT = Platform.OS === 'ios';
const HEADER_HEIGHT = Platform.select({
  ios: 44,
  android: 56,
  default: 50,
});

// Component with multiple platform patterns
export const PlatformDemo = () => {
  // Early return for iOS-only
  if (!PlatformIs.ios() && !__DEV__) {
    return null;
  }

  return (
    <View style={styles.container}>
      {/* Conditional rendering with ternary */}
      {Platform.OS === 'ios' ? (
        <Text>iOS Version</Text>
      ) : (
        <Text>Android Version</Text>
      )}

      {/* Conditional rendering with && */}
      {PlatformIs.android() && <Text>Android Only</Text>}

      {/* Platform-specific prop */}
      <View
        style={{
          height: HEADER_HEIGHT,
          ...Platform.select({
            ios: { shadowOpacity: 0.3 },
            android: { elevation: 4 },
          }),
        }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: Platform.OS === 'ios' ? 20 : 0,
  },
});
```

**Key patterns demonstrated:**
- PlatformIs utility for readable checks
- Platform.OS for direct boolean comparison
- Platform.select for platform-specific values
- Early return pattern
- Ternary operator for component selection
- JSX && pattern for optional rendering
- Platform.select in StyleSheet
- Spread operator for platform-specific styles
- Platform.OS in style objects
- Multiple platform patterns combined

## Summary

The YourCompany codebase consistently follows these platform detection patterns:

1. **PlatformIs utility** - Centralized, readable platform checks (PlatformIs.ios(), PlatformIs.android())
2. **Platform.OS comparison** - Direct string comparison with strict equality (===) and lowercase strings
3. **Platform.select** - Type-safe platform-specific value selection for constants and styles
4. **Early return** - Component guards with !PlatformIs.platform() for platform-only components
5. **Ternary operator** - Inline conditional rendering for small platform differences
6. **JSX && pattern** - Optional platform-specific elements
7. **Platform.OS in headers** - Raw string value for HTTP headers and analytics
8. **Platform.OS in constants** - Boolean flags and string interpolation
9. **Test mocking** - Save, mock, and restore Platform.OS in afterEach
10. **Combined patterns** - Multiple platform checks in single component

These patterns ensure readable, maintainable, and testable cross-platform code with clear platform-specific behavior throughout the app.
