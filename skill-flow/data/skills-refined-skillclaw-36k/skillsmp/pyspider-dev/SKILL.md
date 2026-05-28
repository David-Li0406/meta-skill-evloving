---
name: pyspider-dev
description: "Production-ready PySpider web crawler development toolkit. Use when: (1) Creating new PySpider crawlers for web scraping, (2) Implementing complex crawling with proxies and retries, (3) Handling pagination, authentication, and data extraction, (4) Building enterprise-grade crawlers with error handling. Provides templates, patterns, and best practices for reliable scraping."
---

# PySpider Development

Production-ready PySpider crawler development with templates, patterns, and enterprise-grade practices.

## Decision Tree

Choose your approach based on task complexity:

| Scenario | Template | Reference to Load |
|----------|----------|-------------------|
| Simple HTML scraping (GET only) | Standard Template | SKILL.md only |
| API calls with POST/headers | Advanced Template | api_reference.md (crawl method) |
| Production with proxy rotation | Enterprise Template | api_reference.md (Proxy Management) |
| Pagination handling | Custom + Patterns | api_reference.md (Common Patterns) |
| JavaScript rendering | Custom + JS support | api_reference.md (fetch_type='js') |
| Authentication required | Custom + Auth patterns | api_reference.md (Header Management) |
| Error handling & retry | Custom + Error patterns | api_reference.md (on_error) |
| Database operations | Custom + DB patterns | api_reference.md (Database) |

**Generate templates using**:
```bash
python scripts/init_crawler.py MyCrawler ./projects/my_crawler.py --template=standard
python scripts/init_crawler.py ApiCrawler ./projects/api.py --template=advanced
python scripts/init_crawler.py EnterpriseSpider ./projects/enterprise.py --template=enterprise
```

## Workflow

### Step 1: Choose Template

Based on decision tree above, select appropriate template or use `init_crawler.py` script.

### Step 2: Customize Crawler

Modify the template to fit your target website:
- Update `crawl_config` with proper headers and timeouts
- Implement `on_start()` to initiate crawling
- Add callback functions for response processing

### Step 3: Implement Patterns

Load [`api_reference.md`](references/api_reference.md) for advanced patterns:
- **Pagination**: URL-based or AJAX-based
- **Proxy rotation**: For production crawlers
- **Error handling**: Retry logic with exponential backoff
- **Data deduplication**: Avoid duplicate items
- **Authentication**: Cookie-based or token-based

### Step 4: Test and Deploy

Test locally with small data, then scale to production.

## NEVER Do These (Anti-Patterns)

### Critical Errors (Will Fail)

- ❌ **NEVER use `on_result` method** - PySpider doesn't support it
- ❌ **NEVER use `fetch_type='js'` without PhantomJS** - Will fail silently
- ❌ **NEVER use blocking operations** - PySpider is async, avoid `time.sleep()` in callbacks
- ❌ **NEVER ignore `on_message`** - Required for inter-project communication and data storage

### Common Mistakes

- ❌ **NEVER hardcode URLs** - Use configuration or environment variables
- ❌ **NEVER skip proxy rotation in production** - Will get blocked
- ❌ **NEVER ignore rate limiting** - Respect server limits, add delays
- ❌ **NEVER forget data validation** - Always verify response integrity
- ❌ **NEVER use same taskid for dynamic content** - Use timestamp: `taskid=f"{url}|{time.time()}"`
- ❌ **NEVER assume response is JSON** - Check `Content-Type` or use try/except
- ❌ **NEVER ignore SSL certificate errors in production** - Security risk
- ❌ **NEVER store sensitive data in logs** - Credentials, tokens, passwords

### Performance Anti-Patterns

- ❌ **NEVER fetch all pages sequentially** - Use concurrent crawling with proper task management
- ❌ **NEVER parse entire HTML if not needed** - Use specific selectors
- ❌ **NEVER download unnecessary resources** - Images, CSS, JS (disable with `load_images=False`)
- ❌ **NEVER retry indefinitely** - Set max retry limits (3-5 attempts)
- ❌ **NEVER use same proxy for all requests** - Rotate proxies to avoid blocking

