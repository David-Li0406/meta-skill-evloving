# threat-model Research

Research document for the threat modeling skill.

## Phase 1: Upstream Survey

### 1. obra/superpowers Analysis

After analyzing the [obra/superpowers](https://github.com/obra/superpowers) repository, **no dedicated threat modeling or security analysis skills were found**. The framework focuses primarily on development workflow skills including:

- Code review processes with issue severity assessment
- Test-driven development (RED-GREEN-REFACTOR methodology)
- Systematic debugging with 4-phase root cause analysis
- Design, planning, execution, and collaboration workflows

The repository has a Security tab but no specific threat modeling capabilities are documented as part of the skills library.

### 2. VoltAgent/awesome-claude-code-subagents Analysis

The [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) repository contains several security-focused subagents under the "Quality & Security" category (plugin: `voltagent-qa-sec`):

| Subagent | Description |
|----------|-------------|
| **security-auditor** | Security vulnerability expert |
| **penetration-tester** | Ethical hacking specialist |
| **security-engineer** | Infrastructure security specialist |
| **compliance-auditor** | Regulatory compliance expert |
| **ad-security-reviewer** | Active Directory security and GPO audit specialist |
| **powershell-security-hardening** | PowerShell security hardening and compliance specialist |

Related agents include `code-reviewer`, `architect-reviewer`, and `chaos-engineer`. However, **no dedicated threat modeling subagent exists**.

### 3. Other Claude Code Security Plugins

Several relevant tools and plugins exist in the ecosystem:

| Tool | Description | Source |
|------|-------------|--------|
| **anthropics/claude-code-security-review** | Official AI-powered security review GitHub Action using Claude | [GitHub](https://github.com/anthropics/claude-code-security-review) |
| **nelson-muntz** | Claude Code plugin that "thinks like an attacker" with iterative attack loops | [GitHub](https://github.com/zkarimi22/nelson-muntz) |
| **SecureVibes** | Python-based scanner using five specialized AI agents for code security | [CyberPress](https://cyberpress.org/securevibes-new-ai-vulnerabilities/) |
| **Semgrep + Claude** | Integration for finding vulnerabilities in web apps | [Semgrep Blog](https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex/) |

### 4. Upstream Summary

**Gap Identified**: No comprehensive threat modeling skill exists in the Claude Code ecosystem. Existing tools focus on:
- Static vulnerability scanning
- Code review for security issues
- Penetration testing guidance
- Compliance auditing

A dedicated threat modeling skill would fill a significant gap by providing systematic threat identification and risk assessment capabilities.

---

## Phase 2: Research Findings

### 1. STRIDE Threat Modeling Methodology

**Sources:**
- [STRIDE Threat Modeling - Practical DevSecOps](https://www.practical-devsecops.com/what-is-stride-threat-model/)
- [STRIDE Threat Modeling - Threat-Modeling.com](https://threat-modeling.com/stride-threat-modeling/)
- [IriusRisk - STRIDE Methodology](https://www.iriusrisk.com/resources-blog/threat-modeling-methodology-stride)
- [Microsoft Threat Modeling Tool Overview](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
- [STRIDE Model - Wikipedia](https://en.wikipedia.org/wiki/STRIDE_model)
- [Security Compass - STRIDE](https://www.securitycompass.com/blog/stride-in-threat-modeling/)

#### Overview

STRIDE is a threat modeling framework developed by Microsoft in the late 1990s by Praerit Garg and Loren Kohnfelder. It categorizes threats into six types, each corresponding to a core security principle:

| Threat Category | Security Property Violated | Description |
|----------------|---------------------------|-------------|
| **S**poofing | Authenticity | Pretending to be something or someone else (DNS spoofing, ARP spoofing, IP spoofing) |
| **T**ampering | Integrity | Malicious modification of data or systems |
| **R**epudiation | Non-repudiability | Denying having performed an action |
| **I**nformation Disclosure | Confidentiality | Unauthorized access to sensitive data |
| **D**enial of Service | Availability | Making systems unavailable |
| **E**levation of Privilege | Authorization | Gaining unauthorized access levels |

#### STRIDE Template

```markdown
## STRIDE Analysis for [Component Name]

### Component Description
[Brief description of the component being analyzed]

### Threat Analysis

#### Spoofing
- [ ] Can an attacker impersonate a legitimate user?
- [ ] Are authentication mechanisms properly implemented?
- [ ] Is there protection against session hijacking?

#### Tampering
- [ ] Can data be modified in transit?
- [ ] Can stored data be altered without detection?
- [ ] Are integrity checks in place?

#### Repudiation
- [ ] Are all security-relevant actions logged?
- [ ] Can users deny performing actions?
- [ ] Is there adequate audit trail?

#### Information Disclosure
- [ ] Is sensitive data encrypted at rest?
- [ ] Is sensitive data encrypted in transit?
- [ ] Are error messages leaking information?

#### Denial of Service
- [ ] Is there rate limiting?
- [ ] Are resources bounded?
- [ ] Is there protection against resource exhaustion?

#### Elevation of Privilege
- [ ] Is principle of least privilege followed?
- [ ] Are authorization checks performed at every level?
- [ ] Is input validation preventing injection attacks?
```

#### Best Practices for Developers

1. **Apply Early**: Perform STRIDE analysis during design phase before code is written
2. **Iterate Continuously**: Re-assess when migrating to multi-cloud, refactoring core components, or adjusting IAM policies
3. **Map to Trust Boundaries**: Apply STRIDE per element at trust boundary crossings
4. **Combine with DREAD**: Use DREAD scoring to prioritize identified STRIDE threats
5. **Document Mitigations**: For each threat, document specific countermeasures

---

### 2. Microsoft Threat Modeling Tool and Approach

**Sources:**
- [Microsoft Threat Modeling Tool - Getting Started](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started)
- [Microsoft Threat Modeling Tool Feature Overview](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-feature-overview)
- [Microsoft SDL Threat Modeling](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- [Create Threat Model Using DFD Elements](https://learn.microsoft.com/en-us/training/modules/tm-create-a-threat-model-using-foundational-data-flow-diagram-elements/)

#### Core Approach

Microsoft's threat modeling methodology consists of four main phases:

1. **Create an Application Diagram** - Model the system using Data Flow Diagrams
2. **Identify Threats** - Use STRIDE-per-element analysis
3. **Mitigate Threats** - Develop and implement countermeasures
4. **Validate Mitigations** - Verify threats have been addressed

#### Key Features of Microsoft Threat Modeling Tool

| Feature | Description |
|---------|-------------|
| **Design View** | Create data flow diagrams of the project |
| **Analysis View** | Generate STRIDE-based threat lists automatically |
| **Trust Boundaries** | Red dotted lines showing where trust levels change |
| **Template System** | Pre-built templates for common scenarios |
| **Threat Generation** | Automated threat suggestions based on diagram elements |
| **Reporting** | Security activity and testing verification reports |

#### Design Philosophy

- **Software-Centered**: Builds on activities developers are familiar with (drawing architecture diagrams)
- **Non-Security Expert Friendly**: Designed to be accessible to all developers
- **Layered Diagrams**: Recommends diagrams be layered to preserve relevance without overwhelming detail
- **Standard Notation**: Uses consistent notation for system components, data flows, and security boundaries

#### Microsoft SDL Integration

The tool is a core element of the Microsoft Security Development Lifecycle (SDL), helping teams:
- Shape application design based on security requirements
- Meet company security objectives
- Reduce risk systematically
- Define security requirements from identified threats

---

### 3. Attack Trees and Threat Diagrams

**Sources:**
- [Attack Trees - Schneier on Security](https://www.schneier.com/academic/archives/1999/12/attack_trees.html)
- [Attack Trees - Wikipedia](https://en.wikipedia.org/wiki/Attack_tree)
- [NCSC - Using Attack Trees](https://www.ncsc.gov.uk/collection/risk-management/using-attack-trees-to-understand-cyber-security-risk)
- [Security Compass - How to Use Attack Trees](https://www.securitycompass.com/blog/how-to-use-attack-trees/)
- [Practical DevSecOps - Attack Trees Guide](https://www.practical-devsecops.com/threat-modeling-using-attack-trees/)
- [Attack Trees Threat Modeling](https://threat-modeling.com/attack-trees-threat-modeling/)

#### Overview

Attack trees provide a formal, methodical way of describing security of systems based on varying attacks. The goal is represented as the root node, with different ways of achieving that goal as leaf nodes.

#### Structure

```
                    [Root: Attacker Goal]
                           |
              -------------------------
              |                       |
         [OR: Method 1]          [OR: Method 2]
              |                       |
        -------------           -------------
        |           |           |           |
   [AND: Step A] [AND: Step B]  [Leaf]    [Leaf]
```

**Node Types:**
- **OR Nodes**: Alternative methods (attacker needs only ONE to succeed)
- **AND Nodes**: Sequential steps (attacker needs ALL to succeed)

#### Attack Tree Example Template

```markdown
## Attack Tree: [Goal Name]

### Root Goal
[Describe the attacker's ultimate objective]

### Level 1 - Primary Attack Vectors (OR)
1. **Vector A**: [Description]
2. **Vector B**: [Description]
3. **Vector C**: [Description]

### Level 2 - Sub-goals for Vector A (AND/OR)
1.1. [Sub-step required] (AND)
1.2. [Alternative approach] (OR)

### Risk Assessment
| Node | Likelihood | Impact | Difficulty | Cost |
|------|------------|--------|------------|------|
| 1.1  | High       | Critical| Low       | $    |
| 1.2  | Medium     | High   | Medium     | $$   |

### Recommended Mitigations
- [Mitigation for highest-risk paths]
```

#### Benefits

- **Structure**: Repeatable, logical breakdown of threats
- **Clarity**: Complex threats visualized for technical and non-technical audiences
- **Prioritization**: Assign values (cost, likelihood, complexity) for effective mitigation prioritization
- **Reusability**: Capture and reuse expertise about security

#### Integration with Other Methodologies

Attack trees integrate with:
- **STRIDE**: Threats become root nodes
- **MITRE ATT&CK**: Operational threat modeling
- **PASTA**: Created during Stage 4 (Threat Analysis)
- **Trike**: Discovered threats become attack tree root nodes

---

### 4. Data Flow Diagrams for Security Analysis

**Sources:**
- [Practical DevSecOps - Threat Modeling DFDs](https://www.practical-devsecops.com/threat-modeling-data-flow-diagrams/)
- [Threat-Modeling.com - DFDs in Threat Modeling](https://threat-modeling.com/data-flow-diagrams-in-threat-modeling/)
- [Microsoft Learn - Create Threat Model Using DFD](https://learn.microsoft.com/en-us/training/modules/tm-create-a-threat-model-using-foundational-data-flow-diagram-elements/)
- [ERNI - Data Flow and Threat Modelling Guide](https://www.betterask.erni/data-flow-threat-modelling-and-risk-analysis-a-practical-guide-for-cybersecurity-professionals/)
- [OWASP - Threat Modeling Process](https://owasp.org/www-community/Threat_Modeling_Process)

#### DFD Components

| Component | Symbol | Description |
|-----------|--------|-------------|
| **Process** | Circle/Rounded Rectangle | Applications that apply logic and/or change data |
| **Data Store** | Two parallel lines or Cylinder | Storage locations (databases, files) |
| **External Entity/Interactor** | Rectangle | Endpoints (users, external systems) outside system scope |
| **Data Flow** | Arrow | Movement of data between components |
| **Trust Boundary** | Dotted Line/Rectangle | Boundary between different trust zones |

#### Trust Boundaries

Trust boundaries are critical for security analysis because:
- Calls crossing them often need authentication and authorization
- Data crossing may need to be treated as untrusted and validated
- Business/regulatory rules may restrict data flow (HIPAA, data sovereignty)
- They indicate attack surfaces where attackers can interject

**Types of Trust Boundaries:**
- Machine boundaries
- Privilege boundaries
- Integrity boundaries
- Network boundaries (internal/external)

#### DFD Template for Security Analysis

```markdown
## Data Flow Diagram: [System Name]

### System Boundaries
- **In Scope**: [Components within analysis boundary]
- **Out of Scope**: [External dependencies not analyzed]

### External Entities
| ID | Entity | Description | Trust Level |
|----|--------|-------------|-------------|
| E1 | User   | End user    | Untrusted   |
| E2 | Admin  | Administrator| Trusted    |

### Processes
| ID | Process | Description | Trust Zone |
|----|---------|-------------|------------|
| P1 | Web App | Frontend    | DMZ        |
| P2 | API     | Backend     | Internal   |

### Data Stores
| ID | Store | Data Type | Sensitivity |
|----|-------|-----------|-------------|
| D1 | UserDB| PII       | High        |
| D2 | Logs  | Audit     | Medium      |

### Data Flows
| ID | From | To | Data | Crosses Trust Boundary? |
|----|------|-----|------|------------------------|
| F1 | E1   | P1  | Credentials | Yes (Internet to DMZ) |
| F2 | P1   | P2  | API Requests| Yes (DMZ to Internal) |

### Trust Boundaries Identified
1. **TB1**: Internet / DMZ boundary
2. **TB2**: DMZ / Internal Network boundary
3. **TB3**: Application / Database boundary
```

#### Best Practices

1. **Define System Boundaries**: Clearly outline what's in and out of scope
2. **Identify All Data Flows**: Visualize where data enters, moves, and lands
3. **Mark Trust Boundaries**: Show where trust levels change
4. **Think Like an Attacker**: Consider threats at each stage
5. **Keep It Simple**: Use limited symbols for broad understanding
6. **Layer Appropriately**: Don't go overboard on detail but provide relevant context

---

### 5. Threat Modeling Automation Tools

**Sources:**
- [OWASP pytm - GitHub](https://github.com/OWASP/pytm)
- [OWASP pytm - Foundation Page](https://owasp.org/www-project-pytm/)
- [pytm - OWASP Developer Guide](https://devguide.owasp.org/en/04-design/01-threat-modeling/02-pytm/)
- [Threagile - GitHub](https://github.com/Threagile/threagile)
- [Threagile.io](https://threagile.io/)
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
- [Threat Dragon - GitHub](https://github.com/OWASP/threat-dragon)
- [Threatspec - GitHub](https://github.com/threatspec/threatspec)

#### Tool Comparison

| Tool | Approach | Language | Key Features |
|------|----------|----------|--------------|
| **OWASP pytm** | Threat Modeling WITH Code | Python | Define system in Python, auto-generate DFDs and threats |
| **Threatspec** | Threat Modeling IN Code | Multi-language | Inline code comments/annotations |
| **Threagile** | Threat Model as Code | YAML/Go | Declarative YAML, DevSecOps integration |
| **OWASP Threat Dragon** | Visual Diagramming | Web/Desktop | Drag-and-drop DFD creation, STRIDE/LINDDUN support |
| **Microsoft TMT** | Visual Diagramming | Windows | Enterprise templates, Azure integration |

#### OWASP pytm

```python
# Example pytm model
from pytm import TM, Server, Datastore, Dataflow, Boundary, Actor

tm = TM("My Application")
tm.description = "Threat model for my web application"

internet = Boundary("Internet")
internal = Boundary("Internal Network")

user = Actor("User")
user.inBoundary = internet

web_server = Server("Web Server")
web_server.inBoundary = internal
web_server.protocol = "HTTPS"

database = Datastore("Database")
database.inBoundary = internal
database.isSQL = True

user_to_web = Dataflow(user, web_server, "User Request")
user_to_web.protocol = "HTTPS"

web_to_db = Dataflow(web_server, database, "DB Query")
web_to_db.protocol = "SQL"

tm.process()
```

**pytm Benefits:**
- Version control alongside code
- Automated threat generation
- DFD and sequence diagram output
- pytmGPT integration for AI-assisted modeling

#### Threagile

```yaml
# Example Threagile model
threagile_version: 1.0.0

title: My Application Threat Model
author:
  name: Security Team

technical_assets:
  Web Application:
    id: web-app
    description: Frontend web application
    type: process
    usage: business
    technologies:
      - web-application
    
  Database:
    id: database
    description: PostgreSQL database
    type: datastore
    usage: business
    technologies:
      - postgresql

trust_boundaries:
  DMZ:
    id: dmz
    description: DMZ network
    type: network-cloud-provider
    technical_assets_inside:
      - web-app

communication_links:
  Web to Database:
    source_id: web-app
    target_id: database
    protocol: sql-access-protocol
    authentication: credentials
```

#### OWASP Threat Dragon

**Key Features:**
- Desktop app (Windows, Linux, MacOS) or web application
- Supports STRIDE, LINDDUN, CIA, DIE, PLOT4ai frameworks
- Rule engine for auto-generated threats
- PDF report generation for compliance
- GitHub integration for model storage
- OWASP Automated Threats (OATS) suggestions

---

### 6. Security User Stories and Abuse Cases

**Sources:**
- [OWASP Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html)
- [DZone - Adding AppSec to Agile](https://dzone.com/articles/adding-appsec-agile-security)
- [SAFECode - Practical Security Stories for Agile](https://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf)
- [Rietta - What is an Abuser Story](https://rietta.com/blog/what-is-an-abuser-story-software/)
- [we45 - Abuser Stories for Scrum Teams](https://www.we45.com/post/abuser-stories-a-sneak-peak-for-scrum-teams)

#### Concepts

| Term | Definition |
|------|------------|
| **Abuse Case** | Describes how attackers misuse or exploit weaknesses in controls |
| **Abuser Story** | User story from the perspective of a malicious adversary |
| **Evil User Story** | Negative cases the team needs to consider during implementation |
| **Misuse Case** | How users misuse software features to attack an application |

#### Abuser Story Template

```markdown
## Abuser Story: [Threat Name]

**As a** [malicious actor type],
**I want to** [malicious action],
**So that** [attacker's goal/benefit].

### Example Stories

**As a** malicious user,
**I want to** send SQL injection in form fields,
**So that** I can access unauthorized data.

**As a** hacker,
**I want to** enumerate valid usernames via login error messages,
**So that** I can perform targeted credential attacks.

**As a** disgruntled employee,
**I want to** access another user's account data,
**So that** I can steal or modify their information.
```

#### Evil User Story Examples

From Johan Peeters (2008) and subsequent adaptations:

1. "As a hacker, I can send bad data in URLs, so I can access data and functions for which I'm not authorized."
2. "As a hacker, I can send bad data in the content of requests, so I can access data and functions for which I'm not authorized."
3. "As a hacker, I can intercept network traffic so I can steal credentials and session tokens."
4. "As a hacker, I can exploit weak session management so I can hijack user sessions."

#### Security Story Integration in Agile

```markdown
## User Story with Security Acceptance Criteria

**Title**: User Login

**As a** registered user,
**I want to** log into my account,
**So that** I can access my personal dashboard.

### Acceptance Criteria
- [ ] Login form accepts email and password
- [ ] Successful login redirects to dashboard
- [ ] Invalid credentials show generic error message

### Security Acceptance Criteria (derived from Abuser Stories)
- [ ] Failed login attempts are rate-limited (max 5/minute)
- [ ] Account lockout after 10 failed attempts
- [ ] Passwords are transmitted over HTTPS only
- [ ] Session tokens use secure, HttpOnly cookies
- [ ] Error messages do not reveal if email exists
- [ ] All login attempts are logged with timestamp and IP
```

#### Best Practices

1. **Workshop Integration**: Create abuser stories after sprint planning when user stories are defined
2. **Security Champion**: Have security-aware team member guide initial sessions
3. **Backlog Management**: Add security stories to product backlog for prioritization
4. **Definition of Done**: Include security acceptance criteria in DoD
5. **Automated Testing**: Convert abuser stories into security test cases

---

### 7. Risk Assessment Frameworks (CVSS, DREAD)

**Sources:**
- [MainNerve - DREAD vs CVSS](https://mainnerve.com/pen-testing-risk-rating-frameworks/)
- [Medium - DREAD Framework Case Study](https://medium.com/@Readsec/risk-assessment-using-the-dread-framework-a-case-study-on-cve-2025-21298-2dc8c852b473)
- [Software Secured - STRIDE vs DREAD vs PASTA](https://www.softwaresecured.com/post/comparison-of-stride-dread-pasta)
- [Infosec Institute - DREAD Model](https://resources.infosecinstitute.com/topic/qualitative-risk-analysis-dread-model/)
- [LinkedIn - CVSS, DREAD, STRIDE, PASTA Overview](https://www.linkedin.com/pulse/evaluating-security-risks-overview-cvss-dread-stride-pasta-astori)
- [InfoSecurity Europe - Beyond CVSS](https://www.infosecurityeurope.com/en-gb/blog/future-thinking/new-frameworks-vulnerability-risk-assessment.html)

#### DREAD Framework

DREAD was introduced by Microsoft in 2002 for threat prioritization:

| Factor | Description | Scoring (1-3) |
|--------|-------------|---------------|
| **D**amage | How bad is the impact? | 1=Low, 2=Medium, 3=High |
| **R**eproducibility | How easy to reproduce? | 1=Hard, 2=Sometimes, 3=Always |
| **E**xploitability | How easy to execute? | 1=Hard, 2=Medium, 3=Easy |
| **A**ffected Users | How many users impacted? | 1=Few, 2=Some, 3=All |
| **D**iscoverability | How easy to find? | 1=Hard, 2=Medium, 3=Easy |

**DREAD Score Calculation:**
```
Risk Score = (D + R + E + A + D) / 5
```

**Risk Levels:**
- **High Risk**: 2.5 - 3.0
- **Medium Risk**: 1.5 - 2.4
- **Low Risk**: 1.0 - 1.4

#### DREAD Template

```markdown
## DREAD Assessment: [Vulnerability Name]

### Threat Description
[Describe the threat/vulnerability]

### DREAD Scoring

| Factor | Score | Justification |
|--------|-------|---------------|
| Damage | [1-3] | [Explanation] |
| Reproducibility | [1-3] | [Explanation] |
| Exploitability | [1-3] | [Explanation] |
| Affected Users | [1-3] | [Explanation] |
| Discoverability | [1-3] | [Explanation] |

**Total Score**: [X.X] / 3.0
**Risk Level**: [High/Medium/Low]

### Recommended Priority
[Based on score, recommend mitigation timeline]
```

#### CVSS (Common Vulnerability Scoring System)

CVSS 4.0 (released July 2023) uses three metric groups:

**Base Metrics (6 factors):**
- Attack Vector (AV)
- Attack Complexity (AC)
- Attack Requirements (AR)
- Privileges Required (PR)
- User Interaction (UI)
- Vulnerable System Impact (Confidentiality, Integrity, Availability)

**Temporal Metrics (3 factors):**
- Exploit Code Maturity
- Remediation Level
- Report Confidence

**Environmental Metrics (5 factors):**
- Modified Base Metrics
- Confidentiality/Integrity/Availability Requirements

**CVSS Score Ranges:**
| Score | Severity |
|-------|----------|
| 0.0 | None |
| 0.1 - 3.9 | Low |
| 4.0 - 6.9 | Medium |
| 7.0 - 8.9 | High |
| 9.0 - 10.0 | Critical |

#### Comparison: CVSS vs DREAD

| Aspect | CVSS | DREAD |
|--------|------|-------|
| **Complexity** | High (14 metric groups) | Simple (5 factors) |
| **Standardization** | Industry standard | Qualitative, organization-specific |
| **Best For** | Technical vulnerability assessment | Quick risk triage |
| **Audience** | Security engineers | Mixed technical/business |
| **Maintenance** | Static (requires reassessment) | Flexible, contextual |

#### Hybrid Approach

Many organizations use both:
1. **CVSS** for technical severity baseline
2. **DREAD** for contextual business risk assessment
3. **Risk Matrix** combining both scores for final prioritization

---

### 8. Additional Methodologies

#### PASTA (Process for Attack Simulation and Threat Analysis)

**Sources:**
- [PASTA Threat Modeling - Threat-Modeling.com](https://threat-modeling.com/pasta-threat-modeling/)
- [IriusRisk - PASTA Methodology](https://www.iriusrisk.com/resources-blog/pasta-threat-modeling-methodologies)
- [VerSprite - PASTA Threat Modeling](https://versprite.com/blog/what-is-pasta-threat-modeling/)
- [Drata - PASTA Tutorial](https://drata.com/grc-central/risk/pasta-threat-modeling)

PASTA is a seven-stage, risk-centric methodology developed by Tony UcedaVélez and Marco M. Morana (2015):

| Stage | Name | Purpose |
|-------|------|---------|
| 1 | Define Objectives | Align security with business goals |
| 2 | Define Technical Scope | Identify what we're protecting |
| 3 | Application Decomposition | Break down application architecture |
| 4 | Threat Analysis | Create attack trees, identify threats |
| 5 | Vulnerability Analysis | Identify weaknesses supporting threat assertions |
| 6 | Attack Modeling | Simulate attacks on identified weaknesses |
| 7 | Risk & Impact Analysis | Define countermeasures, reduce risk |

**Key Benefits:**
- Scalable for growing businesses
- Cross-team collaboration
- Attacker-focused perspective
- Compatible with Agile/DevOps workflows

#### LINDDUN (Privacy Threat Modeling)

**Sources:**
- [linddun.org](https://linddun.org/)
- [NIST - LINDDUN Framework](https://www.nist.gov/privacy-framework/linddun-privacy-threat-modeling-framework)
- [Security Compass - LINDDUN](https://www.securitycompass.com/blog/linddun-threat-modeling/)
- [Threat-Modeling.com - LINDDUN](https://threat-modeling.com/linddun-threat-modeling/)

LINDDUN addresses privacy threats that STRIDE doesn't cover:

| Threat | Description |
|--------|-------------|
| **L**inking | Combining data to learn more about individuals |
| **I**dentifying | Learning identity through data |
| **N**on-repudiation | Inability to deny actions (privacy violation) |
| **D**etecting | Distinguishing if item of interest exists |
| **D**ata Disclosure | Exposure of personal data |
| **U**nawareness | Insufficient privacy impact feedback |
| **N**on-compliance | Not following privacy best practices |

**Three Implementation Methods:**
- **LINDDUN Go**: Lean, game-based team approach
- **LINDDUN Pro**: Systematic with DFD usage
- **LINDDUN Maestro**: Exhaustive threat-specific analysis

---

## Audit Checklist Summary

### Critical Items

| Item | Description | Related Methodology |
|------|-------------|---------------------|
| [ ] **Trust Boundary Identification** | Identify and document all trust boundaries in the system | DFD, STRIDE |
| [ ] **Authentication at Boundaries** | Verify authentication for all trust boundary crossings | STRIDE (Spoofing) |
| [ ] **Data Flow Encryption** | Ensure sensitive data is encrypted in transit across boundaries | STRIDE (Information Disclosure) |
| [ ] **Input Validation** | Validate all input at trust boundary entry points | STRIDE (Tampering, Elevation of Privilege) |
| [ ] **Privilege Separation** | Implement least privilege for all components | STRIDE, DREAD |
| [ ] **Critical Asset Identification** | Identify and prioritize protection of high-value assets | PASTA, Attack Trees |
| [ ] **High-Risk Path Mitigation** | Address attack tree paths with highest likelihood/impact | Attack Trees, DREAD |

### Important Items

| Item | Description | Related Methodology |
|------|-------------|---------------------|
| [ ] **Audit Logging** | Log all security-relevant actions with tamper protection | STRIDE (Repudiation) |
| [ ] **Rate Limiting** | Implement rate limiting for authentication and API endpoints | STRIDE (DoS) |
| [ ] **Session Management** | Secure session tokens with proper expiration and rotation | STRIDE (Spoofing) |
| [ ] **Error Handling** | Ensure error messages don't leak sensitive information | STRIDE (Information Disclosure) |
| [ ] **Dependency Analysis** | Review third-party components for known vulnerabilities | CVSS, DREAD |
| [ ] **Abuser Story Coverage** | Create abuser stories for all critical user stories | Agile Security |
| [ ] **Privacy Impact Assessment** | Evaluate data linking, identification, and disclosure risks | LINDDUN |

### Recommended Items

| Item | Description | Related Methodology |
|------|-------------|---------------------|
| [ ] **Threat Model Documentation** | Maintain versioned threat model alongside code | pytm, Threagile |
| [ ] **DFD Currency** | Keep data flow diagrams updated with architecture changes | DFD, Microsoft TMT |
| [ ] **CVSS Baseline** | Establish CVSS scoring for identified vulnerabilities | CVSS |
| [ ] **Attack Tree Library** | Build reusable attack trees for common attack patterns | Attack Trees |
| [ ] **Security Acceptance Criteria** | Include security criteria in Definition of Done | Agile Security |
| [ ] **Automated Threat Generation** | Use pytm or Threagile for automated threat identification | pytm, Threagile |
| [ ] **Regular Re-assessment** | Schedule threat model reviews for major changes | All methodologies |
| [ ] **Cross-Team Review** | Include developers, security, and business stakeholders | PASTA, OWASP |
| [ ] **Compliance Mapping** | Map threats to regulatory requirements (GDPR, HIPAA, SOC2) | LINDDUN, STRIDE |
| [ ] **Tool Integration** | Integrate threat modeling into CI/CD pipeline | Threagile, pytm |

---

## Summary of Key Resources

### Official Documentation
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [OWASP Developer Guide - Threat Modeling](https://devguide.owasp.org/en/04-design/01-threat-modeling/)
- [Microsoft SDL Threat Modeling](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- [Microsoft Threat Modeling Tool](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)

### Tools
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
- [OWASP pytm](https://github.com/OWASP/pytm)
- [Threagile](https://github.com/Threagile/threagile)
- [Anthropic Claude Code Security Review](https://github.com/anthropics/claude-code-security-review)

### Frameworks
- [linddun.org - Privacy Threat Modeling](https://linddun.org/)
- [NIST LINDDUN Framework](https://www.nist.gov/privacy-framework/linddun-privacy-threat-modeling-framework)
- [SEI CMU - 12 Threat Modeling Methods](https://www.sei.cmu.edu/blog/threat-modeling-12-available-methods/)

### Training
- [Microsoft Learn - Threat Modeling Fundamentals](https://learn.microsoft.com/en-us/training/paths/tm-threat-modeling-fundamentals/)
- [Practical DevSecOps - STRIDE](https://www.practical-devsecops.com/what-is-stride-threat-model/)
- [Shostack + Associates - Beginner's Guide](https://shostack.org/resources/threat-modeling)
