---
name: android-patterns
description: "WHAT: Android-specific patterns for BackHandler, StatusBar, and material elevation. WHEN: handling hardware back button, configuring status bar color, implementing shadows. KEYWORDS: android, BackHandler, StatusBar, elevation, ToastAndroid, PlatformIs, Platform.select, shadow, cleanup."
---

# Android Platform Patterns

## Core Principles

**Use PlatformIs.android() for readable platform detection.** The utility function is more readable than Platform.OS === 'android' and provides type safety with consistent API across the codebase.

**Always handle hardware back button on Android.** Android devices have a physical or virtual back button that requires explicit handling. Use BackHandler API to control back button behavior and prevent unwanted app exits.

**Always clean up BackHandler listeners.** BackHandler subscriptions must be removed in useEffect cleanup to prevent memory leaks and unexpected behavior when components unmount.

**Use Zest shadow tokens for cross-platform shadows.** Zest automatically applies Android elevation from shadow tokens, eliminating manual elevation management while ensuring consistent visual design across platforms.

**Why**: Android has unique platform requirements including hardware back button handling, status bar color control, material design elevation, and specific UX patterns. Following these standards ensures native Android user experience while maintaining cross-platform code quality.

## When to Use This Skill

Use these patterns when:

- Detecting Android platform for conditional rendering or logic
- Handling hardware back button in navigation or modal screens
- Configuring status bar background color (Android-only)
- Implementing material design elevation on surfaces
- Using Android-native UI components (ToastAndroid)
- Creating platform-specific implementations
- Testing Android-specific code behavior
- Supporting Android version-specific features
- Implementing Android-specific UI patterns

## Platform Detection

### PlatformIs Utility

Use PlatformIs for readable platform checks:

```typescript
import { PlatformIs } from '@libs/utils/platform';

const MyComponent = () => {
  if (!PlatformIs.android()) {
    return null;
  }

  return <AndroidOnlyFeature />;
};
```

**Why**: `PlatformIs.android()` is more readable than `Platform.OS === 'android'` and provides type safety with consistent API across the codebase.

**Implementation**:

```typescript
// libs/utils/platform.ts
import { Platform } from 'react-native';

export const PlatformIs = {
  android: (): boolean => Platform.OS === 'android',
  ios: (): boolean => Platform.OS === 'ios',
} as const;
```

**Why**: Centralized platform detection prevents typos ('android' vs 'Android'), provides consistent boolean checks, and is easier to mock in tests.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/utils/components/PlatformStatusBar.tsx:1`

## Android StatusBar

### StatusBar with backgroundColor

Android StatusBar supports backgroundColor prop for controlling the status bar color:

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

**Why**: Android status bar color is controlled via `backgroundColor` prop. iOS ignores this prop (iOS status bar is always transparent). Use theme colors for consistent branding.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/utils/components/PlatformStatusBar.tsx:1`

### StatusBar Styles

```typescript
// Light text on dark background
<StatusBar
  barStyle="light-content"
  backgroundColor="#1A1A1A" // Android only
/>

// Dark text on light background
<StatusBar
  barStyle="dark-content"
  backgroundColor="#FFFFFF" // Android only
/>

// Use theme colors
<StatusBar
  barStyle="light-content"
  backgroundColor={theme.alias.color.brand.background.default}
/>
```

**Why**: `barStyle` controls text color on both platforms. `backgroundColor` only affects Android, allowing independent control of status bar background.

## Hardware Back Button (BackHandler)

### Basic BackHandler Usage

Android hardware back button requires explicit handling:

```typescript
import { useEffect } from 'react';
import { BackHandler, Platform } from 'react-native';

export const useBackHandler = (handler: () => boolean) => {
  useEffect(() => {
    if (Platform.OS !== 'android') {
      return;
    }

    const subscription = BackHandler.addEventListener(
      'hardwareBackPress',
      handler
    );

    return () => subscription.remove();
  }, [handler]);
};
```

**Why**: BackHandler is Android-only. Always check Platform.OS before adding listener. Always remove listener in cleanup function to prevent memory leaks.

### BackHandler Return Values

```typescript
const handleBackPress = () => {
  // Return true to suppress default behavior (don't exit app)
  if (shouldPreventBack) {
    return true;
  }

  // Return false to allow default behavior (exit app)
  return false;
};

const subscription = BackHandler.addEventListener(
  'hardwareBackPress',
  handleBackPress
);
```

**Why**: Returning `true` suppresses the default system back behavior. Returning `false` allows the system to handle back (typically exits app or goes to previous activity).

### WebView Back Button Integration

