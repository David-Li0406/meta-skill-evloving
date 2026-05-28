package startup

import (
	"github.com/Dicklesworthstone/ntm/internal/config"
	"github.com/Dicklesworthstone/ntm/internal/profiler"
)

// configLoader manages lazy config loading
var configLoader = NewLazy[*config.Config]("config", func() (*config.Config, error) {
	span := profiler.StartWithPhase("config_load_inner", "deferred")
	defer span.End()

	// Use LoadMerged to include project-specific config
	cfg, err := config.LoadMerged("", configFilePath)
	if err != nil {
		// If loading fails (e.g. project config invalid), return error
		// Note: LoadMerged handles global config missing by using defaults
		return nil, err
	}
	return cfg, nil
})

// configFilePath stores the custom config path if specified
var configFilePath string

// SetConfigPath sets the config file path for lazy loading
func SetConfigPath(path string) {
	configFilePath = path
}

// GetConfig returns the configuration, loading it lazily if needed
func GetConfig() (*config.Config, error) {
	return configLoader.Get()
}

// MustGetConfig returns the configuration, panicking on error
func MustGetConfig() *config.Config {
	return configLoader.MustGet()
}

// IsConfigLoaded returns true if config has been loaded
func IsConfigLoaded() bool {
	return configLoader.IsInitialized()
}

// ResetConfig allows re-loading config (useful for testing)
func ResetConfig() {
	configLoader.Reset()
}
