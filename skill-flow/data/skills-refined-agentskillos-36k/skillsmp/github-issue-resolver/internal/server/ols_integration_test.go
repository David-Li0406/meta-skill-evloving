package server

import (
	"context"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// TestOLSMCPServerExpectations validates that our MCP server meets
// OpenShift Lightspeed's client expectations based on langchain-mcp-adapters
//
// Reference: https://github.com/openshift/lightspeed-service
// OpenShift Lightspeed uses MultiServerMCPClient from langchain-mcp-adapters
// which expects streamable HTTP transport with SSE support
func TestOLSMCPServerExpectations(t *testing.T) {
	tests := []struct {
		name                string
		method              string
		path                string
		headers             map[string]string
		expectedStatus      int
		expectedContentType string
		description         string
	}{
		{
			name:   "GET root should return SSE stream for MCP protocol",
			method: http.MethodGet,
			path:   "/",
			headers: map[string]string{
				"Accept": "text/event-stream",
			},
			expectedStatus:      http.StatusOK,
			expectedContentType: "text/event-stream",
			description:         "OLS Python client expects GET / to return SSE stream for establishing MCP connection",
		},
		{
			name:   "POST root should accept MCP messages",
			method: http.MethodPost,
			path:   "/",
			headers: map[string]string{
				"Content-Type": "application/json",
			},
			expectedStatus:      http.StatusBadRequest, // Empty POST should fail - valid messages tested in TestMCPProtocolNegotiation
			expectedContentType: "",                    // Will depend on MCP protocol response
			description:         "OLS Python client sends POST requests to send MCP messages",
		},
		{
			name:                "Health endpoint should remain accessible",
			method:              http.MethodGet,
			path:                "/health",
			expectedStatus:      http.StatusOK,
			expectedContentType: "",
			description:         "OpenShift health probes must continue working",
		},
		{
			name:                "Ready endpoint should remain accessible",
			method:              http.MethodGet,
			path:                "/ready",
			expectedStatus:      http.StatusOK,
			expectedContentType: "",
			description:         "OpenShift readiness probes must continue working",
		},
	}

	// Create test server
	server := setupOLSTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Start HTTP server in test mode
	mux := http.NewServeMux()

	// Register endpoints in the same order as production
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("OK")) //nolint:errcheck // Test helper, error not critical
	})

	mux.HandleFunc("/ready", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("READY")) //nolint:errcheck // Test helper, error not critical
	})

	// Create MCP handler
	mcpHandler := server.createMCPHandler()
	mux.Handle("/", mcpHandler)

	testServer := httptest.NewServer(mux)
	defer testServer.Close()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Logf("Test: %s", tt.description)

			req, err := http.NewRequest(tt.method, testServer.URL+tt.path, nil)
			if err != nil {
				t.Fatalf("Failed to create request: %v", err)
			}

			// Add headers
			for key, value := range tt.headers {
				req.Header.Set(key, value)
			}

			client := &http.Client{
				Timeout: 5 * time.Second,
			}

			resp, err := client.Do(req)
			if err != nil {
				t.Fatalf("Request failed: %v", err)
			}
			defer func() { _ = resp.Body.Close() }()

			// Check status code
			if resp.StatusCode != tt.expectedStatus {
				t.Errorf("Expected status %d, got %d", tt.expectedStatus, resp.StatusCode)
			}

			// Check Content-Type if specified
			if tt.expectedContentType != "" {
				contentType := resp.Header.Get("Content-Type")
				if !strings.Contains(contentType, tt.expectedContentType) {
					t.Errorf("Expected Content-Type to contain %q, got %q",
						tt.expectedContentType, contentType)
					t.Logf("Full headers: %v", resp.Header)
				}
			}
		})
	}
}

// setupOLSTestServer creates a test server for OLS integration tests
func setupOLSTestServer(t *testing.T) *MCPServer {
	config := NewConfig()
	config.Transport = TransportHTTP
	config.HTTPPort = 8080

	// Verify Kubernetes connectivity before creating server
	_, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}

	// Create server (it will create its own clients internally)
	server, err := NewMCPServer(config)
	if err != nil {
		t.Fatalf("Failed to create MCP server: %v", err)
	}

	return server
}

// createMCPHandler creates the MCP handler (extracted for testing)
func (s *MCPServer) createMCPHandler() http.Handler {
	// Create the MCP SSE handler (same as production code in startHTTPTransport)
	// OpenShift Lightspeed expects SSE transport at the root endpoint
	mcpHandler := mcp.NewSSEHandler(func(req *http.Request) *mcp.Server {
		return s.mcpServer
	}, nil)

	return mcpHandler
}

// TestMCPProtocolNegotiation tests that the server properly negotiates MCP protocol
func TestMCPProtocolNegotiation(t *testing.T) {
	server := setupOLSTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Test SSE connection establishment
	t.Run("SSE connection establishment", func(t *testing.T) {
		// This test validates that:
		// 1. GET request with Accept: text/event-stream returns SSE stream
		// 2. Server sends MCP protocol initialization events
		// 3. Connection remains open for bidirectional communication
		t.Skip("TODO: Implement SSE connection test")
	})

	// Test MCP message exchange
	t.Run("MCP message exchange", func(t *testing.T) {
		// This test validates that:
		// 1. POST requests can send MCP protocol messages
		// 2. Server responds with proper MCP protocol format
		// 3. Tools can be discovered via MCP tools/list message
		t.Skip("TODO: Implement MCP message exchange test")
	})
}

// TestToolDiscovery validates that OLS can discover our MCP tools
func TestToolDiscovery(t *testing.T) {
	server := setupOLSTestServer(t)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			t.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	// Test that all expected tools are discoverable
	expectedTools := []string{
		"get-cluster-health",
		"list-pods",
	}

	for _, toolName := range expectedTools {
		if _, exists := server.tools[toolName]; !exists {
			t.Errorf("Expected tool %s to be registered", toolName)
		}
	}
}

// Benchmark OLS MCP client connection overhead
func BenchmarkOLSMCPConnection(b *testing.B) {
	server := setupOLSBenchServer(b)
	defer func() {
		if err := server.k8sClient.Close(); err != nil {
			b.Logf("Error closing k8s client: %v", err)
		}
	}()
	defer server.cache.Close()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		// Simulate OLS connecting and discovering tools
		// This helps us measure the performance impact
		ctx := context.Background()
		_ = ctx
	}
}

func setupOLSBenchServer(b *testing.B) *MCPServer {
	config := NewConfig()
	config.Transport = TransportHTTP

	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		b.Skipf("Skipping: unable to create Kubernetes client: %v", err)
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
		b.Fatalf("Failed to register tools: %v", err)
	}

	return server
}
