package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// PredictResourceUsageTool provides MCP tool for time-specific resource usage predictions
type PredictResourceUsageTool struct {
	ceClient   *clients.CoordinationEngineClient
	k8sClient  *clients.K8sClient
}

// NewPredictResourceUsageTool creates a new predict-resource-usage tool
func NewPredictResourceUsageTool(ceClient *clients.CoordinationEngineClient, k8sClient *clients.K8sClient) *PredictResourceUsageTool {
	return &PredictResourceUsageTool{
		ceClient:  ceClient,
		k8sClient: k8sClient,
	}
}

// Name returns the tool name
func (t *PredictResourceUsageTool) Name() string {
	return "predict-resource-usage"
}

// Description returns the tool description
func (t *PredictResourceUsageTool) Description() string {
	return `Predict future CPU and memory usage using ML models trained on historical cluster data.

RESPONSE INTERPRETATION:
- predicted_metrics.cpu_percent / memory_percent: Forecasted usage at target time (0-100%)
- current_metrics.cpu_percent: Current estimated CPU utilization baseline (0-100%)
- current_metrics.memory_percent: Current estimated memory utilization baseline (0-100%)
- predicted_metrics.confidence: Model confidence score (0.85 = 85% confident)

PRESENTATION TO USER:
- Lead with prediction: "Predicted CPU at [time]: [X]%"
- Include baseline: "Current baseline: CPU [Y]%, Memory [Z]%"
- Include confidence: "Confidence: [N]%"
- If confidence < 0.7, warn user predictions may be less reliable
- If current_metrics values seem low, note this is estimated from cluster state

SCOPES: cluster (default), namespace, deployment, pod

Example questions this tool answers:
- "What will CPU be at 3 PM?"
- "Predict memory usage for tomorrow morning"
- "What's the resource forecast for openshift-monitoring namespace?"`
}

// InputSchema returns the JSON schema for tool inputs
func (t *PredictResourceUsageTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"target_time": map[string]interface{}{
				"type":        "string",
				"description": "Target time for prediction in HH:MM format (24-hour). Defaults to current time + 1 hour.",
				"pattern":     "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
			},
			"target_date": map[string]interface{}{
				"type":        "string",
				"description": "Target date for prediction in YYYY-MM-DD format. Defaults to today.",
				"pattern":     "^\\d{4}-\\d{2}-\\d{2}$",
			},
			"namespace": map[string]interface{}{
				"type":        "string",
				"description": "Kubernetes namespace to scope the prediction. Supports wildcards (e.g., 'openshift-*').",
			},
			"deployment": map[string]interface{}{
				"type":        "string",
				"description": "Specific deployment name to predict resource usage for.",
			},
			"pod": map[string]interface{}{
				"type":        "string",
				"description": "Specific pod name to predict resource usage for.",
			},
			"metric": map[string]interface{}{
				"type":        "string",
				"description": "Metric type to predict: 'cpu_usage', 'memory_usage', or 'both'.",
				"enum":        []string{"cpu_usage", "memory_usage", "both"},
				"default":     "both",
			},
			"scope": map[string]interface{}{
				"type":        "string",
				"description": "Prediction scope: 'pod', 'deployment', 'namespace', or 'cluster'.",
				"enum":        []string{"pod", "deployment", "namespace", "cluster"},
				"default":     "namespace",
			},
		},
		"required": []string{},
	}
}

// PredictResourceUsageInput represents the input parameters
type PredictResourceUsageInput struct {
	TargetTime string `json:"target_time"`
	TargetDate string `json:"target_date"`
	Namespace  string `json:"namespace"`
	Deployment string `json:"deployment"`
	Pod        string `json:"pod"`
	Metric     string `json:"metric"`
	Scope      string `json:"scope"`
}

// CurrentMetrics represents current metric values
type CurrentMetrics struct {
	CPUPercent    float64 `json:"cpu_percent"`
	MemoryPercent float64 `json:"memory_percent"`
	Timestamp     string  `json:"timestamp"`
}

// PredictedMetrics represents predicted metric values
type PredictedMetrics struct {
	CPUPercent    float64 `json:"cpu_percent,omitempty"`
	MemoryPercent float64 `json:"memory_percent,omitempty"`
	TargetTime    string  `json:"target_time"`
	Confidence    float64 `json:"confidence"`
}

// PredictResourceUsageOutput represents the tool output
type PredictResourceUsageOutput struct {
	Status           string           `json:"status"`
	Scope            string           `json:"scope"`
	Target           string           `json:"target"`
	CurrentMetrics   CurrentMetrics   `json:"current_metrics"`
	PredictedMetrics PredictedMetrics `json:"predicted_metrics"`
	Trend            string           `json:"trend"`
	Recommendation   string           `json:"recommendation"`
	ModelUsed        string           `json:"model_used"`
	ModelVersion     string           `json:"model_version"`
}

