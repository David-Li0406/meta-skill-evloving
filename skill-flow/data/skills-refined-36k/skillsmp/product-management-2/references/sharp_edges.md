# Product Management - Sharp Edges

## Solution First Syndrome

### **Id**
solution-first-syndrome
### **Summary**
Starting with a solution instead of a problem
### **Severity**
critical
### **Situation**
  "Let's build a notification center!" "We need to add social features!"
  Skipping: What problem does this solve? Who has it? Is it their top problem?
  
### **Why**
  You build the wrong thing—beautifully. Feature ships, no one uses it.
  "Users asked for it" = they asked for a solution to a problem you didn't explore.
  Time and resources wasted on features nobody needs.
  
### **Solution**
  # Start with problem statements:
  "Users are missing important updates because..."
  Not: "Users want notifications because..."
  
  # Validate the problem first:
  - How many users have this problem?
  - How severe is it?
  - What's the workaround today?
  
  # Flip solution requests to problems:
  User: "Add export to Excel"
  PM: "What are you trying to accomplish?"
  User: "I need to share reports with my boss"
  Real problem: Report sharing, not Excel
  
  # Problem validation signals:
  □ Are they doing workarounds?
  □ Would they pay for a solution?
  □ Is it mentioned unprompted?
  □ Top 3 problem for this persona?
  
### **Symptoms**
  - Features built that users don't use
  - Requests taken at face value
  - No problem validation before building
  - Solution in PRD before problem
### **Detection Pattern**


## Roadmap Theater

### **Id**
roadmap-theater
### **Summary**
Treating roadmaps as commitments instead of hypotheses
### **Severity**
critical
### **Situation**
  Q1 Roadmap: Feature A ✓, Feature B ✓, Feature C ✓. All shipped!
  Q1 Outcomes: Retention unchanged, Revenue unchanged, NPS dropped.
  "But we hit the roadmap!"
  
### **Why**
  Roadmaps are hypotheses, not promises. Shipping features is output, not outcome.
  Roadmap accuracy ≠ product success. Teams optimize for hitting roadmap
  instead of achieving goals.
  
### **Solution**
  # Outcome-based roadmaps:
  Q1 Goal: Improve activation from 30% to 45%
  Bets: Simplified onboarding, Welcome wizard, Template library
  
  Shipping all 3 is irrelevant if activation stays at 30%
  
  # Continuous reprioritization:
  What did we learn this week?
  Does it change our bets?
  Should we pivot mid-quarter?
  
  # Communicate uncertainty:
  "Now" - Building (committed)
  "Next" - Planned (high confidence)
  "Later" - Exploring (will change)
  
  # Celebrate outcomes, not shipments:
  Shipped feature → Table stakes
  Moved metric → Celebrate
  Killed a project early → Also celebrate
  
### **Symptoms**
  - Celebrating features shipped, not outcomes achieved
  - Roadmap locked for quarters
  - No learning incorporated
  - Success = hitting dates
### **Detection Pattern**


## Stakeholder Hostage

### **Id**
stakeholder-hostage
### **Summary**
Building what stakeholders demand instead of what users need
### **Severity**
high
### **Situation**
  CEO: "Add gamification!" Sales: "We need this to close the deal!"
  Support: "Users keep asking for X!" Marketing: "Competitor has it!"
  PM: "Okay, okay, I'll add it all..."
  
### **Why**
  Product becomes a political battlefield instead of a user solution.
  Bloated product with no coherent vision. Every feature is "urgent."
  Real user problems ignored.
  
### **Solution**
  # Separate input from decision:
  Everyone can provide context
  PM synthesizes into recommendations
  Single decision-maker identified
  
  # Translate demands to problems:
  CEO: "Add gamification"
  PM: "What problem are you trying to solve?"
  CEO: "Users aren't engaged enough"
  PM: "Let me research engagement solutions"
  
  # Use data as arbiter:
  "Let's test this hypothesis"
  Removes personal opinion
  Evidence-based decisions
  
  # Build trust bank:
  Small wins build credibility
  When you say no with credibility, it sticks
  
