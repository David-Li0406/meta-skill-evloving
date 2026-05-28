---
name: wos-errors
description: Review and debug application errors. Shows recent errors from the database, analyzes stack traces, and helps fix issues. Use when you receive an error notification email or want to check for issues.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# WoS Error Review - Debug and Fix Application Errors

## Purpose
Review errors logged to the database, analyze stack traces, identify root causes, and implement fixes. This skill is triggered when:
- User receives an error notification email
- User wants to check for recent errors
- Proactive error monitoring

## Quick Start

### Check Recent Errors
```python
# Run this to see recent errors
import sys
sys.path.insert(0, 'C:/Users/adam/PycharmProjects/WoS')
from utils.error_logger import get_recent_errors, get_error_summary

# Get summary
summary = get_error_summary()
print(f"Error Summary: {summary}")

# Get recent errors
errors = get_recent_errors(limit=10, status='new')
for e in errors:
    print(f"\n#{e.id} [{e.error_type}] {e.page or 'Unknown page'}")
    print(f"  Message: {e.error_message[:100]}")
    print(f"  Time: {e.created_at}")
    print(f"  User: {e.user_id or 'Anonymous'}")
```

### View Full Error Details
```python
from database.db import get_db
from database.models import ErrorLog

db = get_db()
error = db.query(ErrorLog).filter(ErrorLog.id == ERROR_ID).first()

print(f"Error Type: {error.error_type}")
print(f"Message: {error.error_message}")
print(f"Page: {error.page}")
print(f"Function: {error.function}")
print(f"User ID: {error.user_id}")
print(f"Environment: {error.environment}")
print(f"\nStack Trace:\n{error.stack_trace}")
print(f"\nExtra Context: {error.extra_context}")
```

## Error Review Workflow

### 1. Get Error Summary
First, check how many errors exist and their statuses:
```python
from utils.error_logger import get_error_summary
summary = get_error_summary()
# Returns: {'new': 5, 'reviewed': 2, 'fixed': 10, 'ignored': 1, 'last_24h': 3}
```

### 2. Review New Errors
Get detailed info on new errors:
```python
from utils.error_logger import get_recent_errors
errors = get_recent_errors(limit=20, status='new')
```

### 3. Analyze Stack Trace
For each error:
1. Read the stack trace to identify the failing line
2. Use Grep/Read to examine the source code
3. Identify the root cause

### 4. Implement Fix
1. Edit the source file to fix the bug
2. Add error handling if appropriate
3. Test the fix locally

### 5. Mark as Fixed
```python
from utils.error_logger import mark_error_reviewed
mark_error_reviewed(
    error_id=123,
    reviewer_id=1,  # Admin user ID
    fix_notes="Fixed null check in hero_analyzer.py line 45",
    new_status='fixed'
)
```

## Common Error Patterns

### Database Errors
**Pattern:** `sqlalchemy.exc.OperationalError`
**Common Causes:**
- Database locked (another process has it open)
- Missing column (schema migration needed)
- Connection timeout

**Fix Steps:**
1. Check if wos.db is locked by another process
2. Verify schema matches models.py
3. Run migrations if needed

### JSON Decode Errors
**Pattern:** `json.decoder.JSONDecodeError`
**Common Causes:**
- Corrupted JSON file
- Encoding issues
- Trailing commas

**Fix Steps:**
1. Identify which JSON file
2. Validate JSON syntax
3. Check for encoding='utf-8' in open()

### Key Errors
**Pattern:** `KeyError` in data access
**Common Causes:**
- Missing field in JSON data
- Session state not initialized
- User data not found

**Fix Steps:**
1. Add .get() with default value
2. Check data source completeness
3. Add proper initialization

### Attribute Errors
**Pattern:** `AttributeError: 'NoneType' has no attribute`
**Common Causes:**
- Database query returned None
- Optional field accessed without check

**Fix Steps:**
1. Add None check before access
2. Verify query filters
3. Add fallback values

## Error Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| new | Just occurred, not reviewed | Review and fix |
| reviewed | Looked at, needs fix | Implement fix |
| fixed | Fix implemented | Verify in production |
| ignored | Not a real issue | No action needed |

## Database Schema

The `error_logs` table stores:
- `id` - Unique error ID
- `error_type` - Exception class name
- `error_message` - Exception message
- `stack_trace` - Full traceback
- `page` - Which page/module
- `function` - Function name
- `user_id` - User who triggered it (if logged in)
- `profile_id` - Active profile ID
- `session_id` - Streamlit session
- `extra_context` - JSON with additional debug info
- `environment` - production/staging/development
- `status` - new/reviewed/fixed/ignored
- `reviewed_by` - Admin who reviewed
- `fix_notes` - Notes about the fix
- `email_sent` - Whether notification was sent
- `created_at` - When error occurred

## Email Notifications

Errors in production/staging environments automatically send email to:
- `ADMIN_EMAIL` environment variable (default: adam@randomchaoslabs.com)

Email includes:
- Error type and message
- Page and function
- User ID (if logged in)
- Full stack trace
- Link to review

## Adding Error Handling to New Code

Use the `@handle_errors` decorator:
```python
from utils.error_logger import handle_errors

@handle_errors(page="My Page")
def risky_function():
    # Your code here
    pass
```

Or manually log errors:
```python
from utils.error_logger import log_error

try:
    risky_operation()
except Exception as e:
    log_error(e, page="My Page", function="risky_operation",
              extra_context={"input": user_input})
```

## Workflow Summary

1. **Receive notification** - Error email arrives
2. **Run /wos-errors** - Review the error
3. **Analyze** - Read stack trace, find root cause
4. **Fix** - Edit code to resolve issue
5. **Test** - Verify fix locally
6. **Push to dev** - Deploy to staging
7. **Mark fixed** - Update error status
8. **Push to live** - After testing on dev
