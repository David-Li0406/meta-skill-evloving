package cli

import (
	"testing"
)

func TestParsePaneList(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected []int
	}{
		{
			name:     "empty string",
			input:    "",
			expected: nil,
		},
		{
			name:     "single value",
			input:    "0",
			expected: []int{0},
		},
		{
			name:     "multiple values",
			input:    "0,1,2",
			expected: []int{0, 1, 2},
		},
		{
			name:     "with spaces",
			input:    "0, 1, 2",
			expected: []int{0, 1, 2},
		},
		{
			name:     "range",
			input:    "0-3",
			expected: []int{0, 1, 2, 3},
		},
		{
			name:     "mixed range and individual",
			input:    "0-2,5,7-9",
			expected: []int{0, 1, 2, 5, 7, 8, 9},
		},
		{
			name:     "single value range",
			input:    "5-5",
			expected: []int{5},
		},
		{
			name:     "invalid range (reversed)",
			input:    "5-3",
			expected: nil,
		},
		{
			name:     "trailing comma",
			input:    "0,1,",
			expected: []int{0, 1},
		},
		{
			name:     "leading comma",
			input:    ",0,1",
			expected: []int{0, 1},
		},
		{
			name:     "double comma",
			input:    "0,,1",
			expected: []int{0, 1},
		},
		{
			name:     "non-numeric ignored",
			input:    "0,abc,2",
			expected: []int{0, 2},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := parsePaneList(tt.input)

			// Handle nil vs empty slice comparison
			if tt.expected == nil && result == nil {
				return
			}
			if tt.expected == nil && len(result) == 0 {
				return
			}
			if len(result) == 0 && tt.expected == nil {
				return
			}

			if len(result) != len(tt.expected) {
				t.Errorf("parsePaneList(%q) = %v, want %v", tt.input, result, tt.expected)
				return
			}

			for i, v := range result {
				if v != tt.expected[i] {
					t.Errorf("parsePaneList(%q)[%d] = %d, want %d", tt.input, i, v, tt.expected[i])
				}
			}
		})
	}
}

func TestAdoptedAgentCounts_Total(t *testing.T) {
	tests := []struct {
		name     string
		counts   AdoptedAgentCounts
		expected int
	}{
		{
			name:     "all zeros",
			counts:   AdoptedAgentCounts{},
			expected: 0,
		},
		{
			name:     "only claude",
			counts:   AdoptedAgentCounts{Claude: 5},
			expected: 5,
		},
		{
			name:     "mixed",
			counts:   AdoptedAgentCounts{Claude: 3, Codex: 2, Gemini: 1, User: 1},
			expected: 7,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := tt.counts.Total()
			if result != tt.expected {
				t.Errorf("Total() = %d, want %d", result, tt.expected)
			}
		})
	}
}
