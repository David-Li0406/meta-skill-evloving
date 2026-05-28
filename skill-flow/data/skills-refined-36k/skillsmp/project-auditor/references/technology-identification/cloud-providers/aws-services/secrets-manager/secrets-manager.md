# AWS Secrets Manager

**Category**: cloud-providers/aws-services
**Description**: Secrets management service
**Homepage**: https://aws.amazon.com/secrets-manager

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Secrets Manager packages*

- `@aws-sdk/client-secrets-manager` - Secrets Manager SDK v3

#### PYPI
*Secrets Manager Python packages*

- `boto3` - AWS SDK (includes Secrets Manager)

#### GO
*Secrets Manager Go packages*

- `github.com/aws/aws-sdk-go-v2/service/secretsmanager` - Secrets Manager SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-secrets-manager['"]`
- Secrets Manager SDK v3 import
- Example: `import { SecretsManagerClient } from '@aws-sdk/client-secrets-manager';`

#### Python
Extensions: `.py`

**Pattern**: `boto3\.client\(['"]secretsmanager['"]\)`
- Boto3 Secrets Manager client
- Example: `secrets = boto3.client('secretsmanager')`

### Code Patterns

**Pattern**: `secretsmanager\.|GetSecretValue|CreateSecret|PutSecretValue`
- Secrets Manager operations
- Example: `client.get_secret_value(SecretId='...')`

**Pattern**: `SECRET_ARN|SECRET_NAME|SECRETS_MANAGER`
- Secrets Manager environment variables
- Example: `SECRET_ARN=arn:aws:secretsmanager:...`

**Pattern**: `arn:aws:secretsmanager:[a-z0-9-]+:[0-9]+:secret:`
- Secret ARN
- Example: `arn:aws:secretsmanager:us-east-1:123456789:secret:my-secret-abc123`

**Pattern**: `secretsmanager\..*\.amazonaws\.com`
- Secrets Manager endpoint

---

## Environment Variables

- `SECRET_ARN` - Secret ARN
- `SECRET_NAME` - Secret name
- `AWS_SECRET_ARN` - Alternative secret ARN

## Detection Notes

- Automatic rotation supported
- Cross-account sharing
- Versioning for secrets
- Often used for database credentials
- Cached secrets for performance

---

## TIER 3: Configuration Extraction

### Secret Name Extraction

**Pattern**: `(?:SecretId|secret[_-]?name|SECRET_NAME)\s*[=:]\s*['"]?([a-zA-Z0-9/_+=.@-]+)['"]?`
- Secret name or ARN
- Extracts: `secret_name`
- Example: `SECRET_NAME=prod/myapp/database`
