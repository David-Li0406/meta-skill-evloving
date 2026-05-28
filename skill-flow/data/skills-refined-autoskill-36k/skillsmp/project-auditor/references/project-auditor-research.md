# project-auditor Research

Research document for the project auditor skill. This skill helps developers set up projects for success with easy onboarding, quality enforcement, Claude optimization, secure and high-velocity releases.

## Phase 1: Upstream Survey

### Existing Project Auditing Skills

No direct equivalent exists in the upstream sources we curate from:

| Source | Finding |
|--------|---------|
| [obra/superpowers](https://github.com/obra/superpowers) | No project auditing skills. Focuses on development workflow (TDD, debugging, planning, code review) |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | No dedicated auditor. Related: `code-reviewer`, `security-auditor`, `devops-engineer`, `dependency-manager` |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Security-focused auditing (code auditing, static analysis, differential review) but not project health |

### Related Tools in Ecosystem

- **Trail of Bits Skills** — Security auditing, static analysis with CodeQL/Semgrep, differential code review
- **Claude CodePro** — Spec-driven workflows, TDD enforcement, quality hooks
- **Rulesync** — Auto-generates configs for AI coding agents
- **TDD Guard** — Hooks-driven system blocking TDD violations

**Gap identified**: No comprehensive project health/setup auditor exists. This is a novel skill.

---

## Phase 2: Research Findings

### 1. Essential Repository Files

Source: [GitHub Docs - Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)

| File | Purpose | Location |
|------|---------|----------|
| `README.md` | Project overview, setup instructions | Root |
| `LICENSE` | Legal terms for use | Root |
| `CONTRIBUTING.md` | Contribution guidelines | Root, `.github/`, or `docs/` |
| `CODE_OF_CONDUCT.md` | Community behavior standards | Root, `.github/`, or `docs/` |
| `SECURITY.md` | Vulnerability reporting instructions | Root, `.github/`, or `docs/` |
| `CODEOWNERS` | Automatic reviewer assignment | `.github/`, root, or `docs/` |
| `.gitignore` | Files to exclude from version control | Root |
| `CHANGELOG.md` | Version history | Root |

### 2. GitHub Community Standards Profile

Source: [GitHub Docs - About community profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)

GitHub's community profile checklist includes:
- README
- CODE_OF_CONDUCT
- LICENSE
- CONTRIBUTING
- Issue templates
- Pull request templates
- SECURITY.md

**Recommendation**: Audit against this checklist for public repositories.

### 3. CLAUDE.md Standards

Sources: [Anthropic Blog](https://claude.com/blog/using-claude-md-files), [Builder.io Guide](https://www.builder.io/blog/claude-md-guide), [HumanLayer Blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

#### Required Content
- Tech stack (frameworks, languages, versions)
- Project structure (directories and their roles)
- Build/test/deploy commands
- Code style and conventions
- "Do not touch" areas

#### Best Practices
- Keep minimal — only universally applicable instructions
- Be specific ("Use 2-space indentation" not "Format code properly")
- Don't duplicate linter rules — let tools do deterministic work
- Avoid over-referencing files (bloats context window)
- Provide alternatives with constraints, not just "never do X"
- Use `/init` command as starting point, then refine
- Check into source control for team iteration

#### File Locations (Layered System)
1. `~/.claude/CLAUDE.md` — Global preferences
2. `project-root/CLAUDE.md` — Shared team context
3. Subdirectories — Feature/module-specific
4. `CLAUDE.local.md` — Personal (gitignored)

### 4. Branch Protection Rules

Source: [GitHub Docs - About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

#### Recommended Settings for Main Branch
- [ ] Require pull request before merging
- [ ] Require approvals (1-2 minimum)
- [ ] Dismiss stale reviews when new commits pushed
- [ ] Require review from Code Owners
- [ ] Require approval from someone other than last pusher
- [ ] Require status checks to pass
- [ ] Require branches to be up to date before merging
- [ ] Require signed commits (optional, high security)
- [ ] Require linear history (optional, clean git log)
- [ ] Do not allow force pushes
- [ ] Do not allow deletions

#### Rulesets vs Branch Protection
- **Branch Protection**: Per-branch, granular control
- **Rulesets**: Organization-wide, standardized governance
- Use "evaluate" mode before enforcing to test rules

### 5. GitHub Security Features

Source: [GitHub Docs - Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)

#### Minimum Security Configuration
- [ ] Dependabot alerts enabled
- [ ] Secret scanning enabled
- [ ] Push protection enabled
- [ ] Code scanning enabled (CodeQL)
- [ ] Private vulnerability reporting enabled
- [ ] SECURITY.md file present
- [ ] 2FA required for organization members

#### GitHub Actions Security
- Never use self-hosted runners for public repos
- Set `GITHUB_TOKEN` permissions to restricted (read-only by default)
- Pin actions to commit SHA, not branch/tag

### 6. CI/CD Best Practices (GitHub Actions)

Sources: [GitHub Blog](https://github.blog/news-insights/product-news/lets-talk-about-github-actions/), [Graphite Guide](https://graphite.dev/guides/in-depth-guide-ci-cd-best-practices)

#### Workflow Structure
- Use descriptive workflow filenames (`build-and-test.yml`, `deploy-prod.yml`)
- Use reusable workflows (`workflow_call`) for common patterns
- Define clear job dependencies with `needs`
- Run independent jobs in parallel

#### Performance
- Use concurrency strategy to cancel outdated runs
- Use matrix strategy for multi-OS/version testing
- Set reasonable timeouts (30 min typical max)
- Cache dependencies appropriately

#### Required Workflows
- [ ] Build verification
- [ ] Test suite
- [ ] Linting/formatting check
- [ ] Security scanning (SAST)
- [ ] Dependency audit

### 7. CODEOWNERS Best Practices

Source: [GitHub Docs - About code owners](https://docs.github.com/articles/about-code-owners)

#### File Location
Prefer `.github/CODEOWNERS` for organization.

#### Syntax Examples
```
# Default owners for everything
* @org/core-team

# Frontend ownership
/src/components/ @org/frontend-team
*.tsx @org/frontend-team

# Backend ownership
/src/api/ @org/backend-team

# Security-sensitive files
/src/auth/ @org/security-team
/.github/ @org/platform-team

# Protect CODEOWNERS itself
/.github/CODEOWNERS @org/platform-team
```

#### Best Practices
- Use teams over individuals
- Update when team members change
- Define ownership at appropriate granularity
- Protect the CODEOWNERS file itself
- Combine with branch protection for enforcement

### 8. Dependency Management

Source: [GitHub Docs - Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates)

#### Dependabot Configuration
- [ ] Enable Dependabot alerts
- [ ] Enable Dependabot security updates
- [ ] Configure `dependabot.yml` for version updates
- [ ] Use grouped updates to reduce PR noise
- [ ] Set up auto-merge for patch updates (with tests)

#### Best Practices
- Have automated tests before merging dependency updates
- Use compatibility scores to assess breaking change risk
- Schedule regular dependency audits
- Generate SBOM for supply chain visibility

### 9. License Compliance

Source: [Linux Foundation - License Best Practices](https://www.linuxfoundation.org/licensebestpractices), [SPDX](https://spdx.org/licenses/)

#### SPDX License Identifiers
Add to every source file header:
```
// SPDX-License-Identifier: MIT
```

#### Benefits
- Precise and machine-readable
- Language neutral
- Improves SCA tool accuracy
- License info travels with file

#### License Expression Syntax
- Choice: `GPL-2.0-only OR MIT`
- Multiple apply: `Apache-2.0 AND MIT`
- With exception: `GPL-2.0-or-later WITH Bison-exception-2.2`

### 10. Issue and PR Templates

Sources: [GitHub Docs - Issue forms syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms), [GitHub Docs - Form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)

#### Issue Forms (YAML)
Location: `.github/ISSUE_TEMPLATE/`

Issue forms provide structured input with validation. Use `.yml` extension.

**Required top-level keys:**
- `name` — Template name (must be unique)
- `description` — Shown in template chooser
- `body` — Array of form elements

**Optional top-level keys:**
- `title` — Pre-populated issue title (e.g., `"[Bug]: "`)
- `labels` — Auto-applied labels (must exist in repo)
- `assignees` — Auto-assigned users
- `projects` — Add to project board

**Form element types:**
- `markdown` — Static text/instructions
- `input` — Single-line text
- `textarea` — Multi-line text (supports file attachments)
- `dropdown` — Single or multi-select
- `checkboxes` — Multiple choice

#### Example: Bug Report Template
```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting! Please fill out the details below.

  - type: input
    id: version
    attributes:
      label: Version
      description: What version are you using?
      placeholder: "e.g., 1.2.3"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: What happened? What did you expect?
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Critical (blocks all work)
        - High (major feature broken)
        - Medium (workaround exists)
        - Low (minor inconvenience)
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, browser, runtime versions
      render: shell
```

#### Example: Feature Request Template
```yaml
# .github/ISSUE_TEMPLATE/feature_request.yml
name: Feature Request
description: Suggest a new feature or enhancement
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How would you like this to work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: What other solutions have you considered?

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have searched for existing feature requests
          required: true
        - label: I am willing to help implement this feature
```

#### Template Chooser Config
```yaml
# .github/ISSUE_TEMPLATE/config.yml
blank_issues_enabled: false
contact_links:
  - name: Documentation
    url: https://docs.example.com
    about: Check docs before opening an issue
  - name: Discussions
    url: https://github.com/org/repo/discussions
    about: Ask questions in Discussions
```

#### Pull Request Template
Location: `.github/pull_request_template.md`

```markdown
## Summary
<!-- Brief description of changes -->

## Related Issue
Fixes #

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for changes
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] No new warnings introduced
```

#### Best Practices
- Use YAML forms over Markdown templates for better UX
- Keep templates concise — too long and contributors skip them
- Use specific prompts, not vague instructions
- Require fields that are essential for triage
- Set `blank_issues_enabled: false` to enforce templates
- Add contact links for docs/discussions to reduce noise
- Update templates as project evolves
- Integrate with CI/CD triggers on issue/PR events

### 11. Version and Runtime Checks

Sources: [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference), [endoflife.date](https://endoflife.date), [Node.js EOL](https://nodejs.org/en/about/eol)

#### Claude Code Version

Check current version:
```bash
claude --version
```

Update to latest:
```bash
claude update
```

**Recommendation**: Check Claude Code version at start of audit and recommend update if outdated.

#### Runtime EOL Tracking

Use [endoflife.date](https://endoflife.date) as authoritative source for:
- [Node.js](https://endoflife.date/nodejs)
- [Python](https://endoflife.date/python)
- [Go](https://endoflife.date/go)
- [Java](https://endoflife.date/java)
- [Ruby](https://endoflife.date/ruby)
- [PHP](https://endoflife.date/php)
- [.NET](https://endoflife.date/dotnet)

#### Version Detection Commands

| Runtime | Version Check | Config File |
|---------|---------------|-------------|
| Node.js | `node --version` | `.nvmrc`, `.node-version`, `package.json` engines |
| Python | `python --version` | `.python-version`, `pyproject.toml`, `runtime.txt` |
| Go | `go version` | `go.mod` (go directive) |
| Java | `java --version` | `pom.xml`, `build.gradle` |
| Ruby | `ruby --version` | `.ruby-version`, `Gemfile` |

#### Risks of EOL Runtimes

1. **No security patches** — Disclosed vulnerabilities remain unfixed
2. **Ecosystem drift** — Popular packages drop support for EOL versions
3. **Compliance failures** — Many audits forbid unmaintained runtimes
4. **CI/CD issues** — Runners may deprecate old versions

#### Recommended Checks

- [ ] Claude Code is up to date (`claude update`)
- [ ] Runtime version is not EOL
- [ ] Runtime version is specified in config file (reproducible builds)
- [ ] CI/CD uses same runtime version as development
- [ ] Dockerfile/container uses supported base image version

#### Node.js Specific

Check for vulnerabilities in current Node version:
```bash
npx is-my-node-vulnerable
```

Current recommendations (as of Jan 2026):
- Node.js 18 and earlier: **EOL** — upgrade immediately
- Node.js 20: Maintenance LTS (supported until April 2026)
- Node.js 22: Active LTS (recommended, supported until April 2027)

---

## Audit Checklist Summary

### Critical (Must Have)
- [ ] README.md exists and is informative
- [ ] LICENSE file exists
- [ ] .gitignore configured
- [ ] Branch protection on main
- [ ] CI/CD pipeline exists
- [ ] Dependabot alerts enabled
- [ ] Runtime version is not EOL

### Important (Should Have)
- [ ] CLAUDE.md for AI-assisted development
- [ ] Claude Code is up to date
- [ ] CONTRIBUTING.md
- [ ] CODE_OF_CONDUCT.md
- [ ] SECURITY.md
- [ ] CODEOWNERS file
- [ ] Issue templates
- [ ] PR template
- [ ] Secret scanning enabled
- [ ] Code scanning enabled
- [ ] Runtime version pinned in config file

### Recommended (Nice to Have)
- [ ] CHANGELOG.md
- [ ] SPDX license identifiers in source files
- [ ] Signed commits required
- [ ] Linear commit history
- [ ] Dependabot version updates configured
- [ ] GitHub Discussions enabled (for community projects)
- [ ] Project boards for issue tracking
- [ ] Container base images use supported versions

---

## Sources

### Official Documentation
- [GitHub Docs - Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- [GitHub Docs - About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs - About code owners](https://docs.github.com/articles/about-code-owners)
- [GitHub Docs - Dependabot security updates](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates)
- [GitHub Docs - Issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [GitHub Docs - Community profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)

### Claude Code Documentation
- [Anthropic - Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files)
- [Anthropic - Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Builder.io - The Complete Guide to CLAUDE.md](https://www.builder.io/blog/claude-md-guide)
- [HumanLayer - Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

### License Compliance
- [SPDX License List](https://spdx.org/licenses/)
- [Linux Foundation - License Best Practices](https://www.linuxfoundation.org/licensebestpractices)

### CI/CD
- [GitHub Blog - GitHub Actions updates](https://github.blog/news-insights/product-news/lets-talk-about-github-actions/)
- [Graphite - CI/CD Best Practices](https://graphite.dev/guides/in-depth-guide-ci-cd-best-practices)

### Runtime EOL Tracking
- [endoflife.date](https://endoflife.date) — Authoritative source for EOL dates
- [Node.js EOL](https://nodejs.org/en/about/eol)
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)

### Upstream Skills
- [obra/superpowers](https://github.com/obra/superpowers)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [trailofbits/skills](https://github.com/trailofbits/skills)
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
