package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// ListPodsTool provides pod listing functionality via MCP
type ListPodsTool struct {
	k8sClient *clients.K8sClient
}

// NewListPodsTool creates a new list-pods tool
func NewListPodsTool(k8sClient *clients.K8sClient) *ListPodsTool {
	return &ListPodsTool{
		k8sClient: k8sClient,
	}
}

// Name returns the tool name for MCP registration
func (t *ListPodsTool) Name() string {
	return "list-pods"
}

// Description returns the tool description for MCP
func (t *ListPodsTool) Description() string {
	return "List pods in the OpenShift cluster with optional filtering by namespace, labels, and fields. Returns pod status, restarts, age, and readiness information."
}

// InputSchema returns the JSON schema for tool inputs
func (t *ListPodsTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"namespace": map[string]interface{}{
				"type":        "string",
				"description": "Filter pods by namespace. Leave empty for all namespaces.",
				"default":     "",
			},
			"label_selector": map[string]interface{}{
				"type":        "string",
				"description": "Kubernetes label selector (e.g., 'app=nginx,tier=frontend')",
				"default":     "",
			},
			"field_selector": map[string]interface{}{
				"type":        "string",
				"description": "Kubernetes field selector (e.g., 'status.phase=Running')",
				"default":     "",
			},
			"limit": map[string]interface{}{
				"type":        "integer",
				"description": "Maximum number of pods to return (0 = no limit)",
				"default":     100,
				"minimum":     0,
			},
		},
		"required": []string{},
	}
}

// ListPodsInput represents the input parameters
type ListPodsInput struct {
	Namespace     string `json:"namespace"`
	LabelSelector string `json:"label_selector"`
	FieldSelector string `json:"field_selector"`
	Limit         int    `json:"limit"`
}

// PodInfo represents simplified pod information
type PodInfo struct {
	Name       string            `json:"name"`
	Namespace  string            `json:"namespace"`
	Status     string            `json:"status"`
	Phase      string            `json:"phase"`
	Restarts   int32             `json:"restarts"`
	Ready      string            `json:"ready"` // "2/2" format
	Age        string            `json:"age"`   // Human-readable
	Node       string            `json:"node"`
	IP         string            `json:"ip"`
	Labels     map[string]string `json:"labels,omitempty"`
	Containers []ContainerInfo   `json:"containers"`
	CreatedAt  time.Time         `json:"created_at"`
}

// ContainerInfo represents container information
type ContainerInfo struct {
	Name         string `json:"name"`
	Image        string `json:"image"`
	Ready        bool   `json:"ready"`
	RestartCount int32  `json:"restart_count"`
	State        string `json:"state"` // Running, Waiting, Terminated
	Reason       string `json:"reason,omitempty"`
}

// ListPodsOutput represents the tool output
type ListPodsOutput struct {
	Pods      []PodInfo `json:"pods"`
	Count     int       `json:"count"`
	Namespace string    `json:"namespace,omitempty"`
	Filters   struct {
		LabelSelector string `json:"label_selector,omitempty"`
		FieldSelector string `json:"field_selector,omitempty"`
	} `json:"filters,omitempty"`
	Summary struct {
		Running   int `json:"running"`
		Pending   int `json:"pending"`
		Failed    int `json:"failed"`
		Succeeded int `json:"succeeded"`
		Unknown   int `json:"unknown"`
	} `json:"summary"`
}

