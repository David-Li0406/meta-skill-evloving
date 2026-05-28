package server

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/internal/prompts"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/internal/resources"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/internal/tools"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// MCPServer wraps the official MCP SDK server
type MCPServer struct {
	config         *Config
	mcpServer      *mcp.Server
	httpServer     *http.Server
	k8sClient      *clients.K8sClient
	ceClient       *clients.CoordinationEngineClient
	kserve         *clients.KServeClient
	cache          *cache.MemoryCache
	sessionManager *SessionManager          // Session manager for REST API clients
	tools          map[string]Tool          // Registry of available tools (typed for type safety)
	resources      map[string]interface{}   // Registry of available resources
	prompts        map[string]interface{}   // Registry of available prompts
}

// NewMCPServer creates a new MCP server instance
func NewMCPServer(config *Config) (*MCPServer, error) {
	if err := config.Validate(); err != nil {
		return nil, fmt.Errorf("invalid config: %w", err)
	}

	// Initialize Kubernetes client
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create Kubernetes client: %w", err)
	}

	// Verify cluster connectivity
	ctx := context.Background()
	if err := k8sClient.HealthCheck(ctx); err != nil {
		log.Printf("WARNING: Kubernetes health check failed: %v", err)
		log.Printf("Server will start but cluster health tools may not work")
	} else {
		version, _ := k8sClient.GetServerVersion(ctx)
		log.Printf("Connected to Kubernetes cluster (version: %s)", version)
	}

	// Initialize cache with configured TTL
	memoryCache := cache.NewMemoryCache(config.CacheTTL)
	log.Printf("Initialized cache with TTL: %s", config.CacheTTL)

	// Initialize Coordination Engine client if enabled
	var ceClient *clients.CoordinationEngineClient
	if config.EnableCoordinationEngine {
		ceClient = clients.NewCoordinationEngineClient(config.CoordinationEngineURL)
		log.Printf("Initialized Coordination Engine client: %s", config.CoordinationEngineURL)
	} else {
		log.Printf("Coordination Engine integration disabled (use ENABLE_COORDINATION_ENGINE=true to enable)")
	}

	// Initialize KServe client if enabled
	var kserveClient *clients.KServeClient
	if config.EnableKServe {
		kserveClient = clients.NewKServeClient(clients.KServeConfig{
			Namespace:     config.KServeNamespace,
			PredictorPort: config.KServePredictorPort,
			Timeout:       config.RequestTimeout,
			Enabled:       true,
			RestConfig:    k8sClient.GetConfig(), // Pass Kubernetes config for CRD access
		})
		log.Printf("Initialized KServe client for namespace: %s (predictor port: %d)", config.KServeNamespace, config.KServePredictorPort)
	} else {
		log.Printf("KServe integration disabled (use ENABLE_KSERVE=true to enable)")
	}

	// Create MCP server with metadata
	impl := &mcp.Implementation{
		Name:    config.Name,
		Version: config.Version,
	}

	mcpServer := mcp.NewServer(impl, nil)

	// Initialize session manager for REST API clients
	// Default TTL: 30 minutes, Max sessions: 1000
	sessionManager := NewSessionManager(30*time.Minute, 1000)
	log.Printf("Initialized session manager (TTL: 30m, max: 1000 sessions)")

	server := &MCPServer{
		config:         config,
		mcpServer:      mcpServer,
		k8sClient:      k8sClient,
		ceClient:       ceClient,
		kserve:         kserveClient,
		cache:          memoryCache,
		sessionManager: sessionManager,
		tools:          make(map[string]Tool),
		resources:      make(map[string]interface{}),
		prompts:        make(map[string]interface{}),
	}

	// Register tools
	if err := server.registerTools(); err != nil {
		return nil, fmt.Errorf("failed to register tools: %w", err)
	}

	// Register resources
	if err := server.registerResources(); err != nil {
		return nil, fmt.Errorf("failed to register resources: %w", err)
	}

	// Register prompts
	if err := server.registerPrompts(); err != nil {
		return nil, fmt.Errorf("failed to register prompts: %w", err)
	}

	log.Printf("MCP Server initialized: %s v%s", config.Name, config.Version)
	log.Printf("Transport: %s", config.Transport)

	return server, nil
}

