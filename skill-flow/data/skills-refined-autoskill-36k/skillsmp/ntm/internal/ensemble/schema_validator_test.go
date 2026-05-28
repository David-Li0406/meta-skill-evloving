package ensemble

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestSchemaValidator_NewSchemaValidator(t *testing.T) {
	v := NewSchemaValidator()
	if v == nil {
		t.Fatal("NewSchemaValidator returned nil")
	}
	if v.CheckFileExists {
		t.Error("CheckFileExists should default to false")
	}
	if v.BaseDir != "." {
		t.Errorf("BaseDir = %q, want %q", v.BaseDir, ".")
	}
}

func TestSchemaValidator_Validate_ValidOutput(t *testing.T) {
	v := NewSchemaValidator()
	output := &ModeOutput{
		ModeID: "test-mode",
		Thesis: "This is the main conclusion",
		TopFindings: []Finding{
			{
				Finding:    "Important discovery",
				Impact:     ImpactHigh,
				Confidence: 0.9,
			},
		},
		Confidence:  0.85,
		GeneratedAt: time.Now(),
	}

	errs := v.Validate(output)
	if len(errs) > 0 {
		t.Errorf("Validate returned errors for valid output: %v", errs)
	}
}

func TestSchemaValidator_Validate_MissingModeID(t *testing.T) {
	v := NewSchemaValidator()
	output := &ModeOutput{
		Thesis: "Some thesis",
		TopFindings: []Finding{
			{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
		},
		Confidence: 0.8,
	}

	errs := v.Validate(output)
	if len(errs) == 0 {
		t.Error("expected validation error for missing mode_id")
	}

	found := false
	for _, e := range errs {
		if e.Field == "mode_id" {
			found = true
			break
		}
	}
	if !found {
		t.Error("expected error for field 'mode_id'")
	}
}

func TestSchemaValidator_Validate_MissingThesis(t *testing.T) {
	v := NewSchemaValidator()
	output := &ModeOutput{
		ModeID: "test",
		TopFindings: []Finding{
			{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
		},
		Confidence: 0.8,
	}

	errs := v.Validate(output)

	found := false
	for _, e := range errs {
		if e.Field == "thesis" {
			found = true
			break
		}
	}
	if !found {
		t.Error("expected error for field 'thesis'")
	}
}

func TestSchemaValidator_Validate_NoFindings(t *testing.T) {
	v := NewSchemaValidator()
	output := &ModeOutput{
		ModeID:      "test",
		Thesis:      "Some thesis",
		TopFindings: []Finding{},
		Confidence:  0.8,
	}

	errs := v.Validate(output)

	found := false
	for _, e := range errs {
		if e.Field == "top_findings" {
			found = true
			break
		}
	}
	if !found {
		t.Error("expected error for field 'top_findings'")
	}
}

func TestSchemaValidator_Validate_InvalidConfidence(t *testing.T) {
	v := NewSchemaValidator()

	tests := []struct {
		name       string
		confidence Confidence
	}{
		{"negative", -0.1},
		{"greater than 1", 1.5},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			output := &ModeOutput{
				ModeID: "test",
				Thesis: "Thesis",
				TopFindings: []Finding{
					{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
				},
				Confidence: tc.confidence,
			}

			errs := v.Validate(output)

			found := false
			for _, e := range errs {
				if e.Field == "confidence" {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("expected error for confidence=%f", tc.confidence)
			}
		})
	}
}

func TestSchemaValidator_ValidateFindings(t *testing.T) {
	v := NewSchemaValidator()

	t.Run("valid findings", func(t *testing.T) {
		findings := []Finding{
			{Finding: "First finding", Impact: ImpactHigh, Confidence: 0.9},
			{Finding: "Second finding", Impact: ImpactMedium, Confidence: 0.7},
		}
		errs := v.ValidateFindings(findings)
		if len(errs) > 0 {
			t.Errorf("unexpected errors: %v", errs)
		}
	})

	t.Run("missing finding description", func(t *testing.T) {
		findings := []Finding{
			{Finding: "", Impact: ImpactHigh, Confidence: 0.9},
		}
		errs := v.ValidateFindings(findings)
		if len(errs) == 0 {
			t.Error("expected error for missing finding description")
		}
	})

	t.Run("invalid impact level", func(t *testing.T) {
		findings := []Finding{
			{Finding: "Test", Impact: "invalid", Confidence: 0.5},
		}
		errs := v.ValidateFindings(findings)

		found := false
		for _, e := range errs {
			if e.Field == "top_findings[0].impact" {
				found = true
				break
			}
		}
		if !found {
			t.Error("expected error for invalid impact level")
		}
	})

	t.Run("invalid finding confidence", func(t *testing.T) {
		findings := []Finding{
			{Finding: "Test", Impact: ImpactLow, Confidence: 2.0},
		}
		errs := v.ValidateFindings(findings)

		found := false
		for _, e := range errs {
			if e.Field == "top_findings[0].confidence" {
				found = true
				break
			}
		}
		if !found {
			t.Error("expected error for invalid finding confidence")
		}
	})
}

func TestSchemaValidator_ValidateEvidencePointers(t *testing.T) {
	// Create a temp file for testing
	tmpDir := t.TempDir()
	tmpFile := filepath.Join(tmpDir, "test.go")
	if err := os.WriteFile(tmpFile, []byte("package test"), 0644); err != nil {
		t.Fatal(err)
	}

	v := &SchemaValidator{
		CheckFileExists: true,
		BaseDir:         tmpDir,
	}

	t.Run("existing file", func(t *testing.T) {
		findings := []Finding{
			{
				Finding:         "Test",
				Impact:          ImpactLow,
				Confidence:      0.5,
				EvidencePointer: "test.go:10",
			},
		}
		errs := v.ValidateEvidencePointers(findings)
		if len(errs) > 0 {
			t.Errorf("unexpected errors: %v", errs)
		}
	})

	t.Run("non-existing file", func(t *testing.T) {
		findings := []Finding{
			{
				Finding:         "Test",
				Impact:          ImpactLow,
				Confidence:      0.5,
				EvidencePointer: "nonexistent.go:42",
			},
		}
		errs := v.ValidateEvidencePointers(findings)
		if len(errs) == 0 {
			t.Error("expected error for non-existing file")
		}
	})

	t.Run("empty evidence pointer skipped", func(t *testing.T) {
		findings := []Finding{
			{Finding: "Test", Impact: ImpactLow, Confidence: 0.5, EvidencePointer: ""},
		}
		errs := v.ValidateEvidencePointers(findings)
		if len(errs) > 0 {
			t.Errorf("empty evidence pointer should be skipped: %v", errs)
		}
	})
}

func TestSchemaValidator_Validate_Risks(t *testing.T) {
	v := NewSchemaValidator()

	t.Run("valid risks", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			Risks: []Risk{
				{Risk: "Potential issue", Impact: ImpactHigh, Likelihood: 0.3},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)
		if len(errs) > 0 {
			t.Errorf("unexpected errors: %v", errs)
		}
	})

	t.Run("invalid risk", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			Risks: []Risk{
				{Risk: "", Impact: "invalid", Likelihood: 1.5},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)
		if len(errs) < 3 {
			t.Errorf("expected at least 3 errors, got %d", len(errs))
		}
	})
}

