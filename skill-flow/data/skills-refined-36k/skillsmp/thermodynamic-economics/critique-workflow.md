# Critique Tracking Workflow

## Purpose

This document defines the complete workflow for receiving, responding to, and learning from external critiques of the Univrs.io ecosystem. It establishes a systematic process that transforms criticism into improvement.

**Principle**: Every substantive critique deserves engagement, not dismissal.

---

## The Critique Response Pipeline

```
                    CRITIQUE LIFECYCLE

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   RECEIVE    │───▶│   RESPOND    │───▶│    LEARN     │
│              │    │              │    │              │
│ krzy.ai/     │    │ Draft +      │    │ Initiative   │
│ critiques/   │    │ Human Review │    │ Creation     │
└──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    LOG       │    │   PUBLISH    │    │   DELIVER    │
│              │    │              │    │              │
│ Track in     │    │ book.univrs  │    │ learn.univrs │
│ database     │    │ .io          │    │ .io          │
└──────────────┘    └──────────────┘    └──────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ▼
                  ┌──────────────┐
                  │   ENGAGE     │
                  │              │
                  │ Fourth       │
                  │ Transition   │
                  │ Outreach     │
                  └──────────────┘
```

---

## Stage 1: Critique Received

### 1.1 Logging at krzy.ai/critiques/

When a substantive critique is received:

```yaml
# Critique entry schema
critique:
  id: "arnoux-2026"
  source:
    author: "Dr. Louis Arnoux"
    affiliation: "Fourth Transition Institute"
    date: "2026-01-01"
    platform: "book.univrs.io"
    url: "https://book.univrs.io/docs/global-economics-and-geopolitics/alternative-economic-models/thermodynamic#comment"

  summary: |
    The Mycelial Economics framework fails to address fundamental thermodynamic
    constraints. Specifically:
    1. The mycelium metaphor describes heterotrophic distribution, not energy generation
    2. Small Worlds mathematics invoked without actual calculations
    3. Autopoiesis claims lack thermodynamic basis
    4. Risk of making unsubstantiated representations to investors

  severity: "critical"
  category: "thermodynamic_foundations"

  tags:
    - "eroei"
    - "autopoiesis"
    - "small-worlds"
    - "energy"
    - "heterotroph"

  status: "responded"
  response_date: "2026-01-02"
  response_url: "https://book.univrs.io/docs/.../thermodynamic#response"

  learning_initiative:
    id: "thermodynamic-economics-initiative"
    url: "krzy.ai/initiatives/thermodynamic-economics"
```

### 1.2 Classification Criteria

| Severity | Criteria | Response Time |
|----------|----------|---------------|
| **Critical** | Challenges core assumptions; affects investor/user trust | < 7 days |
| **High** | Identifies significant technical or economic gap | < 14 days |
| **Medium** | Suggests improvement to existing features | < 30 days |
| **Low** | Minor feedback or suggestions | < 60 days |

### 1.3 Automatic Logging

The `/critique` skill can automatically log external critiques:

```bash
# When new critique is identified
/critique log --source "book.univrs.io" --author "Dr. Arnoux" --category "thermodynamic"
```

This creates the initial entry at `krzy.ai/critiques/[id]`.

---

## Stage 2: Response Drafted

### 2.1 Initial Response Template

```markdown
# Response to [Critic Name]

## For [Platform]

---

Dear [Name],

Thank you for taking the time to engage so thoughtfully with our work.
Your critique is invaluable—the kind of rigorous feedback that transforms
theoretical speculation into grounded practice.

You're absolutely right on several fundamental points:

**On [Point 1]**: [Acknowledgment and specific commitment]

**On [Point 2]**: [Acknowledgment and specific commitment]

**On [Point 3]**: [Acknowledgment and specific commitment]

[Additional context or clarification if needed]

We are developing a learning curriculum at learn.univrs.io that will
explicitly address these gaps. Our immediate priorities:

1. **[Priority 1]** — [Specific deliverable]
2. **[Priority 2]** — [Specific deliverable]
3. **[Priority 3]** — [Specific deliverable]

We're also connecting with the broader community of researchers working
on these problems. [Specific outreach commitment]

Thank you for the flag. We're taking it seriously.

With gratitude,

**[Name]**
[Organization]

---

*P.S. — We've established a critique response workflow at krzy.ai to track
and address substantive feedback like yours. This exchange will be documented
as a case study in how external review improves our work.*
```