```typescript
import { useRef, useEffect } from 'react';
import { BackHandler, Platform } from 'react-native';
import type WebView from 'react-native-webview';

export const useWebViewBackHandler = ({
  webViewRef,
}: {
  webViewRef: React.RefObject<WebView>;
}) => {
  const canGoBackRef = useRef(false);

  const handleNavigationStateChange = (navState) => {
    canGoBackRef.current = navState.canGoBack;
  };

  useEffect(() => {
    if (Platform.OS !== 'android') {
      return;
    }

    const handleBackPress = () => {
      const canGoBack = canGoBackRef.current;

      if (canGoBack && webViewRef.current) {
        webViewRef.current.goBack();
      }

      // Always return true to prevent app exit
      return true;
    };

    const subscription = BackHandler.addEventListener(
      'hardwareBackPress',
      handleBackPress
    );

    return () => subscription.remove();
  }, [webViewRef]);

  return {
    handleNavigationStateChange,
  };
};
```

**Why**: WebView needs custom back button handling to navigate WebView history instead of exiting the screen. Use ref to track canGoBack state without re-renders. Return true to suppress default app exit.

**Production Example**: `git-resources/shared-mobile-modules/src/features/webview/hooks/useWebViewBackHandler.ts:1`

### BackHandler Cleanup

```typescript
useEffect(() => {
  if (Platform.OS !== 'android') {
    return;
  }

  const handleBackPress = () => {
    // Handle back press
    return true;
  };

  const subscription = BackHandler.addEventListener(
    'hardwareBackPress',
    handleBackPress
  );

  // ✅ ALWAYS remove listener in cleanup
  return () => subscription.remove();
}, []);
```

**Why**: Failing to remove BackHandler listener causes memory leaks and multiple handlers firing simultaneously. Cleanup function ensures listener is removed when component unmounts.

## Android Shadows and Elevation

### Elevation with Zest Tokens

Android uses elevation property for material design depth. Zest shadow tokens automatically apply elevation:

```typescript
import { createStylesConfig } from '@zest/react-native';

const stylesConfig = createStylesConfig({
  card: {
    backgroundColor: 'alias.color.neutral.background.default',
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.md.shadowOpacity',
    shadowRadius: 'global.shadow.md.shadowRadius',
    // elevation is automatically applied by Zest on Android
  },
});
```

**Why**: Zest shadow tokens automatically apply both iOS shadow properties and Android elevation. No manual elevation management needed.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/edit-recipe/components/draggableStepItemStyles.ts:1`

### Manual Elevation (Rare)

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

**Why**: Manual elevation is rarely needed. Use only when not using Zest tokens. Elevation values range from 0-24 for different material design depths.

### Elevation Levels

```typescript
// No elevation
elevation: 0

// Low elevation (buttons, cards)
elevation: 2

// Medium elevation (floating action button)
elevation: 6

// High elevation (navigation drawer)
elevation: 16

// Maximum elevation (modal)
elevation: 24
```

**Why**: Material design defines standard elevation levels for different UI elements. Consistent elevation creates visual hierarchy.

## Android-Native Components

### ToastAndroid

Android provides native toast notifications:

```typescript
import { ToastAndroid, Platform } from 'react-native';

const showToast = (message: string) => {
  if (Platform.OS === 'android') {
    ToastAndroid.show(message, ToastAndroid.SHORT);
  } else {
    // Use custom toast component or Alert on iOS
    Alert.alert(message);
  }
};

// Toast durations
ToastAndroid.SHORT; // ~2 seconds
ToastAndroid.LONG; // ~3.5 seconds

// Toast positions
ToastAndroid.show(message, duration, ToastAndroid.TOP);
ToastAndroid.show(message, duration, ToastAndroid.BOTTOM);
ToastAndroid.show(message, duration, ToastAndroid.CENTER);
```

**Why**: ToastAndroid is Android-only native component. Use for temporary notifications that don't require user action. Always check Platform.OS before using.

## Platform-Specific Rendering

### Conditional Platform Rendering

```typescript
import { Platform, View, Text } from 'react-native';

const MyComponent = () => {
  return (
    <View>
      {Platform.OS === 'android' ? (
        <AndroidSpecificComponent />
      ) : (
        <IOSSpecificComponent />
      )}

      <Text>Shared Content</Text>
    </View>
  );
};
```

**Why**: Inline conditional rendering works well for small platform differences. For larger differences, use platform-specific files (`.android.tsx`, `.ios.tsx`).

### Platform.select for Values

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

**Why**: `Platform.select` chooses values based on platform, providing type-safe platform-specific constants. Useful for dimensions, fonts, or configuration that differs by platform.

### Platform-Specific File Extensions

```typescript
// MyComponent.android.tsx - Android-specific implementation
import { ToastAndroid } from 'react-native';

