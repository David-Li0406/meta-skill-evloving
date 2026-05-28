package swarm

import (
	"strings"
	"testing"
)

func TestNewReviewPromptGenerator(t *testing.T) {
	gen := NewReviewPromptGenerator()

	if gen == nil {
		t.Fatal("NewReviewPromptGenerator returned nil")
	}

	if gen.templates == nil {
		t.Error("expected templates map to be initialized")
	}

	if gen.Logger == nil {
		t.Error("expected Logger to be set to default")
	}
}

func TestReviewPromptGeneratorWithTemplate(t *testing.T) {
	gen := NewReviewPromptGenerator()
	customTemplate := "Custom review template for testing"

	gen.WithReviewTemplate("cc", customTemplate)

	if gen.templates["cc"] != customTemplate {
		t.Errorf("expected custom template, got %q", gen.templates["cc"])
	}
}

func TestDefaultReviewTemplates(t *testing.T) {
	// Check that default templates exist for all agent types
	agentTypes := []string{"cc", "cod", "gmi"}

	for _, agentType := range agentTypes {
		template := defaultReviewTemplates[agentType]
		if template == "" {
			t.Errorf("expected default template for agent type %q", agentType)
		}

		// Templates should mention no changes/modifications
		templateLower := strings.ToLower(template)
		hasNoChanges := strings.Contains(templateLower, "no") &&
			(strings.Contains(templateLower, "change") || strings.Contains(templateLower, "modification"))
		if !hasNoChanges {
			t.Errorf("template for %q should mention 'no changes' or 'no modifications'", agentType)
		}
	}
}

func TestGenerateReviewPromptBasic(t *testing.T) {
	gen := NewReviewPromptGenerator()

	prompt := gen.GenerateReviewPrompt("cc", "/test/project", ReviewOptions{})

	if prompt == "" {
		t.Error("expected non-empty prompt")
	}

	// Should match cc template
	if !strings.Contains(prompt, "Potential bugs") {
		t.Error("expected cc-specific content in prompt")
	}
}

func TestGenerateReviewPromptWithFocusArea(t *testing.T) {
	gen := NewReviewPromptGenerator()

	opts := ReviewOptions{
		FocusArea: "security",
	}

	prompt := gen.GenerateReviewPrompt("cc", "/test/project", opts)

	if !strings.Contains(prompt, "Focus specifically on: security") {
		t.Error("expected focus area to be prepended to prompt")
	}
}

func TestGenerateReviewPromptWithFilePattern(t *testing.T) {
	gen := NewReviewPromptGenerator()

	opts := ReviewOptions{
		FilePattern: "*.go",
	}

	prompt := gen.GenerateReviewPrompt("cc", "/test/project", opts)

	if !strings.Contains(prompt, "Review files matching: *.go") {
		t.Error("expected file pattern to be prepended to prompt")
	}
}

func TestGenerateReviewPromptWithBothOptions(t *testing.T) {
	gen := NewReviewPromptGenerator()

	opts := ReviewOptions{
		FocusArea:   "performance",
		FilePattern: "internal/**",
	}

	prompt := gen.GenerateReviewPrompt("cod", "/test/project", opts)

	// Both options should be present
	if !strings.Contains(prompt, "Focus specifically on: performance") {
		t.Error("expected focus area in prompt")
	}
	if !strings.Contains(prompt, "Review files matching: internal/**") {
		t.Error("expected file pattern in prompt")
	}

	// Should be cod-specific content
	if !strings.Contains(prompt, "Test coverage gaps") {
		t.Error("expected cod-specific content in prompt")
	}
}

func TestGenerateReviewPromptUnknownAgentFallback(t *testing.T) {
	gen := NewReviewPromptGenerator()

	prompt := gen.GenerateReviewPrompt("unknown_agent", "/test/project", ReviewOptions{})

	if prompt == "" {
		t.Error("expected fallback prompt for unknown agent")
	}

	// Should fall back to cc template
	if !strings.Contains(prompt, "Potential bugs") {
		t.Error("expected cc-specific content as fallback")
	}
}

func TestGenerateReviewPromptCustomTemplate(t *testing.T) {
	gen := NewReviewPromptGenerator()
	customTemplate := "Custom template: focus on $FOCUS"

	gen.WithReviewTemplate("cc", customTemplate)

	prompt := gen.GenerateReviewPrompt("cc", "/test/project", ReviewOptions{})

	if prompt != customTemplate {
		t.Errorf("expected custom template, got %q", prompt)
	}
}

func TestGetReviewTemplate(t *testing.T) {
	gen := NewReviewPromptGenerator()

	// Default template
	template := gen.GetReviewTemplate("cc")
	if template == "" {
		t.Error("expected non-empty default template")
	}

	// Custom template
	gen.WithReviewTemplate("cc", "custom")
	template = gen.GetReviewTemplate("cc")
	if template != "custom" {
		t.Errorf("expected custom template, got %q", template)
	}
}

func TestReviewPromptGeneratorAgentTypes(t *testing.T) {
	gen := NewReviewPromptGenerator()

	tests := []struct {
		agentType       string
		expectedContent string
	}{
		{"cc", "Potential bugs"},
		{"cod", "Code quality issues"},
		{"gmi", "Architecture patterns"},
	}

	for _, tt := range tests {
		t.Run(tt.agentType, func(t *testing.T) {
			prompt := gen.GenerateReviewPrompt(tt.agentType, "/test", ReviewOptions{})
			if !strings.Contains(prompt, tt.expectedContent) {
				t.Errorf("expected %q content for agent %q", tt.expectedContent, tt.agentType)
			}
		})
	}
}

func TestReviewOptionsZeroValue(t *testing.T) {
	opts := ReviewOptions{}

	if opts.FocusArea != "" {
		t.Error("expected empty FocusArea in zero value")
	}
	if opts.FilePattern != "" {
		t.Error("expected empty FilePattern in zero value")
	}
}
