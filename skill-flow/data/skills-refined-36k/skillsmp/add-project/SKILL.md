---
name: add-project
description: Add new GitHub projects to nibzard-web projects page. Fetches repo metadata via gh CLI, generates appropriate topics, and formats entries for src/pages/projects.astro. Use when user says "add project", "add to projects page", or mentions adding GitHub repos to the site.
allowed-tools: Bash, Read, Edit
---

# Add Project to nibzard-web

## Quick workflow

For each GitHub repo to add:

1. **Fetch metadata** using gh CLI:
   ```bash
   gh repo view OWNER/REPO --json name,description,repositoryTopics,primaryLanguage,languages,createdAt,updatedAt
   ```

2. **Fetch README** if description is empty or missing:
   ```bash
   gh api repos/OWNER/REPO/readme | jq -r '.content' | base64 -d | head -50
   ```

3. **Generate topics** if `repositoryTopics` is null:
   - Derive from: repo description, README content, primary language
   - Use 3-5 relevant lowercase tags (e.g., "ai", "database", "zig", "embedded")

4. **Read the projects file** to understand current format:
   ```bash
   src/pages/projects.astro
   ```

5. **Add the entry** to the `projects` array using this format:
   ```javascript
   {
     title: "repo-name",
     url: "https://github.com/OWNER/REPO",
     description: "Brief description from gh or README",
     topics: ["topic1", "topic2", "topic3"],
     date: "YYYY-MM-DD"  // use createdAt date
   }
   ```

6. **Insert before** the closing `].sort(...)` line

## Date format

Use `createdAt` from gh CLI, formatted as `YYYY-MM-DD` (extract from ISO date like "2026-01-12T11:00:03Z").

## Verification

After adding, run:
```bash
pnpm run build
```

## Example

```bash
# Fetch repo info
gh repo view nibzard/scribe --json name,description,repositoryTopics,primaryLanguage,languages,createdAt,updatedAt

# Result: description="Distraction-Free Writing firmware for the M5stack ESP32 based Tab5 device", createdAt="2026-01-12T11:00:03Z"

# Entry to add:
{
  title: "scribe",
  url: "https://github.com/nibzard/scribe",
  description: "Distraction-Free Writing firmware for the M5stack ESP32 based Tab5 device",
  topics: ["firmware", "embedded", "esp32", "writing", "m5stack"],
  date: "2026-01-12"
}
```

## Notes

- The array is auto-sorted by date (newest first)
- Use kebab-case for title matching repo name
- Keep descriptions under ~100 characters
- Topics should be single words or hyphenated terms
