---
name: java-debugging-prod-incidents
description: Production incident debugging playbook for Java services: triage with logs/metrics/traces, safe JVM diagnostics (jcmd/JFR/thread dumps), rollback decision tree, communication, and blameless postmortems. Use during outages or flaky production behavior.
license: CC-BY-4.0
compatibility: "JDK 17+ (recommended JDK 21). Requires observability access. Diagnostic commands depend on runtime permissions."
metadata:
  owner: "backend+sre"
  version: "1.0"
  tags: [java, production, incident, troubleshooting, sre, postmortem, jcmd, jfr, rollback]
---

# Debugging Production Incidents (Java) — SRE-first + JVM-safe tooling

## Intent

During incidents, speed matters—but unstructured debugging causes more damage.
This skill provides:

- An SRE-style incident workflow (roles, comms, timeline)
- A **logs/metrics/traces-first** diagnosis approach
- Safe JVM diagnostics: thread dumps, JFR snippets, jcmd snapshots
- A rollback / mitigate decision tree
- A blameless postmortem template and “next guardrails” checklist

---

## Scope

### In scope

- Incident triage and mitigation loop
- Observability-first debugging
- JVM diagnostics:
  - thread dumps
  - JFR capture
  - GC/heap snapshots
- Hypothesis-driven investigation
- Rollback / feature-flag mitigation strategy
- Postmortem and action items (prevention)

### Out of scope

- Full infra incident response for Kubernetes/network (separate ops skill)
- Pen-test level forensic analysis (separate security response playbook)

---

## When to use

Triggers:

- production outage
- SLO burn / severe latency spike
- error rate spike
- memory leak suspected
- queue lag runaway
- deadlocks / thread pool starvation
- “works in staging, fails in prod” mystery

---

## Required inputs (context to attach in Cursor)

- Links or snapshots (not raw secrets):
  - dashboard panels (latency, CPU, GC, error rate)
  - recent deploys/config changes
  - key logs around start time
  - traces for representative failing requests
- Service metadata:
  - version / commit
  - runtime (container/VM), JDK version
  - traffic shape changes (if any)

---

## Roles and workflow (SRE-style)

### Step 1 — Declare incident and assign roles

At minimum:

- Incident Commander (IC): owns decisions and comms
- Tech Lead: drives technical investigation
- Comms: updates stakeholders/users
- Scribe: writes timeline and captures actions

Deliverable: incident channel + timeline doc started.

### Step 2 — Stabilize first (stop the bleeding)

Prioritize mitigations:

- rollback to last known good
- disable feature via flag
- reduce load (rate limit, shed traffic)
- scale out if safe and helps (not always)
- isolate failing dependency (circuit breaker)

Rule: prefer reversible mitigations over risky live fixes.

Deliverable: mitigation chosen + tracked in timeline.

---

## Observability-first diagnosis

### Step 3 — Define the impact and the symptom precisely

- Who is impacted? which endpoints/tenants/regions?
- What changed? (deploy/config/traffic/dependency)
- Which SLO is burning? (latency, availability)

Deliverable: a one-paragraph symptom statement.

### Step 4 — Use the “3 signals” triage order

1) Metrics (what is broken and when)
2) Logs (why requests fail, errors, timeouts)
3) Traces (where time is spent across dependencies)

Common patterns:

- latency increases + CPU flat: likely I/O waits, downstream slowness, locks
- CPU spikes: hot loop, serialization, logging overhead, contention
- GC spikes: allocation storms, memory leak, heap too small
- errors spike: upstream/downstream change, auth expiry, config drift

Deliverable: top 2 hypotheses with supporting signals.

---

## JVM diagnostics (safe playbook)

Use these only if:

- observability is insufficient, OR
- you need thread/heap evidence, OR
- the service is “alive but stuck”.

### Step 5 — Thread dump (fast, low risk)

Use a safe method (depends on permissions):

- `jcmd <pid> Thread.print` is often preferred over legacy tools.

What to look for:

- deadlocks
- thread pool starvation
- many threads blocked on the same lock
- many threads waiting for DB connections
- runaway retries/backoff loops

Deliverable: thread dump snippet + interpretation.

### Step 6 — JFR snippet (bounded capture)

Capture 30–120s around peak symptoms:

- CPU + allocation + locks + thread states
This often answers “what is actually happening” quickly.

Deliverable: JFR file + short summary.

### Step 7 — Heap/GC snapshots (only if needed)

If memory/GC suspicion:

- capture GC log window
- capture class histogram snapshot via jcmd
- only capture heap dump if you have storage/privacy plan

Deliverable: evidence bundle for memory hypothesis.

---

## Hypothesis-driven loop (fast iterations)

### Step 8 — Rank hypotheses and test the cheapest first

For each hypothesis:

- Expected observation if true
- Cheap test (canary, toggle, single node restart, config revert)
- Risk assessment

Avoid:

- making 10 changes at once
- “SSH and tweak random flags”
- “fixing” without evidence

Deliverable: hypothesis table (in timeline).

---

## Rollback / mitigation decision tree

### Step 9 — Decide: mitigate now vs fix forward

Prefer rollback/flag-off if:

- change is recent and correlated
- fix is uncertain
- impact is high

Fix-forward only if:

- rollback is impossible or too risky
- you have a high-confidence minimal patch
- you can canary safely

Deliverable: decision + rationale + next checkpoint time.

---

## After recovery: verification and monitoring

### Step 10 — Verify recovery

- confirm error rate normal
- confirm latency p95/p99 stable
- confirm downstream health
- confirm no hidden queue lag or retry storms

Deliverable: “recovery confirmation” entry in timeline.

---

## Postmortem (blameless) + next guardrails

### Step 11 — Write a blameless postmortem

Use a standard structure:

- Summary + customer impact
- Timeline (UTC + local time if needed)
- Root cause and contributing factors
- Detection and response analysis
- What went well / what went poorly
- Action items with owners and deadlines

### Step 12 — “Next guardrails” checklist (make incidents less likely)

Examples:

- add missing timeouts and retries limits
- add bulkheads / rate limits
- add better alerts (SLO-based)
- add regression tests
- add runbooks for the failure mode
- add feature flags for risky paths
- enforce safer deploy practices (canary, bake time)

Deliverable: postmortem doc + action item tracker.

---

## Outputs / Artifacts

- Incident timeline doc (scribe notes)
- Mitigation decision log
- Evidence bundle (dashboards/logs/traces + optional JVM artifacts)
- Postmortem document (blameless)
- “Next guardrails” action list

---

## Definition of Done (DoD)

- [ ] Service recovered and verified
- [ ] Timeline is complete enough to reconstruct actions
- [ ] Root cause identified (or bounded) with evidence
- [ ] Postmortem written and shared
- [ ] Action items created with owners and deadlines
- [ ] Runbooks and alerts updated

---

## Common failure modes & fixes

- Symptom: incident drags on with random changes
  - Cause: no hypotheses, no IC role, no timeline
  - Fix: establish IC + scribe, hypothesis loop, safe mitigations

- Symptom: recovery but reoccurs
  - Cause: no guardrails added; missing timeouts/backpressure
  - Fix: convert root cause into specific engineering controls

- Symptom: debugging actions cause more outage
  - Cause: high-risk production changes and poor rollback
  - Fix: prefer reversible mitigations and canary; keep changes minimal

---

## Guardrails (What NOT to do)

- Do NOT paste secrets/tokens in incident channels.
- Do NOT take heap dumps without privacy review and storage plan.
- Do NOT run destructive commands on production hosts without explicit approval.
- Do NOT “restart everything” without understanding cascading effects.

---

## References (primary)

- Google SRE — Incident Response / Incident Management (online book): <https://sre.google/sre-book/managing-incidents/>
- Google Cloud — Postmortems / learning culture: <https://cloud.google.com/blog/products/management-tools/incident-management-for-real-life>
- Oracle Java Diagnostic Tools (jcmd/JFR guidance): <https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html>
