# Red Flags in Process Design

This guide catalogs common warning signs in operational processes that indicate problems, fragility, or inability to scale.

---

## Critical Red Flags (High Risk)

### "It's straightforward" / "It's simple"

**Why it's a red flag:** Nothing is straightforward. This usually means user hasn't thought through details or edge cases.

**What to probe:**
- "Walk me through every step"
- "What happens when [edge case]?"
- "What am I missing?"

**Example:**
- User: "We just fulfill the order, it's straightforward"
- Reality: Pick item, check inventory, pack, print label, schedule pickup, track, handle exceptions, process returns...

---

### Single point of failure - One person

**Symptoms:**
- "John handles all the orders"
- "Only Sarah knows how to do this"
- "The founder approves everything"

**Why it's critical:** Business stops when that person is unavailable. Creates bottleneck and key-person risk.

**What to probe:**
- "What happens if they're sick/on vacation/quit?"
- "How many decisions/actions does this person make per day?"
- "Can they keep up when volume increases?"

---

### Single point of failure - One system

**Symptoms:**
- "Everything goes through [one system]"
- "If [vendor] is down, we can't operate"
- "We built our own custom system"

**Why it's critical:** No redundancy = complete failure when system goes down.

**What to probe:**
- "What happens when this system is down?"
- "Do you have a backup or manual fallback?"
- "What's the longest outage you've had?"

---

### Single point of failure - One supplier/partner

**Symptoms:**
- "We only work with [one supplier]"
- "This only works if [big company] gives us access"
- "We're dependent on [partner] for all distribution"

**Why it's critical:** Partner has leverage. No alternative if relationship fails.

**What to probe:**
- "What if they change pricing? Terms? Stop working with you?"
- "Do you have alternative partners?"
- "How long to switch to backup supplier?"

---

### No idea of operational costs

**Symptoms:**
- "We haven't calculated it"
- "It won't cost much"
- "We'll figure that out later"

**Why it's critical:** Can't manage what you don't measure. Might lose money on every transaction.

**What to probe:**
- "What's your cost per [unit/order/customer]?"
- "Is that higher or lower than your revenue per unit?"
- "What's the biggest cost component?"

---

### Process only works at current tiny scale

**Symptoms:**
- "We do everything manually"
- "The founder is involved in every decision"
- "We handle each one custom"

**Why it's critical:** Won't scale. Need complete rebuild for growth.

**What to probe:**
- "What happens when volume doubles? 10x?"
- "Where does this break first?"
- "What needs to change to scale?"

---

### No error handling or edge case planning

**Symptoms:**
- "That won't happen"
- "We'll deal with exceptions manually"
- "We haven't thought about that"

**Why it's critical:** Edge cases WILL happen. Process breaks on exceptions.

**What to probe:**
- "What's the weirdest thing that's happened?"
- "What happens if [specific failure]?"
- "Do you have a fallback?"

---

### Long chains of dependencies

**Symptoms:**
- "A must complete before B before C before D..."
- Many sequential steps
- Everything tightly coupled

**Why it's critical:** Slow, fragile, any delay compounds through the chain.

**What to probe:**
- "What's the critical path?"
- "What if Step 3 takes 2x longer?"
- "Can any steps run in parallel?"

---

## Serious Red Flags (Difficult Problems)

### Too many manual handoffs

**Symptoms:**
- "Then Person A emails Person B who tells Person C..."
- Work passes through many people
- Coordination needed for each handoff

**Why it's risky:** Each handoff = delay, potential drop, communication error.

**What to probe:**
- "How many people touch this before it's complete?"
- "What happens if a handoff is missed?"
- "How long do handoffs take?"

---

### Critical process only exists in someone's head

**Symptoms:**
- "Only [person] knows how to do this"
- No documentation
- Tribal knowledge

**Why it's risky:** Can't train others, can't automate, at risk if person leaves.

**What to probe:**
- "Is this documented anywhere?"
- "Could someone else do this if needed?"
- "What happens if this person quits?"

---

### Many tools that don't integrate

**Symptoms:**
- Using 5+ separate tools
- Manual data entry between tools
- Copy-pasting between systems

**Why it's risky:** Slow, error-prone, doesn't scale, data inconsistencies.

**What to probe:**
- "Do these tools talk to each other?"
- "How much time copying data between tools?"
- "Where do errors happen?"

---

