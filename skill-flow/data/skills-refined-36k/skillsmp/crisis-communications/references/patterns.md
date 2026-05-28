# Crisis Communications

## Patterns


---
  #### **Name**
The First Response Framework
  #### **Description**
How to communicate in the first hour of a crisis
  #### **When**
Something has just gone wrong and you need to respond immediately
  #### **Example**
    # FIRST RESPONSE (within 1 hour):
    
    ## What to communicate:
    """
    1. ACKNOWLEDGE: "We're aware of [specific issue]"
    2. VALIDATE: "We understand this is affecting [specific impact]"
    3. ACTION: "We're actively investigating/working on it"
    4. TIMELINE: "We'll update you in [specific timeframe]"
    """
    
    ## Example - Service Outage:
    """
    We're aware that many of you can't access [product] right now.
    
    We know this is disrupting your work, and we're sorry.
    
    Our team is on it. We've identified the issue and are
    working on a fix.
    
    Next update in 30 minutes, or sooner if we have news.
    """
    
    ## What NOT to do:
    """
    ✗ Wait until you have full details
    ✗ Blame third parties (even if true)
    ✗ Minimize ("a small number of users")
    ✗ Use passive voice ("an issue was discovered")
    ✗ Go silent
    """
    
    ## Channel Priority:
    """
    1. Status page (source of truth)
    2. In-app banner (if possible)
    3. Twitter/X (where complaints surface)
    4. Email (if extended outage)
    5. Support channels (arm your team)
    """
    

---
  #### **Name**
Status Page Updates
  #### **Description**
How to write clear, helpful status updates throughout an incident
  #### **When**
Managing ongoing incident communications
  #### **Example**
    # STATUS PAGE COMMUNICATION:
    
    ## Update Cadence:
    """
    - First 2 hours: Every 30 minutes minimum
    - Hours 2-6: Every hour
    - Extended: Every 2-3 hours
    - ALWAYS update when status changes
    """
    
    ## Status Levels:
    """
    INVESTIGATING:
    "We're aware of [issue] and investigating.
    [X]% of users may experience [specific symptom].
    Next update in 30 minutes."
    
    IDENTIFIED:
    "We've identified the cause: [brief, non-technical explanation].
    We're implementing a fix now.
    Estimated resolution: [time or 'unknown - we'll update you']."
    
    MONITORING:
    "We've deployed a fix and are monitoring.
    Service should be restoring for users.
    We'll confirm full resolution in [timeframe]."
    
    RESOLVED:
    "This incident is resolved.
    [Service] is fully operational.
    We'll publish a full postmortem within [timeframe].
    Thank you for your patience."
    """
    
    ## Good vs Bad Updates:
    """
    BAD: "We're still working on it."
    
    GOOD: "We've ruled out database issues and are now
    focusing on our payment provider integration.
    Our lead engineer is on a call with Stripe.
    Next update in 20 minutes."
    
    Specific > Vague. Progress > Platitudes.
    """
    

---
  #### **Name**
The Public Apology Framework
  #### **Description**
How to apologize when your company has made a significant mistake
  #### **When**
A genuine apology is needed, not just incident acknowledgment
  #### **Example**
    # PUBLIC APOLOGY STRUCTURE:
    
    ## The Five Parts:
    """
    1. ACKNOWLEDGE - What happened (specifically)
    2. RESPONSIBILITY - We did this (not "mistakes were made")
    3. IMPACT - What this meant for you (empathy)
    4. ACTION - What we're doing about it
    5. PREVENTION - How we'll prevent recurrence
    """
    
    ## Example - Data Exposure:
    """
    Subject: We Let You Down
    
    Last Tuesday, we discovered that [specific data] for
    [number] users was accessible to other logged-in users
    for approximately 4 hours.
    
    This is our fault. A code change we deployed had a bug
    that bypassed our access controls. This should never
    have reached production.
    
    We know you trusted us with your data. We violated
    that trust, and we're deeply sorry.
    
    Here's what we've done:
    - Reverted the change within 2 hours of discovery
    - Audited all access logs - [X users] had data viewed
    - Contacted affected users directly
    - Engaged a third-party security firm to audit our process
    
    To prevent this from happening again:
    - All access control changes now require security review
    - We're implementing automated access control testing
    - We're adding real-time anomaly detection
    
    If you were affected, you'll receive a separate email
    with specific details about your account.
    
    I take personal responsibility for this failure.
    
    [Founder Name]
    """
    
    ## Apology Anti-Patterns:
    """
    ✗ "We apologize for any inconvenience"
       → "We're sorry we broke your workflow"
    
    ✗ "Mistakes were made"
       → "We made a mistake"
    
    ✗ "We take security seriously"
       → [Show, don't tell - describe actions]
    
    ✗ "A small number of users"
       → Give the real number if possible
    
    ✗ "We're sorry you feel..."
       → "We're sorry we did..."
    """
    

