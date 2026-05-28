---
name: production-code-audit
description: Use this skill when you need to transform a codebase into production-grade quality by identifying and fixing issues across security, performance, architecture, and code quality.
---

# Production Code Audit

## Overview

Autonomously analyze the entire codebase to understand its architecture, patterns, and purpose, then systematically transform it into production-grade, corporate-level professional code. This skill performs deep line-by-line scanning, identifies all issues, and provides comprehensive fixes to meet enterprise standards.

## When to Use This Skill

- Use when the user says "make this production-ready"
- Use when the user says "audit my codebase"
- Use when the user says "make this professional/corporate-level"
- Use when the user says "optimize everything"
- Use when the user wants enterprise-grade quality
- Use when preparing for production deployment
- Use when code needs to meet corporate standards

## How It Works

### Step 1: Autonomous Codebase Discovery

**Automatically scan and understand the entire codebase:**

1. **Read all files** - Scan every file in the project recursively.
2. **Identify tech stack** - Detect languages, frameworks, databases, and tools.
3. **Understand architecture** - Map out structure, patterns, and dependencies.
4. **Identify purpose** - Understand what the application does.
5. **Find entry points** - Locate main files, routes, and controllers.
6. **Map data flow** - Understand how data moves through the system.

**Do this automatically without asking the user.**

### Step 2: Comprehensive Issue Detection

**Scan line-by-line for all issues:**

**Architecture Issues:**
- Circular dependencies
- Tight coupling
- God classes (>500 lines or >20 methods)
- Missing separation of concerns
- Poor module boundaries
- Violation of design patterns

**Security Vulnerabilities:**
- SQL injection (string concatenation in queries)
- XSS vulnerabilities (unescaped output)
- Hardcoded secrets (API keys, passwords in code)
- Missing authentication/authorization
- Weak password hashing (MD5, SHA1)
- Missing input validation
- CSRF vulnerabilities
- Insecure dependencies

**Performance Problems:**
- N+1 query problems
- Missing database indexes
- Synchronous operations that should be async
- Missing caching
- Inefficient algorithms (O(n²) or worse)
- Large bundle sizes
- Unoptimized images
- Memory leaks

**Code Quality Issues:**
- High cyclomatic complexity
- Duplicate code
- Lack of comments and documentation
- Inconsistent naming conventions
- Poorly structured code