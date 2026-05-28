package templates

import (
	"fmt"
	"regexp"
	"strings"

	"gopkg.in/yaml.v3"
)

// Pre-compiled regex patterns for variable substitution
var (
	// simpleVarRe matches simple {{variable}} placeholders
	simpleVarRe = regexp.MustCompile(`\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}`)
	// conditionalOpenRe matches conditional opening tags {{#variable}}
	conditionalOpenRe = regexp.MustCompile(`\{\{#([a-zA-Z_][a-zA-Z0-9_]*)\}\}`)
)

// Parse parses a template from markdown content with YAML frontmatter.
// Format:
//
//	---
//	name: template_name
//	description: What this template does
//	variables:
//	  - name: file
//	    description: File path to review
//	    required: true
//	---
//	The template body with {{variable}} placeholders.
func Parse(content string) (*Template, error) {
	tmpl := &Template{}

	// Check for frontmatter
	if strings.HasPrefix(content, "---") {
		parts := strings.SplitN(content, "---", 3)
		if len(parts) >= 3 {
			// Parse YAML frontmatter
			if err := yaml.Unmarshal([]byte(parts[1]), tmpl); err != nil {
				return nil, err
			}
			tmpl.Body = strings.TrimSpace(parts[2])
		} else {
			// No valid frontmatter, treat entire content as body
			tmpl.Body = strings.TrimSpace(content)
		}
	} else {
		// No frontmatter, entire content is body
		tmpl.Body = strings.TrimSpace(content)
	}

	return tmpl, nil
}

// Execute substitutes variables in the template body.
func (t *Template) Execute(ctx ExecutionContext) (string, error) {
	// Validate required variables
	if err := t.Validate(ctx); err != nil {
		return "", err
	}

	// Build variable map: defaults < builtins < user vars < special vars
	vars := make(map[string]string)

	// Apply defaults from template definition
	for _, v := range t.Variables {
		if v.Default != "" {
			vars[v.Name] = v.Default
		}
	}

	// Apply builtin variables
	for k, v := range BuiltinVariables() {
		vars[k] = v
	}

	// Apply user-provided variables
	for k, v := range ctx.Variables {
		vars[k] = v
	}

	// Apply special context variables
	if ctx.FileContent != "" {
		vars["file"] = ctx.FileContent
	}
	if ctx.Session != "" {
		vars["session"] = ctx.Session
	}
	if ctx.Clipboard != "" {
		vars["clipboard"] = ctx.Clipboard
	}

	// Apply bead context variables
	if ctx.BeadID != "" {
		vars["bead_id"] = ctx.BeadID
		vars["BEAD_ID"] = ctx.BeadID // Also support uppercase for convenience
	}
	if ctx.BeadTitle != "" {
		vars["bead_title"] = ctx.BeadTitle
		vars["TITLE"] = ctx.BeadTitle // Common alias
	}
	if ctx.BeadPriority != "" {
		vars["bead_priority"] = ctx.BeadPriority
		vars["PRIORITY"] = ctx.BeadPriority
	}
	if ctx.BeadDescription != "" {
		vars["bead_description"] = ctx.BeadDescription
		vars["DESCRIPTION"] = ctx.BeadDescription
	}
	if ctx.BeadStatus != "" {
		vars["bead_status"] = ctx.BeadStatus
	}
	if ctx.BeadType != "" {
		vars["bead_type"] = ctx.BeadType
	}

	// Apply agent context variables
	if ctx.AgentNum > 0 {
		vars["agent_num"] = fmt.Sprintf("%d", ctx.AgentNum)
		vars["AGENT_NUM"] = vars["agent_num"]
	}
	if ctx.AgentType != "" {
		vars["agent_type"] = ctx.AgentType
		vars["AGENT_TYPE"] = ctx.AgentType
	}
	if ctx.AgentVariant != "" {
		vars["agent_variant"] = ctx.AgentVariant
		vars["VARIANT"] = ctx.AgentVariant
	}
	if ctx.AgentPane != "" {
		vars["agent_pane"] = ctx.AgentPane
	}

	// Apply send batch context variables
	if ctx.SendTotal > 0 {
		vars["send_index"] = fmt.Sprintf("%d", ctx.SendIndex)
		vars["send_total"] = fmt.Sprintf("%d", ctx.SendTotal)
		vars["send_num"] = fmt.Sprintf("%d", ctx.SendIndex+1) // 1-indexed for human readability
	}

	// Perform substitution
	result := t.Body

	// First, expand conditionals {{#var}}...{{/var}}
	result = expandConditionals(result, vars)

	// Then, substitute simple variables {{var}}
	result = substituteVariables(result, vars)

	return result, nil
}