export const MyComponent = () => {
  const handlePress = () => {
    ToastAndroid.show('Android Only', ToastAndroid.SHORT);
  };

  return <Button onPress={handlePress}>Show Toast</Button>;
};

// MyComponent.ios.tsx - iOS-specific implementation
import { Alert } from 'react-native';

export const MyComponent = () => {
  const handlePress = () => {
    Alert.alert('iOS Only', 'This runs only on iOS');
  };

  return <Button onPress={handlePress}>Show Alert</Button>;
};
```

**Why**: React Native automatically loads `.android.tsx` on Android and `.ios.tsx` on iOS. This pattern completely separates platform-specific implementations, keeping code clean and maintainable.

## Debug Features on Android

### Development-Only Android Features

```typescript
import { Platform, View } from 'react-native';

export const Profile = () => {
  return (
    <View>
      <UserInfo />
      <Settings />
      {/* Debug settings are only available in android */}
      {__DEV__ && Platform.OS === 'android' && <DebugItems />}
    </View>
  );
};
```

**Why**: Debug features often target Android for easier testing during development. Combine `__DEV__` with `Platform.OS === 'android'` for development-only, platform-specific features.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/profile/screens/profile/Profile.tsx:75`

## Android Permissions

### Permission Protocol

**⚠️ IMPORTANT**: Any code requiring Android runtime permissions needs explicit permission from native developers.

```typescript
// ❌ DON'T: Request permissions without approval
import { check, request, PERMISSIONS } from 'react-native-permissions';

const requestCameraPermission = async () => {
  const result = await request(PERMISSIONS.ANDROID.CAMERA);
  return result === 'granted';
};

// ✅ DO: Document permission requirements and get approval
/**
 * @requires-permission android.permission.CAMERA
 * @permission-status APPROVED (Ticket: JIRA-123, Approved by: @native-team)
 */
const requestCameraPermission = async () => {
  const result = await request(PERMISSIONS.ANDROID.CAMERA);
  return result === 'granted';
};
```

**Why**: Runtime permissions affect user experience and Play Store review. Native developers must verify permission necessity, implement AndroidManifest.xml entries, and handle permission denial gracefully.

## Testing Android-Specific Code

### Mock Platform.OS

```typescript
import { Platform } from 'react-native';

describe('AndroidComponent', () => {
  const originalOS = Platform.OS;

  afterEach(() => {
    Platform.OS = originalOS; // Restore original
  });

  it('should render on Android', () => {
    Platform.OS = 'android';

    const { getByTestId } = render(<AndroidComponent />);

    expect(getByTestId('android-feature')).toBeDefined();
  });

  it('should not render on iOS', () => {
    Platform.OS = 'ios';

    const { queryByTestId } = render(<AndroidComponent />);

    expect(queryByTestId('android-feature')).toBeNull();
  });
});
```

**Why**: Mocking Platform.OS enables testing platform-specific behavior without separate test runs per platform.

**Production Example**: `git-resources/shared-mobile-modules/src/features/webview/hooks/useWebViewBackHandler.test.ts:1`

### Mock BackHandler

```typescript
jest.mock('react-native/Libraries/Utilities/BackHandler', () => ({
  addEventListener: jest.fn(() => ({
    remove: jest.fn(),
  })),
}));

describe('useBackHandler', () => {
  it('should register back handler on Android', () => {
    Platform.OS = 'android';

    renderHook(() => useBackHandler());

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

    Platform.OS = 'android';
    const { unmount } = renderHook(() => useBackHandler());

    unmount();

    expect(removeMock).toHaveBeenCalled();
  });
});
```

**Why**: Mocking BackHandler provides consistent test results and verifies listener cleanup without running on Android device.

**Production Example**: `git-resources/shared-mobile-modules/src/features/webview/hooks/useWebViewBackHandler.test.ts:1`

## Common Mistakes to Avoid

❌ **Don't forget to remove BackHandler listeners**:

```typescript
// ❌ Missing cleanup
useEffect(() => {
  if (Platform.OS !== 'android') return;

  BackHandler.addEventListener('hardwareBackPress', handleBackPress);
  // Missing cleanup!
}, []);
```

**Why**: Failing to remove BackHandler listener causes memory leaks and multiple handlers firing simultaneously.

✅ **Do always clean up BackHandler listeners**:

```typescript
// ✅ Proper cleanup
useEffect(() => {
  if (Platform.OS !== 'android') return;

  const subscription = BackHandler.addEventListener(
    'hardwareBackPress',
    handleBackPress
  );

  return () => subscription.remove();
}, [handleBackPress]);
```

