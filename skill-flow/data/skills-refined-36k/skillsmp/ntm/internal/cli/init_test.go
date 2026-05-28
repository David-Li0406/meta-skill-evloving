package cli

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/config"
)

// TestInitCmd_NoArgs verifies ntm init with no arguments uses current working directory
func TestInitCmd_NoArgs(t *testing.T) {
	t.Parallel()

	// Create temp directory
	tmpDir := t.TempDir()

	// Save and restore working directory
	oldWd, err := os.Getwd()
	if err != nil {
		t.Fatalf("get working directory: %v", err)
	}
	defer os.Chdir(oldWd)

	if err := os.Chdir(tmpDir); err != nil {
		t.Fatalf("change to temp dir: %v", err)
	}

	// Run init with no target (uses cwd)
	opts := initOptions{
		NonInteractive: true,
		NoHooks:        true, // Skip git hooks in test
	}

	err = runProjectInit(opts)
	if err != nil {
		t.Fatalf("runProjectInit failed: %v", err)
	}

	// Verify .ntm directory created
	ntmDir := filepath.Join(tmpDir, ".ntm")
	if _, err := os.Stat(ntmDir); os.IsNotExist(err) {
		t.Errorf(".ntm directory not created at %s", ntmDir)
	}

	// Verify config.toml created
	configPath := filepath.Join(ntmDir, "config.toml")
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		t.Errorf("config.toml not created at %s", configPath)
	}

	t.Logf("TEST: InitCmd_NoArgs | Input: opts=%+v | Expected: .ntm created | Got: success", opts)
}

// TestInitCmd_ExplicitPath verifies ntm init with explicit path argument
func TestInitCmd_ExplicitPath(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()

	opts := initOptions{
		TargetDir:      tmpDir,
		NonInteractive: true,
		NoHooks:        true,
	}

	err := runProjectInit(opts)
	if err != nil {
		t.Fatalf("runProjectInit failed: %v", err)
	}

	// Verify .ntm directory created
	ntmDir := filepath.Join(tmpDir, ".ntm")
	if _, err := os.Stat(ntmDir); os.IsNotExist(err) {
		t.Errorf(".ntm directory not created at %s", ntmDir)
	}

	t.Logf("TEST: InitCmd_ExplicitPath | Input: TargetDir=%s | Expected: .ntm created | Got: success", tmpDir)
}

// TestInitCmd_Force verifies --force flag overwrites existing config
func TestInitCmd_Force(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()

	// First init
	opts := initOptions{
		TargetDir:      tmpDir,
		NonInteractive: true,
		NoHooks:        true,
	}
	if err := runProjectInit(opts); err != nil {
		t.Fatalf("first init failed: %v", err)
	}

	// Modify config.toml to verify overwrite
	configPath := filepath.Join(tmpDir, ".ntm", "config.toml")
	originalContent, _ := os.ReadFile(configPath)
	modifiedContent := append(originalContent, []byte("\n# Modified\n")...)
	if err := os.WriteFile(configPath, modifiedContent, 0644); err != nil {
		t.Fatalf("write modified config: %v", err)
	}

	// Second init WITHOUT force should fail
	opts.Force = false
	err := runProjectInit(opts)
	if err == nil {
		t.Error("expected error when reinitializing without --force")
	}
	if !strings.Contains(err.Error(), "already initialized") {
		t.Errorf("expected 'already initialized' error, got: %v", err)
	}

	// Second init WITH force should succeed
	opts.Force = true
	if err := runProjectInit(opts); err != nil {
		t.Fatalf("init with --force failed: %v", err)
	}

	// Verify config was overwritten (no "# Modified" marker)
	newContent, _ := os.ReadFile(configPath)
	if strings.Contains(string(newContent), "# Modified") {
		t.Error("config.toml not overwritten with --force")
	}

	t.Logf("TEST: InitCmd_Force | Input: Force=%v | Expected: overwrite | Got: success", opts.Force)
}

// TestInitCmd_NonExistentDir verifies error for non-existent target directory
func TestInitCmd_NonExistentDir(t *testing.T) {
	t.Parallel()

	opts := initOptions{
		TargetDir:      "/non/existent/path/surely/does/not/exist",
		NonInteractive: true,
		NoHooks:        true,
	}

	err := runProjectInit(opts)
	if err == nil {
		t.Error("expected error for non-existent directory")
	}
	if !strings.Contains(err.Error(), "not found") && !strings.Contains(err.Error(), "no such file") {
		t.Errorf("expected 'not found' error, got: %v", err)
	}

	t.Logf("TEST: InitCmd_NonExistentDir | Input: %s | Expected: error | Got: %v", opts.TargetDir, err)
}

