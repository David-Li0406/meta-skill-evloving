package config

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"

	"gopkg.in/yaml.v3"
)

// Config represents the cortex configuration
type Config struct {
	Me       MeConfig                `yaml:"me"`
	Adapters map[string]AdapterConfig `yaml:"adapters"`
}

// MeConfig represents the user's identity
type MeConfig struct {
	CanonicalName string     `yaml:"canonical_name"`
	Identities    []Identity `yaml:"identities"`
}

// Identity represents a user identifier in a specific channel
type Identity struct {
	Channel    string `yaml:"channel"`
	Identifier string `yaml:"identifier"`
}

// AdapterConfig represents adapter configuration
type AdapterConfig struct {
	Type    string                 `yaml:"type"`
	Enabled bool                   `yaml:"enabled"`
	Live    *LiveConfig            `yaml:"live,omitempty"`
	Options map[string]interface{} `yaml:"options,omitempty"`
}

// LiveConfig controls live watching for an adapter.
type LiveConfig struct {
	Enabled bool                   `yaml:"enabled"`
	Options map[string]interface{} `yaml:"options,omitempty"`
}

// GetConfigDir returns the XDG-compliant config directory
func GetConfigDir() (string, error) {
	// Explicit override (useful for tests and portable installs)
	if override := os.Getenv("CORTEX_CONFIG_DIR"); override != "" {
		return override, nil
	}
	if override := os.Getenv("COMMS_CONFIG_DIR"); override != "" {
		return override, nil
	}

	var base string
	if xdg := os.Getenv("XDG_CONFIG_HOME"); xdg != "" {
		base = xdg
	} else {
		home, err := os.UserHomeDir()
		if err != nil {
			return "", fmt.Errorf("failed to get home directory: %w", err)
		}
		base = filepath.Join(home, ".config")
	}
	return filepath.Join(base, "cortex"), nil
}

// GetDataDir returns the platform-specific data directory
func GetDataDir() (string, error) {
	// Explicit override (useful for tests and portable installs)
	if override := os.Getenv("CORTEX_DATA_DIR"); override != "" {
		return override, nil
	}
	if override := os.Getenv("COMMS_DATA_DIR"); override != "" {
		return override, nil
	}

	home, err := os.UserHomeDir()
	if err != nil {
		return "", fmt.Errorf("failed to get home directory: %w", err)
	}

	if runtime.GOOS == "darwin" {
		return filepath.Join(home, "Library", "Application Support", "Cortex"), nil
	}

	if xdg := os.Getenv("XDG_DATA_HOME"); xdg != "" {
		return filepath.Join(xdg, "cortex"), nil
	}

	return filepath.Join(home, ".local", "share", "cortex"), nil
}

// Load loads config from the config file
func Load() (*Config, error) {
	configDir, err := GetConfigDir()
	if err != nil {
		return nil, err
	}

	configPath := filepath.Join(configDir, "config.yaml")

	data, err := os.ReadFile(configPath)
	if err != nil {
		if os.IsNotExist(err) {
			// Return default empty config
			return &Config{
				Adapters: make(map[string]AdapterConfig),
			}, nil
		}
		return nil, fmt.Errorf("failed to read config: %w", err)
	}

	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("failed to parse config: %w", err)
	}

	if cfg.Adapters == nil {
		cfg.Adapters = make(map[string]AdapterConfig)
	}

	return &cfg, nil
}

// Save saves the config to the config file
func (c *Config) Save() error {
	configDir, err := GetConfigDir()
	if err != nil {
		return err
	}

	if err := os.MkdirAll(configDir, 0755); err != nil {
		return fmt.Errorf("failed to create config directory: %w", err)
	}

	configPath := filepath.Join(configDir, "config.yaml")

	data, err := yaml.Marshal(c)
	if err != nil {
		return fmt.Errorf("failed to marshal config: %w", err)
	}

	if err := os.WriteFile(configPath, data, 0644); err != nil {
		return fmt.Errorf("failed to write config: %w", err)
	}

	return nil
}
