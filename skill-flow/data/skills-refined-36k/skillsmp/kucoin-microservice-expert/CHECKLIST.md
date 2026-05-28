# KuCoin Change Validation Checklist

Use this checklist to validate any changes to the KuCoin integration.

## Pre-Change Verification

- [ ] Read the current implementation in relevant files
- [ ] Checked git history for recent changes to affected code
- [ ] Verified understanding matches KuCoin official documentation
- [ ] Identified all files that will be affected

## Code Quality

### Authentication & Security
- [ ] API credentials never logged or exposed
- [ ] Signature generation uses correct algorithm (HMAC-SHA256)
- [ ] Timestamp within acceptable drift window
- [ ] Passphrase properly encrypted (API v2)

### Order Handling
- [ ] `clientOid` used for idempotency
- [ ] Quantity rounded to lot size precision
- [ ] Price rounded to tick size precision
- [ ] Order status properly reconciled
- [ ] Partial fills handled correctly

### Financial Calculations
- [ ] All money values use `Decimal.js`
- [ ] No floating-point arithmetic for prices/amounts
- [ ] Fee calculations include all components
- [ ] Net vs gross amounts clearly distinguished

### Rate Limiting
- [ ] Requests go through `EnhancedKuCoinApiClient`
- [ ] Not bypassing rate limit manager
- [ ] Proper priority assigned to requests
- [ ] Backoff logic includes jitter

### Error Handling
- [ ] Network errors caught and logged
- [ ] Rate limit errors trigger backoff
- [ ] Invalid signature errors logged with context (not credentials)
- [ ] Retry logic has max attempts limit

### WebSocket (if applicable)
- [ ] Reconnection logic tested
- [ ] Heartbeat/ping mechanism works
- [ ] Subscription state restored after reconnect
- [ ] Message queue handles backpressure

## Testing Requirements

### Unit Tests
- [ ] New functions have unit tests
- [ ] Edge cases covered (empty, null, invalid)
- [ ] Mocked KuCoin responses match actual API format
- [ ] Error scenarios tested

### Integration Tests
- [ ] Dry run test passes (`npm run test:strategy-rebalance:dry`)
- [ ] Sandbox environment tested (if available)
- [ ] Rate limiting behavior verified
- [ ] WebSocket reconnection tested

### Manual Verification
- [ ] Checked logs for expected output
- [ ] Verified metrics are being recorded
- [ ] Tested with small amounts first

## Deployment Checklist

### Before Deploy
- [ ] All tests passing (`npm test`)
- [ ] Build succeeds (`npm run build`)
- [ ] No TypeScript errors
- [ ] Environment variables documented

### After Deploy
- [ ] Verify service starts without errors
- [ ] Check health endpoint responds
- [ ] Monitor rate limit usage
- [ ] Watch for authentication errors
- [ ] Verify orders execute correctly

## Specific Scenarios to Test

### Order Execution
| Scenario | Expected Behavior |
|----------|-------------------|
| Market buy order | Executes immediately, fills at market price |
| Market sell order | Executes immediately, fills at market price |
| Limit order | Placed on book, may partially fill |
| Cancel order | Order removed from book |
| Insufficient balance | Error returned, no order placed |
| Invalid symbol | Error returned, clear message |

### Rate Limiting
| Scenario | Expected Behavior |
|----------|-------------------|
| Normal load | Requests processed immediately |
| High load | Requests queued by priority |
| Rate limit hit | Backoff with jitter, retry |
| Circuit breaker open | Fail fast, wait for recovery |

### WebSocket
| Scenario | Expected Behavior |
|----------|-------------------|
| Initial connection | Subscribes to required channels |
| Message received | Data cached and processed |
| Connection dropped | Auto-reconnect with backoff |
| Invalid message | Logged and skipped |

### Time Synchronization
| Scenario | Expected Behavior |
|----------|-------------------|
| Cached timestamp valid | Use cached value |
| Cache expired | Fetch new timestamp |
| Server unreachable | Use fallback with safety buffer |
| Large drift detected | Log warning, adjust |

## Logs & Metrics to Monitor

### Key Log Patterns
```
# Successful order
[KuCoin] Order placed: orderId=xxx symbol=BTC-USDT

# Rate limit warning
[RateLimit] Approaching limit: 3800/4000

# WebSocket events
[WS] Connected to private channel
[WS] Reconnecting... attempt 2

# Errors to watch
[KuCoin] Error 400500: Invalid signature
[KuCoin] Error 429000: Rate limit exceeded
```

### Metrics to Track
- Request count per endpoint
- Average latency
- Error rate by error code
- Rate limit headroom
- WebSocket reconnection count
- Order fill rate

## Documentation Updates

After making changes, update if applicable:
- [ ] `README.md` - If API changes
- [ ] `API_DOCUMENTATION.md` - If endpoints change
- [ ] `TRADING_FLOW_GUIDE.md` - If flow changes
- [ ] `src/services/kucoinApi/README.md` - If client changes
- [ ] `CLAUDE.md` - If significant patterns change
