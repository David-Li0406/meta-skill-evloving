---
name: validating-cors-policies
description: Use this skill when you need to validate Cross-Origin Resource Sharing (CORS) policies to ensure they are correctly implemented and secure.
---

# Skill body

## Overview

This skill empowers Claude to assess the security and correctness of CORS policies. By leveraging the cors-policy-validator plugin, it identifies misconfigurations and potential vulnerabilities in CORS settings, helping developers build more secure web applications.

## How It Works

1. **Analyze CORS Configuration**: The skill receives the CORS configuration details, such as headers or policy files.
2. **Validate Policy**: It utilizes the cors-policy-validator plugin to analyze the provided configuration against established security best practices.
3. **Report Findings**: The skill presents a detailed report outlining any identified vulnerabilities or misconfigurations in the CORS policy.

## When to Use This Skill

This skill activates when you need to:
- Validate a CORS policy for a web application.
- Check the CORS configuration of an API endpoint.
- Identify potential security vulnerabilities in existing CORS implementations.

## Examples

### Example 1: Validating a CORS Policy File

User request: "Validate the CORS policy in `cors_policy.json`"

The skill will:
1. Read the `cors_policy.json` file.
2. Use the cors-policy-validator plugin to analyze the CORS configuration.
3. Output a report detailing any identified vulnerabilities or misconfigurations.

### Example 2: Checking CORS Headers for an API Endpoint

User request: "Check CORS headers for the API endpoint at `https://example.com/api`"

The skill will:
1. Fetch the CORS headers from the specified API endpoint.
2. Use the cors-policy-validator plugin to analyze the headers.
3. Output a report summarizing the CORS configuration and any potential issues.

## Best Practices

- **Configuration Source**: Always specify the source of the CORS configuration (e.g., file path, URL) for accurate validation.
- **Regular Validation**: Regularly validate CORS policies, especially after making changes to the application or API.