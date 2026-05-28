# Amazon Cognito

**Category**: cloud-providers/aws-services
**Description**: User authentication and authorization service
**Homepage**: https://aws.amazon.com/cognito

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Cognito JavaScript packages*

- `@aws-sdk/client-cognito-identity-provider` - Cognito Identity Provider SDK
- `@aws-sdk/client-cognito-identity` - Cognito Identity SDK
- `amazon-cognito-identity-js` - Cognito JavaScript SDK
- `@aws-amplify/auth` - Amplify Auth (uses Cognito)
- `aws-amplify` - Amplify SDK

#### PYPI
*Cognito Python packages*

- `boto3` - AWS SDK (includes Cognito)
- `pycognito` - Cognito Python wrapper
- `warrant` - Python Cognito client

#### GO
*Cognito Go packages*

- `github.com/aws/aws-sdk-go-v2/service/cognitoidentityprovider` - Cognito SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]amazon-cognito-identity-js['"]`
- Cognito JS SDK import
- Example: `import { CognitoUserPool } from 'amazon-cognito-identity-js';`

**Pattern**: `from\s+['"]@aws-amplify/auth['"]`
- Amplify Auth import
- Example: `import { Auth } from '@aws-amplify/auth';`

**Pattern**: `from\s+['"]@aws-sdk/client-cognito-identity-provider['"]`
- Cognito SDK v3 import

#### Python
Extensions: `.py`

**Pattern**: `^from\s+pycognito\s+import`
- pycognito import
- Example: `from pycognito import Cognito`

### Code Patterns

**Pattern**: `cognito-idp\.[a-z0-9-]+\.amazonaws\.com|cognito-identity\.`
- Cognito endpoints
- Example: `cognito-idp.us-east-1.amazonaws.com`

**Pattern**: `COGNITO_USER_POOL_ID|COGNITO_CLIENT_ID|COGNITO_IDENTITY_POOL_ID`
- Cognito environment variables
- Example: `COGNITO_USER_POOL_ID=us-east-1_abc123`

**Pattern**: `CognitoUserPool|CognitoUser|AuthenticationDetails`
- Cognito SDK classes
- Example: `new CognitoUserPool({UserPoolId, ClientId})`

**Pattern**: `[a-z]{2}-[a-z]+-[0-9]+_[a-zA-Z0-9]+`
- Cognito User Pool ID format
- Example: `us-east-1_abc123DEF`

**Pattern**: `[a-z0-9]{26}`
- Cognito Client ID format
- Example: `abc123def456ghi789jkl012mn`

**Pattern**: `arn:aws:cognito-idp:[a-z0-9-]+:[0-9]+:userpool/`
- Cognito User Pool ARN
- Example: `arn:aws:cognito-idp:us-east-1:123456789:userpool/us-east-1_abc123`

---

## Environment Variables

- `COGNITO_USER_POOL_ID` - User Pool ID
- `COGNITO_CLIENT_ID` - App Client ID
- `COGNITO_CLIENT_SECRET` - App Client Secret
- `COGNITO_IDENTITY_POOL_ID` - Identity Pool ID
- `COGNITO_REGION` - AWS region
- `AWS_COGNITO_USER_POOL_ID` - Alternative Pool ID
- `REACT_APP_COGNITO_USER_POOL_ID` - React app Pool ID
- `NEXT_PUBLIC_COGNITO_USER_POOL_ID` - Next.js Pool ID

## Detection Notes

- User Pools for authentication
- Identity Pools for authorization
- Hosted UI for OAuth flows
- JWT tokens for API authentication
- Amplify provides higher-level abstractions

---

## Secrets Detection

### Credentials

#### Cognito Client Secret
**Pattern**: `(?:cognito|COGNITO).*(?:client[_-]?secret|CLIENT[_-]?SECRET)\s*[=:]\s*['"]?([a-zA-Z0-9+/=]{52})['"]?`
**Severity**: critical
**Description**: Cognito App Client secret
**Example**: `COGNITO_CLIENT_SECRET=abc123...`

### Validation

#### API Documentation
- **API Reference**: https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/

---

## TIER 3: Configuration Extraction

### User Pool ID Extraction

**Pattern**: `(?:userPoolId|user[_-]?pool[_-]?id|COGNITO_USER_POOL_ID)\s*[=:]\s*['"]?([a-z]{2}-[a-z]+-[0-9]+_[a-zA-Z0-9]+)['"]?`
- Cognito User Pool ID
- Extracts: `user_pool_id`
- Example: `COGNITO_USER_POOL_ID=us-east-1_abc123DEF`

### Client ID Extraction

**Pattern**: `(?:clientId|client[_-]?id|COGNITO_CLIENT_ID)\s*[=:]\s*['"]?([a-z0-9]{26})['"]?`
- Cognito App Client ID
- Extracts: `client_id`
- Example: `COGNITO_CLIENT_ID=abc123def456...`

### Identity Pool ID Extraction

**Pattern**: `(?:identityPoolId|identity[_-]?pool[_-]?id|COGNITO_IDENTITY_POOL_ID)\s*[=:]\s*['"]?([a-z]{2}-[a-z]+-[0-9]+:[a-f0-9-]{36})['"]?`
- Cognito Identity Pool ID
- Extracts: `identity_pool_id`
- Example: `us-east-1:12345678-1234-1234-1234-123456789012`
