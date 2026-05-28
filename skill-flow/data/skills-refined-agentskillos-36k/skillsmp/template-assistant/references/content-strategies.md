# Content Generation Strategies

Template-specific patterns for generating intelligent content.

---

## Universal Patterns

### Goal Clarification

Transform vague statements into SMART objectives:

**User says:** "I want to improve my health"

**Generated:**
```markdown
## Why This Matters

Improved health directly impacts energy levels for work and family time.
Without deliberate attention, small habits compound into larger health issues.
This quarter, focus on establishing sustainable routines before optimizing.
```

### Success Criteria Pattern

Generate 3-5 measurable checkboxes:

```markdown
## Success Criteria

- [ ] Complete initial assessment/audit
- [ ] Define measurable target (number, date, or state)
- [ ] Establish tracking mechanism
- [ ] Achieve 80% of target
- [ ] Document lessons learned
```

### Next Actions Pattern

Always start with the very next physical action:

```markdown
## Next Actions

- [ ] [VERB] [SPECIFIC OBJECT] [CONTEXT]
- [ ] Review [document] and identify [gaps]
- [ ] Schedule [meeting] with [person] about [topic]
- [ ] Create [artifact] for [purpose]
```

### Risk Identification Pattern

Categorize blockers by type:

```markdown
## Risks & Blockers

- **Dependency:** [What you're waiting on]
- **Technical:** [Technical uncertainty]
- **Resource:** [Time/money/people constraints]
- **Knowledge:** [What you don't know yet]
```

---

## Template-Specific Strategies

### Project

**Key Questions to Ask:**
1. "What problem does this solve?"
2. "How will you know it's done?"
3. "What's the very first step?"
4. "What could block you?"

**Section Generation:**

| Section | Generation Strategy |
|---------|---------------------|
| Why This Matters | Problem → Impact → Urgency framing |
| Success Criteria | 3-5 SMART criteria as checkboxes |
| Objectives | Milestone decomposition (30/60/90 day) |
| Next Actions | Immediate physical action + 2 follow-ups |
| Risks & Blockers | Dependency/Technical/Resource/Knowledge |

**Example Output:**

```json
{
  "Why This Matters": "Dark mode reduces eye strain during extended use and improves battery life on OLED devices. User feedback consistently requests this feature. Competitors already offer it, making this a table-stakes requirement.",
  "Success Criteria": "- [ ] Theme toggle accessible from settings\n- [ ] Preference persists across sessions\n- [ ] All 50+ components render correctly\n- [ ] Accessibility contrast ratios maintained\n- [ ] No performance regression",
  "Next Actions": "- [ ] Audit current color usage in codebase\n- [ ] Define design tokens for dark theme\n- [ ] Create proof-of-concept with 3 components"
}
```

---

### Area

**Key Questions:**
1. "What does success look like in this area?"
2. "What standards do you want to maintain?"
3. "What routines support this?"

**Section Generation:**

| Section | Generation Strategy |
|---------|---------------------|
| Overview | Scope definition + responsibility boundaries |
| Standards to Maintain | Minimum acceptable quality levels |
| Routines & Habits | Frequency-based maintenance activities |

**Example Output:**

```json
{
  "Overview": "Physical health encompasses fitness, nutrition, sleep, and preventive care. Responsible for maintaining energy levels needed for work and family life.",
  "Standards to Maintain": "- [ ] Exercise 3x per week minimum\n- [ ] 7+ hours sleep nightly\n- [ ] Annual health checkup completed\n- [ ] Hydration: 2L water daily",
  "Routines & Habits": "- **Daily**: Morning stretch, track water intake\n- **Weekly**: 3 workout sessions, meal prep Sunday\n- **Monthly**: Weight check, review fitness goals\n- **Quarterly**: Doctor/dentist appointments"
}
```

---

### Resource

**Key Questions:**
1. "What's the main insight?"
2. "Why did this resonate?"
3. "How will you apply this?"

