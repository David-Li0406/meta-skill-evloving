# Secrets in Infrastructure as Code

**Category**: devops/secrets-in-iac
**Description**: Detection patterns for hardcoded secrets in IaC files (Terraform, Kubernetes, CloudFormation, Helm, GitHub Actions)
**CWE**: CWE-798 (Use of Hard-coded Credentials), CWE-312 (Cleartext Storage of Sensitive Information)

---

## Terraform Secrets

### Hardcoded AWS Access Key in Terraform
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:access_key|aws_access_key_id)\s*=\s*["']?(AKIA[0-9A-Z]{16})["']?`
- AWS access keys should not be hardcoded in Terraform files
- Example: `access_key = "AKIAIOSFODNN7EXAMPLE"`
- Remediation: Use AWS credentials provider, environment variables, or Vault

### Hardcoded AWS Secret Key in Terraform
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:secret_key|aws_secret_access_key)\s*=\s*["'][A-Za-z0-9/+=]{40}["']`
- AWS secret keys should never be in code
- Example: `secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"`
- Remediation: Use AWS credentials provider, environment variables, or Vault

### Hardcoded Password in Terraform
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:password|passwd|db_password|admin_password)\s*=\s*["'][^"'${}]{8,}["']`
- Passwords should not be hardcoded in Terraform
- Example: `password = "supersecret123"`
- Remediation: Use Terraform variables with sensitive=true, or secrets manager

### Hardcoded Private Key in Terraform
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:private_key|ssh_private_key|tls_private_key)\s*=\s*<<`
- Private keys should not be in Terraform files
- Example: `private_key = <<EOF...EOF`
- Remediation: Reference key files or use secrets manager

### Hardcoded API Key in Terraform
**Type**: regex
**Severity**: high
**Pattern**: `(?i)(?:api_key|apikey|api_secret)\s*=\s*["'][A-Za-z0-9_-]{20,}["']`
- API keys should not be hardcoded
- Example: `api_key = "sk-1234567890abcdefghij"`
- Remediation: Use environment variables or secrets manager

### Hardcoded Database Connection String
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:connection_string|database_url|db_url)\s*=\s*["'][^"']*(?:password|pwd)=[^"']+["']`
- Database connection strings with credentials should not be hardcoded
- Example: `connection_string = "postgresql://user:pass@host/db"`
- Remediation: Use dynamic secrets or reference from secrets manager

### Sensitive Variable Without Sensitive Flag
**Type**: regex
**Severity**: medium
**Pattern**: `(?i)variable\s*["'](?:password|secret|token|api_key|private_key)["']\s*\{(?:(?!sensitive\s*=\s*true).)*\}`
- Sensitive variables should have sensitive=true
- Example: Variable named "password" without sensitive flag
- Remediation: Add `sensitive = true` to variable definition

---

## Kubernetes Secrets

### Base64 Encoded Secret Value
**Type**: regex
**Severity**: high
**Pattern**: `(?i)kind:\s*Secret[\s\S]*?data:[\s\S]*?[a-zA-Z0-9_-]+:\s*[A-Za-z0-9+/]{20,}={0,2}`
- Kubernetes secrets with embedded data should use external secrets
- Example: Secret with base64 encoded password
- Remediation: Use External Secrets Operator or sealed-secrets

### Hardcoded Password in ConfigMap
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)kind:\s*ConfigMap[\s\S]*?data:[\s\S]*?(?:PASSWORD|SECRET|API_KEY|TOKEN):\s*[^\n]+`
- Passwords should never be in ConfigMaps
- Example: `PASSWORD: supersecret`
- Remediation: Use Kubernetes Secrets or external secrets management

### Plain Text Secret in Manifest
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)stringData:[\s\S]*?(?:password|secret|token|api[_-]?key):\s*[^\n${}]+`
- Plain text secrets in stringData are visible in version control
- Example: `password: mysecretpassword`
- Remediation: Use external secrets manager, Vault, or sealed-secrets

### Hardcoded Environment Variable Secret
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)env:[\s\S]*?-\s*name:\s*(?:PASSWORD|SECRET|TOKEN|API_KEY|AWS_SECRET)[^\n]*\n\s*value:\s*["']?[^${"'\n]+["']?`
- Environment variables with secrets should use secretKeyRef
- Example: `value: "hardcoded-secret"`
- Remediation: Use `valueFrom.secretKeyRef` to reference secrets

### AWS Credentials in Kubernetes
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY):\s*(?:["'])?(?:AKIA[0-9A-Z]{16}|[A-Za-z0-9/+=]{40})(?:["'])?`
- AWS credentials should not be in Kubernetes manifests
- Example: `AWS_ACCESS_KEY_ID: AKIAIOSFODNN7EXAMPLE`
- Remediation: Use IAM roles for service accounts (IRSA)

---

## CloudFormation Secrets

