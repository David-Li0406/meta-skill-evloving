---
name: analyzing-dependencies
description: Use this skill when you need to analyze project dependencies for security vulnerabilities, outdated packages, and license compliance issues.
---

# Skill body

## Overview

This skill empowers you to automatically analyze your project's dependencies for security vulnerabilities, outdated packages, and license compliance issues. It uses the dependency-checker plugin to identify potential risks and provides insights for remediation.

## How It Works

1. **Detecting Package Manager**: The skill identifies the relevant package manager (npm, pip, composer, gem, go modules) based on the presence of manifest files (e.g., package.json, requirements.txt, composer.json).
2. **Scanning Dependencies**: The skill utilizes the dependency-checker plugin to scan the identified dependencies against known vulnerability databases (CVEs), outdated package lists, and license information.
3. **Generating Report**: The skill presents a comprehensive report summarizing the findings, including vulnerability summaries, detailed vulnerability information, outdated packages with recommended updates, and license compliance issues.

## When to Use This Skill

This skill activates when you need to:
- Check a project for known security vulnerabilities in its dependencies.
- Identify outdated packages that may contain security flaws or performance issues.
- Ensure that the project's dependencies comply with licensing requirements.

## Examples

### Example 1: Identifying Vulnerabilities Before Deployment

User request: "Check dependencies for vulnerabilities before deploying to production."

The skill will:
1. Detect the relevant package manager (e.g., npm).
2. Scan the project's dependencies for known vulnerabilities using the dependency-checker plugin.
3. Generate a report highlighting any identified vulnerabilities, their severity, and recommended fixes.

### Example 2: Updating Outdated Packages

User request: "Scan for outdated packages and suggest updates."

The skill will:
1. Detect the relevant package manager.
2. Scan the project's dependencies for outdated packages.
3. Generate a report listing outdated packages and recommended updates.