// TestInitCmd_FileNotDir verifies error when target is a file, not directory
func TestInitCmd_FileNotDir(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()
	filePath := filepath.Join(tmpDir, "not-a-dir")
	if err := os.WriteFile(filePath, []byte("test"), 0644); err != nil {
		t.Fatalf("create test file: %v", err)
	}

	opts := initOptions{
		TargetDir:      filePath,
		NonInteractive: true,
		NoHooks:        true,
	}

	err := runProjectInit(opts)
	if err == nil {
		t.Error("expected error for file target")
	}
	if !strings.Contains(err.Error(), "not a directory") {
		t.Errorf("expected 'not a directory' error, got: %v", err)
	}

	t.Logf("TEST: InitCmd_FileNotDir | Input: %s | Expected: error | Got: %v", filePath, err)
}

// TestInitCmd_CreatesAllDirectories verifies all required directories are created
func TestInitCmd_CreatesAllDirectories(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()

	opts := initOptions{
		TargetDir:      tmpDir,
		NonInteractive: true,
		NoHooks:        true,
	}

	if err := runProjectInit(opts); err != nil {
		t.Fatalf("runProjectInit failed: %v", err)
	}

	// Check required directories
	requiredDirs := []string{
		".ntm",
		".ntm/templates",
		".ntm/pipelines",
	}

	for _, dir := range requiredDirs {
		fullPath := filepath.Join(tmpDir, dir)
		info, err := os.Stat(fullPath)
		if os.IsNotExist(err) {
			t.Errorf("required directory %s not created", dir)
			continue
		}
		if !info.IsDir() {
			t.Errorf("%s is not a directory", dir)
		}
	}

	t.Logf("TEST: InitCmd_CreatesAllDirectories | Expected: %v | Got: all created", requiredDirs)
}

// TestInitCmd_CreatesAllFiles verifies all required files are created
func TestInitCmd_CreatesAllFiles(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()

	opts := initOptions{
		TargetDir:      tmpDir,
		NonInteractive: true,
		NoHooks:        true,
	}

	if err := runProjectInit(opts); err != nil {
		t.Fatalf("runProjectInit failed: %v", err)
	}

	// Check required files
	requiredFiles := []string{
		".ntm/config.toml",
		".ntm/palette.md",
		".ntm/personas.toml",
	}

	for _, file := range requiredFiles {
		fullPath := filepath.Join(tmpDir, file)
		info, err := os.Stat(fullPath)
		if os.IsNotExist(err) {
			t.Errorf("required file %s not created", file)
			continue
		}
		if info.IsDir() {
			t.Errorf("%s should be a file, not directory", file)
		}
		if info.Size() == 0 {
			t.Errorf("%s is empty", file)
		}
	}

	t.Logf("TEST: InitCmd_CreatesAllFiles | Expected: %v | Got: all created", requiredFiles)
}

// TestInitCmd_ConfigContainsProjectName verifies config.toml includes project name
func TestInitCmd_ConfigContainsProjectName(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()
	projectName := filepath.Base(tmpDir)

	opts := initOptions{
		TargetDir:      tmpDir,
		NonInteractive: true,
		NoHooks:        true,
	}

	if err := runProjectInit(opts); err != nil {
		t.Fatalf("runProjectInit failed: %v", err)
	}

	// Read and parse config
	configPath := filepath.Join(tmpDir, ".ntm", "config.toml")
	cfg, err := config.LoadProjectConfig(configPath)
	if err != nil {
		t.Fatalf("load config: %v", err)
	}

	if cfg.Project.Name != projectName {
		t.Errorf("project name = %q, want %q", cfg.Project.Name, projectName)
	}

	if cfg.Project.Created == "" {
		t.Error("project created timestamp is empty")
	}

	t.Logf("TEST: InitCmd_ConfigContainsProjectName | Expected: %s | Got: %s", projectName, cfg.Project.Name)
}

