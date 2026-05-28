package swarm

import (
	"fmt"
	"log/slog"
)

// Default review templates per agent type.
var defaultReviewTemplates = map[string]string{
	"cc": `Review the code in this project. Focus on:
1. Potential bugs or edge cases
2. Security vulnerabilities
3. Performance concerns
4. Code clarity and maintainability

Do NOT make any changes. Only provide analysis and recommendations.`,

	"cod": `Analyze the codebase and identify:
- Code quality issues
- Missing error handling
- Test coverage gaps
- Documentation needs

Output findings only, no modifications.`,

	"gmi": `Perform a code review focusing on:
- Architecture patterns
- API design
- Dependency concerns
- Scalability considerations

Analysis mode only - no code changes.`,
}

// ReviewOptions configures review prompt generation.
type ReviewOptions struct {
	FocusArea   string // e.g., "security", "performance"
	FilePattern string // e.g., "*.go", "internal/**"
}

// ReviewPromptGenerator creates review-mode prompts for agents.
// It supports per-agent-type templates and customization options.
type ReviewPromptGenerator struct {
	// templates maps agent type to review template
	templates map[string]string
	// Logger for structured logging
	Logger *slog.Logger
}

// NewReviewPromptGenerator creates a new ReviewPromptGenerator with default templates.
func NewReviewPromptGenerator() *ReviewPromptGenerator {
	return &ReviewPromptGenerator{
		templates: make(map[string]string),
		Logger:    slog.Default(),
	}
}

// WithReviewTemplate sets a custom template for an agent type.
func (g *ReviewPromptGenerator) WithReviewTemplate(agentType, template string) *ReviewPromptGenerator {
	g.templates[agentType] = template
	return g
}

// WithReviewLogger sets a custom logger.
func (g *ReviewPromptGenerator) WithReviewLogger(logger *slog.Logger) *ReviewPromptGenerator {
	g.Logger = logger
	return g
}

// reviewLogger returns the configured logger or the default logger.
func (g *ReviewPromptGenerator) reviewLogger() *slog.Logger {
	if g.Logger != nil {
		return g.Logger
	}
	return slog.Default()
}

// GenerateReviewPrompt creates a review prompt for the given agent type and context.
func (g *ReviewPromptGenerator) GenerateReviewPrompt(agentType, projectPath string, opts ReviewOptions) string {
	// Get template, preferring custom over default
	template := g.templates[agentType]
	if template == "" {
		template = defaultReviewTemplates[agentType]
	}
	if template == "" {
		// Fallback to cc template if agent type not found
		template = defaultReviewTemplates["cc"]
	}

	prompt := template

	// Apply options
	if opts.FilePattern != "" {
		prompt = fmt.Sprintf("Review files matching: %s\n\n%s", opts.FilePattern, prompt)
	}
	if opts.FocusArea != "" {
		prompt = fmt.Sprintf("Focus specifically on: %s\n\n%s", opts.FocusArea, prompt)
	}

	g.reviewLogger().Info("generated review prompt",
		"agent_type", agentType,
		"project", projectPath,
		"focus_area", opts.FocusArea,
		"file_pattern", opts.FilePattern,
		"prompt_len", len(prompt))

	return prompt
}

// GetReviewTemplate returns the review template for a specific agent type.
func (g *ReviewPromptGenerator) GetReviewTemplate(agentType string) string {
	if template, ok := g.templates[agentType]; ok {
		return template
	}
	return defaultReviewTemplates[agentType]
}
