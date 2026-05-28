// Package e2e provides end-to-end tests for NTM.
package e2e

import (
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"testing"
)

// TestDashboardVisualRegression runs VHS-based visual regression tests.
// These tests require VHS to be installed (https://github.com/charmbracelet/vhs).
// If VHS is not available, tests are skipped.
func TestDashboardVisualRegression(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping visual regression tests in short mode")
	}

	// Check if VHS is installed
	if _, err := exec.LookPath("vhs"); err != nil {
		t.Skip("VHS not installed, skipping visual regression tests")
	}

	// Find project root
	projectRoot := findProjectRoot(t)
	scriptPath := filepath.Join(projectRoot, "scripts", "visual-regression.sh")

	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		t.Fatalf("visual-regression.sh not found at %s", scriptPath)
	}

	// Run the visual regression script
	cmd := exec.Command(scriptPath)
	cmd.Dir = projectRoot
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			switch exitErr.ExitCode() {
			case 1:
				t.Fatal("visual regression tests failed: screenshots differ from golden images")
			case 2:
				t.Fatal("visual regression setup error")
			default:
				t.Fatalf("visual regression script failed with exit code %d", exitErr.ExitCode())
			}
		}
		t.Fatalf("failed to run visual regression script: %v", err)
	}
}

// TestDashboardVisualBasic runs only the basic dashboard visual test.
func TestDashboardVisualBasic(t *testing.T) {
	runSingleVisualTest(t, "dashboard-basic")
}

// TestDashboardVisualResize runs only the resize visual test.
func TestDashboardVisualResize(t *testing.T) {
	runSingleVisualTest(t, "dashboard-resize")
}

// TestDashboardVisualNavigation runs only the navigation visual test.
func TestDashboardVisualNavigation(t *testing.T) {
	runSingleVisualTest(t, "dashboard-navigation")
}

// TestDashboardVisualRefresh runs only the refresh visual test.
func TestDashboardVisualRefresh(t *testing.T) {
	runSingleVisualTest(t, "dashboard-refresh")
}

// TestDashboardVisualMinimum runs only the minimum size visual test.
func TestDashboardVisualMinimum(t *testing.T) {
	runSingleVisualTest(t, "dashboard-minimum")
}

// runSingleVisualTest runs a single VHS tape test.
func runSingleVisualTest(t *testing.T, tapeName string) {
	t.Helper()

	if testing.Short() {
		t.Skip("skipping visual regression tests in short mode")
	}

	// Check if VHS is installed
	if _, err := exec.LookPath("vhs"); err != nil {
		t.Skip("VHS not installed, skipping visual regression tests")
	}

	projectRoot := findProjectRoot(t)
	scriptPath := filepath.Join(projectRoot, "scripts", "visual-regression.sh")

	cmd := exec.Command(scriptPath, tapeName)
	cmd.Dir = projectRoot
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok && exitErr.ExitCode() == 1 {
			t.Fatalf("visual regression test %s failed: screenshots differ", tapeName)
		}
		t.Fatalf("visual regression test %s failed: %v", tapeName, err)
	}
}

// findProjectRoot finds the NTM project root directory.
func findProjectRoot(t *testing.T) string {
	t.Helper()

	// Try to find via go.mod
	_, filename, _, ok := runtime.Caller(0)
	if !ok {
		t.Fatal("cannot get current file path")
	}

	dir := filepath.Dir(filename)
	for {
		if _, err := os.Stat(filepath.Join(dir, "go.mod")); err == nil {
			return dir
		}
		parent := filepath.Dir(dir)
		if parent == dir {
			break
		}
		dir = parent
	}

	// Fallback to current working directory
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("cannot get working directory: %v", err)
	}
	return cwd
}

// TestUpdateGoldenImages is a helper test that can be run manually to update golden images.
// Run with: go test -v -run TestUpdateGoldenImages ./tests/e2e -update-golden
func TestUpdateGoldenImages(t *testing.T) {
	if os.Getenv("UPDATE_GOLDEN") != "1" && !hasUpdateGoldenFlag() {
		t.Skip("set UPDATE_GOLDEN=1 or pass -update-golden flag to update golden images")
	}

	if _, err := exec.LookPath("vhs"); err != nil {
		t.Fatal("VHS not installed, cannot update golden images")
	}

	projectRoot := findProjectRoot(t)
	scriptPath := filepath.Join(projectRoot, "scripts", "visual-regression.sh")

	cmd := exec.Command(scriptPath, "--update")
	cmd.Dir = projectRoot
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		t.Fatalf("failed to update golden images: %v", err)
	}

	t.Log("Golden images updated successfully")
}

// hasUpdateGoldenFlag checks if -update-golden flag was passed.
func hasUpdateGoldenFlag() bool {
	for _, arg := range os.Args {
		if arg == "-update-golden" || arg == "--update-golden" {
			return true
		}
	}
	return false
}
