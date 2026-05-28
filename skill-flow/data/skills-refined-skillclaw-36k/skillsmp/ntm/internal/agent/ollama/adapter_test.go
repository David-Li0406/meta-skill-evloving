package ollama

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// mockOllamaServer creates a test server that mimics Ollama API
func mockOllamaServer(t *testing.T, handlers map[string]http.HandlerFunc) *httptest.Server {
	t.Helper()
	return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if handler, ok := handlers[r.URL.Path]; ok {
			handler(w, r)
			return
		}
		http.NotFound(w, r)
	}))
}

func TestNewAdapter(t *testing.T) {
	a := NewAdapter()
	if a == nil {
		t.Fatal("NewAdapter returned nil")
	}
	if a.client == nil {
		t.Error("client should be initialized")
	}
	if a.connected {
		t.Error("should not be connected initially")
	}
}

func TestConnect(t *testing.T) {
	tests := []struct {
		name        string
		serverFunc  func(w http.ResponseWriter, r *http.Request)
		wantErr     bool
		errContains string
	}{
		{
			name: "successful connection",
			serverFunc: func(w http.ResponseWriter, r *http.Request) {
				json.NewEncoder(w).Encode(ollamaTagsResponse{Models: []ollamaModel{}})
			},
			wantErr: false,
		},
		{
			name: "server error",
			serverFunc: func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(http.StatusInternalServerError)
			},
			wantErr:     true,
			errContains: "server returned 500",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			server := mockOllamaServer(t, map[string]http.HandlerFunc{
				"/api/tags": tt.serverFunc,
			})
			defer server.Close()

			a := NewAdapter()
			err := a.Connect(server.URL)

			if tt.wantErr {
				if err == nil {
					t.Error("expected error but got nil")
				} else if tt.errContains != "" && !strings.Contains(err.Error(), tt.errContains) {
					t.Errorf("error should contain %q, got %q", tt.errContains, err.Error())
				}
			} else {
				if err != nil {
					t.Errorf("unexpected error: %v", err)
				}
				if !a.IsConnected() {
					t.Error("should be connected after successful Connect")
				}
			}
		})
	}
}

func TestConnect_InvalidHost(t *testing.T) {
	a := NewAdapter()
	err := a.Connect("http://localhost:99999")
	if err == nil {
		t.Error("expected error for invalid host")
	}
}

func TestConnect_NormalizesHost(t *testing.T) {
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{Models: []ollamaModel{}})
		},
	})
	defer server.Close()

	// Remove http:// prefix to test normalization
	host := strings.TrimPrefix(server.URL, "http://")

	a := NewAdapter()
	if err := a.Connect(host); err != nil {
		t.Errorf("failed to connect with normalized host: %v", err)
	}
}

func TestListModels(t *testing.T) {
	testModels := []ollamaModel{
		{
			Name:       "llama3:latest",
			Size:       4500000000,
			Digest:     "abc123",
			ModifiedAt: time.Now(),
			Details: ModelDetails{
				Family:        "llama",
				ParameterSize: "8B",
			},
		},
		{
			Name:       "mistral:7b",
			Size:       3800000000,
			Digest:     "def456",
			ModifiedAt: time.Now(),
		},
	}

	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{Models: testModels})
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)
	ctx := context.Background()

	models, err := a.ListModels(ctx)
	if err != nil {
		t.Fatalf("ListModels failed: %v", err)
	}

	if len(models) != len(testModels) {
		t.Errorf("expected %d models, got %d", len(testModels), len(models))
	}

	if models[0].Name != "llama3:latest" {
		t.Errorf("expected model name 'llama3:latest', got %q", models[0].Name)
	}

	if models[0].Details.Family != "llama" {
		t.Errorf("expected family 'llama', got %q", models[0].Details.Family)
	}
}

func TestListModels_NotConnected(t *testing.T) {
	a := NewAdapter()
	_, err := a.ListModels(context.Background())
	if err != ErrNotConnected {
		t.Errorf("expected ErrNotConnected, got %v", err)
	}
}

