# Compliance Frameworks Reference

A pragmatic guide to major security and compliance frameworks for architecture decisions.

## NIST Cybersecurity Framework (CSF)

**Purpose**: Risk-based approach to managing cybersecurity across critical infrastructure

### Five Core Functions:
1. **Identify**: Asset management, business environment, governance, risk assessment, risk strategy
2. **Protect**: Access control, awareness training, data security, protective technology
3. **Detect**: Anomalies, continuous monitoring, detection processes
4. **Respond**: Response planning, communications, analysis, mitigation, improvements
5. **Recover**: Recovery planning, improvements, communications

**When to Use**: U.S. organizations, critical infrastructure, federal contractors, or any organization wanting a flexible security framework

**Architecture Impact**: Informs defense-in-depth strategy, guides security control selection across lifecycle

## ISO 27001

**Purpose**: International standard for Information Security Management Systems (ISMS)

### Key Components:
- **Annex A**: 93 security controls across 14 domains (organizational, people, physical, technological)
- **PDCA Cycle**: Plan-Do-Check-Act for continuous improvement
- **Risk-Based Approach**: Tailor controls based on organizational risk assessment

**When to Use**: Global operations, European clients, enterprise security programs, certification requirements

**Architecture Impact**: Requires documented policies, risk assessments, and evidence of control implementation

## SOC 2 (Trust Service Criteria)

**Purpose**: Report on controls relevant to security, availability, processing integrity, confidentiality, or privacy

### Five Trust Service Criteria:
1. **Security**: Protection against unauthorized access (logical and physical)
2. **Availability**: System availability for operation and use as committed
3. **Processing Integrity**: System processing is complete, valid, accurate, timely, authorized
4. **Confidentiality**: Information designated as confidential is protected
5. **Privacy**: Personal information is collected, used, retained, disclosed, and disposed per commitments

**When to Use**: SaaS companies, B2B platforms, startups seeking enterprise customers, vendors requiring third-party assurance

**Architecture Impact**: Emphasizes access controls, monitoring, change management, encryption, audit logging

## PCI DSS (Payment Card Industry Data Security Standard)

**Purpose**: Secure credit card transactions and protect cardholder data

### 12 Requirements Across 6 Goals:
1. Build and maintain secure network (firewalls, secure configs)
2. Protect cardholder data (encryption, strong crypto)
3. Maintain vulnerability management program (antivirus, secure code)
4. Implement strong access control (need-to-know, unique IDs, physical access)
5. Regularly monitor and test networks (logging, testing, monitoring)
6. Maintain information security policy

**When to Use**: Any system that stores, processes, or transmits cardholder data

**Architecture Impact**: Network segmentation required, strict encryption standards, comprehensive logging, quarterly scans

## GDPR (General Data Protection Regulation)

**Purpose**: EU regulation for data protection and privacy

### Key Principles:
- **Lawfulness, Fairness, Transparency**: Clear legal basis and purpose
- **Purpose Limitation**: Data only for specified purposes
- **Data Minimization**: Only necessary data collected
- **Accuracy**: Keep data accurate and current
- **Storage Limitation**: No longer than necessary
- **Integrity and Confidentiality**: Appropriate security
- **Accountability**: Demonstrate compliance

**When to Use**: Processing EU residents' personal data

**Architecture Impact**: Privacy by design, data encryption, breach notification within 72 hours, right to erasure, data portability

## HIPAA (Health Insurance Portability and Accountability Act)

**Purpose**: Protect sensitive patient health information (PHI) in the U.S.

### Security Rule Requirements:
- **Administrative Safeguards**: Security management, workforce training, contingency plans
- **Physical Safeguards**: Facility access, workstation security, device/media controls
- **Technical Safeguards**: Access control, audit logs, integrity controls, transmission security

**When to Use**: Healthcare providers, health plans, healthcare clearinghouses, business associates

**Architecture Impact**: Encryption required for data at rest and in transit, audit logs, access controls, BAAs with vendors

## CIS Controls (Center for Internet Security)

**Purpose**: 18 prioritized cybersecurity best practices

### Implementation Groups (IG1, IG2, IG3):
- **IG1** (Basic): Small organizations, limited IT/security staff - 56 safeguards
- **IG2** (Intermediate): Medium organizations, multiple security roles - 74 additional safeguards  
- **IG3** (Advanced): Large organizations, dedicated security teams - 23 additional safeguards

### Top 5 Controls:
1. Inventory and Control of Enterprise Assets
2. Inventory and Control of Software Assets
3. Data Protection
4. Secure Configuration of Enterprise Assets and Software
5. Account Management

**When to Use**: Practical, prioritized security implementation for any organization

**Architecture Impact**: Asset inventory systems, configuration management, vulnerability scanning, log aggregation

## MITRE ATT&CK Framework

**Purpose**: Knowledge base of adversary tactics and techniques based on real-world observations

### Structure:
- **Tactics**: The "why" - adversary's tactical goal (Initial Access, Execution, Persistence, etc.)
- **Techniques**: The "how" - methods used to achieve tactics (Phishing, Exploit Public-Facing App, etc.)
- **Sub-techniques**: Specific implementations of techniques

**When to Use**: Threat modeling, security testing, detection engineering, gap analysis

**Architecture Impact**: Informs detection and response capabilities, validates security controls against known adversary behaviors

## Framework Mapping Strategy

When designing security architecture:

1. **Identify Applicable Frameworks**: Based on industry, geography, customer requirements
2. **Map Controls**: Create traceability matrix showing how architecture satisfies each control
3. **Prioritize Overlaps**: Focus on controls common across multiple frameworks
4. **Document Gaps**: Identify areas where current architecture doesn't meet requirements
5. **Remediation Plan**: Prioritize gaps by risk and compliance deadlines

**Example Control Overlap:**
- NIST PR.AC-1 (Identities and credentials managed) ↔ ISO 27001 A.9.2.1 (User registration) ↔ SOC 2 CC6.1 (Logical access controls)

All three require strong identity management - implement once, satisfy multiple frameworks.

## Common Architecture Patterns for Compliance

**Pattern 1: Defense in Depth**
Satisfies: All frameworks require layered security

**Pattern 2: Zero Trust**
Satisfies: NIST CSF, SOC 2, CIS Controls (strong access control requirements)

**Pattern 3: Data-Centric Security**
Satisfies: GDPR, HIPAA, PCI DSS (data protection mandates)

**Pattern 4: Continuous Monitoring**
Satisfies: All frameworks require detection and monitoring capabilities

**Pattern 5: Secure Development Lifecycle**
Satisfies: SOC 2, ISO 27001, PCI DSS (secure change management)

---

**Key Insight**: Compliance frameworks are not checklist exercises - they're blueprints for building resilient, trustworthy systems. Treat them as architectural constraints that guide design decisions, not administrative burdens retrofitted after the fact.