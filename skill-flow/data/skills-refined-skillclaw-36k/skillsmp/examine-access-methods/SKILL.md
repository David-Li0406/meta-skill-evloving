---
name: examine_access_methods
description: Examine data sources to determine available access methods
agent_types: [examination, api_key]
task_keywords: [examine, analyze, access, method, api, download, fetch, parse, html, content]
---

# Skill: Data Source Access Method Examination

## Purpose
Examine a data source to determine what access methods are available (API, web service, download, etc.)

## Context
You are a technical examiner analyzing whether a data source can provide the desired data and how to access it.

## Task
Given a data source URL and user requirements:

1. **Visit and understand the source** - What does this source provide?
2. **Find API documentation** - Look for /api, /docs, /developers, /api-docs paths
3. **Check access methods** - API, SOAP, GraphQL, downloadable files, contact required
4. **Verify data relevance** - Does it provide data the user is looking for?
5. **Identify requirements** - Authentication, rate limits, permissions needed

## Available Tools
- fetch_url: Fetch and parse web page content
- check_api: Check if URL responds to API requests
- parse_html: Extract form fields and page structure

## Examination Checklist

### Check for API
- Look for /api, /v1, /v2 paths
- Check robots.txt and sitemap.xml
- Search for API documentation links
- Try /swagger.json or /openapi.json endpoints
- Look for "API Documentation" link

### Check for Web Service
- Look for /service, /ws, /soap paths
- Search for WSDL files
- Check for web service documentation

### Check for Download
- Look for /download, /export, /bulk paths
- Search for "CSV", "JSON", "XML" download links
- Check for data export functionality
- Look for database dumps or archives

### Check for Contact Required
- Search for "contact us for access"
- Look for data request forms
- Check terms of service for access restrictions
- Look for "by request" or "upon approval" language

## Output Format

Return findings as JSON:
```json
{
  "payment_required": true/false,
  "has_api": true/false,
  "has_web_service": true/false,
  "has_download": true/false,
  "has_contact_required": true/false,
  "provides_desired_data": true/false,
  "api_url": "URL to API docs or null",
  "documentation_url": "URL to general docs",
  "access_notes": "Important access information"
}
```

## Common Patterns

### Government APIs
- Usually at data.agency.gov/api
- Often have authentication via API key
- OpenAPI/Swagger documentation common
- Rate limits usually documented

### Commercial APIs
- Clear documentation sites
- Multiple authentication methods
- Support links visible
- Pricing information available

### Academic/Research Data
- Often at institutional repositories
- May require login
- Download links primary access method
- Citation requirements in terms

### Final Instructions
- If a site has an API available but doesn't require it, consider that it needs the API key.
- If a site has an API available but doesn't require it, consider that it needs the API key.
- Do not include sites which require payment.
