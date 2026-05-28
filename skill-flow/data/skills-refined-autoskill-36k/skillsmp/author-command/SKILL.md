---
name: author-command
description: "Auhors a brand new OpenCode command following project best practices and conventions. Trigger on user queries such as: 'Create a new command to <do something>', 'Author a command that <does something>', 'I need a command that <does something>'."
---

# Author Command

## Overview

You are authoring a new OpenCode command that implements a specific functionality as requested by the user. You will ensure that the command follows project best practices and conventions, and that it is well-documented and tested.

## When To Use

- User requests the creation of a new command (e.g., "Create a new command to <do something>", "Author a command that <does something>", "I need a command that <does something>").

## Behavior

1. Review command authoring documentation at https://opencode.ai/docs/commands
2. Review example commands at https://claude.ai/public/artifacts/e2725e41-cca5-48e5-9c15-6eab92012e75
3. Gather requirements from the user about the desired command functionality, inputs, outputs, and any specific constraints or considerations.
4. Draft the command code in markdown format, ensuring it adheres to project coding standards and conventions. Use the format in the examples at in https://claude.ai/public/artifacts/e2725e41-cca5-48e5-9c15-6eab92012e75 
5. Review the command markdown with the user for feedback and make necessary revisions. Do not proceed until the user approves the draft.
6. Once approved, finalize the command markdown and place in the `.opencode/commands` directory
7. Document the command in the README.md file and any other relevant documentation.