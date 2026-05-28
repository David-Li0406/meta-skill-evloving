---
name: scanning-for-data-privacy-and-gdpr-compliance
description: Use this skill when you need to scan code and data systems for potential data privacy vulnerabilities and GDPR compliance issues, ensuring sensitive data is protected and regulatory requirements are met.
---

# Skill body

## Overview

This skill automates the process of identifying data privacy risks and assessing GDPR compliance within a codebase or data system. By leveraging the `data-privacy-scanner` and `gdpr-compliance-scanner` plugins, Claude can quickly pinpoint potential vulnerabilities and compliance violations, helping developers proactively address requirements and protect sensitive user data.

## How It Works

1. **Initiate Scan**: Upon detecting a privacy-related trigger phrase, Claude activates the appropriate scanning plugin.
2. **Analyze Codebase or System**: The plugin analyzes the specified files, codebase, or entire system for potential data privacy violations and GDPR compliance issues.
3. **Report Findings**: The plugin generates a detailed report outlining identified risks, compliance scores, critical gaps, and recommended actions.

## When to Use This Skill

This skill activates when you need to:
- Identify potential data privacy vulnerabilities in a codebase.
- Ensure compliance with data privacy regulations such as GDPR, CCPA, or HIPAA.
- Perform a privacy audit of a project involving sensitive user data.
- Assess an application's GDPR compliance and identify potential violations.

## Examples

### Example 1: Identifying PII Leaks

User request: "Scan this project for PII leaks."

The skill will:
1. Activate the `data-privacy-scanner` plugin to analyze the project.
2. Generate a report highlighting potential Personally Identifiable Information (PII) leaks, such as exposed email addresses or phone numbers.

### Example 2: Checking GDPR Compliance

User request: "Check this configuration file for GDPR compliance issues."

The skill will:
1. Activate the `gdpr-compliance-scanner` plugin to analyze the specified configuration file.
2. Generate a report identifying potential GDPR violations, such as insufficient data anonymization or improper consent management.

### Example 3: Assessing GDPR Compliance of a Web Application

User request: "Scan my web application for GDPR compliance."

The skill will:
1. Activate the `gdpr-compliance-scanner` plugin.
2. Scan the web application for GDPR compliance issues related to data collection, storage, and processing.
3. Generate a report highlighting compliance scores and critical gaps, along with actionable recommendations.

## Best Practices

- **Scope**: Specify the relevant files or directories to narrow the scope of the scan and improve performance.
- **Context**: Provide context about the data being processed to enhance the accuracy of the scan.