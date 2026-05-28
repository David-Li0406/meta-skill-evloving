package tools

import (
	"context"
	"fmt"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// ListModelsTool lists available KServe InferenceService models
type ListModelsTool struct {
	kserve *clients.KServeClient
}

// NewListModelsTool creates a new list models tool
func NewListModelsTool(kserve *clients.KServeClient) *ListModelsTool {
	return &ListModelsTool{
		kserve: kserve,
	}
}

// Name returns the tool name for MCP registration
func (t *ListModelsTool) Name() string {
	return "list-models"
}

// Description returns the tool description for MCP
func (t *ListModelsTool) Description() string {
	return "List all available KServe InferenceService models in the namespace. Use this tool when the user asks 'what models are available', 'show me models', or wants to know model names before checking specific model status."
}

// InputSchema returns the JSON schema for tool inputs
func (t *ListModelsTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type":       "object",
		"properties": map[string]interface{}{},
		"required":   []string{},
	}
}

// ListModelsOutput represents the tool output
type ListModelsOutput struct {
	Models      []ModelInfo `json:"models"`
	TotalCount  int         `json:"total_count"`
	Namespace   string      `json:"namespace"`
	Message     string      `json:"message,omitempty"`
	Suggestions []string    `json:"suggestions,omitempty"`
}

// ModelInfo contains information about a model
type ModelInfo struct {
	Name    string `json:"name"`
	Ready   bool   `json:"ready"`
	URL     string `json:"url,omitempty"`
	Runtime string `json:"runtime,omitempty"`
}

// Execute lists all KServe models
func (t *ListModelsTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	if t.kserve == nil {
		return nil, fmt.Errorf("KServe client not configured - ensure ENABLE_KSERVE=true")
	}

	// Get all InferenceServices from KServe
	services, err := t.kserve.ListInferenceServices(ctx)
	if err != nil {
		return &ListModelsOutput{
			Message: fmt.Sprintf("Failed to list models: %v", err),
			Suggestions: []string{
				"Check if KServe is installed in the namespace",
				"Verify RBAC permissions for listing InferenceServices",
			},
		}, nil
	}

	// Build model info list
	models := []ModelInfo{}
	for _, svc := range services {
		info := ModelInfo{
			Name:    svc.Name,
			Ready:   svc.Status.IsReady,
			URL:     svc.Status.URL,
			Runtime: svc.Spec.Predictor.GetRuntime(),
		}
		models = append(models, info)
	}

	output := &ListModelsOutput{
		Models:     models,
		TotalCount: len(models),
		Namespace:  t.kserve.GetNamespace(),
	}

	// Add helpful suggestions based on results
	if len(models) == 0 {
		output.Message = "No KServe models found in this namespace"
		output.Suggestions = []string{
			"Deploy a KServe InferenceService to get started",
			"Check if you're looking in the correct namespace",
		}
	} else {
		readyCount := 0
		for _, m := range models {
			if m.Ready {
				readyCount++
			}
		}
		output.Message = fmt.Sprintf("Found %d models (%d ready, %d not ready)",
			len(models), readyCount, len(models)-readyCount)

		// Suggest next steps
		if readyCount > 0 {
			output.Suggestions = []string{
				fmt.Sprintf("Use 'get-model-status' with model_name='%s' for detailed status", models[0].Name),
				"Use 'analyze-anomalies' to run ML-powered anomaly detection",
			}
		} else {
			output.Suggestions = []string{
				"Some models are not ready - check their status for details",
				"Use 'get-model-status' to see why models aren't ready",
			}
		}
	}

	return output, nil
}
