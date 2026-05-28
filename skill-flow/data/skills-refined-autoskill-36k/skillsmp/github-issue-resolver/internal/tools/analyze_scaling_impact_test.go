package tools

import (
	"testing"
)

func TestAnalyzeScalingImpactTool_Name(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	if tool.Name() != "analyze-scaling-impact" {
		t.Errorf("Expected name 'analyze-scaling-impact', got '%s'", tool.Name())
	}
}

func TestAnalyzeScalingImpactTool_Description(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	desc := tool.Description()
	if desc == "" {
		t.Error("Expected non-empty description")
	}
	if len(desc) < 20 {
		t.Errorf("Description seems too short: %s", desc)
	}
	// Verify key concepts are mentioned
	if !contains(desc, "scaling") && !contains(desc, "Scaling") {
		t.Error("Description should mention scaling capability")
	}
	if !contains(desc, "impact") {
		t.Error("Description should mention impact analysis")
	}
}

func TestAnalyzeScalingImpactTool_InputSchema(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

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
	expectedProps := []string{"deployment", "namespace", "current_replicas", "target_replicas", "predict_at", "include_infrastructure"}
	for _, prop := range expectedProps {
		if _, exists := properties[prop]; !exists {
			t.Errorf("Expected property '%s' in schema", prop)
		}
	}

	// Check required array
	required, ok := schema["required"].([]string)
	if !ok {
		t.Fatal("Expected required to be a string slice")
	}

	expectedRequired := []string{"deployment", "namespace", "target_replicas"}
	for _, req := range expectedRequired {
		found := false
		for _, actual := range required {
			if actual == req {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Expected '%s' to be in required array", req)
		}
	}
}

func TestAnalyzeScalingImpactTool_ParseInput(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	testCases := []struct {
		name        string
		args        map[string]interface{}
		expected    *AnalyzeScalingImpactInput
		expectError bool
	}{
		{
			name: "All fields provided",
			args: map[string]interface{}{
				"deployment":             "sample-flask-app",
				"namespace":              "my-namespace",
				"current_replicas":       float64(2),
				"target_replicas":        float64(5),
				"predict_at":             "17:00",
				"include_infrastructure": true,
			},
			expected: &AnalyzeScalingImpactInput{
				Deployment:      "sample-flask-app",
				Namespace:       "my-namespace",
				TargetReplicas:  5,
				PredictAt:       "17:00",
			},
			expectError: false,
		},
		{
			name: "Required fields only",
			args: map[string]interface{}{
				"deployment":      "my-app",
				"namespace":       "production",
				"target_replicas": float64(10),
			},
			expected: &AnalyzeScalingImpactInput{
				Deployment:     "my-app",
				Namespace:      "production",
				TargetReplicas: 10,
			},
			expectError: false,
		},
		{
			name: "Integer type for replicas",
			args: map[string]interface{}{
				"deployment":      "api",
				"namespace":       "default",
				"target_replicas": 3,
			},
			expected: &AnalyzeScalingImpactInput{
				Deployment:     "api",
				Namespace:      "default",
				TargetReplicas: 3,
			},
			expectError: false,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			input, err := tool.parseInput(tc.args)

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

			if input.Deployment != tc.expected.Deployment {
				t.Errorf("Expected deployment '%s', got '%s'", tc.expected.Deployment, input.Deployment)
			}
			if input.Namespace != tc.expected.Namespace {
				t.Errorf("Expected namespace '%s', got '%s'", tc.expected.Namespace, input.Namespace)
			}
			if input.TargetReplicas != tc.expected.TargetReplicas {
				t.Errorf("Expected target_replicas %d, got %d", tc.expected.TargetReplicas, input.TargetReplicas)
			}
		})
	}
}

