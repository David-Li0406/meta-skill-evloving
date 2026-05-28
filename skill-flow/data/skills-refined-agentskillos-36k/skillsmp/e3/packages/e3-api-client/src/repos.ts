/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

import { ArrayType, StringType } from '@elaraai/east';
import { get, unwrap, type RequestOptions } from './http.js';

/**
 * List all repositories on the server.
 *
 * @param url - Base URL of the e3 API server
 * @param options - Request options including auth token
 * @returns Array of repository names
 */
export async function repoList(url: string, options: RequestOptions): Promise<string[]> {
  const response = await get(url, `/repos`, ArrayType(StringType), options);
  return unwrap(response);
}
