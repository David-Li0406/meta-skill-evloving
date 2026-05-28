---
id: web_performance
name: Web Performance Analysis (Chrome DevTools)
version: 3.0.0
category: performance
description: Interactive web performance analysis using Chrome DevTools MCP - live profiling, network inspection, caching analysis, and real-time debugging

tool_configs:
  - name: perf_analyze
    description: Get structured guidance for Chrome DevTools MCP-based performance analysis
    method: analyze_performance
    args:
      - name: url
        type: string
        required: true
        description: The URL to analyze
    requires_skill_loaded: true

  - name: perf_check_caching
    description: Get guidance for analyzing caching headers and strategies
    method: check_caching
    args:
      - name: url
        type: string
        required: true
        description: The URL to check caching for
    requires_skill_loaded: true

  - name: perf_analyze_api
    description: Get guidance for analyzing API/XHR performance
    method: analyze_api_calls
    args:
      - name: url
        type: string
        required: true
        description: The URL to analyze API calls for
    requires_skill_loaded: true

  - name: perf_recommendations
    description: Get optimization recommendations based on analysis
    method: get_recommendations
    args:
      - name: metrics
        type: string
        required: true
        description: JSON string or description of performance metrics
    requires_skill_loaded: true

resource_configs:
  - name: cwv_thresholds
    description: Core Web Vitals threshold reference (2024)

  - name: caching_headers
    description: Caching headers reference and best practices

  - name: network_timing
    description: Network timing phases and targets

mcp_tool_configs:
  - server: chrome-devtools
    tools:
      - list_pages
      - select_page
      - new_page
      - navigate_page
      - performance_start_trace
      - performance_stop_trace
      - performance_analyze_insight
      - list_network_requests
      - get_network_request
      - take_screenshot
      - take_snapshot
---

# Web Performance Analysis Skill (Chrome DevTools MCP)

This skill provides **interactive browser-based performance analysis** using Chrome DevTools MCP. It enables live profiling, network inspection, and real-time debugging.

## When to Use This Skill

| Use Case | This Skill (DevTools) | Lighthouse Skill |
|----------|----------------------|------------------|
| Interactive debugging | Yes | No |
| Network request inspection | Yes | No |
| Live profiling with traces | Yes | No |
| Authenticated page analysis | Yes | No |
| API/XHR performance | Yes | No |
| Quick automated audit | No | Yes |
| CI/CD testing | No | Yes |

## Prerequisites

This skill requires the **chrome-devtools** MCP server to be enabled.

---

## Chrome DevTools MCP Tools Reference

| MCP Tool | Description | Use When |
|----------|-------------|----------|
| `performance_start_trace` | Start performance recording | Beginning of analysis |
| `performance_stop_trace` | Stop and get trace results | After page interaction |
| `performance_analyze_insight` | Get detailed insights | Investigating specific metrics |
| `list_network_requests` | List all network requests | Analyzing request patterns |
| `get_network_request` | Get request details + headers | Checking caching, timing |
| `navigate_page` | Navigate to URL | Loading target page |
| `take_screenshot` | Capture page state | Visual verification |

---

## Analysis Workflows

### 1. Full Performance Trace

```
1. mcp__chrome-devtools__new_page(url="about:blank")
2. mcp__chrome-devtools__performance_start_trace(reload=true, autoStop=true)
3. mcp__chrome-devtools__navigate_page(url="https://example.com")
4. Wait for trace to complete
5. mcp__chrome-devtools__performance_analyze_insight(...)
```

### 2. Network Analysis

```
1. mcp__chrome-devtools__navigate_page(url="https://example.com")
2. mcp__chrome-devtools__list_network_requests()
3. For each slow request: mcp__chrome-devtools__get_network_request(reqid=N)
4. Analyze timing, caching headers, payload sizes
```

### 3. API Performance Check

```
1. Navigate to the page
2. mcp__chrome-devtools__list_network_requests(resourceTypes=["xhr", "fetch"])
3. Identify slow API calls (>500ms)
4. Check for waterfall issues (sequential vs parallel)
5. Analyze auth/token refresh patterns
```

---

## Core Web Vitals Reference

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | <= 2.5s | 2.5s - 4.0s | > 4.0s |
| INP | <= 200ms | 200ms - 500ms | > 500ms |
| CLS | <= 0.1 | 0.1 - 0.25 | > 0.25 |
| FCP | <= 1.8s | 1.8s - 3.0s | > 3.0s |
| TTFB | <= 0.8s | 0.8s - 1.8s | > 1.8s |

