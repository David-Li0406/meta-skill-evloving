# Test Generation Patterns

This reference describes patterns for generating effective test blocks in Bruno collections based on OpenAPI specifications.

## Basic Test Patterns

### Status Code Validation

Every endpoint should validate the expected status code:

```javascript
test("Status code is 200", function() {
  expect(res.getStatus()).to.equal(200);
});
```

For different operations:
- GET: 200 (OK)
- POST: 201 (Created) or 200 (OK)
- PUT/PATCH: 200 (OK) or 204 (No Content)
- DELETE: 204 (No Content) or 200 (OK)

### Response Schema Validation

Validate the response structure matches the OpenAPI schema:

```javascript
test("Response has required fields", function() {
  const data = res.getBody();
  expect(data).to.have.property('id');
  expect(data).to.have.property('name');
  expect(data).to.have.property('email');
});

test("Field types are correct", function() {
  const data = res.getBody();
  expect(data.id).to.be.a('number');
  expect(data.name).to.be.a('string');
  expect(data.email).to.be.a('string');
});
```

### Array Response Validation

For endpoints returning arrays:

```javascript
test("Returns array", function() {
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

### Pagination Validation

For paginated endpoints:

```javascript
test("Pagination metadata present", function() {
  const data = res.getBody();
  expect(data).to.have.property('items');
  expect(data).to.have.property('total');
  expect(data).to.have.property('page');
  expect(data).to.have.property('pageSize');
});

test("Items array length respects limit", function() {
  const data = res.getBody();
  const limit = parseInt(bru.getVar('limit')) || 10;
  expect(data.items.length).to.be.at.most(limit);
});
```

## Authentication Patterns

### Bearer Token Authentication

For endpoints requiring authentication, save the token from a login request:

**Login Request (auth/login.bru):**
```javascript
tests {
  test("Status code is 200", function() {
    expect(res.getStatus()).to.equal(200);
  });

  test("Token received", function() {
    const data = res.getBody();
    expect(data).to.have.property('token');
    expect(data.token).to.be.a('string');
    bru.setVar("accessToken", data.token);
  });
}
```

**Protected Request:**
```
auth:bearer {
  token: {{accessToken}}
}

tests {
  test("Authorized successfully", function() {
    expect(res.getStatus()).to.not.equal(401);
  });
}
```

### API Key Authentication

**Pre-request script:**
```javascript
script:pre-request {
  // Ensure API key is set
  const apiKey = bru.getEnvVar("apiKey");
  if (!apiKey) {
    throw new Error("API key not configured");
  }
}
```

**Tests:**
```javascript
tests {
  test("API key accepted", function() {
    expect(res.getStatus()).to.not.equal(401);
    expect(res.getStatus()).to.not.equal(403);
  });
}
```

### OAuth 2.0 Flow

**Token Request:**
```javascript
tests {
  test("OAuth token obtained", function() {
    const data = res.getBody();
    expect(data).to.have.property('access_token');
    expect(data).to.have.property('token_type');
    bru.setVar("accessToken", data.access_token);
    bru.setVar("tokenType", data.token_type);
  });
}
```

## CRUD Operation Patterns

### POST (Create) Pattern

```javascript
script:pre-request {
  // Generate unique test data
  const timestamp = Date.now();
  bru.setVar("testName", `Test_${timestamp}`);
  bru.setVar("testEmail", `test_${timestamp}@example.com`);
}

tests {
  test("Resource created (201)", function() {
    expect(res.getStatus()).to.equal(201);
  });

  test("Created resource returned", function() {
    const data = res.getBody();
    expect(data).to.have.property('id');
    expect(data.name).to.equal(bru.getVar('testName'));
  });

  test("Save resource ID", function() {
    const data = res.getBody();
    bru.setVar("createdResourceId", data.id);
  });

  test("Location header present", function() {
    const location = res.getHeader('Location');
    expect(location).to.be.a('string');
  });
}
```

### GET (Read) Pattern

```javascript
tests {
  test("Resource found (200)", function() {
    expect(res.getStatus()).to.equal(200);
  });

  test("Resource has correct ID", function() {
    const data = res.getBody();
    expect(data.id).to.equal(bru.getVar('createdResourceId'));
  });

  test("Required fields present", function() {
    const data = res.getBody();
    expect(data).to.have.property('id');
    expect(data).to.have.property('name');
    expect(data).to.have.property('createdAt');
  });
}
```

### PUT/PATCH (Update) Pattern

```javascript
script:pre-request {
  bru.setVar("updatedName", `Updated_${Date.now()}`);
}

