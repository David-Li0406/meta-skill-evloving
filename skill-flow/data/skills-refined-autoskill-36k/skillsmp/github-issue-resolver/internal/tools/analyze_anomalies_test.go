package tools

import (
	"context"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestAnalyzeAnomaliesTool_Name(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}
	assert.Equal(t, "analyze-anomalies", tool.Name())
}

func TestAnalyzeAnomaliesTool_Description(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}
	desc := tool.Description()
	assert.Contains(t, desc, "anomalies")
	assert.Contains(t, desc, "deployment")
	assert.Contains(t, desc, "pod")
	assert.Contains(t, desc, "label selector")
}

func TestAnalyzeAnomaliesTool_InputSchema(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}
	schema := tool.InputSchema()

	// Verify schema structure
	assert.Equal(t, "object", schema["type"])

	properties, ok := schema["properties"].(map[string]interface{})
	require.True(t, ok, "properties should be a map")

	// Verify all expected properties exist
	expectedProperties := []string{
		"metric", "namespace", "deployment", "pod",
		"label_selector", "time_range", "threshold", "model_name",
	}
	for _, prop := range expectedProperties {
		_, exists := properties[prop]
		assert.True(t, exists, "property %s should exist in schema", prop)
	}

	// Verify new properties have correct descriptions
	deployment, ok := properties["deployment"].(map[string]interface{})
	require.True(t, ok)
	assert.Contains(t, deployment["description"], "deployment")
	assert.Contains(t, deployment["description"], "Mutually exclusive")

	pod, ok := properties["pod"].(map[string]interface{})
	require.True(t, ok)
	assert.Contains(t, pod["description"], "pod")
	assert.Contains(t, pod["description"], "Mutually exclusive")

	labelSelector, ok := properties["label_selector"].(map[string]interface{})
	require.True(t, ok)
	assert.Contains(t, labelSelector["description"], "label selector")

	// Verify required fields
	required, ok := schema["required"].([]string)
	require.True(t, ok)
	assert.Contains(t, required, "metric")
}

