# Secure Architecture Patterns

Proven design patterns and anti-patterns for building secure, resilient systems.

## Foundational Patterns

### 1. Defense in Depth (Layered Security)

**Intent**: Multiple independent security layers so failure of one doesn't compromise the entire system

**Implementation:**
```
Internet → WAF → Load Balancer → API Gateway → Application → Database
           ↓      ↓                ↓              ↓             ↓
        DDoS    TLS           Authentication    Input       Encryption
        Protect Termination   Authorization     Validation  at Rest
```

**Benefits**: Redundancy, resilience, multiple detection points
**Trade-offs**: Complexity, potential performance impact
**When to Use**: Always - foundational security principle

### 2. Zero Trust Architecture

**Intent**: "Never trust, always verify" - assume breach, verify every request

**Components:**
- **Identity-Centric**: Every user, device, service has verified identity
- **Least Privilege**: Minimal access, just-in-time elevation
- **Micro-Segmentation**: Network segmentation at workload level
- **Continuous Verification**: Validate on every request, not just at perimeter

**Implementation:**
```
Request → Identity Provider → Policy Engine → Access Decision
             (Who?)           (Context?)      (Allow/Deny)
                                  ↓
                           Risk Score:
                           - Device posture
                           - Location
                           - Time
                           - Behavior
```

**Benefits**: Limits blast radius, reduces insider threats, cloud-native
**Trade-offs**: Requires robust identity infrastructure, potential UX friction
**When to Use**: Modern architectures, cloud-native, high-security environments

### 3. Secure by Design

**Intent**: Security is architectural from inception, not retrofitted

**Principles:**
- Threat modeling during design phase
- Security requirements alongside functional requirements
- Security testing in CI/CD pipeline
- Privacy by design (GDPR compliance)

**Benefits**: Lower cost than retrofitting, fewer vulnerabilities, regulatory compliance
**Trade-offs**: Requires security expertise early, may slow initial development
**When to Use**: Always - especially regulated industries, sensitive data

### 4. Principle of Least Privilege

**Intent**: Grant minimum access necessary for function, no more

**Implementation Levels:**
- **User Access**: Role-based access control (RBAC), attribute-based (ABAC)
- **Service Access**: Service accounts with minimal IAM permissions
- **Network Access**: Micro-segmentation, security groups
- **Data Access**: Column/row-level security, encryption scopes

**Benefits**: Limits damage from compromised accounts, reduces insider threats
**Trade-offs**: Requires granular access management, can be operationally complex
**When to Use**: Always - fundamental security principle

## Application Security Patterns

### 5. API Gateway Pattern

**Intent**: Centralized entry point for API security, rate limiting, auth

**Responsibilities:**
- Authentication & Authorization
- Rate limiting & throttling
- Input validation
- TLS termination
- Logging & monitoring
- API versioning

**Benefits**: Centralized security enforcement, simplified client access
**Trade-offs**: Single point of failure (mitigate with HA), potential bottleneck
**When to Use**: Microservices, public APIs, mobile backends

### 6. Backend for Frontend (BFF)

**Intent**: Separate backend for each client type (web, mobile, partners) with tailored security

**Implementation:**
```
Web App → Web BFF → Microservices
Mobile → Mobile BFF → Microservices
Partners → Partner BFF → Microservices
```

**Benefits**: Client-specific security policies, reduced attack surface
**Trade-offs**: More components to maintain, potential code duplication
**When to Use**: Multiple client types with different security requirements

### 7. Secrets Management Pattern

**Intent**: Centralized, encrypted storage and rotation of secrets (API keys, passwords, certificates)

**Implementation:**
- **Tools**: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault
- **Pattern**: Application requests secret at runtime, never stored in code/config
- **Rotation**: Automated periodic rotation without downtime

**Benefits**: No secrets in code, audit trail, automated rotation
**Trade-offs**: Dependency on secrets service, complexity
**When to Use**: Always for production systems

### 8. Circuit Breaker + Bulkhead

**Intent**: Prevent cascading failures, isolate failures to protect system availability

**Circuit Breaker States:**
- **Closed**: Normal operation
- **Open**: Failures detected, reject requests immediately
- **Half-Open**: Testing if service recovered

**Bulkhead**: Isolate resources (thread pools, connections) per service

**Benefits**: Graceful degradation, prevents cascade failures
**Trade-offs**: Requires careful tuning, false positives possible
**When to Use**: Distributed systems, external API dependencies

## Data Security Patterns

### 9. Encryption Everywhere

**Intent**: Encrypt data at rest, in transit, and in use

**Implementation:**
- **At Rest**: AES-256-GCM for databases, object storage, backups
- **In Transit**: TLS 1.3 for all network communication
- **In Use**: Confidential computing (SGX, SEV) for sensitive processing

**Key Management**: Envelope encryption (DEK encrypted by KEK)

**Benefits**: Defense against data breaches, compliance requirements
**Trade-offs**: Performance overhead, key management complexity
**When to Use**: Sensitive data (PII, PHI, PCI), regulatory compliance

### 10. Data Tokenization

