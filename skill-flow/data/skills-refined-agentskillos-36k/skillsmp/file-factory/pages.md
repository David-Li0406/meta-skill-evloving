# Create Next.js pages

```bash
# Pages Router (current squareone setup)
pnpm file-factory page dashboard --package squareone
pnpm file-factory page dashboard/settings --package squareone

# App Router (for future migration)
pnpm file-factory page dashboard --router app --package squareone
```

## Command options

| Option                 | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `--router <type>`      | Router type: `app` or `pages`                     |
| `-p, --package <name>` | Target package (e.g., `squared`, `squareone`)     |
| `--dry-run`            | Show what would be created without writing files  |
| `-v, --verbose`        | Verbose output                                    |

## File structures

**Pages Router structure:**

```
src/pages/dashboard/settings.tsx
```

**App Router structure:**

```
src/app/dashboard/settings/page.tsx
```
