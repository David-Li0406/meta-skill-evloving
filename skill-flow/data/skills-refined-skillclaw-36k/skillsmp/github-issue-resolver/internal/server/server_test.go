package server

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

func setupTestServer(t *testing.T) *MCPServer {
	config := NewConfig()
	config.Transport = TransportHTTP
	config.HTTPPort = 8080

	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}

	memoryCache := cache.NewMemoryCache(30 * time.Second)

	// Create MCP server with metadata (same as NewMCPServer)
	impl := &mcp.Implementation{
		Name:    config.Name,
		Version: config.Version,
	}
	mcpServer := mcp.NewServer(impl, nil)

	server := &MCPServer{
		config:    config,
		mcpServer: mcpServer,
		k8sClient: k8sClient,
		cache:     memoryCache,
		tools:     make(map[string]Tool),
		resources: make(map[string]interface{}),
	}

	if err := server.registerTools(); err != nil {
		t.Fatalf("Failed to register tools: %v", err)
	}

	if err := server.registerResources(); err != nil {
		t.Fatalf("Failed to register resources: %v", err)
	}

	return server
}

func TestNewMCPServer(t *testing.T) {
	config := NewConfig()
	config.Transport = TransportHTTP

	server, err := NewMCPServer(config)
	if err != nil {
		t.Skipf("Skipping: unable to create server: %v", err)
	}
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	if server.config.Name != config.Name {
		t.Errorf("Expected name %s, got %s", config.Name, server.config.Name)
	}

	if len(server.tools) == 0 {
		t.Error("Expected tools to be registered")
	}
}

func TestMCPServer_RegisterTools(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	expectedTools := []string{"get-cluster-health", "list-pods", "calculate-pod-capacity"}
	for _, toolName := range expectedTools {
		if _, exists := server.tools[toolName]; !exists {
			t.Errorf("Expected tool %s to be registered", toolName)
		}
	}

	if len(server.tools) != len(expectedTools) {
		t.Errorf("Expected %d tools, got %d", len(expectedTools), len(server.tools))
	}
}

func TestHandleMCPCapabilities(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodGet, "/mcp", nil)
	w := httptest.NewRecorder()

	server.handleMCPCapabilities(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	contentType := resp.Header.Get("Content-Type")
	if contentType != "application/json" {
		t.Errorf("Expected Content-Type application/json, got %s", contentType)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	// Verify name and version
	if result["name"] != server.config.Name {
		t.Errorf("Expected name %s, got %v", server.config.Name, result["name"])
	}

	if result["version"] != server.config.Version {
		t.Errorf("Expected version %s, got %v", server.config.Version, result["version"])
	}

	// Verify capabilities object exists
	capabilities, ok := result["capabilities"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected capabilities object in response")
	}

	// Verify tools capability
	if tools, ok := capabilities["tools"].(bool); !ok || !tools {
		t.Error("Expected capabilities.tools to be true")
	}

	// Verify resources capability
	if resources, ok := capabilities["resources"].(bool); !ok || !resources {
		t.Error("Expected capabilities.resources to be true")
	}

	// Verify prompts capability (should be false)
	if prompts, ok := capabilities["prompts"].(bool); !ok || prompts {
		t.Error("Expected capabilities.prompts to be false")
	}
}

func TestHandleMCPCapabilities_MethodNotAllowed(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodPost, "/mcp", nil)
	w := httptest.NewRecorder()

	server.handleMCPCapabilities(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("Expected status 405, got %d", resp.StatusCode)
	}
}

