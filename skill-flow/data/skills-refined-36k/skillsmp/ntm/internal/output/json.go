package output

import (
	"encoding/json"
	"io"
	"os"
	"time"
)

// JSON outputs data as JSON to the formatter's writer
func (f *Formatter) JSON(v interface{}) error {
	return WriteJSON(f.writer, v, f.pretty)
}

// WriteJSON writes data as JSON to the given writer
func WriteJSON(w io.Writer, v interface{}, pretty bool) error {
	encoder := json.NewEncoder(w)
	if pretty {
		encoder.SetIndent("", "  ")
	}
	return encoder.Encode(v)
}

// PrintJSON writes data as JSON to stdout
func PrintJSON(v interface{}) error {
	return WriteJSON(os.Stdout, v, true)
}

// PrintJSONCompact writes data as compact JSON to stdout
func PrintJSONCompact(v interface{}) error {
	return WriteJSON(os.Stdout, v, false)
}

// MarshalJSON marshals data to JSON bytes
func MarshalJSON(v interface{}, pretty bool) ([]byte, error) {
	if pretty {
		return json.MarshalIndent(v, "", "  ")
	}
	return json.Marshal(v)
}

// Timestamp returns the current UTC time formatted for JSON output
func Timestamp() time.Time {
	return time.Now().UTC()
}

// FormatTime formats a time for JSON output as ISO 8601
func FormatTime(t time.Time) string {
	return t.UTC().Format(time.RFC3339)
}

// ParseTime parses an ISO 8601 timestamp
func ParseTime(s string) (time.Time, error) {
	return time.Parse(time.RFC3339, s)
}
