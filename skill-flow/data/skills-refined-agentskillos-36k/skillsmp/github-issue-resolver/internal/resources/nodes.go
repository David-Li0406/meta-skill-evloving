package resources

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	corev1 "k8s.io/api/core/v1"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// NodesResource provides the cluster://nodes MCP resource
type NodesResource struct {
	k8sClient *clients.K8sClient
	cache     *cache.MemoryCache
}

// NewNodesResource creates a new nodes resource
func NewNodesResource(k8sClient *clients.K8sClient, cache *cache.MemoryCache) *NodesResource {
	return &NodesResource{
		k8sClient: k8sClient,
		cache:     cache,
	}
}

// URI returns the resource URI
func (r *NodesResource) URI() string {
	return "cluster://nodes"
}

// Name returns the resource name
func (r *NodesResource) Name() string {
	return "Cluster Nodes"
}

// Description returns the resource description
func (r *NodesResource) Description() string {
	return "Information about all nodes in the cluster including status, roles, capacity, and resource allocations"
}

// MimeType returns the MIME type of the resource
func (r *NodesResource) MimeType() string {
	return "application/json"
}

// NodesData represents the nodes resource data
type NodesData struct {
	Timestamp  string     `json:"timestamp"`
	TotalNodes int        `json:"total_nodes"`
	ReadyNodes int        `json:"ready_nodes"`
	Nodes      []NodeInfo `json:"nodes"`
}

// NodeInfo represents information about a single node
type NodeInfo struct {
	Name        string            `json:"name"`
	Status      string            `json:"status"`
	Roles       []string          `json:"roles"`
	Version     string            `json:"version"`
	Capacity    NodeResources     `json:"capacity"`
	Allocatable NodeResources     `json:"allocatable"`
	Conditions  []NodeCondition   `json:"conditions,omitempty"`
	Labels      map[string]string `json:"labels,omitempty"`
	Age         string            `json:"age"`
}

// NodeResources represents node resource information
type NodeResources struct {
	CPU    string `json:"cpu"`
	Memory string `json:"memory"`
	Pods   string `json:"pods"`
}

// NodeCondition represents a node condition
type NodeCondition struct {
	Type    string `json:"type"`
	Status  string `json:"status"`
	Reason  string `json:"reason,omitempty"`
	Message string `json:"message,omitempty"`
}

// Read retrieves the nodes resource
func (r *NodesResource) Read(ctx context.Context) (string, error) {
	// Check cache first (30 second TTL as per PRD)
	cacheKey := "resource:cluster:nodes"
	if cached, found := r.cache.Get(cacheKey); found {
		if data, ok := cached.(string); ok {
			return data, nil
		}
	}

	// Fetch nodes from Kubernetes API
	nodeList, err := r.k8sClient.ListNodes(ctx)
	if err != nil {
		return "", fmt.Errorf("failed to list nodes: %w", err)
	}

	// Build nodes data
	data := NodesData{
		Timestamp:  time.Now().UTC().Format(time.RFC3339),
		TotalNodes: len(nodeList.Items),
		Nodes:      make([]NodeInfo, 0, len(nodeList.Items)),
	}

	// Process each node
	for _, node := range nodeList.Items {
		nodeInfo := NodeInfo{
			Name:    node.Name,
			Status:  getNodeStatus(&node),
			Roles:   getNodeRoles(node.Labels),
			Version: node.Status.NodeInfo.KubeletVersion,
			Age:     formatAge(node.CreationTimestamp.Time),
		}

		// Extract capacity
		nodeInfo.Capacity.CPU = node.Status.Capacity.Cpu().String()
		nodeInfo.Capacity.Memory = formatMemory(node.Status.Capacity.Memory().Value())
		nodeInfo.Capacity.Pods = node.Status.Capacity.Pods().String()

		// Extract allocatable
		nodeInfo.Allocatable.CPU = node.Status.Allocatable.Cpu().String()
		nodeInfo.Allocatable.Memory = formatMemory(node.Status.Allocatable.Memory().Value())
		nodeInfo.Allocatable.Pods = node.Status.Allocatable.Pods().String()

		// Extract conditions (limit to important ones)
		for _, condition := range node.Status.Conditions {
			if condition.Type == "Ready" || condition.Status != "False" {
				nodeInfo.Conditions = append(nodeInfo.Conditions, NodeCondition{
					Type:    string(condition.Type),
					Status:  string(condition.Status),
					Reason:  condition.Reason,
					Message: condition.Message,
				})
			}
		}

		// Extract selected labels
		nodeInfo.Labels = make(map[string]string)
		for key, value := range node.Labels {
			// Only include important labels to reduce payload size
			if isImportantLabel(key) {
				nodeInfo.Labels[key] = value
			}
		}

		// Count ready nodes
		if nodeInfo.Status == "Ready" {
			data.ReadyNodes++
		}

		data.Nodes = append(data.Nodes, nodeInfo)
	}

	// Marshal to JSON
	jsonData, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal nodes data: %w", err)
	}

	jsonStr := string(jsonData)

	// Cache for 30 seconds (as per PRD)
	r.cache.SetWithTTL(cacheKey, jsonStr, 30*time.Second)

	return jsonStr, nil
}

// getNodeStatus determines the overall status of a node
func getNodeStatus(node *corev1.Node) string {
	for _, condition := range node.Status.Conditions {
		if condition.Type == corev1.NodeReady {
			if condition.Status == corev1.ConditionTrue {
				return "Ready"
			}
			return "NotReady"
		}
	}
	return "Unknown"
}

// getNodeRoles extracts node roles from labels
func getNodeRoles(labels map[string]string) []string {
	roles := []string{}
	for key := range labels {
		switch key {
		case "node-role.kubernetes.io/master", "node-role.kubernetes.io/control-plane":
			roles = append(roles, "control-plane")
		case "node-role.kubernetes.io/worker":
			roles = append(roles, "worker")
		case "node-role.kubernetes.io/infra":
			roles = append(roles, "infra")
		}
	}
	if len(roles) == 0 {
		roles = append(roles, "worker") // Default role
	}
	return roles
}

// formatMemory formats bytes to human-readable format
func formatMemory(bytes int64) string {
	const unit = 1024
	if bytes < unit {
		return fmt.Sprintf("%dB", bytes)
	}
	div, exp := int64(unit), 0
	for n := bytes / unit; n >= unit; n /= unit {
		div *= unit
		exp++
	}
	units := []string{"Ki", "Mi", "Gi", "Ti", "Pi"}
	return fmt.Sprintf("%.1f%s", float64(bytes)/float64(div), units[exp])
}

// formatAge formats duration to human-readable age
func formatAge(t time.Time) string {
	duration := time.Since(t)
	days := int(duration.Hours() / 24)
	hours := int(duration.Hours()) % 24

	if days > 0 {
		return fmt.Sprintf("%dd%dh", days, hours)
	} else if hours > 0 {
		return fmt.Sprintf("%dh", hours)
	} else {
		minutes := int(duration.Minutes())
		return fmt.Sprintf("%dm", minutes)
	}
}

// isImportantLabel determines if a label should be included
func isImportantLabel(key string) bool {
	importantPrefixes := []string{
		"node-role.kubernetes.io/",
		"node.kubernetes.io/instance-type",
		"topology.kubernetes.io/zone",
		"topology.kubernetes.io/region",
		"kubernetes.io/arch",
		"kubernetes.io/os",
	}

	for _, prefix := range importantPrefixes {
		if len(key) >= len(prefix) && key[:len(prefix)] == prefix {
			return true
		}
	}
	return false
}
