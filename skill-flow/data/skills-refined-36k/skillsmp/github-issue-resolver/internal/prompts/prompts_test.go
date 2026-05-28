package prompts

import (
	"context"
	"strings"
	"testing"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

// TestDiagnoseClusterPrompt tests the diagnose-cluster-issues prompt
func TestDiagnoseClusterPrompt(t *testing.T) {
	prompt := NewDiagnoseClusterPrompt()

	t.Run("Name", func(t *testing.T) {
		if prompt.Name() != "diagnose-cluster-issues" {
			t.Errorf("Expected name 'diagnose-cluster-issues', got '%s'", prompt.Name())
		}
	})

	t.Run("Description", func(t *testing.T) {
		desc := prompt.Description()
		if desc == "" {
			t.Error("Description should not be empty")
		}
		if !strings.Contains(desc, "cluster") {
			t.Error("Description should mention 'cluster'")
		}
	})

	t.Run("GetPrompt", func(t *testing.T) {
		p := prompt.GetPrompt()
		if p == nil {
			t.Fatal("GetPrompt() returned nil")
		}
		if p.Name != "diagnose-cluster-issues" {
			t.Errorf("Expected prompt name 'diagnose-cluster-issues', got '%s'", p.Name)
		}
		if len(p.Arguments) == 0 {
			t.Error("Expected at least one argument")
		}
	})

	t.Run("Execute_WithDefaultArgs", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}
		if len(result.Messages) == 0 {
			t.Error("Expected at least one message")
		}

		// Check message content
		if len(result.Messages) > 0 {
			msg := result.Messages[0]
			if msg.Role != "user" {
				t.Errorf("Expected role 'user', got '%s'", msg.Role)
			}

			textContent, ok := msg.Content.(*mcp.TextContent)
			if !ok {
				t.Fatal("Expected TextContent")
			}

			text := textContent.Text
			if !strings.Contains(text, "cluster") {
				t.Error("Message should mention 'cluster'")
			}
			if !strings.Contains(text, "health") {
				t.Error("Message should mention 'health'")
			}
		}
	})

	t.Run("Execute_WithSeverityFilter", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{
			"severity": "critical",
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}

		// Check that severity is mentioned in the result
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			if !strings.Contains(textContent.Text, "critical") {
				t.Error("Message should mention severity 'critical'")
			}
		}
	})
}

// TestInvestigatePodsPrompt tests the investigate-pods prompt
func TestInvestigatePodsPrompt(t *testing.T) {
	prompt := NewInvestigatePodsPrompt()

	t.Run("Name", func(t *testing.T) {
		if prompt.Name() != "investigate-pods" {
			t.Errorf("Expected name 'investigate-pods', got '%s'", prompt.Name())
		}
	})

	t.Run("Description", func(t *testing.T) {
		desc := prompt.Description()
		if desc == "" {
			t.Error("Description should not be empty")
		}
		if !strings.Contains(desc, "pod") {
			t.Error("Description should mention 'pod'")
		}
	})

	t.Run("Execute_WithNamespace", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{
			"namespace": "default",
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}

		// Check that namespace is mentioned
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			if !strings.Contains(textContent.Text, "default") {
				t.Error("Message should mention namespace 'default'")
			}
		}
	})

	t.Run("Execute_WithNamespaceAndPod", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{
			"namespace": "kube-system",
			"pod_name":  "coredns-123",
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}

		// Check that both namespace and pod are mentioned
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			text := textContent.Text
			if !strings.Contains(text, "kube-system") {
				t.Error("Message should mention namespace 'kube-system'")
			}
			if !strings.Contains(text, "coredns-123") {
				t.Error("Message should mention pod 'coredns-123'")
			}
		}
	})
}

// TestCheckAnomaliesPrompt tests the check-anomalies prompt
func TestCheckAnomaliesPrompt(t *testing.T) {
	prompt := NewCheckAnomaliesPrompt()

	t.Run("Name", func(t *testing.T) {
		if prompt.Name() != "check-anomalies" {
			t.Errorf("Expected name 'check-anomalies', got '%s'", prompt.Name())
		}
	})

	t.Run("Description", func(t *testing.T) {
		desc := prompt.Description()
		if desc == "" {
			t.Error("Description should not be empty")
		}
		if !strings.Contains(desc, "anomal") {
			t.Error("Description should mention 'anomalies'")
		}
	})

	t.Run("Execute_WithDefaultArgs", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}
	})

	t.Run("Execute_WithTimeframe", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{
			"timeframe": "24h",
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		// Check that timeframe is mentioned
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			if !strings.Contains(textContent.Text, "24h") {
				t.Error("Message should mention timeframe '24h'")
			}
		}
	})
}

