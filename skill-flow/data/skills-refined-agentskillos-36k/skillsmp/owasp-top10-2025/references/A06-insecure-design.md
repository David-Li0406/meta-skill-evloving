# A06 Insecure Design

## Background

Insecure Design has moved from **4th to 6th** place due to the rise of Security Misconfiguration and Supply Chain Failures. Introduced in 2021, this category addresses **"design and architecture flaws"** rather than implementation defects.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 39 |
| Max Incidence Rate | 22.18% |
| Max Coverage | 88.76% |
| Total Occurrences | 729,882 |
| Total CVEs | 7,647 |

### Key Vulnerability Areas
- Unprotected Credential Storage
- Improper Privilege Management
- Unrestricted File Upload
- Trust Boundary Violation
- Insufficiently Protected Credentials

## Description

Insecure Design represents **"missing or ineffective control design"**.

### Important Distinction
> There is a difference between having a secure design with poor implementation and having no secure design at all. The latter cannot be fixed by perfect coding. Protection controls were never designed in the first place.

### Three Foundational Elements

#### 1. Requirements and Resource Management
Business must specify protection requirements for confidentiality, integrity, availability, and authenticity. Plans should include budgets from design through operations, including tenant isolation, technical specifications, and security activities.

#### 2. Secure Design
Continuous threat assessment integrated into the development cycle is required. Teams should analyze data flows, access controls, user story flows, and failure states. Security is a methodology, not an add-on tool.

#### 3. Secure Development Lifecycle
Organizations need established practices including threat modeling, design patterns, component libraries, tools, and post-mortem analysis. OWASP SAMM (Software Assurance Maturity Model) provides structure for secure development efforts.

## How to Prevent

1. **Establish Secure Development Lifecycle**: Establish secure development lifecycle with AppSec professionals who evaluate security controls
2. **Create Secure Design Patterns and Standardized Component Libraries**
3. **Apply Threat Modeling**: Apply threat modeling to authentication, access control, business logic, and critical flows
4. **Use Threat Modeling as Educational Tool**: Use threat modeling as educational tool to promote security mindset
5. **Integrate Security Language into User Stories**
6. **Implement Plausibility Checks at All Application Layers**
7. **Develop Unit and Integration Tests for Critical Flows Against Threat Model**
8. **Segregate System Layers Based on Exposure and Protection Needs**
9. **Implement Strong Tenant Separation by Design at All Layers**

## Example Attack Scenarios

### Scenario #1: Credential Recovery Using Security Questions
```
Using security questions for credential recovery
violates NIST 800-63b, OWASP ASVS and Top 10 standards.
Multiple people may know the answers, so
this mechanism should be replaced with stronger alternatives.
```

### Scenario #2: Movie Theater Chain Group Booking
```
A movie theater chain allows group bookings with 15-person limit without deposit.
Attackers can exploit business logic to reserve
600 seats simultaneously across multiple locations,
causing significant revenue loss due to flawed application design.
```

### Scenario #3: E-commerce Site Bot Protection
```
An e-commerce site without bot protection
allows scalpers to purchase limited inventory (high-end video cards),
damaging retailer reputation and consumer goodwill.
Anti-bot logic and domain rules identifying
suspiciously fast purchases provide mitigation.
```

## References