func TestSendPrompt(t *testing.T) {
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
		"/api/generate": func(w http.ResponseWriter, r *http.Request) {
			var req ollamaGenerateRequest
			json.NewDecoder(r.Body).Decode(&req)

			if req.Model != "llama3" {
				t.Errorf("expected model 'llama3', got %q", req.Model)
			}
			if req.Stream {
				t.Error("expected stream=false for SendPrompt")
			}

			json.NewEncoder(w).Encode(ollamaGenerateResponse{
				Model:           "llama3",
				Response:        "Hello! How can I help you?",
				Done:            true,
				PromptEvalCount: 10,
				EvalCount:       8,
				TotalDuration:   1000000000, // 1 second
			})
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)
	a.SetModel("llama3")

	resp, err := a.SendPrompt(context.Background(), "Hello")
	if err != nil {
		t.Fatalf("SendPrompt failed: %v", err)
	}

	if resp.Content != "Hello! How can I help you?" {
		t.Errorf("unexpected response content: %q", resp.Content)
	}
	if resp.PromptTokens != 10 {
		t.Errorf("expected 10 prompt tokens, got %d", resp.PromptTokens)
	}
	if resp.OutputTokens != 8 {
		t.Errorf("expected 8 output tokens, got %d", resp.OutputTokens)
	}
	if !resp.Done {
		t.Error("expected Done=true")
	}
}

func TestSendPrompt_NoModel(t *testing.T) {
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)
	// Don't set model

	_, err := a.SendPrompt(context.Background(), "Hello")
	if err == nil {
		t.Error("expected error when no model set")
	}
	if !strings.Contains(err.Error(), "no model set") {
		t.Errorf("error should mention 'no model set', got %q", err.Error())
	}
}

func TestStreamResponse(t *testing.T) {
	tokens := []string{"Hello", " ", "world", "!"}

	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
		"/api/generate": func(w http.ResponseWriter, r *http.Request) {
			var req ollamaGenerateRequest
			json.NewDecoder(r.Body).Decode(&req)

			if !req.Stream {
				t.Error("expected stream=true for StreamResponse")
			}

			flusher, ok := w.(http.Flusher)
			if !ok {
				t.Fatal("ResponseWriter doesn't support flushing")
			}

			for i, token := range tokens {
				resp := ollamaGenerateResponse{
					Model:    "llama3",
					Response: token,
					Done:     i == len(tokens)-1,
				}
				json.NewEncoder(w).Encode(resp)
				flusher.Flush()
			}
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)
	a.SetModel("llama3")

	tokenChan, err := a.StreamResponse(context.Background(), "Hello")
	if err != nil {
		t.Fatalf("StreamResponse failed: %v", err)
	}

	var received []string
	for token := range tokenChan {
		if token.Error != nil {
			t.Errorf("unexpected token error: %v", token.Error)
			continue
		}
		received = append(received, token.Content)
	}

	if len(received) != len(tokens) {
		t.Errorf("expected %d tokens, got %d", len(tokens), len(received))
	}

	for i, expected := range tokens {
		if i < len(received) && received[i] != expected {
			t.Errorf("token %d: expected %q, got %q", i, expected, received[i])
		}
	}
}

func TestStreamResponse_ContextCancellation(t *testing.T) {
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
		"/api/generate": func(w http.ResponseWriter, r *http.Request) {
			flusher, _ := w.(http.Flusher)

			// Send tokens slowly - the client should cancel before we finish
			for i := 0; i < 100; i++ {
				select {
				case <-r.Context().Done():
					return
				default:
				}
				json.NewEncoder(w).Encode(ollamaGenerateResponse{
					Response: fmt.Sprintf("token%d", i),
					Done:     false,
				})
				flusher.Flush()
				time.Sleep(50 * time.Millisecond)
			}
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)
	a.SetModel("llama3")

	ctx, cancel := context.WithTimeout(context.Background(), 150*time.Millisecond)
	defer cancel()

	tokenChan, err := a.StreamResponse(ctx, "Hello")
	if err != nil {
		t.Fatalf("StreamResponse failed: %v", err)
	}

	var tokenCount int
	var gotCancellation bool
	for token := range tokenChan {
		tokenCount++
		if token.Error != nil {
			// Accept any error as cancellation-related since the stream was interrupted
			gotCancellation = true
			break
		}
		if token.Done {
			break
		}
	}

	// Either we got a cancellation error, or the stream was truncated (fewer than 100 tokens)
	// Both indicate the context cancellation worked
	if !gotCancellation && tokenCount >= 100 {
		t.Error("expected either cancellation error or truncated stream, but got all 100 tokens")
	}
}

