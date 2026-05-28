package compute

import (
	"context"
	"encoding/json"
	"math"
	"strings"
	"sync"
	"time"
)

type AdaptiveControllerConfig struct {
	MinInFlight int
	MaxInFlight int

	// Controller tick cadence.
	Tick time.Duration

	// Multiplicative decrease on congestion signals (e.g., 0.7).
	DecreaseFactor float64

	// Additive increase each stable tick (e.g., +max(1, ceil(limit*0.05))).
	IncreasePct float64

	// If failure rate exceeds this, treat as congestion.
	FailRateThreshold float64
}

type AdaptiveController struct {
	sem *AdaptiveSemaphore
	cfg AdaptiveControllerConfig

	mu sync.Mutex

	// Window stats (reset every tick)
	winTotal     int
	winOK        int
	winRateLimit int
	winNetErr    int
	winTimeout   int
	winServerErr int
	winOtherErr  int
	winDurSum    time.Duration

	// Smoothed latency (EWMA) and baseline (min EWMA observed)
	ewma     time.Duration
	ewmaBase time.Duration

	// State
	current      int
	adjusts      int
	lastDecision string
}

func DefaultAdaptiveControllerConfig(maxInFlight int) AdaptiveControllerConfig {
	if maxInFlight < 1 {
		maxInFlight = 1
	}
	return AdaptiveControllerConfig{
		MinInFlight:       1,
		MaxInFlight:       maxInFlight,
		Tick:              1 * time.Second,
		DecreaseFactor:    0.85,
		IncreasePct:       0.12,
		FailRateThreshold: 0.08,
	}
}

func NewAdaptiveController(sem *AdaptiveSemaphore, cfg AdaptiveControllerConfig) *AdaptiveController {
	if cfg.MaxInFlight < 1 {
		cfg.MaxInFlight = 1
	}
	if cfg.MinInFlight < 1 {
		cfg.MinInFlight = 1
	}
	if cfg.MinInFlight > cfg.MaxInFlight {
		cfg.MinInFlight = cfg.MaxInFlight
	}
	if cfg.Tick <= 0 {
		cfg.Tick = 1 * time.Second
	}
	if cfg.DecreaseFactor <= 0 || cfg.DecreaseFactor >= 1 {
		cfg.DecreaseFactor = 0.7
	}
	if cfg.IncreasePct <= 0 {
		cfg.IncreasePct = 0.05
	}
	if cfg.FailRateThreshold <= 0 {
		cfg.FailRateThreshold = 0.03
	}

	c := &AdaptiveController{
		sem:     sem,
		cfg:     cfg,
		current: cfg.MaxInFlight, // start at max; back off only when needed
	}
	if sem != nil {
		sem.SetLimit(c.current)
	}
	return c
}

func (c *AdaptiveController) Start(ctx context.Context) {
	if c == nil {
		return
	}
	go c.run(ctx)
}

func (c *AdaptiveController) Observe(d time.Duration, err error) {
	if c == nil {
		return
	}
	kind := classifyComputeError(err)

	c.mu.Lock()
	defer c.mu.Unlock()

	c.winTotal++
	c.winDurSum += d
	if kind == "ok" {
		c.winOK++
		return
	}
	switch kind {
	case "rate_limited":
		c.winRateLimit++
	case "timeout":
		c.winTimeout++
	case "net_error":
		c.winNetErr++
	case "server_error":
		c.winServerErr++
	default:
		c.winOtherErr++
	}
}

func (c *AdaptiveController) SnapshotJSON() json.RawMessage {
	if c == nil {
		return json.RawMessage("null")
	}
	c.mu.Lock()
	defer c.mu.Unlock()

	out := map[string]any{
		"min_in_flight":           c.cfg.MinInFlight,
		"max_in_flight":           c.cfg.MaxInFlight,
		"current_in_flight_limit": c.current,
		"in_flight_now": func() int {
			if c.sem == nil {
				return 0
			}
			return c.sem.InFlight()
		}(),
		"adjustments":   c.adjusts,
		"last_decision": c.lastDecision,
		"ewma_ms":       float64(c.ewma.Milliseconds()),
		"ewma_base_ms": func() float64 {
			if c.ewmaBase <= 0 {
				return 0
			}
			return float64(c.ewmaBase.Milliseconds())
		}(),
	}
	b, _ := json.Marshal(out)
	return b
}

func (c *AdaptiveController) run(ctx context.Context) {
	ticker := time.NewTicker(c.cfg.Tick)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			c.step()
		}
	}
}

