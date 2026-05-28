package layout

import "testing"

func TestTierForWidth(t *testing.T) {
	tests := []struct {
		width int
		want  Tier
	}{
		{0, TierNarrow},
		{119, TierNarrow},
		{120, TierSplit},
		{121, TierSplit},
		{199, TierSplit},
		{200, TierWide},
		{239, TierWide},
		{240, TierUltra},
		{319, TierUltra},
		{320, TierMega},
		{400, TierMega},
	}

	for _, tt := range tests {
		if got := TierForWidth(tt.width); got != tt.want {
			t.Errorf("TierForWidth(%d) = %v, want %v", tt.width, got, tt.want)
		}
	}
}

func TestSplitProportions(t *testing.T) {
	// Below threshold: should return total,0
	l, r := SplitProportions(100)
	if l != 100 || r != 0 {
		t.Fatalf("SplitProportions(100) = %d,%d want 100,0", l, r)
	}

	// At threshold: ensure budget applied and non-zero panes
	l, r = SplitProportions(140) // avail = 132 -> ~52/80
	if l <= 0 || r <= 0 {
		t.Fatalf("SplitProportions(140) returned zero widths: %d,%d", l, r)
	}
	if l+r > 140 {
		t.Fatalf("SplitProportions(140) sum %d exceeds total 140", l+r)
	}
}

func TestUltraProportions(t *testing.T) {
	// Below threshold falls back to center-only
	l, c, r := UltraProportions(239)
	if l != 0 || r != 0 || c != 239 {
		t.Fatalf("UltraProportions(239) = %d,%d,%d want 0,239,0", l, c, r)
	}

	width := 300 // Ultra tier
	l, c, r = UltraProportions(width)

	total := l + c + r
	expectedTotal := width - 6 // padding budget

	if total != expectedTotal {
		t.Errorf("UltraProportions(%d) total width = %d, want %d", width, total, expectedTotal)
	}

	if l == 0 || c == 0 || r == 0 {
		t.Errorf("UltraProportions(%d) returned zero width panel: %d/%d/%d", width, l, c, r)
	}
}

func TestMegaProportions(t *testing.T) {
	// Below threshold should return center-only
	p1, p2, p3, p4, p5 := MegaProportions(300)
	if p1 != 0 || p3 != 0 || p4 != 0 || p5 != 0 || p2 != 300 {
		t.Fatalf("MegaProportions(300) unexpected: %d,%d,%d,%d,%d", p1, p2, p3, p4, p5)
	}

	width := 400 // Mega tier
	p1, p2, p3, p4, p5 = MegaProportions(width)

	total := p1 + p2 + p3 + p4 + p5
	expectedTotal := width - 10 // padding budget

	if total != expectedTotal {
		t.Errorf("MegaProportions(%d) total width = %d, want %d", width, total, expectedTotal)
	}

	if p1 == 0 || p2 == 0 || p3 == 0 || p4 == 0 || p5 == 0 {
		t.Errorf("MegaProportions(%d) returned zero width panel", width)
	}
}

// TestTierForWidthBoundaries specifically tests the Ultra/Mega boundaries as
// specified in the tier system documentation.
func TestTierForWidthBoundaries(t *testing.T) {
	// Ultra boundary: 239 is TierWide, 240 is TierUltra
	if got := TierForWidth(239); got != TierWide {
		t.Errorf("TierForWidth(239) = %v, want TierWide", got)
	}
	if got := TierForWidth(240); got != TierUltra {
		t.Errorf("TierForWidth(240) = %v, want TierUltra", got)
	}

	// Mega boundary: 319 is TierUltra, 320 is TierMega
	if got := TierForWidth(319); got != TierUltra {
		t.Errorf("TierForWidth(319) = %v, want TierUltra", got)
	}
	if got := TierForWidth(320); got != TierMega {
		t.Errorf("TierForWidth(320) = %v, want TierMega", got)
	}
}

// TestTruncateRunes tests the rune-aware string truncation function.
func TestTruncateRunes(t *testing.T) {
	tests := []struct {
		name   string
		s      string
		max    int
		suffix string
		want   string
	}{
		{"empty string", "", 10, "...", ""},
		{"short string no truncate", "hello", 10, "...", "hello"},
		{"exact length", "hello", 5, "...", "hello"},
		{"truncate with suffix", "hello world", 8, "...", "hello..."},
		{"truncate no suffix", "hello world", 8, "", "hello wo"},
		{"max zero", "hello", 0, "...", ""},
		{"max negative", "hello", -1, "...", ""},
		{"suffix longer than max", "hello", 2, "...", "he"},
		{"unicode string", "héllo wörld", 8, "...", "héllo..."},
		{"emoji truncate", "👋🌍🎉✨", 3, ".", "👋🌍."},
		{"emoji exact", "👋🌍", 2, "...", "👋🌍"},
		{"single char max", "hello", 1, "", "h"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := TruncateRunes(tt.s, tt.max, tt.suffix)
			if got != tt.want {
				t.Errorf("TruncateRunes(%q, %d, %q) = %q, want %q",
					tt.s, tt.max, tt.suffix, got, tt.want)
			}
		})
	}
}

