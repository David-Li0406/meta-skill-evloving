package resources

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// ClusterHealthResource provides the cluster://health MCP resource
type ClusterHealthResource struct {
	k8sClient *clients.K8sClient
	ceClient  *clients.CoordinationEngineClient
	cache     *cache.MemoryCache
}

// NewClusterHealthResource creates a new cluster health resource
func NewClusterHealthResource(k8sClient *clients.K8sClient, ceClient *clients.CoordinationEngineClient, cache *cache.MemoryCache) *ClusterHealthResource {
	return &ClusterHealthResource{
		k8sClient: k8sClient,
		ceClient:  ceClient,
		cache:     cache,
	}
}

// URI returns the resource URI
func (r *ClusterHealthResource) URI() string {
	return "cluster://health"
}

// Name returns the resource name
func (r *ClusterHealthResource) Name() string {
	return "Cluster Health"
}

// Description returns the resource description
func (r *ClusterHealthResource) Description() string {
	return "Real-time cluster health snapshot including node status, pod health, resource utilization, and overall cluster state"
}

// MimeType returns the MIME type of the resource
func (r *ClusterHealthResource) MimeType() string {
	return "application/json"
}

// ClusterHealthData represents the cluster health resource data
type ClusterHealthData struct {
	Status        string    `json:"status"`
	Timestamp     string    `json:"timestamp"`
	Source        string    `json:"source"`
	Nodes         NodeStats `json:"nodes"`
	Pods          PodStats  `json:"pods"`
	ResourceUsage struct {
		CPU    ResourceUsageDetail `json:"cpu"`
		Memory ResourceUsageDetail `json:"memory"`
	} `json:"resource_usage"`
	ActiveIssues int      `json:"active_issues"`
	Warnings     []string `json:"warnings,omitempty"`
	Message      string   `json:"message"`
}

// NodeStats represents node statistics
type NodeStats struct {
	Total    int `json:"total"`
	Ready    int `json:"ready"`
	NotReady int `json:"not_ready"`
}

// PodStats represents pod statistics
type PodStats struct {
	Total     int `json:"total"`
	Running   int `json:"running"`
	Pending   int `json:"pending"`
	Failed    int `json:"failed"`
	Succeeded int `json:"succeeded"`
}

// ResourceUsageDetail represents resource usage details
type ResourceUsageDetail struct {
	Used       string  `json:"used"`
	Total      string  `json:"total"`
	Percentage float64 `json:"percentage"`
}

// Read retrieves the cluster health resource
func (r *ClusterHealthResource) Read(ctx context.Context) (string, error) {
	// Check cache first (10 second TTL as per PRD)
	cacheKey := "resource:cluster:health"
	if cached, found := r.cache.Get(cacheKey); found {
		if data, ok := cached.(string); ok {
			return data, nil
		}
	}

	// Fetch from Kubernetes API
	// Note: Coordination Engine's ClusterStatus doesn't include detailed node/pod info
	// so we use K8s API directly for comprehensive health data
	data, err := r.fetchFromKubernetesAPI(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to fetch cluster health: %w", err)
	}
	data.Source = "kubernetes-api"

	return r.cacheAndReturn(cacheKey, data)
}

// fetchFromKubernetesAPI retrieves cluster health from Kubernetes API directly
func (r *ClusterHealthResource) fetchFromKubernetesAPI(ctx context.Context) (ClusterHealthData, error) {
	// Get cluster health from Kubernetes client
	health, err := r.k8sClient.GetClusterHealth(ctx)
	if err != nil {
		return ClusterHealthData{}, fmt.Errorf("failed to get cluster health: %w", err)
	}

	data := ClusterHealthData{
		Timestamp: time.Now().UTC().Format(time.RFC3339),
		Status:    health.Status,
		Message:   generateHealthMessage(health),
	}

	// Map health data
	data.Nodes.Total = health.Nodes.Total
	data.Nodes.Ready = health.Nodes.Ready
	data.Nodes.NotReady = health.Nodes.NotReady

	data.Pods.Total = health.Pods.Total
	data.Pods.Running = health.Pods.Running
	data.Pods.Pending = health.Pods.Pending
	data.Pods.Failed = health.Pods.Failed
	data.Pods.Succeeded = health.Pods.Succeeded

	// Note: Resource usage metrics would come from Prometheus integration (Phase 3)
	// For now, resource usage fields will be empty

	// Calculate active issues
	data.ActiveIssues = health.Nodes.NotReady + health.Pods.Failed + health.Pods.Pending

	// Add warnings for critical issues
	if health.Nodes.NotReady > 0 {
		data.Warnings = append(data.Warnings, fmt.Sprintf("%d nodes are not ready", health.Nodes.NotReady))
	}
	if health.Pods.Failed > 0 {
		data.Warnings = append(data.Warnings, fmt.Sprintf("%d pods have failed", health.Pods.Failed))
	}
	if health.Pods.Pending > 0 {
		data.Warnings = append(data.Warnings, fmt.Sprintf("%d pods are pending", health.Pods.Pending))
	}

	return data, nil
}

// cacheAndReturn caches the data and returns as JSON string
func (r *ClusterHealthResource) cacheAndReturn(cacheKey string, data ClusterHealthData) (string, error) {
	// Marshal to JSON
	jsonData, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal health data: %w", err)
	}

	jsonStr := string(jsonData)

	// Cache for 10 seconds (as per PRD)
	r.cache.SetWithTTL(cacheKey, jsonStr, 10*time.Second)

	return jsonStr, nil
}

// generateHealthMessage creates a human-readable health message
func generateHealthMessage(health *clients.ClusterHealth) string {
	switch health.Status {
	case "healthy":
		return fmt.Sprintf("Cluster is healthy: %d/%d nodes ready, %d/%d pods running",
			health.Nodes.Ready, health.Nodes.Total, health.Pods.Running, health.Pods.Total)
	case "degraded":
		issues := []string{}
		if health.Nodes.NotReady > 0 {
			issues = append(issues, fmt.Sprintf("%d nodes not ready", health.Nodes.NotReady))
		}
		if health.Pods.Failed > 0 {
			issues = append(issues, fmt.Sprintf("%d pods failed", health.Pods.Failed))
		}
		if health.Pods.Pending > 0 {
			issues = append(issues, fmt.Sprintf("%d pods pending", health.Pods.Pending))
		}
		if len(issues) > 0 {
			return fmt.Sprintf("Cluster is degraded: %v", issues)
		}
		return "Cluster is degraded"
	default:
		return "Cluster status: " + health.Status
	}
}
