# Chaos Engineer

## Patterns


---
  #### **Name**
Chaos Experiment Design
  #### **Description**
Scientific approach to chaos engineering
  #### **When**
Planning any resilience test
  #### **Example**
    # Chaos Experiment Template
    
    ## Experiment: Memory Service Database Failure
    Date: 2024-01-15
    Owner: @sre-team
    
    ## 1. Steady State Hypothesis
    "When the memory service is healthy, 99.9% of memory
    retrieval requests complete successfully within 500ms."
    
    ### Metrics to Monitor:
    - `http_requests_total{service="memory", status="200"}`
    - `http_request_duration_seconds{service="memory", quantile="0.99"}`
    - `memory_retrievals_total{status="success"}`
    
    ## 2. Hypothesis Under Chaos
    "When the PostgreSQL primary is unavailable for 30 seconds,
    the memory service fails over to the replica and maintains
    95% success rate with degraded latency (p99 < 2s)."
    
    ## 3. Experiment Design
    ### Chaos Injection:
    - Action: Block network traffic to PostgreSQL primary
    - Duration: 30 seconds
    - Scope: Memory service in production-us-east-1
    
    ### Blast Radius Controls:
    - Only affects 10% of traffic (canary deployment)
    - Auto-abort if error rate exceeds 50%
    - Kill switch: `curl -X POST /chaos/abort`
    
    ### Rollback Plan:
    - Remove network block automatically after 30s
    - If stuck: `kubectl delete networkpolicy chaos-postgres`
    
    ## 4. Execution Checklist
    - [ ] Notify on-call team
    - [ ] Confirm monitoring dashboards ready
    - [ ] Verify kill switch works
    - [ ] Start traffic recording for replay
    - [ ] Execute experiment
    - [ ] Collect results
    - [ ] Notify all-clear
    
    ## 5. Results
    ### Actual Behavior:
    - Failover time: 8 seconds (expected: <10s) ✅
    - Success rate during chaos: 82% ❌ (expected: 95%)
    - P99 latency: 3.2s ❌ (expected: <2s)
    
    ### Findings:
    - Connection pool doesn't retry fast enough
    - Some requests timeout waiting for dead connection
    - Recommendation: Reduce connection timeout from 30s to 5s
    
    ## 6. Action Items
    - [ ] Reduce PostgreSQL connection timeout to 5s
    - [ ] Add circuit breaker for database calls
    - [ ] Re-run experiment after fixes
    

---
  #### **Name**
Game Day Runbook
  #### **Description**
Structured team exercise for failure simulation
  #### **When**
Training team or validating recovery procedures
  #### **Example**
    # Game Day: Memory System Failure Scenarios
    Date: 2024-01-20
    Duration: 4 hours
    Participants: SRE team, Memory team, On-call engineers
    
    ## Objectives
    1. Validate runbooks for common failures
    2. Train new team members on incident response
    3. Identify gaps in monitoring and alerting
    
    ## Pre-Game Checklist
    - [ ] Schedule maintenance window (if needed)
    - [ ] Notify stakeholders
    - [ ] Prepare failure injection tools
    - [ ] Set up war room (virtual or physical)
    - [ ] Assign roles: Facilitator, Injector, Observer, Scribe
    
    ## Scenarios
    
    ### Scenario 1: Database Connection Exhaustion (30 min)
    **Injection:** Slowly consume all database connections
    ```python
    # Inject via API
    async def exhaust_connections():
        connections = []
        for _ in range(100):
            conn = await db.connect()
            connections.append(conn)
            await asyncio.sleep(1)
    ```
    **Expected Behavior:**
    - Alert fires: "Database connection pool exhausted"
    - New requests fail with connection timeout
    - Dashboard shows pool saturation
    
    **Team Actions:**
    1. Identify alert in PagerDuty
    2. Check dashboard for connection pool status
    3. Follow runbook: "Database Connection Issues"
    4. Kill long-running queries or restart service
    
    **Success Criteria:**
    - Alert fires within 1 minute
    - Team identifies issue within 5 minutes
    - Recovery within 10 minutes
    
    ### Scenario 2: Vector Store Latency Spike (30 min)
    **Injection:** Add 5s delay to vector store responses
    **Expected:** Circuit breaker opens, fallback to keyword search
    
    ### Scenario 3: Kafka Consumer Lag (45 min)
    **Injection:** Pause Kafka consumer
    **Expected:** Alert on lag, producer backpressure, graceful degradation
    
    ## Post-Game Review
    - What went well?
    - What was surprising?
    - What runbooks need updates?
    - What monitoring gaps did we find?
    

