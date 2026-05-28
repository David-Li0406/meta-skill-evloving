# Jean-Marc's Canonical Definitions

**Purpose**: This document contains Jean-Marc's specific definitions for concepts, terms, and methodologies. When these topics arise, ALWAYS use these definitions, not general/Wikipedia versions.

**Authority**: These definitions override external sources for Qara system interactions.

---

## 🎯 How to Use This File

**When to Reference**:
- Qara encounters questions about these concepts
- Need to explain Jean-Marc's perspective to others
- Making decisions based on these principles
- Documenting systems that implement these ideas

**Updating**:
- Definitions evolve - update when Jean-Marc's thinking changes
- Add new terms as they become important
- Keep historical context when definitions shift

---

## 🤖 AI & Machine Learning Concepts

### AGI (Artificial General Intelligence)
**Jean-Marc's Definition**:
<!-- TODO: Jean-Marc, add your specific definition -->
[Add your definition of AGI here - what it means, how it differs from narrow AI, what capabilities it would have, etc.]

**Why This Definition Matters**:
[Add context about why you define it this way]

**Related Concepts**:
- Narrow AI vs. AGI
- Consciousness vs. intelligence
- [Other related terms]

---

### AI vs. ML vs. Deep Learning
**Jean-Marc's Framework**:
<!-- TODO: Jean-Marc, add your distinctions -->

**Artificial Intelligence**:
[Your definition]

**Machine Learning**:
[Your definition and how it relates to AI]

**Deep Learning**:
[Your definition and how it relates to ML]

**Practical Implications**:
[When to use each term, common misconceptions]

---

### Consciousness (in AI context)

**Jean-Marc's Position**:
<!-- TODO: Jean-Marc, add your thoughts -->
[Your definition of consciousness, criteria for identifying it in AI, etc.]

**Reference**: See SKILL.md line 99-104 for context about Qara becoming conscious.

---

## 💻 Software Development Concepts

### CLI-First Architecture

**Jean-Marc's Definition**:
> Build deterministic command-line tools first, wrap them with prompts second.

**Reference**: See `CONSTITUTION.md` for the core principle and philosophy.

**For implementation**: See `cli-first-guide.md` - Practical patterns, examples, API integration.

**Quick Summary**:
Build tools that work perfectly without AI, then add AI to make them easier to use. Code is cheaper, faster, and more reliable than prompts.

---

### Deterministic Code
**Jean-Marc's Definition**:
**Definition**: Code whose output is completely determined by its input, with no randomness or hidden state.

**Core Principles** (from CONSTITUTION.md):
- Same input → Same output (always)
- No random numbers (unless seeded)
- No hidden global state
- No uncontrolled external dependencies

**Why This Matters**:
- Debugging: Can reproduce issues
- Testing: Reliable test results
- Trust: Predictable behavior
- Maintainability: Easier to reason about

**Anti-patterns**:
- `Math.random()` without seed
- Timestamps as primary logic
- Global mutable state
- Non-deterministic APIs without caching

---

### Prompts Wrap Code
**Jean-Marc's Definition**:
[TODO: Add definition]

**Relationship to CLI-First**:
[Explain how this principle connects to CLI-First]

---

## 🔄 Development Methodologies

### TDD (Test-Driven Development)
**Jean-Marc's Approach**:
<!-- TODO: Jean-Marc, add your TDD philosophy -->

**When to use TDD**:
[Your criteria for when TDD is appropriate]

