---
name: Security and Compliance
description: This skill should be used when the user asks to "security scan", "vulnerability assessment", "secrets management", "secure configuration", "OWASP", "security audit", "penetration testing", "security hardening", "secure coding", "dependency scanning", or needs help with application security, infrastructure security, or security best practices.
version: 1.0.0
---

# Security and Compliance

Comprehensive guidance for implementing security controls, vulnerability management, and secure coding practices.

## Security Scanning

### Static Application Security Testing (SAST)

```yaml
# GitHub Actions - CodeQL
- name: Initialize CodeQL
  uses: github/codeql-action/init@v3
  with:
    languages: javascript, python

- name: Autobuild
  uses: github/codeql-action/autobuild@v3

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v3
```

```bash
# Semgrep
semgrep scan --config=auto --json > results.json

# Bandit (Python)
bandit -r src/ -f json -o bandit-report.json

# ESLint Security Plugin (JavaScript)
npm install eslint-plugin-security
eslint --ext .js,.jsx src/
```

### Dependency Scanning

```bash
# npm audit
npm audit --json > npm-audit.json
npm audit fix

# Snyk
snyk test --json > snyk-report.json
snyk monitor

# OWASP Dependency-Check
dependency-check --project MyApp --scan ./src --format JSON

# Trivy (containers)
trivy image myapp:latest --format json --output trivy-report.json
```

### Container Security

```bash
# Trivy scan
trivy image --severity HIGH,CRITICAL myapp:latest

# Grype
grype myapp:latest

# Docker Scout
docker scout cves myapp:latest
```

### Infrastructure Security

```bash
# Checkov (IaC scanning)
checkov -d terraform/ --output json > checkov-report.json

# tfsec
tfsec . --format json > tfsec-report.json

# kube-bench (Kubernetes)
kube-bench run --targets=node,master
```

## Secrets Management

### HashiCorp Vault

```bash
# Store secret
vault kv put secret/myapp/database \
  username=admin \
  password=supersecret

# Retrieve secret
vault kv get -field=password secret/myapp/database
```

```python
# Python integration
import hvac

client = hvac.Client(url='http://vault:8200', token=os.environ['VAULT_TOKEN'])
secret = client.secrets.kv.v2.read_secret_version(path='myapp/database')
password = secret['data']['data']['password']
```

### AWS Secrets Manager

```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
db_creds = get_secret('prod/database')
```

### Environment Variables Security

```bash
# Never commit secrets
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Use secret scanning
git secrets --install
git secrets --register-aws
```

## OWASP Top 10 Mitigations

### 1. Injection Prevention

```python
# SQL Injection - Use parameterized queries
# Bad
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Good
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

```javascript
// Command Injection Prevention
// Bad
exec(`ls ${userInput}`);

// Good
const { execFile } = require('child_process');
execFile('ls', [sanitizedPath]);
```

### 2. Broken Authentication

```python
# Secure password hashing
from argon2 import PasswordHasher

ph = PasswordHasher()
hashed = ph.hash(password)
ph.verify(hashed, password)

# Rate limiting
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    pass
```

### 3. Cross-Site Scripting (XSS)

```javascript
// Content Security Policy
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'strict-dynamic'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
  }
}));

// Output encoding
const escapeHtml = (text) => {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
};
```

### 4. Insecure Direct Object References

```python
# Always verify authorization
@app.route('/documents/<doc_id>')
@login_required
def get_document(doc_id):
    document = Document.query.get_or_404(doc_id)

    # Verify ownership
    if document.owner_id != current_user.id:
        abort(403)

    return document.to_dict()
```

### 5. Security Misconfiguration

```yaml
# Secure HTTP headers
server:
  headers:
    X-Frame-Options: DENY
    X-Content-Type-Options: nosniff
    X-XSS-Protection: "1; mode=block"
    Strict-Transport-Security: "max-age=31536000; includeSubDomains"
    Content-Security-Policy: "default-src 'self'"
```

## Secure Configuration

### TLS/SSL Configuration

```nginx
# Nginx TLS config
server {
    listen 443 ssl http2;

    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
}
```

### Database Security

```sql
-- Create least-privilege user
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE ON app_tables TO app_user;
REVOKE DELETE ON sensitive_tables FROM app_user;

-- Enable row-level security
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_documents ON documents
  FOR ALL TO app_user
  USING (owner_id = current_user_id());
```

### Kubernetes Security

```yaml
# Pod Security Context
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    resources:
      limits:
        cpu: "1"
        memory: "512Mi"
```

```yaml
# Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```

## Security Monitoring

### Security Events to Monitor

| Event | Priority | Action |
|-------|----------|--------|
| Multiple failed logins | High | Alert, temp block |
| Privilege escalation | Critical | Alert, investigate |
| Unusual data access | High | Log, review |
| Configuration changes | Medium | Audit log |
| New admin accounts | High | Verify, alert |

### Security Alerting

```yaml
# Prometheus alert rules
groups:
  - name: security
    rules:
      - alert: HighFailedLoginRate
        expr: rate(auth_failures_total[5m]) > 10
        for: 2m
        labels:
          severity: high
        annotations:
          summary: High rate of authentication failures

      - alert: SuspiciousAPIAccess
        expr: rate(api_requests_total{path=~"/admin.*"}[5m]) > 100
        for: 1m
        labels:
          severity: critical
```

## Security Checklist

### Application Security

- [ ] Input validation on all user inputs
- [ ] Output encoding for all dynamic content
- [ ] Parameterized queries for database access
- [ ] Secure password hashing (Argon2, bcrypt)
- [ ] Rate limiting on authentication endpoints
- [ ] CSRF protection on state-changing requests
- [ ] Secure session management
- [ ] Content Security Policy headers

### Infrastructure Security

- [ ] TLS 1.2+ only
- [ ] Secrets in vault, not code
- [ ] Principle of least privilege
- [ ] Network segmentation
- [ ] Regular security patches
- [ ] Intrusion detection
- [ ] Security logging and monitoring
- [ ] Regular backups (tested)

## Additional Resources

### Reference Files

- **`references/owasp-cheatsheets.md`** - OWASP prevention guides
- **`references/security-headers.md`** - HTTP security headers reference

### Example Files

- **`examples/security-scan-pipeline.yml`** - CI security scanning workflow
- **`examples/vault-config.hcl`** - HashiCorp Vault configuration
