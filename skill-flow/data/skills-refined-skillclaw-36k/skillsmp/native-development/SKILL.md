---
name: native-development
description: "WHAT: Native module development with NativeModules and NativeEventEmitter. WHEN: creating native modules, integrating SDKs, implementing JS-native bridge. KEYWORDS: native, NativeModules, NativeEventEmitter, Proxy, bridge, SharedModules, TypeScript, permission, fallback."
---

# Native Development

## Core Principles

**Always request permission before native changes.** Native code changes affect app stability, require native team review, and can impact both iOS and Android platforms. Follow the permission protocol for all native modifications.

**Use Proxy fallback for missing native modules.** Native modules may be unavailable during development, testing, or when running shared modules in regular React Native apps. Proxy with error handlers provides graceful degradation.

**Wrap native modules with TypeScript interfaces.** Direct NativeModules access lacks type safety. Create typed wrapper objects (SharedModules* prefix) that match native APIs for compile-time type checking.

**Use NativeEventEmitter for native-to-JS communication.** One-way async calls work for most native functionality, but bidirectional communication requires NativeEventEmitter for native-initiated events.

**Why**: Native development requires careful coordination between JS and native layers. These patterns ensure type safety, testability, error handling, and maintainability for React Native bridge code.

## When to Use This Skill

Use these patterns when:

- Creating new native modules for platform-specific functionality
- Integrating existing native SDKs or libraries
- Implementing performance-critical native operations
- Building bidirectional communication between JS and native
- Testing code that depends on native modules
- Handling missing native modules gracefully
- Requesting native changes from platform team
- Working with native events or callbacks
- Wrapping native APIs with type-safe interfaces

## Permission Protocol

### Native Change Request Template

**⚠️ CRITICAL**: All native changes require explicit approval before implementation.

```
🔒 NATIVE PERMISSION REQUEST

Files:
- ios/YourCompany/AppDelegate.mm (adding notification setup)
- android/app/src/main/java/com/yourcompany/MainActivity.java (adding notification handling)

Changes:
- Integrate Firebase Cloud Messaging for push notifications
- Add notification permission requests on app launch
- Implement notification tap handlers

Impact:
- User will see permission dialog on first app launch
- Affects app startup time (+50ms estimated)
- Requires Info.plist and AndroidManifest.xml updates
- New runtime permissions required

Type "APPROVED" to proceed.
```

**Why**: Native changes can affect:
- App stability and crash rates
- App Store / Play Store review
- User permissions and privacy
- Build configuration and dependencies
- Multiple teams (iOS, Android, JS)

**Production Example**: Request template from `previous-standards/platform/native-development.md:21`

### Permission Request Components

```typescript
// ❌ DON'T: Make native changes without approval
const MyNativeModule = NativeModules.NewFeature;
MyNativeModule.doSomething();

// ✅ DO: Document and request approval first
/**
 * @requires-native-module NewFeature
 * @platform ios, android
 * @permission-status REQUESTED (Ticket: MOBILE-123)
 * @native-team @ios-team, @android-team
 *
 * Native changes required:
 * - iOS: Add NewFeature.swift with doSomething() method
 * - Android: Add NewFeatureModule.kt with doSomething() method
 */
const MyNativeModule = NativeModules.NewFeature;
```

**Why**: Clear documentation helps native teams understand requirements, estimate effort, and plan implementation across platforms.

## Native Module Access

### Basic Native Module Pattern

```typescript
import { NativeModules } from 'react-native';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

const NavigationModule = NativeModules.SharedModulesNavigation;
const Navigation = NavigationModule
  ? NavigationModule
  : new Proxy(
      {},
      {
        get: () => {
          nativeSharedModuleFetchError('Navigation');
        },
      }
    );

const SharedModulesNavigation = {
  getInitialURL: async (): Promise<string | null> => {
    const { initialURL } = await Navigation.getInitialURL();
    return initialURL;
  },

  popToNative: () => Navigation.popToNative(),
};

export { SharedModulesNavigation };
```

**Why**:
- Check if native module exists (NavigationModule ?)
- Proxy fallback provides graceful error when module missing
- Wrapper object (SharedModulesNavigation) provides clean, typed API
- Async methods for native bridge calls
- Export wrapper instead of raw native module

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/navigation/Navigation.ts:1`

### Native Module with TypeScript Interface

```typescript
import { NativeModules } from 'react-native';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

import type { PerformanceTrackerModule } from './PerformanceTrackerInterface';

const PerformanceTrackerModuleBase =
  NativeModules.SharedModulesPerformanceTracker;

const PerformanceTracker: PerformanceTrackerModule =
  PerformanceTrackerModuleBase
    ? PerformanceTrackerModuleBase
    : new Proxy(
        {},
        {
          get: () => {
            nativeSharedModuleFetchError('PerformanceTracker');
          },
        }
      );

