package resources

import (
	"context"
	"encoding/json"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

func TestNodesResource_URI(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewNodesResource(k8sClient, memCache)
	assert.Equal(t, "cluster://nodes", resource.URI())
}

func TestNodesResource_Name(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewNodesResource(k8sClient, memCache)
	assert.Equal(t, "Cluster Nodes", resource.Name())
}

func TestNodesResource_Description(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewNodesResource(k8sClient, memCache)
	assert.Contains(t, resource.Description(), "Information about all nodes")
}

func TestNodesResource_MimeType(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewNodesResource(k8sClient, memCache)
	assert.Equal(t, "application/json", resource.MimeType())
}

func TestNodesResource_Read(t *testing.T) {
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client (requires cluster access): %v", err)
	}

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewNodesResource(k8sClient, memCache)

	ctx := context.Background()
	data, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data)

	// Verify it's valid JSON
	var nodesData NodesData
	err = json.Unmarshal([]byte(data), &nodesData)
	require.NoError(t, err)

	// Verify required fields
	assert.NotEmpty(t, nodesData.Timestamp)
	assert.GreaterOrEqual(t, nodesData.TotalNodes, 0)
	assert.GreaterOrEqual(t, nodesData.ReadyNodes, 0)
	assert.LessOrEqual(t, nodesData.ReadyNodes, nodesData.TotalNodes)

	// If there are nodes, verify their structure
	if len(nodesData.Nodes) > 0 {
		node := nodesData.Nodes[0]
		assert.NotEmpty(t, node.Name)
		assert.NotEmpty(t, node.Status)
		assert.NotEmpty(t, node.Version)
		assert.NotEmpty(t, node.Capacity.CPU)
		assert.NotEmpty(t, node.Capacity.Memory)
		assert.NotEmpty(t, node.Capacity.Pods)
		assert.NotEmpty(t, node.Allocatable.CPU)
		assert.NotEmpty(t, node.Allocatable.Memory)
		assert.NotNil(t, node.Roles)
		assert.NotEmpty(t, node.Age)

		t.Logf("Node: %s", node.Name)
		t.Logf("  Status: %s", node.Status)
		t.Logf("  Roles: %v", node.Roles)
		t.Logf("  Version: %s", node.Version)
		t.Logf("  Capacity: CPU=%s, Memory=%s, Pods=%s",
			node.Capacity.CPU, node.Capacity.Memory, node.Capacity.Pods)
		t.Logf("  Age: %s", node.Age)
	}

	t.Logf("Total nodes: %d, Ready: %d", nodesData.TotalNodes, nodesData.ReadyNodes)
}

func TestNodesResource_CacheUsage(t *testing.T) {
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client (requires cluster access): %v", err)
	}

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewNodesResource(k8sClient, memCache)

	ctx := context.Background()

	// First read - should fetch from K8s API
	data1, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data1)

	// Second read - should come from cache
	data2, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data2)

	// Should be identical (from cache)
	assert.Equal(t, data1, data2)

	// Verify cache statistics
	stats := memCache.GetStatistics()
	assert.GreaterOrEqual(t, stats.Entries, 1, "Should have at least 1 cache entry")
	assert.GreaterOrEqual(t, stats.Hits, int64(1), "Should have at least 1 cache hit")
}

func TestFormatMemory(t *testing.T) {
	tests := []struct {
		name     string
		bytes    int64
		expected string
	}{
		{"bytes", 512, "512B"},
		{"kilobytes", 2048, "2.0Ki"},
		{"megabytes", 1048576, "1.0Mi"},
		{"gigabytes", 1073741824, "1.0Gi"},
		{"terabytes", 1099511627776, "1.0Ti"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := formatMemory(tt.bytes)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestFormatAge(t *testing.T) {
	now := time.Now()

	tests := []struct {
		name     string
		time     time.Time
		expected string
	}{
		{"minutes", now.Add(-30 * time.Minute), "30m"},
		{"hours", now.Add(-5 * time.Hour), "5h"},
		{"days and hours", now.Add(-25 * time.Hour), "1d1h"},
		{"days", now.Add(-48 * time.Hour), "2d0h"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := formatAge(tt.time)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestGetNodeRoles(t *testing.T) {
	tests := []struct {
		name     string
		labels   map[string]string
		expected []string
	}{
		{
			name: "control-plane node",
			labels: map[string]string{
				"node-role.kubernetes.io/control-plane": "",
			},
			expected: []string{"control-plane"},
		},
		{
			name: "worker node",
			labels: map[string]string{
				"node-role.kubernetes.io/worker": "",
			},
			expected: []string{"worker"},
		},
		{
			name: "infra node",
			labels: map[string]string{
				"node-role.kubernetes.io/infra": "",
			},
			expected: []string{"infra"},
		},
		{
			name:     "default worker",
			labels:   map[string]string{},
			expected: []string{"worker"},
		},
		{
			name: "master node (legacy)",
			labels: map[string]string{
				"node-role.kubernetes.io/master": "",
			},
			expected: []string{"control-plane"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			roles := getNodeRoles(tt.labels)
			assert.ElementsMatch(t, tt.expected, roles)
		})
	}
}

func TestIsImportantLabel(t *testing.T) {
	tests := []struct {
		name     string
		label    string
		expected bool
	}{
		{"node role", "node-role.kubernetes.io/worker", true},
		{"instance type", "node.kubernetes.io/instance-type", true},
		{"zone", "topology.kubernetes.io/zone", true},
		{"region", "topology.kubernetes.io/region", true},
		{"architecture", "kubernetes.io/arch", true},
		{"os", "kubernetes.io/os", true},
		{"random label", "app.kubernetes.io/name", false},
		{"custom label", "mylabel", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := isImportantLabel(tt.label)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestNodesResource_JSONStructure(t *testing.T) {
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client (requires cluster access): %v", err)
	}

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewNodesResource(k8sClient, memCache)

	ctx := context.Background()
	data, err := resource.Read(ctx)
	require.NoError(t, err)

	// Parse and verify JSON structure
	var nodesData NodesData
	err = json.Unmarshal([]byte(data), &nodesData)
	require.NoError(t, err)

	// Verify it can be re-marshaled
	_, err = json.MarshalIndent(nodesData, "", "  ")
	require.NoError(t, err)

	// Verify timestamp format (RFC3339)
	_, err = time.Parse(time.RFC3339, nodesData.Timestamp)
	require.NoError(t, err, "Timestamp should be in RFC3339 format")
}