func TestAnalyzeScalingImpactTool_CalculateNamespaceImpact(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	testCases := []struct {
		name            string
		current         CurrentState
		projected       ProjectedState
		quota           *NamespaceQuotaInfo
		currentReplicas int
		expectExceeded  bool
		expectWarning   bool // projected > 85%
	}{
		{
			name: "Scale up within quota",
			current: CurrentState{
				Replicas:        2,
				CPUPerPodAvg:    100,
				MemoryPerPodAvg: 128,
				TotalCPU:        200,
				TotalMemory:     256,
			},
			projected: ProjectedState{
				Replicas:        5,
				CPUPerPodEst:    105,
				MemoryPerPodEst: 134,
				TotalCPU:        525,
				TotalMemory:     670,
			},
			quota: &NamespaceQuotaInfo{
				CPULimitMillicores: 4000,
				MemoryLimitBytes:   8 * 1024 * 1024 * 1024,
				CPUUsedMillicores:  1000,
				MemoryUsedBytes:    2 * 1024 * 1024 * 1024,
			},
			currentReplicas: 2,
			expectExceeded:  false,
			expectWarning:   false,
		},
		{
			name: "Scale up exceeds quota",
			current: CurrentState{
				Replicas:        5,
				CPUPerPodAvg:    500,
				MemoryPerPodAvg: 512,
				TotalCPU:        2500,
				TotalMemory:     2560,
			},
			projected: ProjectedState{
				Replicas:        20,
				CPUPerPodEst:    510,
				MemoryPerPodEst: 522,
				TotalCPU:        10200,
				TotalMemory:     10440,
			},
			quota: &NamespaceQuotaInfo{
				CPULimitMillicores: 4000,
				MemoryLimitBytes:   4 * 1024 * 1024 * 1024,
				CPUUsedMillicores:  2500,
				MemoryUsedBytes:    2560 * 1024 * 1024,
			},
			currentReplicas: 5,
			expectExceeded:  true,
			expectWarning:   true,
		},
		{
			name: "Scale up approaches threshold",
			current: CurrentState{
				Replicas:        3,
				CPUPerPodAvg:    200,
				MemoryPerPodAvg: 256,
				TotalCPU:        600,
				TotalMemory:     768,
			},
			projected: ProjectedState{
				Replicas:        10,
				CPUPerPodEst:    220,
				MemoryPerPodEst: 280,
				TotalCPU:        2200,
				TotalMemory:     2800,
			},
			quota: &NamespaceQuotaInfo{
				CPULimitMillicores: 2500,
				MemoryLimitBytes:   3 * 1024 * 1024 * 1024,
				CPUUsedMillicores:  600,
				MemoryUsedBytes:    768 * 1024 * 1024,
			},
			currentReplicas: 3,
			expectExceeded:  false,
			expectWarning:   true, // Should be close to or above 85%
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			impact := tool.calculateNamespaceImpact(tc.current, tc.projected, tc.quota, tc.currentReplicas)

			if impact.QuotaExceeded != tc.expectExceeded {
				t.Errorf("Expected QuotaExceeded=%v, got %v (projected: %.1f%%)",
					tc.expectExceeded, impact.QuotaExceeded, impact.ProjectedUsagePercent)
			}

			if tc.expectWarning && impact.ProjectedUsagePercent < 85 {
				t.Errorf("Expected warning threshold (>=85%%), got %.1f%%", impact.ProjectedUsagePercent)
			}

			if impact.LimitingFactor != "cpu" && impact.LimitingFactor != "memory" {
				t.Errorf("Expected limiting_factor to be 'cpu' or 'memory', got '%s'", impact.LimitingFactor)
			}
		})
	}
}

