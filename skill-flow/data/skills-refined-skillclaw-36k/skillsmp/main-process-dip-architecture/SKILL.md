---
name: main-process-dip-architecture
description: Main Process Architecture Guide. Dependency Injection Pattern (DIP). Provides decorators, module patterns, and examples for building modular, testable Electron main process code using dependency injection
---

# Main Process Architecture Guide: Dependency Injection Pattern (DIP)

## When to use this skill

Use this skill when you want to:

- Create or refactor Electron main process modules using the Dependency Injection pattern
- Design testable services, IPC handlers, and window managers with constructor-injected dependencies
- Share provider interfaces across modules and break circular dependencies using the provider pattern
- Establish consistent module and file structure, DI provider registration, and naming conventions
- Onboard contributors to main-process architecture patterns and coding standards

## Overview

The main process architecture is built on a **Dependency Injection Container** pattern, utilizing TypeScript decorators and metadata reflection. This architecture enables modular, testable, and maintainable Electron main process code.

### Key Technologies

- **TypeScript** with decorators and metadata reflection
- **Dependency Injection Container** for managing service lifecycle
- **Module-based architecture** for separation of concerns
- **IPC Communication** between main and renderer processes
- **Window Management** with lifecycle hooks

### Architecture Goals

1. **Modularity**: Each feature is isolated in its own module
2. **Testability**: Dependencies are injected, making mocking straightforward
3. **Scalability**: Easy to add new modules without affecting existing code
4. **Type Safety**: Full TypeScript support with strong typing
5. **Separation of Concerns**: Clear boundaries between services, IPC, windows, and data

---

## Core Principles

### 1. Dependency Injection (DI)

All dependencies are injected through constructors, never instantiated directly within classes.