// registerTools initializes and registers all MCP tools
func (s *MCPServer) registerTools() error {
	// Register cluster health tool (with cache)
	clusterHealthTool := tools.NewClusterHealthTool(s.k8sClient, s.cache)
	s.registerTool(clusterHealthTool)

	// Register list-pods tool (no cache - results change frequently)
	listPodsTool := tools.NewListPodsTool(s.k8sClient)
	s.registerTool(listPodsTool)

	// Register calculate-pod-capacity tool (capacity planning)
	calculatePodCapacityTool := tools.NewCalculatePodCapacityTool(s.k8sClient)
	s.registerTool(calculatePodCapacityTool)

	// Register Coordination Engine tools if enabled
	if s.ceClient != nil {
		listIncidentsTool := tools.NewListIncidentsTool(s.ceClient)
		s.registerTool(listIncidentsTool)

		triggerRemediationTool := tools.NewTriggerRemediationTool(s.ceClient)
		s.registerTool(triggerRemediationTool)

		// NEW: Remediation recommendations tool (ML predictions)
		remediationRecsTool := tools.NewGetRemediationRecommendationsTool(s.ceClient)
		s.registerTool(remediationRecsTool)

		// NEW: Create incident tool
		createIncidentTool := tools.NewCreateIncidentTool(s.ceClient)
		s.registerTool(createIncidentTool)

		// NEW: Predict resource usage tool (time-specific forecasting)
		predictResourceUsageTool := tools.NewPredictResourceUsageTool(s.ceClient, s.k8sClient)
		s.registerTool(predictResourceUsageTool)

		// NEW: Analyze scaling impact tool (capacity planning)
		analyzeScalingImpactTool := tools.NewAnalyzeScalingImpactTool(s.ceClient, s.k8sClient)
		s.registerTool(analyzeScalingImpactTool)
	} else {
		log.Printf("Skipping Coordination Engine tools (not enabled)")
	}

	// Register KServe tools if enabled
	if s.kserve != nil && s.ceClient != nil {
		// analyze-anomalies requires both KServe and Coordination Engine
		// The Coordination Engine handles feature engineering (45 features) and calls KServe
		analyzeAnomaliesTool := tools.NewAnalyzeAnomaliesTool(s.kserve, s.ceClient)
		s.registerTool(analyzeAnomaliesTool)

		getModelStatusTool := tools.NewGetModelStatusTool(s.kserve)
		s.registerTool(getModelStatusTool)

		listModelsTool := tools.NewListModelsTool(s.kserve)
		s.registerTool(listModelsTool)
	} else if s.kserve != nil && s.ceClient == nil {
		log.Printf("Skipping analyze-anomalies tool (requires Coordination Engine for feature engineering)")
		// Register other KServe tools that don't require Coordination Engine
		getModelStatusTool := tools.NewGetModelStatusTool(s.kserve)
		s.registerTool(getModelStatusTool)

		listModelsTool := tools.NewListModelsTool(s.kserve)
		s.registerTool(listModelsTool)
	} else {
		log.Printf("Skipping KServe tools (not enabled)")
	}

	log.Printf("Total tools registered: %d", len(s.tools))
	return nil
}

// Tool interface that our tools implement
type Tool interface {
	Name() string
	Description() string
	InputSchema() map[string]interface{}
	Execute(ctx context.Context, args map[string]interface{}) (interface{}, error)
}

// registerTool registers a tool with both our internal map and the MCP SDK
func (s *MCPServer) registerTool(tool Tool) {
	// Store in our internal map
	s.tools[tool.Name()] = tool

	// Create MCP tool definition
	mcpTool := &mcp.Tool{
		Name:        tool.Name(),
		Description: tool.Description(),
		InputSchema: tool.InputSchema(),
	}

	// Create handler function that wraps our tool's Execute method
	handler := func(ctx context.Context, req *mcp.CallToolRequest, params map[string]interface{}) (*mcp.CallToolResult, any, error) {
		// Add timeout enforcement to prevent hanging on slow operations
		timeoutCtx, cancel := context.WithTimeout(ctx, s.config.RequestTimeout)
		defer cancel()

		// Execute the tool with timeout context
		result, err := tool.Execute(timeoutCtx, params)
		if err != nil {
			return nil, nil, err
		}

		// Convert result to JSON string for MCP response
		resultJSON, err := json.Marshal(result)
		if err != nil {
			return nil, nil, fmt.Errorf("failed to marshal result: %w", err)
		}

		// Return as MCP CallToolResult
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{
					Text: string(resultJSON),
				},
			},
		}, nil, nil
	}

	// Register with MCP SDK
	mcp.AddTool(s.mcpServer, mcpTool, handler)

	log.Printf("Registered tool: %s - %s", tool.Name(), tool.Description())
}

