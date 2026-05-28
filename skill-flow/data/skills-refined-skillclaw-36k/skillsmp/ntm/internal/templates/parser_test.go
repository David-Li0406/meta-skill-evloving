package templates

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestParse_WithFrontmatter(t *testing.T) {
	content := `---
name: test_template
description: A test template
variables:
  - name: file
    description: File to review
    required: true
  - name: focus
    description: Area to focus on
---
Review the following:
{{file}}

{{#focus}}
Focus on: {{focus}}
{{/focus}}`

	tmpl, err := Parse(content)
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}

	if tmpl.Name != "test_template" {
		t.Errorf("Name = %q, want %q", tmpl.Name, "test_template")
	}

	if tmpl.Description != "A test template" {
		t.Errorf("Description = %q, want %q", tmpl.Description, "A test template")
	}

	if len(tmpl.Variables) != 2 {
		t.Errorf("len(Variables) = %d, want 2", len(tmpl.Variables))
	}

	if !tmpl.Variables[0].Required {
		t.Error("First variable should be required")
	}

	if tmpl.Variables[1].Required {
		t.Error("Second variable should not be required")
	}
}

func TestParse_NoFrontmatter(t *testing.T) {
	content := `Just a simple template with {{variable}} placeholders.`

	tmpl, err := Parse(content)
	if err != nil {
		t.Fatalf("Parse failed: %v", err)
	}

	if tmpl.Name != "" {
		t.Errorf("Name = %q, want empty", tmpl.Name)
	}

	if tmpl.Body != content {
		t.Errorf("Body = %q, want %q", tmpl.Body, content)
	}
}

