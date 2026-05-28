package context

import (
	"sync"
	"testing"
	"time"
)

func TestNewContextPredictor(t *testing.T) {
	t.Parallel()

	t.Run("default config", func(t *testing.T) {
		t.Parallel()
		p := NewContextPredictor(DefaultPredictorConfig())
		if p == nil {
			t.Fatal("NewContextPredictor returned nil")
		}
		if len(p.samples) != 64 {
			t.Errorf("expected 64 samples, got %d", len(p.samples))
		}
	})

	t.Run("custom config", func(t *testing.T) {
		t.Parallel()
		cfg := PredictorConfig{
			MaxSamples: 128,
			Window:     10 * time.Minute,
			MinSamples: 5,
		}
		p := NewContextPredictor(cfg)
		if len(p.samples) != 128 {
			t.Errorf("expected 128 samples, got %d", len(p.samples))
		}
	})

	t.Run("zero values get defaults", func(t *testing.T) {
		t.Parallel()
		cfg := PredictorConfig{}
		p := NewContextPredictor(cfg)
		if len(p.samples) != 64 {
			t.Errorf("expected default 64 samples, got %d", len(p.samples))
		}
		if p.config.MinSamples != 3 {
			t.Errorf("expected default MinSamples 3, got %d", p.config.MinSamples)
		}
	})
}

func TestAddSample(t *testing.T) {
	t.Parallel()

	t.Run("basic add", func(t *testing.T) {
		t.Parallel()
		p := NewContextPredictor(DefaultPredictorConfig())

		p.AddSample(1000)
		if p.SampleCount() != 1 {
			t.Errorf("expected 1 sample, got %d", p.SampleCount())
		}

		p.AddSample(2000)
		if p.SampleCount() != 2 {
			t.Errorf("expected 2 samples, got %d", p.SampleCount())
		}
	})

	t.Run("ring buffer wraps", func(t *testing.T) {
		t.Parallel()
		cfg := PredictorConfig{MaxSamples: 4}
		p := NewContextPredictor(cfg)

		for i := 0; i < 10; i++ {
			p.AddSample(int64(i * 100))
		}

		if p.SampleCount() != 4 {
			t.Errorf("expected 4 samples after wrap, got %d", p.SampleCount())
		}
	})

	t.Run("AddSampleAt with timestamp", func(t *testing.T) {
		t.Parallel()
		p := NewContextPredictor(DefaultPredictorConfig())

		past := time.Now().Add(-5 * time.Minute)
		p.AddSampleAt(5000, past)

		latest := p.LatestSample()
		if latest == nil {
			t.Fatal("LatestSample returned nil")
		}
		if latest.Tokens != 5000 {
			t.Errorf("expected 5000 tokens, got %d", latest.Tokens)
		}
		if !latest.Timestamp.Equal(past) {
			t.Errorf("timestamp mismatch: expected %v, got %v", past, latest.Timestamp)
		}
	})
}

