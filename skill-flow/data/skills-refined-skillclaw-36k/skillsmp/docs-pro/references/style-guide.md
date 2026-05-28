# 2026 Documentation Style Guide

A comprehensive guide for maintaining clarity, consistency, and professional tone in Squaads AI documentation.

## 1. Voice and Tone

-   **Active Voice**: Always prefer active voice. 
    -   *Bad*: "The function is called by the agent."
    -   *Good*: "The agent calls the function."
-   **Direct and Concise**: Avoid fluff. Start with the most important information.
-   **Inclusive Language**: Use gender-neutral pronouns (they/them) or avoid pronouns entirely. Use "users" or "developers" instead of "the user."
-   **Professional but Accessible**: Use simple words for complex concepts. Avoid obscure jargon unless defined.

## 2. Structural Standards

-   **The Rule of Three**: Limit heading hierarchies to H1, H2, and H3. If you need H4, consider splitting the page.
-   **TL;DR / Executive Summary**: Every page longer than 500 words must start with a brief summary or table of contents.
-   **Contextual Links**: Use descriptive link text.
    -   *Bad*: "Click [here](...) to read more."
    -   *Good*: "See the [Authentication Guide](...) for more details."

## 3. Formatting Rules

-   **Line Length**: Aim for ~100 characters per line in raw Markdown for easier Git diffs.
-   **Code Blocks**: Always specify the language (e.g., ` ```typescript `). Use meaningful variable names in examples.
-   **Bold and Italics**: Use bold for UI elements (e.g., "Click **Submit**") and italics for technical terms on their first use.
-   **Lists**: Use bulleted lists for unordered items and numbered lists for sequential steps.

## 4. Error Message Guidelines (2026)

Error messages in docs should be modeled as "Problem, Cause, Solution."

-   **Problem**: What happened? (e.g., "401 Unauthorized")
-   **Cause**: Why did it happen? (e.g., "Invalid API Key")
-   **Solution**: How to fix it? (e.g., "Check your .env file for AUTH_SECRET")

## 5. UI/UX for Docs

-   **Navigation**: Ensure the `mkdocs.yml` or navigation structure is logical and mirrors the user's journey.
-   **Admonitions**: Use "Note," "Warning," and "Tip" boxes sparingly to highlight critical info.
-   **Screenshots/Diagrams**: All images must have descriptive `alt` text and be kept in an `assets/` folder.

---
*Updated: January 22, 2026 - 17:00*
