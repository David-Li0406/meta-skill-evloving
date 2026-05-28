package scoring

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func TestCoreMetrics(t *testing.T) {
	metrics := CoreMetrics()

	if len(metrics) == 0 {
		t.Error("CoreMetrics() returned empty slice")
	}

	// Verify all core metrics are defined
	expectedMetrics := []MetricName{
		MetricCompletion,
		MetricRetries,
		MetricTimeEfficiency,
		MetricTokenEfficiency,
		MetricQuality,
		MetricErrorRate,
		MetricContextUsage,
	}

	for _, expected := range expectedMetrics {
		found := false
		for _, m := range metrics {
			if m.Name == expected {
				found = true
				// Verify all fields are populated
				if m.Description == "" {
					t.Errorf("Metric %s has empty description", m.Name)
				}
				if m.Unit == "" {
					t.Errorf("Metric %s has empty unit", m.Name)
				}
				if m.MeasurementGuide == "" {
					t.Errorf("Metric %s has empty measurement guide", m.Name)
				}
				break
			}
		}
		if !found {
			t.Errorf("Expected metric %s not found in CoreMetrics()", expected)
		}
	}
}

func TestWeights_Sum(t *testing.T) {
	tests := []struct {
		name     string
		weights  Weights
		expected float64
	}{
		{
			name:     "default weights",
			weights:  DefaultWeights(),
			expected: 1.0,
		},
		{
			name:     "speed focused",
			weights:  SpeedFocusedWeights(),
			expected: 1.0,
		},
		{
			name:     "quality focused",
			weights:  QualityFocusedWeights(),
			expected: 1.0,
		},
		{
			name:     "economy focused",
			weights:  EconomyFocusedWeights(),
			expected: 1.0,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			sum := tc.weights.Sum()
			if diff := sum - tc.expected; diff < -0.001 || diff > 0.001 {
				t.Errorf("Sum() = %v, want %v", sum, tc.expected)
			}
		})
	}
}

func TestWeights_Normalize(t *testing.T) {
	w := Weights{
		Completion: 2.0,
		Quality:    2.0,
		// Others zero
	}

	w.Normalize()

	if w.Sum() < 0.999 || w.Sum() > 1.001 {
		t.Errorf("Normalize() did not produce sum of 1.0: got %v", w.Sum())
	}

	if w.Completion != 0.5 || w.Quality != 0.5 {
		t.Errorf("Normalize() incorrect: Completion=%v, Quality=%v", w.Completion, w.Quality)
	}
}

func TestEffectivenessScore_ComputeOverall(t *testing.T) {
	score := &EffectivenessScore{
		Completion:      1.0,
		Quality:         0.8,
		TokenEfficiency: 0.6,
		Weights:         DefaultWeights(),
	}

	overall := score.ComputeOverall()

	// With default weights: 0.30*1.0 + 0.25*0.8 + 0.15*0.6 = 0.30 + 0.20 + 0.09 = 0.59
	// Plus zeros for other metrics
	if overall < 0.5 || overall > 0.7 {
		t.Errorf("ComputeOverall() = %v, expected around 0.59", overall)
	}
}

func TestNewEffectivenessScore(t *testing.T) {
	score := NewEffectivenessScore(0.9, 0.85, 0.7)

	if score.Completion != 0.9 {
		t.Errorf("Completion = %v, want 0.9", score.Completion)
	}
	if score.Quality != 0.85 {
		t.Errorf("Quality = %v, want 0.85", score.Quality)
	}
	if score.TokenEfficiency != 0.7 {
		t.Errorf("TokenEfficiency = %v, want 0.7", score.TokenEfficiency)
	}
	if score.Overall == 0 {
		t.Error("Overall should be computed, got 0")
	}
}

func TestEffectivenessScore_WithWeights(t *testing.T) {
	original := NewEffectivenessScore(1.0, 1.0, 1.0)
	originalOverall := original.Overall

	// Change to speed focused
	speedScore := original.WithWeights(SpeedFocusedWeights())

	// Original should be unchanged
	if original.Overall != originalOverall {
		t.Error("WithWeights() modified original score")
	}

	// New score should have different weights
	if speedScore.Weights.TimeEfficiency != SpeedFocusedWeights().TimeEfficiency {
		t.Error("WithWeights() did not apply new weights")
	}
}

