package styles

import "testing"

func TestDefaultSpacing(t *testing.T) {
	s := DefaultSpacing

	if s.None != 0 {
		t.Errorf("None = %d, want 0", s.None)
	}
	if s.XS <= s.None {
		t.Errorf("XS (%d) should be > None (%d)", s.XS, s.None)
	}
	if s.SM <= s.XS {
		t.Errorf("SM (%d) should be > XS (%d)", s.SM, s.XS)
	}
	if s.MD <= s.SM {
		t.Errorf("MD (%d) should be > SM (%d)", s.MD, s.SM)
	}
	if s.LG <= s.MD {
		t.Errorf("LG (%d) should be > MD (%d)", s.LG, s.MD)
	}
	if s.XL <= s.LG {
		t.Errorf("XL (%d) should be > LG (%d)", s.XL, s.LG)
	}
	if s.XXL <= s.XL {
		t.Errorf("XXL (%d) should be > XL (%d)", s.XXL, s.XL)
	}
}

func TestDefaultSize(t *testing.T) {
	s := DefaultSize

	if s.XS <= 0 {
		t.Errorf("XS should be > 0, got %d", s.XS)
	}
	if s.SM <= s.XS {
		t.Errorf("SM (%d) should be > XS (%d)", s.SM, s.XS)
	}
	if s.MD <= s.SM {
		t.Errorf("MD (%d) should be > SM (%d)", s.MD, s.SM)
	}
	if s.LG <= s.MD {
		t.Errorf("LG (%d) should be > MD (%d)", s.LG, s.MD)
	}
	if s.XL <= s.LG {
		t.Errorf("XL (%d) should be > LG (%d)", s.XL, s.LG)
	}
	if s.XXL <= s.XL {
		t.Errorf("XXL (%d) should be > XL (%d)", s.XXL, s.XL)
	}
}

func TestDefaultTypography(t *testing.T) {
	typ := DefaultTypography

	// Font sizes should increase
	if typ.SizeXS <= 0 {
		t.Errorf("SizeXS should be > 0, got %d", typ.SizeXS)
	}
	if typ.SizeSM <= typ.SizeXS {
		t.Errorf("SizeSM (%d) should be > SizeXS (%d)", typ.SizeSM, typ.SizeXS)
	}
	if typ.SizeMD <= typ.SizeSM {
		t.Errorf("SizeMD (%d) should be > SizeSM (%d)", typ.SizeMD, typ.SizeSM)
	}
	if typ.SizeLG <= typ.SizeMD {
		t.Errorf("SizeLG (%d) should be > SizeMD (%d)", typ.SizeLG, typ.SizeMD)
	}
	if typ.SizeXL <= typ.SizeLG {
		t.Errorf("SizeXL (%d) should be > SizeLG (%d)", typ.SizeXL, typ.SizeLG)
	}
	if typ.SizeXXL <= typ.SizeXL {
		t.Errorf("SizeXXL (%d) should be > SizeXL (%d)", typ.SizeXXL, typ.SizeXL)
	}

	// Line heights should increase
	if typ.LineHeightNormal < typ.LineHeightTight {
		t.Errorf("LineHeightNormal (%d) should be >= LineHeightTight (%d)", typ.LineHeightNormal, typ.LineHeightTight)
	}
	if typ.LineHeightLoose < typ.LineHeightNormal {
		t.Errorf("LineHeightLoose (%d) should be >= LineHeightNormal (%d)", typ.LineHeightLoose, typ.LineHeightNormal)
	}
}

