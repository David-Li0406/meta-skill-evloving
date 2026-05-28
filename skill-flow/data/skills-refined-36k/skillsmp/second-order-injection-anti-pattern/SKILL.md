---
name: "second-order-injection-anti-pattern"
description: "Security anti-pattern for second-order injection vulnerabilities (CWE-89 variant). Use when generating or reviewing code that retrieves data from databases, caches, or storage and uses it in subsequent queries or commands. Detects trusted internal data used unsafely."
---

# Second-Order Injection Anti-Pattern

**Severity:** High

## Summary

Malicious payloads are stored safely in databases or logs, then executed later when retrieved and used without re-sanitization. Initial storage appears secure (properly parameterized), but subsequent retrieval and unsafe use activates the payload. Injection and execution points are separated in time and code location, making detection difficult.

## The Anti-Pattern

The anti-pattern is treating database-retrieved data as safe and using it in queries or commands without re-sanitization or parameterization.

### BAD Code Example

```python
# VULNERABLE: Data is stored safely, but later retrieved and used unsafely.
import sqlite3

db = sqlite3.connect("app.db")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, action TEXT, user_email TEXT)")

# Step 1: User Registration (appears safe)
def register_user(name, email):
    # Parameterized query, safe against direct injection.
    # Attacker email: "bad@example.com' UNION SELECT password FROM users -- "
    # Safely stored as string in 'email' column.
    db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    db.commit()

# Step 2: Logging (VULNERABLE on retrieval)
def log_user_action(user_id, action):
    # Retrieve user email from database.
    cursor = db.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    user_email = cursor.fetchone()[0]

    # FLAW: user_email concatenated into query.
    # Application "trusts" data from own database.
    log_query = f"INSERT INTO logs (action, user_email) VALUES ('{action}', '{user_email}')"

    # Result: INSERT INTO logs (action, user_email) VALUES ('view_profile', 'bad@example.com' UNION SELECT password FROM users -- ')
    # Injected SQL executes, exposing passwords.
    db.execute(log_query)
    db.commit()

# Attack: Register with crafted email → trigger logging → payload executes.
```

### GOOD Code Example

```python
# SECURE: All data used in SQL queries is parameterized, regardless of its source.
import sqlite3

db = sqlite3.connect("app_safe.db")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, action TEXT, user_email TEXT)")

# Step 1: User Registration (safe)
def register_user_safe(name, email):
    db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    db.commit()

# Step 2: Logging (safe)
def log_user_action_safe(user_id, action):
    cursor = db.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    user_email = cursor.fetchone()[0]

    # SECURE: Database-retrieved user_email still treated as untrusted.
    # Passed as parameter, not concatenated.
    db.execute("INSERT INTO logs (action, user_email) VALUES (?, ?)", (action, user_email))
    db.commit()
```

## Detection

- **Audit data flows:** Systematically track data from its entry point (user input) through its storage and subsequent retrieval and use.
- **Identify dynamic query/command construction:** Look for any code that builds SQL queries, shell commands, or other interpretive language statements by concatenating strings that include variables whose values originated from user input, even if they were stored in a database.
- **Review stored procedures:** If your application uses stored procedures, examine their definitions for any dynamic SQL that might use input parameters without proper escaping or parameterization.
- **Consider background jobs/asynchronous tasks:** Pay special attention to components that process data in the background, as they might retrieve stored data and use it in new, insecure contexts.

## Prevention

- [ ] **Parameterize all queries:** Always use prepared statements for all database interactions, regardless of data source (user input or database retrieval).
- [ ] **Never trust database data:** Treat database-retrieved data as tainted if it originated from user input. Apply same validation/sanitization as fresh input.
- [ ] **Use ORMs consistently:** ORMs auto-parameterize queries when used correctly. Avoid "raw query" features bypassing protections.
- [ ] **Escape output before display:** Defense-in-depth against XSS when rendering database data in HTML.

## Related Security Patterns & Anti-Patterns

- [SQL Injection Anti-Pattern](../sql-injection/): Second-order SQL injection is a variant of this fundamental vulnerability.
- [Command Injection Anti-Pattern](../command-injection/): Similar second-order risks exist when data stored safely is later used in an insecure shell command.
- [Log Injection Anti-Pattern](../log-injection/): Log files can be a vector for second-order attacks if logged data is later used in an insecure context (e.g., parsing logs with a vulnerable regex).

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM01:2025 - Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP Second Order SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html)
- [CAPEC-66: SQL Injection](https://capec.mitre.org/data/definitions/66.html)
- [PortSwigger: Sql Injection](https://portswigger.net/web-security/sql-injection)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