func TestPredictExhaustion(t *testing.T) {
	t.Parallel()

	t.Run("insufficient samples returns nil", func(t *testing.T) {
		t.Parallel()
		p := NewContextPredictor(DefaultPredictorConfig())

		p.AddSample(1000)
		p.AddSample(2000)

		pred := p.PredictExhaustion(200000)
		if pred != nil {
			t.Errorf("expected nil with insufficient samples, got %+v", pred)
		}
	})

	t.Run("steady growth prediction", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 3
		p := NewContextPredictor(cfg)

		// Simulate steady growth: 10k tokens per minute
		baseTime := time.Now()
		p.AddSampleAt(100000, baseTime.Add(-4*time.Minute)) // 100k at -4min
		p.AddSampleAt(120000, baseTime.Add(-3*time.Minute)) // 120k at -3min
		p.AddSampleAt(140000, baseTime.Add(-2*time.Minute)) // 140k at -2min
		p.AddSampleAt(160000, baseTime.Add(-1*time.Minute)) // 160k at -1min
		p.AddSampleAt(180000, baseTime)                     // 180k now

		pred := p.PredictExhaustion(200000)
		if pred == nil {
			t.Fatal("expected prediction, got nil")
		}

		t.Logf("PREDICTOR_TEST: SteadyGrowth | Usage=%.2f | Velocity=%.1f | MinutesToExhaustion=%.1f",
			pred.CurrentUsage, pred.TokenVelocity, pred.MinutesToExhaustion)

		// Should have ~90% usage (180k/200k)
		if pred.CurrentUsage < 0.89 || pred.CurrentUsage > 0.91 {
			t.Errorf("expected ~90%% usage, got %.2f", pred.CurrentUsage)
		}

		// Velocity should be ~20k tokens/min (80k over 4 min)
		if pred.TokenVelocity < 15000 || pred.TokenVelocity > 25000 {
			t.Errorf("expected ~20k tokens/min velocity, got %.1f", pred.TokenVelocity)
		}

		// Should exhaust in ~1 minute (20k remaining / 20k per min)
		if pred.MinutesToExhaustion < 0.5 || pred.MinutesToExhaustion > 2.0 {
			t.Errorf("expected ~1 min to exhaustion, got %.2f", pred.MinutesToExhaustion)
		}
	})

	t.Run("stable usage no exhaustion", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 3
		p := NewContextPredictor(cfg)

		baseTime := time.Now()
		// Stable at 50k tokens
		p.AddSampleAt(50000, baseTime.Add(-3*time.Minute))
		p.AddSampleAt(50000, baseTime.Add(-2*time.Minute))
		p.AddSampleAt(50000, baseTime.Add(-1*time.Minute))
		p.AddSampleAt(50000, baseTime)

		pred := p.PredictExhaustion(200000)
		if pred == nil {
			t.Fatal("expected prediction, got nil")
		}

		t.Logf("PREDICTOR_TEST: StableUsage | Velocity=%.1f | MinutesToExhaustion=%.1f",
			pred.TokenVelocity, pred.MinutesToExhaustion)

		// Velocity should be ~0
		if pred.TokenVelocity < -1000 || pred.TokenVelocity > 1000 {
			t.Errorf("expected ~0 velocity for stable usage, got %.1f", pred.TokenVelocity)
		}

		// No exhaustion expected
		if pred.MinutesToExhaustion != 0 {
			t.Errorf("expected 0 minutes to exhaustion, got %.1f", pred.MinutesToExhaustion)
		}
	})

	t.Run("decreasing usage", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 3
		p := NewContextPredictor(cfg)

		baseTime := time.Now()
		// Context being compacted - decreasing tokens
		p.AddSampleAt(150000, baseTime.Add(-3*time.Minute))
		p.AddSampleAt(130000, baseTime.Add(-2*time.Minute))
		p.AddSampleAt(110000, baseTime.Add(-1*time.Minute))
		p.AddSampleAt(90000, baseTime)

		pred := p.PredictExhaustion(200000)
		if pred == nil {
			t.Fatal("expected prediction, got nil")
		}

		t.Logf("PREDICTOR_TEST: DecreasingUsage | Velocity=%.1f | MinutesToExhaustion=%.1f",
			pred.TokenVelocity, pred.MinutesToExhaustion)

		// Velocity should be negative
		if pred.TokenVelocity >= 0 {
			t.Errorf("expected negative velocity, got %.1f", pred.TokenVelocity)
		}

		// No exhaustion when decreasing
		if pred.MinutesToExhaustion != 0 {
			t.Errorf("expected 0 minutes to exhaustion for decreasing, got %.1f", pred.MinutesToExhaustion)
		}
	})
}

