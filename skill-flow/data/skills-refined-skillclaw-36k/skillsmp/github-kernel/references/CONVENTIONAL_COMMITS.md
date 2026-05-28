# Conventional Commits

The GitHub Skills ecosystem adheres to the **Conventional Commits 1.0.0** specification.

## Format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Common Types

* `feat`: A new feature
* `fix`: A bug fix
* `docs`: Documentation only changes
* `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
* `refactor`: A code change that neither fixes a bug nor adds a feature
* `perf`: A code change that improves performance
* `test`: Adding missing tests or correcting existing tests
* `build`: Changes that affect the build system or external dependencies
* `ci`: Changes to our CI configuration files and scripts
* `chore`: Other changes that don't modify src or test files

## Examples

### Feature

`feat(auth): add google oauth2 login support`

### Bug Fix

`fix(ui): prevent button overlap on mobile screens`

### Breaking Change

```text
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now reserved
```

## Usage in Skills

* **PR Titles**: `github-pr-flow` should enforce this format for PR titles.
* **Commit Messages**: Agents should use this format when committing via `create_or_update_file` (message param) or `push_files`.
