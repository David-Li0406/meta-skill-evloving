package clients

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/client-go/dynamic"
	"k8s.io/client-go/rest"
)

// KServeClient provides client for KServe InferenceService models
type KServeClient struct {
	namespace     string
	predictorPort int
	httpClient    *http.Client
	dynamicClient dynamic.Interface
	restConfig    *rest.Config
	enabled       bool
}

// KServeConfig holds configuration for KServe client
type KServeConfig struct {
	Namespace     string
	PredictorPort int           // Port for KServe predictor (default: 8080 for RawDeployment)
	Timeout       time.Duration
	Enabled       bool
	RestConfig    *rest.Config // Kubernetes rest config for accessing CRDs
}

// NewKServeClient creates a new KServe client
func NewKServeClient(config KServeConfig) *KServeClient {
	timeout := config.Timeout
	if timeout == 0 {
		timeout = 15 * time.Second
	}

	// Default port for KServe RawDeployment mode is 8080
	predictorPort := config.PredictorPort
	if predictorPort == 0 {
		predictorPort = 8080
	}

	client := &KServeClient{
		namespace:     config.Namespace,
		predictorPort: predictorPort,
		httpClient: &http.Client{
			Timeout: timeout,
		},
		restConfig: config.RestConfig,
		enabled:    config.Enabled,
	}

	// Initialize dynamic client if rest config is provided
	if config.RestConfig != nil {
		dynamicClient, err := dynamic.NewForConfig(config.RestConfig)
		if err == nil {
			client.dynamicClient = dynamicClient
		}
		// If error, client will still work for HTTP-based operations
	}

	return client
}

// IsEnabled returns whether KServe integration is enabled
func (c *KServeClient) IsEnabled() bool {
	return c.enabled
}

// InferenceRequest represents a KServe v2 inference request
type InferenceRequest struct {
	Inputs []InferenceInput `json:"inputs"`
}

// InferenceInput represents input data for inference
type InferenceInput struct {
	Name     string          `json:"name"`
	Shape    []int           `json:"shape"`
	Datatype string          `json:"datatype"`
	Data     [][]interface{} `json:"data"`
}

// InferenceResponse represents a KServe v2 inference response
type InferenceResponse struct {
	ModelName    string            `json:"model_name"`
	ModelVersion string            `json:"model_version,omitempty"`
	ID           string            `json:"id,omitempty"`
	Outputs      []InferenceOutput `json:"outputs"`
}

// InferenceOutput represents output data from inference
type InferenceOutput struct {
	Name     string        `json:"name"`
	Shape    []int         `json:"shape"`
	Datatype string        `json:"datatype"`
	Data     []interface{} `json:"data"`
}

// AnomalyDetectionRequest represents a request to detect anomalies
type AnomalyDetectionRequest struct {
	Metrics []MetricData `json:"metrics"`
}

// MetricData represents time-series metric data
type MetricData struct {
	Name       string    `json:"name"`
	Values     []float64 `json:"values"`
	Timestamps []string  `json:"timestamps"`
}

// AnomalyDetectionResult represents the result of anomaly detection
type AnomalyDetectionResult struct {
	Anomalies []AnomalyDetection `json:"anomalies"`
	Summary   struct {
		TotalMetrics   int `json:"total_metrics"`
		AnomaliesFound int `json:"anomalies_found"`
		HighSeverity   int `json:"high_severity"`
		MediumSeverity int `json:"medium_severity"`
		LowSeverity    int `json:"low_severity"`
	} `json:"summary"`
}

// AnomalyDetection represents a detected anomaly
type AnomalyDetection struct {
	Metric      string  `json:"metric"`
	Timestamp   string  `json:"timestamp"`
	Value       float64 `json:"value"`
	ExpectedMin float64 `json:"expected_min"`
	ExpectedMax float64 `json:"expected_max"`
	Severity    string  `json:"severity"` // low, medium, high, critical
	Score       float64 `json:"score"`    // 0.0-1.0
	Type        string  `json:"type"`     // spike, dip, trend_change
}

// PredictiveAnalyticsRequest represents a request for predictive analytics
type PredictiveAnalyticsRequest struct {
	ResourceType string                 `json:"resource_type"` // pod, node, deployment
	ResourceName string                 `json:"resource_name"`
	Metrics      []MetricData           `json:"metrics"`
	Horizon      string                 `json:"horizon,omitempty"` // Prediction horizon (e.g., "1h", "24h")
	Features     map[string]interface{} `json:"features,omitempty"`
}

