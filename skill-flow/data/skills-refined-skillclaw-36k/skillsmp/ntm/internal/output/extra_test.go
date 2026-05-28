package output

import (
	"bytes"
	"encoding/json"
	"errors"
	"os"
	"strings"
	"testing"
	"time"
)

// Helper to capture stdout/stderr
func captureOutput(f func()) (string, string) {
	oldStdout := os.Stdout
	oldStderr := os.Stderr
	rOut, wOut, _ := os.Pipe()
	rErr, wErr, _ := os.Pipe()
	os.Stdout = wOut
	os.Stderr = wErr

	f()

	wOut.Close()
	wErr.Close()
	os.Stdout = oldStdout
	os.Stderr = oldStderr

	var bufOut bytes.Buffer
	var bufErr bytes.Buffer
	bufOut.ReadFrom(rOut)
	bufErr.ReadFrom(rErr)
	return bufOut.String(), bufErr.String()
}

func TestFormatterErrors(t *testing.T) {
	var buf bytes.Buffer
	f := New(WithWriter(&buf), WithJSON(true))

	// Error
	err := errors.New("test error")
	f.Error(err)
	var resp ErrorResponse
	if err := json.Unmarshal(buf.Bytes(), &resp); err != nil {
		t.Fatalf("JSON invalid: %v", err)
	}
	if resp.Error != "test error" {
		t.Errorf("Error() = %q, want 'test error'", resp.Error)
	}

	// ErrorMsg
	buf.Reset()
	f.ErrorMsg("msg error")
	if err := json.Unmarshal(buf.Bytes(), &resp); err != nil {
		t.Fatalf("JSON invalid: %v", err)
	}
	if resp.Error != "msg error" {
		t.Errorf("ErrorMsg() = %q, want 'msg error'", resp.Error)
	}

	// ErrorWithCode
	buf.Reset()
	f.ErrorWithCode("CODE", "msg")
	if err := json.Unmarshal(buf.Bytes(), &resp); err != nil {
		t.Fatalf("JSON invalid: %v", err)
	}
	if resp.Code != "CODE" {
		t.Errorf("ErrorWithCode() code = %q, want CODE", resp.Code)
	}
}

func TestPrintError(t *testing.T) {
	// Text mode
	_, stderr := captureOutput(func() {
		PrintError(errors.New("oops"), false)
	})
	if stderr != "Error: oops\n" {
		t.Errorf("PrintError text mode = %q, want 'Error: oops\n'", stderr)
	}

	// JSON mode
	stdout, _ := captureOutput(func() {
		PrintError(errors.New("json error"), true)
	})

	var resp ErrorResponse
	if err := json.Unmarshal([]byte(stdout), &resp); err != nil {
		t.Errorf("PrintError JSON invalid: %v", err)
	}
	if resp.Error != "json error" {
		t.Errorf("PrintError JSON error = %q, want 'json error'", resp.Error)
	}
}

func TestTimestamped(t *testing.T) {
	ts := NewTimestamped()
	if ts.GeneratedAt.IsZero() {
		t.Error("NewTimestamped() time is zero")
	}
	// Check if recent
	if time.Since(ts.GeneratedAt) > time.Second {
		t.Error("NewTimestamped() time is too old")
	}
}

func TestPrintJSON(t *testing.T) {
	data := map[string]string{"foo": "bar"}

	stdout, _ := captureOutput(func() {
		if err := PrintJSON(data); err != nil {
			t.Fatal(err)
		}
	})

	var resp map[string]string
	if err := json.Unmarshal([]byte(stdout), &resp); err != nil {
		t.Fatalf("PrintJSON output invalid: %v", err)
	}
	if resp["foo"] != "bar" {
		t.Errorf("PrintJSON foo = %q, want bar", resp["foo"])
	}
}

