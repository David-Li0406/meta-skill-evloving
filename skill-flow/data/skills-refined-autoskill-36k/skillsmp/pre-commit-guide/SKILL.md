---
name: pre-commit-guide
description: Pre-commit hooks setup and usage including code quality checks, gitleaks secret scanning, and configuration
---

# pre-commit

## Overview

[pre-commit](https://pre-commit.com/) is a framework that uses Git hooks to easily run code quality checks. In this repository, the following checks are executed before committing:

- Basic code quality checks (removing whitespace, ensuring end-of-file newlines, etc.)
- Secret information leak checks (using gitleaks)

## Setup

After cloning the repository, run the following command to install pre-commit hooks:

```bash
make pre-commit-init
```

## Running Checks Manually

To run checks on all files manually:

```bash
make pre-commit-run
```

## Secret Scanning

This repository uses [gitleaks](https://github.com/gitleaks/gitleaks) to scan for secret information. This helps prevent accidentally committing sensitive information such as API keys and passwords.

### Configuration

The gitleaks configuration is managed in the `.gitleaks.toml` file. By default, basic secret detection rules are enabled.

### Handling False Positives

To ignore false positives, add path patterns to the `allowlist` section in the `.gitleaks.toml` file.
