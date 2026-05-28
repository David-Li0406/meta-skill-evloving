# Customer Support - Sharp Edges

## Ai Without Content

### **Id**
ai-without-content
### **Summary**
AI chatbots are useless without quality content
### **Severity**
critical
### **Tools Affected**
  - intercom-fin
  - ada
  - chatbase
  - tidio
### **Situation**
Deploying AI agent before building knowledge base
### **Why**
  AI chatbots work by finding relevant content and generating responses.
  No content = no good answers = frustrated customers.
  
  The AI is only as good as what you feed it.
  
### **Solution**
  1. Build comprehensive KB BEFORE enabling AI
  2. Cover top 50 questions thoroughly
  3. Include edge cases and exceptions
  4. Update content based on AI failures
  5. Monitor "I don't know" responses
  
### **Symptoms**
  - AI says 'I don't know' constantly
  - Wrong or generic answers
  - High escalation rate

## Per Resolution Cost Explosion

### **Id**
per-resolution-cost-explosion
### **Summary**
Per-resolution AI pricing can explode unexpectedly
### **Severity**
high
### **Tools Affected**
  - intercom-fin
### **Situation**
Enabling AI without understanding pricing model
### **Why**
  $0.99/resolution sounds cheap until:
  - Volume is higher than expected
  - Definition of "resolution" is broad
  - Simple queries still count
  - No volume discount
  
  Easy to 10x expected AI costs.
  
### **Solution**
  1. Understand exactly what counts as "resolution"
  2. Set spending limits/alerts
  3. Calculate expected volume realistically
  4. Compare to human agent cost
  5. Negotiate caps for high volume
  
### **Symptoms**
  - Unexpected AI charges
  - Cost per ticket higher than expected
  - Bill shock

## Ai Hallucination

### **Id**
ai-hallucination
### **Summary**
AI can confidently give wrong information
### **Severity**
high
### **Tools Affected**
  - intercom-fin
  - chatbase
  - tidio
### **Situation**
AI provides incorrect product/policy information
### **Why**
  Even the best AI can:
  - Mix up similar topics
  - Invent policies that don't exist
  - Give outdated information
  - Miss important exceptions
  
  Customers take AI answers as official.
  
### **Solution**
  1. Monitor AI conversations regularly
  2. Flag high-stakes topics for human review
  3. Keep content current and specific
  4. Avoid vague or conflicting content
  5. Have clear correction process
  
### **Symptoms**
  - Customer complaints about wrong info
  - Support for things you don't offer
  - Policy confusion

## Poor Handoff

### **Id**
poor-handoff
### **Summary**
Bad AI-to-human handoff destroys customer experience
### **Severity**
high
### **Tools Affected**
  - intercom-fin
  - ada
  - tidio
### **Situation**
Customer repeats entire issue to human after AI fails
### **Why**
  Nothing frustrates customers more than:
  - Repeating their problem
  - Agent not seeing AI conversation
  - Starting over from scratch
  - Long wait after AI failure
  
  Worse than no AI at all.
  
### **Solution**
  1. Full conversation context passes to agent
  2. Agent can see what AI tried
  3. Seamless handoff (no new ticket)
  4. Priority routing after AI failure
  5. Warm handoff with summary
  
### **Symptoms**
  - Customer complaints about repetition
  - Lower CSAT after AI handoff
  - Longer handle times

## Inbox Zero Obsession

### **Id**
inbox-zero-obsession
### **Summary**
Chasing inbox zero leads to rushed, poor responses
### **Severity**
medium
### **Tools Affected**
  - zendesk
  - freshdesk
  - helpscout
  - front
### **Situation**
Agents racing to close tickets, not solve problems
### **Why**
  When you incentivize speed:
  - Quality suffers
  - First response != first resolution
  - Tickets reopen
  - Customers unsatisfied
  
  Fast bad support is still bad support.
  
### **Solution**
  1. Measure resolution, not just response
  2. Track reopen rate
  3. Balance speed and quality metrics
  4. CSAT as primary metric
  5. Allow proper resolution time
  
### **Symptoms**
  - High reopen rate
  - Fast response, low CSAT
  - Same issue comes back

## Zombie Tickets

### **Id**
zombie-tickets
### **Summary**
Old tickets haunt your queue forever
### **Severity**
medium
### **Tools Affected**
  - zendesk
  - freshdesk
  - intercom
### **Situation**
Tickets sitting for weeks awaiting customer response
### **Why**
  Some tickets never close:
  - Customer stops responding
  - Agent forgets to follow up
  - No auto-close policy
  - Metrics look terrible
  
  Skews all your reporting.
  
### **Solution**
  1. Auto-close after X days of no response
  2. Clear follow-up reminders
  3. Final "closing this unless you respond"
  4. Separate "awaiting customer" status
  5. Regular queue cleanup
  
