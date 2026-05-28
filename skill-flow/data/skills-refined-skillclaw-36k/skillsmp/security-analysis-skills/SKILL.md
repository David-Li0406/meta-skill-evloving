---
name: security-analysis-skills
description: Comprehensive security analysis framework teaching STRIDE threat modeling, OWASP Top 10 vulnerabilities, CVSS risk scoring, and secure coding patterns. Use when conducting security assessments, code reviews, threat modeling, or implementing security controls. Applicable to all development work requiring security consideration.
license: MIT
---

# Security Analysis Skills

**Purpose**: Universal security knowledge framework for threat modeling, vulnerability assessment, risk scoring, and secure coding. Designed to be applied by ALL development agents (security-agent, developer-agent, devops-agent, rust-expert, python-ml-expert) to ensure security-first development practices.

**Created**: 2025-11-08

---

## When to Use Security Analysis Skills

**✅ Use this skill when:**
- Conducting threat modeling for new features/systems
- Performing security code review
- Assessing vulnerabilities and scoring risk
- Implementing authentication/authorization
- Handling sensitive data (PII, credentials, payment info)
- Deploying to production (security checklist)
- Investigating security incidents
- Designing secure architectures

**❌ NOT required for:**
- Pure documentation tasks with no code
- Read-only data analysis with public data
- Internal tools with no network exposure (but still recommended)

**Target Audience**: Security specialists AND general developers integrating security into daily work

---

## Core Security Frameworks

### 1. STRIDE Threat Modeling

**Purpose**: Systematic identification of threats by category

**STRIDE Categories**:

1. **S - Spoofing Identity**
   - Definition: Attacker pretends to be someone else
   - Examples: Stolen credentials, session hijacking, JWT forgery
   - Mitigations: MFA, certificate pinning, signed tokens

2. **T - Tampering with Data**
   - Definition: Unauthorized modification of data
   - Examples: Man-in-the-middle, SQL injection, XSS
   - Mitigations: HTTPS/TLS, input validation, integrity checks (HMAC)

3. **R - Repudiation**
   - Definition: User denies performing an action
   - Examples: Missing audit logs, unsigned transactions
   - Mitigations: Audit logging, digital signatures, timestamps

4. **I - Information Disclosure**
   - Definition: Exposure of confidential information
   - Examples: Directory traversal, verbose errors, unencrypted data
   - Mitigations: Encryption at rest/transit, least privilege, sanitized errors

5. **D - Denial of Service**
   - Definition: Service becomes unavailable
   - Examples: Resource exhaustion, infinite loops, DDoS attacks
   - Mitigations: Rate limiting, resource quotas, circuit breakers

6. **E - Elevation of Privilege**
   - Definition: Unauthorized permission escalation
   - Examples: Privilege escalation bugs, insecure defaults
   - Mitigations: Principle of least privilege, role-based access control

**How to Apply STRIDE**:
1. For each component/feature, ask: "What STRIDE threats apply?"
2. Fill out threat modeling worksheet (see reference section)
3. Prioritize threats by impact × likelihood
4. Document mitigations for each identified threat

---

### 2. OWASP Top 10 (2021 Edition)

**Purpose**: Most critical web application security risks

#### A01: Broken Access Control

**Description**: Users can act outside their intended permissions

**Examples**:
- Direct object references: `/user/1234/profile` → change to `/user/5678/profile`
- Missing function-level access control: Regular user accesses `/admin/delete`
- IDOR (Insecure Direct Object Reference): Manipulating IDs in URLs/APIs

**Secure Patterns**:
```python
# ❌ VULNERABLE: No ownership check
@app.route('/document/<doc_id>')
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return render_template('doc.html', doc=doc)

# ✅ SECURE: Verify ownership
@app.route('/document/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    if not doc or doc.owner_id != current_user.id:
        abort(403)  # Forbidden
    return render_template('doc.html', doc=doc)
```

**Checklist**:
- [ ] All endpoints verify user permissions
- [ ] Object ownership validated before access
- [ ] Default deny (whitelist not blacklist)
- [ ] Disable directory listing
- [ ] Invalidate sessions on logout

---

#### A02: Cryptographic Failures

**Description**: Sensitive data exposed due to weak/missing encryption

**Examples**:
- Storing passwords in plaintext
- Using weak algorithms (MD5, SHA1 for passwords)
- Transmitting sensitive data over HTTP
- Hardcoded encryption keys

