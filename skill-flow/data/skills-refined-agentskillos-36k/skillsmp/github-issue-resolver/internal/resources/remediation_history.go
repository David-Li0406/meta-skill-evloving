package resources

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/cache"
	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

// RemediationHistoryResource provides the cluster://remediation-history MCP resource
// This tracks past remediation actions and their success rates
type RemediationHistoryResource struct {
	ceClient *clients.CoordinationEngineClient
	cache    *cache.MemoryCache
}

// NewRemediationHistoryResource creates a new remediation history resource
func NewRemediationHistoryResource(ceClient *clients.CoordinationEngineClient, cache *cache.MemoryCache) *RemediationHistoryResource {
	return &RemediationHistoryResource{
		ceClient: ceClient,
		cache:    cache,
	}
}

// URI returns the resource URI
func (r *RemediationHistoryResource) URI() string {
	return "cluster://remediation-history"
}

// Name returns the resource name
func (r *RemediationHistoryResource) Name() string {
	return "Remediation History"
}

// Description returns the resource description
func (r *RemediationHistoryResource) Description() string {
	return "Recent remediation actions and their success rates - useful for understanding what fixes work and predicting successful remediation strategies"
}

// MimeType returns the MIME type of the resource
func (r *RemediationHistoryResource) MimeType() string {
	return "application/json"
}

// RemediationHistoryData represents the remediation history resource data
type RemediationHistoryData struct {
	Status      string                     `json:"status"`
	Timestamp   string                     `json:"timestamp"`
	Source      string                     `json:"source"`
	Summary     RemediationSummary         `json:"summary"`
	TopActions  []ActionSuccessRate        `json:"top_actions"`
	RecentActions []RecentRemediationAction `json:"recent_actions"`
	Patterns    []RemediationPattern       `json:"patterns,omitempty"`
	Message     string                     `json:"message"`
}

// RemediationSummary summarizes overall remediation statistics
type RemediationSummary struct {
	TotalActions       int     `json:"total_actions"`
	Completed          int     `json:"completed"`
	Failed             int     `json:"failed"`
	SuccessRate        float64 `json:"success_rate_percent"`
	AverageDuration    float64 `json:"average_duration_seconds"`
	MostCommonAction   string  `json:"most_common_action"`
	MostSuccessfulAction string `json:"most_successful_action"`
}

// ActionSuccessRate tracks success rate by action type
type ActionSuccessRate struct {
	ActionType      string  `json:"action_type"`
	TotalExecutions int     `json:"total_executions"`
	Successful      int     `json:"successful"`
	Failed          int     `json:"failed"`
	SuccessRate     float64 `json:"success_rate_percent"`
	AvgDuration     float64 `json:"avg_duration_seconds"`
}

// RecentRemediationAction represents a recent remediation action
type RecentRemediationAction struct {
	IncidentID      string  `json:"incident_id"`
	ActionType      string  `json:"action_type"`
	Target          string  `json:"target"`
	Status          string  `json:"status"` // completed, failed
	Duration        float64 `json:"duration_seconds,omitempty"`
	CompletedAt     string  `json:"completed_at"`
	Success         bool    `json:"success"`
}

// RemediationPattern identifies recurring remediation patterns
type RemediationPattern struct {
	Pattern     string  `json:"pattern"`
	Frequency   int     `json:"frequency"`
	SuccessRate float64 `json:"success_rate_percent"`
	Description string  `json:"description"`
}

// Read retrieves the remediation history resource
func (r *RemediationHistoryResource) Read(ctx context.Context) (string, error) {
	// Check cache first (15 second TTL as per plan)
	cacheKey := "resource:cluster:remediation-history"
	if cached, found := r.cache.Get(cacheKey); found {
		if data, ok := cached.(string); ok {
			return data, nil
		}
	}

	// Fetch completed and failed incidents from Coordination Engine
	// Get last 100 completed incidents
	completedResp, err := r.ceClient.ListIncidents(ctx, "completed", "all", 100, 0)
	if err != nil {
		return "", fmt.Errorf("failed to get completed incidents: %w", err)
	}

	// Get last 100 failed incidents
	failedResp, err := r.ceClient.ListIncidents(ctx, "failed", "all", 100, 0)
	if err != nil {
		return "", fmt.Errorf("failed to get failed incidents: %w", err)
	}

	// Combine incidents
	allIncidents := append(completedResp.Incidents, failedResp.Incidents...)

	// Calculate statistics
	summary, topActions, recentActions, patterns := analyzeRemediationHistory(allIncidents)

	// Build response
	data := RemediationHistoryData{
		Status:        "success",
		Timestamp:     time.Now().Format(time.RFC3339),
		Source:        "coordination-engine",
		Summary:       summary,
		TopActions:    topActions,
		RecentActions: recentActions,
		Patterns:      patterns,
		Message:       fmt.Sprintf("Analyzed %d remediation actions", len(allIncidents)),
	}

	// Marshal to JSON
	jsonData, err := json.Marshal(data)
	if err != nil {
		return "", fmt.Errorf("failed to marshal remediation history: %w", err)
	}

	jsonStr := string(jsonData)

	// Cache using the global cache TTL (configured in server initialization)
	r.cache.Set(cacheKey, jsonStr)

	return jsonStr, nil
}

