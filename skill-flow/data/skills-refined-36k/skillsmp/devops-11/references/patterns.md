# DevOps Engineering

## Patterns


---
  #### **Name**
Infrastructure as Code
  #### **Description**
All infrastructure defined in version-controlled code, never manual changes
  #### **When**
Setting up any cloud resources, environments, or deployment infrastructure
  #### **Example**
    # Terraform - declarative infrastructure
    resource "aws_db_instance" "main" {
      identifier          = "prod-db"
      engine              = "postgres"
      instance_class      = "db.t3.medium"
      allocated_storage   = 100
      multi_az            = true
      backup_retention_period = 30
    }
    
    # Benefits:
    # - Repeatable across environments
    # - Code review for infrastructure changes
    # - Rollback by reverting commits
    # - Documentation as code
    

---
  #### **Name**
Blue-Green Deployment
  #### **Description**
Run two identical environments, switch traffic between them for zero-downtime deploys
  #### **When**
Deploying to production, need instant rollback, can't afford downtime
  #### **Example**
    # Deploy to Green (new version)
    kubectl apply -f deployment-green.yaml
    
    # Test Green environment
    ./smoke-tests.sh https://green.app.com
    
    # Switch traffic to Green
    kubectl patch service app -p '{"spec":{"selector":{"version":"green"}}}'
    
    # Keep Blue running for rollback
    # If problems: switch back to Blue instantly
    

---
  #### **Name**
GitOps
  #### **Description**
Git as single source of truth, all changes through PRs, automated sync to clusters
  #### **When**
Managing Kubernetes deployments, need audit trail, multiple environments
  #### **Example**
    # Directory structure
    clusters/
      production/
        apps/
          web.yaml
          api.yaml
      staging/
        apps/
          web.yaml
    
    # ArgoCD watches repo, syncs automatically
    # All changes via PR → review → merge → auto-deploy
    

---
  #### **Name**
Observability Stack
  #### **Description**
Metrics, logs, and traces unified for understanding system behavior
  #### **When**
Running production systems, debugging issues, capacity planning
  #### **Example**
    # Three pillars:
    # Metrics (Prometheus) - what is happening
    # Logs (Loki/ELK) - why it's happening
    # Traces (Jaeger) - where it's happening
    
    # RED metrics for every service:
    # Rate - requests per second
    # Errors - error percentage
    # Duration - latency percentiles
    

---
  #### **Name**
Canary Deployments
  #### **Description**
Gradually shift traffic to new version, automatic rollback on errors
  #### **When**
High-risk deployments, need to catch issues before full rollout
  #### **Example**
    # Stage 1: 5% traffic to new version
    # Monitor for 15 minutes
    # Stage 2: 25% traffic
    # Stage 3: 50% traffic
    # Stage 4: 100% traffic
    
    # If error rate spikes at any stage → automatic rollback
    

---
  #### **Name**
Immutable Infrastructure
  #### **Description**
Never modify running servers, always replace with new ones from images
  #### **When**
Deploying updates, scaling, ensuring consistency
  #### **Example**
    # WRONG - SSH in and update
    ssh server && apt-get update && apt-get upgrade
    
    # RIGHT - Build new image, deploy, destroy old
    docker build -t app:v2 .
    kubectl set image deployment/app app=app:v2
    # Old pods terminated, new pods started
    

## Anti-Patterns


---
  #### **Name**
Snowflake Servers
  #### **Description**
Manually configured servers that can't be reproduced
  #### **Why**
Can't recreate if they fail. No one knows what's installed. Configuration drift. Fear of updates.
  #### **Instead**
Infrastructure as code. Immutable images. Configuration management.

---
  #### **Name**
YOLO Deploy
  #### **Description**
Direct push to main deploys to production with no gates
  #### **Why**
Bugs hit 100% of users instantly. No time to catch issues. Rollback panic.
  #### **Instead**
Staging environment, automated tests, canary deployments, manual approval gate.

---
  #### **Name**
Secrets in Repo
  #### **Description**
Passwords, API keys, credentials committed to git
  #### **Why**
Git history is forever. Anyone with repo access has prod creds. Single breach exposes everything.
  #### **Instead**
Secret managers (AWS Secrets Manager, Vault). Environment variables from CI. Never commit .env files.

---
  #### **Name**
No Resource Limits
  #### **Description**
Containers without CPU/memory limits, auto-scaling without max
  #### **Why**
One runaway container kills the node. Traffic spike scales to 1000 instances, $100K bill.
  #### **Instead**
Always set resource limits. Always cap auto-scaling max. Set cost alerts.

---
  #### **Name**
Alert Fatigue
  #### **Description**
So many alerts that all are ignored
  #### **Why**
When everything alerts, nothing alerts. Real issues get missed in noise.
  #### **Instead**
If alert doesn't need action, delete it. Tune thresholds. Only page on critical.

---
  #### **Name**
Local Terraform State
  #### **Description**
Terraform state file on local machine or in repo
  #### **Why**
State conflict when team runs apply. State loss when laptop lost. Secrets in plain text.
  #### **Instead**
Remote backend (S3 + DynamoDB). State locking. Never commit state files.