# Process Brief Categories Guide

This guide explains each category in the process brief with practical context for stress-testing operational thinking.

---

## CORE - Podstawy procesu

### 1. Kluczowe procesy biznesowe

**What it is:** The major operational processes that must function for the business to work.

**Why it matters:** Missing a critical process = business doesn't work. Understanding all processes helps identify dependencies and complexity.

**Common processes by business type:**
- **SaaS:** Lead generation → Sales → Onboarding → Usage → Support → Renewal
- **E-commerce:** Marketing → Purchase → Fulfillment → Delivery → Returns → Support
- **Marketplace:** Supplier onboarding → Buyer acquisition → Matching → Transaction → Fulfillment
- **Service business:** Lead gen → Sales → Delivery → Invoicing → Support

**Key questions:**
- What are ALL the processes needed from customer awareness to value delivery?
- Which processes are customer-facing vs. internal?
- Which processes are revenue-generating vs. support?
- Are there processes you haven't thought about? (billing, compliance, hiring, etc.)

**Red flags:**
- Only thinking about the "happy path" main process
- Missing support/exception processes
- Forgetting back-office processes (finance, legal, HR)
- Underestimating complexity of "simple" processes

---

### 2. Aktorzy / Role

**What it is:** Every person or entity that participates in processes, and what they're responsible for.

**Why it matters:** Unclear roles = confusion, delays, things falling through cracks. Each actor needs clear ownership.

**Types of actors:**
- **External:** Customer, supplier, partner, regulator, auditor
- **Internal:** Sales, operations, support, engineering, finance, legal
- **System/Automated:** Bots, APIs, automated workflows

**Key questions:**
- Who does what in each process?
- Who makes decisions at each decision point?
- Who is accountable if something goes wrong?
- Are roles clearly defined or will people step on each other's toes?
- Do you have people to fill these roles?

**Red flags:**
- "We'll figure out who does what later"
- Assuming one person can do multiple complex roles
- No clear decision-maker for critical choices
- Relying on external actors you don't control

---

### 3. Flow procesów

**What it is:** Step-by-step sequence of what happens in each process.

**Why it matters:** Understanding detailed flow reveals hidden complexity, dependencies, and potential failure points.

**How to document:**
- Start → Step 1 → Decision point → Step 2 → ... → End
- Include all branches (success, failure, exceptions)
- Note where process hands off between actors

**Key questions:**
- What's the first step? What triggers it?
- What happens next? And then?
- Where are the decision points? What are the options at each?
- Where does the process hand off between people/systems?
- What's the end state? How do you know it's complete?
- What happens if a step fails?

**Red flags:**
- "It's straightforward" (nothing is straightforward)
- Missing exception paths
- Vague steps like "handle the order" (what specifically?)
- No clear end state

---

### 4. Zależności między procesami

**What it is:** How processes depend on each other - what must happen before what.

**Why it matters:** Dependencies create bottlenecks, delays, and complexity. Understanding them helps optimize and identify risks.

**Types of dependencies:**
- **Sequential:** Process B can't start until Process A completes
- **Parallel:** Processes run simultaneously
- **Conditional:** Process C only runs if Process A had outcome X
- **Circular:** Process A feeds Process B which feeds back to Process A

**Key questions:**
- Which processes must happen in sequence?
- Which can happen in parallel?
- What happens if a dependency fails or delays?
- Are there circular dependencies? (usually bad)
- Which dependencies are hard constraints vs. preferences?

**Red flags:**
- Long chains of dependencies (slow, fragile)
- Circular dependencies (complexity, potential deadlock)
- Dependencies on external actors you don't control
- Not understanding critical path

---

## DATA & DECISIONS - Informacje i decyzje

### 5. Inputs / Outputs

**What it is:** What goes into each process step and what comes out.

**Why it matters:** Mismatched inputs/outputs = process breaks. Understanding data flow reveals integration needs and potential errors.

**For each process step, identify:**
- **Inputs:** What information, materials, approvals, or resources are needed?
- **Outputs:** What is produced? (data, product, decision, notification)
- **Format:** What form? (structured data, document, physical item)

**Key questions:**
- What inputs are required for each step to start?
- Where do those inputs come from?
- What if an input is missing or wrong?
- What outputs are produced at each step?
- Who consumes those outputs?
- Are outputs in the format consumers need?

**Red flags:**
- Outputs from one step don't match inputs needed by next step
- Missing data that's needed downstream
- Manual data entry/transformation between steps (error-prone)
- No validation of input quality

---