### 2.2 Human Review Process

**Critical**: All responses MUST be reviewed by a human before publication.

Review checklist:
- [ ] Response accurately represents the critique
- [ ] Acknowledgments are genuine, not defensive
- [ ] Commitments are specific and achievable
- [ ] Timeline is realistic
- [ ] Tone is grateful, not dismissive
- [ ] No promises that cannot be kept
- [ ] Contact information for follow-up included

### 2.3 Response Generation with /respond

For critiques that appear on krzy.ai itself:

```bash
# Generate exegesis for critique post
/respond [critique-slug]
```

This creates a PR with inline builder reflections (see `.claude/skills/respond/SKILL.md`).

---

## Stage 3: Learning Initiative Created

### 3.1 Initiative Structure

Each substantive critique generates a learning initiative:

```yaml
# Learning initiative schema
initiative:
  id: "thermodynamic-economics-initiative"
  triggered_by: "arnoux-2026"
  created: "2026-01-02"

  objectives:
    - "Understand and address heterotroph critique"
    - "Implement actual small-worlds mathematics"
    - "Assess autopoietic closure with thermodynamic basis"
    - "Integrate renewable energy sources"

  phases:
    - id: "phase_1"
      name: "Acknowledge & Learn"
      status: "active"
      deliverables:
        - "response-to-dr-arnoux.md"
        - "thermodynamic-economics skill"
        - "Learning curricula"

    - id: "phase_2"
      name: "Integrate Autotrophic Sources"
      status: "planned"
      deliverables:
        - "Energy architecture proposal"
        - "Solar integration specification"

    - id: "phase_3"
      name: "Do the Math"
      status: "planned"
      deliverables:
        - "EROEI Calculator Spirit"
        - "Small World Metrics Spirit"

    - id: "phase_4"
      name: "Autopoietic Closure Analysis"
      status: "active"  # Current phase
      deliverables:
        - "autopoiesis-audit.md"
        - "autopoiesis-roadmap.md"
        - "ecosystem-health-integration.md"

    - id: "phase_5"
      name: "Community Connection"
      status: "planned"
      deliverables:
        - "Fourth Transition engagement"
        - "Open source tools"

  tracking:
    swarm_config: "thermodynamic-economics-swarm.yaml"
    ecosystem_health: "/ecosystem-health"
    progress_url: "krzy.ai/initiatives/thermodynamic-economics"
```

### 3.2 Swarm Configuration

Complex initiatives use claude-flow swarm configuration:

```bash
# Execute initiative with swarm
claude-flow @alpha run thermodynamic-economics-swarm.yaml
```

See `thermodynamic-economics-swarm.yaml` for the complete configuration.

### 3.3 Tracking in /ecosystem-health

The `community_feedback` metric in `/ecosystem-health` tracks:
- Number of critiques received
- Response rate and timing
- Actions taken per critique
- Learning initiatives created

---

## Stage 4: Deliverables Completed

### 4.1 Publication to learn.univrs.io

Deliverables are published to the learning platform:

```
learn.univrs.io/
├── curriculum/
│   ├── thermodynamics/           # Phase 1 deliverable
│   └── small-worlds/             # Phase 1 deliverable
├── docs/
│   ├── foundations/
│   │   └── heterotroph-critique/ # Phase 1 deliverable
│   └── architecture/
│       └── energy-layers/        # Phase 2 deliverable
├── spirits/
│   ├── eroei-calculator/         # Phase 3 deliverable
│   └── small-world-metrics/      # Phase 3 deliverable
├── analysis/
│   ├── autopoiesis-audit/        # Phase 4 deliverable
│   └── univrs-eroei/             # Phase 3 deliverable
└── roadmap/
    └── autopoietic-closure/      # Phase 4 deliverable
```

