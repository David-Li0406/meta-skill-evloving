# Security Review Checklist

Security-focused code review patterns.

**Principle:** Assume all user input is malicious. Validate at system boundaries.

---

## Critical Security Checks

### 1. No Hardcoded Secrets

```python
# ❌ REJECT: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"  # Never commit secrets!
DATABASE_PASSWORD = "password123"

# ✅ APPROVE: Secrets from environment
import os

API_KEY = os.getenv('OPENROUTER_API_KEY')
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set")
```

**Check:**
- [ ] No API keys in code
- [ ] No passwords in code
- [ ] No tokens in code
- [ ] Secrets loaded from Doppler/env vars
- [ ] `.env` files in `.gitignore`

### 2. SQL Injection Prevention

```python
# ❌ REJECT: SQL injection vulnerable
def get_report(ticker: str):
    query = f"SELECT * FROM reports WHERE symbol = '{ticker}'"
    # If ticker = "'; DROP TABLE reports; --" → SQL injection!
    cursor.execute(query)

# ✅ APPROVE: Parameterized query
def get_report(ticker: str):
    query = "SELECT * FROM reports WHERE symbol = %s"
    cursor.execute(query, (ticker,))  # Safe
```

**Check:**
- [ ] All queries use parameterized statements
- [ ] No f-strings or string concatenation in SQL
- [ ] No raw SQL from user input

### 3. XSS Prevention

```python
# ❌ REJECT: XSS vulnerable
def create_report_html(ticker: str, data: dict):
    html = f"""
    <div class="report">
        <h1>{ticker}</h1>  # If ticker = "<script>alert('XSS')</script>"
        <p>{data['summary']}</p>
    </div>
    """
    return html

# ✅ APPROVE: Escaped output
import html

def create_report_html(ticker: str, data: dict):
    safe_ticker = html.escape(ticker)
    safe_summary = html.escape(data['summary'])

    return f"""
    <div class="report">
        <h1>{safe_ticker}</h1>
        <p>{safe_summary}</p>
    </div>
    """
```

**Check:**
- [ ] HTML output escaped
- [ ] JSON output properly encoded
- [ ] No direct user input in HTML

### 4. Input Validation

```python
# ❌ REJECT: No validation
def generate_report(ticker: str):
    # Accepts any input, including malicious
    return workflow.run({'ticker': ticker})

# ✅ APPROVE: Validated input
import re

def generate_report(ticker: str):
    # Validate format
    if not re.match(r'^[A-Z0-9]{1,10}$', ticker):
        raise ValueError("Invalid ticker format")

    # Length check
    if len(ticker) > 10:
        raise ValueError("Ticker too long")

    return workflow.run({'ticker': ticker})
```

**Check:**
- [ ] Input format validated (regex, length, type)
- [ ] Whitelist validation (not blacklist)
- [ ] Validation at entry points (API handlers, webhooks)

### 5. Authentication/Authorization

```python
# ❌ REJECT: No auth check
@app.get("/api/reports/{ticker}")
def get_report(ticker: str):
    # Anyone can access!
    return db.get_report(ticker)

# ✅ APPROVE: Auth required
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/reports/{ticker}")
def get_report(ticker: str, token: str = Depends(security)):
    # Verify token
    if not verify_token(token.credentials):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Check user has permission
    if not has_permission(token.credentials, ticker):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return db.get_report(ticker)
```

**Check:**
- [ ] Authentication required for protected endpoints
- [ ] Authorization (permissions) checked
- [ ] JWT tokens validated (signature, expiration)

---

## AWS Security

### IAM Principle of Least Privilege

```python
# ❌ REJECT: Overly broad permissions
{
  "Effect": "Allow",
  "Action": "s3:*",  # All S3 actions!
  "Resource": "*"   # All resources!
}

# ✅ APPROVE: Minimal permissions
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::[PROJECT_NAME]-data-dev/*"
}
```

**Check:**
- [ ] IAM policies grant minimum required permissions
- [ ] No wildcards (`*`) unless necessary
- [ ] Resource ARNs specific (not `*`)

### Secrets Manager

```python
# ❌ REJECT: Secrets in environment variables
AURORA_PASSWORD = os.getenv('AURORA_PASSWORD')  # In plain text!

# ✅ APPROVE: Secrets Manager
import boto3

def get_secret(secret_name: str) -> dict:
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

db_credentials = get_secret('aurora-db-credentials')
```

**Check:**
- [ ] Database credentials in Secrets Manager (not env vars)
- [ ] API keys rotated regularly
- [ ] Secrets encrypted at rest

---

## Quick Reference

| Vulnerability | Check For | Prevention |
|---------------|-----------|------------|
| **SQL Injection** | String concatenation in SQL | Parameterized queries |
| **XSS** | Unescaped HTML output | html.escape() |
| **Secrets Leak** | Hardcoded keys/passwords | Environment variables, Secrets Manager |
| **SSRF** | User-controlled URLs | URL whitelist |
| **Path Traversal** | User-controlled file paths | Validate paths, use allowlist |
| **Command Injection** | Shell commands with user input | Avoid shell=True, validate input |

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
