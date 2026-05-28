package compute

import (
	"context"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/Napageneral/cortex/internal/gemini"
	"github.com/Napageneral/taskengine/engine"
	"github.com/Napageneral/taskengine/queue"
	"github.com/google/uuid"
)

const (
	JobTypeAnalysis  = "analysis"
	JobTypeEmbedding = "embedding"
)

// Engine wraps the taskengine with cortex-specific handlers and adaptive control
type Engine struct {
	db           *sql.DB
	geminiClient *gemini.Client
	queue        *queue.Queue
	engine       *engine.Engine
	writer       *engine.TxBatchWriter
	metrics      *JobMetrics

	analysisModel  string
	embeddingModel string

	// Adaptive control components
	sem               *AdaptiveSemaphore
	adaptiveCtrl      *AdaptiveController
	analysisRPMCtrl   *AutoRPMController
	embedRPMCtrl      *AutoRPMController
	cancelControllers context.CancelFunc

	// Embedding batcher for high-throughput batch API calls
	embeddingBatcher *EmbeddingsBatcher

	// Pre-encoded episode cache for high-throughput bulk processing
	// Maps episode_id -> encoded text
	episodeTextCache   map[string]string
	episodeTextCacheMu sync.RWMutex
}

// Config for the compute engine
type Config struct {
	WorkerCount        int
	AnalysisModel      string
	EmbeddingModel     string
	UseBatchWriter     bool // Enable TxBatchWriter for better write performance
	BatchSize          int
	EmbeddingBatchSize int

	// RPM settings (0 = auto-probe)
	AnalysisRPM int
	EmbedRPM    int

	// Disable adaptive concurrency controller (no in-flight throttling)
	DisableAdaptive bool
}

// DefaultConfig returns sensible defaults optimized for high-throughput processing
// Matching ChatStats parallelism settings for Tier-3 API keys
func DefaultConfig() Config {
	return Config{
		// 50 workers to match ChatStats ThreadPoolExecutor(max_workers=50)
		// With Tier-3 Gemini keys, this saturates the API nicely
		WorkerCount: 50,
		// Cortex defaults (per project policy):
		// - Analysis: Gemini 3 Flash Preview
		// - Embeddings: Gemini Embedding 001
		AnalysisModel:      "gemini-3-flash-preview",
		EmbeddingModel:     "gemini-embedding-001",
		UseBatchWriter:     true, // Enable by default
		BatchSize:          25,
		EmbeddingBatchSize: 100,
		AnalysisRPM:        0, // 0 = auto-probe
		EmbedRPM:           0, // 0 = auto-probe
		DisableAdaptive:    false,
	}
}

// NewEngine creates a compute engine for cortex with adaptive control
func NewEngine(db *sql.DB, geminiClient *gemini.Client, cfg Config) (*Engine, error) {
	// Initialize the job queue schema
	if err := queue.Init(db); err != nil {
		return nil, fmt.Errorf("init queue schema: %w", err)
	}

	analysisModel, err := normalizeAnalysisModel(cfg.AnalysisModel)
	if err != nil {
		return nil, err
	}
	cfg.AnalysisModel = analysisModel

	q := queue.New(db)

	engineCfg := engine.DefaultConfig()
	engineCfg.WorkerCount = cfg.WorkerCount
	engineCfg.LeaseOwner = "cortex-compute"

	e := &Engine{
		db:             db,
		geminiClient:   geminiClient,
		queue:          q,
		engine:         engine.New(q, engineCfg),
		metrics:        NewJobMetrics(),
		analysisModel:  cfg.AnalysisModel,
		embeddingModel: cfg.EmbeddingModel,
	}

	// Initialize TxBatchWriter if enabled
	if cfg.UseBatchWriter {
		batchSize := cfg.BatchSize
		if batchSize <= 0 {
			batchSize = 25
		}
		e.writer = engine.NewTxBatchWriter(db, engine.TxBatchWriterConfig{
			BatchSize:     batchSize,
			FlushInterval: 100 * time.Millisecond,
		})
		e.writer.Start()
	}

	// Setup RPM rate limiting
	// If RPM is explicitly set (non-zero), use fixed RPM.
	// If 0, we'll set up auto-probe controllers in Run().
	if cfg.AnalysisRPM > 0 {
		geminiClient.SetAnalysisRPM(cfg.AnalysisRPM)
	}
	if cfg.EmbedRPM > 0 {
		geminiClient.SetEmbedRPM(cfg.EmbedRPM)
	}

	// Create adaptive semaphore/controller for in-flight control (optional)
	if !cfg.DisableAdaptive {
		e.sem = NewAdaptiveSemaphore(cfg.WorkerCount)
		e.adaptiveCtrl = NewAdaptiveController(e.sem, DefaultAdaptiveControllerConfig(cfg.WorkerCount))
	}

	// Create auto-RPM controllers if not using fixed RPM
	if cfg.AnalysisRPM <= 0 {
		e.analysisRPMCtrl = NewAutoRPMController(DefaultAutoRPMConfig(), geminiClient.SetAnalysisRPM)
	}
	if cfg.EmbedRPM <= 0 {
		e.embedRPMCtrl = NewAutoRPMController(DefaultAutoRPMConfig(), geminiClient.SetEmbedRPM)
	}

	// Create embedding batcher for high-throughput batch API calls
	e.embeddingBatcher = NewEmbeddingsBatcher(geminiClient, cfg.EmbeddingModel, cfg.EmbeddingBatchSize)

	// Register handlers (adaptive control optional)
	e.engine.RegisterHandler(JobTypeAnalysis, e.wrapHandler(e.handleAnalysisJob, JobTypeAnalysis))
	e.engine.RegisterHandler(JobTypeEmbedding, e.wrapHandler(e.handleEmbeddingJob, JobTypeEmbedding))

	return e, nil
}

// wrapHandler wraps a job handler with adaptive control (semaphore + observation)
func (e *Engine) wrapHandler(base func(context.Context, *queue.Job) error, jobType string) func(context.Context, *queue.Job) error {
	return func(ctx context.Context, job *queue.Job) error {
		// Acquire semaphore if adaptive control is enabled
		if e.sem != nil {
			if err := e.sem.Acquire(ctx); err != nil {
				return err
			}
			defer e.sem.Release()
		}

		start := time.Now()
		err := base(ctx, job)
		elapsed := time.Since(start)

		// Feed the adaptive controller
		if e.adaptiveCtrl != nil {
			e.adaptiveCtrl.Observe(elapsed, err)
		}

		// Feed the RPM controllers by job type
		switch jobType {
		case JobTypeAnalysis:
			if e.analysisRPMCtrl != nil {
				e.analysisRPMCtrl.Observe(err)
			}
		case JobTypeEmbedding:
			if e.embedRPMCtrl != nil {
				e.embedRPMCtrl.Observe(err)
			}
		}

		return err
	}
}