### Hardcoded Password in CloudFormation
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:Password|MasterUserPassword|AdminPassword):\s*(?:["'])?[^!${}"\n]+(?:["'])?`
- Passwords should not be hardcoded in templates
- Example: `MasterUserPassword: "mysecret123"`
- Remediation: Use Secrets Manager dynamic reference

### Hardcoded Access Key in CloudFormation
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:AccessKeyId|SecretAccessKey):\s*(?:["'])?(?:AKIA[0-9A-Z]{16}|[A-Za-z0-9/+=]{40})(?:["'])?`
- AWS credentials should not be in templates
- Example: `AccessKeyId: AKIAIOSFODNN7EXAMPLE`
- Remediation: Use IAM roles instead of static credentials

### NoEcho Not Used for Sensitive Parameters
**Type**: regex
**Severity**: medium
**Pattern**: `(?i)Parameters:[\s\S]*?(?:Password|Secret|Token)[\w]*:[\s\S]*?Type:\s*String(?:(?!NoEcho:\s*true).)*Default:`
- Sensitive parameters should use NoEcho
- Example: Password parameter without NoEcho
- Remediation: Add `NoEcho: true` to sensitive parameters

### Hardcoded Database Credentials
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:MasterUsername|DBUser):\s*["'][^"']+["'][\s\S]*?(?:MasterUserPassword|DBPassword):\s*["'][^$!{"']+["']`
- Database credentials should use dynamic references
- Example: Hardcoded username and password pair
- Remediation: Use Secrets Manager: `{{resolve:secretsmanager:...}}`

---

## Helm Chart Secrets

### Hardcoded Secret in values.yaml
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:password|secret|token|apiKey|api_key):\s*["']?[A-Za-z0-9_@#$%^&*+=/-]{8,}["']?`
- Secrets should not be in values.yaml files
- Example: `password: "mypassword123"`
- Remediation: Use Helm secrets plugin, external-secrets, or Vault

### Hardcoded Credentials in Chart
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)\.Values\.(?:password|secret|token|apiKey)\s*\|\s*default\s*["'][^"']+["']`
- Default values for secrets expose them in templates
- Example: `.Values.password | default "changeme"`
- Remediation: Make secrets required without defaults

### Base64 Encoded Secret in Template
**Type**: regex
**Severity**: high
**Pattern**: `(?i)data:[\s\S]*?{{.*b64enc.*}}[\s\S]*?`
- Base64 encoding in templates may expose secrets
- Example: `{{ .Values.password | b64enc }}`
- Remediation: Use external secrets management

---

## GitHub Actions Secrets

### Hardcoded Token in Workflow
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:token|api[_-]?key|password|secret):\s*["'][A-Za-z0-9_-]{20,}["']`
- Tokens should be stored as GitHub secrets
- Example: `token: "ghp_xxxxxxxxxxxxxxxxxxxx"`
- Remediation: Use `${{ secrets.TOKEN_NAME }}`

### Hardcoded AWS Credentials in Action
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:aws-access-key-id|aws-secret-access-key):\s*["']?(?:AKIA[0-9A-Z]{16}|[A-Za-z0-9/+=]{40})["']?`
- AWS credentials should be in GitHub secrets
- Example: `aws-access-key-id: AKIAIOSFODNN7EXAMPLE`
- Remediation: Use OIDC federation or secrets reference

### Hardcoded npm Token
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:NPM_TOKEN|NODE_AUTH_TOKEN):\s*["']?npm_[A-Za-z0-9]{36}["']?`
- npm tokens should be GitHub secrets
- Example: `NPM_TOKEN: npm_xxxxxxxxxxxx`
- Remediation: Store in secrets: `${{ secrets.NPM_TOKEN }}`

### Hardcoded Docker Hub Credentials
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:docker_password|dockerhub_token):\s*["'][^${"'\n]+["']`
- Docker credentials should be secrets
- Example: `docker_password: "mypassword"`
- Remediation: Use `${{ secrets.DOCKER_PASSWORD }}`

---

## Ansible Secrets

### Hardcoded Password in Playbook
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:ansible_password|ansible_become_pass|password):\s*["']?[^"'${}]{8,}["']?`
- Passwords should use Ansible Vault
- Example: `ansible_password: "secret123"`
- Remediation: Use ansible-vault encrypt_string

### Hardcoded Private Key in Ansible
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)ansible_ssh_private_key_file:\s*["'][^"']+["'][\s\S]*?-----BEGIN`
- Private keys should not be embedded
- Example: Inline private key content
- Remediation: Reference external key file

---

## Generic IaC Secrets

### Private Key Block in IaC
**Type**: regex
**Severity**: critical
**Pattern**: `-----BEGIN\s*(?:RSA|DSA|EC|OPENSSH)?\s*PRIVATE KEY-----`
- Private keys should never be in IaC files
- Example: RSA private key block
- Remediation: Use secrets manager or external key references

### JWT Token in IaC
**Type**: regex
**Severity**: critical
**Pattern**: `(?i)(?:jwt|bearer_token|auth_token)\s*[:=]\s*["']?eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+["']?`
- JWT tokens should not be hardcoded
- Example: `jwt: "eyJhbGciOiJIUzI1NiIs..."`
- Remediation: Use dynamic token generation or secrets manager

### Generic High Entropy Secret
**Type**: regex
**Severity**: high
**Pattern**: `(?i)(?:secret|key|token|password|credential|auth)\s*[:=]\s*["'][A-Za-z0-9+/=_-]{32,}["']`
- High-entropy strings in sensitive fields may be secrets
- Example: `secret: "aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5z"`
- Remediation: Move to secrets management system

---

## Detection Confidence

**Regex Detection**: 90%
**Context-aware Detection**: 85%

---

## Integration Notes

### Scanner Integration
- These patterns should be run on IaC file types: `.tf`, `.yaml`, `.yml`, `.json`, `.j2`
- Results should be merged with code-security secrets findings
- Findings should include IaC file type context for remediation

### False Positive Reduction
- Exclude example/template files
- Exclude files matching `*.example.*`, `*.sample.*`, `*.template.*`
- Check for variable references `${var.}`, `{{ .Values. }}`, `!Ref`
- Skip placeholder values like `CHANGE_ME`, `TODO`, `xxx`

---

## References

- CIS Benchmark for Cloud Providers
- HashiCorp Terraform Security Best Practices
- Kubernetes Security Best Practices
- AWS Well-Architected Framework - Security Pillar
