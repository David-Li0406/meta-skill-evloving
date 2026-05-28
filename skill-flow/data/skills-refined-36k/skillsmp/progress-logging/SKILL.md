---
name: progress-logging
description: Record session progress to progress.md with date-stamped entries (YYYY-MM-DD format) containing 1-3 sentence summaries. Focuses on outcomes not process, using action verbs like Created, Implemented, Fixed, Refactored. Use automatically after completing tasks, feature implementations, bug fixes, or when user requests logging. Provides guidelines for writing concise summaries that mention specific technologies and components.
---

# Progress Logging

Maintain a chronological log of AI-assisted work sessions in `progress.md`.

## When to Use

**Use this skill:**
- After completing a task or set of related tasks
- At the end of a work session
- When wrapping up feature implementation
- After fixing bugs or addressing issues

**Automatically invoke when:**
- User says "log this" or "record progress"
- Completing a significant milestone
- Finishing implementation work
- User requests session summary

## Log Format

Each entry is a single line with:
- **Date:** YYYY-MM-DD format
- **Description:** 1-3 sentence summary of what was accomplished

**Example:**
```
2025-11-17  Created four Claude Skills for web design, fullstack structure, database setup, and NeonStack architecture. Added utilities.css reference file to web-design-style skill.
2025-11-16  Implemented authentication system with JWT tokens and user session management. Fixed CORS issues in API endpoints.
2025-11-15  Refactored database agent pattern, moved query logic out of routers into dedicated agent classes.
```

## Step-by-Step Process

### 1. Review Context

Look at your entire conversation context and identify:
- What features were implemented?
- What bugs were fixed?
- What files were created or modified?
- What problems were solved?

### 2. Summarize Concisely

Create a 1-3 sentence summary that:
- **Starts with action verbs** (Created, Implemented, Fixed, Refactored, Added, etc.)
- **Focuses on outcomes**, not process
- **Mentions key components** changed
- **Is specific** but not overly detailed

**Good examples:**
```
Created PostgreSQL Docker setup script and environment configuration for local development. Implemented database agent pattern with session management.

Built NeonStack authentication flow with Stack Auth and PostgREST Data API. Added RLS policies for user data isolation.

Refactored CSS to use utilities.css system. Removed all inline styles and converted to utility classes with BEM components.
```

**Bad examples (too vague):**
```
Worked on database stuff.
Made some changes to the frontend.
Fixed issues.
```

**Bad examples (too detailed):**
```
Created setup_postgres.sh script that stops and removes existing containers using docker stop and docker rm commands, then starts a new PostgreSQL 16 Alpine container with environment variables for user, password, and database, mounting a volume for data persistence, and exposing port 5432.
```

### 3. Write to Log File

**IMPORTANT:** Write to `progress.md` in the **workspace root**, NOT inside individual repos.
- Workspace root example: `/home/nsheff/Dropbox/workspaces/refgenie/progress.md`
- NOT repo root: `/home/nsheff/Dropbox/workspaces/refgenie/repos/gtars/progress.md` ❌

Check if `progress.md` exists in workspace root:
- **If exists:** Append new entry at the end
- **If not exists:** Create file with header and first entry

**File structure:**
```markdown
# Progress Log

Record of AI-assisted development sessions.

2025-11-17  First session summary here.
2025-11-17  Second session if multiple entries same day.
2025-11-16  Previous day's work here.
```

### 4. Confirm to User

After writing, briefly confirm what was logged:
```
Logged to progress.md: "Created four Claude Skills for web design, fullstack structure, database setup, and NeonStack architecture."
```

## Writing Guidelines

### Action Verbs to Use

- **Created** - New files, features, components
- **Implemented** - Functionality, systems, patterns
- **Fixed** - Bugs, errors, issues
- **Refactored** - Code improvements, restructuring
- **Added** - New capabilities to existing features
- **Updated** - Modifications to existing code
- **Configured** - Setup, environment, tools
- **Built** - Complex features or systems
- **Optimized** - Performance improvements
- **Integrated** - Connected systems or services