func TestPullModel(t *testing.T) {
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
		"/api/pull": func(w http.ResponseWriter, r *http.Request) {
			var req ollamaPullRequest
			json.NewDecoder(r.Body).Decode(&req)

			if req.Name != "mistral:latest" {
				t.Errorf("expected model 'mistral:latest', got %q", req.Name)
			}

			flusher, _ := w.(http.Flusher)

			// Simulate pull progress
			statuses := []string{
				"pulling manifest",
				"downloading sha256:abc123",
				"verifying sha256:abc123",
				"success",
			}

			for _, status := range statuses {
				json.NewEncoder(w).Encode(ollamaPullResponse{Status: status})
				flusher.Flush()
			}
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)

	err := a.PullModel(context.Background(), "mistral:latest")
	if err != nil {
		t.Errorf("PullModel failed: %v", err)
	}
}

func TestPullModel_NotConnected(t *testing.T) {
	a := NewAdapter()
	err := a.PullModel(context.Background(), "mistral:latest")
	if err != ErrNotConnected {
		t.Errorf("expected ErrNotConnected, got %v", err)
	}
}

func TestErrorClassification(t *testing.T) {
	tests := []struct {
		name        string
		statusCode  int
		body        string
		wantErr     error
		errContains string
	}{
		{
			name:       "model not found",
			statusCode: http.StatusNotFound,
			body:       `{"error": "model 'nonexistent' not found"}`,
			wantErr:    ErrModelNotFound,
		},
		{
			name:       "context length exceeded",
			statusCode: http.StatusBadRequest,
			body:       `{"error": "context length exceeded"}`,
			wantErr:    ErrContextLengthExceeded,
		},
		{
			name:        "GPU memory exhausted",
			statusCode:  http.StatusInternalServerError,
			body:        `{"error": "CUDA out of memory"}`,
			wantErr:     ErrGPUMemoryExhausted,
			errContains: "CUDA out of memory",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			server := mockOllamaServer(t, map[string]http.HandlerFunc{
				"/api/tags": func(w http.ResponseWriter, r *http.Request) {
					json.NewEncoder(w).Encode(ollamaTagsResponse{})
				},
				"/api/generate": func(w http.ResponseWriter, r *http.Request) {
					w.WriteHeader(tt.statusCode)
					w.Write([]byte(tt.body))
				},
			})
			defer server.Close()

			a := NewAdapterWithHost(server.URL)
			a.SetModel("test")

			_, err := a.SendPrompt(context.Background(), "test")
			if err == nil {
				t.Fatal("expected error")
			}

			if tt.wantErr != nil && !strings.Contains(err.Error(), tt.wantErr.Error()) {
				t.Errorf("expected error to wrap %v, got %v", tt.wantErr, err)
			}

			if tt.errContains != "" && !strings.Contains(err.Error(), tt.errContains) {
				t.Errorf("error should contain %q, got %q", tt.errContains, err.Error())
			}
		})
	}
}

func TestClose(t *testing.T) {
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)
	if !a.IsConnected() {
		t.Fatal("should be connected")
	}

	if err := a.Close(); err != nil {
		t.Errorf("Close failed: %v", err)
	}

	if a.IsConnected() {
		t.Error("should not be connected after Close")
	}
}

func TestSetModel(t *testing.T) {
	a := NewAdapter()

	if a.GetModel() != "" {
		t.Error("model should be empty initially")
	}

	a.SetModel("llama3")
	if a.GetModel() != "llama3" {
		t.Errorf("expected model 'llama3', got %q", a.GetModel())
	}

	a.SetModel("mistral:7b")
	if a.GetModel() != "mistral:7b" {
		t.Errorf("expected model 'mistral:7b', got %q", a.GetModel())
	}
}

func TestNewAdapterFromEnv(t *testing.T) {
	// Test with custom env var
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
	})
	defer server.Close()

	t.Setenv("NTM_OLLAMA_HOST", server.URL)

	a := NewAdapterFromEnv()
	if a.Host() != server.URL {
		t.Errorf("expected host %q, got %q", server.URL, a.Host())
	}
}

func TestHost(t *testing.T) {
	server := mockOllamaServer(t, map[string]http.HandlerFunc{
		"/api/tags": func(w http.ResponseWriter, r *http.Request) {
			json.NewEncoder(w).Encode(ollamaTagsResponse{})
		},
	})
	defer server.Close()

	a := NewAdapterWithHost(server.URL)
	if a.Host() != server.URL {
		t.Errorf("expected host %q, got %q", server.URL, a.Host())
	}
}
