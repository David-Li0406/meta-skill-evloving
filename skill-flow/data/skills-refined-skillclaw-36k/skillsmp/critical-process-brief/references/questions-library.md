# Critical Questions Library for Processes

This library contains challenging questions designed to expose blind spots, find weaknesses, and stress-test operational thinking.

## Approach

**Goal:** Find what the user DOESN'T know, not just what they do know.

**Tactics:**
- Ask about specific scenarios
- Push for numbers and details
- Probe edge cases
- Identify single points of failure
- Challenge "it's straightforward" statements
- Ask "what if" repeatedly

---

## CORE - Podstawy procesu

### 1. Kluczowe procesy biznesowe

**Identifying blind spots:**
- "Walk me through every step from when a customer first hears about you to when they get value. What am I missing?"
- "What happens between [Step A] and [Step B]? That seems like a big jump."
- "You mentioned the main process. What about support? Returns? Billing? Compliance?"
- "What processes run in the background that customers don't see?"

**Testing completeness:**
- "If I'm your first customer tomorrow, what needs to happen?"
- "What happens after the customer pays? Walk me through delivery."
- "How do you handle [support tickets, refunds, changes, cancellations]?"
- "What about internal processes - hiring, finance, legal?"

**Exposing assumptions:**
- "You said 'then we fulfill the order' - what specifically does that involve?"
- "How many steps are in your 'simple' onboarding process?"
- "When you say 'customer support,' what exactly does that mean operationally?"

---

### 2. Aktorzy / Role

**Finding gaps:**
- "Who specifically does each step? Name a person or role."
- "Who makes decisions when [X situation] occurs?"
- "What happens if [key person] is on vacation or leaves?"
- "Do you actually have people to fill these roles?"

**Testing clarity:**
- "Who's responsible if [specific thing] goes wrong?"
- "If two people think they're both responsible for X, how do you resolve that?"
- "What happens when responsibilities overlap? Who has final say?"

**Exposing dependencies:**
- "You said 'the team will handle it' - which specific person?"
- "How many people need to touch this before it's complete?"
- "Are you depending on external people you don't control?"

**Testing capacity:**
- "How many hours per week will [role] spend on this?"
- "Can one person really do [all these things]?"
- "When volume doubles, who's overwhelmed first?"

---

### 3. Flow procesów

**Getting specific:**
- "Walk me through step by step. What's literally the first action?"
- "Then what? And after that?"
- "You said 'we process it' - what are the actual steps in 'processing'?"
- "What triggers this process to start?"

**Finding decision points:**
- "At what points do you need to make a choice?"
- "What are the options at each decision point?"
- "Who makes that decision and how long does it take?"

**Testing exception paths:**
- "What happens if [Step 3] fails?"
- "What if the customer provides incomplete information?"
- "What if [System X] is down when you need it?"
- "How do you recover from errors?"

**Exposing handoffs:**
- "Where does this hand off from one person to another?"
- "How does the next person know they need to do their part?"
- "What happens if the handoff is missed?"

---

### 4. Zależności między procesami

**Mapping dependencies:**
- "What has to happen before this process can start?"
- "What's blocked waiting for this to finish?"
- "Can these run in parallel or must they be sequential?"

**Testing critical path:**
- "What's the longest chain of dependent steps?"
- "If we could speed up one thing, what would have biggest impact?"
- "What's the bottleneck in the dependency chain?"

**Finding circular dependencies:**
- "Does Process A depend on Process B which depends on Process A?"
- "How do you break circular dependencies?"

**Testing fragility:**
- "What happens if Process A takes 2x longer than expected?"
- "What if Process B fails completely?"
- "What's your single point of failure in the dependency chain?"

---

## DATA & DECISIONS - Informacje i decyzje

### 5. Inputs / Outputs

**Identifying inputs:**
- "What information do you need before you can start this step?"
- "Where does that information come from?"
- "What if that information is missing or wrong?"
- "Who provides those inputs?"

**Testing outputs:**
- "What gets produced at the end of this step?"
- "Who needs that output? What do they do with it?"
- "What format is it in? Is that the format they need?"
- "How do they know the output is ready?"

**Finding mismatches:**
- "The previous step outputs X, but this step needs Y. How do you transform it?"
- "Is any manual work needed to convert outputs to inputs?"
- "What happens if output quality is poor?"

---

### 6. Decision points

**Identifying decisions:**
- "At what points in the process does someone need to make a choice?"
- "What are they deciding between?"
- "Can this decision be made by a rule or does it need human judgment?"

