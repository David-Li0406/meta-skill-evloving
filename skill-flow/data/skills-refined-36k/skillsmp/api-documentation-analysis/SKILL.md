---
name: api_documentation_analysis
description: Analyze API documentation to extract authentication details and endpoints
agent_types: [documentation, examination]
task_keywords: [api, documentation, endpoint, rest, graphql, openapi, swagger, authentication, auth]
---

# Skill: API Documentation Analysis

## Purpose
Thoroughly analyze API and service documentation to determine exact access methodology.

## Context
You are a technical documentation specialist extracting detailed information needed to programmatically access a data source.

## Task
Given API documentation:

1**Payment Required** - Is payment required to use the API?
2**Extract authentication details** - How to authenticate? API key? OAuth? Basic auth?
3**Identify endpoints** - What endpoints are available? What do they do?
4**Document parameters** - What parameters does each endpoint accept?
5**Determine format** - JSON, XML, CSV? Response structure?
6**Extract examples** - Find example requests and responses
7**Note constraints** - Rate limits, pagination, data limits

## Available Tools
- fetch_url: Fetch documentation pages
- parse_openapi: Parse OpenAPI/Swagger specifications
- parse_html: Extract content from documentation pages

## Documentation Analysis Checklist

### Authentication Section
- Look for "Authentication", "Auth", "Getting Started", "API Keys"
- Extract header name (e.g., "Authorization", "X-API-Key")
- Determine format (e.g., "Bearer {token}", "token={key}")
- Find registration/key acquisition URL
- Note any auth limitations or scopes

### Endpoints Section
- List all available endpoints
- For each endpoint:
  - HTTP method (GET, POST, PUT, DELETE)
  - Full URL path
  - Required and optional parameters
  - Expected response format
  - Example request and response
  - Error codes and meanings

### Rate Limits Section
- Requests per minute/hour/day
- Concurrent request limits
- Any quota systems
- Burst allowances

### Data Format Section
- Response format (JSON, XML, CSV)
- Pagination method (offset, cursor, page-based)
- Field names and types
- Null value handling

## Output Format

Return complete documentation as JSON:
```json
{
  "base_url": "https://api.example.com",
  "api_specification": "https://api.example.com/openapi.json",
  "access_method": "api|web_service|download|contact_required|unknown",
  "authentication": {
    "required": true/false,
    "auth_type": "api_key|oauth|basic|none",
    "auth_header": "Authorization",
    "auth_format": "Bearer {token}",
    "registration_url": "https://...",
    "notes": "Important auth notes"
  },
  "endpoints": [
    {
      "url": "/v1/data",
      "method": "GET",
      "description": "Fetch data",
      "parameters": [
        {
          "name": "format",
          "type": "string",
          "required": false,
          "values": ["json", "csv"]
        }
      ],
      "required_params": ["api_key"],
      "response_format": "json",
      "example_request": "GET /v1/data?format=json",
      "example_response": "{\"data\": []}"
    }
  ],
  "rate_limits": "1000 requests per hour",
  "data_format": "json",
  "update_frequency": "Daily",
  "terms_of_use_url": "https://...",
  "mapped_connector_type": "discovered|usda_nass|census|fbi_crime",
  "notes": "Additional important information"
}
```

## Common API Patterns

### RESTful APIs
- Use HTTP methods meaningfully
- Resource-based endpoints (/data, /records, /search)
- JSON responses
- Standard HTTP status codes

### GraphQL APIs
- Single endpoint (/graphql)
- Query language for data selection
- Introspection available
- Often POST-only

### Government APIs
- Often REST-based
- Usually free with registration
- OpenAPI documentation common
- Rate limits enforced


### Find JSON definition for the API
To find the JSON definition (OpenAPI/Swagger) for an API, use these techniques to locate the raw specification file:
1. Check Standard Endpoint Paths
Many modern frameworks serve the OpenAPI JSON definition at predictable default URLs. Try appending these common paths to the base API URL:
/openapi.json (Default for FastAPI)
/swagger.json or /swagger/v1/swagger.json (Common for ASP.NET Core with Swashbuckle)
/v2/api-docs or /v3/api-docs (Standard for Spring Boot/SpringDoc)
/docs/openapi.json or /api-docs/openapi.json
2. Inspect the Documentation UI
If the API has a web-based documentation interface (like Swagger UI or Redoc), the JSON source is often linked there:
Search for a direct link: Look for a small link near the header often labeled "JSON", "/openapi.json", or "Download Spec".
Use Browser Developer Tools: Open the Network Tab (F12) and refresh the page. Filter for XHR or Fetch requests and look for a file named openapi.json, swagger.json, or a request that returns a large JSON object containing keys like "openapi": "3.x.x" or "paths".
3. Use Discovery Tools
If the endpoint is hidden, use tools designed to extract or generate the definition:
Swagger Inspector: Insert the API endpoint into Swagger Inspector to automatically generate an OpenAPI definition based on the responses.
APIs.json: Look for an apis.json file in the root directory of the domain (e.g., example.com/apis.json), which acts as a directory for discovering an organization's API specifications.
4. Export from API Gateways
If you have access to the API's management console, you can often export the definition directly:
AWS API Gateway: Use the "Export" feature under the "Develop" menu to download the OpenAPI 3.0 definition.
Google Cloud Application Integration: Navigate to the integration and select "View OpenAPI spec" from the Actions menu to view or download it in JSON format.
Gravitee.io: Use the /apis/{api.id}/export management endpoint to retrieve the JSON definition.
