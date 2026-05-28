package gemini

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"math"
	"math/rand"
	"net/http"
	"os/exec"
	"strings"
	"sync"
	"time"

	"github.com/Napageneral/cortex/internal/ratelimit"
)

const (
	baseURL             = "https://generativelanguage.googleapis.com/v1beta"
	maxRetries          = 5
	initialBackoff      = 500 * time.Millisecond
	maxBackoff          = 30 * time.Second
	defaultTimeout      = 120 * time.Second
	maxIdleConns        = 1000
	maxConnsPerHost     = 1000
	idleConnTimeout     = 90 * time.Second
	tlsHandshakeTimeout = 10 * time.Second
)

// Client is a Gemini API client with HTTP/2 support and retries
type Client struct {
	httpClient      *http.Client
	apiKey          string
	analysisLimiter *ratelimit.LeakyBucket
	embedLimiter    *ratelimit.LeakyBucket
	useADC          bool
	accessToken     string
	tokenExpiry     time.Time
	tokenMu         sync.Mutex

	// Usage tracking
	usageMu            sync.Mutex
	totalPromptTokens  int64
	totalOutputTokens  int64
	totalEmbedChars    int64
	generateCalls      int64
	embedCalls         int64
}

// NewClient creates a new Gemini client with HTTP/2 pooling and retries
// If apiKey is empty, uses Application Default Credentials (gcloud auth)
func NewClient(apiKey string) *Client {
	transport := &http.Transport{
		MaxIdleConns:        maxIdleConns,
		MaxIdleConnsPerHost: maxConnsPerHost,
		MaxConnsPerHost:     maxConnsPerHost,
		IdleConnTimeout:     idleConnTimeout,
		TLSHandshakeTimeout: tlsHandshakeTimeout,
		ForceAttemptHTTP2:   true, // Enable HTTP/2
	}

	return &Client{
		httpClient: &http.Client{
			Transport: transport,
			Timeout:   defaultTimeout,
		},
		apiKey: apiKey,
		useADC: apiKey == "",
	}
}

// SetAnalysisRPM sets a smooth rate limit for GenerateContent requests.
// rpm<=0 disables rate limiting.
func (c *Client) SetAnalysisRPM(rpm int) {
	if c == nil {
		return
	}
	if rpm <= 0 {
		if c.analysisLimiter != nil {
			c.analysisLimiter.Close()
		}
		c.analysisLimiter = nil
		return
	}
	if c.analysisLimiter == nil {
		c.analysisLimiter = ratelimit.NewLeakyBucketFromRPM(rpm)
		return
	}
	c.analysisLimiter.SetRPM(rpm)
}

// SetEmbedRPM sets a smooth rate limit for EmbedContent requests.
// rpm<=0 disables rate limiting.
func (c *Client) SetEmbedRPM(rpm int) {
	if c == nil {
		return
	}
	if rpm <= 0 {
		if c.embedLimiter != nil {
			c.embedLimiter.Close()
		}
		c.embedLimiter = nil
		return
	}
	if c.embedLimiter == nil {
		c.embedLimiter = ratelimit.NewLeakyBucketFromRPM(rpm)
		return
	}
	c.embedLimiter.SetRPM(rpm)
}

func (c *Client) getAccessToken() (string, error) {
	c.tokenMu.Lock()
	defer c.tokenMu.Unlock()

	if c.accessToken != "" && time.Now().Add(60*time.Second).Before(c.tokenExpiry) {
		return c.accessToken, nil
	}

	cmd := exec.Command("gcloud", "auth", "application-default", "print-access-token")
	output, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("gcloud auth failed: %w (run 'gcloud auth application-default login')", err)
	}

	c.accessToken = strings.TrimSpace(string(output))
	c.tokenExpiry = time.Now().Add(55 * time.Minute)
	return c.accessToken, nil
}

