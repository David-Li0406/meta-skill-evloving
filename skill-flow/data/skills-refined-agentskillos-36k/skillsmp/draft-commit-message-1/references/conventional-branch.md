# Conventional branch

Conventional Branch refers to a structured and standardized naming convention for Git branches which aims to make branch more readable and actionable. We’ve suggested some branch prefixes you might want to use, but you can also specify your own naming convention. A consistent naming convention makes it easier to identify branches by type.

## Key points

- Purpose-driven Branch Names: each branch name clearly indicates its purpose, making it easy for all developers to understand what the branch is for.
- Integration with CI/CD: by using consistent branch names, it can help automated systems (like Continuous Integration/Continuous Deployment pipelines) to trigger specific actions based on the branch type (e.g., auto-deployment from release branches).
- Team Collaboration: it encourages collaboration within teams by making branch purpose explicit, reducing misunderstandings, and making it easier for team members to switch between tasks without confusion.

## Specification

### Branch naming prefixes

The branch specification supports the following prefixes and should be structured as `type/description` or `type/scope/description`.

- `feature/` (or `feat/`): for new features (e.g., `feature/add-login-page`, `feat/add-login-page`).
- `bugfix/` (or `fix/`): for bug fixes (e.g., `bugfix/fix-header-bug`, `fix/header-bug`).
- `hotfix/`: for urgent fixes (e.g., `hotfix/security-patch`).
- `release/`: for branches preparing a release (e.g., `release/v1.2.0`).
- `chore/`: for non-code tasks like dependency, docs updates (e.g., `chore/update-dependencies`).
- `bump/`: for update/increment version of dependencies.

### Basic rules

- Use Lowercase Alphanumerics, Hyphens, and Dots: Always use lowercase letters (`a-z`), numbers (`0-9`), and hyphens (`-`) to separate words. Avoid special characters, underscores, or spaces. For release branches, dots (`.`) may be used in the description to represent version numbers (e.g., `release/v1.2.0`).
- No Consecutive, Leading, or Trailing Hyphens or Dots: Ensure that hyphens and dots do not appear consecutively (e.g., `feature/new--login`, `release/v1.-2.0`), nor at the start or end of the description (e.g., `feature/-new-login`, `release/v1.2.0.`).
- Keep It Clear and Concise: The branch name should be descriptive yet concise, clearly indicating the purpose of the work.
- Include Ticket Numbers: If applicable, include the ticket number from your project management tool to make tracking easier. For example, for a ticket `issue-123`, the branch name could be `feature/issue-123-new-login`.
