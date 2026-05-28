package config

import (
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/cli/tiers"
)

func TestDefaultProficiencyConfig(t *testing.T) {
	cfg := DefaultProficiencyConfig()

	if cfg.Tier != int(tiers.TierApprentice) {
		t.Errorf("expected tier %d, got %d", tiers.TierApprentice, cfg.Tier)
	}
	if len(cfg.PromotionHistory) != 0 {
		t.Errorf("expected empty promotion history, got %d entries", len(cfg.PromotionHistory))
	}
	if cfg.UsageStats.CommandsRun != 0 {
		t.Errorf("expected 0 commands run, got %d", cfg.UsageStats.CommandsRun)
	}
}

func TestProficiencyLoadSaveCycle(t *testing.T) {
	// Create temp directory for test
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	// Load (should create defaults)
	cfg, err := LoadProficiency()
	if err != nil {
		t.Fatalf("LoadProficiency failed: %v", err)
	}

	if cfg.GetTier() != tiers.TierApprentice {
		t.Errorf("expected Apprentice tier, got %s", cfg.GetTier())
	}

	// Modify and save
	if err := cfg.SetTier(tiers.TierJourneyman, "manual"); err != nil {
		t.Fatalf("SetTier failed: %v", err)
	}

	// Reload and verify
	cfg2, err := LoadProficiency()
	if err != nil {
		t.Fatalf("Second LoadProficiency failed: %v", err)
	}

	if cfg2.GetTier() != tiers.TierJourneyman {
		t.Errorf("expected Journeyman tier after reload, got %s", cfg2.GetTier())
	}

	if len(cfg2.PromotionHistory) != 1 {
		t.Errorf("expected 1 promotion record, got %d", len(cfg2.PromotionHistory))
	}
}

func TestProficiencyEnvOverride(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	// Set env override
	os.Setenv("NTM_PROFICIENCY_TIER", "3")
	defer os.Unsetenv("NTM_PROFICIENCY_TIER")

	// Config file says Apprentice (1), but env says Master (3)
	if cfg.GetTier() != tiers.TierMaster {
		t.Errorf("expected Master tier from env override, got %s", cfg.GetTier())
	}
}

func TestProficiencyEnvOverrideInvalid(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	// Invalid env value should be ignored
	os.Setenv("NTM_PROFICIENCY_TIER", "invalid")
	defer os.Unsetenv("NTM_PROFICIENCY_TIER")

	if cfg.GetTier() != tiers.TierApprentice {
		t.Errorf("expected Apprentice tier (invalid env ignored), got %s", cfg.GetTier())
	}
}

func TestProficiencyUsageStats(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	// Record some usage
	if err := cfg.RecordUsage(10, 2, 5); err != nil {
		t.Fatalf("RecordUsage failed: %v", err)
	}

	stats := cfg.GetUsageStats()
	if stats.CommandsRun != 10 {
		t.Errorf("expected 10 commands, got %d", stats.CommandsRun)
	}
	if stats.SessionsCreated != 2 {
		t.Errorf("expected 2 sessions, got %d", stats.SessionsCreated)
	}
	if stats.PromptsSent != 5 {
		t.Errorf("expected 5 prompts, got %d", stats.PromptsSent)
	}

	// Reload and verify persistence
	cfg2, _ := LoadProficiency()
	stats2 := cfg2.GetUsageStats()
	if stats2.CommandsRun != 10 {
		t.Errorf("expected 10 commands after reload, got %d", stats2.CommandsRun)
	}
}

func TestProficiencyCorruptedConfig(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	// Create corrupted config file
	path := filepath.Join(tmpDir, "ntm", "proficiency.json")
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte("{invalid json"), 0644); err != nil {
		t.Fatal(err)
	}

	// Load should recover gracefully
	cfg, err := LoadProficiency()
	if err != nil {
		t.Fatalf("LoadProficiency should recover from corrupted config: %v", err)
	}

	if cfg.GetTier() != tiers.TierApprentice {
		t.Errorf("expected default Apprentice tier after recovery, got %s", cfg.GetTier())
	}
}

func TestProficiencyReset(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	// Upgrade tier and record usage
	cfg.SetTier(tiers.TierMaster, "manual")
	cfg.RecordUsage(100, 20, 50)

	// Reset
	if err := cfg.Reset(); err != nil {
		t.Fatalf("Reset failed: %v", err)
	}

	if cfg.GetTier() != tiers.TierApprentice {
		t.Errorf("expected Apprentice tier after reset, got %s", cfg.GetTier())
	}

	stats := cfg.GetUsageStats()
	if stats.CommandsRun != 0 {
		t.Errorf("expected 0 commands after reset, got %d", stats.CommandsRun)
	}

	// Should have reset record in history
	history := cfg.GetPromotionHistory()
	found := false
	for _, h := range history {
		if h.Reason == "reset" {
			found = true
			break
		}
	}
	if !found {
		t.Error("expected reset record in promotion history")
	}
}

