package embeddings

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/Napageneral/aix/internal/gemini"
)

const (
	defaultMaxBatchSize  = 100
	defaultFlushInterval = 1 * time.Second
)

type Task struct {
	EntityType string
	EntityID   string
	Text       string
}

type Result struct {
	Task      Task
	Embedding []float64
	Error     error
}

// Batcher batches embedding tasks for efficient Gemini batch API usage.
type Batcher struct {
	client        *gemini.Client
	model         string
	maxBatchSize  int
	flushInterval time.Duration

	mu      sync.Mutex
	batch   []Task
	results chan Result

	ctx    context.Context
	cancel context.CancelFunc
	wg     sync.WaitGroup
}

func NewBatcher(client *gemini.Client, model string) *Batcher {
	ctx, cancel := context.WithCancel(context.Background())
	b := &Batcher{
		client:        client,
		model:         model,
		maxBatchSize:  defaultMaxBatchSize,
		flushInterval: defaultFlushInterval,
		batch:         make([]Task, 0, defaultMaxBatchSize),
		results:       make(chan Result, 200),
		ctx:           ctx,
		cancel:        cancel,
	}

	b.wg.Add(1)
	go b.timerLoop()

	return b
}

func (b *Batcher) Add(task Task) {
	b.mu.Lock()
	defer b.mu.Unlock()

	b.batch = append(b.batch, task)
	if len(b.batch) >= b.maxBatchSize {
		b.flushLocked()
	}
}

func (b *Batcher) Results() <-chan Result {
	return b.results
}

func (b *Batcher) Flush() {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.flushLocked()
}

func (b *Batcher) Close() {
	b.Flush()
	b.cancel()
	b.wg.Wait()
	close(b.results)
}

func (b *Batcher) flushLocked() {
	if len(b.batch) == 0 {
		return
	}
	tasks := make([]Task, len(b.batch))
	copy(tasks, b.batch)
	b.batch = b.batch[:0]

	b.wg.Add(1)
	go func() {
		defer b.wg.Done()
		b.processBatch(tasks)
	}()
}

func (b *Batcher) processBatch(tasks []Task) {
	if len(tasks) == 0 {
		return
	}

	reqs := make([]gemini.EmbedContentRequest, len(tasks))
	for i, t := range tasks {
		reqs[i] = gemini.EmbedContentRequest{
			Model: b.model,
			Content: gemini.Content{
				Parts: []gemini.Part{{Text: t.Text}},
			},
		}
	}

	resp, err := b.client.BatchEmbedContents(b.ctx, b.model, reqs)
	if err != nil {
		for _, t := range tasks {
			select {
			case b.results <- Result{Task: t, Error: err}:
			case <-b.ctx.Done():
				return
			}
		}
		return
	}
	if resp == nil {
		for _, t := range tasks {
			select {
			case b.results <- Result{Task: t, Error: fmt.Errorf("nil batch response")}:
			case <-b.ctx.Done():
				return
			}
		}
		return
	}

	for i, t := range tasks {
		var emb []float64
		var taskErr error
		if i < len(resp.Embeddings) {
			emb = resp.Embeddings[i].Values
			if len(emb) == 0 {
				taskErr = fmt.Errorf("empty embedding")
			}
		} else {
			taskErr = fmt.Errorf("missing embedding in response")
		}

		select {
		case b.results <- Result{Task: t, Embedding: emb, Error: taskErr}:
		case <-b.ctx.Done():
			return
		}
	}
}

func (b *Batcher) timerLoop() {
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
