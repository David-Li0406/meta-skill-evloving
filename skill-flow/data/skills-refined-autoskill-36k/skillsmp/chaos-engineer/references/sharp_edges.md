# Chaos Engineer - Sharp Edges

## Blast Radius Unknown

### **Id**
blast-radius-unknown
### **Summary**
Chaos experiment affects more than intended, causes outage
### **Severity**
critical
### **Situation**
Running chaos experiment without proper scoping
### **Why**
  "Kill one pod" turns into cascade. That pod held critical connection.
  Downstream services fail. Load balancer removes all instances.
  What was supposed to test one component takes down the whole system.
  
### **Solution**
  1. Always scope to minimum blast radius first:
     # Start with 1 pod, not 50%
     PODS_AFFECTED_PERC: "1"
  
  2. Use namespace/label isolation:
     # Only affect pods with chaos-enabled label
     applabel: "chaos-enabled=true"
  
  3. Define abort conditions:
     # Abort if error rate exceeds threshold
     probe:
       - name: "error-rate-check"
         type: "promProbe"
         promProbe/inputs:
           query: "rate(http_errors[1m])"
           comparator:
             type: ">"
             value: "0.1"  # 10% error rate
  
  4. Test abort mechanism before running:
     # Verify kill switch works
     curl -X POST /chaos/abort
  
### **Symptoms**
  - "Simple experiment" caused major outage
  - Unrelated services affected
  - Experiment couldn't be stopped quickly
### **Detection Pattern**
blast.*radius|scope|affected.*percent|PODS_AFFECTED

## Steady State Not Defined

### **Id**
steady-state-not-defined
### **Summary**
Can't tell if chaos caused problem or problem existed before
### **Severity**
high
### **Situation**
Running chaos without baseline measurements
### **Why**
  Error rate during chaos: 5%. Was that because of chaos, or was it
  already 5%? Without steady state, you can't measure impact.
  You might celebrate success when system was already broken.
  
### **Solution**
  1. Define steady state metrics before experiment:
     steady_state:
       - metric: "http_success_rate"
         expected: "> 99.9%"
       - metric: "p99_latency_ms"
         expected: "< 500"
  
  2. Verify steady state before injecting chaos:
     async def pre_chaos_check():
         success_rate = await get_metric("http_success_rate")
         if success_rate < 0.999:
             raise SteadyStateNotMet("Can't run chaos, system unstable")
  
  3. Compare during/after to baseline:
     # Baseline: 99.95% success
     # During chaos: 98.2% success
     # Impact: -1.75% (acceptable?)
  
  4. Record steady state in experiment report:
     ## Baseline (pre-chaos)
     - Success rate: 99.95%
     - P99 latency: 342ms
     - Error types: [none]
  
### **Symptoms**
  - "Was it always this slow?"
  - Can't quantify chaos impact
  - Experiments show inconsistent results
### **Detection Pattern**
steady.*state|baseline|pre.*chaos|before.*experiment

## Kill Switch Fails

### **Id**
kill-switch-fails
### **Summary**
Can't stop chaos experiment when things go wrong
### **Severity**
critical
### **Situation**
Chaos injection stuck or can't be reversed
### **Why**
  Network chaos applied. Pods can't talk to control plane.
  Can't issue command to remove chaos. Stuck in failed state.
  What was 30 second experiment becomes 30 minute outage.
  
### **Solution**
  1. Always use time-limited chaos:
     TOTAL_CHAOS_DURATION: "60"  # Auto-stops after 60s
  
  2. Have out-of-band kill switch:
     # If control plane is affected, use direct kubectl
     kubectl delete chaosengine --all -n memory-service
  
  3. Test kill switch before running:
     # Part of experiment checklist
     - [ ] Verified abort command works
     - [ ] Have SSH access to nodes if needed
     - [ ] Know which resources to delete manually
  
  4. Use chaos with automatic rollback:
     cleanup:
       strategy: always  # Clean up even on failure
  
### **Symptoms**
  - "Can't stop the experiment"
  - Chaos persists after intended duration
  - Manual intervention required to recover
### **Detection Pattern**
kill.*switch|abort|cleanup|rollback|timeout

## Production Without Preparation

### **Id**
production-without-preparation
### **Summary**
First chaos experiment in production causes real incident
### **Severity**
critical
### **Situation**
Running untested chaos in production
### **Why**
  "It worked in staging" - but staging doesn't have real traffic,
  real data, real dependencies. First production chaos reveals all
  the ways staging lied. Discovery during production experiment = outage.
  
