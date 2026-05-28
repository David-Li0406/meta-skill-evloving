package resources

import (
	"context"
	"encoding/json"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

func TestIncidentsResource_URI(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	ceClient := clients.NewCoordinationEngineClient("http://localhost:8080")
	resource := NewIncidentsResource(ceClient, memCache)
	assert.Equal(t, "cluster://incidents", resource.URI())
}

func TestIncidentsResource_Name(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	ceClient := clients.NewCoordinationEngineClient("http://localhost:8080")
	resource := NewIncidentsResource(ceClient, memCache)
	assert.Equal(t, "Active Incidents", resource.Name())
}

func TestIncidentsResource_Description(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	ceClient := clients.NewCoordinationEngineClient("http://localhost:8080")
	resource := NewIncidentsResource(ceClient, memCache)
	assert.Contains(t, resource.Description(), "active and recent incidents")
}

func TestIncidentsResource_MimeType(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	ceClient := clients.NewCoordinationEngineClient("http://localhost:8080")
	resource := NewIncidentsResource(ceClient, memCache)
	assert.Equal(t, "application/json", resource.MimeType())
}

func TestIncidentsResource_Read_WithoutCEClient(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	// Create resource without CE client
	resource := NewIncidentsResource(nil, memCache)

	ctx := context.Background()
	data, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, data)

	// Verify it's valid JSON
	var incidentsData IncidentsData
	err = json.Unmarshal([]byte(data), &incidentsData)
	require.NoError(t, err)

	// Should return empty response
	assert.NotEmpty(t, incidentsData.Timestamp)
	assert.Equal(t, 0, incidentsData.TotalIncidents)
	assert.Equal(t, 0, incidentsData.ActiveIncidents)
	assert.Equal(t, "not-available", incidentsData.Source)
	assert.Empty(t, incidentsData.Incidents)
	assert.Equal(t, 0, incidentsData.Summary.Critical)
	assert.Equal(t, 0, incidentsData.Summary.High)
	assert.Equal(t, 0, incidentsData.Summary.Medium)
	assert.Equal(t, 0, incidentsData.Summary.Low)

	t.Logf("Empty response: %s", data)
}

func TestIncidentsResource_Read_WithCEClient_Unavailable(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	// Create CE client pointing to non-existent server
	ceClient := clients.NewCoordinationEngineClient("http://localhost:9999")
	resource := NewIncidentsResource(ceClient, memCache)

	ctx := context.Background()
	_, err := resource.Read(ctx)

	// Should fail because CE is not available
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "failed to list incidents")
}

func TestIncidentsResource_GetEmptyIncidentsResponse(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewIncidentsResource(nil, memCache)

	data, err := resource.getEmptyIncidentsResponse()
	require.NoError(t, err)
	assert.NotEmpty(t, data)

	// Verify JSON structure
	var incidentsData IncidentsData
	err = json.Unmarshal([]byte(data), &incidentsData)
	require.NoError(t, err)

	assert.Equal(t, "not-available", incidentsData.Source)
	assert.Equal(t, 0, incidentsData.TotalIncidents)
	assert.NotNil(t, incidentsData.Incidents)
	assert.Empty(t, incidentsData.Incidents)
}

func TestIncidentsResource_JSONStructure(t *testing.T) {
	memCache := cache.NewMemoryCache(30 * time.Second)
	defer memCache.Close()

	resource := NewIncidentsResource(nil, memCache)

	ctx := context.Background()
	data, err := resource.Read(ctx)
	require.NoError(t, err)

	// Parse and verify JSON structure
	var incidentsData IncidentsData
	err = json.Unmarshal([]byte(data), &incidentsData)
	require.NoError(t, err)

	// Verify it can be re-marshaled
	_, err = json.MarshalIndent(incidentsData, "", "  ")
	require.NoError(t, err)

	// Verify timestamp format (RFC3339)
	_, err = time.Parse(time.RFC3339, incidentsData.Timestamp)
	require.NoError(t, err, "Timestamp should be in RFC3339 format")
}

func TestIncidentsResource_SeveritySummary(t *testing.T) {
	// This test verifies the structure of the severity summary
	summary := IncidentSummary{
		Critical: 2,
		High:     5,
		Medium:   10,
		Low:      3,
	}

	assert.Equal(t, 2, summary.Critical)
	assert.Equal(t, 5, summary.High)
	assert.Equal(t, 10, summary.Medium)
	assert.Equal(t, 3, summary.Low)

	total := summary.Critical + summary.High + summary.Medium + summary.Low
	assert.Equal(t, 20, total)
}

