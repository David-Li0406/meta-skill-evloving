# Secrets Management with HashiCorp Vault

Complete guide to implementing secrets management using HashiCorp Vault with secret rotation and application integration.

## 📝 Prompt

```
Create comprehensive secrets management implementation:

Context:
- Microservices architecture (Node.js, Python, Go)
- AWS cloud environment
- Kubernetes deployment
- Multiple environments (dev, staging, prod)
- Compliance requirements (PCI-DSS, SOC 2)

Include:
- HashiCorp Vault installation and configuration
- Secret engines (KV, Database, AWS, PKI)
- Dynamic secrets with automatic rotation
- Application integration examples
- Kubernetes integration with injector
- Access policies and authentication methods
- Audit logging and compliance
- Disaster recovery and backup strategies
- Migration from environment variables

Provide production-ready, secure implementations.
```

## 🔐 HashiCorp Vault Setup

### 1. Installation with Docker Compose

**File:** `vault/docker-compose.yml`

```yaml
version: '3.8'

services:
  vault:
    image: hashicorp/vault:1.15
    container_name: vault
    ports:
      - "8200:8200"
    environment:
      VAULT_ADDR: 'http://0.0.0.0:8200'
      VAULT_API_ADDR: 'http://0.0.0.0:8200'
      VAULT_DEV_ROOT_TOKEN_ID: 'root' # Only for development!
    cap_add:
      - IPC_LOCK
    volumes:
      - ./config:/vault/config
      - ./data:/vault/data
      - ./logs:/vault/logs
    command: server
    networks:
      - vault-network

  # Vault UI (optional)
  vault-ui:
    image: djenriquez/vault-ui:latest
    container_name: vault-ui
    ports:
      - "8000:8000"
    environment:
      VAULT_URL_DEFAULT: http://vault:8200
      VAULT_AUTH_DEFAULT: TOKEN
    depends_on:
      - vault
    networks:
      - vault-network

networks:
  vault-network:
    driver: bridge
```

### 2. Production Vault Configuration

**File:** `vault/config/vault.hcl`

```hcl
# Storage backend - Use Consul, etcd, or cloud storage in production
storage "file" {
  path = "/vault/data"
}

# For production, use:
# storage "consul" {
#   address = "consul:8500"
#   path    = "vault/"
# }

# Or AWS S3:
# storage "s3" {
#   bucket     = "my-vault-bucket"
#   region     = "us-east-1"
#   kms_key_id = "aws-kms-key-id"
# }

# Listener for client connections
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable   = 0
  tls_cert_file = "/vault/config/vault.crt"
  tls_key_file  = "/vault/config/vault.key"
}

# API address
api_addr = "https://vault.example.com:8200"

# Cluster address
cluster_addr = "https://vault.example.com:8201"

# UI
ui = true

# Telemetry for monitoring
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname          = false
  statsd_address           = "statsd:8125"
}

# Seal configuration - Use auto-unseal in production
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
}

# Logging
log_level = "info"
log_format = "json"

# Maximum lease TTL
max_lease_ttl = "768h"
default_lease_ttl = "768h"

# Disable mlock in containers (requires IPC_LOCK capability)
disable_mlock = false
```

### 3. Initialize and Unseal Vault

**File:** `scripts/init-vault.sh`

```bash
#!/bin/bash
set -euo pipefail

export VAULT_ADDR='https://vault.example.com:8200'
export VAULT_SKIP_VERIFY=0  # Set to 1 only for development!

echo "🔐 Initializing Vault..."

# Initialize Vault (only run once!)
vault operator init \
  -key-shares=5 \
  -key-threshold=3 \
  -format=json > vault-keys.json

echo "✅ Vault initialized successfully"
echo "⚠️  IMPORTANT: Store vault-keys.json in a secure location!"
echo "⚠️  You'll need 3 out of 5 unseal keys to unseal Vault"

# Extract unseal keys and root token
UNSEAL_KEY_1=$(jq -r '.unseal_keys_b64[0]' vault-keys.json)
UNSEAL_KEY_2=$(jq -r '.unseal_keys_b64[1]' vault-keys.json)
UNSEAL_KEY_3=$(jq -r '.unseal_keys_b64[2]' vault-keys.json)
ROOT_TOKEN=$(jq -r '.root_token' vault-keys.json)

echo ""
echo "🔓 Unsealing Vault..."

# Unseal Vault (requires 3 keys)
vault operator unseal "$UNSEAL_KEY_1"
vault operator unseal "$UNSEAL_KEY_2"
vault operator unseal "$UNSEAL_KEY_3"

echo "✅ Vault unsealed successfully"

# Login with root token
export VAULT_TOKEN="$ROOT_TOKEN"

echo ""
echo "✅ Vault is ready!"
echo "Root Token: $ROOT_TOKEN"
echo ""
echo "⚠️  Revoke root token after initial setup:"
echo "   vault token revoke $ROOT_TOKEN"
```

