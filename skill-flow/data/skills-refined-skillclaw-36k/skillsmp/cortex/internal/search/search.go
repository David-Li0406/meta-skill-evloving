package search

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"math"
	"sort"
	"strconv"
	"strings"
	"time"
)

const (
	defaultLimit    = 10
	defaultMinScore = 0.0
)

type Searcher struct {
	db       *sql.DB
	embedder Embedder
}

// NewSearcher creates a new searcher with an optional embedder.
func NewSearcher(db *sql.DB, embedder Embedder) *Searcher {
	return &Searcher{db: db, embedder: embedder}
}

// SearchEpisodes performs embedding search over episodes.
func (s *Searcher) SearchEpisodes(ctx context.Context, req EpisodeSearchRequest) (EpisodeSearchResponse, error) {
	if s.db == nil {
		return EpisodeSearchResponse{}, errors.New("search: db is nil")
	}
	query := strings.TrimSpace(req.Query)
	if query == "" {
		return EpisodeSearchResponse{}, errors.New("search: query is required")
	}

	limit := req.Limit
	if limit <= 0 {
		limit = defaultLimit
	}
	minScore := req.MinScore
	if minScore <= 0 {
		minScore = defaultMinScore
	}

	model := strings.TrimSpace(req.Model)
	if model == "" {
		model = "gemini-embedding-001"
	}

	useEmbeddings := req.UseEmbeddings
	if !useEmbeddings {
		useEmbeddings = true
	}

	queryEmbedding := req.QueryEmbedding
	embeddingUsed := false
	if useEmbeddings && len(queryEmbedding) == 0 {
		if s.embedder == nil {
			return EpisodeSearchResponse{}, errors.New("search: embedder not configured")
		}
		embedding, err := s.embedder.Embed(query, model)
		if err != nil || len(embedding) == 0 {
			return EpisodeSearchResponse{}, errors.New("search: failed to generate query embedding")
		}
		queryEmbedding = embedding
	}
	if useEmbeddings && len(queryEmbedding) > 0 {
		embeddingUsed = true
	}

	querySQL := `
		SELECT e.target_id, e.embedding_blob, e.dimension,
		       ep.channel, ep.thread_id, ep.start_time, ep.end_time, ep.event_count,
		       d.name, t.name
		FROM embeddings e
		JOIN episodes ep ON e.target_id = ep.id
		LEFT JOIN episode_definitions d ON ep.definition_id = d.id
		LEFT JOIN threads t ON ep.thread_id = t.id
		WHERE e.target_type = 'episode' AND e.model = ?
	`
	args := []any{model}
	if req.Channel != "" {
		querySQL += " AND ep.channel = ?"
		args = append(args, req.Channel)
	}
	if req.DefinitionName != "" {
		querySQL += " AND d.name = ?"
		args = append(args, req.DefinitionName)
	}

	rows, err := s.db.QueryContext(ctx, querySQL, args...)
	if err != nil {
		return EpisodeSearchResponse{}, err
	}
	defer rows.Close()

	results := make([]EpisodeSearchResult, 0)
	for rows.Next() {
		var (
			episodeID      string
			blob           []byte
			dimension      int
			channel        sql.NullString
			threadID       sql.NullString
			startTime      int64
			endTime        int64
			eventCount     int
			definitionName sql.NullString
			threadName     sql.NullString
		)
		if err := rows.Scan(&episodeID, &blob, &dimension, &channel, &threadID, &startTime, &endTime, &eventCount, &definitionName, &threadName); err != nil {
			continue
		}
		if len(queryEmbedding) == 0 || dimension != len(queryEmbedding) {
			continue
		}
		embedding := blobToFloat64Slice(blob)
		if len(embedding) != len(queryEmbedding) {
			continue
		}

		score := normalizeCosine(cosineSimilarity(queryEmbedding, embedding))
		if score < minScore {
			continue
		}

		result := EpisodeSearchResult{
			EpisodeID:      episodeID,
			DefinitionName: definitionName.String,
			Channel:        channel.String,
			ThreadName:     threadName.String,
			StartTime:      startTime,
			EndTime:        endTime,
			EventCount:     eventCount,
			Score:          score,
		}
		if threadID.Valid {
			result.ThreadID = threadID.String
		}
		results = append(results, result)
	}
	if err := rows.Err(); err != nil {
		return EpisodeSearchResponse{}, err
	}

	sort.Slice(results, func(i, j int) bool {
		return results[i].Score > results[j].Score
	})
	if len(results) > limit {
		results = results[:limit]
	}

	return EpisodeSearchResponse{
		Query:         query,
		Model:         model,
		EmbeddingUsed: embeddingUsed,
		Results:       results,
	}, nil
}