func TestAnalyzeScalingImpactTool_AnalyzeInfrastructureImpact(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	testCases := []struct {
		name            string
		currentReplicas int
		targetReplicas  int
		namespace       string
		expectHighAPI   bool
		expectHighEtcd  bool
	}{
		{
			name:            "Small scale up",
			currentReplicas: 2,
			targetReplicas:  4,
			namespace:       "my-app",
			expectHighAPI:   false,
			expectHighEtcd:  false,
		},
		{
			name:            "Large scale up",
			currentReplicas: 2,
			targetReplicas:  15,
			namespace:       "my-app",
			expectHighAPI:   true,
			expectHighEtcd:  true,
		},
		{
			name:            "Infrastructure namespace",
			currentReplicas: 2,
			targetReplicas:  5,
			namespace:       "openshift-monitoring",
			expectHighAPI:   false, // But should be medium due to infra namespace
			expectHighEtcd:  false,
		},
		{
			name:            "Scale down",
			currentReplicas: 10,
			targetReplicas:  5,
			namespace:       "production",
			expectHighAPI:   false,
			expectHighEtcd:  false,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			impact := tool.analyzeInfrastructureImpact(tc.currentReplicas, tc.targetReplicas, tc.namespace)

			if impact == nil {
				t.Fatal("Expected non-nil infrastructure impact")
			}

			if tc.expectHighAPI && impact.APIServerImpact != "high" {
				t.Errorf("Expected high API server impact, got '%s'", impact.APIServerImpact)
			}
			if tc.expectHighEtcd && impact.EtcdImpact != "high" {
				t.Errorf("Expected high etcd impact, got '%s'", impact.EtcdImpact)
			}

			// Verify valid impact levels
			validLevels := map[string]bool{"low": true, "medium": true, "high": true}
			if !validLevels[impact.EtcdImpact] {
				t.Errorf("Invalid etcd impact level: %s", impact.EtcdImpact)
			}
			if !validLevels[impact.APIServerImpact] {
				t.Errorf("Invalid API server impact level: %s", impact.APIServerImpact)
			}
			if !validLevels[impact.SchedulerImpact] {
				t.Errorf("Invalid scheduler impact level: %s", impact.SchedulerImpact)
			}

			if impact.EstimatedOverhead == "" {
				t.Error("Expected non-empty estimated overhead")
			}
		})
	}
}

func TestAnalyzeScalingImpactTool_GenerateWarnings(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	testCases := []struct {
		name           string
		nsImpact       NamespaceImpact
		infraImpact    *InfrastructureImpact
		expectWarnings int
		expectCritical bool
	}{
		{
			name: "No warnings - safe scaling",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  60,
				QuotaExceeded:          false,
				HeadroomRemainingPct:   40,
				LimitingFactor:         "memory",
			},
			infraImpact:    &InfrastructureImpact{EtcdImpact: "low", APIServerImpact: "low", SchedulerImpact: "low"},
			expectWarnings: 0,
			expectCritical: false,
		},
		{
			name: "Warning - approaching threshold",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  88,
				QuotaExceeded:          false,
				HeadroomRemainingPct:   12,
				LimitingFactor:         "cpu",
			},
			infraImpact:    nil,
			expectWarnings: 1,
			expectCritical: false,
		},
		{
			name: "Critical - quota exceeded",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  120,
				QuotaExceeded:          true,
				HeadroomRemainingPct:   0,
				LimitingFactor:         "memory",
			},
			infraImpact:    nil,
			expectWarnings: 2, // quota exceeded + low headroom
			expectCritical: true,
		},
		{
			name: "Multiple warnings - infra impact",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  96,
				QuotaExceeded:          false,
				HeadroomRemainingPct:   4,
				LimitingFactor:         "cpu",
			},
			infraImpact: &InfrastructureImpact{
				EtcdImpact:      "high",
				APIServerImpact: "high",
				SchedulerImpact: "low",
			},
			expectWarnings: 4, // critical usage + low headroom + 2 infra
			expectCritical: true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			warnings := tool.generateWarnings(tc.nsImpact, tc.infraImpact)

			if len(warnings) < tc.expectWarnings {
				t.Errorf("Expected at least %d warnings, got %d: %v", tc.expectWarnings, len(warnings), warnings)
			}

			if tc.expectCritical {
				hasCritical := false
				for _, w := range warnings {
					if contains(w, "CRITICAL") {
						hasCritical = true
						break
					}
				}
				if !hasCritical {
					t.Error("Expected at least one CRITICAL warning")
				}
			}
		})
	}
}

