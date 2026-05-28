---
id: secrets-management
name: "Secrets Management"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Secrets Management

## Overview

Secrets management involves securely storing, accessing, and rotating sensitive information like passwords, API keys, certificates, and encryption keys. This methodology covers secret storage solutions, access patterns, and security best practices.

## When to Use

- Managing application credentials
- Storing API keys and tokens
- Handling database passwords
- Managing TLS certificates
- Implementing zero-trust security
- Meeting compliance requirements

## Process/Steps

### 1. Secrets Management Concepts

**Secret Types:**
```yaml
secret_types:
  credentials:
    - database_passwords
    - service_account_passwords
    - ssh_keys
    - api_keys

  certificates:
    - tls_certificates
    - ca_certificates
    - client_certificates
    - code_signing_keys

  tokens:
    - oauth_tokens
    - jwt_secrets
    - session_secrets
    - webhook_secrets

  encryption_keys:
    - data_encryption_keys
    - key_encryption_keys
    - hmac_keys
```

**Secret Lifecycle:**
```
Creation → Storage → Access → Rotation → Revocation
    │          │        │         │           │
    │          │        │         │           └── Audit, cleanup
    │          │        │         └── Automated or manual
    │          │        └── RBAC, audit logging
    │          └── Encrypted at rest
    └── Secure generation
```

### 2. HashiCorp Vault

**Installation:**
```bash
# Install Vault
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault

# Development mode (not for production)
vault server -dev

# Production configuration
vault server -config=/etc/vault.d/vault.hcl
```

**Configuration:**
```hcl
# /etc/vault.d/vault.hcl

storage "raft" {
  path    = "/opt/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file  = "/opt/vault/tls/vault.key"
}

api_addr = "https://vault.example.com:8200"
cluster_addr = "https://vault.example.com:8201"

ui = true

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-unseal"
}
```

**Basic Operations:**
```bash
# Initialize Vault
vault operator init

# Unseal Vault
vault operator unseal <unseal-key>

# Login
vault login <root-token>
vault login -method=userpass username=admin

# Enable secrets engine
vault secrets enable -path=secret kv-v2
vault secrets enable database
vault secrets enable pki

# Write secret
vault kv put secret/myapp/config \
  db_user="admin" \
  db_password="s3cr3t"

# Read secret
vault kv get secret/myapp/config
vault kv get -field=db_password secret/myapp/config

# Enable auth method
vault auth enable kubernetes
vault auth enable oidc
```

**Policies:**
```hcl
# /etc/vault.d/policies/myapp.hcl

# Read-only access to myapp secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Database credentials
path "database/creds/myapp-db" {
  capabilities = ["read"]
}

# PKI certificates
path "pki/issue/myapp" {
  capabilities = ["create", "update"]
}

# Deny access to admin paths
path "sys/*" {
  capabilities = ["deny"]
}
```

**Dynamic Database Credentials:**
```bash
# Enable database secrets engine
vault secrets enable database

# Configure database connection
vault write database/config/mydb \
  plugin_name=mysql-database-plugin \
  connection_url="{{username}}:{{password}}@tcp(db.example.com:3306)/" \
  allowed_roles="myapp" \
  username="vault" \
  password="vaultpassword"

# Create role
vault write database/roles/myapp \
  db_name=mydb \
  creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}'; GRANT SELECT ON mydb.* TO '{{name}}'@'%';" \
  default_ttl="1h" \
  max_ttl="24h"

# Get credentials
vault read database/creds/myapp
# Returns: username, password (auto-generated, auto-expires)
```

### 3. AWS Secrets Manager

**Create and Manage Secrets:**
```bash
# Create secret
aws secretsmanager create-secret \
  --name myapp/database \
  --secret-string '{"username":"admin","password":"s3cr3t"}'

# Get secret
aws secretsmanager get-secret-value \
  --secret-id myapp/database

# Rotate secret
aws secretsmanager rotate-secret \
  --secret-id myapp/database \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789:function:RotateSecret

# Update secret
aws secretsmanager update-secret \
  --secret-id myapp/database \
  --secret-string '{"username":"admin","password":"newpassword"}'
```

