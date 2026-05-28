---
name: faion-ux-ui-designer
user-invocable: false
description: "UX/UI Designer role: 10 Usability Heuristics, UX research methods, usability testing, persona development, journey mapping, wireframing, prototyping, design systems, accessibility, WCAG 2.2, EAA compliance. 75 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# UX/UI Designer Domain Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates UX (User Experience) research, design, and evaluation. This domain skill provides comprehensive UX methodology based on Nielsen Norman Group research and industry best practices.

**Philosophy:** "Design is not just what it looks like. Design is how it works." — Steve Jobs

---

## 3-Layer Architecture

```
Layer 1: Domain Skills (this) → orchestrators
    ↓ call
Layer 2: Agents → executors
    ↓ use
Layer 3: Technical Skills → tools
```

## Agents

| Agent | Purpose | Modes |
|-------|---------|-------|
| **faion-ux-researcher-agent** | User interviews, surveys, research synthesis | 12 research methodologies |
| **faion-usability-agent** | Usability testing, heuristic evaluation | 10 heuristics + 10 evaluation methods |

---

## Capabilities Overview

| Area | Methodologies | Key Topics |
|------|---------------|------------|
| Usability Heuristics | 10 | Nielsen's 10 principles |
| UX Research | 12 | Interviews, surveys, testing, personas |
| UX Design | 9 | Wireframing, prototyping, IA |
| Accessibility | 8 | WCAG 2.2, EAA, assistive tech |
| AI Design Tools | 6 | Figma AI, Firefly, generative UI |
| Design Systems | 8 | Tokens, W3C standard, cross-platform |
| Voice UI | 10 | VUI principles, LLM integration |
| Spatial Computing | 11 | AR/VR/MR, enterprise XR |

**Total:** 75 methodologies

---

## Decision Trees

### Main Decision Tree: What UX task?

```
START: What is your UX/UI task?
    │
    ├─→ [Understand Users] → Research Decision Tree
    │
    ├─→ [Evaluate Existing Design] → Evaluation Decision Tree
    │
    ├─→ [Create New Design] → Design Decision Tree
    │
    ├─→ [Ensure Accessibility] → Accessibility Decision Tree
    │
    ├─→ [Voice/Conversational] → Voice UI Decision Tree
    │
    ├─→ [AR/VR/XR] → Spatial Computing Decision Tree
    │
    └─→ [Design System] → Design Systems Decision Tree
```

---

### Research Decision Tree

```
What do you need to learn?
    │
    ├─→ [Deep understanding of users]
    │       │
    │       ├─→ Early discovery? → user-interviews, contextual-inquiry
    │       ├─→ Over time? → diary-studies
    │       └─→ Team alignment? → empathy-mapping, personas
    │
    ├─→ [Quantitative data at scale]
    │       │
    │       └─→ surveys (NPS, CSAT, SUS)
    │
    ├─→ [Information Architecture]
    │       │
    │       ├─→ How users categorize? → card-sorting
    │       └─→ Can users find content? → tree-testing
    │
    ├─→ [User journey understanding]
    │       │
    │       └─→ journey-mapping
    │
    ├─→ [Compare design options]
    │       │
    │       └─→ ab-testing
    │
    └─→ [Competitive landscape]
            │
            └─→ competitive-analysis
```

**Research Methods Quick Reference:**

| Need | Method | File |
|------|--------|------|
| Understand motivations | User Interviews | [user-interviews](user-interviews.md) |
| Observe real behavior | Contextual Inquiry | [contextual-inquiry](contextual-inquiry.md) |
| Quantitative feedback | Surveys | [surveys](surveys.md) |
| Test with real users | Usability Testing | [usability-testing](usability-testing.md) |
| Validate IA structure | Tree Testing | [tree-testing](tree-testing.md) |
| Create IA from scratch | Card Sorting | [card-sorting](card-sorting.md) |
| Long-term behavior | Diary Studies | [diary-studies](diary-studies.md) |
| Team empathy | Empathy Mapping | [journey-mapping](journey-mapping.md) |
| Target users | Personas | [personas](personas.md) |
| End-to-end experience | Journey Mapping | [journey-mapping](journey-mapping.md) |
| Data-driven decisions | A/B Testing | [ab-testing](ab-testing.md) |
| Market landscape | Competitive Analysis | [competitive-analysis](competitive-analysis.md) |

