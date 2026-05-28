# Lint verification

Use verification only when requested.
Provide commands without installing or configuring tools automatically.

## Minimal cross-platform command

Prefer quoting glob arguments and use `#` for negated patterns.

```text
markdownlint-cli2 "**/*.md" "#node_modules"
```

## Wrapper script

If this skill repository is available locally, run the bundled script:

```text
scripts/markdownlint-cli2.sh "**/*.md" "#node_modules"
```

## Use npx when Node.js is available

If `markdownlint-cli2` is not installed but Node.js is available, run:

```text
npx markdownlint-cli2 "**/*.md" "#node_modules"
```

## Do not apply fixes without permission

Only run `markdownlint-cli2 --fix` when the user explicitly requests automatic
edits to files.
