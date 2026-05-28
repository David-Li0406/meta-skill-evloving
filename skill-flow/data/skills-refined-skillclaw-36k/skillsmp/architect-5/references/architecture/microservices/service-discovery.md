# Service Discovery and API Contract Patterns

**Category**: architecture/microservices
**Description**: Detect service discovery, API contracts, and routing patterns
**Purpose**: Map service infrastructure and API definitions

---

## OpenAPI/Swagger Specifications

### OpenAPI 3.x Root
**Type**: regex
**Severity**: info
**Pattern**: `["']?openapi["']?\s*:\s*["']3\.\d+\.\d+["']`
- OpenAPI 3.x specification
- Example: `openapi: "3.0.3"`
- Captures: OpenAPI version

### Swagger 2.0 Root
**Type**: regex
**Severity**: info
**Pattern**: `["']?swagger["']?\s*:\s*["']2\.0["']`
- Swagger 2.0 specification
- Example: `swagger: "2.0"`

### API Info Title
**Type**: regex
**Severity**: info
**Pattern**: `info:\s*\n\s*title:\s*["']?([^"'\n]+)["']?`
- API title from OpenAPI spec
- Example: `title: "User Service API"`
- Captures: Service name

### API Server URL
**Type**: regex
**Severity**: info
**Pattern**: `servers:\s*\n\s*-\s*url:\s*["']?([^"'\n]+)["']?`
- Server URL from OpenAPI spec
- Example: `url: "https://api.example.com/v1"`
- Captures: Base URL

### Path Definition
**Type**: regex
**Severity**: info
**Pattern**: `paths:\s*\n\s*(/[^:]+):`
- API path from OpenAPI spec
- Example: `/users/{id}:`
- Captures: Endpoint path

---

## GraphQL Schema

### GraphQL Type Definition
**Type**: regex
**Severity**: info
**Pattern**: `type\s+(\w+)\s*(?:@\w+(?:\([^)]*\))?\s*)*\{`
- GraphQL type definition
- Example: `type User {`
- Captures: Type name

### GraphQL Query Definition
**Type**: regex
**Severity**: info
**Pattern**: `type\s+Query\s*\{[\s\S]*?(\w+)\s*(?:\([^)]*\))?\s*:\s*(\w+)`
- GraphQL query field
- Example: `getUser(id: ID!): User`
- Captures: Query name, return type

### GraphQL Mutation Definition
**Type**: regex
**Severity**: info
**Pattern**: `type\s+Mutation\s*\{[\s\S]*?(\w+)\s*(?:\([^)]*\))?\s*:\s*(\w+)`
- GraphQL mutation field
- Example: `createUser(input: CreateUserInput!): User`
- Captures: Mutation name, return type

### GraphQL Federation Entity
**Type**: regex
**Severity**: info
**Pattern**: `@key\s*\(\s*fields:\s*["']([^"']+)["']\s*\)`
- Apollo Federation entity key
- Example: `@key(fields: "id")`
- Captures: Key fields

---

## Kubernetes Service Discovery

### Kubernetes Service Definition
**Type**: regex
**Severity**: info
**Pattern**: `kind:\s*Service[\s\S]*?metadata:\s*\n\s*name:\s*["']?([^"'\n]+)["']?`
- K8s Service resource
- Example: `name: user-service`
- Captures: Service name

### Service Port Definition
**Type**: regex
**Severity**: info
**Pattern**: `ports:\s*\n\s*-\s*(?:name:\s*["']?(\w+)["']?\s*\n\s*)?port:\s*(\d+)`
- K8s Service port
- Example: `port: 8080`
- Captures: Port name, port number

### Service Selector
**Type**: regex
**Severity**: info
**Pattern**: `selector:\s*\n\s*app:\s*["']?([^"'\n]+)["']?`
- K8s Service selector
- Example: `app: user-service`
- Captures: App label

### Ingress Host
**Type**: regex
**Severity**: info
**Pattern**: `host:\s*["']?([^"'\n]+)["']?`
- K8s Ingress host
- Example: `host: api.example.com`
- Captures: Hostname

### Ingress Path
**Type**: regex
**Severity**: info
**Pattern**: `path:\s*["']?(/[^"'\n]*)["']?`
- K8s Ingress path
- Example: `path: /api/users`
- Captures: Path prefix

---

## Consul Service Discovery

