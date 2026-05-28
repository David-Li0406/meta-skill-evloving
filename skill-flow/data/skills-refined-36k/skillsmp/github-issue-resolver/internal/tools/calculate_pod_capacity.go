package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/capacity"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// CalculatePodCapacityTool provides MCP tool for calculating namespace/cluster pod capacity
type CalculatePodCapacityTool struct {
	k8sClient *clients.K8sClient
}

// NewCalculatePodCapacityTool creates a new calculate-pod-capacity tool
func NewCalculatePodCapacityTool(k8sClient *clients.K8sClient) *CalculatePodCapacityTool {
	return &CalculatePodCapacityTool{
		k8sClient: k8sClient,
	}
}

// Name returns the tool name
func (t *CalculatePodCapacityTool) Name() string {
	return "calculate-pod-capacity"
}

// Description returns the tool description
func (t *CalculatePodCapacityTool) Description() string {
	return `Calculate remaining pod capacity based on current resource usage and cluster/namespace limits.

RESPONSE INTERPRETATION:
- recommended_limit.safe_pod_count: Number of additional pods that can safely be scheduled
- recommended_limit.max_pod_count: Theoretical maximum (without safety margin)
- recommended_limit.limiting_factor: What will run out first ("cpu", "memory", or "pod_count")
- current_usage.cpu_percent / memory_percent: Current resource utilization percentage
- available_capacity.cpu / memory / pod_slots: Raw available resources

PRESENTATION TO USER:
- Lead with capacity: "You can safely deploy approximately [safe_pod_count] more [pod_profile] pods"
- Include limiting factor: "Limited by [limiting_factor]"
- If cpu_percent or memory_percent > 80%: Warn about capacity constraints
- If limiting_factor is "pod_count": Mention cluster pod limits, not just resources
- Always mention both CPU and memory headroom for context
- Include trending info if available: "At current growth rate, capacity exhaustion in [N] days"

DEFAULT ASSUMPTIONS (use if user doesn't specify):
- namespace: 'cluster' (cluster-wide analysis)
- pod_profile: 'medium' (100m CPU, 256Mi memory)
- safety_margin: 15% headroom maintained
- include_trending: true

POD PROFILES:
- small: 50m CPU, 128Mi memory - lightweight workloads
- medium: 100m CPU, 256Mi memory - typical applications
- large: 500m CPU, 1Gi memory - resource-intensive workloads
- custom: User-specified CPU and memory requests

Example questions this tool answers:
- "How many more pods can I run?"
- "Can I deploy 50 monitoring agents?"
- "What's my cluster capacity?"
- "How much headroom do I have in the openshift-monitoring namespace?"`
}

// InputSchema returns the JSON schema for tool inputs
func (t *CalculatePodCapacityTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"namespace": map[string]interface{}{
				"type":        "string",
				"description": "Namespace name to analyze. Use 'cluster' for cluster-wide capacity analysis. Default: 'cluster'",
				"default":     "cluster",
			},
			"pod_profile": map[string]interface{}{
				"type":        "string",
				"description": "Pod resource profile to use for calculations.",
				"enum":        []string{"small", "medium", "large", "custom"},
				"default":     "medium",
			},
			"custom_resources": map[string]interface{}{
				"type":        "object",
				"description": "Custom resource requirements. Required when pod_profile is 'custom'.",
				"properties": map[string]interface{}{
					"cpu": map[string]interface{}{
						"type":        "string",
						"description": "CPU request (e.g., '200m', '0.5', '1')",
					},
					"memory": map[string]interface{}{
						"type":        "string",
						"description": "Memory request (e.g., '128Mi', '1Gi')",
					},
				},
			},
			"safety_margin": map[string]interface{}{
				"type":        "number",
				"description": "Percentage of headroom to maintain for safety (0-50). Default: 15",
				"minimum":     0,
				"maximum":     50,
				"default":     15,
			},
			"include_trending": map[string]interface{}{
				"type":        "boolean",
				"description": "Include usage trend analysis and capacity exhaustion predictions. Default: true",
				"default":     true,
			},
		},
		"required": []string{},
	}
}