**Secure Patterns**:
```python
# ❌ VULNERABLE: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ SECURE: Proper password hashing
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ❌ VULNERABLE: Hardcoded key
AES_KEY = "mysecretkey12345"

# ✅ SECURE: Environment variable
import os
AES_KEY = os.environ['AES_ENCRYPTION_KEY']
```

**Checklist**:
- [ ] Use TLS 1.2+ for all data in transit
- [ ] Hash passwords with bcrypt/Argon2 (not MD5/SHA1)
- [ ] Never hardcode secrets (use env vars/vaults)
- [ ] Encrypt sensitive data at rest
- [ ] Use strong key generation (crypto.randomBytes, secrets module)

---

#### A03: Injection

**Description**: Untrusted data sent to interpreter as command/query

**Types**: SQL Injection, NoSQL Injection, Command Injection, LDAP Injection, XPath Injection

**SQL Injection Example**:
```python
# ❌ VULNERABLE: String concatenation
username = request.form['username']
query = f"SELECT * FROM users WHERE username = '{username}'"
# Attacker inputs: ' OR '1'='1' --
# Result: SELECT * FROM users WHERE username = '' OR '1'='1' --'

# ✅ SECURE: Parameterized query
username = request.form['username']
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**Command Injection Example**:
```python
# ❌ VULNERABLE: Shell injection
filename = request.form['filename']
os.system(f"cat {filename}")  # Attacker: "; rm -rf /"

# ✅ SECURE: Avoid shell, use safe APIs
import subprocess
subprocess.run(['cat', filename], check=True, capture_output=True)
```

**Checklist**:
- [ ] Use parameterized queries (prepared statements)
- [ ] Avoid dynamic query construction with string concat
- [ ] Validate input against whitelist (not blacklist)
- [ ] Escape special characters for context
- [ ] Use ORM frameworks (with parameterization)

---

#### A04: Insecure Design

**Description**: Missing or ineffective security controls in design phase

**Examples**:
- No rate limiting on login (brute force)
- Password reset without identity verification
- Predictable session IDs
- No transaction verification (CSRF)

**Secure Design Patterns**:
- Defense in depth (multiple security layers)
- Principle of least privilege
- Fail securely (default deny)
- Separation of duties
- Security by default (opt-in for risky features)

**Checklist**:
- [ ] Threat model created during design
- [ ] Rate limiting on authentication/sensitive endpoints
- [ ] CSRF tokens for state-changing operations
- [ ] Cryptographically secure random IDs (not sequential)
- [ ] Security requirements defined before coding

---

#### A05: Security Misconfiguration

**Description**: Insecure default configurations, incomplete setups, exposed admin interfaces

**Examples**:
- Default admin credentials (admin/admin)
- Verbose error messages revealing stack traces
- Unnecessary features enabled (debug mode in production)
- Missing security headers
- Outdated software versions

**Secure Configuration**:
```python
# ❌ VULNERABLE: Debug mode in production
app = Flask(__name__)
app.config['DEBUG'] = True  # Exposes code, allows RCE

# ✅ SECURE: Environment-based config
import os
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

# ✅ SECURE: Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

**Checklist**:
- [ ] Change all default credentials
- [ ] Disable debug mode in production
- [ ] Remove unnecessary features/services
- [ ] Configure security headers (CSP, HSTS, X-Frame-Options)
- [ ] Regular security updates applied

---

#### A06: Vulnerable and Outdated Components

**Description**: Using libraries/frameworks with known vulnerabilities

**Examples**:
- Unmaintained dependencies (no security patches)
- Using deprecated crypto libraries
- Outdated frameworks (old Rails, Django, Spring)

**Secure Practices**:
```bash
# Check for vulnerabilities
npm audit          # Node.js
pip-audit          # Python
bundle audit       # Ruby
cargo audit        # Rust

# Update dependencies
npm update
pip install --upgrade -r requirements.txt
cargo update
```

**Checklist**:
- [ ] Dependency scanning in CI/CD
- [ ] Regular updates (monthly for deps, immediate for critical CVEs)
- [ ] Remove unused dependencies
- [ ] Pin versions (avoid wildcards like *)
- [ ] Monitor CVE databases (NVD, GitHub Security Advisories)

---

#### A07: Identification and Authentication Failures

**Description**: Weak authentication allows attackers to compromise accounts

**Examples**:
- Weak password policy (no complexity requirements)
- Session fixation
- Missing MFA
- Predictable session tokens
- No account lockout on brute force

**Secure Authentication**:
```python
# Password Policy
MIN_LENGTH = 12
REQUIRE_UPPERCASE = True
REQUIRE_DIGIT = True
REQUIRE_SPECIAL = True

# Session Management
from secrets import token_urlsafe
session_id = token_urlsafe(32)  # Cryptographically secure

# Rate Limiting
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["5 per minute"])

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic with rate limiting
    pass
```

