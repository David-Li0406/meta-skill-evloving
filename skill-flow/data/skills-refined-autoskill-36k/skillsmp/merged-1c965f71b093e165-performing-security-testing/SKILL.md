---
name: performing-security-testing
description: Use this skill to automate security vulnerability testing for applications and APIs, covering OWASP Top 10 vulnerabilities, SQL injection, XSS, CSRF, and authentication issues.
---

## Overview

This skill enables automated security vulnerability testing on applications and APIs. It leverages the security-test-scanner plugin to identify potential weaknesses and generate comprehensive reports.

## How It Works

1. **Initiate Scan**: The plugin is activated when security testing is requested.
2. **Execute Tests**: The plugin automatically runs a suite of security tests covering OWASP Top 10, injection flaws, XSS, CSRF, and authentication/authorization issues.
3. **Generate Report**: The plugin compiles the test results into a detailed report, highlighting vulnerabilities, severity ratings, and remediation steps.

## When to Use This Skill

This skill activates when you need to:
- Perform a security vulnerability scan of an application.
- Test for OWASP Top 10 vulnerabilities.
- Identify SQL injection or XSS vulnerabilities.
- Assess authentication and authorization security.

## Instructions

### Step 1: Define Test Scope
Identify the security testing parameters:
- Target URLs and endpoints to scan
- Authentication requirements and test credentials
- Specific vulnerability types to focus on (OWASP Top 10, injection, XSS, etc.)
- Testing depth level (passive scan vs. active exploitation)

### Step 2: Execute Security Scan
Run automated vulnerability detection:
1. Use Read tool to analyze application structure and identify entry points.
2. Execute security testing tools via Bash with proper scope.
3. Monitor scan progress and capture all findings.
4. Document identified vulnerabilities with severity ratings.

### Step 3: Analyze Vulnerabilities
Process scan results to identify:
- SQL injection vulnerabilities in database queries
- Cross-Site Scripting (XSS) in user input fields
- Cross-Site Request Forgery (CSRF) token weaknesses
- Authentication and authorization bypass opportunities
- Security misconfigurations and exposed sensitive data

### Step 4: Generate Security Report
Create comprehensive documentation:
- Executive summary with risk overview
- Detailed vulnerability findings with CVSS scores
- Proof-of-concept exploit examples where applicable
- Prioritized remediation recommendations
- Compliance assessment against security standards

## Examples

### Example 1: OWASP Top 10 Vulnerability Scan

User request: "Perform a security test focusing on OWASP Top 10 vulnerabilities for the /api/ endpoint."

The skill will:
1. Activate the security-test-scanner plugin.
2. Execute OWASP Top 10 tests against the specified endpoint.
3. Generate a report detailing any identified vulnerabilities and their severity.

### Example 2: SQL Injection Testing

User request: "Test the API for SQL injection vulnerabilities."

The skill will:
1. Activate the security-test-scanner plugin.
2. Run SQL injection tests against the API.
3. Report any successful injection attempts.

## Best Practices

- **Scope Definition**: Clearly define the scope of the security test (e.g., specific endpoints, modules).
- **Authentication**: Provide necessary authentication credentials for testing protected resources.
- **Regular Testing**: Schedule regular security tests to identify newly introduced vulnerabilities.

## Integration

This skill can be integrated with other plugins to automatically trigger security tests as part of a CI/CD pipeline or after code changes. It also integrates with reporting tools for centralized vulnerability management.

## Error Handling

Common issues and solutions:
- **Access Denied**: Verify credentials are valid and have sufficient permissions.
- **Rate Limiting**: Configure scan throttling to reduce request rate.
- **False Positives**: Manually verify each finding; adjust scanner sensitivity.
- **Tool Installation Missing**: Install required tools using Bash with package manager.

## Resources

### Security Testing Tools
- OWASP ZAP for automated vulnerability scanning
- Burp Suite for manual penetration testing
- sqlmap for SQL injection detection and exploitation
- Nikto for web server vulnerability scanning

### Vulnerability Databases
- Common Vulnerabilities and Exposures (CVE) database
- National Vulnerability Database (NVD) for CVSS scoring
- OWASP Top 10 documentation and remediation guides

### Secure Coding Guidelines
- OWASP Secure Coding Practices checklist
- CWE (Common Weakness Enumeration) catalog
- SANS Top 25 Most Dangerous Software Errors