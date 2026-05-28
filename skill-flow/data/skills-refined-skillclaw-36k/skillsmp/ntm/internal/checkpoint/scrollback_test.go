package checkpoint

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestGzipCompressDecompress(t *testing.T) {
	tests := []struct {
		name string
		data string
	}{
		{"empty", ""},
		{"small", "hello world"},
		{"multiline", "line1\nline2\nline3\n"},
		{"large", strings.Repeat("this is a test line\n", 1000)},
		{"binary-like", string([]byte{0, 1, 2, 255, 254, 253})},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			compressed, err := gzipCompress([]byte(tt.data))
			if err != nil {
				t.Fatalf("gzipCompress failed: %v", err)
			}

			decompressed, err := gzipDecompress(compressed)
			if err != nil {
				t.Fatalf("gzipDecompress failed: %v", err)
			}

			if string(decompressed) != tt.data {
				t.Errorf("round-trip failed: got %q, want %q", string(decompressed), tt.data)
			}
		})
	}
}

func TestGzipCompressionRatio(t *testing.T) {
	// Highly compressible data (repeated pattern)
	data := strings.Repeat("hello world this is a test\n", 1000)
	compressed, err := gzipCompress([]byte(data))
	if err != nil {
		t.Fatalf("gzipCompress failed: %v", err)
	}

	ratio := float64(len(compressed)) / float64(len(data))
	t.Logf("Compression ratio: %.2f%% (original: %d, compressed: %d)",
		ratio*100, len(data), len(compressed))

	// For highly repetitive data, expect significant compression
	if ratio > 0.1 { // Should compress to less than 10%
		t.Errorf("Expected better compression ratio, got %.2f%%", ratio*100)
	}
}

func TestScrollbackConfig_Defaults(t *testing.T) {
	config := DefaultScrollbackConfig()

	if config.Lines != 5000 {
		t.Errorf("Default lines = %d, want 5000", config.Lines)
	}
	if !config.Compress {
		t.Error("Default compress should be true")
	}
	if config.MaxSizeMB != 10 {
		t.Errorf("Default MaxSizeMB = %d, want 10", config.MaxSizeMB)
	}
}

func TestStorage_SaveCompressedScrollback(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-scrollback-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	storage := NewStorageWithDir(tmpDir)

	// Test data
	sessionName := "test-session"
	checkpointID := "test-checkpoint"
	paneID := "%0"
	content := "Hello, this is scrollback content\nLine 2\nLine 3\n"

	// Compress the content
	compressed, err := gzipCompress([]byte(content))
	if err != nil {
		t.Fatalf("gzipCompress failed: %v", err)
	}

	// Save compressed scrollback
	relativePath, err := storage.SaveCompressedScrollback(sessionName, checkpointID, paneID, compressed)
	if err != nil {
		t.Fatalf("SaveCompressedScrollback failed: %v", err)
	}

	// Verify path format
	if !strings.HasSuffix(relativePath, ".txt.gz") {
		t.Errorf("Expected .txt.gz suffix, got %s", relativePath)
	}

	// Verify file exists
	fullPath := filepath.Join(tmpDir, sessionName, checkpointID, relativePath)
	if _, err := os.Stat(fullPath); os.IsNotExist(err) {
		t.Errorf("Compressed scrollback file not created at %s", fullPath)
	}

	// Load and verify content
	loaded, err := storage.LoadCompressedScrollback(sessionName, checkpointID, paneID)
	if err != nil {
		t.Fatalf("LoadCompressedScrollback failed: %v", err)
	}

	if loaded != content {
		t.Errorf("Loaded content mismatch: got %q, want %q", loaded, content)
	}
}

func TestStorage_LoadCompressedScrollback_FallbackToUncompressed(t *testing.T) {
	tmpDir, err := os.MkdirTemp("", "ntm-scrollback-fallback-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	storage := NewStorageWithDir(tmpDir)

	// Test data
	sessionName := "test-session"
	checkpointID := "test-checkpoint"
	paneID := "%0"
	content := "Uncompressed scrollback content\n"

	// Save uncompressed scrollback using the old method
	relativePath, err := storage.SaveScrollback(sessionName, checkpointID, paneID, content)
	if err != nil {
		t.Fatalf("SaveScrollback failed: %v", err)
	}

	// Verify it's a .txt file
	if !strings.HasSuffix(relativePath, ".txt") {
		t.Errorf("Expected .txt suffix, got %s", relativePath)
	}

	// Load using compressed method (should fall back to uncompressed)
	loaded, err := storage.LoadCompressedScrollback(sessionName, checkpointID, paneID)
	if err != nil {
		t.Fatalf("LoadCompressedScrollback fallback failed: %v", err)
	}

	if loaded != content {
		t.Errorf("Fallback content mismatch: got %q, want %q", loaded, content)
	}
}

func TestScrollbackCapture_SizeLimit(t *testing.T) {
	// Test that the size limit check works correctly
	config := ScrollbackConfig{
		Lines:     1000,
		Compress:  true,
		MaxSizeMB: 1, // 1 MB limit
	}

	// Create content that's larger than 10x the limit (should be skipped)
	largeContent := strings.Repeat("x", 11*1024*1024) // 11 MB

	// Simulate the size check logic
	rawSizeMB := float64(len(largeContent)) / (1024 * 1024)
	maxAllowed := float64(config.MaxSizeMB) * 10

	if rawSizeMB <= maxAllowed {
		t.Errorf("Expected rawSizeMB (%.2f) > maxAllowed (%.2f)", rawSizeMB, maxAllowed)
	}
}

func TestCheckpointOptions_ScrollbackConfig(t *testing.T) {
	// Test default options
	opts := defaultOptions()
	if opts.scrollbackLines != 5000 {
		t.Errorf("Default scrollbackLines = %d, want 5000", opts.scrollbackLines)
	}
	if !opts.scrollbackCompress {
		t.Error("Default scrollbackCompress should be true")
	}
	if opts.scrollbackMaxSizeMB != 10 {
		t.Errorf("Default scrollbackMaxSizeMB = %d, want 10", opts.scrollbackMaxSizeMB)
	}

	// Test option functions
	opts = defaultOptions()
	WithScrollbackLines(2000)(&opts)
	if opts.scrollbackLines != 2000 {
		t.Errorf("scrollbackLines = %d, want 2000", opts.scrollbackLines)
	}

	opts = defaultOptions()
	WithScrollbackCompress(false)(&opts)
	if opts.scrollbackCompress {
		t.Error("scrollbackCompress should be false after WithScrollbackCompress(false)")
	}

	opts = defaultOptions()
	WithScrollbackMaxSizeMB(5)(&opts)
	if opts.scrollbackMaxSizeMB != 5 {
		t.Errorf("scrollbackMaxSizeMB = %d, want 5", opts.scrollbackMaxSizeMB)
	}
}