**Why**: Cleanup function ensures listener is removed when component unmounts, preventing memory leaks and unexpected behavior.

❌ **Don't use BackHandler without platform check**:

```typescript
// ❌ No platform check
useEffect(() => {
  const subscription = BackHandler.addEventListener(
    'hardwareBackPress',
    handleBackPress
  );

  return () => subscription.remove();
}, []);
```

**Why**: BackHandler is Android-only. Code will crash on iOS with "undefined is not an object (evaluating 'BackHandler.addEventListener')".

✅ **Do check Platform.OS before using BackHandler**:

```typescript
// ✅ Platform check
useEffect(() => {
  if (Platform.OS !== 'android') {
    return;
  }

  const subscription = BackHandler.addEventListener(
    'hardwareBackPress',
    handleBackPress
  );

  return () => subscription.remove();
}, [handleBackPress]);
```

**Why**: Early return prevents BackHandler usage on iOS, ensuring code runs only on Android.

❌ **Don't use iOS shadows without elevation on Android**:

```typescript
// ❌ No elevation on Android
const styles = StyleSheet.create({
  card: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    // Missing elevation for Android!
  },
});
```

**Why**: Android ignores iOS shadow properties. Android requires elevation property for material design depth.

✅ **Do use Zest tokens for cross-platform shadows**:

```typescript
// ✅ Works on both platforms
const stylesConfig = createStylesConfig({
  card: {
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.md.shadowOpacity',
    shadowRadius: 'global.shadow.md.shadowRadius',
    // elevation automatically applied by Zest on Android
  },
});
```

**Why**: Zest automatically applies correct values for each platform, ensuring visual consistency without manual Platform.select.

❌ **Don't use BackHandler return value inconsistently**:

```typescript
// ❌ Confusing return values
const handleBackPress = () => {
  if (shouldExit) {
    return true; // Wait, this prevents exit!
  }
  return false;
};
```

**Why**: Returning `true` suppresses default behavior (prevents exit), which is counter-intuitive. This causes confusion about when app will exit.

✅ **Do return values consistently with clear intent**:

```typescript
// ✅ Clear intent
const handleBackPress = () => {
  if (shouldPreventBack) {
    // Handle custom back behavior
    goToPreviousScreen();
    return true; // Suppress default (don't exit app)
  }

  // Allow default behavior (exit app)
  return false;
};
```

**Why**: Clear variable names and comments explain intent. `true` = suppress default, `false` = allow default.

## Quick Reference

**Platform detection with PlatformIs**:
```typescript
import { PlatformIs } from '@libs/utils/platform';

if (PlatformIs.android()) {
  // Android-specific code
}
```

**StatusBar with backgroundColor**:
```typescript
import { StatusBar } from 'react-native';

<StatusBar
  barStyle="light-content"
  backgroundColor={theme.alias.color.brand.background.default}
/>
```

**BackHandler with cleanup**:
```typescript
import { BackHandler, Platform } from 'react-native';

useEffect(() => {
  if (Platform.OS !== 'android') return;

  const subscription = BackHandler.addEventListener(
    'hardwareBackPress',
    handleBackPress
  );

  return () => subscription.remove();
}, [handleBackPress]);
```

**BackHandler return values**:
```typescript
const handleBackPress = () => {
  // true = suppress default (don't exit)
  // false = allow default (exit app)
  return shouldPreventBack ? true : false;
};
```

**Cross-platform shadows with Zest**:
```typescript
const stylesConfig = createStylesConfig({
  card: {
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.md.shadowOpacity',
    shadowRadius: 'global.shadow.md.shadowRadius',
    // elevation automatically applied on Android
  },
});
```

**ToastAndroid**:
```typescript
import { ToastAndroid, Platform } from 'react-native';

if (Platform.OS === 'android') {
  ToastAndroid.show('Message', ToastAndroid.SHORT);
}
```

**Platform-specific values**:
```typescript
const HEADER_HEIGHT = Platform.select({
  ios: 44,
  android: 56,
  default: 50,
});
```

**Debug features on Android**:
```typescript
{__DEV__ && Platform.OS === 'android' && <DebugItems />}
```

**Test mocking**:
```typescript
// Mock Platform.OS
Platform.OS = 'android';

// Mock BackHandler
jest.mock('react-native/Libraries/Utilities/BackHandler', () => ({
  addEventListener: jest.fn(() => ({ remove: jest.fn() })),
}));
```

**Key Libraries:**
- react-native 0.75.4
- @zest/react-native 1.3.1

For production examples, see [references/examples.md](references/examples.md).
