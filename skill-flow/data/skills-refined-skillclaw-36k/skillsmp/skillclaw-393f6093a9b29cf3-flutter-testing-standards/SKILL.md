---
name: flutter-testing-standards
description: Use this skill when you need to implement unit, widget, and integration testing in Flutter applications using mocktail and bloc_test.
---

# Testing Standards

## **Priority: P1 (HIGH)**

Ensuring code reliability through multi-layered testing strategies.

## Structure

```text
test/
├── unit/ # Business logic & mapping (Blocs, Repositories, UseCases)
├── widget/ # UI component behavior (Screens, Widgets)
└── integration/ # End-to-end flows
```

## Implementation Guidelines

- **Testing Pyramid**: Maintain ~70% Unit Tests, ~20% Widget Tests, ~10% Integration Tests.
- **Mocks**: Use `mocktail` for type-safe, boilerplate-free mocking.
- **Unit Tests**: Test logic in isolation. Verify all edge cases (Success, Failure, Exception).
- **Widget Tests**: Test high-value interactions (Button clicks, Error states, Loading indicators).
- **BLoC Tests**: Use `blocTest` to verify state emission sequences.
- **Code Coverage**: Aim for 80%+ coverage on Domain and Presentation (Logic) layers.

## 🚫 Anti-Patterns

- **Thread Sleep**: Avoid using `Future.delayed`; instead, use FakeAsync or expectations for deterministic timing.
- **Missing Assertions**: Ensure every test includes an `expect()` call; tests without assertions are invalid.
- **Over-Mocking**: Use real instances for Entities/Models; mock only I/O.
- **Test Pollution**: Ensure every test is independent and does not share state.

## Related Topics

layer-based-clean-architecture | dependency-injection | cicd