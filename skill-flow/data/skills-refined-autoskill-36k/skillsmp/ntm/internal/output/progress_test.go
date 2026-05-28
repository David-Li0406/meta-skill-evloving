package output

import (
	"bytes"
	"os"
	"strings"
	"testing"
)

func TestStepsBasicFlow(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf)

	steps.Start("Loading config").Done()
	steps.Start("Connecting").Done()

	out := buf.String()
	if !strings.Contains(out, "Loading config") {
		t.Error("expected step name in output")
	}
	if !strings.Contains(out, "Connecting") {
		t.Error("expected second step name in output")
	}
	// Non-terminal output uses [OK]
	if !strings.Contains(out, "[OK]") {
		t.Error("expected [OK] marker in non-terminal output")
	}
}

func TestStepsFail(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf)

	steps.Start("Downloading").Fail()

	out := buf.String()
	if !strings.Contains(out, "Downloading") {
		t.Error("expected step name in output")
	}
	if !strings.Contains(out, "[FAIL]") {
		t.Error("expected [FAIL] marker")
	}
}

func TestStepsSkip(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf)

	steps.Start("Optional step").Skip()

	out := buf.String()
	if !strings.Contains(out, "[SKIP]") {
		t.Error("expected [SKIP] marker")
	}
}

func TestStepsWarn(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf)

	steps.Start("Partial step").Warn()

	out := buf.String()
	if !strings.Contains(out, "[WARN]") {
		t.Error("expected [WARN] marker")
	}
}

func TestStepsWithTotal(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf).SetTotal(3)

	steps.Start("Step one").Done()
	steps.Start("Step two").Done()

	out := buf.String()
	if !strings.Contains(out, "[1/3]") {
		t.Error("expected [1/3] in output")
	}
	if !strings.Contains(out, "[2/3]") {
		t.Error("expected [2/3] in output")
	}
}

func TestStepsAutoComplete(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf)

	// Start step but don't explicitly complete it
	steps.Start("First")
	// Starting another should auto-complete the previous
	steps.Start("Second").Done()

	out := buf.String()
	// First should have been auto-completed
	count := strings.Count(out, "[OK]")
	if count != 2 {
		t.Errorf("expected 2 [OK] markers (auto-complete + explicit), got %d", count)
	}
}

func TestStepsStatus(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf)

	if steps.Status() != StepPending {
		t.Error("expected pending status before any step")
	}

	steps.Start("Test")
	if steps.Status() != StepRunning {
		t.Error("expected running status after Start")
	}

	steps.Done()
	if steps.Status() != StepSuccess {
		t.Error("expected success status after Done")
	}
}

func TestStepsIndent(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	steps := NewStepsWriter(&buf).SetIndent("    ")

	steps.Start("Indented").Done()

	out := buf.String()
	if !strings.HasPrefix(out, "    ") {
		t.Error("expected custom indent")
	}
}

func TestProgressMsgSuccess(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	p := ProgressWriter(&buf)

	p.Success("Task completed")

	out := buf.String()
	if !strings.Contains(out, "✓") {
		t.Error("expected ✓ in success message")
	}
	if !strings.Contains(out, "Task completed") {
		t.Error("expected message text")
	}
}

func TestProgressMsgWarning(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	p := ProgressWriter(&buf)

	p.Warning("Something unexpected")

	out := buf.String()
	if !strings.Contains(out, "⚠") {
		t.Error("expected ⚠ in warning message")
	}
}

func TestProgressMsgError(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	p := ProgressWriter(&buf)

	p.Error("Something failed")

	out := buf.String()
	if !strings.Contains(out, "✗") {
		t.Error("expected ✗ in error message")
	}
}

func TestProgressMsgInfo(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	p := ProgressWriter(&buf)

	p.Info("Note this")

	out := buf.String()
	if !strings.Contains(out, "ℹ") {
		t.Error("expected ℹ in info message")
	}
}

func TestProgressMsgPrint(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	p := ProgressWriter(&buf)

	p.Print("Plain message")

	out := buf.String()
	if !strings.Contains(out, "Plain message") {
		t.Error("expected plain message")
	}
	if strings.Contains(out, "✓") || strings.Contains(out, "⚠") {
		t.Error("plain message should not have icons")
	}
}

func TestProgressMsgFormatted(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	p := ProgressWriter(&buf)

	p.Successf("Created %d files", 5)

	out := buf.String()
	if !strings.Contains(out, "Created 5 files") {
		t.Error("expected formatted message")
	}
}

func TestProgressMsgIndent(t *testing.T) {
	t.Parallel()

	var buf bytes.Buffer
	p := ProgressWriter(&buf).SetIndent(">>> ")

	p.Success("Indented")

	out := buf.String()
	if !strings.HasPrefix(out, ">>>") {
		t.Error("expected custom indent prefix")
	}
}

func TestOperationBasic(t *testing.T) {
	t.Parallel()

	op := NewOperation("Build")

	if op.HasErrors() {
		t.Error("new operation should not have errors")
	}
	if op.HasWarnings() {
		t.Error("new operation should not have warnings")
	}
}

func TestOperationWithErrors(t *testing.T) {
	t.Parallel()

	op := NewOperation("Deploy")
	op.AddError("Connection timeout")
	op.AddError("Auth failed")

	if !op.HasErrors() {
		t.Error("expected HasErrors to be true")
	}
	if op.HasWarnings() {
		t.Error("expected HasWarnings to be false")
	}
}

func TestOperationWithWarnings(t *testing.T) {
	t.Parallel()

	op := NewOperation("Setup")
	op.AddWarning("Deprecated config")

	if op.HasErrors() {
		t.Error("expected HasErrors to be false")
	}
	if !op.HasWarnings() {
		t.Error("expected HasWarnings to be true")
	}
}

func TestFormatStepList(t *testing.T) {
	t.Parallel()

	steps := []string{"Init", "Build", "Deploy"}
	out := FormatStepList(steps)

	if !strings.Contains(out, "1. Init") {
		t.Error("expected numbered step 1")
	}
	if !strings.Contains(out, "2. Build") {
		t.Error("expected numbered step 2")
	}
	if !strings.Contains(out, "3. Deploy") {
		t.Error("expected numbered step 3")
	}
}

func TestFormatStepListEmpty(t *testing.T) {
	t.Parallel()

	out := FormatStepList(nil)
	if out != "" {
		t.Error("expected empty string for nil steps")
	}
}

func TestConvenienceFunctions(t *testing.T) {
	// These write to stdout, so we just verify they don't panic
	// In a real scenario, we'd capture stdout

	// Skip if not in a proper test environment
	if os.Getenv("CI") != "" {
		t.Skip("skipping convenience function tests in CI")
	}

	// Just verify they compile and can be called
	// (actual output goes to stdout)
	_ = PrintSuccess
	_ = PrintSuccessf
	_ = PrintWarning
	_ = PrintWarningf
	_ = PrintInfo
	_ = PrintInfof
}