// PredictiveAnalyticsResult represents the result of predictive analytics
type PredictiveAnalyticsResult struct {
	Predictions     []Prediction `json:"predictions"`
	Confidence      float64      `json:"confidence"` // Overall confidence 0.0-1.0
	Recommendations []string     `json:"recommendations"`
	RiskLevel       string       `json:"risk_level"` // low, medium, high, critical
}

// Prediction represents a predicted event or value
type Prediction struct {
	Timestamp            string  `json:"timestamp"`
	PredictedValue       float64 `json:"predicted_value"`
	ConfidenceScore      float64 `json:"confidence_score"`
	ProbabilityOfFailure float64 `json:"probability_of_failure,omitempty"`
	RecommendedAction    string  `json:"recommended_action,omitempty"`
}

// DetectAnomalies uses the anomaly-detector model to detect anomalies
func (c *KServeClient) DetectAnomalies(ctx context.Context, metrics []MetricData) (*AnomalyDetectionResult, error) {
	if !c.enabled {
		return nil, fmt.Errorf("kserve not enabled")
	}

	// Build inference request
	// Convert metrics to the format expected by the model
	inferReq := c.buildAnomalyDetectionRequest(metrics)

	// Call KServe inference endpoint
	url := c.getModelURL("anomaly-detector", "infer")
	resp, err := c.callInference(ctx, url, inferReq)
	if err != nil {
		return nil, fmt.Errorf("failed to call anomaly detector: %w", err)
	}

	// Parse response and convert to AnomalyDetectionResult
	result := c.parseAnomalyDetectionResponse(resp)
	return result, nil
}

// PredictFailures uses the predictive-analytics model to predict failures
func (c *KServeClient) PredictFailures(ctx context.Context, req *PredictiveAnalyticsRequest) (*PredictiveAnalyticsResult, error) {
	if !c.enabled {
		return nil, fmt.Errorf("kserve not enabled")
	}

	// Build inference request
	inferReq := c.buildPredictiveAnalyticsRequest(req)

	// Call KServe inference endpoint
	url := c.getModelURL("predictive-analytics", "infer")
	resp, err := c.callInference(ctx, url, inferReq)
	if err != nil {
		return nil, fmt.Errorf("failed to call predictive analytics: %w", err)
	}

	// Parse response and convert to PredictiveAnalyticsResult
	result := c.parsePredictiveAnalyticsResponse(resp)
	return result, nil
}

// getModelURL constructs the KServe model URL
func (c *KServeClient) getModelURL(modelName, operation string) string {
	// KServe v2 protocol endpoint (KServe 0.11+)
	// Format: http://{model-name}-predictor.{namespace}.svc.cluster.local:{port}/v2/models/model/{operation}
	// Port 8080 is the default for RawDeployment mode, port 80 for Serverless mode
	// Note: KServe RawDeployment uses literal "model" in the URL path, not the model name
	return fmt.Sprintf("http://%s-predictor.%s.svc.cluster.local:%d/v2/models/model/%s",
		modelName, c.namespace, c.predictorPort, operation)
}

// callInference makes an HTTP call to the KServe inference endpoint
func (c *KServeClient) callInference(ctx context.Context, url string, req *InferenceRequest) (*InferenceResponse, error) {
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

	var result InferenceResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &result, nil
}

// buildAnomalyDetectionRequest builds an inference request for anomaly detection
func (c *KServeClient) buildAnomalyDetectionRequest(metrics []MetricData) *InferenceRequest {
	// Convert metrics to inference input format
	// This is a simplified version - actual implementation would depend on model's input format
	var data [][]interface{}
	for _, metric := range metrics {
		row := make([]interface{}, len(metric.Values))
		for i, val := range metric.Values {
			row[i] = val
		}
		data = append(data, row)
	}

	// Determine shape - use 0 for second dimension if no metrics
	secondDim := 0
	if len(metrics) > 0 && len(metrics[0].Values) > 0 {
		secondDim = len(metrics[0].Values)
	}

	return &InferenceRequest{
		Inputs: []InferenceInput{
			{
				Name:     "metrics",
				Shape:    []int{len(metrics), secondDim},
				Datatype: "FP64",
				Data:     data,
			},
		},
	}
}

