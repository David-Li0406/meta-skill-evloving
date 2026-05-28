package e2e

import (
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"

	"github.com/Dicklesworthstone/ntm/tests/testutil"
)

// stripANSI removes ANSI escape codes from output
func stripANSI(str string) string {
	ansi := regexp.MustCompile(`\x1b\[[0-9;]*m`)
	return ansi.ReplaceAllString(str, "")
}

// setupTierTestEnv sets up an isolated environment for tier tests
func setupTierTestEnv(t *testing.T) (cleanup func()) {
	t.Helper()
	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	// Ensure no env override interferes
	os.Unsetenv("NTM_PROFICIENCY_TIER")
	return func() {
		os.Unsetenv("XDG_CONFIG_HOME")
		os.Unsetenv("NTM_PROFICIENCY_TIER")
	}
}

// TestE2E_NewUserHelpShowsMinimalCommands tests that new users see only essential commands
func TestE2E_NewUserHelpShowsMinimalCommands(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing new user help output")

	// Run ntm --minimal (the flag is on root command, not help)
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "--minimal")
	output := string(out)

	// Essential commands should be visible
	essentialCommands := []string{"spawn", "send", "status", "kill", "help"}
	for _, cmd := range essentialCommands {
		if !strings.Contains(output, cmd) {
			t.Errorf("Expected essential command %q in help output", cmd)
		}
	}

	logger.Log("PASS: Essential commands visible in minimal help")
}

// TestE2E_ManualTierPromotion tests promoting tier manually
func TestE2E_ManualTierPromotion(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing manual tier promotion")

	// Show initial level (should be Apprentice)
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Apprentice") {
		t.Errorf("Expected initial tier to be Apprentice, got: %s", string(out))
	}

	// Promote to Journeyman
	logger.Log("Promoting to Journeyman")
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "journeyman")

	// Verify tier changed
	out = testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Journeyman") {
		t.Errorf("Expected tier to be Journeyman after promotion, got: %s", string(out))
	}

	logger.Log("PASS: Manual tier promotion works")
}

// TestE2E_TierDemotion tests demoting tier manually
func TestE2E_TierDemotion(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing tier demotion")

	// Start at Journeyman
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "journeyman")

	// Demote to Apprentice
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "down")

	// Verify tier changed
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Apprentice") {
		t.Errorf("Expected tier to be Apprentice after demotion, got: %s", string(out))
	}

	logger.Log("PASS: Tier demotion works")
}

// TestE2E_TierMasterUnlocksAll tests that Master tier shows all commands
func TestE2E_TierMasterUnlocksAll(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing Master tier unlocks all commands")

	// Set to Master tier
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "master")

	// Run default help (full/stunning help)
	out := testutil.AssertCommandSuccess(t, logger, "ntm")
	output := stripANSI(string(out)) // Strip ANSI codes for reliable string matching

	// All command categories should be visible
	expectedSections := []string{"SESSION CREATION", "AGENT MANAGEMENT", "SESSION NAVIGATION"}
	for _, section := range expectedSections {
		if !strings.Contains(output, section) {
			t.Errorf("Expected section %q in full help output", section)
		}
	}

	logger.Log("PASS: Master tier shows all commands")
}

// TestE2E_EnvTierOverride tests that NTM_PROFICIENCY_TIER overrides config
func TestE2E_EnvTierOverride(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing environment tier override")

	// Set config to Apprentice (default)
	// Then set env to Master
	os.Setenv("NTM_PROFICIENCY_TIER", "3")

	// Check level - should show Master despite config
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Master") {
		t.Errorf("Expected tier to be Master from env override, got: %s", string(out))
	}

	// Clear env and check again - should revert
	os.Unsetenv("NTM_PROFICIENCY_TIER")
	out = testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Apprentice") {
		t.Errorf("Expected tier to revert to Apprentice when env cleared, got: %s", string(out))
	}

	logger.Log("PASS: Environment tier override works")
}

// TestE2E_TierPersistence tests that tier setting persists across invocations
func TestE2E_TierPersistence(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing tier persistence")

	// Set tier to Journeyman
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "journeyman")

	// Run level again (simulating new session)
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Journeyman") {
		t.Errorf("Expected tier to persist as Journeyman, got: %s", string(out))
	}

	logger.Log("PASS: Tier persists across invocations")
}

