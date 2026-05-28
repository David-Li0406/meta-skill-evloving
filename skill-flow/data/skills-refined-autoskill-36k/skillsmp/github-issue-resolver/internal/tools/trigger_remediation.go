package tools

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// TriggerRemediationTool provides MCP tool for triggering remediation actions
type TriggerRemediationTool struct {
	ceClient *clients.CoordinationEngineClient
}

// NewTriggerRemediationTool creates a new trigger-remediation tool
func NewTriggerRemediationTool(ceClient *clients.CoordinationEngineClient) *TriggerRemediationTool {
	return &TriggerRemediationTool{
		ceClient: ceClient,
	}
}

// Name returns the tool name
func (t *TriggerRemediationTool) Name() string {
	return "trigger-remediation"
}

// Description returns the tool description
func (t *TriggerRemediationTool) Description() string {
	return "Trigger automated remediation actions for incidents through the Coordination Engine. Supports actions like scale_deployment, restart_pod, clear_alerts, and more. Can be run in dry-run mode for safety."
}

// InputSchema returns the JSON schema for tool inputs
func (t *TriggerRemediationTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"incident_id": map[string]interface{}{
				"type":        "string",
				"description": "The ID of the incident to remediate",
			},
			"action": map[string]interface{}{
				"type":        "string",
				"description": "The remediation action to trigger",
				"enum": []string{
					"scale_deployment",
					"restart_pod",
					"clear_alerts",
					"run_inference",
					"scale_up",
					"scale_down",
					"remediate_node",
					"correlate_alerts",
				},
			},
			"parameters": map[string]interface{}{
				"type":        "object",
				"description": "Action-specific parameters",
				"properties": map[string]interface{}{
					"target_replicas": map[string]interface{}{
						"type":        "integer",
						"description": "Target number of replicas (for scaling actions)",
					},
					"deployment_name": map[string]interface{}{
						"type":        "string",
						"description": "Name of deployment to scale",
					},
					"pod_name": map[string]interface{}{
						"type":        "string",
						"description": "Name of pod to restart",
					},
					"namespace": map[string]interface{}{
						"type":        "string",
						"description": "Kubernetes namespace",
					},
					"grace_period": map[string]interface{}{
						"type":        "integer",
						"description": "Grace period in seconds for pod termination",
						"default":     30,
					},
					"restart_strategy": map[string]interface{}{
						"type":        "string",
						"description": "Restart strategy (rolling, immediate)",
						"enum":        []string{"rolling", "immediate"},
						"default":     "rolling",
					},
				},
			},
			"priority": map[string]interface{}{
				"type":        "integer",
				"description": "Action priority (1-10, higher is more urgent)",
				"default":     8,
				"minimum":     1,
				"maximum":     10,
			},
			"confidence": map[string]interface{}{
				"type":        "number",
				"description": "Confidence score for this action (0.0-1.0)",
				"default":     0.9,
				"minimum":     0.0,
				"maximum":     1.0,
			},
			"dry_run": map[string]interface{}{
				"type":        "boolean",
				"description": "If true, validate action without executing it",
				"default":     false,
			},
		},
		"required": []string{"incident_id", "action"},
	}
}

// TriggerRemediationInput represents the input parameters
type TriggerRemediationInput struct {
	IncidentID string                 `json:"incident_id"`
	Action     string                 `json:"action"`
	Parameters map[string]interface{} `json:"parameters"`
	Priority   int                    `json:"priority"`
	Confidence float64                `json:"confidence"`
	DryRun     bool                   `json:"dry_run"`
}

// TriggerRemediationOutput represents the tool output
type TriggerRemediationOutput struct {
	Status            string                 `json:"status"`
	ActionID          string                 `json:"action_id"`
	IncidentID        string                 `json:"incident_id"`
	Action            string                 `json:"action"`
	Description       string                 `json:"description"`
	Priority          int                    `json:"priority"`
	Confidence        float64                `json:"confidence"`
	Parameters        map[string]interface{} `json:"parameters"`
	ExecutedAt        string                 `json:"executed_at"`
	EstimatedDuration string                 `json:"estimated_duration"`
	Message           string                 `json:"message"`
	DryRun            bool                   `json:"dry_run,omitempty"`
}

// Execute runs the trigger-remediation tool
func (t *TriggerRemediationTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments
	input := TriggerRemediationInput{
		Priority:   8,
		Confidence: 0.9,
		DryRun:     false,
		Parameters: make(map[string]interface{}),
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Intentionally ignore error, use defaults if unmarshal fails
	}

	// Validate required fields
	if input.IncidentID == "" {
		return nil, fmt.Errorf("incident_id is required")
	}
	if input.Action == "" {
		return nil, fmt.Errorf("action is required")
	}

	// Build remediation request
	req := &clients.TriggerRemediationRequest{
		IncidentID: input.IncidentID,
		Action:     input.Action,
		Parameters: input.Parameters,
		Priority:   &input.Priority,
		Confidence: &input.Confidence,
		DryRun:     &input.DryRun,
	}

	// Call Coordination Engine API
	resp, err := t.ceClient.TriggerRemediation(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("failed to trigger remediation: %w", err)
	}

	// Build output
	output := TriggerRemediationOutput{
		Status:            "success",
		ActionID:          resp.ActionID,
		IncidentID:        resp.IncidentID,
		Action:            resp.Type,
		Description:       resp.Description,
		Priority:          resp.Priority,
		Confidence:        resp.Confidence,
		Parameters:        resp.Parameters,
		ExecutedAt:        resp.ExecutedAt,
		EstimatedDuration: resp.EstimatedDuration,
		Message:           resp.Result,
		DryRun:            input.DryRun,
	}

	if input.DryRun {
		output.Message = fmt.Sprintf("DRY RUN: Remediation action '%s' validated successfully (not executed)", input.Action)
	} else {
		output.Message = fmt.Sprintf("Remediation action '%s' triggered successfully (ID: %s)", input.Action, resp.ActionID)
	}

	return output, nil
}