func TestOutputOrText(t *testing.T) {
	data := map[string]string{"key": "val"}
	textCalled := false
	textFn := func() error {
		textCalled = true
		return nil
	}

	// JSON mode
	// Note: OutputOrText writes to stdout for JSON
	captureOutput(func() {
		OutputOrText(true, data, textFn)
	})
	if textCalled {
		t.Error("OutputOrText(true) called textFn")
	}

	// Text mode
	OutputOrText(false, data, textFn)
	if !textCalled {
		t.Error("OutputOrText(false) did not call textFn")
	}
}

func TestFormatterMethods(t *testing.T) {
	f := New(WithPretty(true))

	// Writer
	if f.Writer() != os.Stdout {
		// Default is stdout
	}

	// Format
	if f.Format() != FormatText {
		t.Error("Expected FormatText default")
	}
}

func TestTextHelpersExtended(t *testing.T) {
	// Text
	var buf bytes.Buffer
	f := New(WithWriter(&buf))

	f.Text("hello")
	if buf.String() != "hello" {
		t.Errorf("Text() = %q, want hello", buf.String())
	}

	buf.Reset()
	f.Line()
	if buf.String() != "\n" {
		t.Errorf("Line() = %q, want newline", buf.String())
	}

	buf.Reset()
	f.Println("world")
	if buf.String() != "world\n" {
		t.Errorf("Println() = %q, want world\\n", buf.String())
	}

	buf.Reset()
	f.Printf("hello %s", "world")
	if buf.String() != "hello world" {
		t.Errorf("Printf() = %q, want hello world", buf.String())
	}
}

func TestTimestampFormat(t *testing.T) {
	now := time.Date(2025, 1, 1, 12, 0, 0, 0, time.UTC)
	s := FormatTime(now)
	if s != "2025-01-01T12:00:00Z" {
		t.Errorf("FormatTime() = %q", s)
	}

	parsed, err := ParseTime(s)
	if err != nil {
		t.Errorf("ParseTime() error: %v", err)
	}
	if !parsed.Equal(now) {
		t.Errorf("ParseTime() = %v, want %v", parsed, now)
	}
}

func TestDefaultFormatter(t *testing.T) {
	f := DefaultFormatter(true)
	if !f.IsJSON() {
		t.Error("DefaultFormatter(true) should be JSON")
	}

	f = DefaultFormatter(false)
	if f.IsJSON() {
		t.Error("DefaultFormatter(false) should be Text")
	}
}

func TestDetectFormatEnv(t *testing.T) {
	// Env var JSON
	os.Setenv("NTM_OUTPUT_FORMAT", "json")
	if f := DetectFormat(false); f != FormatJSON {
		t.Error("DetectFormat(false) with env=json should be JSON")
	}

	// Env var TEXT
	os.Setenv("NTM_OUTPUT_FORMAT", "text")
	if f := DetectFormat(false); f != FormatText {
		t.Error("DetectFormat(false) with env=text should be Text")
	}
	os.Unsetenv("NTM_OUTPUT_FORMAT")
}

func TestTableAlignment(t *testing.T) {
	var buf bytes.Buffer
	tbl := NewTable(&buf, "Col1", "Col2")
	tbl.AddRow("Short", "Long Value Here")
	tbl.Render()

	output := buf.String()
	if !strings.Contains(output, "Col1") {
		t.Error("Table missing header Col1")
	}
	// Check for padding/alignment (heuristic)
	if !strings.Contains(output, "Short ") { // Should have padding
		t.Error("Table row padding seems missing")
	}
}

func TestCLIErrorBasic(t *testing.T) {
	err := NewCLIError("something failed")
	if err.Error() != "something failed" {
		t.Errorf("CLIError.Error() = %q, want 'something failed'", err.Error())
	}
	if err.Message != "something failed" {
		t.Errorf("CLIError.Message = %q, want 'something failed'", err.Message)
	}
}

