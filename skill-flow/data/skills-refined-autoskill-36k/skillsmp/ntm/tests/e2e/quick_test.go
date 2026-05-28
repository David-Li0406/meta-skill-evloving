package e2e

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/Dicklesworthstone/ntm/tests/testutil"
)

func writeProjectsBaseConfig(t *testing.T, projectsBase string) string {
	t.Helper()

	configPath := filepath.Join(t.TempDir(), "config.toml")
	content := fmt.Sprintf("projects_base = %q\n", projectsBase)
	if err := os.WriteFile(configPath, []byte(content), 0644); err != nil {
		t.Fatalf("failed to write config file: %v", err)
	}
	return configPath
}

// TestQuickSetupGo tests ntm quick with Go template creates correct scaffolding.
func TestQuickSetupGo(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectName := fmt.Sprintf("ntm_e2e_test_go_%d", time.Now().UnixNano())

	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)
	projectDir := filepath.Join(projectsBase, projectName)

	// Run ntm quick with Go template
	logger.LogSection("Creating Go project with ntm quick")
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "--config", configPath, "quick", projectName, "--template=go")
	logger.Log("OUTPUT:\n%s", string(out))

	// Verify project directory was created
	logger.LogSection("Verifying project structure")

	assertFileExists(t, logger, projectDir, "project directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".git"), ".git directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".gitignore"), ".gitignore")
	assertFileExists(t, logger, filepath.Join(projectDir, ".vscode", "settings.json"), ".vscode/settings.json")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "settings.toml"), ".claude/settings.toml")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "commands", "review.md"), ".claude/commands/review.md")

	// Go-specific files
	assertFileExists(t, logger, filepath.Join(projectDir, "go.mod"), "go.mod")
	assertFileExists(t, logger, filepath.Join(projectDir, "main.go"), "main.go")

	// Verify .gitignore contains Go patterns
	gitignore, err := os.ReadFile(filepath.Join(projectDir, ".gitignore"))
	if err != nil {
		t.Fatalf("failed to read .gitignore: %v", err)
	}
	assertContains(t, logger, string(gitignore), "*.test", ".gitignore Go patterns")
	assertContains(t, logger, string(gitignore), "go.work", ".gitignore Go patterns")

	// Verify main.go content
	mainGo, err := os.ReadFile(filepath.Join(projectDir, "main.go"))
	if err != nil {
		t.Fatalf("failed to read main.go: %v", err)
	}
	assertContains(t, logger, string(mainGo), "package main", "main.go package declaration")
	assertContains(t, logger, string(mainGo), "func main()", "main.go main function")

	logger.Log("PASS: Go project scaffolding verified successfully")
}

// TestQuickSetupPython tests ntm quick with Python template.
func TestQuickSetupPython(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectName := fmt.Sprintf("ntm_e2e_test_python_%d", time.Now().UnixNano())

	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)
	projectDir := filepath.Join(projectsBase, projectName)

	logger.LogSection("Creating Python project with ntm quick")
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "--config", configPath, "quick", projectName, "--template=python")
	logger.Log("OUTPUT:\n%s", string(out))

	logger.LogSection("Verifying project structure")

	// Common files
	assertFileExists(t, logger, projectDir, "project directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".git"), ".git directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".gitignore"), ".gitignore")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "settings.toml"), ".claude/settings.toml")

	// Python-specific files
	assertFileExists(t, logger, filepath.Join(projectDir, "pyproject.toml"), "pyproject.toml")
	assertFileExists(t, logger, filepath.Join(projectDir, "main.py"), "main.py")

	// Verify .gitignore contains Python patterns
	gitignore, err := os.ReadFile(filepath.Join(projectDir, ".gitignore"))
	if err != nil {
		t.Fatalf("failed to read .gitignore: %v", err)
	}
	assertContains(t, logger, string(gitignore), "*.pyc", ".gitignore Python patterns")
	assertContains(t, logger, string(gitignore), ".pytest_cache", ".gitignore Python patterns")

	logger.Log("PASS: Python project scaffolding verified successfully")
}

