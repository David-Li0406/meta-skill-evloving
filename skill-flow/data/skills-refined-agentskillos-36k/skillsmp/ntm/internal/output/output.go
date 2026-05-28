package output

import "io"

// Result represents a command result that can be output in multiple formats
type Result interface {
	// Text returns the text representation
	Text(w io.Writer) error
	// JSON returns the JSON-serializable data
	JSON() interface{}
}

// Output writes a Result in the appropriate format
func (f *Formatter) Output(r Result) error {
	if f.IsJSON() {
		return f.JSON(r.JSON())
	}
	return r.Text(f.writer)
}

// OutputData outputs either JSON or calls the text function
func (f *Formatter) OutputData(jsonData interface{}, textFn func(w io.Writer) error) error {
	if f.IsJSON() {
		return f.JSON(jsonData)
	}
	return textFn(f.writer)
}

// OutputOrText outputs JSON if in JSON mode, otherwise calls the text function
func OutputOrText(jsonMode bool, jsonData interface{}, textFn func() error) error {
	if jsonMode {
		return PrintJSON(jsonData)
	}
	return textFn()
}

// DefaultFormatter returns a formatter based on the JSON flag
func DefaultFormatter(jsonFlag bool) *Formatter {
	return New(WithJSON(jsonFlag))
}
