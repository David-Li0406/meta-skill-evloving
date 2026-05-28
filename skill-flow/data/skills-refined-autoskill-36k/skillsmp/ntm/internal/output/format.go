// Package output provides unified output formatting for text and JSON output.
// All commands should use this package for consistent output across the CLI.
package output

import (
	"io"
	"os"

	"golang.org/x/term"
)

// Format represents the output format type
type Format int

const (
	// FormatText is human-readable formatted text (default)
	FormatText Format = iota
	// FormatJSON is machine-readable JSON output
	FormatJSON
)

// String returns the string representation of the format
func (f Format) String() string {
	switch f {
	case FormatJSON:
		return "json"
	default:
		return "text"
	}
}

// Formatter handles output formatting for commands
type Formatter struct {
	format Format
	writer io.Writer
	pretty bool // For JSON: whether to indent
}

// New creates a new Formatter with the given options
func New(opts ...Option) *Formatter {
	f := &Formatter{
		format: FormatText,
		writer: os.Stdout,
		pretty: true,
	}
	for _, opt := range opts {
		opt(f)
	}
	return f
}

// Option is a functional option for Formatter
type Option func(*Formatter)

// WithFormat sets the output format
func WithFormat(format Format) Option {
	return func(f *Formatter) {
		f.format = format
	}
}

// WithJSON sets the output format to JSON
func WithJSON(enabled bool) Option {
	return func(f *Formatter) {
		if enabled {
			f.format = FormatJSON
		} else {
			f.format = FormatText
		}
	}
}

// WithWriter sets the output writer
func WithWriter(w io.Writer) Option {
	return func(f *Formatter) {
		f.writer = w
	}
}

// WithPretty sets whether JSON should be indented
func WithPretty(pretty bool) Option {
	return func(f *Formatter) {
		f.pretty = pretty
	}
}

// Format returns the current output format
func (f *Formatter) Format() Format {
	return f.format
}

// IsJSON returns true if the output format is JSON
func (f *Formatter) IsJSON() bool {
	return f.format == FormatJSON
}

// Writer returns the output writer
func (f *Formatter) Writer() io.Writer {
	return f.writer
}

// DetectFormat determines the output format based on environment
// Priority: explicit flag > env var > pipe detection > default text
func DetectFormat(jsonFlag bool) Format {
	// 1. Explicit --json flag takes highest priority
	if jsonFlag {
		return FormatJSON
	}

	// 2. Check NTM_OUTPUT_FORMAT environment variable
	// Supports: "json", "text"
	if envFormat := os.Getenv("NTM_OUTPUT_FORMAT"); envFormat != "" {
		switch envFormat {
		case "json", "JSON":
			return FormatJSON
		case "text", "TEXT":
			return FormatText
		}
	}

	// 3. Auto-detect: if stdout is not a terminal, use JSON
	// This makes piping work better: ntm status myproj | jq .
	if !IsTerminal() {
		return FormatJSON
	}

	// 4. Default to text for interactive terminals
	return FormatText
}

// IsTerminal returns true if stdout is a terminal
func IsTerminal() bool {
	return term.IsTerminal(int(os.Stdout.Fd()))
}
