# CLI / Tooling Layout

Use this for operator tools, admin commands, local runners, and one-off utilities that still need domain correctness.

## Additions to base layout

```text
cmd/
  <service>-cli/
    main.go
internal/
  interface/cli/
    commands/            # Subcommands; argument parsing; output formatting
  bootstrap/
    cli.go               # Construct command tree; inject ports
```

## Guidance

- Keep “business work” in `app`/`domain` and let the CLI be a thin adapter.
- Prefer deterministic output (machine-readable) for automation-friendly tools.
