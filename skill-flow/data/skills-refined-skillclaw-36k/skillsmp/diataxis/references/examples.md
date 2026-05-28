# Real-World Diataxis Examples

Complete, production-grade examples for each documentation type.

## Table of Contents
1. [Example 1: Tutorial](#example-1-tutorial)
2. [Example 2: How-to Guide](#example-2-how-to-guide)
3. [Example 3: Reference](#example-3-reference)
4. [Example 4: Explanation](#example-4-explanation)

---

## Example 1: Tutorial

**Source**: Getting started with a Python web framework

```markdown
# Your First Django App

Create a simple blogging application with posts and comments.

## What you'll build

A working blog where you can create, read, and delete posts. By the end, 
you'll understand Django's MVT (Model-View-Template) architecture.

## Before you start

- Python 3.8+ installed
- pip installed
- Basic familiarity with command line
- A code editor (VS Code, Sublime, etc.)

## Step 1: Create a project directory

```bash
mkdir my_blog
cd my_blog
```

Notice that you're now inside the directory. Your prompt should show `my_blog` 
in the path.

## Step 2: Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

The prompt should now start with `(venv)`. This means the virtual 
environment is active.

## Step 3: Install Django

```bash
pip install django
```

Wait a moment for installation. You should see "Successfully installed Django" 
in your terminal.

## Step 4: Create a Django project

```bash
django-admin startproject blog_config .
django-admin startapp blog
```

You should see new folders: `blog_config/` and a `blog/` folder.

## Step 5: Run the development server

```bash
python manage.py runserver
```

The output will show:

```
Starting development server at http://127.0.0.1:8000/
```

Open your browser and visit `http://127.0.0.1:8000/`. You should see 
Django's welcome page.

## Step 6: Create a simple model

Edit `blog/models.py`:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

Notice that we've defined what a Post is: it has a title, content, and 
creation timestamp.

## What you've built

You've created a Django project with a Post model. You now understand how 
Django organizes projects, applications, and data models. Your development 
server is running, and you can extend it by creating views and templates.

## Next steps

- **Customize it**: [How to add comment functionality](...)
- **Understand it**: [About Django's MVT architecture](...)
- **Explore**: [Django models reference](...)
```

---

## Example 2: How-to Guide

**Source**: Deploying a database migration

```markdown
# How to migrate a PostgreSQL database with zero downtime

This guide shows you how to move your database to a new server while 
keeping your application running.

## When to use this guide

Use this when you need to move PostgreSQL to new infrastructure 
(new server, new provider, new region) while serving live traffic.

## Before you start

- PostgreSQL 9.5+ on both source and destination
- A standby server or read replica capability
- SSH access to both servers
- About 30-60 minutes of work

## Context

Zero-downtime migration works by setting up replication from your old 
database to the new one, letting it catch up, then switching your 
application to use the new server. The entire switch takes seconds.

## Steps

### 1. Set up replication from source to destination

```bash
psql -h source-server -U postgres -c "SELECT pg_start_backup('migration', true);"
```

This creates a consistent backup point that the destination can follow.

### 2. Backup the source database

```bash
pg_basebackup -h source-server -D /var/lib/postgresql/backup -P -v
```

This creates a full backup of your source database. On a large database, 
this may take several minutes.

### 3. Start replication on destination

```bash
psql -h dest-server -c "ALTER SYSTEM SET primary_conninfo = 'host=source-server ...'"
pg_ctl -D /path/to/data restart
```

Wait 5-10 seconds for replication to establish. Check status with `pg_stat_replication` 
on the source.

### 4. Monitor replication lag

```bash
psql -h source-server -U postgres -c "SELECT slot_name, restart_lsn, confirmed_flush_lsn FROM pg_replication_slots;"
```

Replication lag is normal. Wait until it reaches zero before switching.

### 5. Switch application to use destination

Update your connection string to point to the new server. This typically takes 
2-5 seconds per application instance.

```bash
# Update config and restart app
systemctl restart myapp
```

### 6. Verify everything works

```bash
psql -h dest-server -c "SELECT count(*) FROM [your_table];"
```

Compare the row count to your source. They should match.

## Troubleshooting

**Problem: Replication lag is too high**
Solution: The source is getting too much write traffic during migration. 
Reduce application load or increase network bandwidth. Lag is normal; wait 
until it syncs before switching.

**Problem: Application fails after switching**
Solution: Check your new connection string. A common issue is firewall 
blocking the new destination. Test connectivity: `pg_isready -h dest-server`

**Problem: Replication doesn't start**
Solution: Ensure the destination server is empty or a clean backup. Also 
verify network connectivity: `ping dest-server` and check firewall rules 
for port 5432.

## Variations

If you're using Amazon RDS, use AWS Database Migration Service instead. 
It handles replication automatically.

If you're on MySQL, the process is similar but use `mysqldump` and 
`mysqlbinlog` for replication.

## Related guides

- [How to set up read replicas](...)
- [How to monitor replication lag](...)
- [How to handle network failures during migration](...)

## See also

- [About PostgreSQL replication architecture](...)
- [Troubleshooting PostgreSQL connection issues](...)
```

---

## Example 3: Reference

**Source**: API endpoint reference

```markdown
# POST /api/articles Reference

Create a new article.

## Request

**Endpoint**: `POST /api/articles`

**Authentication**: Required. Bearer token in Authorization header.

**Headers**
| Header | Value |
|--------|-------|
| Authorization | `Bearer {jwt_token}` |
| Content-Type | `application/json` |

**Body**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Article title, 1-200 characters |
| content | string | Yes | Article body, 1-50000 characters |
| published | boolean | No | Default: false. If true, article is immediately visible |
| tags | array | No | Up to 10 tags. Each 1-50 characters |

## Response

**Status**: 201 Created

**Body**
```json
{
  "id": "art_abc123",
  "title": "My Article",
  "content": "...",
  "published": false,
  "tags": ["tech", "tutorial"],
  "created_at": "2025-12-19T10:30:00Z",
  "updated_at": "2025-12-19T10:30:00Z"
}
```

## Example

```bash
curl -X POST https://api.example.com/api/articles \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with API",
    "content": "This is my first article...",
    "tags": ["api", "guide"]
  }'
```

## Errors

| Status | Code | Meaning |
|--------|------|---------|
| 400 | invalid_input | Title or content missing, or exceeds limits |
| 401 | unauthorized | Token missing or invalid |
| 403 | forbidden | User lacks permission to create articles |
| 409 | duplicate | Title already exists (if title uniqueness enforced) |

## Notes

- Articles are created in draft status by default. Publish them separately.
- Titles must be unique across your account.
- Content supports Markdown formatting.
- Maximum request size: 1MB
```

---

## Example 4: Explanation

**Source**: Understanding API rate limiting

```markdown
# About API rate limiting

Rate limiting is the practice of restricting how many requests a client 
can make to an API in a given time window.

## Background

Early APIs had no limits, which led to problems: a single misbehaving 
client could overwhelm the server, hurting all users. As APIs became 
critical infrastructure, rate limiting became essential—as important 
as circuit breakers in electrical systems.

Different services implement rate limiting differently. Some (like AWS) 
tie it to your plan. Others (like Twitter) tie it to your authentication. 
This reflects different business models and reliability needs.

## The core concept

Rate limiting works by associating requests with an identity (API key, 
user, IP address) and counting them. When a request would exceed the 
limit, it's rejected with a 429 status.

From the user's perspective, rate limits represent a contract: "You can 
make this many requests per minute. Plan accordingly."

## Token bucket vs. sliding window

Rate limiting algorithms fall into two main categories.

**Token bucket** (used by most modern APIs) works like a bucket that 
refills at a constant rate. Every request costs one token. When the bucket 
is empty, requests are denied. This approach allows bursts: if you didn't 
use your tokens, you can use more now.

Example: Stripe allows 100 requests per second, but with token bucket 
algorithm, you could make 500 requests in 5 seconds if you hadn't made 
any requests before.

**Sliding window** counts requests in a rolling time window. Strictly 
enforces the limit over any N-second window. This prevents bursts, which 
is useful for protecting against denial-of-service attacks.

Google Cloud uses sliding window. You get a hard cap: no more than 1000 
requests per minute, period.

## Why your API cares about limits

Protecting infrastructure is one reason, but not the only reason:

- **Fairness**: Ensures one large customer doesn't monopolize resources
- **Predictability**: Users can build reliable systems if they know the limit
- **Cost management**: For usage-based pricing, limits enforce billing tiers
- **Security**: Limits prevent brute-force attacks (credential stuffing, DDoS)

## Comparison to authentication

Rate limiting is often confused with authentication, but they're distinct:

- **Authentication** answers: "Who are you?" (Validated by token)
- **Rate limiting** answers: "How much can you do?" (Enforced by counter)

You can be authenticated (pass token) but rate-limited (hit the ceiling). 
This is actually a good design: it lets legitimate users be identified 
while still protecting the service.

## Different perspectives

Some argue rate limits should be generous because they build trust: "If 
you trust me, let me make 10,000 requests per minute." This is good for 
developer experience during development.

Others argue limits should be strict because one bad client can hurt 
everyone: "Everyone gets 100 requests per minute, no exceptions." This 
protects the service.

Most production APIs do both: generous limits for authenticated users 
(based on their plan) and very strict limits for unauthenticated requests.

## Further reading

- **Learn it**: [Tutorial: Handling rate limit responses](...)
- **Use it**: [How to design rate limits for your API](...)
- **Details**: [Rate limits reference documentation](...)
```

---

## Using These Examples

Each example above is **production-ready code** you can:
- Copy and adapt for your own documentation
- Use as a reference when writing similar documentation
- Share with your team as a style guide
- Test to ensure it actually works

The examples follow the principles and language patterns from their respective template files.