// Close shuts down the engine gracefully
func (e *Engine) Close() error {
	// Stop controllers
	if e.cancelControllers != nil {
		e.cancelControllers()
	}
	// Close embedding batcher (flushes pending)
	if e.embeddingBatcher != nil {
		e.embeddingBatcher.Close()
	}
	if e.writer != nil {
		return e.writer.Close()
	}
	return nil
}

// JobMetrics returns the job metrics collector
func (e *Engine) JobMetrics() *JobMetrics {
	return e.metrics
}

// Run starts the compute engine and processes jobs until done or context cancelled
func (e *Engine) Run(ctx context.Context) (*engine.Stats, error) {
	// Create a cancellable context for the controllers
	ctrlCtx, cancel := context.WithCancel(ctx)
	e.cancelControllers = cancel

	// Start the adaptive controller
	if e.adaptiveCtrl != nil {
		e.adaptiveCtrl.Start(ctrlCtx)
	}

	// Start RPM auto-controllers
	if e.analysisRPMCtrl != nil {
		e.analysisRPMCtrl.Start(ctrlCtx)
	}
	if e.embedRPMCtrl != nil {
		e.embedRPMCtrl.Start(ctrlCtx)
	}

	return e.engine.Run(ctx)
}

// ControllerStats returns snapshots of all controller states
func (e *Engine) ControllerStats() map[string]any {
	stats := make(map[string]any)
	stats["adaptive_controller"] = json.RawMessage(e.adaptiveCtrl.SnapshotJSON())
	if e.analysisRPMCtrl != nil {
		stats["analysis_rpm_controller"] = json.RawMessage(e.analysisRPMCtrl.SnapshotJSON())
	}
	if e.embedRPMCtrl != nil {
		stats["embed_rpm_controller"] = json.RawMessage(e.embedRPMCtrl.SnapshotJSON())
	}
	if e.embeddingBatcher != nil {
		stats["embedding_batcher"] = e.embeddingBatcher.Metrics()
	}
	return stats
}

// EffectiveRPM returns the current effective RPM for analysis and embedding
func (e *Engine) EffectiveRPM() (analysisRPM, embedRPM int) {
	if e.analysisRPMCtrl != nil {
		analysisRPM = e.analysisRPMCtrl.CurrentRPM()
	}
	if e.embedRPMCtrl != nil {
		embedRPM = e.embedRPMCtrl.CurrentRPM()
	}
	return
}

// PreloadEpisodes pre-encodes all episode texts into memory cache.
// This eliminates per-job DB reads during bulk processing, matching ChatStats'
// pre-encoding strategy for maximum throughput.
// Call this before Run() for best results with large batches.
func (e *Engine) PreloadEpisodes(ctx context.Context) (int, error) {
	log.Printf("[preload] Starting episode pre-encoding...")
	start := time.Now()

	// Get all episode IDs
	rows, err := e.db.QueryContext(ctx, `SELECT id FROM episodes`)
	if err != nil {
		return 0, fmt.Errorf("query episodes: %w", err)
	}

	var episodeIDs []string
	for rows.Next() {
		var id string
		if err := rows.Scan(&id); err != nil {
			rows.Close()
			return 0, err
		}
		episodeIDs = append(episodeIDs, id)
	}
	if err := rows.Err(); err != nil {
		rows.Close()
		return 0, err
	}
	rows.Close()

	if len(episodeIDs) == 0 {
		return 0, nil
	}

	// Pre-encode all episodes
	cache := make(map[string]string, len(episodeIDs))
	for _, episodeID := range episodeIDs {
		text, err := e.buildEpisodeText(ctx, episodeID)
		if err != nil {
			log.Printf("[preload] Warning: failed to encode episode %s: %v", episodeID, err)
			continue
		}
		cache[episodeID] = text
	}

	// Swap in the cache atomically
	e.episodeTextCacheMu.Lock()
	e.episodeTextCache = cache
	e.episodeTextCacheMu.Unlock()

	elapsed := time.Since(start)
	log.Printf("[preload] Pre-encoded %d episodes in %v (%.1f/sec)",
		len(cache), elapsed, float64(len(cache))/elapsed.Seconds())

	return len(cache), nil
}

// PreloadSegments is a backward-compatible alias for PreloadEpisodes.
// Deprecated: Use PreloadEpisodes instead.
func (e *Engine) PreloadSegments(ctx context.Context) (int, error) {
	return e.PreloadEpisodes(ctx)
}

// ClearEpisodeCache clears the pre-encoded episode cache
func (e *Engine) ClearEpisodeCache() {
	e.episodeTextCacheMu.Lock()
	e.episodeTextCache = nil
	e.episodeTextCacheMu.Unlock()
}

// ClearSegmentCache is a backward-compatible alias for ClearEpisodeCache.
// Deprecated: Use ClearEpisodeCache instead.
func (e *Engine) ClearSegmentCache() {
	e.ClearEpisodeCache()
}

// getEpisodeTextCached returns cached episode text if available
func (e *Engine) getEpisodeTextCached(episodeID string) (string, bool) {
	e.episodeTextCacheMu.RLock()
	defer e.episodeTextCacheMu.RUnlock()
	if e.episodeTextCache == nil {
		return "", false
	}
	text, ok := e.episodeTextCache[episodeID]
	return text, ok
}

// QueueStats returns current queue statistics
func (e *Engine) QueueStats() (*queue.Stats, error) {
	return e.queue.GetStats()
}

// EnqueueAnalysis queues analysis jobs for all un-analyzed episodes
func (e *Engine) EnqueueAnalysis(ctx context.Context, analysisTypeName string, episodeIDs ...string) (int, error) {
	// Get the analysis type
	var analysisTypeID string
	err := e.db.QueryRowContext(ctx, `
		SELECT id FROM analysis_types WHERE name = ?
	`, analysisTypeName).Scan(&analysisTypeID)
	if err != nil {
		return 0, fmt.Errorf("analysis type not found: %w", err)
	}

	var epIDs []string

	// If specific episode IDs provided, use those (already filtered by caller)
	if len(episodeIDs) > 0 {
		epIDs = episodeIDs
	} else {
		// Find episodes without analysis runs for this type
		// Collect all IDs first, then close rows before enqueueing (SQLite deadlock avoidance)
		rows, err := e.db.QueryContext(ctx, `
			SELECT ep.id FROM episodes ep
			WHERE NOT EXISTS (
				SELECT 1 FROM analysis_runs ar
				WHERE ar.episode_id = ep.id
				AND ar.analysis_type_id = ?
			)
		`, analysisTypeID)
		if err != nil {
			return 0, fmt.Errorf("query episodes: %w", err)
		}

		for rows.Next() {
			var epID string
			if err := rows.Scan(&epID); err != nil {
				rows.Close()
				return 0, err
			}
			epIDs = append(epIDs, epID)
		}
		if err := rows.Err(); err != nil {
			rows.Close()
			return 0, err
		}
		rows.Close()
	}

	// Now enqueue (rows is closed, no deadlock)
	count := 0
	for _, epID := range epIDs {
		payload := AnalysisJobPayload{
			EpisodeID:      epID,
			AnalysisTypeID: analysisTypeID,
		}

		if err := e.queue.Enqueue(queue.EnqueueOptions{
			Type:    JobTypeAnalysis,
			Key:     fmt.Sprintf("analysis:%s:%s", analysisTypeID, epID),
			Payload: payload,
		}); err != nil {
			log.Printf("failed to enqueue analysis for %s: %v", epID, err)
			continue
		}
		count++
	}

	return count, nil
}

