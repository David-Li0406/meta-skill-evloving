---
name: API Integration Builder
description: Create new API service integrations for Leavn - REST clients, CloudKit, Bible APIs with proper error handling and caching
allowed-tools: Read, Write, Edit
---

# API Integration Builder

Build API service integrations:

1. **Create protocol** in `Services/{Domain}/`
2. **Implement client**: Async/await, proper errors
3. **Add caching**: CacheManager integration
4. **Register in DI**: DIContainer singleton
5. **Add tests**: Mock for testing

Pattern:
```swift
protocol MyAPIProtocol {
    func fetch() async throws -> Data
}

final class MyAPILive: MyAPIProtocol {
    func fetch() async throws -> Data {
        // URLSession, error handling, caching
    }
}
```

Use when: Adding Bible translation API, CloudKit integration, external service