**Intent**: Replace sensitive data with non-sensitive tokens, store mapping securely

**Use Cases:**
- **Credit Cards**: Replace PAN with token, store token in app DB
- **PII**: Tokenize SSN, passport numbers, maintain mapping in vault

**Benefits**: Reduces PCI DSS scope, limits data exposure
**Trade-offs**: Additional tokenization service, query limitations
**When to Use**: Payment processing, PII handling, compliance reduction

### 11. Data Masking & Anonymization

**Intent**: Hide or remove sensitive data in non-production environments

**Techniques:**
- **Masking**: Show only last 4 digits (***-**-1234)
- **Pseudonymization**: Replace with fake but realistic data
- **Anonymization**: Irreversibly remove identifying information

**Benefits**: Safe testing/development, GDPR compliance
**Trade-offs**: Data realism may be reduced
**When to Use**: Non-production environments, data sharing

## Infrastructure Patterns

### 12. Bastion Host (Jump Box)

**Intent**: Secure entry point for administrative access to private networks

**Implementation:**
- Single hardened instance in public subnet
- All admin access goes through bastion
- Multi-factor authentication required
- Session recording for audit

**Modern Alternative**: AWS Systems Manager Session Manager, Azure Bastion (no persistent bastion host)

**Benefits**: Centralized access control, audit trail
**Trade-offs**: Potential single point of failure, requires maintenance
**When to Use**: Administrative access to private networks

### 13. Web Application Firewall (WAF)

**Intent**: Filter malicious HTTP/HTTPS traffic before reaching application

**Protection Against:**
- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- DDoS attacks
- Bot traffic

**Benefits**: Blocks common attacks, reduces load on app
**Trade-offs**: False positives possible, requires tuning
**When to Use**: Public-facing web applications

### 14. Security Information and Event Management (SIEM)

**Intent**: Centralized logging, correlation, and alerting for security events

**Components:**
- Log aggregation from all sources
- Real-time correlation rules
- Anomaly detection
- Incident response workflows

**Benefits**: Centralized visibility, threat detection, compliance
**Trade-offs**: Expensive, requires tuning, alert fatigue
**When to Use**: Mature security programs, compliance requirements

## Anti-Patterns to Avoid

### ❌ Security Through Obscurity

**Problem**: Relying on secrecy of implementation as primary defense

**Example**: Using a "secret" API endpoint path instead of proper authentication

**Why Bad**: Secrets get discovered, provides false sense of security

**Instead**: Use proper authentication, authorization, encryption

### ❌ Rolling Your Own Crypto

**Problem**: Implementing cryptographic algorithms from scratch

**Example**: Creating custom encryption algorithm

**Why Bad**: Crypto is hard, subtle bugs = catastrophic failures

**Instead**: Use established libraries (libsodium, OpenSSL, Bouncy Castle)

### ❌ Hardcoded Secrets

**Problem**: API keys, passwords, certificates in source code or config files

**Example**: `API_KEY = "sk_live_abc123..."`

**Why Bad**: Secrets leaked in version control, container images

**Instead**: Use secrets management services, environment variables

### ❌ Monolithic Security Perimeter

**Problem**: "Castle and moat" - strong perimeter, weak internal security

**Example**: VPN access = trusted for everything

**Why Bad**: Insider threats, lateral movement after breach

**Instead**: Zero Trust, micro-segmentation, least privilege

### ❌ Security as an Afterthought

**Problem**: Building features first, adding security later

**Example**: "We'll add authentication before launch"

**Why Bad**: Retrofitting is expensive, error-prone, often incomplete

**Instead**: Secure by design, security requirements from day one

### ❌ Alert Fatigue

**Problem**: Too many security alerts, most false positives

**Example**: SIEM generating 10,000 alerts/day, all ignored

**Why Bad**: Real threats buried in noise, team burnout

**Instead**: Tune rules, prioritize by severity, automate response

### ❌ Shared Accounts

**Problem**: Multiple people using same credentials

**Example**: "admin" account shared among team

**Why Bad**: No accountability, can't revoke individual access, audit trail useless

**Instead**: Individual accounts, SSO, group-based permissions

## Pattern Selection Guide

Choose patterns based on:

1. **Threat Model**: What are you defending against?
2. **Compliance Requirements**: GDPR, HIPAA, PCI DSS, SOC 2?
3. **Architecture**: Monolith, microservices, serverless, hybrid?
4. **Team Maturity**: Can team implement and maintain complex patterns?
5. **Risk vs. Cost**: High-value assets justify more expensive controls

**Common Combinations:**

**SaaS Application:**
- Zero Trust + API Gateway + Secrets Management + WAF + SIEM

**Financial Services:**
- Defense in Depth + Encryption Everywhere + Tokenization + HSM + Audit Logging

**Healthcare:**
- Secure by Design + RBAC + Data Masking + Encryption + BAA with vendors

**E-Commerce:**
- API Gateway + WAF + PCI-compliant payment processor + Rate Limiting + DDoS Protection

---

**Key Insight**: Security patterns are composable. Combine multiple patterns to address different threat vectors. The best architecture uses simple, well-understood patterns applied consistently across the system.