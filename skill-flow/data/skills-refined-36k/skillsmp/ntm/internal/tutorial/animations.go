package tutorial

import (
	"fmt"
	"math"
	"math/rand"
	"strings"

	"github.com/mattn/go-runewidth"

	"github.com/Dicklesworthstone/ntm/internal/tui/styles"
)

// ParticleType defines different particle effects
type ParticleType int

const (
	ParticleSparkle ParticleType = iota
	ParticleStar
	ParticleConfetti
	ParticleFirework
	ParticleRain
	ParticleSnow
	ParticleGlow
)

// Particle represents an animated particle
type Particle struct {
	X, Y     float64
	VX, VY   float64
	Life     int
	MaxLife  int
	Type     ParticleType
	Char     string
	Color    string
	Size     int
	Gravity  float64
	Friction float64
}

// NewParticle creates a new particle at the given position
func NewParticle(x, y int, ptype ParticleType) Particle {
	p := Particle{
		X:       float64(x),
		Y:       float64(y),
		MaxLife: 30 + rand.Intn(30),
		Type:    ptype,
		Size:    1,
		Gravity: 0.1,
	}
	p.Life = p.MaxLife

	// Set properties based on type
	switch ptype {
	case ParticleSparkle:
		p.Char = "✨"
		p.Color = "#f9e2af"
		p.VX = (rand.Float64() - 0.5) * 2
		p.VY = (rand.Float64() - 0.5) * 2
		p.Gravity = 0
		p.MaxLife = 20 + rand.Intn(20)
		p.Life = p.MaxLife

	case ParticleStar:
		chars := []string{"★", "✦", "✧", "⋆", "✶"}
		p.Char = chars[rand.Intn(len(chars))]
		colors := []string{"#f9e2af", "#f5c2e7", "#89b4fa", "#a6e3a1"}
		p.Color = colors[rand.Intn(len(colors))]
		p.VX = (rand.Float64() - 0.5) * 3
		p.VY = -rand.Float64() * 2
		p.Gravity = 0.08

	case ParticleConfetti:
		chars := []string{"■", "●", "▲", "◆", "★"}
		p.Char = chars[rand.Intn(len(chars))]
		colors := []string{"#f38ba8", "#fab387", "#f9e2af", "#a6e3a1", "#89b4fa", "#cba6f7", "#f5c2e7"}
		p.Color = colors[rand.Intn(len(colors))]
		p.VX = (rand.Float64() - 0.5) * 4
		p.VY = -rand.Float64()*3 - 1
		p.Gravity = 0.15
		p.MaxLife = 40 + rand.Intn(30)
		p.Life = p.MaxLife

	case ParticleFirework:
		p.Char = "●"
		colors := []string{"#f38ba8", "#fab387", "#f9e2af", "#a6e3a1", "#89dceb", "#cba6f7"}
		p.Color = colors[rand.Intn(len(colors))]
		angle := rand.Float64() * math.Pi * 2
		speed := rand.Float64()*2 + 1
		p.VX = math.Cos(angle) * speed
		p.VY = math.Sin(angle) * speed
		p.Gravity = 0.05

	case ParticleRain:
		p.Char = "│"
		p.Color = "#89b4fa"
		p.VX = 0
		p.VY = rand.Float64()*2 + 1
		p.Gravity = 0.1
		p.MaxLife = 60
		p.Life = p.MaxLife

	case ParticleSnow:
		chars := []string{"❄", "❅", "❆", "✻", "•"}
		p.Char = chars[rand.Intn(len(chars))]
		p.Color = "#cdd6f4"
		p.VX = (rand.Float64() - 0.5) * 0.5
		p.VY = rand.Float64()*0.5 + 0.3
		p.Gravity = 0
		p.MaxLife = 100 + rand.Intn(50)
		p.Life = p.MaxLife

	case ParticleGlow:
		p.Char = "◉"
		p.Color = "#f5c2e7"
		p.VX = 0
		p.VY = 0
		p.Gravity = 0
		p.MaxLife = 40
		p.Life = p.MaxLife
	}

	return p
}

// Update advances the particle simulation
func (p *Particle) Update() {
	p.VY += p.Gravity
	p.VX *= (1 - p.Friction)
	p.X += p.VX
	p.Y += p.VY
	p.Life--
}

