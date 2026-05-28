# Native Development - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating native module integration patterns.

## Example 1: Basic Native Module with Proxy Fallback

**File**: `libs/native-modules/navigation/Navigation.ts:1`

This example shows basic native module access with Proxy fallback for graceful error handling.

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
  /**
   * The React Native linking module works the best when React Native controls the app entry point.
   * However since the app entry point is mainly controlled by the consumer native apps, we need them to be able to pass
   * custom deep linking data. This function is handy in this case where the consumer app needs to pass custom deep links to the shared modules.
   *
   * Note: You can keep using React Native's own Linking module for listening to deep link events. This module is only used to get the initial URL.
   * Note: This doesn't respect the application's initialURL. The consumer app has to explicitly set it via the shared modules on the native side. This will always return `null` otherwise.
   */
  getInitialURL: async (): Promise<string | null> => {
    const { initialURL } = await Navigation.getInitialURL();
    return initialURL;
  },

  popToNative: () => Navigation.popToNative(),
};

export { SharedModulesNavigation };
```

**Key patterns demonstrated:**
- NativeModules import from react-native
- Check if native module exists (NavigationModule ?)
- Proxy fallback for graceful error handling when module missing
- nativeSharedModuleFetchError for consistent error messages
- Wrapper object (SharedModulesNavigation) for clean API
- Async method for native bridge calls (getInitialURL)
- Sync method for simple native calls (popToNative)
- JSDoc comments explaining native integration details
- Export wrapper instead of raw native module

## Example 2: Native Event Emitter for Bidirectional Communication

**File**: `libs/native-modules/events/Events.ts:1`

This example shows NativeEventEmitter for listening to events from native side.

```typescript
import { NativeModules, NativeEventEmitter } from 'react-native';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

