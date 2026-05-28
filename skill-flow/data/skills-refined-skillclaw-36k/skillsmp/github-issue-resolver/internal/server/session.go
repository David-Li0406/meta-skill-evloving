package server

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"sync"
	"time"
)

// Session represents an MCP session for REST API clients
type Session struct {
	ID        string                 `json:"session_id"`
	CreatedAt time.Time              `json:"created_at"`
	ExpiresAt time.Time              `json:"expires_at"`
	LastUsed  time.Time              `json:"last_used"`
	Metadata  map[string]interface{} `json:"metadata,omitempty"`
}

// SessionManager manages MCP sessions for REST API clients
// This complements the SSE-based session management in the MCP SDK
type SessionManager struct {
	sessions   map[string]*Session
	mutex      sync.RWMutex
	ttl        time.Duration
	maxSessons int
	stopClean  chan struct{}
}

// NewSessionManager creates a new session manager
func NewSessionManager(sessionTTL time.Duration, maxSessions int) *SessionManager {
	if sessionTTL == 0 {
		sessionTTL = 30 * time.Minute // Default: 30 minutes
	}
	if maxSessions == 0 {
		maxSessions = 1000 // Default: 1000 concurrent sessions
	}

	sm := &SessionManager{
		sessions:   make(map[string]*Session),
		ttl:        sessionTTL,
		maxSessons: maxSessions,
		stopClean:  make(chan struct{}),
	}

	// Start background cleanup goroutine
	go sm.cleanupLoop()

	return sm
}

// CreateSession creates a new session and returns it
func (sm *SessionManager) CreateSession(metadata map[string]interface{}) (*Session, error) {
	sm.mutex.Lock()
	defer sm.mutex.Unlock()

	// Check max sessions limit
	if len(sm.sessions) >= sm.maxSessons {
		// Cleanup expired sessions first
		sm.cleanupExpiredLocked()
		if len(sm.sessions) >= sm.maxSessons {
			return nil, fmt.Errorf("maximum sessions limit reached (%d)", sm.maxSessons)
		}
	}

	// Generate session ID
	sessionID, err := generateSessionID()
	if err != nil {
		return nil, fmt.Errorf("failed to generate session ID: %w", err)
	}

	now := time.Now()
	session := &Session{
		ID:        sessionID,
		CreatedAt: now,
		ExpiresAt: now.Add(sm.ttl),
		LastUsed:  now,
		Metadata:  metadata,
	}

	sm.sessions[sessionID] = session
	return session, nil
}

// GetSession retrieves a session by ID, returns nil if not found or expired
func (sm *SessionManager) GetSession(sessionID string) *Session {
	sm.mutex.RLock()
	session, exists := sm.sessions[sessionID]
	sm.mutex.RUnlock()

	if !exists {
		return nil
	}

	// Check if expired
	if time.Now().After(session.ExpiresAt) {
		sm.DeleteSession(sessionID)
		return nil
	}

	return session
}

// TouchSession updates the last used time and extends expiration
func (sm *SessionManager) TouchSession(sessionID string) bool {
	sm.mutex.Lock()
	defer sm.mutex.Unlock()

	session, exists := sm.sessions[sessionID]
	if !exists {
		return false
	}

	// Check if expired
	if time.Now().After(session.ExpiresAt) {
		delete(sm.sessions, sessionID)
		return false
	}

	// Update timestamps
	session.LastUsed = time.Now()
	session.ExpiresAt = time.Now().Add(sm.ttl)
	return true
}

// DeleteSession removes a session
func (sm *SessionManager) DeleteSession(sessionID string) bool {
	sm.mutex.Lock()
	defer sm.mutex.Unlock()

	if _, exists := sm.sessions[sessionID]; exists {
		delete(sm.sessions, sessionID)
		return true
	}
	return false
}

// GetSessionInfo returns session info without sensitive data
func (sm *SessionManager) GetSessionInfo(sessionID string) *SessionInfo {
	session := sm.GetSession(sessionID)
	if session == nil {
		return nil
	}

	return &SessionInfo{
		ID:          session.ID,
		CreatedAt:   session.CreatedAt,
		ExpiresAt:   session.ExpiresAt,
		LastUsed:    session.LastUsed,
		TTLSeconds:  int(time.Until(session.ExpiresAt).Seconds()),
		IsValid:     true,
		HasMetadata: len(session.Metadata) > 0,
	}
}

// SessionInfo is a public representation of session state
type SessionInfo struct {
	ID          string    `json:"session_id"`
	CreatedAt   time.Time `json:"created_at"`
	ExpiresAt   time.Time `json:"expires_at"`
	LastUsed    time.Time `json:"last_used"`
	TTLSeconds  int       `json:"ttl_seconds"`
	IsValid     bool      `json:"is_valid"`
	HasMetadata bool      `json:"has_metadata"`
}

// GetStats returns session manager statistics
func (sm *SessionManager) GetStats() SessionStats {
	sm.mutex.RLock()
	defer sm.mutex.RUnlock()

	activeCount := 0
	expiredCount := 0
	now := time.Now()

	for _, session := range sm.sessions {
		if now.After(session.ExpiresAt) {
			expiredCount++
		} else {
			activeCount++
		}
	}

	return SessionStats{
		ActiveSessions:  activeCount,
		ExpiredSessions: expiredCount,
		TotalSessions:   len(sm.sessions),
		MaxSessions:     sm.maxSessons,
		SessionTTL:      sm.ttl.String(),
	}
}

// SessionStats holds session manager statistics
type SessionStats struct {
	ActiveSessions  int    `json:"active_sessions"`
	ExpiredSessions int    `json:"expired_sessions"`
	TotalSessions   int    `json:"total_sessions"`
	MaxSessions     int    `json:"max_sessions"`
	SessionTTL      string `json:"session_ttl"`
}

// Stop stops the session manager cleanup goroutine
func (sm *SessionManager) Stop() {
	close(sm.stopClean)
}

// cleanupLoop runs periodic cleanup of expired sessions
func (sm *SessionManager) cleanupLoop() {
	ticker := time.NewTicker(1 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			sm.cleanupExpired()
		case <-sm.stopClean:
			return
		}
	}
}

// cleanupExpired removes expired sessions
func (sm *SessionManager) cleanupExpired() {
	sm.mutex.Lock()
	defer sm.mutex.Unlock()
	sm.cleanupExpiredLocked()
}

// cleanupExpiredLocked removes expired sessions (caller must hold lock)
func (sm *SessionManager) cleanupExpiredLocked() {
	now := time.Now()
	for id, session := range sm.sessions {
		if now.After(session.ExpiresAt) {
			delete(sm.sessions, id)
		}
	}
}

// generateSessionID creates a cryptographically secure session ID
func generateSessionID() (string, error) {
	bytes := make([]byte, 16)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}