// Render returns the styled particle character
func (p Particle) Render() string {
	// Fade based on life
	alpha := float64(p.Life) / float64(p.MaxLife)
	if alpha < 0.3 {
		return ""
	}

	color := styles.ParseHex(p.Color)
	// Apply alpha to brightness
	color.R = int(float64(color.R) * alpha)
	color.G = int(float64(color.G) * alpha)
	color.B = int(float64(color.B) * alpha)

	return fmt.Sprintf("\x1b[38;2;%d;%d;%dm%s\x1b[0m", color.R, color.G, color.B, p.Char)
}

// TypingAnimation creates a typing effect for text
type TypingAnimation struct {
	Lines       []string
	CurrentChar int
	Speed       int // ticks per character
	Cursor      string
	CursorBlink bool
	Done        bool
}

// NewTypingAnimation creates a new typing animation
func NewTypingAnimation(lines []string) *TypingAnimation {
	return &TypingAnimation{
		Lines:       lines,
		Speed:       2,
		Cursor:      "▌",
		CursorBlink: true,
	}
}

// Update advances the typing animation
func (t *TypingAnimation) Update(tick int) {
	if tick%t.Speed == 0 {
		total := 0
		for _, line := range t.Lines {
			total += len(line) + 1 // +1 for newline
		}

		if t.CurrentChar < total {
			t.CurrentChar++
		} else {
			t.Done = true
		}
	}
}

// Render returns the currently visible text with cursor
func (t *TypingAnimation) Render(tick int) string {
	if t.Done {
		return strings.Join(t.Lines, "\n")
	}

	var result strings.Builder
	remaining := t.CurrentChar

	for i, line := range t.Lines {
		if remaining <= 0 {
			break
		}

		if remaining >= len(line)+1 {
			result.WriteString(line)
			if i < len(t.Lines)-1 {
				result.WriteString("\n")
			}
			remaining -= len(line) + 1
		} else {
			result.WriteString(line[:remaining])
			// Add cursor
			if t.CursorBlink && (tick/8)%2 == 0 {
				result.WriteString(t.Cursor)
			}
			remaining = 0
		}
	}

	return result.String()
}

// RevealAnimation creates a line-by-line reveal effect
type RevealAnimation struct {
	Lines       []string
	CurrentLine int
	Speed       int
	RevealStyle string // "fade", "slide", "typewriter"
	Done        bool
}

// NewRevealAnimation creates a new reveal animation
func NewRevealAnimation(lines []string, style string) *RevealAnimation {
	return &RevealAnimation{
		Lines:       lines,
		Speed:       4,
		RevealStyle: style,
	}
}

// Update advances the reveal animation
func (r *RevealAnimation) Update(tick int) {
	if tick%r.Speed == 0 && r.CurrentLine < len(r.Lines) {
		r.CurrentLine++
		if r.CurrentLine >= len(r.Lines) {
			r.Done = true
		}
	}
}

// Render returns the currently visible lines
func (r *RevealAnimation) Render(tick int) string {
	var lines []string
	for i := 0; i < r.CurrentLine && i < len(r.Lines); i++ {
		lines = append(lines, r.Lines[i])
	}
	return strings.Join(lines, "\n")
}

// WaveText creates a wave animation effect on text
func WaveText(text string, tick int, amplitude float64, colors []string) string {
	runes := []rune(text)
	var result strings.Builder

	for i, r := range runes {
		if r == ' ' || r == '\n' {
			result.WriteRune(r)
			continue
		}

		// Calculate wave offset
		phase := float64(i)*0.3 + float64(tick)*0.15
		offset := math.Sin(phase) * amplitude

		// Calculate color based on position
		colorIdx := (i + tick/3) % len(colors)
		color := styles.ParseHex(colors[colorIdx])

		// Apply brightness based on wave
		brightness := 0.7 + 0.3*((offset+amplitude)/(amplitude*2))
		color.R = clamp(int(float64(color.R) * brightness))
		color.G = clamp(int(float64(color.G) * brightness))
		color.B = clamp(int(float64(color.B) * brightness))

		result.WriteString(fmt.Sprintf("\x1b[38;2;%d;%d;%dm%c\x1b[0m", color.R, color.G, color.B, r))
	}

	return result.String()
}

