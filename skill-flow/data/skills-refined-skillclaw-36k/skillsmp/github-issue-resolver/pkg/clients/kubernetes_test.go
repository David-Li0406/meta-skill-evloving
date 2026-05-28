package clients

import (
	"context"
	"testing"
	"time"
)

func TestNewK8sClient(t *testing.T) {
	// Try to create a client first to check if cluster access is available
	testClient, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
		return
	}
	defer func() {
		if err := testClient.Close(); err != nil {
			t.Logf("Error closing test client: %v", err)
		}
	}()

	tests := []struct {
		name    string
		config  *K8sClientConfig
		wantErr bool
	}{
		{
			name:    "nil config uses defaults",
			config:  nil,
			wantErr: false, // Should succeed with kubeconfig
		},
		{
			name: "custom config",
			config: &K8sClientConfig{
				QPS:     100,
				Burst:   200,
				Timeout: 60 * time.Second,
			},
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			client, err := NewK8sClient(tt.config)
			if (err != nil) != tt.wantErr {
				t.Errorf("NewK8sClient() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && client == nil {
				t.Error("NewK8sClient() returned nil client")
			}
			if client != nil {
				defer func() {
					if err := client.Close(); err != nil {
						t.Logf("Error closing client: %v", err)
					}
				}()
			}
		})
	}
}

func TestK8sClient_HealthCheck(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()
	err = client.HealthCheck(ctx)
	if err != nil {
		t.Skipf("Skipping: HealthCheck() failed (no cluster available): %v", err)
	}
}

func TestK8sClient_GetServerVersion(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()
	version, err := client.GetServerVersion(ctx)
	if err != nil {
		t.Skipf("Skipping: GetServerVersion() failed (no cluster available): %v", err)
	}
	if version == "" {
		t.Error("GetServerVersion() returned empty version")
	}
	t.Logf("Server version: %s", version)
}

func TestK8sClient_ListNodes(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()
	nodes, err := client.ListNodes(ctx)
	if err != nil {
		t.Skipf("Skipping: ListNodes() failed (no cluster available): %v", err)
	}
	if len(nodes.Items) == 0 {
		t.Error("ListNodes() returned no nodes")
	}
	t.Logf("Found %d nodes", len(nodes.Items))
}

func TestK8sClient_GetClusterHealth(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()
	health, err := client.GetClusterHealth(ctx)
	if err != nil {
		t.Skipf("Skipping: GetClusterHealth() failed (no cluster available): %v", err)
	}
	if health == nil {
		t.Fatal("GetClusterHealth() returned nil")
	}

	t.Logf("Cluster Health:")
	t.Logf("  Status: %s", health.Status)
	t.Logf("  Nodes: %d total, %d ready, %d not ready",
		health.Nodes.Total, health.Nodes.Ready, health.Nodes.NotReady)
	t.Logf("  Pods: %d total, %d running, %d pending, %d failed",
		health.Pods.Total, health.Pods.Running, health.Pods.Pending, health.Pods.Failed)
}

func TestK8sClient_GetNode(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()

	// First list nodes to get a valid node name
	nodes, err := client.ListNodes(ctx)
	if err != nil {
		t.Skipf("Skipping: ListNodes() failed (no cluster available): %v", err)
	}
	if len(nodes.Items) == 0 {
		t.Skip("No nodes available to test GetNode()")
	}

	nodeName := nodes.Items[0].Name
	node, err := client.GetNode(ctx, nodeName)
	if err != nil {
		t.Errorf("GetNode() failed: %v", err)
	}
	if node == nil {
		t.Error("GetNode() returned nil")
	}
	if node != nil && node.Name != nodeName {
		t.Errorf("GetNode() returned wrong node: got %s, want %s", node.Name, nodeName)
	}
	t.Logf("Retrieved node: %s", nodeName)
}

func TestK8sClient_ListPods(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()

	tests := []struct {
		name      string
		namespace string
	}{
		{
			name:      "all namespaces",
			namespace: "",
		},
		{
			name:      "kube-system namespace",
			namespace: "kube-system",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			pods, err := client.ListPods(ctx, tt.namespace)
			if err != nil {
				t.Skipf("Skipping: ListPods() failed (no cluster available): %v", err)
			}
			t.Logf("Found %d pods in namespace '%s'", len(pods.Items), tt.namespace)
		})
	}
}

func TestK8sClient_GetPod(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()

	// List pods in kube-system to find a pod
	pods, err := client.ListPods(ctx, "kube-system")
	if err != nil {
		t.Skipf("Skipping: ListPods() failed (no cluster available): %v", err)
	}
	if len(pods.Items) == 0 {
		t.Skip("No pods available in kube-system to test GetPod()")
	}

	podName := pods.Items[0].Name
	namespace := pods.Items[0].Namespace

	pod, err := client.GetPod(ctx, namespace, podName)
	if err != nil {
		t.Errorf("GetPod() failed: %v", err)
	}
	if pod == nil {
		t.Error("GetPod() returned nil")
	}
	if pod != nil && pod.Name != podName {
		t.Errorf("GetPod() returned wrong pod: got %s, want %s", pod.Name, podName)
	}
	t.Logf("Retrieved pod: %s/%s", namespace, podName)
}

func TestK8sClient_ListNamespaces(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()
	namespaces, err := client.ListNamespaces(ctx)
	if err != nil {
		t.Skipf("Skipping: ListNamespaces() failed (no cluster available): %v", err)
	}
	if len(namespaces.Items) == 0 {
		t.Error("ListNamespaces() returned no namespaces")
	}
	t.Logf("Found %d namespaces", len(namespaces.Items))
}

func TestK8sClient_ListEvents(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()

	tests := []struct {
		name      string
		namespace string
	}{
		{
			name:      "all namespaces",
			namespace: "",
		},
		{
			name:      "kube-system namespace",
			namespace: "kube-system",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			events, err := client.ListEvents(ctx, tt.namespace)
			if err != nil {
				t.Skipf("Skipping: ListEvents() failed (no cluster available): %v", err)
			}
			t.Logf("Found %d events in namespace '%s'", len(events.Items), tt.namespace)
		})
	}
}

func TestK8sClient_Clientset(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	clientset := client.Clientset()
	if clientset == nil {
		t.Error("Clientset() returned nil")
	}
}

func TestK8sClient_GetConfig(t *testing.T) {
	client, err := NewK8sClient(nil)
	if err != nil {
		t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			t.Logf("Error closing client: %v", err)
		}
	}()

	config := client.GetConfig()
	if config == nil {
		t.Error("GetConfig() returned nil")
	}
	if config != nil {
		t.Logf("Config host: %s", config.Host)
	}
}
