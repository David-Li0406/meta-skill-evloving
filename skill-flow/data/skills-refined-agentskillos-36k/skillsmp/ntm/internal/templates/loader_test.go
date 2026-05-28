package templates

import (
	"os"
	"path/filepath"
	"testing"
)

func TestNewLoader_RespectsProjectTemplatesDir(t *testing.T) {
	root := t.TempDir()

	ntmDir := filepath.Join(root, ".ntm")
	if err := os.MkdirAll(filepath.Join(ntmDir, "mytemplates"), 0755); err != nil {
		t.Fatalf("MkdirAll failed: %v", err)
	}
	if err := os.WriteFile(filepath.Join(ntmDir, "config.toml"), []byte("[templates]\ndir = \"mytemplates\"\n"), 0644); err != nil {
		t.Fatalf("WriteFile(config) failed: %v", err)
	}

	templatePath := filepath.Join(ntmDir, "mytemplates", "hello.md")
	if err := os.WriteFile(templatePath, []byte("hello\n"), 0644); err != nil {
		t.Fatalf("WriteFile(template) failed: %v", err)
	}

	subdir := filepath.Join(root, "sub", "dir")
	if err := os.MkdirAll(subdir, 0755); err != nil {
		t.Fatalf("MkdirAll(subdir) failed: %v", err)
	}

	wd, err := os.Getwd()
	if err != nil {
		t.Fatalf("Getwd failed: %v", err)
	}
	t.Cleanup(func() { _ = os.Chdir(wd) })
	if err := os.Chdir(subdir); err != nil {
		t.Fatalf("Chdir failed: %v", err)
	}

	loader := NewLoader()
	tmpl, err := loader.Load("hello")
	if err != nil {
		t.Fatalf("Load failed: %v", err)
	}

	if tmpl.Source != SourceProject {
		t.Fatalf("expected SourceProject, got %s", tmpl.Source.String())
	}
	// Resolve symlinks for comparison (macOS /var -> /private/var)
	expectedPath, err := filepath.EvalSymlinks(templatePath)
	if err != nil {
		t.Fatalf("EvalSymlinks(expected) failed: %v", err)
	}
	gotPath, err := filepath.EvalSymlinks(tmpl.SourcePath)
	if err != nil {
		t.Fatalf("EvalSymlinks(got) failed: %v", err)
	}
	if gotPath != expectedPath {
		t.Fatalf("expected %s, got %s", expectedPath, gotPath)
	}
}

func TestNewLoader_IgnoresTemplateDirTraversal(t *testing.T) {
	root := t.TempDir()

	ntmDir := filepath.Join(root, ".ntm")
	if err := os.MkdirAll(filepath.Join(ntmDir, "templates"), 0755); err != nil {
		t.Fatalf("MkdirAll failed: %v", err)
	}
	if err := os.WriteFile(filepath.Join(ntmDir, "config.toml"), []byte("[templates]\ndir = \"../evil\"\n"), 0644); err != nil {
		t.Fatalf("WriteFile(config) failed: %v", err)
	}

	templatePath := filepath.Join(ntmDir, "templates", "hello.md")
	if err := os.WriteFile(templatePath, []byte("hello\n"), 0644); err != nil {
		t.Fatalf("WriteFile(template) failed: %v", err)
	}

	subdir := filepath.Join(root, "sub")
	if err := os.MkdirAll(subdir, 0755); err != nil {
		t.Fatalf("MkdirAll(subdir) failed: %v", err)
	}

	wd, err := os.Getwd()
	if err != nil {
		t.Fatalf("Getwd failed: %v", err)
	}
	t.Cleanup(func() { _ = os.Chdir(wd) })
	if err := os.Chdir(subdir); err != nil {
		t.Fatalf("Chdir failed: %v", err)
	}

	loader := NewLoader()
	tmpl, err := loader.Load("hello")
	if err != nil {
		t.Fatalf("Load failed: %v", err)
	}

	if tmpl.Source != SourceProject {
		t.Fatalf("expected SourceProject, got %s", tmpl.Source.String())
	}
	// Resolve symlinks for comparison (macOS /var -> /private/var)
	expectedPath, err := filepath.EvalSymlinks(templatePath)
	if err != nil {
		t.Fatalf("EvalSymlinks(expected) failed: %v", err)
	}
	gotPath, err := filepath.EvalSymlinks(tmpl.SourcePath)
	if err != nil {
		t.Fatalf("EvalSymlinks(got) failed: %v", err)
	}
	if gotPath != expectedPath {
		t.Fatalf("expected %s, got %s", expectedPath, gotPath)
	}
}
