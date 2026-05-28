/**
 * Configuration for API and WebSocket connections
 * Automatically detects the correct backend URL based on current host
 */

// Get the backend URL based on current location
export function getApiUrl(): string {
  // In development with Vite proxy, we can use relative URLs
  // In production or remote access, we need to use the full URL

  const hostname = window.location.hostname;

  // If accessing via localhost, use localhost
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:4000';
  }

  // Otherwise, use the same hostname with port 4000
  return `http://${hostname}:4000`;
}

// Get the WebSocket URL
export function getWebSocketUrl(): string {
  const hostname = window.location.hostname;

  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'ws://localhost:4000/stream';
  }

  return `ws://${hostname}:4000/stream`;
}
