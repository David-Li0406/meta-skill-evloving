# Incident Responder

## Patterns


---
  #### **Name**
The Incident Response Framework
  #### **Description**
Systematic approach to handling any incident
  #### **When**
Any production incident occurs
  #### **Example**
    # THE OODA LOOP FOR INCIDENTS:
    # Observe → Orient → Decide → Act → (Repeat)
    
    ## PHASE 1: DETECT AND ACKNOWLEDGE (first 5 minutes)
    """
    ✓ Acknowledge the alert
    ✓ Open incident channel (#incident-YYYY-MM-DD-title)
    ✓ Post initial summary:
      - What's broken? "Orders API returning 500s"
      - Who's affected? "All checkout users"
      - When did it start? "2:45 PM based on alerts"
      - Who's responding? "@alice is incident commander"
    """
    
    ## PHASE 2: ASSESS SEVERITY
    """
    SEV1 - Critical
    - Core functionality completely broken
    - Data loss or security breach
    - All users affected
    → All hands, wake people up
    
    SEV2 - Major
    - Significant feature broken
    - Many users affected
    - Workaround may exist
    → On-call + relevant owners
    
    SEV3 - Minor
    - Limited feature affected
    - Few users impacted
    - Easy workaround exists
    → On-call handles, may defer
    
    SEV4 - Low
    - Cosmetic or minor issue
    - No user impact
    → Next business day
    """
    
    ## PHASE 3: MITIGATE (first priority)
    """
    Ask: "What's the fastest way to stop the bleeding?"
    
    Options (in order of preference):
    1. Rollback recent deploy
    2. Feature flag off the broken feature
    3. Scale up / failover
    4. Block problematic traffic
    5. Apply hotfix (if fast and safe)
    
    DO NOT: Spend 30 minutes debugging before trying rollback
    """
    
    ## PHASE 4: COMMUNICATE
    """
    Every 30 minutes, post update:
    - Current status
    - What we've tried
    - What we're trying next
    - Expected next update time
    
    Stakeholders need to know we're working on it.
    Silence is terrifying.
    """
    
    ## PHASE 5: RESOLVE AND VERIFY
    """
    When you think it's fixed:
    1. Monitor for 15-30 minutes
    2. Verify with affected users/flows
    3. Check metrics return to baseline
    4. THEN declare resolved
    """
    
    ## PHASE 6: POST-INCIDENT
    """
    Immediately:
    - Timeline document started
    - Incident channel kept open for notes
    
    Within 48 hours:
    - Post-mortem written
    - Action items created
    - Meeting scheduled
    """
    

---
  #### **Name**
Incident Commander Role
  #### **Description**
Clear ownership during incidents
  #### **When**
Any SEV1 or SEV2 incident
  #### **Example**
    # INCIDENT COMMANDER RESPONSIBILITIES:
    
    ## 1. Coordinate, Don't Fix
    """
    Your job is NOT to debug the issue yourself.
    Your job is to ensure the right people are debugging
    and everyone knows what's happening.
    """
    
    ## 2. Delegate Roles
    """
    "Alice, you're on debugging the database"
    "Bob, you're on customer communication"
    "Carol, you're documenting the timeline"
    "I'll coordinate and post updates"
    """
    
    ## 3. Control the Channel
    """
    - Keep chat focused on incident
    - Move side discussions elsewhere
    - Summarize periodically
    - Make decisions when needed
    """
    
    ## 4. Ask the Key Questions
    """
    - "What's the current status?"
    - "What have we tried?"
    - "What's our next step?"
    - "Do we need anyone else?"
    - "Should we rollback?"
    """
    
    ## 5. Make the Calls
    """
    When team is stuck, decide:
    - "Let's try the rollback"
    - "We need to page the database team"
    - "Let's give this 10 more minutes"
    
    A decision made quickly beats a perfect decision made slowly.
    """
    
    ## 6. Declare Resolution
    """
    You decide when incident is over.
    - Metrics back to normal? Check.
    - No new errors? Check.
    - Team agrees? Check.
    "Incident resolved at 15:45. Keep monitoring."
    """
    

