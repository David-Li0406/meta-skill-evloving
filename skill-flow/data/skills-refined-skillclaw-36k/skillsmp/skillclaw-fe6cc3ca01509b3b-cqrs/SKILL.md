---
name: cqrs
description: Use this skill when implementing Command Query Responsibility Segregation (CQRS) patterns in Domain-Driven Design (DDD).
---

# Skill body

This skill provides guidelines and best practices for implementing CQRS. 

1. **Understand CQRS**: Recognize that CQRS separates the handling of commands (writes) from queries (reads) to optimize performance and scalability.
2. **Define Commands and Queries**: Clearly define the commands that change state and the queries that retrieve data.
3. **Implement Separate Models**: Use different models for reading and writing data to ensure that each can be optimized independently.
4. **Use Event Sourcing (Optional)**: Consider using event sourcing to capture state changes as a sequence of events, which can be useful in conjunction with CQRS.
5. **Test and Iterate**: Continuously test your implementation and iterate based on performance and scalability needs.

For detailed documentation, refer to the appropriate resources on CQRS.