### 6. Decision points

**What it is:** Where choices must be made in the process, who makes them, and based on what criteria.

**Why it matters:** Decisions slow things down and introduce variability. Unclear decision criteria = inconsistency and delays.

**For each decision point:**
- **What's being decided?** (approve/reject, which path, how much, etc.)
- **Who decides?** (person, role, automated rule)
- **Based on what?** (criteria, data, judgment)
- **How long does it take?**
- **What happens for each outcome?**

**Key questions:**
- What decisions must be made in this process?
- Are decision criteria clear and objective, or subjective?
- Can decisions be automated?
- What happens if decision-maker is unavailable?
- What if decision is wrong? Can it be reversed?

**Red flags:**
- Too many decision points (slow process)
- Subjective/unclear decision criteria
- Single person as bottleneck for all decisions
- No escalation path when decision is unclear

---

### 7. Dane / Informacje

**What it is:** What data is needed, where it's stored, how it flows, and who has access.

**Why it matters:** Data is the lifeblood of processes. Missing, wrong, or inaccessible data breaks everything.

**Key aspects:**
- **What data:** Customer info, product data, transaction records, etc.
- **Where stored:** Database, CRM, spreadsheet, paper, someone's head
- **How accessed:** API, manual lookup, automated sync
- **Data quality:** How accurate? How current?
- **Data ownership:** Who maintains it?

**Key questions:**
- What data is needed for each process?
- Where does that data live today?
- How do you get access to it?
- How do you know it's accurate and current?
- What happens if data is wrong?
- Who updates the data?

**Red flags:**
- Data in multiple places that can get out of sync
- Critical data only in someone's head
- No single source of truth
- Manual data entry in multiple systems
- No data validation

---

### 8. Handoffy

**What it is:** Points where work passes from one person/team/system to another.

**Why it matters:** Handoffs are where things get dropped, delayed, or miscommunicated. Each handoff is a risk point.

**For each handoff:**
- **From who/what → To who/what**
- **What's being handed off?** (work, data, decision, responsibility)
- **How?** (email, ticket, verbal, automated)
- **When?** (immediately, batched, scheduled)
- **What can go wrong?**

**Key questions:**
- Where do handoffs happen in the process?
- How is the receiving party notified?
- How do they know what to do?
- What if handoff fails? (person on vacation, system down)
- Is there a record of the handoff?
- How long does handoff take?

**Red flags:**
- Many handoffs (each is a delay and risk)
- Informal handoffs (verbal, email) for critical work
- No notification mechanism
- No tracking of handoff status
- Handoff requires manual coordination

---

## PROBLEMS & EDGE CASES - Problemy

### 9. Pain points / Bottlenecki

**What it is:** Where the process is slow, frustrating, error-prone, or breaks down.

**Why it matters:** Pain points cost time and money. Bottlenecks limit capacity and growth.

**Types of problems:**
- **Speed:** Takes too long
- **Quality:** High error rate
- **Capacity:** Can't handle volume
- **Cost:** Too expensive to run
- **Experience:** Frustrating for users
- **Reliability:** Breaks frequently

**Key questions:**
- What's the slowest part of the process?
- Where do errors happen most?
- What do people complain about?
- What breaks when volume increases?
- Where do you need manual intervention most?
- What would you fix first if you could?

**Red flags:**
- "It works fine" (nothing works fine, push harder)
- Not knowing where bottlenecks are
- Accepting pain points as inevitable
- No metrics to identify problems

---

### 10. Edge cases / Wyjątki

**What it is:** Unusual situations, exceptions, and what-if scenarios that don't follow the happy path.

**Why it matters:** Edge cases reveal process fragility. "It usually works" isn't good enough - what happens when it doesn't?

**Common edge cases:**
- **Input errors:** Wrong data, missing fields, invalid format
- **System failures:** API down, database offline, network issue
- **Human errors:** Wrong button clicked, forgot a step
- **Timing issues:** Late delivery, expired token, timeout
- **Volume spikes:** 10x normal traffic
- **External issues:** Payment fails, partner unavailable

**Key questions:**
- What unusual situations could occur?
- What happens when systems fail?
- What if someone makes a mistake?
- What if data is invalid?
- What if external dependency is down?
- Is there a manual fallback?

**Red flags:**
- "That will never happen" (it will)
- No error handling
- Process completely breaks on edge case
- No way to recover from failures
- Manual intervention required for every exception

---

### 11. Ryzyka operacyjne

**What it is:** Things that could go wrong that would significantly impact operations.

