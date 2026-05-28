---
name: security-threat-modeler
description: Identify attackers, assets, trust boundaries, and realistic attack paths. Use when analyzing security posture, reviewing new features for threats, or creating threat models. Triggers on "threat model", "attack surface", "security analysis", "trust boundaries", "attacker goals", "threat assessment", "security review", "attack vectors".
---

# Security Threat Modeler

Identify attackers, assets, trust boundaries, and realistic attack paths. Map threats to mitigations in actual code.

## Core Framework: STRIDE + Attack Trees

| Category | Threat Type | Question |
|----------|-------------|----------|
| **S** | Spoofing | Can an attacker pretend to be someone else? |
| **T** | Tampering | Can an attacker modify data or code? |
| **R** | Repudiation | Can an attacker deny their actions? |
| **I** | Information Disclosure | Can an attacker access unauthorized data? |
| **D** | Denial of Service | Can an attacker make the system unavailable? |
| **E** | Elevation of Privilege | Can an attacker gain higher permissions? |

## When to Use

- Designing new features with security implications
- Reviewing authentication/authorization changes
- Adding new external integrations
- Handling sensitive data (PII, financial, credentials)
- Smart contract development
- Infrastructure changes

## Threat Modeling Workflow

### Step 1: Identify Assets

What are we protecting?

```
┌─────────────────────────────────────────────────────────────┐
│                        ASSETS                                │
├─────────────────────────────────────────────────────────────┤
│ Data Assets:                                                 │
│   • User credentials (passwords, tokens, API keys)          │
│   • Personal data (PII, emails, addresses)                  │
│   • Financial data (balances, transactions, card numbers)   │
│   • Business data (trades, orders, contracts)               │
│                                                             │
│ System Assets:                                              │
│   • Infrastructure (servers, databases, keys)               │
│   • Code/IP (source code, algorithms)                       │
│   • Availability (uptime, service access)                   │
│                                                             │
│ Reputation Assets:                                          │
│   • Trust (user confidence, regulatory standing)            │
│   • Brand (public perception)                               │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Map Trust Boundaries

Where does trust change?

```
┌─────────────────────────────────────────────────────────────┐
│  UNTRUSTED                                                   │
│  ┌─────────────┐                                            │
│  │   Internet  │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│ ════════╪═══════════════════════════════════════════════════│
│         │  BOUNDARY: Public Internet → API Gateway          │
│ ════════╪═══════════════════════════════════════════════════│
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │ API Gateway │  (Auth, Rate Limiting)                     │
│  └──────┬──────┘                                            │
│         │                                                    │
│ ════════╪═══════════════════════════════════════════════════│
│         │  BOUNDARY: Gateway → Internal Services            │
│ ════════╪═══════════════════════════════════════════════════│
│         ▼                                                    │
│  ┌─────────────┐      ┌─────────────┐                       │
│  │  Service A  │◄────►│  Service B  │                       │
│  └──────┬──────┘      └─────────────┘                       │
│         │                                                    │
│ ════════╪═══════════════════════════════════════════════════│
│         │  BOUNDARY: Services → Data Stores                 │
│ ════════╪═══════════════════════════════════════════════════│
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │  Database   │                                            │
│  └─────────────┘                                            │
│  TRUSTED                                                     │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Profile Attackers

Who might attack and why?

| Attacker | Motivation | Capability | Targets |
|----------|------------|------------|---------|
| **Script Kiddie** | Fun, notoriety | Low - automated tools | Public endpoints |
| **Competitor** | Business advantage | Medium - targeted | Trade secrets, pricing |
| **Criminal** | Financial gain | Medium-High | Funds, credentials, PII |
| **Insider** | Revenge, greed | High - system access | Any accessible data |
| **Nation State** | Espionage, disruption | Very High - 0-days | Infrastructure, IP |

### Step 4: Map Attack Surfaces

```bash
# Find external endpoints
grep -rn "@Get\|@Post\|router\." --include="*.ts" --include="*.go"

# Find authentication points
grep -rn "login\|authenticate\|verify.*token" --include="*.ts"

# Find file upload handlers
grep -rn "upload\|multipart\|file" --include="*.ts"

# Find external API calls
grep -rn "fetch\|axios\|http\." --include="*.ts"

# Find admin/privileged functions
grep -rn "admin\|sudo\|privilege\|role" --include="*.ts"
```

### Step 5: Build Attack Trees

For each high-value asset, create an attack tree:

```
                    ┌──────────────────┐
                    │ GOAL: Steal Funds │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
   ┌───────────┐      ┌───────────┐      ┌───────────┐
   │ Compromise│      │  Exploit  │      │  Social   │
   │   Auth    │      │   Logic   │      │ Engineer  │
   └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
         │                  │                  │
    ┌────┴────┐        ┌────┴────┐        ┌────┴────┐
    │         │        │         │        │         │
    ▼         ▼        ▼         ▼        ▼         ▼
 ┌─────┐ ┌─────┐  ┌─────┐ ┌─────┐  ┌─────┐ ┌─────┐
 │Brute│ │Steal│  │Race │ │Price│  │Phish│ │Bribe│
 │Force│ │Token│  │Cond.│ │Manip│  │User │ │Staff│
 └─────┘ └─────┘  └─────┘ └─────┘  └─────┘ └─────┘
```

