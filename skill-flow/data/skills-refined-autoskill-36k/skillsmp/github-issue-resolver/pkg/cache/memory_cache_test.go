package cache

import (
	"context"
	"testing"
	"time"
)

func TestNewMemoryCache(t *testing.T) {
	cache := NewMemoryCache(30 * time.Second)
	if cache == nil {
		t.Fatal("NewMemoryCache returned nil")
	}
	defer cache.Close()

	if cache.defaultTTL != 30*time.Second {
		t.Errorf("Expected defaultTTL 30s, got %v", cache.defaultTTL)
	}
}

func TestMemoryCache_SetAndGet(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	// Test setting and getting a value
	cache.Set("key1", "value1")

	value, found := cache.Get("key1")
	if !found {
		t.Error("Expected to find key1")
	}
	if value != "value1" {
		t.Errorf("Expected value1, got %v", value)
	}

	// Test getting non-existent key
	_, found = cache.Get("nonexistent")
	if found {
		t.Error("Expected not to find nonexistent key")
	}
}

func TestMemoryCache_SetWithTTL(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	// Set with short TTL
	cache.SetWithTTL("shortlived", "value", 100*time.Millisecond)

	// Should exist immediately
	value, found := cache.Get("shortlived")
	if !found || value != "value" {
		t.Error("Expected to find shortlived key immediately")
	}

	// Wait for expiration
	time.Sleep(150 * time.Millisecond)

	// Should be expired
	_, found = cache.Get("shortlived")
	if found {
		t.Error("Expected shortlived key to be expired")
	}
}

func TestMemoryCache_Delete(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	cache.Set("key1", "value1")

	// Verify it exists
	_, found := cache.Get("key1")
	if !found {
		t.Error("Expected to find key1")
	}

	// Delete it
	cache.Delete("key1")

	// Should not exist
	_, found = cache.Get("key1")
	if found {
		t.Error("Expected key1 to be deleted")
	}

	// Delete non-existent key (should not panic)
	cache.Delete("nonexistent")
}

func TestMemoryCache_Clear(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	// Add multiple items
	cache.Set("key1", "value1")
	cache.Set("key2", "value2")
	cache.Set("key3", "value3")

	// Clear cache
	cache.Clear()

	// All keys should be gone
	_, found := cache.Get("key1")
	if found {
		t.Error("Expected cache to be cleared")
	}

	stats := cache.GetStatistics()
	if stats.Entries != 0 {
		t.Errorf("Expected 0 entries after clear, got %d", stats.Entries)
	}
}

func TestMemoryCache_Statistics(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	// Initial stats
	stats := cache.GetStatistics()
	if stats.Hits != 0 || stats.Misses != 0 {
		t.Error("Expected initial stats to be zero")
	}

	// Cause a miss
	cache.Get("nonexistent")
	stats = cache.GetStatistics()
	if stats.Misses != 1 {
		t.Errorf("Expected 1 miss, got %d", stats.Misses)
	}

	// Cause a hit
	cache.Set("key1", "value1")
	cache.Get("key1")
	stats = cache.GetStatistics()
	if stats.Hits != 1 {
		t.Errorf("Expected 1 hit, got %d", stats.Hits)
	}

	// Check hit rate
	total := stats.Hits + stats.Misses
	expectedRate := float64(stats.Hits) / float64(total) * 100
	if stats.HitRate != expectedRate {
		t.Errorf("Expected hit rate %.2f, got %.2f", expectedRate, stats.HitRate)
	}

	// Test eviction counting
	cache.Delete("key1")
	stats = cache.GetStatistics()
	if stats.Evictions != 1 {
		t.Errorf("Expected 1 eviction, got %d", stats.Evictions)
	}
}

func TestMemoryCache_ResetStatistics(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	// Generate some stats
	cache.Set("key1", "value1")
	cache.Get("key1")
	cache.Get("nonexistent")

	// Reset
	cache.ResetStatistics()

	// Should be zero
	stats := cache.GetStatistics()
	if stats.Hits != 0 || stats.Misses != 0 || stats.Evictions != 0 {
		t.Error("Expected statistics to be reset to zero")
	}
}