// TestSplitProportionsBoundary tests SplitProportions at exact threshold.
func TestSplitProportionsBoundary(t *testing.T) {
	// Just below threshold (119): should return total, 0
	l, r := SplitProportions(119)
	if l != 119 || r != 0 {
		t.Errorf("SplitProportions(119) = %d,%d want 119,0", l, r)
	}

	// Exactly at threshold (120): should split
	l, r = SplitProportions(120)
	if l <= 0 || r <= 0 {
		t.Errorf("SplitProportions(120) returned zero width: %d,%d", l, r)
	}
	if l+r > 120 {
		t.Errorf("SplitProportions(120) sum %d exceeds total", l+r)
	}
}

// TestUltraProportionsBoundary tests UltraProportions at exact thresholds.
func TestUltraProportionsBoundary(t *testing.T) {
	// At 239 (below Ultra threshold): center-only
	l, c, r := UltraProportions(239)
	if l != 0 || r != 0 || c != 239 {
		t.Errorf("UltraProportions(239) = %d,%d,%d want 0,239,0", l, c, r)
	}

	// At 240 (exactly Ultra threshold): should give 3-panel
	l, c, r = UltraProportions(240)
	if l == 0 || c == 0 || r == 0 {
		t.Errorf("UltraProportions(240) returned zero panel: %d,%d,%d", l, c, r)
	}
	total := l + c + r
	expectedTotal := 240 - 6 // padding budget
	if total != expectedTotal {
		t.Errorf("UltraProportions(240) total = %d, want %d", total, expectedTotal)
	}
}

// TestMegaProportionsBoundary tests MegaProportions at exact thresholds.
func TestMegaProportionsBoundary(t *testing.T) {
	// At 319 (below Mega threshold): center-only
	p1, p2, p3, p4, p5 := MegaProportions(319)
	if p1 != 0 || p3 != 0 || p4 != 0 || p5 != 0 || p2 != 319 {
		t.Errorf("MegaProportions(319) = %d,%d,%d,%d,%d want 0,319,0,0,0",
			p1, p2, p3, p4, p5)
	}

	// At 320 (exactly Mega threshold): should give 5-panel
	p1, p2, p3, p4, p5 = MegaProportions(320)
	if p1 == 0 || p2 == 0 || p3 == 0 || p4 == 0 || p5 == 0 {
		t.Errorf("MegaProportions(320) returned zero panel: %d,%d,%d,%d,%d",
			p1, p2, p3, p4, p5)
	}
	total := p1 + p2 + p3 + p4 + p5
	expectedTotal := 320 - 10 // padding budget
	if total != expectedTotal {
		t.Errorf("MegaProportions(320) total = %d, want %d", total, expectedTotal)
	}
}

// TestProportionsSmallValues tests proportion functions with edge case inputs.
func TestProportionsSmallValues(t *testing.T) {
	// Test SplitProportions with very small values
	l, r := SplitProportions(0)
	if l != 0 || r != 0 {
		t.Errorf("SplitProportions(0) = %d,%d want 0,0", l, r)
	}

	l, r = SplitProportions(5)
	if l != 5 || r != 0 {
		t.Errorf("SplitProportions(5) = %d,%d want 5,0", l, r)
	}

	// Test UltraProportions with very small values
	ul, uc, ur := UltraProportions(0)
	if ul != 0 || uc != 0 || ur != 0 {
		t.Errorf("UltraProportions(0) = %d,%d,%d want 0,0,0", ul, uc, ur)
	}

	// Test MegaProportions with very small values
	p1, p2, p3, p4, p5 := MegaProportions(0)
	if p1 != 0 || p2 != 0 || p3 != 0 || p4 != 0 || p5 != 0 {
		t.Errorf("MegaProportions(0) = %d,%d,%d,%d,%d want all zeros",
			p1, p2, p3, p4, p5)
	}
}

// TestTruncate tests the convenience truncation function with single-char ellipsis.
func TestTruncate(t *testing.T) {
	tests := []struct {
		name string
		s    string
		max  int
		want string
	}{
		{"empty string", "", 10, ""},
		{"short string no truncate", "hello", 10, "hello"},
		{"exact length", "hello", 5, "hello"},
		{"truncate with ellipsis", "hello world", 8, "hello w…"},
		{"max zero", "hello", 0, ""},
		{"max negative", "hello", -1, ""},
		{"max one", "hello", 1, "…"},
		{"unicode string", "héllo wörld", 8, "héllo w…"},
		{"emoji truncate", "👋🌍🎉✨", 3, "👋🌍…"},
		{"emoji exact", "👋🌍", 2, "👋🌍"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := Truncate(tt.s, tt.max)
			if got != tt.want {
				t.Errorf("Truncate(%q, %d) = %q, want %q",
					tt.s, tt.max, got, tt.want)
			}
		})
	}
}