// parseAnomalyDetectionResponse parses the inference response for anomaly detection
func (c *KServeClient) parseAnomalyDetectionResponse(resp *InferenceResponse) *AnomalyDetectionResult {
	// Parse inference outputs and convert to AnomalyDetectionResult
	// This is a simplified version - actual implementation would depend on model's output format

	result := &AnomalyDetectionResult{
		Anomalies: []AnomalyDetection{},
	}

	// Extract anomalies from model output
	for _, output := range resp.Outputs {
		if output.Name == "anomalies" {
			// Parse anomaly data from output
			for _, data := range output.Data {
				if anomalyMap, ok := data.(map[string]interface{}); ok {
					anomaly := AnomalyDetection{
						Metric:      getString(anomalyMap, "metric"),
						Timestamp:   getString(anomalyMap, "timestamp"),
						Value:       getFloat64(anomalyMap, "value"),
						ExpectedMin: getFloat64(anomalyMap, "expected_min"),
						ExpectedMax: getFloat64(anomalyMap, "expected_max"),
						Severity:    getString(anomalyMap, "severity"),
						Score:       getFloat64(anomalyMap, "score"),
						Type:        getString(anomalyMap, "type"),
					}
					result.Anomalies = append(result.Anomalies, anomaly)
				}
			}
		}
	}

	// Calculate summary statistics
	result.Summary.TotalMetrics = len(resp.Outputs)
	result.Summary.AnomaliesFound = len(result.Anomalies)

	for _, anomaly := range result.Anomalies {
		switch anomaly.Severity {
		case "high", "critical":
			result.Summary.HighSeverity++
		case "medium":
			result.Summary.MediumSeverity++
		case "low":
			result.Summary.LowSeverity++
		}
	}

	return result
}

// buildPredictiveAnalyticsRequest builds an inference request for predictive analytics
func (c *KServeClient) buildPredictiveAnalyticsRequest(req *PredictiveAnalyticsRequest) *InferenceRequest {
	// Convert predictive analytics request to inference input format
	var data [][]interface{}
	for _, metric := range req.Metrics {
		row := make([]interface{}, len(metric.Values))
		for i, val := range metric.Values {
			row[i] = val
		}
		data = append(data, row)
	}

	// Determine shape - use 0 for second dimension if no metrics
	secondDim := 0
	if len(req.Metrics) > 0 && len(req.Metrics[0].Values) > 0 {
		secondDim = len(req.Metrics[0].Values)
	}

	return &InferenceRequest{
		Inputs: []InferenceInput{
			{
				Name:     "features",
				Shape:    []int{len(req.Metrics), secondDim},
				Datatype: "FP64",
				Data:     data,
			},
		},
	}
}

// parsePredictiveAnalyticsResponse parses the inference response for predictive analytics
func (c *KServeClient) parsePredictiveAnalyticsResponse(resp *InferenceResponse) *PredictiveAnalyticsResult {
	// Parse inference outputs and convert to PredictiveAnalyticsResult
	result := &PredictiveAnalyticsResult{
		Predictions:     []Prediction{},
		Recommendations: []string{},
	}

	// Extract predictions from model output
	for _, output := range resp.Outputs {
		if output.Name == "predictions" {
			for _, data := range output.Data {
				if predMap, ok := data.(map[string]interface{}); ok {
					pred := Prediction{
						Timestamp:            getString(predMap, "timestamp"),
						PredictedValue:       getFloat64(predMap, "predicted_value"),
						ConfidenceScore:      getFloat64(predMap, "confidence_score"),
						ProbabilityOfFailure: getFloat64(predMap, "probability_of_failure"),
						RecommendedAction:    getString(predMap, "recommended_action"),
					}
					result.Predictions = append(result.Predictions, pred)
				}
			}
		} else if output.Name == "confidence" && len(output.Data) > 0 {
			result.Confidence = getFloat64Value(output.Data[0])
		}
	}

	// Determine risk level based on predictions
	if result.Confidence > 0 {
		maxFailureProb := 0.0
		for _, pred := range result.Predictions {
			if pred.ProbabilityOfFailure > maxFailureProb {
				maxFailureProb = pred.ProbabilityOfFailure
			}
		}

		if maxFailureProb >= 0.8 {
			result.RiskLevel = "critical"
		} else if maxFailureProb >= 0.6 {
			result.RiskLevel = "high"
		} else if maxFailureProb >= 0.3 {
			result.RiskLevel = "medium"
		} else {
			result.RiskLevel = "low"
		}
	}

	return result
}

