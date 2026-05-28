---
name: performing-security-testing
description: Use this skill when you need to automate security vulnerability testing for applications and APIs, covering OWASP Top 10 vulnerabilities, SQL injection, XSS, CSRF, and authentication issues.
---

# Skill body

## Overview

This skill automates security vulnerability testing on applications and APIs. It leverages the security-test-scanner plugin to identify potential weaknesses and generate comprehensive reports.

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
- Identify target URLs and endpoints to scan.
- Specify authentication requirements and test credentials.
- Determine specific vulnerability types to focus on (e.g., OWASP Top 10, injection, XSS).
- Decide on the testing depth level (passive scan vs. active exploitation).

### Step 2: Execute Security Scan
- Use the Read tool to analyze application structure and identify entry points.
- Execute security testing tools via Bash with proper scope.
- Monitor scan progress and capture all findings.
- Document identified vulnerabilities with severity ratings.

### Step 3: Analyze Vulnerabilities
- Process scan results to identify:
  - SQL injection vulnerabilities in database queries.
  - Cross-Site Scripting (XSS) in user input fields.
  - Cross-Site Request Forgery (CSRF) token weaknesses.
  - Authentication and authorization bypass opportunities.
  - Security misconfigurations and exposed sensitive data.

### Step 4: Generate Security Report
- Create comprehensive documentation in a specified directory:
  - Executive summary with risk overview.
  - Detailed vulnerability findings with CVSS scores.
  - Proof-of-concept exploit examples where applicable.
  - Prioritized remediation recommendations.
  - Compliance assessment against security standards.

## Best Practices
- Clearly define the scope of the security test (e.g., specific endpoints, modules).
- Provide necessary authentication credentials for testing protected resources.
- Schedule regular security tests to identify newly introduced vulnerabilities.