---
name: gemini_search
description: Perform a web search using the Gemini CLI to retrieve up-to-date information, facts, or documentation not in your training data.
allowed-tools:
  - Bash
---

# Gemini Search Skill

This skill allows you to perform web searches using the Gemini CLI. Use this when you need current information that is likely not in your training data, such as recent news, latest library documentation, or specific facts.

## Usage

To perform a search, use the `Bash` tool to execute the `gemini` command with your search query as a quoted string.

```bash
gemini "your search query here"
```

## Prompting Advice

To get the best results from the Gemini CLI, structuring your query effectively is key:

*   **Context is King:** Instead of vague terms, include specific keywords, error messages, or library names.
    *   *Bad:* `gemini "python error"`
    *   *Good:* `gemini "python TypeError: list indices must be integers or slices, not str"`
*   **Be Specific:** Specify the technology stack, version, or environment if relevant.
    *   *Good:* `gemini "react 18 useEffect hook example"`
*   **Ask for Code:** If you need code, explicitly ask for examples or snippets.
    *   *Good:* `gemini "write a bash script to backup postgres database"`
*   **English is Preferred:** For technical topics, queries in English often yield better and more up-to-date results.

## Guidelines

1.  **Specific Queries:** Formulate specific and keyword-rich queries to get the best results.
2.  **Analyze Output:** The Gemini CLI will return a summary or list of search results. Read this output carefully to answer the user's question.
3.  **No Hallucination:** If the search results do not contain the answer, state that you could not find the information rather than making it up.