// SearchSegments is a backward-compatible alias for SearchEpisodes.
// Deprecated: Use SearchEpisodes instead.
func (s *Searcher) SearchSegments(ctx context.Context, req SegmentSearchRequest) (SegmentSearchResponse, error) {
	return s.SearchEpisodes(ctx, req)
}

// SearchDocuments performs hybrid search over document_heads + events.
func (s *Searcher) SearchDocuments(ctx context.Context, req DocumentSearchRequest) (DocumentSearchResponse, error) {
	if s.db == nil {
		return DocumentSearchResponse{}, errors.New("search: db is nil")
	}
	query := strings.TrimSpace(req.Query)
	if query == "" {
		return DocumentSearchResponse{}, errors.New("search: query is required")
	}

	limit := req.Limit
	if limit <= 0 {
		limit = defaultLimit
	}
	minScore := req.MinScore
	if minScore <= 0 {
		minScore = defaultMinScore
	}

	model := strings.TrimSpace(req.Model)
	if model == "" {
		model = "gemini-embedding-001"
	}

	useEmbeddings := req.UseEmbeddings
	useLexical := req.UseLexical
	if !useEmbeddings && !useLexical {
		useEmbeddings = true
		useLexical = true
	}

	docs, err := loadDocuments(ctx, s.db, req.Channels)
	if err != nil {
		return DocumentSearchResponse{}, err
	}
	if len(docs) == 0 {
		return DocumentSearchResponse{Query: query, Model: req.Model}, nil
	}

	queryEmbedding := req.QueryEmbedding
	embeddingUsed := false
	if useEmbeddings && len(queryEmbedding) == 0 {
		if s.embedder == nil {
			useEmbeddings = false
		} else {
			embedding, err := s.embedder.Embed(query, model)
			if err != nil || len(embedding) == 0 {
				useEmbeddings = false
			} else {
				queryEmbedding = embedding
			}
		}
	}
	if useEmbeddings && len(queryEmbedding) > 0 {
		embeddingUsed = true
	}

	docEmbeddings := map[string][]float64{}
	if useEmbeddings && len(queryEmbedding) > 0 {
		docEmbeddings, _ = loadDocumentEmbeddings(ctx, s.db, model, req.Channels)
	}

	terms := splitTerms(query)
	lexicalScores := map[string]float64{}
	maxLexical := 0.0
	if useLexical && len(terms) > 0 {
		for _, doc := range docs {
			score := lexicalScore(doc, terms)
			if score > 0 {
				lexicalScores[doc.DocKey] = score
				if score > maxLexical {
					maxLexical = score
				}
			}
		}
	}

	results := make([]DocumentSearchResult, 0, len(docs))
	for _, doc := range docs {
		breakdown := map[string]float64{}

		vectorScore := 0.0
		if useEmbeddings && len(queryEmbedding) > 0 {
			if emb := docEmbeddings[doc.DocKey]; len(emb) > 0 && len(emb) == len(queryEmbedding) {
				vectorScore = normalizeCosine(cosineSimilarity(queryEmbedding, emb))
				breakdown["vector"] = vectorScore
			}
		}

		lexicalScoreRaw := lexicalScores[doc.DocKey]
		lexicalScoreNorm := 0.0
		if maxLexical > 0 {
			lexicalScoreNorm = lexicalScoreRaw / maxLexical
		}
		if lexicalScoreNorm > 0 {
			breakdown["lexical"] = lexicalScoreNorm
		}

		finalScore := 0.0
		switch {
		case useEmbeddings && useLexical:
			finalScore = 0.6*vectorScore + 0.4*lexicalScoreNorm
		case useEmbeddings:
			finalScore = vectorScore
		case useLexical:
			finalScore = lexicalScoreNorm
		}

		if finalScore < minScore {
			continue
		}

		results = append(results, DocumentSearchResult{
			DocKey:         doc.DocKey,
			EventID:        doc.EventID,
			Channel:        doc.Channel,
			Title:          doc.Title,
			Description:    doc.Description,
			Snippet:        doc.Snippet,
			Score:          finalScore,
			ScoreBreakdown: breakdown,
		})
	}

	sort.Slice(results, func(i, j int) bool {
		return results[i].Score > results[j].Score
	})

	if len(results) > limit {
		results = results[:limit]
	}

	if req.TrackRetrieval && len(results) > 0 {
		_ = trackRetrieval(ctx, s.db, query, results)
	}

	return DocumentSearchResponse{
		Query:         query,
		Model:         model,
		EmbeddingUsed: embeddingUsed,
		LexicalUsed:   useLexical,
		Results:       results,
	}, nil
}

