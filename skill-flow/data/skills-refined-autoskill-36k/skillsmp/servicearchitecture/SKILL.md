---
name: ServiceArchitecture
description: Guidelines for extending the application using the decoupled service layer architecture (IDataProvider, adapters, and hooks).
---

# Service Architecture Skill

This skill defines the mandatory patterns for any frontend interaction with infrastructure or backend services (IPC, database, external APIs). The application uses a decoupled service layer to maintain platform independence and clean separation of concerns.

## Core Components

1.  **`src/core/services/IDataProvider.ts`**: The interface that defines the contract for all data operations. It is platform-agnostic.
2.  **`src/core/adapters/`**: Platform-specific implementations of `IDataProvider`. 
    - `ElectronAdapter.ts`: Bridges the frontend to Electron IPC.
3.  **`src/core/context/DataContext.tsx`**: Provides the chosen implementation via React Context.
4.  **`src/core/hooks/useDataService.ts`**: The primary way for React components to consume services.
5.  **`src/core/types/service-types.ts`**: Common types used across the service boundary.

## Extension Workflow

When adding a new feature that requires backend communication:

### 1. Update Types
Add any necessary request/response types to `src/core/types/service-types.ts`. Avoid using broad types like `any`.

### 2. Update Interface
Add the new method signature to `IDataProvider.ts`. Keep methods focused and descriptive.
```typescript
// Example
getUserProfile(id: string): Promise<UserProfile>;
```

### 3. Implement in Adapter
Update `src/core/adapters/ElectronAdapter.ts` to implement the new method. This is where you use `window.electron.invoke` or other IPC methods.
```typescript
// Example
async getUserProfile(id: string): Promise<UserProfile> {
    return window.electron.invoke('get-user-profile', id);
}
```

### 4. Consume in Component
Use the `useDataService` hook to access the method.
```typescript
const dataService = useDataService();
const profile = await dataService.getUserProfile(id);
```

## Mandatory Rules

- **NEVER** use `window.electron` directly in React components (except for the entry point or specialized system hooks).
- **NEVER** listen to IPC events directly in components using `window.electron.on`. Use the `onStreamEvent` or `onUpdateEvent` patterns in `IDataProvider`.
- **ALWAYS** update the interface first. This ensures that any future platform adapter (e.g., a CloudAdapter) will have a clear implementation guide.
- **TYPE SAFETY**: Ensure that types in `IDataProvider` match exactly what the backend returns.

## Reference Files
- [IDataProvider.ts](../../../src/core/services/IDataProvider.ts)
- [ElectronAdapter.ts](../../../src/core/adapters/ElectronAdapter.ts)
- [useDataService.ts](../../../src/core/hooks/useDataService.ts)
