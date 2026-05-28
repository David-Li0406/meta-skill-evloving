---
name: vault
title: HashiCorp Vault Secrets
description: Patterns for accessing secrets from HashiCorp Vault and syncing to AWS
subtypes:
  - typescript
  - python
  - terraform
  - auth
  - jenkins
---

# HashiCorp Vault Secrets

Patterns for accessing secrets from HashiCorp Vault and syncing to AWS.
ASU uses multiple Vault clusters (CaaS, DCO, Ops) with various auth
methods including AppRole, AWS IAM, Kubernetes, and OIDC.

## Vault Clusters

| Cluster | URL |
|---------|-----|
| CaaS Vault | vault.caas-{env}.asu.edu |
| Ops Vault | ops-vault-prod.opsprod.asu.edu |

## Secret Path Convention

```
secret/services/{org}/{team}/{app}/{environment}/{component}
```

## TypeScript

**RECOMMENDED: Use AWS SDK instead of direct Vault access**

### AWS Secrets Manager (Preferred)

**Package**: @aws-sdk/client-secrets-manager
**Example**: ASU/lms-canvas-enrollment-system

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-west-2' });
const secret = await client.send(
  new GetSecretValueCommand({ SecretId: 'my-secret' })
);
const data = JSON.parse(secret.SecretString!);
```

### SSM Parameter Store

**Package**: @aws-sdk/client-ssm
**Example**: ASU/cremo-cmidp-course-requisite-api

```typescript
import { SSMClient, GetParameterCommand } from '@aws-sdk/client-ssm';

const client = new SSMClient({ region: 'us-west-2' });
const param = await client.send(
  new GetParameterCommand({ Name: '/my/param', WithDecryption: true })
);
```

### Example Repos
- ASU/lms-canvas-enrollment-system
- ASU/cremo-cmidp-course-requisite-api
- ASU/iden-universal-service-provisioner

## Python

### Token File Pattern

**Repo**: ASU/edna-rmi-linux
**Path**: ansible/roles/edna/files/serviceConfigLookup.py

```python
import hvac
import boto3

# Read token from file
with open('/var/run/vault-token') as token:
    TOKENVAL = token.read()
client = hvac.Client(url='https://ops-vault-prod.opsprod.asu.edu', token=TOKENVAL)

# Fallback: AWS IAM authentication
if not client.is_authenticated():
    session = boto3.Session()
    cred = session.get_credentials()
    client.auth.aws.iam_login(cred.access_key, cred.secret_key, cred.token, role='...')

secret = client.secrets.kv.v1.read_secret(path='services/...')['data']
client.logout()
```

### Environment Variables Pattern

**Repo**: ASU/oprah-product-map
**Path**: get_gdrive_sheet.py

```python
import hvac
vault_client = hvac.Client()  # Uses VAULT_ADDR and VAULT_TOKEN
secret_data = vault_client.secrets.kv.v1.read_secret(path='...')
```

## Terraform

### Vault to AWS Secrets Manager

**Repo**: ASU/wflow-kuali-approver-service
**Path**: terraform/secretsmanager.tf

```hcl
data "vault_generic_secret" "api_key" {
  path = "secret/services/dco/jenkins/wflow/kbapi/${terraform.workspace}/kuali_api_key"
}

resource "aws_secretsmanager_secret" "api_key" {
  name_prefix = "kuali-api-key-${terraform.workspace}-"
}

resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id     = aws_secretsmanager_secret.api_key.id
  secret_string = data.vault_generic_secret.api_key.data["api_key"]
}
```

### Vault to SSM Parameter Store

**Repo**: ASU/iden-identity-resolution-service-api
**Path**: terraform/secrets.tf

```hcl
resource "aws_ssm_parameter" "db" {
  name  = "/iden/irs/${terraform.workspace}/api/pscs/db"
  type  = "SecureString"
  value = data.vault_generic_secret.db.data_json
}
```

## Auth

### AppRole (Jenkins CI/CD)
- TTL: 30 minutes
- Example: ASU/caas-caas-vault → vault/approle-jenkins.tf

### AWS IAM (EC2/Lambda)
- Cross-account STS roles for Vault authentication
- Example: ASU/caas-caas-vault → vault/auth-aws.tf

### Kubernetes (EKS pods)
- Native Kubernetes service account auth
- Example: ASU/caas-caas-vault → vault/auth-iam-principals.tf

### OIDC (Human users)
- OIDC via AWS Cognito integration
- Example: ASU/caas-caas-vault → vault/oidc.tf

## Jenkins

From: ASU/devops-jenkins-pipeline-library/vars/

| Function | Description |
|----------|-------------|
| vaultLogin() | Login to Vault |
| caasVaultLogin() | Login to CaaS Vault |
| opsVaultLogin() | Login to Ops Vault |
| getVaultSecret() | Read secret from Vault |
| getVaultToken() | Get Vault token |
| getVaultAppRoleToken() | Get token via AppRole |

## Related Commands

```bash
discover.sh pattern --name vault --type typescript
discover.sh pattern --name vault --type python
discover.sh pattern --name vault --type terraform
discover.sh pattern --name vault --type auth
discover.sh pattern --name vault --type jenkins
discover.sh repos --domain vault
```