---
  #### **Name**
Internal-First Communication
  #### **Description**
Ensuring your team knows before the public does
  #### **When**
Any crisis that will become public
  #### **Example**
    # INTERNAL COMMUNICATION PRIORITY:
    
    ## Why Internal First:
    """
    - Your team will be asked by friends/family
    - Support needs to know what to say
    - Nothing worse than learning from Twitter
    - Aligned team = consistent message
    """
    
    ## Internal Communication Template:
    """
    Subject: [URGENT] Incident - What's Happening and What to Say
    
    WHAT HAPPENED:
    [Clear explanation - more detail than public version]
    
    WHAT WE'RE DOING:
    [Current actions, who's leading]
    
    WHAT TO SAY IF ASKED:
    [Approved messaging - can copy/paste]
    
    WHAT NOT TO SAY:
    [Specific things to avoid]
    
    WHERE TO DIRECT QUESTIONS:
    [Specific person/channel]
    
    TIMELINE:
    [When we'll update internally next]
    """
    
    ## Timing:
    """
    1. Alert leadership immediately
    2. Brief support/CS within 15 minutes
    3. All-hands within 30 minutes (for major issues)
    4. THEN go external
    
    Exception: If it's already public, parallel track.
    """
    

---
  #### **Name**
Post-Crisis Recovery
  #### **Description**
Rebuilding trust after a crisis has passed
  #### **When**
The immediate crisis is resolved but trust needs repair
  #### **Example**
    # TRUST RECOVERY FRAMEWORK:
    
    ## The Postmortem (Public):
    """
    Publish within 3-5 days of resolution.
    
    Structure:
    1. What happened (timeline, technical but accessible)
    2. Why it happened (root cause)
    3. How we fixed it
    4. What we're doing to prevent recurrence
    5. Thank you to affected users
    
    Tone: Humble, specific, technical-but-readable.
    
    Examples to study:
    - GitLab's database incident postmortem
    - Cloudflare's outage reports
    - Linear's transparency posts
    """
    
    ## Ongoing Actions:
    """
    Week 1:
    - Postmortem published
    - Direct outreach to most affected customers
    - Credit/compensation if appropriate
    
    Month 1:
    - Progress update on prevention measures
    - Follow-up with enterprise customers
    
    Quarter 1:
    - Publish learnings/improvements
    - Consider blog post on what you learned
    """
    
    ## Measuring Trust Recovery:
    """
    - NPS change (survey 2 weeks after)
    - Churn in affected cohort
    - Support ticket sentiment
    - Social mention sentiment
    - Customer conversation tone
    """
    
    ## The Counterintuitive Truth:
    """
    Companies that handle crises well often emerge with
    MORE trust than before. Customers think:
    
    "If this is how they handle problems, I can trust
    them when things go wrong."
    
    A crisis is an opportunity to demonstrate your values.
    """
    

---
  #### **Name**
Escalation Communication
  #### **Description**
How to communicate when things are getting worse, not better
  #### **When**
