---
name: git-pr
description: Create or update a pull request for the current branch
invocation: /bkff:git-pr
arguments:
  - name: --title
    type: string
    required: false
    description: Override auto-generated PR title
  - name: --draft
    type: flag
    required: false
    description: Create as draft PR
  - name: --ready
    type: flag
    required: false
    description: Mark draft PR as ready for review
  - name: --comments
    type: flag
    required: false
    description: Retrieve and display PR review comments
  - name: --analyze
    type: flag
    required: false
    description: Analyze comments for requirements compliance (requires --comments)
---

# Manage Pull Request

Creates or updates a pull request for the current branch. Uses the repository's PR template if available, or generates a default description.

## Usage

```
/bkff:git-pr [--title "PR title"] [--draft] [--ready] [--comments] [--analyze]
```

## Options

| Option | Description |
|--------|-------------|
| `--title` | Override the auto-generated PR title |
| `--draft` | Create as a draft pull request |
| `--ready` | Mark existing draft PR as ready for review |
| `--comments` | Retrieve and display PR review comments |
| `--analyze` | Analyze comments for requirements compliance (requires `--comments`) |

## What It Does

1. Checks if PR already exists for branch
2. Pushes branch to origin if needed
3. Creates new PR or updates existing one
4. Uses PR template if available

## Example Output

```
## Pull Request Created

### Branch
- **Head**: feature/auth-login
- **Base**: main

### Pull Request
- **Number**: #123
- **Title**: feat(auth): implement user authentication
- **URL**: https://github.com/owner/repo/pull/123
```

## Requirements

- Must be run inside a git worktree
- `git` CLI for branch operations
- `gh` CLI for PR creation (authenticated)
- Cannot be on main/master branch

## Implementation

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$PLUGIN_DIR/lib/common.sh"
source "$PLUGIN_DIR/lib/git-helpers.sh"
source "$PLUGIN_DIR/lib/pr-analysis.sh"

# Parse arguments
CUSTOM_TITLE=""
DRAFT_FLAG=""
READY_FLAG=""
COMMENTS_FLAG=""
ANALYZE_FLAG=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --title|-t)
            CUSTOM_TITLE="$2"
            shift 2
            ;;
        --draft|-d)
            DRAFT_FLAG="--draft"
            shift
            ;;
        --ready|-r)
            READY_FLAG="true"
            shift
            ;;
        --comments|-c)
            COMMENTS_FLAG="true"
            shift
            ;;
        --analyze|-a)
            ANALYZE_FLAG="true"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# FR-040: Validate --analyze requires --comments
if [[ -n "$ANALYZE_FLAG" && -z "$COMMENTS_FLAG" ]]; then
    error_exit "--analyze requires --comments flag"
fi

require_worktree

# Check if gh is available
command -v gh &>/dev/null || error_exit "gh CLI required but not installed"

CURRENT_BRANCH=$(get_current_branch)
MAIN_BRANCH=$(get_main_branch)

# FR-033: Cannot create PR from main branch
if [[ "$CURRENT_BRANCH" == "$MAIN_BRANCH" || "$CURRENT_BRANCH" == "master" ]]; then
    error_exit "Cannot create PR from $CURRENT_BRANCH branch"
fi

# FR-035: Handle --ready flag to mark draft PR as ready for review
if [[ -n "$READY_FLAG" ]]; then
    # Check if PR exists
    EXISTING_PR=$(gh pr list --head "$CURRENT_BRANCH" --json number,url,title,isDraft --jq '.[0]' 2>/dev/null || echo "")

    if [[ -z "$EXISTING_PR" ]]; then
        error_exit "No PR exists for this branch. Create one first."
    fi

    PR_NUMBER=$(echo "$EXISTING_PR" | jq -r '.number')
    PR_URL=$(echo "$EXISTING_PR" | jq -r '.url')
    PR_TITLE=$(echo "$EXISTING_PR" | jq -r '.title')
    IS_DRAFT=$(echo "$EXISTING_PR" | jq -r '.isDraft')

    if [[ "$IS_DRAFT" == "true" ]]; then
        # Mark as ready using gh pr ready
        if gh pr ready "$PR_NUMBER" 2>/dev/null; then
            echo "## Pull Request Ready for Review"
            echo ""
            echo "### Pull Request"
            echo "- **Number**: #$PR_NUMBER"
            echo "- **Title**: $PR_TITLE"
            echo "- **Status**: Open (was Draft)"
            echo "- **URL**: $PR_URL"
            echo ""
            success "PR is now ready for review."
        else
            error_exit "Failed to mark PR as ready. Check GitHub authentication."
        fi
    else
        # FR-036: Handle --ready on already-ready PR
        echo "## Pull Request Already Ready"
        echo ""
        echo "### Pull Request"
        echo "- **Number**: #$PR_NUMBER"
        echo "- **Title**: $PR_TITLE"
        echo "- **Status**: Open"
        echo ""
        info "PR is already ready for review. No changes made."
    fi
    exit 0
