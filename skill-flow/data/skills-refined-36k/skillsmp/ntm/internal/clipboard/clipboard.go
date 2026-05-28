package clipboard

import (
	"bytes"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strings"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
)

// Clipboard exposes a unified copy/paste interface across platforms.
// Use New() to pick the best available backend at runtime.
type Clipboard interface {
	Copy(text string) error
	Paste() (string, error)
	Available() bool
	Backend() string
}

// backend is an internal abstraction implemented per platform/tool.
type backend interface {
	copy(text string) error
	paste() (string, error)
	available() bool
	name() string
}

type detector struct {
	goos     string
	getenv   func(string) string
	lookPath func(string) error
	readFile func(string) ([]byte, error)
}

// defaultDetector uses the real environment and filesystem.
func defaultDetector() detector {
	return detector{
		goos:   runtime.GOOS,
		getenv: os.Getenv,
		lookPath: func(bin string) error {
			_, err := exec.LookPath(bin)
			return err
		},
		readFile: os.ReadFile,
	}
}

type clipboardImpl struct {
	b backend
}

func (c *clipboardImpl) Copy(text string) error { return c.b.copy(text) }
func (c *clipboardImpl) Paste() (string, error) { return c.b.paste() }
func (c *clipboardImpl) Available() bool        { return c.b.available() }
func (c *clipboardImpl) Backend() string        { return c.b.name() }

// New constructs a Clipboard using the current platform and available tools.
func New() (Clipboard, error) {
	return newWithDetector(defaultDetector())
}

// newWithDetector is test-only entrypoint that accepts a stub detector.
func newWithDetector(det detector) (Clipboard, error) {
	b, err := chooseBackend(det)
	if err != nil {
		return nil, err
	}
	return &clipboardImpl{b: b}, nil
}

func chooseBackend(det detector) (backend, error) {
	switch det.goos {
	case "darwin":
		if det.lookPath("pbcopy") == nil && det.lookPath("pbpaste") == nil {
			return &pbcopyBackend{}, nil
		}
		return nil, fmt.Errorf("pbcopy/pbpaste not found; install Xcode command line tools")

	case "linux":
		if isWSL(det) {
			if det.lookPath("clip.exe") == nil {
				// paste uses powershell.exe if present; copy still works without.
				hasPowershell := det.lookPath("powershell.exe") == nil
				return &wslBackend{hasPaste: hasPowershell}, nil
			}
			// Fall through to other Linux options if clip.exe unavailable.
		}

		if isWayland(det) {
			if det.lookPath("wl-copy") == nil {
				hasPaste := det.lookPath("wl-paste") == nil
				return &wlBackend{hasPaste: hasPaste}, nil
			}
		}

		// X11 tools - require DISPLAY
		if det.getenv("DISPLAY") != "" {
			if det.lookPath("xclip") == nil {
				return &xclipBackend{}, nil
			}
			if det.lookPath("xsel") == nil {
				return &xselBackend{}, nil
			}
		}

		// As a last resort on Linux, try Wayland if present even without env hint.
		if det.lookPath("wl-copy") == nil {
			hasPaste := det.lookPath("wl-paste") == nil
			return &wlBackend{hasPaste: hasPaste}, nil
		}

		if det.lookPath("clip.exe") == nil {
			hasPowershell := det.lookPath("powershell.exe") == nil
			return &wslBackend{hasPaste: hasPowershell}, nil
		}

		if det.lookPath("tmux") == nil && det.getenv("TMUX") != "" {
			return &tmuxBackend{}, nil
		}

		return nil, errors.New("no clipboard utility found (install wl-copy, xclip, or xsel)")

	default:
		return nil, fmt.Errorf("clipboard not supported on %s", det.goos)
	}
}

func isWSL(det detector) bool {
	if det.getenv("WSL_DISTRO_NAME") != "" || det.getenv("WSL_INTEROP") != "" {
		return true
	}
	data, err := det.readFile("/proc/version")
	if err == nil && bytes.Contains(bytes.ToLower(data), []byte("microsoft")) {
		return true
	}
	return false
}

func isWayland(det detector) bool {
	if strings.ToLower(det.getenv("XDG_SESSION_TYPE")) == "wayland" {
		return true
	}
	return det.getenv("WAYLAND_DISPLAY") != ""
}

// ==== Backends ====

type pbcopyBackend struct{}

func (pbcopyBackend) copy(text string) error {
	cmd := exec.Command("pbcopy")
	cmd.Stdin = strings.NewReader(text)
	return cmd.Run()
}

func (pbcopyBackend) paste() (string, error) {
	out, err := exec.Command("pbpaste").Output()
	return string(out), err
}

func (pbcopyBackend) available() bool { return true }
func (pbcopyBackend) name() string    { return "pbcopy" }

type wlBackend struct{ hasPaste bool }

func (b wlBackend) copy(text string) error {
	cmd := exec.Command("wl-copy")
	cmd.Stdin = strings.NewReader(text)
	return cmd.Run()
}

func (b wlBackend) paste() (string, error) {
	if !b.hasPaste {
		return "", errors.New("wl-paste not available")
	}
	out, err := exec.Command("wl-paste").Output()
	return string(out), err
}

func (b wlBackend) available() bool { return true }
func (b wlBackend) name() string    { return "wl-copy" }

type xclipBackend struct{}

func (xclipBackend) copy(text string) error {
	cmd := exec.Command("xclip", "-selection", "clipboard")
	cmd.Stdin = strings.NewReader(text)
	return cmd.Run()
}

func (xclipBackend) paste() (string, error) {
	out, err := exec.Command("xclip", "-selection", "clipboard", "-o").Output()
	return string(out), err
}

func (xclipBackend) available() bool { return true }
func (xclipBackend) name() string    { return "xclip" }

type xselBackend struct{}

func (xselBackend) copy(text string) error {
	cmd := exec.Command("xsel", "--clipboard", "--input")
	cmd.Stdin = strings.NewReader(text)
	return cmd.Run()
}

func (xselBackend) paste() (string, error) {
	out, err := exec.Command("xsel", "--clipboard", "--output").Output()
	return string(out), err
}

func (xselBackend) available() bool { return true }
func (xselBackend) name() string    { return "xsel" }

type wslBackend struct{ hasPaste bool }

func (b wslBackend) copy(text string) error {
	cmd := exec.Command("clip.exe")
	cmd.Stdin = strings.NewReader(text)
	return cmd.Run()
}

func (b wslBackend) paste() (string, error) {
	if !b.hasPaste {
		return "", errors.New("paste not available on WSL without powershell.exe")
	}
	out, err := exec.Command("powershell.exe", "Get-Clipboard").Output()
	return string(out), err
}

func (b wslBackend) available() bool { return true }
func (b wslBackend) name() string    { return "wsl-clipboard" }

type tmuxBackend struct{}

func (tmuxBackend) copy(text string) error {
	cmd := exec.Command(tmux.BinaryPath(), "load-buffer", "-")
	cmd.Stdin = strings.NewReader(text)
	return cmd.Run()
}

func (tmuxBackend) paste() (string, error) {
	out, err := exec.Command(tmux.BinaryPath(), "show-buffer").Output()
	return string(out), err
}

func (tmuxBackend) available() bool { return true }
func (tmuxBackend) name() string    { return "tmux-buffer" }
