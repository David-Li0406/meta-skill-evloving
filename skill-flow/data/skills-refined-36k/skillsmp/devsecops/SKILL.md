---
name: devsecops
description: DevSecOps skill for security automation, vulnerability management, secure CI/CD pipelines, container security, secrets management, compliance, and security testing. Use when implementing security in development workflows, scanning for vulnerabilities, securing infrastructure, or when user mentions security automation, SAST, DAST, container scanning, or compliance.
---

# DevSecOps

A comprehensive DevSecOps skill that helps integrate security practices throughout the software development lifecycle, from code to production.

## Quick Start

Basic DevSecOps workflow:

```
# Shift security left
# Automate security checks in CI/CD
# Scan code, dependencies, containers, infrastructure
# Monitor and respond to security incidents
# Maintain compliance and audit trails
```

## Core Capabilities

### 1. Security Scanning

**Static Application Security Testing (SAST)**
- Code analysis for security vulnerabilities
- Pattern detection for common flaws (SQL injection, XSS, etc.)
- Security code review automation
- Tools: SonarQube, Checkmarx, Semgrep, CodeQL

**Dynamic Application Security Testing (DAST)**
- Runtime security testing
- API security testing
- Penetration testing automation
- Tools: OWASP ZAP, Burp Suite, Acunetix

**Software Composition Analysis (SCA)**
- Dependency vulnerability scanning
- License compliance checking
- Open source security
- Tools: Snyk, Dependabot, WhiteSource, Black Duck

### 2. Container Security

**Image Scanning**
- Vulnerability scanning for base images
- Malware detection
- Configuration analysis
- Tools: Trivy, Clair, Anchore, Aqua Security

**Runtime Security**
- Container behavior monitoring
- Anomaly detection
- Runtime policy enforcement
- Tools: Falco, Sysdig, Aqua, Twistlock

**Kubernetes Security**
- Pod security policies
- Network policies
- RBAC configuration
- Admission controllers
- Tools: OPA, Kyverno, Falco, KubeSec

### 3. Infrastructure Security

**Infrastructure as Code (IaC) Scanning**
- Terraform security analysis
- CloudFormation scanning
- Kubernetes manifests validation
- Tools: Checkov, tfsec, Terrascan, kube-score

**Cloud Security Posture Management (CSPM)**
- AWS/Azure/GCP security configuration
- Compliance monitoring
- Misconfiguration detection
- Tools: AWS Security Hub, Azure Security Center, Prowler

**Network Security**
- Firewall rules analysis
- Network segmentation
- Traffic monitoring
- Security groups validation

### 4. Secrets Management

**Secret Scanning**
- Detect hardcoded credentials in code
- Git history scanning
- Configuration file analysis
- Tools: GitGuardian, TruffleHog, git-secrets, Gitleaks

**Secret Storage & Rotation**
- Centralized secret management
- Automated rotation
- Access control and auditing
- Tools: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault

### 5. CI/CD Pipeline Security

**Pipeline Hardening**
- Secure pipeline configuration
- Build environment isolation
- Artifact signing and verification
- Supply chain security

**Security Gates**
- Automated security checks in pipeline
- Quality gates based on severity
- Break the build on critical issues
- Exception management

**Compliance Automation**
- SOC 2, HIPAA, PCI-DSS checks
- Policy as code
- Automated evidence collection
- Audit trail generation

### 6. Application Security

**API Security**
- API authentication and authorization
- Rate limiting and throttling
- Input validation
- API gateway security

**Authentication & Authorization**
- OAuth2/OIDC implementation
- JWT validation
- RBAC and ABAC
- Multi-factor authentication

**Data Security**
- Encryption at rest and in transit
- Data masking and anonymization
- Key management
- PII/PHI protection

### 7. Monitoring & Incident Response

**Security Monitoring**
- SIEM integration
- Log aggregation and analysis
- Threat detection
- Tools: ELK Stack, Splunk, Datadog Security

**Vulnerability Management**
- CVE tracking and prioritization
- Patch management
- Vulnerability disclosure
- SLA management

**Incident Response**
- Security incident playbooks
- Automated remediation
- Post-incident analysis
- Lessons learned documentation

