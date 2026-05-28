# Improvement Patterns: Optimizing Subagent Configurations

Common patterns for improving subagent descriptions, system prompts, tool configurations, and model selection.

## Description Optimization Patterns

### Pattern 1: Adding Specific Trigger Keywords

**Problem:** Description lacks keywords user would naturally use.

**Before:**
```
description: Helps with code analysis tasks
```

**After:**
```
description: Analyzes Python code for security vulnerabilities including SQL injection, XSS, command injection, and insecure deserialization. Use when reviewing code security, auditing authentication patterns, or identifying OWASP Top 10 vulnerabilities in Python applications.
```

**Improvement rationale:** Added 8+ trigger keywords (security, vulnerabilities, SQL injection, XSS, Python, authentication, OWASP), making agent discoverable when user mentions these terms.

### Pattern 2: Including Data Types and Formats

**Problem:** Description doesn't specify what kinds of data agent processes.

**Before:**
```
description: Processes configuration files and validates them
```

**After:**
```
description: Validates JSON and YAML configuration files against schemas, checking structure, required fields, data types, and enum values. Use when validating config.json, settings.yaml, or custom configuration formats.
```

**Improvement rationale:** Specifies exact formats (JSON, YAML), validation types (schema, structure, data types), and concrete file examples (config.json, settings.yaml).

### Pattern 3: Specifying Action Verbs

**Problem:** Description uses vague verbs like "handles" or "helps with".

**Before:**
```
description: Handles API endpoint operations
```

**After:**
```
description: Searches codebase for REST API endpoint definitions, extracts route patterns, HTTP methods, request/response schemas, and authentication requirements. Use when mapping API surface, documenting endpoints, or finding specific route handlers.
```

**Improvement rationale:** Replaced "handles" with specific verbs (searches, extracts), added concrete outputs (route patterns, HTTP methods), and clear use cases.

### Pattern 4: Adding Context-Specific Triggers

**Problem:** Description doesn't indicate when agent should activate.

**Before:**
```
description: Analyzes test results
```

**After:**
```
description: Analyzes test execution results from pytest, unittest, and Jest, identifying failing tests, flaky tests, error patterns, and coverage gaps. Use when debugging test failures, investigating test flakiness, or when user mentions "tests failing" or "test coverage".
```

**Improvement rationale:** Added framework names (pytest, Jest), specific analysis types (failing, flaky, coverage), and explicit user language patterns that should trigger agent.

### Pattern 5: Removing Vague Language

**Problem:** Description contains generic filler words.

**Before:**
```
description: This agent helps with various database-related tasks and can assist with different types of database operations that you might need help with
```

**After:**
```
description: Searches for database query patterns, identifies SQL injection vulnerabilities, analyzes ORM usage, and validates database schema migrations. Use when auditing database code, reviewing query security, or checking migration safety.
```

**Improvement rationale:** Removed "helps with", "various", "assist with", "different types", "you might need" - replaced with specific operations and clear triggers.

## System Prompt Enhancement Patterns

### Pattern 6: Adding Concrete Examples

**Problem:** System prompt describes task abstractly without examples.

**Before:**
```
Search the codebase for API endpoints and report what you find.
```

**After:**
```
Search the codebase for API endpoints and report what you find.

Expected output format:
```
Endpoint: POST /api/users
File: src/api/users.py:45
Authentication: JWT required
Request body: {username: string, email: string, password: string}
Response: {user_id: string, created_at: timestamp}
```

Example for multiple endpoints:
[List all endpoints in above format]
```

**Improvement rationale:** Shows exact output format with concrete data structure, making agent's reporting consistent and parseable.

### Pattern 7: Specifying Step-by-Step Workflow

**Problem:** System prompt states goal without execution guidance.

**Before:**
```
Find all configuration files and check if they're valid.
```

**After:**
```
1. Use Glob to find all files matching: **/*.config.js, **/*.json, **/*.yaml
2. For each file, use Read to load content
3. Parse file format (JSON/YAML/JS)
4. Validate structure: check for required fields, type correctness, enum values
5. Report per-file: filename, valid/invalid, specific errors if invalid
6. Summary: total files, valid count, invalid count, common error patterns
```

