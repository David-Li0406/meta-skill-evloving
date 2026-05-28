# Search Examples

Real-world examples of effective Airweave search patterns.

## Example 1: Finding Recent Discussions

**User:** "What did the team say about the new pricing in Slack?"

**Approach:**
- Topic: pricing discussions
- Source hint: Slack
- Recency: implied recent (team discussions)

**Search:**
```
query: "new pricing discussion feedback"
recency_bias: 0.7
limit: 15
```

**Response pattern:**
> Based on recent Slack conversations, the team discussed the new pricing last week. Key points:
> 
> 1. **Sarah (Sales)**: Concerned about enterprise tier pricing being too high compared to competitors
> 2. **Mike (Product)**: Suggested adding a mid-tier option
> 3. **Lisa (Customer Success)**: Shared that 3 customers asked about volume discounts
> 
> The main consensus was to revisit the enterprise pricing before the Q2 launch.

---

## Example 2: Finding Documentation

**User:** "Where's the API authentication documentation?"

**Approach:**
- Looking for specific document
- Likely in docs/wiki source
- Exact term matching helpful

**Search:**
```
query: "API authentication documentation guide"
search_method: "hybrid"
enable_reranking: true
limit: 10
```

**Response pattern:**
> I found the API authentication documentation in your Confluence:
> 
> **[API Authentication Guide](link)** - Last updated 2 weeks ago
> 
> It covers:
> - OAuth 2.0 flow
> - API key generation
> - Token refresh handling
> 
> Would you like me to summarize any specific section?

---

## Example 3: Direct Question (Using Completion)

**User:** "What's our refund policy?"

**Approach:**
- Direct question wanting an answer
- Use completion for synthesized response
- Policy docs tend to be stable (low recency)

**Search:**
```
query: "refund policy customer returns"
response_type: "completion"
enable_reranking: true
```

**Response pattern:**
> According to your company documentation, your refund policy is:
> 
> - **Within 30 days**: Full refund, no questions asked
> - **30-60 days**: Store credit or exchange
> - **After 60 days**: Case-by-case basis, manager approval required
> 
> Exceptions: Software licenses and custom orders are non-refundable.

---

## Example 4: Exploring a Topic

**User:** "Show me what customers have been saying about shipping"

**Approach:**
- Exploration, not specific answer
- Want to see multiple perspectives
- Raw results to browse

**Search:**
```
query: "customer feedback shipping delivery"
response_type: "raw"
limit: 20
recency_bias: 0.5
```

**Response pattern:**
> Here's what I found about customer shipping feedback:
> 
> **From Zendesk (last week):**
> - 5 tickets about delayed international shipping
> - 2 complaints about packaging damage
> 
> **From Slack #customer-feedback:**
> - Discussion about carrier switch improving delivery times
> - Note from CS team about tracking notification issues
> 
> **From Salesforce notes:**
> - Enterprise client requested expedited shipping options
> 
> Want me to dig deeper into any of these areas?

---

## Example 5: No Results - Refining

**User:** "Find the Jenkins deployment pipeline config"

**First search:**
```
query: "Jenkins deployment pipeline configuration"
```

**Result:** No matches or low scores

**Refinement approach:**
1. Broaden: "deployment pipeline CI/CD"
2. Try synonyms: "build pipeline automation"
3. Check source: "Is GitHub/GitLab connected?"

**Follow-up:**
> I didn't find specific Jenkins configuration. Let me try a broader search...
> 
> I found deployment-related docs in your GitHub:
> - `.github/workflows/deploy.yml` - GitHub Actions deployment
> - `docs/deployment-guide.md` - General deployment steps
> 
> It looks like you might be using GitHub Actions rather than Jenkins. Would you like me to show the GitHub Actions configuration?

---

## Example 6: Time-Sensitive Search

**User:** "What bugs were reported today?"

**Approach:**
- Very time-sensitive
- High recency bias
- Likely in issue tracker (Jira/Linear/GitHub)

**Search:**
```
query: "bug report issue"
recency_bias: 0.95
limit: 20
```

**Response pattern:**
> Here are the bugs reported today:
> 
> 1. **[JIRA-1234]** Login timeout on mobile - P1, assigned to Alex
> 2. **[JIRA-1235]** Dashboard charts not loading - P2, unassigned
> 3. **[JIRA-1236]** Typo in email template - P3, assigned to Sarah
> 
> The P1 login issue seems most urgent. Want details on that one?

---

## Example 7: Cross-Source Research

**User:** "What do we know about Acme Corp?"

**Approach:**
- Entity search (company name)
- Likely in CRM + communications
- Keyword helpful for exact name

**Search:**
```
query: "Acme Corp customer account"
search_method: "hybrid"
limit: 25
enable_reranking: true
```

**Response pattern:**
> Here's what I found about Acme Corp across your systems:
> 
> **Salesforce:**
> - Enterprise customer since 2023
> - $50k ARR, renews in March
> - Main contact: John Smith (CTO)
> 
> **Slack:**
> - Recent discussion about their API integration needs
> - They requested a custom feature last month
> 
> **Zendesk:**
> - 2 open support tickets
> - Generally positive sentiment in past interactions
> 
> Would you like more detail on any of these?

---

## Anti-Patterns (What Not to Do)

### ❌ Searching for everything
```
query: "all documents"  // Too broad, won't return useful results
```

### ❌ Using completion when sources matter
```
// User: "What messages mentioned the outage?"
response_type: "completion"  // Wrong - user wants to see the messages
response_type: "raw"  // Correct - show the actual messages
```

### ❌ Ignoring no-results signals
```
// First search: no results
// Bad: "I couldn't find anything"
// Good: "Let me try a broader search..." then actually try
```