const SharedModulesPerformanceTracker: PerformanceTrackerModule = {
  start: async (traceName: string): Promise<void> => {
    return PerformanceTracker.start(traceName);
  },

  stop: async (traceName: string): Promise<void> => {
    return PerformanceTracker.stop(traceName);
  },

  record: async ({
    traceName,
    userInfo,
  }: {
    traceName: string;
    userInfo: object;
  }): Promise<void> => {
    return PerformanceTracker.record({ traceName, userInfo });
  },
};

export { SharedModulesPerformanceTracker };
```

**Why**:
- TypeScript interface ensures type safety
- Proxy typed with interface (PerformanceTracker: PerformanceTrackerModule)
- Wrapper implements same interface
- Multiple async methods with different signatures
- Destructured parameters for complex arguments
- Consistent naming convention (SharedModules prefix)

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/performance-tracker/PerformanceTracker.ts:1`

## Native Event Communication

### NativeEventEmitter for Native-to-JS Events

```typescript
import { NativeModules, NativeEventEmitter } from 'react-native';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

import type { JSToNativeEventName } from './JSToNativeEventName';
import type { NativeToJSEventName } from './NativeToJSEventName';
import type {
  SendGetRepositoryEventBody,
  SendSetRepositoryEventBody,
  SendUpdateEventBody,
} from './types';

const EventsModule = NativeModules.SharedModulesEvents;
const Events = EventsModule
  ? EventsModule
  : new Proxy(
      {},
      {
        get: () => {
          nativeSharedModuleFetchError('Events');
        },
      }
    );

class EventEmitter {
  private _eventEmitter = new NativeEventEmitter(Events);

  addListener(
    eventType: NativeToJSEventName,
    listener: (event: object) => void
  ) {
    return this._eventEmitter.addListener(eventType, listener);
  }

  removeAllListeners(eventType: NativeToJSEventName): void {
    this._eventEmitter.removeAllListeners(eventType);
  }
}

const SharedModulesEventEmitter = new EventEmitter();

async function sendEvent(
  name: JSToNativeEventName,
  body?:
    | SendGetRepositoryEventBody
    | SendSetRepositoryEventBody
    | SendUpdateEventBody
): Promise<unknown> {
  return Events.sendEvent(name, body);
}

export { sendEvent, SharedModulesEventEmitter };
```

**Why**:
- NativeEventEmitter for native-to-JS events
- Class wrapper for event handling logic
- Private _eventEmitter instance
- addListener returns subscription for cleanup
- removeAllListeners for bulk cleanup
- Separate function (sendEvent) for JS-to-native
- Type unions for different event body shapes
- Export singleton instance

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/events/Events.ts:1`

### Bidirectional Event Flow

```typescript
// Native-to-JS: Listen for events from native
const subscription = SharedModulesEventEmitter.addListener(
  'nativeToJS/repositoryUpdated',
  (event) => {
    console.log('Repository updated:', event);
  }
);

// Clean up listener
subscription.remove();

// JS-to-Native: Send events to native
await sendEvent('jsToNative/updateRepository', {
  repository: 'feature-flags',
  data: JSON.stringify({ enabled: true }),
});
```

**Why**:
- Native-to-JS uses NativeEventEmitter.addListener
- JS-to-native uses native module method (sendEvent)
- Subscription cleanup prevents memory leaks
- Type-safe event names and bodies
- Async await for native bridge calls

## Error Handling

### Centralized Error Factory

```typescript
// libs/native-modules/commons/NativeModuleErrors.ts
export const nativeSharedModuleFetchError = (moduleName: string): Error => {
  return new Error(
    `Tried to call a ${moduleName} Shared Modules native module, but it is not present. \
    This might happen if you're calling the SharedModulesEvents module in a regular React Native app.`
  );
};
```

**Why**:
- Consistent error messages across all native modules
- Module name parameter for context
- Helpful message explaining when error occurs
- Single source of truth for error format
- Reusable across all native module wrappers

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/commons/NativeModuleErrors.ts:1`

### Proxy Error Handler

```typescript
const MyModule = NativeModules.MyFeature;
const Module = MyModule
  ? MyModule
  : new Proxy(
      {},
      {
        get: () => {
          throw nativeSharedModuleFetchError('MyFeature');
        },
      }
    );
```

**Why**:
- Proxy intercepts all property access
- get trap throws descriptive error
- Any method call on missing module throws
- Consistent error across all methods
- No need to check every method individually

## Conditional Native Logic

### E2E Testing Fallback