type documentRow struct {
	DocKey      string
	EventID     string
	Channel     string
	Title       string
	Description string
	Content     string
	Metadata    map[string]any
	Snippet     string
}

func loadDocuments(ctx context.Context, db *sql.DB, channels []string) ([]documentRow, error) {
	query := `
		SELECT d.doc_key, d.channel, d.title, d.description, d.metadata_json, d.current_event_id, e.content
		FROM document_heads d
		JOIN events e ON e.id = d.current_event_id
	`
	args := []any{}
	if len(channels) > 0 {
		placeholders := make([]string, len(channels))
		for i, ch := range channels {
			placeholders[i] = "?"
			args = append(args, ch)
		}
		query += " WHERE d.channel IN (" + strings.Join(placeholders, ",") + ")"
	}

	rows, err := db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var docs []documentRow
	for rows.Next() {
		var doc documentRow
		var title, description, metadataJSON, content sql.NullString
		if err := rows.Scan(&doc.DocKey, &doc.Channel, &title, &description, &metadataJSON, &doc.EventID, &content); err != nil {
			continue
		}
		if title.Valid {
			doc.Title = title.String
		}
		if description.Valid {
			doc.Description = description.String
		}
		if content.Valid {
			doc.Content = content.String
		}
		if metadataJSON.Valid && metadataJSON.String != "" {
			var meta map[string]any
			if err := json.Unmarshal([]byte(metadataJSON.String), &meta); err == nil {
				doc.Metadata = meta
			}
		}
		doc.Snippet = buildSnippet(doc.Content, 240)
		docs = append(docs, doc)
	}
	return docs, rows.Err()
}

func loadDocumentEmbeddings(ctx context.Context, db *sql.DB, model string, channels []string) (map[string][]float64, error) {
	query := `
		SELECT e.target_id, e.embedding_blob, e.dimension
		FROM embeddings e
		JOIN document_heads d ON d.doc_key = e.target_id
		WHERE e.target_type = 'document' AND e.model = ?
	`
	args := []any{model}
	if len(channels) > 0 {
		placeholders := make([]string, len(channels))
		for i, ch := range channels {
			placeholders[i] = "?"
			args = append(args, ch)
		}
		query += " AND d.channel IN (" + strings.Join(placeholders, ",") + ")"
	}

	rows, err := db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	embeddings := make(map[string][]float64)
	for rows.Next() {
		var docKey string
		var blob []byte
		var dimension int
		if err := rows.Scan(&docKey, &blob, &dimension); err != nil {
			continue
		}
		vector := blobToFloat64Slice(blob)
		if len(vector) != dimension {
			continue
		}
		embeddings[docKey] = vector
	}
	return embeddings, rows.Err()
}

