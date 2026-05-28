package tools

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// AnalyzeAnomaliesTool provides MCP tool for ML-powered anomaly detection
type AnalyzeAnomaliesTool struct {
	kserveClient        *clients.KServeClient
	coordinationEngine  *clients.CoordinationEngineClient
}

// NewAnalyzeAnomaliesTool creates a new analyze-anomalies tool
func NewAnalyzeAnomaliesTool(kserveClient *clients.KServeClient, coordinationEngine *clients.CoordinationEngineClient) *AnalyzeAnomaliesTool {
	return &AnalyzeAnomaliesTool{
		kserveClient:       kserveClient,
		coordinationEngine: coordinationEngine,
	}
}

// Name returns the tool name
func (t *AnalyzeAnomaliesTool) Name() string {
	return "analyze-anomalies"
}

// Description returns the tool description
func (t *AnalyzeAnomaliesTool) Description() string {
	return `Detect anomalies in cluster resource usage using ML models (Isolation Forest) via the Coordination Engine.

RESPONSE INTERPRETATION:
- anomalies[].anomaly_score: Score from 0.0 to 1.0 (higher = more anomalous)
- anomalies[].severity: Classification - "low", "medium", "high", "critical"
- anomaly_count: Total number of anomalies detected above threshold
- max_score: Highest anomaly score found in the analysis period
- average_score: Mean anomaly score across all detected anomalies
- filter_target: What was analyzed (e.g., "deployment 'sample-app' in namespace 'default'")

PRESENTATION TO USER:
- If anomaly_count=0: "No anomalies detected. Cluster metrics appear normal for [filter_target]."
- If anomaly_count>0: "Detected [N] anomalies in [metric] for [filter_target] (max severity: [severity])"
- Always include the recommendation field in your response
- For high/critical severity: Emphasize urgency and suggest immediate investigation
- For memory-related anomalies: Suggest checking pod memory limits and potential memory leaks
- For CPU-related anomalies: Suggest checking for runaway processes or scaling needs

FILTERING OPTIONS:
- namespace: Scope to a specific namespace
- deployment: Analyze specific deployment (mutually exclusive with pod)
- pod: Analyze specific pod (mutually exclusive with deployment)
- label selector: Filter by Kubernetes labels (e.g., 'app=flask')

Example questions this tool answers:
- "Are there any anomalies in CPU usage?"
- "Check for anomalies in the openshift-monitoring namespace"
- "Analyze memory_usage for the sample-flask-app deployment"`
}

// InputSchema returns the JSON schema for tool inputs
func (t *AnalyzeAnomaliesTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"metric": map[string]interface{}{
				"type":        "string",
				"description": "The metric name to analyze (e.g., 'cpu_usage', 'memory_usage', 'pod_restarts')",
			},
			"namespace": map[string]interface{}{
				"type":        "string",
				"description": "Kubernetes namespace to scope the analysis (optional)",
			},
			"deployment": map[string]interface{}{
				"type":        "string",
				"description": "Specific deployment name to filter anomalies for (e.g., 'sample-flask-app'). Mutually exclusive with 'pod'.",
			},
			"pod": map[string]interface{}{
				"type":        "string",
				"description": "Specific pod name to filter anomalies for (e.g., 'etcd-0', 'prometheus-k8s-0'). Mutually exclusive with 'deployment'.",
			},
			"label_selector": map[string]interface{}{
				"type":        "string",
				"description": "Kubernetes label selector to filter pods (e.g., 'app=flask', 'component=etcd'). Can combine with namespace.",
			},
			"time_range": map[string]interface{}{
				"type":        "string",
				"description": "Time range for analysis",
				"enum":        []string{"1h", "6h", "24h", "7d"},
				"default":     "1h",
			},
			"threshold": map[string]interface{}{
				"type":        "number",
				"description": "Anomaly score threshold (0.0-1.0). Values above this are reported.",
				"default":     0.7,
				"minimum":     0.0,
				"maximum":     1.0,
			},
			"model_name": map[string]interface{}{
				"type":        "string",
				"description": "KServe model name to use for prediction",
				"default":     "predictive-analytics",
			},
		},
		"required": []string{"metric"},
	}
}

// AnalyzeAnomaliesInput represents the input parameters
type AnalyzeAnomaliesInput struct {
	Metric        string  `json:"metric"`
	Namespace     string  `json:"namespace"`
	Deployment    string  `json:"deployment"`
	Pod           string  `json:"pod"`
	LabelSelector string  `json:"label_selector"`
	TimeRange     string  `json:"time_range"`
	Threshold     float64 `json:"threshold"`
	ModelName     string  `json:"model_name"`
}