// CalculatePodCapacityInput represents the input parameters
type CalculatePodCapacityInput struct {
	Namespace       string                 `json:"namespace"`
	PodProfile      string                 `json:"pod_profile"`
	CustomResources *CustomResourcesInput  `json:"custom_resources,omitempty"`
	SafetyMargin    *float64               `json:"safety_margin,omitempty"`
	IncludeTrending *bool                  `json:"include_trending,omitempty"`
}

// CustomResourcesInput represents custom pod resource requirements
type CustomResourcesInput struct {
	CPU    string `json:"cpu"`
	Memory string `json:"memory"`
}

// CalculatePodCapacityOutput represents the tool output
type CalculatePodCapacityOutput struct {
	Status            string                            `json:"status"`
	Namespace         string                            `json:"namespace"`
	NamespaceQuota    *NamespaceQuotaOutput             `json:"namespace_quota"`
	CurrentUsage      *CurrentUsageOutput               `json:"current_usage"`
	AvailableCapacity *AvailableCapacityOutput          `json:"available_capacity"`
	PodEstimates      map[string]*PodEstimateOutput     `json:"pod_estimates"`
	RecommendedLimit  *RecommendedLimitOutput           `json:"recommended_limit"`
	Trending          *TrendingOutput                   `json:"trending,omitempty"`
	Recommendation    string                            `json:"recommendation"`
}

// NamespaceQuotaOutput represents namespace quota information
type NamespaceQuotaOutput struct {
	CPULimit       string `json:"cpu_limit"`
	MemoryLimit    string `json:"memory_limit"`
	PodCountLimit  int    `json:"pod_count_limit"`
}

// CurrentUsageOutput represents current resource usage
type CurrentUsageOutput struct {
	CPU           string  `json:"cpu"`
	Memory        string  `json:"memory"`
	CPUPercent    float64 `json:"cpu_percent"`
	MemoryPercent float64 `json:"memory_percent"`
	PodCount      int     `json:"pod_count"`
}

// AvailableCapacityOutput represents available capacity
type AvailableCapacityOutput struct {
	CPU      string `json:"cpu"`
	Memory   string `json:"memory"`
	PodSlots int    `json:"pod_slots"`
}

// PodEstimateOutput represents pod capacity estimates for a profile
type PodEstimateOutput struct {
	CPU            string `json:"cpu"`
	Memory         string `json:"memory"`
	MaxPods        int    `json:"max_pods"`
	SafePods       int    `json:"safe_pods"`
	LimitingFactor string `json:"limiting_factor,omitempty"`
}

// RecommendedLimitOutput represents the recommended deployment limit
type RecommendedLimitOutput struct {
	PodProfile     string `json:"pod_profile"`
	SafePodCount   int    `json:"safe_pod_count"`
	MaxPodCount    int    `json:"max_pod_count"`
	LimitingFactor string `json:"limiting_factor"`
	Explanation    string `json:"explanation"`
}

// TrendingOutput represents usage trending information
type TrendingOutput struct {
	DailyCPUGrowthPercent    float64 `json:"daily_cpu_growth_percent"`
	DailyMemoryGrowthPercent float64 `json:"daily_memory_growth_percent"`
	DaysUntil85Percent       int     `json:"days_until_85_percent"`
	ProjectedDate            string  `json:"projected_date,omitempty"`
}

