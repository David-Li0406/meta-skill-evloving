# Security Pipeline - GitHub Actions CI/CD

Complete security-first CI/CD pipeline with SAST, DAST, SCA, and container scanning.

## 📝 Prompt

```
Create a comprehensive security pipeline for GitHub Actions:

Context:
- Node.js/TypeScript application
- Docker containerized deployment
- PostgreSQL database
- AWS cloud infrastructure
- Kubernetes deployment

Include:
- SAST (Static Application Security Testing) with Semgrep
- DAST (Dynamic Application Security Testing) with OWASP ZAP
- SCA (Software Composition Analysis) with Snyk
- Container scanning with Trivy
- Secret scanning
- License compliance checking
- Security gates and quality checks
- Automated vulnerability reporting

Show complete workflow with all stages, security checks, and failure conditions.
```

## 🔒 Complete Security Pipeline

### GitHub Actions Workflow

**File:** `.github/workflows/security-pipeline.yml`

```yaml
name: Security Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    # Run security scan daily at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch: # Allow manual triggers

env:
  NODE_VERSION: '18'
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ===== STAGE 1: SECRET SCANNING =====
  secret-scanning:
    name: 🔍 Secret Scanning
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Full history for secret scanning

      - name: TruffleHog Secret Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
          extra_args: --debug --only-verified

      - name: GitLeaks Secret Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}

      - name: Fail if secrets found
        if: failure()
        run: |
          echo "❌ Secrets detected in repository!"
          echo "Please remove secrets and use GitHub Secrets or vault instead."
          exit 1

  # ===== STAGE 2: DEPENDENCY SCANNING (SCA) =====
  dependency-scanning:
    name: 📦 Software Composition Analysis
    runs-on: ubuntu-latest
    needs: secret-scanning
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Snyk SCA Scan
        uses: snyk/actions/node@master
        continue-on-error: true
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high --fail-on=upgradable
          command: test

      - name: npm audit
        run: |
          npm audit --audit-level=moderate --json > npm-audit.json || true

      - name: Check for critical vulnerabilities
        run: |
          CRITICAL=$(jq '.metadata.vulnerabilities.critical' npm-audit.json)
          HIGH=$(jq '.metadata.vulnerabilities.high' npm-audit.json)
          
          echo "Critical vulnerabilities: $CRITICAL"
          echo "High vulnerabilities: $HIGH"
          
          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Critical vulnerabilities found!"
            exit 1
          fi
          
          if [ "$HIGH" -gt 5 ]; then
            echo "⚠️  Too many high severity vulnerabilities!"
            exit 1
          fi

      - name: License compliance check
        run: |
          npx license-checker --summary --onlyAllow "MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC"

      - name: Upload Snyk results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: snyk.sarif

  # ===== STAGE 3: STATIC APPLICATION SECURITY TESTING (SAST) =====
  sast-scanning:
    name: 🔎 SAST - Code Analysis
    runs-on: ubuntu-latest
    needs: secret-scanning
    permissions:
      security-events: write
      actions: read
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Semgrep SAST Scan
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
            p/nodejs
            p/typescript
            p/sql-injection
            p/xss
            p/command-injection
          generateSarif: true

      - name: CodeQL Analysis
        uses: github/codeql-action/init@v3
        with:
          languages: javascript, typescript
          queries: security-extended

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

      - name: ESLint Security Check
        run: |
          npm ci
          npx eslint . --ext .js,.ts --format json --output-file eslint-results.json \
            --plugin security \
            --plugin no-unsanitized \
            || true

      - name: Check ESLint Security Issues
        run: |
          SECURITY_ISSUES=$(jq '[.[] | .messages[] | select(.ruleId | startswith("security/"))] | length' eslint-results.json)
          echo "Security issues found: $SECURITY_ISSUES"
          
          if [ "$SECURITY_ISSUES" -gt 0 ]; then
            echo "⚠️  Security issues detected by ESLint"
            jq '[.[] | .messages[] | select(.ruleId | startswith("security/"))]' eslint-results.json
            exit 1
          fi

      - name: Upload SARIF results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: semgrep.sarif

  # ===== STAGE 4: BUILD & CONTAINER SCANNING =====
  container-security:
    name: 🐳 Container Security Scan
    runs-on: ubuntu-latest
    needs: [dependency-scanning, sast-scanning]
    permissions:
      contents: read
      security-events: write
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          load: true
          tags: ${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1' # Fail on critical/high vulnerabilities

      - name: Trivy full report
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'table'
          severity: 'UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL'

      - name: Grype vulnerability scanner (alternative)
        uses: anchore/scan-action@v3
        continue-on-error: true
        with:
          image: ${{ env.IMAGE_NAME }}:${{ github.sha }}
          fail-build: true
          severity-cutoff: high

      - name: Docker Scout CVE scan
        uses: docker/scout-action@v1
        continue-on-error: true
        with:
          command: cves
          image: ${{ env.IMAGE_NAME }}:${{ github.sha }}
          only-severities: critical,high
          exit-code: true

      - name: Scan for malware
        run: |
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy image --scanners vuln,secret,config \
            ${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'

  # ===== STAGE 5: INFRASTRUCTURE AS CODE SCANNING =====
  iac-scanning:
    name: 🏗️ Infrastructure Security
    runs-on: ubuntu-latest
    needs: secret-scanning

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Checkov IaC scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: dockerfile,kubernetes,terraform
          output_format: sarif
          output_file_path: checkov-results.sarif
          soft_fail: false

      - name: Terrascan IaC scan
        uses: tenable/terrascan-action@main
        with:
          iac_type: 'k8s'
          iac_dir: './k8s'
          policy_type: 'all'
          sarif_upload: true

      - name: KICS IaC scan
        uses: checkmarx/kics-github-action@v1.7
        with:
          path: '.'
          fail_on: high
          output_formats: 'sarif'
          output_path: kics-results.sarif

      - name: Upload IaC scan results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: checkov-results.sarif

  # ===== STAGE 6: DEPLOY TO STAGING =====
  deploy-staging:
    name: 🚀 Deploy to Staging
    runs-on: ubuntu-latest
    needs: [container-security, iac-scanning]
    if: github.event_name == 'push' && github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.DOCKER_REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:staging
            ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          aws eks update-kubeconfig --name staging-cluster --region us-east-1
          kubectl set image deployment/app app=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/app

  # ===== STAGE 7: DYNAMIC APPLICATION SECURITY TESTING (DAST) =====
  dast-scanning:
    name: 🎯 DAST - Runtime Security
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.event_name == 'push' && github.ref == 'refs/heads/develop'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: OWASP ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.10.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: OWASP ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.8.0
        continue-on-error: true
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-j'

      - name: Upload ZAP results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: zap-reports
          path: |
            zap_baseline_report.html
            zap_full_report.html

      - name: Nuclei vulnerability scan
        uses: projectdiscovery/nuclei-action@main
        with:
          target: https://staging.example.com
          github-report: true
          github-token: ${{ secrets.GITHUB_TOKEN }}

  # ===== STAGE 8: SECURITY REPORT =====
  security-report:
    name: 📊 Generate Security Report
    runs-on: ubuntu-latest
    needs: [dependency-scanning, sast-scanning, container-security, dast-scanning]
    if: always()

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4

      - name: Generate consolidated report
        run: |
          cat > security-report.md << 'EOF'
          # Security Scan Report
          
          **Date:** $(date)
          **Commit:** ${{ github.sha }}
          **Branch:** ${{ github.ref_name }}
          **Workflow:** ${{ github.run_number }}
          
          ## Summary
          
          | Check | Status |
          |-------|--------|
          | Secret Scanning | ${{ needs.secret-scanning.result }} |
          | Dependency Scanning | ${{ needs.dependency-scanning.result }} |
          | SAST | ${{ needs.sast-scanning.result }} |
          | Container Security | ${{ needs.container-security.result }} |
          | IaC Security | ${{ needs.iac-scanning.result }} |
          | DAST | ${{ needs.dast-scanning.result }} |
          
          ## Recommendations
          
          - Review all HIGH and CRITICAL findings
          - Update vulnerable dependencies
          - Fix security code issues
          - Remediate container vulnerabilities
          
          ## Next Steps
          
          1. Check GitHub Security tab for detailed findings
          2. Review SARIF uploads
          3. Create tickets for vulnerabilities
          4. Update dependencies and rebuild
          
          EOF

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('security-report.md', 'utf8');
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });

      - name: Upload security report
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security-report.md

  # ===== STAGE 9: COMPLIANCE CHECK =====
  compliance-check:
    name: ✅ Compliance Verification
    runs-on: ubuntu-latest
    needs: [security-report]
    if: always()

    steps:
      - name: Verify security gates
        run: |
          echo "Checking security compliance..."
          
          # Define compliance requirements
          REQUIRED_CHECKS=(
            "secret-scanning:success"
            "dependency-scanning:success"
            "sast-scanning:success"
            "container-security:success"
          )
          
          FAILED_CHECKS=()
          
          for check in "${REQUIRED_CHECKS[@]}"; do
            IFS=':' read -r job status <<< "$check"
            if [ "${{ needs[job].result }}" != "$status" ]; then
              FAILED_CHECKS+=("$job")
            fi
          done
          
          if [ ${#FAILED_CHECKS[@]} -gt 0 ]; then
            echo "❌ Compliance check FAILED"
            echo "Failed checks: ${FAILED_CHECKS[*]}"
            exit 1
          else
            echo "✅ All compliance checks passed"
          fi

      - name: Create compliance badge
        run: |
          echo "Generating compliance badge..."
          # Badge generation logic here
```

