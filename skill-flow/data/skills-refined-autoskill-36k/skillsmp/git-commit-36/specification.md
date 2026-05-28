# Git Commit Message Rules (Conventional Commits v1.0.0)

Purpose
- Add human- and machine-readable meaning to commit messages to:
  - Auto-generate CHANGELOGs
  - Drive Semantic Versioning (SemVer)
  - Trigger build/release pipelines
  - Improve collaboration, review, and history navigation

Commit Structure
- Header (required)
  <type>[optional scope][!]: <description>
- Body (optional, starts after one blank line)
- Footer(s) (optional, start after one blank line; can be multiple)
  - Format: Token: Value (follows git trailer style)
  - Examples: BREAKING CHANGE: <details>, Refs: #123

Fields
- type (required)
  - feat: a new feature (SemVer MINOR)
  - fix: a bug fix (SemVer PATCH)
  - Other common types (extensions; not mandated by the spec, no inherent SemVer effect unless BREAKING):
    - docs, style, refactor, perf, test, build, ci, chore, revert, etc.
- scope (optional)
  - Noun describing the affected area in parentheses, e.g., feat(parser):
- ! (optional)
  - Append after type or type(scope) to indicate a breaking change (SemVer MAJOR)
- description (required)
  - Short summary directly after “: ”
- body (optional)
  - Free-form; can contain multiple paragraphs
- footers (optional)
  - Each footer is a separate line: Token: Value or Token #Value
  - Use hyphens instead of spaces in tokens (e.g., Acked-by)
  - Special case: BREAKING CHANGE must be uppercase
  - BREAKING-CHANGE is synonymous with BREAKING CHANGE (as a footer token)

Breaking Changes (MAJOR)
- Indicate in one of two ways (either or both):
  - Add “!” after type/scope: e.g., feat!: ...
  - Add a footer: BREAKING CHANGE: <impact and migration>
- If using only “!” without a BREAKING footer, the description must clearly explain the breaking change

Specification Essentials (MUST/SHOULD)
- Header must start with type, followed by optional scope, optional “!”, then a colon, space, and description
- Description must follow “: ” immediately
- Body starts after one blank line following the description
- Footers start after one blank line following the body; one footer per line
- Implementations MUST treat units case-insensitively, except BREAKING CHANGE which MUST be uppercase
- Custom types are allowed; only feat/fix and BREAKING changes have defined SemVer meaning

Examples
- Basic
  - docs: correct spelling of CHANGELOG
  - feat(lang): add Polish language
- With breaking footer
  - feat: allow provided config object to extend other configs
  - BREAKING CHANGE: `extends` key in config file is now used for extending other config files
- Using “!”
  - feat!: send an email to the customer when a product is shipped
  - feat(api)!: send an email to the customer when a product is shipped
- “!” and footer together
  - chore!: drop support for Node 6
  - BREAKING CHANGE: use JavaScript features not available in Node 6.
- Multi-paragraph body with multiple footers
  - fix: prevent racing of requests
  -
  - Introduce a request id and a reference to latest request. Dismiss
  - incoming responses other than from latest request.
  -
  - Remove timeouts which were used to mitigate the racing issue but are
  - obsolete now.
  -
  - Reviewed-by: Z
  - Refs: #123
- Revert suggestion
  - revert: let us never again speak of the noodle incident
  - Refs: 676104e, a215868

SemVer Mapping
- fix => PATCH release
- feat => MINOR release
- Any type + BREAKING CHANGE or “!” => MAJOR release

Workflow and FAQ Highlights
- Apply the rules even during early development
- If one commit spans multiple types, split into multiple commits when possible
- Wrong type? Prefer fixing via git rebase -i before merge/release
- Non-spec types aren’t fatal but may be ignored by tooling
- Squash-based workflows let maintainers normalize commit messages on merge

Prompts for Claude/Cursor
- Generate commit messages using Conventional Commits v1.0.0:
  - Header format: <type>(<scope>)![optional]: <description>
  - If breaking: add “!” or a BREAKING CHANGE footer with migration guidance
  - If issues/PRs exist: add Refs/Closes <ID> in footers
  - Prefer splitting multi-type diffs; if not possible, explain each change in the body
  - Use appropriate types for docs/style/build/ci/test/etc.

Minimal Lint Checklist (commitlint-friendly)
- Header must match:
  ^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?(!)?: .+
- BREAKING CHANGE token must be uppercase; BREAKING-CHANGE allowed
- Blank line required before body and before footers
- Footers must follow Token: Value or Token #Value formats