func TestCLIErrorChaining(t *testing.T) {
	err := NewCLIError("failed").
		WithCause("network timeout").
		WithHint("check connection").
		WithCode("NET_TIMEOUT")

	if err.Message != "failed" {
		t.Errorf("Message = %q", err.Message)
	}
	if err.Cause != "network timeout" {
		t.Errorf("Cause = %q", err.Cause)
	}
	if err.Hint != "check connection" {
		t.Errorf("Hint = %q", err.Hint)
	}
	if err.Code != "NET_TIMEOUT" {
		t.Errorf("Code = %q", err.Code)
	}
}

func TestFormatCLIErrorPlain(t *testing.T) {
	// Force NO_COLOR to get plain text output
	os.Setenv("NO_COLOR", "1")
	defer os.Unsetenv("NO_COLOR")

	err := NewCLIError("test error").
		WithCause("something went wrong").
		WithHint("try again").
		WithCode("TEST")

	output := FormatCLIError(err)

	if !strings.Contains(output, "Error: test error") {
		t.Errorf("Expected 'Error: test error' in output: %q", output)
	}
	if !strings.Contains(output, "[TEST]") {
		t.Errorf("Expected '[TEST]' in output: %q", output)
	}
	if !strings.Contains(output, "Cause: something went wrong") {
		t.Errorf("Expected cause in output: %q", output)
	}
	if !strings.Contains(output, "Hint: try again") {
		t.Errorf("Expected hint in output: %q", output)
	}
}

func TestFormatCLIErrorMinimal(t *testing.T) {
	os.Setenv("NO_COLOR", "1")
	defer os.Unsetenv("NO_COLOR")

	// Only message, no cause/hint/code
	err := NewCLIError("simple error")
	output := FormatCLIError(err)

	if !strings.Contains(output, "Error: simple error") {
		t.Errorf("Expected 'Error: simple error' in output: %q", output)
	}
	if strings.Contains(output, "Cause:") {
		t.Errorf("Should not have Cause: %q", output)
	}
	if strings.Contains(output, "Hint:") {
		t.Errorf("Should not have Hint: %q", output)
	}
}

func TestPrintCLIErrorOrJSONText(t *testing.T) {
	os.Setenv("NO_COLOR", "1")
	defer os.Unsetenv("NO_COLOR")

	err := NewCLIError("text error").WithHint("do something")

	_, stderr := captureOutput(func() {
		PrintCLIErrorOrJSON(err, false)
	})

	if !strings.Contains(stderr, "Error: text error") {
		t.Errorf("Expected error in stderr: %q", stderr)
	}
	if !strings.Contains(stderr, "Hint: do something") {
		t.Errorf("Expected hint in stderr: %q", stderr)
	}
}

func TestPrintCLIErrorOrJSONMode(t *testing.T) {
	err := NewCLIError("json error").
		WithCause("bad request").
		WithHint("fix it").
		WithCode("BAD_REQ")

	stdout, _ := captureOutput(func() {
		PrintCLIErrorOrJSON(err, true)
	})

	var resp ErrorResponse
	if jsonErr := json.Unmarshal([]byte(stdout), &resp); jsonErr != nil {
		t.Fatalf("JSON invalid: %v\nOutput: %q", jsonErr, stdout)
	}

	if resp.Error != "json error" {
		t.Errorf("Error = %q", resp.Error)
	}
	if resp.Code != "BAD_REQ" {
		t.Errorf("Code = %q", resp.Code)
	}
	if resp.Details != "bad request" {
		t.Errorf("Details = %q", resp.Details)
	}
	if resp.Hint != "fix it" {
		t.Errorf("Hint = %q", resp.Hint)
	}
}

func TestSessionNotFoundError(t *testing.T) {
	err := SessionNotFoundError("myproject")

	if !strings.Contains(err.Message, "myproject") {
		t.Errorf("Message should contain session name: %q", err.Message)
	}
	if err.Code != "SESSION_NOT_FOUND" {
		t.Errorf("Code = %q", err.Code)
	}
	if err.Hint == "" {
		t.Error("Hint should not be empty")
	}
}