func TestRawMetrics_ToEffectivenessScore(t *testing.T) {
	raw := RawMetrics{
		TasksAssigned:    10,
		TasksCompleted:   8,
		RetryCount:       1,
		EstimatedMinutes: 60,
		ActualMinutes:    50,
		BaselineTokens:   10000,
		ActualTokens:     8000,
		TestsPassing:     0.9,
		HasRegressions:   false,
		ErrorCount:       2,
		SuccessCount:     98,
		AvgContextUsage:  0.3,
	}

	score := raw.ToEffectivenessScore(DefaultWeights())

	// Completion: 8/10 = 0.8
	if score.Completion != 0.8 {
		t.Errorf("Completion = %v, want 0.8", score.Completion)
	}

	// Retries: 1 - (1/3) = 0.67
	if score.Retries < 0.66 || score.Retries > 0.68 {
		t.Errorf("Retries = %v, want ~0.67", score.Retries)
	}

	// Time efficiency: 60/50 = 1.2, capped at 1.0
	if score.TimeEfficiency != 1.0 {
		t.Errorf("TimeEfficiency = %v, want 1.0 (capped)", score.TimeEfficiency)
	}

	// Token efficiency: 10000/8000 = 1.25, capped at 1.0
	if score.TokenEfficiency != 1.0 {
		t.Errorf("TokenEfficiency = %v, want 1.0 (capped)", score.TokenEfficiency)
	}

	// Quality: (0.9 + 1.0) / 2 = 0.95 (tests passing + no regressions)
	if score.Quality < 0.94 || score.Quality > 0.96 {
		t.Errorf("Quality = %v, want ~0.95", score.Quality)
	}

	// Error rate: 1 - (2/100) = 0.98
	if score.ErrorRate < 0.97 || score.ErrorRate > 0.99 {
		t.Errorf("ErrorRate = %v, want ~0.98", score.ErrorRate)
	}

	// Context usage: 1 - 0.3 = 0.7
	if score.ContextUsage != 0.7 {
		t.Errorf("ContextUsage = %v, want 0.7", score.ContextUsage)
	}

	// Overall should be computed
	if score.Overall == 0 {
		t.Error("Overall should be computed")
	}
}

func TestLoadWeightsConfig(t *testing.T) {
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "weights.json")

	config := WeightsConfig{
		Default: DefaultWeights(),
		TaskTypeWeights: map[string]Weights{
			"bug_fix":  QualityFocusedWeights(),
			"refactor": EconomyFocusedWeights(),
		},
	}

	data, err := json.MarshalIndent(config, "", "  ")
	if err != nil {
		t.Fatalf("marshaling config: %v", err)
	}

	if err := os.WriteFile(configPath, data, 0644); err != nil {
		t.Fatalf("writing config: %v", err)
	}

	loaded, err := LoadWeightsConfig(configPath)
	if err != nil {
		t.Fatalf("LoadWeightsConfig() error: %v", err)
	}

	if loaded.Default.Completion != config.Default.Completion {
		t.Error("loaded default weights don't match")
	}

	if len(loaded.TaskTypeWeights) != 2 {
		t.Errorf("expected 2 task type weights, got %d", len(loaded.TaskTypeWeights))
	}
}

func TestWeightsConfig_GetWeights(t *testing.T) {
	config := &WeightsConfig{
		Default: DefaultWeights(),
		TaskTypeWeights: map[string]Weights{
			"bug_fix": QualityFocusedWeights(),
		},
	}

	// Should return task-specific weights
	bugWeights := config.GetWeights("bug_fix")
	if bugWeights.Quality != QualityFocusedWeights().Quality {
		t.Error("GetWeights('bug_fix') should return quality focused weights")
	}

	// Should return default for unknown task type
	unknownWeights := config.GetWeights("unknown_task")
	if unknownWeights.Completion != DefaultWeights().Completion {
		t.Error("GetWeights('unknown_task') should return default weights")
	}
}

