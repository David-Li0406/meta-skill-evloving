package agentmail

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
	"time"
)

// TestLoadSessionAgent_Fallback tests the fallback logic in LoadSessionAgent.
func TestLoadSessionAgent_Fallback(t *testing.T) {
	// Setup temporary config directory
	tmpDir := t.TempDir()

	// Mock user config dir via environment variable or override function if possible.
	// Since sessionAgentPath uses os.UserConfigDir(), we can't easily mock it without
	// changing the implementation or using a different approach.
	// Instead, we can create a local version of sessionAgentPath for testing logic,
	// OR we can rely on the fact that LoadSessionAgent calls sessionAgentPath.

	// However, sessionAgentPath is not exported and uses hardcoded os.UserConfigDir().
	// To test this effectively without mocking os.UserConfigDir (which is hard),
	// let's create the directory structure manually in a location and see if we can
	// point the function to it. But we can't redirect it.

	// WAIT: sessionAgentPath uses os.UserConfigDir() OR HOME/.config.
	// We can set HOME environment variable to tmpDir.
	t.Setenv("HOME", tmpDir)

	sessionName := "test-session"
	projectKey := "/path/to/project"
	projectSlug := "project" // ProjectSlugFromPath("/path/to/project") -> "project"

	// Expected paths based on implementation:
	// New: $HOME/.config/ntm/sessions/test-session/project/agent.json
	// Legacy: $HOME/.config/ntm/sessions/test-session/agent.json

	configDir, err := os.UserConfigDir()
	if err != nil {
		configDir = filepath.Join(tmpDir, ".config")
	}
	baseDir := filepath.Join(configDir, "ntm", "sessions", sessionName)
	newPath := filepath.Join(baseDir, projectSlug, "agent.json")
	legacyPath := filepath.Join(baseDir, "agent.json")

	info := SessionAgentInfo{
		AgentName:    "test-agent",
		ProjectKey:   projectKey,
		RegisteredAt: time.Now(),
		LastActiveAt: time.Now(),
	}
	data, _ := json.Marshal(info)

	// Helper to clear directories
	reset := func() {
		os.RemoveAll(configDir)
	}

	// 1. Test finding in new path
	t.Run("Finds in new path", func(t *testing.T) {
		reset()
		if err := os.MkdirAll(filepath.Dir(newPath), 0755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(newPath, data, 0644); err != nil {
			t.Fatal(err)
		}

		loaded, err := LoadSessionAgent(sessionName, projectKey)
		if err != nil {
			t.Fatalf("Failed to load: %v", err)
		}
		if loaded == nil {
			t.Fatal("Expected loaded agent, got nil")
		}
		if loaded.AgentName != info.AgentName {
			t.Errorf("Expected agent %s, got %s", info.AgentName, loaded.AgentName)
		}
	})

	// 2. Test fallback to legacy path when project key is provided but new path missing
	t.Run("Fallback to legacy path", func(t *testing.T) {
		reset()
		if err := os.MkdirAll(filepath.Dir(legacyPath), 0755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(legacyPath, data, 0644); err != nil {
			t.Fatal(err)
		}

		loaded, err := LoadSessionAgent(sessionName, projectKey)
		if err != nil {
			t.Fatalf("Failed to load: %v", err)
		}
		if loaded == nil {
			t.Fatal("Expected loaded agent, got nil")
		}
		if loaded.AgentName != info.AgentName {
			t.Errorf("Expected agent %s, got %s", info.AgentName, loaded.AgentName)
		}
	})

	// 3. Test fallback to searching subdirectories when project key is unknown/empty
	// (Note: LoadSessionAgent calls sessionAgentPath(name, "") which returns legacyPath.
	// If legacyPath doesn't exist, it used to search subdirectories but that unsafe behavior was removed.)
	t.Run("Fallback search subdirectories", func(t *testing.T) {
		reset()
		// Create a random slug dir
		randomSlugDir := filepath.Join(baseDir, "some-random-slug")
		randomPath := filepath.Join(randomSlugDir, "agent.json")

		if err := os.MkdirAll(randomSlugDir, 0755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(randomPath, data, 0644); err != nil {
			t.Fatal(err)
		}

		// Pass empty project key to trigger legacy lookup -> fail -> STOP (no search)
		loaded, err := LoadSessionAgent(sessionName, "")
		if err != nil {
			t.Fatalf("Failed to load: %v", err)
		}
		if loaded != nil {
			t.Fatal("Expected nil (strict loading), got agent")
		}
	})
}