func TestShouldWarnThresholds(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name          string
		currentTokens int64
		modelLimit    int64
		tokensPerMin  int64
		expectWarn    bool
		expectCompact bool
	}{
		{
			name:          "low usage slow growth - no warn",
			currentTokens: 100000,
			modelLimit:    200000,
			tokensPerMin:  1000,
			expectWarn:    false,
			expectCompact: false,
		},
		{
			name:          "high usage fast growth - warn and compact",
			currentTokens: 180000,
			modelLimit:    200000,
			tokensPerMin:  5000,
			expectWarn:    true,
			expectCompact: true,
		},
		{
			name:          "high usage slow growth - warn only",
			currentTokens: 160000,
			modelLimit:    200000,
			tokensPerMin:  3000, // Increased to get minutes < 15 (40000/3000 = 13.3 min)
			expectWarn:    true,
			expectCompact: false,
		},
		{
			name:          "moderate usage very fast growth - warn and compact",
			currentTokens: 152000, // Increased to get usage > 0.75 (152000/200000 = 0.76)
			modelLimit:    200000,
			tokensPerMin:  10000,
			expectWarn:    true,
			expectCompact: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			cfg := DefaultPredictorConfig()
			cfg.MinSamples = 3
			p := NewContextPredictor(cfg)

			baseTime := time.Now()
			// Build samples to achieve target velocity
			startTokens := tt.currentTokens - (tt.tokensPerMin * 3) // 3 minutes of history
			for i := 0; i < 4; i++ {
				tokens := startTokens + (tt.tokensPerMin * int64(i))
				p.AddSampleAt(tokens, baseTime.Add(-time.Duration(3-i)*time.Minute))
			}

			pred := p.PredictExhaustion(tt.modelLimit)
			if pred == nil {
				t.Fatal("expected prediction, got nil")
			}

			t.Logf("PREDICTOR_TEST: Thresholds | Test=%s | Usage=%.2f | Velocity=%.1f | MinutesLeft=%.1f | ShouldWarn=%v | ShouldCompact=%v",
				tt.name, pred.CurrentUsage, pred.TokenVelocity, pred.MinutesToExhaustion, pred.ShouldWarn, pred.ShouldCompact)

			if pred.ShouldWarn != tt.expectWarn {
				t.Errorf("ShouldWarn: expected %v, got %v (usage=%.2f, minutes=%.1f)",
					tt.expectWarn, pred.ShouldWarn, pred.CurrentUsage, pred.MinutesToExhaustion)
			}

			if pred.ShouldCompact != tt.expectCompact {
				t.Errorf("ShouldCompact: expected %v, got %v (usage=%.2f, minutes=%.1f)",
					tt.expectCompact, pred.ShouldCompact, pred.CurrentUsage, pred.MinutesToExhaustion)
			}
		})
	}
}

func TestVelocityTrend(t *testing.T) {
	t.Parallel()

	t.Run("accelerating", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 3
		p := NewContextPredictor(cfg)

		baseTime := time.Now()
		// First half: slow growth (5k/min)
		p.AddSampleAt(100000, baseTime.Add(-4*time.Minute))
		p.AddSampleAt(105000, baseTime.Add(-3*time.Minute))
		// Second half: fast growth (15k/min)
		p.AddSampleAt(120000, baseTime.Add(-2*time.Minute))
		p.AddSampleAt(135000, baseTime.Add(-1*time.Minute))
		p.AddSampleAt(150000, baseTime)

		velocity, accelerating := p.VelocityTrend()

		t.Logf("PREDICTOR_TEST: VelocityTrend | Velocity=%.1f | Accelerating=%v", velocity, accelerating)

		if !accelerating {
			t.Error("expected accelerating=true for increasing velocity")
		}
		if velocity <= 0 {
			t.Errorf("expected positive velocity, got %.1f", velocity)
		}
	})

	t.Run("decelerating", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 3
		p := NewContextPredictor(cfg)

		baseTime := time.Now()
		// First half: fast growth (20k/min)
		p.AddSampleAt(100000, baseTime.Add(-4*time.Minute))
		p.AddSampleAt(120000, baseTime.Add(-3*time.Minute))
		// Second half: slow growth (5k/min)
		p.AddSampleAt(125000, baseTime.Add(-2*time.Minute))
		p.AddSampleAt(130000, baseTime.Add(-1*time.Minute))
		p.AddSampleAt(135000, baseTime)

		velocity, accelerating := p.VelocityTrend()

		t.Logf("PREDICTOR_TEST: VelocityTrend | Velocity=%.1f | Accelerating=%v", velocity, accelerating)

		if accelerating {
			t.Error("expected accelerating=false for decreasing velocity")
		}
	})

	t.Run("insufficient samples", func(t *testing.T) {
		t.Parallel()
		p := NewContextPredictor(DefaultPredictorConfig())

		p.AddSample(1000)
		p.AddSample(2000)

		velocity, _ := p.VelocityTrend()
		if velocity != 0 {
			t.Errorf("expected 0 velocity with insufficient samples, got %.1f", velocity)
		}
	})
}

func TestReset(t *testing.T) {
	t.Parallel()

	p := NewContextPredictor(DefaultPredictorConfig())

	for i := 0; i < 10; i++ {
		p.AddSample(int64(i * 1000))
	}

	if p.SampleCount() != 10 {
		t.Errorf("expected 10 samples before reset, got %d", p.SampleCount())
	}

	p.Reset()

	if p.SampleCount() != 0 {
		t.Errorf("expected 0 samples after reset, got %d", p.SampleCount())
	}

	latest := p.LatestSample()
	if latest != nil {
		t.Error("expected nil LatestSample after reset")
	}
}