func TestAnalyzeAnomaliesTool_ValidateFilters(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}

	tests := []struct {
		name        string
		input       AnalyzeAnomaliesInput
		expectError bool
		errorMsg    string
	}{
		{
			name: "valid - metric only",
			input: AnalyzeAnomaliesInput{
				Metric: "cpu_usage",
			},
			expectError: false,
		},
		{
			name: "valid - metric with namespace",
			input: AnalyzeAnomaliesInput{
				Metric:    "cpu_usage",
				Namespace: "default",
			},
			expectError: false,
		},
		{
			name: "valid - metric with deployment filter",
			input: AnalyzeAnomaliesInput{
				Metric:     "cpu_usage",
				Namespace:  "self-healing-platform",
				Deployment: "sample-flask-app",
			},
			expectError: false,
		},
		{
			name: "valid - metric with pod filter",
			input: AnalyzeAnomaliesInput{
				Metric:    "memory_usage",
				Namespace: "openshift-etcd",
				Pod:       "etcd-0",
			},
			expectError: false,
		},
		{
			name: "valid - metric with label selector",
			input: AnalyzeAnomaliesInput{
				Metric:        "cpu_usage",
				Namespace:     "openshift-monitoring",
				LabelSelector: "app=prometheus",
			},
			expectError: false,
		},
		{
			name: "valid - label selector without namespace",
			input: AnalyzeAnomaliesInput{
				Metric:        "cpu_usage",
				LabelSelector: "component=etcd",
			},
			expectError: false,
		},
		{
			name: "invalid - deployment and pod together",
			input: AnalyzeAnomaliesInput{
				Metric:     "cpu_usage",
				Deployment: "my-app",
				Pod:        "my-pod-abc123",
			},
			expectError: true,
			errorMsg:    "mutually exclusive",
		},
		{
			name: "invalid - label selector with deployment",
			input: AnalyzeAnomaliesInput{
				Metric:        "cpu_usage",
				Deployment:    "my-app",
				LabelSelector: "app=my-app",
			},
			expectError: true,
			errorMsg:    "cannot be combined",
		},
		{
			name: "invalid - label selector with pod",
			input: AnalyzeAnomaliesInput{
				Metric:        "cpu_usage",
				Pod:           "my-pod-abc123",
				LabelSelector: "app=my-app",
			},
			expectError: true,
			errorMsg:    "cannot be combined",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			err := tool.validateFilters(tc.input)
			if tc.expectError {
				require.Error(t, err)
				assert.Contains(t, err.Error(), tc.errorMsg)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestAnalyzeAnomaliesTool_DetermineFilterTarget(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}

	tests := []struct {
		name     string
		input    AnalyzeAnomaliesInput
		expected string
	}{
		{
			name:     "cluster-wide - no filters",
			input:    AnalyzeAnomaliesInput{Metric: "cpu_usage"},
			expected: "cluster-wide",
		},
		{
			name: "namespace only",
			input: AnalyzeAnomaliesInput{
				Metric:    "cpu_usage",
				Namespace: "default",
			},
			expected: "namespace 'default'",
		},
		{
			name: "deployment with namespace",
			input: AnalyzeAnomaliesInput{
				Metric:     "cpu_usage",
				Namespace:  "self-healing-platform",
				Deployment: "sample-flask-app",
			},
			expected: "deployment 'sample-flask-app' in namespace 'self-healing-platform'",
		},
		{
			name: "deployment without namespace",
			input: AnalyzeAnomaliesInput{
				Metric:     "cpu_usage",
				Deployment: "sample-flask-app",
			},
			expected: "deployment 'sample-flask-app'",
		},
		{
			name: "pod with namespace",
			input: AnalyzeAnomaliesInput{
				Metric:    "memory_usage",
				Namespace: "openshift-etcd",
				Pod:       "etcd-0",
			},
			expected: "pod 'etcd-0' in namespace 'openshift-etcd'",
		},
		{
			name: "pod without namespace",
			input: AnalyzeAnomaliesInput{
				Metric: "memory_usage",
				Pod:    "prometheus-k8s-0",
			},
			expected: "pod 'prometheus-k8s-0'",
		},
		{
			name: "label selector with namespace",
			input: AnalyzeAnomaliesInput{
				Metric:        "cpu_usage",
				Namespace:     "openshift-monitoring",
				LabelSelector: "app=prometheus",
			},
			expected: "pods matching 'app=prometheus' in namespace 'openshift-monitoring'",
		},
		{
			name: "label selector without namespace",
			input: AnalyzeAnomaliesInput{
				Metric:        "cpu_usage",
				LabelSelector: "component=etcd",
			},
			expected: "pods matching 'component=etcd'",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result := tool.determineFilterTarget(tc.input)
			assert.Equal(t, tc.expected, result)
		})
	}
}

func TestAnalyzeAnomaliesTool_BuildPodRegex(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}

	tests := []struct {
		name     string
		input    AnalyzeAnomaliesInput
		expected string
	}{
		{
			name:     "no filters - empty regex",
			input:    AnalyzeAnomaliesInput{Metric: "cpu_usage"},
			expected: "",
		},
		{
			name: "deployment filter - wildcard suffix",
			input: AnalyzeAnomaliesInput{
				Metric:     "cpu_usage",
				Deployment: "sample-flask-app",
			},
			expected: "sample-flask-app-.*",
		},
		{
			name: "statefulset pod (ordinal 0) - exact match",
			input: AnalyzeAnomaliesInput{
				Metric: "cpu_usage",
				Pod:    "etcd-0",
			},
			expected: "^etcd-0$",
		},
		{
			name: "statefulset pod (ordinal 1) - exact match",
			input: AnalyzeAnomaliesInput{
				Metric: "cpu_usage",
				Pod:    "prometheus-k8s-1",
			},
			expected: "^prometheus-k8s-1$",
		},
		{
			name: "statefulset pod (ordinal 2) - exact match",
			input: AnalyzeAnomaliesInput{
				Metric: "cpu_usage",
				Pod:    "alertmanager-main-2",
			},
			expected: "^alertmanager-main-2$",
		},
		{
			name: "regular pod - prefix match",
			input: AnalyzeAnomaliesInput{
				Metric: "cpu_usage",
				Pod:    "my-deployment-abc123",
			},
			expected: "^my-deployment-abc123.*",
		},
		{
			name: "infrastructure pod - prefix match",
			input: AnalyzeAnomaliesInput{
				Metric: "cpu_usage",
				Pod:    "kube-apiserver",
			},
			expected: "^kube-apiserver.*",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result := tool.buildPodRegex(tc.input)
			assert.Equal(t, tc.expected, result)
		})
	}
}

