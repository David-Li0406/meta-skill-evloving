package tools

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// ClusterHealthTool provides cluster health information via MCP
type ClusterHealthTool struct {
	k8sClient *clients.K8sClient
	cache     *cache.MemoryCache
}

// NewClusterHealthTool creates a new cluster health tool
func NewClusterHealthTool(k8sClient *clients.K8sClient, memoryCache *cache.MemoryCache) *ClusterHealthTool {
	return &ClusterHealthTool{
		k8sClient: k8sClient,
		cache:     memoryCache,
	}
}

// Name returns the tool name for MCP registration
func (t *ClusterHealthTool) Name() string {
	return "get-cluster-health"
}

// Description returns the tool description for MCP
func (t *ClusterHealthTool) Description() string {
	return "Get comprehensive health summary of the OpenShift cluster including node status, pod health, and overall cluster state"
}

// InputSchema returns the JSON schema for tool inputs
func (t *ClusterHealthTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"include_details": map[string]interface{}{
				"type":        "boolean",
				"description": "Include detailed breakdown of pods and nodes",
				"default":     true,
			},
		},
		"required": []string{},
	}
}

// ClusterHealthInput represents the input parameters
type ClusterHealthInput struct {
	IncludeDetails bool `json:"include_details"`
}

// ClusterHealthOutput represents the tool output
type ClusterHealthOutput struct {
	Status  string                 `json:"status"`
	Nodes   *clients.NodeHealth    `json:"nodes,omitempty"`
	Pods    *clients.PodHealth     `json:"pods,omitempty"`
	Message string                 `json:"message,omitempty"`
	Details map[string]interface{} `json:"details,omitempty"`
}

// Execute runs the cluster health check
func (t *ClusterHealthTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments
	input := ClusterHealthInput{
		IncludeDetails: true, // Default to true
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Intentionally ignore error, use defaults if unmarshal fails
	}

	// Cache key based on detail level
	cacheKey := "cluster-health"
	if !input.IncludeDetails {
		cacheKey = "cluster-health-summary"
	}

	// Try to get from cache using GetOrSet pattern
	healthInterface, err := t.cache.GetOrSet(ctx, cacheKey, func() (interface{}, error) {
		return t.k8sClient.GetClusterHealth(ctx)
	})
	if err != nil {
		return nil, fmt.Errorf("failed to get cluster health: %w", err)
	}

	// Type assertion
	health, ok := healthInterface.(*clients.ClusterHealth)
	if !ok {
		return nil, fmt.Errorf("unexpected cache value type")
	}

	// Build output
	output := ClusterHealthOutput{
		Status: health.Status,
	}

	if input.IncludeDetails {
		output.Nodes = &health.Nodes
		output.Pods = &health.Pods

		// Add descriptive message
		output.Message = fmt.Sprintf(
			"Cluster is %s: %d/%d nodes ready, %d/%d pods running",
			health.Status,
			health.Nodes.Ready,
			health.Nodes.Total,
			health.Pods.Running,
			health.Pods.Total,
		)

		// Add additional details
		output.Details = map[string]interface{}{
			"node_ready_percentage": float64(health.Nodes.Ready) / float64(health.Nodes.Total) * 100,
			"pod_success_rate":      float64(health.Pods.Running) / float64(health.Pods.Total) * 100,
			"has_failed_pods":       health.Pods.Failed > 0,
			"has_pending_pods":      health.Pods.Pending > 0,
		}
	} else {
		output.Message = fmt.Sprintf("Cluster status: %s", health.Status)
	}

	return output, nil
}
