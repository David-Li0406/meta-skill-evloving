package compute

import (
	"context"
	"sync"
	"time"

	"github.com/Napageneral/cortex/internal/gemini"
)

const (
	defaultMaxBatchSize  = 100 // Max texts per batch (Gemini limit)
	defaultFlushInterval = 500 * time.Millisecond
)

// EmbeddingTask represents a single embedding task
type EmbeddingTask struct {
	EntityType string
	EntityID   string
	Text       string
	ResultChan chan EmbeddingResult // Channel to receive result
}

// EmbeddingResult represents the result of an embedding task
type EmbeddingResult struct {
	EntityType string
	EntityID   string
	Embedding  []float64
	Error      error
}

// EmbeddingsBatcher batches embedding tasks for efficient API calls
// Uses BatchEmbedContents API to send up to 100 embeddings per request
type EmbeddingsBatcher struct {
	client        *gemini.Client
	model         string
	maxBatchSize  int
	flushInterval time.Duration

	mu      sync.Mutex
	batch   []EmbeddingTask
	metrics *BatcherMetrics

	ctx    context.Context
	cancel context.CancelFunc
	wg     sync.WaitGroup
}

// BatcherMetrics tracks batcher performance
type BatcherMetrics struct {
	mu            sync.Mutex
	BatchesSent   int
	TotalEmbedded int
	TotalErrors   int
	TotalAPIMs    int64
}

// NewEmbeddingsBatcher creates a new embedding batcher
func NewEmbeddingsBatcher(client *gemini.Client, model string, maxBatchSize int) *EmbeddingsBatcher {
	if maxBatchSize <= 0 || maxBatchSize > defaultMaxBatchSize {
		maxBatchSize = defaultMaxBatchSize
	}
	ctx, cancel := context.WithCancel(context.Background())
	b := &EmbeddingsBatcher{
		client:        client,
		model:         model,
		maxBatchSize:  maxBatchSize,
		flushInterval: defaultFlushInterval,
		batch:         make([]EmbeddingTask, 0, maxBatchSize),
		metrics:       &BatcherMetrics{},
		ctx:           ctx,
		cancel:        cancel,
	}

	// Start flush timer goroutine
	b.wg.Add(1)
	go b.timerLoop()

	return b
}

// Submit adds a task to the batch and waits for the result
func (b *EmbeddingsBatcher) Submit(ctx context.Context, entityType, entityID, text string) ([]float64, error) {
	resultChan := make(chan EmbeddingResult, 1)

	task := EmbeddingTask{
		EntityType: entityType,
		EntityID:   entityID,
		Text:       text,
		ResultChan: resultChan,
	}

	b.mu.Lock()
	b.batch = append(b.batch, task)

	// Flush if batch is full
	if len(b.batch) >= b.maxBatchSize {
		b.flushLocked()
	}
	b.mu.Unlock()

	// Wait for result
	select {
	case result := <-resultChan:
		return result.Embedding, result.Error
	case <-ctx.Done():
		return nil, ctx.Err()
	case <-b.ctx.Done():
		return nil, b.ctx.Err()
	}
}

// Flush flushes any pending tasks in the batch
func (b *EmbeddingsBatcher) Flush() {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.flushLocked()
}

// flushLocked flushes the batch (must be called with lock held)
func (b *EmbeddingsBatcher) flushLocked() {
	if len(b.batch) == 0 {
		return
	}

	// Copy batch for processing
	tasks := make([]EmbeddingTask, len(b.batch))
	copy(tasks, b.batch)
	b.batch = b.batch[:0] // Clear batch

	// Process batch in background
	b.wg.Add(1)
	go func() {
		defer b.wg.Done()
		b.processBatch(tasks)
	}()
}

// processBatch processes a batch of embedding tasks
func (b *EmbeddingsBatcher) processBatch(tasks []EmbeddingTask) {
	if len(tasks) == 0 {
		return
	}

	// Build batch request - don't set Model in individual requests, use endpoint model
	requests := make([]gemini.EmbedContentRequest, len(tasks))
	for i, task := range tasks {
		requests[i] = gemini.EmbedContentRequest{
			Content: gemini.Content{
				Parts: []gemini.Part{
					{Text: task.Text},
				},
			},
		}
	}

	// Call Gemini batch API
	start := time.Now()
	resp, err := b.client.BatchEmbedContents(b.ctx, b.model, requests)
	apiMs := time.Since(start).Milliseconds()

	// Update metrics
	b.metrics.mu.Lock()
	b.metrics.BatchesSent++
	b.metrics.TotalAPIMs += apiMs
	if err != nil {
		b.metrics.TotalErrors += len(tasks)
	} else {
		b.metrics.TotalEmbedded += len(tasks)
	}
	b.metrics.mu.Unlock()

	if err != nil {
		// Send error for all tasks in batch
		for _, task := range tasks {
			select {
			case task.ResultChan <- EmbeddingResult{
				EntityType: task.EntityType,
				EntityID:   task.EntityID,
				Error:      err,
			}:
			default:
			}
		}
		return
	}

	// Send results
	for i, task := range tasks {
		var embedding []float64
		var taskErr error

		if i < len(resp.Embeddings) {
			embedding = resp.Embeddings[i].Values
		} else {
			taskErr = err
		}

		select {
		case task.ResultChan <- EmbeddingResult{
			EntityType: task.EntityType,
			EntityID:   task.EntityID,
			Embedding:  embedding,
			Error:      taskErr,
		}:
		default:
		}
	}
}

// timerLoop periodically flushes the batch
func (b *EmbeddingsBatcher) timerLoop() {
	defer b.wg.Done()

	ticker := time.NewTicker(b.flushInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			b.Flush()
		case <-b.ctx.Done():
			return
		}
	}
}

// Metrics returns current batcher metrics
func (b *EmbeddingsBatcher) Metrics() map[string]any {
	b.metrics.mu.Lock()
	defer b.metrics.mu.Unlock()

	avgApiMs := float64(0)
	if b.metrics.BatchesSent > 0 {
		avgApiMs = float64(b.metrics.TotalAPIMs) / float64(b.metrics.BatchesSent)
	}

	return map[string]any{
		"batches_sent":     b.metrics.BatchesSent,
		"total_embedded":   b.metrics.TotalEmbedded,
		"total_errors":     b.metrics.TotalErrors,
		"avg_batch_api_ms": avgApiMs,
		"embeddings_per_batch": func() float64 {
			if b.metrics.BatchesSent == 0 {
				return 0
			}
			return float64(b.metrics.TotalEmbedded) / float64(b.metrics.BatchesSent)
		}(),
	}
}

// Close closes the batcher and waits for all pending work to complete
func (b *EmbeddingsBatcher) Close() {
	// Flush any remaining tasks
	b.Flush()

	// Stop timer loop
	b.cancel()

	// Wait for all goroutines to finish
	b.wg.Wait()
}