func TestDefaultLayout(t *testing.T) {
	l := DefaultLayout

	// All values should be non-negative
	tests := []struct {
		name  string
		value int
	}{
		{"MarginPage", l.MarginPage},
		{"MarginSection", l.MarginSection},
		{"MarginItem", l.MarginItem},
		{"PaddingCard", l.PaddingCard},
		{"PaddingInline", l.PaddingInline},
		{"PaddingInput", l.PaddingInput},
		{"IconWidth", l.IconWidth},
		{"LabelWidth", l.LabelWidth},
		{"BadgeMinWidth", l.BadgeMinWidth},
		{"InputMinWidth", l.InputMinWidth},
		{"ButtonMinWidth", l.ButtonMinWidth},
		{"ListIndent", l.ListIndent},
		{"ListItemPadding", l.ListItemPadding},
		{"ListGutterWidth", l.ListGutterWidth},
		{"TableColumnGap", l.TableColumnGap},
		{"TableRowPadding", l.TableRowPadding},
		{"ModalWidth", l.ModalWidth},
		{"ModalMinHeight", l.ModalMinHeight},
		{"DashCardWidth", l.DashCardWidth},
		{"DashCardHeight", l.DashCardHeight},
		{"DashGridGap", l.DashGridGap},
	}

	for _, tt := range tests {
		if tt.value < 0 {
			t.Errorf("%s should be >= 0, got %d", tt.name, tt.value)
		}
	}

	// Specific sanity checks
	if l.ModalWidth <= l.InputMinWidth {
		t.Errorf("ModalWidth (%d) should be > InputMinWidth (%d)", l.ModalWidth, l.InputMinWidth)
	}
}

func TestDefaultAnimation(t *testing.T) {
	a := DefaultAnimation

	if a.TickFast <= 0 {
		t.Errorf("TickFast should be > 0, got %d", a.TickFast)
	}
	if a.TickNormal <= a.TickFast {
		t.Errorf("TickNormal (%d) should be > TickFast (%d)", a.TickNormal, a.TickFast)
	}
	if a.TickSlow <= a.TickNormal {
		t.Errorf("TickSlow (%d) should be > TickNormal (%d)", a.TickSlow, a.TickNormal)
	}

	if a.FramesFast <= 0 {
		t.Errorf("FramesFast should be > 0, got %d", a.FramesFast)
	}
	if a.FramesNormal <= 0 {
		t.Errorf("FramesNormal should be > 0, got %d", a.FramesNormal)
	}
	if a.FramesSlow <= 0 {
		t.Errorf("FramesSlow should be > 0, got %d", a.FramesSlow)
	}
}

func TestDefaultBreakpoints(t *testing.T) {
	bp := DefaultBreakpoints

	if bp.XS <= 0 {
		t.Errorf("XS should be > 0, got %d", bp.XS)
	}
	if bp.SM <= bp.XS {
		t.Errorf("SM (%d) should be > XS (%d)", bp.SM, bp.XS)
	}
	if bp.MD <= bp.SM {
		t.Errorf("MD (%d) should be > SM (%d)", bp.MD, bp.SM)
	}
	if bp.LG <= bp.MD {
		t.Errorf("LG (%d) should be > MD (%d)", bp.LG, bp.MD)
	}
	if bp.XL <= bp.LG {
		t.Errorf("XL (%d) should be > LG (%d)", bp.XL, bp.LG)
	}
}

func TestBorderRadius(t *testing.T) {
	tests := []struct {
		name     string
		radius   BorderRadius
		expected int
	}{
		{"None", RadiusNone, 0},
		{"Small", RadiusSmall, 1},
		{"Medium", RadiusMedium, 2},
		{"Large", RadiusLarge, 3},
		{"Full", RadiusFull, 4},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if int(tt.radius) != tt.expected {
				t.Errorf("%s = %d, want %d", tt.name, tt.radius, tt.expected)
			}
		})
	}
}

func TestZIndex(t *testing.T) {
	// Verify ordering
	if ZIndexBase >= ZIndexFloating {
		t.Errorf("ZIndexBase (%d) should be < ZIndexFloating (%d)", ZIndexBase, ZIndexFloating)
	}
	if ZIndexFloating >= ZIndexModal {
		t.Errorf("ZIndexFloating (%d) should be < ZIndexModal (%d)", ZIndexFloating, ZIndexModal)
	}
	if ZIndexModal >= ZIndexOverlay {
		t.Errorf("ZIndexModal (%d) should be < ZIndexOverlay (%d)", ZIndexModal, ZIndexOverlay)
	}
	if ZIndexOverlay >= ZIndexTooltip {
		t.Errorf("ZIndexOverlay (%d) should be < ZIndexTooltip (%d)", ZIndexOverlay, ZIndexTooltip)
	}
	if ZIndexTooltip >= ZIndexMax {
		t.Errorf("ZIndexTooltip (%d) should be < ZIndexMax (%d)", ZIndexTooltip, ZIndexMax)
	}
}