// registerResources initializes and registers all MCP resources
func (s *MCPServer) registerResources() error {
	// Register cluster://health resource (always available)
	clusterHealthResource := resources.NewClusterHealthResource(s.k8sClient, s.ceClient, s.cache)
	s.resources[clusterHealthResource.URI()] = clusterHealthResource
	log.Printf("Registered resource: %s - %s", clusterHealthResource.URI(), clusterHealthResource.Name())

	// Register cluster://nodes resource (always available)
	nodesResource := resources.NewNodesResource(s.k8sClient, s.cache)
	s.resources[nodesResource.URI()] = nodesResource
	log.Printf("Registered resource: %s - %s", nodesResource.URI(), nodesResource.Name())

	// Register cluster://incidents resource (if Coordination Engine enabled)
	if s.ceClient != nil {
		incidentsResource := resources.NewIncidentsResource(s.ceClient, s.cache)
		s.resources[incidentsResource.URI()] = incidentsResource
		log.Printf("Registered resource: %s - %s", incidentsResource.URI(), incidentsResource.Name())

		// NEW: Remediation history resource
		remediationHistoryResource := resources.NewRemediationHistoryResource(s.ceClient, s.cache)
		s.resources[remediationHistoryResource.URI()] = remediationHistoryResource
		log.Printf("Registered resource: %s - %s", remediationHistoryResource.URI(), remediationHistoryResource.Name())
	} else {
		log.Printf("Skipping cluster://incidents resource (Coordination Engine not enabled)")
	}

	log.Printf("Total resources registered: %d", len(s.resources))
	return nil
}

// registerPrompts initializes and registers all MCP prompts
func (s *MCPServer) registerPrompts() error {
	// Core prompts (always available)
	diagnoseCluster := prompts.NewDiagnoseClusterPrompt()
	s.registerPrompt(diagnoseCluster)

	investigatePods := prompts.NewInvestigatePodsPrompt()
	s.registerPrompt(investigatePods)

	checkAnomalies := prompts.NewCheckAnomaliesPrompt()
	s.registerPrompt(checkAnomalies)

	optimizeAccess := prompts.NewOptimizeDataAccessPrompt()
	s.registerPrompt(optimizeAccess)

	// Coordination Engine prompts (if CE enabled)
	if s.ceClient != nil {
		predictAndPrevent := prompts.NewPredictAndPreventPrompt()
		s.registerPrompt(predictAndPrevent)

		correlateIncidents := prompts.NewCorrelateIncidentsPrompt()
		s.registerPrompt(correlateIncidents)
	} else {
		log.Printf("Skipping Coordination Engine prompts (not enabled)")
	}

	log.Printf("Total prompts registered: %d", len(s.prompts))
	return nil
}

// registerPrompt registers a prompt with both our internal map and the MCP SDK
func (s *MCPServer) registerPrompt(prompt prompts.Prompt) {
	// Store in our internal map
	s.prompts[prompt.Name()] = prompt

	// Create handler function that wraps our prompt's Execute method
	handler := func(ctx context.Context, req *mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
		// Convert request arguments to map
		args := make(map[string]interface{})
		if req.Params.Arguments != nil {
			for k, v := range req.Params.Arguments {
				args[k] = v
			}
		}

		// Execute the prompt
		return prompt.Execute(ctx, args)
	}

	// Register with MCP SDK
	// TODO: Check MCP SDK documentation for correct prompt registration method
	// The AddPrompt function may not exist in the current SDK version
	_ = handler // Suppress unused variable warning until SDK registration is implemented
	// mcp.AddPrompt(s.mcpServer, prompt.GetPrompt(), handler)

	log.Printf("Registered prompt: %s - %s", prompt.Name(), prompt.Description())
}

// GetTools returns all registered tools
func (s *MCPServer) GetTools() map[string]Tool {
	return s.tools
}

// GetResources returns all registered resources
func (s *MCPServer) GetResources() map[string]interface{} {
	return s.resources
}

// Start begins serving MCP requests using the configured transport
// As of 2025-12-17, only HTTP/SSE transport is supported (stdio DEPRECATED)
func (s *MCPServer) Start(ctx context.Context) error {
	switch s.config.Transport {
	case TransportHTTP:
		return s.startHTTPTransport(ctx)
	case TransportStdio:
		// stdio transport DEPRECATED - return error
		return s.startStdioTransport(ctx)
	default:
		return fmt.Errorf("unsupported transport: %s (only 'http' is supported)", s.config.Transport)
	}
}

