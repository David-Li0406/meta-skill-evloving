package tools

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// CreateIncidentTool allows manual incident creation for tracking
// Useful for creating correlated parent incidents or manually tracking issues
type CreateIncidentTool struct {
	ceClient *clients.CoordinationEngineClient
}

// NewCreateIncidentTool creates a new incident creation tool
func NewCreateIncidentTool(ceClient *clients.CoordinationEngineClient) *CreateIncidentTool {
	return &CreateIncidentTool{
		ceClient: ceClient,
	}
}

// Name returns the tool name for MCP registration
func (t *CreateIncidentTool) Name() string {
	return "create-incident"
}

// Description returns the tool description for MCP
func (t *CreateIncidentTool) Description() string {
	return "Manually create an incident in the Coordination Engine for tracking - useful for correlated parent incidents or manual issue tracking"
}

// InputSchema returns the JSON schema for tool inputs
func (t *CreateIncidentTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"title": map[string]interface{}{
				"type":        "string",
				"description": "Incident title (concise, descriptive)",
				"minLength":   5,
			},
			"description": map[string]interface{}{
				"type":        "string",
				"description": "Detailed incident description",
				"minLength":   10,
			},
			"severity": map[string]interface{}{
				"type":        "string",
				"description": "Incident severity level",
				"enum":        []string{"critical", "high", "medium", "low"},
			},
			"target": map[string]interface{}{
				"type":        "string",
				"description": "Target resource (namespace/pod, deployment, service, or 'multiple' for correlated incidents)",
			},
			"affected_resources": map[string]interface{}{
				"type":        "array",
				"description": "List of affected resources (pods, deployments, nodes, etc.)",
				"items": map[string]interface{}{
					"type": "string",
				},
			},
			"correlation_id": map[string]interface{}{
				"type":        "string",
				"description": "Correlation ID for grouping related incidents (optional)",
			},
			"external_id": map[string]interface{}{
				"type":        "string",
				"description": "External tracking ID (e.g., Jira ticket, ServiceNow incident)",
			},
			"labels": map[string]interface{}{
				"type":        "object",
				"description": "Custom labels for categorization and filtering",
				"additionalProperties": map[string]interface{}{
					"type": "string",
				},
			},
			"confidence": map[string]interface{}{
				"type":        "number",
				"description": "Confidence score if created based on ML prediction (0.0-1.0)",
				"minimum":     0.0,
				"maximum":     1.0,
			},
		},
		"required": []string{"title", "description", "severity"},
	}
}

// CreateIncidentInput represents the input parameters
type CreateIncidentInput struct {
	Title             string            `json:"title"`
	Description       string            `json:"description"`
	Severity          string            `json:"severity"`
	Target            string            `json:"target,omitempty"`
	AffectedResources []string          `json:"affected_resources,omitempty"`
	CorrelationID     string            `json:"correlation_id,omitempty"`
	ExternalID        string            `json:"external_id,omitempty"`
	Labels            map[string]string `json:"labels,omitempty"`
	Confidence        float64           `json:"confidence,omitempty"`
}

// CreateIncidentOutput represents the tool output
type CreateIncidentOutput struct {
	IncidentID  string `json:"incident_id"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Severity    string `json:"severity"`
	Priority    int    `json:"priority"`
	Status      string `json:"status"`
	CreatedAt   string `json:"created_at"`
	Message     string `json:"message"`
}

// Execute creates a new incident
func (t *CreateIncidentTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments
	var input CreateIncidentInput

	argsJSON, err := json.Marshal(args)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal arguments: %w", err)
	}

	if err := json.Unmarshal(argsJSON, &input); err != nil {
		return nil, fmt.Errorf("failed to parse arguments: %w", err)
	}

	// Validate required fields
	if input.Title == "" {
		return nil, fmt.Errorf("title is required")
	}
	if input.Description == "" {
		return nil, fmt.Errorf("description is required")
	}
	if input.Severity == "" {
		return nil, fmt.Errorf("severity is required")
	}

	// Validate severity
	validSeverities := map[string]bool{"critical": true, "high": true, "medium": true, "low": true}
	if !validSeverities[input.Severity] {
		return nil, fmt.Errorf("invalid severity '%s', must be one of: critical, high, medium, low", input.Severity)
	}

	// Build request to Coordination Engine
	req := &clients.CreateIncidentRequest{
		Title:       input.Title,
		Description: input.Description,
		Severity:    input.Severity,
		Source:      stringPtr("manual"), // Indicate manual creation
		CreatedBy:   stringPtr("mcp-server"),
	}

	// Add optional fields
	if input.Target != "" {
		req.Target = &input.Target
	}
	if input.CorrelationID != "" {
		req.CorrelationID = &input.CorrelationID
	}
	if input.ExternalID != "" {
		req.ExternalID = &input.ExternalID
	}
	if input.Confidence > 0 {
		req.Confidence = &input.Confidence
	}
	if input.Labels != nil {
		req.Labels = input.Labels
	}
	if len(input.AffectedResources) > 0 {
		req.AffectedResources = input.AffectedResources
	}

	// Call Coordination Engine API
	resp, err := t.ceClient.CreateIncident(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("failed to create incident in Coordination Engine: %w", err)
	}

	// Build output
	output := CreateIncidentOutput{
		IncidentID:  resp.IncidentID,
		Title:       resp.Title,
		Description: resp.Description,
		Severity:    resp.Severity,
		Priority:    resp.Priority,
		Status:      resp.Status,
		CreatedAt:   resp.CreatedAt,
		Message:     resp.Message,
	}

	return output, nil
}

// stringPtr is a helper to create a string pointer
func stringPtr(s string) *string {
	return &s
}