**Improvement rationale:** Provides explicit tool sequence, validation steps, and multi-level reporting structure.

### Pattern 8: Removing Redundant Information

**Problem:** System prompt explains concepts Claude already knows.

**Before:**
```
You should use the Grep tool to search for patterns. The Grep tool is a powerful search utility that uses regular expressions to find text patterns in files. Regular expressions are patterns that describe text. When using Grep, you specify a pattern and it will search through files to find matches...
```

**After:**
```
Use Grep to search for: SQL query patterns, string concatenation in queries, unparameterized execute() calls.
```

**Improvement rationale:** Removed explanation of Grep and regex (Claude already knows), kept only domain-specific search targets.

### Pattern 9: Adding Domain-Specific Constraints

**Problem:** System prompt doesn't include relevant validation or constraints.

**Before:**
```
Search for authentication patterns and report them.
```

**After:**
```
Search for authentication patterns and report them.

Constraints:
- Flag any hardcoded credentials (passwords, API keys, tokens)
- Identify weak password validation (no length requirement, no complexity check)
- Check for missing rate limiting on login endpoints
- Verify session timeout configuration
- Confirm secure cookie flags (httpOnly, secure, sameSite)

Security severity levels:
- Critical: Hardcoded credentials, missing authentication
- High: Weak validation, missing rate limiting
- Medium: Suboptimal configuration, missing security flags
- Low: Improvements recommended but not security holes
```

**Improvement rationale:** Added security-specific constraints, severity classification, and concrete criteria for categorization.

### Pattern 10: Clarifying Output Format

**Problem:** Agent returns inconsistent or hard-to-parse output.

**Before:**
```
Report your findings.
```

**After:**
```
Report in this exact structure:

## Summary
- Total files analyzed: [count]
- Issues found: [count]
- Critical: [count], High: [count], Medium: [count], Low: [count]

## Issues by Severity

### Critical
- file_path:line_number | issue_type | description | recommended_fix

### High
- file_path:line_number | issue_type | description | recommended_fix

[Continue for Medium, Low]

## Recommendations
[Prioritized action items]
```

**Improvement rationale:** Specifies exact markdown structure, delimiters, and organization, making output consistent and parseable.

## Tool Configuration Optimization Patterns

### Pattern 11: Removing Unnecessary Restrictions

**Problem:** Tool restrictions unnecessarily limit agent capability.

**Before:**
```yaml
tools: Read, Grep
```
Agent needs to find files before reading them.

**After:**
```yaml
# tools field omitted - inherits all tools
```

**Improvement rationale:** Agent needs Glob to find files, Read to load them, Grep to search. Listing almost all tools defeats purpose of restriction - better to omit field.

### Pattern 12: Adding Focused Restrictions

**Problem:** Agent has unnecessary access to tools it shouldn't use.

**Before:**
```yaml
# tools field omitted
```
Agent only needs to read and analyze, but has access to Write, Edit, Bash.

**After:**
```yaml
tools: Read, Glob, Grep
```

**Improvement rationale:** Read-only analysis agent shouldn't modify files or execute commands. Restriction improves focus and security.

### Pattern 13: Preserving MCP Tool Access

**Problem:** Tool restrictions inadvertently block MCP tools.

**Before:**
```yaml
tools: Read, Write, Glob, Grep, Bash
```
Blocks all MCP tools because tools field specified.

**After (Option 1 - if MCP tools needed):**
```yaml
# tools field omitted - inherits all tools including MCP
```

**After (Option 2 - if restrictions essential):**
```yaml
tools: Read, Write, Glob, Grep, Bash, mcp__tool1, mcp__tool2
```

**Improvement rationale:** MCP tools only inherited when tools field omitted. If agent might need MCP tools (database access, API calls), either omit field or explicitly list MCP tools.

## Model Selection Optimization Patterns

### Pattern 14: Downgrading to Haiku for Simple Tasks

**Problem:** Using expensive model for simple search operations.

**Before:**
```yaml
model: sonnet  # or field omitted, defaulting to sonnet
```
Agent only performs basic Grep and Read operations with straightforward pattern matching.

**After:**
```yaml
model: haiku
```

**Improvement rationale:** Simple search-and-report tasks don't need Sonnet's reasoning capability. Haiku significantly faster and cheaper for straightforward operations.