// TestQuickSetupNode tests ntm quick with Node.js template.
func TestQuickSetupNode(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectName := fmt.Sprintf("ntm_e2e_test_node_%d", time.Now().UnixNano())

	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)
	projectDir := filepath.Join(projectsBase, projectName)

	logger.LogSection("Creating Node.js project with ntm quick")
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "--config", configPath, "quick", projectName, "--template=node")
	logger.Log("OUTPUT:\n%s", string(out))

	logger.LogSection("Verifying project structure")

	// Common files
	assertFileExists(t, logger, projectDir, "project directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".git"), ".git directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".gitignore"), ".gitignore")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "settings.toml"), ".claude/settings.toml")

	// Node-specific files
	assertFileExists(t, logger, filepath.Join(projectDir, "package.json"), "package.json")
	assertFileExists(t, logger, filepath.Join(projectDir, "index.js"), "index.js")

	// Verify .gitignore contains Node patterns
	gitignore, err := os.ReadFile(filepath.Join(projectDir, ".gitignore"))
	if err != nil {
		t.Fatalf("failed to read .gitignore: %v", err)
	}
	assertContains(t, logger, string(gitignore), "node_modules", ".gitignore Node patterns")
	assertContains(t, logger, string(gitignore), "npm-debug.log", ".gitignore Node patterns")

	logger.Log("PASS: Node.js project scaffolding verified successfully")
}

// TestQuickSetupRust tests ntm quick with Rust template.
func TestQuickSetupRust(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectName := fmt.Sprintf("ntm_e2e_test_rust_%d", time.Now().UnixNano())

	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)
	projectDir := filepath.Join(projectsBase, projectName)

	logger.LogSection("Creating Rust project with ntm quick")
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "--config", configPath, "quick", projectName, "--template=rust")
	logger.Log("OUTPUT:\n%s", string(out))

	logger.LogSection("Verifying project structure")

	// Common files
	assertFileExists(t, logger, projectDir, "project directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".git"), ".git directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".gitignore"), ".gitignore")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "settings.toml"), ".claude/settings.toml")

	// Rust-specific files
	assertFileExists(t, logger, filepath.Join(projectDir, "Cargo.toml"), "Cargo.toml")
	assertFileExists(t, logger, filepath.Join(projectDir, "src", "main.rs"), "src/main.rs")

	// Verify .gitignore contains Rust patterns
	gitignore, err := os.ReadFile(filepath.Join(projectDir, ".gitignore"))
	if err != nil {
		t.Fatalf("failed to read .gitignore: %v", err)
	}
	assertContains(t, logger, string(gitignore), "target/", ".gitignore Rust patterns")
	assertContains(t, logger, string(gitignore), "Cargo.lock", ".gitignore Rust patterns")

	logger.Log("PASS: Rust project scaffolding verified successfully")
}

// TestQuickSetupNoTemplate tests ntm quick without a template (basic scaffolding only).
func TestQuickSetupNoTemplate(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectName := fmt.Sprintf("ntm_e2e_test_basic_%d", time.Now().UnixNano())

	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)
	projectDir := filepath.Join(projectsBase, projectName)

	logger.LogSection("Creating basic project with ntm quick (no template)")
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "--config", configPath, "quick", projectName)
	logger.Log("OUTPUT:\n%s", string(out))

	logger.LogSection("Verifying project structure")

	// Common files only - no template-specific files
	assertFileExists(t, logger, projectDir, "project directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".git"), ".git directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".gitignore"), ".gitignore")
	assertFileExists(t, logger, filepath.Join(projectDir, ".vscode", "settings.json"), ".vscode/settings.json")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "settings.toml"), ".claude/settings.toml")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "commands", "review.md"), ".claude/commands/review.md")

	logger.Log("PASS: Basic project scaffolding verified successfully")
}

