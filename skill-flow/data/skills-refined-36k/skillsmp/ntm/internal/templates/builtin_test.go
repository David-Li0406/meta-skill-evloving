package templates

import (
	"strings"
	"testing"
)

func TestGetBuiltin(t *testing.T) {
	tests := []struct {
		name     string
		want     bool
		wantName string
	}{
		{name: "code_review", want: true, wantName: "code_review"},
		{name: "explain", want: true, wantName: "explain"},
		{name: "refactor", want: true, wantName: "refactor"},
		{name: "test", want: true, wantName: "test"},
		{name: "document", want: true, wantName: "document"},
		{name: "fix", want: true, wantName: "fix"},
		{name: "implement", want: true, wantName: "implement"},
		{name: "optimize", want: true, wantName: "optimize"},
		{name: "nonexistent", want: false, wantName: ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			tmpl := GetBuiltin(tt.name)
			if tt.want {
				if tmpl == nil {
					t.Errorf("GetBuiltin(%q) = nil, want template", tt.name)
				} else if tmpl.Name != tt.wantName {
					t.Errorf("GetBuiltin(%q).Name = %q, want %q", tt.name, tmpl.Name, tt.wantName)
				}
			} else {
				if tmpl != nil {
					t.Errorf("GetBuiltin(%q) = %v, want nil", tt.name, tmpl)
				}
			}
		})
	}
}

func TestListBuiltins(t *testing.T) {
	builtins := ListBuiltins()

	if len(builtins) < 5 {
		t.Errorf("len(ListBuiltins()) = %d, want at least 5", len(builtins))
	}

	// Check all have required fields
	for _, tmpl := range builtins {
		if tmpl.Name == "" {
			t.Error("Builtin template has empty Name")
		}
		if tmpl.Body == "" {
			t.Errorf("Builtin template %q has empty Body", tmpl.Name)
		}
		if tmpl.Source != SourceBuiltin {
			t.Errorf("Builtin template %q has Source = %v, want SourceBuiltin", tmpl.Name, tmpl.Source)
		}
	}
}

func TestBuiltinTemplates_Executable(t *testing.T) {
	// Test that all builtin templates can execute with their required variables
	builtins := ListBuiltins()

	for _, tmpl := range builtins {
		t.Run(tmpl.Name, func(t *testing.T) {
			// Build context with all required variables
			ctx := ExecutionContext{
				Variables: make(map[string]string),
			}

			for _, v := range tmpl.Variables {
				if v.Required {
					// Set all required variables, including "file"
					ctx.Variables[v.Name] = "// Sample test content for " + v.Name
				}
			}

			// Also set FileContent for templates that use {{file}}
			ctx.FileContent = "// Sample code content\nfunc main() {}"

			result, err := tmpl.Execute(ctx)
			if err != nil {
				t.Errorf("Execute() failed: %v", err)
			}

			if result == "" {
				t.Error("Execute() returned empty result")
			}
		})
	}
}

func TestGetBuiltin_ReturnsCopy(t *testing.T) {
	// Verify GetBuiltin returns a copy, not the original
	tmpl1 := GetBuiltin("code_review")
	tmpl2 := GetBuiltin("code_review")

	tmpl1.Name = "modified"

	if tmpl2.Name == "modified" {
		t.Error("GetBuiltin should return a copy, not the original")
	}
}

func TestGetBuiltin_WorkflowTemplates(t *testing.T) {
	// Verify new workflow templates exist
	workflowTemplates := []string{
		"marching_orders",
		"self_review",
		"cross_review",
		"handoff",
		"batch_assign",
	}

	for _, name := range workflowTemplates {
		t.Run(name, func(t *testing.T) {
			tmpl := GetBuiltin(name)
			if tmpl == nil {
				t.Errorf("GetBuiltin(%q) = nil, want template", name)
				return
			}
			if tmpl.Name != name {
				t.Errorf("GetBuiltin(%q).Name = %q, want %q", name, tmpl.Name, name)
			}
			// Workflow templates should have workflow tag
			hasWorkflowTag := false
			for _, tag := range tmpl.Tags {
				if tag == "workflow" {
					hasWorkflowTag = true
					break
				}
			}
			if !hasWorkflowTag {
				t.Errorf("Template %q missing 'workflow' tag", name)
			}
		})
	}
}

func TestMarchingOrdersTemplate_WithBeadContext(t *testing.T) {
	tmpl := GetBuiltin("marching_orders")
	if tmpl == nil {
		t.Fatal("marching_orders template not found")
	}

	ctx := ExecutionContext{
		Variables: make(map[string]string),
	}
	ctx = ctx.WithBead("bd-test1", "Fix login bug", "P1", "The login form fails validation", "in_progress", "bug")
	ctx = ctx.WithAgent(3, "claude", "opus", "%123")

	result, err := tmpl.Execute(ctx)
	if err != nil {
		t.Fatalf("Execute() error: %v", err)
	}

	// Check that bead context variables are substituted
	if !strings.Contains(result, "bd-test1") {
		t.Error("Result missing bead_id")
	}
	if !strings.Contains(result, "Fix login bug") {
		t.Error("Result missing bead title")
	}
	if !strings.Contains(result, "P1") {
		t.Error("Result missing priority")
	}
	if !strings.Contains(result, "The login form fails validation") {
		t.Error("Result missing description")
	}
	// Check agent context
	if !strings.Contains(result, "Agent #3") {
		t.Error("Result missing agent number")
	}
	if !strings.Contains(result, "claude") {
		t.Error("Result missing agent type")
	}
}

