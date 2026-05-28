# A10 Mishandling of Exceptional Conditions

## Background

This is a **new category for 2025**, containing 24 CWEs focused on improper error handling and logical failures. This category addresses situations where applications fail to prevent, detect, or appropriately respond to abnormal conditions.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 24 |
| Total Occurrences | 769,581 |
| Total CVEs | 3,416 |
| Avg Exploit Difficulty | 7.11 |
| Avg Impact Score | 3.81 |

### Notable Vulnerabilities
- Sensitive Information Disclosure Through Error Messages
- NULL Pointer Dereference
- "Fail Open" Systems

## Description

Applications mishandle exceptional conditions when they cannot effectively manage abnormal situations, leading to potential crashes, unpredictable behavior, and vulnerabilities.

### Core Failure Dimensions

1. **Prevention Gaps**: Application lacks safeguards against abnormal situations
2. **Detection Failures**: System fails to recognize abnormal conditions as they occur
3. **Response Defects**: Inadequate or absent response to detected problems

### Root Causes

- Insufficient input validation
- Late-stage error handling
- Unexpected environment states (memory, permissions, network issues)
- Unhandled exceptions leaving systems in unstable states

### Security Impact

Affects system confidentiality, availability, and data integrity through logic bugs, overflows, race conditions, fraudulent transactions, and authentication/authorization failures.

## How to Prevent

### Core Strategies

#### Proactive Exception Management
1. **Anticipate Potential Failures and Catch System Errors at Their Origin**
2. **Implement Meaningful Error Handling That Resolves Issues and Enables Recovery**
3. **Provide User-Friendly Error Notifications and Event Logging**
4. **Deploy Global Exception Handlers as Safety Nets**

#### Transaction Integrity
5. **Implement Complete Rollback Procedures for Multi-Step Transactions (Fail Closed)**
6. **Prevent Partial Transaction Recovery That Creates Unrecoverable Errors**

#### Resource Management
7. **Apply Rate Limiting, Quotas, Throttling, and Resource Constraints**
8. **Prevent Unlimited Resource Consumption That Enables Denial of Service Attacks**
9. **Implement Statistical Reporting for Repeated Errors Instead of Individual Logging**

#### Structural Improvements
10. **Centralize Error Handling Organization-Wide for Consistency**
11. **Perform Strict Input Validation with Proper Sanitization**
12. **Conduct Threat Modeling and Security Design Reviews**
13. **Execute Code Reviews, Static Analysis, Stress Testing, and Penetration Testing**
14. **Establish Organizational Security Standards for Exception Handling**

## Example Attack Scenarios

### Scenario #1 - Resource Exhaustion (DoS)
```
Application catches file upload exceptions but
fails to release locked resources.
Each exception exacerbates the problem until all resources are exhausted,
resulting in service unavailability.
```

### Scenario #2 - Information Disclosure
```
Database errors expose sensitive system information to users.
Attackers intentionally trigger errors to gather reconnaissance data,
using disclosed details to craft sophisticated SQL injection attacks.
```

### Scenario #3 - Financial Transaction Abuse
```
During multi-step transactions (account withdrawal → destination deposit → transaction logging),
network interruption causes partial completion.
Without proper rollback mechanisms, attackers manipulate sequences to
drain accounts or execute duplicate transfers through race conditions.
```

## References

### OWASP Resources
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
- [OWASP ASVS V16.5 Error Handling](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md#v165-error-handling)
- [OWASP Web Security Testing Guide - Error Handling](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/01-Testing_For_Improper_Error_Handling)

### Industry Resources
- [Microsoft .NET Best Practices for Exceptions](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions)
- [Clean Code and Exception Handling (Toptal)](https://www.toptal.com/developers/abap/clean-code-and-the-art-of-exception-handling)
- [Google Developers - Error Handling Rules](https://developers.google.com/tech-writing/error-messages/error-handling)

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-209](https://cwe.mitre.org/data/definitions/209.html) | Generation of Error Message Containing Sensitive Information |
| [CWE-215](https://cwe.mitre.org/data/definitions/215.html) | Insertion of Sensitive Information Into Debugging Code |
| [CWE-234](https://cwe.mitre.org/data/definitions/234.html) | Failure to Handle Missing Parameter |
| [CWE-235](https://cwe.mitre.org/data/definitions/235.html) | Improper Handling of Extra Parameters |
| [CWE-248](https://cwe.mitre.org/data/definitions/248.html) | Uncaught Exception |
| [CWE-252](https://cwe.mitre.org/data/definitions/252.html) | Unchecked Return Value |
| [CWE-274](https://cwe.mitre.org/data/definitions/274.html) | Improper Handling of Insufficient Privileges |
| [CWE-280](https://cwe.mitre.org/data/definitions/280.html) | Improper Handling of Insufficient Permissions or Privileges |
| [CWE-369](https://cwe.mitre.org/data/definitions/369.html) | Divide By Zero |
| [CWE-390](https://cwe.mitre.org/data/definitions/390.html) | Detection of Error Condition Without Action |
| [CWE-391](https://cwe.mitre.org/data/definitions/391.html) | Unchecked Error Condition |
| [CWE-394](https://cwe.mitre.org/data/definitions/394.html) | Unexpected Status Code or Return Value |
| [CWE-396](https://cwe.mitre.org/data/definitions/396.html) | Declaration of Catch for Generic Exception |
| [CWE-397](https://cwe.mitre.org/data/definitions/397.html) | Declaration of Throws for Generic Exception |
| [CWE-460](https://cwe.mitre.org/data/definitions/460.html) | Improper Cleanup on Thrown Exception |
| [CWE-476](https://cwe.mitre.org/data/definitions/476.html) | NULL Pointer Dereference |
| [CWE-478](https://cwe.mitre.org/data/definitions/478.html) | Missing Default Case in Multiple Condition Expression |
| [CWE-484](https://cwe.mitre.org/data/definitions/484.html) | Omitted Break Statement in Switch |
| [CWE-550](https://cwe.mitre.org/data/definitions/550.html) | Server-generated Error Message Containing Sensitive Information |
| [CWE-636](https://cwe.mitre.org/data/definitions/636.html) | Not Failing Securely ('Fail Open') |
| [CWE-703](https://cwe.mitre.org/data/definitions/703.html) | Improper Check or Handling of Exceptional Conditions |
| [CWE-754](https://cwe.mitre.org/data/definitions/754.html) | Improper Check for Unusual or Exceptional Conditions |
| [CWE-755](https://cwe.mitre.org/data/definitions/755.html) | Improper Handling of Exceptional Conditions |
| [CWE-756](https://cwe.mitre.org/data/definitions/756.html) | Missing Custom Error Page |
