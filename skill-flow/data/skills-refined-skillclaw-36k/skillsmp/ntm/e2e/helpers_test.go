// Package e2e contains end-to-end tests for NTM robot mode commands.
package e2e

import (
	"os"
	"os/exec"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// SkipIfShort skips the test in short mode.
func SkipIfShort(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping E2E test in short mode")
	}
}

// SkipIfNoTmux skips the test if tmux is not available.
func SkipIfNoTmux(t *testing.T) {
	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not found, skipping E2E test")
	}
}

// SkipIfNoNTM skips the test if ntm is not available.
func SkipIfNoNTM(t *testing.T) {
	if _, err := exec.LookPath("ntm"); err != nil {
		t.Skip("ntm not found, skipping E2E test")
	}
}

// SkipIfNoAgent skips the test if the specified agent CLI is not available.
func SkipIfNoAgent(t *testing.T, agentType string) {
	var alias string
	switch agentType {
	case "cc", "claude":
		alias = "cc"
	case "cod", "codex":
		alias = "cod"
	case "gmi", "gemini":
		alias = "gmi"
	default:
		t.Fatalf("Unknown agent type: %s", agentType)
	}

	if _, err := exec.LookPath(alias); err != nil {
		t.Skipf("%s not found, skipping E2E test", alias)
	}
}

// SkipIfNoAgents skips if none of the common agents are available.
func SkipIfNoAgents(t *testing.T) {
	ccFound := false
	codFound := false
	gmiFound := false

	if _, err := exec.LookPath("cc"); err == nil {
		ccFound = true
	}
	if _, err := exec.LookPath("cod"); err == nil {
		codFound = true
	}
	if _, err := exec.LookPath("gmi"); err == nil {
		gmiFound = true
	}

	if !ccFound && !codFound && !gmiFound {
		t.Skip("No agent CLIs (cc, cod, gmi) found, skipping E2E test")
	}
}

// GetAvailableAgent returns the first available agent type.
func GetAvailableAgent() string {
	if _, err := exec.LookPath("cc"); err == nil {
		return "cc"
	}
	if _, err := exec.LookPath("cod"); err == nil {
		return "cod"
	}
	if _, err := exec.LookPath("gmi"); err == nil {
		return "gmi"
	}
	return ""
}

// IsMockMode returns true if running in mock mode (for CI).
func IsMockMode() bool {
	return os.Getenv("E2E_MOCK_MODE") == "1"
}

// GetMockFile returns the path to the mock caut response file.
func GetMockFile() string {
	return os.Getenv("CAUT_MOCK_FILE")
}

// HasCautInstalled returns true if caut is available.
func HasCautInstalled() bool {
	_, err := exec.LookPath("caut")
	return err == nil
}

// CommonE2EPrerequisites checks all common prerequisites for E2E tests.
func CommonE2EPrerequisites(t *testing.T) {
	SkipIfShort(t)
	SkipIfNoTmux(t)
	SkipIfNoNTM(t)
}