The crisis is extending or escalating
  #### **Example**
    # ESCALATION COMMUNICATION:
    
    ## When to Escalate Messaging:
    """
    - Incident extending beyond initial estimate
    - New impact discovered
    - Root cause more serious than thought
    - Media attention increasing
    - Customer impact worse than stated
    """
    
    ## Escalation Update Template:
    """
    UPDATE - [Time]:
    
    We need to share an update on the ongoing [issue].
    
    WHAT'S CHANGED:
    [Specific new information]
    
    WHY THIS IS TAKING LONGER:
    [Honest explanation]
    
    CURRENT STATUS:
    [Where we are now]
    
    NEW TIMELINE:
    [Updated estimate, or "we don't know yet"]
    
    WHAT WE'RE DOING:
    [Specific actions - who's working on what]
    
    We know this is frustrating. We're as frustrated as you
    are, and we're throwing everything we have at this.
    
    Next update: [Time]
    """
    
    ## CEO/Founder Escalation:
    """
    For major incidents (>2 hours, data, security):
    
    Founder should communicate directly:
    - Personal email or Twitter thread
    - Shows it's being taken seriously
    - Humanizes the company
    - "I'm personally overseeing this"
    
    This isn't about ego - it's about demonstrating
    that leadership is engaged.
    """
    

## Anti-Patterns


---
  #### **Name**
The "Inconvenience" Dismissal
  #### **Description**
Minimizing customer impact with corporate language
  #### **Why**
    "We apologize for any inconvenience" is the most rage-inducing phrase
    in crisis communications. It minimizes real impact and signals that
    you don't understand what you've done.
    
  #### **Instead**
    Name the actual impact:
    ✗ "We apologize for any inconvenience"
    ✓ "We know this broke your workflow and cost you time"
    ✓ "We understand this affected your customers too"
    ✓ "We know you had to explain this to your team"
    

---
  #### **Name**
The Lawyer's Apology
  #### **Description**
Non-apologies designed to avoid liability
  #### **Why**
    "We're sorry you feel that way" or "We regret that this occurred"
    aren't apologies. Customers can smell legal review, and it makes
    the company seem more concerned with liability than people.
    
  #### **Instead**
    Genuine apologies take responsibility:
    ✗ "We regret that this situation occurred"
    ✓ "We made a mistake and we're sorry"
    ✗ "We're sorry if anyone was affected"
    ✓ "We're sorry we affected [number] of you"
    

---
  #### **Name**
The Slow Roll
  #### **Description**
Waiting for complete information before communicating
  #### **Why**
    Silence is interpreted as either incompetence (they don't know) or
    malice (they're hiding something). Every minute of silence erodes
    trust faster than imperfect communication.
    
  #### **Instead**
    Communicate what you know:
    "We're aware of [issue]. Still investigating. More in 30 minutes."
    
    This buys time while showing you're responsive.
    

---
  #### **Name**
The Blame Shift
  #### **Description**
Pointing fingers at vendors, partners, or circumstances
  #### **Why**
    Even if AWS caused your outage, your customers chose YOU.
    Blaming others makes you look like you don't own your product.
    It's also irrelevant to the customer who just wants it fixed.
    
  #### **Instead**
    Own it first, explain later:
    ✗ "Due to an AWS outage beyond our control..."
    ✓ "We're experiencing an outage affecting [X].
       We're working with our infrastructure provider
       to resolve this as quickly as possible."
    

---
  #### **Name**
The Passive Voice Hide
  #### **Description**
Using passive voice to obscure responsibility
  #### **Why**
    "Mistakes were made" or "An issue was discovered" removes agency.
    It sounds like the crisis happened TO the company rather than
    being something the company DID. It feels evasive.
    
  #### **Instead**
    Active voice, clear ownership:
    ✗ "A security vulnerability was discovered"
    ✓ "We discovered a security vulnerability in our code"
    ✗ "Data was exposed"
    ✓ "We exposed customer data"
    

---
  #### **Name**
The Overstatement
  #### **Description**
Promising things you can't guarantee in the heat of crisis
  #### **Why**
    "This will never happen again" is a promise you probably can't keep.
    Overstating your response sets you up for a second crisis when
    something similar happens.
    
  #### **Instead**
    Honest about improvement:
    ✗ "This will never happen again"
    ✓ "We're implementing [specific measures] to reduce the
       likelihood and impact of similar issues"
    

---
  #### **Name**
The One-and-Done
  #### **Description**
Sending one message and disappearing
  #### **Why**
    Crisis communication isn't a single message - it's an ongoing
    conversation. Going silent after initial acknowledgment is almost
    as bad as never responding.
    
  #### **Instead**
    Commit to update cadence:
    - Update every 30-60 minutes during active incident
    - Daily updates for extended issues
    - Postmortem within 1 week
    - Follow-up on prevention measures
    