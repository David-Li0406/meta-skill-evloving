# Pattern: API Client

> Standard pattern for building HTTP clients that call external services.

---

## When to Use This Pattern

- Integrating with third-party APIs (Stripe, Twilio, SendGrid, etc.)
- Calling internal microservices
- Any HTTP-based service communication
- When you need retry logic, timeouts, or circuit breakers

**Do NOT use when:**
- Simple one-off HTTP calls in scripts
- GraphQL (use a GraphQL client instead)
- WebSocket connections (different pattern)

---

## The Pattern

### TypeScript/JavaScript

```typescript
// api-client.ts
import axios, { AxiosInstance, AxiosError } from 'axios';

interface ApiClientConfig {
  baseUrl: string;
  timeout?: number;
  retries?: number;
  apiKey?: string;
}

interface ApiResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

class ApiClient {
  private client: AxiosInstance;
  private retries: number;

  constructor(config: ApiClientConfig) {
    this.retries = config.retries ?? 3;

    this.client = axios.create({
      baseURL: config.baseUrl,
      timeout: config.timeout ?? 10000,
      headers: {
        'Content-Type': 'application/json',
        ...(config.apiKey && { 'Authorization': `Bearer ${config.apiKey}` }),
      },
    });

    // Request interceptor for logging
    this.client.interceptors.request.use((config) => {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
      return config;
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => this.handleError(error)
    );
  }

  private async handleError(error: AxiosError): Promise<never> {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message = (error.response.data as any)?.message || error.message;

      if (status === 429) {
        throw new RateLimitError(message, error.response.headers['retry-after']);
      }
      if (status >= 500) {
        throw new ServerError(message, status);
      }
      throw new ApiError(message, status);
    }

    if (error.code === 'ECONNABORTED') {
      throw new TimeoutError('Request timed out');
    }

    throw new NetworkError(error.message);
  }

  private async withRetry<T>(
    operation: () => Promise<T>,
    retriesLeft: number = this.retries
  ): Promise<T> {
    try {
      return await operation();
    } catch (error) {
      if (retriesLeft > 0 && this.isRetryable(error)) {
        const delay = this.getBackoffDelay(this.retries - retriesLeft);
        await this.sleep(delay);
        return this.withRetry(operation, retriesLeft - 1);
      }
      throw error;
    }
  }

  private isRetryable(error: unknown): boolean {
    return (
      error instanceof ServerError ||
      error instanceof NetworkError ||
      error instanceof TimeoutError ||
      error instanceof RateLimitError
    );
  }

  private getBackoffDelay(attempt: number): number {
    // Exponential backoff: 1s, 2s, 4s, 8s...
    return Math.min(1000 * Math.pow(2, attempt), 30000);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async get<T>(path: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
    return this.withRetry(async () => {
      const response = await this.client.get<T>(path, { params });
      return {
        data: response.data,
        status: response.status,
        headers: response.headers as Record<string, string>,
      };
    });
  }

  async post<T>(path: string, data?: any): Promise<ApiResponse<T>> {
    return this.withRetry(async () => {
      const response = await this.client.post<T>(path, data);
      return {
        data: response.data,
        status: response.status,
        headers: response.headers as Record<string, string>,
      };
    });
  }

  async put<T>(path: string, data?: any): Promise<ApiResponse<T>> {
    return this.withRetry(async () => {
      const response = await this.client.put<T>(path, data);
      return {
        data: response.data,
        status: response.status,
        headers: response.headers as Record<string, string>,
      };
    });
  }

  async delete<T>(path: string): Promise<ApiResponse<T>> {
    return this.withRetry(async () => {
      const response = await this.client.delete<T>(path);
      return {
        data: response.data,
        status: response.status,
        headers: response.headers as Record<string, string>,
      };
    });
  }
}

// Custom error classes
class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = 'ApiError';
  }
}

class ServerError extends ApiError {
  constructor(message: string, status: number) {
    super(message, status);
    this.name = 'ServerError';
  }
}

class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

class TimeoutError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'TimeoutError';
  }
}

class RateLimitError extends Error {
  constructor(message: string, public retryAfter?: string) {
    super(message);
    this.name = 'RateLimitError';
  }
}

export { ApiClient, ApiError, ServerError, NetworkError, TimeoutError, RateLimitError };
```

### Python

```python
# api_client.py
import time
import logging
from typing import TypeVar, Generic, Optional, Dict, Any
from dataclasses import dataclass
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class ApiResponse(Generic[T]):
    data: T
    status: int
    headers: Dict[str, str]

class ApiError(Exception):
    def __init__(self, message: str, status: int):
        super().__init__(message)
        self.status = status

class ServerError(ApiError):
    pass

class RateLimitError(ApiError):
    def __init__(self, message: str, retry_after: Optional[str] = None):
        super().__init__(message, 429)
        self.retry_after = retry_after

class NetworkError(Exception):
    pass

class TimeoutError(Exception):
    pass

class ApiClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        retries: int = 3,
        api_key: Optional[str] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retries = retries

        self.session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'

    def _handle_response(self, response: requests.Response) -> ApiResponse:
        if response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded",
                response.headers.get('Retry-After')
            )

        if response.status_code >= 500:
            raise ServerError(response.text, response.status_code)

        if response.status_code >= 400:
            raise ApiError(response.text, response.status_code)

        return ApiResponse(
            data=response.json() if response.text else None,
            status=response.status_code,
            headers=dict(response.headers)
        )

    def _request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> ApiResponse:
        url = f"{self.base_url}{path}"
        logger.info(f"[API] {method.upper()} {url}")

        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(str(e))

    def get(self, path: str, params: Optional[Dict] = None) -> ApiResponse:
        return self._request('GET', path, params=params)

    def post(self, path: str, data: Optional[Any] = None) -> ApiResponse:
        return self._request('POST', path, json=data)

    def put(self, path: str, data: Optional[Any] = None) -> ApiResponse:
        return self._request('PUT', path, json=data)

    def delete(self, path: str) -> ApiResponse:
        return self._request('DELETE', path)
```

