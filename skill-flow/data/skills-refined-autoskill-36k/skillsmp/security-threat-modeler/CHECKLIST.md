# Threat Modeling Checklist

Complete checklist for identifying and assessing security threats.

---

## Asset Identification

### Data Assets

- [ ] **Credentials** - Passwords, API keys, tokens, private keys
- [ ] **PII** - Names, emails, addresses, phone numbers, SSN
- [ ] **Financial data** - Bank accounts, card numbers, balances, transactions
- [ ] **Business data** - Orders, trades, contracts, pricing
- [ ] **Health data** - Medical records (if applicable)
- [ ] **Intellectual property** - Source code, algorithms, trade secrets

### System Assets

- [ ] **Infrastructure** - Servers, containers, cloud resources
- [ ] **Databases** - Data stores, backups, replicas
- [ ] **Keys & secrets** - Encryption keys, signing keys, certificates
- [ ] **Configurations** - Environment variables, config files
- [ ] **Logs** - Audit trails, application logs, access logs

### Availability Assets

- [ ] **Core services** - Primary business functionality
- [ ] **Supporting services** - Auth, payments, notifications
- [ ] **Data access** - Read/write to critical data
- [ ] **Network** - Connectivity, DNS, load balancers

---

## Trust Boundary Analysis

### External Boundaries

- [ ] **Internet → Load Balancer** - Public traffic entry point
- [ ] **Client → API** - User requests to backend
- [ ] **Mobile App → API** - Mobile client requests
- [ ] **Third-party → Webhook** - External callbacks
- [ ] **CDN → Origin** - Cached content requests

### Internal Boundaries

- [ ] **API Gateway → Services** - Internal service calls
- [ ] **Service → Service** - Inter-service communication
- [ ] **Service → Database** - Data layer access
- [ ] **Service → Cache** - Cache layer access
- [ ] **Service → Queue** - Message queue access

### Privileged Boundaries

- [ ] **User → Admin** - Privilege escalation point
- [ ] **Service → Secrets Manager** - Secret retrieval
- [ ] **Deploy → Production** - Code deployment
- [ ] **Developer → Infrastructure** - Admin access

---

## STRIDE Threat Analysis

### Spoofing (Identity)

- [ ] **Authentication bypass** - Can auth be circumvented?
- [ ] **Session hijacking** - Can sessions be stolen?
- [ ] **Token forgery** - Can tokens be forged?
- [ ] **IP spoofing** - Is IP used for trust?
- [ ] **Certificate spoofing** - Can TLS be bypassed?
- [ ] **Identity impersonation** - Can users impersonate others?

### Tampering (Data Integrity)

- [ ] **Request tampering** - Can requests be modified?
- [ ] **Response tampering** - Can responses be modified?
- [ ] **Database tampering** - Can data be modified directly?
- [ ] **Log tampering** - Can audit trails be modified?
- [ ] **Code tampering** - Can deployed code be modified?
- [ ] **Configuration tampering** - Can configs be modified?

### Repudiation (Accountability)

- [ ] **Missing audit logs** - Are all actions logged?
- [ ] **Log integrity** - Can logs be tampered?
- [ ] **Timestamp manipulation** - Can times be faked?
- [ ] **User action denial** - Can users deny actions?
- [ ] **Transaction proof** - Is there proof of transactions?

### Information Disclosure

- [ ] **Error messages** - Do errors leak information?
- [ ] **API responses** - Do responses over-share?
- [ ] **Logs** - Do logs contain sensitive data?
- [ ] **Source code** - Is code exposed?
- [ ] **Debug endpoints** - Are debug routes enabled?
- [ ] **Directory listing** - Are directories browsable?
- [ ] **Version info** - Is version info exposed?

### Denial of Service

- [ ] **Rate limiting** - Are endpoints rate limited?
- [ ] **Resource exhaustion** - Can resources be exhausted?
- [ ] **Algorithmic complexity** - Are there slow paths?
- [ ] **Amplification** - Can small requests cause large work?
- [ ] **Dependency failure** - Can dependencies be attacked?
- [ ] **Data flooding** - Can storage be filled?

### Elevation of Privilege

- [ ] **Role bypass** - Can role checks be bypassed?
- [ ] **IDOR** - Can object references be manipulated?
- [ ] **SQL injection** - Can queries be injected?
- [ ] **Command injection** - Can commands be injected?
- [ ] **Path traversal** - Can paths be manipulated?
- [ ] **Deserialization** - Can objects be injected?

---

## Attack Surface Enumeration

### Network Surface

- [ ] **Open ports** - What ports are exposed?
- [ ] **Protocols** - What protocols are used?
- [ ] **TLS configuration** - Is TLS properly configured?
- [ ] **DNS** - Is DNS secure (DNSSEC)?
- [ ] **Network segmentation** - Are networks isolated?

### API Surface

- [ ] **Public endpoints** - What's publicly accessible?
- [ ] **Authentication endpoints** - Login, register, reset
- [ ] **Sensitive endpoints** - Admin, financial, PII
- [ ] **File upload** - Any file upload functionality?
- [ ] **Search/query** - Any search functionality?
- [ ] **Export/download** - Any data export?

