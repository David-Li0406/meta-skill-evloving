/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 convert command - Transform data between .east, .json, and .beast2 formats
 *
 * Re-exports the existing convert logic.
 */

export { convertFile as convertCommand } from './convert.impl.js';
