package compute

import (
	"encoding/json"
	"sync"
	"time"
)

// JobMetrics captures timing and outcome metrics for job processing.
// Lightweight and aggregated (no per-job data stored).
type JobMetrics struct {
	mu sync.Mutex

	// Analysis job metrics
	AnalysisTotal   int
	AnalysisOK      int
	AnalysisBlocked int
	AnalysisError   int

	AnalysisDBRead   time.Duration
	AnalysisTextBuild time.Duration
	AnalysisAPICall  time.Duration
	AnalysisParse    time.Duration
	AnalysisDBWrite  time.Duration
	AnalysisOverall  time.Duration

	BlockedReasonCounts map[string]int

	// Embedding job metrics
	EmbeddingTotal   int
	EmbeddingOK      int
	EmbeddingSkipped int // Empty text
	EmbeddingError   int

	EmbeddingTextBuild time.Duration
	EmbeddingAPICall   time.Duration
	EmbeddingDBWrite   time.Duration
	EmbeddingOverall   time.Duration
}

// NewJobMetrics creates a new metrics collector
func NewJobMetrics() *JobMetrics {
	return &JobMetrics{
		BlockedReasonCounts: make(map[string]int),
	}
}

// AnalysisMetricEvent captures a single analysis job's timing
type AnalysisMetricEvent struct {
	DBRead    time.Duration
	TextBuild time.Duration
	APICall   time.Duration
	Parse     time.Duration
	DBWrite   time.Duration
	Overall   time.Duration

	Outcome       string // "ok" | "blocked" | "error"
	BlockedReason string
}

// RecordAnalysis records metrics for an analysis job
func (m *JobMetrics) RecordAnalysis(ev AnalysisMetricEvent) {
	if m == nil {
		return
	}
	m.mu.Lock()
	defer m.mu.Unlock()

	m.AnalysisTotal++
	switch ev.Outcome {
	case "ok":
		m.AnalysisOK++
	case "blocked":
		m.AnalysisBlocked++
		if ev.BlockedReason != "" {
			m.BlockedReasonCounts[ev.BlockedReason]++
		}
	default:
		m.AnalysisError++
	}

	m.AnalysisDBRead += ev.DBRead
	m.AnalysisTextBuild += ev.TextBuild
	m.AnalysisAPICall += ev.APICall
	m.AnalysisParse += ev.Parse
	m.AnalysisDBWrite += ev.DBWrite
	m.AnalysisOverall += ev.Overall
}

// EmbeddingMetricEvent captures a single embedding job's timing
type EmbeddingMetricEvent struct {
	TextBuild time.Duration
	APICall   time.Duration
	DBWrite   time.Duration
	Overall   time.Duration

	Outcome string // "ok" | "skipped" | "error"
}

// RecordEmbedding records metrics for an embedding job
func (m *JobMetrics) RecordEmbedding(ev EmbeddingMetricEvent) {
	if m == nil {
		return
	}
	m.mu.Lock()
	defer m.mu.Unlock()

	m.EmbeddingTotal++
	switch ev.Outcome {
	case "ok":
		m.EmbeddingOK++
	case "skipped":
		m.EmbeddingSkipped++
	default:
		m.EmbeddingError++
	}

	m.EmbeddingTextBuild += ev.TextBuild
	m.EmbeddingAPICall += ev.APICall
	m.EmbeddingDBWrite += ev.DBWrite
	m.EmbeddingOverall += ev.Overall
}

// Snapshot returns a JSON-serializable snapshot of current metrics
func (m *JobMetrics) Snapshot() map[string]any {
	if m == nil {
		return nil
	}
	m.mu.Lock()
	defer m.mu.Unlock()

	div := func(d time.Duration, n int) float64 {
		if n <= 0 {
			return 0
		}
		return float64(d.Milliseconds()) / float64(n)
	}

	return map[string]any{
		"analysis": map[string]any{
			"total":   m.AnalysisTotal,
			"ok":      m.AnalysisOK,
			"blocked": m.AnalysisBlocked,
			"error":   m.AnalysisError,
			"avg_ms": map[string]any{
				"db_read":    div(m.AnalysisDBRead, m.AnalysisTotal),
				"text_build": div(m.AnalysisTextBuild, m.AnalysisTotal),
				"api_call":   div(m.AnalysisAPICall, m.AnalysisTotal),
				"parse":      div(m.AnalysisParse, m.AnalysisTotal),
				"db_write":   div(m.AnalysisDBWrite, m.AnalysisTotal),
				"overall":    div(m.AnalysisOverall, m.AnalysisTotal),
			},
			"blocked_reasons": m.BlockedReasonCounts,
		},
		"embedding": map[string]any{
			"total":   m.EmbeddingTotal,
			"ok":      m.EmbeddingOK,
			"skipped": m.EmbeddingSkipped,
			"error":   m.EmbeddingError,
			"avg_ms": map[string]any{
				"text_build": div(m.EmbeddingTextBuild, m.EmbeddingTotal),
				"api_call":   div(m.EmbeddingAPICall, m.EmbeddingTotal),
				"db_write":   div(m.EmbeddingDBWrite, m.EmbeddingTotal),
				"overall":    div(m.EmbeddingOverall, m.EmbeddingTotal),
			},
		},
	}
}

// SnapshotJSON returns a JSON representation of the metrics
func (m *JobMetrics) SnapshotJSON() json.RawMessage {
	if m == nil {
		return json.RawMessage("null")
	}
	b, _ := json.Marshal(m.Snapshot())
	return b
}