**Testing criteria:**
- "How do you decide [yes/no, A/B, how much]?"
- "Are the criteria clear and objective?"
- "Could two people make different decisions with the same inputs?"
- "What if the decision criteria aren't met?"

**Testing decision-makers:**
- "Who makes this decision?"
- "How long does it take them to decide?"
- "What if they're unavailable?"
- "Do they have all the information they need to decide?"

**Exposing bottlenecks:**
- "How many decisions does [one person] need to make per day?"
- "Can they keep up when volume increases?"
- "What happens if they're slow to decide?"

---

### 7. Dane / Informacje

**Finding data needs:**
- "What data is critical for this process?"
- "Where is that data stored today?"
- "How do you access it? API? Database query? Asking someone?"
- "How current is the data?"

**Testing data quality:**
- "How do you know the data is accurate?"
- "What if it's out of date?"
- "What happens if data is wrong?"
- "Who's responsible for keeping data accurate?"

**Identifying data gaps:**
- "What data do you need that you don't have?"
- "What data exists in multiple places?"
- "How do you keep data in sync across systems?"

**Testing access:**
- "Who can access this data?"
- "What if the person who knows where data is leaves?"
- "Is critical data only in someone's head?"

---

### 8. Handoffy

**Identifying handoffs:**
- "Where does work pass from one person to another?"
- "How does the receiving person know they have work to do?"
- "What information gets passed along?"

**Testing handoff mechanism:**
- "How does the handoff happen? Email? Ticket? Verbal?"
- "What if the email gets lost or ignored?"
- "Is there a record of the handoff?"
- "How do you track if the handoff was successful?"

**Exposing risks:**
- "What happens if Person B is on vacation when A hands off?"
- "What if they misunderstand what needs to be done?"
- "How long does it typically take between handoff and next action?"
- "What's the longest a handoff has taken?"

**Testing at scale:**
- "When you have 10x more handoffs per day, how does this work?"
- "Do handoffs require manual coordination?"

---

## PROBLEMS & EDGE CASES - Problemy

### 9. Pain points / Bottlenecki

**Finding pain:**
- "What's the most frustrating part of this process?"
- "Where does it typically get stuck?"
- "What do people complain about most?"
- "If you could fix one thing, what would it be?"

**Identifying bottlenecks:**
- "What's the slowest step?"
- "Where is capacity limited?"
- "What would break first if volume doubled?"
- "Who's constantly overwhelmed?"

**Testing current state:**
- "How often does this process fail or need to be redone?"
- "What's the error rate?"
- "How much manual intervention is needed?"
- "What workarounds have you built?"

**Exposing hidden costs:**
- "How much time is wasted on [pain point]?"
- "How much does it cost when this fails?"
- "What's the opportunity cost of bottlenecks?"

---

### 10. Edge cases / Wyjątki

**Probing exceptions:**
- "What's the weirdest thing that's happened?"
- "What happens when [specific unusual situation]?"
- "What if the customer provides invalid data?"
- "What if your system is down during a critical moment?"

**Testing error handling:**
- "What happens if [Step 5] fails? Can you retry? Roll back?"
- "What if an external API doesn't respond?"
- "What if payment fails?"
- "How do you handle duplicate submissions?"

**Finding brittle points:**
- "What scenarios have you NOT thought about?"
- "What would completely break your process?"
- "Do you have a manual fallback?"
- "What happens at 3am on Sunday when something breaks?"

**Volume and timing:**
- "What if you get 100 requests at once instead of 10 per day?"
- "What if something takes 10x longer than expected?"
- "What if two processes try to update the same data simultaneously?"

---

### 11. Ryzyka operacyjne

**Identifying single points of failure:**
- "If [person/system/supplier] disappeared tomorrow, what would break?"
- "What's your single point of failure?"
- "What happens if [critical dependency] fails?"

**Testing redundancy:**
- "Do you have a backup for [critical component]?"
- "What if your main supplier can't deliver?"
- "What if your database corrupts?"

**Exposing dependencies:**
- "What are you completely dependent on that you don't control?"
- "What if [partner] changes their terms or pricing?"
- "What if [vendor] goes out of business?"

**Compliance and legal:**
- "What could get you shut down?"
- "What could you get sued for?"
- "Are you compliant with [relevant regulations]?"
- "What happens in an audit?"

**Security and fraud:**
- "How do you prevent fraud?"
- "What if there's a data breach?"
- "What if someone abuses your system?"

---

## REQUIREMENTS - Wymagania

### 12. Czas trwania / SLA

