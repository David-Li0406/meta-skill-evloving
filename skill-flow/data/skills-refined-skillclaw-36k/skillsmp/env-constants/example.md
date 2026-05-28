# Example of EnvConsts.ts file

```typescript
// Environment variable exports with type safety and defaults
export const appVersion = import.meta.env.VITE_APP_VERSION ?? '0.0.0';
export const accessManagementBaseUrl = import.meta.env.VITE_ACCESS_MANAGEMENT_BASE_URL ?? '';
```

*** Important Notes ***
- The above is an example of the structure of EnvConsts.ts that is desired. 
- The scripts and configurations may be outdated.
- When reviewing the above example, make sure to scripts and configuration to apply the latest best pratice.