package tools

import (
	"context"
	"testing"
	"time"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

func TestListPodsTool_Name(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	tool := NewListPodsTool(client)

	if tool.Name() != "list-pods" {
		t.Errorf("Expected name 'list-pods', got '%s'", tool.Name())
	}
}

func TestListPodsTool_Description(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	tool := NewListPodsTool(client)

	desc := tool.Description()
	if desc == "" {
		t.Error("Expected non-empty description")
	}
	if len(desc) < 10 {
		t.Errorf("Description seems too short: %s", desc)
	}
}

func TestListPodsTool_InputSchema(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	tool := NewListPodsTool(client)

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

	// Check required properties
	expectedProps := []string{"namespace", "label_selector", "field_selector", "limit"}
	for _, prop := range expectedProps {
		if _, exists := properties[prop]; !exists {
			t.Errorf("Expected property '%s' to exist", prop)
		}
	}
}

func TestListPodsTool_Execute_Default(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	tool := NewListPodsTool(client)
	ctx := context.Background()

	// Test with default args
	result, err := tool.Execute(ctx, map[string]interface{}{})
	if err != nil {
		t.Fatalf("Execute failed: %v", err)
	}

	output, ok := result.(ListPodsOutput)
	if !ok {
		t.Fatal("Expected ListPodsOutput type")
	}

	// Should have limited results (default limit 100)
	if output.Count > 100 {
		t.Errorf("Expected count <= 100 with default limit, got %d", output.Count)
	}

	// Should have pods array
	if output.Pods == nil {
		t.Error("Expected pods array to be initialized")
	}

	// Should have summary
	if output.Summary.Running < 0 {
		t.Error("Expected valid summary counts")
	}
}

func TestListPodsTool_Execute_WithNamespace(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	tool := NewListPodsTool(client)
	ctx := context.Background()

	// Test with specific namespace
	result, err := tool.Execute(ctx, map[string]interface{}{
		"namespace": "kube-system",
		"limit":     5,
	})
	if err != nil {
		t.Fatalf("Execute failed: %v", err)
	}

	output, ok := result.(ListPodsOutput)
	if !ok {
		t.Fatal("Expected ListPodsOutput type")
	}

	// Verify namespace filter was applied
	if output.Namespace != "kube-system" {
		t.Errorf("Expected namespace 'kube-system', got '%s'", output.Namespace)
	}

	// Verify limit was applied
	if output.Count > 5 {
		t.Errorf("Expected count <= 5, got %d", output.Count)
	}

	// Verify all returned pods are from the specified namespace
	for _, pod := range output.Pods {
		if pod.Namespace != "kube-system" {
			t.Errorf("Expected pod namespace 'kube-system', got '%s'", pod.Namespace)
		}
	}
}

func TestListPodsTool_Execute_WithFieldSelector(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	tool := NewListPodsTool(client)
	ctx := context.Background()

	// Test with field selector for Running pods
	result, err := tool.Execute(ctx, map[string]interface{}{
		"field_selector": "status.phase=Running",
		"limit":          10,
	})
	if err != nil {
		t.Fatalf("Execute failed: %v", err)
	}

	output, ok := result.(ListPodsOutput)
	if !ok {
		t.Fatal("Expected ListPodsOutput type")
	}

	// Verify field selector in output
	if output.Filters.FieldSelector != "status.phase=Running" {
		t.Errorf("Expected field selector to be recorded in output")
	}

	// Verify all returned pods are Running
	for _, pod := range output.Pods {
		if pod.Phase != "Running" {
			t.Errorf("Expected pod phase 'Running', got '%s'", pod.Phase)
		}
	}

	// Summary should only have running pods
	if output.Summary.Running != output.Count {
		t.Errorf("Expected all %d pods to be running, got %d", output.Count, output.Summary.Running)
	}
}

func TestListPodsTool_PodInfo(t *testing.T) {
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	tool := NewListPodsTool(client)
	ctx := context.Background()

	// Get a pod to verify structure
	result, err := tool.Execute(ctx, map[string]interface{}{
		"limit": 1,
	})
	if err != nil {
		t.Fatalf("Execute failed: %v", err)
	}

	output, ok := result.(ListPodsOutput)
	if !ok {
		t.Fatal("Expected ListPodsOutput type")
	}

	if len(output.Pods) == 0 {
		t.Skip("No pods available for testing")
	}

	pod := output.Pods[0]

	// Verify pod structure
	if pod.Name == "" {
		t.Error("Expected pod name to be set")
	}

	if pod.Namespace == "" {
		t.Error("Expected pod namespace to be set")
	}

	if pod.Status == "" {
		t.Error("Expected pod status to be set")
	}

	if pod.Ready == "" {
		t.Error("Expected pod ready status to be set")
	}

	if pod.Age == "" {
		t.Error("Expected pod age to be set")
	}

	// Containers should be populated
	if len(pod.Containers) == 0 {
		t.Error("Expected at least one container")
	}

	// Verify container structure
	container := pod.Containers[0]
	if container.Name == "" {
		t.Error("Expected container name to be set")
	}

	if container.Image == "" {
		t.Error("Expected container image to be set")
	}

	if container.State == "" {
		t.Error("Expected container state to be set")
	}
}

func TestFormatDuration(t *testing.T) {
	tests := []struct {
		duration time.Duration
		expected string
	}{
		{30 * time.Second, "30s"},
		{90 * time.Second, "1m"},
		{45 * time.Minute, "45m"},
		{2 * time.Hour, "2h"},
		{25 * time.Hour, "1d"},
		{3 * 24 * time.Hour, "3d"},
	}

	for _, tt := range tests {
		result := formatDuration(tt.duration)
		if result != tt.expected {
			t.Errorf("formatDuration(%v) = %s, expected %s", tt.duration, result, tt.expected)
		}
	}
}
