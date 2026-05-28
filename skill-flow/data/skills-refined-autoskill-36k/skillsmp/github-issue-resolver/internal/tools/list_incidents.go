package tools

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// ListIncidentsTool provides MCP tool for listing incidents from Coordination Engine
type ListIncidentsTool struct {
	ceClient *clients.CoordinationEngineClient
}

// NewListIncidentsTool creates a new list-incidents tool
func NewListIncidentsTool(ceClient *clients.CoordinationEngineClient) *ListIncidentsTool {
	return &ListIncidentsTool{
		ceClient: ceClient,
	}
}

// Name returns the tool name
func (t *ListIncidentsTool) Name() string {
	return "list-incidents"
}

// Description returns the tool description
func (t *ListIncidentsTool) Description() string {
	return "List and filter incidents from the Coordination Engine. Supports filtering by status (all, active, completed, failed) and severity (all, low, medium, high, critical)."
}

// InputSchema returns the JSON schema for tool inputs
func (t *ListIncidentsTool) InputSchema() map[string]interface{} {
	return map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"status": map[string]interface{}{
				"type":        "string",
				"description": "Filter by incident status",
				"enum":        []string{"all", "active", "completed", "failed"},
				"default":     "all",
			},
			"severity": map[string]interface{}{
				"type":        "string",
				"description": "Filter by severity level",
				"enum":        []string{"all", "low", "medium", "high", "critical"},
				"default":     "all",
			},
			"limit": map[string]interface{}{
				"type":        "integer",
				"description": "Maximum number of incidents to return",
				"default":     100,
				"minimum":     1,
				"maximum":     1000,
			},
			"offset": map[string]interface{}{
				"type":        "integer",
				"description": "Number of incidents to skip for pagination",
				"default":     0,
				"minimum":     0,
			},
		},
		"required": []string{},
	}
}

// ListIncidentsInput represents the input parameters
type ListIncidentsInput struct {
	Status   string `json:"status"`
	Severity string `json:"severity"`
	Limit    int    `json:"limit"`
	Offset   int    `json:"offset"`
}

// ListIncidentsOutput represents the tool output
type ListIncidentsOutput struct {
	Status    string                       `json:"status"`
	Incidents []clients.Incident           `json:"incidents"`
	Summary   clients.IncidentListResponse `json:"summary"`
	Message   string                       `json:"message"`
	Count     int                          `json:"count"`
	Filters   struct {
		Status   string `json:"status"`
		Severity string `json:"severity"`
		Limit    int    `json:"limit"`
		Offset   int    `json:"offset"`
	} `json:"filters"`
}

// Execute runs the list-incidents tool
func (t *ListIncidentsTool) Execute(ctx context.Context, args map[string]interface{}) (interface{}, error) {
	// Parse input arguments with defaults
	input := ListIncidentsInput{
		Status:   "all",
		Severity: "all",
		Limit:    100,
		Offset:   0,
	}

	if argsJSON, err := json.Marshal(args); err == nil {
		_ = json.Unmarshal(argsJSON, &input) //nolint:errcheck // Intentionally ignore error, use defaults if unmarshal fails
	}

	// Call Coordination Engine API
	resp, err := t.ceClient.ListIncidents(ctx, input.Status, input.Severity, input.Limit, input.Offset)
	if err != nil {
		return nil, fmt.Errorf("failed to list incidents: %w", err)
	}

	// Build output
	output := ListIncidentsOutput{
		Status:    "success",
		Incidents: resp.Incidents,
		Summary:   *resp,
		Count:     len(resp.Incidents),
		Message:   fmt.Sprintf("Retrieved %d incidents (total: %d)", len(resp.Incidents), resp.Summary.Total),
	}

	output.Filters.Status = input.Status
	output.Filters.Severity = input.Severity
	output.Filters.Limit = input.Limit
	output.Filters.Offset = input.Offset

	return output, nil
}