// Execute runs the calculate-pod-capacity tool
func (t *CalculatePodCapacityTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Verify k8sClient is available
	if t.k8sClient == nil {
		return nil, fmt.Errorf("kubernetes client not initialized")
	}

	// Parse input arguments
	input, err := t.parseInput(args)
	if err != nil {
		return nil, fmt.Errorf("invalid input: %w", err)
	}

	// Apply default namespace if not specified
	if input.Namespace == "" {
		input.Namespace = "cluster"
	}

	// Handle cluster-wide capacity
	if strings.ToLower(input.Namespace) == "cluster" {
		return t.calculateClusterCapacity(ctx, input)
	}

	// Get namespace quota
	quota, err := t.getNamespaceCapacity(ctx, input.Namespace)
	if err != nil {
		// If no quota found, calculate based on available resources
		quota = t.estimateNamespaceCapacity(ctx, input.Namespace)
	}

	// Parse custom resources if provided
	var customResources *capacity.PodResources
	if input.CustomResources != nil && input.PodProfile == "custom" {
		customResources = &capacity.PodResources{
			CPUMillicores: parseCPU(input.CustomResources.CPU),
			MemoryMB:      parseMemoryMB(input.CustomResources.Memory),
		}
	}

	// Set default safety margin
	safetyMargin := 15.0
	if input.SafetyMargin != nil {
		safetyMargin = *input.SafetyMargin
	}

	// Create calculator
	calc := capacity.NewCalculator(safetyMargin / 100.0)

	// Calculate capacity
	podProfile := capacity.PodProfileMedium
	switch input.PodProfile {
	case "small":
		podProfile = capacity.PodProfileSmall
	case "large":
		podProfile = capacity.PodProfileLarge
	case "custom":
		podProfile = capacity.PodProfileCustom
	}

	result, err := calc.CalculatePodCapacity(quota, podProfile, customResources, &safetyMargin)
	if err != nil {
		return nil, fmt.Errorf("failed to calculate capacity: %w", err)
	}

	// Build output
	output := &CalculatePodCapacityOutput{
		Status:    "success",
		Namespace: input.Namespace,
		NamespaceQuota: &NamespaceQuotaOutput{
			CPULimit:      result.NamespaceQuota.CPULimit,
			MemoryLimit:   result.NamespaceQuota.MemoryLimit,
			PodCountLimit: result.NamespaceQuota.PodCountLimit,
		},
		CurrentUsage: &CurrentUsageOutput{
			CPU:           result.CurrentUsage.CPU,
			Memory:        result.CurrentUsage.Memory,
			CPUPercent:    result.CurrentUsage.CPUPercent,
			MemoryPercent: result.CurrentUsage.MemoryPercent,
			PodCount:      result.CurrentUsage.PodCount,
		},
		AvailableCapacity: &AvailableCapacityOutput{
			CPU:      result.AvailableCapacity.CPU,
			Memory:   result.AvailableCapacity.Memory,
			PodSlots: result.AvailableCapacity.PodSlots,
		},
		PodEstimates:   t.convertPodEstimates(result.PodEstimates),
		RecommendedLimit: &RecommendedLimitOutput{
			PodProfile:     result.RecommendedLimit.PodProfile,
			SafePodCount:   result.RecommendedLimit.SafePodCount,
			MaxPodCount:    result.RecommendedLimit.MaxPodCount,
			LimitingFactor: result.RecommendedLimit.LimitingFactor,
			Explanation:    result.RecommendedLimit.Explanation,
		},
		Recommendation: result.Recommendation,
	}

	// Add trending if requested
	includeTrending := true
	if input.IncludeTrending != nil {
		includeTrending = *input.IncludeTrending
	}
	if includeTrending {
		trending := calc.CalculateTrending(
			nil, nil, // Historical data not available yet, use estimates
			result.CurrentUsage.CPUPercent,
			result.CurrentUsage.MemoryPercent,
		)
		output.Trending = &TrendingOutput{
			DailyCPUGrowthPercent:    trending.DailyCPUGrowthPercent,
			DailyMemoryGrowthPercent: trending.DailyMemoryGrowthPercent,
			DaysUntil85Percent:       trending.DaysUntil85Percent,
			ProjectedDate:            trending.ProjectedDate,
		}

		// Update recommendation with trending info
		if trending.DaysUntil85Percent > 0 && trending.DaysUntil85Percent < 30 {
			output.Recommendation += fmt.Sprintf(" Current trend suggests capacity exhaustion in %d days.", trending.DaysUntil85Percent)
		}
	}

	return output, nil
}

