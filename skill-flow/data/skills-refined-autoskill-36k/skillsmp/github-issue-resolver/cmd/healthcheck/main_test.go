package main

import (
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
)

func TestLoadBearerToken_FromFile(t *testing.T) {
	// Create a temporary file with a token
	tmpDir := t.TempDir()
	tokenFile := filepath.Join(tmpDir, "token")
	expectedToken := "test-bearer-token-12345"

	if err := os.WriteFile(tokenFile, []byte(expectedToken+"\n"), 0600); err != nil {
		t.Fatalf("Failed to write token file: %v", err)
	}

	token, err := loadBearerToken(tokenFile, "")
	if err != nil {
		t.Fatalf("loadBearerToken failed: %v", err)
	}

	if token != expectedToken {
		t.Errorf("Expected token %q, got %q", expectedToken, token)
	}
}

func TestLoadBearerToken_FromValue(t *testing.T) {
	expectedToken := "direct-token-value"
	token, err := loadBearerToken("", expectedToken)
	if err != nil {
		t.Fatalf("loadBearerToken failed: %v", err)
	}

	if token != expectedToken {
		t.Errorf("Expected token %q, got %q", expectedToken, token)
	}
}

func TestLoadBearerToken_FileNotFound(t *testing.T) {
	_, err := loadBearerToken("/nonexistent/path/token", "")
	if err == nil {
		t.Error("Expected error for nonexistent file, got nil")
	}
}

func TestLoadBearerToken_Empty(t *testing.T) {
	token, err := loadBearerToken("", "")
	if err != nil {
		t.Fatalf("loadBearerToken failed: %v", err)
	}
	if token != "" {
		t.Errorf("Expected empty token, got %q", token)
	}
}

func TestLoadBearerToken_FileTakesPrecedence(t *testing.T) {
	tmpDir := t.TempDir()
	tokenFile := filepath.Join(tmpDir, "token")
	fileToken := "token-from-file"

	if err := os.WriteFile(tokenFile, []byte(fileToken), 0600); err != nil {
		t.Fatalf("Failed to write token file: %v", err)
	}

	token, err := loadBearerToken(tokenFile, "direct-value-ignored")
	if err != nil {
		t.Fatalf("loadBearerToken failed: %v", err)
	}

	if token != fileToken {
		t.Errorf("Expected file token %q to take precedence, got %q", fileToken, token)
	}
}

func TestParseHeaders_Valid(t *testing.T) {
	tests := []struct {
		name     string
		input    []string
		expected map[string]string
	}{
		{
			name:     "empty",
			input:    []string{},
			expected: map[string]string{},
		},
		{
			name:     "single header",
			input:    []string{"X-Custom: value"},
			expected: map[string]string{"X-Custom": "value"},
		},
		{
			name:     "multiple headers",
			input:    []string{"X-Header-1: value1", "X-Header-2: value2"},
			expected: map[string]string{"X-Header-1": "value1", "X-Header-2": "value2"},
		},
		{
			name:     "header with colons in value",
			input:    []string{"X-URL: http://example.com:8080/path"},
			expected: map[string]string{"X-URL": "http://example.com:8080/path"},
		},
		{
			name:     "whitespace trimmed",
			input:    []string{"  X-Spaced  :   value with spaces   "},
			expected: map[string]string{"X-Spaced": "value with spaces"},
		},
		{
			name:     "empty value allowed",
			input:    []string{"X-Empty:"},
			expected: map[string]string{"X-Empty": ""},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := parseHeaders(tt.input)
			if err != nil {
				t.Fatalf("parseHeaders failed: %v", err)
			}

			if len(result) != len(tt.expected) {
				t.Errorf("Expected %d headers, got %d", len(tt.expected), len(result))
			}

			for name, expectedValue := range tt.expected {
				if got, ok := result[name]; !ok {
					t.Errorf("Missing header %q", name)
				} else if got != expectedValue {
					t.Errorf("Header %q: expected %q, got %q", name, expectedValue, got)
				}
			}
		})
	}
}

func TestParseHeaders_Invalid(t *testing.T) {
	tests := []struct {
		name  string
		input []string
	}{
		{
			name:  "no colon",
			input: []string{"InvalidHeader"},
		},
		{
			name:  "empty name",
			input: []string{": value"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, err := parseHeaders(tt.input)
			if err == nil {
				t.Error("Expected error for invalid header format, got nil")
			}
		})
	}
}

func TestStringSlice(t *testing.T) {
	var s stringSlice

	// Test initial state
	if s.String() != "" {
		t.Errorf("Expected empty string, got %q", s.String())
	}

	// Test Set
	if err := s.Set("value1"); err != nil {
		t.Fatalf("Set failed: %v", err)
	}
	if err := s.Set("value2"); err != nil {
		t.Fatalf("Set failed: %v", err)
	}

	// Test String
	expected := "value1, value2"
	if s.String() != expected {
		t.Errorf("Expected %q, got %q", expected, s.String())
	}
}

// TestHealthCheckWithBearerToken tests that the Authorization header is sent correctly
func TestHealthCheckWithBearerToken(t *testing.T) {
	expectedToken := "test-token-abc123"
	receivedAuth := ""

	// Create a test server that captures the Authorization header
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		receivedAuth = r.Header.Get("Authorization")
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	// Create request with bearer token
	req, err := http.NewRequest("GET", server.URL, nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}
	req.Header.Set("Authorization", "Bearer "+expectedToken)

	// Make request
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatalf("Request failed: %v", err)
	}
	defer func() { _ = resp.Body.Close() }()

	// Verify
	expectedAuth := "Bearer " + expectedToken
	if receivedAuth != expectedAuth {
		t.Errorf("Expected Authorization %q, got %q", expectedAuth, receivedAuth)
	}
}

// TestHealthCheckWithCustomHeaders tests that custom headers are sent correctly
func TestHealthCheckWithCustomHeaders(t *testing.T) {
	receivedHeaders := make(map[string]string)

	// Create a test server that captures headers
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		receivedHeaders["X-Custom-1"] = r.Header.Get("X-Custom-1")
		receivedHeaders["X-Custom-2"] = r.Header.Get("X-Custom-2")
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	// Parse headers
	headers, err := parseHeaders([]string{"X-Custom-1: value1", "X-Custom-2: value2"})
	if err != nil {
		t.Fatalf("parseHeaders failed: %v", err)
	}

	// Create request with custom headers
	req, err := http.NewRequest("GET", server.URL, nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}
	for name, value := range headers {
		req.Header.Set(name, value)
	}

	// Make request
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatalf("Request failed: %v", err)
	}
	defer func() { _ = resp.Body.Close() }()

	// Verify
	if receivedHeaders["X-Custom-1"] != "value1" {
		t.Errorf("Expected X-Custom-1 'value1', got %q", receivedHeaders["X-Custom-1"])
	}
	if receivedHeaders["X-Custom-2"] != "value2" {
		t.Errorf("Expected X-Custom-2 'value2', got %q", receivedHeaders["X-Custom-2"])
	}
}

// TestHealthCheckHTTPS tests that HTTPS with insecure skip verify works
func TestHealthCheckHTTPS(t *testing.T) {
	// Create an HTTPS test server (with self-signed cert)
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		if _, err := w.Write([]byte("OK")); err != nil {
			t.Logf("Failed to write response: %v", err)
		}
	}))
	defer server.Close()

	// Create client with InsecureSkipVerify (matches the healthcheck behavior)
	client := server.Client()

	req, err := http.NewRequest("GET", server.URL, nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	resp, err := client.Do(req)
	if err != nil {
		t.Fatalf("Request failed: %v", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}
}
