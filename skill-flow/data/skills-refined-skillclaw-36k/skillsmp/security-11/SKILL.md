---
name: "security"
description: "Shared security framework across all phases. Security principles, requirements, architecture, testing, operations, and compliance integration. Warm, story-driven Expert Mentor style for 2026."
type: "shared"
used_by: ["all_phases"]
---

#  Security Framework

---

##  What You'll Learn

 How to build security into every phase (not bolt it on later)
 Which security threats actually matter (and which are hype)
 What tools to use in 2026 (with free alternatives)
 How to sleep at night knowing your system is secure
 What auditors actually look for (spoiler: it's not scary)

**Time Investment:** 45 minutes to read, a lifetime to master
**Difficulty:** Medium (we explain everything in plain English)

---

##  Quick Navigation

**New to Security?** Start here:
- [Security Principles](#-security-principles-the-foundation) - The mindset that protects everything
- [Common Threats](#-threat-modeling-know-your-enemy) - What you're actually fighting against

**Ready to Build?** Jump to:
- [Security by Phase](#-security-by-phase-when-to-do-what) - Your action plan for each phase
- [Security Controls](#-security-controls-your-protection-toolkit) - The specific protections to implement

**Need Specifics?** Go to:
- [Security Testing](#-security-testing-finding-vulnerabilities) - How to test your security
- [Security Tools](#-security-tools-2026-edition) - What to use (with free options)
- [Incident Response](#-when-things-go-wrong-incident-response) - What to do when security fails

---

##  Security Principles: The Foundation

### The CIA Triad (Not the spy agency)

**Confidentiality** - "Only the right people see the data"
- Example: Your medical records should only be visible to you and your doctors
- Real-world analogy: A locked filing cabinet where only certain people have keys

**Integrity** - "The data hasn't been tampered with"
- Example: Your bank balance shows what you actually have
- Real-world analogy: A sealed document—once opened, you know if someone messed with it

**Availability** - "The system works when you need it"
- Example: Your email is accessible 24/7, not crashed under attack
- Real-world analogy: A store that's open during business hours, not "closed due to vandalism"

**Why this matters:** If you fail any one of these, you fail security. Period.

---

### Defense in Depth (Layers of Protection)

**The Castle Analogy:**

Think about a medieval castle:
1. **Moat** - First barrier (network security, firewalls)
2. **Castle walls** - Second barrier (encryption, access controls)
3. **Guards at the gate** - Third barrier (authentication, authorization)
4. **Treasure room lock** - Fourth barrier (data encryption, secrets management)

If an attacker gets past the moat, they still face walls. If they scale the walls, they face guards. If they trick the guards, they still need to pick the lock.

**In software:**
```
Internet → Firewall → WAF → Auth System → Application → Database
  ↓         ↓         ↓         ↓            ↓            ↓
 Layer 1   Layer 2   Layer 3   Layer 4     Layer 5      Layer 6
```

**If one layer fails, the others still protect you.**

---

### Least Privilege (Give Only What's Needed)

**The Principle:** Users (and systems) should have the minimum access required to do their job. Nothing more.

**Example:**
-  **Wrong:** Customer service reps can delete any customer's account
-  **Right:** Customer service reps can only view accounts (not delete)
-  **Right:** Managers can deactivate accounts (but not delete them permanently)

**Real-world analogy:** A hotel key card only opens your room, not every room in the hotel.

**Why this matters:** If an account is compromised, the damage is limited to what that account can access.

---

##  Threat Modeling: Know Your Enemy

Threat modeling is like a fire drill for security. You imagine attacks before they happen, so you can prevent them.

### The STRIDE Method (Easy to Remember)

<details>
<summary><strong>📖 Deep Dive: STRIDE Explained with Examples</strong></summary>

**S - Spoofing (False Identity)**
- **What it is:** Pretending to be someone else
- **Example:** Attacker sends email from "ceo@yourcompany.com" (but it's not really the CEO)
- **Prevention:** Email authentication (SPF, DKIM), multi-factor authentication (MFA)

**T - Tampering (Data Modification)**
- **What it is:** Changing data in transit or at rest
- **Example:** Attacker modifies payment amount from $100 to $1 before it reaches the bank
- **Prevention:** Encryption in transit (TLS), digital signatures, checksums

**R - Repudiation (Denying Actions)**
- **What it is:** Someone claims "I didn't do that" when they did
- **Example:** Employee deletes critical files and claims their account was hacked
- **Prevention:** Comprehensive audit logging, non-repudiation controls

**I - Information Disclosure (Data Exposure)**
- **What it is:** Data is revealed to unauthorized people
- **Example:** API returns all user data when only requesting your own profile
- **Prevention:** Access controls, data filtering, encryption

**D - Denial of Service (Availability Attack)**
- **What it is:** System is overwhelmed and becomes unavailable
- **Example:** Attacker sends 1 million requests per second, crashing your server
- **Prevention:** Rate limiting, DDoS protection, auto-scaling

**E - Elevation of Privilege (Unauthorized Access)**
- **What it is:** Gaining higher-level access than you should have
- **Example:** Regular user finds a vulnerability and becomes admin
- **Prevention:** Role-based access control (RBAC), privilege separation, regular access reviews

</details>

---

### How to Threat Model (In Practice)

**Step 1: Draw Your System**
- Sketch out your architecture (servers, databases, APIs, users)
- Include data flows (how data moves between components)

**Step 2: Identify Threats**
- For each component, ask: "What could go wrong here?"
- Use STRIDE as your checklist

**Step 3: Prioritize**
- High impact + high likelihood = Fix first
- Low impact + low likelihood = Maybe fix later (or accept the risk)

**Step 4: Mitigate**
- Design controls to prevent or detect each threat
- Document your decisions

---

## 🔄 Security by Phase: When to Do What

### Phase 1: Vision & Strategy - "What Are We Building?"

**Security Activities:**
- Identify what data you'll handle (customer data? payments? health records?)
- Identify which regulations apply (GDPR? PCI DSS? HIPAA?)
- Initial security risk assessment (what could go wrong?)
- Include security in the business case (security costs money but saves more)

**Emotional Check:** This might feel like "extra work" but trust me—finding out you need SOC 2 compliance AFTER you've built everything is a nightmare. Discovering it now saves you months of rework.

**Deliverables:**
- Security considerations document (1-2 pages)
- List of applicable regulations
- Initial risk assessment (high/medium/low for major risks)

**Owner:** Product Owner + Security Lead

**⏱️ Time Investment:** 4-8 hours

---

### Phase 2: Requirements & Scope - "What Security Do We Need?"

**Security Activities:**
- Define security requirements using the CIA triad
- Define authentication requirements (MFA? SSO? social login?)
- Define authorization requirements (who can do what?)
- Define data protection requirements (what needs encryption?)
- Define audit logging requirements (what do we need to track?)
- Identify security standards to follow (NIST? ISO 27001? OWASP?)

**Common Mistake to Avoid:** 🚫
> "We'll figure out authentication later."

**Why it's a problem:** Authentication is foundational. If you build your entire app without considering how users will log in, you'll end up rebuilding half your codebase.

**Deliverables:**
- Security requirements specification (5-10 pages)
- Authentication and authorization design
- Data classification (public, internal, confidential, restricted)
- Audit logging requirements
- Updated security risk assessment

**Owner:** Security Architect

**⏱️ Time Investment:** 2-3 weeks

---

### Phase 3: Architecture & Design - "How Will We Secure It?"

**Security Activities:**
- Design security architecture (defense in depth layers)
- Design authentication system (how users prove who they are)
- Design authorization system (how users get permission)
- Design encryption strategy (data at rest + data in transit)
- Design network security (VPC, firewalls, WAF)
- Design secrets management (where do we store API keys, passwords?)
- Conduct threat modeling (use STRIDE or another methodology)
- Define security controls matrix (what we're implementing and why)

**Emotional Reality Check:** 😰
This phase can feel overwhelming. You're making decisions that affect the entire system. Here's the good news: you don't have to be perfect. You just need to be thoughtful and document your decisions. You can always adjust later.

**Deliverables:**
- Security architecture document (10-20 pages with diagrams)
- Authentication and authorization design
- Network security design
- Secrets management design
- Threat models (for major system components)
- Security controls matrix

**Owner:** Security Architect

**⏱️ Time Investment:** 4-6 weeks

---

### Phase 4: Development Planning - "How Will We Build Security?"

**Security Activities:**
- Define how security controls will be implemented
- Define security testing approach (SAST, DAST, SCA—explained later)
- Define vulnerability management process (how we handle security issues)
- Integrate security into CI/CD pipeline (automated security checks)
- Define security documentation requirements

**Key Decision:** Automated vs. Manual Security

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Automated** | Fast, consistent, catches issues early | Can have false positives, misses some issues | CI/CD pipeline, continuous monitoring |
| **Manual** | Catches complex issues, human intuition | Slow, expensive, inconsistent | Penetration testing, security reviews |
| **Hybrid**  | Best of both worlds | More complex setup | Most projects (recommended) |

**Deliverables:**
- Security controls implementation plan
- Security testing approach document
- Vulnerability management process
- CI/CD security integration plan

**Owner:** Security Lead

**⏱️ Time Investment:** 1-2 weeks

---

### Phase 5: Development Execution - "Building Security In"

**Security Activities:**
- Conduct security code reviews (peer reviews focused on security)
- Run Static Application Security Testing (SAST) scans
- Run Software Composition Analysis (SCA) scans
- Hold threat modeling sessions (as you discover new risks)
- Provide secure coding guidance to developers
- Review secrets management implementation
- Validate security controls are being implemented correctly

**The "Shift Left" Movement:**

<details>
<summary><strong>📖 What is "Shift Left"? (And why security people keep saying it)</strong></summary>

**Traditional Security (Right side):**
```
Development → Testing → Deployment → SECURITY CHECK → "Oh no, we have to fix everything!"
```

**Shift Left Security (Left side):**
```
SECURITY CHECK → Development → Testing → Deployment
```

**The Difference:**
- **Traditional:** Find security issues after everything is built (expensive to fix)
- **Shift Left:** Find security issues while you're coding (cheap to fix)

**Real-world Analogy:**
- **Traditional:** Building a house, then realizing you forgot plumbing. Now you have to tear down walls.
- **Shift Left:** Planning plumbing before you start building. Much cheaper.

**Why it matters:**
- Finding a bug during coding: $100 to fix
- Finding a bug during testing: $1,000 to fix
- Finding a bug in production: $10,000+ to fix (plus potential damage)

</details>

**Deliverables:**
- Security code review reports
- SAST scan results (with remediation)
- SCA scan results (dependency vulnerabilities)
- Updated threat models
- Secure coding guidelines (team reference)

**Owner:** Security Lead + Security Architect

**⏱️ Time Investment:** Ongoing (throughout development)

---

### Phase 6: Quality & Security Validation - "Testing Our Security"

**Security Activities:**
- Comprehensive security testing (not just automated scans)
- Penetration testing (ethical hackers try to break in)
- Validate all security controls work as designed
- Vulnerability assessment (systematic search for weaknesses)
- Validate compliance requirements are met
- Security regression testing (ensure we didn't break anything)
- Create security test report (what we tested, what we found, what we fixed)

**The Penetration Testing Question:**

<details>
<summary><strong>💭 Do I really need a penetration test? (It costs $5,000-$50,000!)</strong></summary>

**Short Answer:** Maybe, depending on your situation.

**You DEFINITELY need pentest if:**
-  Handling payment card data (PCI DSS requirement)
-  Handling healthcare data (HIPAA expectation)
-  Seeking SOC 2 certification (expected by auditors)
-  B2B SaaS with enterprise customers (they'll ask for it)
-  Handling highly sensitive data (trade secrets, government data)

**You might NOT need pentest if:**
-  Simple MVP with no sensitive data
-  Internal tool with no external access
-  Early prototype (not production)

**Cost-Effective Alternatives:**
- **Automated DAST tools:** OWASP ZAP (free), Burp Suite Community (free)
- **Bug bounty programs:** HackerOne, Bugcrowd (pay only for results)
- **Internal security team:** If you have security engineers on staff
- **Community feedback:** If open-source, researchers might report issues

**Recommendation:** Start with automated tools ($0). If you're handling sensitive data or pursuing compliance, budget for a professional pentest before production launch.

</details>

**Deliverables:**
- Security test plan (what we'll test and how)
- SAST scan results
- DAST scan results
- SCA scan results
- Penetration test report (if applicable)
- Vulnerability assessment (all findings + remediation status)
- Security sign-off (ready for production)

**Owner:** Security Lead + Security Architect

**⏱️ Time Investment:** 4-8 weeks

---

### Phase 7: Deployment & Release - "Security in Production"

**Security Activities:**
- Validate security controls work in production environment
- Run pre-deployment security scan (catch last-minute issues)
- Validate secrets management in production (are API keys secure?)
- Configure security monitoring and alerting (will we know if something goes wrong?)
- Validate compliance controls in production
- Define security rollback triggers (what causes us to undo deployment?)

**The Pre-Deployment Checklist:**

<details>
<summary><strong> The "Don't Crash Production" Security Checklist</strong></summary>

Before deploying to production, verify:

**Authentication & Authorization:**
- ☐ MFA enabled for all admin accounts
- ☐ Default passwords changed
- ☐ Guest/test accounts disabled
- ☐ Access controls working (users can only see their data)

**Data Protection:**
- ☐ TLS 1.3 enabled (no HTTPS warnings)
- ☐ Encryption at rest enabled (databases, storage)
- ☐ Sensitive data masked in logs (no passwords/credit cards)
- ☐ Backups encrypted and tested

**Secrets Management:**
- ☐ No secrets in code (no API keys, passwords in git)
- ☐ Secrets stored in vault (AWS Secrets Manager, HashiCorp Vault, etc.)
- ☐ Secrets rotated regularly (90-day maximum)
- ☐ Different secrets for dev/staging/production

**Monitoring & Alerting:**
- ☐ Security events logged (logins, permission changes, data access)
- ☐ Alerts configured (failed logins, suspicious activity)
- ☐ Log aggregation working (logs going to SIEM or central logging)
- ☐ Dashboard for security metrics

**Incident Response:**
- ☐ Runbook created (what to do if security incident occurs)
- ☐ Incident response team assigned
- ☐ Communication plan prepared (who to notify)
- ☐ Rollback plan tested (can we undo deployment if needed?)

**Compliance:**
- ☐ Audit trail complete and verifiable
- ☐ Compliance controls validated
- ☐ Documentation up to date
- ☐ Pre-production compliance check completed

**Red Light:** If ANY item is unchecked, don't deploy. Fix it first.

**Yellow Light:** If some items are "best effort" but not required, document the risk and get explicit approval to proceed.

**Green Light:** All items checked. Proceed with deployment (and celebrate!).

</details>

**Deliverables:**
- Pre-deployment security validation (passed )
- Production security validation (passed )
- Security monitoring configuration (documented)
- Security rollback triggers (documented)

**Owner:** Security Lead + DevOps Engineer

**⏱️ Time Investment:** 1-2 weeks

---

### Phase 8: Operations & Maintenance - "Security Never Sleeps"

**Security Activities:**
- Monitor security alerts and incidents
- Analyze security logs regularly
- Manage vulnerabilities (ongoing scanning and patching)
- Conduct regular security assessments
- Manage access controls (add/remove users, review permissions)
- Update security documentation
- Coordinate incident response when things go wrong

**The Ongoing Reality:**

Security isn't a one-time project. It's like maintaining a car—ongoing care prevents breakdowns.

**Daily:**
- Review security alerts (5-15 minutes)
- Check for critical vulnerabilities

**Weekly:**
- Analyze security logs for anomalies (1-2 hours)
- Review new security research/news (30 minutes)

**Monthly:**
- Conduct access reviews (remove unused access) (2-4 hours)
- Update security documentation (2-4 hours)
- Security metrics report (2-4 hours)

**Quarterly:**
- Security assessment (penetration test or vulnerability scan) (1-2 weeks)
- Security training for team (4-8 hours)
- Update threat models based on new threats (4-8 hours)

**Annually:**
- Compliance audit (SOC 2, HIPAA, etc.) (4-8 weeks)
- Security architecture review (2-4 weeks)
- Third-party security review (if applicable) (4-8 weeks)

**Deliverables:**
- Security monitoring dashboard (visible to team)
- Quarterly vulnerability assessments
- Monthly security patch reports
- Quarterly access review reports
- Security metrics (trends over time)
- Incident response reports (if incidents occurred)

**Owner:** Security Lead + SRE

**⏱️ Time Investment:** Ongoing (10-20% of operational time)

---

##  Security Controls: Your Protection Toolkit

### Authentication Controls (Proving Who You Are)

<details>
<summary><strong> Deep Dive: Authentication Options Explained</strong></summary>

**Multi-Factor Authentication (MFA)**
- **What it is:** Requiring multiple pieces of evidence to prove identity
- **Examples:** Password + code from phone, Password + fingerprint, Password + security key
- **Why it matters:** If a hacker steals your password, they still need your phone/fingerprint/key
- **Recommendation:** Require MFA for all admin accounts, optional for regular users
- **Cost:** Free to implement (most auth services have built-in MFA)

**Single Sign-On (SSO)**
- **What it is:** One login for multiple applications
- **Example:** Login once with Google/Microsoft, access all your company apps
- **Why it matters:** Better user experience, centralized account management
- **Recommendation:** Essential for enterprise (B2B) software, optional for consumer apps
- **Cost:** $2,000-$10,000/year for enterprise SSO providers

**Password Policies**
- **What it is:** Rules about what passwords are allowed
- **Common requirements:** Minimum length (8+ characters), complexity (mixed case, numbers, symbols), rotation (change every 90 days)
- **Why it matters:** Prevents weak passwords that are easily guessed
- **Recommendation:** Focus on length over complexity (15+ characters is better than 8 with symbols)
- **Cost:** Free to implement

</details>

---

### Authorization Controls (What You're Allowed to Do)

<details>
<summary><strong> Deep Dive: Authorization Models</strong></summary>

**Role-Based Access Control (RBAC)**
- **What it is:** Access based on user roles
- **Example:** "Admins can delete users, Editors can edit content, Viewers can only read"
- **Why it matters:** Simple to understand, easy to manage, industry standard
- **Recommendation:** Start here unless you have complex needs
- **Cost:** Free to implement (most frameworks have RBAC built-in)

**Principle of Least Privilege**
- **What it is:** Grant minimum access required for role
- **Example:** Customer service can view accounts (not delete), managers can deactivate accounts (not delete permanently)
- **Why it matters:** Limits damage if account is compromised
- **Recommendation:** Apply universally—no exceptions
- **Cost:** Free (it's a design principle, not a tool)

</details>

---

### Data Protection Controls (Protecting the Crown Jewels)

<details>
<summary><strong> Deep Dive: Encryption Strategies</strong></summary>

**Encryption at Rest**
- **What it is:** Encrypting data when it's stored (databases, file systems, backups)
- **Standard:** AES-256 (industry standard, virtually unbreakable)
- **What to encrypt:** Everything sensitive (customer data, secrets, configurations)
- **What NOT to encrypt:** Public data (marketing content, public profiles)
- **Why it matters:** If someone steals your hard drives/backups, they can't read the data
- **Recommendation:** Enable encryption on all cloud storage/databases (usually one checkbox)
- **Cost:** Free on most cloud platforms (AWS, Azure, GCP include it)

**Encryption in Transit**
- **What it is:** Encrypting data as it moves between systems
- **Standard:** TLS 1.3 (current version of HTTPS)
- **What to encrypt:** Everything (no unencrypted connections, ever)
- **Why it matters:** Prevents man-in-the-middle attacks (hackers intercepting data)
- **Recommendation:** Force HTTPS everywhere, use HSTS headers
- **Cost:** Free (Let's Encrypt for certificates, cloud platforms handle the rest)

**Data Classification**
- **What it is:** Categorizing data by sensitivity level
- **Common categories:**
  - **Public:** Can be shared freely (marketing content, public website)
  - **Internal:** Company internal (internal documentation, employee directory)
  - **Confidential:** Sensitive but not regulated (customer lists, internal metrics)
  - **Restricted:** Highly sensitive or regulated (health records, credit card numbers, trade secrets)
- **Why it matters:** Different data needs different protection levels
- **Recommendation:** Classify data in Phase 2, label data in documentation
- **Cost:** Free (it's a planning exercise)

</details>

---

### Network Security Controls (Securing the Pipes)

<details>
<summary><strong> Deep Dive: Network Security Architecture</strong></summary>

**Virtual Private Cloud (VPC)**
- **What it is:** Isolated network environment in the cloud
- **Why it matters:** Keeps your infrastructure separate from other cloud customers
- **Recommendation:** Always use VPC, never use default/public cloud settings
- **Cost:** Free (AWS, Azure, GCP all offer free VPC)

**Security Groups and Firewalls**
- **What it is:** Rules controlling network traffic (what can talk to what)
- **Example:** "Web servers can talk to database servers on port 5432, but nothing else can"
- **Why it matters:** Limits attack surface—if hackers compromise your web server, they can't directly access your database
- **Recommendation:** Whitelist approach (deny all, allow only what's needed)
- **Cost:** Free (built into cloud platforms)

**Web Application Firewall (WAF)**
- **What it is:** Firewall that inspects web traffic (HTTP/HTTPS) for attacks
- **What it blocks:** SQL injection, XSS, CSRF, and other OWASP Top 10 attacks
- **Why it matters:** Catches attacks before they reach your application
- **Recommendation:** Essential for public-facing web applications
- **Cost:** $20-$100/month (AWS WAF, CloudFlare WAF)

</details>

---

### Application Security Controls (Code-Level Protection)

<details>
<summary><strong> Deep Dive: Application Security Best Practices</strong></summary>

**Input Validation**
- **What it is:** Validating all user input before processing it
- **Example:** Email field must contain valid email format, age field must be number between 0-120
- **Why it matters:** Prevents malicious input from causing harm
- **Recommendation:** Validate on both client side (UX) and server side (security)
- **Cost:** Free (development effort)

**SQL Injection Prevention**
- **What it is:** Preventing attackers from manipulating database queries
- **Attack example:** Inputting `' OR '1'='1` to bypass authentication
- **Prevention:** Use parameterized queries or ORM (never string concatenation)
- **Why it matters:** SQL injection is #1 on OWASP Top 10 (very common, very dangerous)
- **Recommendation:** Always use prepared statements/parameterized queries
- **Cost:** Free (best practice coding)

**XSS (Cross-Site Scripting) Prevention**
- **What it is:** Preventing attackers from injecting malicious scripts into web pages
- **Attack example:** Comment field with `<script>stealCookies()</script>` that runs when others view the page
- **Prevention:** Output encoding, Content Security Policy (CSP) headers
- **Why it matters:** XSS is #3 on OWASP Top 10 (very common, can steal session cookies)
- **Recommendation:** Use modern frameworks (React, Vue, Angular), add CSP headers
- **Cost:** Free (framework feature + HTTP header)

**CSRF (Cross-Site Request Forgery) Protection**
- **What it is:** Preventing attackers from tricking users into unwanted actions
- **Attack example:** Victim visits malicious site that silently sends request to your bank's "transfer money" endpoint
- **Prevention:** CSRF tokens (unique token per form, verified on submission)
- **Why it matters:** CSRF is #5 on OWASP Top 10 (can cause unwanted actions)
- **Recommendation:** Most frameworks have CSRF protection built-in—just enable it
- **Cost:** Free (framework feature)

</details>

---

## 🔬 Security Testing: Finding Vulnerabilities

### Static Application Security Testing (SAST)

**What it is:** Scanning source code for vulnerabilities without running the code

**How it works:** Tools analyze your code for known vulnerability patterns (SQL injection, hardcoded secrets, insecure functions)

**When to run:** Every commit in CI/CD pipeline

**Tools (2026 Recommendations):**

| Tool | Best For | Cost | Learning Curve |
|------|----------|------|----------------|
| **SonarQube** | General code quality + security | Free (Community) / Paid (Enterprise) | Medium |
| **Semgrep** | Fast, customizable, developer-friendly | Free / Paid (Cloud) | Low |
| **Checkmarx** | Enterprise, comprehensive | Paid (expensive) | High |

**Recommendation for 2026:**
- **Start with:** SonarQube Community Edition (free) or Semgrep (free tier)
- **Upgrade to:** SonarQube Developer Edition when you need enterprise features

**What it catches:**
- SQL injection vulnerabilities
- Hardcoded secrets (API keys, passwords)
- Insecure dependencies
- Weak cryptography
- Code quality issues (some tools)

**What it misses:**
- Runtime vulnerabilities (only sees code, not execution)
- Business logic flaws (doesn't understand your business rules)
- Environment-specific issues (doesn't know about your deployment)

**⏱️ Time Investment:** 1-2 days to set up, runs automatically thereafter

---

### Dynamic Application Security Testing (DAST)

**What it is:** Testing a running application for vulnerabilities

**How it works:** Tools act like "ethical hackers," sending various inputs to your application and analyzing responses

**When to run:** During testing phase (Phase 6), before production deployment

**Tools (2026 Recommendations):**

| Tool | Best For | Cost | Learning Curve |
|------|----------|------|----------------|
| **OWASP ZAP** | Free, community-supported, great for learning | Free | Medium |
| **Burp Suite** | Professional, comprehensive | Free (Community) / Paid (Professional) | High |

**Recommendation for 2026:**
- **Start with:** OWASP ZAP (free)
- **Upgrade to:** Burp Suite Professional when you need advanced features

**What it catches:**
- SQL injection (confirmed exploitable)
- XSS (cross-site scripting)
- CSRF (cross-site request forgery)
- Authentication/authorization issues
- Session management flaws

**⏱️ Time Investment:** 2-3 days to learn and set up, 1-2 days per test cycle

---

### Software Composition Analysis (SCA)

**What it is:** Scanning dependencies (libraries, packages) for known vulnerabilities

**How it works:** Tools check your dependencies against vulnerability databases (like CVE database)

**When to run:** Every dependency change in CI/CD pipeline

**Why it matters:** 80-90% of modern application code is from dependencies. If you have vulnerable dependencies, you have vulnerable applications.

**Tools (2026 Recommendations):**

| Tool | Best For | Cost | Learning Curve |
|------|----------|------|----------------|
| **Snyk** | Best DX, great integration, PR comments | Free / Paid | Low |
| **Dependabot** | GitHub native, automated PRs for updates | Free | Low |

**Recommendation for 2026:**
- **Start with:** Snyk (free tier for small teams) or Dependabot (free on GitHub)
- **Upgrade to:** Snyk Pro when you need advanced features

**What it catches:**
- Known vulnerabilities in dependencies (CVEs)
- Outdated dependencies
- License compliance issues (some tools)

**⏱️ Time Investment:** 1 day to set up, runs automatically thereafter

---

### Container Security

**What it is:** Scanning container images (Docker) for vulnerabilities

**How it works:** Tools scan container filesystem and installed packages for vulnerabilities

**When to run:** Every container build in CI/CD pipeline

**Tools (2026 Recommendations):**

| Tool | Best For | Cost | Learning Curve |
|------|----------|------|----------------|
| **Trivy** | Free, comprehensive, fast | Free | Low |
| **Clair** | Open-source, API-based | Free | Medium |
| **Aqua** | Enterprise, full lifecycle | Paid (expensive) | High |

**Recommendation for 2026:**
- **Start with:** Trivy (free, excellent coverage)
- **Upgrade to:** Aqua when you need enterprise features (runtime protection)

**⏱️ Time Investment:** 1 day to set up, runs automatically thereafter

---

### Penetration Testing

**What it is:** Human ethical hackers attempting to compromise your system

**How it works:** Security professionals use automated tools + manual techniques to find vulnerabilities that tools miss

**When to run:** Annually or after major changes, before production launch

**Types:**

| Type | Description | Cost | Duration |
|------|-------------|------|----------|
| **Internal Pentest** | Test from inside network (like insider threat) | $5,000-$20,000 | 2-4 weeks |
| **External Pentest** | Test from internet (like external attacker) | $10,000-$30,000 | 2-4 weeks |
| **Web App Pentest** | Focus on web application vulnerabilities | $5,000-$15,000 | 1-3 weeks |

**Recommendation for 2026:**
- **If handling sensitive data:** Budget for annual external pentest ($15,000-$30,000)
- **If pursuing compliance:** Pentest is often required (SOC 2, PCI DSS, HIPAA)
- **If limited budget:** Start with automated DAST tools (OWASP ZAP free), upgrade to human pentest when budget allows

**What it catches:**
- Business logic flaws (tools miss these)
- Complex attack chains (combining multiple vulnerabilities)
- Human error vulnerabilities (misconfigurations, weak processes)
- Things tools miss (by definition—humans find what tools can't)

**⏱️ Time Investment:** 2-4 weeks for testing, 2-4 weeks for remediation

---

##  Security Standards and Compliance

### Common Security Standards

<details>
<summary><strong>📖 Explained Simply: What These Standards Actually Mean</strong></summary>

**NIST Cybersecurity Framework**
- **What it is:** US government framework for managing cybersecurity risk
- **Who uses it:** US government agencies, contractors, many private companies
- **What it requires:** Five functions: Identify, Protect, Detect, Respond, Recover
- **Why it matters:** Comprehensive framework, widely adopted
- **Difficulty:** Medium (flexible, not prescriptive)

**ISO 27001**
- **What it is:** International standard for information security management
- **Who uses it:** Global companies, especially in Europe
- **What it requires:** Information Security Management System (ISMS), 114 controls
- **Why it matters:** Internationally recognized, demonstrates security maturity
- **Difficulty:** High (rigorous certification process)

**OWASP (Open Web Application Security Project)**
- **What it is:** Community-driven knowledge base for web application security
- **Who uses it:** Web developers worldwide (industry standard)
- **What it requires:** Following OWASP Top 10 (top 10 web security risks)
- **Why it matters:** Practical, actionable, free
- **Difficulty:** Low to Medium (depends on which resources you use)

**CIS Controls**
- **What it is:** Prioritized set of actions for cybersecurity
- **Who uses it:** Organizations of all sizes
- **What it requires:** Implementing 18 control categories (153 safeguards)
- **Why it matters:** Prioritized by effectiveness (do the important stuff first)
- **Difficulty:** Medium (but flexible—start with basic controls)

</details>

---

### Regulatory Compliance

<details>
<summary><strong>📖 Compliance Explained: What You Actually Need to Do</strong></summary>

**HIPAA (Health Insurance Portability and Accountability Act)**
- **Applies to:** Healthcare providers, health plans, healthcare clearinghouses + business associates
- **What it protects:** PHI (Protected Health Information) - any health data that can be linked to a person
- **Key requirements:**
  - **Privacy Rule:** PHI must be protected, patients have rights to access their data
  - **Security Rule:** Administrative, physical, and technical safeguards
  - **Breach Notification:** Report breaches affecting 500+ individuals within 60 days
- **Audits:** HHS OCR can audit (though rare—usually triggered by breach)
- **Fines:** $100-$50,000 per violation (max $1.5 million per year)
- **Difficulty:** High (strict requirements, serious consequences)

**SOC 2 (Service Organization Control 2)**
- **Applies to:** Technology service providers storing customer data (especially SaaS companies)
- **What it protects:** Customer data based on Trust Services Criteria
- **Trust Services Criteria (you choose which apply):**
  - **Security:** System is protected against unauthorized access
  - **Availability:** System is available for operation and use
  - **Processing Integrity:** System processing is complete, valid, accurate, timely
  - **Confidentiality:** Information is protected from unauthorized disclosure
  - **Privacy:** Personal information is collected, used, retained, disclosed, and disposed of properly
- **Key requirements:** Documented controls, evidence collection, annual audit
- **Audits:** Annual SOC 2 Type II audit (6-12 months of data collection)
- **Fines:** No government fines (unlike HIPAA), but customers may require it
- **Difficulty:** High (comprehensive control documentation required)

**PCI DSS (Payment Card Industry Data Security Standard)**
- **Applies to:** Any organization handling payment card data (credit/debit cards)
- **What it protects:** Payment card data (PAN - Primary Account Number)
- **12 Requirements:** Network security, data protection, vulnerability management, access controls, monitoring, policy
- **Key requirements:** Quarterly vulnerability scans, annual audit, never store full card data
- **Audits:** Annual ROC (Report on Compliance) by QSA (Qualified Security Assessor)
- **Fines:** $5,000-$100,000 per month (from payment brands)
- **Difficulty:** High (strict, prescriptive requirements)

**SOX (Sarbanes-Oxley Act)**
- **Applies to:** Public companies, companies planning IPO
- **What it protects:** Financial reporting accuracy
- **Key requirements:**
  - **Section 404:** Internal controls over financial reporting (must be documented and tested)
  - **Section 302:** Executive certification of financial reports (CEOs/CFOs sign off)
  - **Segregation of Duties:** Separate roles for financial processes
  - **Audit Trail:** Complete audit trail for financial transactions
- **Audits:** Quarterly reviews, annual audit by external auditor
- **Fines:** Up to $5 million + 20 years in prison for willful violations
- **Difficulty:** Very High (strict requirements, serious consequences)

**GDPR (General Data Protection Regulation)**
- **Applies to:** Any organization processing EU residents' data (regardless of where organization is located)
- **What it protects:** Personal data (any data that can identify a person)
- **Key requirements:**
  - **Lawful Basis:** Legal basis for data processing (consent, contract, legal obligation, vital interests, public task, legitimate interests)
  - **Data Subject Rights:** Access, rectification, erasure ("right to be forgotten"), portability, objection, restrict processing
  - **Data Protection by Design and Default:** Build privacy into systems from the start
  - **Breach Notification:** Report breaches to authorities within 72 hours, to affected individuals if high risk
  - **DPO:** Data Protection Officer required (unless small-scale processing)
- **Audits:** Data Protection Authorities can audit (national authorities in each EU country)
- **Fines:** Up to €20 million or 4% of global annual revenue (whichever is higher)
- **Difficulty:** High (broad scope, strict requirements, massive fines)

**DoD/ITAR (Department of Defense / International Traffic in Arms Regulations)**
- **Applies to:** Defense contractors, organizations handling controlled technical data
- **What it protects:** Defense articles and services (ITAR), CUI (Controlled Unclassified Information)
- **Key requirements:**
  - **CMMC:** Cybersecurity Maturity Model Certification (Level 1-5, based on sensitivity)
  - **NIST 800-171:** Protecting CUI (130 security requirements)
  - **DFARS:** Defense Federal Acquisition Regulation Supplement (contract requirements)
- **Audits:** CMMC assessment by C3PAO (CMMC Third-Party Assessment Organization), DoD audits
- **Fines:** Contract termination, fines, potential criminal penalties
- **Difficulty:** Very High (complex, prescriptive, defense-specific)

</details>

**Which Compliance Applies to You?**

| If you... | Then you need... |
|-----------|------------------|
| Handle healthcare data (US) | HIPAA |
| Store/process credit cards | PCI DSS |
| Are a public company (US) | SOX |
| Have EU customers | GDPR |
| Sell to B2B enterprise | SOC 2 (customers will ask) |
| Work with DoD | CMMC / NIST 800-171 / ITAR |
| Don't do any of the above | None (but follow security best practices anyway) |

---

## 🚨 When Things Go Wrong: Incident Response

### Incident Severity Levels

| Severity | Description | Examples | Response Time |
|----------|-------------|----------|---------------|
| **SEV-1** | Critical (active breach, data loss) | System breach, data exfiltration, ransomware | Immediate (call incident response team) |
| **SEV-2** | High (system compromised) | Suspicious activity, potential breach detected | 1 hour |
| **SEV-3** | Medium (potential impact) | Vulnerability discovered, failed login spike | 4 hours |
| **SEV-4** | Low (minor issue) | Policy violation, minor misconfiguration | 1 business day |

---

### Incident Response Process

**1. Detect - Identify Security Incident**

**Signs of Security Incident:**
- Unusual traffic patterns or login attempts
- Security alerts from monitoring tools
- User reports (strange account activity, data missing)
- Downtime or performance issues
- Ransomware messages
- Third-party notification (someone telling you you've been breached)

**What to Do:**
- Don't panic (easier said than done, but important)
- Document everything (times, symptoms, who reported what)
- Activate incident response team
- Don't destroy evidence (don't reboot servers, don't delete logs)

**⏱️ Time:** 0-30 minutes

---

**2. Contain - Limit Incident Impact**

**Goal:** Stop the bleeding, prevent further damage

**Containment Actions:**
- Isolate affected systems (disconnect from network if needed)
- Disable compromised accounts
- Block malicious IPs
- Shut down vulnerable services
- Switch to backup systems (if available)

**⏱️ Time:** 30 minutes - 2 hours

---

**3. Eradicate - Remove Threat**

**Goal:** Remove attacker/threat from your systems

**Eradication Actions:**
- Delete malicious accounts
- Remove malware/backdoors
- Patch vulnerabilities exploited
- Reset all credentials (if passwords compromised)
- Rebuild clean systems (don't trust compromised systems)

**⏱️ Time:** 2 hours - 2 days

---

**4. Recover - Restore Normal Operations**

**Goal:** Get back to business safely

**Recovery Actions:**
- Restore from clean backups
- Reconnect systems to network
- Monitor for suspicious activity (assume attacker might still be present)
- Test all systems before bringing fully online
- Gradually restore functionality (don't flip everything on at once)

**⏱️ Time:** 1 day - 2 weeks

---

**5. Lessons Learned - Post-Incident Review**

**Goal:** Learn from the incident, prevent recurrence

**Timeline:** Within 2 weeks of incident resolution

**Agenda:**
1. What happened? (timeline)
2. Why did it happen? (root cause analysis)
3. How did we respond? (what worked, what didn't)
4. What can we improve? (action items)

**⏱️ Time:** 2-4 hours for meeting, 1-2 days for report

---

##  Security Tools: 2026 Edition

### Tool Recommendations by Category

| Category | Recommended Tools | Free Alternatives | When to Upgrade |
|----------|-------------------|-------------------|-----------------|
| **SAST** | SonarQube, Semgrep | SonarQube Community | When you need enterprise features |
| **DAST** | OWASP ZAP | OWASP ZAP (same) | Upgrade to Burp Suite Pro for advanced features |
| **SCA** | Snyk, Dependabot | Dependabot (GitHub), Snyk free tier | When you need advanced vulnerability management |
| **Container Security** | Trivy | Trivy (same) | Upgrade to Aqua for runtime protection |
| **IaC Security** | Checkov, tfsec | Checkov, tfsec (same) | When you need enterprise policy management |
| **WAF** | CloudFlare, AWS WAF | AWS WAF (with AWS) | Upgrade when you need advanced rules/custom WAF |
| **SIEM** | Splunk, ELK | ELK Stack | When you need enterprise support/advanced analytics |
| **Secrets Management** | AWS Secrets Manager, HashiCorp Vault | AWS Secrets Manager (with AWS) | When you need multi-cloud or advanced features |
| **Auth Providers** | Auth0, Supabase Auth | Supabase Auth (generous free tier) | When you need enterprise SSO/advanced auth features |

---

### Getting Started: Minimal Toolstack

**For Small Teams (1-10 developers, budget-conscious):**

| Tool | Cost | What It's For |
|------|------|---------------|
| **SonarQube Community** | Free | SAST (code scanning) |
| **Dependabot** | Free (on GitHub) | SCA (dependency scanning) |
| **OWASP ZAP** | Free | DAST (web app scanning) |
| **Trivy** | Free | Container scanning |
| **Checkov/tfsec** | Free | IaC scanning |
| **AWS WAF** | $20/month | Web application firewall |
| **AWS Secrets Manager** | Monthly fee | Secrets management |
| **Supabase Auth** | Free (generous tier) | Authentication |
| **ELK Stack** | Free (self-hosted) | Log aggregation |

**Total Monthly Cost:** ~$50-$100

**Setup Timeline:**
- Week 1: SAST (SonarQube) + SCA (Dependabot)
- Week 2: DAST (OWASP ZAP) + Container security (Trivy)
- Week 3: WAF + Secrets management
- Week 4: Log aggregation (ELK) + Monitoring

---

## 🎓 Common Security Pitfalls (And How to Avoid Them)

### Pitfall #1: "We'll Add Security Later"

**The Problem:** Security is treated as an afterthought, added at the end

**Why It's a Problem:**
- 10x more expensive to fix security issues later
- Some security issues require architectural changes (impossible to retrofit)
- You'll likely miss security considerations in the rush to finish

**Emotional Reality:** 😅
> "We're just building an MVP, we don't need security yet."

Six months later, when you're handling real customer data and realize you have no authentication, no encryption, and no audit trail... that's when the panic sets in.

**How to Avoid:**
- Start with security requirements in Phase 2 (before coding)
- Design security into architecture in Phase 3
- Implement security controls during development (Phase 5)
- Never say "later"—say "which phase?"

---

### Pitfall #2: "Security Is Someone Else's Job"

**The Problem:** Developers assume security team will handle security

**Why It's a Problem:**
- Security team can't review every line of code (they'd be bottlenecks)
- Developers understand the code best—they're best positioned to spot security issues
- Security is everyone's responsibility

**Emotional Reality:** 😤
> "I'm just building features. Security is the security team's job."

Then a vulnerability is found in your code, and you're working weekends to fix it while customer data is at risk.

**How to Avoid:**
- Every developer gets basic security training (OWASP Top 10)
- Code reviews include security checks
- Security team provides guidelines/tools, not gatekeeping
- Celebrate developers who catch security issues

---

### Pitfall #3: "Our App Is Too Small to Be Hacked"

**The Problem:** Assuming attackers only go after big targets

**Why It's a Problem:**
- Automated attacks don't care about size—they scan the entire internet
- Small apps are often easier targets (less security)
- Attackers use small apps as stepping stones to bigger targets

**Emotional Reality:** 😌
> "We're just a small startup, who would hack us?"

Automated bots find your app within hours of deployment. They don't care how big you are—they care how vulnerable you are.

**How to Avoid:**
- Assume you're a target from day 1
- Implement basic security (HTTPS, authentication, encryption)
- Monitor for attacks (you'll be surprised how many attempts you see)
- Size doesn't matter—vulnerability does

---

### Pitfall #4: "Compliance Means We're Secure"

**The Problem:** Assuming compliance = security

**Why It's a Problem:**
- Compliance is minimum baseline, not comprehensive security
- Compliance checkboxes can be gamed (passing audit, still insecure)
- Regulations lag behind threats (compliance might miss current threats)

**Emotional Reality:** 🤷
> "We're SOC 2 compliant, we must be secure."

SOC 2 is about having controls and processes. It doesn't mean your controls are effective against current threats. You can pass SOC 2 and still have trivial vulnerabilities.

**How to Avoid:**
- Treat compliance as baseline, not goal
- Go beyond compliance (follow security best practices)
- Regular security assessments (not just compliance audits)
- Continuous security improvement (compliance is snapshot, security is journey)

---

### Pitfall #5: "We Use Encrypted Libraries, We're Secure"

**The Problem:** Assuming libraries = secure implementation

**Why It's a Problem:**
- Encryption is hard to implement correctly (even with good libraries)
- Key management is often the weak point (not the encryption itself)
- Encrypted data can still be leaked (through logs, errors, backups)

**Emotional Reality:** 😰
> "We use AES-256 encryption, we're good."

But your encryption keys are hardcoded in the repository (which is now public on GitHub), or you're encrypting data but logging the unencrypted version.

**How to Avoid:**
- Use established encryption services (AWS KMS, Azure Key Vault) instead of implementing yourself
- Never hardcode keys (use secrets management)
- Review what gets logged (ensure encrypted data stays encrypted)
- Test your encryption (try to decrypt as attacker would)

---

##  Expected Outcomes

By following this security framework, you will:

 **Prevent the most common attacks** (OWASP Top 10, social engineering, credential theft)
 **Detect security incidents quickly** (monitoring, alerting, log analysis)
 **Respond effectively when things go wrong** (incident response process, runbooks, team)
 **Meet compliance requirements** (SOC 2, HIPAA, PCI DSS, GDPR, etc.)
 **Build customer trust** (security is competitive advantage)
 **Sleep better at night** (knowing you've done the work to protect your systems)

**Security is not a destination.** It's a journey of continuous improvement. This framework gives you the map—you just need to walk the path.

---

## 💬 Final Thoughts

**Security is an investment, not an expense.**

Every hour you spend on security:
- Saves 10 hours of incident response later
- Prevents potential fines ($100-$1.5 million per violation)
- Protects your reputation (hard to quantify, but invaluable)
- Builds customer trust (direct revenue impact)

**You don't need to be perfect.** You just need to be thoughtful, consistent, and continuously improving.

**Start somewhere.** Start with authentication. Add encryption. Implement logging. Set up monitoring. Each layer adds protection.

**Ask for help.** Security professionals want to help. Join communities. Attend meetups. Learn from others' mistakes (so you don't repeat them).

**Remember:** Security protects everything you've built. It deserves the investment.

---

##  Resources and Further Learning

### Free Resources

**Learning:**
- **OWASP Top 10:** [owasp.org](https://owasp.org) - Top 10 web security risks
- **NIST Cybersecurity Framework:** [nist.gov/cyberframework](https://www.nist.gov/cyberframework) - Free security framework
- **AWS Security Best Practices:** [aws.amazon.com/security](https://aws.amazon.com/security) - Cloud security guides

**Tools:**
- **OWASP ZAP:** [zaproxy.org](https://www.zaproxy.org) - Free DAST tool
- **SonarQube Community:** [sonarqube.org](https://www.sonarqube.org) - Free SAST tool
- **Trivy:** [aquasecurity.github.io/trivy](https://aquasecurity.github.io/trivy) - Free container scanner

**Communities:**
- **r/netsec on Reddit:** Active security community
- **OWASP Slack:** Security practitioner community
- **Local OWASP chapters:** Free security meetups

---

##  Templates and Checklists

See `./templates/` for:
- **Security Requirements Template** - Document your security requirements
- **Threat Modeling Template** - Conduct structured threat modeling
- **Security Test Plan Template** - Plan comprehensive security testing
- **Incident Response Template** - Be ready when things go wrong
- **Compliance Checklist** - Track your compliance status

---

**This shared skill is referenced by all phase skills.**

---

**Transformed by:** OCTALUME EXPERT MENTOR
**Transformation:** Complete rewrite to Expert Mentor style (warm, story-driven, emotionally intelligent, progressive disclosure, plain language, 2026 trends)

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