func (c *Client) buildRequest(ctx context.Context, method, endpoint string, body []byte) (*http.Request, error) {
	var url string
	if c.useADC {
		url = fmt.Sprintf("%s/%s", baseURL, endpoint)
	} else {
		url = fmt.Sprintf("%s/%s?key=%s", baseURL, endpoint, c.apiKey)
	}

	req, err := http.NewRequestWithContext(ctx, method, url, bytes.NewReader(body))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")

	if c.useADC {
		token, err := c.getAccessToken()
		if err != nil {
			return nil, err
		}
		req.Header.Set("Authorization", "Bearer "+token)
	}

	return req, nil
}

// GenerateContentRequest for the generateContent API
type GenerateContentRequest struct {
	Contents         []Content         `json:"contents"`
	GenerationConfig *GenerationConfig `json:"generationConfig,omitempty"`
	SafetySettings   []SafetySetting   `json:"safetySettings,omitempty"`
}

type GenerationConfig struct {
	ThinkingConfig     *ThinkingConfig `json:"thinkingConfig,omitempty"`
	ResponseMimeType   string          `json:"responseMimeType,omitempty"`
	ResponseSchema     any             `json:"responseSchema,omitempty"`
	ResponseJsonSchema any             `json:"responseJsonSchema,omitempty"`
}

type ThinkingConfig struct {
	ThinkingLevel string `json:"thinkingLevel,omitempty"`
}

type SafetySetting struct {
	Category  string `json:"category"`
	Threshold string `json:"threshold"`
}

type Content struct {
	Role  string `json:"role,omitempty"`
	Parts []Part `json:"parts"`
}

type Part struct {
	Text string `json:"text,omitempty"`
}

type GenerateContentResponse struct {
	Candidates     []Candidate     `json:"candidates,omitempty"`
	PromptFeedback *PromptFeedback `json:"promptFeedback,omitempty"`
	UsageMetadata  *UsageMetadata  `json:"usageMetadata,omitempty"`
	Error          *APIError       `json:"error,omitempty"`
}

// UsageMetadata contains token usage information from the API
type UsageMetadata struct {
	PromptTokenCount     int `json:"promptTokenCount"`
	CandidatesTokenCount int `json:"candidatesTokenCount"`
	TotalTokenCount      int `json:"totalTokenCount"`
}

type Candidate struct {
	Content       Content        `json:"content"`
	FinishReason  string         `json:"finishReason,omitempty"`
	SafetyRatings []SafetyRating `json:"safetyRatings,omitempty"`
}

type PromptFeedback struct {
	BlockReason        string         `json:"blockReason,omitempty"`
	BlockReasonMessage string         `json:"blockReasonMessage,omitempty"`
	SafetyRatings      []SafetyRating `json:"safetyRatings,omitempty"`
}

type SafetyRating struct {
	Category    string `json:"category"`
	Probability string `json:"probability"`
}

type APIError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
	Status  string `json:"status"`
}

func (e *APIError) Error() string {
	return fmt.Sprintf("gemini API error %d (%s): %s", e.Code, e.Status, e.Message)
}

// EmbedContentRequest for embedding API
type EmbedContentRequest struct {
	Model   string  `json:"model"`
	Content Content `json:"content"`
}

type EmbedContentResponse struct {
	Embedding *Embedding `json:"embedding,omitempty"`
	Error     *APIError  `json:"error,omitempty"`
}

// BatchEmbedContentsRequest for batch embedding API
type BatchEmbedContentsRequest struct {
	Requests []EmbedContentRequest `json:"requests"`
}

// BatchEmbedContentsResponse for batch embedding API
type BatchEmbedContentsResponse struct {
	Embeddings []Embedding `json:"embeddings,omitempty"`
	Error      *APIError   `json:"error,omitempty"`
}

type Embedding struct {
	Values []float64 `json:"values"`
}

