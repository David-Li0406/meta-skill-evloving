# Bruno .bru File Syntax Reference

## File Structure

Each `.bru` file represents a single API request using Bruno's markup language. Files are organized in a directory structure that mirrors the collection hierarchy.

## Collection Structure

```
my-collection/
├── bruno.json                 # Collection configuration
├── environments/
│   ├── dev.bru               # Development environment
│   ├── staging.bru           # Staging environment
│   └── prod.bru              # Production environment
├── auth/
│   └── login.bru             # Auth endpoints
└── users/
    ├── get-users.bru         # GET /users
    ├── create-user.bru       # POST /users
    └── user-id/
        ├── get-user.bru      # GET /users/{id}
        └── update-user.bru   # PUT /users/{id}
```

## bruno.json Configuration

```json
{
  "version": "1",
  "name": "API Collection Name",
  "type": "collection"
}
```

## .bru File Format

### Basic Structure

```
meta {
  name: Request Name
  type: http
  seq: 1
}

get {
  url: {{baseUrl}}/api/users
  body: none
  auth: none
}
```

### Meta Block

```
meta {
  name: Get User By ID
  type: http
  seq: 2
}
```

### HTTP Methods

```
get {
  url: {{baseUrl}}/users
}

post {
  url: {{baseUrl}}/users
  body: json
}

put {
  url: {{baseUrl}}/users/{{userId}}
  body: json
}

patch {
  url: {{baseUrl}}/users/{{userId}}
  body: json
}

delete {
  url: {{baseUrl}}/users/{{userId}}
}
```

### Query Parameters

```
params:query {
  limit: 10
  offset: 0
  sort: name
  filter: active
}
```

### Headers

```
headers {
  Content-Type: application/json
  Accept: application/json
  X-API-Key: {{apiKey}}
  Authorization: Bearer {{token}}
}
```

### Path Parameters

Path parameters are embedded in the URL using double curly braces:

```
get {
  url: {{baseUrl}}/users/{{userId}}/posts/{{postId}}
}
```

### Request Body

#### JSON Body

```
post {
  url: {{baseUrl}}/users
  body: json
}

body:json {
  {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
}
```

#### Form Data

```
post {
  url: {{baseUrl}}/upload
  body: multipartForm
}

body:multipart-form {
  name: John Doe
  email: john@example.com
  file: @file(./document.pdf)
}
```

#### URL Encoded

```
post {
  url: {{baseUrl}}/login
  body: formUrlEncoded
}

body:form-urlencoded {
  username: john
  password: secret123
}
```

#### XML Body

```
post {
  url: {{baseUrl}}/api
  body: xml
}

body:xml {
  <user>
    <name>John Doe</name>
    <email>john@example.com</email>
  </user>
}
```

#### Text/Plain

```
post {
  url: {{baseUrl}}/notes
  body: text
}

body:text {
  This is plain text content
}
```

### Authentication

#### No Auth

```
get {
  url: {{baseUrl}}/public
  auth: none
}
```

#### Bearer Token

```
get {
  url: {{baseUrl}}/protected
  auth: bearer
}

auth:bearer {
  token: {{accessToken}}
}
```

#### Basic Auth

```
get {
  url: {{baseUrl}}/protected
  auth: basic
}

auth:basic {
  username: {{username}}
  password: {{password}}
}
```

#### API Key

Use headers for API key authentication:

```
headers {
  X-API-Key: {{apiKey}}
}
```

#### OAuth 2.0

```
get {
  url: {{baseUrl}}/protected
  auth: oauth2
}

auth:oauth2 {
  grant_type: authorization_code
  callback_url: http://localhost:3000/callback
  authorization_url: {{authUrl}}
  access_token_url: {{tokenUrl}}
  client_id: {{clientId}}
  client_secret: {{clientSecret}}
  scope: read write
}
```

### Variables

Bruno supports multiple variable scopes:

```
{{variableName}}          # Standard variable interpolation
{{collectionVar}}         # Collection-level variable
{{envVar}}                # Environment variable
{{requestVar}}            # Request-level variable
```

### Pre-request Script

```
script:pre-request {
  // Set variables
  bru.setVar("timestamp", Date.now());
  bru.setVar("randomId", Math.random().toString(36).substring(7));

  // Get variables
  const baseUrl = bru.getEnvVar("baseUrl");

  // Conditional logic
  if (someCondition) {
    bru.setVar("param", "value");
  }
}
```