// Helper functions to safely extract values from map[string]interface{}
func getString(m map[string]interface{}, key string) string {
	if val, ok := m[key]; ok {
		if str, ok := val.(string); ok {
			return str
		}
	}
	return ""
}

func getFloat64(m map[string]interface{}, key string) float64 {
	if val, ok := m[key]; ok {
		switch v := val.(type) {
		case float64:
			return v
		case float32:
			return float64(v)
		case int:
			return float64(v)
		case int64:
			return float64(v)
		}
	}
	return 0.0
}

func getFloat64Value(val interface{}) float64 {
	switch v := val.(type) {
	case float64:
		return v
	case float32:
		return float64(v)
	case int:
		return float64(v)
	case int64:
		return float64(v)
	}
	return 0.0
}

// HealthCheck performs a health check on a KServe model
func (c *KServeClient) HealthCheck(ctx context.Context, modelName string) error {
	if !c.enabled {
		return fmt.Errorf("kserve not enabled")
	}

	// KServe health endpoint (v2 protocol)
	// Port 8080 is the default for RawDeployment mode, port 80 for Serverless mode
	// Note: KServe RawDeployment uses literal "model" in the URL path, not the model name
	url := fmt.Sprintf("http://%s-predictor.%s.svc.cluster.local:%d/v2/models/model",
		modelName, c.namespace, c.predictorPort)

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

// GetNamespace returns the KServe namespace
func (c *KServeClient) GetNamespace() string {
	return c.namespace
}

// ModelStatusResponse represents the model status from KServe
type ModelStatusResponse struct {
	ModelName          string                   `json:"name"`
	Ready              bool                     `json:"ready"`
	ModelVersion       string                   `json:"version,omitempty"`
	URL                string                   `json:"url,omitempty"`
	Runtime            string                   `json:"runtime,omitempty"`
	Framework          string                   `json:"framework,omitempty"`
	Replicas           int                      `json:"replicas,omitempty"`
	AvailableReplicas  int                      `json:"available_replicas,omitempty"`
	LastTransitionTime string                   `json:"last_transition_time,omitempty"`
	Conditions         []map[string]interface{} `json:"conditions,omitempty"`
}

// GetModelStatus retrieves the status of a KServe model
func (c *KServeClient) GetModelStatus(ctx context.Context, modelName string) (*ModelStatusResponse, error) {
	if !c.enabled {
		return nil, fmt.Errorf("kserve not enabled")
	}

	// KServe v2 model metadata endpoint
	// Port 8080 is the default for RawDeployment mode, port 80 for Serverless mode
	// Note: KServe RawDeployment uses literal "model" in the URL path, not the model name
	url := fmt.Sprintf("http://%s-predictor.%s.svc.cluster.local:%d/v2/models/model",
		modelName, c.namespace, c.predictorPort)

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
		return nil, fmt.Errorf("failed to get model status (code %d): %s", resp.StatusCode, string(body))
	}

	var status ModelStatusResponse
	if err := json.NewDecoder(resp.Body).Decode(&status); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	// Set default values if not provided
	if status.ModelName == "" {
		status.ModelName = modelName
	}
	status.Ready = resp.StatusCode == http.StatusOK

	return &status, nil
}

// PredictionRequest represents a generic prediction request
type PredictionRequest struct {
	Instances []map[string]interface{} `json:"instances"`
}

// PredictionResponse represents a generic prediction response
type PredictionResponse struct {
	Predictions  interface{} `json:"predictions"`
	ModelName    string      `json:"model_name,omitempty"`
	ModelVersion string      `json:"model_version,omitempty"`
}

