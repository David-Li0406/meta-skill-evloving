package styles

import (
	"os"
	"reflect"
	"testing"

	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

func TestDefaultGradientUsesCurrentThemeColors(t *testing.T) {
	t.Setenv("NTM_THEME", "latte")

	got := defaultGradient()
	want := []string{
		string(theme.CatppuccinLatte.Blue),
		string(theme.CatppuccinLatte.Mauve),
		string(theme.CatppuccinLatte.Pink),
	}

	if !reflect.DeepEqual(got, want) {
		t.Fatalf("defaultGradient() = %v, want %v", got, want)
	}
}

func TestDefaultSurface1UsesCurrentThemeColor(t *testing.T) {
	t.Setenv("NTM_THEME", "latte")

	got := string(defaultSurface1())
	want := string(theme.CatppuccinLatte.Surface1)

	if got != want {
		t.Fatalf("defaultSurface1() = %s, want %s", got, want)
	}
}

func TestDefaultGradientFollowsThemeChange(t *testing.T) {
	t.Setenv("NTM_THEME", "mocha")

	got := defaultGradient()
	want := []string{
		string(theme.CatppuccinMocha.Blue),
		string(theme.CatppuccinMocha.Mauve),
		string(theme.CatppuccinMocha.Pink),
	}

	if !reflect.DeepEqual(got, want) {
		t.Fatalf("after theme change, defaultGradient() = %v, want %v", got, want)
	}
}

// Ensure we don’t leak env between tests when running without -count=1.
func TestMain(m *testing.M) {
	code := m.Run()
	_ = os.Unsetenv("NTM_THEME")
	os.Exit(code)
}
