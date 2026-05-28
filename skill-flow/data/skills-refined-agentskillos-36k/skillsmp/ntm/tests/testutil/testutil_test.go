package testutil

import (
	"os"
	"path/filepath"
	"testing"
)

func TestNewTestLoggerStdout(t *testing.T) {
	logger := NewTestLoggerStdout(t)
	if logger == nil {
		t.Fatal("expected non-nil logger")
	}
	if logger.testName != t.Name() {
		t.Errorf("expected testName %q, got %q", t.Name(), logger.testName)
	}

	// Test logging doesn't panic
	logger.Log("test message %d", 42)
	logger.LogSection("test section")
}

func TestNewTestLogger(t *testing.T) {
	tmpDir := t.TempDir()
	logger := NewTestLogger(t, tmpDir)
	if logger == nil {
		t.Fatal("expected non-nil logger")
	}

	// Log something
	logger.Log("test log entry")
	logger.LogSection("section")

	// Verify a log file was created
	entries, err := os.ReadDir(tmpDir)
	if err != nil {
		t.Fatalf("failed to read temp dir: %v", err)
	}
	if len(entries) == 0 {
		t.Error("expected log file to be created")
	}

	// Verify file contains content
	logPath := filepath.Join(tmpDir, entries[0].Name())
	content, err := os.ReadFile(logPath)
	if err != nil {
		t.Fatalf("failed to read log file: %v", err)
	}
	if len(content) == 0 {
		t.Error("expected log file to have content")
	}
}

func TestLoggerElapsed(t *testing.T) {
	logger := NewTestLoggerStdout(t)
	elapsed := logger.Elapsed()
	if elapsed < 0 {
		t.Errorf("elapsed time should be non-negative: %v", elapsed)
	}
}

func TestRequireTmux(t *testing.T) {
	// This test just verifies RequireTmux doesn't panic
	// It will skip if tmux is not installed
	RequireTmux(t)
	t.Log("tmux is installed")
}

func TestSessionExists(t *testing.T) {
	// Test with a session that definitely doesn't exist
	exists := SessionExists("nonexistent_session_" + t.Name())
	if exists {
		t.Error("session should not exist")
	}
}

func TestAgentConfig(t *testing.T) {
	config := AgentConfig{
		Claude: 2,
		Codex:  1,
		Gemini: 1,
	}

	if config.Claude != 2 {
		t.Errorf("expected Claude=2, got %d", config.Claude)
	}
	if config.Codex != 1 {
		t.Errorf("expected Codex=1, got %d", config.Codex)
	}
	if config.Gemini != 1 {
		t.Errorf("expected Gemini=1, got %d", config.Gemini)
	}
}

func TestSkipConditions(t *testing.T) {
	// These are just sanity checks that the skip functions exist and don't panic
	t.Run("RequireUnix", func(t *testing.T) {
		RequireUnix(t)
	})

	t.Run("IntegrationPrecheck", func(t *testing.T) {
		// This will skip because NTM_INTEGRATION_TESTS is not set
		// Just verify it doesn't panic
		if os.Getenv("NTM_INTEGRATION_TESTS") != "" {
			IntegrationTestPrecheck(t)
		}
	})
}