### 8. Compliance & Governance

**Compliance Frameworks**
- SOC 2 Type II
- ISO 27001
- HIPAA
- PCI-DSS
- GDPR

**Policy Management**
- Security policies as code
- Policy enforcement
- Exception tracking
- Regular audits

**Risk Assessment**
- Threat modeling
- Risk scoring
- Attack surface analysis
- Security metrics and KPIs

## Workflows

### Secure SDLC Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    SECURE SDLC                          │
└─────────────────────────────────────────────────────────┘

1. PLAN & DESIGN
   ├── Threat modeling
   ├── Security requirements
   └── Architecture security review

2. DEVELOP
   ├── Secure coding guidelines
   ├── IDE security plugins
   ├── Pre-commit hooks (secret scanning)
   └── Security-focused code reviews

3. BUILD
   ├── SAST (static code analysis)
   ├── SCA (dependency scanning)
   ├── Container image scanning
   └── IaC security scanning

4. TEST
   ├── DAST (dynamic testing)
   ├── API security testing
   ├── Penetration testing
   └── Security regression testing

5. DEPLOY
   ├── Container runtime security
   ├── Infrastructure security validation
   ├── Secrets injection
   └── Security configuration checks

6. OPERATE
   ├── Runtime monitoring
   ├── Vulnerability management
   ├── Incident response
   └── Compliance monitoring

7. MONITOR
   ├── Security logging
   ├── Threat detection
   ├── Anomaly detection
   └── Security metrics
```

### CI/CD Security Pipeline

```yaml
# Example: Security-Integrated Pipeline

stages:
  - security-scan
  - build
  - test
  - security-test
  - deploy

# Stage 1: Pre-build Security
security-scan:
  stage: security-scan
  script:
    # Secret scanning
    - trufflehog --regex --entropy=False .
    # SAST scanning
    - semgrep --config=auto --sarif > sast-results.sarif
    # Dependency scanning
    - snyk test --severity-threshold=high
    # IaC scanning
    - checkov -d . --framework terraform
  artifacts:
    reports:
      sast: sast-results.sarif

# Stage 2: Build with security
build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    # Sign container image
    - cosign sign myapp:$CI_COMMIT_SHA

# Stage 3: Container scanning
container-scan:
  stage: test
  script:
    - trivy image --severity HIGH,CRITICAL myapp:$CI_COMMIT_SHA
    - docker scan myapp:$CI_COMMIT_SHA
  allow_failure: false  # Break build on critical issues

# Stage 4: Dynamic security testing
dast:
  stage: security-test
  script:
    # Deploy to staging
    - kubectl apply -f k8s/staging/
    # Run DAST
    - zap-baseline.py -t https://staging.example.com
    # API security test
    - postman collection run security-tests.json

# Stage 5: Deploy with security
deploy:
  stage: deploy
  script:
    # Verify image signature
    - cosign verify myapp:$CI_COMMIT_SHA
    # Apply security policies
    - kubectl apply -f k8s/policies/
    # Deploy application
    - kubectl apply -f k8s/production/
    # Verify deployment security
    - kube-bench run --targets master,node
```

### Vulnerability Management Process

```
1. DISCOVERY
   └── Scan code, dependencies, containers, infrastructure
   
2. PRIORITIZATION
   ├── Severity assessment (CVSS score)
   ├── Exploitability analysis
   ├── Business impact evaluation
   └── Risk scoring
   
3. TRIAGE
   ├── Assign ownership
   ├── Set SLA based on severity
   ├── Create remediation tickets
   └── Track in vulnerability management system
   
4. REMEDIATION
   ├── Update dependencies
   ├── Apply patches
   ├── Implement workarounds
   └── Verify fixes
   
5. VALIDATION
   ├── Re-scan to confirm fix
   ├── Test for regressions
   └── Close vulnerability ticket
   
6. REPORTING
   ├── Update security dashboard
   ├── Notify stakeholders
   └── Document lessons learned
```

## Security Patterns

### Defense in Depth

```
Layer 1: Network Security
├── Firewall rules
├── Network segmentation
├── DDoS protection
└── WAF (Web Application Firewall)

Layer 2: Application Security
├── Input validation
├── Output encoding
├── Authentication & authorization
└── Session management

