package tools

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// GetRemediationRecommendationsTool provides ML-powered remediation recommendations
// This tool uses the Coordination Engine's AnalyzeAnomalies API with predictions enabled
type GetRemediationRecommendationsTool struct {
	ceClient *clients.CoordinationEngineClient
}

// NewGetRemediationRecommendationsTool creates a new remediation recommendations tool
func NewGetRemediationRecommendationsTool(ceClient *clients.CoordinationEngineClient) *GetRemediationRecommendationsTool {
	return &GetRemediationRecommendationsTool{
		ceClient: ceClient,
	}
}

// Name returns the tool name for MCP registration
func (t *GetRemediationRecommendationsTool) Name() string {
	return "get-remediation-recommendations"
}

// Description returns the tool description for MCP
func (t *GetRemediationRecommendationsTool) Description() string {
	return "Get ML-powered remediation recommendations and predictions from Coordination Engine - predict issues before they occur and get proactive remediation suggestions"
}

// InputSchema returns the JSON schema for tool inputs
func (t *GetRemediationRecommendationsTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"timeframe": map[string]interface{}{
				"type":        "string",
				"description": "Time window for analysis (1h, 6h, 24h)",
				"enum":        []string{"1h", "6h", "24h"},
				"default":     "6h",
			},
			"include_predictions": map[string]interface{}{
				"type":        "boolean",
				"description": "Enable ML predictions (true for proactive recommendations)",
				"default":     true,
			},
			"confidence_threshold": map[string]interface{}{
				"type":        "number",
				"description": "Minimum confidence threshold for predictions (0.0-1.0)",
				"minimum":     0.0,
				"maximum":     1.0,
				"default":     0.7,
			},
		},
		"required": []string{},
	}
}

// GetRemediationRecommendationsInput represents the input parameters
type GetRemediationRecommendationsInput struct {
	Timeframe            string  `json:"timeframe"`
	IncludePredictions   bool    `json:"include_predictions"`
	ConfidenceThreshold  float64 `json:"confidence_threshold"`
}

// GetRemediationRecommendationsOutput represents the tool output
type GetRemediationRecommendationsOutput struct {
	Status            string                     `json:"status"`
	Timeframe         string                     `json:"timeframe"`
	PredictionsEnabled bool                      `json:"predictions_enabled"`
	Threshold         float64                    `json:"threshold"`
	Recommendations   []string                   `json:"recommendations"`
	PredictedIssues   []clients.AnomalyPattern   `json:"predicted_issues,omitempty"`
	Alerts            []clients.Alert            `json:"alerts,omitempty"`
	Summary           map[string]interface{}     `json:"summary"`
	AnalyzedAt        string                     `json:"analyzed_at"`
}

// Execute runs the remediation recommendations analysis
func (t *GetRemediationRecommendationsTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments
	input := GetRemediationRecommendationsInput{
		Timeframe:           "6h",   // Default
		IncludePredictions:  true,   // Default - enable ML predictions
		ConfidenceThreshold: 0.7,    // Default
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Use defaults if unmarshal fails
	}

	// Build request to Coordination Engine
	req := &clients.AnalyzeAnomaliesRequest{
		TimeRange:          input.Timeframe,
		Metrics:            []interface{}{"cpu", "memory", "disk", "network"}, // Standard metrics
		Threshold:          &input.ConfidenceThreshold,
		IncludePredictions: &input.IncludePredictions,
	}

	// Call Coordination Engine API
	resp, err := t.ceClient.AnalyzeAnomalies(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("failed to get recommendations from Coordination Engine: %w", err)
	}

	// Build output
	output := GetRemediationRecommendationsOutput{
		Status:             resp.Status,
		Timeframe:          resp.TimeRange,
		PredictionsEnabled: input.IncludePredictions,
		Threshold:          resp.Threshold,
		Recommendations:    resp.Recommendations,
		Alerts:             resp.Alerts,
		AnalyzedAt:         resp.AnalyzedAt,
		Summary: map[string]interface{}{
			"total_metrics_analyzed": resp.Summary.TotalMetricsAnalyzed,
			"anomalies_found":        resp.Summary.AnomaliesFound,
			"models_used":            resp.Summary.ModelsUsed,
			"by_severity":            resp.Summary.BySeverity,
		},
	}

	// If predictions enabled, include predicted issues
	if input.IncludePredictions && len(resp.Patterns) > 0 {
		output.PredictedIssues = resp.Patterns
	}

	return output, nil
}
