# no-rot

A skill that prevents brain atrophy from LLM over-reliance by leaving engaging challenges for you to complete.

## The Problem

> "I'm seeing teams nerf their own ability to use their brains because of LLM dependence, and when they run into a problem the LLM can't fix they start doing really weird stuff"

When AI does everything, your problem-solving muscles atrophy. This skill keeps you sharp by intentionally leaving satisfying challenges for you to solve.

## Installation

```bash
npx skills add https://github.com/ameistad/agent-skills --skill no-rot
```

## Usage

Activate the skill by telling your AI agent:
- "Keep me sharp"
- "Challenge me"
- "Don't let me rot"
- "I want to learn while building"

The agent will complete tedious parts (boilerplate, setup, config) while leaving engaging puzzles for you:
- Implementing small algorithms
- Extending patterns to new cases
- Writing clever optimizations
- Designing interfaces

## Example

You ask: "Add rate limiting to this API endpoint"

The agent might:
1. Set up the middleware structure
2. Add the storage mechanism
3. Leave the core logic as a challenge:

> **Challenge:** Implement the `isRateLimited(ip)` function that returns true if the IP has exceeded 100 requests in the last minute.
>
> **Context:** The `requestLog` Map stores arrays of timestamps per IP.

## Philosophy

Good challenges have:
- A clear goal
- Bounded scope
- That satisfying "click" when solved

Bad challenges are:
- Open-ended debugging
- Tedious boilerplate
- Tasks requiring context you don't have

## License

MIT
