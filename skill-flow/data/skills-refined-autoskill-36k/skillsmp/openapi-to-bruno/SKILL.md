---
name: openapi-to-bruno
description: "Convert OpenAPI specifications to Bruno API collections with comprehensive test generation. Use when users need to: (1) Transform OpenAPI/Swagger specs (YAML/JSON) into Bruno .bru collection files, (2) Generate Bruno collections from API contracts, (3) Create test blocks with assertions for API endpoints, (4) Set up request chaining and authentication flows, (5) Generate Bruno directory structure with environments. Triggered by requests like 'convert this OpenAPI spec to Bruno', 'generate Bruno collection from openapi.yaml', or 'create Bruno tests from my API contract'."
---

# OpenAPI to Bruno Converter

## Overview

Convert OpenAPI specifications (versions 3.0+) to Bruno API collections with automatically generated test blocks, proper authentication configuration, and request chaining support. The conversion creates a complete Bruno collection including directory structure, environment files, and executable test assertions.

## Quick Start

### Basic Conversion

For simple conversion from OpenAPI to Bruno:

```bash
python scripts/openapi_to_bruno.py <openapi-file> <output-directory> [collection-name]
```

**Example:**
```bash
python scripts/openapi_to_bruno.py api-spec.yaml ./my-bruno-collection "My API"
```

This generates:
- `bruno.json` - Collection configuration
- `environments/` - Environment files from OpenAPI servers
- Organized `.bru` files for each endpoint
- Test blocks with assertions
- Authentication configuration

### When to Use This Skill

Use this skill when:
- Converting OpenAPI/Swagger specifications to Bruno format
- Setting up API testing from existing contracts
- Generating collections with tests from API documentation
- Creating Bruno collections for CI/CD integration
- Migrating from OpenAPI-based tools to Bruno

## Conversion Workflow

### Step 1: Locate OpenAPI Specification

Identify the OpenAPI specification file (YAML or JSON format):

```bash
# Common locations
./openapi.yaml
./swagger.json
./api/openapi.yml
./docs/api-spec.yaml
```

### Step 2: Run Conversion Script

Execute the conversion script with appropriate parameters:

```bash
python scripts/openapi_to_bruno.py <spec-file> <output-dir> [name]
```

**Parameters:**
- `<spec-file>`: Path to OpenAPI YAML or JSON file
- `<output-dir>`: Target directory for Bruno collection
- `[name]`: Optional collection name (defaults to spec title)

### Step 3: Review Generated Collection

The converter creates:

```
output-directory/
├── bruno.json                    # Collection config
├── environments/
│   ├── production.bru            # From servers
│   ├── staging.bru
│   └── development.bru
└── <organized-endpoints>/
    ├── users/
    │   ├── get-users.bru
    │   ├── create-user.bru
    │   └── user-id/
    │       └── get-user.bru
    └── auth/
        └── login.bru
```

### Step 4: Customize as Needed

After generation, review and customize:
- Test assertions for specific business logic
- Environment variables and secrets
- Pre-request scripts for test data generation
- Request chaining variables

## OpenAPI Mapping

### URL and Servers

**OpenAPI servers** → **Bruno environments**

```yaml
# OpenAPI
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging.example.com/v1
    description: Staging
```

```
# Bruno: environments/production.bru
vars {
  baseUrl: https://api.example.com/v1
}

# Bruno: environments/staging.bru
vars {
  baseUrl: https://staging.example.com/v1
}
```

### Paths and Operations

**OpenAPI paths** → **Bruno .bru files**

Organization strategy:
1. **By tags**: Groups endpoints by OpenAPI tags
2. **By path structure**: Uses path hierarchy for folders
3. **By operationId**: Uses operation ID for filename

Example:
```yaml
# OpenAPI
paths:
  /users/{id}:
    get:
      tags: [users]
      operationId: getUserById
```

Creates: `users/get-user-by-id.bru`

### Authentication

**OpenAPI security schemes** → **Bruno auth blocks**