// TestQuickSetupNoGit tests ntm quick with --no-git flag.
func TestQuickSetupNoGit(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectName := fmt.Sprintf("ntm_e2e_test_nogit_%d", time.Now().UnixNano())

	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)
	projectDir := filepath.Join(projectsBase, projectName)

	logger.LogSection("Creating project with --no-git flag")
	out := testutil.AssertCommandSuccess(t, logger, "ntm", "--config", configPath, "quick", projectName, "--no-git")
	logger.Log("OUTPUT:\n%s", string(out))

	logger.LogSection("Verifying project structure")

	assertFileExists(t, logger, projectDir, "project directory")
	assertFileExists(t, logger, filepath.Join(projectDir, ".gitignore"), ".gitignore")
	assertFileExists(t, logger, filepath.Join(projectDir, ".claude", "settings.toml"), ".claude/settings.toml")

	// .git should NOT exist
	assertFileNotExists(t, logger, filepath.Join(projectDir, ".git"), ".git directory (should not exist)")

	logger.Log("PASS: No-git project scaffolding verified successfully")
}

// TestQuickSetupExistingDirectory tests that ntm quick fails when directory already exists.
func TestQuickSetupExistingDirectory(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectName := fmt.Sprintf("ntm_e2e_test_exists_%d", time.Now().UnixNano())

	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)
	projectDir := filepath.Join(projectsBase, projectName)

	// Create the directory first
	if err := os.MkdirAll(projectDir, 0755); err != nil {
		t.Fatalf("failed to create test directory: %v", err)
	}

	logger.LogSection("Testing ntm quick on existing directory")
	_ = testutil.AssertCommandFails(t, logger, "ntm", "--config", configPath, "quick", projectName)

	logger.Log("PASS: ntm quick correctly failed on existing directory")
}

// TestQuickSetupInvalidName tests that ntm quick fails with invalid project names.
func TestQuickSetupInvalidName(t *testing.T) {
	testutil.RequireNTMBinary(t)

	logger := testutil.NewTestLoggerStdout(t)
	projectsBase := t.TempDir()
	configPath := writeProjectsBaseConfig(t, projectsBase)

	invalidNames := []string{
		"test/project",
		"test:project",
		"test*project",
		"test?project",
	}

	for _, name := range invalidNames {
		logger.LogSection(fmt.Sprintf("Testing invalid name: %s", name))
		_ = testutil.AssertCommandFails(t, logger, "ntm", "--config", configPath, "quick", name)
		logger.Log("PASS: ntm quick correctly rejected invalid name: %s", name)
	}
}

// Helper functions

func assertFileExists(t *testing.T, logger *testutil.TestLogger, path, description string) {
	t.Helper()
	logger.Log("VERIFY: %s exists at %s", description, path)

	info, err := os.Stat(path)
	if os.IsNotExist(err) {
		logger.Log("FAIL: %s does not exist", description)
		t.Errorf("%s does not exist at %s", description, path)
		return
	}
	if err != nil {
		logger.Log("FAIL: Error checking %s: %v", description, err)
		t.Errorf("error checking %s: %v", description, err)
		return
	}

	logger.Log("PASS: %s exists (size=%d, mode=%s)", description, info.Size(), info.Mode())
}

func assertFileNotExists(t *testing.T, logger *testutil.TestLogger, path, description string) {
	t.Helper()
	logger.Log("VERIFY: %s does NOT exist at %s", description, path)

	_, err := os.Stat(path)
	if err == nil {
		logger.Log("FAIL: %s exists but should not", description)
		t.Errorf("%s exists at %s but should not", description, path)
		return
	}
	if !os.IsNotExist(err) {
		logger.Log("FAIL: Unexpected error checking %s: %v", description, err)
		t.Errorf("unexpected error checking %s: %v", description, err)
		return
	}

	logger.Log("PASS: %s does not exist (as expected)", description)
}

func assertContains(t *testing.T, logger *testutil.TestLogger, content, substring, description string) {
	t.Helper()
	logger.Log("VERIFY: %s contains %q", description, substring)

	if !strings.Contains(content, substring) {
		logger.Log("FAIL: %s does not contain %q", description, substring)
		t.Errorf("%s does not contain %q", description, substring)
		return
	}

	logger.Log("PASS: %s contains %q", description, substring)
}