func TestMemoryCache_GetOrSet(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	ctx := context.Background()
	callCount := 0

	compute := func() (interface{}, error) {
		callCount++
		return "computed_value", nil
	}

	// First call - should compute
	value, err := cache.GetOrSet(ctx, "key1", compute)
	if err != nil {
		t.Fatalf("GetOrSet failed: %v", err)
	}
	if value != "computed_value" {
		t.Errorf("Expected computed_value, got %v", value)
	}
	if callCount != 1 {
		t.Errorf("Expected compute to be called once, got %d", callCount)
	}

	// Second call - should use cache
	value, err = cache.GetOrSet(ctx, "key1", compute)
	if err != nil {
		t.Fatalf("GetOrSet failed: %v", err)
	}
	if value != "computed_value" {
		t.Errorf("Expected computed_value, got %v", value)
	}
	if callCount != 1 {
		t.Errorf("Expected compute not to be called again, got %d calls", callCount)
	}
}

func TestMemoryCache_GetOrSetWithTTL(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	ctx := context.Background()
	callCount := 0

	compute := func() (interface{}, error) {
		callCount++
		return "computed_value", nil
	}

	// Set with custom TTL
	value, err := cache.GetOrSetWithTTL(ctx, "key1", 100*time.Millisecond, compute)
	if err != nil {
		t.Fatalf("GetOrSetWithTTL failed: %v", err)
	}
	if value != "computed_value" {
		t.Errorf("Expected computed_value, got %v", value)
	}

	// Should be cached immediately
	_, err = cache.GetOrSetWithTTL(ctx, "key1", 100*time.Millisecond, compute)
	if err != nil {
		t.Fatalf("GetOrSetWithTTL failed: %v", err)
	}
	if callCount != 1 {
		t.Errorf("Expected compute to be called once (cached), got %d", callCount)
	}

	// Wait for expiration
	time.Sleep(150 * time.Millisecond)

	// Should compute again
	_, err = cache.GetOrSetWithTTL(ctx, "key1", 100*time.Millisecond, compute)
	if err != nil {
		t.Fatalf("GetOrSetWithTTL failed: %v", err)
	}
	if callCount != 2 {
		t.Errorf("Expected compute to be called twice (expired), got %d", callCount)
	}
}

func TestMemoryCache_CleanupExpired(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	// Add items with very short TTL
	cache.SetWithTTL("expire1", "value1", 50*time.Millisecond)
	cache.SetWithTTL("expire2", "value2", 50*time.Millisecond)
	cache.SetWithTTL("longlived", "value3", 10*time.Minute)

	// Wait for short items to expire
	time.Sleep(100 * time.Millisecond)

	// Manually trigger cleanup by accessing
	_, found := cache.Get("expire1")
	if found {
		t.Error("Expected expire1 to be expired")
	}

	// Long-lived should still exist
	value, found := cache.Get("longlived")
	if !found || value != "value3" {
		t.Error("Expected longlived to still exist")
	}
}

func TestCacheEntry_IsExpired(t *testing.T) {
	// Not expired
	entry := &CacheEntry{
		Value:      "test",
		Expiration: time.Now().Add(1 * time.Minute),
	}
	if entry.IsExpired() {
		t.Error("Expected entry not to be expired")
	}

	// Expired
	entry = &CacheEntry{
		Value:      "test",
		Expiration: time.Now().Add(-1 * time.Minute),
	}
	if !entry.IsExpired() {
		t.Error("Expected entry to be expired")
	}
}

func TestMemoryCache_ConcurrentAccess(t *testing.T) {
	cache := NewMemoryCache(1 * time.Minute)
	defer cache.Close()

	// Test concurrent writes
	done := make(chan bool)
	for i := 0; i < 10; i++ {
		go func(n int) {
			cache.Set("concurrent", n)
			done <- true
		}(i)
	}

	// Wait for all goroutines
	for i := 0; i < 10; i++ {
		<-done
	}

	// Should not panic and should have some value
	_, found := cache.Get("concurrent")
	if !found {
		t.Error("Expected concurrent key to exist")
	}
}