// TestOptimizeDataAccessPrompt tests the optimize-data-access prompt
func TestOptimizeDataAccessPrompt(t *testing.T) {
	prompt := NewOptimizeDataAccessPrompt()

	t.Run("Name", func(t *testing.T) {
		if prompt.Name() != "optimize-data-access" {
			t.Errorf("Expected name 'optimize-data-access', got '%s'", prompt.Name())
		}
	})

	t.Run("Description", func(t *testing.T) {
		desc := prompt.Description()
		if desc == "" {
			t.Error("Description should not be empty")
		}
		// Should mention Resources and Tools
		if !strings.Contains(desc, "Resource") && !strings.Contains(desc, "Tool") {
			t.Error("Description should mention Resources or Tools")
		}
	})

	t.Run("Execute", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}

		// This is an educational prompt, should mention Resources and Tools
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			text := textContent.Text
			if !strings.Contains(text, "Resource") || !strings.Contains(text, "Tool") {
				t.Error("Educational prompt should mention both Resources and Tools")
			}
			if !strings.Contains(text, "cache") {
				t.Error("Educational prompt should mention caching")
			}
		}
	})
}

// TestPredictAndPreventPrompt tests the predict-and-prevent prompt (CE)
func TestPredictAndPreventPrompt(t *testing.T) {
	prompt := NewPredictAndPreventPrompt()

	t.Run("Name", func(t *testing.T) {
		if prompt.Name() != "predict-and-prevent" {
			t.Errorf("Expected name 'predict-and-prevent', got '%s'", prompt.Name())
		}
	})

	t.Run("Description", func(t *testing.T) {
		desc := prompt.Description()
		if desc == "" {
			t.Error("Description should not be empty")
		}
		// Should mention prediction/proactive
		if !strings.Contains(desc, "predict") && !strings.Contains(desc, "proactive") {
			t.Error("Description should mention prediction or proactive")
		}
	})

	t.Run("Execute_WithDefaultArgs", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}
	})

	t.Run("Execute_WithCustomArgs", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{
			"timeframe":            "6h",
			"confidence_threshold": 0.8,
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		// Check that arguments are reflected in output
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			text := textContent.Text
			if !strings.Contains(text, "6h") {
				t.Error("Message should mention timeframe '6h'")
			}
			if !strings.Contains(text, "0.8") && !strings.Contains(text, "80") {
				t.Error("Message should mention confidence threshold")
			}
		}
	})

	t.Run("Execute_RequiresCoordinationEngine", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		// Should mention Coordination Engine requirement
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			if !strings.Contains(textContent.Text, "Coordination Engine") {
				t.Error("Should mention Coordination Engine requirement")
			}
		}
	})
}

// TestCorrelateIncidentsPrompt tests the correlate-incidents prompt (CE)
func TestCorrelateIncidentsPrompt(t *testing.T) {
	prompt := NewCorrelateIncidentsPrompt()

	t.Run("Name", func(t *testing.T) {
		if prompt.Name() != "correlate-incidents" {
			t.Errorf("Expected name 'correlate-incidents', got '%s'", prompt.Name())
		}
	})

	t.Run("Description", func(t *testing.T) {
		desc := prompt.Description()
		if desc == "" {
			t.Error("Description should not be empty")
		}
		lowerDesc := strings.ToLower(desc)
		if !strings.Contains(lowerDesc, "incident") || !strings.Contains(lowerDesc, "correlat") {
			t.Error("Description should mention incidents and correlation")
		}
	})

	t.Run("Execute_WithDefaultArgs", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Execute returned nil result")
		}
	})

	t.Run("Execute_WithTimeWindow", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{
			"time_window": "6h",
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		// Check that time_window is mentioned
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			if !strings.Contains(textContent.Text, "6h") {
				t.Error("Message should mention time_window '6h'")
			}
		}
	})

	t.Run("Execute_WithSeverityFilter", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{
			"time_window": "1h",
			"severity":    "critical",
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		// Check that both arguments are mentioned
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			text := textContent.Text
			if !strings.Contains(text, "1h") {
				t.Error("Message should mention time_window '1h'")
			}
			if !strings.Contains(text, "critical") {
				t.Error("Message should mention severity 'critical'")
			}
		}
	})

	t.Run("Execute_CorrelationWorkflow", func(t *testing.T) {
		ctx := context.Background()
		args := map[string]interface{}{}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		// Should mention correlation patterns and workflow steps
		if len(result.Messages) > 0 {
			textContent := result.Messages[0].Content.(*mcp.TextContent)
			text := textContent.Text
			if !strings.Contains(text, "root cause") {
				t.Error("Should mention root cause analysis")
			}
			if !strings.Contains(text, "cluster://incidents") {
				t.Error("Should mention cluster://incidents resource")
			}
		}
	})
}