**Terraform Configuration:**
```hcl
# Create secret
resource "aws_secretsmanager_secret" "database" {
  name        = "myapp/database"
  description = "Database credentials for myapp"

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    username = "admin"
    password = random_password.db_password.result
  })
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Rotation configuration
resource "aws_secretsmanager_secret_rotation" "database" {
  secret_id           = aws_secretsmanager_secret.database.id
  rotation_lambda_arn = aws_lambda_function.rotate_secret.arn

  rotation_rules {
    automatically_after_days = 30
  }
}
```

**Application Access (Python):**
```python
import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name, region_name="us-east-1"):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    if 'SecretString' in response:
        return json.loads(response['SecretString'])
    else:
        return base64.b64decode(response['SecretBinary'])

# Usage
db_creds = get_secret("myapp/database")
db_user = db_creds['username']
db_password = db_creds['password']
```

### 4. Kubernetes Secrets

**Create Secrets:**
```yaml
# Opaque secret
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: default
type: Opaque
data:
  db_password: cGFzc3dvcmQxMjM=  # base64 encoded
  api_key: YWJjZGVmMTIzNDU2

# Or create from command line
# kubectl create secret generic myapp-secrets \
#   --from-literal=db_password=password123 \
#   --from-literal=api_key=abcdef123456

---
# TLS secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64-cert>
  tls.key: <base64-key>

---
# Docker registry secret
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-docker-config>
```

**Use Secrets in Pods:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: myapp
      image: myapp:latest

      # Environment variables from secret
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: db_password

      # All keys as env vars
      envFrom:
        - secretRef:
            name: myapp-secrets

      # Volume mount
      volumeMounts:
        - name: secrets-volume
          mountPath: /etc/secrets
          readOnly: true

  volumes:
    - name: secrets-volume
      secret:
        secretName: myapp-secrets
        items:
          - key: api_key
            path: api-key.txt
```

**External Secrets Operator:**
```yaml
# SecretStore for AWS Secrets Manager
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets
  namespace: default
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        secretRef:
          accessKeyIDSecretRef:
            name: aws-credentials
            key: access-key-id
          secretAccessKeySecretRef:
            name: aws-credentials
            key: secret-access-key

---
# ExternalSecret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
  data:
    - secretKey: db_password
      remoteRef:
        key: myapp/database
        property: password
```

### 5. Environment Variables and .env Files

**Secure .env Handling:**
```bash
# .env file (NEVER commit to git)
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=secret123
API_KEY=abcdef123456

# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key
```

**Loading Environment Variables:**
```python
# Python with python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

db_password = os.getenv('DB_PASSWORD')
api_key = os.environ['API_KEY']  # Raises if not set
```

```javascript
// Node.js with dotenv
require('dotenv').config();

const dbPassword = process.env.DB_PASSWORD;
const apiKey = process.env.API_KEY;
```

### 6. SOPS (Secrets OPerationS)

**Encrypt Secrets in Git:**
```yaml
# .sops.yaml configuration
creation_rules:
  - path_regex: secrets/.*\.yaml$
    kms: arn:aws:kms:us-east-1:123456789:key/abc123
    pgp: FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4

  - path_regex: secrets/production/.*
    kms: arn:aws:kms:us-east-1:123456789:key/prod-key

  - path_regex: secrets/staging/.*
    kms: arn:aws:kms:us-east-1:123456789:key/staging-key
```

**Encrypt/Decrypt:**
```bash
# Create encrypted file
sops secrets/database.yaml
# Opens editor, encrypts on save

# Encrypt existing file
sops -e secrets.yaml > secrets.enc.yaml

# Decrypt file
sops -d secrets.enc.yaml > secrets.yaml

# Edit encrypted file in place
sops secrets.enc.yaml

# Extract single value
sops -d --extract '["database"]["password"]' secrets.enc.yaml
```

**Encrypted File Example:**
```yaml
# secrets.enc.yaml (encrypted)
database:
    username: ENC[AES256_GCM,data:dGVzdA==,iv:...,tag:...,type:str]
    password: ENC[AES256_GCM,data:c2VjcmV0,iv:...,tag:...,type:str]
