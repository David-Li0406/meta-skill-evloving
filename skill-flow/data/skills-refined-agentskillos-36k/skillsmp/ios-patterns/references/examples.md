# iOS Patterns - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating iOS-specific patterns.

## Example 1: PlatformIs.ios() for Conditional Rendering

**File**: `features/customization-drawer/CustomizationDrawer.tsx:77`

This example shows using PlatformIs.ios() for platform-specific drawer sizing.

```typescript
import { useWindowDimensions } from 'react-native';
import { PlatformIs } from '@libs/utils';
import { Drawer } from '@zest/react-native';

export const CustomizationDrawer = () => {
  const { height: windowHeight } = useWindowDimensions();
  const { isVisible, footerOffset, handleDismiss } =
    useCustomizationDrawerUi({ customizationId, setCustomizationId });

  const screenHeight = windowHeight - footerOffset;

  return (
    <Drawer
      testID="customization-drawer"
      visible={isVisible}
      onDismiss={handleDismiss}
      hideCloseButton
      sizes={[PlatformIs.ios() ? 'auto' : screenHeight]}
      Footer={<TrackedFooter />}
    >
      <Content />
    </Drawer>
  );
};
```

**Key patterns demonstrated:**
- PlatformIs.ios() for readable platform check
- Platform-specific drawer sizing (iOS uses 'auto', Android uses calculated height)
- useWindowDimensions for screen dimensions
- Conditional expression based on platform
- Import from @libs/utils

## Example 2: SafeAreaView with Explicit Edges

**File**: `modules/store/screens/cart/layouts/default/default.tsx:68`

This example shows SafeAreaView with explicit edges prop for cart screen.

```typescript
import { ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useZestStyles } from '@zest/react-native';

export const DefaultLayout = (props) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <Header />
      <FloatingStoreButtonWrapper screen={StoreStackRoutes.Cart}>
        <ScrollView
          style={styles.scrollContainer}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={[styles.scrollContentContainer]}
        >
          <MealProductsList />
          {hasMarketAddons && (
            <>
              <UpsellCarousel />
              <ProductsList isAddon />
            </>
          )}
          <DeliveryInfo />
          <PriceSummary />
        </ScrollView>
      </FloatingStoreButtonWrapper>
    </SafeAreaView>
  );
};
```

**Key patterns demonstrated:**
- SafeAreaView with explicit edges={['top']} for top-only insets
- Only apply safe area to top edge (custom bottom UI with floating button)
- ScrollView with content inside safe area
- FloatingStoreButtonWrapper manages bottom UI outside safe area
- Styled with useZestStyles

## Example 3: useSafeAreaInsets for Dynamic Positioning

**File**: `modules/loyalty-program/screens/components/close-button/CloseButton.tsx:18`

This example shows using useSafeAreaInsets for dynamic close button positioning.

```typescript
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import type { CloseButtonPlacement } from '@zest/react-native';
import { CloseButton, useZestStyles } from '@zest/react-native';

import { stylesConfig } from './styles';

interface LoyaltyCloseButtonProps {
  placement?: CloseButtonPlacement;
  onPress?: () => void;
}

export const LoyaltyCloseButton = ({
  placement = 'overAssets',
  onPress,
}: LoyaltyCloseButtonProps) => {
  const styles = useZestStyles(stylesConfig);
  const insets = useSafeAreaInsets();

  return (
    <CloseButton
      placement={placement}
      onPress={onPress}
      style={[styles.closeButton, { top: insets.top }]}
      testID="close-button"
    />
  );
};
```

**Key patterns demonstrated:**
- useSafeAreaInsets hook for dynamic inset values
- Apply insets.top directly to style for positioning
- Array style syntax for combining static and dynamic styles
- No hardcoded padding values
- Works across all iOS devices (notched and non-notched)
- TypeScript interface for props
- Default placement value

## Example 4: Zest Shadow Tokens for iOS Shadows

**File**: `features/product-card-feature/variants/skipped/components/style.ts:8`

This example shows using Zest shadow tokens for cross-platform shadows.

```typescript
import { createStylesConfig } from '@zest/react-native';

export const skippedLargeCardStylesConfig = createStylesConfig({
  container: {
    backgroundColor: 'alias.color.neutral.background.default',
    shadowColor: 'global.shadow.sm.shadowColor',
    shadowOffset: {
      width: 'global.shadow.sm.shadowOffset.width',
      height: 'global.shadow.sm.shadowOffset.height',
    },
    elevation: 'global.shadow.sm.elevation',
    shadowRadius: 'global.shadow.sm.shadowRadius',
    shadowOpacity: 'global.shadow.sm.shadowOpacity',
  },
  image: {
    borderTopLeftRadius: 'global.borderRadius.md',
    borderTopRightRadius: 'global.borderRadius.md',
  },
  imageDimmed: {
    opacity: 'global.opacity.50',
  },
  favoriteButton: {
    position: 'absolute',
    top: 'global.spacing.xs',
    left: 'global.spacing.xs',
    zIndex: Z_INDEXES.favorite,
  },
});
```

