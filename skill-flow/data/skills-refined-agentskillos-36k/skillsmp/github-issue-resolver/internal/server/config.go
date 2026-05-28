package server

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

// TransportType defines the MCP transport protocol
type TransportType string

const (
	// TransportHTTP uses Server-Sent Events (SSE) for OpenShift Lightspeed integration
	// This is the ONLY supported transport as of 2025-12-17
	TransportHTTP TransportType = "http"
	// TransportStdio uses standard input/output for local development (Claude Desktop)
	// DEPRECATED: stdio transport is no longer supported as of 2025-12-17
	// Use HTTP transport for all use cases including local development
	TransportStdio TransportType = "stdio"
)

// Config holds the MCP server configuration
type Config struct {
	// Transport specifies the protocol (http or stdio)
	// Default: http (for OpenShift Lightspeed)
	Transport TransportType

	// HTTP Transport Settings
	HTTPHost string // Default: "0.0.0.0"
	HTTPPort int    // Default: 8080

	// Server Metadata
	Name    string // Default: "openshift-cluster-health"
	Version string // Default: "0.1.0"

	// Integration Endpoints
	CoordinationEngineURL string // Coordination Engine base URL
	PrometheusURL         string // Prometheus API URL
	KServeNamespace       string // KServe models namespace
	KServePredictorPort   int    // KServe predictor port (8080 for RawDeployment, 80 for Serverless)

	// Feature Flags
	EnableCoordinationEngine bool // Enable Coordination Engine integration
	EnablePrometheus         bool // Enable Prometheus integration
	EnableKServe             bool // Enable KServe ML model integration

	// Performance Settings
	CacheTTL           time.Duration // Cache TTL for Kubernetes API responses
	RequestTimeout     time.Duration // HTTP client timeout
	MaxConcurrentTools int           // Max concurrent tool executions
}

// NewConfig creates a Config from environment variables with sensible defaults
func NewConfig() *Config {
	cfg := &Config{
		// Transport (default: HTTP for OpenShift Lightspeed)
		// stdio transport DEPRECATED as of 2025-12-17
		Transport: getEnvTransport("MCP_TRANSPORT", TransportHTTP),

		// HTTP Settings
		HTTPHost: getEnv("MCP_HTTP_HOST", "0.0.0.0"),
		HTTPPort: getEnvInt("MCP_HTTP_PORT", 8080),

		// Server Metadata
		Name:    getEnv("MCP_SERVER_NAME", "openshift-cluster-health"),
		Version: getEnv("MCP_SERVER_VERSION", "0.1.0"),

		// Integration Endpoints
		CoordinationEngineURL: getEnv("COORDINATION_ENGINE_URL", "http://coordination-engine:8080"),
		PrometheusURL:         getEnv("PROMETHEUS_URL", "https://prometheus-k8s.openshift-monitoring.svc:9091"),
		KServeNamespace:       getEnv("KSERVE_NAMESPACE", "self-healing-platform"),
		KServePredictorPort:   getEnvInt("KSERVE_PREDICTOR_PORT", 8080), // Default 8080 for RawDeployment mode

		// Feature Flags
		EnableCoordinationEngine: getEnvBool("ENABLE_COORDINATION_ENGINE", false), // Disabled by default (Phase 1)
		EnablePrometheus:         getEnvBool("ENABLE_PROMETHEUS", false),          // Disabled by default (Phase 3)
		EnableKServe:             getEnvBool("ENABLE_KSERVE", false),              // Disabled by default (Phase 4)

		// Performance Settings
		CacheTTL:           getEnvDuration("CACHE_TTL", 30*time.Second),
		RequestTimeout:     getEnvDuration("REQUEST_TIMEOUT", 10*time.Second),
		MaxConcurrentTools: getEnvInt("MAX_CONCURRENT_TOOLS", 10),
	}

	return cfg
}

// Validate checks if the configuration is valid
func (c *Config) Validate() error {
	if c.Transport != TransportHTTP && c.Transport != TransportStdio {
		return fmt.Errorf("invalid transport: %s (must be 'http' or 'stdio')", c.Transport)
	}

	if c.Transport == TransportHTTP {
		if c.HTTPPort < 1 || c.HTTPPort > 65535 {
			return fmt.Errorf("invalid HTTP port: %d (must be 1-65535)", c.HTTPPort)
		}
	}

	if c.CacheTTL < 1*time.Second {
		return fmt.Errorf("cache TTL too low: %v (minimum 1s)", c.CacheTTL)
	}

	return nil
}

// GetHTTPAddr returns the HTTP listen address
func (c *Config) GetHTTPAddr() string {
	return fmt.Sprintf("%s:%d", c.HTTPHost, c.HTTPPort)
}

// Helper functions to read environment variables

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}

func getEnvDuration(key string, defaultValue time.Duration) time.Duration {
	if value := os.Getenv(key); value != "" {
		if duration, err := time.ParseDuration(value); err == nil {
			return duration
		}
	}
	return defaultValue
}

func getEnvTransport(key string, defaultValue TransportType) TransportType {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}

	transport := TransportType(value)
	if transport == TransportHTTP || transport == TransportStdio {
		return transport
	}

	// Invalid value, return default
	return defaultValue
}