// AnomalyResult represents a detected anomaly
type AnomalyResult struct {
	Timestamp    string  `json:"timestamp"`
	MetricName   string  `json:"metric_name"`
	Value        float64 `json:"value"`
	AnomalyScore float64 `json:"anomaly_score"`
	Confidence   float64 `json:"confidence"`
	Severity     string  `json:"severity"`
	Explanation  string  `json:"explanation"`
}

// AnalyzeAnomaliesOutput represents the tool output
type AnalyzeAnomaliesOutput struct {
	Status         string          `json:"status"`
	Metric         string          `json:"metric"`
	TimeRange      string          `json:"time_range"`
	Namespace      string          `json:"namespace,omitempty"`
	Deployment     string          `json:"deployment,omitempty"`
	Pod            string          `json:"pod,omitempty"`
	LabelSelector  string          `json:"label_selector,omitempty"`
	FilterTarget   string          `json:"filter_target,omitempty"`
	ModelUsed      string          `json:"model_used"`
	Anomalies      []AnomalyResult `json:"anomalies"`
	AnomalyCount   int             `json:"anomaly_count"`
	MaxScore       float64         `json:"max_score"`
	AverageScore   float64         `json:"average_score"`
	Message        string          `json:"message"`
	Recommendation string          `json:"recommendation,omitempty"`
}

// Execute runs the analyze-anomalies tool
func (t *AnalyzeAnomaliesTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments with defaults
	input := AnalyzeAnomaliesInput{
		TimeRange: "1h",
		Threshold: 0.7,
		ModelName: "anomaly-detector",
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Intentionally ignore error, use defaults if unmarshal fails
	}

	// Validate required fields
	if input.Metric == "" {
		return nil, fmt.Errorf("metric is required")
	}

	// Validate mutual exclusivity of deployment and pod filters
	if err := t.validateFilters(input); err != nil {
		return nil, err
	}

	// Determine filter target description
	filterTarget := t.determineFilterTarget(input)

	// Call Coordination Engine for anomaly analysis
	// The Coordination Engine handles:
	// 1. Querying Prometheus for the 5 base metrics
	// 2. Feature engineering (45 features: 5 metrics × 9 features each)
	// 3. Calling KServe with properly formatted numeric arrays
	threshold := input.Threshold
	ceRequest := &clients.AnalyzeAnomaliesRequest{
		TimeRange:     input.TimeRange,
		Metrics:       []interface{}{input.Metric},
		Threshold:     &threshold,
		ModelName:     input.ModelName,
		Namespace:     input.Namespace,
		Deployment:    input.Deployment,
		Pod:           input.Pod,
		LabelSelector: input.LabelSelector,
	}

	ceResponse, err := t.coordinationEngine.AnalyzeAnomalies(ctx, ceRequest)
	if err != nil {
		return nil, fmt.Errorf("failed to get anomaly predictions: %w", err)
	}

	// Convert coordination engine response to tool output format
	anomalies := []AnomalyResult{}
	var totalScore float64
	var maxScore float64

	for _, pattern := range ceResponse.Patterns {
		anomaly := AnomalyResult{
			Timestamp:    pattern.Timestamp,
			MetricName:   pattern.Metric,
			Value:        pattern.Value,
			AnomalyScore: pattern.Score,
			Confidence:   pattern.Score, // Use score as confidence if not separately provided
			Severity:     pattern.Severity,
			Explanation:  generateExplanation(pattern.Metric, pattern.Score, pattern.Score),
		}
		anomalies = append(anomalies, anomaly)
		totalScore += pattern.Score
		if pattern.Score > maxScore {
			maxScore = pattern.Score
		}
	}

	// Calculate statistics
	avgScore := 0.0
	if len(anomalies) > 0 {
		avgScore = totalScore / float64(len(anomalies))
	}

	// Determine model used from response or input
	modelUsed := input.ModelName
	if len(ceResponse.Summary.ModelsUsed) > 0 {
		modelUsed = strings.Join(ceResponse.Summary.ModelsUsed, ", ")
	}

	// Build output
	output := AnalyzeAnomaliesOutput{
		Status:        ceResponse.Status,
		Metric:        input.Metric,
		TimeRange:     ceResponse.TimeRange,
		Namespace:     input.Namespace,
		Deployment:    input.Deployment,
		Pod:           input.Pod,
		LabelSelector: input.LabelSelector,
		FilterTarget:  filterTarget,
		ModelUsed:     modelUsed,
		Anomalies:     anomalies,
		AnomalyCount:  len(anomalies),
		MaxScore:      maxScore,
		AverageScore:  avgScore,
	}

	// Use recommendations from coordination engine if available
	if len(ceResponse.Recommendations) > 0 {
		output.Recommendation = strings.Join(ceResponse.Recommendations, " ")
	}

	// Generate message and recommendation with filter context
	if len(anomalies) == 0 {
		output.Message = fmt.Sprintf("No anomalies detected in %s for %s over the last %s (threshold: %.2f)",
			input.Metric, filterTarget, input.TimeRange, input.Threshold)
		if output.Recommendation == "" {
			output.Recommendation = "Metrics appear normal for the specified target. Continue monitoring."
		}
	} else {
		output.Message = fmt.Sprintf("Detected %d anomalies in %s for %s over the last %s (max score: %.2f)",
			len(anomalies), input.Metric, filterTarget, input.TimeRange, maxScore)
		if output.Recommendation == "" {
			output.Recommendation = generateRecommendation(input.Metric, maxScore, len(anomalies))
		}
	}

	return output, nil
}

