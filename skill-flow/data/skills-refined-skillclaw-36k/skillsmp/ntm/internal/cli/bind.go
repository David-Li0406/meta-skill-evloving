package cli

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// validKeyRegex validates tmux key bindings (alphanumeric, -, ^ for Ctrl)
var validKeyRegex = regexp.MustCompile(`^[a-zA-Z0-9\-\^]+$`)

func newBindCmd() *cobra.Command {
	var (
		key      string
		unbind   bool
		showOnly bool
	)

	cmd := &cobra.Command{
		Use:   "bind",
		Short: "Set up tmux keybinding for command palette",
		Long: `Configure a tmux keybinding to open the NTM command palette in a popup.

By default, binds F6 to open a floating popup with the command palette.
The binding is added to both the current tmux server and ~/.tmux.conf.

Examples:
  ntm bind              # Bind F6 (default)
  ntm bind --key=F5     # Bind F5 instead
  ntm bind --show       # Show current binding
  ntm bind --unbind     # Remove the binding`,
		RunE: func(cmd *cobra.Command, args []string) error {
			// Validate key to prevent injection
			// Allowed: alphanumeric, -, ^ (for Ctrl)
			if !validKeyRegex.MatchString(key) {
				return fmt.Errorf("invalid key format: %q (allowed: a-z, 0-9, -, ^)", key)
			}

			if showOnly {
				return showBinding(key)
			}
			if unbind {
				return removeBinding(key)
			}
			return setupBinding(key)
		},
	}

	cmd.Flags().StringVarP(&key, "key", "k", "F6", "Key to bind (e.g., F5, F6, F7)")
	cmd.Flags().BoolVar(&unbind, "unbind", false, "Remove the binding")
	cmd.Flags().BoolVar(&showOnly, "show", false, "Show current binding")

	return cmd
}

func setupBinding(key string) error {
	t := theme.Current()

	// The binding command
	bindCmd := fmt.Sprintf(`bind-key -n %s display-popup -E -w 90%% -h 90%% "ntm palette"`, key)

	// Apply to current tmux server (if running)
	inTmux := os.Getenv("TMUX") != ""
	if inTmux {
		cmd := exec.Command(tmux.BinaryPath(), "bind-key", "-n", key, "display-popup", "-E", "-w", "90%", "-h", "90%", "ntm palette")
		if err := cmd.Run(); err != nil {
			fmt.Printf("%s⚠%s Could not bind in current session: %v\n", colorize(t.Warning), colorize(t.Text), err)
		} else {
			fmt.Printf("%s✓%s Bound %s in current tmux server\n", colorize(t.Success), colorize(t.Text), key)
		}
	} else {
		fmt.Printf("%s→%s Not in tmux, will only update config file\n", colorize(t.Info), colorize(t.Text))
	}

	// Update tmux.conf
	tmuxConf := filepath.Join(os.Getenv("HOME"), ".tmux.conf")

	// Read existing config
	existing := ""
	if data, err := os.ReadFile(tmuxConf); err == nil {
		existing = string(data)
	}

	// Check if binding already exists
	lines := strings.Split(existing, "\n")
	found := false
	var newLines []string

	for _, line := range lines {
		if isBindingLine(line, key) {
			newLines = append(newLines, bindCmd)
			found = true
		} else {
			newLines = append(newLines, line)
		}
	}

	if found {
		if err := os.WriteFile(tmuxConf, []byte(strings.Join(newLines, "\n")), 0600); err != nil {
			return fmt.Errorf("failed to update tmux.conf: %w", err)
		}
		fmt.Printf("%s✓%s Updated existing %s binding in %s\n", colorize(t.Success), colorize(t.Text), key, tmuxConf)
	} else {
		// Append new binding
		f, err := os.OpenFile(tmuxConf, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0600)
		if err != nil {
			return fmt.Errorf("failed to open tmux.conf: %w", err)
		}
		defer func() { _ = f.Close() }()

		// Add comment and binding
		addition := fmt.Sprintf("\n# NTM Command Palette (added by 'ntm bind')\n%s\n", bindCmd)
		if _, err := f.WriteString(addition); err != nil {
			return fmt.Errorf("failed to write tmux.conf: %w", err)
		}
		fmt.Printf("%s✓%s Added %s binding to %s\n", colorize(t.Success), colorize(t.Text), key, tmuxConf)
	}

	// Print usage hint
	fmt.Println()
	fmt.Printf("  Press %s%s%s in tmux to open the command palette.\n",
		colorize(t.Primary), key, colorize(t.Text))

	if !inTmux {
		fmt.Printf("\n  %sNote:%s Run %stmux source ~/.tmux.conf%s to reload config.\n",
			colorize(t.Info), colorize(t.Text),
			colorize(t.Primary), colorize(t.Text))
	}

	return nil
}