---
  #### **Name**
The Blameless Post-Mortem
  #### **Description**
Learning from incidents without finger-pointing
  #### **When**
After any significant incident
  #### **Example**
    # BLAMELESS POST-MORTEM STRUCTURE:
    
    ## 1. Summary
    """
    One paragraph: What happened, how long, who was affected.
    
    Example:
    "On Jan 15, the orders API was unavailable for 45 minutes
    between 14:30-15:15 UTC. All checkout attempts failed,
    affecting approximately 2,000 users. Revenue impact was
    estimated at $50,000."
    """
    
    ## 2. Timeline
    """
    Time    | Event
    --------|------------------------------------------
    14:30   | Alerts fire for orders API 500 errors
    14:32   | On-call acknowledges, opens incident channel
    14:35   | Alice joins, begins investigation
    14:40   | Identified: database connection exhaustion
    14:45   | Decision: restart API pods
    14:50   | Restart complete, errors continue
    14:55   | Identified: connection leak in new code
    15:00   | Rollback to previous version initiated
    15:10   | Rollback complete
    15:15   | Metrics normalized, incident resolved
    """
    
    ## 3. Contributing Factors (not "Root Cause")
    """
    ✗ DON'T: "Alice pushed code without testing"
    ✓ DO: "Code review didn't catch connection leak"
    
    Contributing factors:
    1. Connection pooling change introduced leak
    2. Load testing doesn't simulate long-running connections
    3. No alert for connection pool exhaustion
    4. Rollback took 10 min due to slow deploy pipeline
    """
    
    ## 4. What Went Well
    """
    - Alert fired within 2 minutes of issue
    - Team assembled quickly
    - Communication was clear and timely
    - Rollback successfully resolved issue
    """
    
    ## 5. What Could Be Improved
    """
    - Connection pool monitoring needed
    - Load tests should simulate production patterns
    - Deploy pipeline could be faster
    - More specific runbook for this scenario
    """
    
    ## 6. Action Items (with owners and deadlines)
    """
    | Action | Owner | Due |
    |--------|-------|-----|
    | Add connection pool alerts | Alice | Jan 22 |
    | Update load test scenarios | Bob | Jan 29 |
    | Create runbook for DB issues | Carol | Jan 25 |
    | Investigate deploy speedup | Dave | Feb 5 |
    """
    

---
  #### **Name**
Rollback vs Fix Forward
  #### **Description**
Deciding how to resolve the incident
  #### **When**
Incident caused by recent change
  #### **Example**
    # THE ROLLBACK DECISION:
    
    ## Default: Rollback
    """
    If a recent deploy caused the incident,
    rollback should be your first instinct.
    
    WHY:
    - Immediately restores known-good state
    - Doesn't require understanding the bug
    - Low risk (returning to tested code)
    - Buys time to fix properly
    """
    
    ## When to Rollback:
    - Recent deploy correlates with incident
    - Rollback is fast (< 10 minutes)
    - No data migration makes rollback complex
    - Root cause is unclear
    
    ## When to Fix Forward:
    - Rollback is impossible (data migration)
    - Fix is obvious and quick (< 5 minutes)
    - Rollback would cause worse problems
    - Root cause is clear and fix is safe
    
    # DECISION FRAMEWORK:
    
    """
    Is there a recent deploy? ──No──→ Investigate root cause
         │
        Yes
         │
         ▼
    Is rollback possible? ──No──→ Fix forward (or workaround)
         │
        Yes
         │
         ▼
    Is rollback fast? ──No──→ Consider fix forward if fix is faster
         │
        Yes
         │
         ▼
    ROLLBACK FIRST
    Then fix the bug properly
    """
    
    ## The "10-Minute Rule"
    """
    If you haven't mitigated within 10 minutes of diagnosis,
    seriously consider rollback or failover.
    
    Debugging under pressure leads to mistakes.
    Rollback buys time to fix correctly.
    """
    

---
  #### **Name**
