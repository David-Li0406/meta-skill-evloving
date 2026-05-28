// Package scanner provides UBS scanner integration with config support.
package scanner

import (
	"github.com/Dicklesworthstone/ntm/internal/config"
)

// ScanOptionsFromConfig creates ScanOptions from a ScannerConfig
func ScanOptionsFromConfig(cfg *config.ScannerConfig, context string) ScanOptions {
	opts := ScanOptions{
		Timeout:   cfg.Defaults.GetTimeout(),
		Languages: cfg.Defaults.Languages,
	}

	// Apply context-specific settings
	var threshold config.ThresholdConfig
	switch context {
	case "pre_commit", "precommit":
		threshold = cfg.Thresholds.PreCommit
	case "ci":
		threshold = cfg.Thresholds.CI
	case "dashboard":
		threshold = cfg.Thresholds.Dashboard
	default:
		threshold = cfg.Thresholds.Interactive
	}

	// FailOnWarning maps to threshold config
	opts.FailOnWarning = threshold.ShowWarnings && (threshold.BlockErrors > 0 || threshold.BlockCritical)

	return opts
}

// BridgeConfigFromConfig creates BridgeConfig from a ScannerConfig
func BridgeConfigFromConfig(cfg *config.ScannerConfig) BridgeConfig {
	minSev := SeverityWarning
	switch cfg.Beads.MinSeverity {
	case "critical":
		minSev = SeverityCritical
	case "warning":
		minSev = SeverityWarning
	case "info":
		minSev = SeverityInfo
	}

	return BridgeConfig{
		MinSeverity: minSev,
		DryRun:      false,
		Verbose:     false,
	}
}

// NewScannerWithConfig creates a new Scanner using config for UBS path
func NewScannerWithConfig(cfg *config.ScannerConfig) (*Scanner, error) {
	if cfg.UBSPath != "" {
		return &Scanner{binaryPath: cfg.UBSPath}, nil
	}
	return New()
}

// ShouldAutoCreateBeads returns true if auto-bead creation is enabled
func ShouldAutoCreateBeads(cfg *config.ScannerConfig) bool {
	return cfg.Beads.AutoCreate
}

// ShouldAutoCloseBeads returns true if auto-bead closing is enabled
func ShouldAutoCloseBeads(cfg *config.ScannerConfig) bool {
	return cfg.Beads.AutoClose
}
