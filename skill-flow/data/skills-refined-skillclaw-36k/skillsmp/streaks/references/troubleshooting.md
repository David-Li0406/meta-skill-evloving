# Troubleshooting

## Streaks app not found

- Ensure Streaks is installed in `/Applications/Streaks.app`.
- Re-run: `st discover`.

## Streaks shortcut missing

- Create the corresponding shortcut in Shortcuts.
- Re-run: `st doctor`.
- Run a specific shortcut by name: `st <action> --shortcut "Name"`.
- Map custom names once: `st link task-list --shortcut "My Tasks"`.

## Permission prompts

- Approve automation prompts for Shortcuts and Streaks on first run.

## Discover fails after update

- Re-run discovery and review unmapped keys.
- Update action matching if new Streaks actions appear.

## JSON output not structured

- Shortcuts may return plain text by default.
- Return a Dictionary from the shortcut for structured output.
- Use `--shortcuts-output public.json` and/or `--agent` for stable wrappers.

## Homebrew install issues

- Ensure tap exists: `brew tap vburojevic/tap`.
- Update: `brew update` then `brew upgrade streaks-cli`.