### What to Include

**Do mention:**
- Specific features or components
- Technologies used (PostgreSQL, Stack Auth, React, etc.)
- Architectural patterns (database agents, service layer, RLS)
- File types created (skills, scripts, configs)
- Problems solved (CORS issues, auth errors, etc.)

**Don't mention:**
- Step-by-step process details
- Tool names (Bash, Edit, Write, etc.)
- Internal implementation minutiae
- Temporary debugging steps

### Combining Multiple Activities

If session included several tasks, group related items:

**Instead of:**
```
Created setup_postgres.sh. Created config.py. Created database.py. Added lifespan handler.
```

**Write:**
```
Set up PostgreSQL Docker environment with configuration management, database connection pooling, and automatic table creation on startup.
```

## Common Patterns

### Feature Implementation
```
2025-11-17  Implemented citation management system with CRUD operations, BibTeX parsing, and PostgreSQL storage using database agent pattern.
```

### Bug Fixes
```
2025-11-17  Fixed authentication token refresh issues and CORS errors in Data API client. Added proper error handling for network failures.
```

### Refactoring
```
2025-11-17  Refactored styling system to use utilities.css throughout application. Removed Tailwind dependency and converted all components to BEM naming.
```

### Documentation/Setup
```
2025-11-17  Created comprehensive Rust port plan for peppy library with 7 implementation phases and detailed architecture design.
```

### Multiple Related Tasks
```
2025-11-17  Built complete NeonStack authentication flow with Stack Auth integration, protected routes, and Row Level Security policies. Created service layer for PostgREST Data API access.
```

## Example Session Summary Workflow

**Given this session:**
- Created 2 Claude Skills
- Added utilities.css reference file
- Updated skill documentation
- Fixed some typos

**Analysis:**
- Main accomplishment: Created skills
- Key details: Which skills, what for
- Secondary: Added reference file

**Summary:**
```
2025-11-17  Created Claude Skills for database setup and NeonStack architecture. Added utilities.css reference file to web-design-style skill.
```

## Implementation Code

When writing to `progress.md`:

```python
# Pseudocode for logging
from datetime import date

def log_progress(summary: str, log_file: str = "progress.md"):
    """Log session progress with current date"""
    today = date.today().strftime("%Y-%m-%d")
    entry = f"{today}  {summary}\n"

    # Create or append to log
    if not file_exists(log_file):
        content = "# Progress Log\n\nRecord of AI-assisted development sessions.\n\n"
        content += entry
        write_file(log_file, content)
    else:
        append_file(log_file, entry)

    return f'Logged to {log_file}: "{summary}"'
```

## Checklist

When logging progress:

- [ ] Reviewed entire conversation context
- [ ] Identified main accomplishments
- [ ] Wrote 1-3 sentence summary
- [ ] Started with action verb
- [ ] Included specific components/technologies
- [ ] Kept it concise but informative
- [ ] Used today's date in YYYY-MM-DD format
- [ ] Appended to `progress.md` in workspace root (NOT inside repos/)
- [ ] Confirmed entry to user

## Anti-Patterns to Avoid

**Don't write play-by-play:**
```
❌ First created the directory, then created the files, then edited the config, then...
```

**Don't be too vague:**
```
❌ Worked on the project.
❌ Made some improvements.
❌ Did stuff with the database.
```

**Don't include internal details:**
```
❌ Used the Edit tool to modify main.py, then used the Write tool to create config.py...
```

**Don't make it a technical spec:**
```
❌ Implemented PostgreSQL connection using psycopg2-binary version 2.9.10 with connection pooling via SQLModel create_engine function with echo parameter set to sql_echo variable...
```

## Reference

Based on `/home/nsheff/.claude/commands/log.md` slash command.
