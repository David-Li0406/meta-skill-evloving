# Prompt Caching - Sharp Edges

## Cache Miss Explosion

### **Id**
cache-miss-explosion
### **Summary**
Cache miss causes latency spike with additional overhead
### **Severity**
high
### **Situation**
Slow response when cache miss, slower than no caching
### **Why**
  Cache check adds latency.
  Cache write adds more latency.
  Miss + overhead > no caching.
  
### **Solution**
  // Optimize for cache misses, not just hits
  
  class OptimizedCache {
      async queryWithCache(prompt: string): Promise<string> {
          const cacheKey = this.hash(prompt);
  
          // Non-blocking cache check
          const cachedPromise = this.cache.get(cacheKey);
          const llmPromise = this.queryLLM(prompt);
  
          // Race: use cache if available before LLM returns
          const cached = await Promise.race([
              cachedPromise,
              sleep(50).then(() => null)  // 50ms cache timeout
          ]);
  
          if (cached) {
              // Cancel LLM request if possible
              return cached;
          }
  
          // Cache miss: continue with LLM
          const response = await llmPromise;
  
          // Async cache write (don't block response)
          this.cache.set(cacheKey, response).catch(console.error);
  
          return response;
      }
  }
  
  // Alternative: Probabilistic caching
  // Only cache if query matches known high-frequency patterns
  class SelectiveCache {
      private patterns: Map<string, number> = new Map();
  
      shouldCache(prompt: string): boolean {
          const pattern = this.extractPattern(prompt);
          const frequency = this.patterns.get(pattern) || 0;
  
          // Only cache high-frequency patterns
          return frequency > 10;
      }
  
      recordQuery(prompt: string): void {
          const pattern = this.extractPattern(prompt);
          this.patterns.set(pattern, (this.patterns.get(pattern) || 0) + 1);
      }
  }
  
### **Symptoms**
  - Slow responses on cache miss
  - Cache hit rate below 50%
  - Higher latency than uncached
### **Detection Pattern**
cache\.get|getCached|checkCache

## Stale Cache Wrong Answers

### **Id**
stale-cache-wrong-answers
### **Summary**
Cached responses become incorrect over time
### **Severity**
high
### **Situation**
Users get outdated or wrong information from cache
### **Why**
  Source data changed.
  No cache invalidation.
  Long TTLs for dynamic data.
  
### **Solution**
  // Implement proper cache invalidation
  
  class InvalidatingCache {
      // Version-based invalidation
      private cacheVersion = 1;
  
      getCacheKey(prompt: string): string {
          return `v${this.cacheVersion}:${this.hash(prompt)}`;
      }
  
      invalidateAll(): void {
          this.cacheVersion++;
          // Old keys automatically become orphaned
      }
  
      // Content-hash invalidation
      async setWithContentHash(
          key: string,
          response: string,
          sourceContent: string
      ): Promise<void> {
          const contentHash = this.hash(sourceContent);
          await this.cache.set(key, {
              response,
              contentHash,
              timestamp: Date.now()
          });
      }
  
      async getIfValid(
          key: string,
          currentSourceContent: string
      ): Promise<string | null> {
          const cached = await this.cache.get(key);
          if (!cached) return null;
  
          // Check if source content changed
          const currentHash = this.hash(currentSourceContent);
          if (cached.contentHash !== currentHash) {
              await this.cache.delete(key);
              return null;
          }
  
          return cached.response;
      }
  
      // Event-based invalidation
      onSourceUpdate(sourceId: string): void {
          // Invalidate all caches that used this source
          this.invalidateByTag(`source:${sourceId}`);
      }
  }
  
### **Symptoms**
  - Users report wrong information
  - Answers don't match current data
  - Complaints about outdated responses
### **Detection Pattern**
cache\.set|setCache|TTL|expire

## Prompt Cache Prefix Mismatch

### **Id**
prompt-cache-prefix-mismatch
### **Summary**
Prompt caching doesn't work due to prefix changes
### **Severity**
medium
### **Situation**
Cache misses despite similar prompts
### **Why**
  Anthropic caching requires exact prefix match.
  Timestamps or dynamic content in prefix.
  Different message order.
  
### **Solution**
  // Structure prompts for optimal caching
  
  class CacheOptimizedPrompts {
      // WRONG: Dynamic content in cached prefix
      buildPromptBad(query: string): SystemMessage[] {
          return [
              {
                  type: "text",
                  text: `You are helpful. Current time: ${new Date()}`,  // BREAKS CACHE!
                  cache_control: { type: "ephemeral" }
              }
          ];
      }
  
      // RIGHT: Static prefix, dynamic at end
      buildPromptGood(query: string): SystemMessage[] {
          return [
              {
                  type: "text",
                  text: STATIC_SYSTEM_PROMPT,  // Never changes
                  cache_control: { type: "ephemeral" }
              },
              {
                  type: "text",
                  text: STATIC_KNOWLEDGE_BASE,  // Rarely changes
                  cache_control: { type: "ephemeral" }
              }
              // Dynamic content goes in messages, NOT system
          ];
      }
  
      // Prefix ordering matters
      buildWithConsistentOrder(components: string[]): SystemMessage[] {
          // Sort components for consistent ordering
          const sorted = [...components].sort();
          return sorted.map((c, i) => ({
              type: "text",
              text: c,
              cache_control: i === sorted.length - 1
                  ? { type: "ephemeral" }
                  : undefined  // Only cache the full prefix
          }));
      }
  }
  
### **Symptoms**
  - Cache hit rate lower than expected
  - Cache creation tokens high, read low
  - Similar prompts not hitting cache
### **Detection Pattern**
cache_control|ephemeral|cache.*prefix