// PulseText creates a pulsing brightness effect
func PulseText(text string, tick int, baseColor string) string {
	color := styles.ParseHex(baseColor)

	// Sine wave pulsing
	pulse := 0.6 + 0.4*math.Sin(float64(tick)*0.1)
	color.R = clamp(int(float64(color.R) * pulse))
	color.G = clamp(int(float64(color.G) * pulse))
	color.B = clamp(int(float64(color.B) * pulse))

	return fmt.Sprintf("\x1b[38;2;%d;%d;%dm%s\x1b[0m", color.R, color.G, color.B, text)
}

// GlitchText creates a glitch effect on text
func GlitchText(text string, tick int, intensity float64) string {
	if rand.Float64() > intensity {
		return text
	}

	runes := []rune(text)
	glitchChars := []rune("!@#$%^&*()_+-=[]{}|;:',.<>?/~`")

	// Randomly glitch some characters
	for i := range runes {
		if rand.Float64() < intensity*0.3 {
			runes[i] = glitchChars[rand.Intn(len(glitchChars))]
		}
	}

	// Random color shift
	colors := []string{"#f38ba8", "#a6e3a1", "#89b4fa", "#f9e2af", "#cba6f7"}
	color := colors[rand.Intn(len(colors))]

	return styles.GradientText(string(runes), color, "#cdd6f4")
}

// MatrixRain creates a matrix-style rain effect for a given width/height
func MatrixRain(width, height int, tick int) string {
	chars := "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789"
	runeChars := []rune(chars)

	var result strings.Builder

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			// Determine if this cell should have a character
			seed := x*height + tick
			if (seed+y)%3 == 0 {
				char := runeChars[(seed+y*7)%len(runeChars)]
				// Brightness based on position in "stream"
				streamPos := (tick + x*3) % (height * 2)
				distFromHead := abs(y - streamPos%height)

				if distFromHead < 5 {
					brightness := 1.0 - float64(distFromHead)*0.2
					green := clamp(int(255 * brightness))
					result.WriteString(fmt.Sprintf("\x1b[38;2;0;%d;0m%c\x1b[0m", green, char))
				} else {
					result.WriteRune(' ')
				}
			} else {
				result.WriteRune(' ')
			}
		}
		if y < height-1 {
			result.WriteRune('\n')
		}
	}

	return result.String()
}

// TransitionEffect applies a transition effect between slides
func TransitionEffect(content string, transitionType TransitionType, progress float64, width, height int) string {
	switch transitionType {
	case TransitionFadeOut:
		return fadeEffect(content, 1-progress)
	case TransitionFadeIn:
		return fadeEffect(content, progress)
	case TransitionSlideLeft:
		return slideEffect(content, progress, width, true)
	case TransitionSlideRight:
		return slideEffect(content, progress, width, false)
	case TransitionDissolve:
		return dissolveEffect(content, progress)
	case TransitionZoomIn:
		return zoomEffect(content, progress, width, height, true)
	case TransitionZoomOut:
		return zoomEffect(content, progress, width, height, false)
	default:
		return content
	}
}

func fadeEffect(content string, alpha float64) string {
	lines := strings.Split(content, "\n")
	var result []string

	for _, line := range lines {
		var fadedLine strings.Builder
		for _, r := range line {
			if r == '\x1b' {
				// Skip ANSI codes
				fadedLine.WriteRune(r)
				continue
			}

			// Apply alpha to each character
			brightness := clamp(int(255 * alpha))
			fadedLine.WriteString(fmt.Sprintf("\x1b[38;2;%d;%d;%dm%c\x1b[0m", brightness, brightness, brightness, r))
		}
		result = append(result, fadedLine.String())
	}

	return strings.Join(result, "\n")
}

func slideEffect(content string, progress float64, width int, leftward bool) string {
	lines := strings.Split(content, "\n")
	var result []string

	offset := int(float64(width) * (1 - progress))
	if !leftward {
		offset = -offset
	}

	for _, line := range lines {
		if offset > 0 {
			// Slide right (content coming from left)
			padding := strings.Repeat(" ", offset)
			result = append(result, padding+line)
		} else if offset < 0 {
			// Slide left (content going to right)
			if -offset < len(line) {
				result = append(result, line[-offset:])
			} else {
				result = append(result, "")
			}
		} else {
			result = append(result, line)
		}
	}

	return strings.Join(result, "\n")
}