**Key patterns demonstrated:**
- global.shadow.sm tokens for small shadow
- All iOS shadow properties (shadowColor, shadowOffset, shadowOpacity, shadowRadius)
- elevation token for Android fallback
- createStylesConfig for Zest integration
- Consistent shadow across platforms without Platform.select
- Other Zest tokens (color, spacing, borderRadius, opacity)
- TypeScript type inference

## Example 5: Device Info for User Agent

**File**: `libs/networking-client/client/userAgent.ts:11`

This example shows using react-native-device-info for user agent construction.

```typescript
import DeviceInfo from 'react-native-device-info';

const FRAMEWORK_NAME = 'FetchClient';

/**
 * Generates a User-Agent string matching the native iOS format:
 * {name}/{version} ({bundleIdentifier}; build:{build}; {systemModel} {systemVersion}) {frameworkName}
 *
 * Example: YourCompany/1.2.3 (com.yourcompany.app; build:123; iPhone14,2 iOS 17.0) FetchClient
 */
export const getUserAgent = (): string => {
  const name = DeviceInfo.getApplicationName(); // e.g., "YourCompany"
  const version = DeviceInfo.getVersion(); // e.g., "1.2.3"
  const bundleIdentifier = DeviceInfo.getBundleId(); // e.g., "com.yourcompany.app"
  const build = DeviceInfo.getBuildNumber(); // e.g., "123"
  const systemModel = DeviceInfo.getModel(); // e.g., "iPhone 14 Pro" or "Pixel 7"
  const systemName = DeviceInfo.getSystemName(); // e.g., "iOS" or "Android"
  const systemVersion = DeviceInfo.getSystemVersion(); // e.g., "17.0" or "14"

  return `${name}/${version} (${bundleIdentifier}; build:${build}; ${systemModel} ${systemName} ${systemVersion}) ${FRAMEWORK_NAME}`;
};
```

**Key patterns demonstrated:**
- DeviceInfo import from react-native-device-info
- getApplicationName() for app name
- getVersion() for app version
- getBundleId() for bundle identifier
- getBuildNumber() for build number
- getModel() for device model
- getSystemName() for OS name (iOS/Android)
- getSystemVersion() for OS version
- String template construction
- JSDoc with example output
- Inline comments explaining return values

## Example 6: Device Info for Tracing Attributes

**File**: `libs/tracing/setupTracing.ts:53`

This example shows using react-native-device-info for OpenTelemetry tracing attributes.

```typescript
import { resourceFromAttributes } from '@opentelemetry/resources';
import {
  ATTR_SERVICE_NAME,
  ATTR_SERVICE_VERSION,
} from '@opentelemetry/semantic-conventions';
import {
  getBundleId,
  getDeviceId,
  getSystemName,
  getSystemVersion,
  getVersion,
  getBrand,
  getApplicationName,
  getBuildNumber,
} from 'react-native-device-info';
import uuid from 'react-native-uuid';

const setupTracing = () => {
  /**
   * @property [ATTR_SERVICE_NAME] - The name of the application (YourCompany, Factor, etc.).
   * @property [ATTR_SERVICE_VERSION] - The version of the app.
   * @property ['service.brand'] - The brand name of the application (YourCompany, Factor, GreenChef, etc.).
   * @property ['service.bundle.identifier'] - The bundle ID of the app (com.yourcompany.app, com.factor.app, etc.).
   * @property ['service.build.number'] - The build number of the app for identifying specific builds.
   * @property ['telemetry.distro.name'] - The name of the telemetry distribution (shared-mobile-modules).
   * @property ['os.name'] - The name of the operating system (iOS, Android, etc.).
   * @property ['os.version'] - The version of the operating system.
   * @property ['device.model.identifier'] - The unique identifier of the device.
   * @property ['device.manufacturer'] - The manufacturer of the device (Apple, Google, Xiaomi, etc.).
   */
  const appAndPlatformAttributes = resourceFromAttributes({
    [ATTR_SERVICE_NAME]: 'mobile-app',
    [ATTR_SERVICE_VERSION]: getVersion(),
    ['service.brand']: getApplicationName(),
    ['service.bundle.identifier']: getBundleId(),
    ['service.build.number']: getBuildNumber(),
    ['telemetry.distro.name']: 'shared-mobile-modules',
    ['os.name']: getSystemName(),
    ['os.version']: getSystemVersion(),
    ['device.model.identifier']: getDeviceId(),
    ['device.manufacturer']: getBrand(),
    ['application.instance.id']: uuid.v4(),
  });

  // ... rest of tracing setup
};
```

