package dashboard

import (
	"fmt"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tui/layout"
)

// Benchmarks for wide rendering performance (bd ntm-34qr).
// Additional mega layout benchmarks (bd ntm-jypl).

// BenchmarkMegaLayout benchmarks renderMegaLayout with varying pane counts.
// Target: <50ms initial, <200ms for 1000 panes.

func BenchmarkMegaLayout_10(b *testing.B) {
	m := newBenchModel(400, 60, 10) // 400 width triggers TierMega (>=320)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderMegaLayout()
	}
}

func BenchmarkMegaLayout_50(b *testing.B) {
	m := newBenchModel(400, 60, 50)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderMegaLayout()
	}
}

func BenchmarkMegaLayout_100(b *testing.B) {
	m := newBenchModel(400, 60, 100)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderMegaLayout()
	}
}

func BenchmarkMegaLayout_1000(b *testing.B) {
	m := newBenchModel(400, 60, 1000)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderMegaLayout()
	}
}

// BenchmarkUltraLayout benchmarks renderUltraLayout with varying pane counts.

func BenchmarkUltraLayout_10(b *testing.B) {
	m := newBenchModel(280, 50, 10) // 280 width triggers TierUltra (240-319)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderUltraLayout()
	}
}

func BenchmarkUltraLayout_100(b *testing.B) {
	m := newBenchModel(280, 50, 100)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderUltraLayout()
	}
}

func BenchmarkUltraLayout_1000(b *testing.B) {
	m := newBenchModel(280, 50, 1000)

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderUltraLayout()
	}
}

func BenchmarkPaneList_Wide_1000(b *testing.B) {
	m := newBenchModel(200, 50, 1000)
	listWidth := 90 // emulate wide split list panel

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderPaneList(listWidth)
	}
}

func BenchmarkPaneGrid_Compact_1000(b *testing.B) {
	m := newBenchModel(100, 40, 1000) // narrow/compact uses card grid

	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = m.renderPaneGrid()
	}
}

// newBenchModel builds a dashboard model with synthetic panes for benchmarks.
func newBenchModel(width, height, panes int) Model {
	m := New("bench", "")
	m.width = width
	m.height = height
	m.tier = layout.TierForWidth(width)

	m.panes = make([]tmux.Pane, panes)
	for i := 0; i < panes; i++ {
		agentType := tmux.AgentCodex
		switch i % 3 {
		case 0:
			agentType = tmux.AgentClaude
		case 1:
			agentType = tmux.AgentCodex
		case 2:
			agentType = tmux.AgentGemini
		}
		m.panes[i] = tmux.Pane{
			ID:      fmt.Sprintf("%%%d", i),
			Index:   i,
			Title:   fmt.Sprintf("bench_pane_%04d", i),
			Type:    agentType,
			Variant: "opus",
			Command: "run --long-command --with-flags",
			Width:   width / 2,
			Height:  height / 2,
			Active:  i == 0,
		}

		m.paneStatus[i] = PaneStatus{
			State:          "working",
			ContextPercent: 42.0,
			ContextLimit:   200000,
			ContextTokens:  84000,
		}
	}

	return m
}
