package cli

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestDetectProjectLanguage(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-agents-lang-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	cases := []struct {
		name     string
		marker   string
		expected string
	}{
		{"go", "go.mod", "Go"},
		{"python", "pyproject.toml", "Python"},
		{"node", "package.json", "Node"},
		{"rust", "Cargo.toml", "Rust"},
	}

	for _, tc := range cases {
		dir := filepath.Join(tmpDir, tc.name)
		if err := os.MkdirAll(dir, 0755); err != nil {
			t.Fatalf("failed to create dir %s: %v", dir, err)
		}
		if err := os.WriteFile(filepath.Join(dir, tc.marker), []byte("test"), 0644); err != nil {
			t.Fatalf("failed to write marker %s: %v", tc.marker, err)
		}

		lang := detectProjectLanguage(dir)
		if lang.Name != tc.expected {
			t.Errorf("detectProjectLanguage(%s) = %s, want %s", tc.name, lang.Name, tc.expected)
		}
	}
}

func TestRenderAgentsTemplateIncludesLanguage(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-agents-render-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	if err := os.WriteFile(filepath.Join(tmpDir, "go.mod"), []byte("module example.com/test"), 0644); err != nil {
		t.Fatalf("failed to write go.mod: %v", err)
	}

	content, err := renderAgentsTemplate(tmpDir)
	if err != nil {
		t.Fatalf("renderAgentsTemplate failed: %v", err)
	}

	if !strings.Contains(content, "Language: Go") {
		t.Errorf("expected language line in template")
	}
	if !strings.Contains(content, "go test ./...") {
		t.Errorf("expected Go rules in template")
	}
}

func TestWriteAgentsFileRespectsForce(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-agents-write-*")
	if err != nil {
		t.Fatalf("failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	created, err := writeAgentsFile(tmpDir, false)
	if err != nil {
		t.Fatalf("writeAgentsFile failed: %v", err)
	}
	if !created {
		t.Fatalf("expected AGENTS.md to be created")
	}

	path := filepath.Join(tmpDir, "AGENTS.md")
	if !fileExists(path) {
		t.Fatalf("AGENTS.md should exist")
	}

	custom := []byte("custom rules")
	if err := os.WriteFile(path, custom, 0644); err != nil {
		t.Fatalf("failed to overwrite AGENTS.md: %v", err)
	}

	created, err = writeAgentsFile(tmpDir, false)
	if err != nil {
		t.Fatalf("writeAgentsFile second run failed: %v", err)
	}
	if created {
		t.Fatalf("expected AGENTS.md to remain unchanged without force")
	}

	content, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("failed to read AGENTS.md: %v", err)
	}
	if string(content) != string(custom) {
		t.Fatalf("expected AGENTS.md to be unchanged without force")
	}

	created, err = writeAgentsFile(tmpDir, true)
	if err != nil {
		t.Fatalf("writeAgentsFile force run failed: %v", err)
	}
	if !created {
		t.Fatalf("expected AGENTS.md to be overwritten with force")
	}

	content, err = os.ReadFile(path)
	if err != nil {
		t.Fatalf("failed to read AGENTS.md after force: %v", err)
	}
	if strings.Contains(string(content), "custom rules") {
		t.Fatalf("expected AGENTS.md to be overwritten with generated content")
	}
}
