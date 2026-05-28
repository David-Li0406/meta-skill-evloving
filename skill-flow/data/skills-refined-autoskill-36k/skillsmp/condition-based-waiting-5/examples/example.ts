// Condition-based waiting utilities
// Replace arbitrary timeouts with condition polling

/**
 * Wait for a condition to become truthy
 */
export async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise(r => setTimeout(r, 10));
  }
}

/**
 * Wait for specific event type
 */
export function waitForEvent<T extends { type: string }>(
  getEvents: () => T[],
  eventType: string,
  timeoutMs = 5000
): Promise<T> {
  return waitFor(
    () => getEvents().find(e => e.type === eventType),
    `${eventType} event`,
    timeoutMs
  );
}

/**
 * Wait for N events of a type
 */
export function waitForEventCount<T extends { type: string }>(
  getEvents: () => T[],
  eventType: string,
  count: number,
  timeoutMs = 5000
): Promise<T[]> {
  return waitFor(
    () => {
      const matching = getEvents().filter(e => e.type === eventType);
      return matching.length >= count ? matching : undefined;
    },
    `${count} ${eventType} events`,
    timeoutMs
  );
}

/**
 * Wait for event matching predicate
 */
export function waitForEventMatch<T>(
  getEvents: () => T[],
  predicate: (event: T) => boolean,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  return waitFor(
    () => getEvents().find(predicate),
    description,
    timeoutMs
  );
}

// Usage example:
//
// BEFORE (flaky):
// await new Promise(r => setTimeout(r, 300));
// expect(results.length).toBe(2);  // Fails randomly
//
// AFTER (reliable):
// await waitForEventCount(getEvents, 'RESULT', 2);
// expect(results.length).toBe(2);  // Always succeeds
