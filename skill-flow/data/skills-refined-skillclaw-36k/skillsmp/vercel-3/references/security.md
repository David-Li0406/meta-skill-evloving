# Vercel - Security

**Pages:** 5

---

## Authentication

**URL:** https://vercel.com/docs/ai-gateway/authentication

**Contents:**
- Authentication
- API key
  - Creating an API Key
  - Navigate to the AI Gateway tab
  - Access API key management
  - Create a new API key
  - Save your API key
  - Using the API key
- OIDC token
  - Setting up OIDC authentication

To use the AI Gateway, you need to authenticate your requests. There are two authentication methods available:

API keys provide a secure way to authenticate your requests to the AI Gateway. You can create and manage multiple API keys through the Vercel Dashboard.

From the Vercel dashboard, click the AI Gateway tab to access the AI Gateway settings.

Click API keys on the left sidebar to view and manage your API keys.

Click Create key and proceed with Create key from the dialog to generate a new API key.

Once you have the API key, save it to at the root of your project (or in your preferred environment file):

When you specify a model id as a plain string, the AI SDK will automatically use the Vercel AI Gateway provider to route the request. The AI Gateway provider looks for the API key in the environment variable by default.

The Vercel OIDC token is a way to authenticate your requests to the AI Gateway without needing to manage an API key. Vercel automatically generates the OIDC token that it associates with your Vercel project.

Vercel OIDC tokens are only valid for 12 hours, so you will need to refresh them periodically during local development. You can do this by running again.

Before you can use the OIDC token during local development, ensure that you link your application to a Vercel project:

Pull the environment variables from Vercel to get the OIDC token:

With OIDC authentication, you can directly use the gateway provider without needing to obtain an API key or set it in an environment variable:

---

## Content Security Policy

**URL:** https://vercel.com/docs/headers/security-headers

**Contents:**
- Content Security Policy
- Content Security Policy headers
- Best Practices

Content Security Policy is a browser feature designed to prevent cross-site scripting (XSS) and related code-injection attacks. CSP provides developers with the ability to define an allowlist of sources of trusted content, effectively restricting the browser from loading any resources from non-allowlisted sources.

When a browser receives the HTTP header from a web server it adheres to the defined policy, blocking or allowing content loads based on the provided rules.

XSS remains one of the most prevalent web application vulnerabilities. In an XSS attack, malicious scripts are injected into websites, which run on the end user's browser, potentially leading to stolen data, session hijacking, and other malicious actions.

CSP can reduce the likelihood of XSS by:

While input sanitization and secure coding practices are essential, CSP acts as a second line of defense, reducing the risk of XSS exploits.

Beyond XSS, CSP can prevent the unauthorized loading of content, protecting users from other threats like clickjacking and data injection.

Keep in mind that while CSP is a robust security measure, it's part of a multi-layered security strategy. Input validation, output encoding, and other security practices remain crucial.

Additionally, while CSP is supported by modern browsers, nuances exist in their implementations. Ensure you test your policy across diverse browsers, accounting for variations and ensuring the same security postures.

---

## Two-factor Authentication

**URL:** https://vercel.com/docs/two-factor-authentication

**Contents:**
- Two-factor Authentication
- Enabling Two-factor Authentication
  - Configuring an Authenticator App (TOTP)
  - Configuring a Passkey
  - Recovery Codes
- Enforcing Two-Factor Authentication

To add an additional layer of security to your Vercel account, you can enable two-factor authentication (2FA). This feature requires you to provide a second form of verification when logging in to your account. There are two methods available for 2FA on Vercel:

Scan the QR code with your authenticator app or manually enter the provided key. Once added, enter the generated 6-digit code to verify your setup.

See the Login with passkeys for more information on setting up a security key or biometric key.

After setting up two-factor authentication (2FA), you will be prompted to save your recovery codes. Store these codes in a safe place, as they can be used to access your account if you lose access to your 2FA methods.

Each recovery code can only be used once, and you can generate a new set of codes at any time.

Teams can enforce two-factor authentication (2FA) for all members. Once enabled, team members must configure 2FA before accessing team resources. Visit the Two-Factor Enforcement documentation for more information on how to enforce 2FA for your team.

---

## Drains Security

**URL:** https://vercel.com/docs/drains/security

**Contents:**
- Drains Security
- Secure Drains
- IP Address Visibility
- More resources

All Drains support transport-level encryption using HTTPS protocol.

When your server starts receiving payloads, a third party could send data to your server if it knows the URL. Therefore, you should verify the request is coming from Vercel.

Vercel sends an header with each drain, which is a hash of the payload body created using your Drain signature secret. You can find or update this secret by clicking Edit in the Drains list.

To verify the request is coming from Vercel, you can generate the hash and compare it with the header value as shown below:

For enhanced security against timing attacks, use constant-time comparison when verifying the header. See x-vercel-signature in Request Headers.

For additional authentication or identification purposes, you can also add custom headers when configuring the Drain destination

Managing IP address visibility is available on Enterprise and Pro plans

Those with the owner, admin role can access this feature

Drains can include public IP addresses in the data, which may be considered personal information under certain data protection laws. To hide IP addresses in your drains:

This setting is applied team-wide across all projects and drains.

For more information on Drains security and how to use them, check out the following resources:

---

## Headers

**URL:** https://vercel.com/docs/headers

**Contents:**
- Headers
- Using headers
- Request headers
- Response headers
- Cache-Control header
- More resources

Headers are small pieces of information that are sent between the client (usually a web browser) and the server. They contain metadata about the request and response, such as the content type, cache-control directives, and authentication tokens. HTTP headers can be found in both the HTTP Request and HTTP Response.

By using headers effectively, you can optimize the performance and security of your application on Vercel's edge network. Here are some tips for using headers on Vercel:

To learn about the request headers sent to each Vercel deployment and how to use them to process requests before sending a response, see Request headers.

To learn about the response headers included in Vercel deployment responses and how to use them to process responses before sending a response, see Response headers.

To learn about the cache-control headers sent to each Vercel deployment and how to use them to control the caching behavior of your application, see Cache-Control headers.

---