func TestSubstituteVariables(t *testing.T) {
	tests := []struct {
		name string
		body string
		vars map[string]string
		want string
	}{
		{
			name: "simple substitution",
			body: "Hello {{name}}!",
			vars: map[string]string{"name": "World"},
			want: "Hello World!",
		},
		{
			name: "multiple variables",
			body: "{{greeting}}, {{name}}!",
			vars: map[string]string{"greeting": "Hi", "name": "Alice"},
			want: "Hi, Alice!",
		},
		{
			name: "unmatched variable",
			body: "Hello {{name}}!",
			vars: map[string]string{},
			want: "Hello {{name}}!",
		},
		{
			name: "variable in middle",
			body: "The {{color}} fox jumps.",
			vars: map[string]string{"color": "brown"},
			want: "The brown fox jumps.",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := substituteVariables(tt.body, tt.vars)
			if got != tt.want {
				t.Errorf("substituteVariables() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestExpandConditionals(t *testing.T) {
	tests := []struct {
		name string
		body string
		vars map[string]string
		want string
	}{
		{
			name: "conditional included",
			body: "Start {{#focus}}Focus: here{{/focus}} End",
			vars: map[string]string{"focus": "security"},
			want: "Start Focus: here End",
		},
		{
			name: "conditional excluded",
			body: "Start {{#focus}}Focus: something{{/focus}} End",
			vars: map[string]string{},
			want: "Start  End",
		},
		{
			name: "conditional with empty value",
			body: "Start {{#focus}}Focus: something{{/focus}} End",
			vars: map[string]string{"focus": ""},
			want: "Start  End",
		},
		{
			name: "nested conditionals",
			body: "{{#a}}A{{#b}}B{{/b}}{{/a}}",
			vars: map[string]string{"a": "1", "b": "2"},
			want: "AB",
		},
		{
			name: "multiple conditionals",
			body: "{{#one}}1{{/one}} {{#two}}2{{/two}}",
			vars: map[string]string{"one": "yes"},
			want: "1 ",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := expandConditionals(tt.body, tt.vars)
			if got != tt.want {
				t.Errorf("expandConditionals() = %q, want %q", got, tt.want)
			}
		})
	}
}

func TestTemplate_Execute(t *testing.T) {
	tmpl := &Template{
		Name: "test",
		Variables: []VariableSpec{
			{Name: "file", Required: true},
			{Name: "focus", Required: false},
		},
		Body: `Review this code:
{{file}}

{{#focus}}
Focus on: {{focus}}
{{/focus}}`,
	}

	t.Run("with all variables", func(t *testing.T) {
		ctx := ExecutionContext{
			Variables: map[string]string{
				"file":  "func main() {}",
				"focus": "security",
			},
			FileContent: "func main() {}",
		}

		result, err := tmpl.Execute(ctx)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		if !contains(result, "func main()") {
			t.Error("Result should contain file content")
		}

		if !contains(result, "Focus on: security") {
			t.Error("Result should contain focus section")
		}
	})

	t.Run("without optional variable", func(t *testing.T) {
		ctx := ExecutionContext{
			Variables: map[string]string{
				"file": "func main() {}",
			},
			FileContent: "func main() {}",
		}

		result, err := tmpl.Execute(ctx)
		if err != nil {
			t.Fatalf("Execute failed: %v", err)
		}

		if contains(result, "Focus on:") {
			t.Error("Result should not contain focus section")
		}
	})

	t.Run("missing required variable", func(t *testing.T) {
		ctx := ExecutionContext{
			Variables: map[string]string{},
		}

		_, err := tmpl.Execute(ctx)
		if err == nil {
			t.Error("Execute should fail with missing required variable")
		}
	})
}

func TestExtractVariables(t *testing.T) {
	body := `Hello {{name}}!
{{#greet}}Greetings, {{person}}!{{/greet}}
The {{adjective}} {{noun}}.`

	vars := ExtractVariables(body)

	expected := []string{"name", "person", "adjective", "noun", "greet"}
	if len(vars) != len(expected) {
		t.Errorf("len(vars) = %d, want %d", len(vars), len(expected))
	}

	for _, e := range expected {
		found := false
		for _, v := range vars {
			if v == e {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Variable %q not found", e)
		}
	}
}

func TestLoader_Load_ReturnsParseError(t *testing.T) {
	tmp := t.TempDir()
	t.Setenv("XDG_CONFIG_HOME", tmp)

	projectDir := filepath.Join(tmp, "project")
	templateDir := filepath.Join(projectDir, ".ntm", "templates")
	if err := os.MkdirAll(templateDir, 0755); err != nil {
		t.Fatalf("MkdirAll: %v", err)
	}

	name := "bad_parse_template"
	// Invalid YAML frontmatter: unclosed sequence.
	content := "---\nname: [\n---\nHello\n"
	if err := os.WriteFile(filepath.Join(templateDir, name+".md"), []byte(content), 0644); err != nil {
		t.Fatalf("WriteFile: %v", err)
	}

	loader := NewLoaderWithProject(projectDir)
	_, err := loader.Load(name)
	if err == nil {
		t.Fatalf("Load(%q) expected error, got nil", name)
	}

	var notFound *TemplateNotFoundError
	if errors.As(err, &notFound) {
		t.Fatalf("Load(%q) returned TemplateNotFoundError; want parse error: %v", name, err)
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsHelper(s, substr))
}

func containsHelper(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

func TestExpandMacros(t *testing.T) {
	tests := []struct {
		name        string
		input       string
		contains    []string
		notContains []string
	}{
		{
			name:        "underscore syntax",
			input:       "Please follow @marching_orders",
			contains:    []string{"Marching Orders", "{{BEAD_ID}}"},
			notContains: []string{"@marching_orders"},
		},
		{
			name:        "hyphen syntax",
			input:       "Use @marching-orders for this task",
			contains:    []string{"Marching Orders", "{{BEAD_ID}}"},
			notContains: []string{"@marching-orders"},
		},
		{
			name:        "self review macro",
			input:       "Before completing: @self_review",
			contains:    []string{"Self-Review", "Checklist"},
			notContains: []string{"@self_review"},
		},
		{
			name:     "multiple macros",
			input:    "Start with @marching_orders then do @self_review",
			contains: []string{"Marching Orders", "Self-Review"},
		},
		{
			name:        "code_review macro",
			input:       "Apply @code_review to this file",
			contains:    []string{"Review the following code"},
			notContains: []string{"@code_review"},
		},
		{
			name:     "unknown macro unchanged",
			input:    "Check @nonexistent_macro here",
			contains: []string{"@nonexistent_macro"},
		},
		{
			name:     "email address not expanded",
			input:    "Contact user@example.com for help",
			contains: []string{"user@example.com"},
		},
		{
			name:     "no macros",
			input:    "Plain text without macros",
			contains: []string{"Plain text without macros"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ExpandMacros(tt.input)

			for _, want := range tt.contains {
				if !contains(result, want) {
					t.Errorf("Result should contain %q, got:\n%s", want, result)
				}
			}

			for _, notWant := range tt.notContains {
				if contains(result, notWant) {
					t.Errorf("Result should NOT contain %q, got:\n%s", notWant, result)
				}
			}
		})
	}
}

func TestExpandMacrosWithContext(t *testing.T) {
	input := "Execute @marching_orders for this bead"

	ctx := ExecutionContext{
		Variables: make(map[string]string),
	}
	ctx = ctx.WithBead("bd-test1", "Test Task", "P1", "Task description", "open", "task")
	ctx = ctx.WithAgent(2, "claude", "opus", "%123")

	result, err := ExpandMacrosWithContext(input, ctx)
	if err != nil {
		t.Fatalf("ExpandMacrosWithContext failed: %v", err)
	}

	// Check that variables are substituted
	if !contains(result, "bd-test1") {
		t.Error("Result should contain bead_id")
	}
	if !contains(result, "Test Task") {
		t.Error("Result should contain bead title")
	}
	if !contains(result, "Agent #2") {
		t.Error("Result should contain agent number")
	}
}

func TestListMacros(t *testing.T) {
	macros := ListMacros()

	if len(macros) == 0 {
		t.Error("ListMacros should return at least one macro")
	}

	// Check for expected macros
	expectedMacros := []string{"marching_orders", "self_review", "cross_review", "code_review"}
	for _, expected := range expectedMacros {
		found := false
		for _, m := range macros {
			if m == expected {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Expected macro %q not found in ListMacros", expected)
		}
	}
}
