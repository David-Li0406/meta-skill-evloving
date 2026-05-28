# Security Best Practices

## Secure Storage

Use `expo-secure-store` for tokens—**never** AsyncStorage:

```tsx
import * as SecureStore from 'expo-secure-store';

// Store sensitive data
await SecureStore.setItemAsync('authToken', token);

// Retrieve
const token = await SecureStore.getItemAsync('authToken');

// Delete
await SecureStore.deleteItemAsync('authToken');

// With biometric authentication
await SecureStore.setItemAsync('sensitiveKey', value, {
  requireAuthentication: true,
});
```

## Best Practices
- **Never** store tokens in AsyncStorage—use `expo-secure-store`
- Use HTTPS for all API communication
- Implement token refresh logic
- Clear sensitive data on logout
- Use `requireAuthentication` for highly sensitive data
- Set appropriate keychain accessibility levels