// startHTTPTransport starts the server with HTTP/SSE transport
func (s *MCPServer) startHTTPTransport(ctx context.Context) error {
	addr := s.config.GetHTTPAddr()
	log.Printf("Starting HTTP transport on %s", addr)

	// Create the MCP SSE handler (handles SSE transport for OpenShift Lightspeed compatibility)
	// OpenShift Lightspeed expects SSE transport at the root endpoint
	// Reference: https://github.com/openshift/lightspeed-service/
	mcpHandler := mcp.NewSSEHandler(func(req *http.Request) *mcp.Server {
		return s.mcpServer
	}, nil)

	// Create custom handler that routes to either MCP or health endpoints
	mainHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Route specific endpoints to their handlers
		switch {
		case r.URL.Path == "/health":
			w.WriteHeader(http.StatusOK)
			if _, err := fmt.Fprint(w, "OK"); err != nil {
				log.Printf("Error writing health response: %v", err)
			}
			return
		case r.URL.Path == "/ready":
			w.WriteHeader(http.StatusOK)
			if _, err := fmt.Fprint(w, "READY"); err != nil {
				log.Printf("Error writing ready response: %v", err)
			}
			return
		case r.URL.Path == "/metrics":
			// TODO: Implement Prometheus metrics in Phase 3
			w.WriteHeader(http.StatusOK)
			if _, err := fmt.Fprint(w, "# Metrics endpoint (Phase 3)\n"); err != nil {
				log.Printf("Error writing metrics response: %v", err)
			}
			return
		case r.URL.Path == "/cache/stats":
			s.handleCacheStats(w, r)
			return
		case r.URL.Path == "/mcp/capabilities":
			s.handleMCPCapabilities(w, r)
			return
		case r.URL.Path == "/mcp/info":
			s.handleMCPInfo(w, r)
			return
		case r.URL.Path == "/mcp/tools":
			s.handleListTools(w, r)
			return
		case r.URL.Path == "/mcp/resources":
			s.handleListResources(w, r)
			return
		case r.URL.Path == "/mcp/prompts":
			s.handleListPrompts(w, r)
			return
		// Session management endpoints (REST API)
		case r.URL.Path == "/mcp/session":
			s.handleSession(w, r)
			return
		case r.URL.Path == "/mcp/sessions/stats":
			s.handleSessionStats(w, r)
			return
		case strings.HasPrefix(r.URL.Path, "/mcp/session/"):
			s.handleSessionByID(w, r)
			return
		// Tool invocation endpoints (REST API with session support)
		case strings.HasPrefix(r.URL.Path, "/mcp/tools/") && strings.HasSuffix(r.URL.Path, "/call"):
			s.handleToolCall(w, r)
			return
		// Resource read endpoint (REST API with session support)
		case strings.HasPrefix(r.URL.Path, "/mcp/resources/") && strings.HasSuffix(r.URL.Path, "/read"):
			s.handleResourceRead(w, r)
			return
		default:
			// All other paths go to MCP handler (including root "/")
			// This supports GET (SSE) and POST (messages) for MCP protocol
			log.Printf("Routing %s %s to MCP handler", r.Method, r.URL.Path)
			mcpHandler.ServeHTTP(w, r)
		}
	})

	s.httpServer = &http.Server{
		Addr:    addr,
		Handler: mainHandler,
	}

	// Start server in goroutine
	errChan := make(chan error, 1)
	go func() {
		log.Printf("MCP Server listening on %s", addr)
		if err := s.httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			errChan <- fmt.Errorf("HTTP server error: %w", err)
		}
	}()

	// Wait for context cancellation or error
	select {
	case <-ctx.Done():
		log.Println("Shutting down HTTP server...")
		// Add timeout to graceful shutdown
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
		defer cancel()
		return s.httpServer.Shutdown(shutdownCtx)
	case err := <-errChan:
		return err
	}
}

// startStdioTransport is DEPRECATED as of 2025-12-17
// stdio transport is no longer supported - use HTTP/SSE transport instead
func (s *MCPServer) startStdioTransport(ctx context.Context) error {
	log.Println("ERROR: stdio transport is DEPRECATED as of 2025-12-17")
	log.Println("Please use HTTP/SSE transport instead:")
	log.Println("  MCP_TRANSPORT=http ./mcp-server")
	log.Println("")
	log.Println("Rationale for deprecation:")
	log.Println("  - Primary use case is OpenShift Lightspeed integration via HTTP/SSE")
	log.Println("  - Local development works fine with HTTP transport")
	log.Println("  - stdio was never fully implemented (stub only)")
	log.Println("  - Reduces codebase complexity and maintenance burden")

	return fmt.Errorf("stdio transport is DEPRECATED - use HTTP transport (MCP_TRANSPORT=http)")
}

