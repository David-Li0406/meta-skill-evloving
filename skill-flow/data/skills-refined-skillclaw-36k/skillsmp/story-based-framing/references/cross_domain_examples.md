# Cross-Domain Pattern Examples

This document demonstrates story-based framing applied across diverse domains, showing the technique's universal applicability for pattern detection.

## Business Process Pattern: "The Phantom Approval"

### Act 1: The Promise

The procurement workflow documentation states: "All purchase requests over $5,000 require approval from department head, finance manager, and VP before processing."

**Observable characteristics**: Workflow diagram shows three approval gates, policy manual references the requirement, training materials emphasize this control.

### Act 2: The Betrayal

But requests tagged as "urgent" or "vendor renewal" bypass all approval gates and go directly to processing, with post-hoc notification to approvers.

**The breaking point**: Line 247 in `procurement_workflow.py` contains:

```python
if request.tags.contains("urgent") or request.type == "renewal":
    return auto_approve(request)  # Bypasses approval queue
```

### Act 3: The Consequences

- Audit logs show 40% of purchases over $5,000 lack pre-approval
- Finance team discovers unauthorized spending during quarterly review
- Approvers receive "FYI" emails after purchase completion
- Compliance reports flag this as control weakness

**Symptoms**:

- Inconsistent approval timestamps (some show post-purchase dates)
- Budget overruns in departments with high "urgent" tag usage
- Approvers complaint: "I'm being notified, not asked"

### Act 4: The Source

The auto-approve feature was added during pandemic supply chain crisis (March 2020) to expedite essential purchases. The "temporary" exception was never removed after crisis ended, and "urgent" tag definition was never formalized.

**Origin**: Emergency modification became permanent operational pattern without documentation update or governance review.

### The Fix

1. Remove auto-approve bypass for financial amounts over threshold
2. Create expedited approval workflow (4-hour SLA) for genuine emergencies
3. Define "urgent" criteria with approval from governance committee
4. Add automated check: requests over $5K cannot be tagged "urgent" without C-level authorization

---

## Security Pattern: "The Overprivileged Service Account"

### Act 1: The Promise

IAM policy documentation specifies: "Service accounts follow principle of least privilege - each account has only permissions required for its specific function."

**Observable characteristics**: Security audit checklist includes POLP verification, training emphasizes minimal permissions, compliance framework requires regular access reviews.

### Act 2: The Betrayal

But the `data-pipeline-service` account has AdministratorAccess policy attached, granting full access to all AWS resources including IAM user management, billing, and account settings.

**The breaking point**: CloudTrail logs show service account could:

- Create new IAM users
- Modify security groups
- Access unrelated S3 buckets
- Modify RDS instances in different regions

### Act 3: The Consequences

- Security scanning tool flags 127 excessive permissions
- Penetration test successfully escalates privileges using this account
- Compliance audit marks this as critical finding
- No monitoring alerts trigger because account is "legitimate"

**Symptoms**:

- Service performs only S3 reads but can delete databases
- Account has permissions in regions where service never runs
- IAM access analyzer shows 95% of permissions never used
- Blast radius of credential compromise: entire AWS account

### Act 4: The Source

Account was created during initial POC phase when team "just needed something working quickly." Developer copy-pasted IAM policy from internet tutorial that used AdministratorAccess. Production deployment inherited POC configuration without security review.

**Origin**: Rapid prototyping with overprivileged template, never hardened for production.

### The Fix

1. Audit CloudTrail logs to identify actually-used permissions (last 90 days)
2. Create new policy with only S3 GetObject for specific bucket prefix
3. Add read-only CloudWatch Logs permissions for monitoring
4. Rotate credentials and delete old overprivileged account
5. Implement policy: All service accounts require security review before production

---

## UX/Design Pattern: "The Confirm-Shaming Dark Pattern"

### Act 1: The Promise

Cancel subscription button promises user control: "You can cancel anytime, no questions asked."

**Observable characteristics**: Marketing materials emphasize "no commitment," FAQ states "cancel with one click," user reviews praise "easy cancellation."

### Act 2: The Betrayal

But clicking "Cancel Subscription" shows modal with buttons:

- "Yes, cancel my subscription and lose access to exclusive content" (gray, bottom)
- "No, keep my subscription and continue enjoying benefits!" (bright green, top, default focus)

**The breaking point**: The actual cancel action requires:

1. Clicking gray "Yes, cancel..." button (requires reading negative framing)
2. Selecting reason from dropdown (required field)
3. Clicking "Confirm Cancellation" on second modal
4. Closing "We're sad to see you go" overlay
5. Confirming email notification

### Act 3: The Consequences

- 40% of users who initiate cancellation don't complete it
- Support tickets: "I tried to cancel but it didn't work"
- App store reviews mention "deceptive cancellation process"
- Chargebacks increase 300% (users cancel via credit card dispute)
- Regulatory attention from FTC consumer protection division

**Symptoms**:

- Analytics show 85% of cancellation attempts abandon mid-flow
- Email support receives "How do I actually cancel?" questions daily
- Social media mentions include #CantCancel hashtag
- Class action lawsuit filed alleging "subscription trap"

### Act 4: The Source

Product team was incentivized on monthly recurring revenue (MRR) and retention rate. Design explicitly optimized to reduce cancellation completion rate. Leadership approved based on short-term revenue impact, ignoring long-term brand damage and legal risk.

**Origin**: Misaligned incentives prioritizing retention metrics over user trust and legal compliance.

### The Fix

1. Single-click cancellation from account settings
2. Neutral language: "Cancel" and "Keep Subscription" (equal visual weight)
3. Optional feedback form AFTER cancellation completes
4. Immediate confirmation, no additional modals
5. Update product team OKRs to include customer satisfaction and LTV (not just MRR)

---

## Data Quality Pattern: "The Stale Cache Syndrome"

### Act 1: The Promise

API documentation states: "Returns real-time inventory availability. Data refreshed every 60 seconds."

**Observable characteristics**: Response headers include `Cache-Control: max-age=60`, monitoring dashboard shows "Real-time inventory" with green checkmarks, SLA promises 99.9% data freshness.

### Act 2: The Betrayal

But CDN configuration sets `Cache-Control: max-age=3600` (1 hour), overriding API headers. Additionally, application-layer cache has no expiration policy and grows indefinitely.

**The breaking point**: Multiple cache layers with different policies:

- CDN: 1 hour
- API gateway: 5 minutes
- Application: ∞ (never expires)
- Database: Real-time

### Act 3: The Consequences

- Customers see "In Stock" for items that sold out 45 minutes ago
- Orders fail during checkout: "Sorry, this item is no longer available"
- Customer support receives 200+ calls/day about incorrect inventory
- Conversion rate drops 15% due to checkout failures
- Competitor comparison shows rival has accurate real-time data

**Symptoms**:

- Order failure rate: 12% (industry average: 2%)
- API monitoring shows `cache-age: 3541` in response headers
- Database shows current inventory: 0, but API returns: 47
- Cache hit rate: 95% (too high for "real-time" data)

### Act 4: The Source

CDN was added to reduce database load during Black Friday traffic spike. Operations team configured 1-hour cache based on generic "retail product" template without understanding inventory velocity. Application cache was added by developer to "improve performance" without considering data freshness requirements. No cross-team communication about caching strategy.

**Origin**: Performance optimization without data freshness impact analysis, siloed team decision-making.

### The Fix

1. Reduce CDN cache to 60 seconds for inventory endpoints
2. Add cache key variation by stock level thresholds (>10, 1-10, 0)
3. Implement cache invalidation on inventory updates (publish/subscribe pattern)
4. Add `X-Data-Age` header to responses for observability
5. Create caching decision matrix: correctness vs. performance trade-offs
6. Establish cross-functional "data freshness" SLO with product/engineering/ops alignment

---

## Medical Diagnosis Pattern: "The Anchoring Bias"

### Act 1: The Promise

Diagnostic protocol states: "Evaluate all presenting symptoms objectively. Consider differential diagnoses before committing to primary diagnosis."

**Observable characteristics**: Medical school training emphasizes "think broadly," diagnostic checklists require considering multiple possibilities, peer review process validates diagnostic reasoning.

### Act 2: The Betrayal

But when patient presents with chest pain, clinician immediately anchors on "cardiac event" hypothesis and orders cardiac-focused tests exclusively, dismissing gastroesophageal reflux disease (GERD) despite supporting symptoms (occurs after meals, improves with antacids).

**The breaking point**: Initial assessment note documents: "Chest pain → cardiac workup" without documenting evaluation of GI, pulmonary, or musculoskeletal differential diagnoses. Subsequent clinicians read initial note and continue cardiac-focused investigation.

### Act 3: The Consequences

