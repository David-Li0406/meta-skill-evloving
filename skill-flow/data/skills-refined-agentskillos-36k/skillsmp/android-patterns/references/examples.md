# Android Patterns - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating Android-specific patterns.

## Example 1: PlatformIs.android() and StatusBar backgroundColor

**File**: `libs/utils/components/PlatformStatusBar.tsx:1`

This example shows Android-specific StatusBar component with backgroundColor.

```typescript
import { StatusBar } from 'react-native';
import { useZestTheme } from '@zest/react-native';
import { PlatformIs } from '../platform';

interface PlatformStatusBarProps {
  barStyle?: 'light-content' | 'dark-content';
  backgroundColor?: string;
}

/**
 * Platform-aware StatusBar component that only renders on Android
 * Uses theme colors by default but allows customization
 */
export const PlatformStatusBar = ({
  barStyle = 'light-content',
  backgroundColor,
}: PlatformStatusBarProps) => {
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
- PlatformIs.android() for early return on non-Android
- StatusBar backgroundColor from Zest theme
- Default backgroundColor fallback to theme
- Component renders null on iOS
- useZestTheme for accessing theme colors
- barStyle works on both platforms, backgroundColor is Android-specific
- TypeScript interface for props
- JSDoc comment explaining Android-only behavior

## Example 2: BackHandler for Hardware Back Button

**File**: `features/webview/hooks/useWebViewBackHandler.ts:1`

This example shows BackHandler implementation for Android hardware back button in a WebView.

```typescript
import type { ForwardedRef } from 'react';
import { useRef, useEffect } from 'react';
import { BackHandler, Platform } from 'react-native';
import type { WebViewNavigation } from 'react-native-webview';
import type WebView from 'react-native-webview';

/**
 * A custom hook that handles Android hardware back button behavior for a WebView.
 *
 * Behavior:
 * - If the WebView can go back, it navigates back in history.
 * - If it cannot, it prevents the default behavior to avoid infinite back press loop.
 *
 * Note:
 * - This hook is designed for screens where React Native is rendered
 *   inside a native fragment or non-root activity.
 * - In such cases, BackHandler.exitApp() may not work reliably,
 *   so we return `true` to suppress default system behavior.
 */
export const useWebViewBackHandler = ({
  webViewRef,
}: {
  webViewRef: ForwardedRef<WebView>;
}) => {
  const canGoBackRef = useRef(false);

  const handleNavigationStateChange = (navState: WebViewNavigation) => {
    canGoBackRef.current = navState.canGoBack;
  };

  useEffect(() => {
    if (Platform.OS !== 'android') {
      return;
    }

    const handleBackPress = () => {
      const canGoBack = canGoBackRef.current;

      if (
        canGoBack &&
        webViewRef &&
        typeof webViewRef !== 'function' &&
        webViewRef.current
      ) {
        webViewRef.current.goBack();
      }

      // Always return true to suppress default behavior and prevent infinite loop.
      // In this app setup, BackHandler.exitApp() doesn't work as expected because
      // React Native is hosted inside a native fragment or non-root activity.
      return true;
    };

    const subscription = BackHandler.addEventListener(
      'hardwareBackPress',
      handleBackPress
    );

    return () => subscription.remove();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    webViewRef,
    handleNavigationStateChange,
  };
};
```

**Key patterns demonstrated:**
- Platform.OS !== 'android' early return in useEffect
- BackHandler.addEventListener with 'hardwareBackPress' event
- subscription.remove() in cleanup function
- Return true to suppress default back button behavior
- Return false to allow default behavior (exit app)
- useRef for tracking WebView state without re-renders
- WebView ref type checking (typeof webViewRef !== 'function')
- Comprehensive JSDoc explaining behavior and edge cases
- Custom hook pattern for reusable logic

## Example 3: Platform.OS Check for Debug Features

**File**: `modules/profile/screens/profile/Profile.tsx:75`

This example shows conditional rendering of debug features only on Android.

```typescript
import { Platform, ScrollView, View } from 'react-native';
import { useZestStyles } from '@zest/react-native';
import { AuthGuard } from '@libs/auth-guard';

export const Profile = () => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollViewContent}>
        <AuthGuard stackName="profile" fallback={<LoginSignup />}>
          <AccountHeader />
          <PlanSettings />
          <AccountDetails />
        </AuthGuard>
        <Support />
        {/* Debug settings are only available in android */}
        {__DEV__ && Platform.OS === 'android' && <DebugItems />}
        <AuthGuard stackName="profile" fallback={null}>
          <Logout />
        </AuthGuard>
      </ScrollView>
    </View>
  );
};
```

**Key patterns demonstrated:**
- Platform.OS === 'android' for conditional rendering
- Combine with __DEV__ for debug-only features
- Inline comment explaining Android-only behavior
- Double condition (__DEV__ && Platform.OS)
- JSX conditional rendering with &&

## Example 4: Zest Shadow Tokens (Cross-Platform)

**File**: `modules/social-recipe-bridge/screens/edit-recipe/components/draggableStepItemStyles.ts:1`

This example shows Zest shadow tokens that automatically apply elevation on Android.

```typescript
import { createStylesConfig } from '@zest/react-native';