// handleMCPCapabilities returns MCP server capabilities per MCP specification
// GET /mcp/capabilities - Returns server name, version, and capabilities
// Note: /mcp is reserved for SSE transport (OpenShift Lightspeed integration)
// Reference: https://spec.modelcontextprotocol.io/
func (s *MCPServer) handleMCPCapabilities(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed - use GET", http.StatusMethodNotAllowed)
		return
	}

	// Build capabilities response per MCP specification
	response := map[string]interface{}{
		"name":    s.config.Name,
		"version": s.config.Version,
		"capabilities": map[string]bool{
			"tools":     len(s.tools) > 0,
			"resources": len(s.resources) > 0,
			"prompts":   len(s.prompts) > 0,
		},
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing MCP capabilities response: %v", err)
	}
}

// handleMCPInfo returns server info
func (s *MCPServer) handleMCPInfo(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if _, err := fmt.Fprintf(w, `{"name":"%s","version":"%s","transport":"http/sse","tools_count":%d,"resources_count":%d}`,
		s.config.Name, s.config.Version, len(s.tools), len(s.resources)); err != nil {
		log.Printf("Error writing MCP info response: %v", err)
	}
}

// handleListTools returns all available tools
func (s *MCPServer) handleListTools(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Build tools list response
	type ToolInfo struct {
		Name        string                 `json:"name"`
		Description string                 `json:"description"`
		InputSchema map[string]interface{} `json:"input_schema"`
	}

	toolsList := []ToolInfo{}
	for _, tool := range s.tools {
		// No type assertion needed - tools map is now typed as map[string]Tool
		toolsList = append(toolsList, ToolInfo{
			Name:        tool.Name(),
			Description: tool.Description(),
			InputSchema: tool.InputSchema(),
		})
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"tools": toolsList,
		"count": len(toolsList),
	}

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing JSON response: %v", err)
	}
}

// handleClusterHealthTool executes the cluster health tool
func (s *MCPServer) handleClusterHealthTool(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed - use POST", http.StatusMethodNotAllowed)
		return
	}

	// Get the tool
	tool, ok := s.tools["get-cluster-health"].(*tools.ClusterHealthTool)
	if !ok {
		http.Error(w, "Tool not found", http.StatusNotFound)
		return
	}

	// Parse request body for arguments
	var args map[string]interface{}
	if r.Body != nil {
		defer func() {
			if err := r.Body.Close(); err != nil {
				log.Printf("Error closing request body: %v", err)
			}
		}()
		decoder := json.NewDecoder(r.Body)
		if err := decoder.Decode(&args); err != nil {
			// If no body or invalid JSON, use empty args
			args = make(map[string]interface{})
		}
	} else {
		args = make(map[string]interface{})
	}

	// Execute the tool
	ctx := r.Context()
	result, err := tool.Execute(ctx, args)
	if err != nil {
		http.Error(w, fmt.Sprintf("Tool execution failed: %v", err), http.StatusInternalServerError)
		return
	}

	// Return result
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"success": true,
		"result":  result,
	}

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing JSON response: %v", err)
	}
}

// handleListPodsTool executes the list-pods tool
func (s *MCPServer) handleListPodsTool(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed - use POST", http.StatusMethodNotAllowed)
		return
	}

	// Get the tool
	tool, ok := s.tools["list-pods"].(*tools.ListPodsTool)
	if !ok {
		http.Error(w, "Tool not found", http.StatusNotFound)
		return
	}

	// Parse request body for arguments
	var args map[string]interface{}
	if r.Body != nil {
		defer func() {
			if err := r.Body.Close(); err != nil {
				log.Printf("Error closing request body: %v", err)
			}
		}()
		decoder := json.NewDecoder(r.Body)
		if err := decoder.Decode(&args); err != nil {
			// If no body or invalid JSON, use empty args
			args = make(map[string]interface{})
		}
	} else {
		args = make(map[string]interface{})
	}

	// Execute the tool
	ctx := r.Context()
	result, err := tool.Execute(ctx, args)
	if err != nil {
		http.Error(w, fmt.Sprintf("Tool execution failed: %v", err), http.StatusInternalServerError)
		return
	}

	// Return result
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"success": true,
		"result":  result,
	}

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing JSON response: %v", err)
	}
}

// handleCacheStats returns cache statistics
func (s *MCPServer) handleCacheStats(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed - use GET", http.StatusMethodNotAllowed)
		return
	}

	stats := s.cache.GetStatistics()

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	if err := writeJSON(w, stats); err != nil {
		log.Printf("Error writing JSON response: %v", err)
	}
}

