package tools

import (
	"context"
	"testing"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
	"time"
)

func TestClusterHealthTool_Name(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	tool := NewClusterHealthTool(client, memCache)

	if tool.Name() != "get-cluster-health" {
		t.Errorf("Expected name 'get-cluster-health', got '%s'", tool.Name())
	}
}

func TestClusterHealthTool_Description(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	tool := NewClusterHealthTool(client, memCache)

	desc := tool.Description()
	if desc == "" {
		t.Error("Expected non-empty description")
	}
	if len(desc) < 10 {
		t.Errorf("Description seems too short: %s", desc)
	}
}

func TestClusterHealthTool_InputSchema(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	tool := NewClusterHealthTool(client, memCache)

	schema := tool.InputSchema()
	if schema == nil {
		t.Fatal("InputSchema returned nil")
	}

	// Check schema structure
	if schema["type"] != "object" {
		t.Error("Expected schema type to be 'object'")
	}

	properties, ok := schema["properties"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected properties to be a map")
	}

	// Check include_details property
	includeDetails, ok := properties["include_details"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected include_details property")
	}

	if includeDetails["type"] != "boolean" {
		t.Error("Expected include_details type to be boolean")
	}
}

func TestClusterHealthTool_Execute(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	tool := NewClusterHealthTool(client, memCache)
	ctx := context.Background()

	// Test with default args (include_details: true)
	result, err := tool.Execute(ctx, map[string]interface{}{})
	if err != nil {
		t.Fatalf("Execute failed: %v", err)
	}

	output, ok := result.(ClusterHealthOutput)
	if !ok {
		t.Fatal("Expected ClusterHealthOutput type")
	}

	// Validate output structure
	if output.Status == "" {
		t.Error("Expected status to be set")
	}

	if output.Nodes == nil {
		t.Error("Expected nodes to be present with default args")
	}

	if output.Pods == nil {
		t.Error("Expected pods to be present with default args")
	}

	if output.Message == "" {
		t.Error("Expected message to be set")
	}
}

func TestClusterHealthTool_Execute_WithoutDetails(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	tool := NewClusterHealthTool(client, memCache)
	ctx := context.Background()

	// Test with include_details: false
	result, err := tool.Execute(ctx, map[string]interface{}{
		"include_details": false,
	})
	if err != nil {
		t.Fatalf("Execute failed: %v", err)
	}

	output, ok := result.(ClusterHealthOutput)
	if !ok {
		t.Fatal("Expected ClusterHealthOutput type")
	}

	// Validate output structure
	if output.Status == "" {
		t.Error("Expected status to be set")
	}

	// Details should not be present
	if output.Nodes != nil {
		t.Error("Expected nodes to be nil when include_details is false")
	}

	if output.Pods != nil {
		t.Error("Expected pods to be nil when include_details is false")
	}
}

func TestClusterHealthTool_CacheUsage(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	tool := NewClusterHealthTool(client, memCache)
	ctx := context.Background()

	// First call - should populate cache
	_, err = tool.Execute(ctx, map[string]interface{}{
		"include_details": true,
	})
	if err != nil {
		t.Fatalf("First execute failed: %v", err)
	}

	// Check cache stats
	stats := memCache.GetStatistics()
	if stats.Entries == 0 {
		t.Error("Expected cache to have entries after first call")
	}

	initialMisses := stats.Misses

	// Second call - should use cache
	_, err = tool.Execute(ctx, map[string]interface{}{
		"include_details": true,
	})
	if err != nil {
		t.Fatalf("Second execute failed: %v", err)
	}

	// Verify cache was used (hits should increase or misses should stay same)
	stats = memCache.GetStatistics()
	if stats.Misses > initialMisses+1 {
		t.Error("Expected cache to be used on second call")
	}
}