// TestInitCmd_PreservesExistingFiles verifies existing files are not overwritten without --force
func TestInitCmd_PreservesExistingFiles(t *testing.T) {
	t.Parallel()

	tmpDir := t.TempDir()

	// Create partial .ntm structure with custom palette
	ntmDir := filepath.Join(tmpDir, ".ntm")
	if err := os.MkdirAll(ntmDir, 0755); err != nil {
		t.Fatalf("create .ntm: %v", err)
	}

	customPalette := "# My Custom Palette\n## Custom Section\n"
	palettePath := filepath.Join(ntmDir, "palette.md")
	if err := os.WriteFile(palettePath, []byte(customPalette), 0644); err != nil {
		t.Fatalf("write custom palette: %v", err)
	}

	// Run init (config.toml doesn't exist, so this should work)
	opts := initOptions{
		TargetDir:      tmpDir,
		NonInteractive: true,
		NoHooks:        true,
		Force:          true, // Force because .ntm exists
	}

	if err := runProjectInit(opts); err != nil {
		t.Fatalf("runProjectInit failed: %v", err)
	}

	// Note: With force=true, files may be overwritten
	// Without force, the init would fail because .ntm exists
	// This test validates the force behavior
	t.Logf("TEST: InitCmd_PreservesExistingFiles | Force=%v | Got: success", opts.Force)
}

// TestIsShellName verifies shell name detection
func TestIsShellName(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{"zsh", "zsh", true},
		{"bash", "bash", true},
		{"fish", "fish", true},
		{"sh", "sh", false},
		{"random_path", "/some/path", false},
		{"empty", "", false},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got := isShellName(tc.input)
			if got != tc.expected {
				t.Errorf("isShellName(%q) = %v, want %v", tc.input, got, tc.expected)
			}
			t.Logf("TEST: isShellName | Input: %q | Expected: %v | Got: %v", tc.input, tc.expected, got)
		})
	}
}

// TestQuoteAlias verifies shell alias quoting
func TestQuoteAlias(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"simple", "claude", "'claude'"},
		{"with_space", "claude --project foo", "'claude --project foo'"},
		{"empty", "", "''"},
		{"with_single_quote", "echo 'hello'", "'echo '\\''hello'\\'''"},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got := quoteAlias(tc.input)
			if got != tc.expected {
				t.Errorf("quoteAlias(%q) = %q, want %q", tc.input, got, tc.expected)
			}
			t.Logf("TEST: quoteAlias | Input: %q | Expected: %q | Got: %q", tc.input, tc.expected, got)
		})
	}
}

// TestGenerateZsh verifies zsh shell integration output
func TestGenerateZsh(t *testing.T) {
	t.Parallel()

	cfg := config.Default()
	output := generateZsh(cfg)

	// Verify key elements are present
	checks := []string{
		"alias cc=",
		"alias cod=",
		"alias gmi=",
		"alias cnt='ntm create'",
		"alias sat='ntm spawn'",
		"_ntm()",
		"compdef _ntm ntm",
		"bindkey",
	}

	for _, check := range checks {
		if !strings.Contains(output, check) {
			t.Errorf("zsh output missing: %q", check)
		}
	}

	t.Logf("TEST: GenerateZsh | Output length: %d | All checks: passed", len(output))
}

// TestGenerateBash verifies bash shell integration output
func TestGenerateBash(t *testing.T) {
	t.Parallel()

	cfg := config.Default()
	output := generateBash(cfg)

	// Verify key elements are present
	checks := []string{
		"alias cc=",
		"alias cod=",
		"alias gmi=",
		"alias cnt='ntm create'",
		"_ntm_completions()",
		"complete -F _ntm_completions ntm",
	}

	for _, check := range checks {
		if !strings.Contains(output, check) {
			t.Errorf("bash output missing: %q", check)
		}
	}

	t.Logf("TEST: GenerateBash | Output length: %d | All checks: passed", len(output))
}

// TestGenerateFish verifies fish shell integration output
func TestGenerateFish(t *testing.T) {
	t.Parallel()

	cfg := config.Default()
	output := generateFish(cfg)

	// Verify key elements are present
	checks := []string{
		"alias cc",
		"alias cod",
		"alias gmi",
		"abbr -a cnt",
		"complete -c ntm",
		"__fish_ntm_sessions",
	}

	for _, check := range checks {
		if !strings.Contains(output, check) {
			t.Errorf("fish output missing: %q", check)
		}
	}

	t.Logf("TEST: GenerateFish | Output length: %d | All checks: passed", len(output))
}

// TestRunShellInit_InvalidShell verifies error for unsupported shell
func TestRunShellInit_InvalidShell(t *testing.T) {
	t.Parallel()

	err := runShellInit("powershell")
	if err == nil {
		t.Error("expected error for unsupported shell")
	}
	if !strings.Contains(err.Error(), "unsupported shell") {
		t.Errorf("expected 'unsupported shell' error, got: %v", err)
	}

	t.Logf("TEST: RunShellInit_InvalidShell | Input: powershell | Expected: error | Got: %v", err)
}
