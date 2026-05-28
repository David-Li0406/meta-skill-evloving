package resources

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// IncidentsResource provides the cluster://incidents MCP resource
type IncidentsResource struct {
	ceClient *clients.CoordinationEngineClient
	cache    *cache.MemoryCache
}

// NewIncidentsResource creates a new incidents resource
func NewIncidentsResource(ceClient *clients.CoordinationEngineClient, cache *cache.MemoryCache) *IncidentsResource {
	return &IncidentsResource{
		ceClient: ceClient,
		cache:    cache,
	}
}

// URI returns the resource URI
func (r *IncidentsResource) URI() string {
	return "cluster://incidents"
}

// Name returns the resource name
func (r *IncidentsResource) Name() string {
	return "Active Incidents"
}

// Description returns the resource description
func (r *IncidentsResource) Description() string {
	return "List of active and recent incidents from the Coordination Engine including severity, status, and remediation state"
}

// MimeType returns the MIME type of the resource
func (r *IncidentsResource) MimeType() string {
	return "application/json"
}

// IncidentsData represents the incidents resource data
type IncidentsData struct {
	Timestamp       string          `json:"timestamp"`
	TotalIncidents  int             `json:"total_incidents"`
	ActiveIncidents int             `json:"active_incidents"`
	Summary         IncidentSummary `json:"summary"`
	Incidents       []IncidentInfo  `json:"incidents"`
	Source          string          `json:"source"`
}

// IncidentSummary provides summary statistics
type IncidentSummary struct {
	Critical int `json:"critical"`
	High     int `json:"high"`
	Medium   int `json:"medium"`
	Low      int `json:"low"`
}

// IncidentInfo represents a single incident
type IncidentInfo struct {
	ID               string `json:"id"`
	Severity         string `json:"severity"`
	Status           string `json:"status"`
	Type             string `json:"type"`
	Description      string `json:"description"`
	AffectedResource string `json:"affected_resource,omitempty"`
	Namespace        string `json:"namespace,omitempty"`
	CreatedAt        string `json:"created_at"`
	UpdatedAt        string `json:"updated_at,omitempty"`
	RemediationState string `json:"remediation_state,omitempty"`
	AssignedActions  int    `json:"assigned_actions,omitempty"`
}

// Read retrieves the incidents resource
func (r *IncidentsResource) Read(ctx context.Context) (string, error) {
	// Check if Coordination Engine client is available
	if r.ceClient == nil {
		return r.getEmptyIncidentsResponse()
	}

	// Check cache first (5 second TTL as per PRD)
	cacheKey := "resource:cluster:incidents"
	if cached, found := r.cache.Get(cacheKey); found {
		if data, ok := cached.(string); ok {
			return data, nil
		}
	}

	// Fetch incidents from Coordination Engine
	// Get active incidents (status=active)
	resp, err := r.ceClient.ListIncidents(ctx, "active", "all", 100, 0)
	if err != nil {
		return "", fmt.Errorf("failed to list incidents: %w", err)
	}

	// Build incidents data
	data := IncidentsData{
		Timestamp:       time.Now().UTC().Format(time.RFC3339),
		TotalIncidents:  resp.Summary.Total,
		ActiveIncidents: len(resp.Incidents),
		Source:          "coordination-engine",
		Incidents:       make([]IncidentInfo, 0, len(resp.Incidents)),
	}

	// Process each incident
	for _, incident := range resp.Incidents {
		incidentInfo := IncidentInfo{
			ID:               incident.ID,
			Severity:         incident.Severity,
			Status:           incident.Status,
			Type:             incident.ActionType,
			Description:      incident.Description,
			AffectedResource: incident.Target,
			CreatedAt:        incident.CreatedAt,
		}

		// Add optional fields if available
		if incident.StartedAt != nil {
			incidentInfo.UpdatedAt = *incident.StartedAt
		}
		switch incident.Status {
		case "running":
			incidentInfo.RemediationState = "in_progress"
		case "completed":
			incidentInfo.RemediationState = "completed"
		default:
			incidentInfo.RemediationState = "pending"
		}

		// Update summary counts
		switch incident.Severity {
		case "critical":
			data.Summary.Critical++
		case "high":
			data.Summary.High++
		case "medium":
			data.Summary.Medium++
		case "low":
			data.Summary.Low++
		}

		data.Incidents = append(data.Incidents, incidentInfo)
	}

	// Marshal to JSON
	jsonData, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal incidents data: %w", err)
	}

	jsonStr := string(jsonData)

	// Cache for 5 seconds (as per PRD)
	r.cache.SetWithTTL(cacheKey, jsonStr, 5*time.Second)

	return jsonStr, nil
}

// getEmptyIncidentsResponse returns an empty response when CE is not available
func (r *IncidentsResource) getEmptyIncidentsResponse() (string, error) {
	data := IncidentsData{
		Timestamp:       time.Now().UTC().Format(time.RFC3339),
		TotalIncidents:  0,
		ActiveIncidents: 0,
		Source:          "not-available",
		Incidents:       []IncidentInfo{},
		Summary: IncidentSummary{
			Critical: 0,
			High:     0,
			Medium:   0,
			Low:      0,
		},
	}

	jsonData, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return "", fmt.Errorf("failed to marshal empty incidents data: %w", err)
	}

	return string(jsonData), nil
}