### Unclear responsibilities / Overlapping ownership

**Symptoms:**
- "The team handles it"
- "Someone will take care of it"
- "We all chip in"

**Why it's risky:** Things fall through cracks. No accountability.

**What to probe:**
- "Who specifically is responsible?"
- "Who's accountable if it fails?"
- "What if two people think it's the other's job?"

---

### No quality checks until customer complains

**Symptoms:**
- "Customers will let us know if there's a problem"
- No quality checkpoints in process
- Quality measured by complaints

**Why it's risky:** Bad quality reaches customers. Expensive to fix after delivery.

**What to probe:**
- "When do you check quality?"
- "Who checks it?"
- "What's your error rate?"

---

### Promising SLAs you can't consistently meet

**Symptoms:**
- "We promise 24-hour turnaround"
- "But sometimes it takes 3 days"
- Often missing commitments

**Why it's risky:** Erodes trust, customer churn, potential legal issues.

**What to probe:**
- "What percentage of time do you meet SLA?"
- "What causes you to miss it?"
- "What happens when you miss?"

---

### High error rates considered normal

**Symptoms:**
- "We usually need to redo about 20%"
- "Errors happen, no big deal"
- "We have a lot of rework"

**Why it's risky:** Waste, cost, slow, frustrating for customers and team.

**What to probe:**
- "What's your error rate?"
- "How much time spent fixing errors?"
- "Why are errors happening?"

---

### Process heavily dependent on email for coordination

**Symptoms:**
- "We email to coordinate"
- "We forward emails around"
- Critical information in email threads

**Why it's risky:** Things get missed, no visibility, hard to track, doesn't scale.

**What to probe:**
- "What happens if email gets missed?"
- "How do you track status?"
- "Can you see what's pending?"

---

### "We'll just hire more people" as only scale strategy

**Symptoms:**
- Linear relationship between volume and headcount
- No plan to automate
- Assuming people solve all problems

**Why it's risky:** Expensive, slow to hire/train, quality inconsistent, management overhead.

**What to probe:**
- "How many people needed at 10x volume?"
- "Can you hire and train that many?"
- "What's the cost of all those people?"

---

## Data & Information Red Flags

### Critical data only in spreadsheets

**Symptoms:**
- "We track everything in Excel/Sheets"
- Shared spreadsheets as database
- Manual updates to spreadsheet

**Why it's risky:** No data integrity, version conflicts, doesn't scale, no audit trail.

**What to probe:**
- "What happens when two people edit at once?"
- "How do you prevent errors?"
- "Can this handle 100x more rows?"

---

### Data in multiple places that can get out of sync

**Symptoms:**
- "We update it in System A and System B"
- No single source of truth
- Frequent sync issues

**Why it's risky:** Inconsistent data, errors, confusion about which is correct.

**What to probe:**
- "How do you keep them in sync?"
- "What happens when they differ?"
- "Which system is the source of truth?"

---

### No audit trail / No way to see what happened

**Symptoms:**
- "We just overwrite the data"
- Can't see history
- No record of changes

**Why it's risky:** Can't debug, can't meet compliance, can't understand problems.

**What to probe:**
- "Can you see what changed and when?"
- "Who made this change?"
- "Do you need audit trail for compliance?"

---

### Manual data entry in multiple systems

**Symptoms:**
- "We enter it in System A, then re-enter in System B"
- Typing the same data multiple times
- High error rate from typos

**Why it's risky:** Slow, error-prone, frustrating, doesn't scale.

**What to probe:**
- "How much time spent on data entry?"
- "What's the error rate?"
- "Why can't systems integrate?"

---

## Decision & Approval Red Flags

### Too many approval steps

**Symptoms:**
- "Needs approval from A, B, C, and D"
- Four+ approval layers
- Everything needs executive approval

**Why it's risky:** Extremely slow, bottlenecks, delays compound.

**What to probe:**
- "How long for all approvals?"
- "What if one approver is unavailable?"
- "Why so many approvals?"

---

### Subjective decision criteria

**Symptoms:**
- "We'll know it when we see it"
- "Depends on the situation"
- No clear rules

**Why it's risky:** Inconsistent decisions, can't automate, quality varies by who decides.

**What to probe:**
- "What exactly are you deciding based on?"
- "Would two people make the same decision?"
- "Can you write down the criteria?"

---

### No escalation path for exceptions

