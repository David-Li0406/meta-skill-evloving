# Okta

**Category**: authentication
**Description**: Okta identity and access management platform
**Homepage**: https://www.okta.com

## Package Detection

### NPM
*Okta JavaScript/Node.js SDKs*

- `@okta/okta-react`
- `@okta/okta-auth-js`
- `@okta/okta-sdk-nodejs`
- `@okta/jwt-verifier`
- `@okta/oidc-middleware`

### PYPI
*Okta Python SDKs*

- `okta`
- `okta-jwt-verifier`

### MAVEN
*Okta Java SDKs*

- `com.okta.sdk:okta-sdk-api`
- `com.okta.spring:okta-spring-boot-starter`

### GO
*Okta Go SDKs*

- `github.com/okta/okta-sdk-golang/v2`
- `github.com/okta/okta-jwt-verifier-golang`

### NUGET
*Okta .NET SDKs*

- `Okta.Sdk`
- `Okta.AspNetCore`

### Related Packages
- `@okta/okta-vue`
- `@okta/okta-angular`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@okta/okta-react['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@okta/okta-auth-js['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@okta/jwt-verifier['"]`
- Type: esm_import

**Pattern**: `require\(['"]@okta/okta-sdk-nodejs['"]\)`
- Type: commonjs_require

### Python

**Pattern**: `from\s+okta`
- Type: python_import

**Pattern**: `import\s+okta`
- Type: python_import

### Go

**Pattern**: `"github\.com/okta/okta-sdk-golang`
- Type: go_import

**Pattern**: `"github\.com/okta/okta-jwt-verifier-golang`
- Type: go_import

## Environment Variables

*Okta organization domain*

*Okta application client ID*

*Okta application client secret*

*Okta authorization server issuer*

*Okta API token for management operations*

*Okta organization URL*

*Okta API audience*


## Detection Notes

- Check for OKTA_DOMAIN, OKTA_CLIENT_ID environment variables
- Look for *.okta.com domain references
- Parent company of Auth0

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
