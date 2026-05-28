# Sensitive Files Patterns

**Category**: devops/git-history-security
**Description**: Sensitive files that should never be committed to git repositories
**Type**: security

These patterns detect sensitive files that pose security risks when committed to git.
When found in git history, these indicate potential credential leaks requiring immediate remediation.

---

## Environment Files

### Environment Configuration
**Pattern**: `\.env$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Environment files contain secrets, API keys, and database credentials
- NEVER commit to version control
- Remediation: Rotate all secrets in the file, use secret manager

### Environment File Variants
**Pattern**: `\.env\.(local|dev|development|prod|production|staging|test|ci)$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Environment-specific configuration files
- Often contain environment-specific secrets
- Remediation: Rotate all secrets, add to .gitignore

### Environment Backup Files
**Pattern**: `\.env\.bak$|\.env\.backup$|\.env\.old$`
**Type**: filepath
**Severity**: high
**Languages**: [all]
- Backup copies of environment files
- May contain outdated but still valid credentials
- Remediation: Rotate credentials, remove from history

---

## Cloud Provider Credentials

### AWS Credentials File
**Pattern**: `\.aws/credentials$|aws_credentials$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- AWS access keys and secret keys
- Full account access if leaked
- Remediation: Rotate keys immediately, use IAM roles instead

### AWS Config File
**Pattern**: `\.aws/config$`
**Type**: filepath
**Severity**: high
**Languages**: [all]
- AWS profile configuration
- May contain account IDs and regions
- Remediation: Remove from history, avoid committing

### GCP Service Account Key
**Pattern**: `.*service[-_]?account.*\.json$|gcloud.*\.json$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Google Cloud Platform service account credentials
- Provides programmatic access to GCP resources
- Remediation: Delete key in GCP Console, create new one

### GCP Credentials
**Pattern**: `\.gcp[-_]?credentials.*\.json$|application_default_credentials\.json$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- GCP application default credentials
- Remediation: Revoke and regenerate credentials

### Azure Credentials
**Pattern**: `\.azure/credentials$|azure_credentials\.json$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Azure service principal credentials
- Remediation: Rotate service principal secret

---

## SSH and SSL Keys

### SSH Private Keys
**Pattern**: `id_rsa$|id_dsa$|id_ecdsa$|id_ed25519$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- SSH private keys for authentication
- Can be used to access servers and repositories
- Remediation: Revoke key, generate new keypair

### SSH Private Key (Generic)
**Pattern**: `.*_rsa$|.*_dsa$|.*_ecdsa$|.*_ed25519$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Custom-named SSH private keys
- Remediation: Revoke and regenerate

### PEM Files
**Pattern**: `.*\.pem$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- PEM-encoded private keys or certificates
- May contain SSL/TLS private keys
- Remediation: Revoke certificate if private key exposed

### Private Key Files
**Pattern**: `.*\.key$|.*[-_]key$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Generic private key files
- Remediation: Revoke associated certificates

### PKCS12/PFX Certificates
**Pattern**: `.*\.p12$|.*\.pfx$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Certificate bundles with private keys
- Remediation: Revoke and reissue certificates

### Java Keystores
**Pattern**: `.*\.jks$|.*\.keystore$`
**Type**: filepath
**Severity**: critical
**Languages**: [java]
- Java keystore files with private keys
- Remediation: Regenerate keystore with new keys

---

## Configuration Files with Secrets

### Generic Credentials File
**Pattern**: `credentials\.json$|credentials\.ya?ml$|credentials\.xml$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Application credential files
- Remediation: Rotate all contained credentials

### Secrets Configuration
**Pattern**: `secrets\.json$|secrets\.ya?ml$|secrets\.xml$|secrets\.toml$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Application secrets files
- Remediation: Rotate all secrets

### Password Files
**Pattern**: `.*password.*\.txt$|.*passwd.*$|\.htpasswd$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Password storage files
- Remediation: Change all passwords

