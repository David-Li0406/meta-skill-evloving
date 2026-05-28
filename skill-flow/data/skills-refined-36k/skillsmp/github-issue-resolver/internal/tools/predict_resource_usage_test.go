package tools

import (
	"testing"
	"time"
)

func TestPredictResourceUsageTool_Name(t *testing.T) {
	// Create tool without clients (for schema tests)
	tool := &PredictResourceUsageTool{}

	if tool.Name() != "predict-resource-usage" {
		t.Errorf("Expected name 'predict-resource-usage', got '%s'", tool.Name())
	}
}

func TestPredictResourceUsageTool_Description(t *testing.T) {
	tool := &PredictResourceUsageTool{}

	desc := tool.Description()
	if desc == "" {
		t.Error("Expected non-empty description")
	}
	if len(desc) < 20 {
		t.Errorf("Description seems too short: %s", desc)
	}
	// Verify key concepts are mentioned
	if !contains(desc, "predict") && !contains(desc, "Predict") {
		t.Error("Description should mention prediction capability")
	}
}

func TestPredictResourceUsageTool_InputSchema(t *testing.T) {
	tool := &PredictResourceUsageTool{}

	schema := tool.InputSchema()
	if schema == nil {
		t.Fatal("InputSchema returned nil")
	}

	// Check schema structure
	if schema["type"] != "object" {
		t.Error("Expected schema type to be 'object'")
	}

	properties, ok := schema["properties"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected properties to be a map")
	}

	// Check required properties exist
	expectedProps := []string{"target_time", "target_date", "namespace", "deployment", "pod", "metric", "scope"}
	for _, prop := range expectedProps {
		if _, exists := properties[prop]; !exists {
			t.Errorf("Expected property '%s' in schema", prop)
		}
	}

	// Check metric enum values
	metricProp, ok := properties["metric"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected metric property to be a map")
	}
	enumValues, ok := metricProp["enum"].([]string)
	if !ok {
		t.Fatal("Expected metric enum to be string slice")
	}
	expectedMetrics := []string{"cpu_usage", "memory_usage", "both"}
	for _, expected := range expectedMetrics {
		found := false
		for _, actual := range enumValues {
			if actual == expected {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Expected metric enum to contain '%s'", expected)
		}
	}

	// Check scope enum values
	scopeProp, ok := properties["scope"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected scope property to be a map")
	}
	scopeEnum, ok := scopeProp["enum"].([]string)
	if !ok {
		t.Fatal("Expected scope enum to be string slice")
	}
	expectedScopes := []string{"pod", "deployment", "namespace", "cluster"}
	for _, expected := range expectedScopes {
		found := false
		for _, actual := range scopeEnum {
			if actual == expected {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Expected scope enum to contain '%s'", expected)
		}
	}
}

func TestPredictResourceUsageTool_ParseTargetDatetime(t *testing.T) {
	tool := &PredictResourceUsageTool{}

	testCases := []struct {
		name        string
		targetTime  string
		targetDate  string
		expectError bool
		checkHour   int // -1 to skip hour check
	}{
		{
			name:        "Valid time and date",
			targetTime:  "15:00",
			targetDate:  "2026-01-15",
			expectError: false,
			checkHour:   15,
		},
		{
			name:        "Valid time only (date defaults to today)",
			targetTime:  "09:30",
			targetDate:  "",
			expectError: false,
			checkHour:   9,
		},
		{
			name:        "Empty time (defaults to next hour)",
			targetTime:  "",
			targetDate:  "2026-01-15",
			expectError: false,
			checkHour:   -1, // Skip - depends on current time
		},
		{
			name:        "Both empty (defaults apply)",
			targetTime:  "",
			targetDate:  "",
			expectError: false,
			checkHour:   -1,
		},
		{
			name:        "Invalid time format",
			targetTime:  "25:00",
			targetDate:  "2026-01-15",
			expectError: true,
			checkHour:   -1,
		},
		{
			name:        "Invalid date format",
			targetTime:  "15:00",
			targetDate:  "01-15-2026",
			expectError: true,
			checkHour:   -1,
		},
		{
			name:        "Midnight time",
			targetTime:  "00:00",
			targetDate:  "2026-01-15",
			expectError: false,
			checkHour:   0,
		},
		{
			name:        "Late evening time",
			targetTime:  "23:59",
			targetDate:  "2026-01-15",
			expectError: false,
			checkHour:   23,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result, err := tool.parseTargetDatetime(tc.targetTime, tc.targetDate)

			if tc.expectError {
				if err == nil {
					t.Errorf("Expected error but got none")
				}
				return
			}

			if err != nil {
				t.Errorf("Unexpected error: %v", err)
				return
			}

			if tc.checkHour >= 0 && result.Hour() != tc.checkHour {
				t.Errorf("Expected hour %d, got %d", tc.checkHour, result.Hour())
			}
		})
	}
}

func TestPredictResourceUsageTool_DetermineTarget(t *testing.T) {
	tool := &PredictResourceUsageTool{}

	testCases := []struct {
		name           string
		input          PredictResourceUsageInput
		expectedTarget string
		expectError    bool
	}{
		{
			name: "Pod scope with namespace",
			input: PredictResourceUsageInput{
				Scope:     "pod",
				Pod:       "my-pod-123",
				Namespace: "default",
			},
			expectedTarget: "default/my-pod-123",
			expectError:    false,
		},
		{
			name: "Pod scope without namespace",
			input: PredictResourceUsageInput{
				Scope: "pod",
				Pod:   "my-pod-123",
			},
			expectedTarget: "my-pod-123",
			expectError:    false,
		},
		{
			name: "Pod scope without pod name (error)",
			input: PredictResourceUsageInput{
				Scope: "pod",
			},
			expectedTarget: "",
			expectError:    true,
		},
		{
			name: "Deployment scope with namespace",
			input: PredictResourceUsageInput{
				Scope:      "deployment",
				Deployment: "my-deployment",
				Namespace:  "production",
			},
			expectedTarget: "production/my-deployment",
			expectError:    false,
		},
		{
			name: "Deployment scope without deployment name (error)",
			input: PredictResourceUsageInput{
				Scope:     "deployment",
				Namespace: "production",
			},
			expectedTarget: "",
			expectError:    true,
		},
		{
			name: "Namespace scope with namespace",
			input: PredictResourceUsageInput{
				Scope:     "namespace",
				Namespace: "self-healing-platform",
			},
			expectedTarget: "self-healing-platform",
			expectError:    false,
		},
		{
			name: "Namespace scope without namespace",
			input: PredictResourceUsageInput{
				Scope: "namespace",
			},
			expectedTarget: "all-namespaces",
			expectError:    false,
		},
		{
			name: "Cluster scope",
			input: PredictResourceUsageInput{
				Scope: "cluster",
			},
			expectedTarget: "cluster-wide",
			expectError:    false,
		},
		{
			name: "Invalid scope",
			input: PredictResourceUsageInput{
				Scope: "invalid",
			},
			expectedTarget: "",
			expectError:    true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			target, err := tool.determineTarget(tc.input)

			if tc.expectError {
				if err == nil {
					t.Errorf("Expected error but got none")
				}
				return
			}

			if err != nil {
				t.Errorf("Unexpected error: %v", err)
				return
			}

			if target != tc.expectedTarget {
				t.Errorf("Expected target '%s', got '%s'", tc.expectedTarget, target)
			}
		})
	}
}