// handleListResources returns all available resources
func (s *MCPServer) handleListResources(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Build resources list response
	type ResourceInfo struct {
		URI         string `json:"uri"`
		Name        string `json:"name"`
		Description string `json:"description"`
		MimeType    string `json:"mime_type"`
	}

	resourcesList := []ResourceInfo{}
	for _, resource := range s.resources {
		switch r := resource.(type) {
		case *resources.ClusterHealthResource:
			resourcesList = append(resourcesList, ResourceInfo{
				URI:         r.URI(),
				Name:        r.Name(),
				Description: r.Description(),
				MimeType:    r.MimeType(),
			})
		case *resources.NodesResource:
			resourcesList = append(resourcesList, ResourceInfo{
				URI:         r.URI(),
				Name:        r.Name(),
				Description: r.Description(),
				MimeType:    r.MimeType(),
			})
		case *resources.IncidentsResource:
			resourcesList = append(resourcesList, ResourceInfo{
				URI:         r.URI(),
				Name:        r.Name(),
				Description: r.Description(),
				MimeType:    r.MimeType(),
			})
		case *resources.RemediationHistoryResource:
			resourcesList = append(resourcesList, ResourceInfo{
				URI:         r.URI(),
				Name:        r.Name(),
				Description: r.Description(),
				MimeType:    r.MimeType(),
			})
		}
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"resources": resourcesList,
		"count":     len(resourcesList),
	}

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing JSON response: %v", err)
	}
}

// handleListPrompts returns all available prompts
func (s *MCPServer) handleListPrompts(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Build prompts list response
	type PromptInfo struct {
		Name        string   `json:"name"`
		Description string   `json:"description"`
		Arguments   []string `json:"arguments,omitempty"`
	}

	promptsList := []PromptInfo{}
	for _, prompt := range s.prompts {
		switch p := prompt.(type) {
		case *prompts.DiagnoseClusterPrompt:
			promptsList = append(promptsList, PromptInfo{
				Name:        p.Name(),
				Description: p.Description(),
				Arguments:   []string{"severity"},
			})
		case *prompts.InvestigatePodsPrompt:
			promptsList = append(promptsList, PromptInfo{
				Name:        p.Name(),
				Description: p.Description(),
				Arguments:   []string{"namespace", "pod_name"},
			})
		case *prompts.CheckAnomaliesPrompt:
			promptsList = append(promptsList, PromptInfo{
				Name:        p.Name(),
				Description: p.Description(),
				Arguments:   []string{"namespace", "timeframe"},
			})
		case *prompts.OptimizeDataAccessPrompt:
			promptsList = append(promptsList, PromptInfo{
				Name:        p.Name(),
				Description: p.Description(),
			})
		case *prompts.PredictAndPreventPrompt:
			promptsList = append(promptsList, PromptInfo{
				Name:        p.Name(),
				Description: p.Description(),
				Arguments:   []string{"timeframe", "confidence_threshold"},
			})
		case *prompts.CorrelateIncidentsPrompt:
			promptsList = append(promptsList, PromptInfo{
				Name:        p.Name(),
				Description: p.Description(),
				Arguments:   []string{"time_window", "severity"},
			})
		}
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"prompts": promptsList,
		"count":   len(promptsList),
	}

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing JSON response: %v", err)
	}
}

// writeJSON is a helper to write JSON responses
func writeJSON(w http.ResponseWriter, data interface{}) error {
	encoder := json.NewEncoder(w)
	encoder.SetIndent("", "  ")
	return encoder.Encode(data)
}

// Stop gracefully shuts down the server
func (s *MCPServer) Stop() error {
	// Stop session manager cleanup goroutine
	if s.sessionManager != nil {
		s.sessionManager.Stop()
	}
	if s.httpServer != nil {
		log.Println("Stopping HTTP server...")
		// Add timeout to graceful shutdown
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
		defer cancel()
		return s.httpServer.Shutdown(shutdownCtx)
	}
	return nil
}

