---
name: technical-review
description: "Fact-check and verify technical accuracy of blog articles. Code examples, links, claims, dates. Use at TECHNICAL stage of blog pipeline."
---

# Technical Review Skill

**Purpose:** Verify every technical claim before publication.

---

## When to Use

At the TECHNICAL stage, after VOICE pass, before POLISH.

---

## The Gate Question

> Would you stake your professional reputation on every sentence?

If any sentence makes you hesitate, it needs verification.

---

## Review Categories

### 1. Code Examples

**Verify:**
- [ ] Code actually runs
- [ ] Output matches what's shown
- [ ] No syntax errors
- [ ] Imports/dependencies noted
- [ ] Version-specific behavior documented

**Process:**
```bash
# For each code example:
1. Extract to standalone file
2. Run it
3. Compare output to article
4. Note any environment requirements
```

**Common issues:**
- Code worked when written, now fails (dependency updates)
- Missing context (imports, setup)
- Simplified for readability but now doesn't run

### 2. Links

**Verify:**
- [ ] All links resolve (no 404s)
- [ ] Links go where expected (no redirects to wrong place)
- [ ] External content still says what you're citing

**Process:**
```bash
# Extract all links, check each
curl -I [url]  # Check for 200 OK
```

**Common issues:**
- Link rot (content moved or deleted)
- Paywall appeared
- Content changed since you read it

### 3. Technical Claims

**Verify:**
- [ ] Tool/library does what you say it does
- [ ] Version numbers are correct
- [ ] Performance claims have evidence
- [ ] "Best practice" claims have authoritative source

**Questions to ask:**
- Where did I learn this? Is that source reliable?
- Has this changed since I learned it?
- Am I oversimplifying in a misleading way?

### 4. Dates & Numbers

**Verify:**
- [ ] Event dates are accurate
- [ ] Version numbers are correct
- [ ] Statistics have sources
- [ ] Timelines are consistent within article

**Common issues:**
- Memory is wrong about when something happened
- Mixing up version numbers
- Outdated statistics

### 5. Names & Attribution

**Verify:**
- [ ] Tool/library names spelled correctly
- [ ] People's names spelled correctly
- [ ] Correct attribution for quotes/ideas
- [ ] License compliance for code snippets

---

## Review Output Format

```markdown
## Technical Review: [Article Title]

### Code Examples
| # | Description | Status | Notes |
|---|-------------|--------|-------|
| 1 | [desc] | PASS/FAIL | [issue if any] |

### Links
| Link | Status | Notes |
|------|--------|-------|
| [url] | PASS/FAIL | [issue if any] |

### Claims
| Claim | Verified | Source |
|-------|----------|--------|
| "[claim]" | YES/NO | [source or issue] |

### Dates & Numbers
| Item | Verified | Notes |
|------|----------|-------|
| [date/number] | YES/NO | [correction if needed] |

### Verdict: [PASS / NEEDS FIXES]

### Required Fixes:
1. [Specific fix]
2. [Specific fix]
```

---

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Factually wrong, misleading | Must fix before publish |
| **Major** | Broken code, dead links | Should fix before publish |
| **Minor** | Typo in name, outdated but not wrong | Fix if time permits |

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "I remember this working" | Memory isn't reliable | Run it again now |
| "The link was fine yesterday" | Links break | Check at review time |
| "Everyone knows this" | Assumption may be wrong | Find authoritative source |
| "Close enough" | Erodes trust | Get it exactly right |

---

## Trust Maintenance

Technical accuracy is trust infrastructure. One wrong fact can:
- Undermine the entire article
- Damage credibility for future articles
- Mislead readers who trust you

The standard: **Every technical claim must be verifiable.**

---

*Accuracy is not perfectionism. It's respect for the reader.*