func (c *AdaptiveController) step() {
	c.mu.Lock()
	total := c.winTotal
	ok := c.winOK
	rateLimited := c.winRateLimit
	netErr := c.winNetErr
	timeoutErr := c.winTimeout
	serverErr := c.winServerErr
	otherErr := c.winOtherErr
	sumDur := c.winDurSum

	// reset window
	c.winTotal, c.winOK, c.winRateLimit, c.winNetErr, c.winTimeout, c.winServerErr, c.winOtherErr = 0, 0, 0, 0, 0, 0, 0
	c.winDurSum = 0

	// update EWMA latency if we have samples
	if total > 0 {
		avg := time.Duration(int64(sumDur) / int64(total))
		if c.ewma == 0 {
			c.ewma = avg
		} else {
			// 0.2 EWMA weight
			c.ewma = time.Duration(float64(c.ewma)*0.8 + float64(avg)*0.2)
		}
		if c.ewmaBase == 0 || (c.ewma > 0 && c.ewma < c.ewmaBase) {
			c.ewmaBase = c.ewma
		}
	}

	// Decide adjustment.
	next := c.current
	decision := "hold"

	fail := total - ok
	failRate := 0.0
	if total > 0 {
		failRate = float64(fail) / float64(total)
	}

	congestion := false
	// Strong signals:
	if rateLimited > 0 || timeoutErr > 0 || netErr > 0 || serverErr > 0 {
		congestion = true
	}
	// Also treat high failure rate as congestion (covers assorted network issues).
	if total > 0 && failRate >= c.cfg.FailRateThreshold {
		congestion = true
	}
	// Latency inflation heuristic: if EWMA is >3.0x baseline, treat as congestion.
	if c.ewmaBase > 0 && c.ewma > time.Duration(float64(c.ewmaBase)*3.0) {
		congestion = true
	}

	if congestion {
		next = int(math.Floor(float64(c.current) * c.cfg.DecreaseFactor))
		if next < c.cfg.MinInFlight {
			next = c.cfg.MinInFlight
		}
		decision = "decrease"
	} else if total > 0 {
		// No congestion signals and we observed work: cautiously increase toward max.
		step := int(math.Ceil(float64(c.current) * c.cfg.IncreasePct))
		if step < 1 {
			step = 1
		}
		next = c.current + step
		if next > c.cfg.MaxInFlight {
			next = c.cfg.MaxInFlight
		}
		if next != c.current {
			decision = "increase"
		}
	}

	// Record decision string with key window signals (debuggable but not spammy).
	c.lastDecision = decision + " (total=" + itoa(total) +
		" ok=" + itoa(ok) +
		" 429=" + itoa(rateLimited) +
		" net=" + itoa(netErr) +
		" timeout=" + itoa(timeoutErr) +
		" 5xx=" + itoa(serverErr) +
		" other=" + itoa(otherErr) + ")"

	changed := next != c.current
	if changed {
		c.current = next
		c.adjusts++
	}
	sem := c.sem
	c.mu.Unlock()

	if changed && sem != nil {
		sem.SetLimit(next)
	}
}

func classifyComputeError(err error) string {
	if err == nil {
		return "ok"
	}
	s := strings.ToLower(err.Error())
	switch {
	case strings.Contains(s, " 429") || strings.Contains(s, "status code 429") || strings.Contains(s, "too many requests"):
		return "rate_limited"
	case strings.Contains(s, "context deadline exceeded") || strings.Contains(s, "timeout") || strings.Contains(s, "tls handshake timeout"):
		return "timeout"
	case strings.Contains(s, "connection reset") || strings.Contains(s, "broken pipe") || strings.Contains(s, "eof") ||
		strings.Contains(s, "no such host") || strings.Contains(s, "temporary failure in name resolution") ||
		strings.Contains(s, "network is unreachable") || strings.Contains(s, "i/o timeout"):
		return "net_error"
	case strings.Contains(s, "status code 5") || strings.Contains(s, "gemini api error 5"):
		return "server_error"
	default:
		return "other"
	}
}

// tiny int->string helper to avoid fmt in hot path.
func itoa(n int) string {
	if n == 0 {
		return "0"
	}
	neg := n < 0
	if neg {
		n = -n
	}
	var buf [32]byte
	i := len(buf)
	for n > 0 {
		i--
		buf[i] = byte('0' + (n % 10))
		n /= 10
	}
	if neg {
		i--
		buf[i] = '-'
	}
	return string(buf[i:])
}