// handleSession handles session creation and info
// POST /mcp/session - Create new session
// GET /mcp/session - Get session info (requires sessionid query param or header)
func (s *MCPServer) handleSession(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		// Create new session
		s.handleCreateSession(w, r)
	case http.MethodGet:
		// Get session info (requires sessionid)
		sessionID := s.getSessionID(r)
		if sessionID == "" {
			writeJSONError(w, http.StatusBadRequest, "sessionid must be provided as query parameter or X-MCP-Session-ID header")
			return
		}
		info := s.sessionManager.GetSessionInfo(sessionID)
		if info == nil {
			writeJSONError(w, http.StatusNotFound, "session not found or expired")
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		if err := writeJSON(w, info); err != nil {
			log.Printf("Error writing session info: %v", err)
		}
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

// handleCreateSession creates a new session
func (s *MCPServer) handleCreateSession(w http.ResponseWriter, r *http.Request) {
	// Parse optional metadata from request body
	var metadata map[string]interface{}
	if r.Body != nil {
		defer func() {
			if err := r.Body.Close(); err != nil {
				log.Printf("Error closing request body: %v", err)
			}
		}()
		decoder := json.NewDecoder(r.Body)
		if err := decoder.Decode(&metadata); err != nil {
			// If no body or invalid JSON, use empty metadata
			metadata = make(map[string]interface{})
		}
	}

	// Create session
	session, err := s.sessionManager.CreateSession(metadata)
	if err != nil {
		writeJSONError(w, http.StatusServiceUnavailable, err.Error())
		return
	}

	// Return session info
	response := map[string]interface{}{
		"session_id":  session.ID,
		"created_at":  session.CreatedAt.Format(time.RFC3339),
		"expires_at":  session.ExpiresAt.Format(time.RFC3339),
		"ttl_seconds": int(time.Until(session.ExpiresAt).Seconds()),
		"message":     "Session created successfully. Include sessionid in subsequent requests.",
		"usage": map[string]string{
			"query_param": fmt.Sprintf("?sessionid=%s", session.ID),
			"header":      fmt.Sprintf("X-MCP-Session-ID: %s", session.ID),
		},
	}

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("X-MCP-Session-ID", session.ID)
	w.WriteHeader(http.StatusCreated)
	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing session response: %v", err)
	}

	log.Printf("Created session: %s", session.ID)
}

// handleSessionByID handles operations on a specific session
// GET /mcp/session/{sessionid} - Get session info
// DELETE /mcp/session/{sessionid} - Delete session
func (s *MCPServer) handleSessionByID(w http.ResponseWriter, r *http.Request) {
	// Extract session ID from path: /mcp/session/{sessionid}
	path := strings.TrimPrefix(r.URL.Path, "/mcp/session/")
	sessionID := strings.TrimSuffix(path, "/")

	if sessionID == "" {
		writeJSONError(w, http.StatusBadRequest, "session ID required in path")
		return
	}

	switch r.Method {
	case http.MethodGet:
		info := s.sessionManager.GetSessionInfo(sessionID)
		if info == nil {
			writeJSONError(w, http.StatusNotFound, "session not found or expired")
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		if err := writeJSON(w, info); err != nil {
			log.Printf("Error writing session info: %v", err)
		}
	case http.MethodDelete:
		if s.sessionManager.DeleteSession(sessionID) {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)
			if err := writeJSON(w, map[string]string{"message": "session deleted"}); err != nil {
				log.Printf("Error writing delete response: %v", err)
			}
		} else {
			writeJSONError(w, http.StatusNotFound, "session not found")
		}
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

// handleSessionStats returns session manager statistics
func (s *MCPServer) handleSessionStats(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	stats := s.sessionManager.GetStats()
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := writeJSON(w, stats); err != nil {
		log.Printf("Error writing session stats: %v", err)
	}
}

// handleToolCall handles tool invocation via REST API
// POST /mcp/tools/{toolname}/call
// Requires sessionid query parameter or X-MCP-Session-ID header
func (s *MCPServer) handleToolCall(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed - use POST", http.StatusMethodNotAllowed)
		return
	}

	// Validate session
	sessionID := s.getSessionID(r)
	if sessionID == "" {
		writeJSONError(w, http.StatusBadRequest,
			"sessionid must be provided. Create a session first via POST /mcp/session, then include sessionid as query parameter or X-MCP-Session-ID header")
		return
	}

	if !s.sessionManager.TouchSession(sessionID) {
		writeJSONError(w, http.StatusUnauthorized, "invalid or expired session. Create a new session via POST /mcp/session")
		return
	}

	// Extract tool name from path: /mcp/tools/{toolname}/call
	path := strings.TrimPrefix(r.URL.Path, "/mcp/tools/")
	toolName := strings.TrimSuffix(path, "/call")

	if toolName == "" {
		writeJSONError(w, http.StatusBadRequest, "tool name required in path")
		return
	}

	// Get the tool - no type assertion needed since tools map is now typed as map[string]Tool
	tool, exists := s.tools[toolName]
	if !exists {
		writeJSONError(w, http.StatusNotFound, fmt.Sprintf("tool '%s' not found", toolName))
		return
	}

	// Parse request body for arguments
	var args map[string]interface{}
	if r.Body != nil {
		defer func() {
			if err := r.Body.Close(); err != nil {
				log.Printf("Error closing request body: %v", err)
			}
		}()
		decoder := json.NewDecoder(r.Body)
		if err := decoder.Decode(&args); err != nil {
			// If no body or invalid JSON, use empty args
			args = make(map[string]interface{})
		}
	} else {
		args = make(map[string]interface{})
	}

	ctx := r.Context()
	result, err := tool.Execute(ctx, args)
	if err != nil {
		writeJSONError(w, http.StatusInternalServerError, fmt.Sprintf("tool execution failed: %v", err))
		return
	}

	// Return result
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("X-MCP-Session-ID", sessionID)
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"success":    true,
		"tool":       toolName,
		"session_id": sessionID,
		"result":     result,
	}

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing tool response: %v", err)
	}

	log.Printf("Tool '%s' executed successfully (session: %s)", toolName, sessionID)
}