**Anti-Pattern (Don't do this):**

```
@Injectable()
export class BadService {
  private authService = new AuthService(); // ❌ Direct instantiation
}
```

**Correct Pattern:**

```
@Injectable()
export class GoodService {
  constructor(private authService: AuthService) {} // ✅ Injected dependency
}
```

### 2. Single Responsibility Principle

Each service, IPC handler, and window manager should have one clear responsibility.

### 3. Provider Pattern for Cross-Module Access

When one module needs functionality from another module, use the **Provider Pattern** to expose only the necessary interface.

### 4. Module Encapsulation

Modules export only what other modules need via the `exports` array in `@RgModule`.

---

## Architecture Layers

1. `app.ts (Bootstrap)` initializes every module through `bootstrapModules` so that the DI container and metadata decorators can hydrate the application graph.
2. `Module Layer (@RgModule)` defines metadata such as `imports`, `providers`, `ipc`, `windows`, and `exports`, giving structure to each feature module.
3. `Service Layer`, `IPC Handlers`, and `Window Managers` represent the main entry points for business logic, renderer communication, and BrowserWindow lifecycle hooks within a module.
4. `Shared Utilities ($shared, config)` provide cross-cutting helpers that can be used by services, IPC handlers, and windows to share configuration, storage, and utility functions.

---

## Module System

### Module Structure

Every feature module follows this structure:

```architecture
module-name/
├── module.ts          # Module definition with @RgModule decorator
├── service.ts         # Business logic (optional, can be multiple services)
├── ipc.ts             # IPC communication handlers (optional)
├── window.ts          # BrowserWindow management (optional)
├── tokens.ts          # Dependency injection tokens (optional)
├── types.ts           # TypeScript type definitions (optional)
└── services/          # Additional services (optional)
    ├── service-a.ts
    └── service-b.ts
```

### Module Definition Template

```
import { RgModule } from "../@core/decorators/rg-module.js";
import { SomeService } from "./service.js";
import { SomeIpc } from "./ipc.js";
import { SomeWindow } from "./window.js";

@RgModule({
  imports: [], // Other modules this module depends on
  providers: [], // Services, factories, and values to register
  ipc: [], // IPC handlers
  windows: [], // Window managers
  exports: [], // Services to expose to other modules
})
export class SomeModule {}
```

### Module Metadata Properties

- **imports** (`Class[]`): Modules to import so their exported providers become available in this module.
- **providers** (`Provider[]`): Services, factories, or values registered in the DI container for this module.
- **ipc** (`Class[]`): IPC handler classes decorated with `@IpcHandler()` to manage renderer/main communication.
- **windows** (`Class[]`): Window manager classes decorated with `@WindowManager()` that control BrowserWindow lifecycles.
- **exports** (`Class[]`): Providers that this module exposes to any module that imports it.

---

## Decorators Reference

### @RgModule

Defines a module and its dependencies.

**Usage:**

```
@RgModule({
  imports: [RestApiModule, CryptoModule],
  providers: [UserService],
  ipc: [UserIpc],
  windows: [],
  exports: [UserService],
})
export class UserModule {}
```

### @Injectable

Marks a class as injectable into the DI container.

**Usage:**

```
@Injectable()
export class UserService {
  constructor(
    @Inject(USER_REST_API_PROVIDER)
    private restApiProvider: TUserRestApiProvider
  ) {}

  async fetchUser(id: string): Promise<TUser | undefined> {
    // Implementation
  }
}
```

### @Inject

Injects a dependency using a token (Symbol).

**Usage:**

```
@Injectable()
export class SomeService {
  constructor(@Inject(SOME_TOKEN) private dependency: TSomeType) {}
}
```

### @IpcHandler

Marks a class as an IPC communication handler.

**Usage:**

```
@IpcHandler()
export class UserIpc implements TIpcHandlerInterface {
  constructor(private userService: UserService) {}

  async onInit({ getWindow }: TParamOnInit<TWindows["main"]>) {
    const mainWindow = getWindow("window:main");

    ipcMainOn("fetchUser", async (event, userId: string) => {
      const user = await this.userService.fetchUser(userId);
      event.reply("fetchUser", user);
    });
  }
}
```

**Lifecycle:**

- `onInit()` is called when the module is bootstrapped

### @WindowManager

Defines a window manager with configuration.

**Usage:**

```
@WindowManager<TWindows["main"]>({
  hash: "window:main",
  isCache: true,
  options: {
    width: 800,
    height: 600,
    show: false,
    resizable: true,
  },
})
export class MainWindow implements TWindowManager {
  constructor(@Inject(SOME_PROVIDER) private someProvider: TSomeProvider) {}

  onWebContentsDidFinishLoad(window: BrowserWindow): void {
    // Called after window content finishes loading
  }
}
```

**Lifecycle Methods:**

- `onWebContentsDidFinishLoad(window)` - Called when web contents finish loading

---

## File Structure Conventions

### 1. **module.ts** - Module Definition

**Purpose:** Declare module metadata and wire dependencies.

**Template:**

```
import { RgModule } from "../@core/decorators/rg-module.js";
import { DependencyModule } from "../dependency/module.js";
import { DependencyService } from "../dependency/service.js";
import { FeatureService } from "./service.js";
import { FeatureIpc } from "./ipc.js";
import { FEATURE_DEPENDENCY_PROVIDER } from "./tokens.js";
import type { TFeatureDependencyProvider } from "./types.js";

@RgModule({
  imports: [DependencyModule],
  ipc: [FeatureIpc],
  providers: [
    FeatureService,
    {
      provide: FEATURE_DEPENDENCY_PROVIDER,
      useFactory: (
        depService: DependencyService
      ): TFeatureDependencyProvider => ({
        someMethod: (args) => depService.someMethod(args),
      }),
      inject: [DependencyService],
    },
  ],
  exports: [FeatureService],
})
export class FeatureModule {}
```

### 2. **service.ts** - Business Logic

**Purpose:** Implement core business logic and data operations.

**Template:**

```
import { Injectable } from "../@core/decorators/injectable.js";
import { Inject } from "../@core/decorators/inject.js";
import { FEATURE_DEPENDENCY_PROVIDER } from "./tokens.js";
import type { TFeatureDependencyProvider } from "./types.js";

@Injectable()
export class FeatureService {
  constructor(
    @Inject(FEATURE_DEPENDENCY_PROVIDER)
    private dependencyProvider: TFeatureDependencyProvider
  ) {}

  async performAction(input: string): Promise<TResult | undefined> {
    const result = await this.dependencyProvider.someMethod(input);

    if (result.error !== undefined) {
      console.error("Error:", result.error);
      return undefined;
    }

    return result.data;
  }
}
```

### 3. **ipc.ts** - IPC Communication

**Purpose:** Handle IPC messages between main and renderer processes.

**Template:**

```
import { ipcMainOn } from "../$shared/utils.js";
import { IpcHandler } from "../@core/decorators/ipc-handler.js";
import type {
  TIpcHandlerInterface,
  TParamOnInit,
} from "../@core/types/ipc-handler.js";
import { FeatureService } from "./service.js";

@IpcHandler()
export class FeatureIpc implements TIpcHandlerInterface {
  constructor(private featureService: FeatureService) {}

  async onInit({ getWindow }: TParamOnInit<TWindows["main"]>) {
    const mainWindow = getWindow("window:main");

    ipcMainOn("featureAction", async (event, payload: TPayload) => {
      const result = await this.featureService.performAction(payload.input);
      event.reply("featureAction", result);
    });
  }
}
```

### 4. **window.ts** - Window Management

**Purpose:** Manage BrowserWindow lifecycle and interactions.

**Template:**

```
import { BrowserWindow } from "electron";
import { WindowManager } from "../@core/decorators/window-manager.js";
import { Inject } from "../@core/decorators/inject.js";
import { isDev } from "../$shared/utils.js";
import type { TWindowManager } from "../types.js";
import { FEATURE_PROVIDER } from "./tokens.js";
import type { TFeatureProvider } from "./types.js";

@WindowManager<TWindows["feature"]>({
  hash: "window:feature",
  isCache: true,
  options: {
    width: 500,
    height: 400,
    show: false,
    resizable: isDev(),
  },
})
export class FeatureWindow implements TWindowManager {
  constructor(@Inject(FEATURE_PROVIDER) private provider: TFeatureProvider) {}

  onWebContentsDidFinishLoad(window: BrowserWindow): void {
    // Initialize window after content loads
    this.provider.initialize(window);
  }
}
```

### 5. **tokens.ts** - DI Tokens

**Purpose:** Define unique symbols for dependency injection.

**Template:**

```
export const FEATURE_PROVIDER = Symbol("FEATURE_PROVIDER");
export const FEATURE_DEPENDENCY_PROVIDER = Symbol(
  "FEATURE_DEPENDENCY_PROVIDER"
);
```

### 6. **types.ts** - Type Definitions

**Purpose:** Define TypeScript types and interfaces.

**Template:**

```
import type { BrowserWindow } from "electron";

export type TFeatureProvider = {
  initialize: (window: BrowserWindow) => void;
  cleanup: () => void;
};

export type TFeatureDependencyProvider = {
  someMethod: (input: string) => Promise<TResult>;
};

export type TResult = {
  data?: any;
  error?: {
    message: string;
    code?: string;
  };
};
```

---

## Code Generation Patterns

### Pattern 1: Simple Module (Service Only)

**Use Case:** Utility services with no IPC or windows.

**Example:** CryptoModule, MenuModule, TrayModule

**Structure:**

```
// module.ts
@RgModule({
  providers: [CryptoService],
  exports: [CryptoService],
})
export class CryptoModule {}

// service.ts
@Injectable()
export class CryptoService {
  async encrypt(key: string, data: string): Promise<string> {
    // Implementation
  }

  async decrypt(key: string, encrypted: string): Promise<string> {
    // Implementation
  }
}
```

### Pattern 2: Module with Dependencies

**Use Case:** Service that depends on other modules.

**Example:** AuthModule, UserModule

**Structure:**

```
// module.ts
@RgModule({
  imports: [RestApiModule],
  providers: [
    AuthService,
    {
      provide: AUTH_REST_API_PROVIDER,
      useFactory: (restApiService: RestApiService): TAuthRestApiProvider => ({
        get: (endpoint, options) => restApiService.get(endpoint, options),
      }),
      inject: [RestApiService],
    },
  ],
  exports: [AuthService],
})
export class AuthModule {}

// tokens.ts
export const AUTH_REST_API_PROVIDER = Symbol("AUTH_REST_API_PROVIDER");

// types.ts
export type TAuthRestApiProvider = {
  get: <T>(endpoint: string, options?: any) => Promise<TApiResponse<T>>;
};

// service.ts
@Injectable()
export class AuthService {
  constructor(
    @Inject(AUTH_REST_API_PROVIDER)
    private restApiProvider: TAuthRestApiProvider
  ) {}

  async login(credentials: TCredentials): Promise<TUser | undefined> {
    const response = await this.restApiProvider.get("/auth/login");
    return response.data;
  }
}
```

### Pattern 3: Module with IPC Communication

**Use Case:** Feature that communicates with renderer process.

**Example:** NotificationModule, UserModule

**Structure:**

```
// module.ts
@RgModule({
  ipc: [NotificationIpc],
  providers: [NotificationService],
  exports: [NotificationService],
})
export class NotificationModule {}

// ipc.ts
@IpcHandler()
export class NotificationIpc implements TIpcHandlerInterface {
  constructor(private notificationService: NotificationService) {}

  async onInit({ getWindow }: TParamOnInit<TWindows["main"]>) {
    ipcMainOn(
      "showNotification",
      async (event, options: TNotificationOptions) => {
        this.notificationService.setNotification(options);
        event.reply("showNotification", { success: true });
      }
    );
  }
}
```

### Pattern 4: Module with Window Management

**Use Case:** Feature that creates and manages BrowserWindows.

**Example:** AppModule, ResourcesModule

**Structure:**

```
// module.ts
@RgModule({
  imports: [MenuModule, TrayModule],
  ipc: [AppIpc],
  windows: [AppWindow],
  providers: [
    AppService,
    {
      provide: MENU_PROVIDER,
      useFactory: (menuService: MenuService): TMenuProvider => ({
        buildMenu: (items) => menuService.buildMenu(items),
      }),
      inject: [MenuService],
    },
  ],
})
export class AppModule {}

// window.ts
@WindowManager<TWindows["main"]>({
  hash: "window:main",
  isCache: true,
  options: {
    width: 800,
    height: 600,
    show: false,
  },
})
export class AppWindow implements TWindowManager {
  constructor(@Inject(MENU_PROVIDER) private menuProvider: TMenuProvider) {}

  onWebContentsDidFinishLoad(window: BrowserWindow): void {
    this.menuProvider.buildMenu();
    window.show();
  }
}

// ipc.ts
@IpcHandler()
export class AppIpc implements TIpcHandlerInterface {
  constructor(private appService: AppService) {}

  async onInit({ getWindow }: TParamOnInit<TWindows["main"]>) {
    const mainWindow = getWindow("window:main");
    const window = await mainWindow.create();

    ipcMainOn("closeApp", () => {
      window?.close();
    });
  }
}
```

### Pattern 5: Complex Module with Sub-Services

**Use Case:** Large modules with multiple services.

**Example:** ResourcesModule, UpdaterModule

**Structure:**

```
resources/
├── module.ts
├── ipc/
│   ├── actions.ts
│   └── open.ts
├── services/
│   ├── resources.ts
│   ├── cacheWindows.ts
│   └── types.ts
├── windows/
│   ├── add.ts
│   ├── update.ts
│   └── delete.ts
├── tokens.ts
└── types.ts
```

```
// module.ts
@RgModule({
  imports: [RestApiModule, CryptoModule, TrayModule],
  ipc: [ResourcesActionsIpc, ResourcesOpenIpc],
  windows: [UpdateWindow, AddWindow, DeleteWindow],
  providers: [
    ResourcesService,
    CacheWindowsService,
    {
      provide: RESOURCES_REST_API_PROVIDER,
      useFactory: (
        restApiService: RestApiService
      ): TResourcesRestApiProvider => ({
        get: (endpoint, options) => restApiService.get(endpoint, options),
        post: (endpoint, data, options) =>
          restApiService.post(endpoint, data, options),
        put: (endpoint, data, options) =>
          restApiService.put(endpoint, data, options),
        delete: (endpoint, options) => restApiService.delete(endpoint, options),
      }),
      inject: [RestApiService],
    },
    {
      provide: RESOURCES_CRYPTO_PROVIDER,
      useFactory: (cryptoService: CryptoService): TResourcesCryptoProvider => ({
        encrypt: (key, value) => cryptoService.encrypt(key, value),
        decrypt: (key, vault) => cryptoService.decrypt(key, vault),
      }),
      inject: [CryptoService],
    },
  ],
  exports: [ResourcesService],
})
export class ResourcesModule {}

// services/resources.ts
@Injectable()
export class ResourcesService {
  constructor(
    @Inject(RESOURCES_REST_API_PROVIDER)
    private restApiProvider: TResourcesRestApiProvider
  ) {}

  async byId(id: string): Promise<TResource | undefined> {
    const response = await this.restApiProvider.get(`/resources/${id}`);
    return response.data;
  }

  async create(data: TResourceData): Promise<TResource | undefined> {
    const response = await this.restApiProvider.post("/resources", data);
    return response.data;
  }
}
```

---

## Provider Pattern

### Why Use Providers?

Providers create abstraction layers between modules, exposing only necessary functionality while hiding implementation details.

### Provider Definition Pattern

**1. Create Token:**

```
// tokens.ts
export const SERVICE_PROVIDER = Symbol("SERVICE_PROVIDER");
```

**2. Define Provider Type:**

```
// types.ts
export type TServiceProvider = {
  methodA: (arg: string) => Promise<TResult>;
  methodB: () => void;
};
```

**3. Register in Module:**

```
// module.ts
@RgModule({
  imports: [DependencyModule],
  providers: [
    {
      provide: SERVICE_PROVIDER,
      useFactory: (depService: DependencyService): TServiceProvider => ({
        methodA: (arg) => depService.methodA(arg),
        methodB: () => depService.methodB(),
      }),
      inject: [DependencyService],
    },
  ],
})
export class FeatureModule {}
```

**4. Inject in Consumer:**

```
// service.ts
@Injectable()
export class ConsumerService {
  constructor(@Inject(SERVICE_PROVIDER) private provider: TServiceProvider) {}

  async useProvider(): Promise<void> {
    await this.provider.methodA("input");
    this.provider.methodB();
  }
}
```

### Provider Types

#### 1. Class Provider (Default)

```
providers: [MyService];
// Equivalent to:
providers: [
  {
    provide: MyService,
    useClass: MyService,
  },
];
```

#### 2. Factory Provider

```
providers: [
  {
    provide: MY_TOKEN,
    useFactory: (dep: Dependency): TMyType => ({
      method: () => dep.doSomething(),
    }),
    inject: [Dependency],
  },
];
```

#### 3. Value Provider

```
providers: [
  {
    provide: CONFIG_TOKEN,
    useValue: {
      apiUrl: "https://api.example.com",
      timeout: 5000,
    },
  },
];
```

---

## Complete Examples

### Example 1: Create a New "Settings" Module

**Goal:** Create a module that manages application settings with IPC communication.

**Step 1: Create Directory Structure**

```
src/main/settings/
├── module.ts
├── service.ts
├── ipc.ts
├── tokens.ts
└── types.ts
```

**Step 2: Define Types**

```
// types.ts
export type TSettings = {
  theme: "light" | "dark";
  language: string;
  autoUpdate: boolean;
};

export type TUpdateSettingsPayload = Partial<TSettings>;
```

**Step 3: Create Service**

```
// service.ts
import { Injectable } from "../@core/decorators/injectable.js";
import { getElectronStorage, setElectronStorage } from "../$shared/store.js";

@Injectable()
export class SettingsService {
  constructor() {}

  getSettings(): TSettings {
    const settings = getElectronStorage("settings");

    return (
      settings ?? {
        theme: "light",
        language: "en",
        autoUpdate: true,
      }
    );
  }

  updateSettings(updates: TUpdateSettingsPayload): TSettings {
    const currentSettings = this.getSettings();
    const newSettings = { ...currentSettings, ...updates };

    setElectronStorage("settings", newSettings);

    return newSettings;
  }
}
```

**Step 4: Create IPC Handler**

```
// ipc.ts
import { ipcMainOn } from "../$shared/utils.js";
import { IpcHandler } from "../@core/decorators/ipc-handler.js";
import type {
  TIpcHandlerInterface,
  TParamOnInit,
} from "../@core/types/ipc-handler.js";
import { SettingsService } from "./service.js";
import type { TUpdateSettingsPayload } from "./types.js";

@IpcHandler()
export class SettingsIpc implements TIpcHandlerInterface {
  constructor(private settingsService: SettingsService) {}

  async onInit({ getWindow }: TParamOnInit<TWindows["main"]>) {
    ipcMainOn("getSettings", (event) => {
      const settings = this.settingsService.getSettings();
      event.reply("getSettings", settings);
    });

    ipcMainOn("updateSettings", (event, payload: TUpdateSettingsPayload) => {
      const settings = this.settingsService.updateSettings(payload);
      event.reply("updateSettings", settings);
    });
  }
}
```

**Step 5: Create Module**

```
// module.ts
import { RgModule } from "../@core/decorators/rg-module.js";
import { SettingsService } from "./service.js";
import { SettingsIpc } from "./ipc.js";

@RgModule({
  ipc: [SettingsIpc],
  providers: [SettingsService],
  exports: [SettingsService],
})
export class SettingsModule {}
```

**Step 6: Register in app.ts**

```
// app.ts
import { SettingsModule } from "./settings/module.js";

app.on("ready", async () => {
  await bootstrapModules([
    AppPreloadModule,
    AppModule,
    SettingsModule, // Add here
    // ... other modules
  ]);
});
```

### Example 2: Module with External API Integration

**Goal:** Create a Weather module that fetches weather data from an external API.

**Step 1: Create Structure**

```
src/main/weather/
├── module.ts
├── service.ts
├── ipc.ts
├── tokens.ts
└── types.ts
```

**Step 2: Define Types**

```
// types.ts
export type TWeatherData = {
  temperature: number;
  condition: string;
  humidity: number;
  location: string;
};

export type TWeatherRestApiProvider = {
  get: <T>(endpoint: string, options?: any) => Promise<TApiResponse<T>>;
};

type TApiResponse<T> = {
  data?: T;
  error?: {
    message: string;
    code?: string;
  };
  status: number;
};
```

**Step 3: Create Tokens**

```
// tokens.ts
export const WEATHER_REST_API_PROVIDER = Symbol("WEATHER_REST_API_PROVIDER");
```

**Step 4: Create Service**

```
// service.ts
import { Injectable } from "../@core/decorators/injectable.js";
import { Inject } from "../@core/decorators/inject.js";
import { WEATHER_REST_API_PROVIDER } from "./tokens.js";
import type { TWeatherRestApiProvider, TWeatherData } from "./types.js";

@Injectable()
export class WeatherService {
  constructor(
    @Inject(WEATHER_REST_API_PROVIDER)
    private restApiProvider: TWeatherRestApiProvider
  ) {}

  async getWeather(city: string): Promise<TWeatherData | undefined> {
    const response = await this.restApiProvider.get<TWeatherData>(
      `https://api.weather.com/v1/weather?city=${city}`,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (response.error !== undefined) {
      console.error("Weather API Error:", response.error);
      return undefined;
    }

    return response.data;
  }
}
```

**Step 5: Create IPC Handler**

```
// ipc.ts
import { ipcMainOn } from "../$shared/utils.js";
import { IpcHandler } from "../@core/decorators/ipc-handler.js";
import type {
  TIpcHandlerInterface,
  TParamOnInit,
} from "../@core/types/ipc-handler.js";
import { WeatherService } from "./service.js";

