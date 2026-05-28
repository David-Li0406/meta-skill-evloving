# API Client Patterns for Terraform Providers

## Overview

This guide covers patterns for implementing and testing API clients in Terraform providers, with focus on authentication, request patterns, error handling, and testing strategies.

## Client Architecture

### Basic Client Structure

```go
type APIClient struct {
    endpoint   string
    httpClient *http.Client
    token      string    // or cookie, API key, etc.
    timeout    time.Duration
}

func NewAPIClient(ctx context.Context, endpoint, username, password string,
    insecureSkipVerify bool, timeout int) (*APIClient, error) {

    // Create HTTP client with cookie jar for session management
    jar, _ := cookiejar.New(&cookiejar.Options{
        PublicSuffixList: publicsuffix.List,
    })

    httpClient := &http.Client{
        Jar:     jar,
        Timeout: time.Duration(timeout) * time.Second,
        Transport: &http.Transport{
            TLSClientConfig: &tls.Config{
                InsecureSkipVerify: insecureSkipVerify,
            },
        },
    }

    client := &APIClient{
        endpoint:   endpoint,
        httpClient: httpClient,
        timeout:    time.Duration(timeout) * time.Second,
    }

    // Authenticate during initialization
    if err := client.authenticate(ctx, username, password); err != nil {
        return nil, fmt.Errorf("authentication failed: %w", err)
    }

    return client, nil
}
```

### Authentication Patterns

#### Cookie-Based Authentication

```go
func (c *APIClient) authenticate(ctx context.Context, username, password string) error {
    authPayload := map[string]interface{}{
        "service":  "login",
        "username": username,
        "password": password,
    }

    body, _ := json.Marshal(authPayload)
    req, _ := http.NewRequestWithContext(ctx, "POST", c.endpoint+"/json", bytes.NewBuffer(body))
    req.Header.Set("Content-Type", "application/json")

    resp, err := c.httpClient.Do(req)
    if err != nil {
        return fmt.Errorf("authentication request failed: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("authentication failed with status: %d", resp.StatusCode)
    }

    // Cookie automatically stored in jar
    return nil
}
```

#### Token-Based Authentication

```go
func (c *APIClient) authenticate(ctx context.Context, apiKey string) error {
    // Test authentication by making a simple API call
    req, _ := http.NewRequestWithContext(ctx, "GET", c.endpoint+"/api/v1/user", nil)
    req.Header.Set("Authorization", "Bearer "+apiKey)

    resp, err := c.httpClient.Do(req)
    if err != nil {
        return fmt.Errorf("authentication test failed: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("invalid API key")
    }

    c.token = apiKey
    return nil
}
```

## API Call Patterns

### JSON-RPC Pattern

Common in systems like BCM (Bright Cluster Manager):

```go
func (c *APIClient) CallJSONRPC(ctx context.Context, service, method string,
    args ...interface{}) ([]byte, error) {

    payload := map[string]interface{}{
        "service": service,
        "call":    method,
    }

    // Add args if provided (for parameterized calls)
    if len(args) > 0 {
        payload["args"] = args
    }

    body, _ := json.Marshal(payload)
    req, _ := http.NewRequestWithContext(ctx, "POST", c.endpoint+"/json",
        bytes.NewBuffer(body))
    req.Header.Set("Content-Type", "application/json")

    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("API call failed: %w", err)
    }
    defer resp.Body.Close()

    responseBody, _ := io.ReadAll(resp.Body)

    // Check for API-level errors
    if err := c.parseErrorResponse(responseBody); err != nil {
        return nil, err
    }

    return responseBody, nil
}
```

### REST API Pattern

Standard REST endpoints:

```go
func (c *APIClient) Get(ctx context.Context, path string) ([]byte, error) {
    req, _ := http.NewRequestWithContext(ctx, "GET", c.endpoint+path, nil)
    req.Header.Set("Authorization", "Bearer "+c.token)

    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("GET request failed: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("request failed with status: %d", resp.StatusCode)
    }

    return io.ReadAll(resp.Body)
}

func (c *APIClient) Post(ctx context.Context, path string, data interface{}) ([]byte, error) {
    body, _ := json.Marshal(data)
    req, _ := http.NewRequestWithContext(ctx, "POST", c.endpoint+path,
        bytes.NewBuffer(body))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer "+c.token)

    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("POST request failed: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
        return nil, fmt.Errorf("request failed with status: %d", resp.StatusCode)
    }

    return io.ReadAll(resp.Body)
}
```

