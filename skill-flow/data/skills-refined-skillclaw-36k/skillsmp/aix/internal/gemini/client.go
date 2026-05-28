package gemini

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const (
	baseURL        = "https://generativelanguage.googleapis.com/v1beta"
	defaultTimeout = 60 * time.Second

	// Conservative retry policy for transient failures (429/5xx).
	maxRetries     = 5
	initialBackoff = 500 * time.Millisecond
)

// Client is a minimal Gemini API client for embeddings.
type Client struct {
	apiKey string
	http   *http.Client
}

func NewClient(apiKey string) *Client {
	return &Client{
		apiKey: apiKey,
		http: &http.Client{
			Timeout: defaultTimeout,
			Transport: &http.Transport{
				ForceAttemptHTTP2:   true,
				MaxIdleConns:        256,
				MaxIdleConnsPerHost: 256,
				MaxConnsPerHost:     256,
				IdleConnTimeout:     90 * time.Second,
			},
		},
	}
}

type Part struct {
	Text string `json:"text,omitempty"`
}

type Content struct {
	Parts []Part `json:"parts"`
}

type EmbedContentRequest struct {
	Model   string  `json:"model"`
	Content Content `json:"content"`
}

type Embedding struct {
	Values []float64 `json:"values"`
}

type APIError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
	Status  string `json:"status"`
}

func (e *APIError) Error() string {
	return fmt.Sprintf("gemini API error %d (%s): %s", e.Code, e.Status, e.Message)
}

type EmbedContentResponse struct {
	Embedding *Embedding `json:"embedding,omitempty"`
	Error     *APIError  `json:"error,omitempty"`
}

type BatchEmbedContentsRequest struct {
	Requests []EmbedContentRequest `json:"requests"`
}

type BatchEmbedContentsResponse struct {
	Embeddings []Embedding `json:"embeddings,omitempty"`
	Error      *APIError   `json:"error,omitempty"`
}

func (c *Client) EmbedContent(ctx context.Context, req *EmbedContentRequest) (*EmbedContentResponse, error) {
	if c == nil || c.apiKey == "" {
		return nil, fmt.Errorf("missing api key")
	}
	url := fmt.Sprintf("%s/models/%s:embedContent?key=%s", baseURL, req.Model, c.apiKey)
	return doJSONWithRetry[EmbedContentResponse](ctx, c.http, url, req)
}

func (c *Client) BatchEmbedContents(ctx context.Context, model string, requests []EmbedContentRequest) (*BatchEmbedContentsResponse, error) {
	if c == nil || c.apiKey == "" {
		return nil, fmt.Errorf("missing api key")
	}
	url := fmt.Sprintf("%s/models/%s:batchEmbedContents?key=%s", baseURL, model, c.apiKey)
	// Batch API requires full model path like "models/gemini-embedding-1"
	fullModelName := model
	if len(model) > 0 && model[0] != 'm' {
		fullModelName = "models/" + model
	}
	for i := range requests {
		requests[i].Model = fullModelName
	}
	payload := BatchEmbedContentsRequest{Requests: requests}
	return doJSONWithRetry[BatchEmbedContentsResponse](ctx, c.http, url, &payload)
}

func doJSONWithRetry[T any](ctx context.Context, client *http.Client, url string, payload any) (*T, error) {
	body, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	var lastErr error
	for attempt := 0; attempt <= maxRetries; attempt++ {
		if attempt > 0 {
			backoff := initialBackoff * time.Duration(1<<(attempt-1))
			select {
			case <-ctx.Done():
				return nil, ctx.Err()
			case <-time.After(backoff):
			}
		}

		req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bytes.NewReader(body))
		if err != nil {
			return nil, fmt.Errorf("failed to create request: %w", err)
		}
		req.Header.Set("Content-Type", "application/json")

		resp, err := client.Do(req)
		if err != nil {
			lastErr = fmt.Errorf("request failed: %w", err)
			continue
		}

		respBody, readErr := io.ReadAll(resp.Body)
		resp.Body.Close()
		if readErr != nil {
			lastErr = fmt.Errorf("failed to read response: %w", readErr)
			continue
		}

		// Retry on rate limits / transient server errors.
		if resp.StatusCode == 429 || resp.StatusCode >= 500 {
			lastErr = fmt.Errorf("retryable status code %d", resp.StatusCode)
			continue
		}

		var out T
		if err := json.Unmarshal(respBody, &out); err != nil {
			return nil, fmt.Errorf("failed to unmarshal response: %w", err)
		}

		// If response has embedded API error, bubble it up.
		// (We don't generically introspect; callers validate embedding presence.)
		return &out, nil
	}

	return nil, fmt.Errorf("max retries exceeded: %w", lastErr)
}