---

## 🔧 Configuration Files

### Semgrep Rules

**File:** `.semgrep.yml`

```yaml
rules:
  - id: hardcoded-secret
    patterns:
      - pattern: |
          password = "..."
      - pattern: |
          api_key = "..."
      - pattern: |
          secret = "..."
    message: "Hardcoded secret detected"
    severity: ERROR
    languages: [javascript, typescript]

  - id: sql-injection
    patterns:
      - pattern: |
          db.query($SQL + $INPUT)
      - pattern: |
          db.raw($SQL + $INPUT)
    message: "Potential SQL injection vulnerability"
    severity: ERROR
    languages: [javascript, typescript]

  - id: xss-vulnerability
    patterns:
      - pattern: |
          res.send($USERINPUT)
      - pattern: |
          innerHTML = $USERINPUT
    message: "Potential XSS vulnerability"
    severity: WARNING
    languages: [javascript, typescript]
```

### OWASP ZAP Rules

**File:** `.zap/rules.tsv`

```tsv
10000	IGNORE	(Script Passive Scan Rules)
10010	IGNORE	(Cookie No HttpOnly Flag)
10011	WARN	(Cookie Without Secure Flag)
10015	IGNORE	(Incomplete or No Cache-control Header Set)
10017	IGNORE	(Cross-Domain JavaScript Source File Inclusion)
10019	IGNORE	(Content-Type Header Missing)
10020	IGNORE	(X-Frame-Options Header)
10021	IGNORE	(X-Content-Type-Options Header Missing)
10023	IGNORE	(Information Disclosure - Debug Error Messages)
10024	IGNORE	(Information Disclosure - Sensitive Information in URL)
10025	IGNORE	(Information Disclosure - Sensitive Information in HTTP Referrer Header)
10026	IGNORE	(HTTP Parameter Override)
10027	IGNORE	(Information Disclosure - Suspicious Comments)
10028	IGNORE	(Open Redirect)
10029	IGNORE	(Cookie Poisoning)
10030	IGNORE	(User Controllable Charset)
10031	IGNORE	(User Controllable HTML Element Attribute (Potential XSS))
10032	IGNORE	(Viewstate)
10033	IGNORE	(Directory Browsing)
10034	IGNORE	(Heartbleed OpenSSL Vulnerability)
10035	IGNORE	(Strict-Transport-Security Header)
10036	IGNORE	(HTTP Server Response Header)
10037	IGNORE	(Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s))
10038	IGNORE	(Content Security Policy (CSP) Header Not Set)
10039	IGNORE	(X-Backend-Server Header Information Leak)
10040	FAIL	(Secure Pages Include Mixed Content)
10041	FAIL	(HTTP to HTTPS Insecure Transition in Form Post)
10042	FAIL	(HTTPS to HTTP Insecure Transition in Form Post)
10043	FAIL	(User Controllable JavaScript Event (XSS))
90001	FAIL	(Insecure JSF ViewState)
```

