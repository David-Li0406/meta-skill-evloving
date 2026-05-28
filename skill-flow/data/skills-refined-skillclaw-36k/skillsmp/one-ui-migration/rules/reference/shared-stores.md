# Shared Stores

This document describes shared stores that are commonly used across multiple pages.

## PortDataStore

Manages port data (allPortMap, normalPortMap) for the entire application.

**Location:** `libs/mxsecurity/shared/domain/src/lib/store/port-data/port-data.store.ts`

**Legacy Equivalent:** `apps/mxsecurity-web/src/app/shared/Service/utils.service.ts`

### Import

```typescript
import { PortDataStore, type PortMapType } from '@one-ui/mxsecurity/shared/domain';
```

### PortMapType Interface

```typescript
export interface PortMapType {
  name: string; // Port display name (e.g., "Port 1")
  index: number; // Port index (0-based)
  laMember: boolean; // Whether this port is a Link Aggregation member
  exist: boolean; // Whether this port exists
  bandwidth: number; // Port bandwidth
  laGroup: number; // LA group number (0 = disabled, 1-4 = group index)
  descName: string; // Port description name
}
```

### Method Mapping (Legacy → New)

| Legacy (UtilsService)                 | New (PortDataStore)                    |
| ------------------------------------- | -------------------------------------- |
| `allPortMap` property                 | `allPortMap()` signal                  |
| `normalPortMap` property              | `normalPortMap()` signal               |
| `portNumber` getter                   | `portCount()` computed                 |
| `getPortNameByIndex(index: number)`   | `getPortNameByIndex(index)`            |
| `getPortNameByIndex(index: number[])` | `getPortNamesByIndices(indices)`       |
| `updateLocalStoragePortData()`        | `loadPortData()` / `refreshPortData()` |

### Usage in Components

```typescript
@Component({...})
export class MyPageComponent {
  readonly #portDataStore = inject(PortDataStore);

  // Read port data (reactive)
  readonly allPorts = this.#portDataStore.allPortMap;
  readonly normalPorts = this.#portDataStore.normalPortMap;
  readonly portCount = this.#portDataStore.portCount;

  // Get port name by index
  getPortName(index: number): string {
    return this.#portDataStore.getPortNameByIndex(index);
  }

  // Get multiple port names
  getPortNames(indices: number[]): string {
    return this.#portDataStore.getPortNamesByIndices(indices);
  }

  // Filter ports (example: exclude LA members)
  readonly availablePorts = computed(() =>
    this.#portDataStore.normalPortMap().filter(port => !port.laMember)
  );
}
```

### When Port Data is Loaded

Port data is automatically loaded in two scenarios:

1. **App Initialization (Login):** `login-page.store.ts` calls `loadPortData()` after login
2. **Auto-login (Page Refresh):** `app-init.config.ts` calls `loadPortData()` if already logged in

### When to Refresh Port Data

Call `refreshPortData()` after operations that may change port configuration:

```typescript
// Example: After config restore
this.#portDataStore.refreshPortData();
```

**Known scenarios requiring refresh:**

- After config restore (`config-bk-res-page`)
- After LA (Link Aggregation) settings change
- After port settings change

### Legacy Code Pattern vs New Pattern

**Legacy (reading from sessionStorage):**

```typescript
// Old way - reading from sessionStorage
const normalPortMap: PortMapType[] = JSON.parse(sessionStorage.getItem('normalPortMap'));
const allPort = filter(normalPortMap, (port) => !port.laMember);
```

**New (using PortDataStore):**

```typescript
// New way - using PortDataStore signal
readonly #portDataStore = inject(PortDataStore);

readonly availablePorts = computed(() =>
  this.#portDataStore.normalPortMap().filter(port => !port.laMember)
);
```

### API Service

The underlying API service is `PortDataApiService`:

**Location:** `libs/mxsecurity/shared/domain/src/lib/api/port-data.api.ts`

It fetches data from 4 APIs:

- `SRV_PORT_LINK_STATUS` - port link status
- `SRV_TRUNK_SETTING` - trunk/LA settings (if supported)
- `portBandwidth` - port bandwidth data
- `portDesc` - port descriptions

## AuthStore

Manages authentication state and service permissions for the entire application.

**Location:** `libs/mxsecurity/shared/domain/src/lib/store/auth/auth.store.ts`

**Legacy Equivalent:** `apps/mxsecurity-web/src/app/shared/Service/auth.service.ts` (the `auth` object)

### Import

```typescript
import { AuthStore } from '@one-ui/mxsecurity/shared/domain';
```

### serviceDefine

The `serviceDefine` property contains boolean flags indicating which services/features are available on the current device. This is critical for:

1. **Conditional API calls** - Only fetch data for services that exist on the device
2. **Tab/Section visibility** - Show/hide UI elements based on device capabilities
3. **Feature gating** - Enable/disable functionality based on device support

### Method Mapping (Legacy → New)