---

### Evaluation Decision Tree

```
What needs evaluation?
    │
    ├─→ [Expert review (no users)]
    │       │
    │       ├─→ Against principles? → heuristic-evaluation (10 heuristics)
    │       ├─→ Learnability focus? → cognitive-walkthrough
    │       └─→ Team feedback? → design-critique
    │
    ├─→ [Test with users]
    │       │
    │       ├─→ Complex flows? → usability-testing (moderated)
    │       ├─→ Simple tasks at scale? → usability-testing (unmoderated)
    │       └─→ Measure satisfaction? → surveys (SUS)
    │
    └─→ [Content review]
            │
            └─→ content-audit
```

**10 Usability Heuristics Quick Reference:**

| # | Heuristic | When Violated | File |
|---|-----------|---------------|------|
| 1 | Visibility of System Status | No loading states, no feedback | [visibility-of-system-status](visibility-of-system-status.md) |
| 2 | Match Between System and Real World | Technical jargon, unfamiliar icons | [match-real-world](match-real-world.md) |
| 3 | User Control and Freedom | No undo, no cancel, trapped in flows | [user-control-freedom](user-control-freedom.md) |
| 4 | Consistency and Standards | Different words for same thing | [consistency-standards](consistency-standards.md) |
| 5 | Error Prevention | Users make frequent mistakes | [error-prevention](error-prevention.md) |
| 6 | Recognition Rather Than Recall | Users must remember info | [recognition-over-recall](recognition-over-recall.md) |
| 7 | Flexibility and Efficiency | No shortcuts for experts | [flexibility-efficiency](flexibility-efficiency.md) |
| 8 | Aesthetic and Minimalist Design | Cluttered, too much info | [aesthetic-minimalist](aesthetic-minimalist.md) |
| 9 | Help Users Recover from Errors | Cryptic error messages | [error-recovery](error-recovery.md) |
| 10 | Help and Documentation | No help, hard to find | [help-documentation](help-documentation.md) |

---

### Design Decision Tree

```
What design artifact needed?
    │
    ├─→ [Structure content]
    │       │
    │       └─→ information-architecture
    │
    ├─→ [Explore layouts]
    │       │
    │       ├─→ Low fidelity? → wireframing (paper, Balsamiq)
    │       └─→ High fidelity? → wireframing (Figma)
    │
    ├─→ [Test interactions]
    │       │
    │       └─→ prototyping
    │
    ├─→ [Mobile-specific]
    │       │
    │       └─→ mobile-ux
    │
    ├─→ [Interface text]
    │       │
    │       └─→ ux-writing (microcopy)
    │
    └─→ [Onboarding flow]
            │
            └─→ onboarding-design
```

**Design Methods Quick Reference:**

| Need | Method | File |
|------|--------|------|
| Organize content | Information Architecture | [information-architecture](information-architecture.md) |
| Layout exploration | Wireframing | [wireframing](wireframing.md) |
| Test interactions | Prototyping | [prototyping](prototyping.md) |
| Touch interfaces | Mobile UX | [mobile-ux](mobile-ux.md) |
| Focus groups | Focus Groups | [focus-groups](focus-groups.md) |

---

### Accessibility Decision Tree