```typescript
import { NativeModules } from 'react-native';
import { isE2ETesting } from '@data-access/maestro/MaestroMockStore';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

import type { FeatureToggleProvider } from './FeatureToggleProviderInterface';
import { isFeatureToggleEnabledForTest } from './isFeatureToggleEnabled.e2e';

const FeatureToggleModuleBase =
  NativeModules.SharedModulesFeatureToggleProvider;

const FeatureToggle = FeatureToggleModuleBase
  ? FeatureToggleModuleBase
  : new Proxy(
      {},
      {
        get: () => {
          nativeSharedModuleFetchError('FeatureToggle');
        },
      }
    );

const SharedModulesFeatureToggle: FeatureToggleProvider = {
  isEnabled: async (parameters): Promise<boolean> => {
    if (isE2ETesting()) {
      // Use mock implementation during E2E tests
      return isFeatureToggleEnabledForTest(
        parameters.featureKey,
        parameters.attributes
      );
    }

    return await FeatureToggle.isEnabled(parameters);
  },
};

export { SharedModulesFeatureToggle };
```

**Why**:
- Check isE2ETesting() before native call
- Use mock implementation during E2E tests
- Fall back to real native module in production
- E2E tests don't require native module
- Conditional logic in wrapper, not at call site

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/feature-toggle/FeatureToggle.ts:1`

## Testing Native Modules

### Mock NativeModules

```typescript
import { NativeModules } from 'react-native';

jest.mock('react-native', () => ({
  NativeModules: {},
}));

jest.mock('@libs/native-modules/commons/NativeModuleErrors', () => ({
  nativeSharedModuleFetchError: jest.fn(() => {
    throw new Error('Mocked native module missing error');
  }),
}));

describe('SharedModulesNavigation', () => {
  const mockGetInitialURL = jest
    .fn()
    .mockResolvedValue({ initialURL: 'factor://plan/123' });

  const mockPopToNative = jest.fn();

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('calls NativeModules implementation when available', async () => {
    NativeModules.SharedModulesNavigation = {
      getInitialURL: mockGetInitialURL,
      popToNative: mockPopToNative,
    };

    const { SharedModulesNavigation } = await import('./Navigation');

    const result = await SharedModulesNavigation.getInitialURL();

    expect(mockGetInitialURL).toHaveBeenCalled();
    expect(result).toBe('factor://plan/123');

    await SharedModulesNavigation.popToNative();

    expect(mockPopToNative).toHaveBeenCalled();
  });

  it('throws error when native module is unavailable', async () => {
    delete NativeModules.SharedModulesNavigation;

    const { SharedModulesNavigation } = await import('./Navigation');

    await expect(SharedModulesNavigation.getInitialURL()).rejects.toThrow(
      'Mocked native module missing error'
    );
  });
});
```

**Why**:
- Mock react-native module with jest.mock
- Mock NativeModules as empty object
- Mock nativeSharedModuleFetchError function
- Create mock functions with jest.fn()
- mockResolvedValue for async methods
- jest.resetModules() prevents test pollution
- Dynamic import (await import) for each test
- Test both success and error cases
- delete operator to simulate missing module

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/navigation/Navigation.spec.ts:1`

### Mock NativeEventEmitter

```typescript
import { NativeModules, NativeEventEmitter } from 'react-native';

jest.mock('react-native', () => {
  return {
    NativeModules: {},
    NativeEventEmitter: jest.fn().mockImplementation(() => ({
      addListener: jest.fn(),
      removeAllListeners: jest.fn(),
    })),
  };
});

describe('SharedModulesEventEmitter', () => {
  const mockSendEvent = jest.fn();

  it('should call addListener and removeAllListeners', async () => {
    NativeModules.SharedModulesEvents = {
      sendEvent: mockSendEvent,
    };

    const { sendEvent, SharedModulesEventEmitter } = await import('./Events');

    const listener = jest.fn();
    SharedModulesEventEmitter.addListener('nativeToJS/test', listener);
    SharedModulesEventEmitter.removeAllListeners('nativeToJS/test');

    expect(NativeEventEmitter).toHaveBeenCalledWith(
      NativeModules.SharedModulesEvents
    );

    const instance = (NativeEventEmitter as jest.Mock).mock.results[0]!.value;
    expect(instance.addListener).toHaveBeenCalledWith(
      'nativeToJS/test',
      listener
    );
    expect(instance.removeAllListeners).toHaveBeenCalledWith('nativeToJS/test');
  });
});
```

**Why**:
- Mock NativeEventEmitter with mockImplementation
- Return mock addListener and removeAllListeners
- Test both sendEvent and EventEmitter
- Access mock.results to verify constructor calls
- Verify NativeEventEmitter constructed with module
- Test bidirectional communication

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/events/Events.spec.ts:1`

## Common Mistakes to Avoid

❌ **Don't access NativeModules directly without fallback**:

```typescript
// ❌ Crashes when native module missing
import { NativeModules } from 'react-native';