**Checklist**:
- [ ] Strong password policy enforced
- [ ] MFA available (TOTP, WebAuthn)
- [ ] Account lockout after N failed attempts
- [ ] Session timeout configured
- [ ] Secure session cookie flags (HttpOnly, Secure, SameSite)

---

#### A08: Software and Data Integrity Failures

**Description**: Code/infrastructure relies on untrusted sources without integrity verification

**Examples**:
- Downloading dependencies without checksum verification
- Auto-update without signature validation
- Insecure CI/CD pipeline
- Deserialization of untrusted data

**Secure Practices**:
```python
# ❌ VULNERABLE: Deserialize untrusted data
import pickle
data = pickle.loads(request.data)  # RCE risk!

# ✅ SECURE: Use safe serialization
import json
data = json.loads(request.data)  # Only deserializes JSON primitives

# Verify package integrity
pip install --require-hashes -r requirements.txt
```

**Checklist**:
- [ ] Use signed commits (GPG)
- [ ] Verify package checksums/signatures
- [ ] Secure CI/CD pipeline (no secrets in logs)
- [ ] Avoid insecure deserialization (pickle, YAML.unsafe_load)
- [ ] Implement software bill of materials (SBOM)

---

#### A09: Security Logging and Monitoring Failures

**Description**: Insufficient logging prevents detection of breaches

**Examples**:
- No logging of authentication events
- Logs not reviewed/alerted
- Sensitive data in logs (passwords, tokens)
- No integrity protection (logs can be tampered)

**Secure Logging**:
```python
import logging
import hashlib

# ✅ SECURE: Log security events
logger = logging.getLogger('security')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if authenticate(username, password):
        logger.info(f"Successful login: user={username}, ip={request.remote_addr}")
        return "Success"
    else:
        logger.warning(f"Failed login: user={username}, ip={request.remote_addr}")
        return "Invalid credentials", 401

# ❌ VULNERABLE: Log sensitive data
logger.info(f"User {username} logged in with password {password}")  # DON'T!

# ✅ SECURE: Redact sensitive data
logger.info(f"User {username} logged in")
```

**Checklist**:
- [ ] Log all authentication events (success/failure)
- [ ] Log authorization failures
- [ ] Log input validation failures
- [ ] Never log passwords, tokens, PII
- [ ] Centralized logging with alerting
- [ ] Tamper-evident logs (write-once storage)

---

#### A10: Server-Side Request Forgery (SSRF)

**Description**: Web app fetches remote resource without validating user-supplied URL

**Examples**:
- Fetching arbitrary URLs from user input
- Accessing internal services (localhost, 169.254.169.254)
- Port scanning via web app

**SSRF Example**:
```python
# ❌ VULNERABLE: Fetch arbitrary URL
import requests
url = request.args.get('url')
response = requests.get(url)  # Attacker: http://localhost:6379/

# ✅ SECURE: Whitelist domains
ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']
from urllib.parse import urlparse

url = request.args.get('url')
parsed = urlparse(url)
if parsed.hostname not in ALLOWED_DOMAINS:
    abort(400, "Invalid domain")
response = requests.get(url)
```

**Checklist**:
- [ ] Whitelist allowed domains/IPs
- [ ] Block private IP ranges (10.0.0.0/8, 192.168.0.0/16, 127.0.0.1)
- [ ] Disable URL redirects or validate redirect targets
- [ ] Use network segmentation (no internet access from app servers)

---

### 3. Risk Scoring (CVSS v3.1)

**Purpose**: Quantify vulnerability severity for prioritization

**CVSS Formula**: Base Score (0-10) = f(Impact, Exploitability)

**Severity Levels**:
- **Critical (9.0-10.0)**: Immediate action required, exploit in the wild
- **High (7.0-8.9)**: High priority, exploitable remotely
- **Medium (4.0-6.9)**: Medium priority, requires user interaction
- **Low (0.1-3.9)**: Low priority, limited impact

**Impact Scoring**:
- Confidentiality Impact: None / Low / High
- Integrity Impact: None / Low / High
- Availability Impact: None / Low / High

**Exploitability Scoring**:
- Attack Vector: Network (highest) / Adjacent / Local / Physical (lowest)
- Attack Complexity: Low (easy) / High (difficult)
- Privileges Required: None (highest) / Low / High (lowest)
- User Interaction: None (highest) / Required (lower)

**Quick Risk Matrix** (Impact × Likelihood):

