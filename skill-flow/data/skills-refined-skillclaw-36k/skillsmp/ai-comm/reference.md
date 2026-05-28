# ai-comm Command Reference

## Supported AI CLIs

claude, codex, gemini, aider, cursor, opencode

## list-ai-windows

List Kitty windows running AI CLIs.

```bash
ai-comm list-ai-windows [--json]
```

Output columns: ID (window ID for -w option), CLI (detected AI type), TITLE, CWD.

Example output:

```bash
  ID  CLI         TITLE                           CWD
   5  claude      Reviewing authentication        /home/user/project
   8  aider       Refactoring database layer      /home/user/project
```

## send

Send message to AI window and wait for response.

```bash
ai-comm send MESSAGE --window ID [--raw] [--json]
```

| Option         | Description                                         |
| -------------- | --------------------------------------------------- |
| `--window, -w` | Target window ID (required)                         |
| `--raw`        | Return raw terminal text instead of parsed response |
| `--json`       | Output as JSON                                      |

The message is automatically wrapped with sender metadata. For Aider, /ask is
prepended to prevent automatic file edits.

## get-response

Get parsed response from an AI window. Use after sending with --no-wait.

```bash
ai-comm get-response --window ID [--json]
```

| Option         | Description                 |
| -------------- | --------------------------- |
| `--window, -w` | Target window ID (required) |
| `--json`       | Output as JSON              |