func TestLatestSample(t *testing.T) {
	t.Parallel()

	t.Run("empty predictor", func(t *testing.T) {
		t.Parallel()
		p := NewContextPredictor(DefaultPredictorConfig())

		latest := p.LatestSample()
		if latest != nil {
			t.Error("expected nil for empty predictor")
		}
	})

	t.Run("returns most recent", func(t *testing.T) {
		t.Parallel()
		p := NewContextPredictor(DefaultPredictorConfig())

		p.AddSample(1000)
		p.AddSample(2000)
		p.AddSample(3000)

		latest := p.LatestSample()
		if latest == nil {
			t.Fatal("expected sample, got nil")
		}
		if latest.Tokens != 3000 {
			t.Errorf("expected 3000, got %d", latest.Tokens)
		}
	})

	t.Run("after ring buffer wrap", func(t *testing.T) {
		t.Parallel()
		cfg := PredictorConfig{MaxSamples: 4}
		p := NewContextPredictor(cfg)

		for i := 1; i <= 10; i++ {
			p.AddSample(int64(i * 1000))
		}

		latest := p.LatestSample()
		if latest == nil {
			t.Fatal("expected sample, got nil")
		}
		if latest.Tokens != 10000 {
			t.Errorf("expected 10000, got %d", latest.Tokens)
		}
	})
}

func TestConcurrentAccess(t *testing.T) {
	t.Parallel()

	p := NewContextPredictor(DefaultPredictorConfig())

	var wg sync.WaitGroup
	writers := 10
	readsPerWriter := 100

	for i := 0; i < writers; i++ {
		wg.Add(1)
		go func(writerID int) {
			defer wg.Done()
			for j := 0; j < readsPerWriter; j++ {
				tokens := int64((writerID*readsPerWriter + j) * 100)
				p.AddSample(tokens)
				_ = p.SampleCount()
				_ = p.LatestSample()
				_ = p.PredictExhaustion(200000)
			}
		}(i)
	}

	wg.Wait()

	// Verify predictor is still in valid state
	count := p.SampleCount()
	if count <= 0 || count > 64 {
		t.Errorf("unexpected sample count after concurrent access: %d", count)
	}

	t.Logf("PREDICTOR_TEST: ConcurrentAccess | FinalSampleCount=%d", count)
}

func TestMultiModelPrediction(t *testing.T) {
	t.Parallel()

	models := []struct {
		name  string
		limit int64
	}{
		{"claude-opus-4", 200000},
		{"gpt-4", 128000},
		{"gemini-2.0-flash", 1000000},
	}

	cfg := DefaultPredictorConfig()
	cfg.MinSamples = 3

	for _, model := range models {
		t.Run(model.name, func(t *testing.T) {
			t.Parallel()
			p := NewContextPredictor(cfg)

			baseTime := time.Now()
			// 75% usage with 10k tokens/min growth
			currentTokens := int64(float64(model.limit) * 0.75)
			for i := 0; i < 4; i++ {
				tokens := currentTokens - int64((3-i)*10000)
				p.AddSampleAt(tokens, baseTime.Add(-time.Duration(3-i)*time.Minute))
			}

			pred := p.PredictExhaustion(model.limit)
			if pred == nil {
				t.Fatal("expected prediction, got nil")
			}

			t.Logf("PREDICTOR_TEST: MultiModel | Model=%s | Limit=%d | Usage=%.2f | Velocity=%.1f | MinutesLeft=%.1f",
				model.name, model.limit, pred.CurrentUsage, pred.TokenVelocity, pred.MinutesToExhaustion)

			// All should have ~75% usage
			if pred.CurrentUsage < 0.74 || pred.CurrentUsage > 0.76 {
				t.Errorf("expected ~75%% usage, got %.2f", pred.CurrentUsage)
			}

			// Velocity should be ~10k/min
			if pred.TokenVelocity < 9000 || pred.TokenVelocity > 11000 {
				t.Errorf("expected ~10k/min velocity, got %.1f", pred.TokenVelocity)
			}

			// Minutes to exhaustion varies by model limit
			// Remaining = 25% of limit, divided by 10k/min
			expectedMinutes := float64(model.limit) * 0.25 / 10000
			tolerance := expectedMinutes * 0.2 // 20% tolerance
			if pred.MinutesToExhaustion < expectedMinutes-tolerance || pred.MinutesToExhaustion > expectedMinutes+tolerance {
				t.Errorf("expected ~%.1f min to exhaustion, got %.1f", expectedMinutes, pred.MinutesToExhaustion)
			}
		})
	}
}