### 4.2 Deliverable Checklist

Each deliverable must meet quality criteria:

- [ ] Technically accurate
- [ ] References primary sources
- [ ] Includes executable code where applicable
- [ ] Acknowledges limitations
- [ ] Links back to originating critique
- [ ] Reviewed by subject matter expert if available

### 4.3 Version Control

All deliverables are version-controlled:

```bash
# Tag initiative milestone
git tag -a "thermodynamic-economics/phase-4" -m "Complete autopoiesis analysis"
git push origin thermodynamic-economics/phase-4
```

---

## Stage 5: Follow-up Engagement

### 5.1 Fourth Transition Outreach

For the Arnoux critique specifically:

```yaml
outreach:
  target: "Fourth Transition Institute"
  contacts:
    - "Dr. Louis Arnoux"
    - "FTI team"

  channels:
    - "Direct email"
    - "Planet: Critical podcast (if appropriate)"
    - "Biophysical economics network"

  message_points:
    - "Thank you for the original critique"
    - "Summary of work completed"
    - "Invitation to review and provide feedback"
    - "Interest in ongoing collaboration"

  timing:
    initial_outreach: "After Phase 3 completion"
    progress_updates: "Quarterly"
    final_report: "After Phase 5 completion"
```

### 5.2 General Outreach Template

```markdown
Subject: Follow-up on Univrs.io Critique - Progress Report

Dear [Name],

[Time period] ago, you provided valuable feedback on [specific aspect].
We wanted to share our progress in addressing your concerns.

**What We've Done:**
- [Deliverable 1]: [Brief description and link]
- [Deliverable 2]: [Brief description and link]
- [Deliverable 3]: [Brief description and link]

**Key Findings:**
[Summary of what we learned]

**Remaining Gaps:**
[Honest assessment of what's still unaddressed]

We would welcome your review of this work and any additional feedback.
The materials are publicly available at [URL].

Thank you again for pushing us toward thermodynamic honesty.

Best regards,
[Name]
```

### 5.3 Community Engagement Tracking

```yaml
# Track engagement outcomes
engagement:
  critique_id: "arnoux-2026"
  outreach_attempts:
    - date: "2026-04-01"
      channel: "email"
      status: "sent"
      response: "pending"

    - date: "2026-04-15"
      channel: "email"
      status: "replied"
      response: "positive"
      notes: "Agreed to review Phase 3 deliverables"

  collaboration:
    initiated: true
    type: "advisory"
    outcomes:
      - "Review of EROEI calculator methodology"
      - "Introduction to biophysical economics network"
```

---

## Case Study: Dr. Arnoux Critique

### Timeline

```
2026-01-01  Critique received on book.univrs.io
            └── Severity: Critical
            └── Category: Thermodynamic foundations

2026-01-02  Response drafted and published
            └── response-to-dr-arnoux.md
            └── Acknowledgment of all major points

2026-01-02  Learning initiative created
            └── thermodynamic-economics-swarm.yaml
            └── INITIATIVE_SUMMARY.md

2026-01-02  Phase 1 deliverables completed
            └── Skill: thermodynamic-economics
            └── Reference: eroei-database.md
            └── Reference: small-worlds-math.md
            └── Reference: autopoiesis-checklist.md

2026-01-02  Phase 4 deliverables completed (current)
            └── autopoiesis-audit.md
            └── autopoiesis-roadmap.md
            └── ecosystem-health-integration.md
            └── critique-workflow.md (this document)

2026-Q1     Phase 2-3 deliverables (planned)
            └── Energy architecture
            └── EROEI Calculator Spirit
            └── Small World Metrics Spirit

2026-Q2     Phase 5 deliverables (planned)
            └── Fourth Transition engagement
            └── Open source publication
```

### Lessons Learned