@IpcHandler()
export class WeatherIpc implements TIpcHandlerInterface {
  constructor(private weatherService: WeatherService) {}

  async onInit({ getWindow }: TParamOnInit<TWindows["main"]>) {
    ipcMainOn("getWeather", async (event, city: string) => {
      const weather = await this.weatherService.getWeather(city);
      event.reply("getWeather", weather);
    });
  }
}
```

**Step 6: Create Module with Provider**

```
// module.ts
import { RgModule } from "../@core/decorators/rg-module.js";
import { RestApiModule } from "../rest-api/module.js";
import { RestApiService } from "../rest-api/service.js";
import { WeatherService } from "./service.js";
import { WeatherIpc } from "./ipc.js";
import { WEATHER_REST_API_PROVIDER } from "./tokens.js";
import type { TWeatherRestApiProvider } from "./types.js";

@RgModule({
  imports: [RestApiModule],
  ipc: [WeatherIpc],
  providers: [
    WeatherService,
    {
      provide: WEATHER_REST_API_PROVIDER,
      useFactory: (
        restApiService: RestApiService
      ): TWeatherRestApiProvider => ({
        get: (endpoint, options) => restApiService.get(endpoint, options),
      }),
      inject: [RestApiService],
    },
  ],
  exports: [WeatherService],
})
export class WeatherModule {}
```

### Example 3: Module with Window Management

**Goal:** Create a Preferences window module.

**Step 1: Create Structure**

```
src/main/preferences/
├── module.ts
├── service.ts
├── ipc.ts
├── window.ts
├── tokens.ts
└── types.ts
```

**Step 2: Update Window Types**

```
// src/main/config.ts (add to windows object)
export const windows: TWindows = {
  // ... existing windows
  preferences: "window:preferences",
};
```

**Step 3: Define Types**

```
// types.ts
import type { BrowserWindow } from "electron";