### API Key Files
**Pattern**: `api[-_]?key.*\.txt$|apikey.*$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- API key storage files
- Remediation: Rotate all API keys

---

## Infrastructure State Files

### Terraform State
**Pattern**: `.*\.tfstate$|terraform\.tfstate$`
**Type**: filepath
**Severity**: critical
**Languages**: [terraform]
- Terraform state files contain all resource attributes
- Often includes database passwords, API keys, etc.
- Remediation: Use remote state backend with encryption

### Terraform State Backup
**Pattern**: `.*\.tfstate\.backup$`
**Type**: filepath
**Severity**: critical
**Languages**: [terraform]
- Terraform state backup files
- Contains same sensitive data as state files
- Remediation: Never commit, use remote backend

### Terraform Variables
**Pattern**: `terraform\.tfvars$|.*\.auto\.tfvars$`
**Type**: filepath
**Severity**: high
**Languages**: [terraform]
- Terraform variable files may contain secrets
- Remediation: Use terraform.tfvars.example for templates

### Ansible Vault Files
**Pattern**: `.*vault.*\.ya?ml$|vault\.ya?ml$`
**Type**: filepath
**Severity**: high
**Languages**: [yaml]
- Ansible encrypted variable files
- Should be encrypted but patterns help verify
- Remediation: Ensure vault files are encrypted

---

## Kubernetes and Container Credentials

### Kubernetes Config
**Pattern**: `\.kube/config$|kubeconfig$`
**Type**: filepath
**Severity**: critical
**Languages**: [kubernetes, yaml]
- Kubernetes cluster access credentials
- Contains certificates and tokens
- Remediation: Revoke and regenerate cluster credentials

### Docker Config
**Type**: filepath
**Severity**: high
**Category**: credentials
**Pattern**: `\.docker/config\.json$|docker[-_]?config\.json$`
- Docker registry credentials
- Contains auth tokens for registries
- Remediation: Regenerate registry tokens

### Docker Compose Override
**Type**: filepath
**Severity**: medium
**Category**: configuration
**Pattern**: `docker-compose\.override\.ya?ml$`
- Local override configuration
- May contain development secrets
- Remediation: Use environment variables instead

---

## Database Files

### SQLite Databases
**Type**: filepath
**Severity**: high
**Category**: database
**Pattern**: `.*\.sqlite3?$|.*\.db$`
- SQLite database files
- May contain application data and user information
- Remediation: Remove from history if contains sensitive data

### Database Dumps
**Type**: filepath
**Severity**: critical
**Category**: database
**Pattern**: `.*dump.*\.sql$|.*backup.*\.sql$|.*\.sql\.gz$`
- Database dump files
- Contains all database content
- Remediation: Never commit database dumps

### MySQL/PostgreSQL Connection Files
**Type**: filepath
**Severity**: high
**Category**: credentials
**Pattern**: `\.my\.cnf$|\.pgpass$`
- Database client configuration with credentials
- Remediation: Use environment variables

---

## Token and Session Files

### GitHub Tokens
**Type**: filepath
**Severity**: critical
**Category**: credentials
**Pattern**: `\.github[-_]?token$|github[-_]?pat$`
- GitHub Personal Access Tokens
- Remediation: Revoke in GitHub Settings

### NPM Tokens
**Type**: filepath
**Severity**: high
**Category**: credentials
**Pattern**: `\.npmrc$`
- npm registry credentials
- May contain auth tokens
- Remediation: Regenerate npm token

### PyPI Tokens
**Type**: filepath
**Severity**: high
**Category**: credentials
**Pattern**: `\.pypirc$`
- PyPI registry credentials
- Remediation: Regenerate PyPI API token

### Netrc Files
**Type**: filepath
**Severity**: high
**Category**: credentials
**Pattern**: `\.netrc$|_netrc$`
- Machine credentials for various services
- Remediation: Change all contained passwords

---

## History Cleaning Tools

### Recommended Tools
When sensitive files are found in git history, use these tools to remove them:

1. **BFG Repo-Cleaner** (Recommended for most cases)
   ```
   bfg --delete-files .env
   bfg --replace-text passwords.txt
   git reflog expire --expire=now --all && git gc --prune=now --aggressive
   ```

2. **git-filter-repo** (More flexible but complex)
   ```
   git filter-repo --path .env --invert-paths
   ```

3. **After cleaning**:
   - Force push to all branches
   - Notify all contributors to re-clone
   - Rotate all potentially exposed secrets
   - Check for forks that may have copied the data