1. **Speed of response matters**: Same-day acknowledgment demonstrates seriousness
2. **Specificity over generality**: Concrete deliverables, not vague promises
3. **Honest limitations**: Admitting what cannot be achieved (Level 2 autopoiesis)
4. **Systemic integration**: Embedding in /ecosystem-health ensures ongoing attention
5. **Community connection**: Critique is an invitation to relationship, not conflict

### Metrics

```yaml
arnoux_critique_metrics:
  response_time_hours: 24
  acknowledgment_completeness: 1.0  # All points addressed
  deliverables_created: 12
  phases_completed: 2 of 5
  community_engagement_initiated: pending
  ecosystem_health_integrated: true
```

---

## Workflow Integration with Skills

### /critique Skill

Generates new critiques of Univrs.io releases (internal critical conscience):

```
Monday Morning Ritual:
1. /critique recent          → Generate draft PR
2. Review in GitHub          → Read, sit with discomfort
3. /respond [slug]           → Add exegesis (optional)
4. Merge or revise           → Publish or iterate
5. Align                     → What changes this week?
```

### /respond Skill

Adds builder's exegesis to critique posts:

```
/respond the-progress-machine
→ Creates PR with inline reflections
→ Human reviews and edits
→ Merge publishes exegesis
```

### /ecosystem-health Skill

Tracks critique engagement metrics:

```yaml
community_feedback:
  critiques_received: 1
  critiques_responded: 1
  response_time_days: 1
  actions_taken: 1
  learning_initiatives: 1
```

### /evolve Skill

Triggers skill evolution based on critique outcomes:

```
Critique received → /evolve analyzes patterns
→ Suggests skill improvements
→ Updates ecosystem monitoring
```

---

## Automation Opportunities

### Future: Critique Monitoring Spirit

```dol
// spirit://univrs/critique-monitor
domain CritiqueMonitoring {
  // Watch for new comments on ecosystem sites
  watcher CommentWatcher {
    sources: [
      "book.univrs.io/comments",
      "github.com/univrs/*/issues",
      "twitter.com/mentions/univrs"
    ]

    filters: {
      sentiment: "critical",
      substance: "technical OR economic OR ethical",
      length: "> 100 words"
    }

    on_match: {
      log: "krzy.ai/critiques/inbox",
      notify: "spirit://univrs/kritik-notifier",
      classify: "auto"
    }
  }
}
```

### Future: Response Assistant Spirit

```dol
// spirit://univrs/response-assistant
domain ResponseAssistant {
  function draftResponse(critique: Critique) -> ResponseDraft {
    // Extract key points
    let points = extractCritiquePoints(critique)

    // Match to existing acknowledgments
    let acknowledged = matchToAcknowledgments(points)

    // Identify new gaps
    let newGaps = points.filter(p => !acknowledged.contains(p))

    // Generate draft
    return ResponseDraft {
      acknowledgments: acknowledged,
      new_commitments: newGaps.map(g => generateCommitment(g)),
      requires_human_review: true
    }
  }
}
```

---

## Success Criteria

A critique is successfully processed when:

1. **Logged**: Entry exists at krzy.ai/critiques/[id]
2. **Responded**: Public response published within severity-appropriate timeline
3. **Initiative Created**: Learning initiative with deliverables defined
4. **Deliverables Completed**: All committed deliverables published
5. **Integrated**: Metrics tracked in /ecosystem-health
6. **Engaged**: Follow-up outreach to critic completed
7. **Improved**: Measurable improvement in addressed area

---

## References

1. `.claude/skills/critique/SKILL.md` - Internal critique generation
2. `.claude/skills/respond/SKILL.md` - Exegesis workflow
3. `response-to-dr-arnoux.md` - Case study response
4. `thermodynamic-economics-swarm.yaml` - Initiative configuration
5. `ecosystem-health-integration.md` - Metrics integration

---

*Workflow Date: 2026-01-02*
*Version: 1.0.0*
*Status: Active*
*Tracking: krzy.ai/workflows/critique-response*
