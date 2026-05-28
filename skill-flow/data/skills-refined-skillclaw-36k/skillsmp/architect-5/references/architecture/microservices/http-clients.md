# HTTP Client Communication Patterns

**Category**: architecture/microservices
**Description**: Detect HTTP client usage for service-to-service communication
**Purpose**: Map microservice dependencies and communication patterns

---

## JavaScript/TypeScript HTTP Clients

### Fetch API Call
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `fetch($URL, ...)`
- Native browser/Node.js HTTP client
- Example: `fetch('http://user-service/api/users')`
- Captures: URL patterns for service discovery

### Axios HTTP Call
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `axios.$METHOD($URL, ...)`
- Popular HTTP client library
- Example: `axios.get('http://order-service/orders')`
- Captures: Method and URL

### Axios Instance Call
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `$CLIENT.$METHOD($PATH, ...)`
- Axios instance with baseURL
- Example: `userClient.get('/users/123')`
- Context: Look for axios.create() to find baseURL

### Got HTTP Client
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `got($URL, ...)`
- Lightweight Node.js HTTP client
- Example: `got('http://api-gateway/v1/products')`

### Node-Fetch Call
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `fetch($URL, ...)`
- node-fetch package (same as native fetch)
- Example: `fetch('http://inventory-service/stock')`

### Superagent Request
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `superagent.$METHOD($URL)`
- Superagent HTTP client
- Example: `superagent.get('http://auth-service/validate')`

---

## Python HTTP Clients

### Requests Library
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `requests.$METHOD($URL, ...)`
- Most popular Python HTTP client
- Example: `requests.get('http://payment-service/process')`

### HTTPX Async Client
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `httpx.$METHOD($URL, ...)`
- Modern async HTTP client
- Example: `httpx.post('http://notification-service/send')`

### HTTPX Client Instance
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$CLIENT.$METHOD($PATH, ...)`
- HTTPX client instance
- Example: `client.get('/users')`

### Aiohttp Session
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$SESSION.$METHOD($URL, ...)`
- Async HTTP with aiohttp
- Example: `session.get('http://search-service/query')`

### Urllib Request
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `urllib.request.urlopen($URL, ...)`
- Standard library HTTP
- Example: `urllib.request.urlopen('http://config-service/settings')`

---

## Go HTTP Clients

### http.Get Call
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `http.Get($URL)`
- Standard library GET request
- Example: `http.Get("http://user-service/api/users")`

### http.Post Call
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `http.Post($URL, ...)`
- Standard library POST request
- Example: `http.Post("http://order-service/orders", "application/json", body)`

### http.NewRequest
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `http.NewRequest($METHOD, $URL, ...)`
- Custom HTTP request
- Example: `http.NewRequest("PUT", "http://inventory-service/update", body)`

### Client.Do
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$CLIENT.Do($REQ)`
- HTTP client with custom request
- Example: `client.Do(req)`

### Resty Client
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$CLIENT.R().$METHOD($URL)`
- Resty HTTP client
- Example: `client.R().Get("http://gateway/api/products")`

---

## Java HTTP Clients

### RestTemplate Call
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `$TEMPLATE.$METHOD($URL, ...)`
- Spring RestTemplate
- Example: `restTemplate.getForObject("http://user-service/users", User.class)`

### WebClient Request
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `$CLIENT.$METHOD().uri($URL)...`
- Spring WebClient (reactive)
- Example: `webClient.get().uri("http://order-service/orders").retrieve()`

### Feign Client
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `@FeignClient(...)`
- Declarative REST client
- Example: `@FeignClient(name = "user-service", url = "http://user-service")`

### OkHttp Request
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `new Request.Builder().url($URL)...`
- OkHttp client
- Example: `new Request.Builder().url("http://payment-service/process").build()`

### HttpURLConnection
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `(HttpURLConnection) $URL.openConnection()`
- Standard library HTTP
- Example: `new URL("http://auth-service/validate").openConnection()`

---

## Service URL Patterns

### Internal Service URL
**Type**: regex
**Severity**: info
**Pattern**: `(?i)https?://[a-z0-9-]+(?:-service|-api|-svc)?(?:\.[a-z0-9-]+)*(?::\d+)?/`
- Matches common microservice URL patterns
- Example: `http://user-service:8080/api/users`
- Captures: Service name and port

### Kubernetes Service URL
**Type**: regex
**Severity**: info
**Pattern**: `(?i)https?://[a-z0-9-]+\.[a-z0-9-]+(?:\.svc(?:\.cluster\.local)?)?(?::\d+)?/`
- Kubernetes service DNS patterns
- Example: `http://user-service.default.svc.cluster.local:8080/`
- Captures: Service, namespace

### Docker Compose Service
**Type**: regex
**Severity**: info
**Pattern**: `(?i)https?://[a-z0-9_-]+:\d+/`
- Docker Compose service references
- Example: `http://postgres:5432/`
- Captures: Container name, port

### Environment Variable URL
**Type**: regex
**Severity**: info
**Pattern**: `(?i)(?:process\.env\.|os\.environ(?:\.get)?\(|os\.Getenv\()["']?([A-Z_]+_URL|[A-Z_]+_SERVICE|[A-Z_]+_HOST)["']?\)?`
- URLs from environment variables
- Example: `process.env.USER_SERVICE_URL`
- Captures: Variable name

---

## Detection Confidence

**Semgrep Detection**: 95%
**URL Pattern Matching**: 85%

---

## References

- HTTP Client Libraries Documentation
- Microservices Communication Patterns
- Service Discovery Best Practices