func splitTerms(query string) []string {
	query = strings.ToLower(query)
	parts := strings.FieldsFunc(query, func(r rune) bool {
		return r == ' ' || r == '\n' || r == '\t' || r == ',' || r == '.' || r == ':' || r == ';' || r == '/' || r == '\\'
	})
	var terms []string
	for _, part := range parts {
		part = strings.TrimSpace(part)
		if len(part) >= 2 {
			terms = append(terms, part)
		}
	}
	return terms
}

func lexicalScore(doc documentRow, terms []string) float64 {
	if len(terms) == 0 {
		return 0
	}
	title := strings.ToLower(doc.Title)
	description := strings.ToLower(doc.Description)
	content := strings.ToLower(doc.Content)

	score := 0.0
	for _, term := range terms {
		score += float64(strings.Count(title, term)) * 3.0
		score += float64(strings.Count(description, term)) * 2.0
		score += float64(strings.Count(content, term)) * 1.0
	}
	return score
}

func buildSnippet(content string, maxLen int) string {
	if maxLen <= 0 {
		return ""
	}
	content = strings.TrimSpace(content)
	if len(content) <= maxLen {
		return content
	}
	return content[:maxLen] + "..."
}

func cosineSimilarity(a, b []float64) float64 {
	if len(a) != len(b) || len(a) == 0 {
		return 0
	}
	var dotProduct, normA, normB float64
	for i := range a {
		dotProduct += a[i] * b[i]
		normA += a[i] * a[i]
		normB += b[i] * b[i]
	}
	if normA == 0 || normB == 0 {
		return 0
	}
	return dotProduct / (math.Sqrt(normA) * math.Sqrt(normB))
}

func normalizeCosine(score float64) float64 {
	if score < -1 {
		score = -1
	} else if score > 1 {
		score = 1
	}
	return (score + 1) / 2
}

func blobToFloat64Slice(blob []byte) []float64 {
	if len(blob)%8 != 0 {
		return nil
	}
	values := make([]float64, len(blob)/8)
	for i := 0; i < len(values); i++ {
		bits := uint64(0)
		for j := 0; j < 8; j++ {
			bits |= uint64(blob[i*8+j]) << (j * 8)
		}
		values[i] = math.Float64frombits(bits)
	}
	return values
}

func trackRetrieval(ctx context.Context, db *sql.DB, query string, results []DocumentSearchResult) error {
	if len(results) == 0 {
		return nil
	}
	now := time.Now().Unix()
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	for _, result := range results {
		if result.DocKey == "" {
			continue
		}
		_, _ = tx.ExecContext(ctx, `
			UPDATE document_heads
			SET retrieval_count = retrieval_count + 1,
				last_retrieved_at = ?
			WHERE doc_key = ?
		`, now, result.DocKey)

		_, _ = tx.ExecContext(ctx, `
			INSERT INTO retrieval_log (id, doc_key, event_id, query_text, score, retrieved_at)
			VALUES (?, ?, ?, ?, ?, ?)
		`, newRetrievalID(result.DocKey, now), result.DocKey, result.EventID, query, result.Score, now)
	}

	return tx.Commit()
}

func newRetrievalID(docKey string, ts int64) string {
	// deterministic-ish id: docKey + timestamp. collisions are acceptable to ignore.
	return docKey + ":" + strconv.FormatInt(ts, 10)
}

// EventSearchRequest defines parameters for searching events
type EventSearchRequest struct {
	Query         string    // Search query text
	Channels      []string  // Filter by channels (empty = all)
	ThreadID      string    // Filter by thread_id (empty = all)
	Since         int64     // Filter events after this timestamp (0 = no filter)
	Until         int64     // Filter events before this timestamp (0 = no filter)
	Limit         int       // Max results (default 20)
	MinScore      float64   // Minimum BM25 score (default 0)
	UseEmbeddings bool      // Use vector similarity
	UseFTS        bool      // Use FTS5 full-text search
	Model         string    // Embedding model (default: gemini-embedding-001)
	QueryEmbedding []float64 // Pre-computed query embedding (optional)
}

