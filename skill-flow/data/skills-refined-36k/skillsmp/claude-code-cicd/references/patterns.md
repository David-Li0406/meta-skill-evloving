# Claude Code CI/CD

## Patterns


---
  #### **Name**
Basic Headless Execution
  #### **Description**
Run Claude Code non-interactively
  #### **When To Use**
Any automated context (CI, scripts, cron)
  #### **Implementation**
    # Headless mode basics
    # The -p flag enables non-interactive mode
    
    # Simple prompt execution
    claude -p "Explain what this function does" src/utils.ts
    
    # With specific output format
    claude -p "List all TODOs in this file" src/main.ts --output-format text
    
    # JSON output for parsing
    claude -p "Analyze this code for issues" src/api.ts --output-format json
    
    # Streaming JSON for real-time processing
    claude -p "Review this PR" --output-format stream-json
    
    # Environment variables for CI
    export ANTHROPIC_API_KEY=${{ secrets.ANTHROPIC_API_KEY }}
    
    # Or with explicit provider
    claude -p "Review code" \
      --api-key $ANTHROPIC_API_KEY \
      --model claude-sonnet-4-20250514
    
    # With file input
    cat changes.diff | claude -p "Review these changes"
    
    # Multiple files
    claude -p "Find security issues in these files" \
      src/auth.ts src/api.ts src/db.ts
    

---
  #### **Name**
GitHub Actions Code Review
  #### **Description**
Automated PR code review
  #### **When To Use**
AI-assisted code review on PRs
  #### **Implementation**
    # .github/workflows/claude-review.yml
    name: Claude Code Review
    
    on:
      pull_request:
        types: [opened, synchronize]
        # Only review substantial changes
        paths:
          - 'src/**'
          - '!src/**/*.test.ts'
    
    jobs:
      review:
        runs-on: ubuntu-latest
        # Skip for very small PRs
        if: github.event.pull_request.additions > 10
    
        steps:
          - uses: actions/checkout@v4
            with:
              fetch-depth: 0
    
          - name: Install Claude Code
            run: npm install -g @anthropic-ai/claude-code
    
          - name: Get changed files
            id: files
            run: |
              echo "files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | grep -E '\.(ts|js|py)$' | tr '\n' ' ')" >> $GITHUB_OUTPUT
    
          - name: Run Claude Review
            env:
              ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
            run: |
              claude -p "Review these files for bugs, security issues, and code quality. Be concise. Focus on actionable feedback.
    
              Files: ${{ steps.files.outputs.files }}
    
              Output as markdown suitable for a PR comment." \
                --output-format text > review.md
    
          - name: Post review comment
            uses: actions/github-script@v7
            with:
              script: |
                const fs = require('fs');
                const review = fs.readFileSync('review.md', 'utf8');
    
                await github.rest.issues.createComment({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: context.issue.number,
                  body: `## Claude Code Review\n\n${review}`
                });
    

---
  #### **Name**
Issue Triage Automation
  #### **Description**
Auto-label and triage new issues
  #### **When To Use**
Managing issue intake at scale
  #### **Implementation**
    # .github/workflows/issue-triage.yml
    name: Issue Triage
    
    on:
      issues:
        types: [opened]
    
    jobs:
      triage:
        runs-on: ubuntu-latest
        permissions:
          issues: write
    
        steps:
          - uses: actions/checkout@v4
    
          - name: Install Claude Code
            run: npm install -g @anthropic-ai/claude-code
    
          - name: Analyze issue
            id: analyze
            env:
              ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
            run: |
              # Use smaller model for triage (cost effective)
              claude -p "Analyze this GitHub issue and return JSON:
              {
                \"labels\": [\"bug\"|\"feature\"|\"docs\"|\"question\"],
                \"priority\": \"high\"|\"medium\"|\"low\",
                \"area\": \"frontend\"|\"backend\"|\"infra\"|\"other\",
                \"needs_info\": true|false,
                \"summary\": \"one line summary\"
              }
    
              Issue Title: ${{ github.event.issue.title }}
              Issue Body: ${{ github.event.issue.body }}" \
                --model claude-haiku-3-5 \
                --output-format json > analysis.json
    
              echo "result=$(cat analysis.json)" >> $GITHUB_OUTPUT
    
          - name: Apply labels
            uses: actions/github-script@v7
            with:
              script: |
                const analysis = JSON.parse('${{ steps.analyze.outputs.result }}');
    
                // Apply labels
                const labels = [
                  ...analysis.labels,
                  `priority:${analysis.priority}`,
                  `area:${analysis.area}`
                ];
    
                await github.rest.issues.addLabels({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: context.issue.number,
                  labels: labels
                });
    
                // If needs more info, add comment
                if (analysis.needs_info) {
                  await github.rest.issues.createComment({
                    owner: context.repo.owner,
                    repo: context.repo.repo,
                    issue_number: context.issue.number,
                    body: "Thanks for opening this issue! Could you provide more details about:\n- Steps to reproduce\n- Expected vs actual behavior\n- Your environment"
                  });
                }
    