### **Symptoms**
  - Roadmap driven by loudest voices
  - No coherent product strategy
  - PM can't say no
  - Political wins over user wins
### **Detection Pattern**


## Spec Mountain

### **Id**
spec-mountain
### **Summary**
Writing massive specs before learning anything
### **Severity**
high
### **Situation**
  Before building: 30-page PRD, complete wireframes, technical architecture,
  all edge cases mapped, 6 months of planning. Then: build 3 months, ship,
  users don't want it. All documentation = waste.
  
### **Why**
  Detailed specs are a form of procrastination. Avoiding uncertainty by
  creating false certainty. The spec isn't the product—the product is.
  Waterfall in agile clothing.
  
### **Solution**
  # Thin specs, fast learning:
  One-page brief: Problem, hypothesis, success metric
  Build the smallest thing to learn
  Add detail as you learn
  
  # Progressive documentation:
  Discovery: One-pager
  Validation: Add details
  Building: Full spec (but still minimal)
  Never spec what you haven't validated
  
  # Spec size by stage:
  Discovery: One-pager (problem + hypothesis)
  Validation: 2-3 pages (add what you learned)
  Building: 5-10 pages (enough to build, no more)
  
### **Symptoms**
  - Specs written before validation
  - 30+ page PRDs
  - Weeks of planning before any testing
  - Specs never updated after learning
### **Detection Pattern**


## Metric Trap

### **Id**
metric-trap
### **Summary**
Optimizing for metrics that don't drive business outcomes
### **Severity**
high
### **Situation**
  Team metric: Daily Active Users. Strategy: Push notifications.
  Result: DAU up 40%! Reality: Users annoyed, Uninstalls up,
  Revenue unchanged, NPS tanking. "But we hit our metric!"
  
### **Why**
  Metrics are proxies, not goals. Any metric, optimized hard enough, breaks.
  Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure."
  
### **Solution**
  # North star + input metrics:
  North Star: Value delivered (hard to game)
  Input metrics: Things you can influence
  Watch both—never just input
  
  # Counter-metrics:
  If you optimize engagement, watch churn
  If you optimize signups, watch activation
  Balance keeps you honest
  
  # Metric stack:
  North Star: [What success ultimately looks like]
  Counter: [What could go wrong if we over-optimize]
  Leading: [What we can influence today]
  Lagging: [What proves we were right]
  
  # Metric test:
  "If we hit this metric, would the business succeed?"
  If no, find a better metric.
  
### **Symptoms**
  - Gaming metrics without business impact
  - Team metrics conflict with company goals
  - No counter-metrics defined
  - Celebrating vanity metrics
### **Detection Pattern**


## Estimate Fiction

### **Id**
estimate-fiction
### **Summary**
Treating engineering estimates as commitments
### **Severity**
high
### **Situation**
  PM: "How long will this take?" Engineer: "Maybe 2 weeks?"
  PM to stakeholders: "It'll be done in 2 weeks"
  Reality: 4 weeks. Everyone angry. Engineer stops estimating honestly.
  
### **Why**
  Estimates are guesses about uncertain work. Uncertainty doesn't go away
  by demanding certainty. Padding just adds waste. Trust erodes.
  Death spiral of unrealistic expectations.
  
### **Solution**
  # Communicate ranges, not points:
  "1-3 weeks depending on what we find"
  Under-promise specific, over-promise range
  
  # Estimate in confidence levels:
  High confidence: We've done this before
  Medium confidence: Similar work, some unknowns
  Low confidence: New territory, could be anything
  
  # Time-box discovery:
  "We'll spend 2 days spiking and then re-estimate"
  Reduces uncertainty before committing
  
  # Reframe the question:
  Not: "When will this be done?"
  But: "What can we learn in 2 weeks?"
  