```
What accessibility need?
    │
    ├─→ [Compliance requirements]
    │       │
    │       ├─→ WCAG 2.2 audit? → wcag-22-compliance
    │       ├─→ US government (ADA)? → ada-title-ii-compliance-2026
    │       └─→ EU/EAA compliance? → regulatory-compliance-2026
    │
    ├─→ [Design phase]
    │       │
    │       └─→ accessibility-first-design
    │
    ├─→ [Testing]
    │       │
    │       ├─→ Automated? → ai-accessibility-automation-2026
    │       └─→ Manual/assistive tech? → testing-with-assistive-technology
    │
    ├─→ [Cognitive accessibility]
    │       │
    │       └─→ cognitive-inclusion-design
    │
    └─→ [AI-assisted]
            │
            └─→ ai-assisted-accessibility
```

**Accessibility Quick Reference:**

| Need | File |
|------|------|
| WCAG 2.2 compliance | [wcag-22-compliance](wcag-22-compliance.md) |
| Design-phase accessibility | [accessibility-first-design](accessibility-first-design.md) |
| Regulatory requirements | [regulatory-compliance-2026](regulatory-compliance-2026.md) |
| Assistive tech testing | [testing-with-assistive-technology](testing-with-assistive-technology.md) |
| AI automation | [ai-accessibility-automation-2026](ai-accessibility-automation-2026.md) |
| Cognitive inclusion | [cognitive-inclusion-design](cognitive-inclusion-design.md) |
| ADA Title II (US 2026) | [ada-title-ii-compliance-2026](ada-title-ii-compliance-2026.md) |
| AI-assisted tools | [ai-assisted-accessibility](ai-assisted-accessibility.md) |

---

### Voice UI Decision Tree

```
What voice/conversational need?
    │
    ├─→ [Getting started]
    │       │
    │       ├─→ Market context? → vui-market-context
    │       └─→ Core principles? → core-vui-design-principles
    │
    ├─→ [Conversation design]
    │       │
    │       └─→ vui-conversation-design
    │
    ├─→ [Error handling]
    │       │
    │       └─→ error-handling-in-vui
    │
    ├─→ [Multimodal (voice + visual)]
    │       │
    │       └─→ multimodal-vui-design
    │
    ├─→ [Accessibility]
    │       │
    │       └─→ vui-accessibility-inclusivity
    │
    ├─→ [Privacy/security]
    │       │
    │       └─→ vui-privacy-security
    │
    ├─→ [IoT integration]
    │       │
    │       └─→ vui-iot-integration
    │
    ├─→ [LLM-powered]
    │       │
    │       └─→ llm-powered-conversational-ai
    │
    └─→ [Testing]
            │
            └─→ vui-testing-best-practices
```

**Voice UI Quick Reference:**

| Need | File |
|------|------|
| Market overview | [vui-market-context](vui-market-context.md) |
| Core principles | [core-vui-design-principles](core-vui-design-principles.md) |
| Conversation design | [vui-conversation-design](vui-conversation-design.md) |
| Error handling | [error-handling-in-vui](error-handling-in-vui.md) |
| Voice + visual | [multimodal-vui-design](multimodal-vui-design.md) |
| VUI accessibility | [vui-accessibility-inclusivity](vui-accessibility-inclusivity.md) |
| Privacy/security | [vui-privacy-security](vui-privacy-security.md) |
| Smart home/IoT | [vui-iot-integration](vui-iot-integration.md) |
| LLM-powered AI | [llm-powered-conversational-ai](llm-powered-conversational-ai.md) |
| Testing VUI | [vui-testing-best-practices](vui-testing-best-practices.md) |

---

### Spatial Computing Decision Tree

