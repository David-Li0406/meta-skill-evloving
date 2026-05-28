# Spring Data JPA References

## References

- [**Entity Mapping**](entity-mapping.md) - Inheritance strategies, embeddables, custom converters
- [**Repository Patterns**](repository-patterns.md) - Specifications, custom implementations
- [**Fetching Strategies**](fetching-strategies.md) - N+1 problem, EntityGraph, batch fetching

## Quick Checks

- [ ] Use LAZY fetch for @ManyToOne and @OneToMany
- [ ] JOIN FETCH for eager loading in queries
- [ ] @Transactional(readOnly = true) for reads
- [ ] Projections for read-only partial data
- [ ] Paginate large result sets
- [ ] Avoid open-in-view (disabled by default in Spring Boot 3)
