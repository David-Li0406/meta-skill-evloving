# Auth0

**Category**: authentication
**Description**: Auth0 identity and access management platform
**Homepage**: https://auth0.com

## Package Detection

### NPM
*Auth0 JavaScript/Node.js SDKs*

- `@auth0/auth0-react`
- `@auth0/nextjs-auth0`
- `@auth0/auth0-spa-js`
- `auth0`
- `express-openid-connect`
- `passport-auth0`

### PYPI
*Auth0 Python SDKs*

- `auth0-python`
- `authlib`
- `python-jose`

### RUBYGEMS
*Auth0 Ruby SDKs*

- `auth0`
- `omniauth-auth0`

### MAVEN
*Auth0 Java SDKs*

- `com.auth0:auth0`
- `com.auth0:java-jwt`
- `com.auth0:jwks-rsa`

### GO
*Auth0 Go SDKs*

- `github.com/auth0/go-auth0`
- `github.com/auth0/go-jwt-middleware`

### Related Packages
- `@auth0/auth0-vue`
- `@auth0/auth0-angular`
- `auth0-lock`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@auth0/auth0-react['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@auth0/nextjs-auth0['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@auth0/auth0-spa-js['"]`
- Type: esm_import

**Pattern**: `require\(['"]auth0['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]express-openid-connect['"]`
- Type: esm_import

### Python

**Pattern**: `from\s+auth0`
- Type: python_import

**Pattern**: `import\s+auth0`
- Type: python_import

### Go

**Pattern**: `"github\.com/auth0/go-auth0`
- Type: go_import

**Pattern**: `"github\.com/auth0/go-jwt-middleware`
- Type: go_import

## Environment Variables

*Auth0 tenant domain*

*Auth0 application client ID*

*Auth0 application client secret*

*Auth0 API audience*

*Auth0 issuer base URL*

*Auth0 session secret (Next.js)*

*Application base URL*

*Default OAuth scopes*


## Detection Notes

- Check for AUTH0_DOMAIN, AUTH0_CLIENT_ID environment variables
- Look for *.auth0.com domain references
- Now part of Okta

## Secrets Detection

### API Keys and Credentials

#### Auth0 Client Secret
**Pattern**: `(?:AUTH0_CLIENT_SECRET|auth0_client_secret)\s*[=:]\s*['"]?([A-Za-z0-9_-]{64,})['"]?`
**Severity**: critical
**Description**: Auth0 application client secret - used for backend authentication
**Example**: `AUTH0_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
**Environment Variable**: `AUTH0_CLIENT_SECRET`
**Note**: 64+ character string, varies by application type

#### Auth0 Management API Token
**Pattern**: `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
**Severity**: critical
**Description**: Auth0 Management API JWT token
**Context Required**: Should appear in context of Auth0 management operations
**Note**: Standard JWT format - requires context to distinguish from other JWTs

#### Auth0 API Secret (Legacy)
**Pattern**: `(?:AUTH0_API_SECRET)\s*[=:]\s*['"]?([A-Za-z0-9_-]{32,})['"]?`
**Severity**: high
**Description**: Auth0 API signing secret (legacy applications)
**Environment Variable**: `AUTH0_API_SECRET`

### Validation

#### API Documentation
- **API Reference**: https://auth0.com/docs/api
- **Management API**: https://auth0.com/docs/api/management/v2
- **Authentication API**: https://auth0.com/docs/api/authentication

#### Validation Endpoint
**API**: Auth0 Client Credentials Grant
**Endpoint**: `https://{domain}/oauth/token`
**Method**: POST
**Body**:
```json
{
  "client_id": "<client_id>",
  "client_secret": "<client_secret>",
  "audience": "https://{domain}/api/v2/",
  "grant_type": "client_credentials"
}
```
**Purpose**: Validates client credentials by obtaining access token

```bash
# Validate Auth0 credentials
curl -s --request POST \
  --url "https://${AUTH0_DOMAIN}/oauth/token" \
  --header 'content-type: application/json' \
  --data "{\"client_id\":\"${AUTH0_CLIENT_ID}\",\"client_secret\":\"${AUTH0_CLIENT_SECRET}\",\"audience\":\"https://${AUTH0_DOMAIN}/api/v2/\",\"grant_type\":\"client_credentials\"}"
```

#### Validation Code (Python)
```python
import requests

def validate_auth0_credentials(domain, client_id, client_secret):
    """Validate Auth0 client credentials"""
    try:
        response = requests.post(
            f'https://{domain}/oauth/token',
            json={
                'client_id': client_id,
                'client_secret': client_secret,
                'audience': f'https://{domain}/api/v2/',
                'grant_type': 'client_credentials'
            }
        )
        if response.status_code == 200:
            data = response.json()
            return {
                'valid': True,
                'token_type': data.get('token_type'),
                'expires_in': data.get('expires_in')
            }
        return {'valid': False, 'status': response.status_code, 'error': response.json()}
    except Exception as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
- **Secret Pattern Detection**: 75% (MEDIUM) - Client secrets are generic strings, need context