---

## 🔑 Secret Engines Configuration

### 1. Key-Value Secrets (Static Secrets)

```bash
#!/bin/bash
# Enable KV v2 secrets engine
vault secrets enable -path=secret kv-v2

# Write secrets
vault kv put secret/myapp/config \
  api_key="sk_live_abc123xyz" \
  db_password="SuperSecure123!" \
  jwt_secret="my-jwt-secret-key"

# Read secrets
vault kv get secret/myapp/config

# Get specific field
vault kv get -field=api_key secret/myapp/config

# Create versioned secret
vault kv put secret/myapp/config \
  api_key="sk_live_new_key_456" \
  db_password="NewPassword456!"

# Get specific version
vault kv get -version=1 secret/myapp/config

# List secrets
vault kv list secret/myapp
```

### 2. Database Secrets (Dynamic Secrets)

**Configure PostgreSQL dynamic secrets:**

```bash
#!/bin/bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/postgresql \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly,readwrite" \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb?sslmode=require" \
  username="vault_admin" \
  password="vault_admin_password"

# Create readonly role with automatic rotation
vault write database/roles/readonly \
  db_name=postgresql \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Create readwrite role
vault write database/roles/readwrite \
  db_name=postgresql \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Generate dynamic credentials (automatically rotated)
vault read database/creds/readonly
# Output:
# Key                Value
# ---                -----
# lease_id           database/creds/readonly/abc123
# lease_duration     1h
# lease_renewable    true
# password           A1a-randompassword
# username           v-root-readonly-xyz123

# Rotate root credentials
vault write -force database/rotate-root/postgresql
```

### 3. AWS Secrets Engine

```bash
#!/bin/bash
# Enable AWS secrets engine
vault secrets enable aws

# Configure AWS credentials
vault write aws/config/root \
  access_key=$AWS_ACCESS_KEY_ID \
  secret_key=$AWS_SECRET_ACCESS_KEY \
  region=us-east-1

# Create role for S3 read-only access
vault write aws/roles/s3-readonly \
  credential_type=iam_user \
  policy_document=-<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
EOF

# Generate AWS credentials (automatically rotated and deleted)
vault read aws/creds/s3-readonly
```

### 4. PKI Secrets Engine (TLS Certificates)

```bash
#!/bin/bash
# Enable PKI engine
vault secrets enable pki

# Set max lease TTL to 10 years
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write -field=certificate pki/root/generate/internal \
  common_name="Example Root CA" \
  ttl=87600h > CA_cert.crt

# Configure CA and CRL URLs
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com:8200/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"

# Create role for issuing certificates
vault write pki/roles/example-dot-com \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl="720h"

# Issue certificate
vault write pki/issue/example-dot-com \
  common_name="api.example.com" \
  ttl="24h"
```

---

## 🔒 Access Policies

### 1. Policy Definitions

**File:** `vault/policies/app-policy.hcl`

```hcl
# Policy for application to read secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Allow reading database credentials
path "database/creds/readonly" {
  capabilities = ["read"]
}

# Allow reading AWS credentials
path "aws/creds/s3-readonly" {
  capabilities = ["read"]
}

# Allow token renewal
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Deny everything else
path "*" {
  capabilities = ["deny"]
}
```

**File:** `vault/policies/admin-policy.hcl`

```hcl
# Full access to secrets
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Manage policies
path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Manage auth methods
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Manage secret engines
path "sys/mounts/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Read system health
path "sys/health" {
  capabilities = ["read", "sudo"]
}
```

### 2. Apply Policies

