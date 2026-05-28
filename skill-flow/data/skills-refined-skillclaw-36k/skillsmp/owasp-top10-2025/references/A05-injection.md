# A05 Injection

## Background

Injection vulnerabilities have dropped from **3rd to 5th** place in the 2025 rankings. However, this category maintains relevance with **100% of applications** tested for some form of injection.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 37 |
| Max Incidence Rate | 13.77% |
| Avg Incidence Rate | 3.08% |
| Max Coverage | 100% |
| Avg Coverage | 42.93% |
| Avg Weighted Exploit | 7.15 |
| Avg Weighted Impact | 4.32 |
| Total Occurrences | 1,404,249 |
| Total CVEs | 62,445 |

### Key Vulnerabilities
- **CWE-79 (XSS)**: Over 30,000 CVEs
- **CWE-89 (SQL Injection)**: Over 14,000 CVEs (low frequency/high impact)

## Description

Injection flaws occur when **"untrusted user input is sent to an interpreter (e.g., browser, database, command line) causing the interpreter to execute part of that input as a command."**

### Vulnerability Conditions

Applications become vulnerable when:

1. **Lack of Validation, Filtering, or Sanitization of User-Provided Data**
2. **Dynamic Queries or Non-Parameterized Calls Used Directly in Interpreter Without Context-Aware Escaping**
3. **Unsanitized Data in ORM Search Parameters Extracting Additional Sensitive Records**
4. **Hostile Data Used or Concatenated Directly in SQL, Commands, or Stored Procedures**

### Common Injection Types
- SQL
- NoSQL
- OS Command
- ORM
- LDAP
- Expression Language (EL)
- OGNL

## How to Prevent

### Basic Approach

**The optimal solution is to separate data from commands and queries.**

1. **Use Safe APIs**: Use safe APIs that completely avoid the interpreter, provide parameterized interfaces, or implement ORM (Object Relational Mapping) tools

### Secondary Measures (When Separation Is Not Possible)

2. **Positive Server-Side Input Validation**: Implement positive server-side input validation (not complete defense when special characters are required)
3. **Escape Special Characters**: Escape special characters using interpreter-specific escape syntax

### Important Note
> **SQL structural elements (such as table and column names) cannot be escaped, so user-provided structural names are inherently dangerous.**

## Example Attack Scenarios

### Scenario #1 - SQL Injection
```java
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

Attacker modifies 'id' parameter: `' OR '1'='1`

Example URL:
```
http://example.com/app/accountView?id=' OR '1'='1
```

This returns all records from the accounts table. More sophisticated attacks can modify, delete data, or invoke stored procedures.

### Scenario #2 - ORM/Hibernate Query Language (HQL) Injection
```java
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

Attacker provides: `' OR custID IS NOT NULL OR custID='`

This bypasses the filter and returns all accounts. Even frameworks with fewer dangerous functions are vulnerable to concatenated user input.

### Scenario #3 - OS Command Injection
```java
String cmd = "nslookup " + request.getParameter("domain");
Runtime.getRuntime().exec(cmd);
```

Attacker provides: `example.com; cat /etc/passwd`

This executes arbitrary commands on the server, accessing sensitive system files.

## References

