---
name: umbraco-authentication-providers
description: Use this skill when implementing authentication and MFA providers for the Umbraco backoffice using official documentation.
---

# Umbraco Authentication and MFA Providers

## What is it?
Authentication and MFA Providers enable external login (OAuth/SSO) and Two-Factor Authentication (2FA) for the Umbraco backoffice. These components provide the UI for users to log in using various methods (e.g., Google, GitHub) and to configure their 2FA settings.

## Documentation
Always fetch the latest docs before implementing:

- **External Login Providers**: https://docs.umbraco.com/umbraco-cms/reference/security/external-login-providers
- **Two-Factor Authentication**: https://docs.umbraco.com/umbraco-cms/reference/security/two-factor-authentication
- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - Which OAuth provider or 2FA method? Custom UI needed? Auto-redirect?
3. **Configure backend** - Set up C# authentication or ITwoFactorProvider first.
4. **Generate frontend files** - Create manifest + optional custom element.
5. **Explain** - Show what was created and how to test.

## Minimal Examples

### Authentication Provider Manifest (TypeScript)
```typescript
import type { ManifestAuthProvider } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestAuthProvider = {
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
    behavior: {
      autoRedirect: false,
      popupTarget: 'umbracoAuthPopup',
      popupFeatures: 'width=600,height=600,menubar=no,location=no',
    },
    linking: {
      allowManualLinking: true,
    },
  },
};

export const manifests = [manifest];
```

### MFA Provider Manifest (TypeScript)
```typescript
import type { ManifestMfaLoginProvider } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestMfaLoginProvider = {
  type: 'mfaLoginProvider',
  alias: 'My.MfaProvider.Authenticator',
  name: 'Authenticator App MFA',
  forProviderName: 'Umbraco.GoogleAuthenticator',
  element: () => import('./mfa-setup.element.js'),
  meta: {
    label: 'Authenticator App',
  },
};

export const manifests = [manifest];
```

### Custom Login Button Element (TypeScript)
```typescript
import { html, css, customElement, property } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-custom-auth-button')
export class MyCustomAuthButtonElement extends UmbLitElement {
  @property({ type: String })
  providerName = '';

  @property({ type: String })
  displayName = '';

  #handleClick() {
    this.dispatchEvent(
      new CustomEvent('auth-request', {
        bubbles: true,
        composed: true,
        detail: { providerName: this.providerName },
      })
    );
  }

  render() {
    return html`
      <button @click=${this.#handleClick}>
        <span>${this.displayName}</span>
      </button>
    `;
  }

  static styles = css`
    button {
      padding: 10px;
      cursor: pointer;
    }
  `;
}

export default MyCustomAuthButtonElement;
```

### MFA Setup Element (TypeScript)
```typescript
import { html, css, customElement, property, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-mfa-setup')
export class MyMfaSetupElement extends UmbLitElement {
  @property({ type: String })
  providerName = '';

  @property({ type: String })
  displayName = '';

  @state()
  private _loading = true;

  // Additional properties and methods for handling MFA setup...

  render() {
    if (this._loading) {
      return html`<uui-loader></uui-loader>`;
    }

    return html`
      <form>
        <p>Set up ${this.displayName}</p>
        <!-- Additional UI elements for MFA setup -->
      </form>
    `;
  }

  static styles = css`
    /* Styles for the MFA setup element */
  `;
}

export default MyMfaSetupElement;
```

## Backend C# Configuration (for reference)
```csharp
// Composer to register the provider
public class AuthenticationComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        builder.AddBackOfficeExternalLogins(logins =>
        {
            logins.AddBackOfficeLogin(
                backOfficeAuthenticationBuilder =>
                {
                    backOfficeAuthenticationBuilder.AddGitHub(
                        backOfficeAuthenticationBuilder.SchemeForBackOffice("Umbraco.GitHub")!,
                        options =>
                        {
                            options.ClientId = "your-client-id";
                            options.ClientSecret = "your-client-secret";
                            options.CallbackPath = "/umbraco-github-signin";
                        });
                });
        });
    }
}
```

## Common Meta Properties

| Property | Description |
|----------|-------------|
| `label` | Button text or provider name |
| `defaultView.icon` | Button icon |
| `defaultView.color` | Button color |
| `defaultView.look` | Button style |
| `behavior.autoRedirect` | Auto-redirect to provider on login page |
| `linking.allowManualLinking` | Allow linking to existing accounts |

That's it! Always fetch fresh docs, keep examples minimal, and generate complete working code.