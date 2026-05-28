// Package serve provides an HTTP server for NTM with REST API and event streaming.
package serve

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/events"
	"github.com/Dicklesworthstone/ntm/internal/state"
)

// Server provides HTTP API and event streaming for NTM.
type Server struct {
	host       string
	port       int
	eventBus   *events.EventBus
	stateStore *state.Store
	server     *http.Server

	// SSE clients
	sseClients   map[chan events.BusEvent]struct{}
	sseClientsMu sync.RWMutex
}

// Config holds server configuration.
type Config struct {
	Host       string
	Port       int
	EventBus   *events.EventBus
	StateStore *state.Store
}

// New creates a new HTTP server.
func New(cfg Config) *Server {
	if cfg.Port == 0 {
		cfg.Port = 7337
	}
	if cfg.Host == "" {
		cfg.Host = "127.0.0.1"
	}
	return &Server{
		host:       cfg.Host,
		port:       cfg.Port,
		eventBus:   cfg.EventBus,
		stateStore: cfg.StateStore,
		sseClients: make(map[chan events.BusEvent]struct{}),
	}
}

// Start starts the HTTP server and blocks until shutdown.
func (s *Server) Start(ctx context.Context) error {
	mux := http.NewServeMux()

	// REST API endpoints
	mux.HandleFunc("/api/sessions", s.handleSessions)
	mux.HandleFunc("/api/sessions/", s.handleSession)
	mux.HandleFunc("/api/robot/status", s.handleRobotStatus)
	mux.HandleFunc("/api/robot/health", s.handleRobotHealth)

	// SSE event stream
	mux.HandleFunc("/events", s.handleEventStream)

	// Health check
	mux.HandleFunc("/health", s.handleHealth)

	// Subscribe to events for SSE broadcasting
	if s.eventBus != nil {
		unsubscribe := s.eventBus.SubscribeAll(func(e events.BusEvent) {
			s.broadcastEvent(e)
		})
		defer unsubscribe()
	}

	s.server = &http.Server{
		Addr:         fmt.Sprintf("%s:%d", s.host, s.port),
		Handler:      corsMiddleware(loggingMiddleware(mux)),
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 0, // Disabled to support long-lived SSE streams at /events
		IdleTimeout:  60 * time.Second,
	}

	log.Printf("Starting NTM server on %s:%d", s.host, s.port)

	// Start server in goroutine
	errCh := make(chan error, 1)
	go func() {
		if err := s.server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			errCh <- err
		}
	}()

	// Wait for context cancellation or error
	select {
	case <-ctx.Done():
		log.Println("Shutting down server...")
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		return s.server.Shutdown(shutdownCtx)
	case err := <-errCh:
		return err
	}
}

// Port returns the configured port.
func (s *Server) Port() int {
	return s.port
}

// loggingMiddleware logs HTTP requests.
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(start))
	})
}

// corsMiddleware adds CORS headers for local development.
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

// writeJSON writes a JSON response.
func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(data); err != nil {
		log.Printf("Error encoding JSON: %v", err)
	}
}

// writeError writes an error response.
func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]interface{}{
		"success": false,
		"error":   message,
	})
}

// handleHealth handles health check requests.
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success": true,
		"status":  "healthy",
		"time":    time.Now().UTC().Format(time.RFC3339),
	})
}

// handleSessions handles /api/sessions - list all sessions.
func (s *Server) handleSessions(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	if s.stateStore == nil {
		writeError(w, http.StatusServiceUnavailable, "state store not available")
		return
	}

	sessions, err := s.stateStore.ListSessions("")
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success":  true,
		"sessions": sessions,
		"count":    len(sessions),
	})
}

// handleSession handles /api/sessions/{id} - get session details.
func (s *Server) handleSession(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	// Extract session ID from path
	path := strings.TrimPrefix(r.URL.Path, "/api/sessions/")
	parts := strings.Split(path, "/")
	if len(parts) == 0 || parts[0] == "" {
		writeError(w, http.StatusBadRequest, "session ID required")
		return
	}
	sessionID := parts[0]

	if s.stateStore == nil {
		writeError(w, http.StatusServiceUnavailable, "state store not available")
		return
	}

	session, err := s.stateStore.GetSession(sessionID)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}
	if session == nil {
		writeError(w, http.StatusNotFound, "session not found")
		return
	}

	// Check for sub-resources
	if len(parts) > 1 {
		switch parts[1] {
		case "agents":
			s.handleSessionAgents(w, r, sessionID)
			return
		case "events":
			s.handleSessionEvents(w, r, sessionID)
			return
		}
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success": true,
		"session": session,
	})
}

