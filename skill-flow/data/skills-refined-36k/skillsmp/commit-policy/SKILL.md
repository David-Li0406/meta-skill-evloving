| Metadata | Value |
|:---|:---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-01-24 |
| **Author** | Sangeetha Grantha Team |

# Commit Policy

You are responsible for ensuring that all changes committed to the repository adhere to the strict `commit-guardrails-workflow`. 

## 1. Traceability (The Reference Rule)

**EVERY** commit must be linked to a specific documentation file in `application_documentation`. This ensures that every line of code exists for a documented reason.

### Commit Message Format
Your commit messages must follow this structure:

```text
<Title>: <Short Summary>

Ref: application_documentation/<path-to-file>.md

<Detailed Description (bullet points)>
```

### Rules
1.  **Mandatory Reference**: You CANNOT suggest a commit message without a `Ref:` line.
2.  **Existing File**: The file referenced in `Ref:` MUST exist.
3.  **One Reference Per Commit**: A commit should address only one feature or requirement file. Do not combine unrelated changes.

## 2. Security (The No-Secrets Rule)

You must strictly prevent sensitive data from entering the codebase.

### Blocked Items
- **API Keys**: `SG_GEMINI_API_KEY`, `AWS_SECRET_ACCESS_KEY`, `OPENAI_API_KEY`, etc.
- **Configuration Files**: `config/.env`, `config/.env.development`, `config/.env.production`.
- **Secrets/Tokens**: Any string that looks like a high-entropy secret.

### Pre-Commit Check
Before suggesting `git commit`, mentally (or actually) check:
1.  "Did I add any file that might contain a secret?"
2.  "Am I adding a `.env` file?" (If so, STOP and add it to `.gitignore` instead).

## 3. Workflow

When you are ready to commit changes for the user:
1.  **Stage**: `git add <files>`
2.  **Identify Reference**: Find the relevant markdown file in `application_documentation` that describes why this change is happening.
3.  **Draft Message**: detailed message with the `Ref:` tag.
4.  **Execute**: `git commit -m "..."` (or ask user to approve).

**Example of a Good Commit:**
```bash
git commit -m "Implement user login rate limiting

Ref: application_documentation/01-requirements/features/security-hardening.md

- Added RateLimiter service
- Updated LoginController to use RateLimiter
- Added unit tests"
```