tests {
  test("Resource updated (200)", function() {
    expect(res.getStatus()).to.equal(200);
  });

  test("Updated fields reflect changes", function() {
    const data = res.getBody();
    expect(data.name).to.equal(bru.getVar('updatedName'));
  });

  test("ID unchanged", function() {
    const data = res.getBody();
    expect(data.id).to.equal(bru.getVar('createdResourceId'));
  });
}
```

### DELETE (Delete) Pattern

```javascript
tests {
  test("Resource deleted (204)", function() {
    const status = res.getStatus();
    expect(status).to.be.oneOf([200, 204]);
  });

  test("No content returned", function() {
    if (res.getStatus() === 204) {
      const body = res.getBody();
      expect(body).to.be.empty;
    }
  });
}
```

## Request Chaining Patterns

### Create Then Retrieve

**Create Request (seq: 1):**
```javascript
tests {
  test("Resource created", function() {
    expect(res.getStatus()).to.equal(201);
    const data = res.getBody();
    bru.setVar("resourceId", data.id);
  });
}
```

**Get Request (seq: 2):**
```
get {
  url: {{baseUrl}}/resources/{{resourceId}}
}

tests {
  test("Verify created resource", function() {
    expect(res.getStatus()).to.equal(200);
    const data = res.getBody();
    expect(data.id).to.equal(bru.getVar('resourceId'));
  });
}
```

### Create, Update, Verify

**Sequence:**
1. POST to create resource → save ID
2. PUT/PATCH to update resource
3. GET to verify update

### Dependent Resources

**Create Parent:**
```javascript
tests {
  test("Save parent ID", function() {
    const data = res.getBody();
    bru.setVar("parentId", data.id);
  });
}
```

**Create Child:**
```
post {
  url: {{baseUrl}}/parents/{{parentId}}/children
}

body:json {
  {
    "parentId": {{parentId}},
    "name": "Child Resource"
  }
}
```

## Error Handling Patterns

### 400 Bad Request

```javascript
tests {
  test("Bad request handled (400)", function() {
    expect(res.getStatus()).to.equal(400);
  });

  test("Error message provided", function() {
    const data = res.getBody();
    expect(data).to.have.property('message');
    expect(data.message).to.be.a('string');
  });
}
```

### 401 Unauthorized

```javascript
tests {
  test("Unauthorized access blocked (401)", function() {
    expect(res.getStatus()).to.equal(401);
  });

  test("Error response structure", function() {
    const data = res.getBody();
    expect(data).to.have.property('error');
  });
}
```

### 404 Not Found

```javascript
tests {
  test("Resource not found (404)", function() {
    expect(res.getStatus()).to.equal(404);
  });
}
```

### 422 Unprocessable Entity

```javascript
tests {
  test("Validation error (422)", function() {
    expect(res.getStatus()).to.equal(422);
  });

  test("Validation errors listed", function() {
    const data = res.getBody();
    expect(data).to.have.property('errors');
    expect(data.errors).to.be.an('array');
  });
}
```

## Performance Testing

```javascript
tests {
  test("Response time acceptable", function() {
    expect(res.getResponseTime()).to.be.below(1000);
  });

  test("Fast response for cached data", function() {
    const cacheHeader = res.getHeader('X-Cache');
    if (cacheHeader === 'HIT') {
      expect(res.getResponseTime()).to.be.below(100);
    }
  });
}
```

## Data Validation Patterns

### Email Format

```javascript
test("Email format valid", function() {
  const data = res.getBody();
  expect(data.email).to.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
});
```

### Date Format

```javascript
test("Dates are ISO 8601 format", function() {
  const data = res.getBody();
  expect(data.createdAt).to.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
});
```

### UUID Format

```javascript
test("ID is valid UUID", function() {
  const data = res.getBody();
  expect(data.id).to.match(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i);
});
```

### Enum Values

```javascript
test("Status is valid enum value", function() {
  const data = res.getBody();
  expect(data.status).to.be.oneOf(['pending', 'approved', 'rejected']);
});
```

## Security Testing

### Content Security

```javascript
tests {
  test("Content-Type header present", function() {
    expect(res.getHeader('Content-Type')).to.exist;
  });

  test("Security headers present", function() {
    expect(res.getHeader('X-Content-Type-Options')).to.equal('nosniff');
    expect(res.getHeader('X-Frame-Options')).to.exist;
  });
}
```

### CORS Headers

```javascript
tests {
  test("CORS headers configured", function() {
    expect(res.getHeader('Access-Control-Allow-Origin')).to.exist;
  });
}
```

## OpenAPI Schema Mapping

When generating tests from OpenAPI specs:

1. **Required Fields** → Property existence checks
2. **Field Types** → Type validation (string, number, boolean, array, object)
3. **Formats** → Format validation (email, uuid, date, date-time)
4. **Enums** → oneOf validation
5. **Min/Max** → Range validation
6. **Patterns** → Regex validation
7. **Array Items** → Item structure validation

Example generation logic:

```
OpenAPI: type: string, format: email
→ Bruno: expect(data.email).to.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);

OpenAPI: type: integer, minimum: 0, maximum: 100
→ Bruno: expect(data.age).to.be.within(0, 100);

OpenAPI: type: array, items: { $ref: '#/components/schemas/User' }
→ Bruno: expect(data).to.be.an('array');
         if (data.length > 0) { expect(data[0]).to.have.property('id'); }
```