### **Symptoms**
  - Estimates treated as commitments
  - Engineers pad estimates
  - Constant schedule slippage
  - Blame when estimates wrong
### **Detection Pattern**


## Consensus Trap

### **Id**
consensus-trap
### **Summary**
Waiting for everyone to agree before deciding
### **Severity**
high
### **Situation**
  Meeting 1: Present idea. "Let me think about it." "Have you considered..."
  Meeting 2: More discussion. "I'm not sure about..." "What if we also..."
  Meeting 7: Compromise. Original idea killed. Watered-down version nobody loves.
  
### **Why**
  Consensus is not agreement—it's the absence of objection. Great products
  require conviction, not consensus. Committee decisions are safe but mediocre.
  Speed matters.
  
### **Solution**
  # Clear decision-maker:
  Whose call is this? (State it upfront)
  RACI: Responsible, Accountable, Consulted, Informed
  Consult ≠ Veto
  
  # Disagree and commit:
  Make the decision
  Let objections be recorded
  Move forward together
  
  # Time-box decisions:
  "We're deciding this by Friday"
  Deadline forces clarity
  No decision = a decision (usually bad)
  
  # One-way vs two-way doors:
  Two-way (reversible): Decide fast
  One-way (irreversible): Deliberate
  Most decisions are two-way
  
### **Symptoms**
  - Decisions take weeks
  - Meetings without outcomes
  - Watered-down compromises
  - Everyone has veto power
### **Detection Pattern**


## Feature Factory

### **Id**
feature-factory
### **Summary**
Shipping features without measuring their impact
### **Severity**
critical
### **Situation**
  Q1: Shipped 12 features. Q2: Shipped 15 features. Q3: Shipped 18 features.
  Impact: Unknown. Learnings: None. Product: Bloated mess.
  "But look how productive we are!"
  
### **Why**
  Features are not progress—outcomes are. Shipping without measuring is guessing.
  Most features don't move the needle. You never learn what works.
  
