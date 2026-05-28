# Verification Procedures

How to fact-check claims and verify assumptions using web search and documentation.

---

## When to Verify

### Always Verify
- Performance claims ("X can handle Y requests/second")
- Security claims ("X is secure by default")
- Scalability claims ("X scales horizontally")
- Compatibility claims ("X works with Y")
- Popularity claims ("Everyone uses X")

### Verify If Uncertain
- Best practice claims ("The standard approach is...")
- Technology comparisons ("X is better than Y")
- Historical claims ("X was designed for...")
- Maintenance claims ("X is actively maintained")

### Trust But Note
- Official documentation (but check date)
- Well-known facts (but verify specifics)
- Team's prior experience (but validate assumptions)

---

## Verification Methods

### 1. Web Search

**Use WebSearch for:**
- Current best practices
- Known issues and limitations
- Real-world performance data
- Production case studies
- Recent security vulnerabilities

**Search Strategy:**
```
Topic: Redis performance

Search 1: "Redis performance benchmarks 2024"
→ Find current benchmark data

Search 2: "Redis performance issues production"
→ Find real-world problems

Search 3: "Redis vs [alternative] performance comparison"
→ Find comparative analysis

Search 4: "Redis scaling challenges"
→ Find limitations and gotchas
```

**Evaluate Results:**
| Source Type | Trust Level | Use For |
|-------------|-------------|---------|
| Official docs | High | Features, API, configuration |
| Engineering blogs (known companies) | Medium-High | Production experience |
| Stack Overflow | Medium | Common issues, solutions |
| Random blog posts | Low | Starting points only |
| Vendor marketing | Very Low | Verify independently |

### 2. Documentation Review

**Check These Sources:**
```
1. CLAUDE.md
   - Existing patterns and decisions
   - Technology stack
   - Known constraints

2. Design Documents
   - Prior decisions and rationale
   - Rejected alternatives
   - Known trade-offs

3. ADRs (Architecture Decision Records)
   - Historical context
   - Decision criteria
   - Expected consequences

4. Code Comments / README
   - Implementation notes
   - Known issues
   - Historical context
```

### 3. Cross-Reference with Skills

**microservices-architect:**
- Does this align with Prime Directives?
- Does this follow established patterns?
- Are operational requirements met?

**optima-service-planner:**
- Does this follow Optima conventions?
- Is the Database Gateway pattern respected?
- Are contracts append-only?

---

## Verification Templates

### Performance Claim Verification

```markdown
## Verification: [Claim]

**Claim:** "[Technology] can handle [metric]"
**Source:** [Where did this come from?]

### Search Queries
1. "[technology] benchmark [year]"
2. "[technology] performance production"
3. "[technology] performance issues"
4. "[technology] vs [alternative] performance"

### Findings

**Official Documentation:**
- [Link] - [Summary]

**Production Case Studies:**
- [Company/Source] - [What they found]

**Known Issues:**
- [Issue] - [Impact]

### Conclusion
- [ ] Verified
- [ ] Partially verified (conditions: ___)
- [ ] Not verified
- [ ] Contradicted

**Notes:**
[Relevant context, conditions, caveats]
```

### Technology Choice Verification

```markdown
## Verification: [Technology]

**Claim:** "[Technology] is good for [use case]"

### Maintenance Status
- Last release: [Date]
- Release frequency: [Pattern]
- Open issues: [Count]
- Response to issues: [Quality]

### Production Usage
- Known users: [List]
- Scale references: [Examples]

### Known Issues
- [Issue 1]
- [Issue 2]

### Alternatives Considered
| Alternative | Trade-off |
|-------------|-----------|
| | |

### Conclusion
- [ ] Appropriate for use case
- [ ] Appropriate with caveats
- [ ] Not appropriate
- [ ] More research needed

**Recommendation:**
[Accept/Reject/Investigate]
```

### Security Claim Verification