**Why it matters:** Understanding risks helps prioritize what to build robustly vs. what can be fragile early on.

**Types of risks:**
- **Single point of failure:** One person, one system, one supplier
- **Dependency risk:** Reliance on external party
- **Capacity risk:** Can't handle growth
- **Quality risk:** High error rate leads to customer churn
- **Compliance risk:** Violate regulation, get shut down
- **Security risk:** Data breach, fraud

**Key questions:**
- What's your single point of failure?
- What happens if key person leaves?
- What if a critical system goes down?
- What if a partner stops working with you?
- What could get you sued or shut down?
- What would happen in a worst-case scenario?

**Red flags:**
- No redundancy for critical components
- One person knows how everything works
- Complete dependency on one vendor/partner
- No disaster recovery plan
- Not thinking about risks until they happen

---

## REQUIREMENTS - Wymagania

### 12. Czas trwania / SLA

**What it is:** How long each process step takes and what time commitments you've made to customers.

**Why it matters:** Time is money and customer expectation. Slow processes cost more and create bad experience.

**For each process:**
- **Average duration:** How long does it typically take?
- **Best case:** Fastest possible
- **Worst case:** Longest observed
- **SLA:** What have you promised customers?
- **Dependencies:** What affects duration?

**Key questions:**
- How long does the full process take end-to-end?
- What's the longest step?
- What slows things down?
- Have you promised customers specific timeframes?
- Can you consistently meet those commitments?
- What happens if you miss SLA?

**Red flags:**
- Don't know how long processes take
- Promising SLAs you can't meet consistently
- Long delays with no visibility to customer
- No way to track if you're meeting commitments

---

### 13. Compliance / Regulacje

**What it is:** Legal, regulatory, and contractual requirements the process must satisfy.

**Why it matters:** Non-compliance = fines, lawsuits, shutdown. Can't ignore regulations.

**Common requirements:**
- **Data protection:** GDPR, CCPA, HIPAA
- **Financial:** PCI DSS, SOX, anti-money laundering
- **Industry-specific:** FDA, FCC, SEC, etc.
- **Contractual:** SLAs, terms of service, partner agreements
- **Internal:** Company policies, audit requirements

**Key questions:**
- What regulations apply to your business?
- What are the specific requirements?
- Which processes need to be compliant?
- How do you prove compliance? (audit trail, documentation)
- What happens if you're not compliant?
- Do you need certifications?

**Red flags:**
- "We'll worry about compliance later" (dangerous)
- Not understanding what regulations apply
- No documentation/audit trail
- Assuming you're too small to matter to regulators
- Storing sensitive data without proper controls

---

### 14. Wymagania jakościowe

**What it is:** Quality standards the process must meet - accuracy, consistency, reliability.

**Why it matters:** Poor quality = rework, refunds, churn. Quality problems compound over time.

**Quality dimensions:**
- **Accuracy:** Correctness of outputs
- **Consistency:** Same result every time
- **Completeness:** All required steps done
- **Timeliness:** Done on time
- **Reliability:** Works every time

**Key questions:**
- What quality standards apply?
- How do you measure quality?
- What's acceptable error rate?
- How do you ensure consistency?
- What happens when quality fails?
- Who checks quality?

**Red flags:**
- No quality standards defined
- Not measuring quality
- High error rates considered normal
- No quality checks until customer complains
- Manual quality control that doesn't scale

---

## TECH & TOOLS - Technologia

### 15. Narzędzia / Systemy

**What it is:** Software, hardware, and tools used in each process step.

**Why it matters:** Tools enable or constrain processes. Wrong tools slow you down or prevent scaling.

**For each tool:**
- **Purpose:** What's it used for?
- **Users:** Who uses it?
- **When:** At which process steps?
- **Cost:** How much does it cost?
- **Limitations:** What can't it do?

**Key questions:**
- What tools do you use in each step?
- Are they the right tools or just what you happen to use?
- Do tools integrate with each other?
- What manual work happens between tools?
- Can tools handle your growth?
- What happens if a tool goes down?

**Red flags:**
- Too many tools that don't integrate
- Manual work copying data between tools
- Tools that don't scale
- Expensive tools for simple needs
- Critical process depends on single tool with no backup

---

### 16. Integracje

**What it is:** How systems connect to each other - APIs, data sync, file transfers.

**Why it matters:** Bad integrations = manual work, errors, delays. Good integrations enable automation and scale.

**For each integration:**
- **What systems:** A → B
- **What data:** What's being shared?
- **How:** API, file transfer, manual, ETL
- **When:** Real-time, batch, on-demand
- **Error handling:** What if integration fails?