func dissolveEffect(content string, progress float64) string {
	lines := strings.Split(content, "\n")
	var result []string

	for _, line := range lines {
		var dissolved strings.Builder
		for _, r := range line {
			if rand.Float64() < progress {
				dissolved.WriteRune(r)
			} else {
				dissolved.WriteRune(' ')
			}
		}
		result = append(result, dissolved.String())
	}

	return strings.Join(result, "\n")
}

func zoomEffect(content string, progress float64, width, height int, zoomIn bool) string {
	// Simplified zoom - just scale the visible area
	lines := strings.Split(content, "\n")

	scale := progress
	if !zoomIn {
		scale = 1 - progress
	}

	if scale < 0.1 {
		scale = 0.1
	}

	visibleHeight := int(float64(len(lines)) * scale)
	visibleWidth := int(float64(width) * scale)

	startY := (len(lines) - visibleHeight) / 2
	if startY < 0 {
		startY = 0
	}

	var result []string

	// Add top padding
	topPadding := (height - visibleHeight) / 2
	for i := 0; i < topPadding; i++ {
		result = append(result, "")
	}

	for i := 0; i < visibleHeight && startY+i < len(lines); i++ {
		line := lines[startY+i]
		leftPadding := (width - visibleWidth) / 2
		if leftPadding < 0 {
			leftPadding = 0
		}

		// Truncate or pad line
		if len(line) > visibleWidth {
			start := (len(line) - visibleWidth) / 2
			line = line[start : start+visibleWidth]
		}

		result = append(result, strings.Repeat(" ", leftPadding)+line)
	}

	return strings.Join(result, "\n")
}

// ProgressDots creates animated progress dots
func ProgressDots(current, total int, tick int) string {
	var dots strings.Builder

	for i := 0; i < total; i++ {
		if i < current {
			// Completed dot with glow
			dots.WriteString(PulseText("●", tick+i*5, "#a6e3a1"))
		} else if i == current {
			// Current dot with animation
			dots.WriteString(PulseText("◉", tick, "#89b4fa"))
		} else {
			// Future dot
			dots.WriteString("\x1b[38;2;69;71;90m○\x1b[0m")
		}
		dots.WriteString(" ")
	}

	return dots.String()
}

// AnimatedBorder creates an animated border around content (ASCII only for alignment)
func AnimatedBorder(content string, width int, tick int, colors []string) string {
	lines := strings.Split(content, "\n")

	// Animated top border (ASCII)
	topBorder := "+" + strings.Repeat("-", width-2) + "+"
	topBorder = styles.Shimmer(topBorder, tick, colors...)

	// Animated bottom border (ASCII)
	bottomBorder := "+" + strings.Repeat("-", width-2) + "+"
	bottomBorder = styles.Shimmer(bottomBorder, tick+width/2, colors...)

	var result []string
	result = append(result, topBorder)

	for _, line := range lines {
		// Side borders with shimmer (ASCII)
		leftBorder := styles.Shimmer("|", tick, colors...)
		rightBorder := styles.Shimmer("|", tick+width, colors...)

		// Pad content
		visLen := visibleLength(line)
		padding := width - 4 - visLen
		if padding < 0 {
			padding = 0
		}

		result = append(result, leftBorder+" "+line+strings.Repeat(" ", padding)+" "+rightBorder)
	}

	result = append(result, bottomBorder)

	return strings.Join(result, "\n")
}

// SparkleText adds occasional sparkle characters to text
func SparkleText(text string, tick int, density float64) string {
	sparkles := []string{"✨", "⭐", "✦", "★", "✧"}
	var result strings.Builder

	for _, r := range text {
		result.WriteRune(r)
		if r != ' ' && r != '\n' && rand.Float64() < density && (tick/5)%3 == 0 {
			sparkle := sparkles[rand.Intn(len(sparkles))]
			result.WriteString(styles.GradientText(sparkle, "#f9e2af", "#f5c2e7"))
		}
	}

	return result.String()
}

// Helper functions

func clamp(v int) int {
	if v < 0 {
		return 0
	}
	if v > 255 {
		return 255
	}
	return v
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func visibleLength(s string) int {
	// Strip ANSI escape codes first
	var stripped strings.Builder
	inEscape := false
	for _, r := range s {
		if r == '\x1b' {
			inEscape = true
			continue
		}
		if inEscape {
			if r == 'm' {
				inEscape = false
			}
			continue
		}
		stripped.WriteRune(r)
	}
	// Use runewidth for proper emoji/wide character width calculation
	return runewidth.StringWidth(stripped.String())
}
