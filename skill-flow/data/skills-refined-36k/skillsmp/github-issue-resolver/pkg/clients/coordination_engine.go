package clients

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// CoordinationEngineClient provides client for the Coordination Engine API
type CoordinationEngineClient struct {
	baseURL    string
	httpClient *http.Client
}

// NewCoordinationEngineClient creates a new Coordination Engine client
func NewCoordinationEngineClient(baseURL string) *CoordinationEngineClient {
	return &CoordinationEngineClient{
		baseURL: baseURL,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// Incident represents an incident from the Coordination Engine
type Incident struct {
	ID              string                 `json:"id"`
	Title           string                 `json:"title"`
	Description     string                 `json:"description"`
	Severity        string                 `json:"severity"` // critical, high, medium, low
	Status          string                 `json:"status"`   // pending, running, completed, failed
	Priority        int                    `json:"priority"`
	Target          string                 `json:"target"`
	ActionType      string                 `json:"action_type"`
	Source          string                 `json:"source"`
	Confidence      float64                `json:"confidence"`
	Parameters      map[string]interface{} `json:"parameters"`
	CreatedAt       string                 `json:"created_at"`
	StartedAt       *string                `json:"started_at"`
	CompletedAt     *string                `json:"completed_at"`
	DurationSeconds *float64               `json:"duration_seconds"`
	Tags            []string               `json:"tags"`
}

// IncidentListResponse represents the response from listing incidents
type IncidentListResponse struct {
	Incidents []Incident `json:"incidents"`
	Summary   struct {
		Total      int            `json:"total"`
		Active     int            `json:"active"`
		Completed  int            `json:"completed"`
		Failed     int            `json:"failed"`
		BySeverity map[string]int `json:"by_severity"`
	} `json:"summary"`
}

// CreateIncidentRequest represents a request to create an incident
type CreateIncidentRequest struct {
	Title             string                 `json:"title"`
	Description       string                 `json:"description"`
	Severity          string                 `json:"severity"` // critical, high, medium, low
	Target            *string                `json:"target,omitempty"`
	Source            *string                `json:"source,omitempty"` // manual, auto
	Labels            map[string]string      `json:"labels,omitempty"`
	AffectedResources []string               `json:"affectedResources,omitempty"`
	CorrelationID     *string                `json:"correlationId,omitempty"`
	ExternalID        *string                `json:"externalId,omitempty"`
	CreatedBy         *string                `json:"createdBy,omitempty"`
	Confidence        *float64               `json:"confidence,omitempty"`
	Parameters        map[string]interface{} `json:"parameters,omitempty"`
}

// CreateIncidentResponse represents the response from creating an incident
type CreateIncidentResponse struct {
	IncidentID  string `json:"incident_id"`
	Title       string `json:"title"`
	Description string `json:"description"`
	Severity    string `json:"severity"`
	Priority    int    `json:"priority"`
	Status      string `json:"status"`
	CreatedAt   string `json:"created_at"`
	Message     string `json:"message"`
}

// TriggerRemediationRequest represents a request to trigger remediation
type TriggerRemediationRequest struct {
	IncidentID string                 `json:"incidentId"`
	Action     string                 `json:"action"` // scale_deployment, restart_pod, clear_alerts, etc.
	Parameters map[string]interface{} `json:"parameters,omitempty"`
	Priority   *int                   `json:"priority,omitempty"`   // 1-10
	Confidence *float64               `json:"confidence,omitempty"` // 0.0-1.0
	DryRun     *bool                  `json:"dryRun,omitempty"`
}

// TriggerRemediationResponse represents the response from triggering remediation
type TriggerRemediationResponse struct {
	ActionID          string                 `json:"action_id"`
	IncidentID        string                 `json:"incident_id"`
	Type              string                 `json:"type"`
	MappedType        string                 `json:"mapped_type"`
	Description       string                 `json:"description"`
	Status            string                 `json:"status"`
	Priority          int                    `json:"priority"`
	Confidence        float64                `json:"confidence"`
	Parameters        map[string]interface{} `json:"parameters"`
	Target            string                 `json:"target"`
	Source            string                 `json:"source"`
	ExecutedAt        string                 `json:"executedAt"`
	EstimatedDuration string                 `json:"estimatedDuration"`
	Result            string                 `json:"result"`
}

// AnalyzeAnomaliesRequest represents a request to analyze anomalies
type AnalyzeAnomaliesRequest struct {
	TimeRange          string        `json:"timeRange,omitempty"`     // e.g., "1h", "24h"
	Metrics            []interface{} `json:"metrics,omitempty"`       // Can be metric names or full metric objects
	Threshold          *float64      `json:"threshold,omitempty"`     // 0.0-1.0
	IncludePredictions *bool         `json:"includePredictions,omitempty"`
	Models             []string      `json:"models,omitempty"`        // Specify which ML models to use
	ModelName          string        `json:"modelName,omitempty"`     // Primary model name (e.g., "anomaly-detector")
	Namespace          string        `json:"namespace,omitempty"`     // Kubernetes namespace to scope analysis
	Deployment         string        `json:"deployment,omitempty"`    // Specific deployment name to filter
	Pod                string        `json:"pod,omitempty"`           // Specific pod name to filter
	LabelSelector      string        `json:"labelSelector,omitempty"` // Kubernetes label selector (e.g., "app=flask")
}

// AnomalyPattern represents a detected anomaly pattern
type AnomalyPattern struct {
	Metric      string  `json:"metric"`
	Type        string  `json:"type"`     // statistical_outlier, threshold_exceeded, trend_anomaly
	Severity    string  `json:"severity"` // low, medium, high, critical
	Score       float64 `json:"score"`    // Confidence score
	Timestamp   string  `json:"timestamp"`
	Value       float64 `json:"value"`
	ExpectedMin float64 `json:"expected_min"`
	ExpectedMax float64 `json:"expected_max"`
	Model       string  `json:"model"` // Which model detected it
}

// Alert represents an alert from anomaly detection
type Alert struct {
	Type           string `json:"type"` // resource_exhaustion, memory_issue, network_issue
	Message        string `json:"message"`
	Severity       string `json:"severity"`
	ActionRequired bool   `json:"action_required"`
}

// AnalyzeAnomaliesResponse represents the response from anomaly analysis
type AnalyzeAnomaliesResponse struct {
	Status            string           `json:"status"`
	AnomaliesDetected int              `json:"anomalies_detected"`
	TimeRange         string           `json:"time_range"`
	Threshold         float64          `json:"threshold"`
	Patterns          []AnomalyPattern `json:"patterns"`
	Recommendations   []string         `json:"recommendations"`
	Alerts            []Alert          `json:"alerts"`
	Summary           struct {
		TotalMetricsAnalyzed int            `json:"total_metrics_analyzed"`
		AnomaliesFound       int            `json:"anomalies_found"`
		ModelsUsed           []string       `json:"models_used"`
		BySeverity           map[string]int `json:"by_severity"`
	} `json:"summary"`
	AnalyzedAt string `json:"analyzed_at"`
}

// ClusterStatus represents the cluster status from Coordination Engine
type ClusterStatus struct {
	Status    string `json:"status"` // healthy, degraded, critical
	Timestamp string `json:"timestamp"`
	Actions   struct {
		Total     int `json:"total"`
		Pending   int `json:"pending"`
		Running   int `json:"running"`
		Completed int `json:"completed"`
		Failed    int `json:"failed"`
	} `json:"actions"`
	Conflicts struct {
		Total    int `json:"total"`
		Resolved int `json:"resolved"`
	} `json:"conflicts"`
	Engine struct {
		Running      bool   `json:"running"`
		QueueLength  int    `json:"queue_length"`
		WorkersCount int    `json:"workers_count"`
		Uptime       string `json:"uptime"`
	} `json:"engine"`
}

// ListIncidents retrieves incidents from the Coordination Engine
func (c *CoordinationEngineClient) ListIncidents(ctx context.Context, status, severity string, limit, offset int) (*IncidentListResponse, error) {
	url := fmt.Sprintf("%s/api/v1/incidents?status=%s&severity=%s&limit=%d&offset=%d",
		c.baseURL, status, severity, limit, offset)

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status code %d: %s", resp.StatusCode, string(body))
	}

	var result IncidentListResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &result, nil
}

// CreateIncident creates a new incident
func (c *CoordinationEngineClient) CreateIncident(ctx context.Context, req *CreateIncidentRequest) (*CreateIncidentResponse, error) {
	url := fmt.Sprintf("%s/api/v1/incidents", c.baseURL)

	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusCreated {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status code %d: %s", resp.StatusCode, string(body))
	}

	var result CreateIncidentResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &result, nil
}

// TriggerRemediation triggers a remediation action
func (c *CoordinationEngineClient) TriggerRemediation(ctx context.Context, req *TriggerRemediationRequest) (*TriggerRemediationResponse, error) {
	url := fmt.Sprintf("%s/api/v1/remediation/trigger", c.baseURL)

	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status code %d: %s", resp.StatusCode, string(body))
	}

	var result TriggerRemediationResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &result, nil
}