---

## Network Timing Breakdown

| Phase | Description | Target | Action if Slow |
|-------|-------------|--------|----------------|
| **Queuing** | Waiting for network slot | < 10ms | Reduce concurrent requests |
| **Stalled** | Waiting before request | < 50ms | Check for blocking resources |
| **DNS** | Domain name resolution | < 50ms | Use DNS prefetch, faster DNS |
| **Initial Connection** | TCP handshake | < 100ms | Use HTTP/2, connection pooling |
| **SSL** | TLS negotiation | < 100ms | Use TLS 1.3, session resumption |
| **TTFB** | Server processing | < 200ms | Optimize backend, use caching |
| **Content Download** | Transfer bytes | Varies | Compress, use CDN, optimize size |

---

## Caching Headers Reference

### Cache-Control Directives

| Directive | Description | Use Case |
|-----------|-------------|----------|
| `max-age=N` | Fresh for N seconds | All cacheable resources |
| `s-maxage=N` | CDN cache time | CDN-specific caching |
| `no-cache` | Must revalidate | Dynamic content |
| `no-store` | Never cache | Sensitive data |
| `immutable` | Never changes | Versioned assets |
| `public` | Any cache can store | Public resources |
| `private` | Browser only | User-specific data |

### Recommended Cache Settings

| Resource Type | Cache-Control Value | TTL |
|---------------|---------------------|-----|
| Versioned JS/CSS | `max-age=31536000, immutable` | 1 year |
| Images | `max-age=2592000` | 30 days |
| Fonts | `max-age=31536000` | 1 year |
| HTML | `no-cache` or `max-age=0` | Always revalidate |
| API responses | `max-age=0, must-revalidate` | Based on freshness |

---

## Common Performance Issues

### Slow API Responses

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| TTFB > 500ms | Slow server processing | Optimize queries, add caching |
| Sequential calls | Waterfall pattern | Batch or parallelize requests |
| Repeated auth calls | Token refresh issues | Cache tokens, use refresh tokens |
| Large payloads | Over-fetching data | Pagination, field selection |

### Caching Problems

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| No Cache-Control | Missing headers | Add appropriate cache headers |
| Short max-age | Conservative caching | Extend TTL for static assets |
| No ETag | Missing validation | Add ETag for conditional requests |
| Missing compression | No gzip/brotli | Enable server compression |

### Render Blocking

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| Late FCP | CSS blocking render | Inline critical CSS |
| High TBT | JS blocking main thread | Defer non-critical JS |
| Layout shifts | Late-loading content | Reserve space, preload |

---

## Resource Size Guidelines

| Resource Type | Recommended Size | Notes |
|---------------|------------------|-------|
| HTML | < 100KB | After compression |
| CSS (critical) | < 14KB | Inlined in `<head>` |
| CSS (total) | < 100KB | All stylesheets combined |
| JavaScript (initial) | < 200KB | Parsed JS for initial load |
| JavaScript (total) | < 500KB | All JS combined |
| Images (hero) | < 200KB | Above-the-fold images |
| Fonts | < 100KB | All fonts combined |
| Total Page Weight | < 2MB | Entire page resources |

---

## Request Count Guidelines

| Resource Type | Recommended Max | Notes |
|---------------|-----------------|-------|
| Total requests | < 50 | For initial page load |
| JavaScript files | < 10 | Use bundling |
| CSS files | < 5 | Combine stylesheets |
| Images | < 20 | Lazy load below-fold |
| Fonts | < 4 | Subset, use system fonts |
| Third-party requests | < 10 | Audit third-party impact |

---

## Tool Selection: DevTools vs Lighthouse

| Need | Use DevTools MCP | Use Lighthouse CLI |
|------|-----------------|-------------------|
| Automated audit score | No | Yes |
| Live network inspection | Yes | No |
| Authenticated pages | Yes | Limited |
| Performance traces | Yes | Limited |
| CI/CD integration | No | Yes |
| Interactive debugging | Yes | No |
| API call analysis | Yes | No |
| Caching header inspection | Yes | Limited |

---

## Configuration

### Chrome DevTools MCP Server

The chrome-devtools MCP server must be enabled in `mcp_servers.json`:

```json
{
  "chrome-devtools": {
    "name": "Chrome DevTools",
    "description": "Control and inspect Chrome browsers",
    "command": "npx",
    "args": ["-y", "chrome-devtools-mcp@latest"],
    "enabled": true,
    "timeout_seconds": 60
  }
}
```
