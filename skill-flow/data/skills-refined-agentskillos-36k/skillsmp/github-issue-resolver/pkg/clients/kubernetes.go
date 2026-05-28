package clients

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
)

// K8sClient wraps the Kubernetes clientset with additional functionality
type K8sClient struct {
	clientset *kubernetes.Clientset
	config    *rest.Config
}

// K8sClientConfig holds configuration for the Kubernetes client
type K8sClientConfig struct {
	// KubeconfigPath is the path to the kubeconfig file
	// If empty, will try in-cluster config first, then ~/.kube/config
	KubeconfigPath string

	// QPS and Burst control client-side rate limiting
	QPS   float32 // Default: 50
	Burst int     // Default: 100

	// Timeout for API requests
	Timeout time.Duration // Default: 30s
}

// NewK8sClient creates a new Kubernetes client with connection pooling
// It tries in-cluster config first, then falls back to kubeconfig
func NewK8sClient(cfg *K8sClientConfig) (*K8sClient, error) {
	if cfg == nil {
		cfg = &K8sClientConfig{
			QPS:     50,
			Burst:   100,
			Timeout: 30 * time.Second,
		}
	}

	// Set defaults if not provided
	if cfg.QPS == 0 {
		cfg.QPS = 50
	}
	if cfg.Burst == 0 {
		cfg.Burst = 100
	}
	if cfg.Timeout == 0 {
		cfg.Timeout = 30 * time.Second
	}

	// Try to get Kubernetes config
	config, err := getKubeConfig(cfg.KubeconfigPath)
	if err != nil {
		return nil, fmt.Errorf("failed to get kubeconfig: %w", err)
	}

	// Configure connection pooling and rate limiting
	config.QPS = cfg.QPS
	config.Burst = cfg.Burst
	config.Timeout = cfg.Timeout

	// Create clientset
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		return nil, fmt.Errorf("failed to create Kubernetes clientset: %w", err)
	}

	client := &K8sClient{
		clientset: clientset,
		config:    config,
	}

	return client, nil
}

// getKubeConfig attempts to build a Kubernetes config
// Priority: 1) in-cluster, 2) provided path, 3) ~/.kube/config, 4) $KUBECONFIG
func getKubeConfig(kubeconfigPath string) (*rest.Config, error) {
	// 1. Try in-cluster config (for production in OpenShift)
	if config, err := rest.InClusterConfig(); err == nil {
		return config, nil
	}

	// 2. Try provided kubeconfig path
	if kubeconfigPath != "" {
		config, err := clientcmd.BuildConfigFromFlags("", kubeconfigPath)
		if err == nil {
			return config, nil
		}
	}

	// 3. Try $KUBECONFIG environment variable
	if kubeconfig := os.Getenv("KUBECONFIG"); kubeconfig != "" {
		config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
		if err == nil {
			return config, nil
		}
	}

	// 4. Try default location (~/.kube/config)
	home, err := os.UserHomeDir()
	if err == nil {
		defaultPath := filepath.Join(home, ".kube", "config")
		if _, err := os.Stat(defaultPath); err == nil {
			config, err := clientcmd.BuildConfigFromFlags("", defaultPath)
			if err == nil {
				return config, nil
			}
		}
	}

	return nil, fmt.Errorf("unable to find kubeconfig (tried in-cluster, KUBECONFIG env, ~/.kube/config)")
}

// HealthCheck verifies the client can connect to the cluster
func (c *K8sClient) HealthCheck(ctx context.Context) error {
	// Simple health check: try to get server version
	_, err := c.clientset.Discovery().ServerVersion()
	if err != nil {
		return fmt.Errorf("kubernetes health check failed: %w", err)
	}
	return nil
}

// GetServerVersion returns the Kubernetes server version
func (c *K8sClient) GetServerVersion(ctx context.Context) (string, error) {
	version, err := c.clientset.Discovery().ServerVersion()
	if err != nil {
		return "", fmt.Errorf("failed to get server version: %w", err)
	}
	return version.GitVersion, nil
}

// ListNodes returns all nodes in the cluster
func (c *K8sClient) ListNodes(ctx context.Context) (*corev1.NodeList, error) {
	nodes, err := c.clientset.CoreV1().Nodes().List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to list nodes: %w", err)
	}
	return nodes, nil
}

// GetNode returns a specific node by name
func (c *K8sClient) GetNode(ctx context.Context, name string) (*corev1.Node, error) {
	node, err := c.clientset.CoreV1().Nodes().Get(ctx, name, metav1.GetOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to get node %s: %w", name, err)
	}
	return node, nil
}

// ListPods returns pods in the specified namespace
// If namespace is empty, returns pods from all namespaces
func (c *K8sClient) ListPods(ctx context.Context, namespace string) (*corev1.PodList, error) {
	pods, err := c.clientset.CoreV1().Pods(namespace).List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to list pods in namespace %s: %w", namespace, err)
	}
	return pods, nil
}

