# Migration and Refactoring Strategies

*Practical Guides for Legacy Code Transformation*

## 1. The Strangler Fig Pattern
Incrementally replacing functionality by creating a new system around the edges of the old one.

## 2. Refactoring to Clean Architecture
1. **Identify the Core**: Move pure business logic into `domain/entities`.
2. **Abstract Data Access**: Create interfaces (Ports) for existing database calls.
3. **Isolate External Services**: Move API clients to `infrastructure/gateways`.
4. **Orchestrate with Use Cases**: Create the application layer.

## 3. Breaking the Monolith
- Identify **Bounded Contexts**.
- Use **Context Mapping** to define how they interact.
- Implement asynchronous communication (Events) between contexts.