fi

# FR-037: Handle --comments flag to retrieve PR review comments
if [[ -n "$COMMENTS_FLAG" ]]; then
    # Check if PR exists
    EXISTING_PR=$(gh pr list --head "$CURRENT_BRANCH" --json number,url --jq '.[0]' 2>/dev/null || echo "")

    if [[ -z "$EXISTING_PR" ]]; then
        error_exit "No PR exists for this branch."
    fi

    PR_NUMBER=$(echo "$EXISTING_PR" | jq -r '.number')

    # Get repository info for API calls
    REPO_INFO=$(gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"') || error_exit "Failed to get repository info. Check network connection."

    # T084: Fetch review comments with network failure handling
    API_ERROR=""
    REVIEW_COMMENTS=$(gh api "repos/$REPO_INFO/pulls/$PR_NUMBER/comments" 2>&1) || API_ERROR="$REVIEW_COMMENTS"
    if [[ -n "$API_ERROR" ]]; then
        if [[ "$API_ERROR" == *"connect"* ]] || [[ "$API_ERROR" == *"network"* ]] || [[ "$API_ERROR" == *"timeout"* ]]; then
            error_exit "Network error fetching PR comments. Check your internet connection."
        elif [[ "$API_ERROR" == *"404"* ]]; then
            REVIEW_COMMENTS="[]"
        else
            warn "Failed to fetch review comments: $API_ERROR"
            REVIEW_COMMENTS="[]"
        fi
    fi

    # T084: Fetch issue comments with network failure handling
    API_ERROR=""
    ISSUE_COMMENTS=$(gh api "repos/$REPO_INFO/issues/$PR_NUMBER/comments" 2>&1) || API_ERROR="$ISSUE_COMMENTS"
    if [[ -n "$API_ERROR" ]]; then
        if [[ "$API_ERROR" == *"connect"* ]] || [[ "$API_ERROR" == *"network"* ]] || [[ "$API_ERROR" == *"timeout"* ]]; then
            error_exit "Network error fetching PR comments. Check your internet connection."
        elif [[ "$API_ERROR" == *"404"* ]]; then
            ISSUE_COMMENTS="[]"
        else
            warn "Failed to fetch issue comments: $API_ERROR"
            ISSUE_COMMENTS="[]"
        fi
    fi

    # Count total comments
    REVIEW_COUNT=$(echo "$REVIEW_COMMENTS" | jq 'length')
    ISSUE_COUNT=$(echo "$ISSUE_COMMENTS" | jq 'length')
    TOTAL_COMMENTS=$((REVIEW_COUNT + ISSUE_COUNT))

    # FR-040: Adjust header for analysis mode
    if [[ -n "$ANALYZE_FLAG" ]]; then
        echo "## Review Comments Analysis for PR #$PR_NUMBER"
    else
        echo "## Review Comments for PR #$PR_NUMBER"
    fi
    echo ""

    # FR-039: Handle no comments case
    if [[ "$TOTAL_COMMENTS" -eq 0 ]]; then
        info "No review comments exist for this pull request."
        exit 0
    fi

    # FR-044: Detect spec file for analysis
    SPEC_FILE=""
    if [[ -n "$ANALYZE_FLAG" ]]; then
        SPEC_FILE=$(detect_spec_file "$CURRENT_BRANCH")
    fi

    # FR-038: Calculate reviewer attribution
    ALL_REVIEWERS=$(echo "$REVIEW_COMMENTS $ISSUE_COMMENTS" | jq -s 'add | [.[].user.login] | group_by(.) | map({user: .[0], count: length}) | sort_by(-.count)')
    REVIEWER_SUMMARY=$(echo "$ALL_REVIEWERS" | jq -r 'map("@\(.user) (\(.count))") | join(", ")')

    echo "### Summary"
    echo "- **Total Comments**: $TOTAL_COMMENTS"
    echo "- **Reviewers**: $REVIEWER_SUMMARY"

    # Analysis-specific summary
    if [[ -n "$ANALYZE_FLAG" ]]; then
        if [[ -n "$SPEC_FILE" ]]; then
            echo "- **Spec File**: Found ($(basename "$(dirname "$SPEC_FILE")")/spec.md)"
        else
            echo "- **Spec File**: Not found (evaluating against general principles)"
        fi
    fi
    echo ""

    echo "### Comments"
    echo ""

    # Track high-priority comments for recommendation
    declare -a PRIORITY_COMMENTS=()

    # Function to display a comment with optional analysis
    display_comment() {
        local user="$1"
        local location="$2"
        local body="$3"

        echo "#### @$user on $location"
        echo "> ${body//$'\n'/$'\n'> }"
        echo ""

        if [[ -n "$ANALYZE_FLAG" ]]; then
            # FR-041: Compliance probability scoring
            local category
            category=$(categorize_comment "$body" "$SPEC_FILE")
            local score
            score=$(estimate_compliance_score "$body" "$category")

            echo "**Compliance Score**: $score"
            echo "**Category**: $category"

            # FR-042: Rationale generation
            local rationale=""
            case "$category" in
                "Security-Related")
                    rationale="Addresses security best practices or vulnerability prevention."
                    ;;
                "Requirements-Related")
                    if [[ -n "$SPEC_FILE" ]]; then
                        rationale="May relate to functional requirements in spec file."
                    else
                        rationale="Substantive feedback that may impact functionality."
                    fi
                    ;;
                "Stylistic/Preference")
                    rationale="Code style or naming suggestion. No impact on requirements compliance."
                    ;;
                "General Feedback")
                    rationale="Summary or approval comment without actionable code change."
                    ;;
            esac
            echo "**Rationale**: $rationale"

            # Track high-priority comments (score >= 80)
            if [[ "$score" != "N/A" && "$score" -ge 80 ]]; then
                PRIORITY_COMMENTS+=("$location ($score% - $category)")
            fi
        fi

        echo ""
        echo "---"
        echo ""
    }

    # Display review comments (line-specific)
    if [[ "$REVIEW_COUNT" -gt 0 ]]; then
        while IFS= read -r comment_json; do
            user=$(echo "$comment_json" | jq -r '.user.login')
            path=$(echo "$comment_json" | jq -r '.path')
            line=$(echo "$comment_json" | jq -r '.line // .original_line // "N/A"')
            body=$(echo "$comment_json" | jq -r '.body')
            display_comment "$user" "$path:$line" "$body"
        done < <(echo "$REVIEW_COMMENTS" | jq -c '.[]')
    fi

    # Display issue comments (general)
    if [[ "$ISSUE_COUNT" -gt 0 ]]; then
        while IFS= read -r comment_json; do
            user=$(echo "$comment_json" | jq -r '.user.login')
            body=$(echo "$comment_json" | jq -r '.body')
            display_comment "$user" "(general)" "$body"
        done < <(echo "$ISSUE_COMMENTS" | jq -c '.[]')
    fi

    # FR-081: Analysis summary with priority recommendations
    if [[ -n "$ANALYZE_FLAG" && ${#PRIORITY_COMMENTS[@]} -gt 0 ]]; then
        echo "### Recommendation"
        echo "**Priority comments to address**:"
        local i=1
        for comment in "${PRIORITY_COMMENTS[@]}"; do
            echo "$i. $comment"
            ((i++))
        done
        echo ""
    fi

    exit 0
fi

# FR-034: Adjust header for draft PRs
if [[ -n "$DRAFT_FLAG" ]]; then
    echo "## Draft Pull Request Created"
else
    echo "## Pull Request"
fi
echo ""

# FR-024: Check if PR already exists
echo "### Branch"
echo "- **Head**: $CURRENT_BRANCH"
echo "- **Base**: $MAIN_BRANCH"

EXISTING_PR=$(gh pr list --head "$CURRENT_BRANCH" --json number,url --jq '.[0]' 2>/dev/null || echo "")

# FR-028: Ensure branch is pushed
if ! is_branch_pushed "$CURRENT_BRANCH"; then
    info "Pushing branch to origin..."
    if git push -u origin "$CURRENT_BRANCH"; then
        echo "- **Pushed**: Yes (just pushed)"
    else
        error_exit "Failed to push branch. Check network connection."
    fi
else
    # Check if we're ahead of origin
    AHEAD=$(get_ahead_count "$CURRENT_BRANCH")
    if [[ "$AHEAD" -gt 0 ]]; then
        info "Pushing $AHEAD new commits..."
        git push || warn "Push failed"
    fi
    echo "- **Pushed**: Yes"
fi
echo ""

# Generate PR title from commits if not provided
if [[ -z "$CUSTOM_TITLE" ]]; then
    # Use first commit message as title
    CUSTOM_TITLE=$(git log "$MAIN_BRANCH..HEAD" --format="%s" | tail -1)
fi

# FR-027: Check for PR template
TEMPLATE_FILE=""
for tmpl in .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md PULL_REQUEST_TEMPLATE.md; do
    if [[ -f "$tmpl" ]]; then
        TEMPLATE_FILE="$tmpl"
        break
    fi
done

# Generate PR body
generate_pr_body() {
    echo "## Summary"
    echo ""
    git log "$MAIN_BRANCH..HEAD" --format="- %s" | tac
    echo ""
    echo "## Test Plan"
    echo ""
    echo "- [ ] Unit tests pass"
    echo "- [ ] Manual testing completed"
    echo ""
    echo "---"
    echo ""
    echo "🤖 Generated with [Claude Code](https://claude.ai/code)"
}

if [[ -n "$EXISTING_PR" ]]; then
    # FR-025: Update existing PR
    PR_NUMBER=$(echo "$EXISTING_PR" | jq -r '.number')
    PR_URL=$(echo "$EXISTING_PR" | jq -r '.url')

    echo "### Pull Request (Existing)"
    echo "- **Number**: #$PR_NUMBER"
    echo "- **Status**: Updated"
    echo "- **URL**: $PR_URL"
    echo ""
    success "PR already exists. Branch pushed with latest changes."
else
    # FR-026: Create new PR
    echo "### Pull Request"
    info "Creating pull request..."

    # Build gh pr create command using array for safe argument handling
    CREATE_ARGS=('--title' "$CUSTOM_TITLE" '--base' "$MAIN_BRANCH")
    [[ -n "$DRAFT_FLAG" ]] && CREATE_ARGS+=('--draft')

    # FR-027: Only provide --body if no template file exists
    # gh pr create automatically uses PR template when found and --body is not provided
    if [[ -z "$TEMPLATE_FILE" ]]; then
        PR_BODY=$(generate_pr_body)
        CREATE_ARGS+=('--body' "$PR_BODY")
    fi

    if PR_URL=$(gh pr create "${CREATE_ARGS[@]}" 2>&1); then
        PR_NUMBER=$(echo "$PR_URL" | grep -oE '[0-9]+$' || echo "")
        echo "- **Number**: #$PR_NUMBER"
        echo "- **Title**: $CUSTOM_TITLE"
        [[ -n "$DRAFT_FLAG" ]] && echo "- **Status**: Draft (not ready for review)" || echo "- **Status**: Open"
        echo "- **URL**: $PR_URL"
        [[ -n "$TEMPLATE_FILE" ]] && echo "- **Template**: Used $TEMPLATE_FILE"
        echo ""

        # Display commits included in the PR
        echo "### Commits Included"
        git log "$MAIN_BRANCH..HEAD" --format="%s" | tac | nl -w1 -s'. '
        echo ""

        # FR-034: Different success message for draft PRs
        if [[ -n "$DRAFT_FLAG" ]]; then
            success "Draft PR created. Use \`/bkff:git-pr --ready\` when ready for review."
        else
            success "PR created successfully. Awaiting review."
        fi
    else
        error_exit "Failed to create PR. Check GitHub authentication.\n$PR_URL"
    fi
fi
```