See [CHECKLIST.md](CHECKLIST.md) for complete threat checklist.
See [ATTACK-LIBRARY.md](ATTACK-LIBRARY.md) for common attack patterns.

## Output Format

### A) Assets at Risk

```
┌─────────────────────────────────────────────────────────────┐
│                      ASSETS AT RISK                          │
├───────────────┬──────────────┬───────────────────────────────┤
│ Asset         │ Value        │ Impact if Compromised         │
├───────────────┼──────────────┼───────────────────────────────┤
│ User tokens   │ CRITICAL     │ Account takeover, fund theft  │
│ Trading keys  │ CRITICAL     │ Unauthorized trades           │
│ User PII      │ HIGH         │ Regulatory fines, lawsuits    │
│ Order history │ MEDIUM       │ Privacy violation             │
└───────────────┴──────────────┴───────────────────────────────┘
```

### B) Attack Surfaces

```
┌─────────────────────────────────────────────────────────────┐
│                     ATTACK SURFACES                          │
├───────────────┬──────────────┬───────────────────────────────┤
│ Surface       │ Exposure     │ Entry Points                  │
├───────────────┼──────────────┼───────────────────────────────┤
│ REST API      │ Public       │ /api/*, 15 endpoints          │
│ WebSocket     │ Public       │ /ws/*, price feeds            │
│ Admin Panel   │ Internal     │ /admin/*, 8 endpoints         │
│ Worker Queue  │ Internal     │ RabbitMQ, 3 consumers         │
│ Database      │ Internal     │ PostgreSQL, port 5432         │
└───────────────┴──────────────┴───────────────────────────────┘
```

### C) Threat Scenarios

For each significant threat:

```
### THREAT: [Name]

**ID:** THREAT-001
**Category:** [STRIDE category]
**Attacker:** [Who would attempt this]
**Goal:** [What they want to achieve]

**Attack Path:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Preconditions:**
- [What must be true for attack to work]

**Likelihood:** [Low/Medium/High]
**Impact:** [Low/Medium/High/Critical]
**Risk Score:** [Likelihood × Impact]

**Affected Code:**
- `path/to/vulnerable/code.ts:123`

**Current Mitigations:**
- [Existing defense, if any]

**Recommended Mitigations:**
- [What should be added]
```

### D) Mitigations Mapped to Code

```
┌─────────────────────────────────────────────────────────────┐
│               MITIGATIONS → CODE MAPPING                     │
├─────────────────────┬───────────────────────────────────────┤
│ Mitigation          │ Implementation Location               │
├─────────────────────┼───────────────────────────────────────┤
│ Rate limiting       │ src/middleware/rateLimit.ts:45       │
│ Input validation    │ src/validators/orderSchema.ts:12     │
│ Auth middleware     │ src/middleware/auth.ts:78            │
│ MISSING: CSRF       │ ❌ Not implemented                    │
│ MISSING: WAF rules  │ ❌ Not implemented                    │
└─────────────────────┴───────────────────────────────────────┘
```

### E) Risk Matrix

```
                         IMPACT
              Low      Medium     High      Critical
         ┌─────────┬─────────┬─────────┬─────────┐
   High  │ MEDIUM  │  HIGH   │ CRITICAL│ CRITICAL│
         ├─────────┼─────────┼─────────┼─────────┤
L Medium │   LOW   │ MEDIUM  │  HIGH   │ CRITICAL│
I        ├─────────┼─────────┼─────────┼─────────┤
K  Low   │   LOW   │   LOW   │ MEDIUM  │  HIGH   │
E        └─────────┴─────────┴─────────┴─────────┘
L
I   Threats by risk:
H   • THREAT-003: Token theft [CRITICAL]
O   • THREAT-001: SQL injection [HIGH]
O   • THREAT-007: Rate limit bypass [MEDIUM]
D   • THREAT-012: Info disclosure [LOW]
```

### F) Prioritized Recommendations

```
IMMEDIATE (This Sprint):
1. [Highest risk mitigation] - blocks THREAT-001, THREAT-003

SHORT-TERM (Next 30 days):
2. [Medium risk mitigation] - blocks THREAT-007
3. [Medium risk mitigation]

LONG-TERM (Roadmap):
4. [Defense in depth improvement]
5. [Monitoring enhancement]
```

## Quick Commands

```bash
# Find authentication code
grep -rn "authenticate\|authorize\|checkPermission" --include="*.ts"

# Find cryptographic operations
grep -rn "crypto\|encrypt\|decrypt\|hash\|sign\|verify" --include="*.ts"

# Find SQL queries
grep -rn "SELECT\|INSERT\|UPDATE\|DELETE\|query(" --include="*.ts"

# Find user input handling
grep -rn "req\.body\|req\.params\|req\.query" --include="*.ts"

# Find secret handling
grep -rn "secret\|password\|apiKey\|token" --include="*.ts" --include="*.env*"

# Find privileged operations
grep -rn "admin\|root\|sudo\|elevate" --include="*.ts"
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete threat checklist
- [ATTACK-LIBRARY.md](ATTACK-LIBRARY.md) - Common attack patterns & mitigations
