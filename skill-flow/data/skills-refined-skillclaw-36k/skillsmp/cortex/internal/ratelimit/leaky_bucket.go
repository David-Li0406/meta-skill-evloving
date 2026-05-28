package ratelimit

import (
	"context"
	"sync"
	"time"
)

// LeakyBucket enforces a smooth, non-bursty request rate.
//
// It schedules each caller at least `interval` after the prior scheduled call,
// even under heavy concurrency. This is useful for RPM-based API quotas where
// spiky bursts cause 429s and/or local network instability.
type LeakyBucket struct {
	mu sync.Mutex

	tokens   chan struct{}
	updateCh chan time.Duration
	stopCh   chan struct{}
	stopped  bool
}

func NewLeakyBucketFromRPM(rpm int) *LeakyBucket {
	if rpm <= 0 {
		return nil
	}
	interval := time.Minute / time.Duration(rpm)
	if interval <= 0 {
		interval = time.Nanosecond
	}
	b := &LeakyBucket{
		tokens:   make(chan struct{}, 1),
		updateCh: make(chan time.Duration, 1),
		stopCh:   make(chan struct{}),
	}

	// Allow one immediate request.
	b.tokens <- struct{}{}

	go b.run(interval)
	return b
}

func (b *LeakyBucket) SetRPM(rpm int) {
	if b == nil {
		return
	}
	if rpm <= 0 {
		return
	}
	interval := time.Minute / time.Duration(rpm)
	if interval <= 0 {
		interval = time.Nanosecond
	}

	b.mu.Lock()
	stopped := b.stopped
	b.mu.Unlock()
	if stopped {
		return
	}

	// Best-effort update. Keep only the latest interval.
	select {
	case b.updateCh <- interval:
	default:
		select {
		case <-b.updateCh:
		default:
		}
		select {
		case b.updateCh <- interval:
		default:
		}
	}
}

func (b *LeakyBucket) Close() {
	if b == nil {
		return
	}
	b.mu.Lock()
	if b.stopped {
		b.mu.Unlock()
		return
	}
	b.stopped = true
	close(b.stopCh)
	b.mu.Unlock()
}

func (b *LeakyBucket) run(interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()
	for {
		select {
		case <-ticker.C:
			// Emit at most 1 token ahead (smooth, non-bursty).
			select {
			case b.tokens <- struct{}{}:
			default:
			}
		case newInterval := <-b.updateCh:
			ticker.Stop()
			ticker = time.NewTicker(newInterval)
		case <-b.stopCh:
			close(b.tokens)
			return
		}
	}
}

func (b *LeakyBucket) Wait(ctx context.Context) error {
	if b == nil {
		return nil
	}

	select {
	case <-ctx.Done():
		return ctx.Err()
	case _, ok := <-b.tokens:
		// If closed, treat as unthrottled.
		if !ok {
			return nil
		}
		return nil
	}
}
