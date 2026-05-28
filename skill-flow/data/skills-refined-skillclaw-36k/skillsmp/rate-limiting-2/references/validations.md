# Rate Limiting - Validations

## In-Memory Rate Limiting

### **Id**
rate-limit-memory-store
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new Map\(\).*rate
  - rateLimit.*store.*memory
  - RateLimiterMemory(?![\s\S]{0,200}fallback|backup)
  - limits\s*=\s*\{\}.*rate
### **Message**
In-memory rate limiting doesn't work with multiple servers. Use Redis.
### **Fix Action**
Use RateLimiterRedis or express-rate-limit with Redis store
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/middleware/**

## Missing Retry-After Header

### **Id**
rate-limit-no-retry-after
### **Severity**
error
### **Type**
regex
### **Pattern**
  - status\(429\)(?![\s\S]{0,300}Retry-After|retryAfter)
  - 429.*json(?![\s\S]{0,200}retry)
### **Message**
429 responses should include Retry-After header for proper client backoff.
### **Fix Action**
Add res.set('Retry-After', seconds) before sending 429
### **Applies To**
  - **/*.ts
  - **/*.js

## Non-Atomic Rate Limit Check

### **Id**
rate-limit-race-condition
### **Severity**
error
### **Type**
regex
### **Pattern**
  - redis\.get.*limit.*redis\.incr
  - get.*count.*incr.*count
  - await.*get.*if.*await.*incr
### **Message**
Non-atomic rate limit check has race condition. Use INCR or Lua script.
### **Fix Action**
Use atomic INCR (returns new value) or Lua script for check-and-increment
### **Applies To**
  - **/*.ts
  - **/*.js

## Rate Limiting by IP Only

### **Id**
rate-limit-ip-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - rateLimit.*req\.ip(?![\s\S]{0,300}user|userId)
  - keyGenerator.*req\.ip(?![\s\S]{0,100}user)
  - key.*=.*req\.ip(?![\s\S]{0,100}user)
### **Message**
IP-only rate limiting fails for shared IPs (NAT, VPN). Consider user ID.
### **Fix Action**
Use user ID when available, fall back to IP for anonymous
### **Applies To**
  - **/*.ts
  - **/*.js

## No Rate Limit Headers

### **Id**
rate-limit-no-headers
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - rateLimit(?![\s\S]{0,500}X-RateLimit|standardHeaders)
  - limiter\.consume(?![\s\S]{0,300}remainingPoints|headers)
### **Message**
Rate limit responses should include limit/remaining/reset headers.
### **Fix Action**
Add X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset headers
### **Applies To**
  - **/*.ts
  - **/*.js

## Rate Limiting Health Endpoints

### **Id**
rate-limit-blocking-health
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.use.*rateLimit(?![\s\S]{0,500}skip.*health)
  - router\.use.*rateLimit(?![\s\S]{0,300}/health)
### **Message**
Rate limiting may block health check endpoints, breaking orchestration.
### **Fix Action**
Add skip function to exclude /health and internal endpoints
### **Applies To**
  - **/*.ts
  - **/*.js

## Fixed Window Without Sliding

### **Id**
rate-limit-fixed-window-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Math\.floor.*Date\.now.*60000(?![\s\S]{0,500}sliding|weighted)
  - window.*=.*Math\.floor(?![\s\S]{0,500}previous|sliding)
### **Message**
Fixed window allows 2x burst at boundaries. Consider sliding window.
### **Fix Action**
Use sliding window counter for accurate limiting
### **Applies To**
  - **/*.ts
  - **/*.js

## Immediate Block Without Progressive

### **Id**
rate-limit-no-backoff
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - blockDuration.*3600|block.*hour(?![\s\S]{0,300}progressive)
  - ban.*3600(?![\s\S]{0,200}warning)
### **Message**
Long blocks without warning frustrate legitimate users. Use progressive limits.
### **Fix Action**
Implement progressive enforcement: warning → soft block → hard block
### **Applies To**
  - **/*.ts
  - **/*.js

## Hardcoded Rate Limits

### **Id**
rate-limit-hardcoded
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - max.*100(?![\s\S]{0,100}process\.env|config)
  - points.*100(?![\s\S]{0,100}LIMIT|config)
  - limit.*=.*[0-9]+(?![\s\S]{0,100}env|config)
### **Message**
Hardcoded rate limits are difficult to tune. Use environment variables.
### **Fix Action**
Use process.env.RATE_LIMIT or config file for limits
### **Applies To**
  - **/*.ts
  - **/*.js

## No Rate Limit Event Logging

### **Id**
rate-limit-no-logging
### **Severity**
info
### **Type**
regex
### **Pattern**
  - status\(429\)(?![\s\S]{0,500}log|console|logger)
  - rateLimit(?![\s\S]{0,800}on.*limited|onLimitReached)
### **Message**
Rate limit events should be logged for monitoring and abuse detection.
### **Fix Action**
Log rate limit events with user ID, IP, and endpoint
### **Applies To**
  - **/*.ts
  - **/*.js

## No Rate Limit Metrics

### **Id**
rate-limit-no-metrics
### **Severity**
info
### **Type**
regex
### **Pattern**
  - rateLimit(?![\s\S]{0,1000}counter|histogram|metric)
### **Message**
Rate limiting should expose metrics for monitoring.
### **Fix Action**
Add Prometheus counters for rate limit hits and blocks
### **Applies To**
  - **/*.ts
  - **/*.js

## Same Limit for All Users

### **Id**
rate-limit-single-tier
### **Severity**
info
### **Type**
regex
### **Pattern**
  - max.*[0-9]+(?![\s\S]{0,500}plan|tier|user\.)
  - points.*[0-9]+(?![\s\S]{0,500}plan|tier)
### **Message**
Consider tiered limits based on user plan (free/pro/enterprise).
### **Fix Action**
Implement per-plan limits using user.plan
### **Applies To**
  - **/*.ts
  - **/*.js

## No Bypass for Internal Services

### **Id**
rate-limit-no-bypass-internal
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.use.*rateLimit(?![\s\S]{0,800}internal|service-to-service)
### **Message**
Internal service-to-service calls may be rate limited unnecessarily.
### **Fix Action**
Add skip for internal requests with service key header
### **Applies To**
  - **/*.ts
  - **/*.js

## No Redis Error Fallback

### **Id**
rate-limit-no-redis-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - RateLimiterRedis(?![\s\S]{0,500}catch|fallback|insuranceLimiter)
### **Message**
Rate limiter should handle Redis failures gracefully.
### **Fix Action**
Add fallback limiter for Redis connection failures
### **Applies To**
  - **/*.ts
  - **/*.js

## Synchronous Rate Limit Check

### **Id**
rate-limit-sync-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - rateLimitSync|checkLimitSync
  - redis\..*Sync.*rate
### **Message**
Synchronous rate limit checks block the event loop.
### **Fix Action**
Use async rate limit checks with await
### **Applies To**
  - **/*.ts
  - **/*.js