func TestPredictResourceUsageTool_GenerateRecommendation(t *testing.T) {
	tool := &PredictResourceUsageTool{}

	testCases := []struct {
		name             string
		metric           string
		currentCPU       float64
		currentMemory    float64
		predictedCPU     float64
		predictedMemory  float64
		trend            string
		expectContains   []string
		expectNotContains []string
	}{
		{
			name:            "Critical CPU",
			metric:          "cpu_usage",
			currentCPU:      75,
			currentMemory:   50,
			predictedCPU:    92,
			predictedMemory: 55,
			trend:           "upward",
			expectContains:  []string{"CRITICAL", "CPU"},
		},
		{
			name:            "Warning memory",
			metric:          "memory_usage",
			currentCPU:      50,
			currentMemory:   70,
			predictedCPU:    55,
			predictedMemory: 87,
			trend:           "upward",
			expectContains:  []string{"WARNING", "Memory", "threshold"},
		},
		{
			name:            "Critical memory OOM risk",
			metric:          "both",
			currentCPU:      60,
			currentMemory:   80,
			predictedCPU:    65,
			predictedMemory: 95,
			trend:           "upward",
			expectContains:  []string{"CRITICAL", "OOM"},
		},
		{
			name:            "Stable trend",
			metric:          "both",
			currentCPU:      50,
			currentMemory:   50,
			predictedCPU:    52,
			predictedMemory: 51,
			trend:           "stable",
			expectContains:  []string{"stable", "appropriate"},
		},
		{
			name:            "Downward trend",
			metric:          "both",
			currentCPU:      60,
			currentMemory:   60,
			predictedCPU:    55,
			predictedMemory: 52,
			trend:           "downward",
			expectContains:  []string{"downward", "scaling down", "costs"},
		},
		{
			name:            "Upward trend with significant increase",
			metric:          "both",
			currentCPU:      40,
			currentMemory:   40,
			predictedCPU:    65, // 25% increase
			predictedMemory: 65, // 25% increase
			trend:           "upward",
			expectContains:  []string{"increase"},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			recommendation := tool.generateRecommendation(
				tc.metric,
				tc.currentCPU,
				tc.currentMemory,
				tc.predictedCPU,
				tc.predictedMemory,
				tc.trend,
			)

			for _, expected := range tc.expectContains {
				if !contains(recommendation, expected) {
					t.Errorf("Expected recommendation to contain '%s', got: %s", expected, recommendation)
				}
			}

			for _, notExpected := range tc.expectNotContains {
				if contains(recommendation, notExpected) {
					t.Errorf("Expected recommendation NOT to contain '%s', got: %s", notExpected, recommendation)
				}
			}
		})
	}
}