**Haiku-appropriate patterns:**
- Find files matching pattern
- Search for specific code patterns
- Extract structured data from known formats
- Simple validation against clear criteria

### Pattern 15: Upgrading to Sonnet for Complex Analysis

**Problem:** Using Haiku for tasks requiring nuanced judgment.

**Before:**
```yaml
model: haiku
```
Agent needs to analyze code quality, identify subtle bugs, or make architectural recommendations.

**After:**
```yaml
model: sonnet
```

**Improvement rationale:** Code quality analysis, architectural assessment, and subtle bug detection require Sonnet's reasoning capability.

**Sonnet-appropriate patterns:**
- Code quality assessment
- Architectural analysis
- Security vulnerability detection (beyond pattern matching)
- Refactoring recommendations
- Complex data flow analysis

### Pattern 16: Reserving Opus for Maximum Capability

**Problem:** Using Opus unnecessarily.

**Before:**
```yaml
model: opus
```
Agent performs moderate complexity analysis that Sonnet handles well.

**After:**
```yaml
model: sonnet
```

**Improvement rationale:** Opus expensive and slower. Reserve for tasks genuinely requiring maximum capability.

**Opus-appropriate patterns (rare):**
- Extremely complex system design analysis
- Sophisticated code generation with many constraints
- Nuanced architectural decision-making
- Tasks explicitly requiring maximum reasoning capability

### Pattern 17: Using Inherit for Consistency

**Problem:** Agent model differs from main conversation unnecessarily.

**Before:**
```yaml
model: sonnet
```
No specific reason to differ from main conversation model.

**After:**
```yaml
model: inherit
```
or
```yaml
# model field omitted - defaults to configured subagent model
```

**Improvement rationale:** Maintains consistency with user's chosen model. Use inherit unless specific reason to use different model.

## Combined Optimization Examples

### Example 1: Generic Search Agent → Focused API Explorer

**Before:**
```yaml
---
name: code-searcher
description: Searches code for various patterns
---

Search the codebase for the patterns the user needs and report results.
```

**After:**
```yaml
---
name: api-endpoint-explorer
description: Searches codebase for REST API endpoint definitions, extracting route patterns, HTTP methods, request/response schemas, authentication requirements, and middleware. Use when mapping API surface, documenting endpoints, finding route handlers, or when user mentions "API", "endpoints", "routes", or "REST".
tools: Read, Glob, Grep
model: haiku
---

## Purpose
Search codebase for API endpoint definitions across Express, FastAPI, Flask, and Django frameworks.

## Workflow
1. Use Glob to find route definition files: **/*routes*.{js,py}, **/*api*.{js,py}, **/*endpoints*.{js,py}
2. Use Grep to search for route patterns: app.get, app.post, @app.route, @router, APIRouter
3. For each endpoint found, use Read to extract: route path, HTTP method, handler function, request schema, response schema, authentication middleware
4. Categorize by HTTP method and path structure

## Output Format
```
## API Endpoints Summary
Total endpoints: [count]
GET: [count] | POST: [count] | PUT: [count] | DELETE: [count]

## Endpoints by Resource

### /api/users
- GET /api/users | List users | Auth: JWT | File: src/routes/users.js:12
- POST /api/users | Create user | Auth: None | File: src/routes/users.js:45
- GET /api/users/:id | Get user | Auth: JWT | File: src/routes/users.js:78

[Continue for all resources]
```

## Error Handling
If no endpoints found, search for alternative patterns: route, path, endpoint, handler
Report: "No standard REST endpoints found. Alternative patterns searched: [list]"
```

**Improvements applied:**
- Pattern 1: Added specific triggers (API, endpoints, routes, REST, framework names)
- Pattern 2: Specified frameworks and file patterns
- Pattern 3: Replaced "searches" with specific actions (extracting, mapping, documenting)
- Pattern 6: Added concrete output format with example
- Pattern 7: Specified step-by-step workflow
- Pattern 12: Added tool restrictions (read-only analysis)
- Pattern 14: Downgraded to Haiku (simple search task)

### Example 2: Verbose Helper → Focused Security Auditor