// validateFilters validates the mutual exclusivity and combination rules for filters
func (t *AnalyzeAnomaliesTool) validateFilters(input AnalyzeAnomaliesInput) error {
	// Deployment and pod are mutually exclusive
	if input.Deployment != "" && input.Pod != "" {
		return fmt.Errorf("'deployment' and 'pod' filters are mutually exclusive; specify only one")
	}

	// Label selector cannot be combined with deployment or pod
	if input.LabelSelector != "" && (input.Deployment != "" || input.Pod != "") {
		return fmt.Errorf("'label_selector' cannot be combined with 'deployment' or 'pod' filters")
	}

	return nil
}

// determineFilterTarget returns a human-readable description of what is being analyzed
func (t *AnalyzeAnomaliesTool) determineFilterTarget(input AnalyzeAnomaliesInput) string {
	var parts []string

	if input.Pod != "" {
		parts = append(parts, fmt.Sprintf("pod '%s'", input.Pod))
	} else if input.Deployment != "" {
		parts = append(parts, fmt.Sprintf("deployment '%s'", input.Deployment))
	} else if input.LabelSelector != "" {
		parts = append(parts, fmt.Sprintf("pods matching '%s'", input.LabelSelector))
	}

	if input.Namespace != "" {
		if len(parts) > 0 {
			parts = append(parts, fmt.Sprintf("in namespace '%s'", input.Namespace))
		} else {
			parts = append(parts, fmt.Sprintf("namespace '%s'", input.Namespace))
		}
	}

	if len(parts) == 0 {
		return "cluster-wide"
	}

	return strings.Join(parts, " ")
}

// buildPodRegex constructs a regex pattern for pod filtering based on deployment name
func (t *AnalyzeAnomaliesTool) buildPodRegex(input AnalyzeAnomaliesInput) string {
	if input.Deployment != "" {
		// Deployment pods typically have format: {deployment-name}-{replicaset-hash}-{pod-hash}
		// or for StatefulSets: {statefulset-name}-{ordinal}
		return fmt.Sprintf("%s-.*", input.Deployment)
	}
	if input.Pod != "" {
		// For specific pod, use exact match or prefix match for StatefulSets
		// Infrastructure pods like etcd-0 may be matched as prefix
		if strings.HasSuffix(input.Pod, "-0") || strings.HasSuffix(input.Pod, "-1") || strings.HasSuffix(input.Pod, "-2") {
			// Likely a StatefulSet pod, match exactly
			return fmt.Sprintf("^%s$", input.Pod)
		}
		// For other pods, allow prefix matching
		return fmt.Sprintf("^%s.*", input.Pod)
	}
	return ""
}

// Helper functions

func determineSeverity(score float64) string {
	if score >= 0.9 {
		return "critical"
	} else if score >= 0.8 {
		return "high"
	} else if score >= 0.7 {
		return "medium"
	}
	return "low"
}

func generateExplanation(metric string, score, confidence float64) string {
	severity := determineSeverity(score)
	return fmt.Sprintf("Metric '%s' shows %s anomaly (score: %.2f, confidence: %.2f). "+
		"This indicates unusual behavior compared to historical patterns.",
		metric, severity, score, confidence)
}

func generateRecommendation(metric string, maxScore float64, count int) string {
	if maxScore >= 0.9 {
		return fmt.Sprintf("CRITICAL: Immediate investigation recommended. %d high-severity anomalies detected in %s. "+
			"Consider scaling resources or triggering remediation workflows.", count, metric)
	} else if maxScore >= 0.8 {
		return fmt.Sprintf("WARNING: Monitor closely. %d anomalies detected in %s. "+
			"Review recent deployments or configuration changes.", count, metric)
	}
	return fmt.Sprintf("INFO: %d minor anomalies detected in %s. "+
		"Monitor trends and investigate if anomalies persist.", count, metric)
}