**Key patterns demonstrated:**
- Multiple device info APIs in one object
- resourceFromAttributes from OpenTelemetry
- Semantic conventions (ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION)
- Custom attributes with bracket notation
- JSDoc documenting each attribute
- getVersion() for app version
- getApplicationName() for brand name
- getBundleId() for bundle identifier
- getBuildNumber() for build number
- getSystemName() for OS name
- getSystemVersion() for OS version
- getDeviceId() for device model identifier
- getBrand() for device manufacturer
- uuid.v4() for application instance ID

## Example 7: Testing Platform.OS Mocking

**File**: `features/webview/hooks/useWebViewBackHandler.test.ts:90`

This example shows mocking Platform.OS in tests for platform-specific behavior.

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
});
```

**Key patterns demonstrated:**
- Mock Platform module before tests
- Set Platform.OS = 'ios' for iOS-specific tests
- Restore original Platform.OS after each test
- Test platform-specific behavior without running on device
- renderHook for testing custom hooks
- expect().not.toHaveBeenCalled() for negative assertions
- Mock BackHandler module for Android-specific behavior
- require() to access mocked module and modify OS

## Example 8: Testing useSafeAreaInsets Mocking

**File**: `modules/social-recipe-bridge/screens/cookbook-menu-drawer/CookbookMenuDrawer.test.tsx:21`

This example shows mocking useSafeAreaInsets for consistent test values.

```typescript
import { render, fireEvent, screen } from '@testing-library/react-native';
import { CookbookMenuDrawer } from './CookbookMenuDrawer';

jest.mock('@libs/localization', () => ({
  useT9n: () => ({
    translateRaw: (key: string) => key,
  }),
}));

jest.mock('react-native-safe-area-context', () => ({
  useSafeAreaInsets: () => ({
    top: 44,
    bottom: 34,
    left: 0,
    right: 0,
  }),
}));

jest.mock('@zest/react-native', () => ({
  ...jest.requireActual('@zest/react-native'),
  Overlay: jest.fn(({ onClose, testID, accessibilityLabel }) => {
    const React = require('react');
    const { TouchableOpacity } = require('react-native');

    return React.createElement(TouchableOpacity, {
      testID,
      onPress: onClose,
      accessibilityLabel,
    });
  }),
}));

describe('CookbookMenuDrawer', () => {
  it('should render with safe area insets', () => {
    const { getByTestId } = render(<CookbookMenuDrawer />);

    // Component uses mocked insets (top: 44)
    expect(getByTestId('cookbook-menu-drawer')).toBeDefined();
  });
});
```

**Key patterns demonstrated:**
- Mock react-native-safe-area-context before tests
- Return fixed inset values for consistency
- Mock useSafeAreaInsets hook with specific values
- Notched iPhone values (top: 44, bottom: 34)
- Mock other dependencies (@libs/localization, @zest/react-native)
- jest.requireActual() to preserve actual implementation
- Multiple mocks in single test file
- Clear test description

## Summary

The YourCompany codebase consistently follows these iOS platform patterns:

1. **PlatformIs.ios()** for readable platform detection (vs Platform.OS === 'ios')
2. **SafeAreaView with explicit edges** for granular safe area control
3. **useSafeAreaInsets** for dynamic positioning and calculations
4. **Zest shadow tokens** for cross-platform shadow consistency (shadowColor, shadowOffset, shadowOpacity, shadowRadius, elevation)
5. **react-native-device-info** for device/system information (getVersion, getBundleId, getSystemName, etc.)
6. **Platform.select** for platform-specific values (dimensions, fonts, constants)
7. **Platform-specific files** (.ios.tsx, .android.tsx) for significant platform differences
8. **StatusBar barStyle** for iOS status bar styling (light-content, dark-content)
9. **Platform.OS mocking** in tests for cross-platform behavior validation
10. **useSafeAreaInsets mocking** with notched iPhone values (top: 44, bottom: 34)

These patterns ensure native iOS user experience with proper safe area handling, shadows, device information, and testable platform-specific behavior throughout the app.