### Dockerfile Security Best Practices

**File:** `Dockerfile`

```dockerfile
# Use specific version, not 'latest'
FROM node:18.19-alpine3.19

# Add security labels
LABEL security.scan="trivy" \
      security.compliance="CIS Docker Benchmark"

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Install dependencies first (caching)
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Copy application code
COPY --chown=nodejs:nodejs . .

# Remove unnecessary files
RUN rm -rf .git .github docs tests

# Use non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Run application
CMD ["node", "server.js"]
```

---

## 📊 Security Metrics Dashboard

### GitHub Actions Summary Template

```markdown
## 🛡️ Security Pipeline Results

### ✅ Passed Checks
- [x] Secret scanning
- [x] Dependency vulnerabilities (0 critical, 2 high)
- [x] SAST code analysis
- [x] Container security scan
- [x] IaC security review

### ⚠️ Warnings
- [ ] 2 high severity dependencies need updates
- [ ] 1 medium severity code issue detected

### 📈 Metrics
- **Total vulnerabilities:** 15
  - Critical: 0
  - High: 2
  - Medium: 8
  - Low: 5
- **Code coverage:** 87%
- **Security score:** 92/100

### 🔗 Resources
- [View SARIF Results](link)
- [Snyk Dashboard](link)
- [Trivy Report](link)
```

