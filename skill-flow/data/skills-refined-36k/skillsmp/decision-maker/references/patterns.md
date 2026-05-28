# Decision Maker

## Patterns


---
  #### **Name**
One-Way vs Two-Way Door
  #### **Description**
Classify decision reversibility to apply appropriate rigor
  #### **When**
Any significant technical decision
  #### **Example**
    # The Bezos Framework:
    # One-way doors: Hard/impossible to reverse, require careful analysis
    # Two-way doors: Easily reversible, make quickly and learn
    
    # Classification criteria:
    """
    Reversal cost > 3-6 months of team capacity? → One-way door
    Creates business disruption to undo? → One-way door
    Everything else? → Two-way door
    """
    
    # ONE-WAY DOORS (careful analysis required):
    - Programming language choice
    - Database engine choice
    - Cloud provider selection
    - Architectural style (monolith vs microservices)
    - Data model schema (once populated)
    - Public API contracts (once adopted)
    - Security/compliance architecture
    
    # TWO-WAY DOORS (decide quickly):
    - UI framework version
    - Monitoring/logging tool
    - Internal API design (before widespread use)
    - Testing framework
    - Code style rules
    - Deployment schedule
    - Feature flags
    
    # Process by door type:
    """
    One-way door:
    - Broad stakeholder involvement
    - Written analysis with alternatives
    - ADR documenting context and rationale
    - Review period for objections
    
    Two-way door:
    - Individual or small team decides
    - Minimal documentation
    - Bias toward action
    - Expect to revisit later
    """
    

---
  #### **Name**
Second-Order Thinking
  #### **Description**
Trace consequences beyond the immediate effect
  #### **When**
Evaluating any decision with potential long-term impact
  #### **Example**
    # Ask: "And then what happens?" repeatedly
    
    # DECISION: Add caching to speed up the API
    
    # First-order effect:
    # - API gets faster ✓
    
    # Second-order effects (ask "and then what?"):
    # - Cache invalidation complexity (who owns this?)
    # - Stale data bugs (how do users experience this?)
    # - Debugging becomes harder (how to know if cache is cause?)
    # - Memory usage increases (do we need bigger instances?)
    # - New failure mode: cache service outage (graceful degradation?)
    
    # Third-order effects:
    # - Team needs caching expertise (hiring/training cost)
    # - Every new feature needs to consider cache (velocity slowdown)
    # - Cache becomes critical path (needs monitoring, on-call)
    
    # FRAMEWORK: Draw the consequence chain
    """
    Decision
      └→ First-order effect (immediate, obvious)
          └→ Second-order effect (what does that cause?)
              └→ Third-order effect (and what does THAT cause?)
    """
    
    # Stop when effects become speculative or negligible
    

---
  #### **Name**
Trade-off Matrix
  #### **Description**
Structured comparison of options against weighted criteria
  #### **When**
Multiple viable options with different strengths
  #### **Example**
    # Example: Choosing a database for new service
    
    # Step 1: Define criteria and weights (must total 100%)
    criteria = {
      "query_performance": 25,      # Most important
      "operational_simplicity": 20,
      "team_familiarity": 20,
      "cost": 15,
      "ecosystem_tools": 10,
      "future_scalability": 10
    }
    
    # Step 2: Score each option (1-5) on each criterion
    options = {
      "postgres": {
        "query_performance": 4,
        "operational_simplicity": 4,
        "team_familiarity": 5,     # Team knows it well
        "cost": 4,
        "ecosystem_tools": 5,
        "future_scalability": 3
      },
      "mongodb": {
        "query_performance": 3,
        "operational_simplicity": 3,
        "team_familiarity": 2,     # New to team
        "cost": 3,
        "ecosystem_tools": 4,
        "future_scalability": 4
      }
    }
    
    # Step 3: Calculate weighted scores
    # postgres: (4*25 + 4*20 + 5*20 + 4*15 + 5*10 + 3*10) / 100 = 4.2
    # mongodb:  (3*25 + 3*20 + 2*20 + 3*15 + 4*10 + 4*10) / 100 = 2.9
    
    # Step 4: Document the decision with context
    """
    DECISION: PostgreSQL
    KEY FACTORS: Team familiarity (5/5) and ecosystem (5/5)
    ACCEPTED TRADE-OFFS: Lower scalability score (3/5)
    REVISIT IF: Data volume exceeds 1TB or query patterns change
    """
    

---
  #### **Name**
Architecture Decision Record (ADR)
  #### **Description**
Documented decision with context, rationale, and consequences
  #### **When**