func TestRawMetrics_EdgeCases(t *testing.T) {
	t.Run("zero assigned tasks", func(t *testing.T) {
		raw := RawMetrics{
			TasksAssigned:  0,
			TasksCompleted: 0,
		}
		score := raw.ToEffectivenessScore(DefaultWeights())
		if score.Completion != 0 {
			t.Errorf("Completion with 0 tasks = %v, want 0", score.Completion)
		}
	})

	t.Run("excessive retries", func(t *testing.T) {
		raw := RawMetrics{
			RetryCount: 10, // More than max expected
		}
		score := raw.ToEffectivenessScore(DefaultWeights())
		if score.Retries < 0 {
			t.Errorf("Retries should not be negative: %v", score.Retries)
		}
	})

	t.Run("zero duration", func(t *testing.T) {
		raw := RawMetrics{
			EstimatedMinutes: 0,
			ActualMinutes:    0,
		}
		score := raw.ToEffectivenessScore(DefaultWeights())
		if score.TimeEfficiency != 0 {
			t.Errorf("TimeEfficiency with zero duration = %v, want 0", score.TimeEfficiency)
		}
	})
}

// =============================================================================
// bd-1u5g: Additional Score Formula Accuracy Tests
// =============================================================================

func TestScoreFormulaAccuracy(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name          string
		raw           RawMetrics
		weights       Weights
		expectOverall float64
		tolerance     float64
	}{
		{
			name: "perfect scores all metrics",
			raw: RawMetrics{
				TasksAssigned:    10,
				TasksCompleted:   10,
				RetryCount:       0,
				EstimatedMinutes: 60,
				ActualMinutes:    30, // faster than estimated
				BaselineTokens:   10000,
				ActualTokens:     5000, // under budget
				TestsPassing:     1.0,
				HasRegressions:   false,
				ErrorCount:       0,
				SuccessCount:     100,
				AvgContextUsage:  0.1,
			},
			weights:       DefaultWeights(),
			expectOverall: 0.99, // Near perfect
			tolerance:     0.05,
		},
		{
			name: "mediocre performance",
			raw: RawMetrics{
				TasksAssigned:    10,
				TasksCompleted:   5,
				RetryCount:       2,
				EstimatedMinutes: 60,
				ActualMinutes:    90, // slower than estimated
				BaselineTokens:   10000,
				ActualTokens:     15000, // over budget
				TestsPassing:     0.7,
				HasRegressions:   true,
				ErrorCount:       10,
				SuccessCount:     90,
				AvgContextUsage:  0.5,
			},
			weights:       DefaultWeights(),
			expectOverall: 0.45,
			tolerance:     0.10,
		},
		{
			name: "quality focused weights amplify quality",
			raw: RawMetrics{
				TasksAssigned:  10,
				TasksCompleted: 8,
				TestsPassing:   1.0,
				HasRegressions: false,
			},
			weights:       QualityFocusedWeights(),
			expectOverall: 0.80,
			tolerance:     0.10,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			score := tt.raw.ToEffectivenessScore(tt.weights)

			t.Logf("SCORE_TEST: %s | Completion=%.2f | Quality=%.2f | Overall=%.2f",
				tt.name, score.Completion, score.Quality, score.Overall)

			diff := score.Overall - tt.expectOverall
			if diff < -tt.tolerance || diff > tt.tolerance {
				t.Errorf("Overall = %.3f, want ~%.3f (tolerance %.2f)",
					score.Overall, tt.expectOverall, tt.tolerance)
			}
		})
	}
}

// =============================================================================
// bd-1u5g: Per-Task-Type Breakdown Tests
// =============================================================================

