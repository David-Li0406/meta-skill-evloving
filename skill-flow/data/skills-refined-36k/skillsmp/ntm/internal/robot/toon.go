// Package robot provides machine-readable output for AI agents.
// toon.go implements the TOON (Token-Oriented Object Notation) encoder.
//
// TOON is a token-efficient serialization format designed for LLM consumption.
// This implementation supports:
//   - Uniform arrays of objects (tabular format)
//   - Primitive values (strings, numbers, booleans, null)
//   - Simple objects with scalar fields
//
// For unsupported shapes (deeply nested structures), the encoder returns an error.
// Use FormatAuto to fall back to JSON for such payloads.
//
// Reference: https://github.com/toon-format/spec
package robot

import (
	"bytes"
	"encoding/json"
	"fmt"
	"reflect"
	"sort"
	"strconv"
	"strings"
)

// toonEncode encodes a payload as TOON format.
// Returns an error for unsupported payload shapes.
func toonEncode(payload any, delimiter string) (string, error) {
	if payload == nil {
		return "null\n", nil
	}

	v := reflect.ValueOf(payload)

	// Dereference pointers
	for v.Kind() == reflect.Ptr {
		if v.IsNil() {
			return "null\n", nil
		}
		v = v.Elem()
	}

	enc := &toonEncoder{delimiter: delimiter}

	switch v.Kind() {
	case reflect.Slice, reflect.Array:
		return enc.renderArray(v)
	case reflect.Map, reflect.Struct:
		return enc.renderObject(v, 0)
	case reflect.String:
		return enc.encodeString(v.String()) + "\n", nil
	case reflect.Bool:
		if v.Bool() {
			return "true\n", nil
		}
		return "false\n", nil
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
		return strconv.FormatInt(v.Int(), 10) + "\n", nil
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
		return strconv.FormatUint(v.Uint(), 10) + "\n", nil
	case reflect.Float32, reflect.Float64:
		return enc.formatFloat(v.Float()) + "\n", nil
	default:
		return "", fmt.Errorf("TOON: unsupported type %s", v.Kind())
	}
}

// toonEncoder holds encoding state.
type toonEncoder struct {
	delimiter string
}

// renderArray renders a slice/array as TOON tabular format.
func (enc *toonEncoder) renderArray(v reflect.Value) (string, error) {
	length := v.Len()
	if length == 0 {
		return "[]\n", nil
	}

	// Check if it's an array of objects (maps or structs)
	first := v.Index(0)
	for first.Kind() == reflect.Ptr || first.Kind() == reflect.Interface {
		if first.IsNil() {
			return "", fmt.Errorf("TOON: nil element in array")
		}
		first = first.Elem()
	}

	if first.Kind() == reflect.Map || first.Kind() == reflect.Struct {
		return enc.renderTabular(v)
	}

	// Primitive array: inline format
	var buf strings.Builder
	buf.WriteString(fmt.Sprintf("[%d]:", length))
	for i := 0; i < length; i++ {
		elem := v.Index(i)
		encoded, err := enc.encodeValue(elem)
		if err != nil {
			return "", err
		}
		if i > 0 {
			buf.WriteString(enc.delimiter)
		}
		buf.WriteString(encoded)
	}
	buf.WriteString("\n")
	return buf.String(), nil
}

// renderTabular renders a uniform array of objects in TOON tabular format.
func (enc *toonEncoder) renderTabular(v reflect.Value) (string, error) {
	length := v.Len()
	if length == 0 {
		return "[]\n", nil
	}

	// Extract field names from the first element
	fields, err := enc.extractFields(v.Index(0))
	if err != nil {
		return "", err
	}
	if len(fields) == 0 {
		return "", fmt.Errorf("TOON: empty object in array")
	}

	// Sort fields for deterministic output
	sort.Strings(fields)

	// Check if tab delimiter is safe (no tabs/newlines in values)
	safeDelim := enc.delimiter
	if enc.delimiter == "\t" && !enc.isTabSafe(v, fields) {
		safeDelim = ","
	}

	var buf strings.Builder

	// Header: key[count]{field1,field2,...}:
	buf.WriteString(fmt.Sprintf("[%d]{%s}:\n", length, strings.Join(fields, ",")))

	// Rows
	for i := 0; i < length; i++ {
		elem := v.Index(i)
		for elem.Kind() == reflect.Ptr || elem.Kind() == reflect.Interface {
			if elem.IsNil() {
				return "", fmt.Errorf("TOON: nil element at index %d", i)
			}
			elem = elem.Elem()
		}

		buf.WriteString(" ") // TOON requires single space indent for rows
		for j, field := range fields {
			val, err := enc.getFieldValue(elem, field)
			if err != nil {
				return "", err
			}
			encoded, err := enc.encodeValue(val)
			if err != nil {
				return "", fmt.Errorf("TOON: field %q at index %d: %w", field, i, err)
			}
			if j > 0 {
				buf.WriteString(safeDelim)
			}
			buf.WriteString(encoded)
		}
		buf.WriteString("\n")
	}

	return buf.String(), nil
}

