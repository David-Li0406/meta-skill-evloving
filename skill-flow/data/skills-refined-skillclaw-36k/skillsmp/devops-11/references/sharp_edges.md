# Devops - Sharp Edges

## Missing Health Check

### **Id**
missing-health-check
### **Summary**
Load balancer sends traffic to containers that aren't ready
### **Severity**
critical
### **Situation**
Deploying containers without readiness probes, using basic "is process running" checks
### **Why**
  Container is running but app is still connecting to database, loading config,
  warming caches. Users hit a broken service. Or container is OOM but process
  still running - just failing every request.
  
### **Solution**
  # WRONG - Only checks if container is running
  healthcheck:
    test: ["CMD", "echo", "healthy"]
  
  # RIGHT - Checks if app is actually ready
  livenessProbe:
    httpGet:
      path: /health/live
      port: 3000
    initialDelaySeconds: 10
  
  readinessProbe:
    httpGet:
      path: /health/ready
      port: 3000
    initialDelaySeconds: 5
  
  # Application health endpoint checks dependencies
  app.get('/health/ready', async (req, res) => {
    await db.query('SELECT 1')
    await redis.ping()
    res.json({ status: 'healthy' })
  })
  
### **Symptoms**
  - 502/503 errors after deploy
  - Traffic to containers during startup
  - Containers marked healthy but failing requests
### **Detection Pattern**
healthcheck:.*echo.*healthy|livenessProbe:(?![\\s\\S]*readinessProbe)

## Secrets In Repo

### **Id**
secrets-in-repo
### **Summary**
Credentials committed to git history (forever retrievable)
### **Severity**
critical
### **Situation**
API keys, passwords, tokens in code, .env, or terraform.tfvars committed to repo
### **Why**
  Git history is forever. Even after rotation, keys are in history. Repo becomes
  public or attacker gains read access. Single commit exposes all production creds.
  "Temporarily" committed becomes permanent.
  
### **Solution**
  # .gitignore
  .env
  .env.*
  *.tfvars
  secrets/
  
  # .env.example (commit this, no real values)
  DATABASE_URL=postgres://user:pass@localhost/dev
  
  # Use secret managers
  # AWS: Secrets Manager, Parameter Store
  # GCP: Secret Manager
  # GitHub Actions:
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  
  # Pre-commit hook with gitleaks or trufflehog
  
### **Symptoms**
  - Strings that look like API keys in code
  - .env files in git history
  - No secret scanning in CI