Severity Assessment
  #### **Description**
Determining incident priority
  #### **When**
Incident detected, need to determine response level
  #### **Example**
    # SEVERITY DEFINITIONS:
    
    ## SEV1 - Critical (All hands)
    """
    Impact: Complete service outage or security breach
    Examples:
      - Site completely down
      - Database corruption
      - Security incident / data breach
      - Payment processing broken
    
    Response:
      - Page all relevant on-call
      - All hands if needed
      - Executives notified
      - Customer communication prepared
    """
    
    ## SEV2 - Major (On-call + team)
    """
    Impact: Major feature broken, significant user impact
    Examples:
      - Checkout broken for some users
      - API latency 10x normal
      - One region down, others working
      - Important integration broken
    
    Response:
      - On-call responds
      - Team leads notified
      - Page additional help if needed
      - 30-minute update cadence
    """
    
    ## SEV3 - Minor (On-call)
    """
    Impact: Limited feature impact, workaround exists
    Examples:
      - Non-critical feature broken
      - Degraded performance (not severe)
      - One customer affected
      - Background job delayed
    
    Response:
      - On-call investigates
      - May defer to business hours
      - Fix within 24 hours
      - 2-hour update cadence
    """
    
    ## SEV4 - Low (Next business day)
    """
    Impact: Minimal, cosmetic, no user impact
    Examples:
      - UI alignment issue
      - Log errors (no user impact)
      - Internal tool slow
      - Dashboard broken
    
    Response:
      - Document for next day
      - No after-hours response
      - Fix when convenient
    """
    
    # SEVERITY ESCALATION:
    """
    Escalate if:
    - Issue not resolved within expected time
    - Impact growing
    - Need additional expertise
    - Customer escalations happening
    """
    

## Anti-Patterns


---
  #### **Name**
Hero Debugging
  #### **Description**
One person trying to solve everything alone
  #### **Why**
    The lone hero works in isolation, doesn't communicate, and creates a single
    point of failure. When they get stuck or burned out, nobody knows what's
    been tried. Team collaboration solves incidents faster.
    
  #### **Instead**
Designate roles. Communicate constantly. Work in pairs if possible. Share what you're trying.

---
  #### **Name**
Blame Storming
  #### **Description**
Post-mortem focused on who caused the incident
  #### **Why**
    Blame discourages transparency. People hide mistakes instead of reporting them.
    Future incidents are worse because people don't admit early warnings. Learning
    stops when punishment begins.
    
  #### **Instead**
Focus on contributing factors. Ask "what" and "how," not "who." Blame the process, improve the system.

---
  #### **Name**
Premature All-Clear
  #### **Description**
Declaring incident resolved too quickly
  #### **Why**
    "It looks fixed" is not "it's fixed." Declaring resolution too early leads to
    repeat pages, eroded trust, and incomplete fixes. The incident might not
    actually be resolved.
    
  #### **Instead**
Wait 15-30 minutes after fix. Check metrics return to baseline. Verify with affected flows.

---
  #### **Name**
Fix Without Understanding
  #### **Description**
Applying changes until something works
  #### **Why**
    Random changes might mask the problem or cause new ones. Without understanding
    the cause, you can't prevent recurrence. You might make things worse.
    
  #### **Instead**
Mitigate first (rollback), then understand. Don't ship a "fix" you don't understand.

---
  #### **Name**
Silent Incident
  #### **Description**
Working on incident without communicating
  #### **Why**
    Stakeholders panic when they see impact but hear nothing. Duplicate work
    happens when people don't know who's handling what. Trust erodes with silence.
    
  #### **Instead**
Post updates every 30 minutes. Even "still investigating" is better than silence.

---
  #### **Name**
Alert Fatigue Acceptance
  #### **Description**
Ignoring alerts because there are too many
  #### **Why**
    Noisy alerts train teams to ignore alerts. When a real incident happens,
    it's missed in the noise. On-call becomes meaningless rotation.
    
  #### **Instead**
Every alert should be actionable. Fix or delete noisy alerts. Quality over quantity.