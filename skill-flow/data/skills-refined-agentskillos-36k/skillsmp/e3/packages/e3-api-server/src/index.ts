/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3-api-server: HTTP server exposing e3-core operations
 *
 * Provides a REST API with BEAST2 serialization for remote access to e3 repositories.
 * Stateless design - clients poll /status endpoint to track execution progress.
 */

export { createServer, type ServerConfig, type Server } from './server.js';
export { ApiTypes } from './types.js';

// Export handlers for Lambda reuse
export * from './handlers/index.js';

// Export auth middleware
export { createAuthMiddleware, type AuthConfig } from './middleware/auth.js';

// Export BEAST2 helpers for custom integrations
export { sendSuccess, sendError, sendSuccessWithStatus, decodeBeast2, decodeBody } from './beast2.js';
