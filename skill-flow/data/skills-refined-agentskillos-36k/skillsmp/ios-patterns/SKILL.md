---
name: ios-patterns
description: "WHAT: iOS-specific patterns for SafeAreaView, shadows, and device APIs. WHEN: handling notches, implementing iOS shadows, accessing device info. KEYWORDS: ios, SafeAreaView, useSafeAreaInsets, shadow, StatusBar, device-info, PlatformIs, edges, insets."

tracked_repositories:
  - url: yourcompany/shared-mobile-modules
    type: internal
    paths:
      - /src/**/*.ios.tsx
      - /src/**/*.ios.ts
      - /ios/**/*
    last_synced: 2025-01-04T10:00:00Z
    sync_frequency: weekly

  - url: https://github.com/react-native-community/react-native-safe-area-context
    type: external
    paths:
      - /docs/**/*.md
      - /readme.md
    last_synced: 2025-01-04T10:00:00Z
    sync_frequency: monthly
---

# iOS Platform Patterns

## Core Principles

**Use PlatformIs.ios() for readable platform detection.** The utility function is more readable than Platform.OS === 'ios' and provides type safety with consistent API across the codebase.

**Always specify edges prop on SafeAreaView.** Explicit edges provide granular control over which screen edges receive safe area insets, preventing unwanted padding.

**Use Zest shadow tokens for cross-platform shadows.** iOS requires shadowColor, shadowOffset, shadowOpacity, and shadowRadius properties. Zest tokens automatically apply correct values for both iOS and Android.

**Never hardcode safe area values.** Safe area insets vary by device (notched vs non-notched iPhones, iPads). Always use SafeAreaView or useSafeAreaInsets hook for dynamic values.

**Why**: iOS has unique platform requirements including notch handling, shadow rendering, status bar configuration, and specific UX patterns. Following these standards ensures native iOS user experience while maintaining cross-platform code quality.

## When to Use This Skill

Use these patterns when:

- Detecting iOS platform for conditional rendering or logic
- Handling safe areas for notched iPhones and home indicators
- Implementing shadows on cards, modals, or elevated surfaces
- Configuring status bar appearance (light/dark text)
- Accessing device information for analytics or debugging
- Creating platform-specific implementations
- Testing iOS-specific code behavior
- Implementing iOS-specific UI patterns (blur, haptics)
- Supporting iOS version-specific features

## Platform Detection

### PlatformIs Utility

Use PlatformIs for readable platform checks:

```typescript
import { PlatformIs } from '@libs/utils/platform';

const MyComponent = () => {
  if (!PlatformIs.ios()) {
    return null;
  }

  return <IOSOnlyFeature />;
};
```

**Why**: `PlatformIs.ios()` is more readable than `Platform.OS === 'ios'` and provides type safety with consistent API across the codebase.

**Implementation**:

```typescript
// libs/utils/platform.ts
import { Platform } from 'react-native';

export const PlatformIs = {
  android: (): boolean => Platform.OS === 'android',
  ios: (): boolean => Platform.OS === 'ios',
} as const;
```

**Why**: Centralized platform detection prevents typos ('ios' vs 'iOS'), provides consistent boolean checks, and is easier to mock in tests.

**Production Example**: `git-resources/shared-mobile-modules/src/features/customization-drawer/CustomizationDrawer.tsx:13`

## Safe Area Handling

### SafeAreaView with Edges

iOS devices have notches, status bars, and home indicators that require safe area handling. Use `react-native-safe-area-context` for precise control.

```typescript
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export const MyScreen = () => {
  return (
    <View style={styles.container}>
      <SafeAreaView style={styles.safeAreaContainer} edges={['top']}>
        <Header />
        <Content />
      </SafeAreaView>
    </View>
  );
};
```

**Why**: `edges` prop provides granular control over which edges to apply safe area insets. Specify only the edges you need (e.g., `['top']` for screens with custom bottom navigation).

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/cart/layouts/default/default.tsx:68`

### Common Edge Configurations

```typescript
// Full safe area (all edges)
<SafeAreaView edges={['top', 'bottom', 'left', 'right']}>

// Top only (custom bottom UI like floating buttons)
<SafeAreaView edges={['top']}>

// No safe area handling (modal or custom handling)
<SafeAreaView edges={[]}>

// Bottom only (header rendered outside safe area)
<SafeAreaView edges={['bottom']}>
```

**Why**: Different screen layouts require different safe area configurations. Modals might need full safe area, while screens with custom floating buttons only need top insets.

### useSafeAreaInsets Hook

For dynamic positioning or manual calculations, use `useSafeAreaInsets`:

```typescript
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { View, StyleSheet } from 'react-native';