sops:
    kms:
        - arn: arn:aws:kms:us-east-1:123456789:key/abc123
          created_at: "2024-01-15T10:00:00Z"
          enc: AQICAHh...
```

### 7. Secret Rotation

**Rotation Strategy:**
```yaml
rotation_strategy:
  automatic:
    interval: 30_days
    triggers:
      - scheduled
      - on_compromise
      - on_personnel_change

  process:
    1. generate_new_secret
    2. update_secret_store
    3. update_applications  # graceful
    4. verify_new_secret_works
    5. revoke_old_secret
    6. audit_log

  zero_downtime:
    - dual_secret_support  # app accepts old and new
    - rolling_deployment
    - health_check_verification
```

**AWS Lambda Rotation Function:**
```python
import boto3
import json
import string
import secrets

def lambda_handler(event, context):
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    client = boto3.client('secretsmanager')

    if step == "createSecret":
        # Generate new password
        new_password = ''.join(secrets.choice(
            string.ascii_letters + string.digits + "!@#$%"
        ) for _ in range(32))

        # Store pending secret
        client.put_secret_value(
            SecretId=arn,
            ClientRequestToken=token,
            SecretString=json.dumps({"password": new_password}),
            VersionStages=['AWSPENDING']
        )

    elif step == "setSecret":
        # Update the database with new password
        # (implementation depends on database type)
        pass

    elif step == "testSecret":
        # Test that new password works
        pass

    elif step == "finishSecret":
        # Promote pending to current
        metadata = client.describe_secret(SecretId=arn)
        current_version = None
        for version, stages in metadata['VersionIdsToStages'].items():
            if 'AWSCURRENT' in stages:
                current_version = version
                break

        client.update_secret_version_stage(
            SecretId=arn,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
            RemoveFromVersionId=current_version
        )
```

## Best Practices

### Storage
1. **Encrypt at rest** - Never store secrets in plaintext
2. **Access control** - Principle of least privilege
3. **Audit logging** - Track all access
4. **Backup encryption keys** - Separate from secrets

### Access
1. **Short-lived credentials** - Use dynamic secrets
2. **Application identity** - Not user credentials
3. **No secrets in code** - Environment or secret store
4. **No secrets in logs** - Mask sensitive data

### Rotation
1. **Automate rotation** - Reduce human error
2. **Grace periods** - Support old+new during transition
3. **Test rotation** - Verify before production
4. **Incident response** - Rapid rotation on breach

### Development
1. **Different secrets per env** - Dev, staging, prod
2. **Mock secrets in tests** - Don't use real secrets
3. **Secret scanning** - Pre-commit hooks
4. **Documentation** - Where secrets come from

## Templates/Examples

### Git Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for potential secrets
PATTERNS=(
    'password\s*=\s*["\047][^"\047]+'
    'api[_-]?key\s*=\s*["\047][^"\047]+'
    'secret\s*=\s*["\047][^"\047]+'
    'AKIA[0-9A-Z]{16}'  # AWS Access Key
    '-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----'
)

for pattern in "${PATTERNS[@]}"; do
    if git diff --cached --name-only | xargs grep -l -E "$pattern" 2>/dev/null; then
        echo "ERROR: Potential secret detected!"
        echo "Pattern: $pattern"
        exit 1
    fi
done

exit 0
```

### Application Configuration

```python
# config.py - Secure configuration loading

import os
from functools import lru_cache

class Settings:
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')

    @lru_cache()
    def get_db_password(self):
        """Get database password from secure source"""
        if self.environment == 'development':
            return os.getenv('DB_PASSWORD', 'dev_password')

        # Production: use Vault or AWS Secrets Manager
        import hvac
        client = hvac.Client(url=os.getenv('VAULT_ADDR'))
        secret = client.secrets.kv.v2.read_secret_version(
            path='myapp/database'
        )
        return secret['data']['data']['password']

settings = Settings()
```

## References

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [SOPS](https://github.com/getsops/sops)
- [External Secrets Operator](https://external-secrets.io/)
