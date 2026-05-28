package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"text/tabwriter"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/templates"
)

func newTemplateCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "template",
		Short: "Manage prompt templates",
		Long: `Manage reusable prompt templates with variable substitution.

Templates are markdown files with optional YAML frontmatter that define
reusable prompts. They support variable substitution and conditional sections.

Template locations (in order of precedence):
  1. Project: .ntm/templates/*.md
  2. User:    ~/.config/ntm/templates/*.md
  3. Builtin: Embedded in the ntm binary

Example template format:
  ---
  name: code_review
  description: Review code for quality issues
  variables:
    - name: file
      description: File to review
      required: true
    - name: focus
      description: Area to focus on
  ---
  Review the following code:
  {{file}}

  {{#focus}}
  Focus on: {{focus}}
  {{/focus}}

Variables:
  {{variable}}         - Simple substitution
  {{#var}}...{{/var}}  - Conditional (included only if var is set)

Built-in variables:
  {{cwd}}      - Current working directory
  {{date}}     - Current date (YYYY-MM-DD)
  {{time}}     - Current time (HH:MM:SS)
  {{session}}  - Session name (when using with send)
  {{file}}     - File content (when using --file)

Use with ntm send:
  ntm send myproject --template=code_review --file=src/main.go
  ntm send myproject -t refactor --var goal="simplify" --file=src/main.go`,
	}

	cmd.AddCommand(
		newTemplateListCmd(),
		newTemplateShowCmd(),
	)

	return cmd
}

func newTemplateListCmd() *cobra.Command {
	var showAll bool

	cmd := &cobra.Command{
		Use:   "list",
		Short: "List available templates",
		Long: `List all available prompt templates.

Shows templates from all sources (project, user, builtin) with their
descriptions and source locations.`,
		Aliases: []string{"ls"},
		RunE: func(cmd *cobra.Command, args []string) error {
			return runTemplateList(showAll)
		},
	}

	cmd.Flags().BoolVarP(&showAll, "all", "a", false, "show all details including variables")

	return cmd
}

// TemplateListItem is the JSON output for a single template.
type TemplateListItem struct {
	Name        string   `json:"name"`
	Description string   `json:"description"`
	Source      string   `json:"source"`
	SourcePath  string   `json:"source_path,omitempty"`
	Tags        []string `json:"tags,omitempty"`
	Variables   []string `json:"variables,omitempty"`
}

func runTemplateList(showAll bool) error {
	loader := templates.NewLoader()
	tmpls, err := loader.List()
	if err != nil {
		return err
	}

	if len(tmpls) == 0 {
		if jsonOutput {
			return json.NewEncoder(os.Stdout).Encode([]TemplateListItem{})
		}
		fmt.Println("No templates found")
		return nil
	}

	if jsonOutput {
		items := make([]TemplateListItem, len(tmpls))
		for i, t := range tmpls {
			items[i] = TemplateListItem{
				Name:        t.Name,
				Description: t.Description,
				Source:      t.Source.String(),
				SourcePath:  t.SourcePath,
				Tags:        t.Tags,
			}
			if showAll {
				for _, v := range t.Variables {
					items[i].Variables = append(items[i].Variables, v.Name)
				}
			}
		}
		return json.NewEncoder(os.Stdout).Encode(items)
	}

	// Text output
	w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
	fmt.Fprintln(w, "NAME\tDESCRIPTION\tSOURCE")
	fmt.Fprintln(w, "----\t-----------\t------")

	for _, t := range tmpls {
		desc := t.Description
		if len(desc) > 40 {
			desc = desc[:37] + "..."
		}
		fmt.Fprintf(w, "%s\t%s\t%s\n", t.Name, desc, t.Source.String())
	}
	w.Flush()

	if showAll {
		fmt.Println()
		for _, t := range tmpls {
			if len(t.Variables) > 0 {
				fmt.Printf("Template '%s' variables:\n", t.Name)
				for _, v := range t.Variables {
					req := ""
					if v.Required {
						req = " (required)"
					}
					desc := ""
					if v.Description != "" {
						desc = " - " + v.Description
					}
					fmt.Printf("  - %s%s%s\n", v.Name, req, desc)
				}
				fmt.Println()
			}
		}
	}

	return nil
}

func newTemplateShowCmd() *cobra.Command {
	var showBody bool

	cmd := &cobra.Command{
		Use:   "show <name>",
		Short: "Show template details",
		Long: `Show detailed information about a specific template.

Displays the template's metadata, variables, and optionally the template body.`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runTemplateShow(args[0], showBody)
		},
	}

	cmd.Flags().BoolVarP(&showBody, "body", "b", false, "show the template body")

	return cmd
}

// TemplateShowOutput is the JSON output for template show.
type TemplateShowOutput struct {
	Name        string                   `json:"name"`
	Description string                   `json:"description"`
	Source      string                   `json:"source"`
	SourcePath  string                   `json:"source_path,omitempty"`
	Tags        []string                 `json:"tags,omitempty"`
	Variables   []TemplateVariableOutput `json:"variables,omitempty"`
	Body        string                   `json:"body,omitempty"`
}

// TemplateVariableOutput is the JSON output for a template variable.
type TemplateVariableOutput struct {
	Name        string `json:"name"`
	Description string `json:"description,omitempty"`
	Required    bool   `json:"required"`
	Default     string `json:"default,omitempty"`
}

func runTemplateShow(name string, showBody bool) error {
	loader := templates.NewLoader()
	tmpl, err := loader.Load(name)
	if err != nil {
		return err
	}

	if jsonOutput {
		output := TemplateShowOutput{
			Name:        tmpl.Name,
			Description: tmpl.Description,
			Source:      tmpl.Source.String(),
			SourcePath:  tmpl.SourcePath,
			Tags:        tmpl.Tags,
		}
		for _, v := range tmpl.Variables {
			output.Variables = append(output.Variables, TemplateVariableOutput{
				Name:        v.Name,
				Description: v.Description,
				Required:    v.Required,
				Default:     v.Default,
			})
		}
		if showBody {
			output.Body = tmpl.Body
		}
		return json.NewEncoder(os.Stdout).Encode(output)
	}

	// Text output
	fmt.Printf("Name:        %s\n", tmpl.Name)
	fmt.Printf("Description: %s\n", tmpl.Description)
	fmt.Printf("Source:      %s\n", tmpl.Source.String())
	if tmpl.SourcePath != "" {
		fmt.Printf("Path:        %s\n", tmpl.SourcePath)
	}
	if len(tmpl.Tags) > 0 {
		fmt.Printf("Tags:        %s\n", strings.Join(tmpl.Tags, ", "))
	}

	if len(tmpl.Variables) > 0 {
		fmt.Println("\nVariables:")
		for _, v := range tmpl.Variables {
			req := ""
			if v.Required {
				req = " (required)"
			}
			def := ""
			if v.Default != "" {
				def = fmt.Sprintf(" [default: %s]", v.Default)
			}
			fmt.Printf("  - %s%s%s\n", v.Name, req, def)
			if v.Description != "" {
				fmt.Printf("    %s\n", v.Description)
			}
		}
	}

	if showBody {
		fmt.Println("\nBody:")
		fmt.Println("─────────────────────────────────────────")
		fmt.Println(tmpl.Body)
		fmt.Println("─────────────────────────────────────────")
	}

	return nil
}