// substituteVariables replaces {{variable}} placeholders with values.
// Note: The regex only matches simple variables like {{foo}}, not conditional
// markers like {{#var}} or {{/var}} (which don't start with [a-zA-Z_]).
func substituteVariables(body string, vars map[string]string) string {
	return simpleVarRe.ReplaceAllStringFunc(body, func(match string) string {
		// Extract variable name
		name := match[2 : len(match)-2]

		if val, ok := vars[name]; ok {
			return val
		}
		return match // Leave unmatched variables as-is
	})
}

// expandConditionals handles {{#variable}}...{{/variable}} blocks.
// If the variable is set and non-empty, the block content is included.
// Otherwise, the entire block is removed.
func expandConditionals(body string, vars map[string]string) string {
	// Process until no more matches (handles nested conditionals)
	for {
		matches := conditionalOpenRe.FindStringSubmatchIndex(body)
		if matches == nil {
			break // No more opening tags
		}

		// Extract variable name
		varName := body[matches[2]:matches[3]]
		openStart := matches[0]
		openEnd := matches[1]

		// Find matching closing tag
		closeTag := "{{/" + varName + "}}"
		closeStart := strings.Index(body[openEnd:], closeTag)
		if closeStart == -1 {
			// No matching close tag, leave as-is and skip
			break
		}
		closeStart += openEnd
		closeEnd := closeStart + len(closeTag)

		// Extract content between tags
		content := body[openEnd:closeStart]

		// Determine replacement
		var replacement string
		if val, ok := vars[varName]; ok && val != "" {
			replacement = content
		}
		// else: replacement is empty string, removing the block

		// Rebuild body
		body = body[:openStart] + replacement + body[closeEnd:]
	}

	return body
}

// ExtractVariables finds all variable references in a template body.
// Returns both simple variables ({{var}}) and conditional variables ({{#var}}).
func ExtractVariables(body string) []string {
	seen := make(map[string]bool)
	var vars []string

	// Match simple variables
	for _, match := range simpleVarRe.FindAllStringSubmatch(body, -1) {
		name := match[1]
		if !seen[name] {
			seen[name] = true
			vars = append(vars, name)
		}
	}

	// Match conditional variables
	for _, match := range conditionalOpenRe.FindAllStringSubmatch(body, -1) {
		name := match[1]
		if !seen[name] {
			seen[name] = true
			vars = append(vars, name)
		}
	}

	return vars
}

// macroRe matches @macro-name patterns for inline template expansion.
// Supports both hyphenated names (@marching-orders) and underscored names (@marching_orders).
var macroRe = regexp.MustCompile(`@([a-zA-Z][a-zA-Z0-9_-]*)`)

// ExpandMacros replaces @macro-name patterns with the corresponding builtin template body.
// This allows users to include template content inline within prompts.
//
// Example:
//
//	input:  "Please follow @marching_orders for task bd-xyz"
//	output: "Please follow # Marching Orders: {{BEAD_ID}}\n... for task bd-xyz"
//
// Macros are matched case-insensitively and both hyphens and underscores are normalized.
// If a macro name doesn't match a builtin template, it is left unchanged.
func ExpandMacros(text string) string {
	return macroRe.ReplaceAllStringFunc(text, func(match string) string {
		// Extract macro name (without @ prefix)
		macroName := match[1:]

		// Normalize: convert hyphens to underscores for lookup
		normalizedName := strings.ReplaceAll(macroName, "-", "_")

		// Look up the builtin template
		tmpl := GetBuiltin(normalizedName)
		if tmpl == nil {
			// Try with the original name (maybe already uses underscores)
			tmpl = GetBuiltin(macroName)
		}

		if tmpl != nil {
			return tmpl.Body
		}

		// No matching template, leave the macro unchanged
		return match
	})
}

// ExpandMacrosWithContext expands macros and also substitutes any variables in the expanded content.
// This is a convenience function that combines ExpandMacros with template execution.
func ExpandMacrosWithContext(text string, ctx ExecutionContext) (string, error) {
	// First expand all macros
	expanded := ExpandMacros(text)

	// Then treat the result as a template body and execute it
	tmpl := &Template{
		Name: "_inline_",
		Body: expanded,
	}

	return tmpl.Execute(ctx)
}

// ListMacros returns a list of all available macro names.
// This is useful for documentation and help text.
func ListMacros() []string {
	builtins := ListBuiltins()
	names := make([]string, 0, len(builtins))
	for _, t := range builtins {
		names = append(names, t.Name)
	}
	return names
}
