---
name: research
description: Researches how to use an API, library, or reference architecture. Fallback when the WebSearch tool fails.
---

# Research Skill

## 1. Purpose

Use this skill to research APIs, libraries, or design patterns before implementation.
It produces concise best-practice summaries, alternatives, and tradeoffs.

## 2. Usage Scenarios

Run before:

- Using a new API or library.
- Designing an unfamiliar feature or architecture.
- Evaluating alternative implementations.

## 3. Helper Scripts

| Script                                    | Purpose                          | Quick Mode | Deep Mode |
| ----------------------------------------- | -------------------------------- | ---------- | --------- |
| `scripts/gemini_research.sh`              | General-purpose quick research.  | Default    | `--deep`  |
| `scripts/gemini_research.sh`              | Deep research via Google Gemini. | `--flash`  | Default   |

### Arguments

- Provide the **research topic** as a natural-language sentence.
- Do **not** include year numbers; the agent fetches up-to-date data.
- More context ⇒ better results.

## 4. Examples


Always start with `--flash`. If the result doesn't work or if important parts are missing, use `--deep` to get more information.

### Quick Search

```bash
gemini_research.sh --flash "Which Python HTTP client libraries support caching headers, and with which backends?"
```

### API Research

```bash
perplexity_open_router_research.sh "Write a Python best-practice manual for using the Atlassian Confluence API."
gemini_research "Same as above."
perplexity_open_router_researchi.sh --deep "Give a second opinion on the Atlassian API usage. Alternatives and tradeoffs?"
```

### Library Research

```bash
perplexity_open_router_research.sh "Best practices for using the os-lib library in Scala."
gemini_research.sh "Manual for using os-lib in Scala."
perplexity_open_router_research.sh --deep "Second opinion on using os-lib in Scala. Alternatives and tradeoffs?"
```

### Implementation Planning

```bash
perplexity_open_router_research.sh "How to parse cron expressions in Rust, using stdlib or third-party crates?"
gemini_research.sh "Manual for parsing cron expressions in Rust with the cron crate."
perplexity_open_router_research.sh --deep "Evaluate the cron crate. Alternatives and tradeoffs?"
```

## 5. Tool Modes

| Option                   | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `--flash`                | Fast, shallow lookup for immediate results.       |
| `--deep`                 | Multi-step synthesis with broader exploration.    |
| `perplexity_open_router` | Breadth-first research across multiple sources.   |
| `gemini_research`        | Depth-first synthesis for comprehensive analysis. |

## 6. Fallbacks and Error Handling

If one agent fails, retry with the alternate tool.
Ensure network access and required API keys are configured.

## 7. Output Format

- Markdown-formatted structured output
- Sections for: Overview, Best Practices, Alternatives, Tradeoffs
- Links to primary references where available

## 8. Comparison Table

| Tool       | Scope   | Depth  | Response Speed |
| ---------- | ------- | ------ | -------------- |
| Perplexity | Broad   | Medium | Fast           |
| Gemini     | Focused | Deep   | Moderate       |

## 9. Exit Codes

| Code | Meaning                   |
| ---- | ------------------------- |
| 0    | Success                   |
| 1    | Invalid arguments         |
| 2    | Network or API failure    |
| 3    | Unexpected agent response |

## 10. Environment Variables

| Variable             | Description                    |
| -------------------- | ------------------------------ |
| `OPENROUTER_API_KEY` | Required for Perplexity agent. |
| `GOOGLE_API_KEY`     | Required for Gemini agent.     |

## 11. Troubleshooting

| Problem                       | Possible Cause                    | Fix                           |
| ----------------------------- | --------------------------------- | ----------------------------- |
| `Error: No response from API` | Connectivity issue or invalid key | Check internet or credentials |
| `Output incomplete`           | Timeout or token limit            | Retry with `--deep`           |
| `Invalid topic format`        | Missing sentence structure        | Use full sentences            |

