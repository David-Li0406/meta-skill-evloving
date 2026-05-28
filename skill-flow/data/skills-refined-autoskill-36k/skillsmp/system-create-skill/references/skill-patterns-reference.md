# Skill Patterns Reference

## The 8-Category Routing Pattern

**For comprehensive activation triggers, cover these categories:**

1. **Core Skill Name (Noun)** - "OSINT", "research", "skill name"
2. **Action Verbs** - "do [skill]", "run [skill]", "perform [skill]", "execute [skill]"
3. **Modifiers** - "basic [skill]", "quick [skill]", "comprehensive [skill]", "deep [skill]"
4. **Prepositions** - "[skill] on [target]", "[skill] for [target]", "[skill] about [target]"
5. **Synonyms** - Industry jargon, casual vs formal phrasings
6. **Use Case Oriented** - Why would someone use this? What problem does it solve?
7. **Result-Oriented** - "find [thing]", "discover [thing]", "get [information]"
8. **Tool/Method Specific** - Specific tools or techniques within the skill

**Example from security-OSINT skill:**
```markdown
## When to Activate This Skill

### Direct OSINT Requests (Categories 1-4)
- "do OSINT on [target]" or "do some OSINT"
- "run OSINT", "perform OSINT", "conduct OSINT"
- "basic OSINT", "quick OSINT", "comprehensive OSINT"
- "OSINT [target]", "OSINT on [target]", "OSINT for [target]"

### Investigation & Research (Categories 5-7)
- "investigate [person/company]", "research [target]"
- "background check", "due diligence", "find information"
- "who is [person]", "what can you find about [target]"
```

---

## Routing Patterns Reference

### Pattern 1: Semantic Routing
**Use when:** Distinct capabilities map to different user intents

```markdown
**When user requests [specific intent]:**
Examples: "phrase 1", "phrase 2", "phrase 3"
→ **READ:** ${PAI_DIR}/skills/skill-name/workflows/workflow1.md
→ **EXECUTE:** Brief description
```

### Pattern 2: State-Based Routing
**Use when:** Routing depends on current task state or phase

```markdown
### Phase 1: [State Name]
**Current State:** No spec exists
**Use:** workflow1.md to create spec
```

### Pattern 3: Agent-Delegated Routing
**Use when:** Complex context requires agent decision

```markdown
## Available Capabilities

### Category 1
- workflow1.md - Description of capability
- workflow2.md - Description of capability
```

### Pattern 4: Cross-Skill Delegation
**Use when:** Another skill has specialized methodology

```markdown
**CRITICAL: Check if request should be delegated to specialized skills FIRST**

**When user requests [use case needing delegation]:**
Examples: "phrase 1", "phrase 2"
→ **INVOKE SKILL:** specialized-skill-name
→ **REASON:** Why delegation is required
```

---

## Common Anti-Patterns to Avoid

### Missing Workflow Routing Section
**Problem:** Workflows never get invoked
**Solution:** Add "Workflow Routing (SYSTEM PROMPT)" section FIRST

### Workflows Not Explicitly Routed
**Problem:** Orphaned workflow files that are never used
**Solution:** Route EVERY workflow with examples and file paths

### Files Not Linked from Main Body
**Problem:** Files are invisible and undiscoverable
**Solution:** Reference every .md file in appropriate section

### Vague Activation Triggers
**Problem:** "Any security testing request" - too broad
**Solution:** Use 8-category pattern with specific examples

### Wrong Section Order
**Problem:** Workflow routing buried in middle of file
**Solution:** Workflow Routing section immediately after YAML

### Duplication of CORE Context
**Problem:** Skill repeats information already in CORE
**Solution:** Reference CORE docs, don't duplicate

### No Examples
**Problem:** Users don't understand when to use skill
**Solution:** Provide clear example requests and outcomes