export const CloseButton = ({ onPress }: CloseButtonProps) => {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={[
        styles.closeButton,
        { top: insets.top + 12 }, // 12px padding + safe area
      ]}
    >
      <Button onPress={onPress} />
    </View>
  );
};
```

**Why**: `useSafeAreaInsets` provides numeric values for each safe area inset, enabling custom positioning and calculations that work across all iOS devices (notched and non-notched).

**Production Example**: `git-resources/shared-mobile-modules/src/modules/loyalty-program/screens/components/close-button/CloseButton.tsx:18`

### Insets Object Structure

```typescript
interface EdgeInsets {
  top: number; // Status bar + notch area
  bottom: number; // Home indicator area
  left: number; // Side safe areas
  right: number; // Side safe areas
}

// Example values on iPhone with notch:
// { top: 44, bottom: 34, left: 0, right: 0 }

// Example values on iPhone without notch:
// { top: 20, bottom: 0, left: 0, right: 0 }
```

**Why**: Understanding inset values helps determine appropriate spacing. Notched iPhones have larger top and bottom insets.

## iOS Shadow Patterns

### Shadows with Zest Tokens

iOS renders shadows using `shadowColor`, `shadowOffset`, `shadowOpacity`, and `shadowRadius` properties:

```typescript
import { useZestStyles } from '@zest/react-native';

const stylesConfig = {
  card: {
    backgroundColor: 'alias.color.elevation.background.level2.default',
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.md.shadowOpacity',
    shadowRadius: 'global.shadow.md.shadowRadius',
    elevation: 'global.shadow.md.elevation', // Android fallback
  },
};

