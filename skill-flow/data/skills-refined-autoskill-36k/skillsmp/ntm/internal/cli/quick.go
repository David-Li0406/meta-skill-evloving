package cli

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/output"
)

func newQuickCmd() *cobra.Command {
	var (
		noGit          bool
		noVSCode       bool
		noClaudeConfig bool
		template       string
	)

	cmd := &cobra.Command{
		Use:     "quick <project-name>",
		Aliases: []string{"new", "setup"},
		Short:   "Quick project setup with git, VSCode, and Claude config",
		Long: `Create a new project directory with sensible defaults:

	- Creates directory in projects_base/<name> (defaults: ~/Developer on macOS, /data/projects on Linux)
	- Initializes git repository
	- Creates VSCode workspace settings
	- Creates Claude Code configuration
	- Creates basic .gitignore

Examples:
  ntm quick myproject           # Full setup
  ntm quick myproject --no-git  # Skip git init
  ntm quick api --template=go   # Use Go template`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runQuick(args[0], quickOptions{
				NoGit:          noGit,
				NoVSCode:       noVSCode,
				NoClaudeConfig: noClaudeConfig,
				Template:       template,
			})
		},
	}

	cmd.Flags().BoolVar(&noGit, "no-git", false, "Skip git initialization")
	cmd.Flags().BoolVar(&noVSCode, "no-vscode", false, "Skip VSCode settings")
	cmd.Flags().BoolVar(&noClaudeConfig, "no-claude", false, "Skip Claude config")
	cmd.Flags().StringVarP(&template, "template", "t", "", "Project template (go, python, node, rust)")

	return cmd
}

type quickOptions struct {
	NoGit          bool
	NoVSCode       bool
	NoClaudeConfig bool
	Template       string
}

type quickResponse struct {
	WorkingDirectory string   `json:"working_directory"`
	Session          string   `json:"session"`
	GitInitialized   bool     `json:"git_initialized"`
	GitignoreCreated bool     `json:"gitignore_created"`
	VSCodeCreated    bool     `json:"vscode_created"`
	ClaudeCreated    bool     `json:"claude_created"`
	TemplateApplied  string   `json:"template_applied,omitempty"`
	Warnings         []string `json:"warnings,omitempty"`
}