func TestAnalyzeScalingImpactTool_GenerateRecommendation(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	testCases := []struct {
		name           string
		nsImpact       NamespaceImpact
		infraImpact    *InfrastructureImpact
		targetReplicas int
		expectContains []string
	}{
		{
			name: "Safe scaling",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  60,
				QuotaExceeded:          false,
				HeadroomRemainingPct:   40,
			},
			infraImpact:    nil,
			targetReplicas: 5,
			expectContains: []string{"safe", "5"},
		},
		{
			name: "Quota exceeded",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  120,
				QuotaExceeded:          true,
				HeadroomRemainingPct:   0,
				LimitingFactor:         "memory",
			},
			infraImpact:    nil,
			targetReplicas: 10,
			expectContains: []string{"exceed", "quota", "memory"},
		},
		{
			name: "Critical but not exceeded",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  96,
				QuotaExceeded:          false,
				HeadroomRemainingPct:   4,
			},
			infraImpact:    nil,
			targetReplicas: 8,
			expectContains: []string{"critical", "replicas"},
		},
		{
			name: "Warning threshold",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent:  87,
				QuotaExceeded:          false,
				HeadroomRemainingPct:   13,
			},
			infraImpact:    nil,
			targetReplicas: 6,
			expectContains: []string{"possible", "monitor"},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			recommendation := tool.generateRecommendation(tc.nsImpact, tc.infraImpact, tc.targetReplicas)

			if recommendation == "" {
				t.Error("Expected non-empty recommendation")
			}

			for _, expected := range tc.expectContains {
				if !containsIgnoreCase(recommendation, expected) {
					t.Errorf("Expected recommendation to contain '%s', got: %s", expected, recommendation)
				}
			}
		})
	}
}

func TestAnalyzeScalingImpactTool_GenerateAlternativeScenarios(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	metrics := &PodResourceMetrics{
		CPUMillicores: 100,
		MemoryMB:      128,
	}
	quota := &NamespaceQuotaInfo{
		CPULimitMillicores: 4000,
		MemoryLimitBytes:   8 * 1024 * 1024 * 1024,
		CPUUsedMillicores:  1000,
		MemoryUsedBytes:    2 * 1024 * 1024 * 1024,
	}

	testCases := []struct {
		name            string
		currentReplicas int
		targetReplicas  int
		expectMin       int
		expectMax       int
	}{
		{
			name:            "Scale up with alternatives",
			currentReplicas: 2,
			targetReplicas:  5,
			expectMin:       1,
			expectMax:       3,
		},
		{
			name:            "Large scale up",
			currentReplicas: 2,
			targetReplicas:  10,
			expectMin:       2,
			expectMax:       4,
		},
		{
			name:            "Small scale up - limited alternatives",
			currentReplicas: 2,
			targetReplicas:  3,
			expectMin:       0,
			expectMax:       2,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			scenarios := tool.generateAlternativeScenarios(
				tc.currentReplicas,
				tc.targetReplicas,
				metrics,
				quota,
				1.05,
			)

			if len(scenarios) < tc.expectMin {
				t.Errorf("Expected at least %d alternative scenarios, got %d", tc.expectMin, len(scenarios))
			}
			if len(scenarios) > tc.expectMax {
				t.Errorf("Expected at most %d alternative scenarios, got %d", tc.expectMax, len(scenarios))
			}

			// Verify all scenarios have valid data
			for _, s := range scenarios {
				if s.Replicas < 1 {
					t.Errorf("Invalid replica count in scenario: %d", s.Replicas)
				}
				if s.ProjectedUsage < 0 {
					t.Errorf("Invalid projected usage: %.1f", s.ProjectedUsage)
				}
			}
		})
	}
}