Layer 3: Data Security
├── Encryption at rest
├── Encryption in transit
├── Data masking
└── Access controls

Layer 4: Infrastructure Security
├── OS hardening
├── Patch management
├── Security configuration
└── Vulnerability scanning

Layer 5: Monitoring & Response
├── Security logging
├── SIEM
├── Incident response
└── Threat intelligence
```

### Zero Trust Architecture

```
1. VERIFY EXPLICITLY
   ├── Authenticate every request
   ├── Authorize based on all data points
   └── Use multi-factor authentication

2. LEAST PRIVILEGE ACCESS
   ├── Just-in-time access
   ├── Risk-based adaptive policies
   └── Data protection

3. ASSUME BREACH
   ├── Minimize blast radius
   ├── Segment access
   ├── End-to-end encryption
   └── Analytics for visibility
```

## Security by Technology Stack

### React/TypeScript

**Security Concerns:**
- XSS vulnerabilities
- Dependency vulnerabilities
- API security
- Authentication token storage

**Tools & Practices:**
```bash
# Dependency scanning
npm audit
snyk test

# SAST scanning
eslint --plugin security
semgrep --config=p/react

# Content Security Policy
# Add to HTML or headers
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
```

**Secure Coding:**
```typescript
// ✅ GOOD: Sanitize user input
import DOMPurify from 'dompurify';

const SafeComponent: React.FC<{html: string}> = ({html}) => {
  const sanitized = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{__html: sanitized}} />;
};

// ❌ BAD: Direct use of dangerouslySetInnerHTML
const UnsafeComponent = ({html}) => (
  <div dangerouslySetInnerHTML={{__html: html}} />
);

// ✅ GOOD: Secure token storage
// Store JWT in httpOnly cookie, not localStorage
// Use secure, sameSite=strict cookies

// ❌ BAD: Storing tokens in localStorage
localStorage.setItem('token', jwt);  // Vulnerable to XSS
```

### Python/FastAPI

**Security Concerns:**
- SQL injection
- Command injection
- Insecure deserialization
- Dependency vulnerabilities

**Tools & Practices:**
```bash
# Dependency scanning
safety check
pip-audit
snyk test --file=requirements.txt

# SAST scanning
bandit -r .
semgrep --config=p/python

# Secret scanning
detect-secrets scan
```

**Secure Coding:**
```python
# ✅ GOOD: Use parameterized queries
from sqlalchemy import text

def get_user(user_id: int):
    query = text("SELECT * FROM users WHERE id = :id")
    result = db.execute(query, {"id": user_id})
    return result.first()

# ❌ BAD: String concatenation (SQL injection)
def get_user_unsafe(user_id: str):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)

# ✅ GOOD: Input validation
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    email: str
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

# ✅ GOOD: Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/login")
@limiter.limit("5/minute")
async def login(credentials: LoginRequest):
    return await authenticate(credentials)
```

### Java/Spring Boot

**Security Concerns:**
- Deserialization vulnerabilities
- XXE (XML External Entity)
- LDAP injection
- Dependency vulnerabilities

**Tools & Practices:**
```bash
# Dependency scanning
mvn dependency-check:check
snyk test

# SAST scanning
spotbugs -effort:max -low
semgrep --config=p/java

# Container scanning
trivy image myapp:latest
```

**Secure Coding:**
```java
// ✅ GOOD: Use prepared statements
public User getUserById(int userId) {
    String sql = "SELECT * FROM users WHERE id = ?";
    return jdbcTemplate.queryForObject(sql, new Object[]{userId}, 
                                      new UserRowMapper());
}

// ❌ BAD: String concatenation
public User getUserByIdUnsafe(int userId) {
    String sql = "SELECT * FROM users WHERE id = " + userId;
    return jdbcTemplate.queryForObject(sql, new UserRowMapper());
}

// ✅ GOOD: Spring Security configuration
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
            .and()
            .authorizeRequests()
                .antMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            .and()
            .oauth2ResourceServer().jwt();
        return http.build();
    }
}

// ✅ GOOD: Secure password hashing
@Service
public class PasswordService {
    private final PasswordEncoder encoder = new BCryptPasswordEncoder(12);
    