// EnqueueEmbeddings queues embedding jobs for all un-embedded episodes
func (e *Engine) EnqueueEmbeddings(ctx context.Context) (int, error) {
	// Find episodes without embeddings
	// Collect IDs first, close rows, then enqueue (SQLite deadlock avoidance)
	rows, err := e.db.QueryContext(ctx, `
		SELECT ep.id FROM episodes ep
		WHERE NOT EXISTS (
			SELECT 1 FROM embeddings em
			WHERE em.target_type = 'episode'
			AND em.target_id = ep.id
		)
	`)
	if err != nil {
		return 0, fmt.Errorf("query episodes: %w", err)
	}

	var epIDs []string
	for rows.Next() {
		var epID string
		if err := rows.Scan(&epID); err != nil {
			rows.Close()
			return 0, err
		}
		epIDs = append(epIDs, epID)
	}
	if err := rows.Err(); err != nil {
		rows.Close()
		return 0, err
	}
	rows.Close()

	// Now enqueue (rows is closed, no deadlock)
	count := 0
	for _, epID := range epIDs {
		payload := EmbeddingJobPayload{
			EntityType: "episode",
			EntityID:   epID,
		}

		if err := e.queue.Enqueue(queue.EnqueueOptions{
			Type:    JobTypeEmbedding,
			Key:     fmt.Sprintf("embedding:episode:%s", epID),
			Payload: payload,
		}); err != nil {
			log.Printf("failed to enqueue embedding for %s: %v", epID, err)
			continue
		}
		count++
	}

	return count, nil
}

// EnqueueFacetEmbeddings queues embedding jobs for all un-embedded facets
func (e *Engine) EnqueueFacetEmbeddings(ctx context.Context) (int, error) {
	// Find facets without embeddings
	rows, err := e.db.QueryContext(ctx, `
		SELECT f.id FROM facets f
		WHERE NOT EXISTS (
			SELECT 1 FROM embeddings em
			WHERE em.target_type = 'facet'
			AND em.target_id = f.id
		)
	`)
	if err != nil {
		return 0, fmt.Errorf("query facets: %w", err)
	}

	var facetIDs []string
	for rows.Next() {
		var id string
		if err := rows.Scan(&id); err != nil {
			rows.Close()
			return 0, err
		}
		facetIDs = append(facetIDs, id)
	}
	if err := rows.Err(); err != nil {
		rows.Close()
		return 0, err
	}
	rows.Close()

	count := 0
	for _, id := range facetIDs {
		payload := EmbeddingJobPayload{
			EntityType: "facet",
			EntityID:   id,
		}

		if err := e.queue.Enqueue(queue.EnqueueOptions{
			Type:    JobTypeEmbedding,
			Key:     fmt.Sprintf("embedding:facet:%s", id),
			Payload: payload,
		}); err != nil {
			log.Printf("failed to enqueue facet embedding for %s: %v", id, err)
			continue
		}
		count++
	}

	return count, nil
}

// EnqueuePersonEmbeddings queues embedding jobs for all un-embedded persons
func (e *Engine) EnqueuePersonEmbeddings(ctx context.Context) (int, error) {
	// Find persons without embeddings
	rows, err := e.db.QueryContext(ctx, `
		SELECT p.id FROM persons p
		WHERE NOT EXISTS (
			SELECT 1 FROM embeddings em
			WHERE em.target_type = 'person'
			AND em.target_id = p.id
		)
	`)
	if err != nil {
		return 0, fmt.Errorf("query persons: %w", err)
	}

	var personIDs []string
	for rows.Next() {
		var id string
		if err := rows.Scan(&id); err != nil {
			rows.Close()
			return 0, err
		}
		personIDs = append(personIDs, id)
	}
	if err := rows.Err(); err != nil {
		rows.Close()
		return 0, err
	}
	rows.Close()

	count := 0
	for _, id := range personIDs {
		payload := EmbeddingJobPayload{
			EntityType: "person",
			EntityID:   id,
		}

		if err := e.queue.Enqueue(queue.EnqueueOptions{
			Type:    JobTypeEmbedding,
			Key:     fmt.Sprintf("embedding:person:%s", id),
			Payload: payload,
		}); err != nil {
			log.Printf("failed to enqueue person embedding for %s: %v", id, err)
			continue
		}
		count++
	}

	return count, nil
}

// EnqueueDocumentEmbeddings queues embedding jobs for document heads that are missing
// embeddings or have changed content.
func (e *Engine) EnqueueDocumentEmbeddings(ctx context.Context) (int, error) {
	rows, err := e.db.QueryContext(ctx, `
		SELECT d.doc_key, d.content_hash
		FROM document_heads d
		LEFT JOIN embeddings em
		  ON em.target_type = 'document'
		 AND em.target_id = d.doc_key
		 AND em.model = ?
		WHERE em.id IS NULL
		   OR em.source_text_hash IS NULL
		   OR em.source_text_hash != d.content_hash
	`, e.embeddingModel)
	if err != nil {
		return 0, fmt.Errorf("query documents: %w", err)
	}

	var docKeys []string
	for rows.Next() {
		var docKey string
		var contentHash sql.NullString
		if err := rows.Scan(&docKey, &contentHash); err != nil {
			rows.Close()
			return 0, err
		}
		docKeys = append(docKeys, docKey)
	}
	if err := rows.Err(); err != nil {
		rows.Close()
		return 0, err
	}
	rows.Close()

	count := 0
	for _, docKey := range docKeys {
		payload := EmbeddingJobPayload{
			EntityType: "document",
			EntityID:   docKey,
		}

		if err := e.queue.Enqueue(queue.EnqueueOptions{
			Type:    JobTypeEmbedding,
			Key:     fmt.Sprintf("embedding:document:%s", docKey),
			Payload: payload,
		}); err != nil {
			log.Printf("failed to enqueue document embedding for %s: %v", docKey, err)
			continue
		}
		count++
	}

	return count, nil
}

// AnalysisJobPayload for analysis jobs
type AnalysisJobPayload struct {
	EpisodeID      string `json:"segment_id"` // JSON key kept as segment_id for backward compat with queued jobs
	AnalysisTypeID string `json:"analysis_type_id"`
}

// EmbeddingJobPayload for embedding jobs
type EmbeddingJobPayload struct {
	EntityType string `json:"entity_type"`
	EntityID   string `json:"entity_id"`
}

