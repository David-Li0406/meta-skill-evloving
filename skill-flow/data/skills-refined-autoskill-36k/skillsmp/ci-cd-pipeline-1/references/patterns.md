# CI/CD Pipeline

## Patterns


---
  #### **Name**
Secure GitHub Actions Workflow
  #### **Description**
Production-ready workflow with security hardening
  #### **When**
Any GitHub Actions workflow that touches production
  #### **Example**
    name: Deploy to Production
    
    on:
      push:
        branches: [main]
      workflow_dispatch:
    
    # Explicit permissions - never use defaults
    permissions:
      contents: read
      id-token: write  # For OIDC
    
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4  # Pin to major version minimum
    
          - name: Run tests
            run: npm test
    
      deploy:
        needs: test
        runs-on: ubuntu-latest
        environment: production  # Requires approval
        steps:
          - uses: actions/checkout@v4
    
          # Use OIDC instead of long-lived secrets
          - name: Configure AWS credentials
            uses: aws-actions/configure-aws-credentials@v4
            with:
              role-to-assume: arn:aws:iam::123456789:role/deploy-role
              aws-region: us-east-1
    
          - name: Deploy
            run: |
              # Never echo secrets
              aws s3 sync ./dist s3://my-bucket
    

---
  #### **Name**
Blue-Green Deployment
  #### **Description**
Zero-downtime deployment with instant rollback capability
  #### **When**
Production deployments that cannot tolerate downtime
  #### **Example**
    # Blue-Green with AWS ECS
    name: Blue-Green Deploy
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
        environment: production
        steps:
          - name: Deploy to green environment
            run: |
              # Update green task definition
              aws ecs update-service \
                --cluster production \
                --service api-green \
                --task-definition api:${{ github.sha }}
    
          - name: Wait for green healthy
            run: |
              aws ecs wait services-stable \
                --cluster production \
                --services api-green
    
          - name: Run smoke tests on green
            run: |
              curl -f https://green.api.example.com/health
    
          - name: Switch traffic to green
            run: |
              # Update load balancer to point to green
              aws elbv2 modify-listener \
                --listener-arn $LISTENER_ARN \
                --default-actions Type=forward,TargetGroupArn=$GREEN_TG
    
          - name: Keep blue for rollback
            run: |
              echo "Blue environment preserved for 1 hour rollback window"
              # Don't destroy blue immediately
    
    # Rollback workflow
    # name: Rollback to Blue
    # on: workflow_dispatch
    # jobs:
    #   rollback:
    #     steps:
    #       - name: Switch traffic to blue
    #         run: aws elbv2 modify-listener ... $BLUE_TG
    

---
  #### **Name**
Canary Deployment
  #### **Description**
Gradual rollout with automated rollback on errors
  #### **When**
High-risk changes, want to limit blast radius
  #### **Example**
    name: Canary Deploy
    
    jobs:
      deploy-canary:
        runs-on: ubuntu-latest
        steps:
          - name: Deploy canary (5% traffic)
            run: |
              kubectl set image deployment/api \
                api=myapp:${{ github.sha }} \
                --record
    
              kubectl patch deployment api -p '
                {"spec": {"strategy": {"rollingUpdate": {"maxSurge": 1, "maxUnavailable": 0}}}}'
    
          - name: Monitor canary metrics
            run: |
              # Query Prometheus/Datadog for error rates
              sleep 300  # 5 minute observation window
    
              ERROR_RATE=$(curl -s "prometheus/query?query=rate(http_errors[5m])")
              if [ "$ERROR_RATE" -gt "0.01" ]; then
                echo "Error rate too high, rolling back"
                kubectl rollout undo deployment/api
                exit 1
              fi
    
          - name: Promote to 25%
            run: |
              # Increase canary traffic
              kubectl scale deployment/api-canary --replicas=5
    
          # Continue progressive rollout...
    
          - name: Full rollout
            if: success()
            run: |
              kubectl rollout status deployment/api
    

---
  #### **Name**
Build Caching Strategy
  #### **Description**
Optimize build times with proper caching
  #### **When**
Builds taking too long, CI costs too high
  #### **Example**
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
    
          # Cache node_modules
          - name: Cache dependencies
            uses: actions/cache@v4
            with:
              path: ~/.npm
              key: npm-${{ hashFiles('**/package-lock.json') }}
              restore-keys: |
                npm-
    
          # Cache Docker layers
          - name: Set up Docker Buildx
            uses: docker/setup-buildx-action@v3
    
          - name: Build and push
            uses: docker/build-push-action@v5
            with:
              context: .
              push: true
              tags: myapp:${{ github.sha }}
              cache-from: type=gha
              cache-to: type=gha,mode=max
    
          # For monorepos - only build what changed
          - name: Get changed files
            id: changed
            uses: tj-actions/changed-files@v44
    
          - name: Build affected packages
            run: |
              npx nx affected --target=build
    