### Client Surface

- [ ] **Browser storage** - localStorage, sessionStorage, cookies
- [ ] **Client-side code** - JavaScript, WebAssembly
- [ ] **Mobile storage** - Keychain, shared preferences
- [ ] **Deep links** - URL scheme handlers
- [ ] **WebViews** - Embedded browsers

### Infrastructure Surface

- [ ] **Cloud console** - AWS/GCP/Azure access
- [ ] **CI/CD** - Build and deploy systems
- [ ] **Container registry** - Docker image storage
- [ ] **Secrets manager** - Secret storage access
- [ ] **Monitoring** - Observability systems

---

## Common Attacker Goals

### Financial Gain

- [ ] **Direct theft** - Steal funds, crypto, cards
- [ ] **Fraud** - Fake transactions, refund abuse
- [ ] **Ransomware** - Encrypt and extort
- [ ] **Cryptomining** - Use compute for mining
- [ ] **Data sale** - Sell stolen data

### Competitive Advantage

- [ ] **IP theft** - Steal code, algorithms
- [ ] **Customer theft** - Steal customer lists
- [ ] **Pricing intelligence** - Steal pricing data
- [ ] **Sabotage** - Disrupt competitor

### Hacktivism / Notoriety

- [ ] **Defacement** - Modify public pages
- [ ] **Data leak** - Expose embarrassing data
- [ ] **Service disruption** - Take service offline
- [ ] **Reputation damage** - Public disclosure

### Espionage

- [ ] **Surveillance** - Monitor communications
- [ ] **Data exfiltration** - Long-term data theft
- [ ] **Backdoor** - Maintain persistent access
- [ ] **Supply chain** - Compromise dependencies

---

## Smart Contract Specific Threats

### Access Control

- [ ] **Owner extraction** - Can owner be changed maliciously?
- [ ] **Function visibility** - Are functions properly restricted?
- [ ] **Proxy admin** - Can proxy admin be hijacked?
- [ ] **Multisig bypass** - Can multisig be bypassed?

### Economic Attacks

- [ ] **Flash loans** - Flash loan attack vectors
- [ ] **Price manipulation** - Oracle manipulation
- [ ] **MEV/Frontrunning** - Transaction ordering attacks
- [ ] **Sandwich attacks** - Surrounding victim transactions
- [ ] **Arbitrage exploitation** - Unintended arbitrage

### Logic Vulnerabilities

- [ ] **Reentrancy** - Reentrant call vulnerabilities
- [ ] **Integer overflow** - Arithmetic issues
- [ ] **Precision loss** - Rounding/truncation issues
- [ ] **State manipulation** - Invalid state transitions

### Protocol-Level

- [ ] **Governance attacks** - Voting manipulation
- [ ] **Collateral attacks** - Liquidation exploitation
- [ ] **Bridge attacks** - Cross-chain vulnerabilities
- [ ] **Upgrade attacks** - Malicious upgrades

---

## Risk Assessment Matrix

### Likelihood Factors

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Skill required | Expert | Intermediate | Script kiddie |
| Access required | Physical | Internal | Internet |
| Tools required | Custom | Available | Built-in |
| Detection risk | High | Medium | Low |

### Impact Factors

| Factor | Low | Medium | High | Critical |
|--------|-----|--------|------|----------|
| Data affected | Public | Internal | Sensitive | Regulated |
| Users affected | Few | Some | Many | All |
| Financial loss | <$1K | <$100K | <$1M | >$1M |
| Recovery time | Hours | Days | Weeks | Months |

### Risk Calculation

```
Risk Score = Likelihood × Impact

CRITICAL: Likelihood High × Impact Critical
HIGH:     Likelihood High × Impact High, or Medium × Critical
MEDIUM:   Likelihood Medium × Impact Medium
LOW:      Likelihood Low × Impact Low/Medium
```

---

## Mitigation Categories

### Preventive Controls

- [ ] **Input validation** - Reject malicious input
- [ ] **Authentication** - Verify identity
- [ ] **Authorization** - Enforce permissions
- [ ] **Encryption** - Protect data
- [ ] **Rate limiting** - Prevent abuse

### Detective Controls

- [ ] **Logging** - Record events
- [ ] **Monitoring** - Observe behavior
- [ ] **Alerting** - Notify anomalies
- [ ] **Audit trails** - Track changes

### Corrective Controls

- [ ] **Incident response** - Handle breaches
- [ ] **Backup/restore** - Recover data
- [ ] **Rollback** - Revert changes
- [ ] **Patching** - Fix vulnerabilities

### Compensating Controls

- [ ] **Defense in depth** - Multiple layers
- [ ] **Segmentation** - Limit blast radius
- [ ] **Least privilege** - Minimal access
- [ ] **Monitoring** - Detect failures

---

## Priority Classification

| Priority | Criteria | Timeline |
|----------|----------|----------|
| **P0** | Actively exploited or trivially exploitable | Immediate |
| **P1** | High likelihood, high impact | This sprint |
| **P2** | Medium likelihood or impact | Next 30 days |
| **P3** | Low likelihood and impact | Backlog |
| **P4** | Defense in depth, nice to have | Future |
