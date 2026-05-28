package cache

import (
	"context"
	"sync"
	"time"
)

// CacheEntry represents a cached item with expiration
type CacheEntry struct {
	Value      interface{}
	Expiration time.Time
}

// IsExpired checks if the cache entry has expired
func (e *CacheEntry) IsExpired() bool {
	return time.Now().After(e.Expiration)
}

// Statistics tracks cache performance metrics
type Statistics struct {
	Hits      int64   `json:"hits"`
	Misses    int64   `json:"misses"`
	Evictions int64   `json:"evictions"`
	Entries   int     `json:"entries"`
	HitRate   float64 `json:"hit_rate"`
}

// MemoryCache provides a thread-safe in-memory cache with TTL
type MemoryCache struct {
	mu            sync.RWMutex
	data          map[string]*CacheEntry
	defaultTTL    time.Duration
	cleanupTicker *time.Ticker
	stopCleanup   chan bool
	stats         struct {
		hits      int64
		misses    int64
		evictions int64
	}
}

// NewMemoryCache creates a new in-memory cache with the specified default TTL
func NewMemoryCache(defaultTTL time.Duration) *MemoryCache {
	cache := &MemoryCache{
		data:        make(map[string]*CacheEntry),
		defaultTTL:  defaultTTL,
		stopCleanup: make(chan bool),
	}

	// Start background cleanup every minute
	cache.cleanupTicker = time.NewTicker(1 * time.Minute)
	go cache.cleanupExpired()

	return cache
}

// Get retrieves a value from the cache
func (c *MemoryCache) Get(key string) (interface{}, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entry, exists := c.data[key]
	if !exists {
		c.stats.misses++
		return nil, false
	}

	// Check if expired
	if entry.IsExpired() {
		c.stats.misses++
		return nil, false
	}

	c.stats.hits++
	return entry.Value, true
}

// Set stores a value in the cache with the default TTL
func (c *MemoryCache) Set(key string, value interface{}) {
	c.SetWithTTL(key, value, c.defaultTTL)
}

// SetWithTTL stores a value in the cache with a custom TTL
func (c *MemoryCache) SetWithTTL(key string, value interface{}, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.data[key] = &CacheEntry{
		Value:      value,
		Expiration: time.Now().Add(ttl),
	}
}

// Delete removes a value from the cache
func (c *MemoryCache) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if _, exists := c.data[key]; exists {
		delete(c.data, key)
		c.stats.evictions++
	}
}

// Clear removes all entries from the cache
func (c *MemoryCache) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()

	evicted := len(c.data)
	c.data = make(map[string]*CacheEntry)
	c.stats.evictions += int64(evicted)
}

// GetStatistics returns current cache statistics
func (c *MemoryCache) GetStatistics() Statistics {
	c.mu.RLock()
	defer c.mu.RUnlock()

	total := c.stats.hits + c.stats.misses
	hitRate := 0.0
	if total > 0 {
		hitRate = float64(c.stats.hits) / float64(total) * 100
	}

	return Statistics{
		Hits:      c.stats.hits,
		Misses:    c.stats.misses,
		Evictions: c.stats.evictions,
		Entries:   len(c.data),
		HitRate:   hitRate,
	}
}

// ResetStatistics resets cache statistics counters
func (c *MemoryCache) ResetStatistics() {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.stats.hits = 0
	c.stats.misses = 0
	c.stats.evictions = 0
}

// cleanupExpired removes expired entries from the cache
func (c *MemoryCache) cleanupExpired() {
	for {
		select {
		case <-c.cleanupTicker.C:
			c.mu.Lock()
			now := time.Now()
			expiredKeys := []string{}

			// Find expired entries
			for key, entry := range c.data {
				if now.After(entry.Expiration) {
					expiredKeys = append(expiredKeys, key)
				}
			}

			// Remove expired entries
			for _, key := range expiredKeys {
				delete(c.data, key)
				c.stats.evictions++
			}

			c.mu.Unlock()

		case <-c.stopCleanup:
			c.cleanupTicker.Stop()
			return
		}
	}
}

// Close stops the cleanup goroutine and releases resources
func (c *MemoryCache) Close() {
	close(c.stopCleanup)
}

// GetOrSet retrieves a value from cache or computes it if not present
// This is useful for lazy-loading patterns
func (c *MemoryCache) GetOrSet(ctx context.Context, key string, compute func() (interface{}, error)) (interface{}, error) {
	// Try to get from cache first
	if value, found := c.Get(key); found {
		return value, nil
	}

	// Not in cache, compute the value
	value, err := compute()
	if err != nil {
		return nil, err
	}

	// Store in cache
	c.Set(key, value)

	return value, nil
}

// GetOrSetWithTTL retrieves a value from cache or computes it with custom TTL
func (c *MemoryCache) GetOrSetWithTTL(ctx context.Context, key string, ttl time.Duration, compute func() (interface{}, error)) (interface{}, error) {
	// Try to get from cache first
	if value, found := c.Get(key); found {
		return value, nil
	}

	// Not in cache, compute the value
	value, err := compute()
	if err != nil {
		return nil, err
	}

	// Store in cache with custom TTL
	c.SetWithTTL(key, value, ttl)

	return value, nil
}
