# Agent Invocation

## Alice (Claude CLI)

Write prompt to temp file, then invoke:

```
Task tool:
  subagent_type: general-purpose
  description: "Alice reviews work"
  prompt: |
    You are Alice. Run this command:

    claude -p "$(cat {alice_prompt_file})" --allowedTools "Bash,Glob,Grep,Read,Task" 2>&1

    Return output verbatim. If command fails, report failure immediately.
```

## Bob (Codex)

Write prompt to temp file, then invoke:

```
Task tool:
  subagent_type: general-purpose
  description: "Bob reviews work"
  prompt: |
    You are Bob. Run this command:

    ~/.claude/skills/use-codex/scripts/codex-run.sh -f "{bob_prompt_file}"

    Return output verbatim. If command fails, report failure immediately.
```

## Carl (Gemini)

Write prompt to temp file, then invoke:

```
Task tool:
  subagent_type: general-purpose
  description: "Carl reviews work"
  prompt: |
    You are Carl. Run this command:

    ~/.claude/skills/use-gemini/scripts/gemini-run.sh -f "{carl_prompt_file}"

    Return output verbatim. If command fails, report failure immediately.
```