```bash
#!/bin/bash
# Write policies to Vault
vault policy write app-policy vault/policies/app-policy.hcl
vault policy write admin-policy vault/policies/admin-policy.hcl

# List policies
vault policy list

# Read policy
vault policy read app-policy
```

---

## 🔐 Authentication Methods

### 1. AppRole Authentication (for applications)

```bash
#!/bin/bash
# Enable AppRole auth
vault auth enable approle

# Create AppRole for application
vault write auth/approle/role/myapp \
  token_policies="app-policy" \
  token_ttl=1h \
  token_max_ttl=4h \
  secret_id_ttl=0 \
  secret_id_num_uses=0

# Get Role ID (safe to share)
ROLE_ID=$(vault read -field=role_id auth/approle/role/myapp/role-id)

# Generate Secret ID (keep secret!)
SECRET_ID=$(vault write -field=secret_id -f auth/approle/role/myapp/secret-id)

echo "Role ID: $ROLE_ID"
echo "Secret ID: $SECRET_ID"

# Application uses these to authenticate
vault write auth/approle/login \
  role_id="$ROLE_ID" \
  secret_id="$SECRET_ID"
```

### 2. Kubernetes Authentication

```bash
#!/bin/bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
  token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token

# Create role for Kubernetes service account
vault write auth/kubernetes/role/myapp \
  bound_service_account_names=myapp-sa \
  bound_service_account_namespaces=production \
  policies=app-policy \
  ttl=1h
```

### 3. JWT/OIDC Authentication (for CI/CD)

```bash
#!/bin/bash
# Enable JWT auth
vault auth enable jwt

# Configure JWT auth for GitHub Actions
vault write auth/jwt/config \
  oidc_discovery_url="https://token.actions.githubusercontent.com" \
  bound_issuer="https://token.actions.githubusercontent.com"

# Create role for GitHub Actions
vault write auth/jwt/role/github-actions \
  role_type="jwt" \
  bound_audiences="https://github.com/myorg" \
  bound_claims='{"repository":"myorg/myrepo"}' \
  user_claim="sub" \
  policies="app-policy" \
  ttl=1h
```

---

## 💻 Application Integration

### 1. Node.js Integration

**File:** `src/vault-client.js`

```javascript
const vault = require('node-vault');

class VaultClient {
  constructor() {
    this.client = vault({
      apiVersion: 'v1',
      endpoint: process.env.VAULT_ADDR || 'https://vault.example.com:8200',
      requestOptions: {
        timeout: 5000,
      },
    });
    
    this.token = null;
    this.roleId = process.env.VAULT_ROLE_ID;
    this.secretId = process.env.VAULT_SECRET_ID;
  }

  // Authenticate with AppRole
  async authenticate() {
    try {
      const response = await this.client.approleLogin({
        role_id: this.roleId,
        secret_id: this.secretId,
      });

      this.token = response.auth.client_token;
      this.client.token = this.token;

      console.log('✅ Authenticated with Vault');
      
      // Setup token renewal
      this.setupTokenRenewal(response.auth.lease_duration);
      
      return true;
    } catch (error) {
      console.error('❌ Vault authentication failed:', error.message);
      throw error;
    }
  }

  // Setup automatic token renewal
  setupTokenRenewal(leaseDuration) {
    // Renew token at 90% of lease duration
    const renewInterval = (leaseDuration * 0.9) * 1000;
    
    setInterval(async () => {
      try {
        await this.client.tokenRenewSelf();
        console.log('✅ Token renewed successfully');
      } catch (error) {
        console.error('❌ Token renewal failed:', error.message);
        // Re-authenticate
        await this.authenticate();
      }
    }, renewInterval);
  }

  // Read KV secret
  async getSecret(path) {
    try {
      const response = await this.client.read(`secret/data/${path}`);
      return response.data.data;
    } catch (error) {
      console.error(`❌ Failed to read secret ${path}:`, error.message);
      throw error;
    }
  }

  // Get dynamic database credentials
  async getDatabaseCredentials(role = 'readonly') {
    try {
      const response = await this.client.read(`database/creds/${role}`);
      
      return {
        username: response.data.username,
        password: response.data.password,
        leaseId: response.lease_id,
        leaseDuration: response.lease_duration,
      };
    } catch (error) {
      console.error('❌ Failed to get database credentials:', error.message);
      throw error;
    }
  }

  // Renew lease for dynamic secrets
  async renewLease(leaseId) {
    try {
      await this.client.write('sys/leases/renew', {
        lease_id: leaseId,
      });
      console.log(`✅ Lease ${leaseId} renewed`);
    } catch (error) {
      console.error(`❌ Failed to renew lease ${leaseId}:`, error.message);
      throw error;
    }
  }

  // Revoke lease
  async revokeLease(leaseId) {
    try {
      await this.client.write('sys/leases/revoke', {
        lease_id: leaseId,
      });
      console.log(`✅ Lease ${leaseId} revoked`);
    } catch (error) {
      console.error(`❌ Failed to revoke lease ${leaseId}:`, error.message);
      throw error;
    }
  }
}

// Usage example
async function main() {
  const vaultClient = new VaultClient();
  
  // Authenticate
  await vaultClient.authenticate();
  
  // Get static secrets
  const config = await vaultClient.getSecret('myapp/config');
  console.log('API Key:', config.api_key);
  
  // Get dynamic database credentials
  const dbCreds = await vaultClient.getDatabaseCredentials('readonly');
  console.log('DB Username:', dbCreds.username);
  console.log('DB Password:', dbCreds.password);
  
  // Use credentials...
  
  // Cleanup: revoke lease when done
  // await vaultClient.revokeLease(dbCreds.leaseId);
}

module.exports = { VaultClient };
```