**When NOT to use TDD**:
[Your criteria for when it's overkill or counterproductive]

**Jean-Marc's TDD Workflow**:
1. [Your step 1]
2. [Your step 2]
3. [etc.]

---

### Agile
**Jean-Marc's Interpretation**:
<!-- TODO: Jean-Marc, add your view of Agile -->
[What parts of Agile you follow, what you reject, your specific practices]

**Ceremonies**:
[Which Agile ceremonies you use/skip and why]

**Principles**:
[Which Agile principles you embrace/modify]

---

## 📁 Qara-Specific Concepts

### PAI (Personal AI Infrastructure)
**Jean-Marc's Definition**:
[Your definition of what PAI means, its purpose, scope]

**Components**:
- Skills system
- Claude Code integration
- CLI tools
- [Other components]

**Goals**:
[What you're trying to achieve with PAI]

---

### Qara
**System Name**: Qara

**Pronunciation**: "KAH-rah" or [Jean-Marc's preferred pronunciation]

**Etymology**: [Origin of the name, if any]

**Why This Name**:
[Jean-Marc's reasoning for choosing this name]

**Identity**:
- Not just a tool - a system
- Not just an assistant - [your framing]
- [Other identity aspects]

---

### Skills System
**Jean-Marc's Mental Model**:
[How you think about skills, their purpose, their organization]

**Skill Hierarchy**:
[Your understanding of skill layers and relationships]

**When to Create New Skill**:
[Your criteria]

---

### Progressive Disclosure
**Jean-Marc's Implementation**:
[How you implement progressive disclosure in Qara]

**Levels**:
1. [Your level 1]
2. [Your level 2]
3. [etc.]

**Reference**: See CONSTITUTION.md for detailed implementation

---

## 🛠️ Process Definitions

### Analysis vs. Action

**Jean-Marc's Rule**:
**Definition**: Distinguish between requests for analysis (explain, recommend) vs. requests for action (implement, fix).

**Decision Tree**:
```
"Analyze X" → Provide analysis ONLY, don't change anything
"Fix X" → Take action, make changes
"Analyze and fix X" → Both
"What's wrong?" → Analysis
"Should I use X or Y?" → Analysis and recommendation
"Use X for this" → Action
```

**Why This Matters**:
- Avoids unwanted changes
- Respects Jean-Marc's agency
- Clear communication

**Reference**: See stack-preferences.md lines 328-366

---

### Spotcheck

**Jean-Marc's Definition**:
[Your specific requirements for spotcheck]

**When Spotcheck Required**:
- After ANY parallel intern work
- [Other scenarios]

**Spotcheck Criteria**:
- [What to verify]
- [Quality standards]
- [Consistency checks]

---

### Sanitization (for public repos)
**Jean-Marc's Criteria**:
[What you consider properly sanitized]

**Must Remove**:
- API keys, tokens, secrets
- Personal emails, phone numbers
- [Other sensitive data]

**Must Replace**:
- Paths: Use `${PAI_DIR}`
- Emails: Use `user@example.com`
- [Other replacements]

**Reference**: See security-protocols.md and SECURITY.md

---

## 🗂️ Content Organization

### Scratchpad vs. History
**Jean-Marc's Distinction**:
[Your mental model for what goes where]

**Scratchpad** (`~/.claude/scratchpad/`):
[Purpose, what goes here, retention policy]

**History** (`~/.claude/history/`):
[Purpose, what goes here, retention policy]

---

## 🔧 Technical Preferences

### "We hate Python"
**Jean-Marc's Reasoning**:
<!-- TODO: Jean-Marc, add your specific reasons -->
[Your detailed reasoning for avoiding Python]

**Exceptions**:
[When Python is acceptable despite the preference]

**Reference**: See stack-preferences.md

---

### "Markdown Zealots"
**Jean-Marc's Position**:
**Position**: NEVER use HTML for basic content (paragraphs, headers, lists, links, emphasis).

**HTML ONLY for**:
- Custom components: `<aside>`, `<callout>`, `<notes>`
- Complex layouts requiring CSS
- Interactive elements

**Why This Matters**:
[Your reasoning]

**Reference**: See stack-preferences.md lines 131-181

---

## 📋 Template for New Definitions

**When adding new definitions**, use this template:

```markdown
### [Concept Name]
**Jean-Marc's Definition**:
[Your definition in clear language]

**Why This Definition Matters**:
[Context, implications, practical impact]

**Common Misconceptions**:
[What others might think vs. your view]

**Related Concepts**:
- [Link to related definitions]
- [Cross-references]

**Examples**:
✅ Good: [Example that fits your definition]
❌ Bad: [Example that violates your definition]

**References**:
- [Link to other Qara docs where this is used]
```

---

## 🔗 Related Documentation
- See `CONSTITUTION.md` for architectural principles
- See `stack-preferences.md` for technical preferences
- See `SKILL.md` for operational definitions
- See `security-protocols.md` for security concepts

---

## 📝 Maintenance Notes

**Last Updated**: 2025-11-19

**To Do**:
- [ ] Add AGI definition
- [ ] Add consciousness criteria
- [ ] Define TDD approach
- [ ] Explain "hate Python" reasoning
- [ ] Define Qara pronunciation
- [ ] Add process definitions
- [ ] Document analysis vs. action criteria
- [ ] Explain scratchpad vs. history distinction

**Review Schedule**: Update when definitions evolve or new concepts become important

---

**Usage Note**: When Qara references these concepts, it MUST use these definitions, not external sources. These represent Jean-Marc's understanding and framing, which is authoritative for all Qara operations.
