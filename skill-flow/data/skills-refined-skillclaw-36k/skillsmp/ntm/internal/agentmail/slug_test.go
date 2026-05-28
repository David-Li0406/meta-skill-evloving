package agentmail

import "testing"

func TestProjectSlugFromPath(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"/Users/jemanuel/projects/ntm", "ntm"},
		{"/home/user/code/my-project", "my-project"},
		{"/var/www/html/site_v1", "site_v1"},
		{"/tmp/test project", "test_project"},
		{"/path/to/UPPERCASE", "uppercase"},
		{"/path/to/mixed-CASE_project", "mixed-case_project"},
		{"/root", "root"},
		{".", "root"},
		{"/", "root"},
		{"", ""},
		{"/path/with/!@#$%^&*()", ""}, // All invalid chars
		{"/path/to/valid-123_ok", "valid-123_ok"},
		{"relative/path", "path"},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := ProjectSlugFromPath(tt.input)
			if got != tt.expected {
				t.Errorf("ProjectSlugFromPath(%q) = %q; want %q", tt.input, got, tt.expected)
			}
		})
	}
}