export type TPreferencesProvider = {
  openPreferences: () => void;
  closePreferences: () => void;
};
```

**Step 4: Create Tokens**

```
// tokens.ts
export const PREFERENCES_PROVIDER = Symbol("PREFERENCES_PROVIDER");
```

**Step 5: Create Service**

```
// service.ts
import { Injectable } from "../@core/decorators/injectable.js";
import { getWindow } from "../@core/control-window/receive.js";

@Injectable()
export class PreferencesService {
  constructor() {}

  async openPreferences(): Promise<void> {
    const preferencesWindow =
      getWindow<TWindows["preferences"]>("window:preferences");

    if (preferencesWindow !== undefined) {
      const window = await preferencesWindow.create();
      window?.show();
    }
  }

  closePreferences(): void {
    const preferencesWindow =
      getWindow<TWindows["preferences"]>("window:preferences");

    if (preferencesWindow !== undefined) {
      preferencesWindow.hide();
    }
  }
}
```

**Step 6: Create Window Manager**

```
// window.ts
import { BrowserWindow } from "electron";
import { WindowManager } from "../@core/decorators/window-manager.js";
import { isDev } from "../$shared/utils.js";
import type { TWindowManager } from "../types.js";

@WindowManager<TWindows["preferences"]>({
  hash: "window:preferences",
  isCache: true,
  options: {
    width: 600,
    height: 500,
    show: false,
    resizable: isDev(),
    title: "Preferences",
  },
})
export class PreferencesWindow implements TWindowManager {
  constructor() {}

