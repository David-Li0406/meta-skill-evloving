---
name: scanning-for-input-validation-and-xss-vulnerabilities
description: Use this skill when you need to scan source code for potential input validation and XSS vulnerabilities, ensuring user-supplied data is properly sanitized and validated to prevent security exploits.
---

# Skill body

## Overview

This skill automates the process of identifying potential input validation flaws and XSS (Cross-Site Scripting) vulnerabilities within a codebase. By analyzing how user-provided data is handled, it helps developers proactively address security vulnerabilities before they can be exploited. This skill streamlines security audits and improves the overall security posture of applications.

## How It Works

1. **Initiate Scan**: The user requests a scan for input validation or XSS vulnerabilities, triggering the skill.
2. **Code Analysis**: The skill uses the appropriate plugins to analyze the specified codebase or file for both input validation and XSS vulnerabilities.
3. **Vulnerability Identification**: The skill identifies instances where input validation may be missing or insufficient, as well as potential XSS vulnerabilities across different contexts (HTML, JavaScript, CSS, URL).
4. **Report Generation**: The skill presents a report highlighting potential vulnerabilities, their locations in the code, and recommended remediation steps.

## When to Use This Skill

This skill activates when you need to:
- Audit a codebase for input validation and XSS vulnerabilities.
- Review newly written code for potential security flaws.
- Harden an application against common web security exploits.
- Ensure compliance with security best practices related to input handling and XSS prevention.

## Examples

### Example 1: Identifying XSS Vulnerabilities

User request: "Scan the user profile module for potential XSS vulnerabilities."

The skill will:
1. Activate the scanning process on the specified module.
2. Generate a report highlighting areas where user input is directly rendered without proper sanitization, indicating potential XSS vulnerabilities.

### Example 2: Checking for SQL Injection Risks

User request: "Check the database access layer for potential SQL injection risks."

The skill will:
1. Analyze the code related to database access.
2. Identify instances where user input is not properly validated, indicating potential SQL injection vulnerabilities.

### Example 3: Comprehensive Security Audit

User request: "Perform a security audit on the entire application."

The skill will:
1. Scan the entire codebase for both input validation and XSS vulnerabilities.
2. Generate a comprehensive report detailing all identified vulnerabilities and suggested fixes.