// TestTruncateUsesEllipsis verifies Truncate uses single-char ellipsis (U+2026).
func TestTruncateUsesEllipsis(t *testing.T) {
	result := Truncate("hello world", 8)
	// Should end with "…" (U+2026), not "..." (three periods)
	if result != "hello w…" {
		t.Errorf("Truncate should use single-char ellipsis '…', got %q", result)
	}
	// Verify it's exactly 8 runes
	runes := []rune(result)
	if len(runes) != 8 {
		t.Errorf("Truncate result should be 8 runes, got %d", len(runes))
	}
}

// TestTierConstants verifies tier constant values match thresholds.
func TestTierConstants(t *testing.T) {
	// Verify threshold constants
	if SplitViewThreshold != 120 {
		t.Errorf("SplitViewThreshold = %d, want 120", SplitViewThreshold)
	}
	if WideViewThreshold != 200 {
		t.Errorf("WideViewThreshold = %d, want 200", WideViewThreshold)
	}
	if UltraWideViewThreshold != 240 {
		t.Errorf("UltraWideViewThreshold = %d, want 240", UltraWideViewThreshold)
	}
	if MegaWideViewThreshold != 320 {
		t.Errorf("MegaWideViewThreshold = %d, want 320", MegaWideViewThreshold)
	}

	// Verify tier enum values
	if TierNarrow != 0 {
		t.Errorf("TierNarrow = %d, want 0", TierNarrow)
	}
	if TierSplit != 1 {
		t.Errorf("TierSplit = %d, want 1", TierSplit)
	}
	if TierWide != 2 {
		t.Errorf("TierWide = %d, want 2", TierWide)
	}
	if TierUltra != 4 {
		t.Errorf("TierUltra = %d, want 4", TierUltra)
	}
	if TierMega != 5 {
		t.Errorf("TierMega = %d, want 5", TierMega)
	}
}

// TestTruncatePaneTitle tests the smart truncation function for pane titles
// that preserves the agent suffix (e.g., __cc_1) to keep panes distinguishable.
func TestTruncatePaneTitle(t *testing.T) {
	tests := []struct {
		name     string
		title    string
		maxWidth int
		want     string
	}{
		{
			name:     "fits without truncation",
			title:    "myproject__cc_1",
			maxWidth: 20,
			want:     "myproject__cc_1",
		},
		{
			name:     "truncates prefix preserves suffix",
			title:    "destructive_command_guard__cc_1",
			maxWidth: 20,
			want:     "destructive_c…__cc_1",
		},
		{
			name:     "truncates long prefix preserves suffix",
			title:    "very_long_project_name__cod_10",
			maxWidth: 18,
			want:     "very_long…__cod_10",
		},
		{
			name:     "multiple panes remain distinguishable",
			title:    "destructive_command_guard__cc_2",
			maxWidth: 20,
			want:     "destructive_c…__cc_2",
		},
		{
			name:     "gemini agent suffix",
			title:    "destructive_command_guard__gmi_3",
			maxWidth: 20,
			want:     "destructive_…__gmi_3",
		},
		{
			name:     "no suffix falls back to standard truncation",
			title:    "just_a_regular_long_name",
			maxWidth: 15,
			want:     "just_a_regular…",
		},
		{
			name:     "empty string",
			title:    "",
			maxWidth: 10,
			want:     "",
		},
		{
			name:     "zero width",
			title:    "myproject__cc_1",
			maxWidth: 0,
			want:     "",
		},
		{
			name:     "suffix only when prefix doesn't fit",
			title:    "x__cc_1",
			maxWidth: 7,
			want:     "x__cc_1",
		},
		{
			name:     "very tight width shows suffix",
			title:    "project__cc_1",
			maxWidth: 10,
			want:     "pro…__cc_1",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := TruncatePaneTitle(tt.title, tt.maxWidth)
			if got != tt.want {
				t.Errorf("TruncatePaneTitle(%q, %d) = %q, want %q",
					tt.title, tt.maxWidth, got, tt.want)
			}
		})
	}
}

// TestTruncatePaneTitle_DistinguishableOutput verifies that panes with the same
// project prefix but different agent numbers produce distinguishable output.
func TestTruncatePaneTitle_DistinguishableOutput(t *testing.T) {
	titles := []string{
		"destructive_command_guard__cc_1",
		"destructive_command_guard__cc_2",
		"destructive_command_guard__cc_3",
		"destructive_command_guard__cod_1",
		"destructive_command_guard__gmi_1",
	}

	maxWidth := 20
	results := make(map[string]bool)

	for _, title := range titles {
		truncated := TruncatePaneTitle(title, maxWidth)
		if results[truncated] {
			t.Errorf("duplicate truncated output %q from different titles", truncated)
		}
		results[truncated] = true
	}

	// Verify we got unique outputs for each input
	if len(results) != len(titles) {
		t.Errorf("expected %d unique outputs, got %d", len(titles), len(results))
	}
}