## Core Architecture

Every PySpider crawler inherits from `BaseHandler`:

**Required Methods**:
- `on_start()`: Entry point - initiate crawling tasks
- `callback functions`: Process HTTP responses

**Optional Methods**:
- `on_message(project, message)`: Handle inter-project messages and data storage
- `on_error(exception, response)`: Handle errors with retry logic

**⚠️ CRITICAL**: Use `on_message` for data storage, **NOT** `on_result` (PySpider doesn't support it).

## Quick Reference

### Essential Parameters

| Parameter | Type | When to Use | Default |
|-----------|------|-------------|---------|
| `user_agent` | str | Always set for production | PySpider/0.7 |
| `timeout` | int | Slow sites (60-120s) | 120 |
| `retries` | int | Unstable sites (5-10) | 3 |
| `proxy` | str | Single proxy needed | None |
| `age` | int | Cache control (0=no cache) | 0 |
| `validate_cert` | bool | Self-signed certs | True |

### Common Decorators

| Decorator | When to Use |
|-----------|-------------|
| `@every(minutes=60)` | Scheduled execution only |
| `@config(age=86400)` | Cache for 1 day |
| `@config(priority=9)` | High priority task |
| `@catch_status_code_error` | Handle non-200 responses |

### Response Object

```python
response.url              # Final URL (after redirects)
response.status_code      # HTTP status code
response.text             # Response body as text
response.json             # Parsed JSON (if applicable)
response.doc              # PyQuery object (jQuery-like)
response.save             # State from `save` parameter
response.cookies          # Response cookies
```

## Loading Triggers

### MANDATORY - Loading Rules

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`api_reference.md`](references/api_reference.md) (~733 lines) completely.
**NEVER set range limits when reading this file.**

### Conditional Loading

| Task Type | Must Load | Do NOT Load |
|-----------|-----------|-------------|
| Basic GET crawler | SKILL.md only | api_reference.md (full) |
| POST requests | api_reference.md (crawl method) | Enterprise patterns |
| Proxy management | api_reference.md (Proxy Management) | Standard template |
| Error handling | api_reference.md (on_error) | Basic patterns |
| JavaScript rendering | api_reference.md (fetch_type='js') | HTML patterns |
| Database operations | api_reference.md (Database) | Basic patterns |

### When to Load References

**Load `api_reference.md` completely when**:
- Implementing advanced features (cURL support, JavaScript rendering)
- Working with database operations
- Implementing complex patterns (deduplication, form handling)
- Need detailed API method or parameter information

**Use SKILL.md only when**:
- Creating basic crawler templates
- Understanding core architecture
- Quick reference for common patterns

## Progress Report Format

When working on PySpider tasks, report progress as:

```
✅ Template created: [template_name]
⏳ Implementing: [feature_name]
❌ Error: [error_description] - [solution]
📊 Stats: [pages crawled] / [total pages]
```

## Request Input Format

When requesting PySpider development, provide:

```
Target URL: [URL]
Data to extract: [list of fields]
Authentication: [method if any]
Pagination: [type if any]
Special requirements: [proxies, rate limiting, etc.]
```

## Common Patterns Summary

| Pattern | Use Case | Key Technique |
|---------|----------|---------------|
| Pagination | Multi-page content | URL params or AJAX |
| Proxy Rotation | Production crawling | Proxy pool + retry |
| Error Handling | Unstable network | `on_error` + exponential backoff |
| Deduplication | Avoid duplicates | Database check or in-memory set |
| Authentication | Protected pages | Cookies or Bearer tokens |
| Form Handling | Submit forms | Extract form data + POST |

For detailed implementation of these patterns, see [`api_reference.md`](references/api_reference.md).