// parseInput parses and validates the input arguments
func (t *CalculatePodCapacityTool) parseInput(args map[string]interface{}) (*CalculatePodCapacityInput, error) {
	input := &CalculatePodCapacityInput{
		PodProfile: "medium", // Default
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		if err := json.Unmarshal(argsJSON, input); err != nil {
			return nil, fmt.Errorf("failed to parse input: %w", err)
		}
	}

	// Handle numeric type coercion for safety_margin
	if v, ok := args["safety_margin"]; ok {
		switch val := v.(type) {
		case float64:
			input.SafetyMargin = &val
		case int:
			f := float64(val)
			input.SafetyMargin = &f
		case int64:
			f := float64(val)
			input.SafetyMargin = &f
		}
	}

	// Handle boolean for include_trending
	if v, ok := args["include_trending"]; ok {
		if b, ok := v.(bool); ok {
			input.IncludeTrending = &b
		}
	}

	return input, nil
}

// getNamespaceCapacity retrieves namespace capacity information
func (t *CalculatePodCapacityTool) getNamespaceCapacity(ctx context.Context, namespace string) (*capacity.NamespaceQuota, error) {
	// Get resource quota
	quota, err := t.k8sClient.GetResourceQuota(ctx, namespace)
	if err != nil {
		return nil, err
	}

	// Get current pod count
	pods, err := t.k8sClient.ListPods(ctx, namespace)
	podCount := 0
	if err == nil {
		for _, pod := range pods.Items {
			if pod.Status.Phase == "Running" || pod.Status.Phase == "Pending" {
				podCount++
			}
		}
	}

	// Estimate used resources from pods if not available in quota
	cpuUsed := quota.CPUUsedMillicores
	memoryUsed := quota.MemoryUsedBytes

	if cpuUsed == 0 || memoryUsed == 0 {
		cpuUsed, memoryUsed = t.calculatePodResourceUsage(ctx, namespace)
	}

	return &capacity.NamespaceQuota{
		CPULimitMillicores:  quota.CPULimitMillicores,
		MemoryLimitBytes:    quota.MemoryLimitBytes,
		PodCountLimit:       100, // Default pod limit if not set
		CPUUsedMillicores:   cpuUsed,
		MemoryUsedBytes:     memoryUsed,
		CurrentPodCount:     podCount,
		HasQuota:            true,
	}, nil
}

// estimateNamespaceCapacity estimates capacity when no quota is set
func (t *CalculatePodCapacityTool) estimateNamespaceCapacity(ctx context.Context, namespace string) *capacity.NamespaceQuota {
	// Get current pod count and resource usage
	pods, _ := t.k8sClient.ListPods(ctx, namespace)
	podCount := 0
	if pods != nil {
		for _, pod := range pods.Items {
			if pod.Status.Phase == "Running" || pod.Status.Phase == "Pending" {
				podCount++
			}
		}
	}

	cpuUsed, memoryUsed := t.calculatePodResourceUsage(ctx, namespace)

	// Default unlimited quota (use node capacity estimates)
	// Assume ~4 cores and 8GB per namespace without quota
	return &capacity.NamespaceQuota{
		CPULimitMillicores:  4000,                    // 4 cores
		MemoryLimitBytes:    8 * 1024 * 1024 * 1024,  // 8 GB
		PodCountLimit:       100,                     // Default pod limit
		CPUUsedMillicores:   cpuUsed,
		MemoryUsedBytes:     memoryUsed,
		CurrentPodCount:     podCount,
		HasQuota:            false,
	}
}

// calculatePodResourceUsage calculates total resource usage from pods
func (t *CalculatePodCapacityTool) calculatePodResourceUsage(ctx context.Context, namespace string) (int64, int64) {
	pods, err := t.k8sClient.ListPods(ctx, namespace)
	if err != nil {
		return 0, 0
	}

	var totalCPU, totalMemory int64

	for _, pod := range pods.Items {
		if pod.Status.Phase != "Running" && pod.Status.Phase != "Pending" {
			continue
		}

		for _, container := range pod.Spec.Containers {
			if cpu := container.Resources.Requests.Cpu(); cpu != nil {
				totalCPU += cpu.MilliValue()
			}
			if mem := container.Resources.Requests.Memory(); mem != nil {
				totalMemory += mem.Value()
			}
		}
	}

	return totalCPU, totalMemory
}