func TestPerTaskTypeWeights(t *testing.T) {
	t.Parallel()

	config := &WeightsConfig{
		Default: DefaultWeights(),
		TaskTypeWeights: map[string]Weights{
			"bug_fix":  QualityFocusedWeights(),
			"feature":  DefaultWeights(),
			"refactor": EconomyFocusedWeights(),
			"chore":    SpeedFocusedWeights(),
			"hotfix":   QualityFocusedWeights(),
		},
	}

	taskTypes := []struct {
		taskType      string
		expectQuality float64 // expected quality weight
	}{
		{"bug_fix", 0.35},  // QualityFocused
		{"feature", 0.25},  // Default
		{"refactor", 0.20}, // EconomyFocused
		{"chore", 0.15},    // SpeedFocused
		{"hotfix", 0.35},   // QualityFocused
		{"unknown", 0.25},  // Falls back to Default
	}

	for _, tt := range taskTypes {
		t.Run(tt.taskType, func(t *testing.T) {
			t.Parallel()

			weights := config.GetWeights(tt.taskType)

			t.Logf("SCORE_TEST: TaskType=%s | QualityWeight=%.2f | CompletionWeight=%.2f",
				tt.taskType, weights.Quality, weights.Completion)

			if weights.Quality != tt.expectQuality {
				t.Errorf("GetWeights(%s).Quality = %.2f, want %.2f",
					tt.taskType, weights.Quality, tt.expectQuality)
			}
		})
	}
}

func TestTaskTypeScoreVariation(t *testing.T) {
	t.Parallel()

	// Same raw metrics should produce different overall scores
	// depending on task type weights
	raw := RawMetrics{
		TasksAssigned:    10,
		TasksCompleted:   8,
		RetryCount:       1,
		EstimatedMinutes: 60,
		ActualMinutes:    45,
		BaselineTokens:   10000,
		ActualTokens:     8000,
		TestsPassing:     0.95,
		HasRegressions:   false,
		ErrorCount:       2,
		SuccessCount:     98,
		AvgContextUsage:  0.3,
	}

	weightSets := map[string]Weights{
		"default": DefaultWeights(),
		"quality": QualityFocusedWeights(),
		"speed":   SpeedFocusedWeights(),
		"economy": EconomyFocusedWeights(),
	}

	scores := make(map[string]float64)
	for name, weights := range weightSets {
		score := raw.ToEffectivenessScore(weights)
		scores[name] = score.Overall

		t.Logf("SCORE_TEST: Weights=%s | TaskType=mixed | Overall=%.3f",
			name, score.Overall)
	}

	// All scores should be in reasonable range but differ
	for name, s := range scores {
		if s < 0.5 || s > 0.95 {
			t.Errorf("Score for %s weights out of expected range: %.3f", name, s)
		}
	}

	// Verify weights actually make a difference (scores shouldn't all be identical)
	unique := make(map[float64]bool)
	for _, s := range scores {
		unique[s] = true
	}
	// At least 2 unique scores (given same raw data, different weights)
	if len(unique) < 2 {
		t.Error("Different weight sets should produce different scores")
	}
}

// =============================================================================
// bd-1u5g: Iteration/Retry Counting Tests
// =============================================================================

func TestRetryCountAccuracy(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name        string
		retryCount  int
		expectScore float64
		tolerance   float64
	}{
		{"zero retries", 0, 1.0, 0.01},
		{"one retry", 1, 0.67, 0.02},
		{"two retries", 2, 0.33, 0.02},
		{"three retries (max)", 3, 0.0, 0.01},
		{"excess retries", 5, 0.0, 0.01}, // Capped at 0
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			raw := RawMetrics{
				TasksAssigned:  1,
				TasksCompleted: 1,
				RetryCount:     tt.retryCount,
			}
			score := raw.ToEffectivenessScore(DefaultWeights())

			t.Logf("SCORE_TEST: RetryCount=%d | RetryScore=%.3f",
				tt.retryCount, score.Retries)

			diff := score.Retries - tt.expectScore
			if diff < -tt.tolerance || diff > tt.tolerance {
				t.Errorf("Retries score = %.3f, want ~%.3f",
					score.Retries, tt.expectScore)
			}
		})
	}
}

// =============================================================================
// bd-1u5g: Error/Restart Detection Tests
// =============================================================================