// EventSearchResult represents a single event search result
type EventSearchResult struct {
	EventID        string             `json:"event_id"`
	Timestamp      int64              `json:"timestamp"`
	Channel        string             `json:"channel"`
	ThreadID       string             `json:"thread_id,omitempty"`
	Snippet        string             `json:"snippet"`
	Score          float64            `json:"score"`
	ScoreBreakdown map[string]float64 `json:"score_breakdown,omitempty"`
}

// EventSearchResponse contains event search results
type EventSearchResponse struct {
	Query         string              `json:"query"`
	Model         string              `json:"model,omitempty"`
	FTSUsed       bool                `json:"fts_used"`
	EmbeddingUsed bool                `json:"embedding_used"`
	Results       []EventSearchResult `json:"results"`
}

// SearchEvents performs hybrid search over events using FTS5 and/or embeddings
func (s *Searcher) SearchEvents(ctx context.Context, req EventSearchRequest) (EventSearchResponse, error) {
	if s.db == nil {
		return EventSearchResponse{}, errors.New("search: db is nil")
	}
	query := strings.TrimSpace(req.Query)
	if query == "" {
		return EventSearchResponse{}, errors.New("search: query is required")
	}

	limit := req.Limit
	if limit <= 0 {
		limit = 20
	}
	minScore := req.MinScore

	model := strings.TrimSpace(req.Model)
	if model == "" {
		model = "gemini-embedding-001"
	}

	useFTS := req.UseFTS
	useEmbeddings := req.UseEmbeddings
	if !useFTS && !useEmbeddings {
		useFTS = true
		useEmbeddings = true
	}

	// FTS5 search
	ftsResults := map[string]float64{}
	ftsSnippets := map[string]string{}
	if useFTS {
		ftsResults, ftsSnippets = s.searchEventsFTS(ctx, query, req.Channels, req.ThreadID, req.Since, req.Until, limit*2)
	}

	// Vector search
	embeddingUsed := false
	vectorResults := map[string]float64{}
	if useEmbeddings {
		queryEmbedding := req.QueryEmbedding
		if len(queryEmbedding) == 0 && s.embedder != nil {
			embedding, err := s.embedder.Embed(query, model)
			if err == nil && len(embedding) > 0 {
				queryEmbedding = embedding
			}
		}
		if len(queryEmbedding) > 0 {
			embeddingUsed = true
			vectorResults = s.searchEventsVector(ctx, queryEmbedding, model, req.Channels, req.ThreadID, req.Since, req.Until, limit*2)
		}
	}

	// Collect all event IDs
	eventIDs := make(map[string]bool)
	for id := range ftsResults {
		eventIDs[id] = true
	}
	for id := range vectorResults {
		eventIDs[id] = true
	}

	// Load event metadata
	eventMeta := s.loadEventMeta(ctx, eventIDs)

	// Compute hybrid scores
	maxFTS := 0.0
	for _, score := range ftsResults {
		if score > maxFTS {
			maxFTS = score
		}
	}

	results := make([]EventSearchResult, 0, len(eventIDs))
	for eventID := range eventIDs {
		meta, ok := eventMeta[eventID]
		if !ok {
			continue
		}

		breakdown := map[string]float64{}

		// Normalize FTS score
		ftsScoreNorm := 0.0
		if maxFTS > 0 {
			ftsScoreNorm = ftsResults[eventID] / maxFTS
		}
		if ftsScoreNorm > 0 {
			breakdown["fts"] = ftsScoreNorm
		}

		// Vector score is already normalized (cosine similarity)
		vectorScore := vectorResults[eventID]
		if vectorScore > 0 {
			breakdown["vector"] = vectorScore
		}

		// Hybrid score: 0.6 vector + 0.4 FTS
		finalScore := 0.0
		switch {
		case useEmbeddings && useFTS:
			finalScore = 0.6*vectorScore + 0.4*ftsScoreNorm
		case useEmbeddings:
			finalScore = vectorScore
		case useFTS:
			finalScore = ftsScoreNorm
		}

		if finalScore < minScore {
			continue
		}

		snippet := ftsSnippets[eventID]
		if snippet == "" {
			snippet = buildSnippet(meta.Content, 240)
		}

		results = append(results, EventSearchResult{
			EventID:        eventID,
			Timestamp:      meta.Timestamp,
			Channel:        meta.Channel,
			ThreadID:       meta.ThreadID,
			Snippet:        snippet,
			Score:          finalScore,
			ScoreBreakdown: breakdown,
		})
	}

	sort.Slice(results, func(i, j int) bool {
		return results[i].Score > results[j].Score
	})

	if len(results) > limit {
		results = results[:limit]
	}

	return EventSearchResponse{
		Query:         query,
		Model:         model,
		FTSUsed:       useFTS && len(ftsResults) > 0,
		EmbeddingUsed: embeddingUsed,
		Results:       results,
	}, nil
}