// Execute runs the predict-resource-usage tool
func (t *PredictResourceUsageTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments with defaults
	input := PredictResourceUsageInput{
		Metric: "both",
		Scope:  "namespace",
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Intentionally ignore error, use defaults if unmarshal fails
	}

	// Parse and validate target datetime
	targetTime, err := t.parseTargetDatetime(input.TargetTime, input.TargetDate)
	if err != nil {
		return nil, fmt.Errorf("invalid target time/date: %w", err)
	}

	// Determine the target based on scope
	target, err := t.determineTarget(input)
	if err != nil {
		return nil, err
	}

	// Get current metrics
	currentMetrics, err := t.getCurrentMetrics(ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to get current metrics: %w", err)
	}

	// Extract hour and day_of_week from target time
	hour := targetTime.Hour()
	dayOfWeek := int(targetTime.Weekday())
	// Convert from Go's Sunday=0 to Monday=0 format
	if dayOfWeek == 0 {
		dayOfWeek = 6 // Sunday
	} else {
		dayOfWeek-- // Shift Monday-Saturday
	}

	// Call coordination engine for prediction
	predReq := &clients.PredictResourceUsageRequest{
		Hour:              hour,
		DayOfWeek:         dayOfWeek,
		CPURollingMean:    currentMetrics.CPUPercent,
		MemoryRollingMean: currentMetrics.MemoryPercent,
		Namespace:         input.Namespace,
		Deployment:        input.Deployment,
		Pod:               input.Pod,
		Scope:             input.Scope,
	}

	predResp, err := t.ceClient.PredictResourceUsage(ctx, predReq)
	if err != nil {
		return nil, fmt.Errorf("failed to get prediction from coordination engine: %w", err)
	}

	// Build output - use current metrics from Coordination Engine (Prometheus-based)
	// instead of heuristic calculations
	output := PredictResourceUsageOutput{
		Status: predResp.Status,
		Scope:  input.Scope,
		Target: target,
		CurrentMetrics: CurrentMetrics{
			CPUPercent:    predResp.CurrentCPU,    // Use CE's Prometheus data
			MemoryPercent: predResp.CurrentMemory, // Use CE's Prometheus data
			Timestamp:     time.Now().UTC().Format(time.RFC3339),
		},
		PredictedMetrics: PredictedMetrics{
			TargetTime: targetTime.Format(time.RFC3339),
			Confidence: predResp.Confidence,
		},
		Trend:        predResp.Trend,
		ModelUsed:    predResp.ModelUsed,
		ModelVersion: predResp.ModelVersion,
	}

	// Set predicted metrics based on requested metric type
	switch input.Metric {
	case "cpu_usage":
		output.PredictedMetrics.CPUPercent = predResp.PredictedCPU
	case "memory_usage":
		output.PredictedMetrics.MemoryPercent = predResp.PredictedMemory
	default: // "both"
		output.PredictedMetrics.CPUPercent = predResp.PredictedCPU
		output.PredictedMetrics.MemoryPercent = predResp.PredictedMemory
	}

	// Generate recommendation using CE's Prometheus-based current metrics
	output.Recommendation = t.generateRecommendation(
		input.Metric,
		predResp.CurrentCPU,    // Use CE's Prometheus data
		predResp.CurrentMemory, // Use CE's Prometheus data
		predResp.PredictedCPU,
		predResp.PredictedMemory,
		predResp.Trend,
	)

	// Use response recommendation if available and we don't have one
	if output.Recommendation == "" && predResp.Recommendation != "" {
		output.Recommendation = predResp.Recommendation
	}

	return output, nil
}

// parseTargetDatetime parses the target time and date, applying defaults if not provided
func (t *PredictResourceUsageTool) parseTargetDatetime(targetTime, targetDate string) (time.Time, error) {
	now := time.Now()

	// Default date is today
	if targetDate == "" {
		targetDate = now.Format("2006-01-02")
	}

	// Default time is current hour + 1
	if targetTime == "" {
		nextHour := now.Add(time.Hour)
		targetTime = fmt.Sprintf("%02d:00", nextHour.Hour())
	}

	// Parse the combined datetime
	datetimeStr := fmt.Sprintf("%s %s", targetDate, targetTime)
	parsedTime, err := time.Parse("2006-01-02 15:04", datetimeStr)
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to parse datetime '%s': %w", datetimeStr, err)
	}

	return parsedTime, nil
}

