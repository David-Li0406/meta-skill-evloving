// Package main provides a lightweight health check binary for init containers.
// This replaces curl-based health checks since the container image doesn't include curl.
//
// Usage:
//
//	healthcheck <url> [options]
//
// Options:
//
//	--timeout=<duration>              HTTP request timeout (default: 5s)
//	--interval=<duration>             Retry interval (default: 10s)
//	--max-retries=<n>                 Maximum retries, 0=unlimited (default: 0)
//	--bearer-token-file=<path>        Path to bearer token file
//	--bearer-token=<token>            Bearer token string
//	--insecure-skip-verify            Skip TLS verification
//	--header=<Name:Value>             Custom HTTP header (can be repeated)
//
// Examples:
//
//	# Simple HTTP health check
//	healthcheck http://coordination-engine:8080/health
//
//	# Authenticated Prometheus health check with ServiceAccount token
//	healthcheck https://prometheus-k8s.openshift-monitoring.svc:9091/-/ready \
//	  --bearer-token-file=/var/run/secrets/kubernetes.io/serviceaccount/token \
//	  --insecure-skip-verify
//
//	# With custom timeout and interval
//	healthcheck http://service:8080/healthz --timeout=10s --interval=5s --max-retries=30
package main

import (
	"crypto/tls"
	"flag"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"
)

// stringSlice implements flag.Value for repeated string flags
type stringSlice []string

func (s *stringSlice) String() string {
	return strings.Join(*s, ", ")
}

func (s *stringSlice) Set(value string) error {
	*s = append(*s, value)
	return nil
}

func main() {
	// Existing flags
	timeout := flag.Duration("timeout", 5*time.Second, "HTTP request timeout")
	interval := flag.Duration("interval", 10*time.Second, "Retry interval between health checks")
	maxRetries := flag.Int("max-retries", 0, "Maximum number of retries (0 = unlimited)")

	// New authentication flags
	bearerTokenFile := flag.String("bearer-token-file", "", "Path to bearer token file (e.g., /var/run/secrets/kubernetes.io/serviceaccount/token)")
	bearerToken := flag.String("bearer-token", "", "Bearer token string (alternative to file)")
	insecureSkipVerify := flag.Bool("insecure-skip-verify", false, "Skip TLS certificate verification (use with caution)")

	// Custom headers (can be repeated)
	var headers stringSlice
	flag.Var(&headers, "header", "Additional header in format 'Name: Value' (can be repeated)")

	flag.Parse()

	// Validate args
	args := flag.Args()
	if len(args) < 1 {
		printUsage()
		os.Exit(1)
	}

	url := args[0]

	// Configure HTTP client with TLS settings
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: *insecureSkipVerify, //nolint:gosec // User explicitly requested skip verify
		},
	}
	client := &http.Client{
		Timeout:   *timeout,
		Transport: transport,
	}

	// Load bearer token if specified
	token, err := loadBearerToken(*bearerTokenFile, *bearerToken)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error loading bearer token: %v\n", err)
		os.Exit(1)
	}

	// Parse custom headers
	customHeaders, err := parseHeaders(headers)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing headers: %v\n", err)
		os.Exit(1)
	}

	retries := 0
	for {
		// Create request
		req, err := http.NewRequest("GET", url, nil)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error creating request: %v\n", err)
			os.Exit(1)
		}

		// Add bearer token if provided
		if token != "" {
			req.Header.Set("Authorization", "Bearer "+token)
		}

		// Add custom headers
		for name, value := range customHeaders {
			req.Header.Set(name, value)
		}

		// Execute request
		resp, err := client.Do(req)
		if err == nil && resp.StatusCode >= 200 && resp.StatusCode < 300 {
			_ = resp.Body.Close()
			fmt.Printf("Service at %s is ready! (HTTP %d)\n", url, resp.StatusCode)
			os.Exit(0)
		}

		// Log the failure reason
		if err != nil {
			fmt.Printf("Service at %s not ready: %v\n", url, err)
		} else {
			fmt.Printf("Service at %s not ready: HTTP %d\n", url, resp.StatusCode)
			_ = resp.Body.Close()
		}

		retries++
		if *maxRetries > 0 && retries >= *maxRetries {
			fmt.Fprintf(os.Stderr, "Max retries (%d) exceeded, giving up\n", *maxRetries)
			os.Exit(1)
		}

		fmt.Printf("Retrying in %v... (attempt %d", *interval, retries)
		if *maxRetries > 0 {
			fmt.Printf("/%d", *maxRetries)
		}
		fmt.Println(")")
		time.Sleep(*interval)
	}
}