// renderObject renders a map or struct as TOON key-value pairs.
func (enc *toonEncoder) renderObject(v reflect.Value, indent int) (string, error) {
	fields, err := enc.extractFields(v)
	if err != nil {
		return "", err
	}
	if len(fields) == 0 {
		return "{}\n", nil
	}

	// Sort fields for deterministic output
	sort.Strings(fields)

	var buf strings.Builder
	indentStr := strings.Repeat("  ", indent)

	for _, field := range fields {
		val, err := enc.getFieldValue(v, field)
		if err != nil {
			return "", err
		}

		// Handle nil/invalid values
		if !val.IsValid() {
			buf.WriteString(indentStr + field + ": null\n")
			continue
		}

		for val.Kind() == reflect.Ptr || val.Kind() == reflect.Interface {
			if val.IsNil() {
				buf.WriteString(indentStr + field + ": null\n")
				val = reflect.Value{} // mark as handled
				break
			}
			val = val.Elem()
		}

		if !val.IsValid() {
			continue // already handled as null
		}

		// Check if value is complex (needs nested rendering)
		if val.Kind() == reflect.Slice || val.Kind() == reflect.Array {
			nested, err := enc.renderArray(val)
			if err != nil {
				return "", err
			}
			buf.WriteString(indentStr + field + nested)
		} else if val.Kind() == reflect.Map || val.Kind() == reflect.Struct {
			buf.WriteString(indentStr + field + ":\n")
			nested, err := enc.renderObject(val, indent+1)
			if err != nil {
				return "", err
			}
			buf.WriteString(nested)
		} else {
			encoded, err := enc.encodeValue(val)
			if err != nil {
				return "", err
			}
			buf.WriteString(indentStr + field + ": " + encoded + "\n")
		}
	}

	return buf.String(), nil
}

// extractFields returns the field names from a map or struct.
func (enc *toonEncoder) extractFields(v reflect.Value) ([]string, error) {
	for v.Kind() == reflect.Ptr || v.Kind() == reflect.Interface {
		if v.IsNil() {
			return nil, nil
		}
		v = v.Elem()
	}

	switch v.Kind() {
	case reflect.Map:
		keys := v.MapKeys()
		fields := make([]string, len(keys))
		for i, key := range keys {
			if key.Kind() != reflect.String {
				return nil, fmt.Errorf("TOON: non-string map key")
			}
			fields[i] = key.String()
		}
		return fields, nil
	case reflect.Struct:
		t := v.Type()
		fields := make([]string, 0, t.NumField())
		for i := 0; i < t.NumField(); i++ {
			f := t.Field(i)
			if !f.IsExported() {
				continue
			}
			name := f.Tag.Get("json")
			if name == "-" {
				continue
			}
			if idx := strings.Index(name, ","); idx != -1 {
				name = name[:idx]
			}
			if name == "" {
				name = f.Name
			}
			fields = append(fields, name)
		}
		return fields, nil
	default:
		return nil, fmt.Errorf("TOON: expected map or struct, got %s", v.Kind())
	}
}

// getFieldValue retrieves a field value from a map or struct.
func (enc *toonEncoder) getFieldValue(v reflect.Value, field string) (reflect.Value, error) {
	for v.Kind() == reflect.Ptr || v.Kind() == reflect.Interface {
		if v.IsNil() {
			return reflect.Value{}, nil
		}
		v = v.Elem()
	}

	switch v.Kind() {
	case reflect.Map:
		return v.MapIndex(reflect.ValueOf(field)), nil
	case reflect.Struct:
		// First try JSON tag
		t := v.Type()
		for i := 0; i < t.NumField(); i++ {
			f := t.Field(i)
			name := f.Tag.Get("json")
			if idx := strings.Index(name, ","); idx != -1 {
				name = name[:idx]
			}
			if name == "" {
				name = f.Name
			}
			if name == field {
				return v.Field(i), nil
			}
		}
		return reflect.Value{}, fmt.Errorf("field %q not found", field)
	default:
		return reflect.Value{}, fmt.Errorf("expected map or struct")
	}
}

