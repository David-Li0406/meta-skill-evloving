# Job Queue Management

## Background Job System

Frappe uses Redis Queue (RQ) for background job processing. Jobs are distributed across different queues based on priority and execution time.

### Queue Types

- **short**: Quick tasks (< 5 minutes)
- **default**: Normal tasks (5-30 minutes)
- **long**: Long-running tasks (> 30 minutes)

## Worker Management

### Start Background Workers

```bash
# Start worker for all queues
bench --site development.localhost worker

# Start worker for specific queue
bench --site development.localhost worker --queue short

# Start worker for multiple queues
bench --site development.localhost worker --queue short,default

# Start in burst mode (process existing jobs then exit)
bench --site development.localhost worker --burst

# Start with Redis authentication
bench --site development.localhost worker \
  --rq-username myuser \
  --rq-password mypassword

# Quiet mode (less logging)
bench --site development.localhost worker --quiet

# Choose dequeuing strategy
bench --site development.localhost worker --strategy round_robin
bench --site development.localhost worker --strategy random
```

**Worker Options:**
- `--queue TEXT`: Specific queue(s) to process (comma-separated)
- `--quiet`: Hide log outputs
- `--burst`: Process all pending jobs then exit
- `--strategy`: How to pick from multiple queues
  - `round_robin`: Fair distribution (default)
  - `random`: Random selection

**Use cases:**
- **Development**: Single worker with `--burst` for testing
- **Production**: Multiple workers per queue for throughput
- **Debugging**: Single queue worker with verbose output

### Start Worker Pool

```bash
# Start worker pool (multiple workers)
bench --site development.localhost worker-pool

# Specify number of workers
bench --site development.localhost worker-pool --num-workers 4

# Worker pool for specific queues
bench --site development.localhost worker-pool \
  --queue long \
  --num-workers 2

# Burst mode pool
bench --site development.localhost worker-pool \
  --num-workers 3 \
  --burst

# Quiet mode
bench --site development.localhost worker-pool --quiet
```

**Worker Pool Options:**
- `--num-workers INTEGER`: Number of worker processes to spawn
- `--queue TEXT`: Queue(s) to process
- `--quiet`: Hide log outputs
- `--burst`: Process pending jobs then exit

**Best practices:**
```bash
# Production setup (in Procfile or supervisor):
# Short queue: 2 fast workers
worker_short: bench worker --queue short

# Default queue: 3 workers
worker_default: bench worker --queue default

# Long queue: 2 workers with pool
worker_long: bench worker-pool --queue long --num-workers 2
```

## Scheduler Management

### Control Scheduler

```bash
# Enable scheduler (start processing scheduled jobs)
bench --site development.localhost enable-scheduler

# Disable scheduler (stop processing)
bench --site development.localhost disable-scheduler

# Check scheduler status
bench --site development.localhost scheduler status

# Verbose status
bench --site development.localhost scheduler status --verbose

# Status in JSON format
bench --site development.localhost scheduler status --format json

# Pause scheduler (temporarily)
bench --site development.localhost scheduler pause

# Resume scheduler
bench --site development.localhost scheduler resume
```

**Scheduler States:**
- **enabled**: Active, jobs run on schedule
- **disabled**: Inactive, no jobs run
- **paused**: Temporarily stopped, can resume
- **resumed**: Reactivated after pause

**Status output example:**
```
Scheduler: enabled
Last executed: 2026-01-13 14:30:00
Pending events: 3
Failed jobs: 0
```

### Start Scheduler Process

```bash
# Start scheduler process (usually done by bench start)
bench --site development.localhost schedule
```

**Note:** This command is typically run automatically by `bench start` in development or supervisor/systemd in production. Don't run manually unless needed.

## Job Queue Diagnostics

### View Pending Jobs

```bash
# Show pending jobs for all queues
bench --site development.localhost show-pending-jobs

# Show for specific site
bench --site production.example.com show-pending-jobs
```

**Output example:**
```
Queue: short
  - pending: 5
  - failed: 0
  - started: 2

Queue: default
  - pending: 12
  - failed: 1
  - started: 1

Queue: long
  - pending: 3
  - failed: 0
  - started: 1

Total pending: 20
Total failed: 1
Total processing: 4
```

### Full System Diagnostics

```bash
# Complete worker and queue diagnostics
bench --site development.localhost doctor
```

**What it shows:**
- Site health status
- Scheduler status
- Worker status
- Queue statistics
- Failed job count
- Redis connectivity
- Database status

**Example output:**
```
Site: development.localhost
Status: active

Scheduler: enabled
Last run: 2 minutes ago

Workers:
  - short queue: 1 worker active
  - default queue: 2 workers active
  - long queue: 1 worker active

Queues:
  - short: 3 pending
  - default: 8 pending
  - long: 1 pending

Failed jobs: 0
Redis: connected
Database: connected
```

### Purge Jobs

```bash
# Purge all pending jobs
bench --site development.localhost purge-jobs

# Purge specific queue
bench --site development.localhost purge-jobs --queue default

# Purge specific event type
bench --site development.localhost purge-jobs --event daily
bench --site development.localhost purge-jobs --event hourly
bench --site development.localhost purge-jobs --event all

# Purge everything
bench --site development.localhost purge-jobs --event all
```

**Event types:**
- `all`: All scheduled events
- `hourly`: Jobs scheduled every hour
- `daily`: Jobs scheduled daily
- `weekly`: Jobs scheduled weekly
- `monthly`: Jobs scheduled monthly
- `weekly_long`: Long-running weekly jobs
- `daily_long`: Long-running daily jobs

**Use cases:**
- Clean up stuck jobs
- Reset job queue during development
- Remove old scheduled jobs
- Testing job scheduling

## Scheduled Job Management

### Trigger Scheduler Events

