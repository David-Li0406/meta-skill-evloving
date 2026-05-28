/**
 * N+1 Query Detection Helper
 *
 * Add this to your React app to detect N+1 patterns in real-time.
 * Works with React Query and fetch-based APIs.
 *
 * Usage:
 * 1. Import this script in your main component
 * 2. Call initN1Detection() in useEffect
 * 3. Open browser console and watch for warnings
 */

// Configuration
const CONFIG = {
  QUERY_BURST_THRESHOLD: 5, // Warn if >5 queries in 500ms
  BURST_WINDOW_MS: 500, // Window for burst detection
  SAME_ENDPOINT_THRESHOLD: 3, // Warn if >3 requests to same endpoint
  ENABLE_LOGGING: true, // Log all queries
};

// State
let queryLog: Array<{ url: string; timestamp: number }> = [];
let requestLog: string[] = [];

/**
 * Monitor fetch requests for N+1 patterns
 */
export function initN1Detection() {
  if (typeof window === "undefined") return;

  const originalFetch = window.fetch;

  window.fetch = async (...args) => {
    const url = typeof args[0] === "string" ? args[0] : args[0]?.url;
    const timestamp = Date.now();

    // Log request
    queryLog.push({ url, timestamp });
    requestLog.push(url);

    if (CONFIG.ENABLE_LOGGING) {
      console.debug(`[Query ${queryLog.length}]`, url);
    }

    // Check for burst (many queries in short time)
    checkForBurst(timestamp);

    // Check for repeated endpoints
    checkForRepeatedEndpoints(url);

    // Execute original fetch
    const result = await originalFetch(...args);

    return result;
  };

  console.log("✅ N+1 Detection initialized. Check console for warnings.");
}

/**
 * Detect rapid bursts of queries (N+1 pattern)
 */
function checkForBurst(timestamp: number) {
  // Remove old queries outside burst window
  const cutoff = timestamp - CONFIG.BURST_WINDOW_MS;
  queryLog = queryLog.filter((q) => q.timestamp > cutoff);

  if (queryLog.length > CONFIG.QUERY_BURST_THRESHOLD) {
    const queries = queryLog.map((q) => new URL(q.url).pathname);
    console.warn(
      `🔴 BURST DETECTED: ${queryLog.length} queries in ${CONFIG.BURST_WINDOW_MS}ms`,
      queries,
    );
    console.warn("   This may indicate an N+1 pattern. Check:");
    console.warn("   1. Are you calling useQuery in a mapped component?");
    console.warn("   2. Are you loading data in a loop or forEach?");
    console.warn("   3. Can you batch these requests into one?");
  }
}

/**
 * Detect repeated requests to the same endpoint
 */
function checkForRepeatedEndpoints(url: string) {
  const endpoint = new URL(url).pathname;
  const count = requestLog.filter((u) => new URL(u).pathname === endpoint).length;

  if (count === CONFIG.SAME_ENDPOINT_THRESHOLD) {
    console.warn(
      `⚠️ REPEATED ENDPOINT: "${endpoint}" requested ${count} times`,
      "Recent requests:",
      requestLog.filter((u) => new URL(u).pathname === endpoint),
    );
    console.warn("   Consider batching these into a single request.");
  }
}

/**
 * Monitor React Query for N+1 patterns
 *
 * Usage:
 * const queryClient = useQueryClient();
 * monitorReactQueryN1(queryClient);
 */
export function monitorReactQueryN1(queryClient: any) {
  if (!queryClient) return;

  const cache = queryClient.getQueryCache();

  // Monitor for rapid query updates
  let recentQueries: Array<{ queryKey: any; timestamp: number }> = [];

  // Intercept cache updates
  const originalSetData = cache.setData;
  cache.setData = function (queryKey: any, data: any, options: any) {
    const timestamp = Date.now();
    recentQueries.push({ queryKey, timestamp });

    // Remove old queries outside 500ms window
    recentQueries = recentQueries.filter((q) => timestamp - q.timestamp < 500);

    if (recentQueries.length > CONFIG.QUERY_BURST_THRESHOLD) {
      console.warn(
        `🔴 QUERY BURST (React Query): ${recentQueries.length} updates in 500ms`,
        recentQueries.map((q) => q.queryKey),
      );
    }

    return originalSetData.call(this, queryKey, data, options);
  };

  console.log("✅ React Query N+1 monitoring initialized.");
}

/**
 * Analyze a component for potential N+1 patterns
 * Call this after rendering a component to analyze query patterns
 */
export function analyzeQueryPattern(componentName: string) {
  console.group(`📊 Analysis: ${componentName}`);

  // Count unique endpoints
  const uniqueEndpoints = new Set(requestLog.map((u) => new URL(u).pathname));
  console.log(`Total requests: ${requestLog.length}`);
  console.log(`Unique endpoints: ${uniqueEndpoints.size}`);
  console.log(
    `Queries per endpoint:`,
    Array.from(uniqueEndpoints).map((ep) => ({
      endpoint: ep,
      count: requestLog.filter((u) => new URL(u).pathname === ep).length,
    })),
  );

  // Recommend optimizations
  if (requestLog.length > 5) {
    console.warn("Consider these optimizations:");
    if (
      Array.from(uniqueEndpoints).some(
        (ep) => requestLog.filter((u) => new URL(u).pathname === ep).length > 3,
      )
    ) {
      console.warn("1. Batch multiple requests to the same endpoint");
    }
    if (requestLog.length > 10) {
      console.warn("2. Load data at a higher level component");
    }
    console.warn("3. Use pagination or virtualization for large lists");
  }

  console.groupEnd();
}

/**
 * Reset query log (call between page loads)
 */
export function resetQueryLog() {
  queryLog = [];
  requestLog = [];
  console.log("🔄 Query log reset.");
}

/**
 * Get current query statistics
 */
export function getQueryStats() {
  const uniqueEndpoints = new Set(requestLog.map((u) => new URL(u).pathname));

  return {
    totalQueries: requestLog.length,
    uniqueEndpoints: uniqueEndpoints.size,
    queriesPerEndpoint: Array.from(uniqueEndpoints).map((ep) => ({
      endpoint: ep,
      count: requestLog.filter((u) => new URL(u).pathname === ep).length,
      repeated: requestLog.filter((u) => new URL(u).pathname === ep).length > 1,
    })),
  };
}

// Auto-initialize if in development
if (typeof window !== "undefined" && process.env.NODE_ENV === "development") {
  window.addEventListener("DOMContentLoaded", () => {
    initN1Detection();

    // Expose helpers to window for manual inspection
    (window as any).N1Detection = {
      analyzeQueryPattern,
      getQueryStats,
      resetQueryLog,
      monitorReactQueryN1,
    };

    console.log('💡 Use window.N1Detection.analyzeQueryPattern("ComponentName") for analysis');
  });
}