import type { JSToNativeEventName } from './JSToNativeEventName';
import type { NativeToJSEventName } from './NativeToJSEventName';
import type {
  SendGetRepositoryEventBody,
  SendPostPermissionResultEventBody,
  SendSetRepositoryEventBody,
  SendUpdateEventBody,
  SendProfileEventsBodies,
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

  /**
   * Adds a listener to the certain event
   * @returns a callback to remove the listener
   */
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

/**
 * Allows listening for events from the native side
 */
const SharedModulesEventEmitter = new EventEmitter();

// eslint-disable-next-line prefer-arrow/prefer-arrow-functions
async function sendEvent(
  name: JSToNativeEventName,
  body?:
    | SendGetRepositoryEventBody
    | SendSetRepositoryEventBody
    | SendUpdateEventBody
    | SendPostPermissionResultEventBody
    | SendProfileEventsBodies
): Promise<unknown> {
  return Events.sendEvent(name, body);
}

export { sendEvent, SharedModulesEventEmitter };
```

**Key patterns demonstrated:**
- NativeEventEmitter for native-to-JS events
- Class wrapper (EventEmitter) for event handling
- Private _eventEmitter instance
- addListener returns subscription for cleanup
- removeAllListeners for cleaning all listeners
- Separate function (sendEvent) for JS-to-native communication
- Type unions for different event body types
- JSToNativeEventName vs NativeToJSEventName types
- Export singleton instance (SharedModulesEventEmitter)
- Async sendEvent for native bridge communication

## Example 3: Native Module with TypeScript Interface

**File**: `libs/native-modules/performance-tracker/PerformanceTracker.ts:1`

This example shows TypeScript interface for type-safe native module access.

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
  incrementMetric: async ({
    traceName,
    metricName,
    value,
  }: {
    traceName: string;
    metricName: string;
    value: number;
  }): Promise<void> => {
    return PerformanceTracker.incrementMetric({
      traceName,
      metricName,
      value,
    });
  },
};

export { SharedModulesPerformanceTracker };
```

**Key patterns demonstrated:**
- TypeScript interface import (PerformanceTrackerModule)
- Type annotation on Proxy (PerformanceTracker: PerformanceTrackerModule)
- Wrapper object with same interface type
- Multiple async methods with different signatures
- Destructured parameters for complex method arguments
- Consistent naming (SharedModules prefix)
- All methods return Promise<void>
- Explicit parameter types in wrapper methods

## Example 4: Native Module with Conditional Logic

**File**: `libs/native-modules/feature-toggle/FeatureToggle.ts:1`

This example shows native module with conditional E2E testing logic.

```typescript
import { NativeModules } from 'react-native';
import { isE2ETesting } from '@data-access/maestro/MaestroMockStore';
import { nativeSharedModuleFetchError } from '@libs/native-modules/commons';

import type {
  FeatureToggleProvider,
  FeatureToggleParameters,
} from './FeatureToggleProviderInterface';
import { isFeatureToggleEnabledForTest } from './isFeatureToggleEnabled.e2e';

const FeatureToggleModuleBase =
  NativeModules.SharedModulesFeatureToggleProvider;
// Native module interface (uses individual parameters)
interface NativeFeatureToggleModule {
  isEnabled(parameters: FeatureToggleParameters): Promise<boolean>;
}

const FeatureToggle: NativeFeatureToggleModule = FeatureToggleModuleBase
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
  isEnabled: async (parameters: FeatureToggleParameters): Promise<boolean> => {
    if (isE2ETesting()) {
      // If E2E testing, check if the feature toggle is enabled for the current test
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

**Key patterns demonstrated:**
- Conditional logic before native call (isE2ETesting check)
- E2E testing mocks integrated directly in wrapper
- Fall back to mock implementation during E2E tests
- Inline interface definition (NativeFeatureToggleModule)
- Type imports from separate interface files
- Comment explaining inline interface purpose
- Await keyword on native call
- Boolean return type from native module

## Example 5: Testing Native Modules

**File**: `libs/native-modules/navigation/Navigation.spec.ts:1`

This example shows testing pattern for native modules with mocking.

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

**Key patterns demonstrated:**
- Mock react-native module with jest.mock
- Mock NativeModules as empty object
- Mock nativeSharedModuleFetchError function
- Create mock functions (jest.fn())
- mockResolvedValue for async methods
- jest.resetModules() in afterEach
- Assign mock implementation to NativeModules property
- Dynamic import for testing (await import)
- Test both success and error cases
- delete operator to remove native module
- expect().rejects.toThrow() for error assertions

## Example 6: Testing NativeEventEmitter

**File**: `libs/native-modules/events/Events.spec.ts:1`

This example shows testing pattern for NativeEventEmitter with bidirectional events.

```typescript
import { NativeModules, NativeEventEmitter } from 'react-native';

import type { JSToNativeEventName } from './JSToNativeEventName';
import type { NativeToJSEventName } from './NativeToJSEventName';
import type {
  SendGetRepositoryEventBody,
  SendSetRepositoryEventBody,
  SendUpdateEventBody,
} from './types';

jest.mock('react-native', () => {
  return {
    NativeModules: {},
    NativeEventEmitter: jest.fn().mockImplementation(() => ({
      addListener: jest.fn(),
      removeAllListeners: jest.fn(),
    })),
  };
});

jest.mock('@libs/native-modules/commons/NativeModuleErrors', () => ({
  nativeSharedModuleFetchError: jest.fn(() => {
    throw new Error('Mocked native module missing error');
  }),
}));

describe('SharedModulesEventEmitter & sendEvent', () => {
  const mockSendEvent = jest.fn();
  const nativeEventName = 'nativeToJS/test' as NativeToJSEventName;
  const jsEventName = 'jsToNative/test' as JSToNativeEventName;

  jest.unmock('./Events');

  afterEach(() => {
    jest.clearAllMocks();
    jest.resetModules();
  });

  it('should call native sendEvent and call addListener and removeAllListeners via EventEmitter when module is available ', async () => {
    NativeModules.SharedModulesEvents = {
      sendEvent: mockSendEvent,
    };

    const { sendEvent, SharedModulesEventEmitter } = await import('./Events');

    const eventBody: SendUpdateEventBody = { payload: 'test-payload' };

    await sendEvent(jsEventName, eventBody);

    expect(mockSendEvent).toHaveBeenCalledWith(jsEventName, eventBody);

    const listener = jest.fn();
    SharedModulesEventEmitter.addListener(nativeEventName, listener);
    SharedModulesEventEmitter.removeAllListeners(nativeEventName);

    expect(NativeEventEmitter).toHaveBeenCalledWith(
      NativeModules.SharedModulesEvents
    );

    const instance = (NativeEventEmitter as jest.Mock).mock.results[0]!.value;
    expect(instance.addListener).toHaveBeenCalledWith(
      nativeEventName,
      listener
    );
    expect(instance.removeAllListeners).toHaveBeenCalledWith(nativeEventName);
  });

  it('should throw error when native module is unavailable', async () => {
    delete NativeModules.SharedModulesEvents;

    const { sendEvent } = await import('./Events');

    await expect(sendEvent(jsEventName)).rejects.toThrow(
      'Mocked native module missing error'
    );
  });
});
```

**Key patterns demonstrated:**
- Mock NativeEventEmitter with jest.fn().mockImplementation
- Return mock addListener and removeAllListeners
- Test both sendEvent (JS-to-native) and EventEmitter (native-to-JS)
- Type assertions for event names (as JSToNativeEventName)
- Test different event body types
- Access mock results to verify constructor calls
- mock.results[0]!.value to get NativeEventEmitter instance
- Verify NativeEventEmitter was constructed with module
- Test both directions of communication

## Example 7: Error Handling Helper

**File**: `libs/native-modules/commons/NativeModuleErrors.ts:1`

This example shows centralized error handling for missing native modules.

```typescript
export const nativeSharedModuleFetchError = (moduleName: string): Error => {
  return new Error(
    `Tried to call a ${moduleName} Shared Modules native module, but it is not present. \
    This might happen if you're calling the SharedModulesEvents module in a regular React Native app.`
  );
};
```

**Key patterns demonstrated:**
- Centralized error factory function
- Consistent error message format
- Module name parameter for context
- Helpful error message explaining when error occurs
- Export function for reuse across all native modules
- Multi-line string with backslash continuation

## Summary

The YourCompany codebase consistently follows these native development patterns:

1. **NativeModules import** from react-native for accessing native code
2. **Proxy fallback** for graceful error handling when module missing
3. **Wrapper objects** (SharedModules* prefix) for clean API
4. **TypeScript interfaces** for type-safe native module access
5. **NativeEventEmitter** for native-to-JS event communication
6. **nativeSharedModuleFetchError** for consistent error messages
7. **Dynamic imports** in tests with await import()
8. **Mock NativeModules** as empty object in tests
9. **Test both success and error cases** (module present vs missing)
10. **Conditional logic** for E2E testing or special cases
11. **Async/await** for all native bridge calls
12. **JSDoc comments** explaining native integration details

These patterns ensure type-safe, testable, and maintainable native module integration throughout the app with graceful fallbacks when native modules are unavailable.
