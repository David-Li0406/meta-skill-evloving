---
name: senior-fullstack
description: Use this skill for comprehensive fullstack development of web applications with modern technologies like React, Next.js, Node.js, GraphQL, and PostgreSQL, including project scaffolding and code quality analysis.
---

# Senior Fullstack

Complete toolkit for senior fullstack development with modern tools and best practices.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through automated scripts:

```bash
# Script 1: Fullstack Scaffolder
python scripts/fullstack_scaffolder.py [options]

# Script 2: Project Scaffolder
python scripts/project_scaffolder.py [options]

# Script 3: Code Quality Analyzer
python scripts/code_quality_analyzer.py [options]
```

## Core Capabilities

### 1. Fullstack Scaffolder

Automated tool for fullstack scaffolding tasks.

**Features:**
- Automated scaffolding
- Built-in best practices
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/fullstack_scaffolder.py <project-path> [options]
```

### 2. Project Scaffolder

Comprehensive analysis and optimization tool.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/project_scaffolder.py <target-path> [--verbose]
```

### 3. Code Quality Analyzer

Advanced tooling for specialized tasks.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/code_quality_analyzer.py [arguments] [options]
```

## Tech Stack

**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin  
**Frontend:** React, Next.js, React Native, Flutter  
**Backend:** Node.js, Express, GraphQL, REST APIs  
**Database:** PostgreSQL, Prisma, NeonDB, Supabase  
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI  
**Cloud:** AWS, GCP, Azure  

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
python scripts/project_scaffolder.py .

# Review recommendations
# Apply fixes
```

### 3. Implement Best Practices

Follow the documented patterns and practices.

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
python scripts/project_scaffolder.py .
python scripts/code_quality_analyzer.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Refer to the troubleshooting section in the development workflows.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/tech_stack_guide.md`
- Workflow Guide: `references/architecture_patterns.md`
- Technical Guide: `references/development_workflows.md`
- Tool Scripts: `scripts/` directory