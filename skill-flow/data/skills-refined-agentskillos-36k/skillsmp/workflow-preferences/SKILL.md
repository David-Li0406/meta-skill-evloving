---
name: Workflow Preferences
description: Essential rules and preferences for the agent's workflow and behavior.
---

# Workflow Preferences

## Server Execution & Browser Testing

- **NEVER** automatically run the web server (`npm run dev`, etc.) or check the application using the browser tool unless explicitly instructed by the user.
- The user prefers to handle the running of the application and verification manually.

## Linting and Formatting

- **ALWAYS** run `npm run lint` after code changes and make sure linter is passing.