func TestAnalyzeScalingImpactTool_CalculateSafeReplicas(t *testing.T) {
	tool := &AnalyzeScalingImpactTool{}

	testCases := []struct {
		name           string
		nsImpact       NamespaceImpact
		targetReplicas int
		expectMin      int
		expectMax      int
	}{
		{
			name: "High usage - reduce replicas",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent: 100,
			},
			targetReplicas: 10,
			expectMin:      7,
			expectMax:      9,
		},
		{
			name: "Very high usage - significant reduction",
			nsImpact: NamespaceImpact{
				ProjectedUsagePercent: 150,
			},
			targetReplicas: 15,
			expectMin:      7,
			expectMax:      10,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			safeReplicas := tool.calculateSafeReplicas(tc.nsImpact, tc.targetReplicas)

			if safeReplicas < tc.expectMin || safeReplicas > tc.expectMax {
				t.Errorf("Expected safe replicas between %d and %d, got %d",
					tc.expectMin, tc.expectMax, safeReplicas)
			}
		})
	}
}

func TestAnalyzeScalingImpactTool_OutputStructure(t *testing.T) {
	// Verify the output structure matches the expected schema from issue #28
	output := AnalyzeScalingImpactOutput{
		Status:     "success",
		Deployment: "sample-flask-app",
		Namespace:  "my-namespace",
		CurrentState: CurrentState{
			Replicas:        2,
			CPUPerPodAvg:    45,
			MemoryPerPodAvg: 82,
			TotalCPU:        90,
			TotalMemory:     164,
		},
		ProjectedState: ProjectedState{
			Replicas:        5,
			CPUPerPodEst:    47,
			MemoryPerPodEst: 84,
			TotalCPU:        235,
			TotalMemory:     420,
		},
		NamespaceImpact: NamespaceImpact{
			CurrentUsagePercent:   74.5,
			ProjectedUsagePercent: 92.3,
			QuotaExceeded:         false,
			HeadroomRemainingPct:  7.7,
			LimitingFactor:        "memory",
		},
		InfrastructureImpact: &InfrastructureImpact{
			EtcdImpact:        "low",
			APIServerImpact:   "medium",
			SchedulerImpact:   "low",
			EstimatedOverhead: "5% increase in control plane CPU",
		},
		Warnings: []string{
			"Memory usage will approach 95% threshold",
			"Control plane load will increase moderately",
		},
		Recommendation: "Scale to 4 replicas instead",
		AlternativeScenarios: []AlternativeScenario{
			{Replicas: 4, ProjectedUsage: 86.7, Safe: true},
			{Replicas: 3, ProjectedUsage: 80.1, Safe: true},
		},
		AnalyzedAt: "2026-01-14T10:00:00Z",
	}

	// Verify all required fields are present
	if output.Status == "" {
		t.Error("Status should not be empty")
	}
	if output.Deployment == "" {
		t.Error("Deployment should not be empty")
	}
	if output.Namespace == "" {
		t.Error("Namespace should not be empty")
	}
	if output.CurrentState.Replicas == 0 {
		t.Error("CurrentState.Replicas should not be 0")
	}
	if output.ProjectedState.Replicas == 0 {
		t.Error("ProjectedState.Replicas should not be 0")
	}
	if output.Recommendation == "" {
		t.Error("Recommendation should not be empty")
	}
	if output.AnalyzedAt == "" {
		t.Error("AnalyzedAt should not be empty")
	}
}

func TestAnalyzeScalingImpactTool_MaxFloat(t *testing.T) {
	testCases := []struct {
		a, b     float64
		expected float64
	}{
		{5.5, 3.3, 5.5},
		{3.3, 5.5, 5.5},
		{4.0, 4.0, 4.0},
		{-1.0, 0.0, 0.0},
		{100.5, 100.4, 100.5},
	}

	for _, tc := range testCases {
		result := maxFloat(tc.a, tc.b)
		if result != tc.expected {
			t.Errorf("maxFloat(%.1f, %.1f) = %.1f, expected %.1f", tc.a, tc.b, result, tc.expected)
		}
	}
}