### **Detection Pattern**
sk_live_|AKIA[A-Z0-9]{16}|password\s*=\s*['"][^'"]{8,}

## Unbounded Resources

### **Id**
unbounded-resources
### **Summary**
No limits on containers/auto-scaling causes cost explosion or node crashes
### **Severity**
high
### **Situation**
Containers without memory/CPU limits, auto-scaling without max instances
### **Why**
  One runaway container uses all node memory, killing other pods. Traffic spike
  scales to 1000 instances, $100K surprise bill. No limits means no predictability.
  
### **Solution**
  # WRONG - No limits
  resources: {}
  
  # RIGHT - Always set limits
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  
  # Auto-scaling with bounds
  spec:
    minReplicas: 2
    maxReplicas: 10  # Cap the scaling!
  
  # Budget alerts
  resource "aws_budgets_budget" "monthly" {
    budget_type  = "COST"
    limit_amount = "1000"
    limit_unit   = "USD"
  }
  
### **Symptoms**
  - OOMKilled in pod events
  - Unexpected cost spikes
  - Missing resource limits in manifests
### **Detection Pattern**
resources:\\s*\\{\\}|maxReplicas:\\s*(?:100|1000)|maxReplicas:(?!\\s*\\d)

## Single Point Of Failure

### **Id**
single-point-of-failure
### **Summary**
One component failure takes down entire system
### **Severity**
critical
### **Situation**
Single database instance, single AZ deployment, single replica pods
### **Why**
  That one thing will fail. AWS AZ goes down. Database disk fails. Network partition.
  With no redundancy, you're down until it recovers or you manually intervene.
  
### **Solution**
  # WRONG - Single AZ
  resource "aws_instance" "web" {
    availability_zone = "us-east-1a"
  }
  
  # RIGHT - Multi-AZ
  resource "aws_db_instance" "main" {
    multi_az = true
  }
  
  resource "aws_autoscaling_group" "web" {
    availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
    min_size = 2  # At least 2 for redundancy
  }
  
  # Kubernetes - pod anti-affinity
  spec:
    affinity:
      podAntiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
        - topologyKey: "topology.kubernetes.io/zone"
  
### **Symptoms**
  - Resources in single AZ
  - Single replica/instance counts
  - Blast radius = everything
### **Detection Pattern**
replicas:\\s*1|min_size\\s*=\\s*1|minReplicas:\\s*1

## No Rollback Plan

### **Id**
no-rollback-plan
### **Summary**
Broken deploy with no tested way to roll back
### **Severity**
critical
### **Situation**
Deploying without rollback procedure, forward-only database migrations
### **Why**
  Deploy breaks. How do you roll back? Find old Docker tag? Reverse migrations?
  Hope database is backwards compatible? Every minute of figuring this out is
  downtime for users.
  
### **Solution**
  # Kubernetes - built-in rollback
  kubectl rollout undo deployment/web
  
  # Keep revision history
  spec:
    revisionHistoryLimit: 10
  
  # Database migrations - make reversible
  exports.up = async (db) => {
    await db.schema.alterTable('users', t => {
      t.string('phone').nullable()  # Nullable = backwards compatible
    })
  }
  
  exports.down = async (db) => {
    await db.schema.alterTable('users', t => {
      t.dropColumn('phone')
    })
  }
  
  # Automated rollback in CI
  - name: Rollback on failure
    if: failure()
    run: kubectl rollout undo deployment/web
  
### **Symptoms**
  - No rollback procedure documented
  - Migrations are forward-only
  - No version history kept
### **Detection Pattern**
revisionHistoryLimit:\\s*0|exports\\.down.*throw

## Log Black Hole

### **Id**
log-black-hole
### **Summary**
Logs lost when container dies or scattered across servers
### **Severity**
high
### **Situation**
Logging only to local filesystem, no centralized aggregation
### **Why**
  Container dies, logs gone. Incident happens, SSH to 50 servers to find relevant logs.
  500GB of logs, can't grep fast enough. Unstructured logs impossible to query.
  
### **Solution**
  # Ship logs to central system
  services:
    web:
      logging:
        driver: "json-file"
        options:
          max-size: "10m"
          max-file: "3"
  
  # Structured logging
  logger.info({
    event: 'order_created',
    orderId: order.id,
    userId: user.id
  }, 'Order created')
  
  # NOT: console.log('Order created: ' + order.id)
  
  # Use: ELK, Loki, CloudWatch, Datadog
  
### **Symptoms**
  - No centralized logging
  - Logs only on container filesystem
  - Unstructured console.log everywhere
### **Detection Pattern**
console\.log\([^)]*\+|console\.log\(`

## Terraform Local State

### **Id**
terraform-local-state
### **Summary**
Terraform state file on local disk or committed to repo
### **Severity**
critical
### **Situation**
Running terraform apply locally, state file in git, no state locking
### **Why**
  Two people run apply simultaneously - state conflict, corrupted infrastructure.
  Laptop lost - state gone, can't manage infrastructure. State has secrets in plain text.
  
### **Solution**
  # WRONG - Local state (default)
  # State on your laptop, secrets exposed
  
  # RIGHT - Remote state with locking
  terraform {
    backend "s3" {
      bucket         = "company-terraform-state"
      key            = "prod/infrastructure.tfstate"
      region         = "us-east-1"
      encrypt        = true
      dynamodb_table = "terraform-locks"
    }
  }
  
  # .gitignore
  *.tfstate
  *.tfstate.*
  .terraform/
  *.tfvars
  
  # Run terraform only in CI, never locally for prod
  
### **Symptoms**
  - "*.tfstate" files in repo
  - No remote backend configured
  - Multiple people running apply locally
### **Detection Pattern**
\\.tfstate|backend.*local

## Exposed Database

### **Id**
exposed-database
### **Summary**
Database accessible from public internet
### **Severity**
critical
### **Situation**
Database with public IP, security group allowing 0.0.0.0/0
### **Why**
  Attacker scans internet, finds your database, brute forces or exploits vulnerability.
  "It's password protected" doesn't stop automated attacks. Single compromise exposes
  all data.
  
### **Solution**
  # WRONG - Database publicly accessible
  resource "aws_db_instance" "main" {
    publicly_accessible = true
  }
  
  resource "aws_security_group_rule" "db" {
    cidr_blocks = ["0.0.0.0/0"]  # Internet-accessible!
  }
  
  # RIGHT - Private subnet, app-only access
  resource "aws_db_instance" "main" {
    publicly_accessible = false
    db_subnet_group_name = aws_db_subnet_group.private.name
  }
  
  resource "aws_security_group" "db" {
    ingress {
      from_port       = 5432
      security_groups = [aws_security_group.app.id]  # Only app servers
    }
  }
  
  # For local dev: VPN, bastion host, or SSM tunnels
  
### **Symptoms**
  - publicly_accessible = true
  - Security group with 0.0.0.0/0 on DB port
  - Database has public IP
### **Detection Pattern**
publicly_accessible\\s*=\\s*true|cidr_blocks.*0\\.0\\.0\\.0/0.*5432

## Missing Monitoring

### **Id**
missing-monitoring
### **Summary**
No visibility into system health until users complain
### **Severity**
high
### **Situation**
No metrics collection, no alerting, or too many alerts to act on
### **Why**
  Customer tweets "your site is down" before you know. Check monitoring - there is none.
  Or alerts go to email nobody reads. Or so many alerts everyone ignores them.
  
### **Solution**
  # Core metrics (RED method):
  # Rate - requests per second
  # Errors - error percentage
  # Duration - latency percentiles
  
  # Prometheus alert
  - alert: HighErrorRate
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m])) > 0.05
    for: 5m
    labels:
      severity: critical
  
  # Alert hygiene:
  # If alert doesn't need action → delete it
  # If alert fires too often → tune threshold or fix root cause
  
### **Symptoms**
  - No monitoring dashboard
  - Alerts go to email only
  - Alert:action ratio is low
### **Detection Pattern**


## Unbacked Up Database

### **Id**
unbacked-up-database
### **Summary**
Database backups not configured or never tested
### **Severity**
critical
### **Situation**
Relying on cloud provider defaults, never testing restore procedure
### **Why**
  Disk fails. Ransomware encrypts everything. Developer runs DELETE without WHERE.
  Where's the backup? When was it tested? Can you actually restore? What's the RPO?
  
### **Solution**
  # Automated backups with retention
  resource "aws_db_instance" "main" {
    backup_retention_period = 30
    backup_window           = "03:00-04:00"
    deletion_protection     = true
  }
  
  # Test restore quarterly:
  # 1. Restore snapshot to new instance
  # 2. Verify data integrity
  # 3. Run application against restored DB
  # 4. Measure restore time (RTO)
  
  # Cross-region replication for DR
  
### **Symptoms**
  - No backup retention configured
  - Backups never tested
  - No documented restore procedure
### **Detection Pattern**
backup_retention_period\\s*=\\s*0|backup_retention_period:(?!\\s*\\d)

## Unpinned Dependencies

### **Id**
unpinned-dependencies
### **Summary**
Build uses unpinned versions, causing inconsistent deployments
### **Severity**
high
### **Situation**
Using :latest Docker tags, npm install instead of npm ci, no lock files
### **Why**
  Today installs 1.2.3, tomorrow 1.2.4 with breaking change. Same code, different
  results. Build worked yesterday, fails today. "Works on my machine."
  
### **Solution**
  # WRONG
  FROM node:latest
  RUN npm install
  
  # RIGHT
  FROM node:20.11.0-alpine3.19
  COPY package.json package-lock.json ./
  RUN npm ci  # Uses exact versions from lock file
  
  # Lock files must be committed:
  # package-lock.json (npm)
  # yarn.lock (yarn)
  # pnpm-lock.yaml (pnpm)
  
  # Use Renovate/Dependabot for updates with PRs
  
### **Symptoms**
  - :latest Docker tags
  - No lock files committed
  - npm install instead of npm ci
  - Random build failures
### **Detection Pattern**
FROM\\s+\\w+:latest|npm install(?!.*ci)

## Yolo Deploy

### **Id**
yolo-deploy
### **Summary**
Direct push to production with no testing or approval gates
### **Severity**
critical
### **Situation**
Auto-deploy on push to main, no staging, no smoke tests
### **Why**
  Bug goes to 100% of users instantly. No time to catch issues before impact.
  Rollback is panic mode. Security vulnerability deployed before anyone notices.
  
### **Solution**
  # RIGHT - Pipeline with gates
  jobs:
    test:
      steps:
        - run: npm test
        - run: npm run lint
  
    deploy-staging:
      needs: test
      environment: staging
  
    smoke-test:
      needs: deploy-staging
      steps:
        - run: ./smoke-tests.sh https://staging.app.com
  
    deploy-production:
      needs: smoke-test
      environment: production  # Manual approval
  
  # Canary: 5% → 25% → 50% → 100%
  # Automatic rollback if errors spike
  
### **Symptoms**
  - Direct push to main allowed
  - No staging environment
  - No tests in pipeline
  - 100% traffic immediately
### **Detection Pattern**
on:\\s*push:\\s*branches:\\s*\\[main\\](?![\\s\\S]*environment:.*production)