// Predict makes a generic prediction call to a KServe model
func (c *KServeClient) Predict(ctx context.Context, modelName string, instances []map[string]interface{}) (*PredictionResponse, error) {
	if !c.enabled {
		return nil, fmt.Errorf("kserve not enabled")
	}

	// Build prediction request (v1 protocol - simpler than v2)
	predReq := PredictionRequest{
		Instances: instances,
	}

	body, err := json.Marshal(predReq)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	// KServe v1 prediction endpoint (more widely compatible)
	// Port 8080 is the default for RawDeployment mode, port 80 for Serverless mode
	// Note: KServe RawDeployment uses literal "model" in the URL path, not the model name
	url := fmt.Sprintf("http://%s-predictor.%s.svc.cluster.local:%d/v1/models/model:predict",
		modelName, c.namespace, c.predictorPort)

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

	var result PredictionResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &result, nil
}

// InferenceService represents a KServe InferenceService CRD
type InferenceService struct {
	Name   string
	Spec   InferenceServiceSpec
	Status InferenceServiceStatus
}

// InferenceServiceSpec represents the spec of an InferenceService
type InferenceServiceSpec struct {
	Predictor PredictorSpec
}

// PredictorSpec represents the predictor configuration
type PredictorSpec struct {
	Runtime string
}

// GetRuntime extracts the runtime from predictor spec
func (p *PredictorSpec) GetRuntime() string {
	if p.Runtime != "" {
		return p.Runtime
	}
	return "unknown"
}

// InferenceServiceStatus represents the status of an InferenceService
type InferenceServiceStatus struct {
	IsReady bool
	URL     string
}

// ListInferenceServices lists all InferenceService resources in the namespace
func (c *KServeClient) ListInferenceServices(ctx context.Context) ([]InferenceService, error) {
	if !c.enabled {
		return nil, fmt.Errorf("kserve not enabled")
	}

	if c.dynamicClient == nil {
		return nil, fmt.Errorf("kubernetes client not configured - unable to list InferenceServices")
	}

	// Define the GVR for InferenceService
	gvr := schema.GroupVersionResource{
		Group:    "serving.kserve.io",
		Version:  "v1beta1",
		Resource: "inferenceservices",
	}

	// List InferenceServices in the namespace
	list, err := c.dynamicClient.Resource(gvr).Namespace(c.namespace).List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("failed to list inferenceservices: %w", err)
	}

	// Convert unstructured list to InferenceService structs
	services := make([]InferenceService, 0, len(list.Items))
	for _, item := range list.Items {
		svc := c.convertToInferenceService(&item)
		services = append(services, svc)
	}

	return services, nil
}

// convertToInferenceService converts an unstructured object to InferenceService
func (c *KServeClient) convertToInferenceService(obj *unstructured.Unstructured) InferenceService {
	svc := InferenceService{
		Name: obj.GetName(),
	}

	// Extract spec.predictor runtime
	spec, found, err := unstructured.NestedMap(obj.Object, "spec", "predictor")
	if found && err == nil {
		runtime := extractRuntime(spec)
		svc.Spec.Predictor.Runtime = runtime
	}

	// Extract status
	statusMap, found, err := unstructured.NestedMap(obj.Object, "status")
	if found && err == nil {
		// Check if ready
		conditions, found, err := unstructured.NestedSlice(statusMap, "conditions")
		if found && err == nil {
			for _, cond := range conditions {
				if condMap, ok := cond.(map[string]interface{}); ok {
					if condType, ok := condMap["type"].(string); ok && condType == "Ready" {
						if status, ok := condMap["status"].(string); ok {
							svc.Status.IsReady = status == "True"
						}
					}
				}
			}
		}

		// Extract URL
		if url, found, err := unstructured.NestedString(statusMap, "url"); found && err == nil {
			svc.Status.URL = url
		}
	}

	return svc
}

// extractRuntime determines the runtime from predictor spec
func extractRuntime(predictor map[string]interface{}) string {
	// KServe supports multiple runtime types: sklearn, xgboost, pytorch, tensorflow, onnx, etc.
	runtimeKeys := []string{"sklearn", "xgboost", "pytorch", "tensorflow", "onnx", "triton", "huggingface", "pmml", "lightgbm"}

	for _, key := range runtimeKeys {
		if _, found := predictor[key]; found {
			return key
		}
	}

	// Check for custom predictor
	if _, found := predictor["model"]; found {
		if runtime, ok := predictor["runtime"].(string); ok {
			return runtime
		}
		return "custom"
	}

	return "unknown"
}