---
  #### **Name**
GitLab CI/CD Integration
  #### **Description**
Claude Code in GitLab pipelines
  #### **When To Use**
GitLab-based projects
  #### **Implementation**
    # .gitlab-ci.yml
    stages:
      - review
      - test
      - deploy
    
    variables:
      CLAUDE_MODEL: claude-sonnet-4-20250514
    
    claude-review:
      stage: review
      image: node:20
      rules:
        - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      before_script:
        - npm install -g @anthropic-ai/claude-code
      script:
        # Get MR diff
        - git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD > changes.diff
    
        # Run Claude review
        - |
          claude -p "Review this diff for a merge request.
          Focus on: bugs, security issues, performance problems.
          Format as GitLab markdown.
    
          $(cat changes.diff)" \
            --output-format text > review.md
    
        # Post to MR (using GitLab API)
        - |
          curl --request POST \
            --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
            --header "Content-Type: application/json" \
            --data "{\"body\": \"## Claude Review\n\n$(cat review.md | jq -Rs .)\"}" \
            "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"
      variables:
        ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
    
    # Automated fix suggestions
    claude-fix:
      stage: review
      image: node:20
      rules:
        - if: $CI_PIPELINE_SOURCE == "merge_request_event"
          when: manual  # Manual trigger to control costs
      script:
        - npm install -g @anthropic-ai/claude-code
        - git config user.email "claude-bot@example.com"
        - git config user.name "Claude Bot"
    
        # Run Claude to fix issues
        - |
          claude -p "Fix any linting errors and type issues in the changed files.
          Do not make other changes." \
            --allowedTools "Edit,Bash(npm run lint:fix)"
    
        # If changes made, commit them
        - |
          if [ -n "$(git status --porcelain)" ]; then
            git add .
            git commit -m "fix: Auto-fix linting issues [Claude]"
            git push origin HEAD:$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME
          fi
    

---
  #### **Name**
Automated PR Creation
  #### **Description**
Create PRs from issues or descriptions
  #### **When To Use**
Converting specs to code
  #### **Implementation**
    # .github/workflows/auto-implement.yml
    name: Auto-implement Issue
    
    on:
      issues:
        types: [labeled]
    
    jobs:
      implement:
        runs-on: ubuntu-latest
        if: github.event.label.name == 'auto-implement'
        permissions:
          contents: write
          pull-requests: write
    
        steps:
          - uses: actions/checkout@v4
            with:
              token: ${{ secrets.GITHUB_TOKEN }}
    
          - name: Setup Git
            run: |
              git config user.email "claude-bot@users.noreply.github.com"
              git config user.name "Claude Bot"
    
          - name: Install Claude Code
            run: npm install -g @anthropic-ai/claude-code
    
          - name: Create branch
            run: |
              BRANCH="auto/issue-${{ github.event.issue.number }}"
              git checkout -b $BRANCH
              echo "branch=$BRANCH" >> $GITHUB_ENV
    
          - name: Implement feature
            env:
              ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
            run: |
              # Let Claude implement with controlled tools
              claude -p "Implement this feature request:
    
              Title: ${{ github.event.issue.title }}
              Description: ${{ github.event.issue.body }}
    
              Requirements:
              1. Follow existing code patterns
              2. Add tests for new functionality
              3. Update documentation if needed
              4. Make atomic, focused commits" \
                --allowedTools "Read,Write,Edit,Bash(npm test),Bash(npm run lint)"
    
          - name: Create PR
            env:
              GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            run: |
              git push origin ${{ env.branch }}
    
              gh pr create \
                --title "Implement: ${{ github.event.issue.title }}" \
                --body "Automated implementation of #${{ github.event.issue.number }}
    
              This PR was generated by Claude Code. Please review carefully before merging.
    
              Closes #${{ github.event.issue.number }}" \
                --base main \
                --head ${{ env.branch }} \
                --label "auto-generated"
    

---
  #### **Name**
SDK-Based Automation
  #### **Description**
Programmatic Claude Code control
  #### **When To Use**
