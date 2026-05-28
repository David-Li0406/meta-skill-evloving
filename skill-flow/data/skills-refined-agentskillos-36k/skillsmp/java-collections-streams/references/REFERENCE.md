# Java Collections & Streams References

## References

- [**Stream Pipelines**](stream-pipelines.md) - Advanced stream operations, lazy evaluation, short-circuiting
- [**Collectors Patterns**](collectors-patterns.md) - Custom collectors, complex aggregations, downstream collectors

## Quick Checks

- [ ] Use List.of/Set.of/Map.of for immutable collections
- [ ] Size ArrayList/HashMap when capacity known
- [ ] Stream once - don't reuse after terminal operation
- [ ] Parallel streams only for large, CPU-bound operations
- [ ] Optional for return types, never parameters or fields
- [ ] Avoid nulls in collections - use empty collections instead
