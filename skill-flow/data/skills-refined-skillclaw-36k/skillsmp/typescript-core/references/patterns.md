# Component & Code Patterns

## One Module, One Responsibility

Each module (or component, for front-end) should have a single well-defined responsibility. If you find “and” in the description of a module’s purpose, it likely should be split.

- **Cohesion**: Group related functionality and separate unrelated. For example, a UserProfile component displays user info, and a separate UserProfileLoader handles data fetching.
- **No God Objects**: Avoid huge classes or modules that do everything. Break them into smaller pieces (utilities, helpers, sub-components) that are easier to test and maintain.

## Composition Over Inheritance

Favor composing functionality by combining small functions/objects over class inheritance.

- Use functional composition or higher-order functions to extend behavior.
- In React, prefer composition via children or hooks rather than deep prop drilling or inheritance.
- Only use classes/inheritance in TypeScript if there is a clear “is-a” relationship and polymorphic behavior needed. Even then, consider interfaces and composition first.

## Composition Over Configuration

When designing components or modules, allow composition instead of endless configuration flags.

- Instead of a single complex function with many boolean flags or options, provide smaller composable functions.
- For React: rather than a prop to conditionally show/hide part of component, consider letting callers pass children or supply a render prop for flexible composition.
- In APIs: prefer allowing the caller to pass in strategy objects or callbacks (composition) rather than adding more parameters for every variation.

**Example**: Instead of a Table component with a prop for `sortable` and `filterable`, provide composable higher-order components or hooks to enhance a basic Table with sorting or filtering.

## Immutability and Pure Functions

Adopt a functional mindset for business logic:

- Use pure functions (no side effects, return value only depends on input parameters) for core computations. They are easier to test and reuse.
- Avoid mutating inputs; instead return new values. If using libraries like Immer or seamless-immutable, ensure team is aligned.
- Keep side effects (I/O, state mutations) at the edges (in Effect pipelines, in React effects, or specific service classes). This is akin to the "functional core, imperative shell" pattern.

## Railway-Oriented Flow for Errors

Use a consistent pattern for error propagation:

- If using Effect, chain computations with `Effect.flatMap`/`andThen` and handle failures with `catch` combinators. This prevents throwing exceptions and instead returns a predictable error container[1][2].
- If not using Effect, use `Result`/`Either` monads (like True Myth’s Result or neverthrow) to return errors instead of throwing. This allows composing functions without `try/catch` and clearly signals which functions can fail.
- Structure code so that errors flow through the system in a controlled way (e.g. at a high level you might log and present an error message, but deeper functions just return errors up the call chain).

## Pattern Matching for Clarity

Leverage pattern matching techniques to handle union types clearly (with libraries like `ts-pattern` if needed).

- Rather than many `if/else` or `switch` statements checking types/tags, a pattern matching utility can make code more declarative and ensure all cases are handled (exhaustive checking).
- This is particularly useful for complex discriminated unions or `Result` handling (Ok vs Err): a pattern match can handle each variant in one expression, making the code more readable.

**Example using ts-pattern**:

```ts
import { match } from 'ts-pattern';
match(result)
  .with({ status: 'ok', value: P.select() }, value => { /* handle success */ })
  .with({ status: 'error', error: P.select() }, err => { /* handle error */ })
  .exhaustive();
```

This ensures both `Ok` and `Error` cases are covered, and if a new variant is added to `result`, TypeScript will flag the pattern match as incomplete[3].

## Reactive & Concurrency Patterns

When dealing with concurrency (especially on backend or with asynchronous tasks):

- Use Effect fibers to handle concurrency with safety (e.g., `Effect.race` for racing tasks, `Effect.forEach` with a concurrency limit to process collections in parallel).
- Avoid manual `Promise.then` chaining – prefer `async/await` or `Effect.gen` for sequential logic; it’s easier to read.
- Avoid deeply nested callbacks or promise chains (callback hell). Use abstraction (helper functions or Effect pipeline) to linearize the flow.

## Clean Error Handling Pattern

Design functions to either return a `Result`/`Either` or to throw exceptions in a controlled manner at boundaries (not both). Our preference is returning structured results:

- For example, use `Result<SuccessType, ErrorType>` for a function that could fail, and document that it never throws.
- At high-level boundary (like an Express route or a CLI command handler), convert these to user-facing messages or throw if it will be caught by a global handler.
- This pattern, combined with pattern matching, leads to robust error management where nothing gets swallowed silently.

## Plugin/Hook Architecture for Extensibility

When building a system that might need extension (like a CLI with plugins, or an app that runs user-defined modules), design with hooks or plugin points:

- Define interfaces or callback signatures for the extension points.
- Use dependency injection or event emitters to decouple core logic from extensions.
- Ensure that the plugin interface is stable and clearly documented, as changes will propagate to all implementations.

Keep the core minimal and let plugins add optional features, keeping them isolated.