**Symptoms:**
- "We don't know what to do in that case"
- Process stops when exception occurs
- No way to handle edge cases

**Why it's risky:** Process breaks on exceptions, requires manual intervention each time.

**What to probe:**
- "What do you do when [edge case]?"
- "Who handles exceptions?"
- "How often do exceptions happen?"

---

## Technical & Integration Red Flags

### Building all integrations yourself

**Symptoms:**
- "We're building custom connectors for everything"
- Reinventing integration infrastructure
- Each integration is a project

**Why it's risky:** Time-consuming, maintenance burden, fragile, diverts from core product.

**What to probe:**
- "Can you use existing integration platforms?"
- "Who maintains these integrations?"
- "How long to add a new integration?"

---

### Fragile integrations that break often

**Symptoms:**
- "The integration goes down a lot"
- "We have to restart it manually"
- "Sometimes data doesn't sync"

**Why it's risky:** Unreliable, requires constant attention, data loss risk.

**What to probe:**
- "How often does it break?"
- "What breaks it?"
- "Do you have error handling and retries?"

---

### No automated testing of process

**Symptoms:**
- "We manually test everything"
- "We test in production"
- "We find bugs when customers report them"

**Why it's risky:** Changes break things, slow to release, quality issues reach customers.

**What to probe:**
- "How do you test changes?"
- "How do you know you didn't break something?"
- "Can you test automatically?"

---

### Custom-built system that only one person understands

**Symptoms:**
- "John built our custom system"
- No documentation
- Hard to modify

**Why it's risky:** Key-person dependency, hard to maintain, technical debt.

**What to probe:**
- "Is it documented?"
- "Can others modify it?"
- "What happens if John leaves?"

---

## Compliance & Risk Red Flags

### "We'll worry about compliance later"

**Symptoms:**
- Not thinking about regulations
- Assuming too small to matter
- No legal review

**Why it's critical:** Can get shut down, fined, sued. Expensive to retrofit compliance.

**What to probe:**
- "What regulations apply?"
- "Have you talked to a lawyer?"
- "What happens if you're audited?"

---

### Handling sensitive data without proper controls

**Symptoms:**
- "We store credit cards in our database"
- "Everyone has access to customer data"
- "We haven't thought about security"

**Why it's critical:** Data breach = lawsuit, fines, reputation damage, potential shutdown.

**What to probe:**
- "How do you protect sensitive data?"
- "Who has access?"
- "Are you PCI/GDPR/HIPAA compliant?"

---

### No disaster recovery plan

**Symptoms:**
- "We haven't thought about that"
- No backups or untested backups
- "That won't happen"

**Why it's risky:** When (not if) disaster strikes, business stops.

**What to probe:**
- "What if your database corrupts?"
- "What if your office burns down?"
- "When did you last test backup recovery?"

---

## Scaling Red Flags

### Everything breaks at 2x current volume

**Symptoms:**
- "We're at capacity now"
- "Can't handle much more"
- Current process already stressed

**Why it's critical:** Can't grow. Need to rebuild process before scaling.

**What to probe:**
- "What's your current capacity?"
- "What breaks first when volume increases?"
- "What needs to change to handle 2x?"

---

### Costs scale faster than revenue

**Symptoms:**
- "We need to double headcount to double revenue"
- "Each customer costs more as we grow"
- Negative economies of scale

**Why it's critical:** Unit economics get worse with growth. Can't be profitable at scale.

**What to probe:**
- "What's cost per unit at current scale vs. 10x scale?"
- "Why do costs scale faster?"
- "Can you get economies of scale?"

---

### Process requires geographic proximity

**Symptoms:**
- "Everyone needs to be in the office"
- "We need face-to-face coordination"
- Can't work remotely or in multiple locations

**Why it's risky:** Limits hiring, limits scale, limits geographic expansion.

**What to probe:**
- "Why does it need to be in-person?"
- "Can you redesign for remote work?"
- "What if you want to expand to other cities?"

---

## Measurement & Visibility Red Flags

### No metrics / No visibility

**Symptoms:**
- "We don't track that"
- "Not sure, let me check"
- Flying blind

**Why it's risky:** Can't identify problems, can't improve, don't know when things break.

**What to probe:**
- "How do you know if the process is working well?"
- "What metrics do you track?"
- "How do you know when something's wrong?"

---

### Metrics exist but no one acts on them

