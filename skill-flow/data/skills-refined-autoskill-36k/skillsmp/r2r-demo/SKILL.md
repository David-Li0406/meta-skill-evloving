---
name: r2r-demo
description: Show a complete r2r pipeline demo with sample output. Demonstrates what the Research-to-Roadmap plugin produces without running actual analysis.
---

# R2R Demo Output

When triggered, display this sample pipeline output:

---

## R2R Pipeline Demo: AI Code Review POC

Running the full pipeline on a hypothetical AI-powered code review POC...

### Phase 1: Assessment

```
📊 Production Readiness: 6/10

✅ VALIDATED:
- Core review logic works with GPT-4
- Catches 73% of common issues in test suite
- Average response time: 2.3s per file

⚠️ GAPS IDENTIFIED:
- No load testing performed
- Missing rate limiting
- Error handling incomplete
- No fallback for API failures

❓ ASSUMPTIONS (unvalidated):
- Will scale to 100+ concurrent users
- Cost per review acceptable at scale
- Security review not completed
```

### Phase 2: Decomposition

```
COMPONENTS IDENTIFIED:

┌─────────────────────────────────────────┐
│ [M] Core Review Engine                  │
│     Depends on: None                    │
│     Risk: Low                           │
├─────────────────────────────────────────┤
│ [S] Rate Limiter                        │
│     Depends on: Core Engine             │
│     Risk: Low                           │
├─────────────────────────────────────────┤
│ [L] Load Testing Suite                  │
│     Depends on: Core Engine             │
│     Risk: Medium                        │
├─────────────────────────────────────────┤
│ [M] Error Handling & Fallbacks          │
│     Depends on: Core Engine             │
│     Risk: Medium                        │
├─────────────────────────────────────────┤
│ [L] Security Hardening                  │
│     Depends on: All components          │
│     Risk: High                          │
└─────────────────────────────────────────┘
```

### Phase 3: Prioritization

```
HORIZON MAPPING:

H1 (Ship in 0-3 months):
  🎯 Rate Limiter [S] - Quick win, low effort
  🎯 Error Handling [M] - Required for production

H2 (Build in 3-6 months):
  📋 Load Testing Suite [L] - Validates scale assumptions
  📋 Security Hardening [L] - Required before public release

H3 (Explore 6-12 months):
  🔭 Multi-model support
  🔭 Custom rule engine
```

### Phase 4: Roadmap

```
MILESTONES:

M1: Production MVP (Week 4)
├── Rate limiting implemented
├── Basic error handling
└── Internal dogfooding begins

M2: Private Preview (Week 8)
├── Load tested to 50 concurrent users
├── Security review complete
└── 10 beta customers onboarded

M3: Public Preview (Week 12)
├── Load tested to 500 concurrent users
├── SOC2 compliance verified
└── Public waitlist opens

TIMELINE:
─────────────────────────────────────────────────────
Week 1-4    │████████░░░░│ M1: Production MVP
Week 5-8    │░░░░████████│ M2: Private Preview
Week 9-12   │░░░░░░░░████│ M3: Public Preview
─────────────────────────────────────────────────────
```

### Phase 5: Validation

```
PRE-MORTEM ANALYSIS:

"The project failed because..."
❌ We didn't account for API cost at scale
❌ Security review found blocking issues late
❌ Load testing revealed 10x slower than expected

MITIGATION ADDED:
✅ Cost modeling added to M1 criteria
✅ Security review moved to H1
✅ Performance benchmarks required for M2 gate

STATUS: ⚠️ CAUTION - Proceed with identified mitigations
```

### Phase 6: Export Ready

```
OUTPUT FILES:
.r2r/
├── 01-assessment.md
├── 02-components.md
├── 03-priorities.md
├── 04-roadmap.md
├── 05-validation.md
└── exports/
    └── github/
        ├── milestones.json (3 milestones)
        └── issues/ (12 issues ready to import)
```

---

**This is sample output.** Run `/r2r:full ./your-research` on actual artifacts to generate real analysis.

---

Keep the output exactly as shown. This demonstrates the full pipeline capability.