| Legacy (auth service)                          | New (AuthStore)                                      |
| ---------------------------------------------- | ---------------------------------------------------- |
| `auth.serviceDefine`                           | `AuthStore.serviceDefine()`                          |
| `auth.serviceDefine.SRV_PORT_EVENT`            | `AuthStore.serviceDefine()?.SRV_PORT_EVENT`          |
| `auth.serviceDefine.SRV_CPU_USAGE_ALARM`       | `AuthStore.serviceDefine()?.SRV_CPU_USAGE_ALARM`     |
| `auth.serviceDefine.SRV_PORT_USAGE_ALARM`      | `AuthStore.serviceDefine()?.SRV_PORT_USAGE_ALARM`    |
| `auth.serviceDefine.SRV_PORT_RXDISCARD_ALARM`  | `AuthStore.serviceDefine()?.SRV_PORT_RXDISCARD_ALARM`|
| `auth.serviceDefine.SRV_LICENSE_NOTIFICATION`  | `AuthStore.serviceDefine()?.SRV_LICENSE_NOTIFICATION`|
| `auth.serviceDefine.SRV_TRUNK_SETTING`         | `AuthStore.serviceDefine()?.SRV_TRUNK_SETTING`       |
| `auth.serviceDefine.SRV_IGMP_SNOOP`            | `AuthStore.serviceDefine()?.SRV_IGMP_SNOOP`          |
| `auth.serviceDefine.SRV_POWER_MANAGEMENT`      | `AuthStore.serviceDefine()?.SRV_POWER_MANAGEMENT`    |

### Usage in Store

```typescript
import { AuthStore } from '@one-ui/mxsecurity/shared/domain';

export const MyPageStore = signalStore(
  withMethods((store, authStore = inject(AuthStore)) => {
    // Get permissions for conditional API calls
    const getPermissions = () => {
      const serviceDefine = authStore.serviceDefine();
      return {
        SRV_PORT_EVENT: serviceDefine?.SRV_PORT_EVENT ?? false,
        SRV_CPU_USAGE_ALARM: serviceDefine?.SRV_CPU_USAGE_ALARM ?? false,
      };
    };

    return {
      // Permission getters for tab visibility
      hasPortEventPermission: () => authStore.serviceDefine()?.SRV_PORT_EVENT ?? false,
      hasCpuUsageAlarmPermission: () => authStore.serviceDefine()?.SRV_CPU_USAGE_ALARM ?? false,

      loadPageData: queryMethod({
        observe: () => api.loadPageData$(getPermissions()),
        // ...
      }),
    };
  })
);
```

### Usage in Components

```typescript
@Component({...})
export class MyPageComponent {
  readonly #store = inject(MyPageStore);

  // Expose permission checks to template
  readonly hasPortEventPermission = this.#store.hasPortEventPermission;
  readonly hasCpuUsageAlarmPermission = this.#store.hasCpuUsageAlarmPermission;
}
```

### Usage in Templates (Tab Visibility)

```html
<mat-tab-group>
  <!-- Always visible tab -->
  <mat-tab [label]="t('general.common.system')">...</mat-tab>

  <!-- Permission-based tabs -->
  @if (hasPortEventPermission()) {
    <mat-tab [label]="t('general.common_port.port')">...</mat-tab>
  }
  @if (hasCpuUsageAlarmPermission()) {
    <mat-tab [label]="t('features.event_notification.cpu_usage')">...</mat-tab>
  }
</mat-tab-group>
```

### Legacy Code Pattern vs New Pattern

**Legacy (checking auth.serviceDefine directly):**

```typescript
// Old way - in Angular controller/component
if (this.auth.serviceDefine.SRV_PORT_EVENT) {
  this.loadPortEventData();
}

// Old way - in template
<div *ngIf="auth.serviceDefine.SRV_CPU_USAGE_ALARM">...</div>
```

**New (using AuthStore in store + exposing to component):**

```typescript
// New way - in store
hasPortEventPermission: () => authStore.serviceDefine()?.SRV_PORT_EVENT ?? false,

// New way - in component
readonly hasPortEventPermission = this.#store.hasPortEventPermission;

// New way - in template
@if (hasPortEventPermission()) { ... }
```

### Common serviceDefine Flags

| Flag                          | Description                              |
| ----------------------------- | ---------------------------------------- |
| `SRV_PORT_EVENT`              | Port event notifications                 |
| `SRV_CPU_USAGE_ALARM`         | CPU usage alarm feature                  |
| `SRV_PORT_USAGE_ALARM`        | Port usage alarm feature                 |
| `SRV_PORT_RXDISCARD_ALARM`    | Port RX discard alarm feature            |
| `SRV_LICENSE_NOTIFICATION`    | License notification feature             |
| `SRV_TRUNK_SETTING`           | Link Aggregation (trunk) settings        |
| `SRV_IGMP_SNOOP`              | IGMP snooping feature                    |
| `SRV_POWER_MANAGEMENT`        | Power management (PoE) feature           |
| `SRV_CELLULAR`                | Cellular modem feature                   |
| `SRV_VPN`                     | VPN feature                              |
| `SRV_FIREWALL`                | Firewall feature                         |

### Important Notes

1. **Always use optional chaining** - `serviceDefine()` may be `null` before auth is loaded
2. **Default to `false`** - If permission is undefined, treat as not available
3. **Permission vs Data** - Use permissions for tab visibility, not data availability
4. **Conditional API calls** - Skip API calls for services not available on device (prevents 404 errors)
