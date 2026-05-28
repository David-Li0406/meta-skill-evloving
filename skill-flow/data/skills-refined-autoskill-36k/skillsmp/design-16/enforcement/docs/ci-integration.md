# CI/CD Integration Guide

Integrate the invariant validator into your continuous integration pipeline to catch spec violations before they reach production.

**Goal**: Block PRs with violations, allow PRs with warnings, surface all issues clearly.

---

## Quick Start

| Platform | Time to Setup | Jump to Section |
|----------|---------------|-----------------|
| GitHub Actions | 2 min | [GitHub Actions](#github-actions) |
| GitLab CI | 3 min | [GitLab CI](#gitlab-ci) |
| Jenkins | 5 min | [Jenkins](#jenkins) |
| Azure Pipelines | 3 min | [Azure Pipelines](#azure-pipelines) |
| Pre-commit Hooks | 1 min | [Git Hooks](#git-hooks) |

---

## GitHub Actions

The simplest integration. Copy the workflow file and you're done.

### Setup

1. Copy `.github/workflows/validate-specs.yml` to your repo
2. Ensure `enforcement/validator.sh` is in your repo
3. Push and create a PR with spec changes

### What It Does

- Triggers on PRs modifying `specs/**/*.md` or `prp/**/*.md`
- Validates each changed spec file
- Posts results as PR comment
- Blocks merge if violations found
- Allows merge with warnings (shows them)

### Customization

**Change spec directories:**
```yaml
on:
  pull_request:
    paths:
      - 'your-specs-dir/**/*.md'    # Modify this
      - 'another-dir/**/*.md'
```

**Add domain-specific validation:**
```yaml
- name: Validate specs
  run: |
    # Add domain flags based on file path
    if [[ "$spec" == *"/construction/"* ]]; then
      ./enforcement/validator.sh "$spec" --domain domains/physical-construction.md
    else
      ./enforcement/validator.sh "$spec"
    fi
```

**Skip validation for certain files:**
```yaml
- name: Find spec files
  run: |
    # Exclude drafts
    CHANGED_FILES=$(git diff --name-only ... | grep -v "draft-" | tr '\n' ' ')
```

### Gotchas

1. **File permissions**: The workflow makes `validator.sh` executable, but ensure it has correct shebang (`#!/bin/bash`)
2. **Path sensitivity**: GitHub Actions paths are case-sensitive
3. **PR comment permissions**: The workflow needs `pull-requests: write` permission (default for GITHUB_TOKEN)

---

## GitLab CI

### Setup

Create `.gitlab-ci.yml` in your repo root:

```yaml
# .gitlab-ci.yml - Invariant Validator for GitLab CI

stages:
  - validate

variables:
  VALIDATOR_PATH: "./enforcement/validator.sh"
  SPEC_DIRS: "specs prp"

validate-specs:
  stage: validate
  image: alpine:latest
  before_script:
    - apk add --no-cache bash grep findutils
    - chmod +x $VALIDATOR_PATH
  script: |
    #!/bin/bash
    set -e

    TOTAL_VIOLATIONS=0
    TOTAL_WARNINGS=0
    FAILED_FILES=""

    # Get changed files for MRs, or all specs for pushes
    if [ -n "$CI_MERGE_REQUEST_IID" ]; then
      # Merge Request - validate changed files
      apk add --no-cache git
      git fetch origin $CI_MERGE_REQUEST_TARGET_BRANCH_NAME
      SPEC_FILES=$(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD -- $SPEC_DIRS | grep '\.md$' || true)
    else
      # Direct push - validate all specs
      SPEC_FILES=$(find $SPEC_DIRS -name "*.md" -type f 2>/dev/null || true)
    fi

    if [ -z "$SPEC_FILES" ]; then
      echo "No spec files to validate"
      exit 0
    fi

    for spec in $SPEC_FILES; do
      [ ! -f "$spec" ] && continue

      echo "=========================================="
      echo "Validating: $spec"
      echo "=========================================="

      set +e
      OUTPUT=$($VALIDATOR_PATH "$spec" 2>&1)
      EXIT_CODE=$?
      set -e

      echo "$OUTPUT"

      VIOLATIONS=$(echo "$OUTPUT" | grep -c "VIOLATION:" || true)
      WARNINGS=$(echo "$OUTPUT" | grep -c "WARNING:" || true)

      TOTAL_VIOLATIONS=$((TOTAL_VIOLATIONS + VIOLATIONS))
      TOTAL_WARNINGS=$((TOTAL_WARNINGS + WARNINGS))

      [ $EXIT_CODE -ne 0 ] && FAILED_FILES="$FAILED_FILES $spec"
    done

    echo ""
    echo "=========================================="
    echo "SUMMARY"
    echo "=========================================="
    echo "Total Violations: $TOTAL_VIOLATIONS"
    echo "Total Warnings: $TOTAL_WARNINGS"

    if [ $TOTAL_VIOLATIONS -gt 0 ]; then
      echo ""
      echo "FAILED - Fix violations before merging"
      echo "Failed files:$FAILED_FILES"
      exit 1
    elif [ $TOTAL_WARNINGS -gt 0 ]; then
      echo ""
      echo "PASSED with warnings - Consider addressing before production"
      exit 0
    else
      echo ""
      echo "PASSED - All specs valid"
      exit 0
    fi
  rules:
    - if: $CI_MERGE_REQUEST_IID
      changes:
        - specs/**/*.md
        - prp/**/*.md
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      changes:
        - specs/**/*.md
        - prp/**/*.md
  artifacts:
    when: always
    reports:
      dotenv: validation.env
    expire_in: 7 days
  allow_failure: false
```

### What It Does

- Runs on merge requests modifying spec files
- Validates changed specs (MR) or all specs (push to main)
- Fails pipeline on violations
- Passes with warnings

### Customization

**Add domain validation:**
```yaml
script: |
  # Detect domain from path
  DOMAIN_FLAG=""
  if [[ "$spec" == *"/house/"* ]]; then
    DOMAIN_FLAG="--domain domains/physical-construction.md"
  fi
  $VALIDATOR_PATH "$spec" $DOMAIN_FLAG
```

**Post results to MR:**
```yaml
after_script:
  - |
    if [ -n "$CI_MERGE_REQUEST_IID" ]; then
      curl --request POST \
        --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
        --data "body=Validation complete: $TOTAL_VIOLATIONS violations, $TOTAL_WARNINGS warnings" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"
    fi
```

### Gotchas

1. **Alpine image**: Requires `bash`, `grep`, `findutils` packages
2. **Git availability**: Need to add `git` package for MR diff detection
3. **File globbing**: GitLab CI uses Ruby-style globs, not bash

---

## Jenkins

### Setup

Create `Jenkinsfile` in your repo root:

```groovy
// Jenkinsfile - Invariant Validator for Jenkins

pipeline {
    agent any

    environment {
        VALIDATOR_PATH = './enforcement/validator.sh'
        SPEC_DIRS = 'specs prp'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Validator') {
            steps {
                sh 'chmod +x ${VALIDATOR_PATH}'
            }
        }

        stage('Find Spec Files') {
            steps {
                script {
                    // For PRs, get changed files; otherwise validate all
                    if (env.CHANGE_ID) {
                        // Pull Request
                        def changedFiles = sh(
                            script: "git diff --name-only origin/${env.CHANGE_TARGET}...HEAD -- ${SPEC_DIRS} | grep '\\.md\$' || true",
                            returnStdout: true
                        ).trim()
                        env.SPEC_FILES = changedFiles
                    } else {
                        // Direct push
                        def allFiles = sh(
                            script: "find ${SPEC_DIRS} -name '*.md' -type f 2>/dev/null | tr '\\n' ' ' || true",
                            returnStdout: true
                        ).trim()
                        env.SPEC_FILES = allFiles
                    }

                    if (env.SPEC_FILES?.trim()) {
                        echo "Files to validate: ${env.SPEC_FILES}"
                    } else {
                        echo "No spec files to validate"
                    }
                }
            }
        }

        stage('Validate Specs') {
            when {
                expression { env.SPEC_FILES?.trim() }
            }
            steps {
                script {
                    def totalViolations = 0
                    def totalWarnings = 0
                    def failedFiles = []

                    env.SPEC_FILES.split().each { spec ->
                        if (!fileExists(spec)) {
                            echo "WARNING: File not found: ${spec}"
                            return
                        }

                        echo "=========================================="
                        echo "Validating: ${spec}"
                        echo "=========================================="

                        def result = sh(
                            script: "${env.VALIDATOR_PATH} '${spec}' 2>&1",
                            returnStdout: true,
                            returnStatus: false
                        )

                        echo result

                        // Count violations and warnings
                        def violations = (result =~ /VIOLATION:/).size()
                        def warnings = (result =~ /WARNING:/).size()

                        totalViolations += violations
                        totalWarnings += warnings

                        if (violations > 0) {
                            failedFiles << spec
                        }
                    }

                    echo ""
                    echo "=========================================="
                    echo "SUMMARY"
                    echo "=========================================="
                    echo "Total Violations: ${totalViolations}"
                    echo "Total Warnings: ${totalWarnings}"

                    // Store for post actions
                    env.TOTAL_VIOLATIONS = totalViolations.toString()
                    env.TOTAL_WARNINGS = totalWarnings.toString()
                    env.FAILED_FILES = failedFiles.join(', ')

                    if (totalViolations > 0) {
                        error("Spec validation failed with ${totalViolations} violation(s)")
                    } else if (totalWarnings > 0) {
                        unstable("Spec validation passed with ${totalWarnings} warning(s)")
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (env.CHANGE_ID && env.TOTAL_VIOLATIONS) {
                    // Post comment to PR (requires GitHub/GitLab plugin)
                    def status = env.TOTAL_VIOLATIONS.toInteger() > 0 ? 'FAILED' : 'PASSED'
                    def message = """
                    ## Invariant Validation ${status}

                    | Metric | Count |
                    |--------|-------|
                    | Violations | ${env.TOTAL_VIOLATIONS} |
                    | Warnings | ${env.TOTAL_WARNINGS} |

                    ${env.FAILED_FILES ? "Failed files: ${env.FAILED_FILES}" : ''}
                    """.stripIndent()

                    echo message
                    // Uncomment if using GitHub PR Builder plugin:
                    // pullRequest.comment(message)
                }
            }
        }
        failure {
            echo "Spec validation failed - violations must be fixed"
        }
        unstable {
            echo "Spec validation passed with warnings"
        }
        success {
            echo "Spec validation passed"
        }
    }
}
```

### What It Does

- Validates on PRs and pushes
- Detects changed files for PRs
- Reports violations/warnings
- Marks build failed (violations) or unstable (warnings)

### Customization

**Add domain validation:**
```groovy
def domainFlag = ""
if (spec.contains("/construction/")) {
    domainFlag = "--domain domains/physical-construction.md"
}
sh "${env.VALIDATOR_PATH} '${spec}' ${domainFlag}"
```

**Email notifications:**
```groovy
post {
    failure {
        emailext(
            subject: "Spec Validation Failed: ${env.JOB_NAME}",
            body: "Violations: ${env.TOTAL_VIOLATIONS}\nWarnings: ${env.TOTAL_WARNINGS}",
            recipientProviders: [requestor()]
        )
    }
}
```

### Gotchas

1. **Groovy regex**: Use `=~` for regex matching, escape backslashes
2. **Script security**: May need to approve regex methods in script security
3. **File paths**: Use quotes around paths with spaces
4. **Git availability**: Ensure git is in PATH on Jenkins agent

---

## Azure Pipelines

### Setup

Create `azure-pipelines.yml` in your repo root:

```yaml
# azure-pipelines.yml - Invariant Validator for Azure Pipelines

trigger:
  branches:
    include:
      - main
      - master
  paths:
    include:
      - specs/**/*.md
      - prp/**/*.md

pr:
  branches:
    include:
      - main
      - master
  paths:
    include:
      - specs/**/*.md
      - prp/**/*.md

pool:
  vmImage: 'ubuntu-latest'

variables:
  VALIDATOR_PATH: './enforcement/validator.sh'
  SPEC_DIRS: 'specs prp'

stages:
  - stage: Validate
    displayName: 'Validate Spec Invariants'
    jobs:
      - job: ValidateSpecs
        displayName: 'Run Invariant Validator'
        steps:
          - checkout: self
            fetchDepth: 0

          - task: Bash@3
            displayName: 'Make validator executable'
            inputs:
              targetType: 'inline'
              script: 'chmod +x $(VALIDATOR_PATH)'

          - task: Bash@3
            displayName: 'Find and validate spec files'
            inputs:
              targetType: 'inline'
              script: |
                #!/bin/bash
                set -e

                TOTAL_VIOLATIONS=0
                TOTAL_WARNINGS=0
                FAILED_FILES=""

                # Detect if this is a PR
                if [ -n "$(System.PullRequest.TargetBranch)" ]; then
                  # PR - validate changed files
                  TARGET_BRANCH=$(echo "$(System.PullRequest.TargetBranch)" | sed 's|refs/heads/||')
                  git fetch origin $TARGET_BRANCH
                  SPEC_FILES=$(git diff --name-only origin/$TARGET_BRANCH...HEAD -- $(SPEC_DIRS) | grep '\.md$' || true)
                else
                  # Push - validate all specs
                  SPEC_FILES=$(find $(SPEC_DIRS) -name "*.md" -type f 2>/dev/null | tr '\n' ' ' || true)
                fi

                if [ -z "$SPEC_FILES" ]; then
                  echo "No spec files to validate"
                  echo "##vso[task.setvariable variable=VALIDATION_RESULT]skip"
                  exit 0
                fi

                echo "Files to validate:"
                echo "$SPEC_FILES"
                echo ""

                for spec in $SPEC_FILES; do
                  [ ! -f "$spec" ] && continue

                  echo "=========================================="
                  echo "Validating: $spec"
                  echo "=========================================="

                  set +e
                  OUTPUT=$($(VALIDATOR_PATH) "$spec" 2>&1)
                  EXIT_CODE=$?
                  set -e

                  echo "$OUTPUT"

                  VIOLATIONS=$(echo "$OUTPUT" | grep -c "VIOLATION:" || true)
                  WARNINGS=$(echo "$OUTPUT" | grep -c "WARNING:" || true)

                  TOTAL_VIOLATIONS=$((TOTAL_VIOLATIONS + VIOLATIONS))
                  TOTAL_WARNINGS=$((TOTAL_WARNINGS + WARNINGS))

                  [ $EXIT_CODE -ne 0 ] && FAILED_FILES="$FAILED_FILES $spec"
                done

                echo ""
                echo "=========================================="
                echo "SUMMARY"
                echo "=========================================="
                echo "Total Violations: $TOTAL_VIOLATIONS"
                echo "Total Warnings: $TOTAL_WARNINGS"

                # Set output variables for subsequent tasks
                echo "##vso[task.setvariable variable=TOTAL_VIOLATIONS]$TOTAL_VIOLATIONS"
                echo "##vso[task.setvariable variable=TOTAL_WARNINGS]$TOTAL_WARNINGS"
                echo "##vso[task.setvariable variable=FAILED_FILES]$FAILED_FILES"

                if [ $TOTAL_VIOLATIONS -gt 0 ]; then
                  echo "##vso[task.setvariable variable=VALIDATION_RESULT]failure"
                  echo "##vso[task.logissue type=error]Spec validation failed with $TOTAL_VIOLATIONS violation(s)"
                  echo "##vso[task.complete result=Failed;]"
                elif [ $TOTAL_WARNINGS -gt 0 ]; then
                  echo "##vso[task.setvariable variable=VALIDATION_RESULT]warnings"
                  echo "##vso[task.logissue type=warning]Spec validation passed with $TOTAL_WARNINGS warning(s)"
                else
                  echo "##vso[task.setvariable variable=VALIDATION_RESULT]success"
                  echo "All specs validated successfully"
                fi

          - task: Bash@3
            displayName: 'Post PR comment'
            condition: and(succeeded(), eq(variables['Build.Reason'], 'PullRequest'))
            inputs:
              targetType: 'inline'
              script: |
                # Azure DevOps API to post PR comment
                # Requires: System.AccessToken with PR comment permissions

                COMMENT="## Invariant Validation Results\n\n"
                COMMENT+="| Metric | Count |\n"
                COMMENT+="|--------|-------|\n"
                COMMENT+="| Violations | $(TOTAL_VIOLATIONS) |\n"
                COMMENT+="| Warnings | $(TOTAL_WARNINGS) |\n"

                if [ "$(VALIDATION_RESULT)" = "failure" ]; then
                  COMMENT+="\n**FAILED** - Fix violations before merging\n"
                  COMMENT+="Failed files: $(FAILED_FILES)"
                elif [ "$(VALIDATION_RESULT)" = "warnings" ]; then
                  COMMENT+="\n**PASSED** with warnings"
                else
                  COMMENT+="\n**PASSED** - All specs valid"
                fi

                echo -e "$COMMENT"

                # Uncomment to post via API:
                # curl -X POST \
                #   -H "Authorization: Bearer $(System.AccessToken)" \
                #   -H "Content-Type: application/json" \
                #   -d "{\"content\": \"$COMMENT\"}" \
                #   "$(System.CollectionUri)$(System.TeamProject)/_apis/git/repositories/$(Build.Repository.Name)/pullRequests/$(System.PullRequest.PullRequestId)/threads?api-version=7.0"
            env:
              SYSTEM_ACCESSTOKEN: $(System.AccessToken)

          - task: Bash@3
            displayName: 'Set final status'
            inputs:
              targetType: 'inline'
              script: |
                if [ "$(VALIDATION_RESULT)" = "failure" ]; then
                  exit 1
                fi
```

### What It Does

- Triggers on PRs and pushes to main
- Validates changed specs (PR) or all specs (push)
- Sets pipeline status based on results
- Can post comments to PRs (requires API setup)

### Customization

**Add domain validation:**
```yaml
script: |
  DOMAIN_FLAG=""
  if [[ "$spec" == *"/construction/"* ]]; then
    DOMAIN_FLAG="--domain domains/physical-construction.md"
  fi
  $(VALIDATOR_PATH) "$spec" $DOMAIN_FLAG
```

**Different pools for different branches:**
```yaml
pool:
  ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
    vmImage: 'ubuntu-latest'
  ${{ else }}:
    name: 'Self-Hosted-Pool'
```

### Gotchas

1. **Variable syntax**: Use `$(VAR)` for pipeline variables, `$VAR` in bash
2. **Fetch depth**: Set `fetchDepth: 0` for full git history
3. **PR comment API**: Requires proper authentication setup
4. **Branch refs**: Azure uses `refs/heads/` prefix for branch names

---

## Git Hooks

For immediate local validation before code leaves your machine.

### Setup

```bash
# From your repo root
./enforcement/docs/git-hooks/install.sh
```

### Available Hooks

| Hook | When | Behavior |
|------|------|----------|
| `pre-commit` | Before commit | Validates staged spec files |
| `pre-push` | Before push | Validates all changed specs vs remote |

### Manual Installation

```bash
# Copy hooks to .git/hooks
cp enforcement/docs/git-hooks/pre-commit .git/hooks/
cp enforcement/docs/git-hooks/pre-push .git/hooks/
chmod +x .git/hooks/pre-commit .git/hooks/pre-push
```

### Skip Hooks (Emergency)

```bash
# Skip pre-commit
git commit --no-verify -m "Emergency fix"

# Skip pre-push
git push --no-verify
```

### Gotchas

1. **Hooks not shared**: Git hooks aren't committed; run install.sh on each clone
2. **Path sensitivity**: Hooks use relative paths from repo root
3. **Exit codes**: Hook must return 0 to proceed, non-zero blocks action
4. **Performance**: Validates only changed files to stay fast

---

## Best Practices

### 1. Fail Fast, Fix Fast

Configure CI to run validation early in the pipeline:

```yaml
stages:
  - validate    # First!
  - test
  - build
  - deploy
```

### 2. Provide Clear Fix Guidance

Point developers to documentation:

```yaml
- name: Validation failed
  run: |
    echo "See enforcement/violation-messages.md for fix guidance"
    echo "Run locally: ./enforcement/validator.sh <spec>.md"
```

### 3. Domain-Aware Validation

Route specs to appropriate domains automatically:

```bash
# Detect domain from directory structure
get_domain_flags() {
  local spec="$1"
  local flags=""

  [[ "$spec" == *"/house/"* ]] && flags="--domain domains/physical-construction.md"
  [[ "$spec" == *"/api/"* ]] && flags="--domain domains/integration.md"
  [[ "$spec" == *"/data/"* ]] && flags="--domain domains/data-architecture.md"

  echo "$flags"
}
```

### 4. Cache Validation Results

For large repos, cache unchanged specs:

```yaml
- name: Cache validation results
  uses: actions/cache@v3
  with:
    path: .validation-cache
    key: validation-${{ hashFiles('specs/**/*.md') }}
```

### 5. Gradual Rollout

Start permissive, tighten over time:

```yaml
# Phase 1: Warnings only
allow_failure: true

# Phase 2: Block violations, allow warnings
allow_failure: false
# (default behavior)

# Phase 3: Block everything
# Modify validator to exit 1 on warnings
```

---

## Troubleshooting

### Validator not found

```
Error: enforcement/validator.sh: No such file or directory
```

**Fix**: Ensure validator.sh is committed to the repo and path is correct.

### Permission denied

```
Error: permission denied: ./enforcement/validator.sh
```

**Fix**: Add `chmod +x` step before running validator.

### No specs found

```
No spec files to validate
```

**Check**:
- Path patterns match your directory structure
- Files have `.md` extension
- For PRs, ensure base branch is fetched

### Colors not showing

Validator uses ANSI colors which may not render in all CI logs.

**Fix**: Most modern CI systems support colors. For plain text:
```bash
# Strip colors
./validator.sh spec.md 2>&1 | sed 's/\x1b\[[0-9;]*m//g'
```

### Git diff fails

```
fatal: bad revision 'origin/main...HEAD'
```

**Fix**: Ensure full git history is fetched:
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```