---
  #### **Name**
Environment Promotion
  #### **Description**
Safe promotion from staging to production with gates
  #### **When**
Multi-environment deployment pipeline
  #### **Example**
    name: Environment Promotion
    
    on:
      push:
        branches: [main]
    
    jobs:
      build:
        runs-on: ubuntu-latest
        outputs:
          image-tag: ${{ steps.build.outputs.tag }}
        steps:
          - name: Build image
            id: build
            run: |
              TAG="${{ github.sha }}"
              docker build -t myapp:$TAG .
              docker push myapp:$TAG
              echo "tag=$TAG" >> $GITHUB_OUTPUT
    
      deploy-staging:
        needs: build
        runs-on: ubuntu-latest
        environment: staging
        steps:
          - name: Deploy to staging
            run: |
              kubectl set image deployment/api api=myapp:${{ needs.build.outputs.image-tag }}
    
          - name: Run integration tests
            run: |
              npm run test:integration
    
      deploy-production:
        needs: deploy-staging
        runs-on: ubuntu-latest
        environment: production  # Requires manual approval
        steps:
          - name: Deploy to production
            run: |
              kubectl set image deployment/api api=myapp:${{ needs.build.outputs.image-tag }}
    
          - name: Verify deployment
            run: |
              kubectl rollout status deployment/api --timeout=300s
    

---
  #### **Name**
Reusable Workflow
  #### **Description**
DRY workflows shared across repositories
  #### **When**
Multiple repos with similar CI/CD needs
  #### **Example**
    # .github/workflows/reusable-deploy.yml (in shared repo)
    name: Reusable Deploy
    
    on:
      workflow_call:
        inputs:
          environment:
            required: true
            type: string
          image-tag:
            required: true
            type: string
        secrets:
          AWS_ROLE_ARN:
            required: true
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
        environment: ${{ inputs.environment }}
        steps:
          - uses: aws-actions/configure-aws-credentials@v4
            with:
              role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
              aws-region: us-east-1
    
          - name: Deploy
            run: |
              # Deployment logic here
    
    # Calling workflow (in app repo)
    # jobs:
    #   deploy:
    #     uses: org/shared-workflows/.github/workflows/reusable-deploy.yml@v1
    #     with:
    #       environment: production
    #       image-tag: ${{ github.sha }}
    #     secrets:
    #       AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
    

## Anti-Patterns


---
  #### **Name**
Secrets in Logs
  #### **Description**
Accidentally logging secrets or sensitive data
  #### **Why**
CI logs are often accessible to many people. One echo $SECRET or debug mode and credentials are exposed. Log aggregators persist secrets forever.
  #### **Instead**
Never echo secrets. Use ::add-mask::. Review all log output. Use OIDC instead of long-lived tokens.

---
  #### **Name**
Unpinned Actions
  #### **Description**
Using @main or @latest for third-party actions
  #### **Why**
Supply chain attack vector. Action changes between runs. tj-actions/changed-files attack compromised thousands of repos. Malicious code runs with your secrets.
  #### **Instead**
Pin to specific versions (@v4) or SHA digests. Use Dependabot to update safely. Audit third-party actions.

---
  #### **Name**
Overly Broad Permissions
  #### **Description**
Using default GITHUB_TOKEN permissions or assuming admin
  #### **Why**
Token with write-all can modify repo, push code, access secrets. Compromised workflow becomes full repo takeover. Blast radius is entire organization.
  #### **Instead**
Explicit permissions block. Read-only by default. Least privilege for each job.

---
  #### **Name**
No Rollback Strategy
  #### **Description**
Deploy forward only, no way to quickly revert
  #### **Why**
Bad deploy goes live. Only option is "fix forward" which takes hours. Users suffer. Revenue lost. On-call engineer stressed.
  #### **Instead**
Every deployment must be reversible. Blue-green for instant rollback. Version pinning. Database migrations that support rollback.

---
  #### **Name**
Testing Only in CI
  #### **Description**
Tests only run in CI, not locally by developers
  #### **Why**
Developers push and pray. CI becomes the first feedback. Long cycle times. "It works on my machine" when tests fail in CI.
  #### **Instead**
Tests must run identically locally and in CI. Same Docker images. Same environment variables. Make local testing fast.

---
  #### **Name**
Pipeline Bypasses
  #### **Description**
Allowing deployments outside the CI/CD pipeline
  #### **Why**
Emergency fix deployed via kubectl. No tests ran. No audit trail. "Just this once" becomes habit. Pipeline is optional, not mandatory.
  #### **Instead**
Pipeline is the only way to production. Emergency procedures still go through pipeline (fast-track, not bypass).