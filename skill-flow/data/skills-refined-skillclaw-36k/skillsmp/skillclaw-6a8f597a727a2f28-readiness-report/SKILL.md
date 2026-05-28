---
name: readiness-report
description: Use this skill when you want to evaluate how well a codebase supports autonomous AI development by analyzing it across eight technical pillars and five maturity levels.
---

# Agent Readiness Report

Evaluate how well a repository supports autonomous AI development by analyzing it across eight technical pillars and five maturity levels.

## Overview

Agent Readiness measures how prepared a codebase is for AI-assisted development. Poor feedback loops, missing documentation, or lack of tooling can cause agents to waste cycles on preventable errors. This skill identifies those gaps and prioritizes fixes.

## Quick Start

Run `/readiness-report` to evaluate the current repository. The analysis will:
1. Clone the repository and scan its structure, CI configurations, and tooling.
2. Evaluate 81 criteria across 8 technical pillars.
3. Determine maturity level (L1-L5) based on an 80% threshold per level.
4. Provide prioritized recommendations for improvements.

## Workflow

### Step 1: Run Repository Analysis

Execute the analysis script to gather signals from the repository:

```bash
python scripts/analyze_repo.py --repo-path .
```

This script checks for:
- Configuration files (e.g., `.eslintrc`, `pyproject.toml`)
- CI/CD workflows (e.g., `.github/workflows/`, `.gitlab-ci.yml`)
- Documentation (e.g., `README`, `AGENTS.md`, `CONTRIBUTING.md`)
- Test infrastructure (e.g., test directories, coverage configurations)
- Security configurations (e.g., `CODEOWNERS`, `.gitignore`, secrets management)

### Step 2: Generate Report

After analysis, generate the formatted report:

```bash
python scripts/generate_report.py --analysis-file /tmp/readiness_analysis.json
```

### Step 3: Present Results

The report includes:
1. **Overall Score**: Pass rate percentage and maturity level achieved.
2. **Level Progress**: Bar showing L1-L5 completion percentages.
3. **Strengths**: Top-performing pillars with passing criteria.
4. **Opportunities**: Prioritized list of improvements to implement.
5. **Detailed Criteria**: Full breakdown by pillar showing each criterion status.

## Nine Technical Pillars

Each pillar addresses specific failure modes in AI-assisted development:

| Pillar | Purpose | Key Signals |
|--------|---------|-------------|
| **Style & Validation** | Catch bugs instantly | ... |
| **Build System** | Ensure reliable builds | ... |
| **Testing** | Validate functionality | ... |
| **Documentation** | Provide clear guidance | ... |
| **Dev Environment** | Streamline development | ... |
| **Debugging & Observability** | Enhance troubleshooting | ... |
| **Security** | Protect against vulnerabilities | ... |
| **Task Discovery** | Facilitate task identification | ... |