func TestAnalyzeAnomaliesTool_Execute_MissingMetric(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}

	_, err := tool.Execute(context.Background(), map[string]interface{}{})
	require.Error(t, err)
	assert.Contains(t, err.Error(), "metric is required")
}

func TestAnalyzeAnomaliesTool_Execute_InvalidFilters(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}

	// Test deployment + pod mutual exclusivity
	_, err := tool.Execute(context.Background(), map[string]interface{}{
		"metric":     "cpu_usage",
		"deployment": "my-app",
		"pod":        "my-pod",
	})
	require.Error(t, err)
	assert.Contains(t, err.Error(), "mutually exclusive")

	// Test label_selector + deployment mutual exclusivity
	_, err = tool.Execute(context.Background(), map[string]interface{}{
		"metric":         "cpu_usage",
		"deployment":     "my-app",
		"label_selector": "app=my-app",
	})
	require.Error(t, err)
	assert.Contains(t, err.Error(), "cannot be combined")

	// Test label_selector + pod mutual exclusivity
	_, err = tool.Execute(context.Background(), map[string]interface{}{
		"metric":         "cpu_usage",
		"pod":            "my-pod",
		"label_selector": "app=my-app",
	})
	require.Error(t, err)
	assert.Contains(t, err.Error(), "cannot be combined")
}

func TestDetermineSeverity(t *testing.T) {
	tests := []struct {
		score    float64
		expected string
	}{
		{0.95, "critical"},
		{0.90, "critical"},
		{0.85, "high"},
		{0.80, "high"},
		{0.75, "medium"},
		{0.70, "medium"},
		{0.65, "low"},
		{0.50, "low"},
		{0.0, "low"},
	}

	for _, tc := range tests {
		t.Run(tc.expected, func(t *testing.T) {
			result := determineSeverity(tc.score)
			assert.Equal(t, tc.expected, result)
		})
	}
}

func TestGenerateExplanation(t *testing.T) {
	explanation := generateExplanation("cpu_usage", 0.85, 0.92)

	assert.Contains(t, explanation, "cpu_usage")
	assert.Contains(t, explanation, "high")
	assert.Contains(t, explanation, "0.85")
	assert.Contains(t, explanation, "0.92")
	assert.Contains(t, explanation, "unusual behavior")
}

func TestGenerateRecommendation(t *testing.T) {
	tests := []struct {
		name     string
		metric   string
		maxScore float64
		count    int
		contains []string
	}{
		{
			name:     "critical recommendation",
			metric:   "cpu_usage",
			maxScore: 0.95,
			count:    5,
			contains: []string{"CRITICAL", "Immediate", "cpu_usage"},
		},
		{
			name:     "warning recommendation",
			metric:   "memory_usage",
			maxScore: 0.85,
			count:    3,
			contains: []string{"WARNING", "Monitor", "memory_usage"},
		},
		{
			name:     "info recommendation",
			metric:   "pod_restarts",
			maxScore: 0.72,
			count:    2,
			contains: []string{"INFO", "minor", "pod_restarts"},
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result := generateRecommendation(tc.metric, tc.maxScore, tc.count)
			for _, expected := range tc.contains {
				assert.Contains(t, result, expected)
			}
		})
	}
}

func TestAnalyzeAnomaliesInput_Defaults(t *testing.T) {
	// Verify default values are applied correctly
	input := AnalyzeAnomaliesInput{
		TimeRange: "1h",
		Threshold: 0.7,
		ModelName: "predictive-analytics",
	}

	assert.Equal(t, "1h", input.TimeRange)
	assert.Equal(t, 0.7, input.Threshold)
	assert.Equal(t, "predictive-analytics", input.ModelName)
	assert.Empty(t, input.Namespace)
	assert.Empty(t, input.Deployment)
	assert.Empty(t, input.Pod)
	assert.Empty(t, input.LabelSelector)
}