### Python Consul Register
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$CONSUL.agent.service.register($NAME, ...)`
- Registers service with Consul
- Example: `consul.agent.service.register("user-service", port=8080)`
- Captures: Service name

### Go Consul Register
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$AGENT.ServiceRegister($REGISTRATION)`
- Registers service with Consul in Go
- Example: `agent.ServiceRegister(&consul.AgentServiceRegistration{Name: "user-service"})`

### Consul Service Lookup
**Type**: semgrep
**Severity**: info
**Languages**: [python, go]
**Pattern**: `$CONSUL.$METHOD.service($NAME, ...)`
- Looks up service in Consul
- Example: `consul.catalog.service("user-service")`

---

## Eureka Service Discovery

### Eureka Client Annotation
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `@EnableEurekaClient`
- Enables Eureka discovery client
- Example: `@EnableEurekaClient`

### Eureka Server Annotation
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `@EnableEurekaServer`
- Enables Eureka discovery server
- Example: `@EnableEurekaServer`

### Eureka Application Name
**Type**: regex
**Severity**: info
**Pattern**: `eureka\.instance\.appname\s*=\s*["']?([^"'\n]+)["']?`
- Eureka application name
- Example: `eureka.instance.appname=user-service`
- Captures: Service name

---

## API Gateway Patterns

### Kong Route Configuration
**Type**: regex
**Severity**: info
**Pattern**: `services:\s*\n\s*-\s*name:\s*["']?([^"'\n]+)["']?`
- Kong service definition
- Example: `name: user-service`
- Captures: Service name

### Kong Upstream
**Type**: regex
**Severity**: info
**Pattern**: `upstreams:\s*\n\s*-\s*name:\s*["']?([^"'\n]+)["']?`
- Kong upstream definition
- Example: `name: user-service-upstream`
- Captures: Upstream name

### AWS API Gateway Integration
**Type**: regex
**Severity**: info
**Pattern**: `uri:\s*["']?arn:aws:apigateway:[^:]+:lambda:path/[^"'\n]+["']?`
- AWS API Gateway Lambda integration
- Captures: Lambda function ARN

### Envoy Cluster
**Type**: regex
**Severity**: info
**Pattern**: `clusters:\s*\n\s*-\s*name:\s*["']?([^"'\n]+)["']?`
- Envoy cluster definition
- Example: `name: user-service-cluster`
- Captures: Cluster name

---

## Docker Compose Services

### Service Definition
**Type**: regex
**Severity**: info
**Pattern**: `services:\s*\n\s*(\w+):\s*\n`
- Docker Compose service name
- Example: `user-service:`
- Captures: Service name

### Service Image
**Type**: regex
**Severity**: info
**Pattern**: `image:\s*["']?([^"'\n:]+)(?::([^"'\n]+))?["']?`
- Docker image reference
- Example: `image: user-service:latest`
- Captures: Image name, tag

### Depends On
**Type**: regex
**Severity**: info
**Pattern**: `depends_on:\s*\n(?:\s*-\s*["']?(\w+)["']?\s*\n)+`
- Service dependencies
- Example: `depends_on: [postgres, redis]`
- Captures: Dependent service names

### Service Network
**Type**: regex
**Severity**: info
**Pattern**: `networks:\s*\n(?:\s*-?\s*["']?(\w+)["']?\s*\n)+`
- Docker network membership
- Captures: Network names

---

## Environment-Based Service URLs

### SERVICE_URL Pattern
**Type**: regex
**Severity**: info
**Pattern**: `([A-Z][A-Z0-9_]*_(?:URL|HOST|ENDPOINT|SERVICE))\s*[:=]\s*["']?([^"'\n]+)["']?`
- Service URL from environment
- Example: `USER_SERVICE_URL=http://user-service:8080`
- Captures: Variable name, URL

### Spring Cloud Config
**Type**: regex
**Severity**: info
**Pattern**: `([a-z][a-z0-9-]*\.(?:url|host|baseUrl))\s*=\s*["']?([^"'\n]+)["']?`
- Spring service configuration
- Example: `user-service.url=http://user-service:8080`
- Captures: Property name, URL

---

## Detection Confidence

**OpenAPI Detection**: 95%
**GraphQL Detection**: 90%
**Kubernetes Detection**: 95%
**Service Discovery**: 85%

---

## References

- OpenAPI Specification
- GraphQL Specification
- Kubernetes Service Discovery
- Consul Documentation
- Spring Cloud Netflix
