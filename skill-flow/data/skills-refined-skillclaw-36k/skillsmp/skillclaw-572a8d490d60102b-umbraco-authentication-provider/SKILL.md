---
name: umbraco-authentication-provider
description: Use this skill when implementing authentication and multi-factor authentication providers for the Umbraco backoffice.
---

# Umbraco Authentication Provider

## What is it?
An Authentication Provider enables both external login (OAuth/SSO) and multi-factor authentication (MFA) for the Umbraco backoffice. It provides the UI components for users to configure their authentication methods, including options like Google Authenticator, SMS codes, and various OAuth providers (e.g., Google, Microsoft, GitHub).

## Documentation
Always fetch the latest docs before implementing:

- **External Login Providers**: https://docs.umbraco.com/umbraco-cms/reference/security/external-login-providers
- **Two-Factor Authentication**: https://docs.umbraco.com/umbraco-cms/reference/security/two-factor-authentication
- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What authentication method is needed? Which OAuth provider? Is a custom UI required?
3. **Configure backend** - Set up the C# authentication provider or ITwoFactorProvider first.
4. **Generate frontend files** - Create manifest + configuration elements for both authentication and MFA.
5. **Explain** - Show what was created and how to test.

## Minimal Examples

### Manifest for MFA Provider (umbraco-package.json)
```json
{
  "name": "My MFA Provider",
  "extensions": [
    {
      "type": "mfaLoginProvider",
      "alias": "My.MfaProvider.Authenticator",
      "name": "Authenticator App MFA",
      "forProviderName": "Umbraco.GoogleAuthenticator",
      "element": "/App_Plugins/MyMfa/mfa-setup.js",
      "meta": {
        "label": "Authenticator App"
      }
    }
  ]
}
```

### Manifest for Auth Provider (umbraco-package.json)
```json
{
  "name": "My Auth Provider",
  "extensions": [
    {
      "type": "authProvider",
      "alias": "My.AuthProvider.Google",
      "name": "Google Login",
      "forProviderName": "Umbraco.Google",
      "meta": {
        "label": "Sign in with Google",
        "defaultView": {
          "icon": "icon-google",
          "color": "default",
          "look": "outline"
        }
      }
    }
  ]
}
```

### Example Manifest (TypeScript)
```typescript
import type { ManifestAuthProvider, ManifestMfaLoginProvider } from '@umbraco-cms/backoffice/extension-registry';

const authManifest: ManifestAuthProvider = {
  type: 'authProvider',
  alias: 'My.AuthProvider.Google',
  name: 'Google Login',
  forProviderName: 'Umbraco.Google',
  meta: {
    label: 'Sign in with Google',
    defaultView: {
      icon: 'icon-google',
      color: 'default',
      look: 'outline',
    },
  },
};

const mfaManifest: ManifestMfaLoginProvider = {
  type: 'mfaLoginProvider',
  alias: 'My.MfaProvider.Authenticator',
  name: 'Authenticator MFA Provider',
  forProviderName: 'Umbraco.GoogleAuthenticator',
  element: () => import('./mfa-setup.element.js'),
  meta: {
    label: 'Authenticator App',
  },
};

export const manifests = [authManifest, mfaManifest];
```