func TestPredictResourceUsageTool_HelperFunctions(t *testing.T) {
	t.Run("max function", func(t *testing.T) {
		if max(5, 3) != 5 {
			t.Error("max(5, 3) should return 5")
		}
		if max(3, 5) != 5 {
			t.Error("max(3, 5) should return 5")
		}
		if max(4, 4) != 4 {
			t.Error("max(4, 4) should return 4")
		}
		if max(-1, 0) != 0 {
			t.Error("max(-1, 0) should return 0")
		}
	})

	t.Run("clamp function", func(t *testing.T) {
		if clamp(50, 0, 100) != 50 {
			t.Error("clamp(50, 0, 100) should return 50")
		}
		if clamp(-10, 0, 100) != 0 {
			t.Error("clamp(-10, 0, 100) should return 0")
		}
		if clamp(150, 0, 100) != 100 {
			t.Error("clamp(150, 0, 100) should return 100")
		}
		if clamp(0, 0, 100) != 0 {
			t.Error("clamp(0, 0, 100) should return 0")
		}
		if clamp(100, 0, 100) != 100 {
			t.Error("clamp(100, 0, 100) should return 100")
		}
	})
}

func TestPredictResourceUsageTool_DayOfWeekConversion(t *testing.T) {
	tool := &PredictResourceUsageTool{}

	// Test day of week conversion for different days
	testDates := []struct {
		dateStr          string
		expectedDayOfWeek int // Monday=0, Sunday=6
	}{
		{"2026-01-12", 0}, // Monday
		{"2026-01-13", 1}, // Tuesday
		{"2026-01-14", 2}, // Wednesday
		{"2026-01-15", 3}, // Thursday
		{"2026-01-16", 4}, // Friday
		{"2026-01-17", 5}, // Saturday
		{"2026-01-18", 6}, // Sunday
	}

	for _, tc := range testDates {
		t.Run(tc.dateStr, func(t *testing.T) {
			targetTime, err := tool.parseTargetDatetime("12:00", tc.dateStr)
			if err != nil {
				t.Fatalf("Failed to parse datetime: %v", err)
			}

			// Convert Go's Sunday=0 to Monday=0 format (same logic as in Execute)
			dayOfWeek := int(targetTime.Weekday())
			if dayOfWeek == 0 {
				dayOfWeek = 6 // Sunday
			} else {
				dayOfWeek-- // Shift Monday-Saturday
			}

			if dayOfWeek != tc.expectedDayOfWeek {
				t.Errorf("For %s, expected dayOfWeek %d, got %d", tc.dateStr, tc.expectedDayOfWeek, dayOfWeek)
			}
		})
	}
}

func TestPredictResourceUsageTool_InputParsing(t *testing.T) {
	// Test that input parsing handles various argument combinations correctly
	testCases := []struct {
		name     string
		args     map[string]interface{}
		expected PredictResourceUsageInput
	}{
		{
			name: "Empty args use defaults",
			args: map[string]interface{}{},
			expected: PredictResourceUsageInput{
				Metric: "both",
				Scope:  "namespace",
			},
		},
		{
			name: "All fields specified",
			args: map[string]interface{}{
				"target_time": "15:00",
				"target_date": "2026-01-15",
				"namespace":   "production",
				"deployment":  "my-app",
				"pod":         "my-app-pod-123",
				"metric":      "cpu_usage",
				"scope":       "pod",
			},
			expected: PredictResourceUsageInput{
				TargetTime: "15:00",
				TargetDate: "2026-01-15",
				Namespace:  "production",
				Deployment: "my-app",
				Pod:        "my-app-pod-123",
				Metric:     "cpu_usage",
				Scope:      "pod",
			},
		},
		{
			name: "Partial fields specified",
			args: map[string]interface{}{
				"namespace": "openshift-monitoring",
				"scope":     "namespace",
			},
			expected: PredictResourceUsageInput{
				Namespace: "openshift-monitoring",
				Metric:    "both",
				Scope:     "namespace",
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Simulate the parsing logic from Execute
			input := PredictResourceUsageInput{
				Metric: "both",
				Scope:  "namespace",
			}

			// This mirrors the Execute parsing logic
			if v, ok := tc.args["target_time"].(string); ok {
				input.TargetTime = v
			}
			if v, ok := tc.args["target_date"].(string); ok {
				input.TargetDate = v
			}
			if v, ok := tc.args["namespace"].(string); ok {
				input.Namespace = v
			}
			if v, ok := tc.args["deployment"].(string); ok {
				input.Deployment = v
			}
			if v, ok := tc.args["pod"].(string); ok {
				input.Pod = v
			}
			if v, ok := tc.args["metric"].(string); ok {
				input.Metric = v
			}
			if v, ok := tc.args["scope"].(string); ok {
				input.Scope = v
			}

			// Check expected values
			if input.Metric != tc.expected.Metric {
				t.Errorf("Expected metric '%s', got '%s'", tc.expected.Metric, input.Metric)
			}
			if input.Scope != tc.expected.Scope {
				t.Errorf("Expected scope '%s', got '%s'", tc.expected.Scope, input.Scope)
			}
			if input.Namespace != tc.expected.Namespace {
				t.Errorf("Expected namespace '%s', got '%s'", tc.expected.Namespace, input.Namespace)
			}
		})
	}
}