export const Card = () => {
  const styles = useZestStyles(stylesConfig);
  return <View style={styles.card}>...</View>;
};
```

**Why**: Zest theme tokens provide consistent cross-platform shadows. The design system automatically applies correct values for iOS and Android.

**Production Example**: `git-resources/shared-mobile-modules/src/features/product-card-feature/variants/skipped/components/style.ts:8`

### Shadow Levels

```typescript
// Small shadow (subtle depth)
const stylesConfig = {
  surface: {
    shadowColor: 'global.shadow.sm.shadowColor',
    shadowOffset: {
      width: 'global.shadow.sm.shadowOffset.width',
      height: 'global.shadow.sm.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.sm.shadowOpacity',
    shadowRadius: 'global.shadow.sm.shadowRadius',
    elevation: 'global.shadow.sm.elevation',
  },
};

// Medium shadow (cards, elevated surfaces)
const stylesConfig = {
  card: {
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.md.shadowOpacity',
    shadowRadius: 'global.shadow.md.shadowRadius',
    elevation: 'global.shadow.md.elevation',
  },
};

// Large shadow (modals, floating elements)
const stylesConfig = {
  modal: {
    shadowColor: 'global.shadow.lg.shadowColor',
    shadowOffset: {
      width: 'global.shadow.lg.shadowOffset.width',
      height: 'global.shadow.lg.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.lg.shadowOpacity',
    shadowRadius: 'global.shadow.lg.shadowRadius',
    elevation: 'global.shadow.lg.elevation',
  },
};
```

**Why**: Consistent shadow levels create visual hierarchy. Small shadows for subtle elevation, medium for cards, large for prominent floating elements.

## iOS Status Bar

### Status Bar Styling

```typescript
import { StatusBar } from 'react-native';
import { useZestTheme } from '@zest/react-native';

export const MyScreen = () => {
  const theme = useZestTheme();

  return (
    <>
      <StatusBar
        barStyle="dark-content" // Black text on light background
        backgroundColor="transparent" // iOS ignores this
      />
      <View>
        <Text>Screen Content</Text>
      </View>
    </>
  );
};
```

**Why**: iOS status bar styling uses `barStyle` prop. `backgroundColor` is ignored on iOS (use `SafeAreaView` or background color on container instead).

### Status Bar Styles

```typescript
// Light text on dark background
<StatusBar barStyle="light-content" />

// Dark text on light background
<StatusBar barStyle="dark-content" />

// Automatically adjust based on background (iOS 13+)
<StatusBar barStyle="default" />
```

**Why**: Status bar text color must be readable against screen background. Use `light-content` for dark backgrounds, `dark-content` for light backgrounds.

## Device Information (react-native-device-info)

### Common Device Info Patterns

```typescript
import {
  getBundleId,
  getSystemName,
  getSystemVersion,
  getVersion,
  getBrand,
  getApplicationName,
  getBuildNumber,
  getDeviceId,
} from 'react-native-device-info';

// User agent construction
export const getUserAgent = (): string => {
  const appId = getBundleId(); // e.g., "com.yourcompany.app"
  const applicationName = getApplicationName(); // e.g., "YourCompany"
  const platform = Platform.OS; // "ios"

  return `${applicationName}/${appId}/${platform}`;
};

// Tracing attributes
const appAndPlatformAttributes = {
  'service.name': 'mobile-app',
  'service.version': getVersion(), // e.g., "5.2.1"
  'service.brand': getApplicationName(), // e.g., "YourCompany"
  'service.bundle.identifier': getBundleId(), // e.g., "com.yourcompany.app"
  'service.build.number': getBuildNumber(), // e.g., "123"
  'os.name': getSystemName(), // "iOS"
  'os.version': getSystemVersion(), // e.g., "17.0"
  'device.model.identifier': getDeviceId(), // e.g., "iPhone14,2"
  'device.manufacturer': getBrand(), // "Apple"
};
```

**Why**: `react-native-device-info` provides consistent device information APIs. Use for analytics, tracing, debugging, and conditional feature support.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/networking-client/client/userAgent.ts:11`, `git-resources/shared-mobile-modules/src/libs/tracing/setupTracing.ts:53`

### Device-Specific Feature Detection

```typescript
import { getSystemVersion } from 'react-native-device-info';
import { Platform } from 'react-native';

const isIOS15OrHigher = (): boolean => {
  if (Platform.OS !== 'ios') return false;

  const version = getSystemVersion();
  const majorVersion = parseInt(version.split('.')[0], 10);

  return majorVersion >= 15;
};

// Usage
if (isIOS15OrHigher()) {
  // Use iOS 15+ feature
}
```

**Why**: Some APIs and features are iOS version-specific. Check system version before using version-dependent features to prevent crashes on older iOS versions.

## Platform-Specific Rendering

### Conditional Platform Rendering

```typescript
import { Platform, View, Text } from 'react-native';

const MyComponent = () => {
  return (
    <View>
      {Platform.OS === 'ios' ? (
        <IOSSpecificComponent />
      ) : (
        <AndroidSpecificComponent />
      )}

      <Text>Shared Content</Text>
    </View>
  );
};
```

**Why**: Inline conditional rendering works well for small platform differences. For larger differences, use platform-specific files (`.ios.tsx`, `.android.tsx`).

### Platform.select for Values

```typescript
import { Platform, StyleSheet } from 'react-native';

const HEADER_HEIGHT = Platform.select({
  ios: 44, // iOS standard navigation bar height
  android: 56,
  default: 50,
});

const FONT_FAMILY = Platform.select({
  ios: 'System', // iOS uses San Francisco
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
// MyComponent.ios.tsx - iOS-specific implementation
import { Alert } from 'react-native';

export const MyComponent = () => {
  const handlePress = () => {
    Alert.alert('iOS Only', 'This runs only on iOS');
  };

  return <Button onPress={handlePress}>Show Alert</Button>;
};

// MyComponent.android.tsx - Android-specific implementation
import { ToastAndroid } from 'react-native';

export const MyComponent = () => {
  const handlePress = () => {
    ToastAndroid.show('Android Only', ToastAndroid.SHORT);
  };

  return <Button onPress={handlePress}>Show Toast</Button>;
};
```

**Why**: React Native automatically loads `.ios.tsx` on iOS and `.android.tsx` on Android. This pattern completely separates platform-specific implementations, keeping code clean and maintainable.

## iOS Permissions

### Permission Protocol

**⚠️ IMPORTANT**: Any code requiring iOS runtime permissions needs explicit permission from native developers.

```typescript
// ❌ DON'T: Request permissions without approval
import { check, request, PERMISSIONS } from 'react-native-permissions';

const requestCameraPermission = async () => {
  const result = await request(PERMISSIONS.IOS.CAMERA);
  return result === 'granted';
};

// ✅ DO: Document permission requirements and get approval
/**
 * @requires-permission ios.permission.CAMERA
 * @permission-status APPROVED (Ticket: JIRA-123, Approved by: @native-team)
 */
const requestCameraPermission = async () => {
  const result = await request(PERMISSIONS.IOS.CAMERA);
  return result === 'granted';
};
```

**Why**: Runtime permissions affect user experience and App Store review. Native developers must verify permission necessity, implement Info.plist entries, and handle permission denial gracefully.

## iOS-Specific UI Patterns

### Blur Effects (iOS)

iOS supports native blur effects for overlays and modals:

```typescript
import { BlurView } from '@react-native-community/blur';

export const BlurredOverlay = ({ children }: BlurredOverlayProps) => {
  return (
    <BlurView
      style={StyleSheet.absoluteFill}
      blurType="light" // "light", "dark", "regular"
      blurAmount={10}
      reducedTransparencyFallbackColor="white"
    >
      {children}
    </BlurView>
  );
};
```

**Why**: iOS provides native blur effects that match system UI. Use for modals, overlays, or glassmorphism effects.

### Haptic Feedback (iOS)

```typescript
import ReactNativeHapticFeedback from 'react-native-haptic-feedback';
import { Platform } from 'react-native';

const triggerHaptic = () => {
  if (Platform.OS === 'ios') {
    ReactNativeHapticFeedback.trigger('impactLight', {
      enableVibrateFallback: true,
      ignoreAndroidSystemSettings: false,
    });
  }
};

// Haptic types for iOS:
// - "impactLight" - Gentle tap
// - "impactMedium" - Medium tap
// - "impactHeavy" - Strong tap
// - "selection" - Selection change
// - "notificationSuccess" - Success feedback
// - "notificationWarning" - Warning feedback
// - "notificationError" - Error feedback
```

**Why**: iOS Taptic Engine provides precise haptic feedback. Use to enhance tactile user experience for interactions like button presses, toggles, or confirmation actions.

## Testing iOS-Specific Code

### Mock Platform.OS

```typescript
import { Platform } from 'react-native';

describe('IOSComponent', () => {
  const originalOS = Platform.OS;

  afterEach(() => {
    Platform.OS = originalOS; // Restore original
  });

  it('should render on iOS', () => {
    Platform.OS = 'ios';

    const { getByTestId } = render(<IOSComponent />);

    expect(getByTestId('ios-feature')).toBeDefined();
  });

  it('should not render on Android', () => {
    Platform.OS = 'android';

    const { queryByTestId } = render(<IOSComponent />);

    expect(queryByTestId('ios-feature')).toBeNull();
  });
});
```

**Why**: Mocking Platform.OS enables testing platform-specific behavior without separate test runs per platform.

**Production Example**: `git-resources/shared-mobile-modules/src/features/webview/hooks/useWebViewBackHandler.test.ts:90`

### Mock useSafeAreaInsets

```typescript
jest.mock('react-native-safe-area-context', () => ({
  useSafeAreaInsets: () => ({
    top: 44,
    bottom: 34,
    left: 0,
    right: 0,
  }),
  SafeAreaView: ({ children }: { children: React.ReactNode }) => children,
}));

describe('Component with Safe Area', () => {
  it('should apply safe area insets', () => {
    const { getByTestId } = render(<MyComponent />);

    const element = getByTestId('close-button');
    const style = element.props.style;

    expect(style[1]).toEqual({ top: 44 + 12 }); // insets.top + padding
  });
});
```

**Why**: Mocking `useSafeAreaInsets` provides consistent test values and prevents test failures due to platform-specific safe area behavior.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/cookbook-menu-drawer/CookbookMenuDrawer.test.tsx:21`

### Mock react-native-device-info

```typescript
jest.mock('react-native-device-info', () => ({
  getBundleId: () => 'com.yourcompany.app',
  getSystemName: () => 'iOS',
  getSystemVersion: () => '17.0',
  getVersion: () => '5.2.1',
  getBrand: () => 'Apple',
  getApplicationName: () => 'YourCompany',
  getBuildNumber: () => '123',
  getDeviceId: () => 'iPhone14,2',
}));

describe('getUserAgent', () => {
  it('should return formatted user agent', () => {
    const userAgent = getUserAgent();

    expect(userAgent).toBe('YourCompany/com.yourcompany.app/ios');
  });
});
```

**Why**: Mocking device info ensures consistent test results across different test environments and CI systems.

## Common Mistakes to Avoid

❌ **Don't forget to specify edges on SafeAreaView**:

```typescript
// ❌ Applies insets to all edges (might not be desired)
<SafeAreaView>
  <Content />
</SafeAreaView>
```

**Why**: Without `edges` prop, `SafeAreaView` applies insets to all edges, which may add unwanted padding.

✅ **Do explicitly specify which edges need safe area**:

```typescript
// ✅ Only top edge gets safe area treatment
<SafeAreaView edges={['top']}>
  <Content />
</SafeAreaView>
```

**Why**: Explicit `edges` prop gives precise control over safe area behavior, preventing unwanted padding on edges that should extend to screen edges.

❌ **Don't use Android elevation without shadow properties on iOS**:

```typescript
// ❌ No shadow on iOS
const styles = StyleSheet.create({
  card: {
    elevation: 4, // Android only
    // Missing iOS shadow properties!
  },
});
```

**Why**: iOS ignores Android's `elevation` property. iOS requires shadow properties (`shadowColor`, `shadowOffset`, `shadowOpacity`, `shadowRadius`).

✅ **Do use Zest tokens for cross-platform shadows**:

```typescript
// ✅ Works on both platforms
const stylesConfig = {
  card: {
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.md.shadowOpacity',
    shadowRadius: 'global.shadow.md.shadowRadius',
    elevation: 'global.shadow.md.elevation', // Android fallback
  },
};
```

**Why**: Zest automatically applies correct shadow values for each platform, ensuring visual consistency without manual Platform.select.

❌ **Don't use backgroundColor on StatusBar for iOS**:

```typescript
// ❌ backgroundColor is ignored on iOS
<StatusBar
  barStyle="dark-content"
  backgroundColor="#FF0000" // Ignored on iOS
/>
```

**Why**: iOS StatusBar ignores `backgroundColor` prop. Android uses it, but iOS status bar is always transparent.

✅ **Do style the container instead**:

```typescript
// ✅ Control background color via container
<View style={{ backgroundColor: theme.colors.background }}>
  <StatusBar barStyle="dark-content" />
  <SafeAreaView edges={['top']}>
    <Content />
  </SafeAreaView>
</View>
```

**Why**: iOS status bar is transparent and shows the content behind it. Control background color on the container View.

❌ **Don't hardcode safe area values**:

```typescript
// ❌ Hardcoded values don't work across devices
const styles = StyleSheet.create({
  header: {
    paddingTop: 44, // Only correct for notched iPhones
  },
});
```

**Why**: Safe area insets vary by device (notched vs non-notched iPhones, iPads). Hardcoding values breaks on different devices.

✅ **Do use SafeAreaView or useSafeAreaInsets**:

```typescript
// ✅ Dynamic safe area handling
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const Header = () => {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ paddingTop: insets.top }}>
      <Text>Header</Text>
    </View>
  );
};
```

**Why**: `useSafeAreaInsets` provides actual safe area values for the current device, ensuring correct spacing across all iOS devices.

## Quick Reference

**Platform detection with PlatformIs**:
```typescript
import { PlatformIs } from '@libs/utils/platform';