    public String hashPassword(String plainPassword) {
        return encoder.encode(plainPassword);
    }
}
```

### Kubernetes/Docker

**Security Concerns:**
- Container breakout
- Privilege escalation
- Insecure configurations
- Supply chain attacks

**Tools & Practices:**
```bash
# Container scanning
trivy image nginx:latest
docker scan nginx:latest
grype nginx:latest

# K8s security scanning
kubesec scan pod.yaml
kube-bench
kube-hunter

# Policy enforcement
kubectl apply -f pod-security-policy.yaml
gatekeeper install
```

**Secure Configurations:**
```yaml
# ✅ GOOD: Secure Pod configuration
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      capabilities:
        drop:
          - ALL
    resources:
      limits:
        cpu: "1"
        memory: "512Mi"
      requests:
        cpu: "0.5"
        memory: "256Mi"
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080

# ✅ GOOD: Network Policy
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
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

## Security Tools Integration

### GitHub Actions Security Pipeline

```yaml
name: Security Pipeline

on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: TruffleHog Secret Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
      - name: Run CodeQL
        uses: github/codeql-action/analyze@v2

  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  iac-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: infrastructure/
          framework: terraform
          output_format: sarif
          output_file_path: checkov-results.sarif
```

### GitLab CI Security Pipeline

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/DAST.gitlab-ci.yml

variables:
  SECURE_LOG_LEVEL: "debug"

stages:
  - test
  - security
  - deploy

security-scan:
  stage: security
  image: securego/gosec:latest
  script:
    - gosec -fmt json -out gosec-report.json ./...
  artifacts:
    reports:
      sast: gosec-report.json

custom-container-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Compliance Frameworks

### SOC 2 Type II

**Key Controls:**
```
CC6.1: Logical and Physical Access Controls
├── Multi-factor authentication
├── Password policies
├── Access reviews (quarterly)
└── Privileged access management

CC6.2: System Monitoring
├── Security logging enabled
├── Log retention (1 year)
├── SIEM implementation
└── Anomaly detection

CC7.1: Threat Detection
├── Vulnerability scanning (weekly)
├── Penetration testing (annual)
├── Security awareness training
└── Incident response plan

CC7.2: Infrastructure Security
├── Network segmentation
├── Encryption at rest and in transit
├── Patch management
└── Configuration management
```

### PCI-DSS

**Requirements:**
```
Requirement 1: Firewall Configuration
├── Network diagram documentation
├── Firewall rule reviews (6 months)
└── DMZ implementation

Requirement 2: System Security
├── Change default passwords
├── Disable unnecessary services
└── Security configuration standards

Requirement 3: Protect Cardholder Data
├── Data encryption
├── Minimize data retention
└── Secure key management

Requirement 6: Secure Development
├── Security training for developers
├── SAST/DAST scanning
├── Code review process
└── Vulnerability management

Requirement 10: Logging and Monitoring
├── Audit trails
├── Log review
├── Time synchronization
└── Log protection

Requirement 11: Security Testing
├── Quarterly vulnerability scans
├── Annual penetration testing
├── IDS/IPS deployment
└── File integrity monitoring
```

## Security Metrics & KPIs

### Key Metrics to Track

```
1. VULNERABILITY METRICS
   ├── Mean Time to Detect (MTTD): < 24 hours
   ├── Mean Time to Remediate (MTTR): < 30 days (critical), < 90 days (high)
   ├── Vulnerability density: # of vulnerabilities per 1000 lines of code
   └── False positive rate: < 10%

2. SECURITY TESTING COVERAGE
   ├── Code coverage by SAST: > 80%
   ├── API endpoints covered by DAST: > 90%
   ├── Dependencies scanned: 100%
   └── Containers scanned: 100%

3. PIPELINE SECURITY
   ├── Security gate failures: Track trend
   ├── Time added by security scans: < 10% of total build time
   ├── Security exceptions granted: < 5% of findings
   └── Pipeline security incidents: 0

4. INCIDENT RESPONSE
   ├── Security incidents: Track count and trend
   ├── Incident response time: < 1 hour
   ├── Incident resolution time: Based on severity
   └── Post-incident reviews completed: 100%

5. COMPLIANCE
   ├── Policy compliance rate: > 95%
   ├── Audit findings: Track and trend
   ├── Training completion: 100% annually
   └── Access reviews completed: 100% quarterly
```