**Before:**
```yaml
---
name: security-helper
description: Helps with security-related tasks
model: sonnet
---

You are a security analysis agent. Your job is to help analyze code for security issues. Security is very important because vulnerabilities can be exploited by attackers. When analyzing code, you should look for common security problems.

Start by reading files that the user mentions. Use the Read tool to read files. The Read tool allows you to access file contents. After reading, examine the code carefully for security issues like SQL injection, which happens when user input is concatenated into SQL queries, and XSS, which is cross-site scripting...

Report any security issues you find in the code.
```

**After:**
```yaml
---
name: python-security-auditor
description: Audits Python code for OWASP Top 10 vulnerabilities including SQL injection, XSS, command injection, insecure deserialization, authentication flaws, and sensitive data exposure. Searches for vulnerable patterns in database queries, user input handling, authentication logic, and cryptography usage. Use when reviewing code security, auditing Python applications, or when user mentions "security", "vulnerabilities", "OWASP", or "audit".
model: sonnet
---

## Audit Scope
Search for these vulnerability categories in Python code:

**Injection Vulnerabilities:**
- SQL: string concatenation in queries, unparameterized execute(), format strings in SQL
- Command: os.system(), subprocess with shell=True, eval(), exec()
- NoSQL: unvalidated data in MongoDB queries

**Authentication/Authorization:**
- Hardcoded credentials, weak password validation, missing rate limiting, insecure session management

**Sensitive Data:**
- Plaintext passwords, unencrypted secrets, logging sensitive data, insecure cookies

**Cryptography:**
- Weak algorithms (MD5, SHA1 for passwords), hardcoded keys, insufficient entropy

## Workflow
1. Use Glob to find Python files: **/*.py
2. Use Grep to search for vulnerability patterns (see Audit Scope)
3. For each match, use Read to analyze context and confirm vulnerability
4. Classify severity: Critical, High, Medium, Low
5. Generate fix recommendations

## Output Format
```
## Security Audit Results

### Summary
Files scanned: [count]
Vulnerabilities: [count] (Critical: X, High: Y, Medium: Z, Low: W)

### Critical Vulnerabilities
src/auth/login.py:23 | Hardcoded credentials | CRITICAL
  Code: password = "admin123"
  Impact: System compromise
  Fix: Use environment variables: os.getenv('ADMIN_PASSWORD')

[Continue for all severities]

### Recommendations
1. [Priority action items]
```

## Severity Classification
- Critical: Hardcoded credentials, SQL injection in production, RCE vulnerabilities
- High: Missing authentication, weak crypto, XSS in sensitive contexts
- Medium: Insufficient validation, missing rate limiting, weak password policy
- Low: Suboptimal practices, missing security headers, verbose error messages
```

**Improvements applied:**
- Pattern 1: Added 10+ trigger keywords
- Pattern 2: Specified language (Python) and vulnerability types
- Pattern 5: Removed vague language ("helps with", "various")
- Pattern 8: Removed redundant explanations (SQL injection definition, tool descriptions)
- Pattern 9: Added domain-specific constraints (severity classification)
- Pattern 10: Specified exact output format
- Pattern 7: Added explicit workflow steps

## Quick Reference: When to Apply Each Pattern

| Issue | Pattern | Quick Fix |
|-------|---------|-----------|
| Description lacks keywords | Pattern 1, 2, 3 | Add 5+ specific technical terms, data types, action verbs |
| Description too generic | Pattern 5 | Remove "various", "helps with", "handles" |
| System prompt verbose | Pattern 8 | Delete explanations of basic concepts |
| System prompt unclear | Pattern 7 | Add numbered workflow steps |
| Output inconsistent | Pattern 10 | Specify exact format with example |
| Missing examples | Pattern 6 | Add concrete input/output pairs |
| Tool restrictions wrong | Pattern 11, 12, 13 | Omit field unless security/focus benefit |
| Model too powerful | Pattern 14 | Use Haiku for simple searches |
| Model underpowered | Pattern 15 | Use Sonnet for complex analysis |
| Model inconsistent | Pattern 17 | Use inherit unless specific reason |
| Missing constraints | Pattern 9 | Add validation rules, severity levels |
| Vague activation | Pattern 4 | Add context-specific triggers |
