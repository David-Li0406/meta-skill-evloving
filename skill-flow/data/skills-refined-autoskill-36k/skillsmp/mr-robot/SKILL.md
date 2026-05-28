---
name: mr-robot
description: Security and data integrity checks for org run mr robot leak and org run mr robot db requests. Use when asked to audit PII exposure, auth gaps, or database issues.
---

# Mr Robot

## Overview

Inspect security posture and database integrity for leaks, misconfigurations, or unsafe access.

## Workflow

### 1) Leak audit (org run mr robot leak)

- Scan for PII logging, secret leakage, or unsafe error handling.
- Verify auth and tenant isolation on API routes.
- Flag storage or vault exposures.

### 2) DB audit (org run mr robot db)

- Check migrations for RLS correctness and tenant scoping.
- Verify constraints, indexes, and data retention safety.
- Identify schema risks and provide fixes.

### 3) Output

- List issues by severity with file references.
- Provide concrete mitigation steps.