  onWebContentsDidFinishLoad(window: BrowserWindow): void {
    // Initialize preferences window
    console.log("Preferences window loaded");
  }
}
```

**Step 7: Create IPC Handler**

```
// ipc.ts
import { ipcMainOn } from "../$shared/utils.js";
import { IpcHandler } from "../@core/decorators/ipc-handler.js";
import type {
  TIpcHandlerInterface,
  TParamOnInit,
} from "../@core/types/ipc-handler.js";
import { PreferencesService } from "./service.js";

@IpcHandler()
export class PreferencesIpc implements TIpcHandlerInterface {
  constructor(private preferencesService: PreferencesService) {}

  async onInit({ getWindow }: TParamOnInit<TWindows["main"]>) {
    ipcMainOn("openPreferences", async () => {
      await this.preferencesService.openPreferences();
    });

    ipcMainOn("closePreferences", () => {
      this.preferencesService.closePreferences();
    });
  }
}
```

**Step 8: Create Module**

```
// module.ts
import { RgModule } from "../@core/decorators/rg-module.js";
import { PreferencesService } from "./service.js";
import { PreferencesIpc } from "./ipc.js";
import { PreferencesWindow } from "./window.js";

@RgModule({
  ipc: [PreferencesIpc],
  windows: [PreferencesWindow],
  providers: [PreferencesService],
  exports: [PreferencesService],
})
export class PreferencesModule {}
```

---

## Best Practices

### 1. Module Organization

✅ **Do:**

- Keep modules focused on a single feature or domain
- Use sub-services for complex modules
- Export only what other modules need
- Import only required modules

❌ **Don't:**

- Create circular dependencies between modules
- Export everything from a module
- Mix unrelated functionality in one module

### 2. Service Design

✅ **Do:**

- Inject all dependencies via constructor
- Use `@Injectable()` decorator on all services
- Keep services stateless when possible
- Return `undefined` on errors with logging
- Use TypeScript types for all parameters and return values

❌ **Don't:**

- Instantiate services directly (`new MyService()`)
- Store mutable state in services without careful consideration
- Throw errors without handling them
- Use `any` type

### 3. Provider Pattern

✅ **Do:**

- Create provider interfaces that expose minimal API surface
- Use descriptive names for provider tokens
- Document provider type interfaces
- Use factory providers for cross-module dependencies

❌ **Don't:**

- Expose entire services across module boundaries
- Create providers without type definitions
- Use string tokens (use Symbols instead)

### 4. IPC Communication

✅ **Do:**

- Define clear IPC channel names
- Type all IPC payloads
- Handle errors gracefully
- Use `ipcMainOn` helper for type safety
- Reply to all IPC calls

❌ **Don't:**

- Use generic channel names like "data" or "message"
- Send untyped data over IPC
- Forget to handle errors
- Create memory leaks by not removing listeners

### 5. Window Management

✅ **Do:**

- Use descriptive window hash names
- Set appropriate default window options
- Implement `onWebContentsDidFinishLoad` for initialization
- Use `isCache: true` for singleton windows
- Hide windows instead of destroying when reusable

❌ **Don't:**

- Create multiple instances of singleton windows
- Show windows before content is loaded
- Hardcode window dimensions (use config)
- Forget to clean up window resources

### 6. Error Handling

✅ **Do:**

- Return `undefined` on errors
- Log errors with context
- Use `dialog.showMessageBox` for critical errors
- Validate input before processing
- Handle async errors with try-catch

❌ **Don't:**

- Silently swallow errors
- Use error codes without messages
- Crash the app on recoverable errors

### 7. Type Safety

✅ **Do:**

- Define all types in `types.ts`
- Use strict TypeScript compiler options
- Type all function parameters and returns
- Use discriminated unions for state
- Export types for cross-module usage

❌ **Don't:**

- Use `any` type
- Skip type definitions
- Use implicit types
- Create type inconsistencies

### 8. Naming Conventions

✅ **Do:**

- Use `PascalCase` for class names
- Use `camelCase` for method and variable names
- Use `UPPER_SNAKE_CASE` for constants and tokens
- Prefix types with `T` (e.g., `TUser`, `TSettings`)
- Suffix modules with `Module`
- Suffix services with `Service`
- Suffix IPC handlers with `Ipc`
- Suffix windows with `Window`

❌ **Don't:**

- Mix naming conventions
- Use abbreviations without context
- Create ambiguous names

### 9. File Organization

✅ **Do:**

- Keep related files together in module folders
- Use `services/` subfolder for multiple services
- Use `ipc/` subfolder for multiple IPC handlers
- Use `windows/` subfolder for multiple windows
- Use index files sparingly

❌ **Don't:**

- Create deeply nested folder structures
- Mix module files with core framework files
- Create circular file dependencies

### 10. Dependency Management

✅ **Do:**

- Declare all module dependencies in `imports`
- Use provider pattern for cross-module access
- Register services in the correct module
- Export services that other modules need

❌ **Don't:**

- Access services from unimported modules
- Create tight coupling between modules
- Import modules unnecessarily

---

## Common Patterns Summary

### 1. **Simple Utility Module** (e.g., CryptoModule)

```
@RgModule({
  providers: [UtilityService],
  exports: [UtilityService],
})
export class UtilityModule {}
```

### 2. **Module with External Dependency** (e.g., AuthModule)

```
@RgModule({
  imports: [DependencyModule],
  providers: [
    FeatureService,
    {
      provide: FEATURE_PROVIDER,
      useFactory: (dep: DependencyService) => ({
        method: () => dep.method(),
      }),
      inject: [DependencyService],
    },
  ],
  exports: [FeatureService],
})
export class FeatureModule {}
```

### 3. **Module with IPC** (e.g., NotificationModule)

```
@RgModule({
  ipc: [FeatureIpc],
  providers: [FeatureService],
  exports: [FeatureService],
})
export class FeatureModule {}
```

### 4. **Module with Window** (e.g., AppModule)

```
@RgModule({
  imports: [DependencyModule],
  ipc: [FeatureIpc],
  windows: [FeatureWindow],
  providers: [FeatureService],
})
export class FeatureModule {}
```

### 5. **Complex Module** (e.g., ResourcesModule, UpdaterModule)

```
@RgModule({
  imports: [Dep1Module, Dep2Module, Dep3Module],
  ipc: [Feature1Ipc, Feature2Ipc],
  windows: [Window1, Window2],
  providers: [
    Service1,
    Service2,
    Service3,
    { provide: PROVIDER_1, useFactory: ..., inject: [...] },
    { provide: PROVIDER_2, useFactory: ..., inject: [...] },
  ],
  exports: [Service1],
})
export class ComplexModule {}
```

---

## Troubleshooting

### Issue: "Cannot inject undefined"

**Cause:** Service is not registered in module providers or dependency module is not imported.

**Solution:**

1. Ensure service is in `providers` array
2. Check that dependency module is in `imports` array
3. Verify exported services in dependency modules

### Issue: "Circular dependency detected"

**Cause:** Two modules import each other.

**Solution:**

1. Refactor shared functionality into a third module
2. Use provider pattern to break circular dependency
3. Reconsider module boundaries

### Issue: "Window is undefined"

**Cause:** Window not registered in module or hash mismatch.

**Solution:**

1. Add window class to `windows` array in `@RgModule`
2. Verify `hash` in `@WindowManager` matches usage
3. Check window is registered in config.ts

### Issue: "IPC handler not called"

**Cause:** IPC handler not registered or channel name mismatch.

**Solution:**

1. Add IPC handler to `ipc` array in `@RgModule`
2. Verify channel names match between main and renderer
3. Ensure `onInit` is implemented

---

## Conclusion

This architecture provides a robust, scalable foundation for Electron main process development using Dependency Injection and modular design. By following these patterns and best practices, you can create maintainable, testable, and well-organized code.

**Key Takeaways:**

1. **Use decorators** (`@RgModule`, `@Injectable`, `@IpcHandler`, `@WindowManager`) for metadata-driven architecture
2. **Inject dependencies** via constructors, never instantiate directly
3. **Use providers** to expose functionality across module boundaries
4. **Follow file conventions** for consistent codebase structure
5. **Type everything** for maximum type safety
6. **Keep modules focused** on single responsibilities
7. **Handle errors gracefully** with appropriate user feedback

When generating new code, always follow these patterns to maintain architectural consistency.