// encodeValue encodes a single value as TOON.
func (enc *toonEncoder) encodeValue(v reflect.Value) (string, error) {
	if !v.IsValid() {
		return "null", nil
	}

	for v.Kind() == reflect.Ptr || v.Kind() == reflect.Interface {
		if v.IsNil() {
			return "null", nil
		}
		v = v.Elem()
	}

	switch v.Kind() {
	case reflect.String:
		return enc.encodeString(v.String()), nil
	case reflect.Bool:
		if v.Bool() {
			return "true", nil
		}
		return "false", nil
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
		return strconv.FormatInt(v.Int(), 10), nil
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
		return strconv.FormatUint(v.Uint(), 10), nil
	case reflect.Float32, reflect.Float64:
		return enc.formatFloat(v.Float()), nil
	case reflect.Map, reflect.Struct, reflect.Slice, reflect.Array:
		// Nested complex types in tabular rows: fall back to JSON inline
		var buf bytes.Buffer
		encoder := json.NewEncoder(&buf)
		encoder.SetEscapeHTML(false)
		if err := encoder.Encode(v.Interface()); err != nil {
			return "", fmt.Errorf("encoding nested value: %w", err)
		}
		// Remove trailing newline from JSON
		s := strings.TrimSuffix(buf.String(), "\n")
		return enc.encodeString(s), nil
	default:
		return "", fmt.Errorf("unsupported value type %s", v.Kind())
	}
}

// encodeString encodes a string, quoting only when necessary.
// Unquoted strings match: ^[A-Za-z_][A-Za-z0-9_]*$
func (enc *toonEncoder) encodeString(s string) string {
	if s == "" {
		return `""`
	}

	// Check if it needs quoting
	needsQuote := false
	if !toonIsIdentifierStart(rune(s[0])) {
		needsQuote = true
	} else {
		for _, c := range s[1:] {
			if !toonIsIdentifierChar(c) {
				needsQuote = true
				break
			}
		}
	}

	// Also quote if it looks like a TOON keyword or number
	if !needsQuote {
		switch s {
		case "true", "false", "null":
			needsQuote = true
		}
	}

	if !needsQuote {
		return s
	}

	// Quote and escape
	var buf strings.Builder
	buf.WriteByte('"')
	for _, c := range s {
		switch c {
		case '\\':
			buf.WriteString(`\\`)
		case '"':
			buf.WriteString(`\"`)
		case '\n':
			buf.WriteString(`\n`)
		case '\r':
			buf.WriteString(`\r`)
		case '\t':
			buf.WriteString(`\t`)
		default:
			buf.WriteRune(c)
		}
	}
	buf.WriteByte('"')
	return buf.String()
}

// formatFloat formats a float without scientific notation.
func (enc *toonEncoder) formatFloat(f float64) string {
	// Use 'f' format to avoid scientific notation
	s := strconv.FormatFloat(f, 'f', -1, 64)
	// Remove trailing zeros after decimal point
	if strings.Contains(s, ".") {
		s = strings.TrimRight(s, "0")
		s = strings.TrimRight(s, ".")
	}
	return s
}

// isTabSafe checks if tab delimiter is safe for all values.
func (enc *toonEncoder) isTabSafe(v reflect.Value, fields []string) bool {
	for i := 0; i < v.Len(); i++ {
		elem := v.Index(i)
		for elem.Kind() == reflect.Ptr || elem.Kind() == reflect.Interface {
			if elem.IsNil() {
				continue
			}
			elem = elem.Elem()
		}
		for _, field := range fields {
			val, err := enc.getFieldValue(elem, field)
			if err != nil {
				continue
			}
			if val.Kind() == reflect.String {
				s := val.String()
				if strings.ContainsAny(s, "\t\n\r") {
					return false
				}
			}
		}
	}
	return true
}

func toonIsIdentifierStart(c rune) bool {
	return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_'
}

func toonIsIdentifierChar(c rune) bool {
	return toonIsIdentifierStart(c) || (c >= '0' && c <= '9')
}
