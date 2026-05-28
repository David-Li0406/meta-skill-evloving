/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * Local filesystem implementation of StorageBackend.
 *
 * This wraps the existing e3-core filesystem functions to provide a
 * StorageBackend that works with local repositories.
 */

export { LocalStorage, LocalBackend } from './LocalBackend.js';
export { LocalObjectStore } from './LocalObjectStore.js';
export { LocalRefStore } from './LocalRefStore.js';
export { LocalLockService } from './LocalLockService.js';
export { LocalLogStore } from './LocalLogStore.js';