// loadBearerToken loads the bearer token from file or returns the direct token value
func loadBearerToken(tokenFile, tokenValue string) (string, error) {
	if tokenFile != "" {
		tokenBytes, err := os.ReadFile(tokenFile)
		if err != nil {
			return "", fmt.Errorf("reading bearer token file: %w", err)
		}
		// Trim whitespace/newlines from token
		return strings.TrimSpace(string(tokenBytes)), nil
	}
	return tokenValue, nil
}

// parseHeaders parses header strings in "Name: Value" format
func parseHeaders(headerFlags []string) (map[string]string, error) {
	headers := make(map[string]string)
	for _, h := range headerFlags {
		// Split on first colon
		idx := strings.Index(h, ":")
		if idx == -1 {
			return nil, fmt.Errorf("invalid header format %q, expected 'Name: Value'", h)
		}
		name := strings.TrimSpace(h[:idx])
		value := strings.TrimSpace(h[idx+1:])
		if name == "" {
			return nil, fmt.Errorf("empty header name in %q", h)
		}
		headers[name] = value
	}
	return headers, nil
}

// printUsage prints the help message
func printUsage() {
	fmt.Fprintln(os.Stderr, "Usage: healthcheck <url> [options]")
	fmt.Fprintln(os.Stderr, "")
	fmt.Fprintln(os.Stderr, "A lightweight health check utility for init containers.")
	fmt.Fprintln(os.Stderr, "Retries until the URL returns HTTP 2xx or max retries is reached.")
	fmt.Fprintln(os.Stderr, "")
	fmt.Fprintln(os.Stderr, "Options:")
	fmt.Fprintln(os.Stderr, "  --timeout=<duration>              HTTP request timeout (default: 5s)")
	fmt.Fprintln(os.Stderr, "  --interval=<duration>             Retry interval (default: 10s)")
	fmt.Fprintln(os.Stderr, "  --max-retries=<n>                 Maximum retries, 0=unlimited (default: 0)")
	fmt.Fprintln(os.Stderr, "  --bearer-token-file=<path>        Path to bearer token file")
	fmt.Fprintln(os.Stderr, "  --bearer-token=<token>            Bearer token string")
	fmt.Fprintln(os.Stderr, "  --insecure-skip-verify            Skip TLS verification")
	fmt.Fprintln(os.Stderr, "  --header=<Name:Value>             Custom HTTP header (can be repeated)")
	fmt.Fprintln(os.Stderr, "")
	fmt.Fprintln(os.Stderr, "Examples:")
	fmt.Fprintln(os.Stderr, "  # Simple HTTP health check")
	fmt.Fprintln(os.Stderr, "  healthcheck http://coordination-engine:8080/health")
	fmt.Fprintln(os.Stderr, "")
	fmt.Fprintln(os.Stderr, "  # Authenticated Prometheus health check with ServiceAccount token")
	fmt.Fprintln(os.Stderr, "  healthcheck https://prometheus-k8s.openshift-monitoring.svc:9091/-/ready \\")
	fmt.Fprintln(os.Stderr, "    --bearer-token-file=/var/run/secrets/kubernetes.io/serviceaccount/token \\")
	fmt.Fprintln(os.Stderr, "    --insecure-skip-verify")
	fmt.Fprintln(os.Stderr, "")
	fmt.Fprintln(os.Stderr, "  # With custom timeout, interval, and headers")
	fmt.Fprintln(os.Stderr, "  healthcheck http://service:8080/healthz \\")
	fmt.Fprintln(os.Stderr, "    --timeout=10s --interval=5s --max-retries=30 \\")
	fmt.Fprintln(os.Stderr, "    --header=\"X-Custom-Header: value\"")
}