// handleSessionAgents handles /api/sessions/{id}/agents.
func (s *Server) handleSessionAgents(w http.ResponseWriter, r *http.Request, sessionID string) {
	if s.stateStore == nil {
		writeError(w, http.StatusServiceUnavailable, "state store not available")
		return
	}

	agents, err := s.stateStore.ListAgents(sessionID)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err.Error())
		return
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success":    true,
		"session_id": sessionID,
		"agents":     agents,
		"count":      len(agents),
	})
}

// handleSessionEvents handles /api/sessions/{id}/events.
func (s *Server) handleSessionEvents(w http.ResponseWriter, r *http.Request, sessionID string) {
	if s.eventBus == nil {
		writeError(w, http.StatusServiceUnavailable, "event bus not available")
		return
	}

	// Get recent events from event bus history
	eventsData := s.eventBus.History(100)

	// Filter to session if specified
	var filtered []events.BusEvent
	for _, e := range eventsData {
		if sessionID == "" || e.EventSession() == sessionID {
			filtered = append(filtered, e)
		}
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success":    true,
		"session_id": sessionID,
		"events":     filtered,
		"count":      len(filtered),
	})
}

// handleRobotStatus handles /api/robot/status - proxies to robot status.
func (s *Server) handleRobotStatus(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	// Return basic status - in a full implementation, this would call robot.Status()
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success":   true,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"note":      "full robot status requires robot package integration",
	})
}

// handleRobotHealth handles /api/robot/health.
func (s *Server) handleRobotHealth(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeError(w, http.StatusMethodNotAllowed, "method not allowed")
		return
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success":   true,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"note":      "full robot health requires robot package integration",
	})
}

// handleEventStream handles SSE event streaming at /events.
func (s *Server) handleEventStream(w http.ResponseWriter, r *http.Request) {
	// Set SSE headers
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("X-Accel-Buffering", "no") // Disable nginx buffering

	// Create client channel
	clientCh := make(chan events.BusEvent, 100)
	s.addSSEClient(clientCh)
	defer s.removeSSEClient(clientCh)

	// Get flusher for streaming
	flusher, ok := w.(http.Flusher)
	if !ok {
		writeError(w, http.StatusInternalServerError, "streaming not supported")
		return
	}

	// Send initial connection event
	fmt.Fprintf(w, "event: connected\ndata: {\"status\":\"connected\",\"time\":\"%s\"}\n\n",
		time.Now().UTC().Format(time.RFC3339))
	flusher.Flush()

	// Stream events
	ctx := r.Context()
	for {
		select {
		case <-ctx.Done():
			return
		case event := <-clientCh:
			data, err := json.Marshal(map[string]interface{}{
				"type":      event.EventType(),
				"timestamp": event.EventTimestamp().Format(time.RFC3339),
				"session":   event.EventSession(),
			})
			if err != nil {
				continue
			}
			fmt.Fprintf(w, "event: %s\ndata: %s\n\n", event.EventType(), data)
			flusher.Flush()
		}
	}
}

// addSSEClient adds a client to the SSE broadcast list.
func (s *Server) addSSEClient(ch chan events.BusEvent) {
	s.sseClientsMu.Lock()
	defer s.sseClientsMu.Unlock()
	s.sseClients[ch] = struct{}{}
}

// removeSSEClient removes a client from the SSE broadcast list.
func (s *Server) removeSSEClient(ch chan events.BusEvent) {
	s.sseClientsMu.Lock()
	defer s.sseClientsMu.Unlock()
	delete(s.sseClients, ch)
	close(ch)
}

// broadcastEvent sends an event to all SSE clients.
func (s *Server) broadcastEvent(event events.BusEvent) {
	s.sseClientsMu.RLock()
	defer s.sseClientsMu.RUnlock()

	for ch := range s.sseClients {
		select {
		case ch <- event:
		default:
			// Client buffer full, skip
		}
	}
}