#### Bearer Token
```yaml
# OpenAPI
securitySchemes:
  bearerAuth:
    type: http
    scheme: bearer
```

```
# Bruno
auth:bearer {
  token: {{accessToken}}
}
```

#### API Key
```yaml
# OpenAPI
securitySchemes:
  apiKey:
    type: apiKey
    in: header
    name: X-API-Key
```

```
# Bruno
headers {
  X-API-Key: {{apiKey}}
}
```

#### Basic Auth
```yaml
# OpenAPI
securitySchemes:
  basicAuth:
    type: http
    scheme: basic
```

```
# Bruno
auth:basic {
  username: {{username}}
  password: {{password}}
}
```

#### OAuth 2.0
```yaml
# OpenAPI
securitySchemes:
  oauth2:
    type: oauth2
    flows:
      authorizationCode:
        authorizationUrl: https://example.com/oauth/authorize
        tokenUrl: https://example.com/oauth/token
```

```
# Bruno
auth:oauth2 {
  grant_type: authorization_code
  authorization_url: {{authUrl}}
  access_token_url: {{tokenUrl}}
}
```

### Parameters

**Query parameters** → `params:query` block
**Path parameters** → URL template variables `{{paramName}}`
**Header parameters** → `headers` block

### Request Bodies

**OpenAPI requestBody** → **Bruno body blocks**

#### JSON
```yaml
# OpenAPI
requestBody:
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/User'
```

```
# Bruno
body:json {
  {
    "name": "string",
    "email": "string"
  }
}
```

#### Form Data
```yaml
# OpenAPI
requestBody:
  content:
    application/x-www-form-urlencoded:
      schema:
        properties:
          username:
            type: string
```

```
# Bruno
body:form-urlencoded {
  username: value
}
```

### Responses

**OpenAPI responses** → **Bruno test assertions**

The converter analyzes response schemas to generate appropriate tests.

## Test Generation

The skill automatically generates comprehensive test blocks based on OpenAPI specifications and established testing patterns.

### Status Code Tests

Generated for every endpoint based on expected response:

```javascript
test("Status code is 200", function() {
  expect(res.getStatus()).to.equal(200);
});
```

Expected codes:
- GET: 200
- POST: 201 or 200
- PUT/PATCH: 200 or 204
- DELETE: 204 or 200

### Schema Validation Tests

Generated from OpenAPI response schemas:

**Object responses:**
```javascript
test("Response has required fields", function() {
  const data = res.getBody();
  expect(data).to.have.property('id');
  expect(data).to.have.property('name');
  expect(data).to.have.property('email');
});

test("Field types are correct", function() {
  const data = res.getBody();
  if (data.id !== undefined) {
    expect(data.id).to.be.a('number');
  }
  if (data.name !== undefined) {
    expect(data.name).to.be.a('string');
  }
});
```

**Array responses:**
```javascript
test("Response is array", function() {
  const data = res.getBody();
  expect(data).to.be.an('array');
});

test("Array items have correct structure", function() {
  const data = res.getBody();
  if (data.length > 0) {
    expect(data[0]).to.have.property('id');
    expect(data[0]).to.have.property('name');
  }
});
```

### Performance Tests

```javascript
test("Response time acceptable", function() {
  expect(res.getResponseTime()).to.be.below(2000);
});
```

### Request Chaining

For POST and PUT operations, the converter includes variable saving for request chaining:

```javascript
test("Save resource ID", function() {
  const data = res.getBody();
  if (data && data.id) {
    bru.setVar("resourceId", data.id);
  }
});
```

This enables follow-up requests to use the created resource:

```
get {
  url: {{baseUrl}}/resources/{{resourceId}}
}
```

### Pre-request Scripts

Generated when request bodies are present:

```javascript
script:pre-request {
  // Generate test data if needed
  const timestamp = Date.now();
  // bru.setVar("testValue", `value_${timestamp}`);
}
```

Uncomment and customize to generate unique test data.

## Advanced Patterns

