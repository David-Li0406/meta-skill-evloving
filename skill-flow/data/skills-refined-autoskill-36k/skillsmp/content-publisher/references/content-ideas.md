# Content Ideas Generator

## Automated Content Sources

### 1. Ralph Completions
When Ralph finishes a PRD feature, auto-generate:

**Template:**
```
We just shipped: [Feature Title]

[Brief description of what it does]

Why it matters:
• [Impact point 1]
• [Impact point 2]
• [Impact point 3]

#BuildingDifferently #TechForJustice
```

**Query:** Check `ralph/progress.txt` for recent entries

### 2. Sprint Milestones
Weekly sprint completion summaries:

**Template:**
```
Sprint [N] Complete

[X] issues across [Projects]

Highlights:
• [Key achievement 1]
• [Key achievement 2]

Velocity trending: [up/stable/down]

#BuildingInPublic
```

**Query:** Notion Sprint Tracking database

### 3. Deployment Events
When projects deploy to production:

**Template:**
```
Just deployed: [Project] v[Version]

What's new:
• [Change 1]
• [Change 2]

[Link to changelog or demo]

#ShippingCode #RegenerativeInnovation
```

**Query:** Check deployment logs, git tags

### 4. DORA Metrics
Quarterly engineering health updates:

**Template:**
```
Engineering health check:

Deploy frequency: [X/week]
Change failure rate: [X%]
Mean time to recovery: [Xh]

Performance class: [Elite/High/Medium/Low]

We're building sustainably.

#DevOps #EngineeringExcellence
```

**Query:** Momentum Dashboard metrics

---

## Manual Content Themes

### Weekly Content Calendar

| Day | Theme | Example |
|-----|-------|---------|
| Monday | Technical insight | Architecture decisions, code patterns |
| Tuesday | Community story | Partner highlights, volunteer spotlights |
| Wednesday | Project update | Feature announcements, milestone progress |
| Thursday | Industry reflection | Justice tech trends, regenerative innovation |
| Friday | Behind the scenes | Team culture, process improvements |

### Recurring Content Series

#### "Building Differently" Series
Monthly deep-dives on ACT's approach:
- How we do sprint planning
- Why we chose [technology]
- Our approach to Indigenous data sovereignty
- Building AI that respects community

#### "Ecosystem Connections" Series
Cross-project synergy stories:
- How JusticeHub and Empathy Ledger work together
- The data flow across 7 projects
- Shared infrastructure patterns

#### "Regenerative Tech" Series
Broader industry thought leadership:
- OCAP principles in software
- Designing for obsolescence
- Community ownership models

---

## Content Mining Queries

### Recent Git Activity
```bash
# Find significant commits across all repos
git log --since="7 days ago" --oneline --all | head -20
```

### Notion Activity
```javascript
// Query sprint tracking for completed items
filter: { property: 'Status', select: { equals: 'Done' } }
```

### Ralph Progress
```bash
# Check recent Ralph completions
tail -50 ralph/progress.txt
```

### Documentation Updates
```bash
# Find recently updated docs
find docs -name "*.md" -mtime -7
```

---

## Brand Voice Reminders

Before publishing, ensure:

**DO:**
- Use farm metaphors (seeds, harvest, cultivating, soil)
- Emphasize community ownership
- Reference "designing for obsolescence"
- Mention Jinibara Country when relevant
- Include 40% profit-sharing commitment

**DON'T:**
- Overclaim ("revolutionary", "world-leading")
- Use extractive/luxury language
- Frame communities as beneficiaries (they're co-owners)
- Corporate jargon
- Imply permanence

---

## Hashtag Library

### Primary Tags
- #RegenerativeInnovation
- #TechForJustice
- #BuildingDifferently
- #CommunityTech

### Technical Tags
- #DevOps
- #SoftwareArchitecture
- #AIEthics
- #MultiAgentSystems

### Community Tags
- #IndigenousLed
- #CulturalSovereignty
- #CommunityOwnership
- #StorytellingMatters

### Campaign Tags
- #JusticeHub
- #EmpathyLedger
- #ACTFarm
- #TheHarvest
