---
name: detect-sql-injection-vulnerabilities
description: Use this skill when you need to identify SQL injection vulnerabilities in a codebase and receive remediation guidance.
---

# Skill body

## Overview

This skill empowers Claude to proactively identify and address SQL injection vulnerabilities within a codebase. By leveraging the sql-injection-detector plugin, Claude can perform comprehensive scans, pinpoint potential security flaws, and offer actionable recommendations to mitigate risks.

## How It Works

1. **Initiate Scan**: Upon receiving a relevant request, Claude activates the sql-injection-detector plugin.
2. **Code Analysis**: The plugin analyzes the codebase, examining code patterns, input vectors, and query contexts.
3. **Vulnerability Identification**: The plugin identifies potential SQL injection vulnerabilities, categorizing them by severity.
4. **Report Generation**: A detailed report is generated, outlining the identified vulnerabilities, their locations, and recommended remediation steps.

## When to Use This Skill

This skill activates when you need to:
- Audit a codebase for SQL injection vulnerabilities.
- Secure a web application against SQL injection attacks.
- Review code changes for potential SQL injection risks.
- Understand how SQL injection vulnerabilities occur and how to prevent them.

## Examples

### Example 1: Securing a Web Application

User request: "Scan my web application for SQL injection vulnerabilities."

The skill will:
1. Activate the sql-injection-detector plugin.
2. Scan the web application's codebase for potential SQL injection flaws.
3. Generate a report detailing any identified vulnerabilities, their severity, and remediation recommendations.

### Example 2: Reviewing Code Changes

User request: "Check these code changes for potential SQL injection risks."

The skill will:
1. Activate the sql-injection-detector plugin.
2. Analyze the provided code changes for potential SQL injection vulnerabilities.
3. Provide feedback on the security implications of the changes and suggest improvements.