// handleResourceRead handles resource read via REST API
// POST /mcp/resources/{uri}/read
// Requires sessionid query parameter or X-MCP-Session-ID header
func (s *MCPServer) handleResourceRead(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost && r.Method != http.MethodGet {
		http.Error(w, "Method not allowed - use GET or POST", http.StatusMethodNotAllowed)
		return
	}

	// Validate session
	sessionID := s.getSessionID(r)
	if sessionID == "" {
		writeJSONError(w, http.StatusBadRequest,
			"sessionid must be provided. Create a session first via POST /mcp/session, then include sessionid as query parameter or X-MCP-Session-ID header")
		return
	}

	if !s.sessionManager.TouchSession(sessionID) {
		writeJSONError(w, http.StatusUnauthorized, "invalid or expired session. Create a new session via POST /mcp/session")
		return
	}

	// Extract resource URI from path: /mcp/resources/{uri}/read
	// The URI is URL-encoded in the path
	path := strings.TrimPrefix(r.URL.Path, "/mcp/resources/")
	resourceURI := strings.TrimSuffix(path, "/read")

	if resourceURI == "" {
		writeJSONError(w, http.StatusBadRequest, "resource URI required in path")
		return
	}

	// URL decode the resource URI (e.g., cluster%3A%2F%2Fhealth -> cluster://health)
	// The URI should be provided URL-encoded in the path

	// Find the resource
	resourceInterface, exists := s.resources[resourceURI]
	if !exists {
		// Try with cluster:// prefix if not found
		if !strings.Contains(resourceURI, "://") {
			resourceURI = "cluster://" + resourceURI
			resourceInterface, exists = s.resources[resourceURI]
		}
		if !exists {
			writeJSONError(w, http.StatusNotFound, fmt.Sprintf("resource '%s' not found", resourceURI))
			return
		}
	}

	// Execute the resource read
	ctx := r.Context()
	var result interface{}
	var err error

	switch res := resourceInterface.(type) {
	case *resources.ClusterHealthResource:
		result, err = res.Read(ctx)
	case *resources.NodesResource:
		result, err = res.Read(ctx)
	case *resources.IncidentsResource:
		result, err = res.Read(ctx)
	case *resources.RemediationHistoryResource:
		result, err = res.Read(ctx)
	default:
		writeJSONError(w, http.StatusInternalServerError, "resource type not supported")
		return
	}

	if err != nil {
		writeJSONError(w, http.StatusInternalServerError, fmt.Sprintf("resource read failed: %v", err))
		return
	}

	// Return result
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("X-MCP-Session-ID", sessionID)
	w.WriteHeader(http.StatusOK)

	response := map[string]interface{}{
		"success":    true,
		"uri":        resourceURI,
		"session_id": sessionID,
		"content":    result,
	}

	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing resource response: %v", err)
	}

	log.Printf("Resource '%s' read successfully (session: %s)", resourceURI, sessionID)
}

// getSessionID extracts session ID from query parameter or header
func (s *MCPServer) getSessionID(r *http.Request) string {
	// Check query parameter first (MCP standard)
	sessionID := r.URL.Query().Get("sessionid")
	if sessionID != "" {
		return sessionID
	}

	// Also check the common header variant
	sessionID = r.Header.Get("X-MCP-Session-ID")
	if sessionID != "" {
		return sessionID
	}

	// Check Mcp-Session-Id header (used by StreamableHTTPHandler)
	sessionID = r.Header.Get("Mcp-Session-Id")
	return sessionID
}

// writeJSONError writes a JSON error response
func writeJSONError(w http.ResponseWriter, statusCode int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	response := map[string]interface{}{
		"success": false,
		"error":   message,
	}
	if err := writeJSON(w, response); err != nil {
		log.Printf("Error writing error response: %v", err)
	}
}