// GetPod returns a specific pod
func (c *K8sClient) GetPod(ctx context.Context, namespace, name string) (*corev1.Pod, error) {
	pod, err := c.clientset.CoreV1().Pods(namespace).Get(ctx, name, metav1.GetOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to get pod %s/%s: %w", namespace, name, err)
	}
	return pod, nil
}

// ListNamespaces returns all namespaces
func (c *K8sClient) ListNamespaces(ctx context.Context) (*corev1.NamespaceList, error) {
	namespaces, err := c.clientset.CoreV1().Namespaces().List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to list namespaces: %w", err)
	}
	return namespaces, nil
}

// ListEvents returns events in the specified namespace
func (c *K8sClient) ListEvents(ctx context.Context, namespace string) (*corev1.EventList, error) {
	events, err := c.clientset.CoreV1().Events(namespace).List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to list events in namespace %s: %w", namespace, err)
	}
	return events, nil
}

// GetClusterHealth returns a summary of cluster health
func (c *K8sClient) GetClusterHealth(ctx context.Context) (*ClusterHealth, error) {
	// Get nodes
	nodes, err := c.ListNodes(ctx)
	if err != nil {
		return nil, err
	}

	// Get all pods
	pods, err := c.ListPods(ctx, "")
	if err != nil {
		return nil, err
	}

	// Calculate node health
	totalNodes := len(nodes.Items)
	readyNodes := 0
	notReadyNodes := 0

	for _, node := range nodes.Items {
		for _, condition := range node.Status.Conditions {
			if condition.Type == corev1.NodeReady {
				if condition.Status == corev1.ConditionTrue {
					readyNodes++
				} else {
					notReadyNodes++
				}
				break
			}
		}
	}

	// Calculate pod health
	totalPods := len(pods.Items)
	runningPods := 0
	pendingPods := 0
	failedPods := 0
	succeededPods := 0
	unknownPods := 0

	for _, pod := range pods.Items {
		switch pod.Status.Phase {
		case corev1.PodRunning:
			runningPods++
		case corev1.PodPending:
			pendingPods++
		case corev1.PodFailed:
			failedPods++
		case corev1.PodSucceeded:
			succeededPods++
		default:
			unknownPods++
		}
	}

	// Determine overall health status
	status := "healthy"
	if notReadyNodes > 0 || failedPods > 0 {
		status = "degraded"
	}
	if readyNodes == 0 || totalNodes == 0 {
		status = "unhealthy"
	}

	return &ClusterHealth{
		Status: status,
		Nodes: NodeHealth{
			Total:    totalNodes,
			Ready:    readyNodes,
			NotReady: notReadyNodes,
		},
		Pods: PodHealth{
			Total:     totalPods,
			Running:   runningPods,
			Pending:   pendingPods,
			Failed:    failedPods,
			Succeeded: succeededPods,
			Unknown:   unknownPods,
		},
	}, nil
}

// ClusterHealth represents the overall health of the cluster
type ClusterHealth struct {
	Status string     `json:"status"` // healthy, degraded, unhealthy
	Nodes  NodeHealth `json:"nodes"`
	Pods   PodHealth  `json:"pods"`
}

// NodeHealth represents node health metrics
type NodeHealth struct {
	Total    int `json:"total"`
	Ready    int `json:"ready"`
	NotReady int `json:"not_ready"`
}

// PodHealth represents pod health metrics
type PodHealth struct {
	Total     int `json:"total"`
	Running   int `json:"running"`
	Pending   int `json:"pending"`
	Failed    int `json:"failed"`
	Succeeded int `json:"succeeded"`
	Unknown   int `json:"unknown"`
}

// Clientset returns the underlying Kubernetes clientset
// This is useful for advanced operations not covered by helper methods
func (c *K8sClient) Clientset() *kubernetes.Clientset {
	return c.clientset
}

// GetConfig returns the Kubernetes rest config
// This is useful for creating additional clients (e.g., dynamic clients)
func (c *K8sClient) GetConfig() *rest.Config {
	return c.config
}

// Close cleans up the client resources
// Note: Kubernetes clientset doesn't require explicit cleanup,
// but this method is provided for future extensibility
func (c *K8sClient) Close() error {
	// No-op for now, but can be extended if needed
	return nil
}

// DeploymentInfo represents deployment information for scaling analysis
type DeploymentInfo struct {
	Name              string `json:"name"`
	Namespace         string `json:"namespace"`
	Replicas          int    `json:"replicas"`
	AvailableReplicas int    `json:"available_replicas"`
	CPURequest        int64  `json:"cpu_request_millicores"`
	MemoryRequest     int64  `json:"memory_request_bytes"`
	CPULimit          int64  `json:"cpu_limit_millicores"`
	MemoryLimit       int64  `json:"memory_limit_bytes"`
}