func TestSessionExistsError(t *testing.T) {
	err := SessionExistsError("existing")

	if !strings.Contains(err.Message, "existing") {
		t.Errorf("Message should contain session name: %q", err.Message)
	}
	if err.Code != "SESSION_EXISTS" {
		t.Errorf("Code = %q", err.Code)
	}
}

func TestTmuxNotInstalledError(t *testing.T) {
	err := TmuxNotInstalledError()

	if !strings.Contains(err.Message, "tmux") {
		t.Errorf("Message should mention tmux: %q", err.Message)
	}
	if err.Code != "TMUX_NOT_INSTALLED" {
		t.Errorf("Code = %q", err.Code)
	}
	if !strings.Contains(err.Hint, "brew") && !strings.Contains(err.Hint, "apt") {
		t.Errorf("Hint should include install instructions: %q", err.Hint)
	}
}

func TestPaneNotFoundError(t *testing.T) {
	err := PaneNotFoundError("mysession", 5)

	if !strings.Contains(err.Message, "5") {
		t.Errorf("Message should contain pane index: %q", err.Message)
	}
	if !strings.Contains(err.Message, "mysession") {
		t.Errorf("Message should contain session name: %q", err.Message)
	}
	if err.Code != "PANE_NOT_FOUND" {
		t.Errorf("Code = %q", err.Code)
	}
}

func TestPrintErrorWithHint(t *testing.T) {
	os.Setenv("NO_COLOR", "1")
	defer os.Unsetenv("NO_COLOR")

	_, stderr := captureOutput(func() {
		PrintErrorWithHint("something broke", "fix it", false)
	})

	if !strings.Contains(stderr, "something broke") {
		t.Errorf("Expected error in stderr: %q", stderr)
	}
	if !strings.Contains(stderr, "fix it") {
		t.Errorf("Expected hint in stderr: %q", stderr)
	}
}

func TestPrintErrorFull(t *testing.T) {
	os.Setenv("NO_COLOR", "1")
	defer os.Unsetenv("NO_COLOR")

	_, stderr := captureOutput(func() {
		PrintErrorFull("failed", "reason", "solution", false)
	})

	if !strings.Contains(stderr, "failed") {
		t.Errorf("Expected error message: %q", stderr)
	}
	if !strings.Contains(stderr, "reason") {
		t.Errorf("Expected cause: %q", stderr)
	}
	if !strings.Contains(stderr, "solution") {
		t.Errorf("Expected hint: %q", stderr)
	}
}

func TestNewErrorWithHint(t *testing.T) {
	resp := NewErrorWithHint("failed", "try again")
	if resp.Error != "failed" {
		t.Errorf("Error = %q", resp.Error)
	}
	if resp.Hint != "try again" {
		t.Errorf("Hint = %q", resp.Hint)
	}
}

func TestNewErrorFull(t *testing.T) {
	resp := NewErrorFull("CODE", "error msg", "details", "hint")
	if resp.Code != "CODE" {
		t.Errorf("Code = %q", resp.Code)
	}
	if resp.Error != "error msg" {
		t.Errorf("Error = %q", resp.Error)
	}
	if resp.Details != "details" {
		t.Errorf("Details = %q", resp.Details)
	}
	if resp.Hint != "hint" {
		t.Errorf("Hint = %q", resp.Hint)
	}
}

func TestSpawnSuggestions(t *testing.T) {
	suggestions := SpawnSuggestions("myproject")
	if len(suggestions) != 3 {
		t.Fatalf("SpawnSuggestions() returned %d suggestions, want 3", len(suggestions))
	}
	if !strings.Contains(suggestions[0].Command, "attach") {
		t.Errorf("First suggestion should be attach, got %q", suggestions[0].Command)
	}
	if !strings.Contains(suggestions[1].Command, "dashboard") {
		t.Errorf("Second suggestion should be dashboard, got %q", suggestions[1].Command)
	}
}