### Tests Block

```
tests {
  // Status code assertion
  test("Status code is 200", function() {
    expect(res.getStatus()).to.equal(200);
  });

  // Response body assertions
  test("Response has user data", function() {
    const data = res.getBody();
    expect(data).to.have.property('id');
    expect(data.name).to.equal('John Doe');
  });

  // Response time
  test("Response time is acceptable", function() {
    expect(res.getResponseTime()).to.be.below(1000);
  });

  // Header assertions
  test("Content-Type is JSON", function() {
    expect(res.getHeader('Content-Type')).to.include('application/json');
  });

  // Array assertions
  test("Returns array of users", function() {
    const users = res.getBody();
    expect(users).to.be.an('array');
    expect(users).to.have.length.above(0);
  });

  // Save data for next request
  test("Save user ID", function() {
    const data = res.getBody();
    bru.setVar("userId", data.id);
  });

  // Nested property validation
  test("User has valid address", function() {
    const user = res.getBody();
    expect(user.address).to.have.property('city');
    expect(user.address.zipCode).to.match(/^\d{5}$/);
  });
}
```

### Script Block (Post-response)

```
script {
  // Run after response (deprecated, use tests block)
  const token = res.getBody().token;
  bru.setVar("accessToken", token);
}
```

### Assertions

```
tests {
  // Equality
  expect(value).to.equal(expected);
  expect(value).to.eql(expected);  // Deep equality

  // Type checks
  expect(value).to.be.a('string');
  expect(value).to.be.an('array');
  expect(value).to.be.true;
  expect(value).to.be.null;

  // Numeric comparisons
  expect(value).to.be.above(10);
  expect(value).to.be.below(100);
  expect(value).to.be.within(10, 100);

  // String matching
  expect(value).to.include('substring');
  expect(value).to.match(/regex/);

  // Property checks
  expect(obj).to.have.property('key');
  expect(obj).to.have.all.keys('key1', 'key2');

  // Array checks
  expect(arr).to.include(item);
  expect(arr).to.have.length(5);
  expect(arr).to.be.empty;

  // Negation
  expect(value).to.not.equal(other);
}
```

### Response Object Methods

```
res.getStatus()           // HTTP status code
res.getBody()             // Response body (parsed JSON)
res.getHeader(name)       // Get header value
res.getHeaders()          // All headers
res.getResponseTime()     // Response time in ms
```

### Variable Methods

```
bru.setVar(key, value)           // Set collection variable
bru.getVar(key)                  // Get collection variable
bru.setEnvVar(key, value)        // Set environment variable
bru.getEnvVar(key)               // Get environment variable
```

## Environment Files

### environments/dev.bru

```
vars {
  baseUrl: https://api.dev.example.com
  apiKey: dev_key_123
}

vars:secret {
  token: secret_dev_token
}
```

### environments/prod.bru

```
vars {
  baseUrl: https://api.example.com
  apiKey: prod_key_456
}

vars:secret {
  token: secret_prod_token
}
```

## Complete Example

```
meta {
  name: Create User and Verify
  type: http
  seq: 1
}

post {
  url: {{baseUrl}}/api/users
  body: json
  auth: bearer
}

auth:bearer {
  token: {{accessToken}}
}

headers {
  Content-Type: application/json
  Accept: application/json
}

body:json {
  {
    "name": "{{userName}}",
    "email": "{{userEmail}}",
    "role": "admin"
  }
}

tests {
  test("Status code is 201", function() {
    expect(res.getStatus()).to.equal(201);
  });

  test("User created successfully", function() {
    const user = res.getBody();
    expect(user).to.have.property('id');
    expect(user.name).to.equal(bru.getVar('userName'));
    expect(user.email).to.equal(bru.getVar('userEmail'));
  });

  test("Response time under 500ms", function() {
    expect(res.getResponseTime()).to.be.below(500);
  });

  test("Save user ID for next request", function() {
    const user = res.getBody();
    bru.setVar("createdUserId", user.id);
  });
}

script:pre-request {
  // Generate test data
  const timestamp = Date.now();
  bru.setVar("userName", `TestUser_${timestamp}`);
  bru.setVar("userEmail", `test_${timestamp}@example.com`);
}
```