// GenerateContent calls the Gemini generateContent API
func (c *Client) GenerateContent(ctx context.Context, model string, req *GenerateContentRequest) (*GenerateContentResponse, error) {
	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("marshal request: %w", err)
	}

	endpoint := fmt.Sprintf("models/%s:generateContent", model)

	var lastErr error
	for attempt := 0; attempt <= maxRetries; attempt++ {
		// Wait for rate limiter if configured
		if c.analysisLimiter != nil {
			if err := c.analysisLimiter.Wait(ctx); err != nil {
				return nil, err
			}
		}
		if attempt > 0 {
			backoff := calculateBackoff(attempt)
			time.Sleep(backoff)
		}

		httpReq, err := c.buildRequest(ctx, "POST", endpoint, body)
		if err != nil {
			return nil, err
		}

		resp, err := c.httpClient.Do(httpReq)
		if err != nil {
			lastErr = err
			continue
		}

		respBody, err := io.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			lastErr = err
			continue
		}

		if isRetryableStatus(resp.StatusCode) {
			lastErr = fmt.Errorf("status %d", resp.StatusCode)
			continue
		}

		var result GenerateContentResponse
		if err := json.Unmarshal(respBody, &result); err != nil {
			return nil, fmt.Errorf("unmarshal response: %w", err)
		}

		if result.Error != nil {
			if isRetryableStatus(result.Error.Code) {
				lastErr = result.Error
				continue
			}
			return nil, result.Error
		}

		// Record usage for cost tracking
		c.recordGenerateUsage(result.UsageMetadata)

		return &result, nil
	}

	return nil, fmt.Errorf("max retries exceeded: %w", lastErr)
}

// EmbedContent calls the Gemini embedContent API
func (c *Client) EmbedContent(ctx context.Context, req *EmbedContentRequest) (*EmbedContentResponse, error) {
	// Calculate character count for cost tracking
	charCount := 0
	for _, part := range req.Content.Parts {
		charCount += len(part.Text)
	}

	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("marshal request: %w", err)
	}

	endpoint := fmt.Sprintf("models/%s:embedContent", req.Model)

	var lastErr error
	for attempt := 0; attempt <= maxRetries; attempt++ {
		// Wait for rate limiter if configured
		if c.embedLimiter != nil {
			if err := c.embedLimiter.Wait(ctx); err != nil {
				return nil, err
			}
		}
		if attempt > 0 {
			backoff := calculateBackoff(attempt)
			time.Sleep(backoff)
		}

		httpReq, err := c.buildRequest(ctx, "POST", endpoint, body)
		if err != nil {
			return nil, err
		}

		resp, err := c.httpClient.Do(httpReq)
		if err != nil {
			lastErr = err
			continue
		}

		respBody, err := io.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			lastErr = err
			continue
		}

		if isRetryableStatus(resp.StatusCode) {
			lastErr = fmt.Errorf("status %d", resp.StatusCode)
			continue
		}

		var result EmbedContentResponse
		if err := json.Unmarshal(respBody, &result); err != nil {
			return nil, fmt.Errorf("unmarshal response: %w", err)
		}

		if result.Error != nil {
			if isRetryableStatus(result.Error.Code) {
				lastErr = result.Error
				continue
			}
			return nil, result.Error
		}

		// Record usage for cost tracking
		c.recordEmbedUsage(charCount)

		return &result, nil
	}

	return nil, fmt.Errorf("max retries exceeded: %w", lastErr)
}

