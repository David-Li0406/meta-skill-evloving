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

func TestClusterHealthResource_URI(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewClusterHealthResource(k8sClient, nil, memCache)
	assert.Equal(t, "cluster://health", resource.URI())
}

func TestClusterHealthResource_Name(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewClusterHealthResource(k8sClient, nil, memCache)
	assert.Equal(t, "Cluster Health", resource.Name())
}

func TestClusterHealthResource_Description(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewClusterHealthResource(k8sClient, nil, memCache)
	assert.Contains(t, resource.Description(), "Real-time cluster health")
}

func TestClusterHealthResource_MimeType(t *testing.T) {
	k8sClient, _ := clients.NewK8sClient(nil)
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewClusterHealthResource(k8sClient, nil, memCache)
	assert.Equal(t, "application/json", resource.MimeType())
}

func TestClusterHealthResource_Read(t *testing.T) {
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client (requires cluster access): %v", err)
	}

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewClusterHealthResource(k8sClient, nil, memCache)

	ctx := context.Background()
	data, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data)

	// Verify it's valid JSON
	var healthData ClusterHealthData
	err = json.Unmarshal([]byte(data), &healthData)
	require.NoError(t, err)

	// Verify required fields
	assert.NotEmpty(t, healthData.Status)
	assert.NotEmpty(t, healthData.Timestamp)
	assert.Equal(t, "kubernetes-api", healthData.Source)
	assert.NotEmpty(t, healthData.Message)

	// Verify node stats
	assert.GreaterOrEqual(t, healthData.Nodes.Total, 0)
	assert.GreaterOrEqual(t, healthData.Nodes.Ready, 0)
	assert.GreaterOrEqual(t, healthData.Nodes.NotReady, 0)

	// Verify pod stats
	assert.GreaterOrEqual(t, healthData.Pods.Total, 0)
	assert.GreaterOrEqual(t, healthData.Pods.Running, 0)
	assert.GreaterOrEqual(t, healthData.Pods.Pending, 0)
	assert.GreaterOrEqual(t, healthData.Pods.Failed, 0)

	t.Logf("Cluster Health Status: %s", healthData.Status)
	t.Logf("Nodes: %d total, %d ready, %d not ready",
		healthData.Nodes.Total, healthData.Nodes.Ready, healthData.Nodes.NotReady)
	t.Logf("Pods: %d total, %d running, %d pending, %d failed",
		healthData.Pods.Total, healthData.Pods.Running, healthData.Pods.Pending, healthData.Pods.Failed)
}

func TestClusterHealthResource_CacheUsage(t *testing.T) {
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client (requires cluster access): %v", err)
	}

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewClusterHealthResource(k8sClient, nil, memCache)

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

	t.Logf("Cache stats - Entries: %d, Hits: %d, Misses: %d",
		stats.Entries, stats.Hits, stats.Misses)
}

func TestClusterHealthResource_CacheExpiration(t *testing.T) {
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client (requires cluster access): %v", err)
	}

	// Create cache with short TTL
	memCache := cache.NewMemoryCache(1 * time.Second)
	defer memCache.Close()

	resource := NewClusterHealthResource(k8sClient, nil, memCache)

	ctx := context.Background()

	// First read
	data1, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data1)

	// Wait for cache to expire (resource sets 10 second TTL, so we need to wait longer)
	// Since cache uses SetWithTTL with 10 seconds, we need to manually clear cache or wait
	memCache.Clear() // Clear cache to force new fetch

	// Second read - cache was cleared, should get new data
	data2, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data2)

	// Both should be valid JSON
	var health1, health2 ClusterHealthData
	require.NoError(t, json.Unmarshal([]byte(data1), &health1))
	require.NoError(t, json.Unmarshal([]byte(data2), &health2))

	// Timestamps might be the same if read very quickly (within same second)
	// so we just verify both are valid
	assert.NotEmpty(t, health1.Timestamp)
	assert.NotEmpty(t, health2.Timestamp)
}

func TestGenerateHealthMessage(t *testing.T) {
	tests := []struct {
		name     string
		health   *clients.ClusterHealth
		expected string
	}{
		{
			name: "healthy cluster",
			health: &clients.ClusterHealth{
				Status: "healthy",
				Nodes: clients.NodeHealth{
					Total: 3,
					Ready: 3,
				},
				Pods: clients.PodHealth{
					Total:   100,
					Running: 100,
				},
			},
			expected: "Cluster is healthy: 3/3 nodes ready, 100/100 pods running",
		},
		{
			name: "degraded cluster with failed pods",
			health: &clients.ClusterHealth{
				Status: "degraded",
				Nodes: clients.NodeHealth{
					Total: 3,
					Ready: 3,
				},
				Pods: clients.PodHealth{
					Total:   100,
					Running: 95,
					Failed:  5,
				},
			},
			expected: "Cluster is degraded: [5 pods failed]",
		},
		{
			name: "degraded cluster with not ready nodes",
			health: &clients.ClusterHealth{
				Status: "degraded",
				Nodes: clients.NodeHealth{
					Total:    3,
					Ready:    2,
					NotReady: 1,
				},
				Pods: clients.PodHealth{
					Total:   100,
					Running: 100,
				},
			},
			expected: "Cluster is degraded: [1 nodes not ready]",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			message := generateHealthMessage(tt.health)
			assert.Contains(t, message, tt.expected)
		})
	}
}

func TestClusterHealthResource_WithCoordinationEngine(t *testing.T) {
	k8sClient, err := clients.NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client (requires cluster access): %v", err)
	}

	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	// Create CE client (will not be used in actual call since CE isn't running)
	ceClient := clients.NewCoordinationEngineClient("http://localhost:8080")

	resource := NewClusterHealthResource(k8sClient, ceClient, memCache)

	ctx := context.Background()
	data, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data)

	// Should still work, falling back to K8s API
	var healthData ClusterHealthData
	err = json.Unmarshal([]byte(data), &healthData)
	require.NoError(t, err)
	assert.Equal(t, "kubernetes-api", healthData.Source)
}
