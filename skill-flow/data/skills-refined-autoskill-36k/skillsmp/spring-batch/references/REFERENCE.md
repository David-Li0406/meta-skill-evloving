# Spring Batch References

## References

- [**Chunk Processing**](chunk-processing.md) - Chunk sizing, transaction boundaries, skip/retry

## Quick Checks

- [ ] Use JobBuilder/StepBuilder (not deprecated *BuilderFactory)
- [ ] Set appropriate chunk size (100-1000)
- [ ] Configure skip/retry for fault tolerance
- [ ] Use RunIdIncrementer for re-runnable jobs
