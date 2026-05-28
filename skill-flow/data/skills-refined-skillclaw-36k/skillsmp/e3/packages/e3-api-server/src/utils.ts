/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Extract the wildcard path portion from a request path.
 *
 * For routes like `/api/workspaces/:ws/list/*`, this extracts the `*` portion
 * after the known prefix.
 *
 * @param requestPath - The full request path (e.g., "/api/workspaces/prod/list/inputs/config")
 * @param prefixPattern - Regex matching the prefix to strip (e.g., /^\/api\/workspaces\/[^/]+\/list\//)
 * @returns The wildcard portion (e.g., "inputs/config")
 *
 * @example
 * ```ts
 * extractWildcardPath("/api/workspaces/prod/list/inputs/config", /^\/api\/workspaces\/[^/]+\/list\//)
 * // "inputs/config"
 *
 * extractWildcardPath("/api/workspaces/prod/get/data", /^\/api\/workspaces\/[^/]+\/get\//)
 * // "data"
 * ```
 */
export function extractWildcardPath(requestPath: string, prefixPattern: RegExp): string {
  return requestPath.replace(prefixPattern, '');
}