// Integration test that requires real K8s client and Coordination Engine
func TestAnalyzeScalingImpactTool_Execute_Integration(t *testing.T) {
	// Skip if not running integration tests
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}

	t.Skip("Integration test - requires running cluster and coordination engine")

	// Example of how the full integration test would work:
	/*
		import (
			"context"
			"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
		)

		k8sClient, err := clients.NewK8sClient(nil)
		if err != nil {
			t.Skipf("Skipping: unable to create Kubernetes client: %v", err)
		}
		defer k8sClient.Close()

		ceClient := clients.NewCoordinationEngineClient("http://localhost:8000")

		tool := NewAnalyzeScalingImpactTool(ceClient, k8sClient)
		ctx := context.Background()

		result, err := tool.Execute(ctx, map[string]interface{}{
			"deployment":      "sample-flask-app",
			"namespace":       "default",
			"target_replicas": float64(5),
		})
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		output, ok := result.(AnalyzeScalingImpactOutput)
		if !ok {
			t.Fatal("Expected AnalyzeScalingImpactOutput type")
		}

		if output.Status != "success" {
			t.Errorf("Expected status 'success', got '%s'", output.Status)
		}
	*/
}

// Benchmark tests
func BenchmarkCalculateNamespaceImpact(b *testing.B) {
	tool := &AnalyzeScalingImpactTool{}
	current := CurrentState{Replicas: 2, CPUPerPodAvg: 100, MemoryPerPodAvg: 128, TotalCPU: 200, TotalMemory: 256}
	projected := ProjectedState{Replicas: 5, CPUPerPodEst: 105, MemoryPerPodEst: 134, TotalCPU: 525, TotalMemory: 670}
	quota := &NamespaceQuotaInfo{CPULimitMillicores: 4000, MemoryLimitBytes: 8 * 1024 * 1024 * 1024, CPUUsedMillicores: 1000, MemoryUsedBytes: 2 * 1024 * 1024 * 1024}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = tool.calculateNamespaceImpact(current, projected, quota, 2)
	}
}

func BenchmarkGenerateWarnings(b *testing.B) {
	tool := &AnalyzeScalingImpactTool{}
	nsImpact := NamespaceImpact{ProjectedUsagePercent: 92, QuotaExceeded: false, HeadroomRemainingPct: 8, LimitingFactor: "cpu"}
	infraImpact := &InfrastructureImpact{EtcdImpact: "medium", APIServerImpact: "high", SchedulerImpact: "low"}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = tool.generateWarnings(nsImpact, infraImpact)
	}
}

func BenchmarkGenerateAlternativeScenarios(b *testing.B) {
	tool := &AnalyzeScalingImpactTool{}
	metrics := &PodResourceMetrics{CPUMillicores: 100, MemoryMB: 128}
	quota := &NamespaceQuotaInfo{CPULimitMillicores: 4000, MemoryLimitBytes: 8 * 1024 * 1024 * 1024, CPUUsedMillicores: 1000, MemoryUsedBytes: 2 * 1024 * 1024 * 1024}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = tool.generateAlternativeScenarios(2, 10, metrics, quota, 1.05)
	}
}

// Helper function for case-insensitive contains
func containsIgnoreCase(s, substr string) bool {
	sLower := toLower(s)
	substrLower := toLower(substr)
	return contains(sLower, substrLower)
}

func toLower(s string) string {
	result := make([]byte, len(s))
	for i := 0; i < len(s); i++ {
		c := s[i]
		if c >= 'A' && c <= 'Z' {
			c += 'a' - 'A'
		}
		result[i] = c
	}
	return string(result)
}