if (PlatformIs.ios()) {
  // iOS-specific code
}
```

**Safe area with explicit edges**:
```typescript
<SafeAreaView edges={['top']}>
  <Content />
</SafeAreaView>
```

**Dynamic safe area positioning**:
```typescript
const insets = useSafeAreaInsets();
<View style={{ top: insets.top + 12 }} />
```

**Cross-platform shadows with Zest**:
```typescript
const stylesConfig = {
  card: {
    shadowColor: 'global.shadow.md.shadowColor',
    shadowOffset: {
      width: 'global.shadow.md.shadowOffset.width',
      height: 'global.shadow.md.shadowOffset.height',
    },
    shadowOpacity: 'global.shadow.md.shadowOpacity',
    shadowRadius: 'global.shadow.md.shadowRadius',
    elevation: 'global.shadow.md.elevation',
  },
};
```

**Status bar styling**:
```typescript
<StatusBar barStyle="dark-content" />
```

**Device information**:
```typescript
import { getVersion, getBundleId, getSystemName } from 'react-native-device-info';

const version = getVersion(); // "5.2.1"
const bundleId = getBundleId(); // "com.yourcompany.app"
const systemName = getSystemName(); // "iOS"
```

**Platform-specific values**:
```typescript
const HEADER_HEIGHT = Platform.select({
  ios: 44,
  android: 56,
  default: 50,
});
```

**Test mocking**:
```typescript
// Mock Platform.OS
Platform.OS = 'ios';

// Mock useSafeAreaInsets
jest.mock('react-native-safe-area-context', () => ({
  useSafeAreaInsets: () => ({ top: 44, bottom: 34, left: 0, right: 0 }),
}));

// Mock device info
jest.mock('react-native-device-info', () => ({
  getVersion: () => '5.2.1',
  getBundleId: () => 'com.yourcompany.app',
}));
```

**Key Libraries:**
- react-native 0.75.4
- react-native-safe-area-context 4.12.0
- react-native-device-info 14.0.0
- @zest/react-native 1.3.1

For production examples, see [references/examples.md](references/examples.md).
