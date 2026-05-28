package util

import (
	"strings"
	"testing"
)

func TestExtractNewOutput(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name   string
		before string
		after  string
		want   string
	}{
		{
			name:   "empty before returns all after",
			before: "",
			after:  "hello world",
			want:   "hello world",
		},
		{
			name:   "empty after returns empty",
			before: "hello",
			after:  "",
			want:   "",
		},
		{
			name:   "both empty",
			before: "",
			after:  "",
			want:   "",
		},
		{
			name:   "simple append",
			before: "hello",
			after:  "hello world",
			want:   " world",
		},
		{
			name:   "exact match returns empty",
			before: "hello",
			after:  "hello",
			want:   "",
		},
		{
			name:   "scrolled output with overlap",
			before: "line1\nline2\nline3",
			after:  "line2\nline3\nline4",
			want:   "\nline4",
		},
		{
			name:   "no overlap returns all",
			before: "abc",
			after:  "xyz",
			want:   "xyz",
		},
		{
			name:   "partial overlap at end",
			before: "abcdef",
			after:  "defghi",
			want:   "ghi",
		},
		{
			name:   "multiline overlap",
			before: "first\nsecond\nthird",
			after:  "second\nthird\nfourth",
			want:   "\nfourth",
		},
		{
			name:   "before longer than after with overlap",
			before: "this is a very long before string that ends with: overlap",
			after:  "overlap and new content",
			want:   " and new content",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := ExtractNewOutput(tt.before, tt.after)
			if got != tt.want {
				t.Errorf("ExtractNewOutput(%q, %q) = %q, want %q", tt.before, tt.after, got, tt.want)
			}
		})
	}
}

func TestExtractNewOutput_LargeOverlap(t *testing.T) {
	t.Parallel()

	// Test with overlap larger than chunkSize (40)
	overlap := strings.Repeat("x", 50)
	before := "prefix" + overlap
	after := overlap + "suffix"

	got := ExtractNewOutput(before, after)
	want := "suffix"

	if got != want {
		t.Errorf("ExtractNewOutput with 50-char overlap = %q, want %q", got, want)
	}
}

func TestExtractNewOutput_SmallOverlap(t *testing.T) {
	t.Parallel()

	// Test with overlap smaller than chunkSize but after > chunkSize
	overlap := "xyz"                           // 3 char overlap
	before := "prefix" + overlap               // "prefixyz" (8 chars, ends with "xyz")
	after := overlap + strings.Repeat("b", 47) // "xyz" + 47 b's = 50 chars, starts with "xyz"

	got := ExtractNewOutput(before, after)
	want := strings.Repeat("b", 47)

	if got != want {
		t.Errorf("ExtractNewOutput with 3-char overlap, long after = %q, want %q", got, want)
	}
}

func TestTruncate(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		input string
		n     int
		want  string
	}{
		{"empty string", "", 10, ""},
		{"n is zero", "hello", 0, ""},
		{"n is negative", "hello", -5, ""},
		{"string shorter than n", "hi", 10, "hi"},
		{"string equals n", "hello", 5, "hello"},
		{"truncate with ellipsis", "hello world", 8, "hello..."},
		{"truncate minimal ellipsis", "hello world", 5, "he..."},
		{"n too small for ellipsis", "hello", 2, "he"},
		{"n equals 3", "hello", 3, "hel"},
		{"single char n=1", "a", 1, "a"},
		{"multi-char n=1", "hello", 1, "h"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := Truncate(tt.input, tt.n)
			if got != tt.want {
				t.Errorf("Truncate(%q, %d) = %q, want %q", tt.input, tt.n, got, tt.want)
			}
		})
	}
}

func TestTruncate_UTF8(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		input string
		n     int
		want  string
	}{
		{
			name:  "multibyte char that fits",
			input: "世界",
			n:     10,
			want:  "世界",
		},
		{
			name:  "multibyte truncated at boundary",
			input: "a世界",
			n:     4,
			want:  "a...",
		},
		{
			name:  "multibyte n too small",
			input: "世界",
			n:     2,
			want:  "", // First char is 3 bytes, can't fit in 2
		},
		{
			name:  "mixed ASCII and multibyte",
			input: "hi世界",
			n:     5,
			want:  "hi...",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := Truncate(tt.input, tt.n)
			if got != tt.want {
				t.Errorf("Truncate(%q, %d) = %q, want %q", tt.input, tt.n, got, tt.want)
			}
		})
	}
}

func TestSanitizeFilename(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		input string
		want  string
	}{
		{"simple", "hello", "hello"},
		{"with spaces", "hello world", "hello_world"},
		{"with slashes", "path/to/file", "path-to-file"},
		{"with backslashes", "path\\to\\file", "path-to-file"},
		{"with special chars", "file:name?.txt", "file-name-_txt"},
		{"with dots", "my.file.name", "my_file_name"},
		{"with leading space", "  trimmed  ", "trimmed"},
		{"empty string", "", ""},
		{"long string truncated", strings.Repeat("a", 100), strings.Repeat("a", 50)},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got := SanitizeFilename(tt.input)
			if got != tt.want {
				t.Errorf("SanitizeFilename(%q) = %q, want %q", tt.input, got, tt.want)
			}
		})
	}
}
