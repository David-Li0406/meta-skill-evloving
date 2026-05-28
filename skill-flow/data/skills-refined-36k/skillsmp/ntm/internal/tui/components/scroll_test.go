package components

import (
	"strings"
	"testing"
)

func TestScrollState_Indicator(t *testing.T) {
	tests := []struct {
		name     string
		state    ScrollState
		expected string
	}{
		{
			name:     "all visible",
			state:    ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 5},
			expected: "",
		},
		{
			name:     "empty list",
			state:    ScrollState{FirstVisible: 0, LastVisible: 0, TotalItems: 0},
			expected: "",
		},
		{
			name:     "more below only",
			state:    ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 10},
			expected: "▼",
		},
		{
			name:     "more above only",
			state:    ScrollState{FirstVisible: 5, LastVisible: 9, TotalItems: 10},
			expected: "▲",
		},
		{
			name:     "more both above and below",
			state:    ScrollState{FirstVisible: 3, LastVisible: 6, TotalItems: 10},
			expected: "▲▼",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := tt.state.Indicator()
			if got != tt.expected {
				t.Errorf("Indicator() = %q, want %q", got, tt.expected)
			}
		})
	}
}

func TestScrollState_AllVisible(t *testing.T) {
	tests := []struct {
		name     string
		state    ScrollState
		expected bool
	}{
		{
			name:     "all visible",
			state:    ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 5},
			expected: true,
		},
		{
			name:     "single item",
			state:    ScrollState{FirstVisible: 0, LastVisible: 0, TotalItems: 1},
			expected: true,
		},
		{
			name:     "partial view",
			state:    ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 10},
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := tt.state.AllVisible()
			if got != tt.expected {
				t.Errorf("AllVisible() = %v, want %v", got, tt.expected)
			}
		})
	}
}

func TestRenderScrollIndicator(t *testing.T) {
	tests := []struct {
		name          string
		opts          ScrollIndicatorOptions
		shouldBeEmpty bool
		shouldContain string
	}{
		{
			name: "all visible returns empty",
			opts: ScrollIndicatorOptions{
				State: ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 5},
				Width: 30,
			},
			shouldBeEmpty: true,
		},
		{
			name: "partial with count - wide format",
			opts: ScrollIndicatorOptions{
				State:     ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 20},
				Width:     30,
				ShowCount: true,
			},
			shouldContain: "Showing",
		},
		{
			name: "partial with count - medium format",
			opts: ScrollIndicatorOptions{
				State:     ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 20},
				Width:     20,
				ShowCount: true,
			},
			shouldContain: "/20)",
		},
		{
			name: "partial without count shows arrow",
			opts: ScrollIndicatorOptions{
				State:     ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 20},
				Width:     30,
				ShowCount: false,
			},
			shouldContain: "▼",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := RenderScrollIndicator(tt.opts)
			if tt.shouldBeEmpty && got != "" {
				t.Errorf("expected empty string, got %q", got)
			}
			if tt.shouldContain != "" && !strings.Contains(got, tt.shouldContain) {
				t.Errorf("expected indicator to contain %q, got %q", tt.shouldContain, got)
			}
		})
	}
}

func TestScrollFooter(t *testing.T) {
	// All visible - should return empty
	state := ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 5}
	got := ScrollFooter(state, 30)
	if got != "" {
		t.Errorf("ScrollFooter with all visible should be empty, got %q", got)
	}

	// Partial - should return non-empty
	state = ScrollState{FirstVisible: 0, LastVisible: 4, TotalItems: 20}
	got = ScrollFooter(state, 30)
	if got == "" {
		t.Errorf("ScrollFooter with partial view should not be empty")
	}
}