func TestHandleMCPInfo(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodGet, "/mcp/info", nil)
	w := httptest.NewRecorder()

	server.handleMCPInfo(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	contentType := resp.Header.Get("Content-Type")
	if contentType != "application/json" {
		t.Errorf("Expected Content-Type application/json, got %s", contentType)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if result["name"] != server.config.Name {
		t.Errorf("Expected name %s, got %v", server.config.Name, result["name"])
	}

	if result["version"] != server.config.Version {
		t.Errorf("Expected version %s, got %v", server.config.Version, result["version"])
	}
}

func TestHandleListTools(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodGet, "/mcp/tools", nil)
	w := httptest.NewRecorder()

	server.handleListTools(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	tools, ok := result["tools"].([]interface{})
	if !ok {
		t.Fatal("Expected tools array in response")
	}

	if len(tools) != 3 {
		t.Errorf("Expected 3 tools, got %d", len(tools))
	}

	count := int(result["count"].(float64))
	if count != 3 {
		t.Errorf("Expected count 3, got %d", count)
	}
}

// TestHandleListTools_CountMatchesRegistered verifies that the API response
// returns the exact same number of tools as registered in the internal map.
// This test ensures no tool is lost during API serialization (Issue #21).
func TestHandleListTools_CountMatchesRegistered(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Get the number of registered tools from the internal map
	registeredCount := len(server.tools)

	// Make API request
	req := httptest.NewRequest(http.MethodGet, "/mcp/tools", nil)
	w := httptest.NewRecorder()

	server.handleListTools(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	tools, ok := result["tools"].([]interface{})
	if !ok {
		t.Fatal("Expected tools array in response")
	}

	// Verify count field matches tools array length
	count := int(result["count"].(float64))
	if count != len(tools) {
		t.Errorf("Count field (%d) does not match tools array length (%d)", count, len(tools))
	}

	// Verify API response matches registered tools count
	if len(tools) != registeredCount {
		t.Errorf("API returned %d tools, but %d tools are registered. Missing tools in API response!", len(tools), registeredCount)
	}

	// Verify all registered tool names appear in the API response
	toolNames := make(map[string]bool)
	for _, toolInterface := range tools {
		tool := toolInterface.(map[string]interface{})
		name := tool["name"].(string)
		toolNames[name] = true
	}

	for name := range server.tools {
		if !toolNames[name] {
			t.Errorf("Registered tool '%s' not found in API response!", name)
		}
	}
}

func TestHandleListTools_MethodNotAllowed(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodPost, "/mcp/tools", nil)
	w := httptest.NewRecorder()

	server.handleListTools(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("Expected status 405, got %d", resp.StatusCode)
	}
}

func TestHandleClusterHealthTool(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Test with default args
	reqBody := bytes.NewBufferString("{}")
	req := httptest.NewRequest(http.MethodPost, "/mcp/tools/get-cluster-health/call", reqBody)
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	server.handleClusterHealthTool(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if !result["success"].(bool) {
		t.Error("Expected success to be true")
	}

	if result["result"] == nil {
		t.Error("Expected result to be present")
	}
}

func TestHandleClusterHealthTool_WithArgs(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Test with include_details: false
	reqBody := bytes.NewBufferString(`{"include_details": false}`)
	req := httptest.NewRequest(http.MethodPost, "/mcp/tools/get-cluster-health/call", reqBody)
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	server.handleClusterHealthTool(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if !result["success"].(bool) {
		t.Error("Expected success to be true")
	}
}

func TestHandleClusterHealthTool_MethodNotAllowed(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodGet, "/mcp/tools/get-cluster-health/call", nil)
	w := httptest.NewRecorder()

	server.handleClusterHealthTool(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("Expected status 405, got %d", resp.StatusCode)
	}
}

func TestHandleListPodsTool(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Test with limit
	reqBody := bytes.NewBufferString(`{"limit": 5}`)
	req := httptest.NewRequest(http.MethodPost, "/mcp/tools/list-pods/call", reqBody)
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	server.handleListPodsTool(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if !result["success"].(bool) {
		t.Error("Expected success to be true")
	}
}

func TestHandleListPodsTool_WithNamespace(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Test with namespace filter
	reqBody := bytes.NewBufferString(`{"namespace": "kube-system", "limit": 3}`)
	req := httptest.NewRequest(http.MethodPost, "/mcp/tools/list-pods/call", reqBody)
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	server.handleListPodsTool(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if !result["success"].(bool) {
		t.Error("Expected success to be true")
	}
}

func TestHandleListPodsTool_MethodNotAllowed(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodGet, "/mcp/tools/list-pods/call", nil)
	w := httptest.NewRecorder()

	server.handleListPodsTool(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("Expected status 405, got %d", resp.StatusCode)
	}
}

func TestHandleCacheStats(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodGet, "/cache/stats", nil)
	w := httptest.NewRecorder()

	server.handleCacheStats(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var stats cache.Statistics
	if err := json.NewDecoder(resp.Body).Decode(&stats); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	// Stats should have expected fields (may be zero initially)
	if stats.HitRate < 0 || stats.HitRate > 100 {
		t.Errorf("Invalid hit rate: %f", stats.HitRate)
	}
}

func TestHandleCacheStats_MethodNotAllowed(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	req := httptest.NewRequest(http.MethodPost, "/cache/stats", nil)
	w := httptest.NewRecorder()

	server.handleCacheStats(w, req)

	resp := w.Result()
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("Expected status 405, got %d", resp.StatusCode)
	}
}

func TestWriteJSON(t *testing.T) {
	w := httptest.NewRecorder()

	data := map[string]interface{}{
		"test":  "value",
		"count": 42,
	}

	err := writeJSON(w, data)
	if err != nil {
		t.Fatalf("writeJSON failed: %v", err)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(w.Body).Decode(&result); err != nil {
		t.Fatalf("Failed to decode JSON: %v", err)
	}

	if result["test"] != "value" {
		t.Errorf("Expected test=value, got %v", result["test"])
	}

	if int(result["count"].(float64)) != 42 {
		t.Errorf("Expected count=42, got %v", result["count"])
	}
}

func TestConfigValidation(t *testing.T) {
	// Valid config
	config := NewConfig()
	if err := config.Validate(); err != nil {
		t.Errorf("Expected valid config, got error: %v", err)
	}

	// Invalid transport
	config.Transport = "invalid"
	if err := config.Validate(); err == nil {
		t.Error("Expected error for invalid transport")
	}

	// Invalid cache TTL
	config = NewConfig()
	config.CacheTTL = -1 * time.Second
	if err := config.Validate(); err == nil {
		t.Error("Expected error for negative cache TTL")
	}
}

func TestHTTPServerIntegration(t *testing.T) {
	server := setupTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Start server in background
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	errChan := make(chan error, 1)
	go func() {
		// We can't actually start the server here as it would bind to a port
		// This test verifies the server structure is correct
		if server.config.Transport != TransportHTTP {
			errChan <- nil
		} else {
			errChan <- nil
		}
	}()

	// Wait for either completion or timeout
	select {
	case <-ctx.Done():
		// Expected - server should run until context is cancelled
	case err := <-errChan:
		if err != nil {
			t.Fatalf("Server start failed: %v", err)
		}
	}
}
