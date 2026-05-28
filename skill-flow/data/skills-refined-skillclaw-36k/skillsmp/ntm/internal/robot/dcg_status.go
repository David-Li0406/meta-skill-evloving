package robot

import (
	"bufio"
	"context"
	"encoding/json"
	"os"
	"path/filepath"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/integrations/dcg"
	"github.com/Dicklesworthstone/ntm/internal/tools"
)

// DCGStatusOutput represents the response from --robot-dcg-status
type DCGStatusOutput struct {
	RobotResponse
	DCG DCGStatus `json:"dcg"`
}

// DCGStatus contains DCG status information
type DCGStatus struct {
	Enabled    bool            `json:"enabled"`
	Available  bool            `json:"available"`
	Version    string          `json:"version,omitempty"`
	BinaryPath string          `json:"binary_path,omitempty"`
	Config     DCGConfigStatus `json:"config"`
	Stats      DCGStatsStatus  `json:"stats"`
}

// DCGConfigStatus contains DCG configuration information
type DCGConfigStatus struct {
	AuditLog             string `json:"audit_log,omitempty"`
	AllowOverride        bool   `json:"allow_override"`
	CustomBlocklistCount int    `json:"custom_blocklist_count"`
	CustomWhitelistCount int    `json:"custom_whitelist_count"`
}

// DCGStatsStatus contains DCG runtime statistics
type DCGStatsStatus struct {
	CommandsChecked int                 `json:"commands_checked"`
	CommandsBlocked int                 `json:"commands_blocked"`
	LastBlocked     *LastBlockedCommand `json:"last_blocked,omitempty"`
}

// LastBlockedCommand contains information about the most recently blocked command
type LastBlockedCommand struct {
	Command   string `json:"command"`
	Timestamp string `json:"timestamp"`
	Pane      string `json:"pane"`
}

// PrintDCGStatus handles the --robot-dcg-status command
// Usage:
//
//	ntm --robot-dcg-status
func PrintDCGStatus() error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	adapter := tools.NewDCGAdapter()

	// Check DCG availability
	availability, err := adapter.GetAvailability(ctx)
	if err != nil {
		output := DCGStatusOutput{
			RobotResponse: NewErrorResponse(err, ErrCodeInternalError, "Failed to check DCG availability"),
			DCG: DCGStatus{
				Enabled:   false,
				Available: false,
			},
		}
		return outputJSON(output)
	}

	// Build status
	status := DCGStatus{
		Enabled:    availability.Available && availability.Compatible,
		Available:  availability.Available,
		BinaryPath: availability.Path,
	}

	if availability.Version.Major > 0 || availability.Version.Minor > 0 || availability.Version.Patch > 0 {
		status.Version = availability.Version.String()
	}

	// Get audit log stats
	stats := DCGStatsStatus{}
	auditLogPath := getDefaultAuditLogPath()

	// Try to read audit log for stats
	if auditLogPath != "" {
		blockedCount, lastBlocked := readAuditLogStats(auditLogPath)
		stats.CommandsBlocked = blockedCount
		stats.LastBlocked = lastBlocked
	}

	status.Config = DCGConfigStatus{
		AuditLog:             auditLogPath,
		AllowOverride:        false, // Default
		CustomBlocklistCount: 0,
		CustomWhitelistCount: 0,
	}
	status.Stats = stats

	output := DCGStatusOutput{
		RobotResponse: NewRobotResponse(true),
		DCG:           status,
	}

	return outputJSON(output)
}

// getDefaultAuditLogPath returns the default audit log path
func getDefaultAuditLogPath() string {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return ""
	}
	return filepath.Join(homeDir, ".local", "share", "ntm", "dcg-audit.jsonl")
}

// readAuditLogStats reads the audit log and returns statistics
func readAuditLogStats(logPath string) (int, *LastBlockedCommand) {
	file, err := os.Open(logPath)
	if err != nil {
		return 0, nil
	}
	defer file.Close()

	var count int
	var lastEntry *dcg.AuditEntry

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			continue
		}

		var entry dcg.AuditEntry
		if err := json.Unmarshal([]byte(line), &entry); err != nil {
			continue
		}

		if entry.Event == "command_blocked" {
			count++
			lastEntry = &entry
		}
	}

	if lastEntry == nil {
		return count, nil
	}

	return count, &LastBlockedCommand{
		Command:   lastEntry.Command,
		Timestamp: lastEntry.Timestamp,
		Pane:      lastEntry.Pane,
	}
}
