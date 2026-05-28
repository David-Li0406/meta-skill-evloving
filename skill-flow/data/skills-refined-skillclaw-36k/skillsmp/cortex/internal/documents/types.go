package documents

// DocumentInput describes a document-like object to be stored as an event.
// docKey is the stable identifier (ex: "skill:gog").
type DocumentInput struct {
	DocKey        string
	Channel       string
	Title         string
	Description   string
	Content       string
	Metadata      map[string]any
	SourceAdapter string
	Timestamp     int64
}

// DocumentResult reports how the upsert was applied.
type DocumentResult struct {
	DocKey          string
	EventID         string
	ContentHash     string
	Created         bool
	Updated         bool
	Skipped         bool
	PreviousEventID string
	Reason          string
}