### Security Dashboard

```
┌─────────────────────────────────────────────┐
│         SECURITY DASHBOARD                  │
├─────────────────────────────────────────────┤
│ Vulnerability Status                        │
│ ┌─────────────────────────────────────────┐ │
│ │ Critical:  3  ⚠️  (↓ 2 from last week) │ │
│ │ High:     12  ⚠️  (↑ 3 from last week) │ │
│ │ Medium:   45  ℹ️                        │ │
│ │ Low:     128  ℹ️                        │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Mean Time to Remediate                      │
│ ┌─────────────────────────────────────────┐ │
│ │ Critical: 5 days  ✅ (Target: < 7)     │ │
│ │ High:    18 days  ✅ (Target: < 30)    │ │
│ │ Medium:  45 days  ⚠️  (Target: < 60)   │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Security Scan Coverage                      │
│ ┌─────────────────────────────────────────┐ │
│ │ SAST:  87% ✅                           │ │
│ │ SCA:   100% ✅                          │ │
│ │ DAST:  75% ⚠️                           │ │
│ │ Container: 100% ✅                      │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Best Practices

### 1. Shift Security Left
- Integrate security early in SDLC
- Provide security training to developers
- Use IDE security plugins
- Implement pre-commit hooks

### 2. Automate Everything
- Automated security scanning in CI/CD
- Automated vulnerability management
- Automated compliance checks
- Infrastructure as code

### 3. Defense in Depth
- Multiple layers of security controls
- Assume each layer can be breached
- Redundant security mechanisms
- Principle of least privilege

### 4. Continuous Monitoring
- Real-time security monitoring
- Automated alerting
- Log aggregation and analysis
- Threat intelligence integration

### 5. Fail Securely
- Secure defaults
- Fail closed, not open
- Error messages don't leak information
- Graceful degradation

### 6. Security as Code
- Policy as code
- Automated compliance testing
- Version controlled security configs
- Immutable infrastructure

### 7. Regular Testing
- Automated security testing
- Penetration testing
- Red team exercises
- Chaos engineering for security

### 8. Incident Response Preparedness
- Documented incident response plan
- Regular drills and tabletop exercises
- Clear escalation procedures
- Post-incident reviews

### 9. Supply Chain Security
- Verify software provenance
- Sign and verify artifacts
- SBOM (Software Bill of Materials)
- Dependency pinning and updates

### 10. Security Culture
- Security champions program
- Regular security training
- Blameless post-mortems
- Security metrics visibility

## Common Security Vulnerabilities

### OWASP Top 10 (2021)

**A01:2021 – Broken Access Control**
```
Prevention:
- Implement proper authorization checks
- Deny by default
- Test access controls thoroughly
- Log access control failures
```

**A02:2021 – Cryptographic Failures**
```
Prevention:
- Use strong encryption (AES-256, RSA-2048+)
- Implement TLS 1.3
- Secure key management
- Don't store sensitive data unnecessarily
```

**A03:2021 – Injection**
```
Prevention:
- Use parameterized queries
- Validate and sanitize input
- Use ORM frameworks
- Implement WAF
```

**A04:2021 – Insecure Design**
```
Prevention:
- Threat modeling
- Secure design patterns
- Security requirements in user stories
- Security architecture review
```

**A05:2021 – Security Misconfiguration**
```
Prevention:
- Automated configuration management
- Remove default credentials
- Disable unnecessary features
- Regular security audits
```

**A06:2021 – Vulnerable and Outdated Components**
```
Prevention:
- Dependency scanning
- Regular updates
- Remove unused dependencies
- Monitor CVE databases
```

**A07:2021 – Identification and Authentication Failures**
```
Prevention:
- Multi-factor authentication
- Strong password policies
- Session management
- Rate limiting
```

**A08:2021 – Software and Data Integrity Failures**
```
Prevention:
- Digital signatures
- Verify integrity of updates
- Secure CI/CD pipeline
- Supply chain security
```

**A09:2021 – Security Logging and Monitoring Failures**
```
Prevention:
- Comprehensive logging
- Real-time monitoring
- Automated alerting
- Log protection
```

**A10:2021 – Server-Side Request Forgery (SSRF)**
```
Prevention:
- Input validation
- Network segmentation
- Whitelist allowed destinations
- Disable unused URL schemas
```

## When to Use This Skill

Use the DevSecOps skill when you need to:

- ✅ Implement security in CI/CD pipelines
- ✅ Set up vulnerability scanning
- ✅ Configure container security
- ✅ Manage secrets securely
- ✅ Implement compliance controls
- ✅ Design secure architectures
- ✅ Respond to security incidents
- ✅ Perform security code reviews
- ✅ Set up security monitoring
- ✅ Automate security testing
- ✅ Implement zero trust architecture
- ✅ Secure cloud infrastructure
- ✅ Configure authentication/authorization
- ✅ Implement encryption
- ✅ Conduct threat modeling

## Examples

### Example 1: Setting Up Security Pipeline

**Request**: "Set up a complete security scanning pipeline for a Python FastAPI application"

**Response**:
```yaml
# .github/workflows/security.yml
name: Security Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly scan