func TestIncidentInfo_Structure(t *testing.T) {
	// Test the incident info structure
	incident := IncidentInfo{
		ID:               "INC-12345",
		Severity:         "high",
		Status:           "active",
		Type:             "pod_restart",
		Description:      "Pod restarting frequently",
		AffectedResource: "my-app-pod",
		Namespace:        "production",
		CreatedAt:        "2024-01-01T12:00:00Z",
		UpdatedAt:        "2024-01-01T12:30:00Z",
		RemediationState: "in_progress",
		AssignedActions:  2,
	}

	assert.Equal(t, "INC-12345", incident.ID)
	assert.Equal(t, "high", incident.Severity)
	assert.Equal(t, "active", incident.Status)
	assert.Equal(t, "pod_restart", incident.Type)
	assert.Equal(t, "production", incident.Namespace)
	assert.Equal(t, "in_progress", incident.RemediationState)
	assert.Equal(t, 2, incident.AssignedActions)
}

func TestIncidentsResource_CacheTTL(t *testing.T) {
	memCache := cache.NewMemoryCache(1 * time.Second)
	defer memCache.Close()

	resource := NewIncidentsResource(nil, memCache)

	ctx := context.Background()

	// First read
	data1, err := resource.Read(ctx)
	require.NoError(t, err)

	// Immediate second read - should come from cache
	data2, err := resource.Read(ctx)
	require.NoError(t, err)
	assert.Equal(t, data1, data2, "Should return cached data")

	// Parse timestamps to verify they're the same
	var incidents1, incidents2 IncidentsData
	require.NoError(t, json.Unmarshal([]byte(data1), &incidents1))
	require.NoError(t, json.Unmarshal([]byte(data2), &incidents2))
	assert.Equal(t, incidents1.Timestamp, incidents2.Timestamp, "Timestamps should match (cached)")

	// Wait for cache to expire
	time.Sleep(2 * time.Second)

	// Third read - cache expired, should get new data
	data3, err := resource.Read(ctx)
	require.NoError(t, err)

	var incidents3 IncidentsData
	require.NoError(t, json.Unmarshal([]byte(data3), &incidents3))

	// Timestamps should be different (new fetch)
	assert.NotEqual(t, incidents1.Timestamp, incidents3.Timestamp, "New timestamp after cache expiration")
}

func TestIncidentsData_Marshaling(t *testing.T) {
	// Create sample incidents data
	data := IncidentsData{
		Timestamp:       time.Now().UTC().Format(time.RFC3339),
		TotalIncidents:  5,
		ActiveIncidents: 3,
		Source:          "coordination-engine",
		Summary: IncidentSummary{
			Critical: 1,
			High:     2,
			Medium:   1,
			Low:      1,
		},
		Incidents: []IncidentInfo{
			{
				ID:               "INC-001",
				Severity:         "critical",
				Status:           "active",
				Type:             "node_down",
				Description:      "Node is not responding",
				AffectedResource: "worker-node-1",
				CreatedAt:        time.Now().UTC().Format(time.RFC3339),
				RemediationState: "pending",
			},
		},
	}

	// Marshal to JSON
	jsonData, err := json.MarshalIndent(data, "", "  ")
	require.NoError(t, err)
	assert.NotEmpty(t, jsonData)

	// Unmarshal back
	var unmarshaled IncidentsData
	err = json.Unmarshal(jsonData, &unmarshaled)
	require.NoError(t, err)

	// Verify data integrity
	assert.Equal(t, data.TotalIncidents, unmarshaled.TotalIncidents)
	assert.Equal(t, data.ActiveIncidents, unmarshaled.ActiveIncidents)
	assert.Equal(t, data.Source, unmarshaled.Source)
	assert.Equal(t, data.Summary.Critical, unmarshaled.Summary.Critical)
	assert.Equal(t, len(data.Incidents), len(unmarshaled.Incidents))

	if len(unmarshaled.Incidents) > 0 {
		assert.Equal(t, data.Incidents[0].ID, unmarshaled.Incidents[0].ID)
		assert.Equal(t, data.Incidents[0].Severity, unmarshaled.Incidents[0].Severity)
	}
}