```markdown
## Verification: [Security Claim]

**Claim:** "[System] is secure"

### Search Queries
1. "[system] CVE"
2. "[system] security vulnerability [year]"
3. "[system] security best practices"
4. "[system] security audit"

### CVE History
- Recent CVEs: [List]
- Severity distribution: [Analysis]
- Patch response time: [Evaluation]

### Security Practices
- [ ] Security team/process exists
- [ ] Regular security audits
- [ ] Bug bounty program
- [ ] Secure by default configuration

### Known Issues
- [Issue 1] - Severity: [H/M/L]
- [Issue 2] - Severity: [H/M/L]

### Conclusion
- [ ] Security claim verified
- [ ] Partially verified (requires: ___)
- [ ] Not verified
- [ ] Security concerns identified

**Required Mitigations:**
1. [Mitigation]
2. [Mitigation]
```

---

## Red Flags in Verification

### Source Quality Red Flags
| Red Flag | Why It Matters |
|----------|----------------|
| Only vendor sources | Biased toward positive |
| Old information (2+ years) | Technology changes fast |
| No production references | Theoretical only |
| Conflicting information | Need more research |
| "Works for us" without details | May not apply |

### Claim Red Flags
| Red Flag | Example |
|----------|---------|
| Round numbers | "100k requests/second" |
| Superlatives | "The fastest", "The best" |
| Universal claims | "Always", "Never", "Everyone" |
| No conditions | "Works great" (under what conditions?) |
| Vendor benchmarks only | Marketing, not reality |

### Missing Information Red Flags
| Missing | Why It Matters |
|---------|----------------|
| Test conditions | Results may not apply |
| Hardware specs | Can't compare fairly |
| Data size | Performance varies |
| Concurrency level | Different at scale |
| Real workload | Synthetic ≠ production |

---

## Search Query Patterns

### Finding Issues
```
"[technology] problems"
"[technology] issues production"
"[technology] doesn't work"
"[technology] bug"
"[technology] limitations"
"[technology] gotchas"
"[technology] pitfalls"
```

### Finding Alternatives
```
"[technology] alternatives"
"[technology] vs"
"better than [technology]"
"instead of [technology]"
"[technology] replacement"
```

### Finding Production Experience
```
"[technology] production"
"[technology] at scale"
"[technology] case study"
"using [technology] in production"
"[company] [technology]"
```

### Finding Best Practices
```
"[technology] best practices [year]"
"[technology] recommended configuration"
"[technology] security hardening"
"[technology] performance tuning"
```

### Finding Recent Information
```
"[technology] [year]"
"[technology] latest"
"[technology] news"
"[technology] update"
"[technology] roadmap"
```

---

## Verification Checklist

Before accepting a claim, verify:

### Source Quality
- [ ] Source is authoritative
- [ ] Information is current (<2 years)
- [ ] Multiple sources agree
- [ ] No obvious bias

### Applicability
- [ ] Conditions match our use case
- [ ] Scale is comparable
- [ ] Technology versions align
- [ ] Environment is similar

### Completeness
- [ ] Searched for contrary evidence
- [ ] Found real-world examples
- [ ] Identified limitations
- [ ] Documented assumptions

### Documentation
- [ ] Findings documented
- [ ] Sources linked
- [ ] Caveats noted
- [ ] Decision recorded

---

## Quick Verification Protocol

For time-sensitive decisions:

### 5-Minute Verification
1. One search for official documentation
2. One search for known issues
3. Check CLAUDE.md for prior decisions
4. Note as "partially verified" with caveats

### 15-Minute Verification
1. Official documentation review
2. Search for production case studies
3. Search for known issues
4. Check against existing skills/patterns
5. Document findings and confidence level

### Full Verification
1. Complete search strategy (4+ queries)
2. Multiple source types
3. Cross-reference with documentation
4. Cross-reference with skills
5. Document with templates
6. Explicit recommendation

> Rule: Verification depth should match decision impact and reversibility.