// AnalyzeAnomalies analyzes metrics for anomalies
func (c *CoordinationEngineClient) AnalyzeAnomalies(ctx context.Context, req *AnalyzeAnomaliesRequest) (*AnalyzeAnomaliesResponse, error) {
	url := fmt.Sprintf("%s/api/v1/anomalies/analyze", c.baseURL)

	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status code %d: %s", resp.StatusCode, string(body))
	}

	var result AnalyzeAnomaliesResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &result, nil
}

// GetClusterStatus retrieves the cluster status from Coordination Engine
func (c *CoordinationEngineClient) GetClusterStatus(ctx context.Context) (*ClusterStatus, error) {
	url := fmt.Sprintf("%s/api/v1/cluster/status", c.baseURL)

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status code %d: %s", resp.StatusCode, string(body))
	}

	var result ClusterStatus
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &result, nil
}

// HealthCheck performs a health check on the Coordination Engine
func (c *CoordinationEngineClient) HealthCheck(ctx context.Context) error {
	url := fmt.Sprintf("%s/health", c.baseURL)

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to execute request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("health check failed with status %d", resp.StatusCode)
	}

	return nil
}

// PredictResourceUsageRequest represents a request for time-specific resource prediction
type PredictResourceUsageRequest struct {
	Hour              int     `json:"hour"`               // Hour of day (0-23)
	DayOfWeek         int     `json:"day_of_week"`        // Day of week (0=Monday, 6=Sunday)
	CPURollingMean    float64 `json:"cpu_rolling_mean"`   // Current CPU rolling mean
	MemoryRollingMean float64 `json:"memory_rolling_mean"` // Current memory rolling mean
	Namespace         string  `json:"namespace,omitempty"` // Target namespace (optional)
	Deployment        string  `json:"deployment,omitempty"` // Target deployment (optional)
	Pod               string  `json:"pod,omitempty"`       // Target pod (optional)
	Scope             string  `json:"scope,omitempty"`     // Scope: pod, deployment, namespace, cluster
}