func TestSamplesOutsideWindow(t *testing.T) {
	t.Parallel()

	cfg := PredictorConfig{
		Window:     2 * time.Minute, // Short window
		MinSamples: 3,
		MaxSamples: 64,
	}
	p := NewContextPredictor(cfg)

	baseTime := time.Now()

	// Add old samples (outside window)
	p.AddSampleAt(10000, baseTime.Add(-10*time.Minute))
	p.AddSampleAt(20000, baseTime.Add(-8*time.Minute))
	p.AddSampleAt(30000, baseTime.Add(-6*time.Minute))

	// Prediction should fail - samples are outside window
	pred := p.PredictExhaustion(200000)
	if pred != nil {
		t.Errorf("expected nil prediction for samples outside window, got %+v", pred)
	}

	// Add recent samples
	p.AddSampleAt(100000, baseTime.Add(-90*time.Second))
	p.AddSampleAt(110000, baseTime.Add(-60*time.Second))
	p.AddSampleAt(120000, baseTime.Add(-30*time.Second))
	p.AddSampleAt(130000, baseTime)

	// Now should predict
	pred = p.PredictExhaustion(200000)
	if pred == nil {
		t.Fatal("expected prediction with recent samples")
	}

	t.Logf("PREDICTOR_TEST: WindowedSamples | SampleCount=%d | Velocity=%.1f",
		pred.SampleCount, pred.TokenVelocity)

	// Should only use recent samples (4 within window)
	if pred.SampleCount != 4 {
		t.Errorf("expected 4 samples in window, got %d", pred.SampleCount)
	}
}

func TestPredictorEdgeCases(t *testing.T) {
	t.Parallel()

	t.Run("zero model limit", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 2
		p := NewContextPredictor(cfg)

		p.AddSample(1000)
		p.AddSample(2000)
		p.AddSample(3000)

		// Should not panic with zero limit
		pred := p.PredictExhaustion(0)
		if pred == nil {
			t.Log("nil prediction with zero limit (expected)")
		} else {
			t.Logf("prediction with zero limit: usage=%.2f", pred.CurrentUsage)
		}
	})

	t.Run("tokens exceed limit", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 3
		p := NewContextPredictor(cfg)

		baseTime := time.Now()
		// Tokens already exceed limit
		p.AddSampleAt(250000, baseTime.Add(-2*time.Minute))
		p.AddSampleAt(260000, baseTime.Add(-1*time.Minute))
		p.AddSampleAt(270000, baseTime)

		pred := p.PredictExhaustion(200000)
		if pred == nil {
			t.Fatal("expected prediction")
		}

		t.Logf("PREDICTOR_TEST: ExceedsLimit | Usage=%.2f | MinutesLeft=%.1f",
			pred.CurrentUsage, pred.MinutesToExhaustion)

		// Usage should be > 100%
		if pred.CurrentUsage < 1.0 {
			t.Errorf("expected usage > 100%%, got %.2f", pred.CurrentUsage)
		}

		// No time to exhaustion when already exceeded
		if pred.MinutesToExhaustion != 0 {
			t.Errorf("expected 0 minutes when already exceeded, got %.1f", pred.MinutesToExhaustion)
		}
	})

	t.Run("very small token counts", func(t *testing.T) {
		t.Parallel()
		cfg := DefaultPredictorConfig()
		cfg.MinSamples = 3
		p := NewContextPredictor(cfg)

		baseTime := time.Now()
		p.AddSampleAt(10, baseTime.Add(-2*time.Minute))
		p.AddSampleAt(20, baseTime.Add(-1*time.Minute))
		p.AddSampleAt(30, baseTime)

		pred := p.PredictExhaustion(200000)
		if pred == nil {
			t.Fatal("expected prediction")
		}

		t.Logf("PREDICTOR_TEST: SmallTokens | Usage=%.6f | Velocity=%.1f | MinutesLeft=%.1f",
			pred.CurrentUsage, pred.TokenVelocity, pred.MinutesToExhaustion)

		// Very low usage
		if pred.CurrentUsage > 0.001 {
			t.Errorf("expected very low usage, got %.6f", pred.CurrentUsage)
		}
	})
}