```
What AR/VR/XR need?
    │
    ├─→ [Getting started]
    │       │
    │       ├─→ Overview? → spatial-computing-overview
    │       └─→ UX fundamentals? → spatial-ux-fundamentals
    │
    ├─→ [Interaction design]
    │       │
    │       └─→ spatial-interaction-patterns
    │
    ├─→ [UI patterns]
    │       │
    │       └─→ spatial-ui-patterns
    │
    ├─→ [Platform-specific]
    │       │
    │       ├─→ AR design? → ar-design-patterns
    │       └─→ VR design? → vr-design-patterns
    │
    ├─→ [Immersion]
    │       │
    │       └─→ immersive-design-principles
    │
    ├─→ [Enterprise]
    │       │
    │       └─→ enterprise-xr-applications
    │
    ├─→ [AI integration]
    │       │
    │       └─→ ai-spatial-computing
    │
    ├─→ [Accessibility]
    │       │
    │       └─→ spatial-accessibility
    │
    └─→ [Tools]
            │
            └─→ spatial-design-tools
```

**Spatial Computing Quick Reference:**

| Need | File |
|------|------|
| Platform overview | [spatial-computing-overview](spatial-computing-overview.md) |
| UX fundamentals | [spatial-ux-fundamentals](spatial-ux-fundamentals.md) |
| Interaction patterns | [spatial-interaction-patterns](spatial-interaction-patterns.md) |
| UI patterns | [spatial-ui-patterns](spatial-ui-patterns.md) |
| Immersive design | [immersive-design-principles](immersive-design-principles.md) |
| AR patterns | [ar-design-patterns](ar-design-patterns.md) |
| VR patterns | [vr-design-patterns](vr-design-patterns.md) |
| Enterprise XR | [enterprise-xr-applications](enterprise-xr-applications.md) |
| AI + spatial | [ai-spatial-computing](ai-spatial-computing.md) |
| XR accessibility | [spatial-accessibility](spatial-accessibility.md) |
| Design tools | [spatial-design-tools](spatial-design-tools.md) |

---

### Design Systems Decision Tree

```
What design system need?
    │
    ├─→ [Token fundamentals]
    │       │
    │       └─→ design-tokens-fundamentals
    │
    ├─→ [Token organization]
    │       │
    │       └─→ token-organization
    │
    ├─→ [Theming/modes]
    │       │
    │       └─→ semantic-tokens-and-modes
    │
    ├─→ [Standards]
    │       │
    │       └─→ w3c-design-tokens-standard
    │
    ├─→ [AI enhancement]
    │       │
    │       └─→ ai-enhanced-design-systems
    │
    ├─→ [Success factors]
    │       │
    │       └─→ design-system-success-factors
    │
    ├─→ [Tailwind integration]
    │       │
    │       └─→ tailwind-design-tokens
    │
    └─→ [Cross-platform]
            │
            └─→ cross-platform-token-distribution
```

**Design Systems Quick Reference:**

| Need | File |
|------|------|
| Token basics | [design-tokens-fundamentals](design-tokens-fundamentals.md) |
| Token structure | [token-organization](token-organization.md) |
| Theming/dark mode | [semantic-tokens-and-modes](semantic-tokens-and-modes.md) |
| W3C standard | [w3c-design-tokens-standard](w3c-design-tokens-standard.md) |
| AI-enhanced | [ai-enhanced-design-systems](ai-enhanced-design-systems.md) |
| Success factors | [design-system-success-factors](design-system-success-factors.md) |
| Tailwind | [tailwind-design-tokens](tailwind-design-tokens.md) |
| Cross-platform | [cross-platform-token-distribution](cross-platform-token-distribution.md) |

---

### AI Design Tools Decision Tree

```
What AI tool need?
    │
    ├─→ [Figma ecosystem]
    │       │
    │       └─→ figma-ai-ecosystem
    │
    ├─→ [Adobe tools]
    │       │
    │       └─→ adobe-firefly-integration
    │
    ├─→ [Generative UI]
    │       │
    │       └─→ generative-ui-design
    │
    ├─→ [Plugin ecosystem]
    │       │
    │       └─→ ai-plugin-ecosystem
    │
    ├─→ [Assistant patterns]
    │       │
    │       └─→ ai-design-assistant-patterns
    │
    └─→ [Tool comparison]
            │
            └─→ figma-vs-adobe-strategy-2026
```