const result = await NativeModules.MyFeature.doSomething();
```

**Why**: Native module may be unavailable during development, testing, or in different app configurations. Direct access crashes with "undefined is not an object".

✅ **Do use Proxy fallback for graceful error**:

```typescript
// ✅ Graceful error when module missing
import { NativeModules } from 'react-native';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

const MyFeatureModule = NativeModules.MyFeature;
const MyFeature = MyFeatureModule
  ? MyFeatureModule
  : new Proxy(
      {},
      {
        get: () => {
          throw nativeSharedModuleFetchError('MyFeature');
        },
      }
    );

const SharedModulesMyFeature = {
  doSomething: async () => {
    return MyFeature.doSomething();
  },
};
```

**Why**: Proxy provides graceful error with context, wrapper provides typed API, error message helps debug missing module.

❌ **Don't forget to remove event listeners**:

```typescript
// ❌ Memory leak - listener never removed
useEffect(() => {
  SharedModulesEventEmitter.addListener('nativeToJS/event', handleEvent);
  // Missing cleanup!
}, []);
```

**Why**: Event listeners remain active after component unmounts, causing memory leaks and potential crashes when events fire.

✅ **Do clean up event listeners**:

```typescript
// ✅ Proper cleanup
useEffect(() => {
  const subscription = SharedModulesEventEmitter.addListener(
    'nativeToJS/event',
    handleEvent
  );

  return () => subscription.remove();
}, [handleEvent]);
```

**Why**: subscription.remove() in cleanup function ensures listener is removed when component unmounts, preventing memory leaks.

❌ **Don't make native changes without permission**:

```typescript
// ❌ No permission requested
// Added native module without approval
const MyNewModule = NativeModules.MyNewFeature;
MyNewModule.experimentalFeature();
```

**Why**: Native changes affect app stability, require iOS/Android team coordination, can impact App Store review, and need testing on both platforms.

✅ **Do request permission with clear documentation**:

```typescript
// ✅ Permission requested with documentation
/**
 * @requires-native-module MyNewFeature
 * @permission-status APPROVED (Ticket: MOBILE-456, Approved by: @native-team)
 * @platform ios, android
 *
 * Native implementation:
 * - iOS: MyNewFeature.swift with experimentalFeature() method
 * - Android: MyNewFeatureModule.kt with experimentalFeature() method
 */
const MyNewModule = NativeModules.MyNewFeature;
```

**Why**: Clear documentation helps native teams plan implementation, review impact, and coordinate across platforms.

❌ **Don't skip TypeScript interfaces**:

```typescript
// ❌ No type safety
const SharedModulesFeature = {
  doSomething: (param) => {
    return NativeModules.Feature.doSomething(param);
  },
};
```

**Why**: No type checking for parameters or return values, easy to make mistakes, no IDE autocomplete.

✅ **Do use TypeScript interfaces**:

```typescript
// ✅ Type-safe with interface
interface FeatureModule {
  doSomething(param: string): Promise<{ result: boolean }>;
}

const SharedModulesFeature: FeatureModule = {
  doSomething: async (param: string): Promise<{ result: boolean }> => {
    return NativeModules.Feature.doSomething(param);
  },
};
```

**Why**: Compile-time type checking, IDE autocomplete, prevents passing wrong types, documents expected types.

## Quick Reference

**Basic native module with fallback**:
```typescript
import { NativeModules } from 'react-native';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

const MyModule = NativeModules.MyFeature;
const Module = MyModule
  ? MyModule
  : new Proxy({}, { get: () => { throw nativeSharedModuleFetchError('MyFeature'); } });

const SharedModulesMyFeature = {
  doSomething: async () => Module.doSomething(),
};
```

**NativeEventEmitter for native-to-JS events**:
```typescript
import { NativeEventEmitter } from 'react-native';

const eventEmitter = new NativeEventEmitter(Module);
const subscription = eventEmitter.addListener('eventName', handler);
subscription.remove(); // Cleanup
```

**Permission request template**:
```
🔒 NATIVE PERMISSION REQUEST
Files: [list]
Changes: [describe]
Impact: [affected areas]
Type "APPROVED" to proceed.
```

**Testing native modules**:
```typescript
jest.mock('react-native', () => ({ NativeModules: {} }));
jest.mock('@libs/native-modules/commons/NativeModuleErrors', () => ({
  nativeSharedModuleFetchError: jest.fn(() => { throw new Error('Mock error'); }),
}));

NativeModules.MyFeature = { method: jest.fn() };
const { SharedModulesMyFeature } = await import('./MyFeature');
```

**Error handling**:
```typescript
export const nativeSharedModuleFetchError = (moduleName: string): Error => {
  return new Error(`Module ${moduleName} not present`);
};
```

**Key Libraries:**
- react-native 0.75.4

For production examples, see [references/examples.md](references/examples.md).