| Impact / Likelihood | Low | Medium | High |
|---------------------|-----|--------|------|
| **High**            | Med | High   | Crit |
| **Medium**          | Low | Med    | High |
| **Low**             | Low | Low    | Med  |

**Example Scoring**:
```
Vulnerability: SQL Injection in login endpoint

CVSS Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
- Attack Vector: Network (AV:N) - remotely exploitable
- Attack Complexity: Low (AC:L) - easy to exploit
- Privileges Required: None (PR:N) - unauthenticated
- User Interaction: None (UI:N) - no user action needed
- Confidentiality: High (C:H) - all user data exposed
- Integrity: High (I:H) - data can be modified
- Availability: None (A:N) - no DoS

Base Score: 9.1 (CRITICAL)
```

**Checklist**:
- [ ] Score all identified vulnerabilities using CVSS
- [ ] Prioritize remediation: Critical → High → Medium → Low
- [ ] Define risk acceptance criteria (e.g., no Critical in production)
- [ ] Track vulnerabilities in registry (Jira, GitHub Security)

---

### 4. Security Code Review Patterns

**Purpose**: Identify common vulnerabilities during code review

#### Input Validation

**Rule**: Never trust user input

**Patterns**:
```python
# Whitelist validation (preferred)
ALLOWED_EXTENSIONS = {'.jpg', '.png', '.pdf'}
file_ext = os.path.splitext(filename)[1].lower()
if file_ext not in ALLOWED_EXTENSIONS:
    raise ValueError("Invalid file type")

# Regex validation
import re
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
if not EMAIL_PATTERN.match(email):
    raise ValueError("Invalid email")

# Type validation
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    age: int
    email: str

    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Invalid age')
        return v
```

---

#### Authentication & Authorization

**Rule**: Verify identity and permissions at every access point

**Patterns**:
```python
# Decorator-based authorization
from functools import wraps

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_role(role):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin/users')
@require_role('admin')
def list_users():
    return render_template('users.html', users=User.query.all())

# Resource ownership check
def check_ownership(resource, user):
    if resource.owner_id != user.id and not user.is_admin():
        abort(403, "Not authorized to access this resource")
```

---

#### Cryptography Best Practices

**Rules**:
1. Don't roll your own crypto
2. Use standard libraries (cryptography, libsodium)
3. Use authenticated encryption (AES-GCM, ChaCha20-Poly1305)

**Patterns**:
```python
# ✅ SECURE: Modern authenticated encryption
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = os.urandom(12)  # 96-bit nonce
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

# ✅ SECURE: Password hashing
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# ✅ SECURE: Secure random token
import secrets
token = secrets.token_urlsafe(32)
```

---

#### Secrets Management

**Rule**: Never hardcode secrets

**Patterns**:
```python
# ❌ VULNERABLE
API_KEY = "sk_live_abc123xyz789"

# ✅ SECURE: Environment variables
import os
API_KEY = os.environ['API_KEY']

# ✅ SECURE: Secrets manager (AWS Secrets Manager)
import boto3
client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='prod/api-key')
API_KEY = response['SecretString']

# ✅ SECURE: Configuration file (gitignored)
import json
with open('/etc/secrets/config.json') as f:
    config = json.load(f)
    API_KEY = config['api_key']
```

**Checklist**:
- [ ] No secrets in source code
- [ ] No secrets in git history (use git-secrets)
- [ ] Secrets in environment variables or vault
- [ ] Rotate secrets regularly
- [ ] Use different secrets per environment (dev/staging/prod)

---

## STRIDE Threat Modeling Worksheet

**Use this template for every new feature/component**:

```markdown
## Threat Model: [Feature/Component Name]

**Description**: [Brief description of functionality]

**Date**: [YYYY-MM-DD]

**Reviewer**: [Your name]

---

### Components

List all components involved:
1. [Component 1: e.g., Login API endpoint]
2. [Component 2: e.g., User database]
3. [Component 3: e.g., Session store]

---

### Data Flow

Describe how data flows:
1. User submits credentials → Login API
2. Login API queries User DB
3. On success, create session in Session Store
4. Return session token to user

---

### Threats Identified

#### Spoofing
- [ ] **Threat**: Attacker uses stolen credentials
  - **Mitigation**: Implement MFA
  - **Priority**: High

#### Tampering
- [ ] **Threat**: Man-in-the-middle modifies login request
  - **Mitigation**: Enforce HTTPS/TLS 1.3
  - **Priority**: Critical

#### Repudiation
- [ ] **Threat**: User denies login action
  - **Mitigation**: Log all authentication events with timestamp
  - **Priority**: Medium

#### Information Disclosure
- [ ] **Threat**: Verbose error reveals username existence
  - **Mitigation**: Generic error message "Invalid credentials"
  - **Priority**: Medium

#### Denial of Service
- [ ] **Threat**: Brute force attack exhausts server resources
  - **Mitigation**: Rate limiting (5 attempts/minute)
  - **Priority**: High

#### Elevation of Privilege
- [ ] **Threat**: Session fixation allows privilege escalation
  - **Mitigation**: Regenerate session ID on login
  - **Priority**: High

---

### Risk Summary

Total threats identified: [N]
- Critical: [N]
- High: [N]
- Medium: [N]
- Low: [N]

**Overall Risk Level**: [Critical/High/Medium/Low]
```