func runQuick(name string, opts quickOptions) error {
	// Validate project name
	if strings.ContainsAny(name, "/\\:*?\"<>|") {
		return fmt.Errorf("invalid project name: contains forbidden characters")
	}

	projectDir := ""
	if cfg != nil {
		projectDir = cfg.GetProjectDir(name)
	} else {
		// Fallback: preserve legacy behavior if config somehow isn't initialized.
		home, err := os.UserHomeDir()
		if err != nil {
			return fmt.Errorf("failed to get home directory: %w", err)
		}
		projectDir = filepath.Join(home, "projects", name)
	}

	// Check if directory exists
	if _, err := os.Stat(projectDir); err == nil {
		return fmt.Errorf("project directory already exists: %s", projectDir)
	}

	res := quickResponse{
		WorkingDirectory: projectDir,
		Session:          name,
	}

	// Create project directory
	if err := os.MkdirAll(projectDir, 0755); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	if !IsJSONOutput() {
		output.PrintSuccessf("Created %s", projectDir)
	}

	// Initialize git
	if !opts.NoGit {
		if err := initGit(projectDir); err != nil {
			res.Warnings = append(res.Warnings, fmt.Sprintf("git init failed: %v", err))
			if !IsJSONOutput() {
				output.PrintWarningf("Git init failed: %v", err)
			}
		} else {
			res.GitInitialized = true
			if !IsJSONOutput() {
				output.PrintSuccess("Initialized git repository")
			}
		}
	}

	// Create .gitignore
	if err := createGitignore(projectDir, opts.Template); err != nil {
		res.Warnings = append(res.Warnings, fmt.Sprintf("failed to create .gitignore: %v", err))
		if !IsJSONOutput() {
			output.PrintWarningf("Failed to create .gitignore: %v", err)
		}
	} else {
		res.GitignoreCreated = true
		if !IsJSONOutput() {
			output.PrintSuccess("Created .gitignore")
		}
	}

	// Create VSCode settings
	if !opts.NoVSCode {
		if err := createVSCodeSettings(projectDir); err != nil {
			res.Warnings = append(res.Warnings, fmt.Sprintf("failed to create VSCode settings: %v", err))
			if !IsJSONOutput() {
				output.PrintWarningf("Failed to create VSCode settings: %v", err)
			}
		} else {
			res.VSCodeCreated = true
			if !IsJSONOutput() {
				output.PrintSuccess("Created VSCode settings")
			}
		}
	}

	// Create Claude config
	if !opts.NoClaudeConfig {
		if err := createClaudeConfig(projectDir); err != nil {
			res.Warnings = append(res.Warnings, fmt.Sprintf("failed to create Claude config: %v", err))
			if !IsJSONOutput() {
				output.PrintWarningf("Failed to create Claude config: %v", err)
			}
		} else {
			res.ClaudeCreated = true
			if !IsJSONOutput() {
				output.PrintSuccess("Created Claude Code config")
			}
		}
	}

	// Apply template-specific setup
	if opts.Template != "" {
		if err := applyTemplate(projectDir, opts.Template); err != nil {
			res.Warnings = append(res.Warnings, fmt.Sprintf("template setup failed: %v", err))
			if !IsJSONOutput() {
				output.PrintWarningf("Template setup failed: %v", err)
			}
		} else {
			res.TemplateApplied = opts.Template
			if !IsJSONOutput() {
				output.PrintSuccessf("Applied %s template", opts.Template)
			}
		}
	}

	if IsJSONOutput() {
		return output.PrintJSON(res)
	}

	fmt.Println()
	output.PrintSuccessf("Project ready at: %s", projectDir)

	// Print "What's next?" suggestions
	output.SuccessFooter(output.QuickSuggestions(projectDir, name)...)

	return nil
}

func initGit(dir string) error {
	cmd := exec.Command("git", "init")
	cmd.Dir = dir
	cmd.Stdout = nil
	cmd.Stderr = nil
	return cmd.Run()
}

func createGitignore(dir, template string) error {
	content := `# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Dependencies
node_modules/
vendor/
.venv/
venv/
__pycache__/

# Build outputs
dist/
build/
*.exe
*.dll
*.so
*.dylib

# Logs
*.log
logs/

# Environment
.env
.env.local
.env.*.local

# Coverage
coverage/
*.lcov
`

	// Add template-specific ignores
	switch template {
	case "go":
		content += `
# Go
*.test
*.out
go.work
`
	case "python":
		content += `
# Python
*.pyc
*.pyo
*.egg-info/
.eggs/
.pytest_cache/
.mypy_cache/
`
	case "node":
		content += `
# Node
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm/
`
	case "rust":
		content += `
# Rust
target/
Cargo.lock
**/*.rs.bk
`
	}

	return os.WriteFile(filepath.Join(dir, ".gitignore"), []byte(content), 0644)
}

func createVSCodeSettings(dir string) error {
	vscodePath := filepath.Join(dir, ".vscode")
	if err := os.MkdirAll(vscodePath, 0755); err != nil {
		return err
	}

	settings := `{
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "editor.tabSize": 2,
  "editor.detectIndentation": true
}
`
	return os.WriteFile(filepath.Join(vscodePath, "settings.json"), []byte(settings), 0644)
}