// calculateClusterCapacity calculates cluster-wide capacity
func (t *CalculatePodCapacityTool) calculateClusterCapacity(ctx context.Context, input *CalculatePodCapacityInput) (*CalculatePodCapacityOutput, error) {
	// Get all nodes to calculate cluster capacity
	nodes, err := t.k8sClient.ListNodes(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to list nodes: %w", err)
	}

	var totalCPU, totalMemory int64
	var allocatableCPU, allocatableMemory int64

	for _, node := range nodes.Items {
		// Skip non-ready nodes
		ready := false
		for _, condition := range node.Status.Conditions {
			if condition.Type == "Ready" && condition.Status == "True" {
				ready = true
				break
			}
		}
		if !ready {
			continue
		}

		// Get allocatable resources
		if cpu := node.Status.Allocatable.Cpu(); cpu != nil {
			allocatableCPU += cpu.MilliValue()
		}
		if mem := node.Status.Allocatable.Memory(); mem != nil {
			allocatableMemory += mem.Value()
		}

		// Get capacity
		if cpu := node.Status.Capacity.Cpu(); cpu != nil {
			totalCPU += cpu.MilliValue()
		}
		if mem := node.Status.Capacity.Memory(); mem != nil {
			totalMemory += mem.Value()
		}
	}

	// Get all pods to calculate used resources
	pods, err := t.k8sClient.ListPods(ctx, "") // All namespaces
	if err != nil {
		return nil, fmt.Errorf("failed to list pods: %w", err)
	}

	var usedCPU, usedMemory int64
	podCount := 0

	for _, pod := range pods.Items {
		if pod.Status.Phase != "Running" && pod.Status.Phase != "Pending" {
			continue
		}
		podCount++

		for _, container := range pod.Spec.Containers {
			if cpu := container.Resources.Requests.Cpu(); cpu != nil {
				usedCPU += cpu.MilliValue()
			}
			if mem := container.Resources.Requests.Memory(); mem != nil {
				usedMemory += mem.Value()
			}
		}
	}

	// Build cluster quota
	quota := &capacity.NamespaceQuota{
		CPULimitMillicores:  allocatableCPU,
		MemoryLimitBytes:    allocatableMemory,
		PodCountLimit:       len(nodes.Items) * 110, // ~110 pods per node default
		CPUUsedMillicores:   usedCPU,
		MemoryUsedBytes:     usedMemory,
		CurrentPodCount:     podCount,
		HasQuota:            true,
	}

	// Parse custom resources if provided
	var customResources *capacity.PodResources
	if input.CustomResources != nil && input.PodProfile == "custom" {
		customResources = &capacity.PodResources{
			CPUMillicores: parseCPU(input.CustomResources.CPU),
			MemoryMB:      parseMemoryMB(input.CustomResources.Memory),
		}
	}

	// Set safety margin
	safetyMargin := 15.0
	if input.SafetyMargin != nil {
		safetyMargin = *input.SafetyMargin
	}

	// Create calculator
	calc := capacity.NewCalculator(safetyMargin / 100.0)

	// Calculate capacity
	podProfile := capacity.PodProfileMedium
	switch input.PodProfile {
	case "small":
		podProfile = capacity.PodProfileSmall
	case "large":
		podProfile = capacity.PodProfileLarge
	case "custom":
		podProfile = capacity.PodProfileCustom
	}

	result, err := calc.CalculatePodCapacity(quota, podProfile, customResources, &safetyMargin)
	if err != nil {
		return nil, fmt.Errorf("failed to calculate capacity: %w", err)
	}

	// Build output
	output := &CalculatePodCapacityOutput{
		Status:    "success",
		Namespace: "cluster",
		NamespaceQuota: &NamespaceQuotaOutput{
			CPULimit:      result.NamespaceQuota.CPULimit,
			MemoryLimit:   result.NamespaceQuota.MemoryLimit,
			PodCountLimit: result.NamespaceQuota.PodCountLimit,
		},
		CurrentUsage: &CurrentUsageOutput{
			CPU:           result.CurrentUsage.CPU,
			Memory:        result.CurrentUsage.Memory,
			CPUPercent:    result.CurrentUsage.CPUPercent,
			MemoryPercent: result.CurrentUsage.MemoryPercent,
			PodCount:      result.CurrentUsage.PodCount,
		},
		AvailableCapacity: &AvailableCapacityOutput{
			CPU:      result.AvailableCapacity.CPU,
			Memory:   result.AvailableCapacity.Memory,
			PodSlots: result.AvailableCapacity.PodSlots,
		},
		PodEstimates:   t.convertPodEstimates(result.PodEstimates),
		RecommendedLimit: &RecommendedLimitOutput{
			PodProfile:     result.RecommendedLimit.PodProfile,
			SafePodCount:   result.RecommendedLimit.SafePodCount,
			MaxPodCount:    result.RecommendedLimit.MaxPodCount,
			LimitingFactor: result.RecommendedLimit.LimitingFactor,
			Explanation:    result.RecommendedLimit.Explanation,
		},
		Recommendation: result.Recommendation,
	}

	// Add trending if requested
	includeTrending := true
	if input.IncludeTrending != nil {
		includeTrending = *input.IncludeTrending
	}
	if includeTrending {
		trending := calc.CalculateTrending(
			nil, nil,
			result.CurrentUsage.CPUPercent,
			result.CurrentUsage.MemoryPercent,
		)
		output.Trending = &TrendingOutput{
			DailyCPUGrowthPercent:    trending.DailyCPUGrowthPercent,
			DailyMemoryGrowthPercent: trending.DailyMemoryGrowthPercent,
			DaysUntil85Percent:       trending.DaysUntil85Percent,
			ProjectedDate:            trending.ProjectedDate,
		}
	}

	return output, nil
}