### 2. Python Integration

**File:** `vault_client.py`

```python
import os
import hvac
import time
from threading import Thread

class VaultClient:
    def __init__(self):
        self.vault_addr = os.getenv('VAULT_ADDR', 'https://vault.example.com:8200')
        self.role_id = os.getenv('VAULT_ROLE_ID')
        self.secret_id = os.getenv('VAULT_SECRET_ID')
        
        self.client = hvac.Client(url=self.vault_addr)
        self.token = None
        self.lease_duration = None

    def authenticate(self):
        """Authenticate with Vault using AppRole"""
        try:
            response = self.client.auth.approle.login(
                role_id=self.role_id,
                secret_id=self.secret_id
            )
            
            self.token = response['auth']['client_token']
            self.client.token = self.token
            self.lease_duration = response['auth']['lease_duration']
            
            print('✅ Authenticated with Vault')
            
            # Start token renewal thread
            self._start_token_renewal()
            
            return True
        except Exception as e:
            print(f'❌ Vault authentication failed: {str(e)}')
            raise

    def _start_token_renewal(self):
        """Start background thread for token renewal"""
        def renew_token():
            while True:
                # Sleep for 90% of lease duration
                time.sleep(self.lease_duration * 0.9)
                try:
                    self.client.auth.token.renew_self()
                    print('✅ Token renewed successfully')
                except Exception as e:
                    print(f'❌ Token renewal failed: {str(e)}')
                    # Re-authenticate
                    self.authenticate()
        
        thread = Thread(target=renew_token, daemon=True)
        thread.start()

    def get_secret(self, path):
        """Read KV v2 secret"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret'
            )
            return response['data']['data']
        except Exception as e:
            print(f'❌ Failed to read secret {path}: {str(e)}')
            raise

    def get_database_credentials(self, role='readonly'):
        """Get dynamic database credentials"""
        try:
            response = self.client.read(f'database/creds/{role}')
            
            return {
                'username': response['data']['username'],
                'password': response['data']['password'],
                'lease_id': response['lease_id'],
                'lease_duration': response['lease_duration']
            }
        except Exception as e:
            print(f'❌ Failed to get database credentials: {str(e)}')
            raise

    def renew_lease(self, lease_id):
        """Renew lease for dynamic secrets"""
        try:
            self.client.sys.renew_lease(lease_id=lease_id)
            print(f'✅ Lease {lease_id} renewed')
        except Exception as e:
            print(f'❌ Failed to renew lease {lease_id}: {str(e)}')
            raise

    def revoke_lease(self, lease_id):
        """Revoke lease"""
        try:
            self.client.sys.revoke_lease(lease_id=lease_id)
            print(f'✅ Lease {lease_id} revoked')
        except Exception as e:
            print(f'❌ Failed to revoke lease {lease_id}: {str(e)}')
            raise

# Usage example
if __name__ == '__main__':
    vault = VaultClient()
    
    # Authenticate
    vault.authenticate()
    
    # Get static secrets
    config = vault.get_secret('myapp/config')
    print(f"API Key: {config['api_key']}")
    
    # Get dynamic database credentials
    db_creds = vault.get_database_credentials('readonly')
    print(f"DB Username: {db_creds['username']}")
    print(f"DB Password: {db_creds['password']}")
    
    # Use credentials...
    
    # Cleanup: revoke lease when done
    # vault.revoke_lease(db_creds['lease_id'])
```

