package server

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewSessionManager(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	assert.NotNil(t, sm)
	assert.NotNil(t, sm.sessions)
	assert.Equal(t, 5*time.Minute, sm.ttl)
	assert.Equal(t, 100, sm.maxSessons)
}

func TestNewSessionManager_Defaults(t *testing.T) {
	sm := NewSessionManager(0, 0)
	defer sm.Stop()

	assert.Equal(t, 30*time.Minute, sm.ttl)
	assert.Equal(t, 1000, sm.maxSessons)
}

func TestCreateSession(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	metadata := map[string]interface{}{
		"client": "test-client",
	}

	session, err := sm.CreateSession(metadata)
	require.NoError(t, err)
	assert.NotNil(t, session)
	assert.NotEmpty(t, session.ID)
	assert.Equal(t, 32, len(session.ID)) // 16 bytes = 32 hex chars
	assert.Equal(t, "test-client", session.Metadata["client"])
	assert.WithinDuration(t, time.Now(), session.CreatedAt, time.Second)
	assert.WithinDuration(t, time.Now().Add(5*time.Minute), session.ExpiresAt, time.Second)
}

func TestCreateSession_MaxSessionsLimit(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 2)
	defer sm.Stop()

	// Create first session
	_, err := sm.CreateSession(nil)
	require.NoError(t, err)

	// Create second session
	_, err = sm.CreateSession(nil)
	require.NoError(t, err)

	// Third session should fail
	_, err = sm.CreateSession(nil)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "maximum sessions limit reached")
}

func TestGetSession(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	// Create session
	session, err := sm.CreateSession(nil)
	require.NoError(t, err)

	// Get existing session
	retrieved := sm.GetSession(session.ID)
	assert.NotNil(t, retrieved)
	assert.Equal(t, session.ID, retrieved.ID)

	// Get non-existent session
	notFound := sm.GetSession("non-existent-id")
	assert.Nil(t, notFound)
}

func TestGetSession_Expired(t *testing.T) {
	// Use very short TTL
	sm := NewSessionManager(1*time.Millisecond, 100)
	defer sm.Stop()

	session, err := sm.CreateSession(nil)
	require.NoError(t, err)

	// Wait for expiration
	time.Sleep(10 * time.Millisecond)

	// Session should be nil (expired)
	retrieved := sm.GetSession(session.ID)
	assert.Nil(t, retrieved)
}

func TestTouchSession(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	session, err := sm.CreateSession(nil)
	require.NoError(t, err)
	originalExpiry := session.ExpiresAt

	// Wait a bit
	time.Sleep(100 * time.Millisecond)

	// Touch session
	success := sm.TouchSession(session.ID)
	assert.True(t, success)

	// Verify expiration was extended
	retrieved := sm.GetSession(session.ID)
	assert.True(t, retrieved.ExpiresAt.After(originalExpiry))
}

func TestTouchSession_NonExistent(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	success := sm.TouchSession("non-existent-id")
	assert.False(t, success)
}

func TestDeleteSession(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	session, err := sm.CreateSession(nil)
	require.NoError(t, err)

	// Delete session
	deleted := sm.DeleteSession(session.ID)
	assert.True(t, deleted)

	// Verify it's gone
	retrieved := sm.GetSession(session.ID)
	assert.Nil(t, retrieved)

	// Delete again should fail
	deleted = sm.DeleteSession(session.ID)
	assert.False(t, deleted)
}

func TestGetSessionInfo(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	session, err := sm.CreateSession(map[string]interface{}{"key": "value"})
	require.NoError(t, err)

	info := sm.GetSessionInfo(session.ID)
	assert.NotNil(t, info)
	assert.Equal(t, session.ID, info.ID)
	assert.True(t, info.IsValid)
	assert.True(t, info.HasMetadata)
	assert.Greater(t, info.TTLSeconds, 0)
}

func TestGetSessionInfo_NotFound(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	info := sm.GetSessionInfo("non-existent-id")
	assert.Nil(t, info)
}

func TestGetStats(t *testing.T) {
	sm := NewSessionManager(5*time.Minute, 100)
	defer sm.Stop()

	// Create some sessions
	_, _ = sm.CreateSession(nil)
	_, _ = sm.CreateSession(nil)

	stats := sm.GetStats()
	assert.Equal(t, 2, stats.ActiveSessions)
	assert.Equal(t, 2, stats.TotalSessions)
	assert.Equal(t, 0, stats.ExpiredSessions)
	assert.Equal(t, 100, stats.MaxSessions)
	assert.Equal(t, "5m0s", stats.SessionTTL)
}

func TestCleanupExpired(t *testing.T) {
	// Use very short TTL
	sm := NewSessionManager(1*time.Millisecond, 100)
	defer sm.Stop()

	// Create sessions
	_, _ = sm.CreateSession(nil)
	_, _ = sm.CreateSession(nil)

	// Verify they exist
	stats := sm.GetStats()
	assert.Equal(t, 2, stats.TotalSessions)

	// Wait for expiration
	time.Sleep(10 * time.Millisecond)

	// Manually trigger cleanup
	sm.cleanupExpired()

	// Verify sessions are cleaned up
	stats = sm.GetStats()
	assert.Equal(t, 0, stats.TotalSessions)
}

func TestGenerateSessionID_Uniqueness(t *testing.T) {
	ids := make(map[string]bool)
	for i := 0; i < 100; i++ {
		id, err := generateSessionID()
		require.NoError(t, err)
		assert.NotEmpty(t, id)
		assert.False(t, ids[id], "duplicate session ID generated")
		ids[id] = true
	}
}