type eventMeta struct {
	EventID   string
	Timestamp int64
	Channel   string
	ThreadID  string
	Content   string
}

func (s *Searcher) loadEventMeta(ctx context.Context, eventIDs map[string]bool) map[string]eventMeta {
	if len(eventIDs) == 0 {
		return nil
	}

	ids := make([]string, 0, len(eventIDs))
	for id := range eventIDs {
		ids = append(ids, id)
	}

	placeholders := make([]string, len(ids))
	args := make([]any, len(ids))
	for i, id := range ids {
		placeholders[i] = "?"
		args[i] = id
	}

	query := `
		SELECT id, timestamp, channel, thread_id, content
		FROM events
		WHERE id IN (` + strings.Join(placeholders, ",") + `)`

	rows, err := s.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil
	}
	defer rows.Close()

	result := make(map[string]eventMeta)
	for rows.Next() {
		var meta eventMeta
		var threadID, content sql.NullString
		if err := rows.Scan(&meta.EventID, &meta.Timestamp, &meta.Channel, &threadID, &content); err != nil {
			continue
		}
		if threadID.Valid {
			meta.ThreadID = threadID.String
		}
		if content.Valid {
			meta.Content = content.String
		}
		result[meta.EventID] = meta
	}
	return result
}

func (s *Searcher) searchEventsFTS(ctx context.Context, query string, channels []string, threadID string, since, until int64, limit int) (map[string]float64, map[string]string) {
	// Escape query for FTS5 safety
	safeQuery := escapeFTS5Query(query)
	if safeQuery == "" {
		return nil, nil
	}

	ftsQuery := `
		SELECT fts.event_id, bm25(events_fts) as score, snippet(events_fts, 2, '<mark>', '</mark>', '...', 64)
		FROM events_fts fts
		JOIN events e ON e.id = fts.event_id
		WHERE events_fts MATCH ?`
	args := []any{safeQuery}

	if len(channels) > 0 {
		placeholders := make([]string, len(channels))
		for i, ch := range channels {
			placeholders[i] = "?"
			args = append(args, ch)
		}
		ftsQuery += " AND e.channel IN (" + strings.Join(placeholders, ",") + ")"
	}
	if threadID != "" {
		ftsQuery += " AND e.thread_id = ?"
		args = append(args, threadID)
	}
	if since > 0 {
		ftsQuery += " AND e.timestamp >= ?"
		args = append(args, since)
	}
	if until > 0 {
		ftsQuery += " AND e.timestamp <= ?"
		args = append(args, until)
	}

	ftsQuery += " ORDER BY score LIMIT ?"
	args = append(args, limit)

	rows, err := s.db.QueryContext(ctx, ftsQuery, args...)
	if err != nil {
		return nil, nil
	}
	defer rows.Close()

	scores := make(map[string]float64)
	snippets := make(map[string]string)
	for rows.Next() {
		var eventID string
		var score float64
		var snippet sql.NullString
		if err := rows.Scan(&eventID, &score, &snippet); err != nil {
			continue
		}
		// BM25 returns negative scores, lower is better. Negate for consistency.
		scores[eventID] = -score
		if snippet.Valid {
			snippets[eventID] = snippet.String
		}
	}
	return scores, snippets
}