func TestQuickSuggestions(t *testing.T) {
	suggestions := QuickSuggestions("/home/user/project", "myproject")
	if len(suggestions) != 2 {
		t.Fatalf("QuickSuggestions() returned %d suggestions, want 2", len(suggestions))
	}
	if !strings.Contains(suggestions[0].Command, "cd") {
		t.Errorf("First suggestion should be cd, got %q", suggestions[0].Command)
	}
}

func TestFormatSuggestions(t *testing.T) {
	suggestions := []Suggestion{
		{Command: "ntm attach test", Description: "Connect to session"},
		{Command: "ntm dashboard test", Description: "Live status"},
	}
	result := FormatSuggestions(suggestions)
	if !strings.Contains(result, "What's next?") {
		t.Error("FormatSuggestions should include 'What's next?' header")
	}
	if !strings.Contains(result, "ntm attach test") {
		t.Error("FormatSuggestions should include commands")
	}
	if !strings.Contains(result, "Connect to session") {
		t.Error("FormatSuggestions should include descriptions")
	}
}

func TestFormatSuggestionsEmpty(t *testing.T) {
	result := FormatSuggestions(nil)
	if result != "" {
		t.Errorf("FormatSuggestions(nil) = %q, want empty string", result)
	}
}

func TestNewSuccessWithSuggestions(t *testing.T) {
	suggestions := []Suggestion{
		{Command: "ntm status", Description: "Check status"},
	}
	resp := NewSuccessWithSuggestions("Done!", suggestions)
	if !resp.Success {
		t.Error("Success should be true")
	}
	if resp.Message != "Done!" {
		t.Errorf("Message = %q, want 'Done!'", resp.Message)
	}
	if len(resp.Suggestions) != 1 {
		t.Fatalf("Suggestions count = %d, want 1", len(resp.Suggestions))
	}
	if resp.Suggestions[0].Command != "ntm status" {
		t.Errorf("Suggestion command = %q", resp.Suggestions[0].Command)
	}
}

func TestPrintSuccessFooterToBuffer(t *testing.T) {
	var buf bytes.Buffer
	suggestions := []Suggestion{
		{Command: "ntm test", Description: "Test command"},
	}
	// Buffer is not a terminal, so this should skip output
	PrintSuccessFooter(&buf, suggestions...)
	// Since buf is not a *os.File terminal, it should still output
	// Actually the check is for *os.File, so buffer will get output
	output := buf.String()
	if !strings.Contains(output, "What's next?") {
		t.Errorf("Expected 'What's next?' in output, got: %q", output)
	}
}

func TestSuccessCheckToBuffer(t *testing.T) {
	var buf bytes.Buffer
	PrintSuccessCheck(&buf, "Task completed")
	output := buf.String()
	if !strings.Contains(output, "✓") {
		t.Error("SuccessCheck should include checkmark")
	}
	if !strings.Contains(output, "Task completed") {
		t.Error("SuccessCheck should include message")
	}
}

func TestAddSuggestions(t *testing.T) {
	suggestions := AddSuggestions("proj", 3)
	if len(suggestions) != 3 {
		t.Fatalf("AddSuggestions() returned %d suggestions, want 3", len(suggestions))
	}
}

func TestSendSuggestions(t *testing.T) {
	suggestions := SendSuggestions("proj")
	if len(suggestions) != 2 {
		t.Fatalf("SendSuggestions() returned %d suggestions, want 2", len(suggestions))
	}
}

func TestKillSuggestions(t *testing.T) {
	suggestions := KillSuggestions()
	if len(suggestions) != 2 {
		t.Fatalf("KillSuggestions() returned %d suggestions, want 2", len(suggestions))
	}
}
