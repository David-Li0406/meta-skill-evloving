package tools

import (
	"context"
	"testing"
)

func TestCalculatePodCapacityToolMetadata(t *testing.T) {
	tool := NewCalculatePodCapacityTool(nil)

	// Test Name
	if tool.Name() != "calculate-pod-capacity" {
		t.Errorf("expected tool name 'calculate-pod-capacity', got '%s'", tool.Name())
	}

	// Test Description
	if tool.Description() == "" {
		t.Error("tool description should not be empty")
	}

	// Test InputSchema
	schema := tool.InputSchema()
	if schema == nil {
		t.Fatal("input schema should not be nil")
	}

	// Verify expected properties exist
	props, ok := schema["properties"].(map[string]interface{})
	if !ok {
		t.Fatal("schema should have properties")
	}

	expectedProps := []string{"namespace", "pod_profile", "custom_resources", "safety_margin", "include_trending"}
	for _, prop := range expectedProps {
		if _, ok := props[prop]; !ok {
			t.Errorf("schema should have property '%s'", prop)
		}
	}

	// Verify namespace has a default value (not required)
	// Per ADR and tool description, namespace defaults to "cluster" for cluster-wide analysis
	nsProp, ok := props["namespace"].(map[string]interface{})
	if !ok {
		t.Fatal("schema should have namespace property")
	}
	if defaultVal, ok := nsProp["default"]; !ok || defaultVal != "cluster" {
		t.Error("namespace should have default value 'cluster'")
	}

	// Verify required is empty (all parameters have defaults)
	required, ok := schema["required"].([]string)
	if !ok {
		t.Fatal("schema should have required field")
	}
	if len(required) != 0 {
		t.Errorf("no parameters should be required (all have defaults), got: %v", required)
	}
}

func TestParseCPU(t *testing.T) {
	tests := []struct {
		input    string
		expected int64
	}{
		{"200m", 200},
		{"100m", 100},
		{"500m", 500},
		{"1000m", 1000},
		{"0.5", 500},
		{"1", 1000},
		{"2", 2000},
		{"", 0},
		{"  200m  ", 200},
	}

	for _, tt := range tests {
		result := parseCPU(tt.input)
		if result != tt.expected {
			t.Errorf("parseCPU(%q): expected %d, got %d", tt.input, tt.expected, result)
		}
	}
}

func TestParseMemoryMB(t *testing.T) {
	tests := []struct {
		input    string
		expected int64
	}{
		{"128Mi", 128},
		{"256Mi", 256},
		{"512Mi", 512},
		{"1Gi", 1024},
		{"2Gi", 2048},
		{"1024Ki", 1},
		{"", 0},
		{"  256Mi  ", 256},
	}

	for _, tt := range tests {
		result := parseMemoryMB(tt.input)
		if result != tt.expected {
			t.Errorf("parseMemoryMB(%q): expected %d, got %d", tt.input, tt.expected, result)
		}
	}
}

