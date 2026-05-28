package cli

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/events"
	"github.com/Dicklesworthstone/ntm/internal/serve"
	"github.com/Dicklesworthstone/ntm/internal/state"
)

func newServeCmd() *cobra.Command {
	var (
		port int
	)

	cmd := &cobra.Command{
		Use:   "serve",
		Short: "Start HTTP server with REST API and event streaming",
		Long: `Start a local HTTP server providing REST API and SSE event streaming
for dashboards, monitoring tools, and robot consumption.

API Endpoints:
  GET /api/sessions          List all sessions
  GET /api/sessions/:id      Get session details
  GET /api/sessions/:id/agents  Get agents in session
  GET /api/sessions/:id/events  Get recent events for session
  GET /api/robot/status      Robot status (JSON)
  GET /api/robot/health      Robot health (JSON)
  GET /events                Server-Sent Events stream
  GET /health                Health check

Examples:
  ntm serve                  # Start on default port 7337
  ntm serve --port 8080      # Start on custom port`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runServe(port)
		},
	}

	cmd.Flags().IntVar(&port, "port", 7337, "HTTP server port")

	return cmd
}

func runServe(port int) error {
	// Get state store path
	home, err := os.UserHomeDir()
	if err != nil {
		return fmt.Errorf("get home dir: %w", err)
	}
	dbPath := filepath.Join(home, ".config", "ntm", "state.db")

	// Open state store
	stateStore, err := state.Open(dbPath)
	if err != nil {
		return fmt.Errorf("open state store: %w", err)
	}
	defer stateStore.Close()

	// Ensure migrations are applied
	if err := stateStore.Migrate(); err != nil {
		return fmt.Errorf("apply migrations: %w", err)
	}

	// Create server with default event bus
	srv := serve.New(serve.Config{
		Port:       port,
		EventBus:   events.DefaultBus,
		StateStore: stateStore,
	})

	// Setup signal handling for graceful shutdown
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigCh
		fmt.Println("\nReceived shutdown signal")
		cancel()
	}()

	fmt.Printf("Starting NTM server on http://localhost:%d\n", port)
	fmt.Println("Press Ctrl+C to stop")

	return srv.Start(ctx)
}