---

## Security Checklist (Pre-Deployment)

**Use this before deploying any code to production**:

### Authentication & Authorization
- [ ] Strong password policy enforced (12+ chars, complexity)
- [ ] MFA available for sensitive accounts
- [ ] Session timeout configured (15-30 minutes)
- [ ] Secure session cookies (HttpOnly, Secure, SameSite)
- [ ] Authorization checks on all endpoints
- [ ] Default deny (whitelist approach)

### Input Validation
- [ ] All user input validated (whitelist preferred)
- [ ] Parameterized queries used (no string concatenation)
- [ ] File upload restrictions (type, size, content)
- [ ] Output encoding for XSS prevention

### Cryptography
- [ ] TLS 1.2+ enforced for all connections
- [ ] Passwords hashed with bcrypt/Argon2
- [ ] No hardcoded secrets
- [ ] Secrets in environment variables or vault
- [ ] Secure random generators used (secrets module)

### Error Handling
- [ ] Generic error messages (no stack traces)
- [ ] Errors logged with context (user, IP, timestamp)
- [ ] No sensitive data in logs

### Security Headers
- [ ] Content-Security-Policy configured
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY or SAMEORIGIN
- [ ] Strict-Transport-Security (HSTS)
- [ ] X-XSS-Protection: 1; mode=block

### Logging & Monitoring
- [ ] Authentication events logged
- [ ] Authorization failures logged
- [ ] Security alerts configured
- [ ] Log retention policy defined

### Dependencies
- [ ] No known vulnerabilities (npm audit, pip-audit)
- [ ] Dependencies up to date
- [ ] Unused dependencies removed
- [ ] CI/CD includes security scanning

### Infrastructure
- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Unnecessary services disabled
- [ ] Network segmentation implemented
- [ ] Rate limiting configured

---

## Reference Materials

**Detailed Guides**:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- STRIDE Methodology: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- CVSS Calculator: https://www.first.org/cvss/calculator/3.1
- CWE Database: https://cwe.mitre.org/

**Secure Coding Guides**:
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- NIST Secure Software Development Framework: https://csrc.nist.gov/projects/ssdf

**Tools**:
- Static Analysis: Bandit (Python), ESLint (JS), cargo-audit (Rust)
- Dependency Scanning: Snyk, Dependabot, npm audit
- Dynamic Analysis: OWASP ZAP, Burp Suite

---

## Self-Assessment

After applying security analysis, verify:

- [ ] **STRIDE Coverage**: All 6 threat categories considered for this component
- [ ] **OWASP Awareness**: Top 10 vulnerabilities reviewed and mitigated
- [ ] **Risk Scoring**: Vulnerabilities scored and prioritized
- [ ] **Secure Patterns**: Code review patterns applied
- [ ] **Checklist Completion**: Pre-deployment checklist 100% complete
- [ ] **Documentation**: Threat model and mitigations documented
- [ ] **Testing**: Security tests written (auth bypass, injection, etc.)

**Confidence Level**:
- **High (90%+)**: All frameworks applied, threat model complete, security tests passing
- **Medium (70-89%)**: Main threats addressed, some edge cases remain
- **Low (<70%)**: Significant security gaps identified - continue working

---

## Summary

Security Analysis Skills provide systematic frameworks for integrating security into all development work:

1. **STRIDE Threat Modeling**: Identify threats by category (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege)
2. **OWASP Top 10**: Address most critical web vulnerabilities
3. **CVSS Risk Scoring**: Quantify and prioritize vulnerability remediation
4. **Secure Coding Patterns**: Apply proven security patterns in code review

**Remember**: Security is not a feature, it's a requirement. Apply these frameworks proactively during design and development, not reactively after incidents.

**Target**: Zero Critical/High vulnerabilities in production deployments.