- [OWASP Cheat Sheet: Secure Design Principles](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html)
- [OWASP SAMM: Design | Secure Architecture](https://owaspsamm.org/model/design/secure-architecture/)
- [OWASP SAMM: Design | Threat Assessment](https://owaspsamm.org/model/design/threat-assessment/)
- [NIST Guidelines on Minimum Standards for Developer Verification of Software](https://www.nist.gov/publications)
- [The Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/)
- [Awesome Threat Modeling (GitHub repository)](https://github.com/hysnsec/awesome-threat-modelling)

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-73](https://cwe.mitre.org/data/definitions/73.html) | External Control of File Name or Path |
| [CWE-183](https://cwe.mitre.org/data/definitions/183.html) | Permissive List of Allowed Inputs |
| [CWE-256](https://cwe.mitre.org/data/definitions/256.html) | Unprotected Storage of Credentials |
| [CWE-266](https://cwe.mitre.org/data/definitions/266.html) | Incorrect Privilege Assignment |
| [CWE-269](https://cwe.mitre.org/data/definitions/269.html) | Improper Privilege Management |
| [CWE-286](https://cwe.mitre.org/data/definitions/286.html) | Incorrect User Management |
| [CWE-311](https://cwe.mitre.org/data/definitions/311.html) | Missing Encryption of Sensitive Data |
| [CWE-312](https://cwe.mitre.org/data/definitions/312.html) | Cleartext Storage of Sensitive Information |
| [CWE-313](https://cwe.mitre.org/data/definitions/313.html) | Cleartext Storage in File or on Disk |
| [CWE-316](https://cwe.mitre.org/data/definitions/316.html) | Cleartext Storage in Memory |
| [CWE-362](https://cwe.mitre.org/data/definitions/362.html) | Concurrent Execution Using Shared Resource with Improper Synchronization (Race Condition) |
| [CWE-382](https://cwe.mitre.org/data/definitions/382.html) | J2EE Bad Practice: Use of finalize() |
| [CWE-419](https://cwe.mitre.org/data/definitions/419.html) | Unprotected Primary Channel |
| [CWE-434](https://cwe.mitre.org/data/definitions/434.html) | Unrestricted Upload of File with Dangerous Type |
| [CWE-436](https://cwe.mitre.org/data/definitions/436.html) | Interpretation Conflict |
| [CWE-444](https://cwe.mitre.org/data/definitions/444.html) | HTTP Request/Response Smuggling |
| [CWE-451](https://cwe.mitre.org/data/definitions/451.html) | User Interface Misrepresentation of Security-Relevant Information |
| [CWE-454](https://cwe.mitre.org/data/definitions/454.html) | External Initialization of Trusted Variables or Data Stores |
| [CWE-472](https://cwe.mitre.org/data/definitions/472.html) | External Control of Assumed-Immutable Data |
| [CWE-501](https://cwe.mitre.org/data/definitions/501.html) | Trust Boundary Violation |
| [CWE-522](https://cwe.mitre.org/data/definitions/522.html) | Insufficiently Protected Credentials |
| [CWE-525](https://cwe.mitre.org/data/definitions/525.html) | Use of Web Browser Cache Containing Sensitive Information |
| [CWE-539](https://cwe.mitre.org/data/definitions/539.html) | Use of Persistent Cookies Containing Sensitive Information |
| [CWE-598](https://cwe.mitre.org/data/definitions/598.html) | Use of GET Request Method With Sensitive Query Strings |
| [CWE-602](https://cwe.mitre.org/data/definitions/602.html) | Client-Side Enforcement of Server-Side Security |
| [CWE-628](https://cwe.mitre.org/data/definitions/628.html) | Function Call with Incorrectly Specified Arguments |
| [CWE-642](https://cwe.mitre.org/data/definitions/642.html) | External Control of Critical State Data |
| [CWE-646](https://cwe.mitre.org/data/definitions/646.html) | Reliance on External Access to Source Code in Web Folder |
| [CWE-653](https://cwe.mitre.org/data/definitions/653.html) | Insufficient Compartmentalization |
| [CWE-656](https://cwe.mitre.org/data/definitions/656.html) | Reliance on Security Through Obscurity |
| [CWE-657](https://cwe.mitre.org/data/definitions/657.html) | Violation of Secure Design Principles |
| [CWE-676](https://cwe.mitre.org/data/definitions/676.html) | Use of Potentially Dangerous Function |
| [CWE-693](https://cwe.mitre.org/data/definitions/693.html) | Protection Mechanism Failure |
| [CWE-799](https://cwe.mitre.org/data/definitions/799.html) | Improper Control of Interaction Frequency |
| [CWE-807](https://cwe.mitre.org/data/definitions/807.html) | Reliance on Untrusted Inputs in a Security Decision |
| [CWE-841](https://cwe.mitre.org/data/definitions/841.html) | Improper Enforcement of Behavioral Workflow |
| [CWE-1021](https://cwe.mitre.org/data/definitions/1021.html) | Improper Restriction of Rendered UI Layers or Frames |
| [CWE-1022](https://cwe.mitre.org/data/definitions/1022.html) | Use of Web Link to Untrusted Target with window.opener Access |
| [CWE-1125](https://cwe.mitre.org/data/definitions/1125.html) | Excessive Attack Surface |