// convertPodEstimates converts capacity package estimates to output format
func (t *CalculatePodCapacityTool) convertPodEstimates(estimates map[string]*capacity.PodEstimate) map[string]*PodEstimateOutput {
	result := make(map[string]*PodEstimateOutput)
	for name, est := range estimates {
		result[name] = &PodEstimateOutput{
			CPU:            fmt.Sprintf("%dm", est.CPUMillicores),
			Memory:         fmt.Sprintf("%dMi", est.MemoryMB),
			MaxPods:        est.MaxPods,
			SafePods:       est.SafePods,
			LimitingFactor: est.LimitingFactor,
		}
	}
	return result
}

// Helper functions for parsing resource strings

// parseCPU parses CPU strings like "200m", "0.5", "1" into millicores
func parseCPU(cpu string) int64 {
	if cpu == "" {
		return 0
	}

	cpu = strings.TrimSpace(cpu)
	
	// Handle millicores format (e.g., "200m")
	if strings.HasSuffix(cpu, "m") {
		var value int64
		_, _ = fmt.Sscanf(cpu, "%dm", &value) //nolint:errcheck // Best effort parsing
		return value
	}

	// Handle decimal format (e.g., "0.5", "1")
	var value float64
	_, _ = fmt.Sscanf(cpu, "%f", &value) //nolint:errcheck // Best effort parsing
	return int64(value * 1000)
}

// parseMemoryMB parses memory strings like "128Mi", "1Gi" into MB
func parseMemoryMB(memory string) int64 {
	if memory == "" {
		return 0
	}

	memory = strings.TrimSpace(memory)

	// Handle Gi format
	if strings.HasSuffix(memory, "Gi") {
		var value int64
		_, _ = fmt.Sscanf(memory, "%dGi", &value) //nolint:errcheck // Best effort parsing
		return value * 1024
	}

	// Handle Mi format
	if strings.HasSuffix(memory, "Mi") {
		var value int64
		_, _ = fmt.Sscanf(memory, "%dMi", &value) //nolint:errcheck // Best effort parsing
		return value
	}

	// Handle Ki format
	if strings.HasSuffix(memory, "Ki") {
		var value int64
		_, _ = fmt.Sscanf(memory, "%dKi", &value) //nolint:errcheck // Best effort parsing
		return value / 1024
	}

	// Handle plain bytes
	var value int64
	_, _ = fmt.Sscanf(memory, "%d", &value) //nolint:errcheck // Best effort parsing
	return value / (1024 * 1024)
}