// handleAnalysisJob processes an analysis job
func (e *Engine) handleAnalysisJob(ctx context.Context, job *queue.Job) error {
	overallStart := time.Now()
	var (
		dbReadDur     time.Duration
		textBuildDur  time.Duration
		apiDur        time.Duration
		parseDur      time.Duration
		dbWriteDur    time.Duration
		outcome       = "error"
		blockedReason string
	)
	defer func() {
		e.metrics.RecordAnalysis(AnalysisMetricEvent{
			DBRead:        dbReadDur,
			TextBuild:     textBuildDur,
			APICall:       apiDur,
			Parse:         parseDur,
			DBWrite:       dbWriteDur,
			Overall:       time.Since(overallStart),
			Outcome:       outcome,
			BlockedReason: blockedReason,
		})
	}()

	var payload AnalysisJobPayload
	if err := json.Unmarshal([]byte(job.PayloadJSON), &payload); err != nil {
		return fmt.Errorf("parse payload: %w", err)
	}

	// Get analysis type config
	t0 := time.Now()
	var promptTemplate, outputType, analysisTypeName string
	var facetsConfigJSON sql.NullString
	err := e.db.QueryRowContext(ctx, `
		SELECT name, prompt_template, output_type, facets_config_json
		FROM analysis_types WHERE id = ?
	`, payload.AnalysisTypeID).Scan(&analysisTypeName, &promptTemplate, &outputType, &facetsConfigJSON)
	if err != nil {
		return fmt.Errorf("get analysis type: %w", err)
	}
	dbReadDur = time.Since(t0)

	// Build episode text (check cache first for pre-encoded text)
	episodeID := payload.EpisodeID
	t1 := time.Now()
	var epText string
	if analysisTypeName == "pii_extraction" {
		var err error
		epText, err = e.buildEpisodeTextMasked(ctx, episodeID)
		if err != nil {
			return fmt.Errorf("build episode text (masked): %w", err)
		}
	} else if analysisTypeName == "turn_quality_v1" {
		var err error
		epText, err = e.buildTurnQualityText(ctx, episodeID)
		if err != nil {
			return fmt.Errorf("build episode text (turn quality): %w", err)
		}
	} else {
		if cached, ok := e.getEpisodeTextCached(episodeID); ok {
			epText = cached
		} else {
			var err error
			epText, err = e.buildEpisodeText(ctx, episodeID)
			if err != nil {
				return fmt.Errorf("build episode text: %w", err)
			}
		}
	}
	textBuildDur = time.Since(t1)

	// Build prompt (template uses {{{segment_text}}} for backward compatibility)
	prompt := strings.ReplaceAll(promptTemplate, "{{{segment_text}}}", epText)

	// Check if analysis already exists (idempotency)
	var existingRunID, existingStatus string
	err = e.db.QueryRowContext(ctx, `
		SELECT id, status FROM analysis_runs
		WHERE analysis_type_id = ? AND episode_id = ?
	`, payload.AnalysisTypeID, episodeID).Scan(&existingRunID, &existingStatus)

	var runID string
	now := time.Now().Unix()

	if err == nil {
		// Existing record found
		if existingStatus == "completed" || existingStatus == "blocked" {
			// Already processed successfully
			outcome = "skipped"
			return nil
		}
		// Update existing record to running
		runID = existingRunID
		_, err = e.db.ExecContext(ctx, `
			UPDATE analysis_runs SET status = 'running', started_at = ?, error_message = NULL
			WHERE id = ?
		`, now, runID)
		if err != nil {
			return fmt.Errorf("update analysis run: %w", err)
		}
	} else {
		// Create new record
		runID = uuid.New().String()
		_, err = e.db.ExecContext(ctx, `
			INSERT INTO analysis_runs (id, analysis_type_id, episode_id, status, started_at, created_at)
			VALUES (?, ?, ?, 'running', ?, ?)
		`, runID, payload.AnalysisTypeID, episodeID, now, now)
		if err != nil {
			return fmt.Errorf("create analysis run: %w", err)
		}
	}

	// Call Gemini (or local extractor for specific analysis types)
	if analysisTypeName == "nexus_cli_invocations" || analysisTypeName == "terminal_invocations" {
		tCustom := time.Now()
		var outputText string
		var err error
		switch analysisTypeName {
		case "nexus_cli_invocations":
			outputText, err = e.buildNexusCLIOutput(ctx, episodeID)
		case "terminal_invocations":
			outputText, err = e.buildTerminalInvocationOutput(ctx, episodeID)
		default:
			err = fmt.Errorf("unsupported local analysis type: %s", analysisTypeName)
		}
		parseDur = time.Since(tCustom)
		if err != nil {
			e.db.ExecContext(ctx, `
				UPDATE analysis_runs SET status = 'failed', error_message = ?, completed_at = ?
				WHERE id = ?
			`, err.Error(), time.Now().Unix(), runID)
			return fmt.Errorf("build local output: %w", err)
		}

		tWrite := time.Now()
		if facetsConfigJSON.Valid {
			if err := e.extractAndPersistFacets(ctx, runID, episodeID, outputText, facetsConfigJSON.String); err != nil {
				log.Printf("warning: facet extraction failed: %v", err)
			}
		}

		_, err = e.db.ExecContext(ctx, `
			UPDATE analysis_runs SET status = 'completed', output_text = ?, completed_at = ?
			WHERE id = ?
		`, outputText, time.Now().Unix(), runID)
		dbWriteDur = time.Since(tWrite)

		if err == nil {
			outcome = "ok"
		}
		return err
	}

	req := &gemini.GenerateContentRequest{
		Contents: []gemini.Content{{
			Role:  "user",
			Parts: []gemini.Part{{Text: prompt}},
		}},
		SafetySettings: []gemini.SafetySetting{
			{Category: "HARM_CATEGORY_HARASSMENT", Threshold: "BLOCK_NONE"},
			{Category: "HARM_CATEGORY_HATE_SPEECH", Threshold: "BLOCK_NONE"},
			{Category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", Threshold: "BLOCK_NONE"},
			{Category: "HARM_CATEGORY_DANGEROUS_CONTENT", Threshold: "BLOCK_NONE"},
		},
	}

	if outputType == "structured" {
		req.GenerationConfig = &gemini.GenerationConfig{
			ResponseMimeType: "application/json",
		}
		if supportsThinkingModel(e.analysisModel) {
			// ThinkingLevel: "minimal" dramatically reduces per-call latency for
			// structured extraction tasks by minimizing the model's "thinking" phase.
			// This is critical for high-throughput bulk processing.
			req.GenerationConfig.ThinkingConfig = &gemini.ThinkingConfig{ThinkingLevel: "minimal"}
		}

		// Add response schema for known analysis types (improves output reliability)
		if schema := getResponseSchema(analysisTypeName); schema != nil {
			req.GenerationConfig.ResponseJsonSchema = schema
		}
	}

	t2 := time.Now()
	resp, err := e.geminiClient.GenerateContent(ctx, e.analysisModel, req)
	apiDur = time.Since(t2)
	if err != nil {
		// Mark as failed
		e.db.ExecContext(ctx, `
			UPDATE analysis_runs SET status = 'failed', error_message = ?, completed_at = ?
			WHERE id = ?
		`, err.Error(), time.Now().Unix(), runID)
		return fmt.Errorf("gemini API: %w", err)
	}

	// Extract and parse output
	t3 := time.Now()
	outputText := extractText(resp)
	parseDur = time.Since(t3)

	if outputText == "" {
		// Check if blocked
		if resp.PromptFeedback != nil && resp.PromptFeedback.BlockReason != "" {
			blockedReason = resp.PromptFeedback.BlockReason
			outcome = "blocked"
			e.db.ExecContext(ctx, `
				UPDATE analysis_runs SET status = 'blocked', blocked_reason = ?, completed_at = ?
				WHERE id = ?
			`, resp.PromptFeedback.BlockReason, time.Now().Unix(), runID)
			return nil // Not an error, just blocked
		}
		e.db.ExecContext(ctx, `
			UPDATE analysis_runs SET status = 'failed', error_message = 'empty output', completed_at = ?
			WHERE id = ?
		`, time.Now().Unix(), runID)
		return fmt.Errorf("empty model output")
	}

	// Persist results
	t4 := time.Now()
	if outputType == "structured" && facetsConfigJSON.Valid {
		if err := e.extractAndPersistFacets(ctx, runID, episodeID, outputText, facetsConfigJSON.String); err != nil {
			log.Printf("warning: facet extraction failed: %v", err)
		}
	}

	// Mark complete
	_, err = e.db.ExecContext(ctx, `
		UPDATE analysis_runs SET status = 'completed', output_text = ?, completed_at = ?
		WHERE id = ?
	`, outputText, time.Now().Unix(), runID)
	dbWriteDur = time.Since(t4)

	if err == nil {
		outcome = "ok"
	}
	return err
}

// handleEmbeddingJob processes an embedding job using the batch API
func (e *Engine) handleEmbeddingJob(ctx context.Context, job *queue.Job) error {
	overallStart := time.Now()
	var (
		textBuildDur time.Duration
		apiDur       time.Duration
		dbWriteDur   time.Duration
		outcome      = "error"
	)
	defer func() {
		e.metrics.RecordEmbedding(EmbeddingMetricEvent{
			TextBuild: textBuildDur,
			APICall:   apiDur,
			DBWrite:   dbWriteDur,
			Overall:   time.Since(overallStart),
			Outcome:   outcome,
		})
	}()

	var payload EmbeddingJobPayload
	if err := json.Unmarshal([]byte(job.PayloadJSON), &payload); err != nil {
		return fmt.Errorf("parse payload: %w", err)
	}

	// Get text to embed (check cache first for segments)
	t0 := time.Now()
	var text string
	var err error
	switch payload.EntityType {
	case "episode":
		if cached, ok := e.getEpisodeTextCached(payload.EntityID); ok {
			text = cached
		} else {
			text, err = e.buildEpisodeText(ctx, payload.EntityID)
		}
	case "facet":
		text, err = e.buildFacetText(ctx, payload.EntityID)
	case "person":
		text, err = e.buildPersonText(ctx, payload.EntityID)
	case "document":
		text, err = e.buildDocumentText(ctx, payload.EntityID)
	default:
		return fmt.Errorf("unsupported entity type: %s", payload.EntityType)
	}
	if err != nil {
		return fmt.Errorf("get entity text: %w", err)
	}
	textBuildDur = time.Since(t0)

	// Skip if no text content (Gemini requires non-empty text)
	text = strings.TrimSpace(text)
	if text == "" {
		// Just complete successfully - no embedding for empty content
		outcome = "skipped"
		return nil
	}

	// Submit to batcher for batched API call (up to 100 embeddings per request)
	t1 := time.Now()
	embedding, err := e.embeddingBatcher.Submit(ctx, payload.EntityType, payload.EntityID, text)
	apiDur = time.Since(t1)
	if err != nil {
		return fmt.Errorf("gemini batch embed: %w", err)
	}

	if len(embedding) == 0 {
		return fmt.Errorf("empty embedding response")
	}

	// Convert to blob
	blob := float64SliceToBlob(embedding)
	embID := uuid.New().String()
	now := time.Now().Unix()
	model := e.embeddingModel
	dimension := len(embedding)
	sourceTextHash := hashText(text)

	// Persist using batch writer if available
	t2 := time.Now()
	apply := func(tx *sql.Tx) error {
		_, err := tx.Exec(`
			INSERT INTO embeddings (
				id, target_type, target_id, model,
				embedding_blob, dimension, source_text_hash, created_at
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
			ON CONFLICT(target_type, target_id, model) DO UPDATE SET
				embedding_blob = excluded.embedding_blob,
				dimension = excluded.dimension,
				source_text_hash = excluded.source_text_hash
		`, embID, payload.EntityType, payload.EntityID, model, blob, dimension, sourceTextHash, now)
		return err
	}

	var writeErr error
	if e.writer != nil {
		writeErr = e.writer.Submit(ctx, apply)
	} else {
		// Fallback: direct write
		tx, err := e.db.BeginTx(ctx, nil)
		if err != nil {
			return fmt.Errorf("begin tx: %w", err)
		}
		defer tx.Rollback()
		if err := apply(tx); err != nil {
			writeErr = err
		} else {
			writeErr = tx.Commit()
		}
	}
	dbWriteDur = time.Since(t2)

	if writeErr == nil {
		outcome = "ok"
	}
	return writeErr
}

// buildEpisodeText builds text representation of an episode
// Format matches Eve's encoding: "Name: message text [Image] [Attachment: file.pdf]"
// Attachments are encoded as [Image], [Video], [Audio], [Sticker], or [Attachment: filename]
func (e *Engine) buildEpisodeText(ctx context.Context, episodeID string) (string, error) {
	// Query events with aggregated attachment info
	rows, err := e.db.QueryContext(ctx, `
		SELECT
			e.id,
			e.content,
			e.timestamp,
			p.canonical_name,
			e.direction,
			(
				SELECT GROUP_CONCAT(
					CASE
						WHEN a.media_type = 'image' THEN 'image'
						WHEN a.media_type = 'video' THEN 'video'
						WHEN a.media_type = 'audio' THEN 'audio'
						WHEN a.media_type = 'sticker' THEN 'sticker'
						ELSE COALESCE(a.filename, 'file')
					END, '|'
				)
				FROM attachments a WHERE a.event_id = e.id
			) as attachments
		FROM episode_events ee
		JOIN events e ON ee.event_id = e.id
		LEFT JOIN event_participants ep ON e.id = ep.event_id AND ep.role = 'sender'
		LEFT JOIN persons p ON ep.person_id = p.id
		WHERE ee.episode_id = ?
		ORDER BY ee.position
	`, episodeID)
	if err != nil {
		return "", err
	}
	defer rows.Close()

	var sb strings.Builder
	for rows.Next() {
		var eventID string
		var content sql.NullString
		var timestamp int64
		var senderName sql.NullString
		var direction string
		var attachments sql.NullString

		if err := rows.Scan(&eventID, &content, &timestamp, &senderName, &direction, &attachments); err != nil {
			return "", err
		}

		name := "Unknown"
		if senderName.Valid && senderName.String != "" {
			name = senderName.String
		}

		// Build message parts
		var parts []string

		// Add text content if present
		if content.Valid && content.String != "" {
			parts = append(parts, content.String)
		}

		// Add attachments
		if attachments.Valid && attachments.String != "" {
			for _, att := range strings.Split(attachments.String, "|") {
				switch att {
				case "image":
					parts = append(parts, "[Image]")
				case "video":
					parts = append(parts, "[Video]")
				case "audio":
					parts = append(parts, "[Audio]")
				case "sticker":
					parts = append(parts, "[Sticker]")
				default:
					parts = append(parts, fmt.Sprintf("[Attachment: %s]", att))
				}
			}
		}

		// Only write line if there's content
		if len(parts) > 0 {
			sb.WriteString(fmt.Sprintf("%s: %s\n", name, strings.Join(parts, " ")))
		}
	}

	return sb.String(), rows.Err()
}

// buildTurnQualityText builds a compact turn-quality input using user messages only.
func (e *Engine) buildTurnQualityText(ctx context.Context, episodeID string) (string, error) {
	rows, err := e.db.QueryContext(ctx, `
		SELECT e.content, e.direction
		FROM episode_events ee
		JOIN events e ON ee.event_id = e.id
		WHERE ee.episode_id = ?
		  AND e.direction IN ('sent', 'received')
		ORDER BY ee.position
	`, episodeID)
	if err != nil {
		return "", err
	}
	defer rows.Close()

	var sb strings.Builder
	for rows.Next() {
		var content sql.NullString
		var direction string
		if err := rows.Scan(&content, &direction); err != nil {
			return "", err
		}
		if !content.Valid || strings.TrimSpace(content.String) == "" {
			continue
		}
		label := "User"
		if direction == "received" {
			label = "Assistant"
		}
		sb.WriteString(fmt.Sprintf("%s: %s\n", label, strings.TrimSpace(content.String)))
	}
	if err := rows.Err(); err != nil {
		return "", err
	}
	return sb.String(), nil
}

// buildEpisodeTextMasked builds text for PII extraction with anonymized speaker labels.
// Speaker labels are metadata only (User/ParticipantN) to avoid name leakage.
func (e *Engine) buildEpisodeTextMasked(ctx context.Context, episodeID string) (string, error) {
	rows, err := e.db.QueryContext(ctx, `
		SELECT
			e.id,
			e.content,
			e.timestamp,
			p.id,
			p.is_me,
			e.direction,
			(
				SELECT GROUP_CONCAT(
					CASE
						WHEN a.media_type = 'image' THEN 'image'
						WHEN a.media_type = 'video' THEN 'video'
						WHEN a.media_type = 'audio' THEN 'audio'
						WHEN a.media_type = 'sticker' THEN 'sticker'
						ELSE COALESCE(a.filename, 'file')
					END, '|'
				)
				FROM attachments a WHERE a.event_id = e.id
			) as attachments
		FROM episode_events ee
		JOIN events e ON ee.event_id = e.id
		LEFT JOIN event_participants ep ON e.id = ep.event_id AND ep.role = 'sender'
		LEFT JOIN persons p ON ep.person_id = p.id
		WHERE ee.episode_id = ?
		ORDER BY ee.position
	`, episodeID)
	if err != nil {
		return "", err
	}
	defer rows.Close()

	var sb strings.Builder
	labels := map[string]string{}
	participantCount := 0

	for rows.Next() {
		var eventID string
		var content sql.NullString
		var timestamp int64
		var senderID sql.NullString
		var isMe sql.NullInt64
		var direction string
		var attachments sql.NullString

		if err := rows.Scan(&eventID, &content, &timestamp, &senderID, &isMe, &direction, &attachments); err != nil {
			return "", err
		}

		name := "Unknown"
		if senderID.Valid && senderID.String != "" {
			if isMe.Valid && isMe.Int64 == 1 {
				name = "User"
			} else if label, ok := labels[senderID.String]; ok {
				name = label
			} else {
				participantCount++
				label := fmt.Sprintf("Participant%d", participantCount)
				labels[senderID.String] = label
				name = label
			}
		}

		var parts []string
		if content.Valid && content.String != "" {
			parts = append(parts, content.String)
		}
		if attachments.Valid && attachments.String != "" {
			for _, att := range strings.Split(attachments.String, "|") {
				switch att {
				case "image":
					parts = append(parts, "[Image]")
				case "video":
					parts = append(parts, "[Video]")
				case "audio":
					parts = append(parts, "[Audio]")
				case "sticker":
					parts = append(parts, "[Sticker]")
				default:
					parts = append(parts, fmt.Sprintf("[Attachment: %s]", att))
				}
			}
		}

		if len(parts) > 0 {
			sb.WriteString(fmt.Sprintf("%s: %s\n", name, strings.Join(parts, " ")))
		}
	}

	return sb.String(), rows.Err()
}

// buildFacetText builds text representation of a facet for embedding
// Format: "facet_type: value" (e.g., "entity: Paris", "topic: travel")
func (e *Engine) buildFacetText(ctx context.Context, facetID string) (string, error) {
	var facetType, value string
	err := e.db.QueryRowContext(ctx, `
		SELECT facet_type, value FROM facets WHERE id = ?
	`, facetID).Scan(&facetType, &value)
	if err != nil {
		return "", fmt.Errorf("get facet: %w", err)
	}

	value = strings.TrimSpace(value)
	if value == "" {
		return "", nil
	}

	return fmt.Sprintf("%s: %s", facetType, value), nil
}

// buildPersonText builds text representation of a person for embedding
// Includes name and all known identities/facts
func (e *Engine) buildPersonText(ctx context.Context, personID string) (string, error) {
	// Get person name
	var canonicalName string
	var displayName sql.NullString
	err := e.db.QueryRowContext(ctx, `
		SELECT canonical_name, display_name FROM persons WHERE id = ?
	`, personID).Scan(&canonicalName, &displayName)
	if err != nil {
		return "", fmt.Errorf("get person: %w", err)
	}

	var sb strings.Builder
	sb.WriteString("person: ")
	sb.WriteString(canonicalName)
	if displayName.Valid && displayName.String != "" && displayName.String != canonicalName {
		sb.WriteString(" (")
		sb.WriteString(displayName.String)
		sb.WriteString(")")
	}

	// Get identities
	rows, err := e.db.QueryContext(ctx, `
		SELECT channel, identifier FROM identities WHERE person_id = ?
	`, personID)
	if err != nil {
		return sb.String(), nil // Return what we have
	}
	defer rows.Close()

	var identities []string
	for rows.Next() {
		var channel, identifier string
		if err := rows.Scan(&channel, &identifier); err != nil {
			continue
		}
		identities = append(identities, fmt.Sprintf("%s: %s", channel, identifier))
	}

	if len(identities) > 0 {
		sb.WriteString(" | identities: ")
		sb.WriteString(strings.Join(identities, ", "))
	}

	return sb.String(), nil
}

// buildDocumentText builds text representation of a document head for embedding.
// Includes title, description, metadata, and full content.
func (e *Engine) buildDocumentText(ctx context.Context, docKey string) (string, error) {
	var title, description, metadataJSON, content sql.NullString
	err := e.db.QueryRowContext(ctx, `
		SELECT d.title, d.description, d.metadata_json, e.content
		FROM document_heads d
		JOIN events e ON d.current_event_id = e.id
		WHERE d.doc_key = ?
	`, docKey).Scan(&title, &description, &metadataJSON, &content)
	if err != nil {
		return "", fmt.Errorf("get document: %w", err)
	}

	var sb strings.Builder
	sb.WriteString("[DOC_KEY] ")
	sb.WriteString(docKey)
	sb.WriteString("\n")
	if title.Valid && strings.TrimSpace(title.String) != "" {
		sb.WriteString("[TITLE] ")
		sb.WriteString(strings.TrimSpace(title.String))
		sb.WriteString("\n")
	}
	if description.Valid && strings.TrimSpace(description.String) != "" {
		sb.WriteString("[DESCRIPTION] ")
		sb.WriteString(strings.TrimSpace(description.String))
		sb.WriteString("\n")
	}
	if metadataJSON.Valid && strings.TrimSpace(metadataJSON.String) != "" {
		sb.WriteString("[METADATA] ")
		sb.WriteString(strings.TrimSpace(metadataJSON.String))
		sb.WriteString("\n")
	}
	if content.Valid && strings.TrimSpace(content.String) != "" {
		sb.WriteString("[CONTENT]\n")
		sb.WriteString(strings.TrimSpace(content.String))
	}

	return sb.String(), nil
}

// extractAndPersistFacets parses structured output and saves facets
func (e *Engine) extractAndPersistFacets(ctx context.Context, runID, episodeID, outputText, facetsConfig string) error {
	// Parse the JSON output (object or array)
	jsonText := extractJSON(outputText)
	if jsonText == "" {
		return fmt.Errorf("no JSON payload found")
	}

	var raw any
	if err := json.Unmarshal([]byte(jsonText), &raw); err != nil {
		return fmt.Errorf("parse JSON: %w", err)
	}

	// Parse facets config
	var config struct {
		Mappings []struct {
			JsonPath  string `json:"json_path"`
			FacetType string `json:"facet_type"`
		} `json:"mappings"`
	}
	if err := json.Unmarshal([]byte(facetsConfig), &config); err != nil {
		return fmt.Errorf("parse facets config: %w", err)
	}

	now := time.Now().Unix()

	var payloads []map[string]any
	switch v := raw.(type) {
	case map[string]any:
		payloads = append(payloads, v)
	case []any:
		for _, item := range v {
			if m, ok := item.(map[string]any); ok {
				payloads = append(payloads, m)
			}
		}
	default:
		return nil
	}
	if len(payloads) == 0 {
		return nil
	}

	// Collect all facets to insert
	type facetRow struct {
		id        string
		facetType string
		value     string
	}
	var facets []facetRow

	for _, mapping := range config.Mappings {
		for _, payload := range payloads {
			values := extractValues(payload, mapping.JsonPath)
			for _, val := range values {
				facets = append(facets, facetRow{
					id:        uuid.New().String(),
					facetType: mapping.FacetType,
					value:     val,
				})
			}
		}
	}

	if len(facets) == 0 {
		return nil
	}

	// Batch insert using TxBatchWriter if available
	apply := func(tx *sql.Tx) error {
		for _, f := range facets {
			_, err := tx.Exec(`
				INSERT INTO facets (id, analysis_run_id, episode_id, facet_type, value, created_at)
				VALUES (?, ?, ?, ?, ?, ?)
			`, f.id, runID, episodeID, f.facetType, f.value, now)
			if err != nil {
				log.Printf("insert facet error: %v", err)
			}
		}
		return nil
	}

	if e.writer != nil {
		return e.writer.Submit(ctx, apply)
	}

	// Fallback: direct write
	tx, err := e.db.BeginTx(ctx, nil)
	if err != nil {
		return fmt.Errorf("begin tx: %w", err)
	}
	defer tx.Rollback()
	if err := apply(tx); err != nil {
		return err
	}
	return tx.Commit()
}

func extractText(resp *gemini.GenerateContentResponse) string {
	if resp == nil || len(resp.Candidates) == 0 {
		return ""
	}
	for _, c := range resp.Candidates {
		for _, p := range c.Content.Parts {
			if strings.TrimSpace(p.Text) != "" {
				return p.Text
			}
		}
	}
	return ""
}

func extractJSON(text string) string {
	s := strings.TrimSpace(text)
	if strings.HasPrefix(s, "```") {
		if idx := strings.Index(s, "\n"); idx != -1 {
			s = s[idx+1:]
		} else {
			return ""
		}
		if end := strings.LastIndex(s, "```"); end != -1 {
			s = s[:end]
		}
		s = strings.TrimSpace(s)
	}

	if strings.HasPrefix(s, "[") {
		if end := strings.LastIndexByte(s, ']'); end > 0 {
			return s[:end+1]
		}
	}
	if strings.HasPrefix(s, "{") {
		if end := strings.LastIndexByte(s, '}'); end > 0 {
			return s[:end+1]
		}
	}

	start := strings.IndexByte(s, '{')
	end := strings.LastIndexByte(s, '}')
	if start != -1 && end > start {
		return s[start : end+1]
	}

	start = strings.IndexByte(s, '[')
	end = strings.LastIndexByte(s, ']')
	if start != -1 && end > start {
		return s[start : end+1]
	}

	return ""
}

// extractValues extracts values from a JSON path like "entities[].name"
func extractValues(data map[string]any, path string) []string {
	parts := strings.Split(path, ".")
	return extractValuesRecursive(data, parts)
}

func extractValuesRecursive(data any, parts []string) []string {
	if len(parts) == 0 {
		switch v := data.(type) {
		case string:
			return []string{v}
		case bool:
			return []string{strconv.FormatBool(v)}
		case float64:
			return []string{strconv.FormatFloat(v, 'f', -1, 64)}
		case float32:
			return []string{strconv.FormatFloat(float64(v), 'f', -1, 32)}
		case int:
			return []string{strconv.Itoa(v)}
		case int64:
			return []string{strconv.FormatInt(v, 10)}
		case json.Number:
			return []string{v.String()}
		default:
			return nil
		}
	}

	part := parts[0]
	remaining := parts[1:]

	// Handle array notation
	if strings.HasSuffix(part, "[]") {
		key := strings.TrimSuffix(part, "[]")
		m, ok := data.(map[string]any)
		if !ok {
			return nil
		}
		arr, ok := m[key].([]any)
		if !ok {
			return nil
		}
		var results []string
		for _, item := range arr {
			results = append(results, extractValuesRecursive(item, remaining)...)
		}
		return results
	}

	// Regular key access
	m, ok := data.(map[string]any)
	if !ok {
		return nil
	}
	return extractValuesRecursive(m[part], remaining)
}

func float64SliceToBlob(values []float64) []byte {
	blob := make([]byte, len(values)*8)
	for i, v := range values {
		bits := math.Float64bits(v)
		for j := 0; j < 8; j++ {
			blob[i*8+j] = byte(bits >> (j * 8))
		}
	}
	return blob
}

func hashText(text string) string {
	sum := sha256.Sum256([]byte(text))
	return hex.EncodeToString(sum[:])
}

func supportsThinkingModel(model string) bool {
	name := strings.ToLower(strings.TrimSpace(model))
	if name == "" {
		return false
	}
	return strings.Contains(name, "thinking") ||
		strings.HasPrefix(name, "gemini-3") ||
		strings.HasPrefix(name, "gemini-2.5")
}

func normalizeAnalysisModel(model string) (string, error) {
	name := strings.TrimSpace(model)
	if name == "" {
		return "gemini-3-flash-preview", nil
	}
	lower := strings.ToLower(name)
	if !strings.HasPrefix(lower, "gemini-3") {
		return "", fmt.Errorf("analysis model must be gemini-3.* (got %s)", name)
	}
	return name, nil
}

// getResponseSchema returns the Gemini response schema for known analysis types
// This enforces JSON structure at the API level for more reliable output parsing
func getResponseSchema(analysisTypeName string) any {
	switch analysisTypeName {
	case "convo-all-v1":
		// Schema for segment analysis: summary, entities, topics, emotions, humor
		return map[string]any{
			"type": "object",
			"properties": map[string]any{
				"summary": map[string]any{
					"type": "string",
				},
				"entities": map[string]any{
					"type": "array",
					"items": map[string]any{
						"type": "string",
					},
				},
				"topics": map[string]any{
					"type": "array",
					"items": map[string]any{
						"type": "string",
					},
				},
				"emotions": map[string]any{
					"type": "array",
					"items": map[string]any{
						"type": "string",
					},
				},
				"humor": map[string]any{
					"type": "array",
					"items": map[string]any{
						"type": "string",
					},
				},
			},
			"required": []string{"summary", "entities", "topics", "emotions", "humor"},
		}
	case "pii_extraction":
		// JSON schema for PII extraction (use responseJsonSchema)
		return map[string]any{
			"type": "object",
			"properties": map[string]any{
				"extraction_metadata": map[string]any{
					"type": "object",
					"properties": map[string]any{
						"channel":                    map[string]any{"type": "string"},
						"primary_contact_name":       map[string]any{"type": "string"},
						"primary_contact_identifier": map[string]any{"type": "string"},
						"user_name":                  map[string]any{"type": "string"},
						"message_count":              map[string]any{"type": "integer"},
						"date_range": map[string]any{
							"type": "object",
							"properties": map[string]any{
								"start": map[string]any{"type": "string"},
								"end":   map[string]any{"type": "string"},
							},
						},
					},
					"additionalProperties": false,
				},
				"facts": map[string]any{
					"type": "array",
					"items": map[string]any{
						"type": "object",
						"properties": map[string]any{
							"subject_kind": map[string]any{
								"type": "string",
								"enum": []string{"user", "primary_contact", "third_party"},
							},
							"subject_ref": map[string]any{"type": "string"},
							"category":    map[string]any{"type": "string"},
							"fact_type":   map[string]any{"type": "string"},
							"value":       map[string]any{"type": "string"},
							"confidence": map[string]any{
								"type": "string",
								"enum": []string{"high", "medium", "low"},
							},
							"evidence":           map[string]any{"type": "string"},
							"self_disclosed":     map[string]any{"type": "boolean"},
							"source":             map[string]any{"type": "string"},
							"related_person_ref": map[string]any{"type": "string"},
							"note":               map[string]any{"type": "string"},
						},
						"required": []string{
							"subject_kind",
							"subject_ref",
							"category",
							"fact_type",
							"value",
							"confidence",
							"evidence",
						},
						"additionalProperties": false,
					},
				},
				"unattributed_facts": map[string]any{
					"type": "array",
					"items": map[string]any{
						"type": "object",
						"properties": map[string]any{
							"fact_type":  map[string]any{"type": "string"},
							"fact_value": map[string]any{"type": "string"},
							"shared_by":  map[string]any{"type": "string"},
							"context":    map[string]any{"type": "string"},
							"possible_attributions": map[string]any{
								"type":  "array",
								"items": map[string]any{"type": "string"},
							},
							"note": map[string]any{"type": "string"},
						},
						"required":             []string{"fact_type", "fact_value"},
						"additionalProperties": false,
					},
				},
			},
			"required": []string{"facts"},
		}
	case "turn_quality_v1":
		return map[string]any{
			"type": "object",
			"properties": map[string]any{
				"feedback": map[string]any{
					"type": "array",
					"items": map[string]any{
						"type": "object",
						"properties": map[string]any{
							"message_index": map[string]any{"type": "integer"},
							"sentiment":     map[string]any{"type": "string"},
							"correction":    map[string]any{"type": "boolean"},
							"frustration":   map[string]any{"type": "boolean"},
							"praise":        map[string]any{"type": "boolean"},
							"confusion":     map[string]any{"type": "boolean"},
							"acceptance":    map[string]any{"type": "boolean"},
							"evidence": map[string]any{
								"type":  "array",
								"items": map[string]any{"type": "string"},
							},
						},
						"required": []string{
							"message_index",
							"sentiment",
							"correction",
							"frustration",
							"praise",
							"confusion",
							"acceptance",
							"evidence",
						},
					},
				},
				"aggregate": map[string]any{
					"type": "object",
					"properties": map[string]any{
						"positive_streak":   map[string]any{"type": "integer"},
						"negative_streak":   map[string]any{"type": "integer"},
						"correction_count":  map[string]any{"type": "integer"},
						"frustration_count": map[string]any{"type": "integer"},
						"praise_count":      map[string]any{"type": "integer"},
						"quality_score":     map[string]any{"type": "number"},
						"quality_band":      map[string]any{"type": "string"},
					},
					"required": []string{
						"positive_streak",
						"negative_streak",
						"correction_count",
						"frustration_count",
						"praise_count",
						"quality_score",
						"quality_band",
					},
				},
			},
			"required": []string{"feedback", "aggregate"},
		}
	default:
		return nil
	}
}
