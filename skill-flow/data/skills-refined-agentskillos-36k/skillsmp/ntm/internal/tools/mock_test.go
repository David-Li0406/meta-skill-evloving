package tools

import (
	"context"
	"time"
)

// mockAdapter is a test adapter that can be configured
type mockAdapter struct {
	name      ToolName
	installed bool
	path      string
	version   Version
	caps      []Capability
	healthy   bool
}

// newMockAdapter creates a mock adapter for testing
func newMockAdapter(name ToolName, installed bool) *mockAdapter {
	return &mockAdapter{
		name:      name,
		installed: installed,
		path:      "/usr/local/bin/" + string(name),
		version:   Version{Major: 1, Minor: 0, Patch: 0},
		caps:      []Capability{CapRobotMode},
		healthy:   installed, // Healthy if installed
	}
}

func (m *mockAdapter) Name() ToolName {
	return m.name
}

func (m *mockAdapter) Detect() (string, bool) {
	if m.installed {
		return m.path, true
	}
	return "", false
}

func (m *mockAdapter) Version(ctx context.Context) (Version, error) {
	if !m.installed {
		return Version{}, ErrToolNotInstalled
	}
	return m.version, nil
}

func (m *mockAdapter) Capabilities(ctx context.Context) ([]Capability, error) {
	return m.caps, nil
}

func (m *mockAdapter) Health(ctx context.Context) (*HealthStatus, error) {
	if !m.installed {
		return &HealthStatus{
			Healthy:     false,
			Message:     "not installed",
			LastChecked: time.Now(),
		}, nil
	}

	return &HealthStatus{
		Healthy:     m.healthy,
		Message:     "ok",
		LastChecked: time.Now(),
	}, nil
}

func (m *mockAdapter) HasCapability(ctx context.Context, cap Capability) bool {
	for _, c := range m.caps {
		if c == cap {
			return true
		}
	}
	return false
}

func (m *mockAdapter) Info(ctx context.Context) (*ToolInfo, error) {
	health, _ := m.Health(ctx)
	return &ToolInfo{
		Name:         m.name,
		Installed:    m.installed,
		Version:      m.version,
		Capabilities: m.caps,
		Path:         m.path,
		Health:       *health,
	}, nil
}