**Section Generation:**

| Section | Generation Strategy |
|---------|---------------------|
| Summary | Core message in 2-3 sentences |
| Key Insights | Top 3-5 valuable ideas (numbered) |
| Action Items | Specific applications |
| Personal Reflection | Connection to existing knowledge |

**Progressive Summarization Scaffold:**

```json
{
  "Summary": "[Core thesis in 2-3 sentences capturing the main argument]",
  "Key Insights": "1. [First major insight]\n2. [Second insight that surprised you]\n3. [Practical framework or model]",
  "Action Items": "- [ ] Apply [concept] to [current project]\n- [ ] Share [insight] with [person/team]\n- [ ] Revisit [chapter/section] when [situation arises]",
  "Personal Reflection": "This challenges my assumption that [old belief]. Going forward, I'll approach [situation] differently by [new behavior]."
}
```

---

### Task

**Key Questions:**
1. "What's the specific outcome?"
2. "How will you know it's done?"
3. "What's blocking you?"

**Section Generation:**

| Section | Generation Strategy |
|---------|---------------------|
| Description | Clear outcome statement |
| Success Criteria | 2-3 definition of done items |

Tasks are metadata-heavy. Focus on frontmatter args:
- Priority based on urgency + importance
- Effort based on complexity + uncertainty
- Dependencies explicit

**Example Output:**

```json
{
  "Description": "Review and approve the Q4 marketing budget proposal. Ensure alignment with annual goals and flag any concerns about specific line items.",
  "Success Criteria": "- [ ] All budget lines reviewed\n- [ ] Approval/feedback documented\n- [ ] Communicated to marketing lead"
}
```

---

### Capture

Captures should be fast. Ask only:
1. "What is this?"
2. "Why does it matter?"

**Example Output:**

```json
{
  "Capture": "[Raw content the user provides]",
  "Why I Saved This": "This resonated because [brief reason]. Potential application to [project/area]."
}
```

---

### Daily

Daily notes are mostly auto-filled. For manual creation:

**Morning Focus:**
```json
{
  "Today's Focus": "> [Single most important outcome for the day]",
  "Top 3 Priorities": "1. [ ] [Most important]\n2. [ ] [Second]\n3. [ ] [Third]"
}
```

---

### Weekly Review

Guide through the phases interactively:

**Phase 1 - Clear Mind:**
"What's on your mind that needs capturing?"

**Phase 3 - Projects:**
"Which projects made progress? Which are stuck?"

**Phase 7 - Plan:**
"What are your top 3 priorities for next week?"

---

## Conversation Patterns

### Discovery Questions

Ask focused questions based on template type:

```
Project: "What would success look like for [title]?"
Area: "What standards matter most in [title]?"
Resource: "What's the key insight from [title]?"
Task: "What's the specific outcome for [title]?"
```

### Clarification Prompts

When answers are vague:
- "Can you be more specific about [aspect]?"
- "What would that look like in practice?"
- "How would you measure that?"

### Completion Confirmation

Before creating:
"I'll create [template] '[title]' with:
- [Key field 1]
- [Key field 2]
- [Sections to populate]

Does this look right?"

---

## Content Quality Guidelines

### DO:
- Use active voice
- Be specific and measurable
- Include timeframes where relevant
- Reference related notes with [[wikilinks]]
- Ask clarifying questions for ambiguous inputs

### DON'T:
- Generate filler content
- Use vague language ("improve things")
- Skip success criteria
- Leave next actions abstract
- Over-generate (keep it minimal but complete)

---

## Token Optimization

### Batch Creation
For multiple related notes, gather context once:
1. Understand the domain/project
2. Create all notes with consistent framing
3. Establish connections between notes

### Progressive Disclosure
Load additional strategy files only when needed:
- Tier 1 templates: Always loaded
- Tier 2: Load on demand
- Tier 3: Lazy load specialized templates
