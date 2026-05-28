# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Quota exceeded` | Unexpected traffic spike | Implement emergency rate limits |
| `Critical errors filtered` | Over-aggressive filtering | Whitelist critical error types |
| `Billing surprise` | No spend alerts | Configure spend notifications |
| `Data missing for debugging` | Sampling too aggressive | Increase rate for critical paths |