func (s *Searcher) searchEventsVector(ctx context.Context, queryEmbedding []float64, model string, channels []string, threadID string, since, until int64, limit int) map[string]float64 {
	// Load episode embeddings and find matching events
	query := `
		SELECT e.target_id, e.embedding_blob, e.dimension
		FROM embeddings e
		WHERE e.target_type = 'episode' AND e.model = ?`
	args := []any{model}

	rows, err := s.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil
	}
	defer rows.Close()

	type candidate struct {
		episodeID string
		score     float64
	}
	var candidates []candidate

	for rows.Next() {
		var episodeID string
		var blob []byte
		var dim int
		if err := rows.Scan(&episodeID, &blob, &dim); err != nil {
			continue
		}
		if dim != len(queryEmbedding) {
			continue
		}
		embedding := blobToFloat64Slice(blob)
		score := normalizeCosine(cosineSimilarity(queryEmbedding, embedding))
		if score > 0.1 { // Threshold
			candidates = append(candidates, candidate{episodeID: episodeID, score: score})
		}
	}

	if len(candidates) == 0 {
		return nil
	}

	// Sort by score and take top N
	sort.Slice(candidates, func(i, j int) bool {
		return candidates[i].score > candidates[j].score
	})
	if len(candidates) > limit {
		candidates = candidates[:limit]
	}

	// Map episodes to events
	episodeIDs := make([]string, len(candidates))
	episodeScores := make(map[string]float64)
	for i, c := range candidates {
		episodeIDs[i] = c.episodeID
		episodeScores[c.episodeID] = c.score
	}

	// Query episode_events to get event IDs
	placeholders := make([]string, len(episodeIDs))
	args2 := make([]any, len(episodeIDs))
	for i, id := range episodeIDs {
		placeholders[i] = "?"
		args2[i] = id
	}

	eventQuery := `
		SELECT ee.episode_id, ee.event_id, e.channel, e.thread_id, e.timestamp
		FROM episode_events ee
		JOIN events e ON e.id = ee.event_id
		WHERE ee.episode_id IN (` + strings.Join(placeholders, ",") + `)`

	// Add filters
	var filterClauses []string
	if len(channels) > 0 {
		chPlaceholders := make([]string, len(channels))
		for i, ch := range channels {
			chPlaceholders[i] = "?"
			args2 = append(args2, ch)
		}
		filterClauses = append(filterClauses, "e.channel IN ("+strings.Join(chPlaceholders, ",")+")")
	}
	if threadID != "" {
		filterClauses = append(filterClauses, "e.thread_id = ?")
		args2 = append(args2, threadID)
	}
	if since > 0 {
		filterClauses = append(filterClauses, "e.timestamp >= ?")
		args2 = append(args2, since)
	}
	if until > 0 {
		filterClauses = append(filterClauses, "e.timestamp <= ?")
		args2 = append(args2, until)
	}

	if len(filterClauses) > 0 {
		eventQuery += " AND " + strings.Join(filterClauses, " AND ")
	}

	rows2, err := s.db.QueryContext(ctx, eventQuery, args2...)
	if err != nil {
		return nil
	}
	defer rows2.Close()

	// Map event to best episode score
	result := make(map[string]float64)
	for rows2.Next() {
		var episodeID, eventID, channel string
		var threadIDNullable sql.NullString
		var timestamp int64
		if err := rows2.Scan(&episodeID, &eventID, &channel, &threadIDNullable, &timestamp); err != nil {
			continue
		}
		score := episodeScores[episodeID]
		if existing, ok := result[eventID]; !ok || score > existing {
			result[eventID] = score
		}
	}

	return result
}

func escapeFTS5Query(query string) string {
	// Simple escape: wrap each term in quotes if it contains special chars
	// FTS5 special chars: AND OR NOT NEAR ( ) " * - + :
	terms := splitTerms(query)
	escaped := make([]string, 0, len(terms))
	for _, term := range terms {
		term = strings.TrimSpace(term)
		if term == "" {
			continue
		}
		// Quote the term to escape special characters
		escaped = append(escaped, "\""+strings.ReplaceAll(term, "\"", "\"\"")+"\"")
	}
	if len(escaped) == 0 {
		return ""
	}
	// Join with OR for broader matching
	return strings.Join(escaped, " OR ")
}