### **Solution**
  # Every feature has a hypothesis:
  "We believe [feature] will [outcome] for [users]"
  Measurable outcome, specific users
  
  # Every feature has success criteria:
  Launch: How we'll measure success
  4 weeks later: Was it successful?
  No measure = no learning
  
  # Kill non-performers:
  Feature shipped, no impact → Remove it
  Reduces complexity
  Frees up space for what works
  
  # Feature lifecycle:
  1. Hypothesis (what we believe)
  2. Success criteria (how we'll know)
  3. Build (minimum to test)
  4. Measure (did it work?)
  5. Decide (keep, iterate, kill)
  
### **Symptoms**
  - Features never measured post-launch
  - No features ever removed
  - Can't answer "what worked?"
  - Roadmap is features, not outcomes
### **Detection Pattern**


## Scope Creep Monster

### **Id**
scope-creep-monster
### **Summary**
Scope constantly expanding during development
### **Severity**
high
### **Situation**
  Original scope: Login page. During build: "Add social login" "What about SSO?"
  "We need password strength meter" "Add biometrics" "What about MFA?"
  Original: 2 weeks. Actual: 3 months.
  
### **Why**
  Scope creep feels like improvement. It's actually failure to prioritize.
  Each addition has hidden cost. Projects never ship, or ship late and bloated.
  
### **Solution**
  # V1 mindset:
  What's the smallest thing that's useful?
  Ship it, then improve
  V1 is launch, not final
  
  # Explicit scope document:
  In scope: [List]
  Out of scope: [Also list]
  Add to "V2 ideas" not current build
  
  # Trade-offs, not additions:
  "We can add X if we remove Y"
  Fixed time, flexible scope
  Or: Fixed scope, flexible time (pick one)
  
  # Scope defense:
  "Great idea for V2!"
  "What would we cut to add this?"
  "Let's see if users actually need it first."
  
### **Symptoms**
  - Scope grows during development
  - No explicit out-of-scope list
  - Projects always late
  - Everything is V1 priority
### **Detection Pattern**


## User Research Vacuum

### **Id**
user-research-vacuum
### **Summary**
Building based on assumptions instead of user evidence
### **Severity**
critical
### **Situation**
  PM: "Users want this." Interviewer: "How do you know?"
  PM: "It's obvious." / "I would want it." / "The CEO said so." / "Competitor has it."
  Evidence: None.
  
### **Why**
  You are not your user. Your intuition is built on your experience.
  Users are surprising—that's the point. You build for imaginary users.
  
### **Solution**
  # Continuous discovery:
  Talk to users every week
  Not a phase—a habit
  Doesn't have to be formal
  
  # Multiple evidence types:
  Quantitative: Usage data, surveys
  Qualitative: Interviews, observation
  Behavioral: What they do, not say
  
  # Problem interviews, not solution interviews:
  "Tell me about last time you..."
  Not: "Would you use feature X?"
  
  # Kill assumptions explicitly:
  List assumptions behind the feature
  Which are validated? Which are risks?
  Validate the risky ones
  
  # User research minimum:
  - 5 user conversations per week
  - Data review every sprint
  - Persona validation quarterly
  
### **Symptoms**
  - No recent user interviews
  - Assumptions not documented
  - PM intuition drives decisions
  - Surprised when features fail
### **Detection Pattern**


## Launch And Forget

### **Id**
launch-and-forget
### **Summary**
Shipping features and immediately moving to the next thing
### **Severity**
high
### **Situation**
  Sprint 1: Build feature A. Sprint 2: Build feature B. Sprint 3: Build feature C.
  Feature A problems: "We'll fix it later." "We're focused on new stuff."
  Later never comes. Feature A: Abandoned, broken, useless.
  
### **Why**
  Launch is the beginning, not the end. Real product work is iteration.
  The first version is rarely right. Features degrade without attention.
  
### **Solution**
  # Post-launch review:
  2-4 weeks after launch: How's it doing?
  What's working? What's not?
  What did we learn?
  
  # Iteration budget:
  20-30% of capacity for improving existing
  Not just bugs—actual improvement
  Protect this time
  
  # Feature owner mindset:
  Someone owns each feature
  Responsible for its success
  Advocates for improvements
  
  # Launch checklist:
  □ Success metrics defined
  □ Instrumentation in place
  □ 2-week review scheduled
  □ Kill criteria defined
  
### **Symptoms**
  - No post-launch reviews
  - Old features never improved
  - Technical debt accumulates
  - Always building new, never improving existing
### **Detection Pattern**


## Stakeholder Surprise

### **Id**
stakeholder-surprise
### **Summary**
Surprising stakeholders with decisions at the last minute
### **Severity**
high
### **Situation**
  PM works heads down for 2 months. Launch day presentation:
  Stakeholders: "Why wasn't I consulted?" "This isn't what I expected"
  "We need to go back to the drawing board."
  All work wasted. Trust broken. Future: Micro-management.
  
### **Why**
  Stakeholder surprises create stakeholder anxiety. Anxiety creates control.
  Control slows everything down. No buy-in means no support.
  
### **Solution**
  # Early and ugly:
  Share early, when it's rough
  "Here's our thinking, what are we missing?"
  Ugly prototypes prevent polished surprises
  
  # Regular updates:
  Weekly status (async is fine)
  What we did, what we learned, what's next
  No news is not good news
  
  # Explicit decision points:
  "We're deciding X next week"
  "Here are the options"
  "Here's our recommendation"
  
  # No launch day surprises:
  Everyone's seen it
  Everyone's been heard
  Launch is execution, not reveal
  
### **Symptoms**
  - Stakeholders blindsided
  - Major rework after reveals
  - Increasing micro-management
  - Trust deficit with leadership
### **Detection Pattern**
