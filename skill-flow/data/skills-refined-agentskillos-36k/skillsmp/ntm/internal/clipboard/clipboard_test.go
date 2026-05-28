package clipboard

import (
	"fmt"
	"os"
	"testing"
)

func newStubDetector(goos string, env map[string]string, bins map[string]bool, version string) detector {
	getenv := func(key string) string {
		if env == nil {
			return ""
		}
		return env[key]
	}
	lookPath := func(bin string) error {
		if bins != nil && bins[bin] {
			return nil
		}
		return fmt.Errorf("not found")
	}
	readFile := func(path string) ([]byte, error) {
		if path == "/proc/version" && version != "" {
			return []byte(version), nil
		}
		return nil, os.ErrNotExist
	}
	return detector{
		goos:     goos,
		getenv:   getenv,
		lookPath: lookPath,
		readFile: readFile,
	}
}

func TestChooseBackendDarwinPbcopy(t *testing.T) {
	det := newStubDetector("darwin", nil, map[string]bool{"pbcopy": true, "pbpaste": true}, "")
	b, err := chooseBackend(det)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if b.name() != "pbcopy" {
		t.Fatalf("expected pbcopy backend, got %s", b.name())
	}
}

func TestChooseBackendWayland(t *testing.T) {
	det := newStubDetector("linux", map[string]string{"XDG_SESSION_TYPE": "wayland"}, map[string]bool{"wl-copy": true, "wl-paste": true}, "")
	b, err := chooseBackend(det)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if b.name() != "wl-copy" {
		t.Fatalf("expected wl-copy backend, got %s", b.name())
	}
}

func TestChooseBackendXclip(t *testing.T) {
	det := newStubDetector("linux", map[string]string{"DISPLAY": ":0"}, map[string]bool{"xclip": true}, "")
	b, err := chooseBackend(det)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if b.name() != "xclip" {
		t.Fatalf("expected xclip backend, got %s", b.name())
	}
}

func TestChooseBackendXselFallback(t *testing.T) {
	det := newStubDetector("linux", map[string]string{"DISPLAY": ":0"}, map[string]bool{"xsel": true}, "")
	b, err := chooseBackend(det)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if b.name() != "xsel" {
		t.Fatalf("expected xsel backend, got %s", b.name())
	}
}

func TestChooseBackendWSL(t *testing.T) {
	det := newStubDetector("linux", map[string]string{"WSL_DISTRO_NAME": "Ubuntu"}, map[string]bool{"clip.exe": true, "powershell.exe": true}, "")
	b, err := chooseBackend(det)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if b.name() != "wsl-clipboard" {
		t.Fatalf("expected wsl-clipboard backend, got %s", b.name())
	}
}

func TestChooseBackendTmuxFallback(t *testing.T) {
	det := newStubDetector("linux", map[string]string{"TMUX": "1"}, map[string]bool{"tmux": true}, "")
	b, err := chooseBackend(det)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if b.name() != "tmux-buffer" {
		t.Fatalf("expected tmux-buffer backend, got %s", b.name())
	}
}

func TestChooseBackendNoTools(t *testing.T) {
	det := newStubDetector("linux", nil, nil, "")
	if _, err := chooseBackend(det); err == nil {
		t.Fatalf("expected error when no clipboard tools found")
	}
}