func TestSelfReviewTemplate_WithBeadContext(t *testing.T) {
	tmpl := GetBuiltin("self_review")
	if tmpl == nil {
		t.Fatal("self_review template not found")
	}

	ctx := ExecutionContext{
		Variables: make(map[string]string),
	}
	ctx = ctx.WithBead("ntm-abc1", "Add caching layer", "P2", "", "in_progress", "feature")
	ctx = ctx.WithAgent(1, "codex", "gpt4", "%200")
	ctx.Variables["checklist"] = "- [ ] Cache invalidation tested\n- [ ] TTL configured"

	result, err := tmpl.Execute(ctx)
	if err != nil {
		t.Fatalf("Execute() error: %v", err)
	}

	if !strings.Contains(result, "ntm-abc1") {
		t.Error("Result missing bead_id")
	}
	if !strings.Contains(result, "Add caching layer") {
		t.Error("Result missing bead title")
	}
	if !strings.Contains(result, "Agent #1") {
		t.Error("Result missing agent number")
	}
	// Check custom checklist included
	if !strings.Contains(result, "Cache invalidation tested") {
		t.Error("Result missing custom checklist")
	}
}

func TestCrossReviewTemplate_WithContext(t *testing.T) {
	tmpl := GetBuiltin("cross_review")
	if tmpl == nil {
		t.Fatal("cross_review template not found")
	}

	ctx := ExecutionContext{
		Variables: map[string]string{
			"author_agent": "2",
			"files":        "- internal/cache/cache.go\n- internal/cache/cache_test.go",
			"focus":        "Thread safety of cache operations",
		},
	}
	ctx = ctx.WithBead("bd-xyz9", "Implement cache", "", "", "", "")
	ctx = ctx.WithAgent(5, "gemini", "pro", "%300")

	result, err := tmpl.Execute(ctx)
	if err != nil {
		t.Fatalf("Execute() error: %v", err)
	}

	if !strings.Contains(result, "Agent #5") {
		t.Error("Result missing reviewer agent number")
	}
	if !strings.Contains(result, "Agent #2") {
		t.Error("Result missing author agent reference")
	}
	if !strings.Contains(result, "internal/cache/cache.go") {
		t.Error("Result missing files list")
	}
	if !strings.Contains(result, "Thread safety") {
		t.Error("Result missing focus area")
	}
}

func TestBatchAssignTemplate_WithSendContext(t *testing.T) {
	tmpl := GetBuiltin("batch_assign")
	if tmpl == nil {
		t.Fatal("batch_assign template not found")
	}

	ctx := ExecutionContext{
		Variables: make(map[string]string),
	}
	ctx = ctx.WithBead("bd-task5", "Implement feature X", "", "", "", "")
	ctx = ctx.WithAgent(2, "claude", "sonnet", "%150")
	ctx = ctx.WithSendBatch(2, 5) // 3rd of 5 (0-indexed)

	result, err := tmpl.Execute(ctx)
	if err != nil {
		t.Fatalf("Execute() error: %v", err)
	}

	// Check send batch variables
	if !strings.Contains(result, "3/5") { // send_num is 1-indexed
		t.Error("Result missing send_num/send_total")
	}
	if !strings.Contains(result, "Agent #2") {
		t.Error("Result missing agent number")
	}
	if !strings.Contains(result, "bd-task5") {
		t.Error("Result missing bead_id")
	}
}

func TestHandoffTemplate_WithContext(t *testing.T) {
	tmpl := GetBuiltin("handoff")
	if tmpl == nil {
		t.Fatal("handoff template not found")
	}

	ctx := ExecutionContext{
		Variables: map[string]string{
			"target_agent": "4",
			"context":      "Completed the database migration, tests passing",
			"next_steps":   "1. Deploy to staging\n2. Monitor for errors",
		},
	}
	ctx = ctx.WithBead("ntm-mig1", "Database migration", "", "", "", "")
	ctx = ctx.WithAgent(1, "claude", "opus", "%100")

	result, err := tmpl.Execute(ctx)
	if err != nil {
		t.Fatalf("Execute() error: %v", err)
	}

	if !strings.Contains(result, "Agent #1") {
		t.Error("Result missing source agent number")
	}
	if !strings.Contains(result, "Agent #4") {
		t.Error("Result missing target agent number")
	}
	if !strings.Contains(result, "database migration") {
		t.Error("Result missing context")
	}
	if !strings.Contains(result, "Deploy to staging") {
		t.Error("Result missing next steps")
	}
}