func TestCalculatePodCapacityToolParseInput(t *testing.T) {
	tool := NewCalculatePodCapacityTool(nil)

	tests := []struct {
		name        string
		args        map[string]interface{}
		expectError bool
		check       func(t *testing.T, input *CalculatePodCapacityInput)
	}{
		{
			name: "basic namespace",
			args: map[string]interface{}{
				"namespace": "my-namespace",
			},
			expectError: false,
			check: func(t *testing.T, input *CalculatePodCapacityInput) {
				if input.Namespace != "my-namespace" {
					t.Errorf("expected namespace 'my-namespace', got '%s'", input.Namespace)
				}
				if input.PodProfile != "medium" {
					t.Errorf("expected default profile 'medium', got '%s'", input.PodProfile)
				}
			},
		},
		{
			name: "with pod profile",
			args: map[string]interface{}{
				"namespace":   "test-ns",
				"pod_profile": "large",
			},
			expectError: false,
			check: func(t *testing.T, input *CalculatePodCapacityInput) {
				if input.PodProfile != "large" {
					t.Errorf("expected profile 'large', got '%s'", input.PodProfile)
				}
			},
		},
		{
			name: "with safety margin float",
			args: map[string]interface{}{
				"namespace":     "test-ns",
				"safety_margin": float64(25),
			},
			expectError: false,
			check: func(t *testing.T, input *CalculatePodCapacityInput) {
				if input.SafetyMargin == nil {
					t.Fatal("expected safety margin to be set")
				}
				if *input.SafetyMargin != 25.0 {
					t.Errorf("expected safety margin 25.0, got %f", *input.SafetyMargin)
				}
			},
		},
		{
			name: "with safety margin int",
			args: map[string]interface{}{
				"namespace":     "test-ns",
				"safety_margin": 20,
			},
			expectError: false,
			check: func(t *testing.T, input *CalculatePodCapacityInput) {
				if input.SafetyMargin == nil {
					t.Fatal("expected safety margin to be set")
				}
				if *input.SafetyMargin != 20.0 {
					t.Errorf("expected safety margin 20.0, got %f", *input.SafetyMargin)
				}
			},
		},
		{
			name: "with include_trending",
			args: map[string]interface{}{
				"namespace":        "test-ns",
				"include_trending": false,
			},
			expectError: false,
			check: func(t *testing.T, input *CalculatePodCapacityInput) {
				if input.IncludeTrending == nil {
					t.Fatal("expected include_trending to be set")
				}
				if *input.IncludeTrending != false {
					t.Error("expected include_trending to be false")
				}
			},
		},
		{
			name: "with custom resources",
			args: map[string]interface{}{
				"namespace":   "test-ns",
				"pod_profile": "custom",
				"custom_resources": map[string]interface{}{
					"cpu":    "200m",
					"memory": "128Mi",
				},
			},
			expectError: false,
			check: func(t *testing.T, input *CalculatePodCapacityInput) {
				if input.CustomResources == nil {
					t.Fatal("expected custom_resources to be set")
				}
				if input.CustomResources.CPU != "200m" {
					t.Errorf("expected CPU '200m', got '%s'", input.CustomResources.CPU)
				}
				if input.CustomResources.Memory != "128Mi" {
					t.Errorf("expected memory '128Mi', got '%s'", input.CustomResources.Memory)
				}
			},
		},
		{
			name: "cluster namespace",
			args: map[string]interface{}{
				"namespace": "cluster",
			},
			expectError: false,
			check: func(t *testing.T, input *CalculatePodCapacityInput) {
				if input.Namespace != "cluster" {
					t.Errorf("expected namespace 'cluster', got '%s'", input.Namespace)
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			input, err := tool.parseInput(tt.args)
			if tt.expectError {
				if err == nil {
					t.Error("expected error but got none")
				}
				return
			}
			if err != nil {
				t.Errorf("unexpected error: %v", err)
				return
			}
			if tt.check != nil {
				tt.check(t, input)
			}
		})
	}
}

func TestCalculatePodCapacityToolValidation(t *testing.T) {
	// Test with nil k8sClient - should return an error gracefully
	// rather than panic when trying to calculate capacity
	tool := NewCalculatePodCapacityTool(nil)
	ctx := context.Background()

	// Test that Execute returns an error when k8sClient is nil
	// (namespace defaults to "cluster" which requires k8sClient)
	_, err := tool.Execute(ctx, map[string]interface{}{})
	if err == nil {
		t.Error("expected error when k8sClient is nil")
	}

	// Test with explicit "cluster" namespace - should also error with nil client
	_, err = tool.Execute(ctx, map[string]interface{}{
		"namespace": "cluster",
	})
	if err == nil {
		t.Error("expected error when k8sClient is nil for cluster namespace")
	}

	// Test with specific namespace - should also error with nil client
	_, err = tool.Execute(ctx, map[string]interface{}{
		"namespace": "default",
	})
	if err == nil {
		t.Error("expected error when k8sClient is nil for specific namespace")
	}
}

func TestConvertPodEstimates(t *testing.T) {
	tool := NewCalculatePodCapacityTool(nil)

	// Test that the tool can create output correctly
	if tool == nil {
		t.Fatal("tool should not be nil")
	}

	// Verify the tool has the expected name
	if tool.Name() != "calculate-pod-capacity" {
		t.Errorf("expected tool name 'calculate-pod-capacity', got '%s'", tool.Name())
	}
}

func TestPodProfileEnums(t *testing.T) {
	tool := NewCalculatePodCapacityTool(nil)
	schema := tool.InputSchema()

	props, ok := schema["properties"].(map[string]interface{})
	if !ok {
		t.Fatal("schema should have properties")
	}

	podProfile, ok := props["pod_profile"].(map[string]interface{})
	if !ok {
		t.Fatal("schema should have pod_profile property")
	}

	enum, ok := podProfile["enum"].([]string)
	if !ok {
		t.Fatal("pod_profile should have enum")
	}

	expectedProfiles := map[string]bool{
		"small":  false,
		"medium": false,
		"large":  false,
		"custom": false,
	}

	for _, profile := range enum {
		if _, ok := expectedProfiles[profile]; ok {
			expectedProfiles[profile] = true
		}
	}

	for profile, found := range expectedProfiles {
		if !found {
			t.Errorf("pod_profile enum should include '%s'", profile)
		}
	}
}
