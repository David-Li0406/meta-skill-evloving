package swarm

import (
	"fmt"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// SessionOrchestrator handles creation and management of tmux sessions
// for the weighted multi-project swarm system.
//
// The orchestrator uses an explicit tmux binary path (via tmux.BinaryPath())
// to avoid issues with shell plugins (e.g., zsh tmux plugins) that may
// intercept or modify tmux commands when relying on PATH resolution.
type SessionOrchestrator struct {
	// TmuxClient is the tmux client used for session operations.
	// If nil, the default tmux client is used.
	TmuxClient *tmux.Client

	// StaggerDelay is the delay between pane creations to avoid rate limits.
	StaggerDelay time.Duration
}

// NewSessionOrchestrator creates a new SessionOrchestrator with default settings.
func NewSessionOrchestrator() *SessionOrchestrator {
	return &SessionOrchestrator{
		TmuxClient:   nil, // Use default client
		StaggerDelay: 300 * time.Millisecond,
	}
}

// NewSessionOrchestratorWithClient creates a SessionOrchestrator with a custom tmux client.
func NewSessionOrchestratorWithClient(client *tmux.Client) *SessionOrchestrator {
	return &SessionOrchestrator{
		TmuxClient:   client,
		StaggerDelay: 300 * time.Millisecond,
	}
}

// NewRemoteSessionOrchestrator creates a SessionOrchestrator configured for remote SSH execution.
// The host parameter should be in the format "user@host" (e.g., "ubuntu@192.168.1.100").
// All tmux operations will be executed on the remote host via SSH.
func NewRemoteSessionOrchestrator(host string) *SessionOrchestrator {
	return &SessionOrchestrator{
		TmuxClient:   tmux.NewClient(host),
		StaggerDelay: 300 * time.Millisecond,
	}
}

// NewRemoteSessionOrchestratorWithDelay creates a remote SessionOrchestrator with custom stagger delay.
// The host parameter should be in the format "user@host".
// The staggerDelay parameter controls the delay between pane creations.
func NewRemoteSessionOrchestratorWithDelay(host string, staggerDelay time.Duration) *SessionOrchestrator {
	return &SessionOrchestrator{
		TmuxClient:   tmux.NewClient(host),
		StaggerDelay: staggerDelay,
	}
}

// tmuxClient returns the configured tmux client or the default client.
func (o *SessionOrchestrator) tmuxClient() *tmux.Client {
	if o.TmuxClient != nil {
		return o.TmuxClient
	}
	return tmux.DefaultClient
}

// CreateSessionResult contains the result of creating a single session.
type CreateSessionResult struct {
	SessionSpec SessionSpec
	SessionName string
	PaneIDs     []string
	Error       error
}

// OrchestrationResult contains the complete result of session orchestration.
type OrchestrationResult struct {
	Sessions        []CreateSessionResult
	TotalPanes      int
	SuccessfulPanes int
	FailedPanes     int
	Errors          []error
}

// CreateSessions creates all sessions defined in the SwarmPlan.
// It creates sessions, splits panes, sets titles, and applies tiled layout.
func (o *SessionOrchestrator) CreateSessions(plan *SwarmPlan) (*OrchestrationResult, error) {
	if plan == nil {
		return nil, fmt.Errorf("plan cannot be nil")
	}

	if len(plan.Sessions) == 0 {
		return &OrchestrationResult{}, nil
	}

	result := &OrchestrationResult{
		Sessions: make([]CreateSessionResult, 0, len(plan.Sessions)),
	}

	client := o.tmuxClient()

	for _, spec := range plan.Sessions {
		sessionResult := o.createSession(client, spec)
		result.Sessions = append(result.Sessions, sessionResult)

		if sessionResult.Error != nil {
			result.Errors = append(result.Errors, sessionResult.Error)
		}

		result.TotalPanes += spec.PaneCount
		result.SuccessfulPanes += len(sessionResult.PaneIDs)
		result.FailedPanes += spec.PaneCount - len(sessionResult.PaneIDs)
	}

	return result, nil
}

// createSession creates a single tmux session with its panes.
func (o *SessionOrchestrator) createSession(client *tmux.Client, spec SessionSpec) CreateSessionResult {
	result := CreateSessionResult{
		SessionSpec: spec,
		SessionName: spec.Name,
		PaneIDs:     make([]string, 0, spec.PaneCount),
	}

	// Validate session name
	if err := tmux.ValidateSessionName(spec.Name); err != nil {
		result.Error = fmt.Errorf("invalid session name %q: %w", spec.Name, err)
		return result
	}

	// Check if session already exists
	if client.SessionExists(spec.Name) {
		result.Error = fmt.Errorf("session %q already exists", spec.Name)
		return result
	}

	// Determine the directory for the session (use first pane's project or /tmp)
	directory := "/tmp"
	if len(spec.Panes) > 0 && spec.Panes[0].Project != "" {
		directory = spec.Panes[0].Project
	}

	// Create the session
	if err := client.CreateSession(spec.Name, directory); err != nil {
		result.Error = fmt.Errorf("failed to create session %q: %w", spec.Name, err)
		return result
	}

	// Get the initial pane ID
	panes, err := client.GetPanes(spec.Name)
	if err != nil || len(panes) == 0 {
		result.Error = fmt.Errorf("failed to get initial pane for session %q: %v", spec.Name, err)
		return result
	}

	// Set up the first pane
	firstPaneID := panes[0].ID
	if len(spec.Panes) > 0 {
		title := o.formatPaneTitle(spec.Name, spec.Panes[0])
		if err := client.SetPaneTitle(firstPaneID, title); err != nil {
			// Non-fatal, continue
		}
		result.PaneIDs = append(result.PaneIDs, firstPaneID)
	}

	// Create additional panes
	for i := 1; i < len(spec.Panes); i++ {
		paneSpec := spec.Panes[i]

		// Stagger pane creation to avoid rate limits
		if o.StaggerDelay > 0 && i > 0 {
			time.Sleep(o.StaggerDelay)
		}

		// Determine directory for this pane
		paneDir := "/tmp"
		if paneSpec.Project != "" {
			paneDir = paneSpec.Project
		}

		// Split the window to create a new pane
		paneID, err := client.SplitWindow(spec.Name, paneDir)
		if err != nil {
			// Log error but continue with other panes
			continue
		}

		// Set pane title
		title := o.formatPaneTitle(spec.Name, paneSpec)
		if err := client.SetPaneTitle(paneID, title); err != nil {
			// Non-fatal, continue
		}

		result.PaneIDs = append(result.PaneIDs, paneID)
	}

	// Apply tiled layout for even pane distribution
	if err := client.ApplyTiledLayout(spec.Name); err != nil {
		// Non-fatal, panes are still created
	}

	return result
}

// formatPaneTitle formats a pane title according to NTM convention.
func (o *SessionOrchestrator) formatPaneTitle(sessionName string, pane PaneSpec) string {
	return tmux.FormatPaneName(sessionName, pane.AgentType, pane.Index, "")
}

// DestroySession destroys a single session by name.
func (o *SessionOrchestrator) DestroySession(sessionName string) error {
	client := o.tmuxClient()

	if !client.SessionExists(sessionName) {
		return fmt.Errorf("session %q does not exist", sessionName)
	}

	return client.KillSession(sessionName)
}

// DestroySessions destroys all sessions created from a SwarmPlan.
func (o *SessionOrchestrator) DestroySessions(plan *SwarmPlan) error {
	if plan == nil {
		return nil
	}

	var errs []error
	for _, spec := range plan.Sessions {
		if err := o.DestroySession(spec.Name); err != nil {
			errs = append(errs, err)
		}
	}

	if len(errs) > 0 {
		return fmt.Errorf("failed to destroy %d session(s): %v", len(errs), errs[0])
	}

	return nil
}

// SessionExists checks if a session with the given name exists.
func (o *SessionOrchestrator) SessionExists(sessionName string) bool {
	return o.tmuxClient().SessionExists(sessionName)
}

// GetSessionPanes returns the panes in a session.
func (o *SessionOrchestrator) GetSessionPanes(sessionName string) ([]tmux.Pane, error) {
	return o.tmuxClient().GetPanes(sessionName)
}

// PaneGeometry represents the dimensions of a pane.
type PaneGeometry struct {
	Width  int `json:"width"`
	Height int `json:"height"`
}

// GeometryResult contains the geometry verification result for a session.
type GeometryResult struct {
	SessionName    string         `json:"session_name"`
	PaneCount      int            `json:"pane_count"`
	Geometries     []PaneGeometry `json:"geometries"`
	IsUniform      bool           `json:"is_uniform"`
	MaxWidthDelta  int            `json:"max_width_delta"`
	MaxHeightDelta int            `json:"max_height_delta"`
}

// VerifyGeometry checks if panes in a session have uniform geometry.
// Returns geometry information and whether panes are uniformly sized.
// Tolerance allows for small variations (e.g., 1-2 cells difference).
func (o *SessionOrchestrator) VerifyGeometry(sessionName string, tolerance int) (*GeometryResult, error) {
	client := o.tmuxClient()

	panes, err := client.GetPanes(sessionName)
	if err != nil {
		return nil, fmt.Errorf("failed to get panes for session %q: %w", sessionName, err)
	}

	if len(panes) == 0 {
		return &GeometryResult{
			SessionName: sessionName,
			PaneCount:   0,
			IsUniform:   true,
		}, nil
	}

	result := &GeometryResult{
		SessionName: sessionName,
		PaneCount:   len(panes),
		Geometries:  make([]PaneGeometry, len(panes)),
		IsUniform:   true,
	}

	// Collect geometries
	var minWidth, maxWidth, minHeight, maxHeight int
	for i, pane := range panes {
		result.Geometries[i] = PaneGeometry{
			Width:  pane.Width,
			Height: pane.Height,
		}

		if i == 0 {
			minWidth, maxWidth = pane.Width, pane.Width
			minHeight, maxHeight = pane.Height, pane.Height
		} else {
			if pane.Width < minWidth {
				minWidth = pane.Width
			}
			if pane.Width > maxWidth {
				maxWidth = pane.Width
			}
			if pane.Height < minHeight {
				minHeight = pane.Height
			}
			if pane.Height > maxHeight {
				maxHeight = pane.Height
			}
		}
	}

	result.MaxWidthDelta = maxWidth - minWidth
	result.MaxHeightDelta = maxHeight - minHeight

	// Check if within tolerance
	if result.MaxWidthDelta > tolerance || result.MaxHeightDelta > tolerance {
		result.IsUniform = false
	}

	return result, nil
}

// RebalanceGeometry reapplies tiled layout to ensure uniform pane sizes.
func (o *SessionOrchestrator) RebalanceGeometry(sessionName string) error {
	client := o.tmuxClient()

	if !client.SessionExists(sessionName) {
		return fmt.Errorf("session %q does not exist", sessionName)
	}

	return client.ApplyTiledLayout(sessionName)
}

// EnsureUniformGeometry verifies geometry and rebalances if needed.
// Returns the final geometry state after any corrections.
func (o *SessionOrchestrator) EnsureUniformGeometry(sessionName string, tolerance int) (*GeometryResult, error) {
	// First check current geometry
	result, err := o.VerifyGeometry(sessionName, tolerance)
	if err != nil {
		return nil, err
	}

	// If already uniform, return
	if result.IsUniform {
		return result, nil
	}

	// Rebalance and verify again
	if err := o.RebalanceGeometry(sessionName); err != nil {
		return result, fmt.Errorf("failed to rebalance geometry: %w", err)
	}

	// Re-verify after rebalancing
	return o.VerifyGeometry(sessionName, tolerance)
}

// GetAverageGeometry calculates the average pane dimensions for a session.
func (o *SessionOrchestrator) GetAverageGeometry(sessionName string) (*PaneGeometry, error) {
	panes, err := o.tmuxClient().GetPanes(sessionName)
	if err != nil {
		return nil, err
	}

	if len(panes) == 0 {
		return nil, fmt.Errorf("session %q has no panes", sessionName)
	}

	var totalWidth, totalHeight int
	for _, pane := range panes {
		totalWidth += pane.Width
		totalHeight += pane.Height
	}

	return &PaneGeometry{
		Width:  totalWidth / len(panes),
		Height: totalHeight / len(panes),
	}, nil
}

// TmuxBinaryPath returns the resolved path to the tmux binary being used.
// This uses an explicit binary path (preferring /usr/bin/tmux) to avoid
// issues with shell plugins that may intercept tmux commands.
func (o *SessionOrchestrator) TmuxBinaryPath() string {
	return tmux.BinaryPath()
}

// VerifyTmuxBinary checks if the tmux binary is accessible and functional.
// Returns the binary path if successful, or an error if tmux is not available.
func (o *SessionOrchestrator) VerifyTmuxBinary() (string, error) {
	if err := tmux.EnsureInstalled(); err != nil {
		return "", err
	}
	return tmux.BinaryPath(), nil
}

// TmuxBinaryInfo contains information about the tmux binary being used.
type TmuxBinaryInfo struct {
	Path      string `json:"path"`
	Available bool   `json:"available"`
	IsRemote  bool   `json:"is_remote"`
}

// GetTmuxBinaryInfo returns detailed information about the tmux binary configuration.
func (o *SessionOrchestrator) GetTmuxBinaryInfo() *TmuxBinaryInfo {
	client := o.tmuxClient()
	isRemote := client.Remote != ""

	info := &TmuxBinaryInfo{
		Path:      tmux.BinaryPath(),
		Available: tmux.IsInstalled(),
		IsRemote:  isRemote,
	}

	return info
}

// IsRemote returns true if the orchestrator is configured for remote SSH execution.
func (o *SessionOrchestrator) IsRemote() bool {
	return o.tmuxClient().Remote != ""
}

// RemoteHost returns the remote host string (e.g., "user@host") if configured,
// or an empty string if the orchestrator operates locally.
func (o *SessionOrchestrator) RemoteHost() string {
	return o.tmuxClient().Remote
}

// TestConnection verifies connectivity to the remote host (or local tmux).
// For remote orchestrators, this tests SSH connectivity.
// For local orchestrators, this verifies tmux is installed and accessible.
// Returns nil if the connection test succeeds, or an error describing the failure.
func (o *SessionOrchestrator) TestConnection() error {
	client := o.tmuxClient()

	if client.Remote == "" {
		// Local: verify tmux is installed
		if !tmux.IsInstalled() {
			return fmt.Errorf("tmux is not installed locally")
		}
		return nil
	}

	// Remote: verify SSH connectivity and tmux availability
	if !client.IsInstalled() {
		return fmt.Errorf("cannot connect to remote host %q or tmux is not installed", client.Remote)
	}
	return nil
}

// VerifyRemoteTmux checks if tmux is available and functional on the target host.
// For local orchestrators, this behaves the same as VerifyTmuxBinary.
// For remote orchestrators, this verifies the remote tmux installation.
// Returns the tmux version string if successful, or an error if tmux is not available.
func (o *SessionOrchestrator) VerifyRemoteTmux() (string, error) {
	client := o.tmuxClient()

	// Get tmux version to verify it's working
	version, err := client.Run("-V")
	if err != nil {
		if client.Remote != "" {
			return "", fmt.Errorf("failed to verify tmux on remote host %q: %w", client.Remote, err)
		}
		return "", fmt.Errorf("failed to verify local tmux: %w", err)
	}

	return version, nil
}

// RemoteConnectionInfo contains detailed information about the remote connection.
type RemoteConnectionInfo struct {
	Host        string `json:"host"`            // Remote host (user@host) or empty for local
	IsRemote    bool   `json:"is_remote"`       // Whether this is a remote connection
	Connected   bool   `json:"connected"`       // Whether connection test succeeded
	TmuxVersion string `json:"tmux_version"`    // tmux version string if available
	Error       string `json:"error,omitempty"` // Error message if connection failed
}

// GetRemoteConnectionInfo returns detailed information about the remote connection status.
// This is useful for diagnostics and status reporting.
func (o *SessionOrchestrator) GetRemoteConnectionInfo() *RemoteConnectionInfo {
	client := o.tmuxClient()
	info := &RemoteConnectionInfo{
		Host:     client.Remote,
		IsRemote: client.Remote != "",
	}

	version, err := o.VerifyRemoteTmux()
	if err != nil {
		info.Connected = false
		info.Error = err.Error()
	} else {
		info.Connected = true
		info.TmuxVersion = version
	}

	return info
}