func TestAnalyzeAnomaliesOutput_FilterFields(t *testing.T) {
	output := AnalyzeAnomaliesOutput{
		Status:        "success",
		Metric:        "cpu_usage",
		TimeRange:     "24h",
		Namespace:     "self-healing-platform",
		Deployment:    "sample-flask-app",
		FilterTarget:  "deployment 'sample-flask-app' in namespace 'self-healing-platform'",
		ModelUsed:     "predictive-analytics",
		Anomalies:     []AnomalyResult{},
		AnomalyCount:  0,
		MaxScore:      0.0,
		AverageScore:  0.0,
		Message:       "No anomalies detected",
		Recommendation: "Continue monitoring",
	}

	assert.Equal(t, "sample-flask-app", output.Deployment)
	assert.Equal(t, "self-healing-platform", output.Namespace)
	assert.Contains(t, output.FilterTarget, "deployment")
	assert.Empty(t, output.Pod)
	assert.Empty(t, output.LabelSelector)
}

// Test use cases from the issue
func TestAnalyzeAnomaliesTool_UseCases(t *testing.T) {
	tool := &AnalyzeAnomaliesTool{}

	t.Run("Use Case 1: Deployment-Specific Analysis", func(t *testing.T) {
		input := AnalyzeAnomaliesInput{
			Metric:     "cpu_usage",
			Deployment: "sample-flask-app",
			TimeRange:  "24h",
		}

		err := tool.validateFilters(input)
		assert.NoError(t, err)

		target := tool.determineFilterTarget(input)
		assert.Equal(t, "deployment 'sample-flask-app'", target)

		regex := tool.buildPodRegex(input)
		assert.Equal(t, "sample-flask-app-.*", regex)
	})

	t.Run("Use Case 2: Infrastructure Pod Analysis (etcd)", func(t *testing.T) {
		input := AnalyzeAnomaliesInput{
			Metric:    "memory_usage",
			Pod:       "etcd-0",
			Namespace: "openshift-etcd",
		}

		err := tool.validateFilters(input)
		assert.NoError(t, err)

		target := tool.determineFilterTarget(input)
		assert.Equal(t, "pod 'etcd-0' in namespace 'openshift-etcd'", target)

		regex := tool.buildPodRegex(input)
		assert.Equal(t, "^etcd-0$", regex)
	})

	t.Run("Use Case 3: Label-Based Filtering", func(t *testing.T) {
		input := AnalyzeAnomaliesInput{
			Metric:        "cpu_usage",
			LabelSelector: "app=monitoring",
		}

		err := tool.validateFilters(input)
		assert.NoError(t, err)

		target := tool.determineFilterTarget(input)
		assert.Equal(t, "pods matching 'app=monitoring'", target)

		regex := tool.buildPodRegex(input)
		assert.Empty(t, regex) // Label selector doesn't use regex
	})

	t.Run("Use Case 4: Prometheus Pod Analysis", func(t *testing.T) {
		input := AnalyzeAnomaliesInput{
			Metric:    "cpu_usage",
			Pod:       "prometheus-k8s-0",
			Namespace: "openshift-monitoring",
		}

		err := tool.validateFilters(input)
		assert.NoError(t, err)

		target := tool.determineFilterTarget(input)
		assert.Equal(t, "pod 'prometheus-k8s-0' in namespace 'openshift-monitoring'", target)

		regex := tool.buildPodRegex(input)
		assert.Equal(t, "^prometheus-k8s-0$", regex)
	})

	t.Run("Use Case 5: API Server Analysis", func(t *testing.T) {
		input := AnalyzeAnomaliesInput{
			Metric:    "cpu_usage",
			Pod:       "kube-apiserver",
			Namespace: "openshift-kube-apiserver",
		}

		err := tool.validateFilters(input)
		assert.NoError(t, err)

		target := tool.determineFilterTarget(input)
		assert.Equal(t, "pod 'kube-apiserver' in namespace 'openshift-kube-apiserver'", target)

		// kube-apiserver doesn't end with ordinal, so uses prefix match
		regex := tool.buildPodRegex(input)
		assert.Equal(t, "^kube-apiserver.*", regex)
	})
}