**Key questions:**
- What systems need to talk to each other?
- How do they integrate today?
- Is integration real-time or batch?
- What happens if integration breaks?
- Do you have to build custom integrations?
- What's the cost/complexity of integrations?

**Red flags:**
- No integrations (everything manual)
- Fragile integrations that break often
- Building all integrations yourself
- No error handling or retry logic
- Data sync issues between systems

---

### 17. Automatyzacja

**What it is:** What's automated, what's manual, and what could be automated.

**Why it matters:** Manual work doesn't scale and is error-prone. Automation enables growth and consistency.

**Categories:**
- **Fully automated:** No human involvement
- **Semi-automated:** Human triggers or approves
- **Manual with tools:** Human does it with software help
- **Fully manual:** Human does everything

**Key questions:**
- What's automated today?
- What's still manual?
- Why is it manual? (complexity, volume too low, technical limitation)
- What should be automated next?
- What should stay manual? (judgment, customer touch, exceptions)
- What's the ROI of automation?

**Red flags:**
- Everything is manual (won't scale)
- Automating before understanding process (premature optimization)
- No plan for what to automate as you grow
- Assuming you can automate everything

---

## ECONOMICS & SCALE - Ekonomia

### 18. Koszty operacyjne

**What it is:** How much it costs to run each process.

**Why it matters:** High operational costs eat into margins. Understanding costs helps prioritize optimization.

**Cost categories:**
- **Labor:** People time (salary × hours)
- **Tools:** Software subscriptions, licenses
- **Infrastructure:** Servers, hosting, services
- **Transaction costs:** Payment processing, per-unit fees
- **Overhead:** Support, management, facilities

**Key questions:**
- What does each process cost to run?
- What's the biggest cost component?
- What's the cost per unit? (per customer, per order, per transaction)
- How do costs change with volume?
- Where can you reduce costs?
- Are costs fixed or variable?

**Red flags:**
- Don't know what processes cost
- Cost per unit higher than revenue per unit
- Fixed costs that don't scale
- Expensive manual processes that could be automated
- Not tracking costs at all

---

### 19. Skalowanie

**What it is:** What happens when volume increases 2x, 10x, 100x.

**Why it matters:** Processes that work at 10 customers often break at 100 or 1000. Understanding scale limitations helps plan growth.

**Scale dimensions:**
- **Volume:** More transactions/customers/orders
- **Speed:** Faster processing required
- **Complexity:** More edge cases, more integration
- **Geography:** More locations, more languages
- **Team:** More people doing the work

**Key questions:**
- What happens when volume doubles?
- Where does the process break?
- What's the current capacity limit?
- What needs to change to handle 10x volume?
- Do costs scale linearly or better?
- What becomes a bottleneck first?

**Red flags:**
- Process works only at current tiny scale
- Costs scale faster than revenue
- Bottlenecks obvious at 2x volume
- Manual steps that can't scale
- "We'll hire more people" as only scale strategy

---

### 20. Metryki procesu

**What it is:** How you measure process performance and health.

**Why it matters:** Can't improve what you don't measure. Metrics show when process is degrading.

**Key metrics categories:**
- **Speed:** Cycle time, lead time, throughput
- **Quality:** Error rate, defect rate, customer satisfaction
- **Cost:** Cost per unit, cost per transaction
- **Capacity:** Utilization, queue length, backlog
- **Reliability:** Uptime, success rate, failure rate

**Key questions:**
- What metrics do you track for each process?
- How often do you review them?
- What are target values?
- What do you do when metrics degrade?
- Do you have real-time visibility or only periodic reports?

**Red flags:**
- Not measuring anything
- Measuring vanity metrics that don't matter
- No alerts when metrics degrade
- Metrics exist but no one looks at them
- No action taken when metrics show problems

---

## Using This Guide

**During dialogue:**
- Start with Core categories (1-4) to understand basic process
- Explore Data & Decisions (5-8) to understand information flow
- Probe Problems (9-11) to find weaknesses
- Cover Requirements (12-14) if relevant to business
- Discuss Tech (15-17) if technology is involved
- Analyze Economics (18-20) to understand viability

**Critical attitude:**
- Assume user hasn't thought through details
- Ask about specific scenarios
- Push for numbers (time, cost, volume)
- Identify what they don't know
- Point out where process will break

**Recording:**
- Capture what user knows
- Mark what's uncertain
- Note assumptions that need testing
- Identify biggest risks