---

## ☸️ Kubernetes Integration

### Vault Agent Injector

**File:** `k8s/deployment-with-vault.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        # Enable Vault Agent Injector
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "myapp"
        
        # Inject secret as file
        vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/config"
        vault.hashicorp.com/agent-inject-template-config: |
          {{- with secret "secret/data/myapp/config" -}}
          export API_KEY="{{ .Data.data.api_key }}"
          export DB_PASSWORD="{{ .Data.data.db_password }}"
          export JWT_SECRET="{{ .Data.data.jwt_secret }}"
          {{- end -}}
        
        # Inject database credentials
        vault.hashicorp.com/agent-inject-secret-db-creds: "database/creds/readonly"
        vault.hashicorp.com/agent-inject-template-db-creds: |
          {{- with secret "database/creds/readonly" -}}
          export DB_USERNAME="{{ .Data.username }}"
          export DB_PASSWORD="{{ .Data.password }}"
          {{- end -}}
    spec:
      serviceAccountName: myapp-sa
      containers:
        - name: app
          image: myapp:v1
          command: ["/bin/sh", "-c"]
          args:
            - |
              source /vault/secrets/config
              source /vault/secrets/db-creds
              node server.js
          ports:
            - containerPort: 3000
```

---

## 📊 Audit Logging

### Enable Audit Device

```bash
#!/bin/bash
# Enable file audit device
vault audit enable file file_path=/vault/logs/audit.log

# Enable syslog audit device
vault audit enable syslog tag="vault" facility="LOCAL7"

# List audit devices
vault audit list

# Example audit log entry
cat /vault/logs/audit.log | jq .
```

---

## 🔄 Secret Rotation Strategy

**File:** `scripts/rotate-secrets.sh`

```bash
#!/bin/bash
set -euo pipefail

echo "🔄 Starting secret rotation..."

# Rotate database root credentials
vault write -force database/rotate-root/postgresql
echo "✅ Database root credentials rotated"

# Rotate static secrets (manual process)
NEW_API_KEY=$(openssl rand -hex 32)
vault kv put secret/myapp/config \
  api_key="$NEW_API_KEY" \
  db_password="$(vault kv get -field=db_password secret/myapp/config)" \
  jwt_secret="$(openssl rand -base64 64)"

echo "✅ Static secrets rotated"

# Restart applications to pick up new secrets
kubectl rollout restart deployment/myapp -n production

echo "✅ Secret rotation complete"
```

---

## 💡 Best Practices

1. **Never use root token in production** - Create specific policies and roles
2. **Enable audit logging** - Track all secret access
3. **Use dynamic secrets when possible** - Automatic rotation and revocation
4. **Implement least privilege** - Grant minimal required permissions
5. **Rotate secrets regularly** - Automated rotation schedules
6. **Use auto-unseal in production** - AWS KMS, Azure Key Vault, or GCP KMS
7. **Backup Vault data** - Regular encrypted backups
8. **Monitor Vault health** - Alerting on seal/unseal events
9. **Secure Vault communication** - Always use TLS
10. **Test disaster recovery** - Regular DR drills

---

## 🎯 Quick Start

```bash
# 1. Start Vault
docker-compose up -d

# 2. Initialize and unseal
./scripts/init-vault.sh

# 3. Enable secret engines
vault secrets enable -path=secret kv-v2
vault secrets enable database

# 4. Create policies
vault policy write app-policy vault/policies/app-policy.hcl

# 5. Enable auth methods
vault auth enable approle

# 6. Test secret retrieval
vault kv get secret/myapp/config
```