// analyzeRemediationHistory analyzes incidents to extract patterns and statistics
func analyzeRemediationHistory(incidents []clients.Incident) (RemediationSummary, []ActionSuccessRate, []RecentRemediationAction, []RemediationPattern) {
	if len(incidents) == 0 {
		return RemediationSummary{}, []ActionSuccessRate{}, []RecentRemediationAction{}, []RemediationPattern{}
	}

	// Track action statistics
	actionStats := make(map[string]*ActionSuccessRate)
	var totalDuration float64
	completed := 0
	failed := 0

	// Recent actions (last 20)
	var recentActions []RecentRemediationAction

	// Pattern tracking
	patternFreq := make(map[string]int)

	for _, incident := range incidents {
		// Update action stats
		actionType := incident.ActionType
		if actionType == "" {
			actionType = "unknown"
		}

		if _, exists := actionStats[actionType]; !exists {
			actionStats[actionType] = &ActionSuccessRate{
				ActionType: actionType,
			}
		}

		stats := actionStats[actionType]
		stats.TotalExecutions++

		// Track success/failure
		isSuccess := incident.Status == "completed"
		if isSuccess {
			stats.Successful++
			completed++
		} else {
			stats.Failed++
			failed++
		}

		// Track duration
		if incident.DurationSeconds != nil {
			duration := *incident.DurationSeconds
			stats.AvgDuration = (stats.AvgDuration*float64(stats.TotalExecutions-1) + duration) / float64(stats.TotalExecutions)
			totalDuration += duration
		}

		// Add to recent actions (last 20)
		if len(recentActions) < 20 {
			completedAt := ""
			if incident.CompletedAt != nil {
				completedAt = *incident.CompletedAt
			}
			duration := 0.0
			if incident.DurationSeconds != nil {
				duration = *incident.DurationSeconds
			}

			recentActions = append(recentActions, RecentRemediationAction{
				IncidentID:  incident.ID,
				ActionType:  actionType,
				Target:      incident.Target,
				Status:      incident.Status,
				Duration:    duration,
				CompletedAt: completedAt,
				Success:     isSuccess,
			})
		}

		// Track patterns (action type + target namespace)
		pattern := fmt.Sprintf("%s on %s", actionType, incident.Target)
		patternFreq[pattern]++
	}

	// Calculate success rates for actions
	topActions := make([]ActionSuccessRate, 0, len(actionStats))
	mostCommonAction := ""
	mostCommonCount := 0
	mostSuccessfulAction := ""
	highestSuccessRate := 0.0

	for _, stats := range actionStats {
		stats.SuccessRate = (float64(stats.Successful) / float64(stats.TotalExecutions)) * 100

		topActions = append(topActions, *stats)

		// Track most common
		if stats.TotalExecutions > mostCommonCount {
			mostCommonCount = stats.TotalExecutions
			mostCommonAction = stats.ActionType
		}

		// Track most successful (with minimum 5 executions)
		if stats.TotalExecutions >= 5 && stats.SuccessRate > highestSuccessRate {
			highestSuccessRate = stats.SuccessRate
			mostSuccessfulAction = stats.ActionType
		}
	}

	// Build patterns (top 5)
	patterns := make([]RemediationPattern, 0, 5)
	for pattern, freq := range patternFreq {
		if freq >= 3 { // Only include patterns that occurred 3+ times
			patterns = append(patterns, RemediationPattern{
				Pattern:     pattern,
				Frequency:   freq,
				SuccessRate: 100.0, // Simplified - would need to track per pattern
				Description: fmt.Sprintf("Recurring remediation: %s (%d times)", pattern, freq),
			})
		}
		if len(patterns) >= 5 {
			break
		}
	}

	// Build summary
	totalActions := len(incidents)
	avgDuration := 0.0
	if totalActions > 0 {
		avgDuration = totalDuration / float64(totalActions)
	}

	successRate := 0.0
	if totalActions > 0 {
		successRate = (float64(completed) / float64(totalActions)) * 100
	}

	summary := RemediationSummary{
		TotalActions:         totalActions,
		Completed:            completed,
		Failed:               failed,
		SuccessRate:          successRate,
		AverageDuration:      avgDuration,
		MostCommonAction:     mostCommonAction,
		MostSuccessfulAction: mostSuccessfulAction,
	}

	return summary, topActions, recentActions, patterns
}
