---
name: broadcast
description: Add a feature notification to announce new features, improvements, or bug fixes to users. Use when the user wants to broadcast a change, add a notification, or announce a new feature after completing work on a PR.
---

# Broadcast Feature Notification

Add a notification that appears in the "What's New" bell icon for all users.

## Process

### Step 1: Analyze PR Changes

Run these commands to understand the changes:
```bash
git diff main...HEAD
gh pr view --json title,body,number
```

### Step 2: Determine Notification Type

Based on changes, classify as one of:
- `Feature` - New functionality added
- `Improvement` - Enhancement to existing functionality
- `BugFix` - Bug or issue fixed

### Step 3: Create EF Core Migration

Create two files in `src/PraxisNote.Infrastructure/Migrations/Data/FeatureNotifications/`:

> **Note**: The `Data/` subfolder separates data migrations from structural schema migrations.

**Naming**: `YYYYMMDDHHMMSS_AddNotification{PascalCaseTitle}.cs`

Use current UTC timestamp (e.g., `20260117120000` for Jan 17, 2026 12:00:00 UTC).

**Migration file** (`YYYYMMDDHHMMSS_AddNotification{Title}.cs`):
```csharp
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PraxisNote.Infrastructure.Migrations.Data.FeatureNotifications
{
    public partial class AddNotification{PascalCaseTitle} : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql("""
                INSERT INTO "FeatureNotifications" ("Type", "Title", "Summary", "IssueUrl", "CreatedAt")
                VALUES (
                    '{Type}',
                    '{Title}',
                    '{Summary}',
                    'https://github.com/garethbaumgart/praxis-note/pull/{PRNumber}',
                    '{ISO8601Timestamp}'
                );
                """);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql("""
                DELETE FROM "FeatureNotifications"
                WHERE "Title" = '{Title}';
                """);
        }
    }
}
```

**Designer file** (`YYYYMMDDHHMMSS_AddNotification{Title}.Designer.cs`):
- Copy from the most recent migration's Designer.cs in the parent Migrations folder
- Update the `[Migration("...")]` attribute to match your new migration name
- Update the `partial class` name to match
- Update the `namespace` to `PraxisNote.Infrastructure.Migrations.Data.FeatureNotifications`

### Step 4: Build and Restart

```bash
# Build to verify migration compiles
cd src && dotnet build

# Restart API to trigger migration
docker restart praxisnote-api-dev
```

### Step 5: Verify

```bash
# Check migration was applied
docker exec praxisnote-db-dev psql -U praxisnote -d praxisnote -c \
  "SELECT \"Id\", \"Title\" FROM \"FeatureNotifications\" ORDER BY \"Id\" DESC LIMIT 3;"
```

## Writing Guidelines

**Title**:
- Short, action-oriented (max 50 chars)
- Examples: "Task search and filtering", "Faster task archiving", "Equal column heights"

**Summary**:
- One sentence describing the user benefit (max 200 chars)
- Focus on what users can now DO, not technical details
- Examples:
  - "Sort tasks within each column by date created, due date, or priority."
  - "Kanban columns now maintain equal heights on desktop for a cleaner layout."

## When to Skip

Do NOT create a notification for:
- Internal refactoring with no user-visible changes
- Test-only changes
- Documentation-only changes
- CI/workflow changes
- Dependency updates (unless they fix a user-facing issue)