func TestSchemaValidator_Validate_Recommendations(t *testing.T) {
	v := NewSchemaValidator()

	t.Run("valid recommendations", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			Recommendations: []Recommendation{
				{Recommendation: "Do this", Priority: ImpactHigh},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)
		if len(errs) > 0 {
			t.Errorf("unexpected errors: %v", errs)
		}
	})

	t.Run("missing recommendation text", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			Recommendations: []Recommendation{
				{Recommendation: "", Priority: ImpactHigh},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)

		found := false
		for _, e := range errs {
			if e.Field == "recommendations[0].recommendation" {
				found = true
				break
			}
		}
		if !found {
			t.Error("expected error for missing recommendation text")
		}
	})

	t.Run("invalid priority", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			Recommendations: []Recommendation{
				{Recommendation: "Do this", Priority: "invalid"},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)

		found := false
		for _, e := range errs {
			if e.Field == "recommendations[0].priority" {
				found = true
				break
			}
		}
		if !found {
			t.Error("expected error for invalid priority")
		}
	})
}

func TestSchemaValidator_Validate_Questions(t *testing.T) {
	v := NewSchemaValidator()

	t.Run("valid questions", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			QuestionsForUser: []Question{
				{Question: "What should we do?"},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)
		if len(errs) > 0 {
			t.Errorf("unexpected errors: %v", errs)
		}
	})

	t.Run("missing question text", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			QuestionsForUser: []Question{
				{Question: ""},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)

		found := false
		for _, e := range errs {
			if e.Field == "questions_for_user[0].question" {
				found = true
				break
			}
		}
		if !found {
			t.Error("expected error for missing question text")
		}
	})
}

