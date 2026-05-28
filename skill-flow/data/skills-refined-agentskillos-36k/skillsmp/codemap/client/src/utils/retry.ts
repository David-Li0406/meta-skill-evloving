/**
 * Retry utility with exponential backoff
 */
export interface RetryOptions {
  maxAttempts?: number;
  initialDelay?: number;
  maxDelay?: number;
  backoffFactor?: number;
  shouldRetry?: (error: Error) => boolean;
  onRetry?: (attempt: number, error: Error) => void;
}

export async function retry<T>(fn: () => Promise<T>, options: RetryOptions = {}): Promise<T> {
  const {
    maxAttempts = 3,
    initialDelay = 1000,
    maxDelay = 30000,
    backoffFactor = 2,
    shouldRetry = () => true,
    onRetry,
  } = options;

  let lastError: Error | null = null;
  let attempt = 0;

  while (attempt < maxAttempts) {
    attempt++;

    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (attempt >= maxAttempts || !shouldRetry(lastError)) {
        throw lastError;
      }

      onRetry?.(attempt, lastError);

      // Exponential backoff with jitter
      const delay = Math.min(initialDelay * Math.pow(backoffFactor, attempt - 1), maxDelay);
      const jitter = delay * 0.1 * Math.random();
      const effectiveDelay = delay + jitter;

      await sleep(effectiveDelay);
    }
  }

  throw lastError;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Tauri API wrapper with retry logic
 */
export async function invokeWithRetry<T>(
  command: string,
  args?: Record<string, unknown>,
  options?: RetryOptions
): Promise<T> {
  return retry(() => {
    return window.__TAURI__.core.invoke<T>(command, args);
  }, options);
}

/**
 * Retry configuration for different operation types
 */
export const RetryConfig = {
  // File operations - retry on network issues
  fileOperations: {
    maxAttempts: 3,
    initialDelay: 1000,
    shouldRetry: (error: Error) => {
      const message = error.message.toLowerCase();
      return (
        message.includes('network') ||
        message.includes('timeout') ||
        message.includes('econnrefused')
      );
    },
  },

  // Code map generation - retry with longer delay
  codeGeneration: {
    maxAttempts: 2,
    initialDelay: 2000,
    shouldRetry: (error: Error) => {
      const message = error.message.toLowerCase();
      return !message.includes('invalid') && !message.includes('not found');
    },
  },

  // Storage operations - quick retry
  storage: {
    maxAttempts: 3,
    initialDelay: 500,
    shouldRetry: () => true,
  },
} as const;