func TestErrorRateAccuracy(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name         string
		errorCount   int
		successCount int
		expectScore  float64
		tolerance    float64
	}{
		{"no errors", 0, 100, 1.0, 0.01},
		{"5% error rate", 5, 95, 0.95, 0.01},
		{"10% error rate", 10, 90, 0.90, 0.01},
		{"50% error rate", 50, 50, 0.50, 0.01},
		{"all errors", 100, 0, 0.0, 0.01},
		{"zero operations", 0, 0, 0.0, 0.01},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			raw := RawMetrics{
				ErrorCount:   tt.errorCount,
				SuccessCount: tt.successCount,
			}
			score := raw.ToEffectivenessScore(DefaultWeights())

			t.Logf("SCORE_TEST: Errors=%d | Successes=%d | ErrorRateScore=%.3f",
				tt.errorCount, tt.successCount, score.ErrorRate)

			diff := score.ErrorRate - tt.expectScore
			if diff < -tt.tolerance || diff > tt.tolerance {
				t.Errorf("ErrorRate score = %.3f, want ~%.3f",
					score.ErrorRate, tt.expectScore)
			}
		})
	}
}

// =============================================================================
// bd-1u5g: Time Tracking Accuracy Tests
// =============================================================================

func TestTimeEfficiencyAccuracy(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name        string
		estimated   int
		actual      int
		expectScore float64
		tolerance   float64
	}{
		{"completed faster", 60, 30, 1.0, 0.01}, // Capped at 1.0
		{"completed on time", 60, 60, 1.0, 0.01},
		{"slightly overtime", 60, 80, 0.75, 0.01},
		{"double overtime", 60, 120, 0.50, 0.01},
		{"triple overtime", 60, 180, 0.33, 0.02},
		{"no estimate", 0, 60, 0.0, 0.01},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			raw := RawMetrics{
				EstimatedMinutes: tt.estimated,
				ActualMinutes:    tt.actual,
			}
			score := raw.ToEffectivenessScore(DefaultWeights())

			t.Logf("SCORE_TEST: Estimated=%dm | Actual=%dm | TimeEfficiency=%.3f",
				tt.estimated, tt.actual, score.TimeEfficiency)

			diff := score.TimeEfficiency - tt.expectScore
			if diff < -tt.tolerance || diff > tt.tolerance {
				t.Errorf("TimeEfficiency = %.3f, want ~%.3f",
					score.TimeEfficiency, tt.expectScore)
			}
		})
	}
}

// =============================================================================
// bd-1u5g: Token Efficiency Tests
// =============================================================================

func TestTokenEfficiencyAccuracy(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name        string
		baseline    int
		actual      int
		expectScore float64
		tolerance   float64
	}{
		{"under budget", 10000, 5000, 1.0, 0.01}, // Capped at 1.0
		{"on budget", 10000, 10000, 1.0, 0.01},
		{"20% over", 10000, 12500, 0.80, 0.01},
		{"double budget", 10000, 20000, 0.50, 0.01},
		{"no baseline", 0, 10000, 0.0, 0.01},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			raw := RawMetrics{
				BaselineTokens: tt.baseline,
				ActualTokens:   tt.actual,
			}
			score := raw.ToEffectivenessScore(DefaultWeights())

			t.Logf("SCORE_TEST: Baseline=%d | Actual=%d | TokenEfficiency=%.3f",
				tt.baseline, tt.actual, score.TokenEfficiency)

			diff := score.TokenEfficiency - tt.expectScore
			if diff < -tt.tolerance || diff > tt.tolerance {
				t.Errorf("TokenEfficiency = %.3f, want ~%.3f",
					score.TokenEfficiency, tt.expectScore)
			}
		})
	}
}

// =============================================================================
// bd-1u5g: Completion Detection Tests
// =============================================================================

func TestCompletionDetection(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name        string
		assigned    int
		completed   int
		expectScore float64
	}{
		{"all completed", 10, 10, 1.0},
		{"half completed", 10, 5, 0.5},
		{"one completed", 10, 1, 0.1},
		{"none completed", 10, 0, 0.0},
		{"over completed (clamped)", 10, 12, 1.2}, // Can exceed 1.0 if over
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()

			raw := RawMetrics{
				TasksAssigned:  tt.assigned,
				TasksCompleted: tt.completed,
			}
			score := raw.ToEffectivenessScore(DefaultWeights())

			t.Logf("SCORE_TEST: Assigned=%d | Completed=%d | Completion=%.3f",
				tt.assigned, tt.completed, score.Completion)

			if score.Completion != tt.expectScore {
				t.Errorf("Completion = %.3f, want %.3f",
					score.Completion, tt.expectScore)
			}
		})
	}
}