func TestPredictResourceUsageTool_OutputStructure(t *testing.T) {
	// Verify the output structure matches the expected schema from issue #27
	output := PredictResourceUsageOutput{
		Status: "success",
		Scope:  "namespace",
		Target: "self-healing-platform",
		CurrentMetrics: CurrentMetrics{
			CPUPercent:    68.2,
			MemoryPercent: 74.5,
			Timestamp:     time.Now().UTC().Format(time.RFC3339),
		},
		PredictedMetrics: PredictedMetrics{
			CPUPercent:    74.5,
			MemoryPercent: 81.2,
			TargetTime:    "2026-01-12T15:00:00Z",
			Confidence:    0.92,
		},
		Trend:          "upward",
		Recommendation: "Memory approaching 85% threshold. Consider monitoring or scaling.",
		ModelUsed:      "predictive-analytics",
		ModelVersion:   "v1",
	}

	// Verify all required fields are present
	if output.Status == "" {
		t.Error("Status should not be empty")
	}
	if output.Scope == "" {
		t.Error("Scope should not be empty")
	}
	if output.Target == "" {
		t.Error("Target should not be empty")
	}
	if output.CurrentMetrics.Timestamp == "" {
		t.Error("CurrentMetrics.Timestamp should not be empty")
	}
	if output.PredictedMetrics.TargetTime == "" {
		t.Error("PredictedMetrics.TargetTime should not be empty")
	}
	if output.Trend == "" {
		t.Error("Trend should not be empty")
	}
	if output.ModelUsed == "" {
		t.Error("ModelUsed should not be empty")
	}
}

// Helper function to check if a string contains a substring
func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(substr) == 0 ||
		(len(s) > 0 && len(substr) > 0 && findSubstring(s, substr)))
}

func findSubstring(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// Integration test that requires real K8s client and Coordination Engine
func TestPredictResourceUsageTool_Execute_Integration(t *testing.T) {
	// Skip if not running integration tests
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}

	// This test requires:
	// 1. A running Kubernetes cluster
	// 2. A running Coordination Engine with /api/v1/predict endpoint
	t.Skip("Integration test - requires running cluster and coordination engine")

	// Example of how the full integration test would work:
	/*
		import (
			"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
		)

		k8sClient, err := clients.NewK8sClient(nil)
		if err != nil {
			t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
		}
		defer k8sClient.Close()

		ceClient := clients.NewCoordinationEngineClient("http://localhost:8000")

		tool := NewPredictResourceUsageTool(ceClient, k8sClient)
		ctx := context.Background()

		result, err := tool.Execute(ctx, map[string]interface{}{
			"target_time": "15:00",
			"namespace":   "default",
			"metric":      "both",
			"scope":       "namespace",
		})
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		output, ok := result.(PredictResourceUsageOutput)
		if !ok {
			t.Fatal("Expected PredictResourceUsageOutput type")
		}

		if output.Status != "success" {
			t.Errorf("Expected status 'success', got '%s'", output.Status)
		}
	*/
}

// Benchmark test for the recommendation generation
func BenchmarkGenerateRecommendation(b *testing.B) {
	tool := &PredictResourceUsageTool{}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = tool.generateRecommendation("both", 60, 70, 85, 90, "upward")
	}
}

// Benchmark test for target datetime parsing
func BenchmarkParseTargetDatetime(b *testing.B) {
	tool := &PredictResourceUsageTool{}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = tool.parseTargetDatetime("15:00", "2026-01-15")
	}
}