func TestSchemaValidator_Validate_FailureModes(t *testing.T) {
	v := NewSchemaValidator()

	t.Run("valid failure modes", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			FailureModesToWatch: []FailureModeWarning{
				{Mode: "confirmation-bias", Description: "May favor confirming evidence"},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)
		if len(errs) > 0 {
			t.Errorf("unexpected errors: %v", errs)
		}
	})

	t.Run("missing mode identifier", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			FailureModesToWatch: []FailureModeWarning{
				{Mode: "", Description: "Description"},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)

		found := false
		for _, e := range errs {
			if e.Field == "failure_modes_to_watch[0].mode" {
				found = true
				break
			}
		}
		if !found {
			t.Error("expected error for missing mode identifier")
		}
	})

	t.Run("missing description", func(t *testing.T) {
		output := &ModeOutput{
			ModeID: "test",
			Thesis: "Thesis",
			TopFindings: []Finding{
				{Finding: "Finding", Impact: ImpactLow, Confidence: 0.5},
			},
			FailureModesToWatch: []FailureModeWarning{
				{Mode: "bias", Description: ""},
			},
			Confidence: 0.8,
		}
		errs := v.Validate(output)

		found := false
		for _, e := range errs {
			if e.Field == "failure_modes_to_watch[0].description" {
				found = true
				break
			}
		}
		if !found {
			t.Error("expected error for missing description")
		}
	})
}

func TestSchemaValidator_ParseYAML(t *testing.T) {
	v := NewSchemaValidator()

	t.Run("valid YAML", func(t *testing.T) {
		yaml := `
mode_id: bayesian
thesis: Evidence supports hypothesis A
top_findings:
  - finding: Strong correlation found
    impact: high
    confidence: 0.85
confidence: 0.8
`
		output, err := v.ParseYAML(yaml)
		if err != nil {
			t.Fatalf("ParseYAML error: %v", err)
		}
		if output.ModeID != "bayesian" {
			t.Errorf("ModeID = %q, want %q", output.ModeID, "bayesian")
		}
		if output.Thesis != "Evidence supports hypothesis A" {
			t.Errorf("Thesis = %q", output.Thesis)
		}
		if len(output.TopFindings) != 1 {
			t.Errorf("TopFindings count = %d, want 1", len(output.TopFindings))
		}
		if output.RawOutput != yaml {
			t.Error("RawOutput should preserve original YAML")
		}
	})

	t.Run("invalid YAML", func(t *testing.T) {
		yaml := `{invalid: yaml: syntax`
		_, err := v.ParseYAML(yaml)
		if err == nil {
			t.Error("expected error for invalid YAML")
		}
	})
}

func TestSchemaValidator_ParseAndValidate(t *testing.T) {
	v := NewSchemaValidator()

	t.Run("valid YAML with validation", func(t *testing.T) {
		yaml := `
mode_id: deductive
thesis: The conclusion follows from the premises
top_findings:
  - finding: Premise 1 is true
    impact: high
    confidence: 0.95
confidence: 0.9
`
		output, errs, err := v.ParseAndValidate(yaml)
		if err != nil {
			t.Fatalf("ParseAndValidate error: %v", err)
		}
		if len(errs) > 0 {
			t.Errorf("unexpected validation errors: %v", errs)
		}
		if output.ModeID != "deductive" {
			t.Errorf("ModeID = %q, want %q", output.ModeID, "deductive")
		}
	})

	t.Run("valid YAML with validation errors", func(t *testing.T) {
		yaml := `
thesis: Missing mode_id
top_findings: []
confidence: 1.5
`
		_, errs, err := v.ParseAndValidate(yaml)
		if err != nil {
			t.Fatalf("ParseAndValidate error: %v", err)
		}
		if len(errs) == 0 {
			t.Error("expected validation errors")
		}

		// Should have errors for: mode_id, top_findings, confidence
		fields := make(map[string]bool)
		for _, e := range errs {
			fields[e.Field] = true
		}
		if !fields["mode_id"] {
			t.Error("expected error for mode_id")
		}
		if !fields["top_findings"] {
			t.Error("expected error for top_findings")
		}
		if !fields["confidence"] {
			t.Error("expected error for confidence")
		}
	})
}

func TestValidationError_Error(t *testing.T) {
	t.Run("with value", func(t *testing.T) {
		e := ValidationError{
			Field:   "confidence",
			Message: "must be between 0.0 and 1.0",
			Value:   1.5,
		}
		got := e.Error()
		want := "confidence: must be between 0.0 and 1.0 (got 1.5)"
		if got != want {
			t.Errorf("Error() = %q, want %q", got, want)
		}
	})

	t.Run("without value", func(t *testing.T) {
		e := ValidationError{
			Field:   "mode_id",
			Message: "required field is missing",
		}
		got := e.Error()
		want := "mode_id: required field is missing"
		if got != want {
			t.Errorf("Error() = %q, want %q", got, want)
		}
	})
}
