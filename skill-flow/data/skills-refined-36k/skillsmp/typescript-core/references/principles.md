# Core Principles

## General Rules

- TypeScript only (strict mode on)
- Follow the [naming conventions](naming.md)
- All code must have zero linter, formatter, and type checker errors or warnings
- Before writing a custom hook check [usehooks](https://github.com/uidotdev/usehooks)
- Always use the most recent version of all dependencies
- Always use pnpm

## Simplicity & Pragmatism (KISS + YAGNI)

Do the simplest thing that works today. Avoid speculative architecture.

- No "in case we need it later" hooks, contexts, caching layers, or utilities
- If a component's responsibility fits in a sentence, it's scoped correctly
- Dependencies must **earn their place**

> Perfect architecture that ships nothing is worse than imperfect UI that works.

## User Experience First

UI should be obvious, predictable, and kind.

- Errors must be understandable and actionable
- Async UX must always handle loading, error, empty, and success
- Don't force users to infer intent — show what's happening and why

> You are designing for someone under pressure. Help them.

## Make It Work, Then Make It Fast

Correctness and clarity come before optimization.

- Only optimize when measurement proves a bottleneck
- Memoization should prevent real cost, not theoretical cost
- UI should be correct first, then efficient

> Fast wrong UI is worse than slow correct UI.

## Build for Joy, Not Scale

The codebase should feel pleasant and obvious to work in.

- Names should read like clear English
- Components should be predictable and composable
- Delight comes from clarity, not clever code

> The best frontend feels like a well-made tool: effortless, reliable, enjoyable.

## Final Directive

When in doubt, choose the path that:

1. Keeps the UI simple and obvious
2. Feels predictable and enjoyable to work on
3. Avoids abstractions until they are proven necessary
4. Uses composition over configuration
5. Favors clarity and real-world UX over clever code

**If something hurts: simplify it, don't complicate it.**
