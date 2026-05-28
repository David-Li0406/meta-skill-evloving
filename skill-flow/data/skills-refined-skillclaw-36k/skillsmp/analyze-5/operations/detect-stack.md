# Tech Stack Detection

Comprehensive commands for detecting programming languages, frameworks, and build systems.

## Overview

Run all detection commands **in parallel** to identify the technology stack. Missing files are normal - they just mean that technology isn't used.

---

## Detection Commands

Execute these commands to detect the primary language and framework:

```bash
# Get current directory context
pwd

# Show directory contents
ls -la

# Get git repository info
git remote -v 2>/dev/null

# Language/Framework Detection (run all in parallel)
cat package.json 2>/dev/null          # Node.js/JavaScript/TypeScript
cat composer.json 2>/dev/null         # PHP
cat requirements.txt 2>/dev/null      # Python (pip)
cat Pipfile 2>/dev/null               # Python (pipenv)
cat pyproject.toml 2>/dev/null        # Python (poetry)
cat Gemfile 2>/dev/null               # Ruby
cat pom.xml 2>/dev/null               # Java/Maven
cat build.gradle 2>/dev/null          # Java/Gradle
cat Cargo.toml 2>/dev/null            # Rust
cat go.mod 2>/dev/null                # Go
cat pubspec.yaml 2>/dev/null          # Dart/Flutter
cat mix.exs 2>/dev/null               # Elixir
find . -maxdepth 2 -name "*.csproj" 2>/dev/null   # .NET/C#
find . -maxdepth 2 -name "*.sln" 2>/dev/null      # .NET Solution
```

---

## Framework-Specific Detection

### JavaScript/TypeScript Frameworks

If `package.json` exists, look for these framework indicators:

```json
{
  "dependencies": {
    "react": "...",           // React
    "next": "...",            // Next.js
    "vue": "...",             // Vue.js
    "nuxt": "...",            // Nuxt.js
    "@angular/core": "...",   // Angular
    "svelte": "...",          // Svelte
    "express": "...",         // Express.js (backend)
    "fastify": "...",         // Fastify (backend)
    "nestjs": "..."           // NestJS (backend)
  }
}
```

### Python Frameworks

Look for these imports or dependencies:

- `django` - Django web framework
- `flask` - Flask micro-framework
- `fastapi` - FastAPI
- `pyramid` - Pyramid
- `tornado` - Tornado

### Ruby Frameworks

In `Gemfile`:

- `rails` - Ruby on Rails
- `sinatra` - Sinatra
- `hanami` - Hanami

### PHP Frameworks

In `composer.json`:

- `laravel/framework` - Laravel
- `symfony/symfony` - Symfony
- `slim/slim` - Slim

### Java Frameworks

In `pom.xml` or `build.gradle`:

- `spring-boot` - Spring Boot
- `quarkus` - Quarkus
- `micronaut` - Micronaut

---

## Database Detection

Look for database-related dependencies or configuration:

### SQL Databases

```bash
# PostgreSQL indicators
grep -r "postgres" package.json composer.json requirements.txt 2>/dev/null
ls -la prisma/ 2>/dev/null   # Prisma ORM

# MySQL indicators
grep -r "mysql" package.json composer.json requirements.txt 2>/dev/null

# SQLite
find . -name "*.db" -o -name "*.sqlite" 2>/dev/null
```

### NoSQL Databases

```bash
# MongoDB
grep -r "mongodb\|mongoose" package.json requirements.txt 2>/dev/null

# Redis
grep -r "redis" package.json requirements.txt 2>/dev/null

# DynamoDB (AWS)
grep -r "dynamodb\|@aws-sdk" package.json requirements.txt 2>/dev/null
```

---

## Infrastructure Detection

### Cloud Providers

```bash
# AWS
find . -name "*.tf" -o -name "terraform.tfvars" 2>/dev/null  # Terraform
find . -name "serverless.yml" 2>/dev/null                     # Serverless Framework
find . -name "cdk.json" 2>/dev/null                           # AWS CDK
grep -r "@aws-sdk\|aws-lambda" package.json 2>/dev/null

# Azure
grep -r "@azure" package.json 2>/dev/null

# GCP
grep -r "@google-cloud" package.json 2>/dev/null
```

### Container/Orchestration

```bash
# Docker
ls -la Dockerfile docker-compose.yml 2>/dev/null

# Kubernetes
find . -name "*.yaml" | xargs grep -l "apiVersion: apps/v1" 2>/dev/null
```

---

## Build System Detection

Identify the build tool based on manifest files:

- `package.json` → npm, yarn, or pnpm (check for lock files)
- `pom.xml` → Maven
- `build.gradle` → Gradle
- `Cargo.toml` → Cargo (Rust)
- `go.mod` → Go modules
- `Gemfile` → Bundler
- `composer.json` → Composer
- `requirements.txt` → pip
- `Pipfile` → pipenv
- `pyproject.toml` → poetry

---

## Version Extraction

Extract version numbers from manifests:

```bash
# Node.js
cat package.json | grep '"version"' | head -1

# Python
cat setup.py | grep "version=" 2>/dev/null
cat pyproject.toml | grep "version =" 2>/dev/null

# Java
cat pom.xml | grep "<version>" | head -1

# Rust
cat Cargo.toml | grep "version =" | head -1
```

---

## Multi-Language Projects

If multiple language manifest files exist, identify:

- **Primary language** - The main application language (most source files)
- **Secondary languages** - Supporting tools, scripts, infrastructure

Example:
- Primary: TypeScript (Next.js frontend + backend)
- Secondary: Python (data processing scripts), Terraform (infrastructure)

---

## Output Summary

After detection, summarize as:

```markdown
## Technology Stack

### Primary Language
- TypeScript 5.2

### Frameworks & Libraries
- Next.js 14.0.3 (React framework)
- Prisma 5.6.0 (ORM)
- tRPC 10.45.0 (API)

### Build System
- npm 10.2.3

### Database
- PostgreSQL (via Prisma)

### Infrastructure
- AWS Lambda (Serverless)
- Terraform 1.6.0 (IaC)
```

---

## Common Patterns

### Full-Stack JavaScript/TypeScript
- Frontend: React/Next.js/Vue
- Backend: Express/Fastify/NestJS
- Database: PostgreSQL/MongoDB
- Infrastructure: AWS/Vercel/Netlify

### Python Web App
- Framework: Django/Flask/FastAPI
- Database: PostgreSQL/MySQL
- Cache: Redis
- Infrastructure: AWS/GCP

### Ruby on Rails
- Framework: Rails
- Database: PostgreSQL
- Cache: Redis
- Infrastructure: Heroku/AWS

### Java Enterprise
- Framework: Spring Boot
- Database: PostgreSQL/Oracle
- Message Queue: RabbitMQ/Kafka
- Infrastructure: Kubernetes