```bash
# Manually trigger specific event
bench --site development.localhost trigger-scheduler-event daily
bench --site development.localhost trigger-scheduler-event hourly
bench --site development.localhost trigger-scheduler-event weekly

# Trigger all events
bench --site development.localhost trigger-scheduler-event all
```

**Use when:**
- Testing scheduled jobs
- Running missed jobs
- Development/debugging
- Recovery after downtime

### Publish Realtime Events

```bash
# Publish realtime event
bench --site development.localhost publish-realtime my_event \
  --message "Test message" \
  --room "user:admin@example.com"

# Publish to specific user
bench --site development.localhost publish-realtime notification \
  --message "New order" \
  --user "admin@example.com"

# Publish for specific document
bench --site development.localhost publish-realtime doc_update \
  --doctype "Sales Order" \
  --docname "SO-2024-00001"
```

**Options:**
- `--message TEXT`: Event message/data
- `--room TEXT`: Socket.io room
- `--user TEXT`: Specific user
- `--doctype TEXT`: Document type
- `--docname TEXT`: Document name
- `--after-commit TEXT`: Execute after DB commit

## Development Workflows

### Testing Background Jobs

```bash
# 1. Disable scheduler to control execution
bench --site development.localhost disable-scheduler

# 2. Clear any pending jobs
bench --site development.localhost purge-jobs --event all

# 3. Enqueue your test job (via console or code)
bench --site development.localhost console
>>> frappe.enqueue('my_module.my_function', queue='short')

# 4. Process jobs in burst mode
bench --site development.localhost worker --queue short --burst

# 5. Check for errors
bench --site development.localhost show-pending-jobs
```

### Debugging Failed Jobs

```bash
# 1. Check system status
bench --site development.localhost doctor

# 2. View pending/failed jobs
bench --site development.localhost show-pending-jobs

# 3. Start worker with verbose output (no quiet)
bench --site development.localhost worker --queue default

# 4. Check Redis directly
bench --site development.localhost console
>>> from rq import Queue
>>> from frappe.utils.background_jobs import get_redis_conn
>>> conn = get_redis_conn()
>>> q = Queue('default', connection=conn)
>>> q.failed_job_registry.get_job_ids()

# 5. Clear failed jobs
bench --site development.localhost purge-jobs --queue default
```

### Production Worker Setup

**Using Supervisor (recommended):**

Create `/etc/supervisor/conf.d/frappe-workers.conf`:
```ini
[program:frappe-worker-short]
command=/path/to/bench/env/bin/bench worker --site production.site --queue short
directory=/path/to/bench
autostart=true
autorestart=true
stopwaitsecs=30
user=frappe

[program:frappe-worker-default]
command=/path/to/bench/env/bin/bench worker --site production.site --queue default
directory=/path/to/bench
autostart=true
autorestart=true
stopwaitsecs=60
user=frappe
numprocs=2
process_name=%(program_name)s-%(process_num)d

[program:frappe-worker-long]
command=/path/to/bench/env/bin/bench worker-pool --site production.site --queue long --num-workers 2
directory=/path/to/bench
autostart=true
autorestart=true
stopwaitsecs=300
user=frappe
```

Reload supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
```

## Monitoring and Maintenance

### Regular Health Checks

```bash
# Daily check
bench --site production.example.com doctor

# Check pending jobs
bench --site production.example.com show-pending-jobs

# Verify scheduler
bench --site production.example.com scheduler status
```

### Clean Up Stuck Jobs

```bash
# 1. Identify the problem
bench --site development.localhost show-pending-jobs

# 2. Stop workers (in production, use supervisor)
sudo supervisorctl stop frappe-worker:*

# 3. Purge problematic queue
bench --site development.localhost purge-jobs --queue long

# 4. Restart workers
sudo supervisorctl start frappe-worker:*

# 5. Verify
bench --site development.localhost show-pending-jobs
```

### Performance Optimization

```bash
# Monitor queue depth
watch -n 5 'bench --site development.localhost show-pending-jobs'

# If queues are backing up:

# Option 1: Add more workers
bench --site development.localhost worker-pool --num-workers 4

# Option 2: Process with burst mode
bench --site development.localhost worker --queue default --burst

# Option 3: Scale horizontally (multiple servers)
# Start workers on different servers with same Redis
```

## Troubleshooting

### Workers Not Processing Jobs

```bash
# Check if workers are running
ps aux | grep "bench worker"

# Check Redis connectivity
bench --site development.localhost console
>>> import redis
>>> frappe.cache().ping()

# Restart workers
# Development:
# Stop bench start, then restart

# Production:
sudo supervisorctl restart frappe-worker:*

# Check for errors
tail -f logs/worker.error.log
```

### Scheduler Not Running

```bash
# Check status
bench --site development.localhost scheduler status

# Enable if disabled
bench --site development.localhost enable-scheduler

# Check if schedule process is running
ps aux | grep "bench schedule"

# In production, check supervisor
sudo supervisorctl status frappe-schedule
```

### Jobs Stuck in Queue

```bash
# Check pending jobs
bench --site development.localhost show-pending-jobs

# View doctor output
bench --site development.localhost doctor

# Purge and restart
bench --site development.localhost purge-jobs --queue default
bench --site development.localhost worker --queue default --burst

# If persistent, check Redis
bench --site development.localhost console
>>> frappe.cache().flushall()  # Careful! Clears all cache
```

### High Memory Usage

```bash
# Check worker memory
ps aux | grep worker | awk '{print $4, $11}'

# Restart workers periodically (in production)
# Add to cron: restart workers every 6 hours

# Use burst mode for controlled memory usage
bench --site development.localhost worker --burst

# Scale with more smaller workers instead of fewer large ones
bench --site development.localhost worker-pool --num-workers 4
```