func TestDefaultTokens(t *testing.T) {
	tokens := DefaultTokens()

	// Verify all components are set
	if tokens.Spacing.MD == 0 {
		t.Error("Spacing should be initialized")
	}
	if tokens.Size.MD == 0 {
		t.Error("Size should be initialized")
	}
	if tokens.Typography.SizeMD == 0 {
		t.Error("Typography should be initialized")
	}
	if tokens.Layout.MarginPage == 0 && tokens.Layout.ModalWidth == 0 {
		t.Error("Layout should be initialized")
	}
	if tokens.Animation.TickNormal == 0 {
		t.Error("Animation should be initialized")
	}
	if tokens.Breakpoints.MD == 0 {
		t.Error("Breakpoints should be initialized")
	}
}

func TestCompact(t *testing.T) {
	compact := Compact()
	def := DefaultTokens()

	// Compact spacing should be smaller
	if compact.Spacing.MD >= def.Spacing.MD {
		t.Errorf("Compact spacing MD (%d) should be < default (%d)", compact.Spacing.MD, def.Spacing.MD)
	}

	// Compact sizes should be smaller
	if compact.Size.MD >= def.Size.MD {
		t.Errorf("Compact size MD (%d) should be < default (%d)", compact.Size.MD, def.Size.MD)
	}

	// Compact layout should be smaller
	if compact.Layout.ModalWidth >= def.Layout.ModalWidth {
		t.Errorf("Compact ModalWidth (%d) should be < default (%d)", compact.Layout.ModalWidth, def.Layout.ModalWidth)
	}
}

func TestSpacious(t *testing.T) {
	spacious := Spacious()
	def := DefaultTokens()

	// Spacious spacing should be larger
	if spacious.Spacing.MD <= def.Spacing.MD {
		t.Errorf("Spacious spacing MD (%d) should be > default (%d)", spacious.Spacing.MD, def.Spacing.MD)
	}

	// Spacious sizes should be larger
	if spacious.Size.MD <= def.Size.MD {
		t.Errorf("Spacious size MD (%d) should be > default (%d)", spacious.Size.MD, def.Size.MD)
	}

	// Spacious layout should be larger
	if spacious.Layout.ModalWidth <= def.Layout.ModalWidth {
		t.Errorf("Spacious ModalWidth (%d) should be > default (%d)", spacious.Layout.ModalWidth, def.Layout.ModalWidth)
	}
}

func TestTokensForWidth(t *testing.T) {
	bp := DefaultBreakpoints

	tests := []struct {
		name           string
		width          int
		expectCompact  bool
		expectDefault  bool
		expectSpacious bool
	}{
		{"very narrow", 20, true, false, false},
		{"narrow", bp.XS - 1, true, false, false},
		{"small", bp.XS + 10, false, true, false},
		{"medium", bp.SM + 10, false, true, false},
		{"large", bp.MD + 10, false, false, true},
		{"very wide", 150, false, false, true},
	}

	compactTokens := Compact()
	defaultTokens := DefaultTokens()
	spaciousTokens := Spacious()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			tokens := TokensForWidth(tt.width)

			if tt.expectCompact && tokens.Spacing.MD != compactTokens.Spacing.MD {
				t.Errorf("width %d should use compact tokens", tt.width)
			}
			if tt.expectDefault && tokens.Spacing.MD != defaultTokens.Spacing.MD {
				t.Errorf("width %d should use default tokens", tt.width)
			}
			if tt.expectSpacious && tokens.Spacing.MD != spaciousTokens.Spacing.MD {
				t.Errorf("width %d should use spacious tokens", tt.width)
			}
		})
	}
}