### Handling Authentication Flows

For APIs requiring authentication:

1. **Token-based auth**: Create a login endpoint request first
2. **Save token in tests**:
   ```javascript
   test("Token received", function() {
     const data = res.getBody();
     bru.setVar("accessToken", data.token);
   });
   ```
3. **Use in subsequent requests**:
   ```
   auth:bearer {
     token: {{accessToken}}
   }
   ```

### CRUD Operation Sequences

The converter sets up request chaining for typical CRUD flows:

**Sequence 1: Create → Verify**
1. POST `/users` → Save `userId`
2. GET `/users/{{userId}}` → Verify creation

**Sequence 2: Create → Update → Delete**
1. POST `/users` → Save `userId`
2. PUT `/users/{{userId}}` → Update resource
3. DELETE `/users/{{userId}}` → Clean up

### Environment-Specific Configuration

Customize generated environments for different contexts:

```
# environments/development.bru
vars {
  baseUrl: http://localhost:3000
  apiKey: dev_key_123
}

vars:secret {
  accessToken: dev_token
}

# environments/production.bru
vars {
  baseUrl: https://api.example.com
  apiKey: prod_key_456
}

vars:secret {
  accessToken: prod_token
}
```

## Customization

### Enhancing Generated Tests

After conversion, enhance tests with business logic validation:

```javascript
test("Business rule validation", function() {
  const user = res.getBody();

  // Domain-specific checks
  expect(user.email).to.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
  expect(user.age).to.be.within(18, 120);
  expect(user.role).to.be.oneOf(['admin', 'user', 'guest']);
});
```

### Adding Test Data Generation

Enhance pre-request scripts for dynamic test data:

```javascript
script:pre-request {
  const timestamp = Date.now();
  const randomId = Math.random().toString(36).substring(7);

  bru.setVar("testEmail", `test_${timestamp}@example.com`);
  bru.setVar("testUsername", `user_${randomId}`);
  bru.setVar("testPassword", `Pass${randomId}!123`);
}
```

### Organizing Complex APIs

For large APIs, organize by:

1. **Tags**: Use OpenAPI tags for logical grouping
2. **Versioning**: Separate v1, v2 endpoints
3. **Modules**: Group related functionality (auth, users, orders)

## References

For detailed information about specifications and syntax:

- **[openapi-spec.md](references/openapi-spec.md)**: Complete OpenAPI 3.0 specification reference with all object types, authentication schemes, and data formats
- **[bruno-syntax.md](references/bruno-syntax.md)**: Comprehensive Bruno .bru file syntax including all blocks, authentication types, and test patterns
- **[test-patterns.md](references/test-patterns.md)**: Test generation patterns for different scenarios including CRUD operations, authentication flows, and request chaining

These references are loaded as needed when:
- Clarifying OpenAPI structure or features
- Understanding Bruno syntax details
- Implementing specific test patterns
- Debugging conversion issues

## Troubleshooting

### Script Execution

If the script fails to execute:

```bash
# Make executable
chmod +x scripts/openapi_to_bruno.py

# Run with Python directly
python3 scripts/openapi_to_bruno.py <spec> <output>
```

### Missing Dependencies

Install required Python packages:

```bash
pip install pyyaml
```

### Invalid OpenAPI Spec

Validate your OpenAPI specification before conversion:

```bash
# Online validators
https://editor.swagger.io/

# CLI tools
openapi-generator validate -i openapi.yaml
```

### Path Parameter Issues

Path parameters must use correct OpenAPI format:

```yaml
# Correct
/users/{userId}

# Incorrect
/users/:userId
```

### Response Schema Issues

Ensure response schemas are properly defined:

```yaml
responses:
  '200':
    description: Success
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
```

## Running Generated Tests

Execute tests using Bruno CLI:

```bash
# Run entire collection
bru run <collection-directory> --env production

# Run specific folder
bru run <collection-directory>/users --env development

# Generate report
bru run <collection-directory> --output results.json
```
