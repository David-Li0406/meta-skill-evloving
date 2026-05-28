package icons

import (
	"os"
	"reflect"
	"testing"

	"github.com/charmbracelet/lipgloss"
)

func assertNoEmptyIcons(t *testing.T, icons IconSet) {
	t.Helper()

	v := reflect.ValueOf(icons)
	typ := v.Type()
	for i := 0; i < v.NumField(); i++ {
		if v.Field(i).Kind() != reflect.String {
			continue
		}
		if v.Field(i).String() == "" {
			t.Fatalf("empty icon field %s", typ.Field(i).Name)
		}
	}
}

func assertMaxIconWidth(t *testing.T, icons IconSet, maxWidth int) {
	t.Helper()

	v := reflect.ValueOf(icons)
	typ := v.Type()
	for i := 0; i < v.NumField(); i++ {
		if v.Field(i).Kind() != reflect.String {
			continue
		}
		value := v.Field(i).String()
		w := lipgloss.Width(value)
		if w > maxWidth {
			t.Fatalf("icon field %s too wide: %q (width=%d, max=%d)", typ.Field(i).Name, value, w, maxWidth)
		}
	}
}

func TestDetectDefaults(t *testing.T) {
	// Clear env vars
	os.Unsetenv("NTM_ICONS")
	os.Unsetenv("NTM_USE_ICONS")
	os.Unsetenv("NERD_FONTS")

	// Should default to ASCII
	icons := Detect()
	if icons.Session != "[]" { // ASCII session
		t.Errorf("Expected ASCII default, got session=%q", icons.Session)
	}
}

func TestDetectExplicit(t *testing.T) {
	os.Setenv("NTM_ICONS", "unicode")
	defer os.Unsetenv("NTM_ICONS")

	icons := Detect()
	if icons.Session != "◆" { // Unicode session
		t.Errorf("Expected Unicode, got session=%q", icons.Session)
	}
	assertNoEmptyIcons(t, icons)
	assertMaxIconWidth(t, icons, 2)

	os.Setenv("NTM_ICONS", "ascii")
	icons = Detect()
	if icons.Session != "[]" {
		t.Errorf("Expected ASCII, got session=%q", icons.Session)
	}
	assertNoEmptyIcons(t, icons)
}

func TestDetectAuto(t *testing.T) {
	os.Setenv("NTM_ICONS", "auto")
	defer os.Unsetenv("NTM_ICONS")
	os.Setenv("NTM_USE_ICONS", "0")
	os.Setenv("NERD_FONTS", "0")
	defer os.Unsetenv("NTM_USE_ICONS")
	defer os.Unsetenv("NERD_FONTS")

	// This depends on environment, but should return something valid
	icons := Detect()
	if icons.Session == "" {
		t.Error("Returned empty icons")
	}
	assertNoEmptyIcons(t, icons)
}

func TestWithFallbackFillsMissingIcons(t *testing.T) {
	out := NerdFonts.WithFallback(Unicode).WithFallback(ASCII)
	assertNoEmptyIcons(t, out)
	assertMaxIconWidth(t, out, 2)

	// A couple targeted sanity checks: NerdFonts has blanks that should be filled.
	if NerdFonts.Search == "" && out.Search == "" {
		t.Fatal("expected Search to be filled via fallback")
	}
	if NerdFonts.CodeQuality == "" && out.CodeQuality == "" {
		t.Fatal("expected CodeQuality to be filled via fallback")
	}
}
