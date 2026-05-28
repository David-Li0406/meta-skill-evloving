# Development Policy

## TypeScript Coding Guidelines

### File and Folder Naming
- Use kebab-case for all file names and folder names.
  - ✅ Good: `user-handler.ts`, `api-client-utils/`, `data-processors/`
  - ❌ Bad: `userHandler.ts`, `ApiClient.ts`, `DataProcessors/`, `apiClientUtils/`

### Functions
- Prefer arrow functions (`const fn = () => {}`) over function declarations.
  - ✅ Good:
    ```typescript
    const handleUserRequest = (id: string) => {
      // implementation
    };
    ```
  - ❌ Bad:
    ```typescript
    function handleUserRequest(id: string) {
      // implementation
    }
    ```