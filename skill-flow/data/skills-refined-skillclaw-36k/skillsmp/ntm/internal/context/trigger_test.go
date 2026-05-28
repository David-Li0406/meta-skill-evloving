package context

import (
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

func TestNewCompactionTrigger(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	if trigger == nil {
		t.Fatal("NewCompactionTrigger returned nil")
	}

	if trigger.config.PollInterval != 30*time.Second {
		t.Errorf("Expected PollInterval 30s, got %v", trigger.config.PollInterval)
	}

	if !trigger.config.AutoCompact {
		t.Error("Expected AutoCompact to be true")
	}
}

func TestDefaultCompactionTriggerConfig(t *testing.T) {
	config := DefaultCompactionTriggerConfig()

	if config.PollInterval != 30*time.Second {
		t.Errorf("Expected PollInterval 30s, got %v", config.PollInterval)
	}

	if !config.AutoCompact {
		t.Error("Expected AutoCompact to be true by default")
	}

	if config.CompactionCooldown != 5*time.Minute {
		t.Errorf("Expected CompactionCooldown 5m, got %v", config.CompactionCooldown)
	}

	if config.WaitAfterCommand != 15*time.Second {
		t.Errorf("Expected WaitAfterCommand 15s, got %v", config.WaitAfterCommand)
	}

	if !config.EnableRecoveryInjection {
		t.Error("Expected EnableRecoveryInjection to be true by default")
	}
}

func TestCanCompact_NoPriorCompaction(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	// Should be able to compact with no prior history
	if !trigger.canCompact("agent1") {
		t.Error("Expected canCompact to return true for new agent")
	}
}

func TestCanCompact_WithCooldown(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	config.CompactionCooldown = 100 * time.Millisecond // Short for testing

	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	// Simulate a recent compaction
	trigger.mu.Lock()
	trigger.lastCompaction["agent1"] = time.Now()
	trigger.mu.Unlock()

	// Should not be able to compact immediately
	if trigger.canCompact("agent1") {
		t.Error("Expected canCompact to return false during cooldown")
	}

	// Wait for cooldown
	time.Sleep(150 * time.Millisecond)

	// Should be able to compact after cooldown
	if !trigger.canCompact("agent1") {
		t.Error("Expected canCompact to return true after cooldown")
	}
}

func TestCompactionStatus(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	// Initially empty
	status := trigger.GetCompactionStatus()
	if len(status) != 0 {
		t.Errorf("Expected empty status, got %d entries", len(status))
	}

	// Add a compaction record
	now := time.Now()
	trigger.mu.Lock()
	trigger.lastCompaction["agent1"] = now
	trigger.activeCompactions["agent2"] = true
	trigger.lastCompaction["agent2"] = now.Add(-10 * time.Minute)
	trigger.mu.Unlock()

	status = trigger.GetCompactionStatus()

	if len(status) != 2 {
		t.Errorf("Expected 2 status entries, got %d", len(status))
	}

	if status["agent1"].IsCompacting {
		t.Error("Expected agent1 to not be compacting")
	}

	if !status["agent2"].IsCompacting {
		t.Error("Expected agent2 to be compacting")
	}
}

func TestSetHandlers(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	triggered := false
	completed := false

	trigger.SetCompactionTriggeredHandler(func(event CompactionTriggerEvent) {
		triggered = true
	})

	trigger.SetCompactionCompleteHandler(func(event CompactionTriggerEvent) {
		completed = true
	})

	trigger.mu.RLock()
	if trigger.onCompactionTriggered == nil {
		t.Error("Expected triggered handler to be set")
	}
	if trigger.onCompactionComplete == nil {
		t.Error("Expected complete handler to be set")
	}
	trigger.mu.RUnlock()

	// Handlers set but not called yet
	if triggered {
		t.Error("Triggered handler should not have been called")
	}
	if completed {
		t.Error("Completed handler should not have been called")
	}
}

func TestGenerateRecoveryPrompt(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	tests := []struct {
		agentType tmux.AgentType
		wantEmpty bool
	}{
		{tmux.AgentClaude, false},
		{tmux.AgentCodex, false},
		{tmux.AgentGemini, false},
		{tmux.AgentUser, false},
	}

	for _, tt := range tests {
		prompt := trigger.generateRecoveryPrompt(tt.agentType)
		if tt.wantEmpty && prompt != "" {
			t.Errorf("Expected empty prompt for %s, got %q", tt.agentType, prompt)
		}
		if !tt.wantEmpty && prompt == "" {
			t.Errorf("Expected non-empty prompt for %s", tt.agentType)
		}
	}
}

func TestTriggerCompactionNow_AgentNotFound(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	_, err := trigger.TriggerCompactionNow("nonexistent")
	if err == nil {
		t.Error("Expected error for nonexistent agent")
	}
}

func TestStartStop(t *testing.T) {
	config := DefaultCompactionTriggerConfig()
	config.PollInterval = 50 * time.Millisecond // Fast for testing

	monitor := NewContextMonitor(DefaultMonitorConfig())
	compactor := NewCompactor(monitor, DefaultCompactorConfig())
	predictor := NewContextPredictor(DefaultPredictorConfig())

	trigger := NewCompactionTrigger(config, monitor, compactor, predictor)

	// Start monitoring
	trigger.Start()

	// Let it run a bit
	time.Sleep(100 * time.Millisecond)

	// Stop monitoring
	trigger.Stop()

	// Should complete without hanging
}

func TestCompactionTriggerEvent(t *testing.T) {
	event := CompactionTriggerEvent{
		AgentID:     "agent1",
		PaneID:      "%123",
		AgentType:   tmux.AgentClaude,
		TriggeredAt: time.Now(),
		Prediction: &Prediction{
			CurrentUsage:        0.8,
			ShouldCompact:       true,
			MinutesToExhaustion: 5.0,
		},
	}

	if event.AgentID != "agent1" {
		t.Errorf("Expected AgentID 'agent1', got %q", event.AgentID)
	}

	if event.AgentType != tmux.AgentClaude {
		t.Errorf("Expected AgentType Claude, got %v", event.AgentType)
	}

	if event.Prediction == nil {
		t.Error("Expected Prediction to be set")
	}

	if !event.Prediction.ShouldCompact {
		t.Error("Expected ShouldCompact to be true")
	}
}