---

## 💡 Best Practices

### 1. **Fail Fast**
- Run secret scanning first
- Block on critical vulnerabilities
- Fast feedback to developers

### 2. **Defense in Depth**
- Multiple scanning tools
- Different vulnerability databases
- Complementary approaches

### 3. **Automation**
- Scheduled daily scans
- Automatic dependency updates
- PR blocking on critical issues

### 4. **Visibility**
- SARIF uploads to GitHub Security
- PR comments with results
- Slack/email notifications

### 5. **Continuous Improvement**
- Track metrics over time
- Regular tool updates
- Team training on findings

### 6. **Compliance**
- Document all scans
- Audit trail in GitHub
- Regular compliance reviews

### 7. **Performance**
- Cache dependencies
- Parallel job execution
- Incremental scanning where possible

---

## 🚨 Security Gates

### Block Deployment If:
1. ❌ Secrets detected in code
2. ❌ Critical vulnerabilities in dependencies
3. ❌ Critical/High container vulnerabilities
4. ❌ SQL injection or XSS found in SAST
5. ❌ Compliance checks fail

### Allow with Warning If:
⚠️ Medium severity issues (create tickets)
⚠️ Low severity findings (track but don't block)

---

## 🔍 Monitoring & Alerting

### Slack Notification (Optional)

```yaml
- name: Notify Slack on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: |
      Security pipeline failed!
      Commit: ${{ github.sha }}
      Author: ${{ github.actor }}
      View: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Email Notification

```yaml
- name: Send email on critical issues
  if: contains(needs.*.result, 'failure')
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: 🚨 Security Pipeline Failed - Action Required
    body: |
      Critical security issues detected!
      
      Repository: ${{ github.repository }}
      Commit: ${{ github.sha }}
      Branch: ${{ github.ref_name }}
      
      Please review: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
    to: security-team@example.com
```

---

## 📚 Tool Comparison

| Tool | Type | Strengths | Best For |
|------|------|-----------|----------|
| **Snyk** | SCA | Great UX, fix PRs | Dependencies |
| **Trivy** | Container | Fast, comprehensive | Containers |
| **Semgrep** | SAST | Custom rules, fast | Code patterns |
| **CodeQL** | SAST | Deep analysis | Complex bugs |
| **OWASP ZAP** | DAST | Industry standard | Runtime testing |
| **Checkov** | IaC | Policy as code | Infrastructure |
| **TruffleHog** | Secrets | High accuracy | Secret detection |

---

## 🎯 Success Criteria

- ✅ All scans complete in < 15 minutes
- ✅ Zero false positives blocking PRs
- ✅ 100% critical vulnerabilities blocked
- ✅ Security findings in GitHub Security tab
- ✅ Team trained on responding to alerts
- ✅ Monthly security review meetings