func removeBinding(key string) error {
	t := theme.Current()

	// Remove from current tmux server
	if os.Getenv("TMUX") != "" {
		cmd := exec.Command(tmux.BinaryPath(), "unbind-key", "-n", key)
		if err := cmd.Run(); err != nil {
			fmt.Printf("%s⚠%s Could not unbind in current session: %v\n", colorize(t.Warning), colorize(t.Text), err)
		} else {
			fmt.Printf("%s✓%s Unbound %s in current tmux server\n", colorize(t.Success), colorize(t.Text), key)
		}
	}

	// Remove from tmux.conf
	tmuxConf := filepath.Join(os.Getenv("HOME"), ".tmux.conf")

	data, err := os.ReadFile(tmuxConf)
	if err != nil {
		if os.IsNotExist(err) {
			fmt.Printf("%s→%s No tmux.conf found\n", colorize(t.Info), colorize(t.Text))
			return nil
		}
		return err
	}

	// Remove the binding lines
	lines := strings.Split(string(data), "\n")
	var newLines []string
	found := false
	skipNext := false

	for _, line := range lines {
		// Skip comment line before binding
		if strings.Contains(line, "NTM Command Palette") {
			skipNext = true
			continue
		}
		if skipNext && isBindingLine(line, key) {
			found = true
			skipNext = false
			continue
		}
		// Also catch manual bindings without the comment
		if isBindingLine(line, key) {
			found = true
			skipNext = false
			continue
		}

		skipNext = false
		newLines = append(newLines, line)
	}

	if !found {
		fmt.Printf("%s→%s No %s binding found in tmux.conf\n", colorize(t.Info), colorize(t.Text), key)
		return nil
	}

	if err := os.WriteFile(tmuxConf, []byte(strings.Join(newLines, "\n")), 0600); err != nil {
		return fmt.Errorf("failed to update tmux.conf: %w", err)
	}

	fmt.Printf("%s✓%s Removed %s binding from %s\n", colorize(t.Success), colorize(t.Text), key, tmuxConf)
	return nil
}

func showBinding(key string) error {
	t := theme.Current()

	// Check tmux.conf
	tmuxConf := filepath.Join(os.Getenv("HOME"), ".tmux.conf")
	data, err := os.ReadFile(tmuxConf)
	if err != nil {
		if os.IsNotExist(err) {
			fmt.Printf("%s→%s No tmux.conf found\n", colorize(t.Info), colorize(t.Text))
			return nil
		}
		return err
	}

	lines := strings.Split(string(data), "\n")

	found := false
	for _, line := range lines {
		if isBindingLine(line, key) {
			fmt.Printf("%s✓%s Found binding:\n", colorize(t.Success), colorize(t.Text))
			fmt.Printf("  %s%s%s\n", colorize(t.Primary), line, colorize(t.Text))
			found = true
		}
	}

	if !found {
		fmt.Printf("%s→%s No %s binding found in tmux.conf\n", colorize(t.Info), colorize(t.Text), key)
		fmt.Printf("\n  Run %sntm bind%s to set it up.\n", colorize(t.Primary), colorize(t.Text))
	}

	return nil
}

// isBindingLine checks if a line is a tmux binding for the given key.
// Matches "bind-key -n KEY ..." or "bind -n KEY ..."
func isBindingLine(line, key string) bool {
	fields := strings.Fields(line)
	// Check for "bind-key" or "bind"
	if len(fields) < 3 {
		return false
	}

	cmd := fields[0]
	if cmd != "bind-key" && cmd != "bind" {
		return false
	}

	// Check for -n flag (root table)
	if fields[1] != "-n" {
		return false
	}

	// Check key
	return fields[2] == key
}
