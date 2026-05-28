# Commit Message Style Guide

Conventions for git commit messages in Sun Lab projects.

---

## Format

**Header line limit**: The first line (header) must be no longer than 72 characters. This ensures proper display in Git
logs, GitHub, and other tools.

**Single-line commits**: Use for focused, single-purpose changes.

```
Added Python 3.14 support.
Fixed a bug that allowed valves to violate keepalive guard.
Optimized the behavior of camera ID discovery functionality.
```

**Multi-line commits**: Use for changes that bundle related modifications.

```
Added MCP server module for agentic library interaction.

-- Added mcp_server.py exposing camera discovery and video session management.
-- Added 'axvs mcp' CLI command to start the MCP server.
-- Added frame display support to MCP video sessions.
-- Fixed various documentation and code style inconsistencies.
```

---

## Writing Style

**Verb tense**: Start with a past tense verb:

| Verb       | Use Case                                    |
|------------|---------------------------------------------|
| Added      | New features, files, or functionality       |
| Fixed      | Bug fixes and error corrections             |
| Updated    | Modifications to existing functionality     |
| Refactored | Code restructuring without behavior changes |
| Optimized  | Performance improvements                    |
| Improved   | Enhancements to existing features           |
| Removed    | Deletions of code, files, or features       |
| Deprecated | Marking functionality for future removal    |
| Prepared   | Release preparation tasks                   |
| Finalized  | Completing a feature or release             |

**Punctuation**: Always end commit messages with a period.

**Content**: Focus on *what* was changed and *why*, not *how*.

---

## Examples

**Good commit messages:**

```
Added trigger_type field to all task templates.
Fixed zone range calculation for occupancy zones.
Updated configuration-verification skill with cross-platform support.
Refactored style guide into separate domain-specific files.
Removed deprecated API endpoints from configuration loader.
```

**Avoid:**

```
fixed bug                          # Too vague, no punctuation
Updated stuff                      # Not specific
Changes to Task.cs                 # Describes file, not change
WIP                                # Not descriptive
```

---

## Input/Output Examples

Transform descriptions into proper commit messages:

| Input (What was done)                                    | Output (Commit message)                                       |
|----------------------------------------------------------|---------------------------------------------------------------|
| Added user authentication with JWT tokens                | Added JWT-based authentication for user sessions.             |
| Fixed bug where dates displayed incorrectly              | Fixed date formatting in timezone conversion.                 |
| Updated dependencies and refactored error handling       | Updated dependencies and standardized error response format.  |
| Removed deprecated API endpoints                         | Removed deprecated v1 API endpoints from configuration.       |
| Refactored the zone detection logic for clarity          | Refactored zone detection logic to improve readability.       |

---

## Common Mistakes

| Wrong                              | Correct                                     | Issue                      |
|------------------------------------|---------------------------------------------|----------------------------|
| `fixed bug`                        | `Fixed null reference in zone detection.`   | Too vague, no punctuation  |
| `Updated stuff`                    | `Updated MQTT topic names to match spec.`   | Not specific               |
| `Changes to Task.cs`               | `Added corridor reset logic to Task.`       | Describes file, not change |
| `WIP`                              | `Added initial zone boundary detection.`    | Not descriptive            |
| `Add new feature`                  | `Added new feature.`                        | Present tense, no period   |
| `This commit fixes the login bug`  | `Fixed login validation error.`             | Unnecessary preamble       |

---

## Verification Checklist

**You MUST verify your commit message against this checklist before submitting.**

```
Commit Message Compliance:
- [ ] Starts with past tense verb (Added, Fixed, Updated, Refactored, Removed)
- [ ] Header line ≤ 72 characters
- [ ] Ends with a period
- [ ] Describes *what* was changed and *why*, not *how*
- [ ] Specific and descriptive (not vague like "Updated stuff")
- [ ] Multi-line format used for bundled changes (if applicable)
```