jobs:
  secret-scanning:
    name: Secret Detection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - name: Gitleaks Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  dependency-scanning:
    name: Dependency Vulnerabilities
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install safety pip-audit
      - name: Safety Check
        run: safety check --json > safety-report.json
        continue-on-error: true
      - name: Pip Audit
        run: pip-audit --format json > pip-audit-report.json
      - name: Snyk Test
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  sast-scanning:
    name: Static Code Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Bandit Security Scan
        run: |
          pip install bandit[toml]
          bandit -r . -f json -o bandit-report.json
      - name: Semgrep Scan
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/python
            p/owasp-top-ten
            p/security-audit

  container-scanning:
    name: Container Security
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker Image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
      - name: Grype Scan
        uses: anchore/scan-action@v3
        with:
          image: myapp:${{ github.sha }}
          fail-build: true
          severity-cutoff: high

  api-security-testing:
    name: DAST - API Security
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Start Application
        run: |
          docker-compose up -d
          sleep 10
      - name: OWASP ZAP API Scan
        uses: zaproxy/action-api-scan@v0.4.0
        with:
          target: 'http://localhost:8000/openapi.json'
          fail_action: true
      - name: Stop Application
        run: docker-compose down

  security-report:
    name: Generate Security Report
    needs: [secret-scanning, dependency-scanning, sast-scanning, container-scanning]
    runs-on: ubuntu-latest
    steps:
      - name: Collect Results
        run: echo "Security scans completed"
      - name: Post to Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Security scan completed for ${{ github.repository }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Example 2: Kubernetes Security Hardening

**Request**: "Harden Kubernetes deployment for production"

**Response** provided in examples folder (see EXAMPLES.md)

### Example 3: Implementing Secrets Management

**Request**: "Set up secure secrets management with HashiCorp Vault"

**Response** provided in examples folder (see EXAMPLES.md)

## Resources

### Tools

**SAST:**
- SonarQube, Checkmarx, Veracode, Semgrep, CodeQL

**SCA:**
- Snyk, Dependabot, WhiteSource, Black Duck, OWASP Dependency-Check

**DAST:**
- OWASP ZAP, Burp Suite, Acunetix, Netsparker

**Container Security:**
- Trivy, Clair, Anchore, Aqua Security, Sysdig

**IaC Security:**
- Checkov, tfsec, Terrascan, Snyk IaC

**Secrets Management:**
- HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, CyberArk

### Standards & Frameworks

- OWASP Top 10
- OWASP ASVS (Application Security Verification Standard)
- NIST Cybersecurity Framework
- CIS Benchmarks
- ISO 27001
- SOC 2
- PCI-DSS

### Learning Resources

- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)
- [DevSecOps Manifesto](https://www.devsecops.org/)
- [Cloud Security Alliance](https://cloudsecurityalliance.org/)
- [SANS Institute](https://www.sans.org/)

---

**Note**: Security is everyone's responsibility. This skill provides guidance, but always consult security professionals for critical systems and stay updated with the latest threats and mitigation strategies.