// TestE2E_TierBoundsAtMaximum tests behavior when trying to promote beyond Master
func TestE2E_TierBoundsAtMaximum(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing tier bounds at maximum")

	// Set to Master
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "master")

	// Try to go up
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level", "up")
	output := string(out)

	// Should indicate already at max
	if !strings.Contains(output, "maximum") && !strings.Contains(output, "Master") {
		t.Errorf("Expected message about maximum tier, got: %s", output)
	}

	// Verify still at Master
	out = testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Master") {
		t.Errorf("Expected to remain at Master tier, got: %s", string(out))
	}

	logger.Log("PASS: Tier bounds at maximum work correctly")
}

// TestE2E_TierBoundsAtMinimum tests behavior when trying to demote below Apprentice
func TestE2E_TierBoundsAtMinimum(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing tier bounds at minimum")

	// Default is Apprentice - try to go down
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level", "down")
	output := string(out)

	// Should indicate already at min
	if !strings.Contains(output, "minimum") && !strings.Contains(output, "Apprentice") {
		t.Errorf("Expected message about minimum tier, got: %s", output)
	}

	// Verify still at Apprentice
	out = testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Apprentice") {
		t.Errorf("Expected to remain at Apprentice tier, got: %s", string(out))
	}

	logger.Log("PASS: Tier bounds at minimum work correctly")
}

// TestE2E_UsageStatsDisplay tests that usage stats are shown in level command
func TestE2E_UsageStatsDisplay(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing usage stats display")

	// Check level command output includes stats
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	output := stripANSI(string(out)) // Strip ANSI codes for reliable string matching

	// Should show usage stats section
	expectedStats := []string{"Commands run:", "Sessions created:", "Using NTM for:"}
	for _, stat := range expectedStats {
		if !strings.Contains(output, stat) {
			t.Errorf("Expected usage stat %q in level output", stat)
		}
	}

	logger.Log("PASS: Usage stats displayed in level command")
}

// TestE2E_ConfigFileCreation tests that proficiency config file is created
func TestE2E_ConfigFileCreation(t *testing.T) {
	testutil.RequireNTMBinary(t)

	tmpDir := t.TempDir()
	os.Setenv("XDG_CONFIG_HOME", tmpDir)
	defer os.Unsetenv("XDG_CONFIG_HOME")

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing config file creation")

	// Run level command to trigger config creation
	testutil.AssertCommandSuccess(t, logger, "ntm", "level")

	// Verify config file exists
	configPath := filepath.Join(tmpDir, "ntm", "proficiency.json")
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		t.Errorf("Expected config file at %s to exist", configPath)
	}

	// Read and verify content is valid JSON
	content, err := os.ReadFile(configPath)
	if err != nil {
		t.Fatalf("Failed to read config file: %v", err)
	}

	if !strings.Contains(string(content), "tier") {
		t.Errorf("Expected config file to contain 'tier' field")
	}

	logger.Log("PASS: Config file created and contains valid data")
}

// TestE2E_TierFullProgression tests full progression from Apprentice to Master
func TestE2E_TierFullProgression(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing full tier progression")

	// Start at Apprentice (default)
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Apprentice") {
		t.Fatalf("Expected to start at Apprentice tier")
	}

	// Promote to Journeyman
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "up")
	out = testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Journeyman") {
		t.Errorf("Expected Journeyman after first 'up', got: %s", string(out))
	}

	// Promote to Master
	testutil.AssertCommandSuccess(t, logger, "ntm", "level", "up")
	out = testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Master") {
		t.Errorf("Expected Master after second 'up', got: %s", string(out))
	}

	logger.Log("PASS: Full tier progression Apprentice -> Journeyman -> Master works")
}

// TestE2E_InvalidEnvTierIgnored tests that invalid env tier values are ignored
func TestE2E_InvalidEnvTierIgnored(t *testing.T) {
	testutil.RequireNTMBinary(t)

	cleanup := setupTierTestEnv(t)
	defer cleanup()

	logger := testutil.NewTestLoggerStdout(t)
	logger.LogSection("Testing invalid env tier is ignored")

	// Set invalid tier value
	os.Setenv("NTM_PROFICIENCY_TIER", "invalid")

	// Should fall back to config (default Apprentice)
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Apprentice") {
		t.Errorf("Expected Apprentice tier when env is invalid, got: %s", string(out))
	}

	// Set out of range tier
	os.Setenv("NTM_PROFICIENCY_TIER", "99")
	out = testutil.AssertCommandSuccess(t, logger, "ntm", "level")
	if !strings.Contains(string(out), "Apprentice") {
		t.Errorf("Expected Apprentice tier when env is out of range, got: %s", string(out))
	}

	logger.Log("PASS: Invalid env tier values are ignored")
}
