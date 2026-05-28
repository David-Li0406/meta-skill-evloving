package compute

import (
	"context"
	"encoding/json"
	"math"
	"sync"
	"time"
)

type AutoRPMConfig struct {
	MinRPM   int
	MaxRPM   int
	StartRPM int

	Tick time.Duration

	// Slow start: multiply RPM by this factor while below SlowStartUntilRPM.
	SlowStartFactor   float64
	SlowStartUntilRPM int
	// Congestion response
	DecreaseFactor float64
	// Steady-state increase
	IncreaseFactor float64
}

type AutoRPMController struct {
	cfg AutoRPMConfig

	setRPM func(int)

	mu sync.Mutex

	current int
	adjusts int

	// window stats
	total int
	ok    int
	rl    int
	net   int
	to    int
	s5xx  int
	other int

	lastDecision string
}

func DefaultAutoRPMConfig() AutoRPMConfig {
	return AutoRPMConfig{
		MinRPM: 100,
		// Tier-3 keys max out at 20k RPM
		MaxRPM: 20000,
		// Start at max; only back off if we see congestion.
		// Tier-1 users will hit 429s and back off automatically.
		StartRPM: 20000,

		Tick: 1 * time.Second,

		// Slow-start is effectively disabled since we start at MaxRPM.
		SlowStartFactor:   2.0,
		SlowStartUntilRPM: 20000,

		DecreaseFactor: 0.6,
		IncreaseFactor: 1.25,
	}
}

func NewAutoRPMController(cfg AutoRPMConfig, setRPM func(int)) *AutoRPMController {
	if cfg.MinRPM < 1 {
		cfg.MinRPM = 1
	}
	if cfg.MaxRPM < cfg.MinRPM {
		cfg.MaxRPM = cfg.MinRPM
	}
	if cfg.StartRPM < cfg.MinRPM {
		cfg.StartRPM = cfg.MinRPM
	}
	if cfg.StartRPM > cfg.MaxRPM {
		cfg.StartRPM = cfg.MaxRPM
	}
	if cfg.Tick <= 0 {
		cfg.Tick = 1 * time.Second
	}
	if cfg.SlowStartFactor <= 1.0 {
		cfg.SlowStartFactor = 2.0
	}
	if cfg.DecreaseFactor <= 0 || cfg.DecreaseFactor >= 1 {
		cfg.DecreaseFactor = 0.7
	}
	if cfg.IncreaseFactor <= 1.0 {
		cfg.IncreaseFactor = 1.1
	}
	if setRPM == nil {
		setRPM = func(int) {}
	}

	c := &AutoRPMController{
		cfg:     cfg,
		setRPM:  setRPM,
		current: cfg.StartRPM,
	}
	c.setRPM(c.current)
	return c
}

func (c *AutoRPMController) Start(ctx context.Context) {
	if c == nil {
		return
	}
	go func() {
		t := time.NewTicker(c.cfg.Tick)
		defer t.Stop()
		for {
			select {
			case <-ctx.Done():
				return
			case <-t.C:
				c.step()
			}
		}
	}()
}

func (c *AutoRPMController) Observe(err error) {
	if c == nil {
		return
	}
	kind := classifyComputeError(err)

	c.mu.Lock()
	defer c.mu.Unlock()
	c.total++
	switch kind {
	case "ok":
		c.ok++
	case "rate_limited":
		c.rl++
	case "timeout":
		c.to++
	case "net_error":
		c.net++
	case "server_error":
		c.s5xx++
	default:
		c.other++
	}
}

func (c *AutoRPMController) CurrentRPM() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.current
}

func (c *AutoRPMController) SnapshotJSON() json.RawMessage {
	if c == nil {
		return json.RawMessage("null")
	}
	c.mu.Lock()
	defer c.mu.Unlock()
	out := map[string]any{
		"current_rpm":   c.current,
		"min_rpm":       c.cfg.MinRPM,
		"max_rpm":       c.cfg.MaxRPM,
		"start_rpm":     c.cfg.StartRPM,
		"adjustments":   c.adjusts,
		"last_decision": c.lastDecision,
	}
	b, _ := json.Marshal(out)
	return b
}

func (c *AutoRPMController) step() {
	c.mu.Lock()
	total := c.total
	ok := c.ok
	rl := c.rl
	net := c.net
	to := c.to
	s5xx := c.s5xx
	other := c.other
	c.total, c.ok, c.rl, c.net, c.to, c.s5xx, c.other = 0, 0, 0, 0, 0, 0, 0

	cur := c.current
	next := cur
	decision := "hold"

	congestion := rl > 0 || net > 0 || to > 0 || s5xx > 0
	if congestion {
		next = int(math.Floor(float64(cur) * c.cfg.DecreaseFactor))
		if next < c.cfg.MinRPM {
			next = c.cfg.MinRPM
		}
		decision = "decrease"
	} else if total > 0 && ok > 0 {
		// ramp up only if we saw real successful traffic in the last window
		if cur < c.cfg.SlowStartUntilRPM {
			next = int(math.Ceil(float64(cur) * c.cfg.SlowStartFactor))
		} else {
			next = int(math.Ceil(float64(cur) * c.cfg.IncreaseFactor))
		}
		if next > c.cfg.MaxRPM {
			next = c.cfg.MaxRPM
		}
		if next != cur {
			decision = "increase"
		}
	}

	c.lastDecision = decision + " (total=" + itoa(total) +
		" ok=" + itoa(ok) +
		" 429=" + itoa(rl) +
		" net=" + itoa(net) +
		" timeout=" + itoa(to) +
		" 5xx=" + itoa(s5xx) +
		" other=" + itoa(other) + ")"

	changed := next != cur
	if changed {
		c.current = next
		c.adjusts++
	}
	setRPM := c.setRPM
	c.mu.Unlock()

	if changed {
		setRPM(next)
	}
}
