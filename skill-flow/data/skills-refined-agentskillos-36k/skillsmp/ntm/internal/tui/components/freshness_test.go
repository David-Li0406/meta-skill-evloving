package components

import (
	"strings"
	"testing"
	"time"
)

func TestIsStale(t *testing.T) {
	tests := []struct {
		name     string
		elapsed  time.Duration
		interval time.Duration
		expected bool
	}{
		{
			name:     "zero lastUpdate not stale",
			elapsed:  0, // will use time.Time{}
			interval: 10 * time.Second,
			expected: false,
		},
		{
			name:     "fresh data",
			elapsed:  5 * time.Second,
			interval: 10 * time.Second,
			expected: false,
		},
		{
			name:     "just under 2x interval not stale",
			elapsed:  19 * time.Second,
			interval: 10 * time.Second,
			expected: false,
		},
		{
			name:     "stale data (>2x interval)",
			elapsed:  25 * time.Second,
			interval: 10 * time.Second,
			expected: true,
		},
		{
			name:     "zero interval not stale",
			elapsed:  100 * time.Second,
			interval: 0,
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var lastUpdate time.Time
			if tt.elapsed > 0 {
				lastUpdate = time.Now().Add(-tt.elapsed)
			}
			got := IsStale(lastUpdate, tt.interval)
			if got != tt.expected {
				t.Errorf("IsStale() = %v, want %v", got, tt.expected)
			}
		})
	}
}

func TestRenderFreshnessIndicator(t *testing.T) {
	t.Run("zero lastUpdate returns empty", func(t *testing.T) {
		got := RenderFreshnessIndicator(FreshnessOptions{
			LastUpdate:      time.Time{},
			RefreshInterval: 10 * time.Second,
			Width:           30,
		})
		if got != "" {
			t.Errorf("expected empty string for zero time, got %q", got)
		}
	})

	t.Run("fresh data shows Updated", func(t *testing.T) {
		got := RenderFreshnessIndicator(FreshnessOptions{
			LastUpdate:      time.Now().Add(-5 * time.Second),
			RefreshInterval: 10 * time.Second,
			Width:           30,
		})
		if !strings.Contains(got, "Updated") {
			t.Errorf("expected 'Updated' in output, got %q", got)
		}
	})

	t.Run("shows seconds for recent update", func(t *testing.T) {
		got := RenderFreshnessIndicator(FreshnessOptions{
			LastUpdate:      time.Now().Add(-5 * time.Second),
			RefreshInterval: 10 * time.Second,
			Width:           30,
		})
		if !strings.Contains(got, "5s") && !strings.Contains(got, "ago") {
			t.Errorf("expected time indication, got %q", got)
		}
	})
}

func TestRenderStaleBadge(t *testing.T) {
	t.Run("fresh data returns empty", func(t *testing.T) {
		got := RenderStaleBadge(time.Now().Add(-5*time.Second), 10*time.Second)
		if got != "" {
			t.Errorf("expected empty string for fresh data, got %q", got)
		}
	})

	t.Run("stale data returns badge", func(t *testing.T) {
		got := RenderStaleBadge(time.Now().Add(-25*time.Second), 10*time.Second)
		if !strings.Contains(got, "STALE") {
			t.Errorf("expected STALE badge, got %q", got)
		}
	})
}
