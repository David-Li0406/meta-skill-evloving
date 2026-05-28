package clients

import (
	"context"
	"fmt"
	"time"

	"k8s.io/apimachinery/pkg/api/errors"
)

// RetryConfig defines retry behavior
type RetryConfig struct {
	MaxRetries     int           // Maximum number of retry attempts
	InitialBackoff time.Duration // Initial backoff duration
	MaxBackoff     time.Duration // Maximum backoff duration
	Multiplier     float64       // Backoff multiplier
}

// DefaultRetryConfig returns sensible retry defaults
func DefaultRetryConfig() *RetryConfig {
	return &RetryConfig{
		MaxRetries:     3,
		InitialBackoff: 100 * time.Millisecond,
		MaxBackoff:     5 * time.Second,
		Multiplier:     2.0,
	}
}

// RetryWithBackoff retries a function with exponential backoff
func RetryWithBackoff(ctx context.Context, cfg *RetryConfig, fn func() error) error {
	if cfg == nil {
		cfg = DefaultRetryConfig()
	}

	var lastErr error
	backoff := cfg.InitialBackoff

	for attempt := 0; attempt <= cfg.MaxRetries; attempt++ {
		// Execute the function
		err := fn()
		if err == nil {
			return nil // Success!
		}

		lastErr = err

		// Check if error is retryable
		if !isRetryable(err) {
			return fmt.Errorf("non-retryable error: %w", err)
		}

		// Don't sleep after the last attempt
		if attempt == cfg.MaxRetries {
			break
		}

		// Check context before sleeping
		select {
		case <-ctx.Done():
			return fmt.Errorf("context cancelled after %d attempts: %w", attempt+1, ctx.Err())
		case <-time.After(backoff):
			// Increase backoff exponentially
			backoff = time.Duration(float64(backoff) * cfg.Multiplier)
			if backoff > cfg.MaxBackoff {
				backoff = cfg.MaxBackoff
			}
		}
	}

	return fmt.Errorf("max retries (%d) exceeded: %w", cfg.MaxRetries, lastErr)
}

// isRetryable determines if a Kubernetes API error should be retried
func isRetryable(err error) bool {
	if err == nil {
		return false
	}

	// Kubernetes API errors
	if errors.IsTimeout(err) {
		return true
	}
	if errors.IsServerTimeout(err) {
		return true
	}
	if errors.IsTooManyRequests(err) {
		return true
	}
	if errors.IsInternalError(err) {
		return true
	}
	if errors.IsServiceUnavailable(err) {
		return true
	}

	// Temporary network errors (connection refused, etc.)
	// These would need more sophisticated detection in production
	return false
}

// WithRetry wraps a Kubernetes operation with retry logic
// Example:
//
//	nodes, err := WithRetry(ctx, client, func(c *K8sClient) (*corev1.NodeList, error) {
//	    return c.ListNodes(ctx)
//	})
func WithRetry[T any](ctx context.Context, client *K8sClient, fn func(*K8sClient) (T, error)) (T, error) {
	var result T
	var resultErr error

	err := RetryWithBackoff(ctx, DefaultRetryConfig(), func() error {
		var err error
		result, err = fn(client)
		resultErr = err
		return err
	})

	if err != nil {
		return result, err
	}
	return result, resultErr
}
