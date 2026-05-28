package templates

// builtinTemplates holds the default templates embedded in the binary.
var builtinTemplates = []*Template{
	{
		Name:        "code_review",
		Description: "Review code for quality issues",
		Variables: []VariableSpec{
			{Name: "file", Description: "File content to review", Required: true},
			{Name: "focus", Description: "Specific area to focus on"},
		},
		Tags:   []string{"review", "quality"},
		Source: SourceBuiltin,
		Body: `Review the following code for:
- Code quality issues
- Potential bugs
- Performance concerns
- Security vulnerabilities
- Readability and maintainability

{{#focus}}
Focus especially on: {{focus}}
{{/focus}}

---

{{file}}`,
	},
	{
		Name:        "explain",
		Description: "Explain how code works",
		Variables: []VariableSpec{
			{Name: "file", Description: "File content to explain", Required: true},
		},
		Tags:   []string{"explain", "understand"},
		Source: SourceBuiltin,
		Body: `Explain how the following code works in detail.

Walk through:
1. The overall purpose and design
2. The control flow and data transformations
3. Key functions and their responsibilities
4. Any non-obvious patterns or techniques used

---

{{file}}`,
	},
	{
		Name:        "refactor",
		Description: "Refactor code for better quality",
		Variables: []VariableSpec{
			{Name: "file", Description: "File content to refactor", Required: true},
			{Name: "goal", Description: "Refactoring goal (e.g., 'simplify', 'extract functions')"},
		},
		Tags:   []string{"refactor", "improve"},
		Source: SourceBuiltin,
		Body: `Refactor the following code to improve:
- Code structure and organization
- Readability and naming
- Removal of duplication
- Simplification of complex logic

{{#goal}}
Primary goal: {{goal}}
{{/goal}}

Preserve the existing functionality while making these improvements.

---

{{file}}`,
	},
	{
		Name:        "test",
		Description: "Write tests for code",
		Variables: []VariableSpec{
			{Name: "file", Description: "File content to test", Required: true},
			{Name: "framework", Description: "Test framework to use (e.g., 'jest', 'pytest', 'go test')"},
		},
		Tags:   []string{"test", "quality"},
		Source: SourceBuiltin,
		Body: `Write comprehensive tests for the following code.

{{#framework}}
Use the {{framework}} testing framework.
{{/framework}}

Include:
- Unit tests for individual functions
- Edge case handling
- Error condition tests
- Integration tests where appropriate

---

{{file}}`,
	},
	{
		Name:        "document",
		Description: "Add documentation to code",
		Variables: []VariableSpec{
			{Name: "file", Description: "File content to document", Required: true},
			{Name: "style", Description: "Documentation style (e.g., 'jsdoc', 'godoc', 'docstring')"},
		},
		Tags:   []string{"docs", "documentation"},
		Source: SourceBuiltin,
		Body: `Add comprehensive documentation to the following code.

{{#style}}
Use {{style}} style documentation.
{{/style}}

Include:
- File/module level documentation
- Function/method docstrings
- Parameter and return value descriptions
- Usage examples where helpful
- Any important notes or warnings

---

{{file}}`,
	},
	{
		Name:        "fix",
		Description: "Fix a specific issue in code",
		Variables: []VariableSpec{
			{Name: "file", Description: "File content with the issue", Required: true},
			{Name: "issue", Description: "Description of the issue to fix", Required: true},
		},
		Tags:   []string{"fix", "bug"},
		Source: SourceBuiltin,
		Body: `Fix the following issue in the code:

**Issue:** {{issue}}

Provide:
1. Root cause analysis
2. The fix with explanation
3. Any related changes needed

---

{{file}}`,
	},
	{
		Name:        "implement",
		Description: "Implement a feature or function",
		Variables: []VariableSpec{
			{Name: "description", Description: "What to implement", Required: true},
			{Name: "file", Description: "Existing code context"},
			{Name: "language", Description: "Programming language to use"},
		},
		Tags:   []string{"implement", "feature"},
		Source: SourceBuiltin,
		Body: `Implement the following:

**Description:** {{description}}

{{#language}}
Use {{language}}.
{{/language}}

{{#file}}
Here is the existing code context:

---

{{file}}
{{/file}}`,
	},
	{
		Name:        "optimize",
		Description: "Optimize code for performance",
		Variables: []VariableSpec{
			{Name: "file", Description: "File content to optimize", Required: true},
			{Name: "metric", Description: "Metric to optimize (e.g., 'time', 'memory', 'both')"},
		},
		Tags:   []string{"optimize", "performance"},
		Source: SourceBuiltin,
		Body: `Optimize the following code for better performance.

{{#metric}}
Focus on: {{metric}}
{{/metric}}

Consider:
- Algorithm efficiency (time complexity)
- Memory usage
- I/O operations
- Caching opportunities
- Parallelization potential

Explain the optimizations and their expected impact.

---

{{file}}`,
	},
	// Multi-agent workflow templates using bead/agent context variables
	{
		Name:        "marching_orders",
		Description: "Initial instructions for an agent working on a bead task",
		Variables: []VariableSpec{
			{Name: "bead_id", Description: "Bead ID (auto-injected from context)"},
			{Name: "bead_title", Description: "Bead title (auto-injected from context)"},
			{Name: "bead_description", Description: "Bead description (auto-injected from context)"},
			{Name: "bead_priority", Description: "Bead priority (auto-injected from context)"},
			{Name: "agent_num", Description: "Agent number (auto-injected from context)"},
			{Name: "agent_type", Description: "Agent type (auto-injected from context)"},
			{Name: "constraints", Description: "Additional constraints or requirements"},
		},
		Tags:   []string{"workflow", "bead", "assignment"},
		Source: SourceBuiltin,
		Body: `# Marching Orders: {{BEAD_ID}}

## Task
**{{TITLE}}**

{{#bead_priority}}
**Priority:** {{bead_priority}}
{{/bead_priority}}

{{#bead_description}}
## Description
{{bead_description}}
{{/bead_description}}

## Instructions
You are Agent #{{agent_num}} ({{agent_type}}). Execute this task methodically:

1. **Understand**: Read and fully understand the task requirements
2. **Plan**: Create a clear implementation plan before coding
3. **Execute**: Implement the solution step by step
4. **Verify**: Test your changes and ensure they work correctly
5. **Document**: Update any relevant documentation

{{#constraints}}
## Constraints
{{constraints}}
{{/constraints}}

## Completion
When done, mark the bead as completed:
` + "```" + `
br update {{bead_id}} --status closed
` + "```" + `

If blocked, note what's blocking and move on:
` + "```" + `
br update {{bead_id}} --add-note "Blocked: <reason>"
` + "```",
	},
	{
		Name:        "self_review",
		Description: "Agent reviews its own work before marking task complete",
		Variables: []VariableSpec{
			{Name: "bead_id", Description: "Bead ID (auto-injected from context)"},
			{Name: "bead_title", Description: "Bead title (auto-injected from context)"},
			{Name: "agent_num", Description: "Agent number (auto-injected from context)"},
			{Name: "checklist", Description: "Custom checklist items to verify"},
		},
		Tags:   []string{"workflow", "review", "quality"},
		Source: SourceBuiltin,
		Body: `# Self-Review: {{BEAD_ID}}

Agent #{{agent_num}}, review your work on **{{TITLE}}** before marking complete.

## Checklist

### Code Quality
- [ ] Code compiles/builds without errors
- [ ] No new warnings introduced
- [ ] Code follows project style guidelines
- [ ] No hardcoded values that should be configurable

### Testing
- [ ] All existing tests pass
- [ ] New tests written for new functionality
- [ ] Edge cases considered and tested

### Documentation
- [ ] Code is self-documenting with clear names
- [ ] Complex logic has comments explaining "why"
- [ ] Public APIs documented appropriately

### Safety
- [ ] No obvious security vulnerabilities
- [ ] Error handling is appropriate
- [ ] No resource leaks (files, connections, etc.)

{{#checklist}}
### Additional Checks
{{checklist}}
{{/checklist}}

## Action
If all checks pass, mark the bead as closed. If issues found, fix them first.`,
	},
	{
		Name:        "cross_review",
		Description: "One agent reviews another agent's work",
		Variables: []VariableSpec{
			{Name: "bead_id", Description: "Bead ID being reviewed (auto-injected)"},
			{Name: "bead_title", Description: "Bead title (auto-injected)"},
			{Name: "agent_num", Description: "Your agent number (auto-injected)"},
			{Name: "author_agent", Description: "Agent number who authored the work"},
			{Name: "files", Description: "List of files to review"},
			{Name: "focus", Description: "Specific areas to focus review on"},
		},
		Tags:   []string{"workflow", "review", "collaboration"},
		Source: SourceBuiltin,
		Body: `# Cross-Review: {{BEAD_ID}}

You are Agent #{{agent_num}}. Review the work done by Agent #{{author_agent}} on **{{TITLE}}**.

{{#files}}
## Files to Review
{{files}}
{{/files}}

## Review Focus

{{#focus}}
### Priority Areas
{{focus}}
{{/focus}}

### General Review
1. **Correctness**: Does the implementation match the requirements?
2. **Quality**: Is the code clean, readable, and maintainable?
3. **Edge Cases**: Are edge cases handled properly?
4. **Tests**: Are there adequate tests?
5. **Performance**: Any obvious performance issues?

## Feedback Format

Provide feedback as:
- **APPROVE**: Work is ready to merge
- **REQUEST_CHANGES**: Issues that must be fixed
- **COMMENT**: Suggestions or observations (non-blocking)

Be constructive and specific. Reference line numbers when possible.

## Communication
After review, notify the author agent via Agent Mail if available.`,
	},
	{
		Name:        "handoff",
		Description: "Transfer work context from one agent to another",
		Variables: []VariableSpec{
			{Name: "bead_id", Description: "Bead ID (auto-injected from context)"},
			{Name: "bead_title", Description: "Bead title (auto-injected from context)"},
			{Name: "agent_num", Description: "Your agent number (auto-injected)"},
			{Name: "target_agent", Description: "Agent number receiving the handoff"},
			{Name: "context", Description: "Important context to transfer"},
			{Name: "next_steps", Description: "Recommended next steps"},
		},
		Tags:   []string{"workflow", "collaboration", "handoff"},
		Source: SourceBuiltin,
		Body: `# Handoff: {{BEAD_ID}}

Agent #{{agent_num}} is handing off **{{TITLE}}** to Agent #{{target_agent}}.

## Current Status
Summarize what has been accomplished so far.

{{#context}}
## Context
{{context}}
{{/context}}

## Files Touched
List all files modified during this work session.

{{#next_steps}}
## Recommended Next Steps
{{next_steps}}
{{/next_steps}}

## Blockers/Issues
List any blockers or unresolved issues.

## Notes
Additional observations or warnings for the receiving agent.

---

Agent #{{target_agent}}: Review this handoff and continue the work.`,
	},
	{
		Name:        "batch_assign",
		Description: "Template for distributing multiple beads across agents",
		Variables: []VariableSpec{
			{Name: "bead_id", Description: "Bead ID (auto-injected from context)"},
			{Name: "bead_title", Description: "Bead title (auto-injected from context)"},
			{Name: "send_num", Description: "Assignment number in batch (1-indexed, auto-injected)"},
			{Name: "send_total", Description: "Total assignments in batch (auto-injected)"},
			{Name: "agent_num", Description: "Target agent number (auto-injected)"},
		},
		Tags:   []string{"workflow", "batch", "assignment"},
		Source: SourceBuiltin,
		Body: `# Assignment {{send_num}}/{{send_total}}: {{BEAD_ID}}

Agent #{{agent_num}}, you have been assigned: **{{TITLE}}**

This is one of {{send_total}} tasks being distributed. Focus on your assigned task.

## Instructions
1. Mark the bead as in_progress: ` + "`br update {{bead_id}} --status in_progress`" + `
2. Read and understand the full bead description
3. Complete the task
4. Run tests and verify your work
5. Mark as closed when done: ` + "`br update {{bead_id}} --status closed`" + `

## Coordination
- If you need files another agent might be using, coordinate via Agent Mail
- If blocked, add a note and move to your next assigned task`,
	},
}

// GetBuiltin returns a builtin template by name, or nil if not found.
func GetBuiltin(name string) *Template {
	for _, t := range builtinTemplates {
		if t.Name == name {
			// Return a copy to prevent modification
			copy := *t
			return &copy
		}
	}
	return nil
}

// ListBuiltins returns all builtin templates.
func ListBuiltins() []*Template {
	// Return copies to prevent modification
	result := make([]*Template, len(builtinTemplates))
	for i, t := range builtinTemplates {
		copy := *t
		result[i] = &copy
	}
	return result
}