- [OWASP Proactive Controls: Secure Database Access](https://owasp.org/www-project-proactive-controls/)
- [OWASP ASVS: V5 Input Validation and Encoding](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Testing Guide: SQL Injection, Command Injection, ORM Injection](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Cheat Sheet: Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
- [OWASP Cheat Sheet: SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Cheat Sheet: Injection Prevention in Java](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_in_Java_Cheat_Sheet.html)
- [OWASP Cheat Sheet: Query Parameterization](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html)
- [OWASP Automated Threats to Web Applications – OAT-014](https://owasp.org/www-project-automated-threats-to-web-applications/)
- [PortSwigger: Server-side template injection](https://portswigger.net/web-security/server-side-template-injection)
- [Awesome Fuzzing: Fuzzing Resources List](https://github.com/secfigo/Awesome-Fuzzing)

### Related Resources
> LLM injection vulnerabilities are discussed separately in **LLM01:2025 Prompt Injection** of OWASP LLM Top 10.

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-20](https://cwe.mitre.org/data/definitions/20.html) | Improper Input Validation |
| [CWE-74](https://cwe.mitre.org/data/definitions/74.html) | Improper Neutralization of Special Elements in Output |
| [CWE-76](https://cwe.mitre.org/data/definitions/76.html) | Improper Neutralization of Equivalent Special Elements |
| [CWE-77](https://cwe.mitre.org/data/definitions/77.html) | Improper Neutralization of Special Elements in Command |
| [CWE-78](https://cwe.mitre.org/data/definitions/78.html) | Improper Neutralization of Special Elements in OS Command |
| [CWE-79](https://cwe.mitre.org/data/definitions/79.html) | Improper Neutralization of Input During Web Page Generation (XSS) |
| [CWE-80](https://cwe.mitre.org/data/definitions/80.html) | Improper Neutralization of Script-Related HTML Tags (Basic XSS) |
| [CWE-83](https://cwe.mitre.org/data/definitions/83.html) | Improper Neutralization of Script in Attributes |
| [CWE-86](https://cwe.mitre.org/data/definitions/86.html) | Improper Neutralization of Invalid Characters in Identifiers |
| [CWE-88](https://cwe.mitre.org/data/definitions/88.html) | Improper Neutralization of Argument Delimiters (Argument Injection) |
| [CWE-89](https://cwe.mitre.org/data/definitions/89.html) | Improper Neutralization of Special Elements in SQL Command (SQL Injection) |
| [CWE-90](https://cwe.mitre.org/data/definitions/90.html) | Improper Neutralization of Special Elements in LDAP Query |
| [CWE-91](https://cwe.mitre.org/data/definitions/91.html) | XML Injection (Blind XPath Injection) |
| [CWE-93](https://cwe.mitre.org/data/definitions/93.html) | Improper Neutralization of CRLF Sequences |
| [CWE-94](https://cwe.mitre.org/data/definitions/94.html) | Improper Control of Generation of Code (Code Injection) |
| [CWE-95](https://cwe.mitre.org/data/definitions/95.html) | Improper Neutralization of Directives in Dynamically Evaluated Code (Eval Injection) |
| [CWE-96](https://cwe.mitre.org/data/definitions/96.html) | Improper Neutralization of Directives in Statically Saved Code |
| [CWE-97](https://cwe.mitre.org/data/definitions/97.html) | Improper Neutralization of Server-Side Includes (SSI) |
| [CWE-98](https://cwe.mitre.org/data/definitions/98.html) | Improper Control of Filename for Include/Require in PHP (PHP RFI) |
| [CWE-99](https://cwe.mitre.org/data/definitions/99.html) | Improper Control of Resource Identifiers (Resource Injection) |
| [CWE-103](https://cwe.mitre.org/data/definitions/103.html) | Struts: Incomplete validate() Method Definition |
| [CWE-104](https://cwe.mitre.org/data/definitions/104.html) | Struts: Form Bean Does Not Extend Validation Class |
| [CWE-112](https://cwe.mitre.org/data/definitions/112.html) | Missing XML Validation |
| [CWE-113](https://cwe.mitre.org/data/definitions/113.html) | Improper Neutralization of CRLF in HTTP Headers (HTTP Response Splitting) |
| [CWE-114](https://cwe.mitre.org/data/definitions/114.html) | Process Control |
| [CWE-115](https://cwe.mitre.org/data/definitions/115.html) | Misinterpretation of Output |
| [CWE-116](https://cwe.mitre.org/data/definitions/116.html) | Improper Encoding or Escaping of Output |
| [CWE-129](https://cwe.mitre.org/data/definitions/129.html) | Improper Validation of Array Index |
| [CWE-159](https://cwe.mitre.org/data/definitions/159.html) | Improper Handling of Invalid Use of Special Elements |
| [CWE-470](https://cwe.mitre.org/data/definitions/470.html) | Use of Externally-Controlled Input to Select Classes (Unsafe Reflection) |
| [CWE-493](https://cwe.mitre.org/data/definitions/493.html) | Critical Public Variable Without Final Modifier |
| [CWE-500](https://cwe.mitre.org/data/definitions/500.html) | Public Static Field Not Marked Final |
| [CWE-564](https://cwe.mitre.org/data/definitions/564.html) | SQL Injection: Hibernate |
| [CWE-610](https://cwe.mitre.org/data/definitions/610.html) | Externally Controlled Reference to Resource in Another Sphere |
| [CWE-643](https://cwe.mitre.org/data/definitions/643.html) | Improper Neutralization of Data in XPath Expression (XPath Injection) |
| [CWE-644](https://cwe.mitre.org/data/definitions/644.html) | Improper Neutralization of HTTP Headers for Scripting Syntax |
| [CWE-917](https://cwe.mitre.org/data/definitions/917.html) | Improper Neutralization of Special Elements in Expression Language Statement |