---
  #### **Name**
Automated Chaos Pipeline
  #### **Description**
CI/CD integrated chaos testing
  #### **When**
Continuous resilience verification
  #### **Example**
    # LitmusChaos Experiment for Kubernetes
    
    apiVersion: litmuschaos.io/v1alpha1
    kind: ChaosEngine
    metadata:
      name: memory-service-chaos
      namespace: memory-service
    spec:
      appinfo:
        appns: memory-service
        applabel: "app=memory-service"
        appkind: deployment
      engineState: active
      chaosServiceAccount: litmus-admin
      experiments:
        - name: pod-network-latency
          spec:
            components:
              env:
                - name: NETWORK_INTERFACE
                  value: eth0
                - name: NETWORK_LATENCY
                  value: "500"  # 500ms latency
                - name: TOTAL_CHAOS_DURATION
                  value: "60"  # 60 seconds
                - name: PODS_AFFECTED_PERC
                  value: "50"  # Affect 50% of pods
    
    ---
    # Chaos Workflow with abort conditions
    
    apiVersion: argoproj.io/v1alpha1
    kind: Workflow
    metadata:
      name: chaos-resilience-test
    spec:
      entrypoint: chaos-test
      templates:
        - name: chaos-test
          steps:
            - - name: steady-state-check
                template: verify-steady-state
            - - name: inject-chaos
                template: run-chaos
            - - name: verify-hypothesis
                template: check-hypothesis
            - - name: cleanup
                template: abort-chaos
    
        - name: verify-steady-state
          container:
            image: curlimages/curl
            command: [sh, -c]
            args:
              - |
                # Check baseline metrics
                SUCCESS_RATE=$(curl -s prometheus/api/v1/query?query=...)
                if [ "$SUCCESS_RATE" -lt "99" ]; then
                  echo "Steady state not met, aborting"
                  exit 1
                fi
    
        - name: check-hypothesis
          container:
            image: curlimages/curl
            command: [sh, -c]
            args:
              - |
                # Verify system maintained expected behavior
                SUCCESS_RATE=$(curl -s prometheus/api/v1/query?query=...)
                if [ "$SUCCESS_RATE" -lt "95" ]; then
                  echo "HYPOTHESIS FAILED: Success rate dropped below 95%"
                  exit 1
                fi
                echo "HYPOTHESIS VERIFIED"
    

## Anti-Patterns


---
  #### **Name**
Chaos Without Hypothesis
  #### **Description**
Breaking things without defining expected behavior
  #### **Why**
No learning happens. You just break things and fix them.
  #### **Instead**
Define hypothesis first, then design experiment to test it

---
  #### **Name**
Starting in Production
  #### **Description**
First chaos experiment in production
  #### **Why**
Unknown blast radius. Untested tooling. Recipe for real outage.
  #### **Instead**
Start in staging, then canary, then limited production

---
  #### **Name**
No Kill Switch
  #### **Description**
Chaos experiment that can't be stopped quickly
  #### **Why**
If experiment causes more damage than expected, you're stuck.
  #### **Instead**
Every experiment needs abort mechanism tested before running

---
  #### **Name**
Weekend Chaos
  #### **Description**
Running experiments when response team is minimal
  #### **Why**
If it goes wrong, recovery is slow. Real incidents don't wait.
  #### **Instead**
Run during business hours with full team available

---
  #### **Name**
Chaos as Punishment
  #### **Description**
Using chaos to prove team isn't ready
  #### **Why**
Creates fear, not learning. Team hides problems instead of fixing.
  #### **Instead**
Chaos is learning, not testing. Everyone should want to find gaps.