**AI Tools Quick Reference:**

| Need | File |
|------|------|
| Figma AI features | [figma-ai-ecosystem](figma-ai-ecosystem.md) |
| Adobe Firefly | [adobe-firefly-integration](adobe-firefly-integration.md) |
| Generative UI (v0, Galileo) | [generative-ui-design](generative-ui-design.md) |
| AI plugins | [ai-plugin-ecosystem](ai-plugin-ecosystem.md) |
| Assistant patterns | [ai-design-assistant-patterns](ai-design-assistant-patterns.md) |
| Figma vs Adobe | [figma-vs-adobe-strategy-2026](figma-vs-adobe-strategy-2026.md) |

---

## Complete Methodology Index

### Nielsen's 10 Usability Heuristics

| # | Name | File |
|---|------|------|
| 1 | Visibility of System Status | [visibility-of-system-status](visibility-of-system-status.md) |
| 2 | Match Between System and Real World | [match-real-world](match-real-world.md) |
| 3 | User Control and Freedom | [user-control-freedom](user-control-freedom.md) |
| 4 | Consistency and Standards | [consistency-standards](consistency-standards.md) |
| 5 | Error Prevention | [error-prevention](error-prevention.md) |
| 6 | Recognition Rather Than Recall | [recognition-over-recall](recognition-over-recall.md) |
| 7 | Flexibility and Efficiency of Use | [flexibility-efficiency](flexibility-efficiency.md) |
| 8 | Aesthetic and Minimalist Design | [aesthetic-minimalist](aesthetic-minimalist.md) |
| 9 | Help Users Recover from Errors | [error-recovery](error-recovery.md) |
| 10 | Help and Documentation | [help-documentation](help-documentation.md) |

### UX Research Methods

| Name | File |
|------|------|
| User Interviews | [user-interviews](user-interviews.md) |
| Contextual Inquiry | [contextual-inquiry](contextual-inquiry.md) |
| Surveys | [surveys](surveys.md) |
| Usability Testing | [usability-testing](usability-testing.md) |
| A/B Testing | [ab-testing](ab-testing.md) |
| Card Sorting | [card-sorting](card-sorting.md) |
| Tree Testing | [tree-testing](tree-testing.md) |
| Journey Mapping | [journey-mapping](journey-mapping.md) |
| Personas | [personas](personas.md) |
| Diary Studies | [diary-studies](diary-studies.md) |
| Competitive Analysis | [competitive-analysis](competitive-analysis.md) |
| Focus Groups | [focus-groups](focus-groups.md) |

### Evaluation Methods

| Name | File |
|------|------|
| Heuristic Evaluation | [heuristic-evaluation](heuristic-evaluation.md) |
| Cognitive Walkthrough | [cognitive-walkthrough](cognitive-walkthrough.md) |
| Design Critique | [design-critique](design-critique.md) |
| Content Audit | [content-audit](content-audit.md) |
| Accessibility Evaluation | [accessibility-evaluation](accessibility-evaluation.md) |

### Design Methods

| Name | File |
|------|------|
| Information Architecture | [information-architecture](information-architecture.md) |
| Wireframing | [wireframing](wireframing.md) |
| Prototyping | [prototyping](prototyping.md) |
| Mobile UX | [mobile-ux](mobile-ux.md) |
| Voice UI | [voice-ui](voice-ui.md) |

---

## Sources

- [Nielsen Norman Group](https://www.nngroup.com/) - 10 Usability Heuristics
- [IDEO Design Kit](https://www.designkit.org/) - Human-Centered Design
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/) - Accessibility Guidelines
- [Material Design](https://m3.material.io/) - Google Design System
- [Human Interface Guidelines](https://developer.apple.com/design/) - Apple Design

---

*UX/UI Designer Domain Skill v2.0*
*75 Methodologies | 2 Agents | Decision Trees for Navigation*