Complex automation requiring code
  #### **Implementation**
    // Using Claude Code SDK for programmatic control
    // automation/review-service.ts
    
    import Anthropic from "@anthropic-ai/sdk";
    import { execSync } from "child_process";
    
    interface ReviewRequest {
      files: string[];
      context: string;
      strictness: "lenient" | "normal" | "strict";
    }
    
    interface ReviewResult {
      summary: string;
      issues: Array<{
        file: string;
        line: number;
        severity: "error" | "warning" | "info";
        message: string;
      }>;
      approved: boolean;
    }
    
    async function reviewCode(request: ReviewRequest): Promise<ReviewResult> {
      // Read file contents
      const fileContents = request.files.map(file => {
        const content = execSync(`cat ${file}`).toString();
        return `### ${file}\n\`\`\`\n${content}\n\`\`\``;
      }).join("\n\n");
    
      // Use Claude Code in headless mode via SDK
      const result = execSync(
        `claude -p "${buildPrompt(request, fileContents)}" --output-format json`,
        {
          env: {
            ...process.env,
            ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY
          }
        }
      ).toString();
    
      return JSON.parse(result);
    }
    
    function buildPrompt(request: ReviewRequest, files: string): string {
      const strictnessGuide = {
        lenient: "Focus only on critical bugs and security issues",
        normal: "Balance thoroughness with practicality",
        strict: "Apply rigorous standards, flag all potential issues"
      };
    
      return `You are reviewing code for a PR.
    
      Context: ${request.context}
      Review strictness: ${request.strictness}
      Guidelines: ${strictnessGuide[request.strictness]}
    
      Files to review:
      ${files}
    
      Return JSON matching this schema:
      {
        "summary": "Brief overall assessment",
        "issues": [
          {
            "file": "path/to/file",
            "line": 42,
            "severity": "error|warning|info",
            "message": "Description of issue"
          }
        ],
        "approved": true/false
      }`;
    }
    
    // Usage in CI script
    async function main() {
      const changedFiles = execSync(
        "git diff --name-only origin/main...HEAD"
      ).toString().trim().split("\n");
    
      const result = await reviewCode({
        files: changedFiles.filter(f => f.endsWith(".ts")),
        context: "Feature branch for user authentication",
        strictness: "normal"
      });
    
      console.log(JSON.stringify(result, null, 2));
    
      // Exit with error if not approved
      if (!result.approved) {
        process.exit(1);
      }
    }
    
    main();
    

## Anti-Patterns


---
  #### **Name**
Running Claude on Every Commit
  #### **Description**
Triggering Claude for every single commit
  #### **Why Bad**
    Expensive - each run costs money.
    Slow - adds latency to every commit.
    Noisy - too many reviews causes alert fatigue.
    
  #### **What To Do Instead**
    Trigger on PR events, not individual commits.
    Add size filters (skip very small PRs).
    Use labels for opt-in expensive analysis.
    

---
  #### **Name**
Unbounded Tool Access in CI
  #### **Description**
Not restricting which tools Claude can use
  #### **Why Bad**
    CI environments need controlled access.
    Unrestricted Bash could run dangerous commands.
    Could accidentally push or delete things.
    
  #### **What To Do Instead**
    Use --allowedTools to whitelist specific tools.
    claude -p "..." --allowedTools "Read,Edit,Bash(npm test)"
    

---
  #### **Name**
Secrets in Prompts
  #### **Description**
Including secrets directly in prompt text
  #### **Why Bad**
    Secrets appear in logs.
    Prompt text may be stored/logged.
    Security risk in multi-tenant CI.
    
  #### **What To Do Instead**
    Use environment variables.
    export ANTHROPIC_API_KEY=${{ secrets.KEY }}
    Never echo or cat secrets.
    

---
  #### **Name**
No Cost Controls
  #### **Description**
Running without usage limits or model tiers
  #### **Why Bad**
    Costs can spiral unexpectedly.
    Large PRs trigger large context.
    No visibility into spend.
    
  #### **What To Do Instead**
    Use Haiku for triage, Sonnet for review.
    Set --max-tokens to limit output.
    Add spend monitoring and alerts.
    

---
  #### **Name**
Trusting AI Output Blindly
  #### **Description**
Auto-merging or deploying based solely on AI approval
  #### **Why Bad**
    AI can hallucinate or miss issues.
    Removes human accountability.
    Risky for security-sensitive code.
    
  #### **What To Do Instead**
    Use AI for draft reviews, human for final approval.
    AI suggests, human decides.
    Keep auto-merge for low-risk changes only.
    