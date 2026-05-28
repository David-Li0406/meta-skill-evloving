package tools

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// GetModelStatusTool provides MCP tool for checking KServe model status
type GetModelStatusTool struct {
	kserveClient *clients.KServeClient
}

// NewGetModelStatusTool creates a new get-model-status tool
func NewGetModelStatusTool(kserveClient *clients.KServeClient) *GetModelStatusTool {
	return &GetModelStatusTool{
		kserveClient: kserveClient,
	}
}

// Name returns the tool name
func (t *GetModelStatusTool) Name() string {
	return "get-model-status"
}

// Description returns the tool description
func (t *GetModelStatusTool) Description() string {
	return "Get the status and metadata of a KServe InferenceService model. Returns readiness status, version, runtime information, and replica counts."
}

// InputSchema returns the JSON schema for tool inputs
func (t *GetModelStatusTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"model_name": map[string]interface{}{
				"type":        "string",
				"description": "The name of the KServe InferenceService to check",
			},
			"include_endpoints": map[string]interface{}{
				"type":        "boolean",
				"description": "Include detailed endpoint information",
				"default":     true,
			},
		},
		"required": []string{"model_name"},
	}
}

// GetModelStatusInput represents the input parameters
type GetModelStatusInput struct {
	ModelName        string `json:"model_name"`
	IncludeEndpoints bool   `json:"include_endpoints"`
}

// ModelEndpoint represents an endpoint configuration
type ModelEndpoint struct {
	URL      string `json:"url"`
	Type     string `json:"type"` // predictor, transformer, explainer
	Ready    bool   `json:"ready"`
	Replicas int    `json:"replicas"`
}

// GetModelStatusOutput represents the tool output
type GetModelStatusOutput struct {
	Status            string          `json:"status"`
	ModelName         string          `json:"model_name"`
	Ready             bool            `json:"ready"`
	State             string          `json:"state"`
	Runtime           string          `json:"runtime"`
	Version           string          `json:"version"`
	Framework         string          `json:"framework"`
	Namespace         string          `json:"namespace"`
	Replicas          int             `json:"replicas"`
	AvailableReplicas int             `json:"available_replicas"`
	Endpoints         []ModelEndpoint `json:"endpoints,omitempty"`
	LastUpdated       string          `json:"last_updated"`
	Message           string          `json:"message"`
	Details           interface{}     `json:"details,omitempty"`
}

// Execute runs the get-model-status tool
func (t *GetModelStatusTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments with defaults
	input := GetModelStatusInput{
		IncludeEndpoints: true,
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Intentionally ignore error, use defaults if unmarshal fails
	}

	// Validate required fields
	if input.ModelName == "" {
		return nil, fmt.Errorf("model_name is required")
	}

	// Get model status from KServe
	modelStatus, err := t.kserveClient.GetModelStatus(ctx, input.ModelName)
	if err != nil {
		return nil, fmt.Errorf("failed to get model status: %w", err)
	}

	// Build endpoints list if requested
	var endpoints []ModelEndpoint
	if input.IncludeEndpoints && modelStatus.URL != "" {
		endpoints = []ModelEndpoint{
			{
				URL:      modelStatus.URL,
				Type:     "predictor",
				Ready:    modelStatus.Ready,
				Replicas: modelStatus.Replicas,
			},
		}
	}

	// Build output
	output := GetModelStatusOutput{
		Status:            "success",
		ModelName:         input.ModelName,
		Ready:             modelStatus.Ready,
		State:             determineState(modelStatus.Ready, modelStatus.Replicas, modelStatus.AvailableReplicas),
		Runtime:           modelStatus.Runtime,
		Version:           modelStatus.ModelVersion,
		Framework:         modelStatus.Framework,
		Namespace:         t.kserveClient.GetNamespace(),
		Replicas:          modelStatus.Replicas,
		AvailableReplicas: modelStatus.AvailableReplicas,
		Endpoints:         endpoints,
		LastUpdated:       modelStatus.LastTransitionTime,
		Details:           modelStatus.Conditions,
	}

	// Generate status message
	if modelStatus.Ready {
		output.Message = fmt.Sprintf("Model '%s' is ready and serving (replicas: %d/%d)",
			input.ModelName, modelStatus.AvailableReplicas, modelStatus.Replicas)
	} else {
		output.Message = fmt.Sprintf("Model '%s' is not ready (state: %s, replicas: %d/%d)",
			input.ModelName, output.State, modelStatus.AvailableReplicas, modelStatus.Replicas)
	}

	return output, nil
}

// determineState calculates the overall state of the model
func determineState(ready bool, replicas, availableReplicas int) string {
	if ready && availableReplicas == replicas && replicas > 0 {
		return "Running"
	} else if availableReplicas > 0 && availableReplicas < replicas {
		return "Degraded"
	} else if availableReplicas == 0 {
		return "Starting"
	} else if !ready {
		return "NotReady"
	}
	return "Unknown"
}
