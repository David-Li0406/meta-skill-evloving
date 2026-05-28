package prompt

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/codeblock"
)

func TestParseFileSpec(t *testing.T) {
	tests := []struct {
		input     string
		wantPath  string
		wantStart int
		wantEnd   int
	}{
		{"file.go", "file.go", 0, 0},
		{"src/auth.py", "src/auth.py", 0, 0},
		{"file.go:10-50", "file.go", 10, 50},
		{"file.go:10-", "file.go", 10, 0},
		{"file.go:-50", "file.go", 0, 50},
		{"file.go:25", "file.go", 25, 25},
		{"/abs/path/file.go:1-10", "/abs/path/file.go", 1, 10},
		{"file.go:abc-1", "file.go:abc-1", 0, 0},                 // not a line range suffix
		{`C:\proj-1\main.go`, `C:\proj-1\main.go`, 0, 0},         // Windows drive path (no range)
		{`C:\proj-1\main.go:12-34`, `C:\proj-1\main.go`, 12, 34}, // Windows drive path with range
		{`C:\proj-1\main.go:12-`, `C:\proj-1\main.go`, 12, 0},    // Windows drive path with open range
		{`C:\proj-1\main.go:-34`, `C:\proj-1\main.go`, 0, 34},    // Windows drive path with end-only range
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			spec, err := ParseFileSpec(tt.input)
			if err != nil {
				t.Fatalf("ParseFileSpec(%q) error: %v", tt.input, err)
			}
			if spec.Path != tt.wantPath {
				t.Errorf("Path = %q, want %q", spec.Path, tt.wantPath)
			}
			if spec.StartLine != tt.wantStart {
				t.Errorf("StartLine = %d, want %d", spec.StartLine, tt.wantStart)
			}
			if spec.EndLine != tt.wantEnd {
				t.Errorf("EndLine = %d, want %d", spec.EndLine, tt.wantEnd)
			}
		})
	}
}

func TestDetectLanguage(t *testing.T) {
	tests := []struct {
		path string
		want string
	}{
		{"file.go", "go"},
		{"src/auth.py", "python"},
		{"app.js", "javascript"},
		{"app.tsx", "typescript"},
		{"Makefile", "makefile"},
		{"Dockerfile", "dockerfile"},
		{"unknown.xyz", ""},
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			got := codeblock.DetectLanguage(tt.path)
			if got != tt.want {
				t.Errorf("DetectLanguage(%q) = %q, want %q", tt.path, got, tt.want)
			}
		})
	}
}

func TestInjectFiles(t *testing.T) {
	// Create temp test file
	tmpDir := t.TempDir()
	testFile := filepath.Join(tmpDir, "test.go")
	content := "package main\n\nfunc main() {\n\tfmt.Println(\"hello\")\n}"
	if err := os.WriteFile(testFile, []byte(content), 0644); err != nil {
		t.Fatal(err)
	}

	specs := []FileSpec{{Path: testFile}}
	result, err := InjectFiles(specs, "Review this code")
	if err != nil {
		t.Fatalf("InjectFiles error: %v", err)
	}

	// Check structure
	if !strings.Contains(result, "# File:") {
		t.Error("Missing file header")
	}
	if !strings.Contains(result, "```go") {
		t.Error("Missing language tag")
	}
	if !strings.Contains(result, content) {
		t.Error("Missing file content")
	}
	if !strings.Contains(result, "---\n\nReview this code") {
		t.Error("Missing prompt separator")
	}
}

func TestInjectFilesWithLineRange(t *testing.T) {
	tmpDir := t.TempDir()
	testFile := filepath.Join(tmpDir, "test.txt")
	lines := "line1\nline2\nline3\nline4\nline5\n"
	if err := os.WriteFile(testFile, []byte(lines), 0644); err != nil {
		t.Fatal(err)
	}

	specs := []FileSpec{{Path: testFile, StartLine: 2, EndLine: 4}}
	result, err := InjectFiles(specs, "Check these lines")
	if err != nil {
		t.Fatalf("InjectFiles error: %v", err)
	}

	if !strings.Contains(result, "line2") {
		t.Error("Should contain line2")
	}
	if !strings.Contains(result, "line4") {
		t.Error("Should contain line4")
	}
	if strings.Contains(result, "line1\n") {
		t.Error("Should not contain line1")
	}
	if strings.Contains(result, "line5") {
		t.Error("Should not contain line5")
	}
}

func TestIsBinary(t *testing.T) {
	tests := []struct {
		name    string
		content string
		want    bool
	}{
		{"empty", "", false},
		{"text", "Hello, World!", false},
		{"with newlines", "line1\nline2\nline3", false},
		{"with tabs", "col1\tcol2\tcol3", false},
		{"null byte", "hello\x00world", true},
		{"binary with nulls", string([]byte{0x89, 0x50, 0x4E, 0x47, 0x00, 0x00, 0x00}), true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := isBinary(tt.content)
			if got != tt.want {
				t.Errorf("isBinary() = %v, want %v", got, tt.want)
			}
		})
	}
}
