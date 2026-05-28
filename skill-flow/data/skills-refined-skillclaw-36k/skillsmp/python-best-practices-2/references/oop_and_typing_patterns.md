# OOP + typing patterns (recommended)

## Prefer composition
- Inject clients/services into constructors or functions.
- Keep wiring in a composition root.

## Data models
- Use @dataclass for data carriers.
- Avoid mutable defaults; use default_factory.
- Consider frozen models when invariants matter.

## Interfaces
- Prefer Protocol for structural typing.
- Use ABC only when runtime enforcement is required.

## Avoid Singleton
- Use DI (pass dependencies explicitly).
- Use module constants only for immutable configuration.