### **Symptoms**
  - Average resolution time is weeks
  - Thousands of open tickets
  - Metrics don't reflect reality

## Routing Chaos

### **Id**
routing-chaos
### **Summary**
Tickets go to wrong team/agent constantly
### **Severity**
medium
### **Tools Affected**
  - zendesk
  - freshdesk
  - intercom
### **Situation**
Manual routing or poor automation leads to chaos
### **Why**
  Bad routing means:
  - Delays while ticket finds right person
  - Agents working outside expertise
  - Finger-pointing between teams
  - Customer frustration
  
  Support org runs inefficiently.
  
### **Solution**
  1. Clear routing rules based on keywords, customer
  2. Skills-based routing
  3. Auto-tagging with AI
  4. Default to triage queue if unsure
  5. Audit routing accuracy regularly
  
### **Symptoms**
  - Tickets bounced between teams
  - Long time in queue
  - Agents complaining about wrong tickets

## Agent Burnout

### **Id**
agent-burnout
### **Summary**
Support work leads to high turnover
### **Severity**
high
### **Tools Affected**
  - all
### **Situation**
High-volume, repetitive support work burns out agents
### **Why**
  Support is emotionally demanding:
  - Angry customers all day
  - Repetitive questions
  - Unrealistic metrics
  - Little autonomy
  
  Burned out agents = bad support = churn.
  
### **Solution**
  1. Use AI to handle repetitive queries
  2. Rotate difficult queues
  3. Reasonable workload expectations
  4. Career growth paths
  5. Recognition and support
  6. Breaks and mental health support
  
### **Symptoms**
  - High turnover rate
  - Declining CSAT
  - Absenteeism
  - Negative Glassdoor reviews

## Stale Content

### **Id**
stale-content
### **Summary**
Knowledge base becomes outdated and wrong
### **Severity**
high
### **Tools Affected**
  - document360
  - notion
  - gitbook
  - guru
### **Situation**
Articles written once and never updated
### **Why**
  Your product changes but content doesn't:
  - Features added/removed
  - Policies change
  - Pricing changes
  - UI changes
  
  Outdated KB = wrong AI answers = bad support.
  
### **Solution**
  1. Regular content audits (quarterly minimum)
  2. Ownership for each article
  3. Product releases trigger content review
  4. Track "this didn't help" feedback
  5. Archive outdated content
  
### **Symptoms**
  - Articles reference old UI
  - Pricing/policy conflicts
  - AI gives wrong answers

## Knowledge Silos

### **Id**
knowledge-silos
### **Summary**
Knowledge stuck in people's heads, not systems
### **Severity**
medium
### **Tools Affected**
  - all
### **Situation**
Only certain agents can answer certain questions
### **Why**
  When knowledge isn't documented:
  - Certain agents become bottlenecks
  - Quality varies by who responds
  - Risk when people leave
  - Can't train AI on it
  
  Tribal knowledge hurts scale.
  
### **Solution**
  1. Knowledge-centered service (every resolution → article)
  2. Regular knowledge sharing sessions
  3. Documentation as part of resolution
  4. Cross-training requirements
  5. Exit interviews capture knowledge
  
### **Symptoms**
  - Only Maria knows billing
  - Inconsistent answers to same question
  - Knowledge leaves with people

## Customer Context Scattered

### **Id**
customer-context-scattered
### **Summary**
Customer info scattered across tools
### **Severity**
medium
### **Tools Affected**
  - all
### **Situation**
Agent tabs between 5 tools to understand customer
### **Why**
  Without integration:
  - CRM in one place
  - Product usage in another
  - Billing somewhere else
  - Previous tickets not visible
  
  Slow, frustrating, impersonal support.
  
### **Solution**
  1. Customer data in helpdesk sidebar
  2. API integrations to pull context
  3. Single customer view
  4. Auto-populate relevant info
  5. Deep links to other tools
  
### **Symptoms**
  - Long handle times
  - Agent asks for info you should know
  - Alt-tabbing constantly

## Survey Fatigue

### **Id**
survey-fatigue
### **Summary**
Too many CSAT surveys annoy customers
### **Severity**
low
### **Tools Affected**
  - all
### **Situation**
Surveying after every interaction
### **Why**
  When you survey too much:
  - Response rates drop
  - Only angry people respond
  - Becomes noise
  - Customers unsubscribe
  
  Less feedback, not more.
  
### **Solution**
  1. Sample-based surveys (not every ticket)
  2. Vary survey timing
  3. Make it very quick (1-click)
  4. Don't survey same person too often
  5. Consider relationship surveys (NPS) instead
  
### **Symptoms**
  - Low survey response rate
  - Complaints about survey spam
  - Biased responses