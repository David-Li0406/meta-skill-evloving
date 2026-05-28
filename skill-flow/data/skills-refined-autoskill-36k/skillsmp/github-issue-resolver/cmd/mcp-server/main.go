package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/internal/server"
)

var (
	// Version is set during build via -ldflags
	Version = "0.1.0-dev"
)

func main() {
	fmt.Println("╔═══════════════════════════════════════════════════════════╗")
	fmt.Println("║  OpenShift Cluster Health MCP Server                     ║")
	fmt.Printf("║  Version: %-48s║\n", Version)
	fmt.Println("╚═══════════════════════════════════════════════════════════╝")
	fmt.Println()

	// Load configuration from environment
	config := server.NewConfig()

	// Display configuration
	printConfig(config)

	// Validate configuration
	if err := config.Validate(); err != nil {
		log.Fatalf("Configuration error: %v", err)
	}

	// Create MCP server
	mcpServer, err := server.NewMCPServer(config)
	if err != nil {
		log.Fatalf("Failed to create MCP server: %v", err)
	}

	// TODO Phase 1.3-1.4: Register MCP tools
	// tools := []mcp.Tool{
	//     NewClusterHealthTool(),
	//     NewListPodsTool(),
	// }
	// if err := mcpServer.RegisterTools(tools); err != nil {
	//     log.Fatalf("Failed to register tools: %v", err)
	// }

	log.Println("MCP Server starting...")

	// Create context that listens for shutdown signals
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Handle shutdown signals gracefully
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	go func() {
		sig := <-sigChan
		log.Printf("Received signal: %v", sig)
		log.Println("Initiating graceful shutdown...")
		cancel()
	}()

	// Start the MCP server
	if err := mcpServer.Start(ctx); err != nil {
		log.Fatalf("Server error: %v", err)
	}

	log.Println("MCP Server stopped")
}

// printConfig displays the server configuration
func printConfig(cfg *server.Config) {
	fmt.Println("Configuration:")
	fmt.Println("──────────────────────────────────────────────────────────")
	fmt.Printf("  Transport:           %s\n", cfg.Transport)

	if cfg.Transport == server.TransportHTTP {
		fmt.Printf("  HTTP Address:        %s\n", cfg.GetHTTPAddr())
	}

	fmt.Printf("  Cache TTL:           %v\n", cfg.CacheTTL)
	fmt.Printf("  Request Timeout:     %v\n", cfg.RequestTimeout)
	fmt.Println()

	fmt.Println("Integrations:")
	fmt.Println("──────────────────────────────────────────────────────────")
	fmt.Printf("  Coordination Engine: %v", cfg.EnableCoordinationEngine)
	if cfg.EnableCoordinationEngine {
		fmt.Printf(" (%s)", cfg.CoordinationEngineURL)
	}
	fmt.Println()

	fmt.Printf("  Prometheus:          %v", cfg.EnablePrometheus)
	if cfg.EnablePrometheus {
		fmt.Printf(" (%s)", cfg.PrometheusURL)
	}
	fmt.Println()

	fmt.Printf("  KServe:              %v", cfg.EnableKServe)
	if cfg.EnableKServe {
		fmt.Printf(" (namespace: %s, port: %d)", cfg.KServeNamespace, cfg.KServePredictorPort)
	}
	fmt.Println()
	fmt.Println("──────────────────────────────────────────────────────────")
	fmt.Println()
}