func TestProficiencyDaysSinceFirstUse(t *testing.T) {
	cfg := DefaultProficiencyConfig()

	// Just created, should be 0 days
	if days := cfg.DaysSinceFirstUse(); days != 0 {
		t.Errorf("expected 0 days since first use, got %d", days)
	}

	// Backdate first use
	cfg.UsageStats.FirstUse = time.Now().Add(-72 * time.Hour) // 3 days ago
	if days := cfg.DaysSinceFirstUse(); days != 3 {
		t.Errorf("expected 3 days since first use, got %d", days)
	}
}

func TestProficiencyRecordCommand(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	// Record some commands
	if err := cfg.RecordCommand("spawn"); err != nil {
		t.Fatalf("RecordCommand failed: %v", err)
	}
	if err := cfg.RecordCommand("send"); err != nil {
		t.Fatalf("RecordCommand failed: %v", err)
	}
	if err := cfg.RecordCommand("spawn"); err != nil {
		t.Fatalf("RecordCommand failed: %v", err)
	}

	stats := cfg.GetUsageStats()
	if stats.CommandsRun != 3 {
		t.Errorf("expected 3 commands, got %d", stats.CommandsRun)
	}

	if cfg.GetUniqueCommandCount() != 2 {
		t.Errorf("expected 2 unique commands, got %d", cfg.GetUniqueCommandCount())
	}

	if stats.UniqueCommands["spawn"] != 2 {
		t.Errorf("expected spawn count 2, got %d", stats.UniqueCommands["spawn"])
	}
}

func TestProficiencyAdvancedAttempts(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	if err := cfg.RecordAdvancedAttempt("dashboard"); err != nil {
		t.Fatalf("RecordAdvancedAttempt failed: %v", err)
	}
	if err := cfg.RecordAdvancedAttempt("robot-status"); err != nil {
		t.Fatalf("RecordAdvancedAttempt failed: %v", err)
	}

	stats := cfg.GetUsageStats()
	if stats.AdvancedAttempts != 2 {
		t.Errorf("expected 2 advanced attempts, got %d", stats.AdvancedAttempts)
	}
}

func TestProficiencyPromotionCriteria(t *testing.T) {
	cfg := DefaultProficiencyConfig()

	// Initially no promotion
	suggest, _, _ := cfg.ShouldSuggestPromotion()
	if suggest {
		t.Error("should not suggest promotion for new user")
	}

	// After 100 commands, should suggest Journeyman
	cfg.UsageStats.CommandsRun = 100
	suggest, tier, _ := cfg.ShouldSuggestPromotion()
	if !suggest {
		t.Error("should suggest promotion after 100 commands")
	}
	if tier != tiers.TierJourneyman {
		t.Errorf("expected Journeyman tier, got %s", tier)
	}

	// After upgrading, need more for next tier
	cfg.Tier = int(tiers.TierJourneyman)
	suggest, _, _ = cfg.ShouldSuggestPromotion()
	if suggest {
		t.Error("should not suggest promotion right after upgrade")
	}

	// After 500 commands at Journeyman, should suggest Master
	cfg.UsageStats.CommandsRun = 500
	suggest, tier, _ = cfg.ShouldSuggestPromotion()
	if !suggest {
		t.Error("should suggest promotion after 500 commands")
	}
	if tier != tiers.TierMaster {
		t.Errorf("expected Master tier, got %s", tier)
	}
}

func TestProficiencyCheckPromotion(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	// Set up for promotion
	cfg.UsageStats.CommandsRun = 100
	cfg.Save()

	// First check should suggest
	suggest, msg := cfg.CheckPromotion("session1")
	if !suggest {
		t.Error("should suggest promotion")
	}
	if msg == "" {
		t.Error("expected promotion message")
	}

	// Same session should not suggest again
	suggest, _ = cfg.CheckPromotion("session1")
	if suggest {
		t.Error("should not suggest in same session")
	}

	// Different session within same hour should not suggest
	suggest, _ = cfg.CheckPromotion("session2")
	if suggest {
		t.Error("should not suggest within same hour")
	}
}

func TestProficiencyDaysActive(t *testing.T) {
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	cfg, _ := LoadProficiency()

	// Initial days active should be 1
	stats := cfg.GetUsageStats()
	if stats.DaysActive != 1 {
		t.Errorf("expected 1 day active, got %d", stats.DaysActive)
	}

	// Recording command on same day shouldn't increment
	cfg.RecordCommand("spawn")
	stats = cfg.GetUsageStats()
	if stats.DaysActive != 1 {
		t.Errorf("expected still 1 day active, got %d", stats.DaysActive)
	}

	// Simulate previous day
	cfg.UsageStats.LastActiveDate = "2024-01-01"
	cfg.RecordCommand("send")
	stats = cfg.GetUsageStats()
	if stats.DaysActive != 2 {
		t.Errorf("expected 2 days active after new day, got %d", stats.DaysActive)
	}
}