- Patient undergoes unnecessary cardiac catheterization (invasive, risky)
- 3-day hospital admission for cardiac monitoring (negative results)
- $47,000 in charges for cardiac workup
- Actual diagnosis (GERD) identified only after patient requests GI consultation
- Resolved with $8 generic medication (omeprazole)
- Patient files complaint about unnecessary procedures

**Symptoms**:

- Documentation shows no consideration of differential diagnoses
- All ordered tests relate to single hypothesis
- Disconfirming evidence (negative troponin, normal EKG) doesn't prompt hypothesis revision
- Consultation note from GI specialist: "Classic GERD presentation, surprised cardiac workup was performed"

### Act 4: The Source

Emergency department protocols prioritize "rule out MI (myocardial infarction)" for any chest pain due to medicolegal risk. First physician's cardiac anchor influences all subsequent clinicians due to status quo bias ("previous doctor must have had good reason"). Time pressure and cognitive load reduce thoroughness of differential diagnosis consideration.

**Origin**: Risk-averse institutional culture, cognitive bias in high-stress environment, documentation creating confirmation cascade.

### The Fix

1. Implement structured differential diagnosis documentation requirement
2. Checklist prompts: "Have you considered GI/pulmonary/MSK causes?"
3. Decision support system flags when presenting symptoms match multiple diagnoses
4. Peer review includes evaluation of differential diagnosis consideration
5. Departmental training on debiasing strategies and diagnostic calibration
6. Culture shift: "Accuracy over speed" for non-emergent presentations

---

## Operations Pattern: "The Alert Fatigue"

### Act 1: The Promise

Monitoring system promises: "Immediate notification of production incidents. On-call engineers alerted within 1 minute of critical issues."

**Observable characteristics**: PagerDuty configured, escalation policies defined, SLA promises 5-minute acknowledgment time, dashboards show "system health."

### Act 2: The Betrayal

But monitoring generates 847 alerts per day, with 98.5% false positives. Critical production outage alert is indistinguishable from "disk 71% full on staging server" alert.

**The breaking point**: On-call engineer receives:

- 3am: "SSL certificate expiring in 45 days" (LOW)
- 3:02am: "API response time 510ms" (WARNING, threshold: 500ms)
- 3:05am: "Database connection pool 80% utilized" (CRITICAL)
- 3:07am: **"Payment processing down, $50K/minute revenue loss"** (CRITICAL)

### Act 3: The Consequences

- Critical production outage goes unnoticed for 23 minutes (SLA: 5 minutes)
- Engineer acknowledges without investigating (habitually silencing alerts)
- $1.15M revenue lost during outage
- Post-incident review: "Alert fatigue prevented timely response"
- On-call engineer burnout: 3 engineers quit in 2 months

**Symptoms**:

- 847 alerts/day → 1.3 acknowledged/day
- Mean time to acknowledge: 8 hours (SLA: 5 minutes)
- Engineers create email rules to auto-archive monitoring alerts
- Critical alerts have same notification sound as trivial warnings
- PagerDuty shows 99.8% "acknowledged without comment"

### Act 4: The Source

Default monitoring templates were applied across all systems without customization. "Better safe than sorry" approach led to alerting on everything. Thresholds were never tuned based on actual incident history. Each team added their alerts without considering total alert volume. No alert retirement policy as systems evolved.

**Origin**: Overcautious configuration, lack of alert hygiene, no feedback loop between alerts and actual incidents.

### The Fix

1. Audit all alerts: Which ones preceded actual incidents in past 6 months?
2. Delete alerts with zero incident correlation
3. Tune thresholds using 99th percentile of normal behavior + margin
4. Implement alert severity guidelines:
   - CRITICAL: Revenue/customer impact, immediate action required
   - WARNING: Potential future problem, actionable during business hours
   - INFO: Observability only, no action required
5. Different notification channels by severity (SMS vs email vs dashboard)
6. Quarterly alert review: Delete low-value alerts
7. Measure: Alerts per day, signal-to-noise ratio, mean time to acknowledge

---

## Pattern Template for Any Domain

### Act 1: The Promise

{What the system/process/service claims to do}

**Observable characteristics**: {How you recognize the promise}

### Act 2: The Betrayal

{Where reality violates the promise}

**The breaking point**: {Specific point where it fails}

### Act 3: The Consequences

{Observable symptoms}

**Symptoms**:

- {Symptom 1}
- {Symptom 2}
- {Symptom 3}

### Act 4: The Source

{Why this pattern exists}

**Origin**: {Root cause}

### The Fix

{How to address the root cause}
