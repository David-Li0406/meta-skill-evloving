package compute

import (
	"context"
	"sync"
)

// AdaptiveSemaphore is a context-aware semaphore whose limit can be changed at runtime.
// It is used to cap effective "in-flight" work without needing to resize worker pools.
type AdaptiveSemaphore struct {
	mu       sync.Mutex
	limit    int
	inFlight int
	changed  chan struct{}
}

func NewAdaptiveSemaphore(limit int) *AdaptiveSemaphore {
	if limit < 1 {
		limit = 1
	}
	return &AdaptiveSemaphore{
		limit:   limit,
		changed: make(chan struct{}),
	}
}

func (s *AdaptiveSemaphore) Limit() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.limit
}

func (s *AdaptiveSemaphore) InFlight() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.inFlight
}

func (s *AdaptiveSemaphore) SetLimit(limit int) {
	if limit < 1 {
		limit = 1
	}
	s.mu.Lock()
	if s.limit == limit {
		s.mu.Unlock()
		return
	}
	s.limit = limit
	s.notifyLocked()
	s.mu.Unlock()
}

func (s *AdaptiveSemaphore) Acquire(ctx context.Context) error {
	for {
		s.mu.Lock()
		if s.inFlight < s.limit {
			s.inFlight++
			s.mu.Unlock()
			return nil
		}
		ch := s.changed
		s.mu.Unlock()

		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-ch:
		}
	}
}

func (s *AdaptiveSemaphore) Release() {
	s.mu.Lock()
	if s.inFlight > 0 {
		s.inFlight--
	}
	s.notifyLocked()
	s.mu.Unlock()
}

func (s *AdaptiveSemaphore) notifyLocked() {
	// Broadcast to all waiters.
	close(s.changed)
	s.changed = make(chan struct{})
}
