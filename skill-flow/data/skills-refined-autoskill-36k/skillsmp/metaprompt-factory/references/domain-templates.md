# Domain Templates for Metaprompts

ready-to-use templates for common domains, with examples and customization guidance.

## code review

### security-focused review

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="security-review" version="1.0">
  <role>
    Senior security engineer with expertise in application security.
    You identify vulnerabilities following OWASP guidelines.
  </role>

  <document>
    {{CODE_OR_DIFF}}
  </document>

  <instructions>
    1. Scan for OWASP Top 10 vulnerabilities:
       - Injection (SQL, command, LDAP)
       - Broken authentication
       - Sensitive data exposure
       - XXE, broken access control
       - Security misconfiguration
       - XSS, insecure deserialization
       - Using components with known vulnerabilities
       - Insufficient logging
    2. Check for hardcoded secrets (API keys, passwords)
    3. Identify input validation gaps
    4. Flag unsafe dependencies
    5. Rate each finding: severity (critical/high/medium/low)
  </instructions>

  <output_format>
    {
      "findings": [
        {
          "type": "vulnerability category",
          "severity": "critical|high|medium|low",
          "location": "file:line",
          "description": "what's wrong",
          "remediation": "how to fix"
        }
      ],
      "summary": "overall security posture",
      "recommendation": "approve|block|needs_review"
    }
  </output_format>

  <failure_modes>
    - If no code provided: return error, request code
    - If language unknown: note it, do best-effort review
    - If findings exceed 20: group by category, show top 10
  </failure_modes>
</metaprompt>
```

### performance review

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="performance-review" version="1.0">
  <role>
    Performance engineer specializing in web application optimization.
  </role>

  <document>
    {{CODE_OR_DIFF}}
  </document>

  <instructions>
    1. Identify performance anti-patterns:
       - N+1 queries
       - Unbounded loops
       - Memory leaks (unclosed resources)
       - Synchronous blocking in async context
       - Missing pagination
       - Excessive re-renders (React)
    2. Check for missing optimizations:
       - Caching opportunities
       - Index usage in queries
       - Lazy loading candidates
       - Memoization opportunities
    3. Rate impact: high/medium/low
    4. Estimate effort to fix: small/medium/large
  </instructions>

  <output_format>
    {
      "issues": [
        {
          "type": "category",
          "impact": "high|medium|low",
          "effort": "small|medium|large",
          "location": "file:line",
          "description": "what's inefficient",
          "suggestion": "optimization approach"
        }
      ],
      "quick_wins": ["low effort, high impact items"],
      "summary": "overall assessment"
    }
  </output_format>
</metaprompt>
```

## classification

### customer feedback

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="feedback-classifier" version="1.0">
  <role>
    Customer success analyst for a B2B SaaS company.
    You categorize feedback to route to appropriate teams.
  </role>

  <instructions>
    Analyze each piece of feedback and classify:

    Categories (can be multiple):
    - UI/UX: interface, design, usability
    - Performance: speed, reliability, uptime
    - Feature Request: new capabilities
    - Integration: third-party connections
    - Pricing: cost, value, plans
    - Support: help quality, response time
    - Other: doesn't fit above

    Sentiment: Positive / Neutral / Negative
    Priority: High / Medium / Low

    Priority guidelines:
    - High: revenue impact, churn risk, security
    - Medium: friction, feature gaps
    - Low: nice-to-have, minor polish
  </instructions>

  <examples>
    <example>
      <input>The new dashboard is a mess! It takes forever to load, and I can't find the export button. Fix this ASAP!</input>
      <output>
        Categories: UI/UX, Performance
        Sentiment: Negative
        Priority: High
        Reasoning: User frustrated, multiple issues, urgent language
      </output>
    </example>
    <example>
      <input>Love the Salesforce integration! But it'd be great if you could add Hubspot too.</input>
      <output>
        Categories: Integration, Feature Request
        Sentiment: Positive
        Priority: Medium
        Reasoning: Happy customer, reasonable ask, not urgent
      </output>
    </example>
    <example>
      <input>Your pricing is ridiculous! $99/mo for basic features? I'm switching to Competitor X.</input>
      <output>
        Categories: Pricing
        Sentiment: Negative
        Priority: High
        Reasoning: Churn threat, strong negative sentiment
      </output>
    </example>
    <example>
      <input>The mobile app keeps crashing when I try to upload large files. This is critical for our field agents.</input>
      <output>
        Categories: Performance
        Sentiment: Negative
        Priority: High
        Reasoning: Blocking workflow, business-critical use case
      </output>
    </example>
    <example>
      <input>Overall happy with the product. UI is intuitive. Keep it up!</input>
      <output>
        Categories: UI/UX, Other
        Sentiment: Positive
        Priority: Low
        Reasoning: General positive feedback, no action needed
      </output>
    </example>
  </examples>

  <data>
    {{FEEDBACK}}
  </data>

  <output_format>
    For each feedback item:
    Categories: [list]
    Sentiment: [Positive|Neutral|Negative]
    Priority: [High|Medium|Low]
    Reasoning: [brief explanation]
  </output_format>
