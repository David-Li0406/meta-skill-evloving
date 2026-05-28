package plugins

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

// CommandPlugin represents an executable script plugin
type CommandPlugin struct {
	Name        string
	Path        string
	Description string
	Usage       string
}

// LoadCommandPlugins scans directory for executable files
func LoadCommandPlugins(dir string) ([]CommandPlugin, error) {
	var plugins []CommandPlugin

	entries, err := os.ReadDir(dir)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, err
	}

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}

		path := filepath.Join(dir, entry.Name())
		info, err := entry.Info()
		if err != nil {
			continue
		}

		// Check if executable (Mode & 0111)
		// Note: On Windows this check might be insufficient or different,
		// but for Unix-like systems (target for tmux), this works.
		if info.Mode()&0111 == 0 {
			continue
		}

		plugin := CommandPlugin{
			Name: entry.Name(),
			Path: path,
		}

		// Parse header comments for metadata
		if desc, usage, err := parseScriptHeader(path); err == nil {
			plugin.Description = desc
			plugin.Usage = usage
		}

		if plugin.Description == "" {
			plugin.Description = fmt.Sprintf("Custom command: %s", plugin.Name)
		}

		plugins = append(plugins, plugin)
	}

	return plugins, nil
}

// parseScriptHeader extracts Description and Usage from comments
func parseScriptHeader(path string) (string, string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", "", err
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	var description, usage string

	// Read first 10 lines
	for i := 0; i < 10 && scanner.Scan(); i++ {
		line := strings.TrimSpace(scanner.Text())

		// Handle shebang
		if i == 0 && strings.HasPrefix(line, "#!") {
			continue
		}

		if !strings.HasPrefix(line, "#") {
			// Stop at first non-comment line
			break
		}

		// Remove leading # and space
		content := strings.TrimSpace(strings.TrimPrefix(line, "#"))

		if strings.HasPrefix(content, "Description:") {
			description = strings.TrimSpace(strings.TrimPrefix(content, "Description:"))
		} else if strings.HasPrefix(content, "Usage:") {
			usage = strings.TrimSpace(strings.TrimPrefix(content, "Usage:"))
		}
	}

	return description, usage, nil
}

// Execute runs the plugin command
func (p *CommandPlugin) Execute(args []string, env map[string]string) error {
	cmd := exec.Command(p.Path, args...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	currentEnv := os.Environ()
	for k, v := range env {
		currentEnv = append(currentEnv, fmt.Sprintf("%s=%s", k, v))
	}
	cmd.Env = currentEnv

	return cmd.Run()
}