### **Solution**
  1. Progressive environment ladder:
     # Development → Staging → Canary → Production
  
  2. Run same experiment multiple times before production:
     # Staging: 3 runs, understand behavior
     # Canary: 1 run with 1% traffic
     # Production: start with 10%, increase
  
  3. Shadow traffic first:
     # Replay production traffic to staging
     # Run chaos on shadow system
     # Compare behavior
  
  4. Canary chaos:
     # Inject chaos to small subset
     # Compare canary metrics to control
     chaos:
       scope: canary
       traffic_percentage: 10
  
### **Symptoms**
  - "Works in staging" fails in production
  - First production experiment causes incident
  - Unexpected dependencies discovered during chaos
### **Detection Pattern**
production|staging|canary|environment

## Chaos Without Observability

### **Id**
chaos-without-observability
### **Summary**
Chaos runs but you can't see what happened
### **Severity**
high
### **Situation**
Injecting failures without proper monitoring
### **Why**
  Chaos happened. Nothing alerted. Did that mean system is resilient?
  Or did it mean monitoring doesn't work? Without observability,
  chaos experiments are blind. You're just breaking things.
  
### **Solution**
  1. Verify monitoring before chaos:
     pre_checks:
       - alert: "ErrorRateHigh"
         verify: "Can fire manually"
       - dashboard: "Memory Service Health"
         verify: "All panels loading"
  
  2. Add experiment-specific logging:
     logger.info(
         "chaos_experiment_started",
         experiment="database-failure",
         target="postgres-primary",
         duration=60
     )
  
  3. Correlate chaos with metrics:
     # Add annotation to Grafana
     POST /api/annotations
     {"time": now, "text": "Chaos: DB failure started"}
  
  4. Record all metrics during experiment:
     # Export metrics window for post-analysis
     prometheus_snapshot --start=T1 --end=T2
  
### **Symptoms**
  - "Nothing happened" but system was down
  - Can't correlate failures to chaos events
  - Alerts didn't fire when they should have
### **Detection Pattern**
observability|monitoring|alert|dashboard|metrics

## Team Not Notified

### **Id**
team-not-notified
### **Summary**
Chaos experiment surprises on-call, causes confusion
### **Severity**
medium
### **Situation**
Running chaos without telling the team
### **Why**
  On-call gets paged. Real incident? Checks everything. Spends 30 minutes.
  Finally discovers: "Oh, chaos experiment was running."
  Wastes time, creates distrust, on-call ignores future real alerts.
  
### **Solution**
  1. Always announce experiments:
     # Slack: #incidents
     "🔬 Chaos experiment starting in 5 minutes
     Experiment: Database failover test
     Duration: 30 minutes
     Contact: @sre-team"
  
  2. Use experiment status page:
     # chaos.internal/status shows active experiments
  
  3. Add to on-call handoff:
     # "Today's experiments: ..."
  
  4. Create calendar events:
     # Team calendar shows chaos windows
  
  5. Automatically notify:
     @chaos_experiment_started
     async def notify_team():
         await slack.post("#incidents", "Chaos starting...")
  
### **Symptoms**
  - On-call confused about "incidents"
  - Team doesn't trust alerts
  - Duplicate incident investigation
### **Detection Pattern**
notify|announce|on.*call|team

## No Learning Loop

### **Id**
no-learning-loop
### **Summary**
Chaos runs but nothing improves
### **Severity**
medium
### **Situation**
Chaos experiments without follow-through
### **Why**
  Experiment reveals gap. Filed ticket. Ticket gets deprioritized.
  Gap remains. Next chaos experiment finds same gap. Repeat.
  Chaos becomes theater - we "do chaos" but never improve.
  
### **Solution**
  1. Tie experiments to action items:
     ## Experiment Results
     Finding: Failover takes 45s, too slow
     Action: [JIRA-123] Reduce connection timeout
     Owner: @database-team
     Due: 2024-02-01
  
  2. Track fix verification:
     # Re-run experiment after fix
     # Verify finding is resolved
  
  3. Dashboard for chaos findings:
     # Track: findings, fixes, verified, outstanding
  
  4. SLO for chaos actions:
     # All critical findings fixed within 2 sprints
     # All findings verified within 4 sprints
  
  5. Make chaos findings visible:
     # Weekly report to engineering leadership
  
### **Symptoms**
  - Same findings in multiple experiments
  - Ticket backlog of unfixed chaos issues
  - Team skeptical about chaos value
### **Detection Pattern**
finding|action.*item|follow.*up|ticket