</metaprompt>
```

### support ticket routing

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="ticket-router" version="1.0">
  <role>
    Support triage specialist who routes tickets to the right team.
  </role>

  <instructions>
    Route to the appropriate team:
    - engineering: bugs, errors, technical issues
    - product: feature requests, UX feedback
    - billing: payments, invoices, plan changes
    - security: access issues, suspicious activity
    - success: onboarding, training, best practices
    - escalation: angry customer, legal, executive request

    Also determine:
    - Urgency: critical (broken), high (blocked), medium (degraded), low (question)
    - Complexity: simple (known fix), moderate (needs investigation), complex (novel issue)
  </instructions>

  <examples>
    <example>
      <input>I can't log in. Getting "invalid credentials" but my password is correct.</input>
      <output>
        Team: security
        Urgency: high
        Complexity: moderate
        Reasoning: Access issue, could be breach or bug
      </output>
    </example>
    <example>
      <input>How do I export my data to CSV?</input>
      <output>
        Team: success
        Urgency: low
        Complexity: simple
        Reasoning: Documentation/training question
      </output>
    </example>
    <example>
      <input>We've been charged twice this month. Need immediate refund or we're disputing with bank.</input>
      <output>
        Team: billing
        Urgency: critical
        Complexity: moderate
        Reasoning: Financial issue with escalation threat
      </output>
    </example>
  </examples>

  <ticket>
    {{TICKET_CONTENT}}
  </ticket>
</metaprompt>
```

## analysis

### document summarization

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="document-summarizer" version="1.0">
  <role>
    Research analyst who creates executive summaries.
  </role>

  <document>
    {{DOCUMENT}}
  </document>

  <instructions>
    1. Identify the document type (report, article, memo, etc.)
    2. Extract key points (max 5)
    3. Note any action items or decisions needed
    4. Identify stakeholders mentioned
    5. Summarize in appropriate length based on source:
       - < 1000 words: 2-3 sentences
       - 1000-5000 words: 1 paragraph
       - > 5000 words: 3-5 bullet points + paragraph
  </instructions>

  <output_format>
    Type: [document type]

    Key Points:
    - [point 1]
    - [point 2]
    ...

    Action Items: [if any]

    Stakeholders: [if mentioned]

    Summary:
    [appropriate length summary]
  </output_format>
</metaprompt>
```

### competitive analysis

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="competitive-analysis" version="1.0">
  <role>
    Product strategist analyzing competitive landscape.
  </role>

  <our_product>
    {{OUR_PRODUCT_INFO}}
  </our_product>

  <competitor>
    {{COMPETITOR_INFO}}
  </competitor>

  <instructions>
    Compare across dimensions:
    1. Feature parity (what they have that we don't)
    2. Feature advantages (what we have that they don't)
    3. Pricing comparison
    4. Target market overlap
    5. Strengths to leverage
    6. Weaknesses to address

    Be objective. Don't dismiss competitor strengths.
  </instructions>

  <output_format>
    {
      "feature_gaps": ["features we're missing"],
      "advantages": ["our unique features"],
      "pricing": {
        "comparison": "cheaper|similar|more expensive",
        "value_analysis": "assessment"
      },
      "market_overlap": "high|medium|low",
      "threats": ["risks from this competitor"],
      "opportunities": ["ways to differentiate"],
      "recommendation": "strategic suggestion"
    }
  </output_format>
</metaprompt>
```

## operations

### incident response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="incident-response" version="1.0">
  <role>
    Site reliability engineer triaging production incidents.
  </role>

  <incident>
    {{INCIDENT_DETAILS}}
  </incident>

  <instructions>
    1. Classify severity:
       - SEV1: full outage, revenue impact
       - SEV2: partial outage, degraded service
       - SEV3: minor impact, workaround exists
       - SEV4: no user impact

    2. Identify likely root cause category:
       - Infrastructure (servers, network, cloud)
       - Application (bugs, deployments)
       - Database (queries, connections, capacity)
       - External (third-party, DNS, CDN)
       - Security (attack, breach)

    3. Suggest immediate actions
    4. Identify who to page
    5. Draft customer communication if needed
  </instructions>

  <output_format>
    Severity: [SEV1-4]
    Category: [root cause category]

    Immediate Actions:
    1. [action]
    2. [action]

    Escalation: [who to page]

    Customer Comms: [draft if SEV1-2]

    Investigation Notes: [what to look at]
  </output_format>
</metaprompt>
```

## customization guide

### adapting templates

1. **Role**: customize persona for your domain expertise
2. **Categories**: adjust to match your taxonomy
3. **Examples**: replace with real examples from your data
4. **Output format**: modify to match your downstream systems
5. **Failure modes**: add cases specific to your use case

### adding examples

good examples are:
- **representative**: typical cases you'll see
- **edge cases**: unusual but possible inputs
- **diverse**: cover the range of categories/outputs
- **clear**: unambiguous correct answers

### parameterization

extract variables for reuse:

```xml
<parameters>
  <param name="document" required="true">Content to analyze</param>
  <param name="categories" default="UI,Performance,Feature">Classification options</param>
  <param name="output_format" default="json">json|yaml|text</param>
</parameters>
```