// determineTarget determines the target name based on scope and input
func (t *PredictResourceUsageTool) determineTarget(input PredictResourceUsageInput) (string, error) {
	switch input.Scope {
	case "pod":
		if input.Pod == "" {
			return "", fmt.Errorf("pod name is required when scope is 'pod'")
		}
		if input.Namespace != "" {
			return fmt.Sprintf("%s/%s", input.Namespace, input.Pod), nil
		}
		return input.Pod, nil
	case "deployment":
		if input.Deployment == "" {
			return "", fmt.Errorf("deployment name is required when scope is 'deployment'")
		}
		if input.Namespace != "" {
			return fmt.Sprintf("%s/%s", input.Namespace, input.Deployment), nil
		}
		return input.Deployment, nil
	case "namespace":
		if input.Namespace == "" {
			return "all-namespaces", nil
		}
		return input.Namespace, nil
	case "cluster":
		return "cluster-wide", nil
	default:
		return "", fmt.Errorf("invalid scope: %s", input.Scope)
	}
}

// getCurrentMetrics retrieves current metrics for the target scope
func (t *PredictResourceUsageTool) getCurrentMetrics(ctx context.Context, input PredictResourceUsageInput) (*CurrentMetrics, error) {
	// Get metrics based on scope
	switch input.Scope {
	case "cluster":
		return t.getClusterMetrics(ctx)
	case "namespace":
		return t.getNamespaceMetrics(ctx, input.Namespace)
	case "deployment":
		return t.getDeploymentMetrics(ctx, input.Namespace, input.Deployment)
	case "pod":
		return t.getPodMetrics(ctx, input.Namespace, input.Pod)
	default:
		return t.getClusterMetrics(ctx)
	}
}

// getClusterMetrics retrieves cluster-wide metrics
func (t *PredictResourceUsageTool) getClusterMetrics(ctx context.Context) (*CurrentMetrics, error) {
	// Get cluster health which includes node metrics
	health, err := t.k8sClient.GetClusterHealth(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get cluster health: %w", err)
	}

	// Calculate cluster-wide CPU and memory usage from node readiness ratio
	// This is a simplified approach - in production, you'd query Prometheus directly
	nodeReadyRatio := float64(health.Nodes.Ready) / float64(max(health.Nodes.Total, 1))
	podRunningRatio := float64(health.Pods.Running) / float64(max(health.Pods.Total, 1))

	// Estimate CPU and memory based on cluster state
	// These are approximations based on cluster health indicators
	cpuPercent := (1 - nodeReadyRatio) * 100 * 0.5 // Higher when nodes are not ready
	memoryPercent := podRunningRatio * 60          // Base memory usage scales with pods

	// Ensure reasonable bounds
	cpuPercent = clamp(cpuPercent, 0, 100)
	memoryPercent = clamp(memoryPercent, 0, 100)

	return &CurrentMetrics{
		CPUPercent:    cpuPercent,
		MemoryPercent: memoryPercent,
		Timestamp:     time.Now().UTC().Format(time.RFC3339),
	}, nil
}

// getNamespaceMetrics retrieves namespace-scoped metrics
func (t *PredictResourceUsageTool) getNamespaceMetrics(ctx context.Context, namespace string) (*CurrentMetrics, error) {
	// Get pods in namespace
	podList, err := t.k8sClient.ListPods(ctx, namespace)
	if err != nil {
		return nil, fmt.Errorf("failed to list pods in namespace %s: %w", namespace, err)
	}

	// Calculate metrics from pod states
	var runningPods, totalPods int
	for _, pod := range podList.Items {
		totalPods++
		if pod.Status.Phase == "Running" {
			runningPods++
		}
	}

	// Estimate usage based on pod density and states
	runningRatio := float64(runningPods) / float64(max(totalPods, 1))
	cpuPercent := runningRatio * 50 // Base CPU usage
	memoryPercent := runningRatio * 60 // Base memory usage

	// Adjust for infrastructure namespaces which typically have higher usage
	if strings.HasPrefix(namespace, "openshift-") || strings.HasPrefix(namespace, "kube-") {
		cpuPercent *= 1.3
		memoryPercent *= 1.2
	}

	cpuPercent = clamp(cpuPercent, 0, 100)
	memoryPercent = clamp(memoryPercent, 0, 100)

	return &CurrentMetrics{
		CPUPercent:    cpuPercent,
		MemoryPercent: memoryPercent,
		Timestamp:     time.Now().UTC().Format(time.RFC3339),
	}, nil
}

