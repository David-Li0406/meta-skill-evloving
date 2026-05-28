---
name: validating-csrf-protection
description: Use this skill when you need to analyze your web application's security posture against Cross-Site Request Forgery (CSRF) attacks and validate the effectiveness of its CSRF protection mechanisms.
---

# Skill body

## Overview

This skill empowers you to analyze web applications for CSRF vulnerabilities. It assesses the effectiveness of implemented CSRF protection mechanisms, providing insights into potential weaknesses and recommendations for remediation.

## How It Works

1. **Analyze Endpoints**: Examine application endpoints to identify those lacking CSRF protection.
2. **Assess Protection Mechanisms**: Validate the implementation of CSRF protection mechanisms, including:
   - Synchronizer tokens
   - Double-submit cookies
   - SameSite attributes
   - Origin validation
3. **Generate Report**: Create a detailed report highlighting vulnerable endpoints, potential attack scenarios, and recommended fixes.

## When to Use This Skill

Activate this skill when you need to:
- Validate existing CSRF protection measures.
- Identify CSRF vulnerabilities in a web application.
- Assess the risk associated with unprotected endpoints.
- Generate a report outlining CSRF vulnerabilities and recommended fixes.

## Examples

### Example 1: Identifying Unprotected API Endpoints

User request: "validate csrf"

The skill will:
1. Analyze the application's API endpoints.
2. Identify endpoints lacking CSRF protection, such as those handling sensitive data modifications.
3. Generate a report outlining vulnerable endpoints and potential attack vectors.

### Example 2: Checking SameSite Cookie Attributes

User request: "Check for csrf vulnerabilities in my application"

The skill will:
1. Analyze the application's cookie settings.
2. Verify that SameSite attributes are properly configured to mitigate CSRF attacks.
3. Report any cookies lacking the SameSite attribute or using an insecure setting.

## Best Practices

- **Regular Validation**: Regularly validate CSRF protection mechanisms as part of the development lifecycle.
- **Comprehensive Coverage**: Ensure all state-changing operations are protected against CSRF attacks.
- **Secure Configuration**: Use secure configurations for cookies and other relevant settings.