**Getting numbers:**
- "How long does this process take end-to-end?"
- "What's the fastest it's ever completed? Slowest?"
- "What's the average time for each step?"

**Testing commitments:**
- "Have you promised customers a specific timeframe?"
- "Can you consistently meet that commitment?"
- "What percentage of the time do you miss SLA?"
- "What happens when you miss it?"

**Finding delays:**
- "What causes delays?"
- "Where does work sit waiting?"
- "What's the longest someone has waited?"

**Testing at scale:**
- "When volume doubles, how does this affect speed?"
- "Can you maintain SLA at 10x volume?"

---

### 13. Compliance / Regulacje

**Identifying requirements:**
- "What regulations apply to your business?"
- "Do you know all compliance requirements?"
- "Have you talked to a lawyer about this?"

**Testing understanding:**
- "What specifically do you need to do to comply with [regulation]?"
- "How do you prove compliance?"
- "What documentation is required?"
- "Who's responsible for compliance?"

**Exposing gaps:**
- "Are you collecting data that requires compliance?"
- "Do you have proper consents and disclosures?"
- "Are you handling payments? (PCI DSS)"
- "Are you processing EU data? (GDPR)"

**Testing consequences:**
- "What's the penalty for non-compliance?"
- "Have you been audited?"
- "What would an auditor find?"

---

### 14. Wymagania jakościowe

**Setting standards:**
- "What quality standards apply?"
- "What's acceptable error rate?"
- "How do you define 'good quality' for this process?"

**Testing measurement:**
- "How do you measure quality?"
- "Who checks quality and when?"
- "What happens when quality fails?"

**Finding quality gaps:**
- "What's your current error rate?"
- "How often do you need to redo work?"
- "What quality issues do customers complain about?"

**Testing scale:**
- "Can you maintain quality at 10x volume?"
- "Does quality degrade when you're busy?"

---

## TECH & TOOLS - Technologia

### 15. Narzędzia / Systemy

**Identifying tools:**
- "What tools do you use for each step?"
- "Why those specific tools?"
- "Do they do what you need or are you working around limitations?"

**Testing integration:**
- "Do your tools talk to each other?"
- "How much manual work happens between tools?"
- "Are you copying data between systems?"

**Exposing limitations:**
- "What can't your tools do that you need?"
- "What happens when a tool goes down?"
- "Can your tools handle 10x growth?"

**Testing cost:**
- "How much do all these tools cost?"
- "Does cost scale with usage?"
- "Are you paying for features you don't use?"

---

### 16. Integracje

**Mapping integrations:**
- "What systems need to connect?"
- "How are they integrated today?"
- "Is it real-time or batch?"

**Testing reliability:**
- "How often do integrations break?"
- "What happens when an integration fails?"
- "Do you have retry logic?"
- "How long before you notice an integration is down?"

**Exposing gaps:**
- "What integrations are missing?"
- "Where do you manually transfer data?"
- "What's the impact of integration lag?"

**Testing maintainability:**
- "Who built the integrations?"
- "If they leave, can someone else maintain them?"
- "How much work is it to add a new integration?"

---

### 17. Automatyzacja

**Finding manual work:**
- "What's still done manually?"
- "Why haven't you automated it?"
- "How much time is spent on manual work?"

**Testing automation:**
- "What have you automated?"
- "Does the automation work reliably?"
- "What happens when automation fails?"
- "Is there a manual fallback?"

**Prioritizing automation:**
- "What should you automate next?"
- "What's the ROI of automating [specific thing]?"
- "What's too complex or low-volume to automate?"

**Exposing premature automation:**
- "Why automate before you've proven the process works?"
- "Is the manual process understood well enough to automate?"

---

## ECONOMICS & SCALE - Ekonomia

### 18. Koszty operacyjne

**Getting numbers:**
- "How much does this process cost to run?"
- "What's the cost per [customer/order/transaction]?"
- "What's the biggest cost component?"

**Breaking down costs:**
- "How much is labor? Tools? Infrastructure?"
- "What costs are fixed vs. variable?"
- "What would happen to costs if volume doubled?"

**Testing viability:**
- "Is cost per unit higher than revenue per unit?"
- "At what volume do you break even?"
- "Can you afford these costs long-term?"

**Finding savings:**
- "Where could you reduce costs?"
- "What's worth investing in to lower costs?"
- "What expensive thing could be automated?"

---

### 19. Skalowanie

**Testing current limits:**
- "What's your current capacity?"
- "How many [customers/orders/transactions] can you handle?"
- "What breaks first when volume increases?"

**Probing 2x growth:**
- "What happens when volume doubles?"
- "What would you need to change?"
- "Do costs double or less?"