export const stylesConfig = createStylesConfig({
  stepRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 'global.spacing.xxs',
    marginBottom: 'global.spacing.sm2',
    backgroundColor: 'alias.color.neutral.background.default',
    borderRadius: 'global.borderRadius.md',
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowRadius: 'global.shadow.md.shadowRadius',
  },
  stepContent: {
    flex: 1,
  },
});
```

**Key patterns demonstrated:**
- Zest shadow tokens work on both platforms
- Android automatically applies elevation from shadow tokens
- iOS uses shadowColor, shadowOffset, shadowRadius
- createStylesConfig for Zest integration
- No explicit elevation property needed (handled by Zest)
- Other Zest tokens (spacing, color, borderRadius)
- Type-safe style configuration

## Example 5: BackHandler in Tests

**File**: `features/webview/hooks/useWebViewBackHandler.test.ts:1`

This example shows mocking BackHandler and Platform.OS in tests.

```typescript
import { renderHook } from '@testing-library/react-native';
import { BackHandler } from 'react-native';
import { useWebViewBackHandler } from './useWebViewBackHandler';

jest.mock('react-native/Libraries/Utilities/Platform', () => ({
  OS: 'android',
}));

jest.mock('react-native/Libraries/Utilities/BackHandler', () => ({
  addEventListener: jest.fn(() => ({
    remove: jest.fn(),
  })),
}));

describe('useWebViewBackHandler', () => {
  it('should not register back handler when Platform.OS is not android', () => {
    const originalPlatform = require('react-native/Libraries/Utilities/Platform');
    originalPlatform.OS = 'ios';

    const webViewRef = { current: null };
    renderHook(() => useWebViewBackHandler({ webViewRef }));

    expect(BackHandler.addEventListener).not.toHaveBeenCalled();

    // Restore original Platform.OS
    originalPlatform.OS = 'android';
  });

  it('should register back handler on android', () => {
    const originalPlatform = require('react-native/Libraries/Utilities/Platform');
    originalPlatform.OS = 'android';

    const webViewRef = { current: null };
    renderHook(() => useWebViewBackHandler({ webViewRef }));

    expect(BackHandler.addEventListener).toHaveBeenCalledWith(
      'hardwareBackPress',
      expect.any(Function)
    );
  });

  it('should remove listener on unmount', () => {
    const removeMock = jest.fn();
    (BackHandler.addEventListener as jest.Mock).mockReturnValue({
      remove: removeMock,
    });

    const webViewRef = { current: null };
    const { unmount } = renderHook(() =>
      useWebViewBackHandler({ webViewRef })
    );

    unmount();

    expect(removeMock).toHaveBeenCalled();
  });
});
```

**Key patterns demonstrated:**
- Mock Platform module with jest.mock
- Set Platform.OS = 'android' for Android-specific tests
- Mock BackHandler.addEventListener
- Mock subscription.remove for cleanup testing
- Test platform-specific behavior without running on device
- renderHook for testing custom hooks
- expect().not.toHaveBeenCalled() for negative assertions
- Restore Platform.OS after tests
- Test cleanup function calls remove()

## Summary

The YourCompany codebase consistently follows these Android platform patterns:

1. **PlatformIs.android()** for readable platform detection (vs Platform.OS === 'android')
2. **StatusBar backgroundColor** for Android status bar color (iOS ignores this prop)
3. **BackHandler** for hardware back button handling with addEventListener and subscription.remove()
4. **Return true/false** from BackHandler to control default behavior (true = suppress, false = allow)
5. **Zest shadow tokens** automatically apply elevation on Android (no manual elevation needed)
6. **Platform.OS === 'android'** for conditional rendering
7. **Platform-specific features** in debug builds (__DEV__ && Platform.OS === 'android')
8. **Listener cleanup** in useEffect return function (subscription.remove())
9. **Platform.OS mocking** in tests for cross-platform behavior validation
10. **BackHandler mocking** with jest.fn() for testing Android-specific hooks

These patterns ensure native Android user experience with proper hardware back button handling, status bar colors, material design elevation, and testable platform-specific behavior throughout the app.