### Go

```go
// apiclient.go
package apiclient

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

type Config struct {
    BaseURL string
    Timeout time.Duration
    Retries int
    APIKey  string
}

type Client struct {
    httpClient *http.Client
    baseURL    string
    retries    int
    apiKey     string
}

type Response struct {
    Data    json.RawMessage
    Status  int
    Headers http.Header
}

func New(cfg Config) *Client {
    timeout := cfg.Timeout
    if timeout == 0 {
        timeout = 10 * time.Second
    }

    retries := cfg.Retries
    if retries == 0 {
        retries = 3
    }

    return &Client{
        httpClient: &http.Client{Timeout: timeout},
        baseURL:    cfg.BaseURL,
        retries:    retries,
        apiKey:     cfg.APIKey,
    }
}

func (c *Client) doWithRetry(ctx context.Context, req *http.Request) (*Response, error) {
    var lastErr error

    for attempt := 0; attempt <= c.retries; attempt++ {
        if attempt > 0 {
            backoff := time.Duration(1<<uint(attempt-1)) * time.Second
            time.Sleep(backoff)
        }

        resp, err := c.httpClient.Do(req.WithContext(ctx))
        if err != nil {
            lastErr = fmt.Errorf("network error: %w", err)
            continue
        }
        defer resp.Body.Close()

        body, _ := io.ReadAll(resp.Body)

        if resp.StatusCode >= 500 {
            lastErr = fmt.Errorf("server error: %d", resp.StatusCode)
            continue
        }

        if resp.StatusCode >= 400 {
            return nil, fmt.Errorf("api error %d: %s", resp.StatusCode, string(body))
        }

        return &Response{
            Data:    body,
            Status:  resp.StatusCode,
            Headers: resp.Header,
        }, nil
    }

    return nil, lastErr
}

func (c *Client) Get(ctx context.Context, path string) (*Response, error) {
    req, err := http.NewRequest("GET", c.baseURL+path, nil)
    if err != nil {
        return nil, err
    }
    c.setHeaders(req)
    return c.doWithRetry(ctx, req)
}

func (c *Client) Post(ctx context.Context, path string, data any) (*Response, error) {
    body, err := json.Marshal(data)
    if err != nil {
        return nil, err
    }

    req, err := http.NewRequest("POST", c.baseURL+path, bytes.NewReader(body))
    if err != nil {
        return nil, err
    }
    c.setHeaders(req)
    return c.doWithRetry(ctx, req)
}

func (c *Client) setHeaders(req *http.Request) {
    req.Header.Set("Content-Type", "application/json")
    if c.apiKey != "" {
        req.Header.Set("Authorization", "Bearer "+c.apiKey)
    }
}
```

---

## Common Mistakes to Avoid

### 1. No Timeout Configuration
```typescript
// BAD - no timeout, request can hang forever
const client = axios.create({ baseURL: 'https://api.example.com' });

// GOOD - always set a timeout
const client = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000
});
```

### 2. Retrying Non-Idempotent Operations
```typescript
// BAD - retrying POST without idempotency key can cause duplicates
async post(path, data) {
  return this.withRetry(() => this.client.post(path, data));
}

// GOOD - use idempotency keys for non-idempotent operations
async post(path, data, idempotencyKey?: string) {
  const headers = idempotencyKey
    ? { 'Idempotency-Key': idempotencyKey }
    : {};
  return this.client.post(path, data, { headers });
}
```

### 3. Not Handling Rate Limits
```typescript
// BAD - treats rate limit like any other error
if (error.response.status >= 400) {
  throw new Error('Request failed');
}

// GOOD - specific handling for rate limits
if (error.response.status === 429) {
  const retryAfter = error.response.headers['retry-after'];
  throw new RateLimitError('Rate limited', retryAfter);
}
```

### 4. Logging Sensitive Data
```typescript
// BAD - logs full request including auth headers
console.log('Request:', JSON.stringify(config));

// GOOD - sanitize before logging
console.log('Request:', config.method, config.url);
```

### 5. Hardcoding Base URLs
```typescript
// BAD - hardcoded URL
const client = new ApiClient({ baseUrl: 'https://api.stripe.com' });

// GOOD - from configuration
const client = new ApiClient({ baseUrl: process.env.STRIPE_API_URL });
```

---

## Validation Commands

```bash
# Verify API client module exists and compiles
npx tsc --noEmit src/api-client.ts

# Run API client unit tests
npm test -- --testPathPattern="api-client"

# Test timeout behavior (should fail gracefully)
curl --max-time 1 http://localhost:8080/slow-endpoint || echo "Timeout handled"

# Verify retry logic with mock server
npm run test:integration -- --grep "retry"

# Check for hardcoded URLs
! grep -rE "https?://[a-z]+\.(com|io|net)" src/api-client.ts || echo "WARNING: Hardcoded URLs found"
```

---

## Related Conventions

- **Timeouts**: All HTTP clients MUST have timeouts configured (default: 10s)
- **Retries**: Use exponential backoff with max 3 retries
- **Error Types**: Use typed errors (ApiError, NetworkError, TimeoutError)
- **Logging**: Log request method and URL, never log auth headers or request bodies
- **Configuration**: Base URLs MUST come from environment/config, never hardcoded

---

## See Also

- [Error Handling](error-handling.md) - For comprehensive error strategies
- [Config Loading](config-loading.md) - For loading API keys and base URLs
- [Test Fixtures](test-fixtures.md) - For mocking API responses in tests