**Probing 10x growth:**
- "What about 10x volume?"
- "Would your process completely break?"
- "What would need to be completely rebuilt?"

**Finding bottlenecks:**
- "What's your constraint on growth?"
- "What can't scale?"
- "Where would you need to hire?"

**Testing assumptions:**
- "You said you'd 'just hire more people' - how many?"
- "Can you really find and train that many people?"
- "Do your tools scale or do you need new ones?"

---

### 20. Metryki procesu

**Identifying metrics:**
- "How do you measure if this process is working?"
- "What metrics do you track?"
- "How often do you review metrics?"

**Testing measurement:**
- "How do you actually measure [metric]?"
- "Is it manual or automated?"
- "How current is the data?"

**Finding blind spots:**
- "What important things are you NOT measuring?"
- "Do you know your error rate? Cycle time? Cost per unit?"
- "What metrics would tell you the process is degrading?"

**Testing action:**
- "When metrics show a problem, what do you do?"
- "Do you have alerts when metrics cross thresholds?"
- "What's an example of using metrics to improve?"

**Exposing vanity:**
- "Are you measuring things that don't actually matter?"
- "Do those metrics tie to business outcomes?"

---

## Cross-Cutting Critical Questions

### "How do you know?"
Use this constantly to push for evidence over assumptions.

**Examples:**
- "How do you know this step takes 2 hours?"
- "How do you know customers are satisfied?"
- "How do you know your error rate is low?"

### "What if?"
Use this to explore edge cases and risks.

**Examples:**
- "What if volume is 10x higher?"
- "What if [key person] quits?"
- "What if [critical system] is down for a day?"
- "What if [assumption] is wrong?"

### "Walk me through..."
Use this to force detailed explanation and expose gaps.

**Examples:**
- "Walk me through exactly what happens when [specific scenario]"
- "Walk me through the last time this failed"
- "Walk me through a specific example end-to-end"

### "Who specifically?"
Use this to avoid vague roles and identify gaps.

**Examples:**
- "Who specifically does this step?"
- "Who specifically decides this?"
- "Who specifically is accountable when it fails?"

### "That seems straightforward - what am I missing?"
Use this when user glosses over complexity.

**Examples:**
- User: "Then we just deliver it"
- You: "That seems straightforward - what am I missing?"

### "Have you actually done this?"
Use this to distinguish between theoretical and proven.

**Examples:**
- "Have you actually run this process?"
- "How many times have you done this?"
- "What went wrong the last time?"

---

## Conversation Patterns

### Pattern 1: The Dig
When user gives surface answer, dig deeper.

**Example:**
- User: "We handle customer support"
- You: "What does 'handle' mean specifically?"
- User: "We answer questions"
- You: "How? Email? Phone? Chat?"
- User: "Email"
- You: "How fast? Who answers? What if volume is high?"

### Pattern 2: The Specific Scenario
Force user to think through concrete example.

**Example:**
- You: "Let's say I'm a customer who just signed up. Walk me through exactly what happens next."
- [User describes]
- You: "You said 'we set up your account' - what are the actual steps in setting up?"

### Pattern 3: The Edge Case
Once you understand happy path, probe exceptions.

**Example:**
- You: "OK, that's the normal flow. What if [system is down / data is wrong / person is unavailable]?"

### Pattern 4: The Math
Use numbers to expose problems.

**Example:**
- User: "We manually review each order"
- You: "How long does one review take?"
- User: "About 10 minutes"
- You: "So at 100 orders per day, that's 1000 minutes = 16 hours. Who does that?"

### Pattern 5: The Contradiction
Point out when things don't add up.

**Example:**
- User: "We need to be very fast" ... "and each order is manually reviewed by 3 people"
- You: "Those seem contradictory. How do you maintain speed with 3 manual reviews?"

---

## Summary: Most Powerful Questions

1. **"Walk me through exactly what happens when [specific scenario]"** - Forces detail
2. **"What am I missing?"** - Finds gaps in your understanding and their thinking
3. **"What if [specific failure]?"** - Tests resilience
4. **"Who specifically?"** - Avoids vague answers
5. **"How do you know?"** - Demands evidence
6. **"What happens at 10x volume?"** - Tests scalability
7. **"Where does this break?"** - Finds weaknesses
8. **"How long does this take?"** - Gets concrete numbers
9. **"What's the worst case?"** - Explores risks
10. **"Have you actually done this?"** - Distinguishes theory from practice

Use these relentlessly to find blind spots and expose weak thinking.