// TestPromptInterface ensures all prompts implement the Prompt interface
func TestPromptInterface(t *testing.T) {
	prompts := []Prompt{
		NewDiagnoseClusterPrompt(),
		NewInvestigatePodsPrompt(),
		NewCheckAnomaliesPrompt(),
		NewOptimizeDataAccessPrompt(),
		NewPredictAndPreventPrompt(),
		NewCorrelateIncidentsPrompt(),
	}

	for _, p := range prompts {
		t.Run(p.Name(), func(t *testing.T) {
			// Test Name()
			if p.Name() == "" {
				t.Error("Name() should not return empty string")
			}

			// Test Description()
			if p.Description() == "" {
				t.Error("Description() should not return empty string")
			}

			// Test GetPrompt()
			prompt := p.GetPrompt()
			if prompt == nil {
				t.Fatal("GetPrompt() should not return nil")
			}
			if prompt.Name != p.Name() {
				t.Errorf("GetPrompt().Name '%s' should match Name() '%s'", prompt.Name, p.Name())
			}

			// Test Execute()
			ctx := context.Background()
			args := map[string]interface{}{}

			// investigate-pods requires namespace argument
			if p.Name() == "investigate-pods" {
				args["namespace"] = "default"
			}

			result, err := p.Execute(ctx, args)
			if err != nil {
				t.Fatalf("Execute() failed: %v", err)
			}
			if result == nil {
				t.Fatal("Execute() should not return nil result")
			}
			if len(result.Messages) == 0 {
				t.Error("Execute() should return at least one message")
			}
		})
	}
}

// TestPromptConsistency checks that prompts follow consistent patterns
func TestPromptConsistency(t *testing.T) {
	prompts := []Prompt{
		NewDiagnoseClusterPrompt(),
		NewInvestigatePodsPrompt(),
		NewCheckAnomaliesPrompt(),
		NewOptimizeDataAccessPrompt(),
		NewPredictAndPreventPrompt(),
		NewCorrelateIncidentsPrompt(),
	}

	for _, p := range prompts {
		t.Run(p.Name(), func(t *testing.T) {
			// Name should use kebab-case
			name := p.Name()
			if strings.Contains(name, "_") || strings.Contains(name, " ") {
				t.Errorf("Name '%s' should use kebab-case (hyphens)", name)
			}

			// Description should not be empty
			if p.Description() == "" {
				t.Error("Description() should not return empty string")
			}

			// Execute should always return valid messages
			ctx := context.Background()
			args := map[string]interface{}{}

			// investigate-pods requires namespace argument
			if p.Name() == "investigate-pods" {
				args["namespace"] = "default"
			}

			result, err := p.Execute(ctx, args)
			if err != nil {
				t.Fatalf("Execute failed: %v", err)
			}

			for i, msg := range result.Messages {
				if msg.Role != "user" {
					t.Errorf("Message %d: expected role 'user', got '%s'", i, msg.Role)
				}

				textContent, ok := msg.Content.(*mcp.TextContent)
				if !ok {
					t.Errorf("Message %d: expected TextContent", i)
					continue
				}

				if textContent.Text == "" {
					t.Errorf("Message %d: text should not be empty", i)
				}
			}
		})
	}
}

// TestPromptArgumentHandling tests that prompts handle arguments correctly
func TestPromptArgumentHandling(t *testing.T) {
	t.Run("DiagnoseCluster_InvalidSeverity", func(t *testing.T) {
		prompt := NewDiagnoseClusterPrompt()
		ctx := context.Background()
		args := map[string]interface{}{
			"severity": "invalid-severity",
		}

		// Should not error, but use the provided value
		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute should not error on invalid severity: %v", err)
		}
		if result == nil {
			t.Fatal("Result should not be nil")
		}
	})

	t.Run("InvestigatePods_EmptyNamespace", func(t *testing.T) {
		prompt := NewInvestigatePodsPrompt()
		ctx := context.Background()
		args := map[string]interface{}{
			"namespace": "",
		}

		// Should error since namespace is required
		_, err := prompt.Execute(ctx, args)
		if err == nil {
			t.Fatal("Execute should error on empty namespace (namespace is required)")
		}
		if !strings.Contains(err.Error(), "namespace") {
			t.Errorf("Error message should mention namespace, got: %v", err)
		}
	})

	t.Run("PredictAndPrevent_NumericConfidence", func(t *testing.T) {
		prompt := NewPredictAndPreventPrompt()
		ctx := context.Background()
		args := map[string]interface{}{
			"confidence_threshold": 0.75,
		}

		result, err := prompt.Execute(ctx, args)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}
		if result == nil {
			t.Fatal("Result should not be nil")
		}
	})
}

// BenchmarkPromptExecution benchmarks prompt execution performance
func BenchmarkPromptExecution(b *testing.B) {
	prompts := []Prompt{
		NewDiagnoseClusterPrompt(),
		NewInvestigatePodsPrompt(),
		NewCheckAnomaliesPrompt(),
		NewOptimizeDataAccessPrompt(),
		NewPredictAndPreventPrompt(),
		NewCorrelateIncidentsPrompt(),
	}

	for _, p := range prompts {
		b.Run(p.Name(), func(b *testing.B) {
			ctx := context.Background()
			args := map[string]interface{}{}

			b.ResetTimer()
			for i := 0; i < b.N; i++ {
				_, _ = p.Execute(ctx, args)
			}
		})
	}
}