**Symptoms:**
- "We have dashboards but rarely look"
- "Metrics show problems but we haven't fixed them"
- Measurement theater

**Why it's risky:** Waste of effort measuring. Problems persist.

**What to probe:**
- "When's the last time you reviewed metrics?"
- "What did you change based on metrics?"
- "Why measure if you don't act?"

---

### Only measuring outputs, not outcomes

**Symptoms:**
- "We processed 100 orders" (but how many had errors?)
- "We sent 1000 emails" (but how many responded?)
- Activity metrics, not result metrics

**Why it's risky:** Can look busy while failing. Don't measure what matters.

**What to probe:**
- "What's the outcome you're trying to achieve?"
- "How do you measure success, not just activity?"

---

## How to Use These Red Flags

### Pattern recognition
Listen for symptoms that indicate red flags. User might not explicitly say "single point of failure" but will describe it.

### Severity assessment
- **🔴 Critical:** Business likely fails or can't scale (single points of failure, broken unit economics)
- **🟡 Serious:** Major problems that need addressing (many handoffs, no error handling)
- **🟢 Caution:** Worth discussing but may be acceptable early on (manual processes, minimal documentation)

### Combinations amplify risk
Multiple red flags together = very high risk.

**Example:** "Only John knows how to do it" + "No documentation" + "If system is down, process stops" = disaster waiting to happen

### Context matters
Some red flags acceptable in early stages but must be addressed for scale.

**Early stage OK:**
- Manual processes (when volume is low)
- Founder does everything (when there's no team)
- Minimal documentation (when testing product-market fit)

**Not OK at any stage:**
- Broken unit economics
- Non-compliance with regulations
- No single point of failure plan

### Use red flags to prioritize
When multiple red flags exist, help user prioritize which to address first:
1. Critical risks (compliance, single points of failure)
2. Scale blockers (what prevents growth)
3. Operational pain (what's most frustrating)
4. Future optimization (nice-to-have improvements)

---

## Example Red Flag Conversations

### Example 1: Single Point of Failure

**User:** "John handles all our order fulfillment."

**You:** "What happens when John is sick or on vacation?"

**User:** "Um, orders pile up until he gets back."

**You:** "That's a single point of failure. How many orders per day?"

**User:** "About 50."

**You:** "So if John is out for a week, 350 orders pile up? What's the customer experience?"

**User:** "Not great..."

**You:** "This will get worse as you grow. What's your plan to eliminate this dependency?"

---

### Example 2: Process Only Works at Tiny Scale

**User:** "We manually review each order."

**You:** "How long does that take?"

**User:** "About 15 minutes per order."

**You:** "And how many orders per day?"

**User:** "Right now, 20."

**You:** "So that's 5 hours per day. What happens when you have 100 orders per day?"

**User:** "Um... that would be 25 hours..."

**You:** "Right. So this process breaks at 5x growth. You're hiring 3 more reviewers? Or automating? What's the plan?"

---

### Example 3: No Error Handling

**User:** "The process is pretty straightforward - we import the data, process it, and export."

**You:** "What happens if the import file is malformed?"

**User:** "Uh... I guess it would fail?"

**You:** "Then what? Does someone get notified? Can you retry? Does it leave partial data?"

**User:** "We haven't really thought about that..."

**You:** "What about if the external API you export to is down?"

**User:** "I guess we'd need to try again manually..."

**You:** "So every exception requires manual intervention? That's going to be a lot of your time. What's your error rate?"

---

## Summary: Top 15 Process Red Flags

1. **"It's straightforward"** - Never is, probe deeper
2. **Single point of failure (person)** - Key-person risk
3. **Single point of failure (system)** - No redundancy
4. **Single point of failure (partner)** - No control
5. **No idea of costs** - Can't manage finances
6. **Only works at tiny scale** - Can't grow
7. **No error handling** - Breaks on exceptions
8. **Long dependency chains** - Slow and fragile
9. **Many manual handoffs** - Delays and drops
10. **Knowledge only in someone's head** - Can't scale or train
11. **Too many approvals** - Bottleneck
12. **No compliance thinking** - Legal risk
13. **Everything breaks at 2x volume** - Can't grow
14. **No metrics** - Flying blind
15. **Data in multiple places** - Inconsistency and errors

When you see these, probe deeply and help user understand the risk and cost of not addressing them.
