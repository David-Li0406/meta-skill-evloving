---
name: senior-qa
description: Use this skill for comprehensive quality assurance and testing strategies, including test automation, test suite generation, coverage analysis, and E2E testing for ReactJS, NextJS, and NodeJS applications.
---

# Senior QA

Complete toolkit for senior QA with modern tools and best practices.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through automated scripts:

```bash
# Script 1: Test Suite Generator
python scripts/test_suite_generator.py [options]

# Script 2: Coverage Analyzer
python scripts/coverage_analyzer.py [options]

# Script 3: E2E Test Scaffolder
python scripts/e2e_test_scaffolder.py [options]
```

## Core Capabilities

### 1. Test Suite Generator

Automated tool for generating test suites.

**Features:**
- Automated scaffolding
- Best practices built-in
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/test_suite_generator.py <project-path> [options]
```

### 2. Coverage Analyzer

Comprehensive analysis and optimization tool.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/coverage_analyzer.py <target-path> [--verbose]
```

### 3. E2E Test Scaffolder

Advanced tooling for end-to-end testing.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/e2e_test_scaffolder.py [arguments] [options]
```

## Development Workflow

### 1. Setup and Configuration

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Run Quality Checks

```bash
# Use the analyzer script
python scripts/coverage_analyzer.py .

# Review recommendations
# Apply fixes
```

### 3. Implement Best Practices

Follow documented patterns and practices for testing strategies, automation, and QA best practices.

## Best Practices Summary

### Code Quality
- Follow established patterns
- Write comprehensive tests
- Document decisions
- Review regularly

### Performance
- Measure before optimizing
- Use appropriate caching
- Optimize critical paths
- Monitor in production

### Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Keep dependencies updated

### Maintainability
- Write clear code
- Use consistent naming
- Add helpful comments
- Keep it simple

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/coverage_analyzer.py .
python scripts/e2e_test_scaffolder.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Refer to the troubleshooting section in the QA best practices documentation.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/testing_strategies.md`
- Workflow Guide: `references/test_automation_patterns.md`
- Technical Guide: `references/qa_best_practices.md`
- Tool Scripts: `scripts/` directory