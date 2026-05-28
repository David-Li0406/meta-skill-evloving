package testutil

import (
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// RequireTmux skips the test if tmux is not installed.
func RequireTmux(t *testing.T) {
	t.Helper()
	if !tmux.DefaultClient.IsInstalled() {
		t.Skip("tmux not installed, skipping test")
	}
}

// RequireNTMBinary ensures tests run against a repo-built ntm binary.
//
// Many integration/E2E tests invoke "ntm" via PATH; relying on a globally installed
// binary is fragile (it may not match the workspace source). This helper builds the
// local binary once per test process and prepends it to PATH so LookPath/exec resolve
// the correct version.
func RequireNTMBinary(t *testing.T) {
	t.Helper()

	binary := BuildLocalNTM(t)
	binDir := filepath.Dir(binary)

	existing := os.Getenv("PATH")
	sep := string(os.PathListSeparator)
	if existing == "" {
		t.Setenv("PATH", binDir)
		return
	}
	if existing == binDir || strings.HasPrefix(existing, binDir+sep) {
		return
	}
	t.Setenv("PATH", binDir+sep+existing)
}

// RequireTmuxServer skips the test if no tmux server is running.
// Some tests need a tmux server already running.
func RequireTmuxServer(t *testing.T) {
	t.Helper()
	RequireTmux(t)
	if err := exec.Command(tmux.BinaryPath(), "list-sessions").Run(); err != nil {
		// Start a temporary server
		t.Log("No tmux server running, will create one for test")
	}
}

// RequireNotCI skips the test when running in CI environments.
// Useful for tests that require interactive terminal features.
func RequireNotCI(t *testing.T) {
	t.Helper()
	if os.Getenv("CI") != "" || os.Getenv("GITHUB_ACTIONS") != "" {
		t.Skip("skipping test in CI environment")
	}
}

// RequireCI only runs the test in CI environments.
func RequireCI(t *testing.T) {
	t.Helper()
	if os.Getenv("CI") == "" && os.Getenv("GITHUB_ACTIONS") == "" {
		t.Skip("test only runs in CI environment")
	}
}

// RequireRoot skips the test if not running as root.
func RequireRoot(t *testing.T) {
	t.Helper()
	if os.Getuid() != 0 {
		t.Skip("test requires root privileges")
	}
}

// RequireEnv skips the test if the specified environment variable is not set.
func RequireEnv(t *testing.T, envVar string) {
	t.Helper()
	if os.Getenv(envVar) == "" {
		t.Skipf("environment variable %s not set, skipping test", envVar)
	}
}

// RequireLinux skips the test on non-Linux systems.
func RequireLinux(t *testing.T) {
	t.Helper()
	if runtime.GOOS != "linux" {
		t.Skipf("test requires Linux, running on %s", runtime.GOOS)
	}
}

// RequireMacOS skips the test on non-macOS systems.
func RequireMacOS(t *testing.T) {
	t.Helper()
	if runtime.GOOS != "darwin" {
		t.Skipf("test requires macOS, running on %s", runtime.GOOS)
	}
}

// RequireUnix skips the test on non-Unix systems (Windows).
func RequireUnix(t *testing.T) {
	t.Helper()
	if runtime.GOOS == "windows" {
		t.Skip("test requires Unix-like system")
	}
}

// RequireIntegration skips the test unless integration tests are enabled.
// Set NTM_INTEGRATION_TESTS=1 to run integration tests.
func RequireIntegration(t *testing.T) {
	t.Helper()
	if os.Getenv("NTM_INTEGRATION_TESTS") == "" {
		t.Skip("integration tests disabled, set NTM_INTEGRATION_TESTS=1 to enable")
	}
}

// RequireE2E skips the test unless E2E tests are enabled.
// Set NTM_E2E_TESTS=1 to run E2E tests.
func RequireE2E(t *testing.T) {
	t.Helper()
	if os.Getenv("NTM_E2E_TESTS") == "" {
		t.Skip("E2E tests disabled, set NTM_E2E_TESTS=1 to enable")
	}
}

// SkipShort skips the test if -short flag is passed.
func SkipShort(t *testing.T) {
	t.Helper()
	if testing.Short() {
		t.Skip("skipping in short mode")
	}
}

// IntegrationTestPrecheck runs all common prechecks for integration tests.
// This is a convenience function that combines common skip conditions.
func IntegrationTestPrecheck(t *testing.T) {
	t.Helper()
	RequireIntegration(t)
	RequireTmux(t)
	RequireNTMBinary(t)
}

// E2ETestPrecheck runs all common prechecks for E2E tests.
func E2ETestPrecheck(t *testing.T) {
	t.Helper()
	RequireE2E(t)
	RequireTmux(t)
	RequireNTMBinary(t)
}