## Error Handling

### Multi-Layer Error Detection

APIs may return errors in multiple formats:

```go
func (c *APIClient) parseErrorResponse(body []byte) error {
    // Layer 1: Check for error object
    var errorResponse map[string]interface{}
    if err := json.Unmarshal(body, &errorResponse); err == nil {
        if errMsg, ok := errorResponse["error"].(string); ok && errMsg != "" {
            return fmt.Errorf("API error: %s", errMsg)
        }
    }

    // Layer 2: Check for success=false
    if success, ok := errorResponse["success"].(bool); ok && !success {
        if msg, ok := errorResponse["message"].(string); ok {
            return fmt.Errorf("API request failed: %s", msg)
        }
        return fmt.Errorf("API request failed")
    }

    // Layer 3: Check for status field
    if status, ok := errorResponse["status"].(string); ok && status == "error" {
        if msg, ok := errorResponse["message"].(string); ok {
            return fmt.Errorf("API error: %s", msg)
        }
    }

    return nil
}
```

### Retry Logic with Exponential Backoff

```go
func (c *APIClient) CallWithRetry(ctx context.Context, maxRetries int,
    callFunc func() ([]byte, error)) ([]byte, error) {

    var lastErr error

    for i := 0; i < maxRetries; i++ {
        result, err := callFunc()
        if err == nil {
            return result, nil
        }

        lastErr = err

        // Don't retry on certain errors (e.g., 404, 401)
        if isNonRetryableError(err) {
            return nil, err
        }

        // Exponential backoff: 1s, 2s, 4s, 8s, etc.
        if i < maxRetries-1 {
            backoff := time.Duration(1<<uint(i)) * time.Second
            time.Sleep(backoff)
        }
    }

    return nil, fmt.Errorf("max retries exceeded: %w", lastErr)
}

func isNonRetryableError(err error) bool {
    // Check for specific error types that shouldn't be retried
    if strings.Contains(err.Error(), "401") ||
       strings.Contains(err.Error(), "403") ||
       strings.Contains(err.Error(), "404") {
        return true
    }
    return false
}
```

## Testing Patterns

### Client Creation for Tests

Create a dedicated test helper:

```go
// test_helpers.go
func createTestAPIClient(t *testing.T) *APIClient {
    endpoint := os.Getenv("API_ENDPOINT")
    username := os.Getenv("API_USERNAME")
    password := os.Getenv("API_PASSWORD")

    if endpoint == "" || username == "" || password == "" {
        t.Fatalf("API credentials not set (API_ENDPOINT, API_USERNAME, API_PASSWORD)")
    }

    client, err := NewAPIClient(context.Background(), endpoint, username, password, true, 30)
    if err != nil {
        t.Fatalf("Failed to create API client: %v", err)
    }

    return client
}
```

### Eventual Consistency Handling

```go
func verifyResourceState(ctx context.Context, client *APIClient,
    resourceID, expectedState string, maxRetries int) (bool, error) {

    for i := 0; i < maxRetries; i++ {
        body, err := client.Get(ctx, "/resources/"+resourceID)
        if err != nil {
            // Resource might not exist yet
            if i < maxRetries-1 {
                time.Sleep(time.Duration(1<<uint(i)) * time.Second)
                continue
            }
            return false, err
        }

        var resource map[string]interface{}
        json.Unmarshal(body, &resource)

        if state, ok := resource["state"].(string); ok && state == expectedState {
            return true, nil
        }

        // Wait before next retry (exponential backoff)
        if i < maxRetries-1 {
            time.Sleep(time.Duration(1<<uint(i)) * time.Second)
        }
    }

    return false, fmt.Errorf("resource did not reach expected state after %d retries", maxRetries)
}
```

## Field Name Mapping

### Snake Case vs Camel Case

Terraform uses snake_case, but many APIs use camelCase:

```go
// Document mappings in test_helpers.go
//
// Field Name Mappings (Terraform → API):
//   kernel_parameters     → kernelParameters
//   enable_sol           → enableSOL
//   sol_speed            → solSpeed
//   management_network   → managementNetwork
//   boot_loader          → bootLoader

// Helper to convert field names
func toAPIFieldName(terraformField string) string {
    // Map of special cases (acronyms, etc.)
    specialCases := map[string]string{
        "enable_sol":      "enableSOL",
        "sol_speed":       "solSpeed",
        "sol_flow_control": "solFlowControl",
        "sol_port":        "solPort",
    }

    if apiName, ok := specialCases[terraformField]; ok {
        return apiName
    }

    // Standard snake_case to camelCase conversion
    parts := strings.Split(terraformField, "_")
    for i := 1; i < len(parts); i++ {
        parts[i] = strings.Title(parts[i])
    }
    return strings.Join(parts, "")
}
```

## Advanced Patterns

### Async Operations with Polling

```go
func (c *APIClient) CreateResourceAsync(ctx context.Context, resourceData map[string]interface{}) (string, error) {
    // Initiate async operation
    body, err := c.Post(ctx, "/resources", resourceData)
    if err != nil {
        return "", err
    }

    var response map[string]interface{}
    json.Unmarshal(body, &response)
    resourceID := response["id"].(string)

    // Poll for completion
    for i := 0; i < 30; i++ { // 30 attempts = ~1 minute
        body, err := c.Get(ctx, "/resources/"+resourceID)
        if err != nil {
            return "", err
        }

        var resource map[string]interface{}
        json.Unmarshal(body, &resource)

        status := resource["status"].(string)
        if status == "completed" {
            return resourceID, nil
        } else if status == "failed" {
            return "", fmt.Errorf("resource creation failed: %s", resource["error"])
        }

        // Wait before next poll (exponential backoff)
        time.Sleep(time.Duration(1<<uint(i/3)) * time.Second)
    }

    return "", fmt.Errorf("resource creation timeout")
}
```

### Batch Operations

```go
func (c *APIClient) BatchGet(ctx context.Context, resourceIDs []string) ([]map[string]interface{}, error) {
    results := make([]map[string]interface{}, 0, len(resourceIDs))

    // Use goroutines for parallel fetching
    type result struct {
        data map[string]interface{}
        err  error
        idx  int
    }

    resultChan := make(chan result, len(resourceIDs))

    for i, id := range resourceIDs {
        go func(idx int, resourceID string) {
            body, err := c.Get(ctx, "/resources/"+resourceID)
            if err != nil {
                resultChan <- result{err: err, idx: idx}
                return
            }

            var data map[string]interface{}
            json.Unmarshal(body, &data)
            resultChan <- result{data: data, idx: idx}
        }(i, id)
    }

    // Collect results
    resultsMap := make(map[int]map[string]interface{})
    for i := 0; i < len(resourceIDs); i++ {
        res := <-resultChan
        if res.err != nil {
            return nil, res.err
        }
        resultsMap[res.idx] = res.data
    }

    // Return in original order
    for i := 0; i < len(resourceIDs); i++ {
        results = append(results, resultsMap[i])
    }

    return results, nil
}
```

## Best Practices

1. **Authentication**: Perform during client initialization, not per-request
2. **Timeouts**: Always set reasonable timeouts (30-60s recommended)
3. **Context**: Always accept and pass context for cancellation support
4. **Error Wrapping**: Use `fmt.Errorf` with `%w` to preserve error chains
5. **Retry Logic**: Implement exponential backoff for transient failures
6. **Session Management**: Use `http.Client` with cookiejar for cookie-based auth
7. **TLS**: Support `InsecureSkipVerify` for development, but default to secure
8. **Testing**: Create separate test client helpers to avoid duplication
9. **Field Mapping**: Document snake_case ↔ camelCase mappings explicitly
10. **Eventual Consistency**: Always account for async operations with polling

## Common Pitfalls

❌ Not handling multi-layer error responses
❌ Missing exponential backoff for retries
❌ Ignoring eventual consistency (immediate reads after writes)
❌ Not documenting field name mappings
❌ Hardcoding credentials in tests
❌ Missing context cancellation support
❌ Not setting HTTP client timeouts
❌ Retrying non-retryable errors (401, 403, 404)
❌ Not preserving error context with `%w`
❌ Duplicating client creation logic across tests