// GetDeployment returns deployment information
func (c *K8sClient) GetDeployment(ctx context.Context, namespace, name string) (*DeploymentInfo, error) {
	deployment, err := c.clientset.AppsV1().Deployments(namespace).Get(ctx, name, metav1.GetOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to get deployment %s/%s: %w", namespace, name, err)
	}

	info := &DeploymentInfo{
		Name:              deployment.Name,
		Namespace:         deployment.Namespace,
		Replicas:          int(*deployment.Spec.Replicas),
		AvailableReplicas: int(deployment.Status.AvailableReplicas),
	}

	// Extract resource requests/limits from the first container
	if len(deployment.Spec.Template.Spec.Containers) > 0 {
		container := deployment.Spec.Template.Spec.Containers[0]
		if cpu := container.Resources.Requests.Cpu(); cpu != nil {
			info.CPURequest = cpu.MilliValue()
		}
		if mem := container.Resources.Requests.Memory(); mem != nil {
			info.MemoryRequest = mem.Value()
		}
		if cpu := container.Resources.Limits.Cpu(); cpu != nil {
			info.CPULimit = cpu.MilliValue()
		}
		if mem := container.Resources.Limits.Memory(); mem != nil {
			info.MemoryLimit = mem.Value()
		}
	}

	return info, nil
}

// ListDeployments returns all deployments in a namespace
func (c *K8sClient) ListDeployments(ctx context.Context, namespace string) (*appsv1.DeploymentList, error) {
	deployments, err := c.clientset.AppsV1().Deployments(namespace).List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to list deployments in namespace %s: %w", namespace, err)
	}
	return deployments, nil
}

// ResourceQuotaInfo represents resource quota information for a namespace
type ResourceQuotaInfo struct {
	Name                 string `json:"name"`
	Namespace            string `json:"namespace"`
	CPULimitMillicores   int64  `json:"cpu_limit_millicores"`
	MemoryLimitBytes     int64  `json:"memory_limit_bytes"`
	CPUUsedMillicores    int64  `json:"cpu_used_millicores"`
	MemoryUsedBytes      int64  `json:"memory_used_bytes"`
	CPURequestMillicores int64  `json:"cpu_request_millicores"`
	MemoryRequestBytes   int64  `json:"memory_request_bytes"`
	PodCountLimit        int    `json:"pod_count_limit"`
	PodCountUsed         int    `json:"pod_count_used"`
}

// GetResourceQuota returns resource quota information for a namespace
func (c *K8sClient) GetResourceQuota(ctx context.Context, namespace string) (*ResourceQuotaInfo, error) {
	quotaList, err := c.clientset.CoreV1().ResourceQuotas(namespace).List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to list resource quotas in namespace %s: %w", namespace, err)
	}

	if len(quotaList.Items) == 0 {
		return nil, fmt.Errorf("no resource quota found in namespace %s", namespace)
	}

	// Use the first quota (typically there's only one)
	quota := quotaList.Items[0]

	info := &ResourceQuotaInfo{
		Name:      quota.Name,
		Namespace: quota.Namespace,
	}

	// Extract hard limits
	if cpu, ok := quota.Spec.Hard[corev1.ResourceLimitsCPU]; ok {
		info.CPULimitMillicores = cpu.MilliValue()
	}
	if mem, ok := quota.Spec.Hard[corev1.ResourceLimitsMemory]; ok {
		info.MemoryLimitBytes = mem.Value()
	}
	if cpu, ok := quota.Spec.Hard[corev1.ResourceRequestsCPU]; ok {
		info.CPURequestMillicores = cpu.MilliValue()
	}
	if mem, ok := quota.Spec.Hard[corev1.ResourceRequestsMemory]; ok {
		info.MemoryRequestBytes = mem.Value()
	}
	// Extract pod count limit
	if pods, ok := quota.Spec.Hard[corev1.ResourcePods]; ok {
		info.PodCountLimit = int(pods.Value())
	}

	// Extract used values
	if cpu, ok := quota.Status.Used[corev1.ResourceLimitsCPU]; ok {
		info.CPUUsedMillicores = cpu.MilliValue()
	}
	if mem, ok := quota.Status.Used[corev1.ResourceLimitsMemory]; ok {
		info.MemoryUsedBytes = mem.Value()
	}
	// Extract used pod count
	if pods, ok := quota.Status.Used[corev1.ResourcePods]; ok {
		info.PodCountUsed = int(pods.Value())
	}

	// If limits not set, use requests as fallback
	if info.CPULimitMillicores == 0 && info.CPURequestMillicores > 0 {
		info.CPULimitMillicores = info.CPURequestMillicores
	}
	if info.MemoryLimitBytes == 0 && info.MemoryRequestBytes > 0 {
		info.MemoryLimitBytes = info.MemoryRequestBytes
	}
	// Default pod limit if not set
	if info.PodCountLimit == 0 {
		info.PodCountLimit = 100 // Default to 100 pods
	}

	return info, nil
}