// PredictResourceUsageResponse represents the prediction response (public interface)
type PredictResourceUsageResponse struct {
	Status             string  `json:"status"`
	PredictedCPU       float64 `json:"predicted_cpu_percent"`
	PredictedMemory    float64 `json:"predicted_memory_percent"`
	CurrentCPU         float64 `json:"current_cpu_percent"`         // From Prometheus via CE
	CurrentMemory      float64 `json:"current_memory_percent"`      // From Prometheus via CE
	Confidence         float64 `json:"confidence"`
	Trend              string  `json:"trend"`       // upward, downward, stable
	ModelUsed          string  `json:"model_used"`
	ModelVersion       string  `json:"model_version,omitempty"`
	Recommendation     string  `json:"recommendation,omitempty"`
	PredictedTimestamp string  `json:"predicted_timestamp,omitempty"`
}

// coordinationEnginePredictResponse represents the actual nested response from coordination engine
type coordinationEnginePredictResponse struct {
	Status      string `json:"status"`
	Scope       string `json:"scope"`
	Target      string `json:"target"`
	Predictions struct {
		CPUPercent    float64 `json:"cpu_percent"`
		MemoryPercent float64 `json:"memory_percent"`
	} `json:"predictions"`
	ModelInfo struct {
		Name       string  `json:"name"`
		Version    string  `json:"version"`
		Confidence float64 `json:"confidence"`
	} `json:"model_info"`
	CurrentMetrics struct {
		CPURollingMean    float64 `json:"cpu_rolling_mean"`
		MemoryRollingMean float64 `json:"memory_rolling_mean"`
		Timestamp         string  `json:"timestamp"`
	} `json:"current_metrics"`
	TargetTime struct {
		Hour         int    `json:"hour"`
		DayOfWeek    int    `json:"day_of_week"`
		ISOTimestamp string `json:"iso_timestamp"`
	} `json:"target_time"`
	Trend          string `json:"trend,omitempty"`
	Recommendation string `json:"recommendation,omitempty"`
}

// PredictResourceUsage calls the coordination engine's /api/v1/predict endpoint
// for time-specific resource usage forecasting
func (c *CoordinationEngineClient) PredictResourceUsage(ctx context.Context, req *PredictResourceUsageRequest) (*PredictResourceUsageResponse, error) {
	url := fmt.Sprintf("%s/api/v1/predict", c.baseURL)

	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	httpReq.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("prediction failed (code %d): %s", resp.StatusCode, string(body))
	}

	// Parse the nested response from coordination engine
	var ceResp coordinationEnginePredictResponse
	if err := json.NewDecoder(resp.Body).Decode(&ceResp); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	// Convert to the public response format
	result := &PredictResourceUsageResponse{
		Status:             ceResp.Status,
		PredictedCPU:       ceResp.Predictions.CPUPercent,
		PredictedMemory:    ceResp.Predictions.MemoryPercent,
		CurrentCPU:         ceResp.CurrentMetrics.CPURollingMean,    // Use Prometheus data from CE
		CurrentMemory:      ceResp.CurrentMetrics.MemoryRollingMean, // Use Prometheus data from CE
		Confidence:         ceResp.ModelInfo.Confidence,
		Trend:              ceResp.Trend,
		ModelUsed:          ceResp.ModelInfo.Name,
		ModelVersion:       ceResp.ModelInfo.Version,
		Recommendation:     ceResp.Recommendation,
		PredictedTimestamp: ceResp.TargetTime.ISOTimestamp,
	}

	return result, nil
}