// Execute runs the list-pods operation
func (t *ListPodsTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments
	input := ListPodsInput{
		Namespace: "",
		Limit:     100, // Default limit
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Intentionally ignore error, use defaults if unmarshal fails
	}

	// Build list options
	listOpts := metav1.ListOptions{}
	if input.LabelSelector != "" {
		listOpts.LabelSelector = input.LabelSelector
	}
	if input.FieldSelector != "" {
		listOpts.FieldSelector = input.FieldSelector
	}
	if input.Limit > 0 {
		limit := int64(input.Limit)
		listOpts.Limit = limit
	}

	// Get pods from K8s client
	var podList *corev1.PodList
	var err error

	if input.Namespace != "" {
		// List pods in specific namespace
		podList, err = t.k8sClient.Clientset().CoreV1().Pods(input.Namespace).List(ctx, listOpts)
	} else {
		// List pods in all namespaces
		podList, err = t.k8sClient.Clientset().CoreV1().Pods("").List(ctx, listOpts)
	}

	if err != nil {
		return nil, fmt.Errorf("failed to list pods: %w", err)
	}

	// Build output
	output := ListPodsOutput{
		Pods:  make([]PodInfo, 0, len(podList.Items)),
		Count: len(podList.Items),
	}

	if input.Namespace != "" {
		output.Namespace = input.Namespace
	}
	if input.LabelSelector != "" {
		output.Filters.LabelSelector = input.LabelSelector
	}
	if input.FieldSelector != "" {
		output.Filters.FieldSelector = input.FieldSelector
	}

	// Process each pod
	for _, pod := range podList.Items {
		podInfo := t.podToPodInfo(&pod)
		output.Pods = append(output.Pods, podInfo)

		// Update summary counts
		switch pod.Status.Phase {
		case corev1.PodRunning:
			output.Summary.Running++
		case corev1.PodPending:
			output.Summary.Pending++
		case corev1.PodFailed:
			output.Summary.Failed++
		case corev1.PodSucceeded:
			output.Summary.Succeeded++
		default:
			output.Summary.Unknown++
		}
	}

	return output, nil
}

// podToPodInfo converts a Kubernetes Pod to PodInfo
func (t *ListPodsTool) podToPodInfo(pod *corev1.Pod) PodInfo {
	// Calculate total restarts
	totalRestarts := int32(0)
	for _, cs := range pod.Status.ContainerStatuses {
		totalRestarts += cs.RestartCount
	}

	// Calculate ready containers
	readyContainers := 0
	totalContainers := len(pod.Spec.Containers)
	for _, cs := range pod.Status.ContainerStatuses {
		if cs.Ready {
			readyContainers++
		}
	}

	// Calculate age
	age := time.Since(pod.CreationTimestamp.Time)
	ageStr := formatDuration(age)

	// Determine overall status
	status := string(pod.Status.Phase)
	if pod.DeletionTimestamp != nil {
		status = "Terminating"
	} else if pod.Status.Reason != "" {
		status = pod.Status.Reason
	}

	// Extract container information
	containers := make([]ContainerInfo, 0, len(pod.Status.ContainerStatuses))
	for _, cs := range pod.Status.ContainerStatuses {
		containerInfo := ContainerInfo{
			Name:         cs.Name,
			Image:        cs.Image,
			Ready:        cs.Ready,
			RestartCount: cs.RestartCount,
		}

		// Determine container state
		if cs.State.Running != nil {
			containerInfo.State = "Running"
		} else if cs.State.Waiting != nil {
			containerInfo.State = "Waiting"
			containerInfo.Reason = cs.State.Waiting.Reason
		} else if cs.State.Terminated != nil {
			containerInfo.State = "Terminated"
			containerInfo.Reason = cs.State.Terminated.Reason
		}

		containers = append(containers, containerInfo)
	}

	return PodInfo{
		Name:       pod.Name,
		Namespace:  pod.Namespace,
		Status:     status,
		Phase:      string(pod.Status.Phase),
		Restarts:   totalRestarts,
		Ready:      fmt.Sprintf("%d/%d", readyContainers, totalContainers),
		Age:        ageStr,
		Node:       pod.Spec.NodeName,
		IP:         pod.Status.PodIP,
		Labels:     pod.Labels,
		Containers: containers,
		CreatedAt:  pod.CreationTimestamp.Time,
	}
}

// formatDuration converts a duration to human-readable format
func formatDuration(d time.Duration) string {
	if d < time.Minute {
		return fmt.Sprintf("%ds", int(d.Seconds()))
	} else if d < time.Hour {
		return fmt.Sprintf("%dm", int(d.Minutes()))
	} else if d < 24*time.Hour {
		return fmt.Sprintf("%dh", int(d.Hours()))
	} else {
		days := int(d.Hours() / 24)
		return fmt.Sprintf("%dd", days)
	}
}