// BatchEmbedContents calls the Gemini batchEmbedContents API for batch embeddings
func (c *Client) BatchEmbedContents(ctx context.Context, model string, requests []EmbedContentRequest) (*BatchEmbedContentsResponse, error) {
	// Calculate total character count for cost tracking
	totalCharCount := 0
	for _, req := range requests {
		for _, part := range req.Content.Parts {
			totalCharCount += len(part.Text)
		}
	}

	// Set model in each request (must be fully qualified with models/ prefix)
	fullModel := "models/" + model
	for i := range requests {
		requests[i].Model = fullModel
	}

	batchReq := BatchEmbedContentsRequest{
		Requests: requests,
	}

	body, err := json.Marshal(batchReq)
	if err != nil {
		return nil, fmt.Errorf("marshal request: %w", err)
	}

	endpoint := fmt.Sprintf("models/%s:batchEmbedContents", model)

	var lastErr error
	for attempt := 0; attempt <= maxRetries; attempt++ {
		// Wait for rate limiter if configured
		if c.embedLimiter != nil {
			if err := c.embedLimiter.Wait(ctx); err != nil {
				return nil, err
			}
		}
		if attempt > 0 {
			backoff := calculateBackoff(attempt)
			time.Sleep(backoff)
		}

		httpReq, err := c.buildRequest(ctx, "POST", endpoint, body)
		if err != nil {
			return nil, err
		}

		resp, err := c.httpClient.Do(httpReq)
		if err != nil {
			lastErr = err
			continue
		}

		respBody, err := io.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			lastErr = err
			continue
		}

		if isRetryableStatus(resp.StatusCode) {
			lastErr = fmt.Errorf("status %d", resp.StatusCode)
			continue
		}

		var result BatchEmbedContentsResponse
		if err := json.Unmarshal(respBody, &result); err != nil {
			return nil, fmt.Errorf("unmarshal response: %w", err)
		}

		if result.Error != nil {
			if isRetryableStatus(result.Error.Code) {
				lastErr = result.Error
				continue
			}
			return nil, result.Error
		}

		// Record usage for cost tracking
		c.recordEmbedUsage(totalCharCount)

		return &result, nil
	}

	return nil, fmt.Errorf("max retries exceeded: %w", lastErr)
}

func isRetryableStatus(code int) bool {
	return code == 429 || code >= 500
}

func calculateBackoff(attempt int) time.Duration {
	backoff := float64(initialBackoff) * math.Pow(2, float64(attempt-1))
	if backoff > float64(maxBackoff) {
		backoff = float64(maxBackoff)
	}
	jitter := backoff * 0.25 * (rand.Float64()*2 - 1)
	return time.Duration(backoff + jitter)
}

// UsageStats contains accumulated usage statistics
type UsageStats struct {
	PromptTokens    int64   `json:"prompt_tokens"`
	OutputTokens    int64   `json:"output_tokens"`
	EmbedChars      int64   `json:"embed_chars"`
	GenerateCalls   int64   `json:"generate_calls"`
	EmbedCalls      int64   `json:"embed_calls"`
	EstimatedCostUSD float64 `json:"estimated_cost_usd"`
}

// GetUsageStats returns accumulated usage statistics and estimated cost
// Pricing (Gemini 2.0 Flash as of Jan 2026):
//   - Input: $0.075 per 1M tokens
//   - Output: $0.30 per 1M tokens
//   - Embeddings: $0.00001 per 1K characters
func (c *Client) GetUsageStats() UsageStats {
	c.usageMu.Lock()
	defer c.usageMu.Unlock()

	stats := UsageStats{
		PromptTokens:  c.totalPromptTokens,
		OutputTokens:  c.totalOutputTokens,
		EmbedChars:    c.totalEmbedChars,
		GenerateCalls: c.generateCalls,
		EmbedCalls:    c.embedCalls,
	}

	// Calculate cost
	inputCost := float64(c.totalPromptTokens) * 0.075 / 1_000_000
	outputCost := float64(c.totalOutputTokens) * 0.30 / 1_000_000
	embedCost := float64(c.totalEmbedChars) * 0.00001 / 1_000
	stats.EstimatedCostUSD = inputCost + outputCost + embedCost

	return stats
}

// ResetUsageStats clears accumulated usage statistics
func (c *Client) ResetUsageStats() {
	c.usageMu.Lock()
	defer c.usageMu.Unlock()
	c.totalPromptTokens = 0
	c.totalOutputTokens = 0
	c.totalEmbedChars = 0
	c.generateCalls = 0
	c.embedCalls = 0
}

func (c *Client) recordGenerateUsage(usage *UsageMetadata) {
	if usage == nil {
		return
	}
	c.usageMu.Lock()
	defer c.usageMu.Unlock()
	c.totalPromptTokens += int64(usage.PromptTokenCount)
	c.totalOutputTokens += int64(usage.CandidatesTokenCount)
	c.generateCalls++
}

func (c *Client) recordEmbedUsage(charCount int) {
	c.usageMu.Lock()
	defer c.usageMu.Unlock()
	c.totalEmbedChars += int64(charCount)
	c.embedCalls++
}