// getDeploymentMetrics retrieves deployment-scoped metrics
func (t *PredictResourceUsageTool) getDeploymentMetrics(ctx context.Context, namespace, deployment string) (*CurrentMetrics, error) {
	// Get pods for the deployment
	podList, err := t.k8sClient.ListPods(ctx, namespace)
	if err != nil {
		return nil, fmt.Errorf("failed to list pods: %w", err)
	}

	// Filter pods belonging to the deployment
	var runningPods, totalPods int
	for _, pod := range podList.Items {
		// Check if pod belongs to deployment (simplified check based on naming)
		if strings.Contains(pod.Name, deployment) {
			totalPods++
			if pod.Status.Phase == "Running" {
				runningPods++
			}
		}
	}

	if totalPods == 0 {
		return nil, fmt.Errorf("no pods found for deployment %s", deployment)
	}

	runningRatio := float64(runningPods) / float64(totalPods)
	cpuPercent := runningRatio * 45
	memoryPercent := runningRatio * 55

	cpuPercent = clamp(cpuPercent, 0, 100)
	memoryPercent = clamp(memoryPercent, 0, 100)

	return &CurrentMetrics{
		CPUPercent:    cpuPercent,
		MemoryPercent: memoryPercent,
		Timestamp:     time.Now().UTC().Format(time.RFC3339),
	}, nil
}

// getPodMetrics retrieves pod-scoped metrics
func (t *PredictResourceUsageTool) getPodMetrics(ctx context.Context, namespace, podName string) (*CurrentMetrics, error) {
	// Get pods to find the specific one
	podList, err := t.k8sClient.ListPods(ctx, namespace)
	if err != nil {
		return nil, fmt.Errorf("failed to list pods: %w", err)
	}

	// Find the specific pod
	for _, pod := range podList.Items {
		if pod.Name == podName || strings.HasPrefix(pod.Name, podName) {
			// Estimate metrics based on pod state
			var cpuPercent, memoryPercent float64
			switch pod.Status.Phase {
			case "Running":
				cpuPercent = 40
				memoryPercent = 50
			case "Pending":
				cpuPercent = 10
				memoryPercent = 20
			case "Failed", "Unknown":
				cpuPercent = 5
				memoryPercent = 10
			default:
				cpuPercent = 30
				memoryPercent = 40
			}

			return &CurrentMetrics{
				CPUPercent:    cpuPercent,
				MemoryPercent: memoryPercent,
				Timestamp:     time.Now().UTC().Format(time.RFC3339),
			}, nil
		}
	}

	return nil, fmt.Errorf("pod %s not found", podName)
}

// generateRecommendation generates a natural language recommendation based on predictions
func (t *PredictResourceUsageTool) generateRecommendation(
	metric string,
	currentCPU, currentMemory float64,
	predictedCPU, predictedMemory float64,
	trend string,
) string {
	var recommendations []string

	// CPU recommendations
	if metric == "cpu_usage" || metric == "both" {
		cpuChange := predictedCPU - currentCPU
		if predictedCPU >= 90 {
			recommendations = append(recommendations,
				fmt.Sprintf("CRITICAL: CPU predicted to reach %.1f%%. Consider immediate scaling or resource allocation.", predictedCPU))
		} else if predictedCPU >= 80 {
			recommendations = append(recommendations,
				fmt.Sprintf("WARNING: CPU predicted to reach %.1f%%. Plan for scaling within the prediction window.", predictedCPU))
		} else if cpuChange > 20 {
			recommendations = append(recommendations,
				fmt.Sprintf("CPU usage expected to increase by %.1f%% (from %.1f%% to %.1f%%). Monitor closely.", cpuChange, currentCPU, predictedCPU))
		}
	}

	// Memory recommendations
	if metric == "memory_usage" || metric == "both" {
		memChange := predictedMemory - currentMemory
		if predictedMemory >= 90 {
			recommendations = append(recommendations,
				fmt.Sprintf("CRITICAL: Memory predicted to reach %.1f%%. Risk of OOM conditions. Scale up urgently.", predictedMemory))
		} else if predictedMemory >= 85 {
			recommendations = append(recommendations,
				fmt.Sprintf("WARNING: Memory approaching %.1f%% threshold. Consider scaling or monitoring.", predictedMemory))
		} else if memChange > 20 {
			recommendations = append(recommendations,
				fmt.Sprintf("Memory usage expected to increase by %.1f%% (from %.1f%% to %.1f%%). Monitor for potential issues.", memChange, currentMemory, predictedMemory))
		}
	}

	// Trend-based recommendations
	if len(recommendations) == 0 {
		switch trend {
		case "upward":
			recommendations = append(recommendations,
				"Resource usage trending upward. Continue monitoring and prepare for potential scaling.")
		case "downward":
			recommendations = append(recommendations,
				"Resource usage trending downward. Consider scaling down to optimize costs.")
		default: // stable
			recommendations = append(recommendations,
				"Resource usage stable. Current allocation appears appropriate.")
		}
	}

	return strings.Join(recommendations, " ")
}

// Helper functions

// max returns the maximum of two integers
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// clamp restricts a value to a range
func clamp(value, minVal, maxVal float64) float64 {
	if value < minVal {
		return minVal
	}
	if value > maxVal {
		return maxVal
	}
	return value
}
