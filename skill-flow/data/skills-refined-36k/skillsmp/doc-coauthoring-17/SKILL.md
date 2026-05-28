---
name: doc-coauthoring
description: 'Collaborative document creation workflow. Structured approach cho writing proposals, reports, documentation với human-AI collaboration hiệu quả.'
---

# Document Co-authoring Skill

Skill này provide structured workflow cho collaborative document creation giữa human và AI, ensuring high-quality output với efficient iterations.

## Khi Nào Sử Dụng

- Viết technical proposals
- Create project documentation
- Draft reports và presentations
- Write blog posts/articles
- Create user guides
- Develop training materials

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: BRIEF                                             │
│  Human provides context, goals, constraints                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: OUTLINE                                           │
│  AI proposes structure, human refines                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: DRAFT                                             │
│  AI writes sections, human provides feedback                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: REFINE                                            │
│  Iterate on style, tone, details                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 5: FINALIZE                                          │
│  Final review, formatting, polish                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Brief

### Information to Gather

| Category | Questions |
|----------|-----------|
| **Purpose** | What is the document for? |
| **Audience** | Who will read this? |
| **Goals** | What should reader do/think after? |
| **Constraints** | Length, format, deadline? |
| **Tone** | Formal? Casual? Technical? |
| **Examples** | Similar documents to reference? |

### Brief Template
```markdown
## Document Brief

**Document Type**: [proposal/report/guide/article]
**Working Title**: [Title]

### Audience
- Primary: [Who]
- Secondary: [Who else]
- Knowledge level: [Beginner/Intermediate/Expert]

### Purpose & Goals
- Main objective: [What you want to achieve]
- Success criteria: [How will you know it worked]

### Key Messages
1. [Main point 1]
2. [Main point 2]
3. [Main point 3]

### Constraints
- Length: [pages/words]
- Format: [PDF/Web/Slides]
- Deadline: [Date]
- Brand/Style guide: [Link if any]

### Tone & Voice
- Tone: [Formal/Conversational/Technical]
- Perspective: [First person/Third person]
- Examples to emulate: [Links]

### Source Materials
- [Document/Link 1]
- [Document/Link 2]
```

---

## Phase 2: Outline

### Outline Format
```markdown
# [Document Title]

## 1. Introduction
- Hook/opening
- Context
- Thesis/main point
- Preview of structure

## 2. [Section Name]
### 2.1 [Subsection]
- Key point
- Supporting evidence
- Example

### 2.2 [Subsection]
- Key point
- Supporting evidence

## 3. [Section Name]
### 3.1 [Subsection]
...

## 4. Conclusion
- Summary of key points
- Call to action
- Next steps

## Appendix (if needed)
- Supporting data
- References
```

### Review Checklist
- [ ] All key topics covered?
- [ ] Logical flow?
- [ ] Appropriate depth for audience?
- [ ] Meets length constraints?
- [ ] Missing anything critical?

---

## Phase 3: Draft

### Section by Section Approach

1. **Start with easiest section** - Build momentum
2. **Don't edit while drafting** - Get content down first
3. **Mark uncertainties** - [TBD] or [VERIFY] placeholders
4. **Include transitions** - Connect sections

### Draft Review Questions
- [ ] Does this section serve its purpose?
- [ ] Is the information accurate?
- [ ] Is the level of detail appropriate?
- [ ] Does it connect to previous/next section?
- [ ] Any gaps in logic?

### Feedback Format
```markdown
## Feedback on [Section Name]

### What's Working
- [Strength 1]
- [Strength 2]

### Needs Improvement
1. **Issue**: [Description]
   **Suggestion**: [How to fix]

2. **Issue**: [Description]
   **Suggestion**: [How to fix]

### Questions/Clarifications
- [Question about specific point]
- [Need more detail on X]

### Priority Changes
1. [Most important change]
2. [Second priority]
3. [Nice to have]
```

---

## Phase 4: Refine

### Refinement Checklist

#### Content
- [ ] All facts verified
- [ ] Examples relevant and current
- [ ] No repetition
- [ ] Appropriate depth

#### Structure
- [ ] Clear hierarchy
- [ ] Smooth transitions
- [ ] Logical flow
- [ ] Good paragraph breaks

#### Style
- [ ] Consistent tone
- [ ] Active voice preferred
- [ ] Jargon appropriate for audience
- [ ] Varied sentence structure

#### Clarity
- [ ] No ambiguous statements
- [ ] Technical terms explained
- [ ] Acronyms defined
- [ ] Clear antecedents

---

## Phase 5: Finalize

### Final Review Checklist

#### Formatting
- [ ] Consistent headings
- [ ] Proper numbering
- [ ] Tables/figures labeled
- [ ] Page numbers
- [ ] Table of contents (if needed)

#### Polish
- [ ] Spell check
- [ ] Grammar check
- [ ] Punctuation consistent
- [ ] Capitalization consistent

#### Completeness
- [ ] All sections present
- [ ] All [TBD] resolved
- [ ] References complete
- [ ] Appendices included

#### Final Read
- [ ] Read aloud for flow
- [ ] Check for awkward phrasing
- [ ] Verify call to action clear
- [ ] Confirm meets original brief

---

## Document Types

### Technical Proposal
```
1. Executive Summary
2. Problem Statement
3. Proposed Solution
4. Technical Approach
5. Timeline & Milestones
6. Budget
7. Team/Qualifications
8. Risks & Mitigations
9. Appendix
```

### Project Report
```
1. Executive Summary
2. Introduction
3. Methodology
4. Findings
5. Analysis
6. Recommendations
7. Conclusion
8. Appendix
```

### User Guide
```
1. Introduction
2. Getting Started
3. Basic Features
4. Advanced Features
5. Troubleshooting
6. FAQ
7. Glossary
8. Index
```

### Blog Post
```
1. Hook/Opening
2. Problem/Context
3. Solution/Insight
4. Supporting Points
5. Examples/Evidence
6. Conclusion
7. Call to Action
```

---

## Collaboration Tips

### For Humans
1. **Be specific** - "Make it better" không helpful
2. **Explain why** - Context helps AI improve
3. **Prioritize feedback** - Focus on high-impact changes
4. **Show examples** - "Like this document" helps
5. **Iterate small** - One round of changes at a time

### For AI
1. **Ask clarifying questions** - Don't assume
2. **Show structure first** - Outline before writing
3. **Offer options** - "I can do A or B, which prefer?"
4. **Flag uncertainties** - Mark what needs verification
5. **Summarize changes** - Explain what was modified

---

## Revision Tracking

```markdown
## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2024-01-01 | AI | Initial outline |
| 0.2 | 2024-01-02 | Human | Revised structure |
| 0.3 | 2024-01-03 | AI | First draft |
| 0.4 | 2024-01-04 | Human | Feedback incorporated |
| 1.0 | 2024-01-05 | Both | Final version |
```