Any one-way door decision or decision that warrants explanation
  #### **Example**
    # ADR Template (MADR format)
    
    """
    # ADR-001: Use PostgreSQL for primary database
    
    ## Status
    Accepted (2024-01-15)
    
    ## Context
    We need a database for the new Order service. Expected volume:
    100k orders/day, 99.9% reads, complex queries for reporting.
    
    Team has 5 years experience with PostgreSQL, none with alternatives.
    
    ## Decision
    We will use PostgreSQL 15 with standard AWS RDS deployment.
    
    ## Rationale
    - Team expertise eliminates ramp-up time (weeks saved)
    - Strong ecosystem for monitoring and tooling
    - Query needs are well-suited to relational model
    - Acceptable trade-off on horizontal scaling
    
    ## Alternatives Considered
    
    ### MongoDB
    Rejected: Team would need 2+ months training. Aggregation
    queries for reporting are more complex than SQL.
    
    ### DynamoDB
    Rejected: Query flexibility insufficient for reporting needs.
    Would require additional data pipeline for analytics.
    
    ## Consequences
    
    ### Positive
    - Faster development due to team familiarity
    - Rich ecosystem of tools and libraries
    - Strong consistency model
    
    ### Negative
    - Vertical scaling limits (revisit at 1TB)
    - Need to manage schema migrations
    - Connection pooling complexity at scale
    
    ## Review Triggers
    - Data volume exceeds 500GB
    - Read latency p99 exceeds 100ms
    - Team composition changes significantly
    """
    

---
  #### **Name**
Timeboxed Decision
  #### **Description**
Set deadline to prevent analysis paralysis
  #### **When**
Decision is dragging without new information
  #### **Example**
    # The pattern:
    # 1. Set a timebox (hours for two-way, days for one-way)
    # 2. Gather information until timebox expires
    # 3. Decide with available information
    # 4. Accept that more information always exists
    
    # Example dialogue:
    """
    Team: "Should we use React or Vue?"
    
    Decision Maker:
    "This is a two-way door - UI frameworks can be changed.
     Let's timebox this to 2 hours.
    
     Spend 1 hour: List must-have requirements
     Spend 30 min: Quick evaluation against requirements
     Spend 30 min: Make decision and document
    
     If we can't decide in 2 hours, we'll default to React
     (team has more experience) and revisit in 3 months."
    """
    
    # Why this works:
    # - Prevents endless debate
    # - Forces focus on what actually matters
    # - Acknowledges that perfect information doesn't exist
    # - Creates bias toward action
    

---
  #### **Name**
Disagree and Commit
  #### **Description**
Proceed despite disagreement once decision is made
  #### **When**
Team has genuine disagreement on a decision
  #### **Example**
    # The principle: Once a decision is made, everyone commits fully,
    # even those who disagreed. Sabotage-by-half-effort helps no one.
    
    # How it works:
    """
    1. Ensure everyone has genuinely been heard
    2. Make the decision (usually by designated owner)
    3. Explicitly state: "This is the decision. Who disagrees?"
    4. Record disagreements for future learning
    5. Everyone commits to making the decision succeed
    6. Set review date to evaluate the outcome
    """
    
    # The commitment means:
    # - No "I told you so" if it fails
    # - Full effort to make it work
    # - Raise concerns early if new data emerges
    # - Honest evaluation at review date
    
    # Document disagreement for learning:
    """
    ## Dissenting View (recorded at decision time)
    Engineer A disagreed, believing microservices would slow
    development. If velocity drops >20% after 6 months,
    we should revisit this decision.
    """
    

## Anti-Patterns


---
  #### **Name**
Analysis Paralysis
  #### **Description**
Endless research and discussion, never deciding
  #### **Why**
    More information feels safe. But decisions have deadlines, and
    the cost of not deciding compounds. Often the "perfect" choice
    doesn't exist, and any choice would have been better than none.
    
  #### **Instead**
Timebox decisions. If you can't decide with current info, no amount of research will help.

---
  #### **Name**
HiPPO Decisions
  #### **Description**
Highest Paid Person's Opinion wins by default
  #### **Why**
    Seniority doesn't equal correctness. When decisions are made by
    title rather than merit, the organization loses access to better
    ideas from junior people, and senior people lose touch with reality.
    
  #### **Instead**
Delegate decisions to people closest to the problem. Use seniority for tie-breakers.

---
  #### **Name**
Reversibility Theater
  #### **Description**
Treating every decision as a one-way door
  #### **Why**
    When every choice requires committees and documents, velocity dies.
    Teams become afraid to make any decision. Simple choices take weeks.
    The irony: by being "careful," you're making a much worse meta-decision.
    
  #### **Instead**
Default to two-way door classification. Only escalate when reversal cost is truly high.

---
  #### **Name**
Decision Amnesia
  #### **Description**
Making decisions without documentation
  #### **Why**
    Without records, you'll repeat the same debates. New team members
    won't understand why things are the way they are. You can't learn
    from past decisions if you don't remember the context.
    
  #### **Instead**
Lightweight ADRs for one-way doors. Even a Slack message is better than nothing.

---
  #### **Name**
Consensus Requirement
  #### **Description**
Needing everyone to agree before proceeding
  #### **Why**
    Unanimous agreement is rare and shouldn't be required. Chasing
    consensus delays decisions indefinitely. Strong opinions become
    vetoes, and the loudest voices win.
    
  #### **Instead**
Disagree and commit. Document dissent, decide, and revisit with data.

---
  #### **Name**
Ignoring Second-Order Effects
  #### **Description**
Only considering immediate consequences
  #### **Why**
    The obvious effect is rarely the most important. Caching speeds up
    the API (first order) but creates invalidation complexity, debugging
    difficulty, and operational overhead (second order).
    
  #### **Instead**
Always ask "and then what?" at least twice.