func createClaudeConfig(dir string) error {
	claudePath := filepath.Join(dir, ".claude")
	if err := os.MkdirAll(claudePath, 0755); err != nil {
		return err
	}

	// Create settings.toml
	settings := `# Claude Code Settings
# See: https://docs.anthropic.com/claude-code

[model]
# Preferred model for this project
# default = "claude-sonnet-4-20250514"

[context]
# Additional context files to include
# include = ["README.md", "ARCHITECTURE.md"]

[tools]
# Tool permissions
# allow_bash = true
# allow_edit = true
`
	if err := os.WriteFile(filepath.Join(claudePath, "settings.toml"), []byte(settings), 0644); err != nil {
		return err
	}

	// Create commands directory
	cmdPath := filepath.Join(claudePath, "commands")
	if err := os.MkdirAll(cmdPath, 0755); err != nil {
		return err
	}

	// Create a sample command
	sampleCmd := `# Review PR
Review the current changes and provide feedback.

## What to check
- Code quality and best practices
- Potential bugs or issues
- Test coverage
- Documentation
`
	return os.WriteFile(filepath.Join(cmdPath, "review.md"), []byte(sampleCmd), 0644)
}

func applyTemplate(dir, template string) error {
	switch template {
	case "go":
		return applyGoTemplate(dir)
	case "python":
		return applyPythonTemplate(dir)
	case "node":
		return applyNodeTemplate(dir)
	case "rust":
		return applyRustTemplate(dir)
	default:
		return fmt.Errorf("unknown template: %s", template)
	}
}

func applyGoTemplate(dir string) error {
	// Create go.mod
	projectName := filepath.Base(dir)
	goMod := fmt.Sprintf(`module %s

go 1.22
`, projectName)

	if err := os.WriteFile(filepath.Join(dir, "go.mod"), []byte(goMod), 0644); err != nil {
		return err
	}

	// Create main.go
	mainGo := `package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
`
	return os.WriteFile(filepath.Join(dir, "main.go"), []byte(mainGo), 0644)
}

func applyPythonTemplate(dir string) error {
	// Create pyproject.toml
	projectName := filepath.Base(dir)
	pyproject := fmt.Sprintf(`[project]
name = "%s"
version = "0.1.0"
description = ""
requires-python = ">=3.10"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
`, projectName)

	if err := os.WriteFile(filepath.Join(dir, "pyproject.toml"), []byte(pyproject), 0644); err != nil {
		return err
	}

	// Create main.py
	mainPy := `#!/usr/bin/env python3
"""Main entry point."""


def main() -> None:
    """Run the application."""
    print("Hello, World!")


if __name__ == "__main__":
    main()
`
	return os.WriteFile(filepath.Join(dir, "main.py"), []byte(mainPy), 0644)
}

func applyNodeTemplate(dir string) error {
	// Create package.json
	projectName := filepath.Base(dir)
	packageJSON := fmt.Sprintf(`{
  "name": "%s",
  "version": "0.1.0",
  "description": "",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js"
  },
  "keywords": [],
  "author": "",
  "license": "MIT"
}
`, projectName)

	if err := os.WriteFile(filepath.Join(dir, "package.json"), []byte(packageJSON), 0644); err != nil {
		return err
	}

	// Create index.js
	indexJS := `console.log("Hello, World!");
`
	return os.WriteFile(filepath.Join(dir, "index.js"), []byte(indexJS), 0644)
}

func applyRustTemplate(dir string) error {
	// Create Cargo.toml
	projectName := filepath.Base(dir)
	cargoToml := fmt.Sprintf(`[package]
name = "%s"
version = "0.1.0"
edition = "2021"

[dependencies]
`, projectName)

	if err := os.WriteFile(filepath.Join(dir, "Cargo.toml"), []byte(cargoToml), 0644); err != nil {
		return err
	}

	// Create src directory and main.rs
	srcDir := filepath.Join(dir, "src")
	if err := os.MkdirAll(srcDir, 0755); err != nil {
		return err
	}

	mainRs := `fn main() {
    println!("Hello, World!");
}
`
	return os.WriteFile(filepath.Join(srcDir, "main.rs"), []byte(mainRs), 0644)
}
